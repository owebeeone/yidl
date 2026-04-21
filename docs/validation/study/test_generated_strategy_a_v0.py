"""Focused tests for the generated-strategy-A v0 Counter.

Covers paths beyond ``scenario_default_tx_increment`` (which only
checks the happy single-write/commit flow):

- VOID-sentinel lazy default materialisation on first read,
- read-through precedence of working over current inside an active tx,
- commit promotes working to current and clears working state,
- rollback (via propagated exception) discards working and leaves
  current untouched,
- writes without an active transaction raise,
- constructor-time seeding bypasses the default factory.

These tests assert against ``Counter._state`` internals where useful to
pin the backing invariant (e.g. ``working_value is _VOID`` after
commit). That's acceptable because the generated-strategy-A backend is
validation-only; the invariants tested here are exactly what any
future generator must preserve.
"""

from __future__ import annotations

import pytest

from study.generated_strategy_a_backend import (
    Counter,
    YidlCantWriteWithoutActiveTransaction,
    _VOID,
)
from yidl.runtime import TransactionManager


def _make() -> Counter:
    return Counter(transaction_manager=TransactionManager())


def test_default_on_first_read() -> None:
    c = _make()
    assert c._state.current_value is _VOID
    assert c.value == 0


def test_default_is_materialised_after_first_read() -> None:
    c = _make()
    assert c.value == 0
    assert c._state.current_value == 0


def test_write_without_transaction_raises() -> None:
    c = _make()
    with pytest.raises(YidlCantWriteWithoutActiveTransaction):
        c.value = 1


def test_read_through_prefers_working_during_tx() -> None:
    c = _make()
    txm = c._state.transaction_manager
    with txm.begin():
        c.value = 5
        assert c.value == 5


def test_commit_promotes_working_to_current() -> None:
    c = _make()
    txm = c._state.transaction_manager
    with txm.begin():
        c.value = 7
    assert c.value == 7
    assert c._state.current_value == 7
    assert c._state.working_value is _VOID
    assert c._state.working_tx_id is None


def test_rollback_discards_working() -> None:
    c = _make()
    txm = c._state.transaction_manager
    with pytest.raises(RuntimeError, match="abort"):
        with txm.begin():
            c.value = 7
            raise RuntimeError("abort")
    assert c.value == 0
    assert c._state.current_value == 0
    assert c._state.working_value is _VOID
    assert c._state.working_tx_id is None


def test_constructor_time_seed_skips_default() -> None:
    c = Counter(transaction_manager=TransactionManager(), value=99)
    assert c._state.current_value == 99
    assert c.value == 99


def test_second_tx_sees_first_committed_value() -> None:
    c = _make()
    txm = c._state.transaction_manager
    with txm.begin():
        c.value = 3
    with txm.begin():
        assert c.value == 3
        c.value = 11
    assert c.value == 11
