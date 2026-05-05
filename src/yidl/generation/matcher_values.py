"""Generated values returned by matcher runtimes."""

from __future__ import annotations

import ast
import builtins
from collections.abc import Iterable, Mapping
from dataclasses import dataclass
from dataclasses import field
import textwrap

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
        raise ValueError("astichi_code must be a non-empty string")
    source = textwrap.dedent(astichi_code).strip()
    if not source:
        raise ValueError("astichi_code must be a non-empty string")
    return MatcherGeneratedValue(
        source=source,
        file_name=file_name,
        line_number=line_number,
        offset=offset,
        arg_names=tuple((arg_names or {}).items()),
        keep_names=_merge_keep_names(keep_names),
        source_kind=source_kind,
    )


def constructor_expr_for(value: MatcherGeneratedValue) -> ast.expr:
    """Build an expression that recreates a matcher-generated value."""

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
        args=[_literal_to_ast(value.source)],
        keywords=keywords,
    )


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


__all__ = [
    "MatcherGeneratedValue",
    "PYTHON_BUILTIN_KEEP_NAMES",
    "constructor_expr_for",
    "from_astichi_code",
    "from_literal",
]
