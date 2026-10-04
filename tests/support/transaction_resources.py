from __future__ import annotations

from collections.abc import Hashable
from dataclasses import dataclass
from dataclasses import field

DEFAULT_TRANSACTION: Hashable = "default_transaction"


@dataclass(slots=True)
class LifecycleTransaction:
    tx_id: int
    tx_key: Hashable = DEFAULT_TRANSACTION
    dirty_contexts: dict[int, object] = field(default_factory=dict)
    _manager: TransactionManager | None = field(default=None, init=False, repr=False)

    def __enter__(self) -> "LifecycleTransaction":
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc: BaseException | None,
        tb: object,
    ) -> bool:
        del exc, tb
        if exc_type is None:
            self._manager.commit(self.tx_key)
        else:
            self._manager.rollback(self.tx_key)
        return False

    def bind_manager(self, manager: TransactionManager) -> "LifecycleTransaction":
        self._manager = manager
        return self


class TransactionManager:
    """Minimal test-owned transaction manager for YIDL validation fixtures."""

    def __init__(self, *, tx_keys: tuple[Hashable, ...] = ()) -> None:
        self.tx_keys = tx_keys
        self._next_tx_id = 1
        self._active: dict[Hashable, LifecycleTransaction] = {}

    def active_transaction_for(
        self,
        tx_key: Hashable = DEFAULT_TRANSACTION,
    ) -> LifecycleTransaction | None:
        return self._active.get(tx_key)

    def begin(
        self,
        tx_key: Hashable = DEFAULT_TRANSACTION,
    ) -> LifecycleTransaction:
        if tx_key in self._active:
            return self._active[tx_key]
        tx = LifecycleTransaction(self._next_tx_id, tx_key).bind_manager(self)
        self._next_tx_id += 1
        self._active[tx_key] = tx
        return tx

    def enlist(
        self,
        context: object,
        tx_key: Hashable = DEFAULT_TRANSACTION,
    ) -> int:
        tx = self._active.get(tx_key)
        if tx is None:
            raise RuntimeError("no active test transaction")
        tx.dirty_contexts[id(context)] = context
        return tx.tx_id

    def commit(self, tx_key: Hashable = DEFAULT_TRANSACTION) -> int:
        tx = self._require_active(tx_key)
        try:
            for context in sorted(
                tx.dirty_contexts.values(),
                key=lambda item: item.commit_order_key_for(tx_key),
                reverse=True,
            ):
                commit = getattr(context, "_commit_transaction")
                commit(tx.tx_id, tx_key)
            return tx.tx_id
        finally:
            self._active.pop(tx_key, None)

    def rollback(self, tx_key: Hashable = DEFAULT_TRANSACTION) -> int:
        tx = self._require_active(tx_key)
        try:
            for context in tx.dirty_contexts.values():
                rollback = getattr(context, "_rollback_transaction")
                rollback(tx.tx_id, tx_key)
            return tx.tx_id
        finally:
            self._active.pop(tx_key, None)

    def _require_active(self, tx_key: Hashable) -> LifecycleTransaction:
        tx = self._active.get(tx_key)
        if tx is None:
            raise RuntimeError("no active test transaction")
        return tx
