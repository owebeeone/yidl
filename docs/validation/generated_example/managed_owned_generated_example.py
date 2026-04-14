"""Hand-curated generated managed-owned example for PRE_IMPL validation."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from yidl.runtime import DEFAULT_TRANSACTION
from yidl.runtime import TransactionManager


MISSING = object()


class YidlCantWriteWithoutActiveTransaction(RuntimeError):
    pass


class SpyBinding:
    """Validation-only ref-counted binding with lifecycle-like semantics."""

    def __init__(self, label: str) -> None:
        self.label = label
        self.ref_count = 1
        self.is_accepted = False
        self.is_closed = False
        self.closed_states: list[bool] = []

    def inc_ref(self) -> None:
        if self.is_closed or self.ref_count <= 0:
            raise RuntimeError("cannot retain a closed binding")
        self.ref_count += 1

    def accepted(self) -> None:
        if self.is_closed:
            raise RuntimeError("cannot accept a closed binding")
        self.is_accepted = True

    def dec_ref(self) -> None:
        if self.ref_count <= 0:
            raise AssertionError("dec_ref called without a matching inc_ref")
        self.ref_count -= 1
        if self.ref_count == 0:
            if self.is_closed:
                raise AssertionError("binding closed more than once")
            self.is_closed = True
            self._close()

    def _close(self) -> None:
        self.closed_states.append(self.is_accepted)


class OwnedSource:
    """User-declared source shape before YIDL code generation."""

    child: SpyBinding | None


@dataclass(frozen=True)
class YidlFieldMeta:
    public_name: str
    tx_group: str
    kind: str


class YidlFieldState:
    __slots__ = ("working_value", "working_tx_id")

    def __init__(self) -> None:
        self.working_value: SpyBinding | None | object = MISSING
        self.working_tx_id: int | None = None


class YidlState:
    __slots__ = ("transaction_manager", "field_meta", "owned_child")

    def __init__(self, *, transaction_manager: TransactionManager) -> None:
        self.transaction_manager = transaction_manager
        self.field_meta = {
            "child": YidlFieldMeta(
                public_name="child",
                tx_group=DEFAULT_TRANSACTION,
                kind="owned",
            ),
        }
        self.owned_child = YidlFieldState()


def build_generated_owned_context(source_cls: type = OwnedSource) -> type:
    """Generate the proxy and child surfaces for the validation example."""

    del source_cls
    field_name = "child"

    class _CurrentView:
        __slots__ = ("_owner",)

        def __init__(self, owner: Any) -> None:
            self._owner = owner

        @property
        def child(self) -> SpyBinding | None:
            return self._owner._current_child

    class _WorkingView:
        __slots__ = ("_owner",)

        def __init__(self, owner: Any) -> None:
            self._owner = owner

        @property
        def child(self) -> SpyBinding | None:
            field_state = self._owner._yidl_state.owned_child
            if field_state.working_value is not MISSING:
                return field_state.working_value
            return self._owner._current_child

        @child.setter
        def child(self, value: SpyBinding | None) -> None:
            self._owner._stage_owned_value(value)

    class GeneratedOwnedContext:
        __slots__ = (
            "_current_child",
            "_deferred_commit_cleanup",
            "_yidl_state",
            "current",
            "working",
        )

        def __init__(
            self,
            *,
            transaction_manager: TransactionManager,
            child: SpyBinding | None = None,
        ) -> None:
            self._current_child = child
            self._deferred_commit_cleanup: list[tuple[SpyBinding, str]] = []
            self._yidl_state = YidlState(transaction_manager=transaction_manager)
            self.current = _CurrentView(self)
            self.working = _WorkingView(self)

            if child is not None:
                child.accepted()

        def _field_meta(self) -> YidlFieldMeta:
            return self._yidl_state.field_meta[field_name]

        def _field_state(self) -> YidlFieldState:
            return self._yidl_state.owned_child

        def _active_tx_id(self) -> int:
            meta = self._field_meta()
            tx = self._yidl_state.transaction_manager.active_transaction_for(meta.tx_group)
            if tx is None:
                raise YidlCantWriteWithoutActiveTransaction(meta.public_name)
            return tx.tx_id

        def _ensure_enlisted(self, tx_id: int) -> None:
            field_state = self._field_state()
            if field_state.working_tx_id == tx_id:
                return
            self._yidl_state.transaction_manager.enlist(self, self._field_meta().tx_group)
            field_state.working_tx_id = tx_id

        def _stage_owned_value(self, value: SpyBinding | None) -> None:
            tx_id = self._active_tx_id()
            self._ensure_enlisted(tx_id)

            field_state = self._field_state()
            visible = field_state.working_value if field_state.working_value is not MISSING else self._current_child
            if visible is value:
                return

            field_state.working_value = value

        @property
        def child(self) -> SpyBinding | None:
            tx = self._yidl_state.transaction_manager.active_transaction_for(DEFAULT_TRANSACTION)
            if tx is not None and self._field_state().working_tx_id == tx.tx_id:
                return self.working.child
            return self.current.child

        @child.setter
        def child(self, value: SpyBinding | None) -> None:
            self.working.child = value

        def commit_order_key_for(self, tx_group: str = DEFAULT_TRANSACTION) -> tuple[object, ...]:
            del tx_group
            return ()

        def requires_validation_for(self, tx_group: str = DEFAULT_TRANSACTION) -> bool:
            del tx_group
            return False

        def validate_commit_for(self, tx_group: str = DEFAULT_TRANSACTION) -> bool:
            del tx_group
            return True

        def _commit_transaction(self, tx_id: int, tx_group: str = DEFAULT_TRANSACTION) -> object:
            meta = self._field_meta()
            field_state = self._field_state()
            if tx_group != meta.tx_group or field_state.working_tx_id != tx_id:
                return self.current

            next_value = field_state.working_value
            current = self._current_child
            if next_value is MISSING:
                field_state.working_tx_id = None
                return self.current

            if next_value is not None and next_value is not current:
                next_value.accepted()
            if current is not None and current is not next_value:
                self._deferred_commit_cleanup.append((current, "dec_ref"))

            self._current_child = next_value
            field_state.working_value = MISSING
            field_state.working_tx_id = None

            pending = list(self._deferred_commit_cleanup)
            self._deferred_commit_cleanup.clear()
            for binding, op_name in pending:
                getattr(binding, op_name)()
            return self.current

        def _rollback_transaction(self, tx_id: int, tx_group: str = DEFAULT_TRANSACTION) -> object:
            meta = self._field_meta()
            field_state = self._field_state()
            if tx_group != meta.tx_group or field_state.working_tx_id != tx_id:
                return self.current

            staged = field_state.working_value
            current = self._current_child
            if staged is not MISSING and staged is not None and staged is not current:
                staged.dec_ref()

            field_state.working_value = MISSING
            field_state.working_tx_id = None
            self._deferred_commit_cleanup.clear()
            return self.current

        def close(self) -> None:
            current = self._current_child
            if current is not None:
                current.dec_ref()
                self._current_child = None

    GeneratedOwnedContext.__name__ = "GeneratedOwnedContext"
    return GeneratedOwnedContext
