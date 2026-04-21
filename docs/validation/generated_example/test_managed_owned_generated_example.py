from __future__ import annotations

import pytest

from generated_example.managed_owned_generated_example import (
    OwnedSource,
    SpyBinding,
    YidlCantWriteWithoutActiveTransaction,
    build_generated_owned_context,
)
from yidl.runtime import BindingList
from yidl.runtime import TransactionManager


GeneratedOwnedContext = build_generated_owned_context(OwnedSource)


def test_generated_owned_requires_active_transaction_for_write() -> None:
    txm = TransactionManager()
    ctx = GeneratedOwnedContext(transaction_manager=txm)

    with pytest.raises(YidlCantWriteWithoutActiveTransaction, match="child"):
        ctx.child = SpyBinding("new")
    with pytest.raises(YidlCantWriteWithoutActiveTransaction, match="child_list"):
        ctx.child_list = BindingList()


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

    assert first.closed_states == [False]
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


def test_generated_surfaces_inherit_user_base_and_mirror_name() -> None:
    txm = TransactionManager()
    ctx = GeneratedOwnedContext(transaction_manager=txm)

    assert isinstance(ctx, OwnedSource)
    assert isinstance(ctx.current, OwnedSource)
    assert isinstance(ctx.working, OwnedSource)
    assert ctx.__class__.__name__ == OwnedSource.__name__
    assert ctx.current.__class__.__name__ == OwnedSource.__name__
    assert ctx.working.__class__.__name__ == OwnedSource.__name__


def test_user_method_on_proxy_and_views_sees_routed_child() -> None:
    txm = TransactionManager()
    ctx = GeneratedOwnedContext(transaction_manager=txm)
    binding = SpyBinding("alpha")

    assert ctx.describe_child() == "<none>"
    assert ctx.current.describe_child() == "<none>"

    with txm.begin():
        ctx.child = binding
        assert ctx.describe_child() == "alpha"
        assert ctx.current.describe_child() == "<none>"
        assert ctx.working.describe_child() == "alpha"

    assert ctx.describe_child() == "alpha"
    assert ctx.current.describe_child() == "alpha"


def test_generated_owned_child_list_rollback_releases_provisional_children() -> None:
    txm = TransactionManager()
    ctx = GeneratedOwnedContext(transaction_manager=txm)
    left = SpyBinding("left")
    right = SpyBinding("right")

    txm.begin()
    ctx.child_list = BindingList([left, right])
    assert ctx.describe_child_list() == ("left", "right")
    txm.rollback()

    assert ctx.describe_child_list() == ()
    assert left.closed_states == [False]
    assert right.closed_states == [False]


def test_generated_owned_child_list_commit_releases_previous_committed_children() -> None:
    txm = TransactionManager()
    ctx = GeneratedOwnedContext(transaction_manager=txm)
    first = SpyBinding("first")
    second = SpyBinding("second")
    third = SpyBinding("third")

    with txm.begin():
        ctx.child_list = BindingList([first, second])

    assert ctx.describe_child_list() == ("first", "second")
    assert first.is_accepted is True
    assert second.is_accepted is True

    with txm.begin():
        ctx.child_list = BindingList([third])
        assert ctx.describe_child_list() == ("third",)
        assert ctx.current.describe_child_list() == ("first", "second")

    assert ctx.describe_child_list() == ("third",)
    assert first.closed_states == [True]
    assert second.closed_states == [True]
    assert third.is_accepted is True


def test_generated_owned_close_releases_committed_child_list() -> None:
    txm = TransactionManager()
    ctx = GeneratedOwnedContext(transaction_manager=txm)
    left = SpyBinding("left")
    right = SpyBinding("right")

    with txm.begin():
        ctx.child_list = BindingList([left, right])

    ctx.close()

    assert left.closed_states == [True]
    assert right.closed_states == [True]
