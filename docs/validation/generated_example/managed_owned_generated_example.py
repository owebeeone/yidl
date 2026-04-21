"""Hand-curated generated multi-facade owned example for PRE_IMPL validation."""

from __future__ import annotations

from dataclasses import dataclass
from dataclasses import field
from typing import Any
from typing import Iterable

from yidl.runtime import BindingBase
from yidl.runtime import BindingList
from yidl.runtime import DEFAULT_TRANSACTION
from yidl.runtime import TransactionManager


class YidlCantWriteWithoutActiveTransaction(RuntimeError):
    pass


class SpyBinding(BindingBase):
    """Validation-only binding that records whether it was closed accepted/not."""

    def __init__(self, label: str) -> None:
        super().__init__()
        self.label = label
        self.closed_states: list[bool] = []

    def _close(self) -> None:
        self.closed_states.append(self.is_accepted)


class OwnedSource:
    """User-declared source shape before YIDL code generation."""

    child: SpyBinding | None
    child_list: BindingList

    def describe_child(self) -> str:
        child = getattr(self, "child", None)
        if child is None:
            return "<none>"
        return child.label

    def describe_child_list(self) -> tuple[str, ...]:
        return tuple(child.label for child in getattr(self, "child_list", ()))


@dataclass(frozen=True)
class YidlFieldMeta:
    public_name: str
    tx_group: str
    kind: str
    store_name: str


@dataclass(slots=True)
class _KildFieldRuntimeState:
    tx_group: str
    has_working_value: bool = False
    working_tx_id: int | None = None
    previous_committed_value: object | None = None


@dataclass(slots=True)
class _KildCurrentStore:
    child: SpyBinding | None = None
    child_list: BindingList = field(default_factory=BindingList)


@dataclass(slots=True)
class _KildCommitScratchStore:
    previous_child: SpyBinding | None = None
    previous_child_list: BindingList | None = None


class YidlState:
    __slots__ = (
        "transaction_manager",
        "field_meta",
        "field_state",
        "rollback_errors",
    )

    def __init__(self, *, transaction_manager: TransactionManager) -> None:
        self.transaction_manager = transaction_manager
        self.field_meta = {
            "child": YidlFieldMeta(
                public_name="child",
                tx_group=DEFAULT_TRANSACTION,
                kind="owned",
                store_name="child",
            ),
            "child_list": YidlFieldMeta(
                public_name="child_list",
                tx_group=DEFAULT_TRANSACTION,
                kind="owned_list",
                store_name="child_list",
            ),
        }
        self.field_state = {
            "child": _KildFieldRuntimeState(tx_group=DEFAULT_TRANSACTION),
            "child_list": _KildFieldRuntimeState(tx_group=DEFAULT_TRANSACTION),
        }
        self.rollback_errors: list[BaseException] = []


def _mirror_user_class_names(emit: type, user_cls: type) -> None:
    emit.__name__ = user_cls.__name__
    emit.__qualname__ = user_cls.__qualname__
    emit.__module__ = user_cls.__module__


def _accept_owned_value(value: SpyBinding | None) -> None:
    if value is not None:
        value.accepted()


def _accept_owned_list(value: BindingList) -> None:
    for item in value:
        item.accepted()


def _best_effort_close_owned_value(value: SpyBinding | None, errors: list[BaseException]) -> None:
    if value is None:
        return
    try:
        value.dec_ref()
    except BaseException as exc:
        errors.append(exc)


def _best_effort_clear_owned_list(value: BindingList | None, errors: list[BaseException]) -> None:
    if value is None:
        return
    try:
        value.clear()
    except BaseException as exc:
        errors.append(exc)


def _normalize_owned_list(value: BindingList | Iterable[SpyBinding] | None) -> BindingList:
    if value is None:
        return BindingList()
    if isinstance(value, BindingList):
        return value
    normalized = BindingList()
    for child in value:
        normalized.append(child)
    return normalized


def build_generated_owned_context(source_cls: type = OwnedSource) -> type:
    """Generate a proxy plus current/working facades for one owned example."""

    base = source_cls

    class _CurrentView(base):
        __slots__ = ("__kild_owner",)

        def __init__(self, owner: "GeneratedOwnedContext") -> None:
            super().__init__()
            self.__kild_owner = owner

        @property
        def child(self) -> SpyBinding | None:
            return self.__kild_owner._GeneratedOwnedContext__kild_current_store.child

        @property
        def child_list(self) -> BindingList:
            return self.__kild_owner._GeneratedOwnedContext__kild_current_store.child_list

    class _WorkingView(base):
        __slots__ = ("__kild_owner",)

        def __init__(self, owner: "GeneratedOwnedContext") -> None:
            super().__init__()
            self.__kild_owner = owner

        @property
        def child(self) -> SpyBinding | None:
            state = self.__kild_owner._kild_field_state("child")
            if state.has_working_value:
                return self.__kild_owner._GeneratedOwnedContext__kild_working_child
            return self.__kild_owner._GeneratedOwnedContext__kild_current_store.child

        @child.setter
        def child(self, value: SpyBinding | None) -> None:
            self.__kild_owner._kild_stage_child(value)

        @property
        def child_list(self) -> BindingList:
            state = self.__kild_owner._kild_field_state("child_list")
            if state.has_working_value:
                return self.__kild_owner._GeneratedOwnedContext__kild_working_child_list
            return self.__kild_owner._GeneratedOwnedContext__kild_current_store.child_list

        @child_list.setter
        def child_list(self, value: BindingList | Iterable[SpyBinding] | None) -> None:
            self.__kild_owner._kild_stage_child_list(value)

    class GeneratedOwnedContext(base):
        __slots__ = (
            "__kild_commit_scratch_store",
            "__kild_current_store",
            "__kild_state",
            "__kild_working_child",
            "__kild_working_child_list",
            "current",
            "working",
        )

        def __init__(
            self,
            *,
            transaction_manager: TransactionManager,
            child: SpyBinding | None = None,
            child_list: BindingList | Iterable[SpyBinding] | None = None,
        ) -> None:
            super().__init__()
            self.__kild_current_store = _KildCurrentStore()
            self.__kild_commit_scratch_store = _KildCommitScratchStore()
            self.__kild_state = YidlState(transaction_manager=transaction_manager)
            self.__kild_working_child: SpyBinding | None = None
            self.__kild_working_child_list = BindingList()
            self.current = _CurrentView(self)
            self.working = _WorkingView(self)

            if child is not None:
                self.__kild_current_store.child = child
                child.accepted()
            if child_list is not None:
                normalized = _normalize_owned_list(child_list)
                self.__kild_current_store.child_list = normalized
                _accept_owned_list(normalized)

        def _kild_field_meta(self, name: str) -> YidlFieldMeta:
            return self.__kild_state.field_meta[name]

        def _kild_field_state(self, name: str) -> _KildFieldRuntimeState:
            return self.__kild_state.field_state[name]

        def _kild_active_tx_id(self, name: str) -> int:
            meta = self._kild_field_meta(name)
            tx = self.__kild_state.transaction_manager.active_transaction_for(meta.tx_group)
            if tx is None:
                raise YidlCantWriteWithoutActiveTransaction(meta.public_name)
            return tx.tx_id

        def _kild_ensure_enlisted(self, name: str, tx_id: int) -> None:
            state = self._kild_field_state(name)
            if state.working_tx_id == tx_id:
                return
            self.__kild_state.transaction_manager.enlist(self, self._kild_field_meta(name).tx_group)
            state.working_tx_id = tx_id

        def _kild_stage_child(self, value: SpyBinding | None) -> None:
            tx_id = self._kild_active_tx_id("child")
            self._kild_ensure_enlisted("child", tx_id)
            state = self._kild_field_state("child")
            visible = self.__kild_working_child if state.has_working_value else self.__kild_current_store.child
            if visible is value:
                return
            if state.has_working_value and self.__kild_working_child is not None and self.__kild_working_child is not self.__kild_current_store.child:
                _best_effort_close_owned_value(self.__kild_working_child, self.__kild_state.rollback_errors)
            self.__kild_working_child = value
            state.has_working_value = True

        def _kild_stage_child_list(self, value: BindingList | Iterable[SpyBinding] | None) -> None:
            tx_id = self._kild_active_tx_id("child_list")
            self._kild_ensure_enlisted("child_list", tx_id)
            state = self._kild_field_state("child_list")
            normalized = _normalize_owned_list(value)
            visible = self.__kild_working_child_list if state.has_working_value else self.__kild_current_store.child_list
            if visible is normalized:
                return
            if state.has_working_value and self.__kild_working_child_list is not self.__kild_current_store.child_list:
                _best_effort_clear_owned_list(self.__kild_working_child_list, self.__kild_state.rollback_errors)
            self.__kild_working_child_list = normalized
            state.has_working_value = True

        @property
        def child(self) -> SpyBinding | None:
            tx = self.__kild_state.transaction_manager.active_transaction_for(DEFAULT_TRANSACTION)
            state = self._kild_field_state("child")
            if tx is not None and state.working_tx_id == tx.tx_id and state.has_working_value:
                return self.__kild_working_child
            return self.__kild_current_store.child

        @child.setter
        def child(self, value: SpyBinding | None) -> None:
            self.working.child = value

        @property
        def child_list(self) -> BindingList:
            tx = self.__kild_state.transaction_manager.active_transaction_for(DEFAULT_TRANSACTION)
            state = self._kild_field_state("child_list")
            if tx is not None and state.working_tx_id == tx.tx_id and state.has_working_value:
                return self.__kild_working_child_list
            return self.__kild_current_store.child_list

        @child_list.setter
        def child_list(self, value: BindingList | Iterable[SpyBinding] | None) -> None:
            self.working.child_list = value

        def commit_order_key_for(self, tx_group: str = DEFAULT_TRANSACTION) -> tuple[object, ...]:
            del tx_group
            return ()

        def requires_validation_for(self, tx_group: str = DEFAULT_TRANSACTION) -> bool:
            del tx_group
            return False

        def validate_commit_for(self, tx_group: str = DEFAULT_TRANSACTION) -> bool:
            del tx_group
            return True

        def _commit_transaction(self, tx_id: int, tx_group: str = DEFAULT_TRANSACTION) -> _CurrentView:
            self._kild_commit_child(tx_id, tx_group)
            self._kild_commit_child_list(tx_id, tx_group)
            return self.current

        def _rollback_transaction(self, tx_id: int, tx_group: str = DEFAULT_TRANSACTION) -> _CurrentView:
            self._kild_rollback_child(tx_id, tx_group)
            self._kild_rollback_child_list(tx_id, tx_group)
            return self.current

        def _kild_commit_child(self, tx_id: int, tx_group: str) -> None:
            meta = self._kild_field_meta("child")
            state = self._kild_field_state("child")
            if tx_group != meta.tx_group or state.working_tx_id != tx_id or not state.has_working_value:
                return
            current = self.__kild_current_store.child
            next_value = self.__kild_working_child
            self.__kild_commit_scratch_store.previous_child = current
            state.previous_committed_value = current
            _accept_owned_value(next_value)
            self.__kild_current_store.child = next_value
            state.has_working_value = False
            state.working_tx_id = None
            self.__kild_working_child = None
            if current is not None and current is not next_value:
                _best_effort_close_owned_value(current, self.__kild_state.rollback_errors)
            self.__kild_commit_scratch_store.previous_child = None
            state.previous_committed_value = None

        def _kild_commit_child_list(self, tx_id: int, tx_group: str) -> None:
            meta = self._kild_field_meta("child_list")
            state = self._kild_field_state("child_list")
            if tx_group != meta.tx_group or state.working_tx_id != tx_id or not state.has_working_value:
                return
            current = self.__kild_current_store.child_list
            next_value = self.__kild_working_child_list
            self.__kild_commit_scratch_store.previous_child_list = current
            state.previous_committed_value = current
            _accept_owned_list(next_value)
            self.__kild_current_store.child_list = next_value
            state.has_working_value = False
            state.working_tx_id = None
            self.__kild_working_child_list = BindingList()
            if current is not next_value:
                _best_effort_clear_owned_list(current, self.__kild_state.rollback_errors)
            self.__kild_commit_scratch_store.previous_child_list = None
            state.previous_committed_value = None

        def _kild_rollback_child(self, tx_id: int, tx_group: str) -> None:
            meta = self._kild_field_meta("child")
            state = self._kild_field_state("child")
            if tx_group != meta.tx_group or state.working_tx_id != tx_id or not state.has_working_value:
                return
            if self.__kild_working_child is not None and self.__kild_working_child is not self.__kild_current_store.child:
                _best_effort_close_owned_value(self.__kild_working_child, self.__kild_state.rollback_errors)
            state.has_working_value = False
            state.working_tx_id = None
            self.__kild_working_child = None

        def _kild_rollback_child_list(self, tx_id: int, tx_group: str) -> None:
            meta = self._kild_field_meta("child_list")
            state = self._kild_field_state("child_list")
            if tx_group != meta.tx_group or state.working_tx_id != tx_id or not state.has_working_value:
                return
            if self.__kild_working_child_list is not self.__kild_current_store.child_list:
                _best_effort_clear_owned_list(self.__kild_working_child_list, self.__kild_state.rollback_errors)
            state.has_working_value = False
            state.working_tx_id = None
            self.__kild_working_child_list = BindingList()

        def close(self) -> None:
            _best_effort_close_owned_value(self.__kild_current_store.child, self.__kild_state.rollback_errors)
            _best_effort_clear_owned_list(self.__kild_current_store.child_list, self.__kild_state.rollback_errors)
            self.__kild_current_store.child = None
            self.__kild_current_store.child_list = BindingList()

    _mirror_user_class_names(_CurrentView, base)
    _mirror_user_class_names(_WorkingView, base)
    _mirror_user_class_names(GeneratedOwnedContext, base)
    return GeneratedOwnedContext
