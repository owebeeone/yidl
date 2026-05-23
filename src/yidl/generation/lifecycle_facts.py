"""Lifecycle fact analyzers used by generated DDS operations."""

from __future__ import annotations

from collections.abc import Iterable
from inspect import Parameter
from inspect import signature


CURRENT_FACADE = "current_facade"
WORKING_FACADE = "working_facade"
TX_KEY = "tx_key"
INITVAR = "initvar"


class CallableAnalysis:
    """Signature facts produced for one lifecycle callable."""

    __slots__ = ("injections", "params", "spec")

    def __init__(
        self,
        *,
        spec: dict[str, object],
        params: tuple[dict[str, object], ...],
        injections: tuple[dict[str, object], ...],
    ) -> None:
        self.spec = spec
        self.params = params
        self.injections = injections


def analyze_callable(
    *,
    name: str,
    source_label: str,
    role: str,
    callable_obj: object,
    allowed_injections: Iterable[str] = (),
) -> CallableAnalysis:
    """Return DDS-ready signature facts for one lifecycle callable."""

    label = _label(name, source_label)
    if not callable(callable_obj):
        raise TypeError(f"{label}: callable object is not callable")

    allowed_initvars = _allowed_initvars(allowed_injections, label)
    params: list[dict[str, object]] = []
    injections: list[dict[str, object]] = []

    for order, param in enumerate(signature(callable_obj).parameters.values()):
        if param.kind is Parameter.VAR_POSITIONAL:
            raise TypeError(f"{label}: unsupported *args parameter {param.name!r}")
        if param.kind is Parameter.VAR_KEYWORD:
            raise TypeError(f"{label}: unsupported **kwargs parameter {param.name!r}")
        if param.kind is Parameter.POSITIONAL_ONLY:
            raise TypeError(
                f"{label}: unsupported positional-only parameter {param.name!r}"
            )

        injection_kind = _injection_kind(param.name, allowed_initvars, label)
        params.append(
            {
                "callable_name": name,
                "param_name": param.name,
                "param_kind": param.kind.name,
                "param_order": order,
            }
        )
        injections.append(
            {
                "callable_name": name,
                "param_name": param.name,
                "injection_kind": injection_kind,
                "required": param.default is Parameter.empty,
            }
        )

    return CallableAnalysis(
        spec={
            "name": name,
            "source_label": source_label,
            "callable_role": role,
            "accepts_var_args": False,
            "accepts_var_kwargs": False,
        },
        params=tuple(params),
        injections=tuple(injections),
    )


def _allowed_initvars(values: Iterable[str], label: str) -> frozenset[str]:
    allowed = tuple(values)
    if not all(isinstance(item, str) and item for item in allowed):
        raise TypeError(f"{label}: allowed injections must be non-empty strings")
    return frozenset(allowed)


def _injection_kind(name: str, allowed_initvars: frozenset[str], label: str) -> str:
    if name == "current":
        return CURRENT_FACADE
    if name == "working":
        return WORKING_FACADE
    if name == "tx_key":
        return TX_KEY
    if name in allowed_initvars:
        return INITVAR
    raise TypeError(f"{label}: unknown injection parameter {name!r}")


def _label(name: str, source_label: str) -> str:
    return source_label or name


__all__ = [
    "CURRENT_FACADE",
    "CallableAnalysis",
    "INITVAR",
    "TX_KEY",
    "WORKING_FACADE",
    "analyze_callable",
]
