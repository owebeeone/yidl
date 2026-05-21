from __future__ import annotations

from dataclasses import dataclass

from yidl.runtime.transaction_yidl import DEFAULT_TRANSACTION
from yidl.sentinel_maker import sentinels


MISSING = sentinels.MISSING
_HAS_DEFAULT_FACTORY = sentinels.HAS_DEFAULT_FACTORY


class LifecycleDefinitionError(ValueError):
    """Raised when lifecycle marker or class definition metadata is invalid."""


@dataclass(frozen=True, slots=True)
class LifecycleMarker:
    """Base marker stored on a decorated class before harvesting."""

    kind: str
    default: object = MISSING
    default_factory: object = MISSING
    init: bool = True
    tx_group: object = MISSING


@dataclass(frozen=True, slots=True)
class FieldDecl:
    """Normalized lifecycle field declaration consumed by the harvester."""

    name: str
    annotation: object
    kind: str
    init: bool
    has_default: bool
    default: object
    has_default_factory: bool
    default_factory: object
    tx_group: object


def field(
    *,
    default: object = MISSING,
    default_factory: object = MISSING,
    init: bool = True,
) -> LifecycleMarker:
    """Declare a plain lifecycle field."""

    return _marker(
        kind="field",
        default=default,
        default_factory=default_factory,
        init=init,
        tx_group=MISSING,
    )


def initvar(
    *,
    default: object = MISSING,
    default_factory: object = MISSING,
    init: bool = True,
) -> LifecycleMarker:
    """Declare a constructor-only lifecycle value."""

    return _marker(
        kind="initvar",
        default=default,
        default_factory=default_factory,
        init=init,
        tx_group=MISSING,
    )


def classvar(*, default: object = MISSING) -> LifecycleMarker:
    """Declare a class-level lifecycle value."""

    return _marker(
        kind="classvar",
        default=default,
        default_factory=MISSING,
        init=False,
        tx_group=MISSING,
    )


def managed(
    tx_group: object = DEFAULT_TRANSACTION,
    *,
    default: object = MISSING,
    default_factory: object = MISSING,
    init: bool = True,
) -> LifecycleMarker:
    """Declare a transaction-managed lifecycle field."""

    return _marker(
        kind="managed",
        default=default,
        default_factory=default_factory,
        init=init,
        tx_group=tx_group,
    )


def normalize_marker(
    name: str,
    annotation: object,
    marker: LifecycleMarker,
    *,
    context: str | None = None,
) -> FieldDecl:
    """Normalize one marker into a field declaration."""

    if not isinstance(marker, LifecycleMarker):
        raise LifecycleDefinitionError(
            _message(context, name, f"expected lifecycle marker, got {type(marker).__name__}"),
        )
    _validate_name(name, context=context)
    return FieldDecl(
        name=name,
        annotation=annotation,
        kind=marker.kind,
        init=marker.init,
        has_default=marker.default is not MISSING,
        default=marker.default,
        has_default_factory=marker.default_factory is not MISSING,
        default_factory=marker.default_factory,
        tx_group=(
            DEFAULT_TRANSACTION
            if marker.kind == "managed" and marker.tx_group is MISSING
            else marker.tx_group
        ),
    )


def _marker(
    *,
    kind: str,
    default: object,
    default_factory: object,
    init: bool,
    tx_group: object,
) -> LifecycleMarker:
    if default is not MISSING and default_factory is not MISSING:
        raise LifecycleDefinitionError("cannot specify both default and default_factory")
    if not isinstance(init, bool):
        raise LifecycleDefinitionError("init must be a bool")
    if default_factory is not MISSING and not callable(default_factory):
        raise LifecycleDefinitionError("default_factory must be callable")
    return LifecycleMarker(
        kind=kind,
        default=default,
        default_factory=default_factory,
        init=init,
        tx_group=tx_group,
    )


def _validate_name(name: str, *, context: str | None) -> None:
    if not name:
        raise LifecycleDefinitionError(_message(context, name, "field name is required"))
    if name.startswith("_y_") or (
        name.startswith("__yidl_") and name.endswith("__")
    ):
        raise LifecycleDefinitionError(
            _message(context, name, "field name uses a reserved lifecycle prefix"),
        )


def _message(context: str | None, name: str, detail: str) -> str:
    prefix = f"{context}.{name}" if context else name
    return f"{prefix}: {detail}" if prefix else detail
