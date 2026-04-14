from __future__ import annotations

import pytest

from generated_example.managed_owned_generated_example import (
    OwnedSource,
    SpyBinding,
    YidlCantWriteWithoutActiveTransaction,
    build_generated_owned_context,
)
from yidl.runtime import TransactionManager


GeneratedOwnedContext = build_generated_owned_context(OwnedSource)


def test_generated_owned_requires_active_transaction_for_write() -> None:
    txm = TransactionManager()
    ctx = GeneratedOwnedContext(transaction_manager=txm)

    with pytest.raises(YidlCantWriteWithoutActiveTransaction, match="child"):
        ctx.child = SpyBinding("new")


def test_generated_owned_rollback_discards_provisional_value() -> None:
    txm = TransactionManager()
    ctx = GeneratedOwnedContext(transaction_manager=txm)
    binding = SpyBinding("new")

    with txm.begin():
        ctx.child = binding
        assert ctx.child is binding
        assert ctx.current.child is None

    assert ctx.child is binding
    assert binding.is_accepted is True
    assert binding.closed_states == []

    provisional = SpyBinding("provisional")
    txm.begin()
    ctx.child = provisional
    txm.rollback()

    assert ctx.child is binding
    assert provisional.closed_states == [False]


def test_generated_owned_commit_releases_replaced_child() -> None:
    txm = TransactionManager()
    ctx = GeneratedOwnedContext(transaction_manager=txm)
    first = SpyBinding("first")
    second = SpyBinding("second")

    with txm.begin():
        ctx.child = first

    assert ctx.child is first
    assert first.is_accepted is True

    with txm.begin():
        ctx.child = second
        assert ctx.child is second
        assert ctx.current.child is first

    assert ctx.child is second
    assert second.is_accepted is True
    assert first.closed_states == [True]


def test_generated_owned_overwrite_in_one_transaction_releases_only_final_provisional() -> None:
    txm = TransactionManager()
    ctx = GeneratedOwnedContext(transaction_manager=txm)
    first = SpyBinding("first")
    second = SpyBinding("second")

    txm.begin()
    ctx.child = first
    ctx.child = second
    txm.rollback()

    assert first.closed_states == []
    assert second.closed_states == [False]
    assert ctx.child is None


def test_generated_owned_close_releases_committed_child() -> None:
    txm = TransactionManager()
    ctx = GeneratedOwnedContext(transaction_manager=txm)
    child = SpyBinding("child")

    with txm.begin():
        ctx.child = child

    assert child.is_accepted is True
    ctx.close()

    assert child.closed_states == [True]
