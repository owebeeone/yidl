from __future__ import annotations
import weakref
from yidl.runtime.lifecycle import _HAS_DEFAULT_FACTORY
from yidl.runtime.transaction_yidl import DEFAULT_TRANSACTION
from yidl.runtime.transaction_yidl import TransactionManager
VOID = object()

def build_lifecycle_class(decorated_cls, *, _B_lifecycle_definition, _B_annotations, _B_tx_groups, _B_plain_default, _B_seed_default, _B_KIND_default, _B_v1_default, _B_v2_default):

    class B_State:
        __slots__ = ('_y_transaction_manager', '_y_default_ref', '_y_current_ref', '_y_working_ref', '_y_plain_current', '_y_plain_working', '_y_v1_current', '_y_v1_working', '_y_v2_current', '_y_v2_working', '_y_working_tx_ids')
        __yidl_tx_index_to_group__ = _B_tx_groups
        __yidl_tx_group_to_index__ = {group: index for index, group in enumerate(_B_tx_groups)}

        def _y_get_default_facade(self):
            ref = self._y_default_ref
            facade = None if ref is None else ref()
            if facade is None:
                facade = object.__new__(B)
                object.__setattr__(facade, '_y_state', self)
                self._y_default_ref = weakref.ref(facade)
            return facade

        def _y_get_current_facade(self):
            ref = self._y_current_ref
            facade = None if ref is None else ref()
            if facade is None:
                facade = object.__new__(B_Current)
                object.__setattr__(facade, '_y_state', self)
                self._y_current_ref = weakref.ref(facade)
            return facade

        def _y_get_working_facade(self):
            ref = self._y_working_ref
            facade = None if ref is None else ref()
            if facade is None:
                facade = object.__new__(B_Working)
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
            return ()

        def requires_validation_for(self, tx_group=DEFAULT_TRANSACTION):
            return False

        def validate_commit_for(self, tx_group=DEFAULT_TRANSACTION):
            return True

        def _commit_transaction(self, tx_id, tx_group=DEFAULT_TRANSACTION):
            tx_index = self.__yidl_tx_group_to_index__[tx_group]
            if self._y_working_tx_ids[tx_index] != tx_id:
                return self._y_get_default_facade()
            if tx_index == 0:
                if self._y_plain_working is not VOID:
                    self._y_plain_current = self._y_plain_working
                    self._y_plain_working = VOID
            if tx_index == 0:
                if self._y_v1_working is not VOID:
                    self._y_v1_current = self._y_v1_working
                    self._y_v1_working = VOID
            if tx_index == 0:
                if self._y_v2_working is not VOID:
                    self._y_v2_current = self._y_v2_working
                    self._y_v2_working = VOID
            self._y_working_tx_ids[tx_index] = None
            return self._y_get_default_facade()

        def _rollback_transaction(self, tx_id, tx_group=DEFAULT_TRANSACTION):
            tx_index = self.__yidl_tx_group_to_index__[tx_group]
            if self._y_working_tx_ids[tx_index] != tx_id:
                return self._y_get_default_facade()
            if tx_index == 0:
                self._y_plain_working = VOID
            if tx_index == 0:
                self._y_v1_working = VOID
            if tx_index == 0:
                self._y_v2_working = VOID
            self._y_working_tx_ids[tx_index] = None
            return self._y_get_default_facade()

    class B_FacadeBase(decorated_cls):
        __slots__ = ('_y_state',)
        _y_lifecycle_field_names = frozenset(('plain', 'v1', 'v2'))

        def __setattr__(self, name, value):
            if name in self._y_lifecycle_field_names:
                descriptor = getattr(type(self), name, None)
                if descriptor is None or not hasattr(descriptor, '__set__'):
                    raise AttributeError(f'lifecycle field {name!r} is not assignable')
                descriptor.__set__(self, value)
                return
            if name.startswith('_y_') or name.startswith('__yidl_'):
                raise AttributeError(f'{name!r} is reserved for generated lifecycle state')
            object.__setattr__(self, name, value)

        def __delattr__(self, name):
            if name in self._y_lifecycle_field_names:
                raise AttributeError(f'lifecycle field {name!r} cannot be deleted')
            if name.startswith('_y_') or name.startswith('__yidl_'):
                raise AttributeError(f'{name!r} is reserved for generated lifecycle state')
            object.__delattr__(self, name)

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
        KIND = _B_KIND_default

    class B(B_FacadeBase):
        __slots__ = ()
        __annotations__ = _B_annotations
        __yidl_lifecycle_generated__ = True
        __yidl_lifecycle_user_class__ = decorated_cls
        __yidl_lifecycle_definition__ = _B_lifecycle_definition
        __yidl_tx_index_to_group__ = _B_tx_groups
        __yidl_tx_group_to_index__ = {group: index for index, group in enumerate(_B_tx_groups)}

        @property
        def plain(self):
            state = self._y_state
            if state._y_plain_working is not VOID:
                return state._y_plain_working
            return state._y_plain_current

        @plain.setter
        def plain(self, value):
            state = self._y_state
            state._y_ensure_working_transaction(0)
            state._y_plain_working = value

        @property
        def v1(self):
            state = self._y_state
            if state._y_v1_working is not VOID:
                return state._y_v1_working
            return state._y_v1_current

        @v1.setter
        def v1(self, value):
            state = self._y_state
            state._y_ensure_working_transaction(0)
            state._y_v1_working = value

        @property
        def v2(self):
            state = self._y_state
            if state._y_v2_working is not VOID:
                return state._y_v2_working
            return state._y_v2_current

        @v2.setter
        def v2(self, value):
            state = self._y_state
            state._y_ensure_working_transaction(0)
            state._y_v2_working = value

        def __init__(self, plain: 'int'=_B_plain_default, seed: 'int'=_B_seed_default, v1: 'int'=_B_v1_default, v2: 'int'=_B_v2_default, *, transaction_manager=None):
            state = object.__new__(B_State)
            object.__setattr__(self, '_y_state', state)
            state._y_transaction_manager = transaction_manager or TransactionManager(tx_groups=tuple((group for group in _B_tx_groups if group != DEFAULT_TRANSACTION)))
            state._y_default_ref = weakref.ref(self)
            state._y_current_ref = None
            state._y_working_ref = None
            state._y_plain_current = plain
            state._y_plain_working = VOID
            state._y_v1_current = v1
            state._y_v1_working = VOID
            state._y_v2_current = v2
            state._y_v2_working = VOID
            state._y_working_tx_ids = [None for _group in _B_tx_groups]

    class B_Current(B_FacadeBase):
        __slots__ = ()

        @property
        def plain(self):
            return self._y_state._y_plain_current

        @plain.setter
        def plain(self, value):
            del value
            raise AttributeError('current facade is read-only for transactional field ' + 'plain')

        @property
        def v1(self):
            return self._y_state._y_v1_current

        @v1.setter
        def v1(self, value):
            del value
            raise AttributeError('current facade is read-only for transactional field ' + 'v1')

        @property
        def v2(self):
            return self._y_state._y_v2_current

        @v2.setter
        def v2(self, value):
            del value
            raise AttributeError('current facade is read-only for transactional field ' + 'v2')

    class B_Working(B_FacadeBase):
        __slots__ = ()

        @property
        def plain(self):
            state = self._y_state
            if state._y_plain_working is not VOID:
                return state._y_plain_working
            return state._y_plain_current

        @plain.setter
        def plain(self, value):
            state = self._y_state
            state._y_ensure_working_transaction(0)
            state._y_plain_working = value

        @property
        def v1(self):
            state = self._y_state
            if state._y_v1_working is not VOID:
                return state._y_v1_working
            return state._y_v1_current

        @v1.setter
        def v1(self, value):
            state = self._y_state
            state._y_ensure_working_transaction(0)
            state._y_v1_working = value

        @property
        def v2(self):
            state = self._y_state
            if state._y_v2_working is not VOID:
                return state._y_v2_working
            return state._y_v2_current

        @v2.setter
        def v2(self, value):
            state = self._y_state
            state._y_ensure_working_transaction(0)
            state._y_v2_working = value
    B.__name__ = decorated_cls.__name__
    B.__qualname__ = decorated_cls.__qualname__
    B.__module__ = decorated_cls.__module__
    return B
