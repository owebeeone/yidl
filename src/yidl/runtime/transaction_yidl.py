from __future__ import annotations

from collections.abc import Callable
from collections.abc import Hashable
from collections.abc import Iterable
from dataclasses import dataclass
from dataclasses import field
from typing import Protocol
from typing import TypeAlias


DEFAULT_TRANSACTION: Hashable = "default_transaction"


class TransactionContext(Protocol):
    def commit_order_key_for(self, tx_group: Hashable = DEFAULT_TRANSACTION) -> tuple[object, ...]:
        ...

    def requires_validation_for(self, tx_group: Hashable = DEFAULT_TRANSACTION) -> bool:
        ...

    def validate_commit_for(self, tx_group: Hashable = DEFAULT_TRANSACTION) -> bool:
        ...

    def _prepare_commit_tx_by_key(
        self,
        tx_group: Hashable = DEFAULT_TRANSACTION,
        tx_token: int | None = None,
    ) -> object:
        ...

    def _apply_prepared_commit_tx_by_key(
        self,
        tx_group: Hashable = DEFAULT_TRANSACTION,
        tx_token: int | None = None,
    ) -> object:
        ...

    def _after_commit_tx_by_key(
        self,
        tx_group: Hashable = DEFAULT_TRANSACTION,
        tx_token: int | None = None,
    ) -> object:
        ...

    def _rollback_tx_by_key(
        self,
        tx_group: Hashable = DEFAULT_TRANSACTION,
        tx_token: int | None = None,
    ) -> object:
        ...

    def _after_rollback_tx_by_key(
        self,
        tx_group: Hashable = DEFAULT_TRANSACTION,
        tx_token: int | None = None,
    ) -> object:
        ...


class YidlValidatorReturnedFalse(RuntimeError):
    """Raised when a context's validate_commit hook returns False."""

    def __init__(self, context: TransactionContext) -> None:
        self.context = context
        super().__init__(
            f"validate_commit returned False for {type(context).__qualname__!r}",
        )


@dataclass(slots=True)
class LifecycleTransaction:
    tx_id: int
    tx_group: Hashable = DEFAULT_TRANSACTION
    dirty_contexts: dict[int, TransactionContext] = field(default_factory=dict)
    validator_contexts: dict[int, TransactionContext] = field(default_factory=dict)
    _scope_commit: Callable[[], object] | None = field(default=None, init=False, repr=False, compare=False)
    _scope_rollback: Callable[[], object] | None = field(default=None, init=False, repr=False, compare=False)

    def commit_order(self) -> tuple[TransactionContext, ...]:
        contexts = list(self.dirty_contexts.values())
        contexts.sort(key=lambda context: context.commit_order_key_for(self.tx_group), reverse=True)
        return tuple(contexts)

    def rollback_dirty(self) -> None:
        for context in list(self.dirty_contexts.values()):
            context._rollback_tx_by_key(self.tx_group, self.tx_id)

    def after_rollbacks(self) -> None:
        for context in list(self.dirty_contexts.values()):
            context._after_rollback_tx_by_key(self.tx_group, self.tx_id)

    def validate_commit(self) -> None:
        failures: list[BaseException] = []
        for context in self.validator_contexts.values():
            try:
                ok = context.validate_commit_for(self.tx_group)
            except BaseException as exc:
                failures.append(exc)
                continue
            if not ok:
                failures.append(YidlValidatorReturnedFalse(context))
        if failures:
            raise ExceptionGroup("yidl commit validation failed", failures)

    def prepare_commits(self) -> None:
        for context in self.commit_order():
            context._prepare_commit_tx_by_key(self.tx_group, self.tx_id)

    def apply_prepared_commits(self) -> None:
        for context in self.commit_order():
            context._apply_prepared_commit_tx_by_key(self.tx_group, self.tx_id)

    def after_commits(self) -> None:
        for context in self.commit_order():
            context._after_commit_tx_by_key(self.tx_group, self.tx_id)

    def bind_scope(
        self,
        *,
        commit: Callable[[], object],
        rollback: Callable[[], object],
    ) -> "LifecycleTransaction":
        self._scope_commit = commit
        self._scope_rollback = rollback
        return self

    def __enter__(self) -> "LifecycleTransaction":
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc: BaseException | None,
        tb: object,
    ) -> bool:
        del exc, tb
        if self._scope_commit is None or self._scope_rollback is None:
            raise RuntimeError("yidl transaction scope is not bound")
        if exc_type is None:
            self._scope_commit()
        else:
            self._scope_rollback()
        return False


@dataclass(slots=True)
class GroupTransactionManager:
    tx_group: Hashable = DEFAULT_TRANSACTION
    _next_tx_id: int = field(default=1, init=False, repr=False)
    active_transaction: LifecycleTransaction | None = field(default=None, init=False, repr=False)
    begin_count: int = field(default=0, init=False, repr=False)

    def active_transaction_for(self, tx_group: Hashable = DEFAULT_TRANSACTION) -> LifecycleTransaction | None:
        if tx_group != self.tx_group:
            raise RuntimeError(f"unknown yidl transaction group {tx_group!r}")
        return self.active_transaction

    def begin(self, tx_group: Hashable = DEFAULT_TRANSACTION) -> LifecycleTransaction:
        if tx_group != self.tx_group:
            raise RuntimeError(f"unknown yidl transaction group {tx_group!r}")
        if self.begin_count == 0:
            if self.active_transaction is not None:
                raise RuntimeError("yidl transaction manager state is corrupted")
            self.active_transaction = LifecycleTransaction(tx_id=self._next_tx_id, tx_group=self.tx_group)
            self._next_tx_id += 1
        self.begin_count += 1
        transaction = self.active_transaction
        assert transaction is not None
        return transaction.bind_scope(
            commit=lambda: self.commit(self.tx_group),
            rollback=lambda: self.rollback(self.tx_group),
        )

    def validate(self, tx_group: Hashable = DEFAULT_TRANSACTION) -> None:
        if tx_group != self.tx_group:
            raise RuntimeError(f"unknown yidl transaction group {tx_group!r}")
        if self.begin_count <= 0:
            raise RuntimeError("no active yidl transaction")
        transaction = self.active_transaction
        if transaction is None:
            raise RuntimeError("yidl transaction manager state is corrupted")
        transaction.validate_commit()

    def commit_only(self, tx_group: Hashable = DEFAULT_TRANSACTION) -> int | None:
        if tx_group != self.tx_group:
            raise RuntimeError(f"unknown yidl transaction group {tx_group!r}")
        if self.begin_count <= 0:
            raise RuntimeError("no active yidl transaction")
        if self.begin_count > 1:
            self.begin_count -= 1
            return None
        transaction = self.active_transaction
        if transaction is None:
            raise RuntimeError("yidl transaction manager state is corrupted")
        tx_id = transaction.tx_id
        try:
            try:
                transaction.prepare_commits()
            except BaseException:
                transaction.rollback_dirty()
                transaction.after_rollbacks()
                raise
            transaction.apply_prepared_commits()
            transaction.after_commits()
        finally:
            self.active_transaction = None
            self.begin_count = 0
        return tx_id

    def commit(self, tx_group: Hashable = DEFAULT_TRANSACTION) -> int | None:
        if tx_group != self.tx_group:
            raise RuntimeError(f"unknown yidl transaction group {tx_group!r}")
        if self.begin_count <= 0:
            raise RuntimeError("no active yidl transaction")
        if self.begin_count > 1:
            self.begin_count -= 1
            return None
        try:
            self.validate(tx_group)
        except BaseException:
            self.rollback(tx_group)
            raise
        return self.commit_only(tx_group)

    def rollback(self, tx_group: Hashable = DEFAULT_TRANSACTION) -> int | None:
        if tx_group != self.tx_group:
            raise RuntimeError(f"unknown yidl transaction group {tx_group!r}")
        if self.begin_count <= 0 or self.active_transaction is None:
            raise RuntimeError("no active yidl transaction")
        transaction = self.active_transaction
        tx_id = transaction.tx_id
        try:
            transaction.rollback_dirty()
            transaction.after_rollbacks()
        finally:
            self.active_transaction = None
            self.begin_count = 0
        return tx_id

    def enlist(self, context: TransactionContext, tx_group: Hashable = DEFAULT_TRANSACTION) -> int:
        if tx_group != self.tx_group:
            raise RuntimeError(f"unknown yidl transaction group {tx_group!r}")
        transaction = self.active_transaction
        if transaction is None:
            raise RuntimeError("no active yidl transaction")
        context_id = id(context)
        transaction.dirty_contexts[context_id] = context
        if context.requires_validation_for(tx_group):
            transaction.validator_contexts[context_id] = context
        return transaction.tx_id

    def drop(
        self,
        context: TransactionContext,
        tx_id: int | None = None,
        tx_group: Hashable = DEFAULT_TRANSACTION,
    ) -> None:
        if tx_group != self.tx_group:
            raise RuntimeError(f"unknown yidl transaction group {tx_group!r}")
        transaction = self.active_transaction
        if transaction is None:
            return
        if tx_id is not None and transaction.tx_id != tx_id:
            return
        context_id = id(context)
        transaction.dirty_contexts.pop(context_id, None)
        transaction.validator_contexts.pop(context_id, None)


@dataclass(slots=True, frozen=True)
class _MultiGroupTransactionScope:
    manager: "TransactionManager"
    groups: tuple[Hashable, ...]

    def __enter__(self) -> "_MultiGroupTransactionScope":
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc: BaseException | None,
        tb: object,
    ) -> bool:
        del exc, tb
        if exc_type is None:
            self.manager.commit(*reversed(self.groups))
        else:
            self.manager.rollback(*reversed(self.groups))
        return False


CommitResult: TypeAlias = int | tuple[int | None, ...] | None


class TransactionManager:
    __slots__ = ("_tx_groups", "_tx_group_set", "_group_managers")

    def __init__(self, *, tx_groups: Iterable[Hashable] = ()) -> None:
        normalized_groups: list[Hashable] = []
        seen = {DEFAULT_TRANSACTION}
        for group in tx_groups:
            if group in seen:
                continue
            seen.add(group)
            normalized_groups.append(group)
        self._tx_groups = tuple(normalized_groups)
        self._tx_group_set = frozenset((DEFAULT_TRANSACTION, *self._tx_groups))
        self._group_managers: dict[Hashable, GroupTransactionManager] = {}

    @property
    def tx_groups(self) -> tuple[Hashable, ...]:
        return self._tx_groups

    @property
    def active_transaction(self) -> LifecycleTransaction | None:
        return self._get_group_manager(DEFAULT_TRANSACTION).active_transaction

    @active_transaction.setter
    def active_transaction(self, value: LifecycleTransaction | None) -> None:
        self._get_group_manager(DEFAULT_TRANSACTION).active_transaction = value

    @property
    def begin_count(self) -> int:
        return self._get_group_manager(DEFAULT_TRANSACTION).begin_count

    def active_transaction_for(self, tx_group: Hashable = DEFAULT_TRANSACTION) -> LifecycleTransaction | None:
        return self._get_group_manager(tx_group).active_transaction

    def _normalize_groups(self, groups: tuple[Hashable, ...]) -> tuple[Hashable, ...]:
        if not groups:
            return (DEFAULT_TRANSACTION, *self._tx_groups)
        normalized: list[Hashable] = []
        seen: set[Hashable] = set()
        for group in groups:
            self._require_known_group(group)
            if group in seen:
                continue
            seen.add(group)
            normalized.append(group)
        return tuple(normalized)

    def _require_known_group(self, group: Hashable) -> None:
        if group not in self._tx_group_set:
            raise RuntimeError(f"unknown yidl transaction group {group!r}")

    def _get_group_manager(self, group: Hashable) -> GroupTransactionManager:
        self._require_known_group(group)
        manager = self._group_managers.get(group)
        if manager is None:
            manager = GroupTransactionManager(tx_group=group)
            self._group_managers[group] = manager
        return manager

    def begin(self, *groups: Hashable) -> LifecycleTransaction | _MultiGroupTransactionScope:
        normalized_groups = self._normalize_groups(groups)
        if len(normalized_groups) == 1:
            return self._get_group_manager(normalized_groups[0]).begin(normalized_groups[0])
        for group in normalized_groups:
            self._get_group_manager(group).begin(group)
        return _MultiGroupTransactionScope(self, normalized_groups)

    def validate(self, *groups: Hashable) -> None:
        normalized_groups = self._normalize_groups(groups)
        failures: list[BaseException] = []
        for group in normalized_groups:
            try:
                self._get_group_manager(group).validate(group)
            except BaseException as exc:
                failures.append(exc)
        if not failures:
            return
        if len(failures) == 1:
            raise failures[0]
        raise ExceptionGroup("yidl transaction group validation failed", failures)

    def commit_only(self, *groups: Hashable) -> CommitResult:
        normalized_groups = self._normalize_groups(groups)
        if len(normalized_groups) == 1:
            return self._get_group_manager(normalized_groups[0]).commit_only(normalized_groups[0])
        failures: list[BaseException] = []
        results: list[int | None] = []
        for group in normalized_groups:
            try:
                results.append(self._get_group_manager(group).commit_only(group))
            except BaseException as exc:
                failures.append(exc)
        if failures:
            if len(failures) == 1:
                raise failures[0]
            raise ExceptionGroup("yidl transaction group commit_only failed", failures)
        return tuple(results)

    def commit(self, *groups: Hashable) -> CommitResult:
        normalized_groups = self._normalize_groups(groups)
        if len(normalized_groups) == 1:
            return self._get_group_manager(normalized_groups[0]).commit(normalized_groups[0])
        failures: list[BaseException] = []
        results: list[int | None] = []
        for group in normalized_groups:
            try:
                results.append(self._get_group_manager(group).commit(group))
            except BaseException as exc:
                failures.append(exc)
        if failures:
            if len(failures) == 1:
                raise failures[0]
            raise ExceptionGroup("yidl transaction group commit failed", failures)
        return tuple(results)

    def rollback(self, *groups: Hashable) -> CommitResult:
        normalized_groups = self._normalize_groups(groups)
        if len(normalized_groups) == 1:
            return self._get_group_manager(normalized_groups[0]).rollback(normalized_groups[0])
        failures: list[BaseException] = []
        results: list[int | None] = []
        for group in normalized_groups:
            try:
                results.append(self._get_group_manager(group).rollback(group))
            except BaseException as exc:
                failures.append(exc)
        if failures:
            if len(failures) == 1:
                raise failures[0]
            raise ExceptionGroup("yidl transaction group rollback failed", failures)
        return tuple(results)

    def enlist(self, context: TransactionContext, tx_group: Hashable = DEFAULT_TRANSACTION) -> int:
        return self._get_group_manager(tx_group).enlist(context, tx_group)

    def drop(
        self,
        context: TransactionContext,
        tx_id: int | None = None,
        tx_group: Hashable = DEFAULT_TRANSACTION,
    ) -> None:
        self._get_group_manager(tx_group).drop(context, tx_id, tx_group)
