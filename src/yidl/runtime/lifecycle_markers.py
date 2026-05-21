from __future__ import annotations

from dataclasses import dataclass

from yidl.runtime.transaction_yidl import DEFAULT_TRANSACTION
from yidl.sentinel_maker import sentinels


MISSING = sentinels.MISSING
_HAS_DEFAULT_FACTORY = sentinels.HAS_DEFAULT_FACTORY
_TRANSACTION_METHOD_MARKERS_ATTR = "__yidl_lifecycle_transaction_method_markers__"


class LifecycleDefinitionError(ValueError):
    """Raised when lifecycle marker or class definition metadata is invalid."""


class LifecycleDefinitionWarning(UserWarning):
    """Warns when lifecycle metadata must fall back to conservative behavior."""


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


@dataclass(frozen=True, slots=True)
class TransactionMethodMarker:
    """Marker attached to transaction hook/validator methods."""

    kind: str
    tx_group: object = DEFAULT_TRANSACTION


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


def commit_order_key(
    *args: object,
    tx_group: object = MISSING,
) -> object:
    """Mark a method as the commit-order key provider for a transaction group."""

    return _transaction_method_marker("commit_order_key", *args, tx_group=tx_group)


def validate_commit(
    *args: object,
    tx_group: object = MISSING,
) -> object:
    """Mark a method as a commit validator for a transaction group."""

    return _transaction_method_marker("validate_commit", *args, tx_group=tx_group)


def before_commit(
    *args: object,
    tx_group: object = MISSING,
) -> object:
    """Mark a method as a before-commit hook for a transaction group."""

    return _transaction_method_marker("before_commit", *args, tx_group=tx_group)


def after_commit(
    *args: object,
    tx_group: object = MISSING,
) -> object:
    """Mark a method as an after-commit hook for a transaction group."""

    return _transaction_method_marker("after_commit", *args, tx_group=tx_group)


def after_rollback(
    *args: object,
    tx_group: object = MISSING,
) -> object:
    """Mark a method as an after-rollback hook for a transaction group."""

    return _transaction_method_marker("after_rollback", *args, tx_group=tx_group)


def transaction_method_markers(value: object) -> tuple[TransactionMethodMarker, ...]:
    """Return transaction method markers attached to ``value``."""

    markers = getattr(value, _TRANSACTION_METHOD_MARKERS_ATTR, ())
    if not isinstance(markers, tuple):
        raise LifecycleDefinitionError("transaction method marker metadata is invalid")
    for marker in markers:
        if not isinstance(marker, TransactionMethodMarker):
            raise LifecycleDefinitionError("transaction method marker metadata is invalid")
    return markers


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


def _transaction_method_marker(
    kind: str,
    *args: object,
    tx_group: object,
) -> object:
    if len(args) > 1:
        raise LifecycleDefinitionError("unsupported transaction marker call shape")
    if args and tx_group is not MISSING:
        raise LifecycleDefinitionError("unsupported transaction marker call shape")
    if args:
        selected_tx_group = args[0]
        if callable(selected_tx_group):
            raise LifecycleDefinitionError(
                "transaction method marker requires an explicit transaction group",
            )
    else:
        selected_tx_group = (
            DEFAULT_TRANSACTION if tx_group is MISSING else tx_group
        )

    def decorate(target: object) -> object:
        if not callable(target):
            raise LifecycleDefinitionError(
                "transaction method marker target must be callable",
            )
        existing = transaction_method_markers(target)
        setattr(
            target,
            _TRANSACTION_METHOD_MARKERS_ATTR,
            (*existing, TransactionMethodMarker(kind, selected_tx_group)),
        )
        return target

    return decorate


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
