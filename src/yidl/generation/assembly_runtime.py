"""Runtime helpers for evaluating YIDL assembly values."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from typing import cast

from yidl.generation.assembly_plan import AndConditionSpec
from yidl.generation.assembly_plan import AssemblyConditionSpec
from yidl.generation.assembly_plan import AssemblyValueRef
from yidl.generation.assembly_plan import EqConditionSpec
from yidl.generation.assembly_plan import LiteralValueRef
from yidl.generation.assembly_plan import TupleValueRef
from yidl.generation.assembly_plan import ValueRef


_MISSING = object()


class Undefined(NameError):
    """Raised when an assembly value is not visible in the current stack."""


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
