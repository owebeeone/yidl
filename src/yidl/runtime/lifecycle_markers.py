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
    working_default_factory: object = MISSING
    allow_self_factory: bool = False
    init: bool = True
    tx_key: object = MISSING
    compare: str = "value"
    freeze: object = MISSING
    thaw: object = MISSING


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
    allow_self_factory: bool
    has_working_default_factory: bool
    working_default_factory: object
    tx_key: object
    has_freeze: bool = False
    freeze: object = MISSING
    has_thaw: bool = False
    thaw: object = MISSING


@dataclass(frozen=True, slots=True)
class TransactionMethodMarker:
    """Marker attached to transaction hook/validator methods."""

    kind: str
    tx_key: object = DEFAULT_TRANSACTION


def field(
    *,
    default: object = MISSING,
    default_factory: object = MISSING,
    allow_self_factory: bool = False,
    init: bool = True,
) -> LifecycleMarker:
    """Declare a plain lifecycle field."""

    return _marker(
        kind="field",
        default=default,
        default_factory=default_factory,
        working_default_factory=MISSING,
        allow_self_factory=allow_self_factory,
        init=init,
        tx_key=MISSING,
    )


def initvar(
    *,
    default: object = MISSING,
    default_factory: object = MISSING,
    allow_self_factory: bool = False,
    init: bool = True,
) -> LifecycleMarker:
    """Declare a constructor-only lifecycle value."""

    return _marker(
        kind="initvar",
        default=default,
        default_factory=default_factory,
        working_default_factory=MISSING,
        allow_self_factory=allow_self_factory,
        init=init,
        tx_key=MISSING,
    )


def classvar(*, default: object = MISSING) -> LifecycleMarker:
    """Declare a class-level lifecycle value."""

    return _marker(
        kind="classvar",
        default=default,
        default_factory=MISSING,
        working_default_factory=MISSING,
        allow_self_factory=False,
        init=False,
        tx_key=MISSING,
    )


def const(
    *,
    default: object = MISSING,
    default_factory: object = MISSING,
    allow_self_factory: bool = False,
    init: bool = True,
) -> LifecycleMarker:
    """Declare an immutable per-instance lifecycle value."""

    return _marker(
        kind="const",
        default=default,
        default_factory=default_factory,
        working_default_factory=MISSING,
        allow_self_factory=allow_self_factory,
        init=init,
        tx_key=MISSING,
    )


def static(
    *,
    default: object = MISSING,
    default_factory: object = MISSING,
    allow_self_factory: bool = False,
    init: bool = True,
) -> LifecycleMarker:
    """Declare a write-once per-instance lifecycle value."""

    return _marker(
        kind="static",
        default=default,
        default_factory=default_factory,
        working_default_factory=MISSING,
        allow_self_factory=allow_self_factory,
        init=init,
        tx_key=MISSING,
    )


def managed(
    tx_key: object = DEFAULT_TRANSACTION,
    *,
    compare: str = "value",
    default: object = MISSING,
    default_factory: object = MISSING,
    allow_self_factory: bool = False,
    init: bool = True,
    freeze: object = MISSING,
    thaw: object = MISSING,
) -> LifecycleMarker:
    """Declare a transaction-managed lifecycle field."""

    return _marker(
        kind="managed",
        default=default,
        default_factory=default_factory,
        working_default_factory=MISSING,
        allow_self_factory=allow_self_factory,
        init=init,
        tx_key=tx_key,
        compare=compare,
        freeze=freeze,
        thaw=thaw,
    )


def owned(
    tx_key: object = DEFAULT_TRANSACTION,
    *,
    compare: str = "value",
    default: object = MISSING,
    default_factory: object = MISSING,
    allow_self_factory: bool = False,
    init: bool = True,
) -> LifecycleMarker:
    """Declare an owned retained BindingBase resource field."""

    return _marker(
        kind="owned",
        default=default,
        default_factory=default_factory,
        working_default_factory=MISSING,
        allow_self_factory=allow_self_factory,
        init=init,
        tx_key=tx_key,
        compare=compare,
    )


def binding(
    *,
    default: object = MISSING,
    default_factory: object = MISSING,
    allow_self_factory: bool = False,
    init: bool = True,
) -> LifecycleMarker:
    """Declare a plain stored BindingBase resource field."""

    return _marker(
        kind="binding",
        default=default,
        default_factory=default_factory,
        working_default_factory=MISSING,
        allow_self_factory=allow_self_factory,
        init=init,
        tx_key=MISSING,
    )


def local_store(
    *,
    default: object = MISSING,
    default_factory: object = MISSING,
    **unsupported: object,
) -> LifecycleMarker:
    """Declare non-transactional lifecycle-owned scratch storage."""

    if unsupported:
        name = next(iter(unsupported))
        raise LifecycleDefinitionError(f"local_store does not support {name}")
    return _marker(
        kind="local_store",
        default=default,
        default_factory=default_factory,
        working_default_factory=MISSING,
        allow_self_factory=False,
        init=False,
        tx_key=MISSING,
    )


def transient(
    tx_key: object = DEFAULT_TRANSACTION,
    *,
    compare: str = "value",
    default: object = MISSING,
    default_factory: object = MISSING,
    allow_self_factory: bool = False,
    working_default_factory: object = MISSING,
    init: bool = True,
) -> LifecycleMarker:
    """Declare a transient lifecycle field with a tx-local working overlay."""

    return _marker(
        kind="transient",
        default=default,
        default_factory=default_factory,
        working_default_factory=working_default_factory,
        allow_self_factory=allow_self_factory,
        init=init,
        tx_key=tx_key,
        compare=compare,
    )


def commit_order_key(
    *args: object,
    tx_key: object = MISSING,
) -> object:
    """Mark a method as the commit-order key provider for a transaction key."""

    return _transaction_method_marker("commit_order_key", *args, tx_key=tx_key)


def validate_commit(
    *args: object,
    tx_key: object = MISSING,
) -> object:
    """Mark a method as a commit validator for a transaction key."""

    return _transaction_method_marker("validate_commit", *args, tx_key=tx_key)


def before_commit(
    *args: object,
    tx_key: object = MISSING,
) -> object:
    """Mark a method as a before-commit hook for a transaction key."""

    return _transaction_method_marker("before_commit", *args, tx_key=tx_key)


def after_commit(
    *args: object,
    tx_key: object = MISSING,
) -> object:
    """Mark a method as an after-commit hook for a transaction key."""

    return _transaction_method_marker("after_commit", *args, tx_key=tx_key)


def after_rollback(
    *args: object,
    tx_key: object = MISSING,
) -> object:
    """Mark a method as an after-rollback hook for a transaction key."""

    return _transaction_method_marker("after_rollback", *args, tx_key=tx_key)


def transaction_method_markers(value: object) -> tuple[TransactionMethodMarker, ...]:
    """Return transaction method markers attached to ``value``."""

    markers = getattr(value, _TRANSACTION_METHOD_MARKERS_ATTR, ())
    if not isinstance(markers, tuple):
        raise LifecycleDefinitionError("transaction method marker metadata is invalid")
    for marker in markers:
        if not isinstance(marker, TransactionMethodMarker):
            raise LifecycleDefinitionError(
                "transaction method marker metadata is invalid"
            )
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
            _message(
                context, name, f"expected lifecycle marker, got {type(marker).__name__}"
            ),
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
        allow_self_factory=marker.allow_self_factory,
        has_working_default_factory=marker.working_default_factory is not MISSING,
        working_default_factory=marker.working_default_factory,
        tx_key=(
            DEFAULT_TRANSACTION
            if marker.kind in {"managed", "owned", "transient"}
            and marker.tx_key is MISSING
            else marker.tx_key
        ),
        has_freeze=marker.freeze is not MISSING,
        freeze=marker.freeze,
        has_thaw=marker.thaw is not MISSING,
        thaw=marker.thaw,
    )


def _marker(
    *,
    kind: str,
    default: object,
    default_factory: object,
    working_default_factory: object,
    allow_self_factory: bool,
    init: bool,
    tx_key: object,
    compare: str = "value",
    freeze: object = MISSING,
    thaw: object = MISSING,
) -> LifecycleMarker:
    if default is not MISSING and default_factory is not MISSING:
        raise LifecycleDefinitionError(
            "cannot specify both default and default_factory"
        )
    if not isinstance(init, bool):
        raise LifecycleDefinitionError("init must be a bool")
    if not isinstance(allow_self_factory, bool):
        raise LifecycleDefinitionError("allow_self_factory must be a bool")
    if compare not in {"value", "identity"}:
        raise LifecycleDefinitionError("compare must be 'value' or 'identity'")
    if default_factory is not MISSING and not callable(default_factory):
        raise LifecycleDefinitionError("default_factory must be callable")
    if working_default_factory is not MISSING and not callable(working_default_factory):
        raise LifecycleDefinitionError("working_default_factory must be callable")
    if working_default_factory is not MISSING and kind != "transient":
        raise LifecycleDefinitionError(
            "working_default_factory is only valid for transient fields",
        )
    if freeze is not MISSING and not callable(freeze):
        raise LifecycleDefinitionError("freeze must be callable")
    if thaw is not MISSING and not callable(thaw):
        raise LifecycleDefinitionError("thaw must be callable")
    if kind != "managed" and (freeze is not MISSING or thaw is not MISSING):
        raise LifecycleDefinitionError(
            "freeze and thaw are only valid for managed fields"
        )
    return LifecycleMarker(
        kind=kind,
        default=default,
        default_factory=default_factory,
        working_default_factory=working_default_factory,
        allow_self_factory=allow_self_factory,
        init=init,
        tx_key=tx_key,
        compare=compare,
        freeze=freeze,
        thaw=thaw,
    )


def _transaction_method_marker(
    kind: str,
    *args: object,
    tx_key: object,
) -> object:
    if len(args) > 1:
        raise LifecycleDefinitionError("unsupported transaction marker call shape")
    if args and tx_key is not MISSING:
        raise LifecycleDefinitionError("unsupported transaction marker call shape")
    if args:
        selected_tx_key = args[0]
        if callable(selected_tx_key):
            raise LifecycleDefinitionError(
                "transaction method marker requires an explicit transaction key",
            )
    else:
        selected_tx_key = DEFAULT_TRANSACTION if tx_key is MISSING else tx_key

    def decorate(target: object) -> object:
        if not callable(target):
            raise LifecycleDefinitionError(
                "transaction method marker target must be callable",
            )
        existing = transaction_method_markers(target)
        setattr(
            target,
            _TRANSACTION_METHOD_MARKERS_ATTR,
            (*existing, TransactionMethodMarker(kind, selected_tx_key)),
        )
        return target

    return decorate


def _validate_name(name: str, *, context: str | None) -> None:
    if not name:
        raise LifecycleDefinitionError(
            _message(context, name, "field name is required")
        )
    if name.startswith("_y_") or (name.startswith("__yidl_") and name.endswith("__")):
        raise LifecycleDefinitionError(
            _message(context, name, "field name uses a reserved lifecycle prefix"),
        )


def _message(context: str | None, name: str, detail: str) -> str:
    prefix = f"{context}.{name}" if context else name
    return f"{prefix}: {detail}" if prefix else detail
