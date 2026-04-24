"""Tiny lambda wrapper for spec-context compute/filter operations."""

from __future__ import annotations

from collections.abc import Callable
from collections.abc import Mapping
from dataclasses import dataclass
import inspect
from typing import Any

from .core import CapsuleSpecInstance

_MISSING = object()


def inspect_names(
    function: Callable[..., Any],
    *,
    context: str = "spec lambda",
) -> tuple[str, ...]:
    try:
        signature = inspect.signature(function)
    except (TypeError, ValueError) as exc:
        raise TypeError(f"{context}: cannot inspect signature of {function!r}") from exc

    names: list[str] = []
    for parameter in signature.parameters.values():
        if parameter.kind not in {
            inspect.Parameter.POSITIONAL_OR_KEYWORD,
            inspect.Parameter.KEYWORD_ONLY,
        }:
            raise TypeError(
                f"{context}: {function!r} must use named parameters only "
                "(no positional-only, *args, or **kwargs)",
            )
        names.append(parameter.name)
    return tuple(names)


@dataclass(frozen=True, slots=True)
class SpecContext:
    values: Mapping[str, Any]

    @classmethod
    def from_spec_instance(cls, spec: CapsuleSpecInstance) -> SpecContext:
        return cls(
            values={
                value.property_name: value.value
                for value in spec.values
            }
        )

    @classmethod
    def from_mapping(cls, values: Mapping[str, Any]) -> SpecContext:
        return cls(values=dict(values))

    def get(self, name: str, default: Any = _MISSING) -> Any:
        if name in self.values:
            return self.values[name]
        return default

    def require(self, name: str) -> Any:
        value = self.get(name)
        if value is _MISSING:
            raise ValueError(f"unknown spec property {name!r}")
        return value

    def compute(
        self,
        function: Callable[..., Any],
        *,
        context: str = "spec compute",
    ) -> Any:
        kwargs = {
            name: self.require(name)
            for name in inspect_names(function, context=context)
        }
        return function(**kwargs)

    def filter(
        self,
        function: Callable[..., Any],
        *,
        context: str = "spec filter",
    ) -> bool:
        result = self.compute(function, context=context)
        if not isinstance(result, bool):
            raise TypeError(
                f"{context}: spec filter must return bool, got {type(result).__name__}",
            )
        return result


def spec_compute(
    spec: SpecContext | CapsuleSpecInstance | Mapping[str, Any],
    function: Callable[..., Any],
) -> Any:
    return _coerce_spec_context(spec).compute(function)


def spec_filter(
    spec: SpecContext | CapsuleSpecInstance | Mapping[str, Any],
    function: Callable[..., Any],
) -> bool:
    return _coerce_spec_context(spec).filter(function)


def _coerce_spec_context(
    spec: SpecContext | CapsuleSpecInstance | Mapping[str, Any],
) -> SpecContext:
    if isinstance(spec, SpecContext):
        return spec
    if isinstance(spec, CapsuleSpecInstance):
        return SpecContext.from_spec_instance(spec)
    if isinstance(spec, Mapping):
        return SpecContext.from_mapping(spec)
    raise TypeError(f"unsupported spec context {type(spec).__name__}")


__all__ = [
    "SpecContext",
    "inspect_names",
    "spec_compute",
    "spec_filter",
]
