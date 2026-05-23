from __future__ import annotations
from collections.abc import Mapping
from yidl.runtime.bindings import BindingBase, BindingDict
import weakref
from yidl.runtime.lifecycle import _HAS_DEFAULT_FACTORY
from yidl.runtime.transaction_yidl import DEFAULT_TRANSACTION
from yidl.runtime.transaction_yidl import TransactionManager

VOID = object()


def build_lifecycle_class(
    decorated_cls,
    *,
    _Example_lifecycle_definition,
    _Example_annotations,
    _Example_tx_keys,
    _Example_SCALE_default,
    _Example_owner_default,
    _Example_owner_tag_default_factory,
    _Example_seed_default,
    _Example_class_name_size_default_factory,
    _Example_self_tag_size_default_factory,
    _Example_temp_default_factory,
    _Example_v2_default_factory,
    _Example_v3_default_factory,
    _Example_v4_default_factory,
    _Example_v5_default_factory,
):

    def _y_validate_binding_value(field_name, value):
        if value is not None and (not isinstance(value, BindingBase)):
            raise TypeError(
                "binding field " + repr(field_name) + " expects BindingBase or None"
            )
        return value

    def _y_validate_binding_map_value(field_name, value):
        if value is None:
            return None
        if not isinstance(value, Mapping):
            raise TypeError(
                "binding map field " + repr(field_name) + " expects a mapping or None"
            )
        result = value if isinstance(value, BindingDict) else BindingDict(value)
        for key, item in result.items():
            if not isinstance(item, BindingBase):
                raise TypeError(
                    "binding map field "
                    + repr(field_name)
                    + " expects BindingBase values; key "
                    + repr(key)
                    + " has "
                    + type(item).__name__
                )
        return result

    class Example_State:
        __slots__ = (
            "_y_transaction_manager",
            "_y_default_ref",
            "_y_current_ref",
            "_y_working_ref",
            "_y_v1_value",
            "_y_owner_value",
            "_y_owner_tag_value",
            "_y_v2_current",
            "_y_v2_working",
            "_y_v2_staged",
            "_y_v3_current",
            "_y_v3_working",
            "_y_v3_staged",
            "_y_v4_current",
            "_y_v4_working",
            "_y_v4_staged",
            "_y_v5_current",
            "_y_v5_working",
            "_y_v5_staged",
            "_y_working_tx_ids",
        )
        __yidl_tx_index_to_key__ = _Example_tx_keys
        __yidl_tx_key_to_index__ = {
            key: index for index, key in enumerate(_Example_tx_keys)
        }

        def _y_get_default_facade(self):
            ref = self._y_default_ref
            facade = None if ref is None else ref()
            if facade is None:
                facade = object.__new__(Example)
                object.__setattr__(facade, "_y_state", self)
                current_ref = self._y_current_ref
                working_ref = self._y_working_ref
                object.__setattr__(
                    facade,
                    "_y_current_facade",
                    None if current_ref is None else current_ref(),
                )
                object.__setattr__(
                    facade,
                    "_y_working_facade",
                    None if working_ref is None else working_ref(),
                )
                self._y_default_ref = weakref.ref(facade)
            return facade

        def _y_get_current_facade(self):
            ref = self._y_current_ref
            facade = None if ref is None else ref()
            if facade is None:
                facade = object.__new__(Example_Current)
                object.__setattr__(facade, "_y_state", self)
                self._y_current_ref = weakref.ref(facade)
                default_ref = self._y_default_ref
                default = None if default_ref is None else default_ref()
                if default is not None:
                    object.__setattr__(default, "_y_current_facade", facade)
            return facade

        def _y_get_working_facade(self):
            ref = self._y_working_ref
            facade = None if ref is None else ref()
            if facade is None:
                facade = object.__new__(Example_Working)
                object.__setattr__(facade, "_y_state", self)
                self._y_working_ref = weakref.ref(facade)
                default_ref = self._y_default_ref
                default = None if default_ref is None else default_ref()
                if default is not None:
                    object.__setattr__(default, "_y_working_facade", facade)
            return facade

        def _y_require_active_transaction(self, tx_index):
            tx_key = self.__yidl_tx_index_to_key__[tx_index]
            transaction = self._y_transaction_manager.active_transaction_for(tx_key)
            if transaction is None:
                if self._y_working_tx_ids[tx_index] is not None:
                    raise RuntimeError(
                        "stale yidl working value without an active transaction"
                    )
                raise RuntimeError("writes require an active yidl transaction")
            existing_tx_id = self._y_working_tx_ids[tx_index]
            if existing_tx_id is not None and existing_tx_id != transaction.tx_id:
                raise RuntimeError(
                    "working value belongs to a different yidl transaction"
                )
            return transaction

        def _y_ensure_working_transaction(self, tx_index):
            transaction = self._y_require_active_transaction(tx_index)
            if self._y_working_tx_ids[tx_index] is None:
                tx_key = self.__yidl_tx_index_to_key__[tx_index]
                self._y_working_tx_ids[tx_index] = self._y_transaction_manager.enlist(
                    self, tx_key
                )
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
                raise RuntimeError("stale yidl transaction token")
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

        def _apply_prepared_commit_tx_by_key(
            self, tx_key=DEFAULT_TRANSACTION, tx_token=None
        ):
            tx_index = self.__yidl_tx_key_to_index__[tx_key]
            if self._y_working_tx_ids[tx_index] != tx_token:
                raise RuntimeError("stale yidl transaction token")
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
            if self._y_v2_staged is not VOID:
                self._y_v2_current = self._y_v2_staged
                self._y_v2_staged = VOID
                self._y_v2_working = VOID
            if self._y_v3_staged is not VOID:
                self._y_v3_current = self._y_v3_staged
                self._y_v3_staged = VOID
                self._y_v3_working = VOID
            if self._y_v4_staged is not VOID:
                self._y_v4_current = self._y_v4_staged
                self._y_v4_staged = VOID
                self._y_v4_working = VOID
            if self._y_v5_staged is not VOID:
                self._y_v5_current = self._y_v5_staged
                self._y_v5_staged = VOID
                self._y_v5_working = VOID

        def _prepare_commit_tx_0_fields(self):
            if self._y_v2_working is not VOID:
                self._y_v2_staged = self._y_v2_working
            if self._y_v3_working is not VOID:
                self._y_v3_staged = self._y_v3_working
            if self._y_v4_working is not VOID:
                self._y_v4_staged = self._y_v4_working
            if self._y_v5_working is not VOID:
                self._y_v5_staged = self._y_v5_working

        def _after_rollback_tx_0(self):
            pass

        def _rollback_tx_0_fields(self):
            self._y_v2_staged = VOID
            self._y_v2_working = VOID
            self._y_v3_staged = VOID
            self._y_v3_working = VOID
            self._y_v4_staged = VOID
            self._y_v4_working = VOID
            self._y_v5_staged = VOID
            self._y_v5_working = VOID

    class Example_FacadeBase(decorated_cls):
        __slots__ = (
            ("_y_state",)
            if hasattr(decorated_cls, "__weakref__")
            else ("_y_state", "__weakref__")
        )
        _y_lifecycle_field_names = frozenset(
            ("v1", "owner", "owner_tag", "v2", "v3", "v4", "v5")
        )

        def __setattr__(self, name, value):
            if name in self._y_lifecycle_field_names:
                descriptor = getattr(type(self), name, None)
                if descriptor is None or not hasattr(descriptor, "__set__"):
                    raise AttributeError(f"lifecycle field {name!r} is not assignable")
                descriptor.__set__(self, value)
                return
            if name.startswith("_y_") or name.startswith("__yidl_"):
                raise AttributeError(
                    f"{name!r} is reserved for generated lifecycle state"
                )
            object.__setattr__(self, name, value)

        def __delattr__(self, name):
            if name in self._y_lifecycle_field_names:
                raise AttributeError(f"lifecycle field {name!r} cannot be deleted")
            if name.startswith("_y_") or name.startswith("__yidl_"):
                raise AttributeError(
                    f"{name!r} is reserved for generated lifecycle state"
                )
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

        SCALE = _Example_SCALE_default

        @property
        def v1(self):
            return self._y_state._y_v1_value

        @v1.setter
        def v1(self, value):
            self._y_state._y_v1_value = value

        @property
        def owner(self):
            return self._y_state._y_owner_value

        @owner.setter
        def owner(self, value):
            del value
            raise AttributeError(f"const field {'owner'!r} is read-only")

        @property
        def owner_tag(self):
            return self._y_state._y_owner_tag_value

        @owner_tag.setter
        def owner_tag(self, value):
            del value
            raise AttributeError(f"const field {'owner_tag'!r} is read-only")

    class Example(Example_FacadeBase):
        __slots__ = ("_y_current_facade", "_y_working_facade")
        __annotations__ = _Example_annotations
        __yidl_lifecycle_generated__ = True
        __yidl_lifecycle_user_class__ = decorated_cls
        __yidl_lifecycle_definition__ = _Example_lifecycle_definition
        __yidl_tx_index_to_key__ = _Example_tx_keys
        __yidl_tx_key_to_index__ = {
            key: index for index, key in enumerate(_Example_tx_keys)
        }

        @property
        def v2(self):
            state = self._y_state
            if state._y_v2_working is not VOID:
                return state._y_v2_working
            return state._y_v2_current

        @v2.setter
        def v2(self, value):
            state = self._y_state
            state._y_require_active_transaction(0)
            if state._y_v2_working is not VOID:
                current = state._y_v2_working
            else:
                current = state._y_v2_current
            next_value = value
            if current == next_value:
                return
            state._y_ensure_working_transaction(0)
            state._y_v2_working = next_value

        @property
        def v3(self):
            state = self._y_state
            if state._y_v3_working is not VOID:
                return state._y_v3_working
            return state._y_v3_current

        @v3.setter
        def v3(self, value):
            state = self._y_state
            state._y_require_active_transaction(0)
            if state._y_v3_working is not VOID:
                current = state._y_v3_working
            else:
                current = state._y_v3_current
            next_value = value
            if current == next_value:
                return
            state._y_ensure_working_transaction(0)
            state._y_v3_working = next_value

        @property
        def v4(self):
            state = self._y_state
            if state._y_v4_working is not VOID:
                return state._y_v4_working
            return state._y_v4_current

        @v4.setter
        def v4(self, value):
            state = self._y_state
            state._y_require_active_transaction(0)
            if state._y_v4_working is not VOID:
                current = state._y_v4_working
            else:
                current = state._y_v4_current
            next_value = value
            if current == next_value:
                return
            state._y_ensure_working_transaction(0)
            state._y_v4_working = next_value

        @property
        def v5(self):
            state = self._y_state
            if state._y_v5_working is not VOID:
                return state._y_v5_working
            return state._y_v5_current

        @v5.setter
        def v5(self, value):
            state = self._y_state
            state._y_require_active_transaction(0)
            if state._y_v5_working is not VOID:
                current = state._y_v5_working
            else:
                current = state._y_v5_current
            next_value = value
            if current == next_value:
                return
            state._y_ensure_working_transaction(0)
            state._y_v5_working = next_value

        def __init__(
            self,
            v1: "int",
            owner: "str" = _Example_owner_default,
            owner_tag: "str" = _HAS_DEFAULT_FACTORY,
            v2: "int" = _HAS_DEFAULT_FACTORY,
            v3: "int" = _HAS_DEFAULT_FACTORY,
            *,
            transaction_manager=None,
        ):
            state = object.__new__(Example_State)
            object.__setattr__(self, "_y_state", state)
            object.__setattr__(self, "_y_current_facade", None)
            object.__setattr__(self, "_y_working_facade", None)
            state._y_transaction_manager = transaction_manager or TransactionManager(
                tx_keys=tuple(
                    (
                        group
                        for group in _Example_tx_keys
                        if group != DEFAULT_TRANSACTION
                    )
                )
            )
            state._y_default_ref = weakref.ref(self)
            state._y_current_ref = None
            state._y_working_ref = None
            state._y_v1_value = v1
            state._y_owner_value = owner
            seed = _Example_seed_default
            state._y_v2_working = VOID
            state._y_v2_staged = VOID
            state._y_v3_working = VOID
            state._y_v3_staged = VOID
            state._y_v4_working = VOID
            state._y_v4_staged = VOID
            state._y_v5_working = VOID
            state._y_v5_staged = VOID
            class_name_size = _Example_class_name_size_default_factory(
                cls=decorated_cls
            )
            temp = _Example_temp_default_factory(seed=seed, v1=self.v1)
            if v2 is _HAS_DEFAULT_FACTORY:
                v2 = _Example_v2_default_factory(v1=self.v1)
            state._y_v2_current = v2
            if v3 is _HAS_DEFAULT_FACTORY:
                v3 = _Example_v3_default_factory(v2=self.v2, v1=self.v1)
            state._y_v3_current = v3
            v4 = _Example_v4_default_factory(v3=self.v3)
            state._y_v4_current = v4
            self_tag_size = _Example_self_tag_size_default_factory(self=self)
            v5 = _Example_v5_default_factory(
                class_name_size=class_name_size,
                self_tag_size=self_tag_size,
                SCALE=self.SCALE,
                v4=self.v4,
            )
            state._y_v5_current = v5
            if owner_tag is _HAS_DEFAULT_FACTORY:
                owner_tag = _Example_owner_tag_default_factory(self=self)
            state._y_owner_tag_value = owner_tag
            state._y_working_tx_ids = [None for _group in _Example_tx_keys]

    class Example_Current(Example_FacadeBase):
        __slots__ = ()

        @property
        def v2(self):
            return self._y_state._y_v2_current

        @v2.setter
        def v2(self, value):
            del value
            raise AttributeError(
                "current facade is read-only for transactional field " + "v2"
            )

        @property
        def v3(self):
            return self._y_state._y_v3_current

        @v3.setter
        def v3(self, value):
            del value
            raise AttributeError(
                "current facade is read-only for transactional field " + "v3"
            )

        @property
        def v4(self):
            return self._y_state._y_v4_current

        @v4.setter
        def v4(self, value):
            del value
            raise AttributeError(
                "current facade is read-only for transactional field " + "v4"
            )

        @property
        def v5(self):
            return self._y_state._y_v5_current

        @v5.setter
        def v5(self, value):
            del value
            raise AttributeError(
                "current facade is read-only for transactional field " + "v5"
            )

    class Example_Working(Example_FacadeBase):
        __slots__ = ()

        @property
        def v2(self):
            state = self._y_state
            if state._y_v2_working is not VOID:
                return state._y_v2_working
            return state._y_v2_current

        @v2.setter
        def v2(self, value):
            state = self._y_state
            state._y_require_active_transaction(0)
            if state._y_v2_working is not VOID:
                current = state._y_v2_working
            else:
                current = state._y_v2_current
            next_value = value
            if current == next_value:
                return
            state._y_ensure_working_transaction(0)
            state._y_v2_working = next_value

        @property
        def v3(self):
            state = self._y_state
            if state._y_v3_working is not VOID:
                return state._y_v3_working
            return state._y_v3_current

        @v3.setter
        def v3(self, value):
            state = self._y_state
            state._y_require_active_transaction(0)
            if state._y_v3_working is not VOID:
                current = state._y_v3_working
            else:
                current = state._y_v3_current
            next_value = value
            if current == next_value:
                return
            state._y_ensure_working_transaction(0)
            state._y_v3_working = next_value

        @property
        def v4(self):
            state = self._y_state
            if state._y_v4_working is not VOID:
                return state._y_v4_working
            return state._y_v4_current

        @v4.setter
        def v4(self, value):
            state = self._y_state
            state._y_require_active_transaction(0)
            if state._y_v4_working is not VOID:
                current = state._y_v4_working
            else:
                current = state._y_v4_current
            next_value = value
            if current == next_value:
                return
            state._y_ensure_working_transaction(0)
            state._y_v4_working = next_value

        @property
        def v5(self):
            state = self._y_state
            if state._y_v5_working is not VOID:
                return state._y_v5_working
            return state._y_v5_current

        @v5.setter
        def v5(self, value):
            state = self._y_state
            state._y_require_active_transaction(0)
            if state._y_v5_working is not VOID:
                current = state._y_v5_working
            else:
                current = state._y_v5_current
            next_value = value
            if current == next_value:
                return
            state._y_ensure_working_transaction(0)
            state._y_v5_working = next_value

    Example.__name__ = decorated_cls.__name__
    Example.__qualname__ = decorated_cls.__qualname__
    Example.__module__ = decorated_cls.__module__
    return Example
