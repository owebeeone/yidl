from __future__ import annotations
import weakref
from yidl.runtime.transaction_yidl import DEFAULT_TRANSACTION
from yidl.runtime.transaction_yidl import TransactionManager
VOID = object()

def build_lifecycle_class(decorated_cls, *, _Counter_lifecycle_definition, _Counter_annotations, _Counter_tx_groups, _Counter_plain_default, _Counter_seed_default, _Counter_KIND_default, _Counter_count_default, _Counter_audit_count_default):

    class Counter_State:
        __slots__ = ('_y_transaction_manager', '_y_default_ref', '_y_current_ref', '_y_working_ref', '_y_plain_value', '_y_count_current', '_y_count_working', '_y_audit_count_current', '_y_audit_count_working', '_y_working_tx_ids')
        __yidl_tx_index_to_group__ = _Counter_tx_groups
        __yidl_tx_group_to_index__ = {group: index for index, group in enumerate(_Counter_tx_groups)}

        def _y_get_default_facade(self):
            ref = self._y_default_ref
            facade = None if ref is None else ref()
            if facade is None:
                facade = object.__new__(Counter)
                object.__setattr__(facade, '_y_state', self)
                self._y_default_ref = weakref.ref(facade)
            return facade

        def _y_get_current_facade(self):
            ref = self._y_current_ref
            facade = None if ref is None else ref()
            if facade is None:
                facade = object.__new__(Counter_Current)
                object.__setattr__(facade, '_y_state', self)
                self._y_current_ref = weakref.ref(facade)
            return facade

        def _y_get_working_facade(self):
            ref = self._y_working_ref
            facade = None if ref is None else ref()
            if facade is None:
                facade = object.__new__(Counter_Working)
                object.__setattr__(facade, '_y_state', self)
                self._y_working_ref = weakref.ref(facade)
            return facade

        def _y_require_active_transaction(self, tx_index):
            tx_group = self.__yidl_tx_index_to_group__[tx_index]
            transaction = self._y_transaction_manager.active_transaction_for(tx_group)
            if transaction is None:
                if self._y_working_tx_ids[tx_index] is not None:
                    raise RuntimeError('stale yidl working value without an active transaction')
                raise RuntimeError('writes require an active yidl transaction')
            existing_tx_id = self._y_working_tx_ids[tx_index]
            if existing_tx_id is not None and existing_tx_id != transaction.tx_id:
                raise RuntimeError('working value belongs to a different yidl transaction')
            return transaction

        def _y_ensure_working_transaction(self, tx_index):
            transaction = self._y_require_active_transaction(tx_index)
            if self._y_working_tx_ids[tx_index] is None:
                tx_group = self.__yidl_tx_index_to_group__[tx_index]
                self._y_working_tx_ids[tx_index] = self._y_transaction_manager.enlist(self, tx_group)
            return transaction

        def commit_order_key_for(self, tx_group=DEFAULT_TRANSACTION):
            del tx_group
            return ()

        def requires_validation_for(self, tx_group=DEFAULT_TRANSACTION):
            del tx_group
            return False

        def validate_commit_for(self, tx_group=DEFAULT_TRANSACTION):
            del tx_group
            return True

        def _commit_transaction(self, tx_id, tx_group=DEFAULT_TRANSACTION):
            tx_index = self.__yidl_tx_group_to_index__[tx_group]
            if self._y_working_tx_ids[tx_index] != tx_id:
                return self._y_get_default_facade()
            pass
            if tx_index == 0:
                if self._y_count_working is not VOID:
                    self._y_count_current = self._y_count_working
                    self._y_count_working = VOID
            if tx_index == 1:
                if self._y_audit_count_working is not VOID:
                    self._y_audit_count_current = self._y_audit_count_working
                    self._y_audit_count_working = VOID
            self._y_working_tx_ids[tx_index] = None
            return self._y_get_default_facade()

        def _rollback_transaction(self, tx_id, tx_group=DEFAULT_TRANSACTION):
            tx_index = self.__yidl_tx_group_to_index__[tx_group]
            if self._y_working_tx_ids[tx_index] != tx_id:
                return self._y_get_default_facade()
            pass
            if tx_index == 0:
                self._y_count_working = VOID
            if tx_index == 1:
                self._y_audit_count_working = VOID
            self._y_working_tx_ids[tx_index] = None
            return self._y_get_default_facade()

    class Counter_FacadeBase(decorated_cls):
        __slots__ = ('_y_state',)

        @property
        def default(self):
            return self._y_state._y_get_default_facade()

        @property
        def current(self):
            return self._y_state._y_get_current_facade()

        @property
        def working(self):
            return self._y_state._y_get_working_facade()

        def begin(self, *tx_groups):
            return self._y_state._y_transaction_manager.begin(*tx_groups)

        def validate(self, *tx_groups):
            return self._y_state._y_transaction_manager.validate(*tx_groups)

        def commit_only(self, *tx_groups):
            return self._y_state._y_transaction_manager.commit_only(*tx_groups)

        def commit(self, *tx_groups):
            return self._y_state._y_transaction_manager.commit(*tx_groups)

        def rollback(self, *tx_groups):
            return self._y_state._y_transaction_manager.rollback(*tx_groups)
        pass
        KIND = _Counter_KIND_default
        pass

        @property
        def plain(self):
            return self._y_state._y_plain_value

        @plain.setter
        def plain(self, value):
            self._y_state._y_plain_value = value

    class Counter(Counter_FacadeBase):
        __slots__ = ()
        __annotations__ = _Counter_annotations
        __yidl_lifecycle_generated__ = True
        __yidl_lifecycle_user_class__ = decorated_cls
        __yidl_lifecycle_definition__ = _Counter_lifecycle_definition
        __yidl_tx_index_to_group__ = _Counter_tx_groups
        __yidl_tx_group_to_index__ = {group: index for index, group in enumerate(_Counter_tx_groups)}
        pass

        @property
        def count(self):
            state = self._y_state
            if state._y_count_working is not VOID:
                return state._y_count_working
            return state._y_count_current

        @count.setter
        def count(self, value):
            state = self._y_state
            state._y_ensure_working_transaction(0)
            state._y_count_working = value

        @property
        def audit_count(self):
            state = self._y_state
            if state._y_audit_count_working is not VOID:
                return state._y_audit_count_working
            return state._y_audit_count_current

        @audit_count.setter
        def audit_count(self, value):
            state = self._y_state
            state._y_ensure_working_transaction(1)
            state._y_audit_count_working = value

        def __init__(self, plain: 'int'=_Counter_plain_default, seed: 'int'=_Counter_seed_default, count: 'int'=_Counter_count_default, audit_count: 'int'=_Counter_audit_count_default, *, transaction_manager=None):
            state = object.__new__(Counter_State)
            object.__setattr__(self, '_y_state', state)
            state._y_transaction_manager = transaction_manager or TransactionManager(tx_groups=tuple((group for group in _Counter_tx_groups if group != DEFAULT_TRANSACTION)))
            state._y_default_ref = weakref.ref(self)
            state._y_current_ref = None
            state._y_working_ref = None
            pass
            state._y_plain_value = plain
            state._y_count_current = count
            state._y_count_working = VOID
            state._y_audit_count_current = audit_count
            state._y_audit_count_working = VOID
            state._y_working_tx_ids = [None for _group in _Counter_tx_groups]

    class Counter_Current(Counter_FacadeBase):
        __slots__ = ()
        pass

        @property
        def count(self):
            return self._y_state._y_count_current

        @count.setter
        def count(self, value):
            del value
            raise AttributeError('current facade is read-only for transactional field ' + 'count')

        @property
        def audit_count(self):
            return self._y_state._y_audit_count_current

        @audit_count.setter
        def audit_count(self, value):
            del value
            raise AttributeError('current facade is read-only for transactional field ' + 'audit_count')

    class Counter_Working(Counter_FacadeBase):
        __slots__ = ()
        pass

        @property
        def count(self):
            state = self._y_state
            if state._y_count_working is not VOID:
                return state._y_count_working
            return state._y_count_current

        @count.setter
        def count(self, value):
            state = self._y_state
            state._y_ensure_working_transaction(0)
            state._y_count_working = value

        @property
        def audit_count(self):
            state = self._y_state
            if state._y_audit_count_working is not VOID:
                return state._y_audit_count_working
            return state._y_audit_count_current

        @audit_count.setter
        def audit_count(self, value):
            state = self._y_state
            state._y_ensure_working_transaction(1)
            state._y_audit_count_working = value
    Counter.__name__ = decorated_cls.__name__
    Counter.__qualname__ = decorated_cls.__qualname__
    Counter.__module__ = decorated_cls.__module__
    return Counter
