"""Composable capsule for plain init-only class generation."""

from __future__ import annotations

import ast
from dataclasses import dataclass
from typing import Any, Iterable

from .base_capsule import BaseCapsule
from .core import CapsuleSpecInstance, UNSPECIFIED, YidlCapsule, build_from

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

# Planned lambda-selector shape once the selector/binding engine exists.
# Property definitions keep semantic names such as `Init`, `Default`,
# `FieldName`, and `FieldAnno`. Callable/resource parameter names use the
# derived binding names `init`, `default`, `field_name`, and `field_anno`
# unless a later capsule overrides that mapping.
#
# def build_init_only_capsule() -> YidlCapsule:
#     builder = build_from(BaseCapsule)
#     builder.property.add.FieldName(str)
#     builder.property.add.FieldAnno(object, default=UNSPECIFIED)
#     builder.spec.add.field_spec.FieldName.FieldAnno.Init.Default
#     builder.method.add.Main.named("__init__").on(INIT_ONLY_METHOD_SHELL)\
#         .define.params.specs(lambda init: init)\
#         .define.prep.any()\
#         .define.field_init.specs(lambda field_name: True)\
#         .define.finalize.any()\
#         .done()
#     builder.resource.add.init_param.into.params.specs(lambda init: init)\
#         .on(INIT_ONLY_PARAM_RESOURCE)\
#         .define.field_name.spec.field_name()\
#         .define.anno.spec.compute(
#             lambda field_anno: field_anno if field_anno is not UNSPECIFIED else None
#         )\
#         .define.default_value.spec.compute(
#             lambda default: default if default is not UNSPECIFIED else UNSPECIFIED
#         )\
#         .done()
#     builder.resource.add.field_assign.into.field_init.specs(lambda field_name: True)\
#         .on(INIT_ONLY_FIELD_INIT_RESOURCE)\
#         .define.field_name.spec.field_name()\
#         .define.field_value.spec.compute(
#             lambda field_name, init, default: field_name if init else default
#         )\
#         .done()
#     return builder.build()


@dataclass(frozen=True, slots=True)
class ResolvedInitField:
    field_name: str
    field_anno: Any = UNSPECIFIED
    init: bool = True
    default: Any = UNSPECIFIED

ParameterSnippet = """
def astichi_params(*, field_name__astichi_arg__: astichi_hole(anno) = astichi_hole(default_value)):
    pass
"""

MethodSnippet = """
def method_name__astichi_arg__(self, method_params__astichi_param_hole__):
    astichi_hole(method_preparation)
    astichi_hole(method_body)
    astichi_hole(method_cleanup)
"""

def build_init_only_capsule() -> YidlCapsule:
    builder = build_from(BaseCapsule)
    builder.property.add.FieldName(str)
    builder.property.add.FieldAnno(object, default=UNSPECIFIED)
    # "field_spec" is defined to contain a field name, annotation, and init/default values.
    builder.spec.add.field_spec.FieldName.FieldAnno.Init.Default
    # uses the Main facade and defines the __init__ method.
    builder.method.add.Main.InitMethod(
        "__init__", 
        method_snippet=MethodSnippet, # holes - method_preparation, method_body, method_cleanup
        parameter_snippet=ParameterSnippet) # holes - field_name, anno, default_value
    builder.InitMethod.params.over.spec.filter(lambda spec: spec.init)
    builder.InitMethod.body.over.spec
    return builder.build()


InitOnlyCapsule = build_init_only_capsule()


def render_init_only_class(
    class_name: str,
    fields: Iterable[CapsuleSpecInstance],
    *,
    capsule: YidlCapsule = InitOnlyCapsule,
) -> str:
    resolved_fields = tuple(
        _resolve_field_spec(capsule, field_spec_instance)
        for field_spec_instance in fields
    )
    module = ast.Module(
        body=[_build_class_def(class_name, resolved_fields)],
        type_ignores=[],
    )
    ast.fix_missing_locations(module)
    return ast.unparse(module)


def _resolve_field_spec(
    capsule: YidlCapsule,
    field_spec_instance: CapsuleSpecInstance,
) -> ResolvedInitField:
    field_spec = _spec_named(capsule, field_spec_instance.spec_name)
    defined_properties = {prop.name: prop for prop in capsule.properties}
    allowed_properties = tuple(
        defined_properties[property_name]
        for property_name in field_spec.property_names
    )
    allowed_property_names = {prop.property_name for prop in allowed_properties}
    property_defaults = {
        prop.property_name: prop.default
        for prop in allowed_properties
    }
    provided_values: dict[str, Any] = {}
    for value in field_spec_instance.values:
        if value.property_name not in allowed_property_names:
            raise ValueError(
                f"unknown property {value.property_name!r} for spec "
                f"{field_spec_instance.spec_name!r}"
            )
        provided_values[value.property_name] = value.value

    field_name = provided_values.get(
        "field_name",
        property_defaults.get("field_name", UNSPECIFIED),
    )
    field_anno = provided_values.get(
        "field_anno",
        property_defaults.get("field_anno", UNSPECIFIED),
    )
    init = provided_values.get(
        "init",
        property_defaults.get("init", True),
    )
    default = provided_values.get(
        "default",
        property_defaults.get("default", UNSPECIFIED),
    )

    if field_name is UNSPECIFIED:
        raise ValueError(f"missing FieldName for spec {field_spec_instance.spec_name!r}")
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


def _spec_named(capsule: YidlCapsule, spec_name: str):
    for spec in capsule.specs:
        if spec.name == spec_name:
            return spec
    raise ValueError(f"unknown spec {spec_name!r}")


__all__ = [
    "InitOnlyCapsule",
    "ResolvedInitField",
    "build_init_only_capsule",
    "render_init_only_class",
]
