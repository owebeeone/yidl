from __future__ import annotations

from dataclasses import dataclass
import pytest

from yidl.runtime.transaction_yidl import DEFAULT_TRANSACTION
from yidl.runtime.transaction_yidl import TransactionManager
from yidl.runtime.transaction_yidl import YidlValidatorReturnedFalse


GROUP_ALPHA = "group_alpha"
GROUP_BETA = "group_beta"


@dataclass(eq=False, slots=True)
class FakeContext:
    name: str
    rank: tuple[object, ...] = ()
    validate_ok: bool = True
    require_validation: bool = False
    committed: list[tuple[int, object]] | None = None
    rolled_back: list[tuple[int, object]] | None = None
    validations: list[object] | None = None
    commit_error: BaseException | None = None
    rollback_error: BaseException | None = None

    def __post_init__(self) -> None:
        if self.committed is None:
            self.committed = []
        if self.rolled_back is None:
            self.rolled_back = []
        if self.validations is None:
            self.validations = []

    def commit_order_key_for(self, tx_group: object = DEFAULT_TRANSACTION) -> tuple[object, ...]:
        del tx_group
        return self.rank

    def requires_validation_for(self, tx_group: object = DEFAULT_TRANSACTION) -> bool:
        del tx_group
        return self.require_validation

    def validate_commit_for(self, tx_group: object = DEFAULT_TRANSACTION) -> bool:
        assert self.validations is not None
        self.validations.append(tx_group)
        return self.validate_ok

    def _commit_transaction(self, tx_id: int, tx_group: object = DEFAULT_TRANSACTION) -> object:
        if self.commit_error is not None:
            raise self.commit_error
        assert self.committed is not None
        self.committed.append((tx_id, tx_group))
        return None

    def _rollback_transaction(self, tx_id: int, tx_group: object = DEFAULT_TRANSACTION) -> object:
        if self.rollback_error is not None:
            raise self.rollback_error
        assert self.rolled_back is not None
        self.rolled_back.append((tx_id, tx_group))
        return None


def test_transaction_manager_commit_and_rollback_require_balanced_begin() -> None:
    manager = TransactionManager()
    with pytest.raises(RuntimeError, match="no active yidl transaction"):
        manager.commit()
    with pytest.raises(RuntimeError, match="no active yidl transaction"):
        manager.rollback()

    manager.begin()
    manager.rollback()
    with pytest.raises(RuntimeError, match="no active yidl transaction"):
        manager.rollback()


def test_transaction_manager_enlist_commit_and_drop() -> None:
    manager = TransactionManager()
    context = FakeContext(name="ctx")

    tx = manager.begin()
    tx_id = manager.enlist(context)
    assert tx.tx_id == tx_id

    manager.drop(context, tx_id)
    assert manager.commit() == tx_id
    assert context.committed == []


def test_transaction_manager_commit_order_is_highest_rank_first() -> None:
    manager = TransactionManager()
    low = FakeContext(name="low", rank=(1,))
    high = FakeContext(name="high", rank=(2,))

    manager.begin()
    manager.enlist(low)
    manager.enlist(high)
    manager.commit()

    assert high.committed == [(1, DEFAULT_TRANSACTION)]
    assert low.committed == [(1, DEFAULT_TRANSACTION)]


def test_transaction_manager_validation_failure_rolls_back_and_resets_manager() -> None:
    manager = TransactionManager()
    context = FakeContext(name="bad", validate_ok=False, require_validation=True)

    manager.begin()
    manager.enlist(context)
    with pytest.raises(ExceptionGroup, match="yidl commit validation failed") as failure:
        manager.commit()

    assert len(failure.value.exceptions) == 1
    assert isinstance(failure.value.exceptions[0], YidlValidatorReturnedFalse)
    assert context.validations == [DEFAULT_TRANSACTION]
    assert context.rolled_back == [(1, DEFAULT_TRANSACTION)]
    assert manager.active_transaction is None
    assert manager.begin_count == 0

    tx2 = manager.begin()
    assert tx2.tx_id == 2


def test_transaction_manager_commit_failure_rolls_back_and_resets_manager() -> None:
    manager = TransactionManager()
    context = FakeContext(name="bad", commit_error=RuntimeError("commit boom"))

    manager.begin()
    manager.enlist(context)
    with pytest.raises(RuntimeError, match="commit boom"):
        manager.commit_only()

    assert context.rolled_back == [(1, DEFAULT_TRANSACTION)]
    assert manager.active_transaction is None
    assert manager.begin_count == 0

    tx2 = manager.begin()
    assert tx2.tx_id == 2


def test_transaction_manager_rollback_failure_resets_manager() -> None:
    manager = TransactionManager()
    context = FakeContext(name="bad", rollback_error=RuntimeError("rollback boom"))

    manager.begin()
    manager.enlist(context)
    with pytest.raises(RuntimeError, match="rollback boom"):
        manager.rollback()

    assert manager.active_transaction is None
    assert manager.begin_count == 0

    tx2 = manager.begin()
    assert tx2.tx_id == 2


def test_group_begin_counts_are_tracked_independently() -> None:
    manager = TransactionManager(tx_groups={GROUP_ALPHA, GROUP_BETA})
    left = FakeContext(name="left")
    right = FakeContext(name="right")

    manager.begin(GROUP_ALPHA)
    manager.begin(GROUP_ALPHA)
    manager.begin(GROUP_BETA)
    manager.enlist(left, GROUP_ALPHA)
    manager.enlist(right, GROUP_BETA)

    assert manager.commit(GROUP_ALPHA) is None
    assert left.committed == []
    assert right.committed == []

    manager.commit(GROUP_BETA)
    assert right.committed == [(1, GROUP_BETA)]

    manager.commit(GROUP_ALPHA)
    assert left.committed == [(1, GROUP_ALPHA)]


def test_multi_group_context_manager_commits_each_group() -> None:
    manager = TransactionManager(tx_groups={GROUP_ALPHA, GROUP_BETA})
    left = FakeContext(name="left")
    right = FakeContext(name="right")

    with manager.begin(GROUP_ALPHA, GROUP_BETA):
        manager.enlist(left, GROUP_ALPHA)
        manager.enlist(right, GROUP_BETA)

    assert left.committed == [(1, GROUP_ALPHA)]
    assert right.committed == [(1, GROUP_BETA)]
