"""Composable capsule for plain init-only class generation."""

from __future__ import annotations

import ast
from collections.abc import Callable, Iterable
from dataclasses import dataclass, field
from functools import cache
import textwrap
from typing import Any


class UnspecifiedType:
    """Sentinel for absent field annotations/defaults."""

    __slots__ = ()

    def __repr__(self) -> str:
        return "UNSPECIFIED"


UNSPECIFIED = UnspecifiedType()

INIT_ONLY_METHOD_SHELL = """
def __init__(self, params__astichi_param_hole__):
    astichi_hole(prep)
    astichi_hole(field_init)
    astichi_hole(finalize)
"""

INIT_ONLY_PARAM_RESOURCE = """
def astichi_params(
    field_name__astichi_arg__: astichi_hole(anno) = astichi_hole(default_value),
):
    pass
"""

INIT_ONLY_FIELD_INIT_RESOURCE = """
self.field_name__astichi_arg__ = field_value__astichi_arg__
"""

_FACTORY_ROOT_SRC = """
def make_wrapper_class(class_definition):
    astichi_hole(factory_locals)
    class class_name__astichi_arg__(astichi_ref("_y_wrapped_class")):
        astichi_hole(class_defs)
        astichi_hole(class_methods)
    return class_name__astichi_arg__
"""

_CLASS_DEFINITION_LOCAL_SRC = """
astichi_ref("_y_class_definition")._ = astichi_pass(class_definition, outer_bind=True)
"""

_WRAPPED_CLASS_LOCAL_SRC = """
astichi_ref("_y_wrapped_class")._ = astichi_ref("_y_class_definition").wrapped_class
"""

_CLASS_DEFINITION_ATTR_SRC = """
__yidl_class_definition__ = astichi_ref("_y_class_definition")
"""

_INIT_METHOD_SRC = """
def __init__(self, method_params__astichi_param_hole__):
    astichi_hole(method_body)
"""

_PASS_SRC = """
pass
"""

_ANNO_LOCAL_SRC = """
astichi_ref(external=local_name)._ = astichi_pass(_y_class_definition, outer_bind=True).fields_by_name[astichi_bind_external(field_name)].field_anno
"""

_DEFAULT_LOCAL_SRC = """
astichi_ref(external=local_name)._ = astichi_pass(_y_class_definition, outer_bind=True).fields_by_name[astichi_bind_external(field_name)].default
"""

_REQUIRED_PARAM_SRC = """
def astichi_params(
    *,
    field_name__astichi_arg__: astichi_pass(anno_local, outer_bind=True),
):
    pass
"""

_DEFAULTED_PARAM_SRC = """
def astichi_params(
    *,
    field_name__astichi_arg__: astichi_pass(anno_local, outer_bind=True)=astichi_pass(default_local, outer_bind=True),
):
    pass
"""

_PARAM_ASSIGN_SRC = """
astichi_import(self)
self.astichi_ref(external=target_path)._ = astichi_pass(field_value, outer_bind=True)
"""

_DEFAULT_ASSIGN_SRC = """
astichi_import(self)
self.astichi_ref(external=target_path)._ = astichi_pass(default_local, outer_bind=True)
"""

_FIELD_RESOURCE_SOURCES = {
    "AnnoLocal": _ANNO_LOCAL_SRC,
    "DefaultLocal": _DEFAULT_LOCAL_SRC,
    "RequiredParam": _REQUIRED_PARAM_SRC,
    "DefaultedParam": _DEFAULTED_PARAM_SRC,
    "ParamAssign": _PARAM_ASSIGN_SRC,
    "DefaultAssign": _DEFAULT_ASSIGN_SRC,
}


@dataclass(frozen=True, slots=True)
class ResolvedInitField:
    field_name: str
    field_anno: Any = UNSPECIFIED
    init: bool = True
    default: Any = UNSPECIFIED

    def __post_init__(self) -> None:
        if not isinstance(self.field_name, str):
            raise TypeError(
                f"FieldName must be str, got {type(self.field_name).__name__}"
            )
        if not isinstance(self.init, bool):
            raise TypeError(f"Init must be bool for field {self.field_name!r}")
        if not self.init and self.default is UNSPECIFIED:
            raise ValueError(f"missing initial value for field {self.field_name!r}")


@dataclass(frozen=True, slots=True)
class InitOnlyFieldSpec:
    init: bool = True
    default: Any = UNSPECIFIED


@dataclass(frozen=True, slots=True)
class InitOnlyClassDefinition:
    class_name: str
    wrapped_class: type[Any]
    fields: tuple[ResolvedInitField, ...] = ()
    fields_by_name: dict[str, ResolvedInitField] = field(init=False, repr=False)

    def __post_init__(self) -> None:
        object.__setattr__(
            self,
            "fields_by_name",
            {field.field_name: field for field in self.fields},
        )


def field_spec(*, init: bool = True, default: Any = UNSPECIFIED) -> InitOnlyFieldSpec:
    """Declare an init-only managed field on a decorated class."""

    if not isinstance(init, bool):
        raise TypeError(f"init must be bool, got {type(init).__name__}")
    return InitOnlyFieldSpec(init=init, default=default)


def compile_init_only_capsule() -> Callable[[type[Any]], type[Any]]:
    """Return a decorator that emits an init-only wrapper class."""

    def decorate(decorated_class: type[Any]) -> type[Any]:
        class_definition = class_definition_from_class(decorated_class)
        _strip_field_spec_markers(decorated_class)
        factory_source = emit_init_only_factory_source(class_definition)
        wrapped_class = _materialize_init_only_wrapper_class(
            class_definition,
            factory_source,
        )
        wrapped_class.__module__ = decorated_class.__module__
        wrapped_class.__qualname__ = decorated_class.__qualname__
        wrapped_class.__doc__ = decorated_class.__doc__
        wrapped_class.__annotations__ = dict(getattr(decorated_class, "__annotations__", {}))
        wrapped_class.__wrapped__ = decorated_class
        wrapped_class.__yidl_class_definition__ = class_definition
        wrapped_class.__yidl_factory_source__ = factory_source
        return wrapped_class

    return decorate


def class_definition_from_class(
    decorated_class: type[Any],
) -> InitOnlyClassDefinition:
    """Scan a decorated class for ``field_spec(...)`` declarations."""

    annotations = dict(getattr(decorated_class, "__annotations__", {}))
    unannotated_fields = tuple(
        name
        for name, value in decorated_class.__dict__.items()
        if isinstance(value, InitOnlyFieldSpec) and name not in annotations
    )
    if unannotated_fields:
        raise ValueError(
            "field_spec requires annotations for managed fields: "
            f"{unannotated_fields!r}"
        )

    fields: list[ResolvedInitField] = []
    for field_name, field_anno in annotations.items():
        value = decorated_class.__dict__.get(field_name, UNSPECIFIED)
        if not isinstance(value, InitOnlyFieldSpec):
            continue
        fields.append(
            _resolve_init_field(
                field_name=field_name,
                field_anno=field_anno,
                init=value.init,
                default=value.default,
            )
        )

    return InitOnlyClassDefinition(
        class_name=decorated_class.__name__,
        wrapped_class=decorated_class,
        fields=tuple(fields),
    )


def emit_init_only_factory_source(class_definition: InitOnlyClassDefinition) -> str:
    """Emit the Astichi-built wrapper factory source for ``class_definition``."""

    astichi = _import_astichi()
    builder = astichi.build()
    builder.add.Root(
        _piece(_FACTORY_ROOT_SRC),
        arg_names={"class_name": class_definition.class_name},
        keep_names=[
            class_definition.class_name,
            "class_definition",
            "_y_class_definition",
            "_y_wrapped_class",
        ],
    )
    builder.add.ClassDefinitionLocal(
        _piece(_CLASS_DEFINITION_LOCAL_SRC),
        keep_names=["class_definition", "_y_class_definition"],
    )
    builder.add.WrappedClassLocal(
        _piece(_WRAPPED_CLASS_LOCAL_SRC),
        keep_names=["_y_class_definition", "_y_wrapped_class"],
    )
    builder.add.ClassDefinitionAttr(_piece(_CLASS_DEFINITION_ATTR_SRC))
    builder.add.InitMethod(_piece(_INIT_METHOD_SRC))
    registered_field_resources: set[str] = set()

    def ensure_field_resource(name: str) -> None:
        if name in registered_field_resources:
            return
        builder.add(name, _piece(_FIELD_RESOURCE_SOURCES[name]))
        registered_field_resources.add(name)

    builder.Root.factory_locals.add.ClassDefinitionLocal(order=0)
    builder.Root.factory_locals.add.WrappedClassLocal(order=1)
    builder.Root.class_defs.add.ClassDefinitionAttr(order=0)
    builder.Root.class_methods.add.InitMethod(order=0)

    for order, field_definition in enumerate(class_definition.fields):
        hoist_order = 10 + (order * 10)
        if field_definition.init:
            anno_local_name = _anno_local_name(field_definition.field_name)
            ensure_field_resource("AnnoLocal")
            builder.Root.factory_locals.add.AnnoLocal(
                order=hoist_order,
                bind={
                    "local_name": anno_local_name,
                    "field_name": field_definition.field_name,
                },
                keep_names=[anno_local_name],
            )
            if field_definition.default is not UNSPECIFIED:
                default_local_name = _default_local_name(field_definition.field_name)
                ensure_field_resource("DefaultLocal")
                builder.Root.factory_locals.add.DefaultLocal(
                    order=hoist_order + 1,
                    bind={
                        "local_name": default_local_name,
                        "field_name": field_definition.field_name,
                    },
                    keep_names=[default_local_name],
                )
            param_resource = (
                "DefaultedParam"
                if field_definition.default is not UNSPECIFIED
                else "RequiredParam"
            )
            ensure_field_resource(param_resource)
            param_arg_names = {"anno_local": anno_local_name}
            if field_definition.default is not UNSPECIFIED:
                param_arg_names["default_local"] = _default_local_name(
                    field_definition.field_name
                )
            builder.InitMethod.method_params.add(
                param_resource,
                order=order,
                arg_names={
                    "field_name": field_definition.field_name,
                    **param_arg_names,
                },
            )
            ensure_field_resource("ParamAssign")
            builder.InitMethod.method_body.add.ParamAssign(
                order=order,
                arg_names={
                    "self": "self",
                    "field_value": field_definition.field_name,
                },
                bind={"target_path": f"{field_definition.field_name}"},
            )
            continue

        default_local_name = _default_local_name(field_definition.field_name)
        ensure_field_resource("DefaultLocal")
        builder.Root.factory_locals.add.DefaultLocal(
            order=hoist_order,
            bind={
                "local_name": default_local_name,
                "field_name": field_definition.field_name,
            },
            keep_names=[default_local_name],
        )
        ensure_field_resource("DefaultAssign")
        builder.InitMethod.method_body.add.DefaultAssign(
            order=order,
            arg_names={
                "self": "self",
                "default_local": default_local_name,
            },
            bind={"target_path": f"{field_definition.field_name}"},
        )

    if not class_definition.fields:
        builder.add.Pass(_piece(_PASS_SRC))
        builder.InitMethod.method_body.add.Pass(order=0)

    return builder.build().materialize().emit(provenance=False)


def render_init_only_class(
    class_name: str,
    fields: Iterable[ResolvedInitField],
) -> str:
    resolved_fields = tuple(fields)
    module = ast.Module(
        body=[_build_class_def(class_name, resolved_fields)],
        type_ignores=[],
    )
    ast.fix_missing_locations(module)
    return ast.unparse(module)


def _materialize_init_only_wrapper_class(
    class_definition: InitOnlyClassDefinition,
    factory_source: str,
) -> type[Any]:
    namespace: dict[str, object] = {"__name__": class_definition.wrapped_class.__module__}
    exec(compile(factory_source, "<yidl.init_only.factory>", "exec"), namespace)
    make_wrapper_class = namespace["make_wrapper_class"]
    if not callable(make_wrapper_class):
        raise TypeError("generated init-only factory is not callable")
    wrapped_class = make_wrapper_class(class_definition)
    if not isinstance(wrapped_class, type):
        raise TypeError("generated init-only wrapper is not a class")
    return wrapped_class


def _strip_field_spec_markers(decorated_class: type[Any]) -> None:
    annotations = getattr(decorated_class, "__annotations__", {})
    for field_name in annotations:
        value = decorated_class.__dict__.get(field_name, UNSPECIFIED)
        if isinstance(value, InitOnlyFieldSpec):
            delattr(decorated_class, field_name)


def _import_astichi() -> Any:
    import astichi

    return astichi


@cache
def _piece(src: str):
    return _import_astichi().compile(textwrap.dedent(src).strip() + "\n")


def _anno_local_name(field_name: str) -> str:
    return f"_y_{field_name}_anno"


def _default_local_name(field_name: str) -> str:
    return f"_y_{field_name}_default"


def _resolve_init_field(
    *,
    field_name: str,
    field_anno: Any = UNSPECIFIED,
    init: bool = True,
    default: Any = UNSPECIFIED,
) -> ResolvedInitField:
    if not isinstance(field_name, str):
        raise TypeError(f"FieldName must be str, got {type(field_name).__name__}")
    if not isinstance(init, bool):
        raise TypeError(f"Init must be bool for field {field_name!r}")
    if not init and default is UNSPECIFIED:
        raise ValueError(f"missing initial value for field {field_name!r}")

    return ResolvedInitField(
        field_name=field_name,
        field_anno=field_anno,
        init=init,
        default=default,
    )


def _build_class_def(class_name: str, fields: tuple[ResolvedInitField, ...]) -> ast.ClassDef:
    return ast.ClassDef(
        name=class_name,
        bases=[],
        keywords=[],
        decorator_list=[],
        body=[_build_init_method(fields)],
    )


def _build_init_method(fields: tuple[ResolvedInitField, ...]) -> ast.FunctionDef:
    kwonlyargs: list[ast.arg] = []
    kw_defaults: list[ast.expr | None] = []
    body: list[ast.stmt] = []

    for field in fields:
        if field.init:
            kwonlyargs.append(
                ast.arg(
                    arg=field.field_name,
                    annotation=_annotation_expr(field.field_anno),
                )
            )
            kw_defaults.append(
                None if field.default is UNSPECIFIED else _expression_for_value(field.default)
            )
            value_expr: ast.expr = ast.Name(id=field.field_name, ctx=ast.Load())
        else:
            value_expr = _expression_for_value(field.default)

        body.append(
            ast.Assign(
                targets=[
                    ast.Attribute(
                        value=ast.Name(id="self", ctx=ast.Load()),
                        attr=field.field_name,
                        ctx=ast.Store(),
                    )
                ],
                value=value_expr,
            )
        )

    if not body:
        body = [ast.Pass()]

    return ast.FunctionDef(
        name="__init__",
        args=ast.arguments(
            posonlyargs=[],
            args=[ast.arg(arg="self")],
            vararg=None,
            kwonlyargs=kwonlyargs,
            kw_defaults=kw_defaults,
            kwarg=None,
            defaults=[],
        ),
        body=body,
        decorator_list=[],
    )


def _annotation_expr(annotation: Any) -> ast.expr | None:
    if annotation is UNSPECIFIED:
        return None
    if isinstance(annotation, str):
        return ast.parse(annotation, mode="eval").body
    if isinstance(annotation, type):
        return ast.Name(id=annotation.__name__, ctx=ast.Load())
    annotation_name = getattr(annotation, "__name__", None)
    if isinstance(annotation_name, str):
        return ast.Name(id=annotation_name, ctx=ast.Load())
    return ast.parse(repr(annotation), mode="eval").body


def _expression_for_value(value: Any) -> ast.expr:
    return ast.parse(repr(value), mode="eval").body


__all__ = [
    "InitOnlyClassDefinition",
    "InitOnlyFieldSpec",
    "ResolvedInitField",
    "class_definition_from_class",
    "compile_init_only_capsule",
    "emit_init_only_factory_source",
    "field_spec",
    "render_init_only_class",
]
