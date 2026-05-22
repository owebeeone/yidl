from __future__ import annotations
import weakref
from yidl.runtime.lifecycle import _HAS_DEFAULT_FACTORY
from yidl.runtime.transaction_yidl import DEFAULT_TRANSACTION
from yidl.runtime.transaction_yidl import TransactionManager

VOID = object()


def build_lifecycle_class(
    decorated_cls,
    *,
    _Counter_lifecycle_definition,
    _Counter_annotations,
    _Counter_tx_groups,
    _Counter_plain_default,
    _Counter_seed_default,
    _Counter_KIND_default,
):

    class Counter_State:
        __slots__ = (
            "_y_transaction_manager",
            "_y_default_ref",
            "_y_current_ref",
            "_y_working_ref",
            "_y_plain_value",
            "_y_working_tx_ids",
        )
        __yidl_tx_index_to_key__ = _Counter_tx_groups
        __yidl_tx_key_to_index__ = {
            key: index for index, key in enumerate(_Counter_tx_groups)
        }

        def _y_get_default_facade(self):
            ref = self._y_default_ref
            facade = None if ref is None else ref()
            if facade is None:
                facade = object.__new__(Counter)
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
                facade = object.__new__(Counter_Current)
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
                facade = object.__new__(Counter_Working)
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
            elif True:
                return ()

        def requires_validation_for(self, tx_key=DEFAULT_TRANSACTION):
            tx_index = self.__yidl_tx_key_to_index__[tx_key]
            if False:
                pass
            elif True:
                return False

        def validate_commit_for(self, tx_key=DEFAULT_TRANSACTION):
            tx_index = self.__yidl_tx_key_to_index__[tx_key]
            if False:
                pass
            elif True:
                return True

        def _prepare_commit_tx_by_key(self, tx_key=DEFAULT_TRANSACTION, tx_token=None):
            tx_index = self.__yidl_tx_key_to_index__[tx_key]
            if self._y_working_tx_ids[tx_index] != tx_token:
                raise RuntimeError("stale yidl transaction token")
            if False:
                pass
            elif True:
                pass
            if False:
                pass
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
            elif True:
                pass
            pass
            self._y_working_tx_ids[tx_index] = None
            return self._y_get_default_facade()

        def _after_commit_tx_by_key(self, tx_key=DEFAULT_TRANSACTION, tx_token=None):
            del tx_token
            tx_index = self.__yidl_tx_key_to_index__[tx_key]
            if False:
                pass
            elif True:
                pass
            return self._y_get_default_facade()

        def _rollback_tx_by_key(self, tx_key=DEFAULT_TRANSACTION, tx_token=None):
            tx_index = self.__yidl_tx_key_to_index__[tx_key]
            del tx_token
            if False:
                pass
            elif True:
                pass
            pass
            self._y_working_tx_ids[tx_index] = None
            return self._y_get_default_facade()

        def _after_rollback_tx_by_key(self, tx_key=DEFAULT_TRANSACTION, tx_token=None):
            del tx_token
            tx_index = self.__yidl_tx_key_to_index__[tx_key]
            if False:
                pass
            elif True:
                pass
            return self._y_get_default_facade()

        pass
        pass

    class Counter_FacadeBase(decorated_cls):
        __slots__ = (
            ("_y_state",)
            if hasattr(decorated_cls, "__weakref__")
            else ("_y_state", "__weakref__")
        )
        _y_lifecycle_field_names = frozenset(())

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

        KIND = _Counter_KIND_default

        @property
        def plain(self):
            return self._y_state._y_plain_value

        @plain.setter
        def plain(self, value):
            self._y_state._y_plain_value = value

    class Counter(Counter_FacadeBase):
        __slots__ = ("_y_current_facade", "_y_working_facade")
        __annotations__ = _Counter_annotations
        __yidl_lifecycle_generated__ = True
        __yidl_lifecycle_user_class__ = decorated_cls
        __yidl_lifecycle_definition__ = _Counter_lifecycle_definition
        __yidl_tx_index_to_key__ = _Counter_tx_groups
        __yidl_tx_key_to_index__ = {
            key: index for index, key in enumerate(_Counter_tx_groups)
        }
        pass

        def __init__(
            self,
            plain: "int" = _Counter_plain_default,
            seed: "int" = _Counter_seed_default,
            *,
            transaction_manager=None,
        ):
            state = object.__new__(Counter_State)
            object.__setattr__(self, "_y_state", state)
            object.__setattr__(self, "_y_current_facade", None)
            object.__setattr__(self, "_y_working_facade", None)
            state._y_transaction_manager = transaction_manager or TransactionManager(
                tx_groups=tuple(
                    (
                        group
                        for group in _Counter_tx_groups
                        if group != DEFAULT_TRANSACTION
                    )
                )
            )
            state._y_default_ref = weakref.ref(self)
            state._y_current_ref = None
            state._y_working_ref = None
            state._y_plain_value = plain
            state._y_working_tx_ids = [None for _group in _Counter_tx_groups]

    class Counter_Current(Counter_FacadeBase):
        __slots__ = ()
        pass

    class Counter_Working(Counter_FacadeBase):
        __slots__ = ()
        pass

    Counter.__name__ = decorated_cls.__name__
    Counter.__qualname__ = decorated_cls.__qualname__
    Counter.__module__ = decorated_cls.__module__
    return Counter
