"""Lifecycle example exercising every `pyrolyze.lifecycle` surface.

Covers the 15 concrete ``LCKind`` helpers plus managed-class inheritance,
two ``tx_group``\\s (``Key1``, ``Key2``), initvars in both ``init=True`` and
``init=False`` flavours, a ``default_factory`` that consumes an initvar, and a
``managed`` field using ``freeze=/thaw=``/``initial_working=``.

A small ``__main__`` scenario drives two transactions end-to-end so the shape
is proven to decorate, construct, and cycle through commit and rollback.
"""

from __future__ import annotations

from pyrolyze.lifecycle import (
    managed, managed_context, local_store, const, static, derived, owned,
    transient, binding, initvar, classvar, commit_order_key, commit_validator,
    on_before_commit, on_after_commit, on_after_rollback,
    TransactionManager,
)


Key1: str = "key1"
Key2: str = "key2"


# ---- non-managed resource stubs used by binding / owned -----------------

class Handle:
    """Identity-compared resource used by ``binding`` / ``owned`` fields."""

    __slots__ = ("label", "closed")

    def __init__(self, label: str) -> None:
        self.label = label
        self.closed = False

    def close(self) -> None:
        self.closed = True


# ---- module-level callables used as lifecycle defaults ------------------

def _seeded_items_factory(self, seed: int) -> list[int]:
    """``default_factory`` consuming ``self`` + an initvar by name."""
    del self
    return [seed]


def _validate_key1_commit(self, salt: int) -> bool:
    """Commit validator reading an ``init=False`` initvar."""
    return self.key1_total >= 0 and salt >= 0


def _before_commit_key1(self, working, tx_group) -> None:
    self.audit_log.append(("before_commit", tx_group, working.key1_total))


def _after_commit_key1(self, previous, current, tx_group) -> None:
    self.audit_log.append(
        ("after_commit", tx_group, previous.key1_total, current.key1_total)
    )


def _after_rollback_key1(self, current, tx_group) -> None:
    self.audit_log.append(("after_rollback", tx_group, current.key1_total))


def _after_commit_key2(self, previous, current, tx_group) -> None:
    self.audit_log.append(("after_commit", tx_group, current.key2_total))


# ---- nested managed context ---------------------------------------------

@managed_context
class Counter:
    value: int = managed(default=0)

    def increment(self) -> None:
        self.value += 1

    def get_value(self) -> int:
        return self.value


# ---- inheritance: base + derived managed contexts -----------------------

@managed_context
class BaseMultiTxMultiCounter:
    """Base class: the two per-group totals that hooks/validators read."""

    key1_total: int = managed(default=0, tx_group=Key1)
    key2_total: int = managed(default=0, tx_group=Key2)


@managed_context
class MultiTxMultiCounter(BaseMultiTxMultiCounter):
    # managed with overlay knobs: freeze/thaw and initial_working
    items: tuple[int, ...] = managed(
        default_factory=tuple, freeze=tuple, thaw=list, tx_group=Key1,
    )
    first_pass: bool = managed(default=False, initial_working=True, tx_group=Key1)

    # initvars: constructor-provided and factory-provided
    seed: int = initvar(default=0)
    salt: int = initvar(init=False, default_factory=lambda cls: 7)

    # default_factory that pulls in an initvar by parameter name
    seeded_items: list[int] = managed(
        default_factory=_seeded_items_factory, tx_group=Key1,
    )

    # const / static / classvar
    label: str = const(default="mtx")
    declared_at: tuple[str, ...] = static(default_factory=tuple)
    schema_version: int = classvar(default=1)

    # non-transactional store
    audit_log: list[tuple] = local_store(default_factory=list)

    # derived value (cached; reset on commit/rollback/close)
    derived_key1: int = derived(default_factory=lambda self: self.key1_total * 2)

    # transient scratch with working-only factory
    key1_scratch: list[int] | None = transient(
        default=None, working_default_factory=list, tx_group=Key1,
    )

    # binding / owned identity-compared resources
    handle: Handle | None = binding(default=None, tx_group=Key1)
    child: Handle | None = owned(default=None, tx_group=Key2)

    # per-group commit metadata (at most one order_key / validator per group)
    key1_order: tuple[int, ...] = commit_order_key(default=(1,), tx_group=Key1)
    key2_order: tuple[int, ...] = commit_order_key(default=(2,), tx_group=Key2)
    key1_validator: object | None = commit_validator(
        default=_validate_key1_commit, tx_group=Key1,
    )

    # hooks per group (before commit, after commit, after rollback)
    key1_before: object | None = on_before_commit(
        default=_before_commit_key1, tx_group=Key1,
    )
    key1_after: object | None = on_after_commit(
        default=_after_commit_key1, tx_group=Key1,
    )
    key1_rollback: object | None = on_after_rollback(
        default=_after_rollback_key1, tx_group=Key1,
    )
    key2_after: object | None = on_after_commit(
        default=_after_commit_key2, tx_group=Key2,
    )

    # drivers
    def increment_key1(self) -> None:
        self.key1_total += 1
        if self.key1_scratch is not None:
            self.key1_scratch.append(self.key1_total)

    def increment_key2(self) -> None:
        self.key2_total += 1


if __name__ == "__main__":
    manager = TransactionManager(tx_groups={Key1, Key2})
    ctx = MultiTxMultiCounter(
        transaction_manager=manager,
        seed=5,
        handle=Handle("h1"),
        child=Handle("c1"),
    )

    # const / classvar / seeded_items resolved at construction time
    assert ctx.label == "mtx"
    assert MultiTxMultiCounter.schema_version == 1
    assert ctx.seeded_items == [5]

    # drive Key1: before/after commit hooks and validator fire, derived clears
    with manager.begin(Key1):
        ctx.increment_key1()
        ctx.increment_key1()
    assert ctx.key1_total == 2

    # drive Key2: roll back; after-rollback path is Key1-only so Key2 stays quiet
    try:
        with manager.begin(Key2):
            ctx.increment_key2()
            raise RuntimeError("rollback key2")
    except RuntimeError:
        pass
    assert ctx.key2_total == 0

    # force a Key1 rollback too
    try:
        with manager.begin(Key1):
            ctx.increment_key1()
            raise RuntimeError("rollback key1")
    except RuntimeError:
        pass
    assert ctx.key1_total == 2

    tags = [row[0] for row in ctx.audit_log]
    assert "before_commit" in tags
    assert "after_commit" in tags
    assert "after_rollback" in tags
    print("lifecycle example exercised successfully:")
    for row in ctx.audit_log:
        print(" ", row)
