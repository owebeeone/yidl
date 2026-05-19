"""Generated values returned by matcher runtimes."""

from __future__ import annotations

import ast
import builtins
from collections.abc import Iterable, Mapping
from dataclasses import dataclass
from dataclasses import field
import textwrap
from typing import Any

import astichi


PYTHON_BUILTIN_KEEP_NAMES = tuple(sorted(dir(builtins)))


@dataclass(frozen=True)
class MatcherGeneratedValue:
    """Astichi compile inputs for a value selected by a matcher."""

    source: str
    file_name: str | None = None
    line_number: int = 1
    offset: int = 0
    arg_names: tuple[tuple[str, str], ...] = ()
    keep_names: tuple[str, ...] = ()
    source_kind: str = "authored"
    _generator: astichi.Composable | None = field(
        default=None,
        init=False,
        repr=False,
        compare=False,
    )

    def to_generator(self) -> astichi.Composable:
        if self._generator is not None:
            return self._generator
        generator = astichi.compile(
            self.source,
            file_name=self.file_name,
            line_number=self.line_number,
            offset=self.offset,
            arg_names=dict(self.arg_names) or None,
            keep_names=self.keep_names or None,
            source_kind=self.source_kind,
        )
        object.__setattr__(self, "_generator", generator)
        return generator


@dataclass(frozen=True)
class AstichiTemplateValue:
    """Astichi template plus generated edge-binding expressions."""

    template: MatcherGeneratedValue
    edge_arg_names: MatcherGeneratedValue | None = None
    edge_bind: MatcherGeneratedValue | None = None
    edge_keep_names: MatcherGeneratedValue | None = None

    def to_generator(self) -> astichi.Composable:
        return self.template.to_generator()

    def arg_names_for(self, record: object) -> Mapping[str, str] | None:
        value = _evaluate_edge_value(self.edge_arg_names, record)
        if value is None:
            return None
        if not isinstance(value, Mapping):
            raise TypeError(f"edge arg_names must be mapping, got {type(value).__name__}")
        result = dict(value)
        if not all(
            isinstance(key, str) and isinstance(item, str)
            for key, item in result.items()
        ):
            raise TypeError("edge arg_names keys and values must be str")
        return result or None

    def bind_for(self, record: object) -> Mapping[str, object] | None:
        value = _evaluate_edge_value(self.edge_bind, record)
        if value is None:
            return None
        if not isinstance(value, Mapping):
            raise TypeError(f"edge bind must be mapping, got {type(value).__name__}")
        result = dict(value)
        if not all(isinstance(key, str) for key in result):
            raise TypeError("edge bind keys must be str")
        return result or None

    def keep_names_for(self, record: object) -> tuple[str, ...] | None:
        value = _evaluate_edge_value(self.edge_keep_names, record)
        if value is None:
            return None
        result = tuple(value)
        if not all(isinstance(item, str) for item in result):
            raise TypeError("edge keep_names values must be str")
        return result or None


@dataclass(frozen=True)
class ImportedGeneratedValue:
    """Imported symbol selected as a generated value."""

    module: str
    name: str
    _generator: astichi.Composable | None = field(
        default=None,
        init=False,
        repr=False,
        compare=False,
    )

    def to_generator(self) -> astichi.Composable:
        if self._generator is not None:
            return self._generator
        generator = astichi.compile(
            f"astichi_pyimport(module={self.module}, names=({self.name},))\n"
            f"{self.name}\n"
        )
        object.__setattr__(self, "_generator", generator)
        return generator


GeneratedValue = MatcherGeneratedValue | AstichiTemplateValue | ImportedGeneratedValue


def from_literal(value: object) -> MatcherGeneratedValue:
    """Create a matcher-generated value from a Python literal."""

    return from_astichi_code(_literal_to_source(value))


def from_astichi_code(
    astichi_code: str,
    file_name: str | None = None,
    line_number: int = 1,
    offset: int = 0,
    *,
    arg_names: Mapping[str, str] | None = None,
    keep_names: Iterable[str] | None = None,
    source_kind: str = "authored",
) -> MatcherGeneratedValue:
    """Create a matcher-generated value from Astichi source."""

    if not isinstance(astichi_code, str):
        raise ValueError("astichi_code must be a string")
    source = textwrap.dedent(astichi_code).strip()
    return MatcherGeneratedValue(
        source=source,
        file_name=file_name,
        line_number=line_number,
        offset=offset,
        arg_names=tuple((arg_names or {}).items()),
        keep_names=_merge_keep_names(keep_names),
        source_kind=source_kind,
    )


def from_import(module: str, name: str) -> ImportedGeneratedValue:
    """Create a generated value that references an imported symbol."""

    _require_dotted_path(module, "import module")
    _require_identifier(name, "import name")
    return ImportedGeneratedValue(module=module, name=name)


def astichi_template(
    template: MatcherGeneratedValue,
    *,
    arg_names: MatcherGeneratedValue | None = None,
    bind: MatcherGeneratedValue | None = None,
    keep_names: MatcherGeneratedValue | None = None,
) -> AstichiTemplateValue:
    """Create an Astichi template resource with source-emittable edge bindings."""

    _require_matcher_generated_value(template, "template")
    if arg_names is not None:
        _require_matcher_generated_value(arg_names, "arg_names")
    if bind is not None:
        _require_matcher_generated_value(bind, "bind")
    if keep_names is not None:
        _require_matcher_generated_value(keep_names, "keep_names")
    return AstichiTemplateValue(
        template=template,
        edge_arg_names=arg_names,
        edge_bind=bind,
        edge_keep_names=keep_names,
    )


def constructor_expr_for(value: GeneratedValue) -> ast.expr:
    """Build an expression that recreates a matcher-generated value."""

    return _constructor_expr(value, placeholders=None)


def render_value_constructor(value: GeneratedValue) -> str:
    """Render a generated-value constructor as Python source.

    Source strings whose content spans multiple lines are emitted as
    triple-quoted multi-line literals when that preserves the string byte for
    byte and the result remains lexically unambiguous. Everything else falls
    back to the default ``ast.unparse`` rendering.
    """

    placeholders: dict[str, str] = {}
    expr = _constructor_expr(value, placeholders=placeholders)
    ast.fix_missing_locations(expr)
    rendered = ast.unparse(expr)
    for token, literal in placeholders.items():
        rendered = rendered.replace(repr(token), literal, 1)
    return rendered


def _constructor_expr(
    value: GeneratedValue,
    *,
    placeholders: dict[str, str] | None,
) -> ast.expr:
    if isinstance(value, ImportedGeneratedValue):
        return ast.Call(
            func=ast.Name(id="from_import", ctx=ast.Load()),
            args=[
                _literal_to_ast(value.module),
                _literal_to_ast(value.name),
            ],
            keywords=[],
        )

    if isinstance(value, AstichiTemplateValue):
        keywords: list[ast.keyword] = []
        if value.edge_arg_names is not None:
            keywords.append(
                ast.keyword(
                    arg="arg_names",
                    value=_constructor_expr(value.edge_arg_names, placeholders=placeholders),
                )
            )
        if value.edge_bind is not None:
            keywords.append(
                ast.keyword(
                    arg="bind",
                    value=_constructor_expr(value.edge_bind, placeholders=placeholders),
                )
            )
        if value.edge_keep_names is not None:
            keywords.append(
                ast.keyword(
                    arg="keep_names",
                    value=_constructor_expr(value.edge_keep_names, placeholders=placeholders),
                )
            )
        return ast.Call(
            func=ast.Name(id="astichi_template", ctx=ast.Load()),
            args=[_constructor_expr(value.template, placeholders=placeholders)],
            keywords=keywords,
        )

    keywords: list[ast.keyword] = []
    if value.file_name is not None:
        keywords.append(
            ast.keyword(arg="file_name", value=_literal_to_ast(value.file_name))
        )
    if value.line_number != 1:
        keywords.append(
            ast.keyword(arg="line_number", value=_literal_to_ast(value.line_number))
        )
    if value.offset != 0:
        keywords.append(ast.keyword(arg="offset", value=_literal_to_ast(value.offset)))
    if value.arg_names:
        keywords.append(
            ast.keyword(arg="arg_names", value=_literal_to_ast(dict(value.arg_names)))
        )
    explicit_keep_names = _explicit_keep_names(value.keep_names)
    if explicit_keep_names:
        keywords.append(
            ast.keyword(arg="keep_names", value=_literal_to_ast(explicit_keep_names))
        )
    if value.source_kind != "authored":
        keywords.append(
            ast.keyword(arg="source_kind", value=_literal_to_ast(value.source_kind))
        )
    return ast.Call(
        func=ast.Name(id="from_astichi_code", ctx=ast.Load()),
        args=[_source_arg(value.source, placeholders)],
        keywords=keywords,
    )


def _source_arg(
    source: str,
    placeholders: dict[str, str] | None,
) -> ast.expr:
    if placeholders is not None and _can_render_as_triple_quoted(source):
        token = f"__YIDL_SOURCE_PLACEHOLDER_{len(placeholders)}__"
        placeholders[token] = f'"""\\\n{source}"""'
        return ast.Constant(value=token)
    return ast.Constant(value=source)


def _can_render_as_triple_quoted(source: str) -> bool:
    return (
        "\n" in source
        and "\\" not in source
        and '"""' not in source
        and not source.endswith('"')
    )


def is_generated_value(value: object) -> bool:
    return isinstance(
        value,
        (
            MatcherGeneratedValue,
            AstichiTemplateValue,
            ImportedGeneratedValue,
        ),
    )


def generated_value_keep_names(value: GeneratedValue) -> tuple[str, ...]:
    if isinstance(value, AstichiTemplateValue):
        names = {
            "astichi_template",
            *generated_value_keep_names(value.template),
        }
        if value.edge_arg_names is not None:
            names.update(generated_value_keep_names(value.edge_arg_names))
        if value.edge_bind is not None:
            names.update(generated_value_keep_names(value.edge_bind))
        if value.edge_keep_names is not None:
            names.update(generated_value_keep_names(value.edge_keep_names))
        return tuple(sorted(names))
    if isinstance(value, ImportedGeneratedValue):
        return ("from_import",)
    return ("from_astichi_code",)


def generated_value_uses_astichi_template(value: GeneratedValue) -> bool:
    return isinstance(value, AstichiTemplateValue)


def generated_value_constructor_names(value: GeneratedValue) -> tuple[str, ...]:
    """Names that must be imported to recreate a generated value in source."""

    return generated_value_keep_names(value)


def _literal_to_source(value: object) -> str:
    expr = _literal_to_ast(value)
    ast.fix_missing_locations(expr)
    return ast.unparse(expr)


def _literal_to_ast(value: object) -> ast.expr:
    if value is None or isinstance(value, bool | int | float | complex | str):
        return ast.Constant(value=value)
    if isinstance(value, tuple):
        return ast.Tuple(
            elts=[_literal_to_ast(item) for item in value],
            ctx=ast.Load(),
        )
    if isinstance(value, list):
        return ast.List(
            elts=[_literal_to_ast(item) for item in value],
            ctx=ast.Load(),
        )
    if isinstance(value, dict):
        return ast.Dict(
            keys=[_literal_to_ast(key) for key in value.keys()],
            values=[_literal_to_ast(item) for item in value.values()],
        )
    if isinstance(value, set):
        return ast.Set(
            elts=sorted(
                (_literal_to_ast(item) for item in value),
                key=ast.unparse,
            )
        )
    raise TypeError(f"unsupported matcher literal type: {type(value).__name__}")


def _merge_keep_names(keep_names: Iterable[str] | None) -> tuple[str, ...]:
    merged: dict[str, None] = {name: None for name in PYTHON_BUILTIN_KEEP_NAMES}
    for name in keep_names or ():
        merged[name] = None
    return tuple(merged)


def _explicit_keep_names(keep_names: Iterable[str]) -> tuple[str, ...]:
    builtins_set = frozenset(PYTHON_BUILTIN_KEEP_NAMES)
    return tuple(name for name in keep_names if name not in builtins_set)


def _require_dotted_path(value: str, label: str) -> None:
    if not isinstance(value, str) or not value:
        raise ValueError(f"{label} must be a non-empty dotted identifier path")
    for part in value.split("."):
        _require_identifier(part, f"{label} component")


def _require_identifier(value: str, label: str) -> None:
    if not isinstance(value, str) or not value.isidentifier():
        raise ValueError(f"{label} must be a valid identifier: {value!r}")


def _evaluate_edge_value(value: MatcherGeneratedValue | None, record: object) -> Any:
    if value is None:
        return None
    source = value.to_generator().materialize().emit(provenance=False).strip()
    return eval(
        compile(source, value.file_name or "<yidl.matcher.edge>", "eval"),
        {},
        {"record": record},
    )


def _require_matcher_generated_value(value: object, label: str) -> None:
    if not isinstance(value, MatcherGeneratedValue):
        raise TypeError(f"{label} must be a MatcherGeneratedValue")


__all__ = [
    "AstichiTemplateValue",
    "GeneratedValue",
    "ImportedGeneratedValue",
    "MatcherGeneratedValue",
    "PYTHON_BUILTIN_KEEP_NAMES",
    "astichi_template",
    "constructor_expr_for",
    "from_astichi_code",
    "from_import",
    "from_literal",
    "generated_value_constructor_names",
    "generated_value_keep_names",
    "generated_value_uses_astichi_template",
    "is_generated_value",
    "render_value_constructor",
]
