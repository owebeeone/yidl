from __future__ import annotations
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
    _Example_tx_groups,
    _Example_SCALE_default,
    _Example_seed_default,
    _Example_temp_default_factory,
    _Example_v2_default_factory,
    _Example_v3_default_factory,
    _Example_v4_default_factory,
    _Example_v5_default_factory,
):

    class Example_State:
        __slots__ = (
            "_y_transaction_manager",
            "_y_default_ref",
            "_y_current_ref",
            "_y_working_ref",
            "_y_v1_value",
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
        __yidl_tx_index_to_group__ = _Example_tx_groups
        __yidl_tx_group_to_index__ = {
            group: index for index, group in enumerate(_Example_tx_groups)
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
            default_ref = self._y_default_ref
            default = None if default_ref is None else default_ref()
            if default is not None:
                facade = default._y_current_facade
                if facade is None:
                    facade = object.__new__(Example_Current)
                    object.__setattr__(facade, "_y_state", self)
                    object.__setattr__(default, "_y_current_facade", facade)
                    self._y_current_ref = weakref.ref(facade)
                return facade
            ref = self._y_current_ref
            facade = None if ref is None else ref()
            if facade is None:
                facade = object.__new__(Example_Current)
                object.__setattr__(facade, "_y_state", self)
                self._y_current_ref = weakref.ref(facade)
            return facade

        def _y_get_working_facade(self):
            default_ref = self._y_default_ref
            default = None if default_ref is None else default_ref()
            if default is not None:
                facade = default._y_working_facade
                if facade is None:
                    facade = object.__new__(Example_Working)
                    object.__setattr__(facade, "_y_state", self)
                    object.__setattr__(default, "_y_working_facade", facade)
                    self._y_working_ref = weakref.ref(facade)
                return facade
            ref = self._y_working_ref
            facade = None if ref is None else ref()
            if facade is None:
                facade = object.__new__(Example_Working)
                object.__setattr__(facade, "_y_state", self)
                self._y_working_ref = weakref.ref(facade)
            return facade

        def _y_require_active_transaction(self, tx_index):
            tx_group = self.__yidl_tx_index_to_group__[tx_index]
            transaction = self._y_transaction_manager.active_transaction_for(tx_group)
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
                tx_group = self.__yidl_tx_index_to_group__[tx_index]
                self._y_working_tx_ids[tx_index] = self._y_transaction_manager.enlist(
                    self, tx_group
                )
            return transaction

        def commit_order_key_for(self, tx_group=DEFAULT_TRANSACTION):
            tx_index = self.__yidl_tx_group_to_index__[tx_group]
            if tx_index == 0:
                return self._commit_order_key_tx_0()
            return ()

        def requires_validation_for(self, tx_group=DEFAULT_TRANSACTION):
            tx_index = self.__yidl_tx_group_to_index__[tx_group]
            if tx_index == 0:
                return self._requires_validation_tx_0()
            return False

        def validate_commit_for(self, tx_group=DEFAULT_TRANSACTION):
            tx_index = self.__yidl_tx_group_to_index__[tx_group]
            if tx_index == 0:
                return self._validate_commit_tx_0()
            return True

        def _prepare_commit_tx_by_key(
            self, tx_group=DEFAULT_TRANSACTION, tx_token=None
        ):
            tx_index = self.__yidl_tx_group_to_index__[tx_group]
            if self._y_working_tx_ids[tx_index] != tx_token:
                raise RuntimeError("stale yidl transaction token")
            if tx_index == 0:
                self._before_commit_tx_0()
            if tx_index == 0:
                self._prepare_commit_tx_0_fields()
            return self._y_get_default_facade()

        def _apply_prepared_commit_tx_by_key(
            self, tx_group=DEFAULT_TRANSACTION, tx_token=None
        ):
            tx_index = self.__yidl_tx_group_to_index__[tx_group]
            if self._y_working_tx_ids[tx_index] != tx_token:
                raise RuntimeError("stale yidl transaction token")
            if tx_index == 0:
                self._apply_prepared_commit_tx_0_fields()
            self._y_working_tx_ids[tx_index] = None
            return self._y_get_default_facade()

        def _after_commit_tx_by_key(self, tx_group=DEFAULT_TRANSACTION, tx_token=None):
            del tx_token
            tx_index = self.__yidl_tx_group_to_index__[tx_group]
            if tx_index == 0:
                self._after_commit_tx_0()
            return self._y_get_default_facade()

        def _rollback_tx_by_key(self, tx_group=DEFAULT_TRANSACTION, tx_token=None):
            tx_index = self.__yidl_tx_group_to_index__[tx_group]
            del tx_token
            if tx_index == 0:
                self._rollback_tx_0_fields()
            self._y_working_tx_ids[tx_index] = None
            return self._y_get_default_facade()

        def _after_rollback_tx_by_key(
            self, tx_group=DEFAULT_TRANSACTION, tx_token=None
        ):
            del tx_token
            tx_index = self.__yidl_tx_group_to_index__[tx_group]
            if tx_index == 0:
                self._after_rollback_tx_0()
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
        __slots__ = ("_y_state",)
        _y_lifecycle_field_names = frozenset(("v1", "v2", "v3", "v4", "v5"))

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

        SCALE = _Example_SCALE_default

        @property
        def v1(self):
            return self._y_state._y_v1_value

        @v1.setter
        def v1(self, value):
            self._y_state._y_v1_value = value

    class Example(Example_FacadeBase):
        __slots__ = ("_y_current_facade", "_y_working_facade")
        __annotations__ = _Example_annotations
        __yidl_lifecycle_generated__ = True
        __yidl_lifecycle_user_class__ = decorated_cls
        __yidl_lifecycle_definition__ = _Example_lifecycle_definition
        __yidl_tx_index_to_group__ = _Example_tx_groups
        __yidl_tx_group_to_index__ = {
            group: index for index, group in enumerate(_Example_tx_groups)
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
            state._y_ensure_working_transaction(0)
            state._y_v2_working = value

        @property
        def v3(self):
            state = self._y_state
            if state._y_v3_working is not VOID:
                return state._y_v3_working
            return state._y_v3_current

        @v3.setter
        def v3(self, value):
            state = self._y_state
            state._y_ensure_working_transaction(0)
            state._y_v3_working = value

        @property
        def v4(self):
            state = self._y_state
            if state._y_v4_working is not VOID:
                return state._y_v4_working
            return state._y_v4_current

        @v4.setter
        def v4(self, value):
            state = self._y_state
            state._y_ensure_working_transaction(0)
            state._y_v4_working = value

        @property
        def v5(self):
            state = self._y_state
            if state._y_v5_working is not VOID:
                return state._y_v5_working
            return state._y_v5_current

        @v5.setter
        def v5(self, value):
            state = self._y_state
            state._y_ensure_working_transaction(0)
            state._y_v5_working = value

        def __init__(
            self,
            v1: "int",
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
                tx_groups=tuple(
                    (
                        group
                        for group in _Example_tx_groups
                        if group != DEFAULT_TRANSACTION
                    )
                )
            )
            state._y_default_ref = weakref.ref(self)
            state._y_current_ref = None
            state._y_working_ref = None
            state._y_v1_value = v1
            seed = _Example_seed_default
            state._y_v2_working = VOID
            state._y_v2_staged = VOID
            state._y_v3_working = VOID
            state._y_v3_staged = VOID
            state._y_v4_working = VOID
            state._y_v4_staged = VOID
            state._y_v5_working = VOID
            state._y_v5_staged = VOID
            temp = _Example_temp_default_factory(seed=seed, v1=self.v1)
            if v2 is _HAS_DEFAULT_FACTORY:
                v2 = _Example_v2_default_factory(v1=self.v1)
            state._y_v2_current = v2
            if v3 is _HAS_DEFAULT_FACTORY:
                v3 = _Example_v3_default_factory(v2=self.v2, v1=self.v1)
            state._y_v3_current = v3
            v4 = _Example_v4_default_factory(v3=self.v3)
            state._y_v4_current = v4
            v5 = _Example_v5_default_factory(SCALE=self.SCALE, v4=self.v4)
            state._y_v5_current = v5
            state._y_working_tx_ids = [None for _group in _Example_tx_groups]

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
            state._y_ensure_working_transaction(0)
            state._y_v2_working = value

        @property
        def v3(self):
            state = self._y_state
            if state._y_v3_working is not VOID:
                return state._y_v3_working
            return state._y_v3_current

        @v3.setter
        def v3(self, value):
            state = self._y_state
            state._y_ensure_working_transaction(0)
            state._y_v3_working = value

        @property
        def v4(self):
            state = self._y_state
            if state._y_v4_working is not VOID:
                return state._y_v4_working
            return state._y_v4_current

        @v4.setter
        def v4(self, value):
            state = self._y_state
            state._y_ensure_working_transaction(0)
            state._y_v4_working = value

        @property
        def v5(self):
            state = self._y_state
            if state._y_v5_working is not VOID:
                return state._y_v5_working
            return state._y_v5_current

        @v5.setter
        def v5(self, value):
            state = self._y_state
            state._y_ensure_working_transaction(0)
            state._y_v5_working = value

    Example.__name__ = decorated_cls.__name__
    Example.__qualname__ = decorated_cls.__qualname__
    Example.__module__ = decorated_cls.__module__
    return Example
