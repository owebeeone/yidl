from __future__ import annotations
from collections.abc import Mapping
from yidl.runtime.bindings import BindingBase, BindingDict
import weakref
from yidl.runtime.lifecycle import _HAS_DEFAULT_FACTORY
from yidl.runtime.transaction_yidl import DEFAULT_TRANSACTION
from yidl.runtime.transaction_yidl import TransactionManager
VOID = object()

def build_lifecycle_class(decorated_cls, *, _Owner_lifecycle_definition, _Owner_annotations, _Owner_tx_keys, _Owner_value_state_default_factory, _Owner_identity_state_default_factory, _Owner_child_default, _Owner_identity_child_default, _Owner_children_default_factory, _Owner_handle_default, _Owner_handles_default_factory):

    def _y_validate_binding_value(field_name, value):
        if value is not None and (not isinstance(value, BindingBase)):
            raise TypeError('binding field ' + repr(field_name) + ' expects BindingBase or None')
        return value

    def _y_validate_binding_map_value(field_name, value):
        if value is None:
            return None
        if not isinstance(value, Mapping):
            raise TypeError('binding map field ' + repr(field_name) + ' expects a mapping or None')
        result = value if isinstance(value, BindingDict) else BindingDict(value)
        for key, item in result.items():
            if not isinstance(item, BindingBase):
                raise TypeError('binding map field ' + repr(field_name) + ' expects BindingBase values; key ' + repr(key) + ' has ' + type(item).__name__)
        return result

    class Owner_State:
        __slots__ = ('_y_transaction_manager', '_y_default_ref', '_y_current_ref', '_y_working_ref', '_y_value_state_current', '_y_value_state_working', '_y_value_state_staged', '_y_identity_state_current', '_y_identity_state_working', '_y_identity_state_staged', '_y_child_current', '_y_child_working', '_y_child_staged', '_y_identity_child_current', '_y_identity_child_working', '_y_identity_child_staged', '_y_children_current', '_y_children_working', '_y_children_staged', '_y_handle_value', '_y_handles_value', '_y_working_tx_ids')
        __yidl_tx_index_to_key__ = _Owner_tx_keys
        __yidl_tx_key_to_index__ = {key: index for index, key in enumerate(_Owner_tx_keys)}

        def _y_get_default_facade(self):
            ref = self._y_default_ref
            facade = None if ref is None else ref()
            if facade is None:
                facade = object.__new__(Owner)
                object.__setattr__(facade, '_y_state', self)
                current_ref = self._y_current_ref
                working_ref = self._y_working_ref
                object.__setattr__(facade, '_y_current_facade', None if current_ref is None else current_ref())
                object.__setattr__(facade, '_y_working_facade', None if working_ref is None else working_ref())
                self._y_default_ref = weakref.ref(facade)
            return facade

        def _y_get_current_facade(self):
            ref = self._y_current_ref
            facade = None if ref is None else ref()
            if facade is None:
                facade = object.__new__(Owner_Current)
                object.__setattr__(facade, '_y_state', self)
                self._y_current_ref = weakref.ref(facade)
                default_ref = self._y_default_ref
                default = None if default_ref is None else default_ref()
                if default is not None:
                    object.__setattr__(default, '_y_current_facade', facade)
            return facade

        def _y_get_working_facade(self):
            ref = self._y_working_ref
            facade = None if ref is None else ref()
            if facade is None:
                facade = object.__new__(Owner_Working)
                object.__setattr__(facade, '_y_state', self)
                self._y_working_ref = weakref.ref(facade)
                default_ref = self._y_default_ref
                default = None if default_ref is None else default_ref()
                if default is not None:
                    object.__setattr__(default, '_y_working_facade', facade)
            return facade

        def _y_require_active_transaction(self, tx_index):
            tx_key = self.__yidl_tx_index_to_key__[tx_index]
            transaction = self._y_transaction_manager.active_transaction_for(tx_key)
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
                tx_key = self.__yidl_tx_index_to_key__[tx_index]
                self._y_working_tx_ids[tx_index] = self._y_transaction_manager.enlist(self, tx_key)
            return transaction

        def commit_order_key_for(self, tx_key=DEFAULT_TRANSACTION):
            tx_index = self.__yidl_tx_key_to_index__[tx_key]
            if False:
                pass
            elif tx_index == 0:
                return self._commit_order_key_tx_0()
            elif True:
                return ()

        def requires_validation_for(self, tx_key=DEFAULT_TRANSACTION):
            tx_index = self.__yidl_tx_key_to_index__[tx_key]
            if False:
                pass
            elif tx_index == 0:
                return self._requires_validation_tx_0()
            elif True:
                return False

        def validate_commit_for(self, tx_key=DEFAULT_TRANSACTION):
            tx_index = self.__yidl_tx_key_to_index__[tx_key]
            if False:
                pass
            elif tx_index == 0:
                return self._validate_commit_tx_0()
            elif True:
                return True

        def _prepare_commit_tx_by_key(self, tx_key=DEFAULT_TRANSACTION, tx_token=None):
            tx_index = self.__yidl_tx_key_to_index__[tx_key]
            if self._y_working_tx_ids[tx_index] != tx_token:
                raise RuntimeError('stale yidl transaction token')
            if False:
                pass
            elif tx_index == 0:
                self._before_commit_tx_0()
            elif True:
                pass
            if False:
                pass
            elif tx_index == 0:
                self._prepare_commit_tx_0_fields()
            elif True:
                pass
            return self._y_get_default_facade()

        def _apply_prepared_commit_tx_by_key(self, tx_key=DEFAULT_TRANSACTION, tx_token=None):
            tx_index = self.__yidl_tx_key_to_index__[tx_key]
            if self._y_working_tx_ids[tx_index] != tx_token:
                raise RuntimeError('stale yidl transaction token')
            if False:
                pass
            elif tx_index == 0:
                self._apply_prepared_commit_tx_0_fields()
            elif True:
                pass
            self._y_working_tx_ids[tx_index] = None
            return self._y_get_default_facade()

        def _after_commit_tx_by_key(self, tx_key=DEFAULT_TRANSACTION, tx_token=None):
            del tx_token
            tx_index = self.__yidl_tx_key_to_index__[tx_key]
            if False:
                pass
            elif tx_index == 0:
                self._after_commit_tx_0()
            elif True:
                pass
            return self._y_get_default_facade()

        def _rollback_tx_by_key(self, tx_key=DEFAULT_TRANSACTION, tx_token=None):
            tx_index = self.__yidl_tx_key_to_index__[tx_key]
            del tx_token
            if False:
                pass
            elif tx_index == 0:
                self._rollback_tx_0_fields()
            elif True:
                pass
            self._y_working_tx_ids[tx_index] = None
            return self._y_get_default_facade()

        def _after_rollback_tx_by_key(self, tx_key=DEFAULT_TRANSACTION, tx_token=None):
            del tx_token
            tx_index = self.__yidl_tx_key_to_index__[tx_key]
            if False:
                pass
            elif tx_index == 0:
                self._after_rollback_tx_0()
            elif True:
                pass
            return self._y_get_default_facade()

        def _commit_order_key_tx_0(self):
            return ()

        def _requires_validation_tx_0(self):
            return False

        def _validate_commit_tx_0(self):
            return True

        def _before_commit_tx_0(self):
            pass

        def _after_commit_tx_0(self):
            pass

        def _apply_prepared_commit_tx_0_fields(self):
            if self._y_value_state_staged is not VOID:
                self._y_value_state_current = self._y_value_state_staged
                self._y_value_state_staged = VOID
                self._y_value_state_working = VOID
            if self._y_identity_state_staged is not VOID:
                self._y_identity_state_current = self._y_identity_state_staged
                self._y_identity_state_staged = VOID
                self._y_identity_state_working = VOID
            if self._y_child_staged is not VOID:
                self._y_child_current = self._y_child_staged
                self._y_child_staged = VOID
                self._y_child_working = VOID
            if self._y_identity_child_staged is not VOID:
                self._y_identity_child_current = self._y_identity_child_staged
                self._y_identity_child_staged = VOID
                self._y_identity_child_working = VOID
            if self._y_children_staged is not VOID:
                self._y_children_current = self._y_children_staged
                self._y_children_staged = VOID
                self._y_children_working = VOID

        def _prepare_commit_tx_0_fields(self):
            if self._y_value_state_working is not VOID:
                self._y_value_state_staged = self._y_value_state_working
            if self._y_identity_state_working is not VOID:
                self._y_identity_state_staged = self._y_identity_state_working
            if self._y_child_working is not VOID:
                value = self._y_child_working
                if value is not None:
                    value.accepted()
                self._y_child_staged = value
            if self._y_identity_child_working is not VOID:
                value__astichi_scoped_1 = self._y_identity_child_working
                if value__astichi_scoped_1 is not None:
                    value__astichi_scoped_1.accepted()
                self._y_identity_child_staged = value__astichi_scoped_1
            if self._y_children_working is not VOID:
                value__astichi_scoped_2 = self._y_children_working
                if value__astichi_scoped_2 is not None:
                    for item in value__astichi_scoped_2.values():
                        item.accepted()
                self._y_children_staged = value__astichi_scoped_2

        def _after_rollback_tx_0(self):
            pass

        def _rollback_tx_0_fields(self):
            self._y_value_state_staged = VOID
            self._y_value_state_working = VOID
            self._y_identity_state_staged = VOID
            self._y_identity_state_working = VOID
            self._y_child_staged = VOID
            self._y_child_working = VOID
            self._y_identity_child_staged = VOID
            self._y_identity_child_working = VOID
            self._y_children_staged = VOID
            self._y_children_working = VOID

    class Owner_FacadeBase(decorated_cls):
        __slots__ = ('_y_state',) if hasattr(decorated_cls, '__weakref__') else ('_y_state', '__weakref__')
        _y_lifecycle_field_names = frozenset(('value_state', 'identity_state', 'child', 'identity_child', 'children', 'handle', 'handles'))

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

        def _y_get_transaction_manager(self):
            return self._y_state._y_transaction_manager

        def begin(self, *tx_keys):
            return self._y_get_transaction_manager().begin(*tx_keys)

        def validate(self, *tx_keys):
            return self._y_get_transaction_manager().validate(*tx_keys)

        def commit_only(self, *tx_keys):
            return self._y_get_transaction_manager().commit_only(*tx_keys)

        def commit(self, *tx_keys):
            return self._y_get_transaction_manager().commit(*tx_keys)

        def rollback(self, *tx_keys):
            return self._y_get_transaction_manager().rollback(*tx_keys)

        @property
        def handle(self):
            return self._y_state._y_handle_value

        @handle.setter
        def handle(self, value):
            self._y_state._y_handle_value = _y_validate_binding_value('handle', value)

        @property
        def handles(self):
            return self._y_state._y_handles_value

        @handles.setter
        def handles(self, value):
            self._y_state._y_handles_value = _y_validate_binding_map_value('handles', value)

    class Owner(Owner_FacadeBase):
        __slots__ = ('_y_current_facade', '_y_working_facade')
        __annotations__ = _Owner_annotations
        __yidl_lifecycle_generated__ = True
        __yidl_lifecycle_user_class__ = decorated_cls
        __yidl_lifecycle_definition__ = _Owner_lifecycle_definition
        __yidl_tx_index_to_key__ = _Owner_tx_keys
        __yidl_tx_key_to_index__ = {key: index for index, key in enumerate(_Owner_tx_keys)}

        @property
        def value_state(self):
            state = self._y_state
            if state._y_value_state_working is not VOID:
                return state._y_value_state_working
            return state._y_value_state_current

        @value_state.setter
        def value_state(self, value):
            state = self._y_state
            state._y_require_active_transaction(0)
            if state._y_value_state_working is not VOID:
                current = state._y_value_state_working
            else:
                current = state._y_value_state_current
            next_value = value
            if current == next_value:
                return
            state._y_ensure_working_transaction(0)
            state._y_value_state_working = next_value

        @property
        def identity_state(self):
            state = self._y_state
            if state._y_identity_state_working is not VOID:
                return state._y_identity_state_working
            return state._y_identity_state_current

        @identity_state.setter
        def identity_state(self, value):
            state = self._y_state
            state._y_require_active_transaction(0)
            if state._y_identity_state_working is not VOID:
                current = state._y_identity_state_working
            else:
                current = state._y_identity_state_current
            next_value = value
            if current is next_value:
                return
            state._y_ensure_working_transaction(0)
            state._y_identity_state_working = next_value

        @property
        def child(self):
            state = self._y_state
            if state._y_child_working is not VOID:
                return state._y_child_working
            return state._y_child_current

        @child.setter
        def child(self, value):
            state = self._y_state
            state._y_require_active_transaction(0)
            next_value = _y_validate_binding_value('child', value)
            if state._y_child_working is not VOID:
                current = state._y_child_working
            else:
                current = state._y_child_current
            if current == next_value:
                return
            state._y_ensure_working_transaction(0)
            state._y_child_working = next_value

        @property
        def identity_child(self):
            state = self._y_state
            if state._y_identity_child_working is not VOID:
                return state._y_identity_child_working
            return state._y_identity_child_current

        @identity_child.setter
        def identity_child(self, value):
            state = self._y_state
            state._y_require_active_transaction(0)
            next_value = _y_validate_binding_value('identity_child', value)
            if state._y_identity_child_working is not VOID:
                current = state._y_identity_child_working
            else:
                current = state._y_identity_child_current
            if current is next_value:
                return
            state._y_ensure_working_transaction(0)
            state._y_identity_child_working = next_value

        @property
        def children(self):
            state = self._y_state
            if state._y_children_working is not VOID:
                return state._y_children_working
            return state._y_children_current

        @children.setter
        def children(self, value):
            state = self._y_state
            state._y_require_active_transaction(0)
            next_value = _y_validate_binding_map_value('children', value)
            if state._y_children_working is not VOID:
                current = state._y_children_working
            else:
                current = state._y_children_current
            if current == next_value:
                return
            state._y_ensure_working_transaction(0)
            state._y_children_working = next_value

        def __init__(self, value_state: 'list[int]'=_HAS_DEFAULT_FACTORY, identity_state: 'list[int]'=_HAS_DEFAULT_FACTORY, child: 'BindingBase | None'=_Owner_child_default, identity_child: 'BindingBase | None'=_Owner_identity_child_default, children: 'dict[str, BindingBase]'=_HAS_DEFAULT_FACTORY, handle: 'BindingBase | None'=_Owner_handle_default, handles: 'dict[str, BindingBase]'=_HAS_DEFAULT_FACTORY, *, transaction_manager=None):
            state = object.__new__(Owner_State)
            object.__setattr__(self, '_y_state', state)
            object.__setattr__(self, '_y_current_facade', None)
            object.__setattr__(self, '_y_working_facade', None)
            state._y_transaction_manager = transaction_manager or TransactionManager(tx_keys=tuple((group for group in _Owner_tx_keys if group != DEFAULT_TRANSACTION)))
            state._y_default_ref = weakref.ref(self)
            state._y_current_ref = None
            state._y_working_ref = None
            state._y_value_state_working = VOID
            state._y_value_state_staged = VOID
            state._y_identity_state_working = VOID
            state._y_identity_state_staged = VOID
            value = _y_validate_binding_value('child', child)
            state._y_child_current = value
            state._y_child_working = VOID
            state._y_child_staged = VOID
            value__astichi_scoped_3 = _y_validate_binding_value('identity_child', identity_child)
            state._y_identity_child_current = value__astichi_scoped_3
            state._y_identity_child_working = VOID
            state._y_identity_child_staged = VOID
            state._y_children_working = VOID
            state._y_children_staged = VOID
            value__astichi_scoped_4 = _y_validate_binding_value('handle', handle)
            state._y_handle_value = value__astichi_scoped_4
            if value_state is _HAS_DEFAULT_FACTORY:
                value_state = _Owner_value_state_default_factory()
            state._y_value_state_current = value_state
            if identity_state is _HAS_DEFAULT_FACTORY:
                identity_state = _Owner_identity_state_default_factory()
            state._y_identity_state_current = identity_state
            if children is _HAS_DEFAULT_FACTORY:
                children = _Owner_children_default_factory()
            value__astichi_scoped_5 = _y_validate_binding_map_value('children', children)
            state._y_children_current = value__astichi_scoped_5
            if handles is _HAS_DEFAULT_FACTORY:
                handles = _Owner_handles_default_factory()
            self.handles = handles
            state._y_working_tx_ids = [None for _group in _Owner_tx_keys]

    class Owner_Current(Owner_FacadeBase):
        __slots__ = ()

        @property
        def value_state(self):
            return self._y_state._y_value_state_current

        @value_state.setter
        def value_state(self, value):
            del value
            raise AttributeError('current facade is read-only for transactional field ' + 'value_state')

        @property
        def identity_state(self):
            return self._y_state._y_identity_state_current

        @identity_state.setter
        def identity_state(self, value):
            del value
            raise AttributeError('current facade is read-only for transactional field ' + 'identity_state')

        @property
        def child(self):
            return self._y_state._y_child_current

        @child.setter
        def child(self, value):
            del value
            raise AttributeError('current facade is read-only for owned field ' + 'child')

        @property
        def identity_child(self):
            return self._y_state._y_identity_child_current

        @identity_child.setter
        def identity_child(self, value):
            del value
            raise AttributeError('current facade is read-only for owned field ' + 'identity_child')

        @property
        def children(self):
            return self._y_state._y_children_current

        @children.setter
        def children(self, value):
            del value
            raise AttributeError('current facade is read-only for owned field ' + 'children')

    class Owner_Working(Owner_FacadeBase):
        __slots__ = ()

        @property
        def value_state(self):
            state = self._y_state
            if state._y_value_state_working is not VOID:
                return state._y_value_state_working
            return state._y_value_state_current

        @value_state.setter
        def value_state(self, value):
            state = self._y_state
            state._y_require_active_transaction(0)
            if state._y_value_state_working is not VOID:
                current = state._y_value_state_working
            else:
                current = state._y_value_state_current
            next_value = value
            if current == next_value:
                return
            state._y_ensure_working_transaction(0)
            state._y_value_state_working = next_value

        @property
        def identity_state(self):
            state = self._y_state
            if state._y_identity_state_working is not VOID:
                return state._y_identity_state_working
            return state._y_identity_state_current

        @identity_state.setter
        def identity_state(self, value):
            state = self._y_state
            state._y_require_active_transaction(0)
            if state._y_identity_state_working is not VOID:
                current = state._y_identity_state_working
            else:
                current = state._y_identity_state_current
            next_value = value
            if current is next_value:
                return
            state._y_ensure_working_transaction(0)
            state._y_identity_state_working = next_value

        @property
        def child(self):
            state = self._y_state
            if state._y_child_working is not VOID:
                return state._y_child_working
            return state._y_child_current

        @child.setter
        def child(self, value):
            state = self._y_state
            state._y_require_active_transaction(0)
            next_value = _y_validate_binding_value('child', value)
            if state._y_child_working is not VOID:
                current = state._y_child_working
            else:
                current = state._y_child_current
            if current == next_value:
                return
            state._y_ensure_working_transaction(0)
            state._y_child_working = next_value

        @property
        def identity_child(self):
            state = self._y_state
            if state._y_identity_child_working is not VOID:
                return state._y_identity_child_working
            return state._y_identity_child_current

        @identity_child.setter
        def identity_child(self, value):
            state = self._y_state
            state._y_require_active_transaction(0)
            next_value = _y_validate_binding_value('identity_child', value)
            if state._y_identity_child_working is not VOID:
                current = state._y_identity_child_working
            else:
                current = state._y_identity_child_current
            if current is next_value:
                return
            state._y_ensure_working_transaction(0)
            state._y_identity_child_working = next_value

        @property
        def children(self):
            state = self._y_state
            if state._y_children_working is not VOID:
                return state._y_children_working
            return state._y_children_current

        @children.setter
        def children(self, value):
            state = self._y_state
            state._y_require_active_transaction(0)
            next_value = _y_validate_binding_map_value('children', value)
            if state._y_children_working is not VOID:
                current = state._y_children_working
            else:
                current = state._y_children_current
            if current == next_value:
                return
            state._y_ensure_working_transaction(0)
            state._y_children_working = next_value
    Owner.__name__ = decorated_cls.__name__
    Owner.__qualname__ = decorated_cls.__qualname__
    Owner.__module__ = decorated_cls.__module__
    return Owner
