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
    _Config_lifecycle_definition,
    _Config_annotations,
    _Config_tx_groups,
    _Config_seed_default,
    _Config_slot_id_default,
    _Config_derived_id_default_factory,
    _Config_lazy_number_default,
    _Config_items_default_factory,
    _Config_seeded_static_default_factory,
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

    class Config_State:
        __slots__ = (
            "_y_transaction_manager",
            "_y_default_ref",
            "_y_current_ref",
            "_y_working_ref",
            "_y_slot_id_value",
            "_y_derived_id_value",
            "_y_declared_value",
            "_y_lazy_number_value",
            "_y_items_value",
            "_y_seeded_static_value",
            "_y_working_tx_ids",
        )
        __yidl_tx_index_to_key__ = _Config_tx_groups
        __yidl_tx_key_to_index__ = {
            key: index for index, key in enumerate(_Config_tx_groups)
        }

        def _y_get_default_facade(self):
            ref = self._y_default_ref
            facade = None if ref is None else ref()
            if facade is None:
                facade = object.__new__(Config)
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
                facade = object.__new__(Config_Current)
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
                facade = object.__new__(Config_Working)
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
            pass

        def _prepare_commit_tx_0_fields(self):
            pass

        def _after_rollback_tx_0(self):
            pass

        def _rollback_tx_0_fields(self):
            pass

    class Config_FacadeBase(decorated_cls):
        __slots__ = (
            ("_y_state",)
            if hasattr(decorated_cls, "__weakref__")
            else ("_y_state", "__weakref__")
        )
        _y_lifecycle_field_names = frozenset(
            (
                "slot_id",
                "derived_id",
                "declared",
                "lazy_number",
                "items",
                "seeded_static",
            )
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

        def begin(self, *tx_keys):
            return self._y_state._y_transaction_manager.begin(*tx_keys)

        def validate(self, *tx_keys):
            return self._y_state._y_transaction_manager.validate(*tx_keys)

        def commit_only(self, *tx_keys):
            return self._y_state._y_transaction_manager.commit_only(*tx_keys)

        def commit(self, *tx_keys):
            return self._y_state._y_transaction_manager.commit(*tx_keys)

        def rollback(self, *tx_keys):
            return self._y_state._y_transaction_manager.rollback(*tx_keys)

        @property
        def slot_id(self):
            return self._y_state._y_slot_id_value

        @slot_id.setter
        def slot_id(self, value):
            del value
            raise AttributeError(f"const field {'slot_id'!r} is read-only")

        @property
        def derived_id(self):
            return self._y_state._y_derived_id_value

        @derived_id.setter
        def derived_id(self, value):
            del value
            raise AttributeError(f"const field {'derived_id'!r} is read-only")

        @property
        def declared(self):
            value = self._y_state._y_declared_value
            if value is VOID:
                raise AttributeError(f"static field {'declared'!r} is not initialized")
            return value

        @declared.setter
        def declared(self, value):
            state = self._y_state
            if state._y_declared_value is VOID:
                state._y_declared_value = value
                return
            raise AttributeError(f"static field {'declared'!r} is already initialized")

        @property
        def lazy_number(self):
            state = self._y_state
            value = state._y_lazy_number_value
            if value is VOID:
                value = _Config_lazy_number_default
                state._y_lazy_number_value = value
            return value

        @lazy_number.setter
        def lazy_number(self, value):
            state = self._y_state
            if state._y_lazy_number_value is VOID:
                state._y_lazy_number_value = value
                return
            raise AttributeError(
                f"static field {'lazy_number'!r} is already initialized"
            )

        @property
        def items(self):
            state = self._y_state
            value = state._y_items_value
            if value is VOID:
                value = _Config_items_default_factory()
                state._y_items_value = value
            return value

        @items.setter
        def items(self, value):
            state = self._y_state
            if state._y_items_value is VOID:
                state._y_items_value = value
                return
            raise AttributeError(f"static field {'items'!r} is already initialized")

        @property
        def seeded_static(self):
            state = self._y_state
            value = state._y_seeded_static_value
            if value is VOID:
                value = _Config_seeded_static_default_factory(slot_id=self.slot_id)
                state._y_seeded_static_value = value
            return value

        @seeded_static.setter
        def seeded_static(self, value):
            state = self._y_state
            if state._y_seeded_static_value is VOID:
                state._y_seeded_static_value = value
                return
            raise AttributeError(
                f"static field {'seeded_static'!r} is already initialized"
            )

    class Config(Config_FacadeBase):
        __slots__ = ("_y_current_facade", "_y_working_facade")
        __annotations__ = _Config_annotations
        __yidl_lifecycle_generated__ = True
        __yidl_lifecycle_user_class__ = decorated_cls
        __yidl_lifecycle_definition__ = _Config_lifecycle_definition
        __yidl_tx_index_to_key__ = _Config_tx_groups
        __yidl_tx_key_to_index__ = {
            key: index for index, key in enumerate(_Config_tx_groups)
        }

        def __init__(
            self,
            seed: "int" = _Config_seed_default,
            slot_id: "int" = _Config_slot_id_default,
            derived_id: "int" = _HAS_DEFAULT_FACTORY,
            declared: "tuple[str, ...]" = _HAS_DEFAULT_FACTORY,
            lazy_number: "int" = _HAS_DEFAULT_FACTORY,
            items: "list[int]" = _HAS_DEFAULT_FACTORY,
            seeded_static: "int" = _HAS_DEFAULT_FACTORY,
            *,
            transaction_manager=None,
        ):
            state = object.__new__(Config_State)
            object.__setattr__(self, "_y_state", state)
            object.__setattr__(self, "_y_current_facade", None)
            object.__setattr__(self, "_y_working_facade", None)
            state._y_transaction_manager = transaction_manager or TransactionManager(
                tx_groups=tuple(
                    (
                        group
                        for group in _Config_tx_groups
                        if group != DEFAULT_TRANSACTION
                    )
                )
            )
            state._y_default_ref = weakref.ref(self)
            state._y_current_ref = None
            state._y_working_ref = None
            state._y_slot_id_value = slot_id
            if declared is _HAS_DEFAULT_FACTORY:
                state._y_declared_value = VOID
            else:
                state._y_declared_value = declared
            if lazy_number is _HAS_DEFAULT_FACTORY:
                state._y_lazy_number_value = VOID
            else:
                state._y_lazy_number_value = lazy_number
            if items is _HAS_DEFAULT_FACTORY:
                state._y_items_value = VOID
            else:
                state._y_items_value = items
            if seeded_static is _HAS_DEFAULT_FACTORY:
                state._y_seeded_static_value = VOID
            else:
                state._y_seeded_static_value = seeded_static
            if derived_id is _HAS_DEFAULT_FACTORY:
                derived_id = _Config_derived_id_default_factory(
                    seed=seed, slot_id=self.slot_id
                )
            state._y_derived_id_value = derived_id
            if False:
                _Config_items_default_factory()
            if False:
                _Config_seeded_static_default_factory(slot_id=self.slot_id)
            state._y_working_tx_ids = [None for _group in _Config_tx_groups]

    class Config_Current(Config_FacadeBase):
        __slots__ = ()

    class Config_Working(Config_FacadeBase):
        __slots__ = ()

    Config.__name__ = decorated_cls.__name__
    Config.__qualname__ = decorated_cls.__qualname__
    Config.__module__ = decorated_cls.__module__
    return Config
