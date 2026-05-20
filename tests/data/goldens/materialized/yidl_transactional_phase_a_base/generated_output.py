from __future__ import annotations
import weakref
from yidl.runtime.transaction_yidl import DEFAULT_TRANSACTION
from yidl.runtime.transaction_yidl import TransactionManager
VOID = object()

def build_lifecycle_class(decorated_cls, *, _Counter_lifecycle_definition, _Counter_annotations, _Counter_tx_groups, _Counter_plain_default, _Counter_seed_default, _Counter_KIND_default):

    class Counter_State:
        __slots__ = ('_y_transaction_manager', '_y_default_ref', '_y_current_ref', '_y_working_ref', '_y_plain_value', '_y_working_tx_ids')
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

        @property
        def plain(self):
            return self._y_state._y_plain_value

        @plain.setter
        def plain(self, value):
            self._y_state._y_plain_value = value

    class Counter(Counter_FacadeBase):
        __slots__ = ()
        KIND = _Counter_KIND_default

        def __init__(self, plain: 'int'=_Counter_plain_default, seed: 'int'=_Counter_seed_default, *, transaction_manager=None):
            state = object.__new__(Counter_State)
            object.__setattr__(self, '_y_state', state)
            state._y_transaction_manager = transaction_manager or TransactionManager(tx_groups=tuple((group for group in _Counter_tx_groups if group != DEFAULT_TRANSACTION)))
            state._y_default_ref = weakref.ref(self)
            state._y_current_ref = None
            state._y_working_ref = None
            state._y_plain_value = plain
            state._y_working_tx_ids = [None for _group in _Counter_tx_groups]

    class Counter_Current(Counter_FacadeBase):
        __slots__ = ()

    class Counter_Working(Counter_FacadeBase):
        __slots__ = ()
    Counter.__name__ = decorated_cls.__name__
    Counter.__qualname__ = decorated_cls.__qualname__
    Counter.__module__ = decorated_cls.__module__
    return Counter
