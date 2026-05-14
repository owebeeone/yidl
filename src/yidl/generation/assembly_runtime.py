"""Runtime helpers for evaluating YIDL assembly values."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
import keyword
from typing import cast

from astichi.pathmatch import parse_path_selector

from yidl.generation.assembly_plan import AndConditionSpec
from yidl.generation.assembly_plan import AssemblyConditionSpec
from yidl.generation.assembly_plan import AssemblyValueRef
from yidl.generation.assembly_plan import EqConditionSpec
from yidl.generation.assembly_plan import LiteralValueRef
from yidl.generation.assembly_plan import PathSpec
from yidl.generation.assembly_plan import TupleValueRef
from yidl.generation.assembly_plan import ValueRef


_MISSING = object()
_PATH_OPERATOR_TEXT = {
    "current": ".",
    "optional": "?",
    "any": "*",
    "many": "+",
}


class Undefined(NameError):
    """Raised when an assembly value is not visible in the current stack."""


class AssemblyPathError(ValueError):
    """Raised when an assembly path selector cannot be rendered or parsed."""


@dataclass(frozen=True, slots=True)
class DataStack:
    """Stack of record values visible to one assembly scope."""

    value_dicts: tuple[Mapping[str, object], ...] = ()
    parent: DataStack | None = None

    def push(self, *value_dicts: Mapping[str, object]) -> DataStack:
        """Return a child stack that searches ``value_dicts`` before this stack."""

        return DataStack(value_dicts=tuple(value_dicts), parent=self)

    def get(self, name: str) -> object:
        """Return the first visible value named ``name``."""

        for values in self.value_dicts:
            value = values.get(name, _MISSING)
            if value is not _MISSING:
                return value
        if self.parent is not None:
            return self.parent.get(name)
        raise Undefined(name)

    def get_mapping(self, name: str) -> Mapping[str, object]:
        value = self.get(name)
        if not isinstance(value, Mapping):
            raise TypeError(f"{name} must be a mapping")
        return cast(Mapping[str, object], value)

    def get_string(self, name: str) -> str:
        value = self.get(name)
        if not isinstance(value, str):
            raise TypeError(f"{name} must be a string")
        return value

    def get_integer(self, name: str) -> int:
        value = self.get(name)
        if not isinstance(value, int):
            raise TypeError(f"{name} must be an integer")
        return value


def evaluate_value(value: AssemblyValueRef, stack: DataStack) -> object:
    """Evaluate an assembly value reference against ``stack``."""

    if isinstance(value, ValueRef):
        return stack.get(value.name)
    if isinstance(value, LiteralValueRef):
        return value.value
    if isinstance(value, TupleValueRef):
        return tuple(evaluate_value(item, stack) for item in value.items)
    raise TypeError(f"unsupported assembly value: {type(value).__name__}")


def evaluate_index(
    value: AssemblyValueRef | None,
    stack: DataStack,
) -> int | tuple[int, ...] | None:
    """Evaluate a contribution build index."""

    if value is None:
        return None
    result = evaluate_value(value, stack)
    if isinstance(result, int):
        return result
    if isinstance(result, tuple) and all(isinstance(item, int) for item in result):
        return result
    raise TypeError("index must evaluate to int, tuple[int, ...], or None")


def evaluate_order(value: AssemblyValueRef, stack: DataStack) -> int:
    """Evaluate a contribution insertion order."""

    result = evaluate_value(value, stack)
    if not isinstance(result, int):
        raise TypeError("order must evaluate to int")
    return result


def evaluate_path_index(value: AssemblyValueRef, stack: DataStack) -> int:
    """Evaluate one path-index element."""

    result = evaluate_value(value, stack)
    if not isinstance(result, int):
        raise TypeError("path index must evaluate to int")
    return result


def evaluate_identifier(value: AssemblyValueRef, stack: DataStack) -> str:
    """Evaluate an identifier binding value."""

    result = evaluate_value(value, stack)
    if not isinstance(result, str) or not result.isidentifier() or keyword.iskeyword(result):
        raise TypeError("identifier binding must evaluate to a valid Python identifier")
    return result


def evaluate_external(value: AssemblyValueRef, stack: DataStack) -> object:
    """Evaluate an external Astichi binding value."""

    return evaluate_value(value, stack)


def evaluate_condition(condition: AssemblyConditionSpec, stack: DataStack) -> bool:
    """Evaluate an assembly condition against ``stack``."""

    if isinstance(condition, EqConditionSpec):
        return evaluate_value(condition.left, stack) == evaluate_value(
            condition.right,
            stack,
        )
    if isinstance(condition, AndConditionSpec):
        return all(evaluate_condition(item, stack) for item in condition.items)
    raise TypeError(f"unsupported assembly condition: {type(condition).__name__}")


def render_path_selector(path: PathSpec, stack: DataStack) -> str:
    """Render a structural YIDL path without its authored leading slash."""

    parts: list[str] = []
    for segment in path.segments:
        if segment.kind == "name":
            if segment.name is None:
                raise AssemblyPathError("named path segment is missing its name")
            if not segment.indexes:
                parts.append(segment.name)
                continue
            indexes = tuple(
                evaluate_path_index(index, stack)
                for index in segment.indexes
            )
            parts.append(f"{segment.name}[{','.join(str(index) for index in indexes)}]")
            continue
        operator = _PATH_OPERATOR_TEXT.get(segment.kind)
        if operator is None:
            raise AssemblyPathError(f"unsupported path segment kind {segment.kind!r}")
        parts.append(operator)
    return "/".join(parts)


def path_selector_tuple(
    path: PathSpec,
    stack: DataStack,
    *,
    context: str,
) -> tuple[str, ...]:
    """Render and parse a path selector, wrapping parser errors with context."""

    rendered = render_path_selector(path, stack)
    try:
        return parse_path_selector(rendered)
    except ValueError as exc:
        raise AssemblyPathError(f"{context}: invalid path selector {rendered!r}") from exc
