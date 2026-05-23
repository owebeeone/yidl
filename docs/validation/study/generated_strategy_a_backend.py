"""Hand-crafted "generated strategy A" subject — VOID-sentinel MVP shape.

This realises the generated code shape locked in by
``yidl/dev-docs/history/InitStudyResults.md`` (§TL;DR — VOID sentinel) for the
minimal lifecycle scenario exercised by ``scenarios.py``
(``scenario_default_tx_increment``: one managed ``int`` field, one
transaction key, one commit).

The shape deliberately mirrors the split used by
``pyrolyze.lifecycle``: one **facade** class (public surface) bijective
with one **state** object (backing storage + per-tx bookkeeping). What
differs from lifecycle is the init-detection primitive: lifecycle uses
a dict-backed ``Record`` where "unset" is "key not in dict"; this
generated shape uses slotted storage with a module-level ``_VOID``
sentinel per the §Phase 3 init-detection study.

Layout:

- ``Counter`` — facade. ``__slots__ = ("_state",)``; all field access
  goes through generated ``@property`` descriptors that route into the
  bijective state object. Implements the ``TransactionContext``
  protocol from ``yidl.runtime`` so the transaction manager can enlist
  it on writes and call commit/rollback on the facade at tx close.
- ``_CounterState`` — state object bijective with one facade. Holds
  the transaction-manager reference plus per-field ``current_value``
  and ``working_value`` slots, both initialised to ``_VOID`` ("not
  yet written; the default applies"). Identity against ``_VOID`` also
  doubles as the "has working value?" bit — safe because ``_VOID`` is
  module-private and cannot escape user code.

Deferred to later revisions (will force new v1/v2 backends):

- multi-field bodies and cross-field reads during default resolution,
- bulk clear / commit traversal optimisations (bitmask etc. —
  `InitStudyResults.md` §Phase 3 remains available once a real workload
  justifies a second look),
- ``derived`` / ``local_store`` / ``owned`` / ``binding`` kinds,
- non-default transaction keys, multi-group commit,
- close / on_before_commit / on_after_commit hooks.
"""

from __future__ import annotations

from collections.abc import Hashable
from typing import Any, Final

from study.contract import StudySubject
from yidl.runtime import DEFAULT_TRANSACTION, TransactionManager


_VOID: Final[Any] = object()
"""'Slot not yet initialised' sentinel. Identity comparison (``is _VOID``)
is the init-detection check per ``InitStudyResults.md`` §TL;DR.

Module-private: user code never sees or passes this value, so using
VOID-identity to encode both "field not yet defaulted" and "no working
value staged" collapses two booleans into one slot read."""


class YidlCantWriteWithoutActiveTransaction(RuntimeError):
    """Raised when a managed field is written outside an active
    transaction. Matches the semantic used by the pre-existing
    ``managed_owned_generated_example.py`` so harness-level error
    handling is uniform across generated examples."""


def _counter_default_value(state: "_CounterState") -> int:
    """Default factory for ``Counter.value`` (equivalent to
    ``managed(default=0)`` on the lifecycle side)."""
    del state
    return 0


class _CounterState:
    __slots__ = (
        "transaction_manager",
        "current_value",
        "working_value",
        "working_tx_id",
    )

    def __init__(self, transaction_manager: TransactionManager) -> None:
        self.transaction_manager = transaction_manager
        self.current_value: Any = _VOID
        self.working_value: Any = _VOID
        self.working_tx_id: int | None = None


class Counter:
    __slots__ = ("_state",)

    def __init__(
        self,
        *,
        transaction_manager: TransactionManager,
        value: Any = _VOID,
    ) -> None:
        self._state = _CounterState(transaction_manager)
        if value is not _VOID:
            self._state.current_value = value

    @property
    def value(self) -> Any:
        s = self._state
        tx = s.transaction_manager.active_transaction_for(DEFAULT_TRANSACTION)
        if (
            tx is not None
            and s.working_tx_id == tx.tx_id
            and s.working_value is not _VOID
        ):
            return s.working_value
        cur = s.current_value
        if cur is _VOID:
            cur = _counter_default_value(s)
            s.current_value = cur
        return cur

    @value.setter
    def value(self, value: Any) -> None:
        s = self._state
        tx = s.transaction_manager.active_transaction_for(DEFAULT_TRANSACTION)
        if tx is None:
            raise YidlCantWriteWithoutActiveTransaction("value")
        if s.working_tx_id != tx.tx_id:
            s.transaction_manager.enlist(self, DEFAULT_TRANSACTION)
            s.working_tx_id = tx.tx_id
        s.working_value = value

    def commit_order_key_for(
        self, tx_key: Hashable = DEFAULT_TRANSACTION
    ) -> tuple[object, ...]:
        del tx_key
        return ()

    def requires_validation_for(
        self, tx_key: Hashable = DEFAULT_TRANSACTION
    ) -> bool:
        del tx_key
        return False

    def validate_commit_for(
        self, tx_key: Hashable = DEFAULT_TRANSACTION
    ) -> bool:
        del tx_key
        return True

    def _commit_transaction(
        self, tx_id: int, tx_key: Hashable = DEFAULT_TRANSACTION
    ) -> "Counter":
        del tx_key
        s = self._state
        if s.working_tx_id != tx_id:
            return self
        if s.working_value is not _VOID:
            s.current_value = s.working_value
        s.working_value = _VOID
        s.working_tx_id = None
        return self

    def _rollback_transaction(
        self, tx_id: int, tx_key: Hashable = DEFAULT_TRANSACTION
    ) -> "Counter":
        del tx_key
        s = self._state
        if s.working_tx_id != tx_id:
            return self
        s.working_value = _VOID
        s.working_tx_id = None
        return self


class GeneratedStrategyACounterSubject(StudySubject):
    def __init__(self) -> None:
        super().__init__(name="generated_strategy_a")

    def build_class(self) -> type:
        return Counter

    def build_transaction_manager(self) -> Any:
        return TransactionManager()
