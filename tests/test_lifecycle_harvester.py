from __future__ import annotations

import inspect

import pytest

from yidl.runtime.lifecycle import LifecycleDefinitionError
from yidl.runtime.lifecycle import LifecycleDefinitionWarning
from yidl.runtime.lifecycle import MISSING
from yidl.runtime.lifecycle import after_commit
from yidl.runtime.lifecycle import after_rollback
from yidl.runtime.lifecycle import before_commit
from yidl.runtime.lifecycle import classvar
from yidl.runtime.lifecycle import commit_order_key
from yidl.runtime.lifecycle import field
from yidl.runtime.lifecycle import harvest_lifecycle_definition
from yidl.runtime.lifecycle import initvar
from yidl.runtime.lifecycle import local_store
from yidl.runtime.lifecycle import managed
from yidl.runtime.lifecycle import validate_commit
from yidl.runtime.transaction_yidl import DEFAULT_TRANSACTION


def test_harvests_phase_a_compatible_facts() -> None:
    def freeze_count(value: object) -> object:
        return value

    def thaw_count(value: object) -> object:
        return value

    class Counter:
        plain: int = field(default=3)
        optional: str | None = field(default=None)
        tags: list[str] = field(default_factory=list)
        seed: int = initvar(default=2)
        KIND: str = classvar(default="counter")
        count: int = managed(default=1, freeze=freeze_count, thaw=thaw_count)
        audit_count: int = managed("audit", default=10)

    harvested = harvest_lifecycle_definition(Counter)

    assert harvested.class_fact == {
        "class_id": "test_harvests_phase_a_compatible_facts.<locals>.Counter",
        "class_name": "Counter",
        "class_order": 10,
        "module_name": __name__,
        "state_class_name": "Counter_State",
        "facade_base_class_name": "Counter_FacadeBase",
        "current_facade_class_name": "Counter_Current",
        "working_facade_class_name": "Counter_Working",
        "lifecycle_definition_param_name": "_Counter_lifecycle_definition",
        "annotations_param_name": "_Counter_annotations",
        "tx_keys_param_name": "_Counter_tx_keys",
        "lifecycle_field_names": (
            "plain",
            "optional",
            "tags",
            "count",
            "audit_count",
        ),
    }
    assert [
        (
            fact["field_name"],
            fact["field_kind"],
            fact["field_order"],
            fact["default_value_param_name"],
            fact["tx_key_key"],
        )
        for fact in harvested.field_facts
    ] == [
        ("plain", "field", 10, "_Counter_plain_default", None),
        ("optional", "field", 20, "_Counter_optional_default", None),
        ("tags", "field", 30, "", None),
        ("seed", "initvar", 40, "_Counter_seed_default", None),
        ("KIND", "classvar", 50, "_Counter_KIND_default", None),
        ("count", "managed", 60, "_Counter_count_default", DEFAULT_TRANSACTION),
        ("audit_count", "managed", 70, "_Counter_audit_count_default", "audit"),
    ]
    assert harvested.field_facts[0]["value_slot_name"] == "_y_plain_value"
    assert harvested.field_facts[5]["current_slot_name"] == "_y_count_current"
    assert harvested.field_facts[5]["working_slot_name"] == "_y_count_working"
    assert harvested.field_facts[5]["staged_slot_name"] == "_y_count_staged"
    assert harvested.field_facts[5]["has_freeze"] is True
    assert harvested.field_facts[5]["freeze"] is freeze_count
    assert harvested.field_facts[5]["freeze_param_name"] == "_Counter_count_freeze"
    assert harvested.field_facts[5]["has_thaw"] is True
    assert harvested.field_facts[5]["thaw"] is thaw_count
    assert harvested.field_facts[5]["thaw_param_name"] == "_Counter_count_thaw"
    assert harvested.field_facts[5]["has_optional_none"] is False
    assert harvested.field_facts[6]["has_freeze"] is False
    assert harvested.field_facts[6]["has_thaw"] is False
    assert harvested.tx_keys == (DEFAULT_TRANSACTION, "audit")
    assert harvested.lifecycle_definition["version"] == 1
    assert harvested.lifecycle_definition["fields"] == harvested.field_facts
    assert harvested.build_kwargs["_Counter_lifecycle_definition"] is (
        harvested.lifecycle_definition
    )
    assert harvested.build_kwargs["_Counter_annotations"] == Counter.__annotations__
    assert harvested.build_kwargs["_Counter_tx_keys"] == (
        DEFAULT_TRANSACTION,
        "audit",
    )
    assert harvested.build_kwargs["_Counter_optional_default"] is None
    assert harvested.build_kwargs["_Counter_tags_default_factory"] is list
    assert harvested.build_kwargs["_Counter_count_freeze"] is freeze_count
    assert harvested.build_kwargs["_Counter_count_thaw"] is thaw_count


def test_harvester_marks_optional_none_managed_field() -> None:
    class Counter:
        optional: tuple[int, ...] | None = managed(default=None)

    harvested = harvest_lifecycle_definition(Counter)

    assert harvested.field_facts[0]["field_name"] == "optional"
    assert harvested.field_facts[0]["has_optional_none"] is True


def test_harvester_treats_plain_assignment_as_default_field() -> None:
    class Counter:
        plain: int = 3
        required: str

    harvested = harvest_lifecycle_definition(Counter)

    assert [
        (fact["field_name"], fact["has_default"], fact["default_value"])
        for fact in harvested.field_facts
    ] == [
        ("plain", True, 3),
        ("required", False, MISSING),
    ]


def test_harvester_keeps_init_false_initvar_with_default_as_provider() -> None:
    class Counter:
        seed: int = initvar(init=False, default=2)
        plain: int = field(default=3)

    harvested = harvest_lifecycle_definition(Counter)

    assert [fact["field_name"] for fact in harvested.field_facts] == [
        "seed",
        "plain",
    ]
    assert harvested.field_facts[0]["field_kind"] == "initvar"
    assert harvested.field_facts[0]["init"] is False
    assert harvested.build_kwargs["_Counter_seed_default"] == 2


def test_harvester_keeps_init_false_initvar_with_default_factory_as_provider() -> None:
    def make_seed() -> int:
        return 2

    class Counter:
        seed: int = initvar(init=False, default_factory=make_seed)
        plain: int = field(default=3)

    harvested = harvest_lifecycle_definition(Counter)

    assert [fact["field_name"] for fact in harvested.field_facts] == [
        "seed",
        "plain",
    ]
    assert harvested.field_facts[0]["default_factory"] is make_seed
    assert harvested.field_facts[0]["default_factory_param_names"] == ()
    assert harvested.build_kwargs["_Counter_seed_default_factory"] is make_seed


def test_harvester_rejects_init_false_initvar_without_value_source() -> None:
    class Counter:
        seed: int = initvar(init=False)

    with pytest.raises(
        LifecycleDefinitionError,
        match=r"Counter\.seed: initvar\(init=False\) must define default or default_factory",
    ):
        harvest_lifecycle_definition(Counter)


def test_harvester_collects_default_factory_parameter_names() -> None:
    def make_v3(cls: type[object], v2: int, v1: int = 4, *, scale: int) -> int:
        del cls
        return v1 + v2 + scale

    class Counter:
        v1: int
        v2: int = field(default_factory=list)
        v3: int = managed(default_factory=make_v3)

    harvested = harvest_lifecycle_definition(Counter)

    assert [
        (fact["field_name"], fact["default_factory_param_names"])
        for fact in harvested.field_facts
    ] == [
        ("v1", ()),
        ("v2", ()),
        ("v3", ("cls", "v2", "v1", "scale")),
    ]


def test_harvester_ignores_optional_factory_class_parameters() -> None:
    class Value:
        def __init__(self, runtime_func: object | None = None) -> None:
            self.runtime_func = runtime_func

    class Counter:
        value: Value = field(default_factory=Value)

    harvested = harvest_lifecycle_definition(Counter)

    assert harvested.field_facts[0]["default_factory_param_names"] == ()


def test_harvester_carries_allow_self_factory() -> None:
    def make_value(self: object) -> int:
        del self
        return 1

    class Counter:
        value: int = field(
            default_factory=make_value,
            allow_self_factory=True,
        )

    harvested = harvest_lifecycle_definition(Counter)

    assert harvested.field_facts[0]["allow_self_factory"] is True
    assert harvested.field_facts[0]["default_factory_param_names"] == ("self",)


def test_harvester_collects_local_store_field() -> None:
    class Scratch:
        cache: dict[str, int] = local_store(default_factory=dict)
        token: str = local_store(default="ready")

    harvested = harvest_lifecycle_definition(Scratch)

    assert harvested.field_facts[0]["field_kind"] == "local_store"
    assert harvested.field_facts[0]["init"] is False
    assert harvested.field_facts[0]["value_slot_name"] == "_y_cache_value"
    assert harvested.field_facts[0]["default_factory_param_names"] == ()
    assert harvested.build_kwargs["_Scratch_cache_default_factory"] is dict
    assert harvested.field_facts[1]["field_kind"] == "local_store"
    assert harvested.field_facts[1]["has_default"] is True
    assert harvested.build_kwargs["_Scratch_token_default"] == "ready"


def test_harvester_rejects_local_store_default_factory_parameters() -> None:
    def make_cache(seed: int) -> dict[str, int]:
        return {"seed": seed}

    class Scratch:
        cache: dict[str, int] = local_store(default_factory=make_cache)

    with pytest.raises(
        LifecycleDefinitionError,
        match="Scratch.cache: local_store default_factory must be zero-argument",
    ):
        harvest_lifecycle_definition(Scratch)


def test_local_store_marker_rejects_transaction_options() -> None:
    with pytest.raises(
        LifecycleDefinitionError,
        match="local_store does not support tx_key",
    ):
        local_store(default_factory=dict, tx_key=DEFAULT_TRANSACTION)

    with pytest.raises(
        LifecycleDefinitionError,
        match="local_store does not support working_default_factory",
    ):
        local_store(default_factory=dict, working_default_factory=list)


def test_harvester_warns_for_unintrospectable_default_factory(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    def make_value() -> int:
        return 1

    def raise_for_callable(value: object) -> object:
        if value is make_value:
            raise ValueError("no signature")
        return original_signature(value)

    original_signature = inspect.signature
    monkeypatch.setattr(inspect, "signature", raise_for_callable)

    class Counter:
        value: int = field(default_factory=make_value)

    with pytest.warns(
        LifecycleDefinitionWarning,
        match="default_factory signature could not be introspected",
    ):
        harvested = harvest_lifecycle_definition(Counter)

    assert harvested.field_facts[0]["default_factory_param_names"] == ()


def test_harvester_warns_for_unintrospectable_class_default_factory(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    class Factory:
        pass

    def raise_for_callable(value: object) -> object:
        if value is Factory:
            raise ValueError("no signature")
        return original_signature(value)

    original_signature = inspect.signature
    monkeypatch.setattr(inspect, "signature", raise_for_callable)

    class Counter:
        value: object = field(default_factory=Factory)

    with pytest.warns(
        LifecycleDefinitionWarning,
        match="default_factory signature could not be introspected",
    ):
        harvested = harvest_lifecycle_definition(Counter)

    assert harvested.field_facts[0]["default_factory_param_names"] == ()


def test_harvester_rejects_required_positional_only_default_factory_parameter() -> None:
    def make_value(v1: int, /) -> int:
        return v1

    class Counter:
        v1: int
        v2: int = managed(default_factory=make_value)

    with pytest.raises(
        LifecycleDefinitionError,
        match="default_factory parameters must be bindable by name",
    ):
        harvest_lifecycle_definition(Counter)


def test_harvester_rejects_varargs_default_factory_parameter() -> None:
    def make_value(*values: int) -> int:
        return sum(values)

    class Counter:
        v1: int
        v2: int = managed(default_factory=make_value)

    with pytest.raises(
        LifecycleDefinitionError,
        match="default_factory parameters must be bindable by name",
    ):
        harvest_lifecycle_definition(Counter)


def test_harvester_rejects_kwargs_default_factory_parameter() -> None:
    def make_value(**values: int) -> int:
        return sum(values.values())

    class Counter:
        v1: int
        v2: int = managed(default_factory=make_value)

    with pytest.raises(
        LifecycleDefinitionError,
        match="default_factory parameters must be bindable by name",
    ):
        harvest_lifecycle_definition(Counter)


def test_harvester_rejects_reserved_class_body_names() -> None:
    class Counter:
        _y_state: int = 1

    with pytest.raises(LifecycleDefinitionError, match="Counter._y_state"):
        harvest_lifecycle_definition(Counter)


def test_harvester_rejects_transaction_manager_helper_collision() -> None:
    class Counter:
        def _y_get_transaction_manager(self) -> object:
            return None

    with pytest.raises(
        LifecycleDefinitionError,
        match="Counter._y_get_transaction_manager",
    ):
        harvest_lifecycle_definition(Counter)


def test_harvester_preserves_first_transaction_group_order() -> None:
    class Counter:
        audit: int = managed("audit", default=1)
        plain: int = field(default=2)
        other: int = managed("other", default=3)
        audit_again: int = managed("audit", default=4)

    harvested = harvest_lifecycle_definition(Counter)

    assert harvested.tx_keys == (DEFAULT_TRANSACTION, "audit", "other")


def test_harvester_merges_inherited_generated_lifecycle_facts() -> None:
    class BaseOriginal:
        plain: int = field(default=1)
        v1: int = managed("audit", default=2)

    base_harvested = harvest_lifecycle_definition(BaseOriginal)

    class GeneratedBase:
        __yidl_lifecycle_generated__ = True
        __yidl_lifecycle_definition__ = base_harvested.lifecycle_definition

    class Derived(GeneratedBase):
        plain: int = managed("audit", default=3)
        v2: int = managed("other", default=4)

    harvested = harvest_lifecycle_definition(Derived)

    assert [
        (
            fact["field_name"],
            fact["field_kind"],
            fact["field_order"],
            fact["field_owner"],
            fact["default_value"],
            fact["default_value_param_name"],
            fact["tx_key_key"],
        )
        for fact in harvested.field_facts
    ] == [
        (
            "plain",
            "managed",
            10,
            "test_harvester_merges_inherited_generated_lifecycle_facts.<locals>.Derived",
            3,
            "_Derived_plain_default",
            "audit",
        ),
        (
            "v1",
            "managed",
            20,
            "test_harvester_merges_inherited_generated_lifecycle_facts.<locals>.Derived",
            2,
            "_Derived_v1_default",
            "audit",
        ),
        (
            "v2",
            "managed",
            30,
            "test_harvester_merges_inherited_generated_lifecycle_facts.<locals>.Derived",
            4,
            "_Derived_v2_default",
            "other",
        ),
    ]
    assert harvested.tx_keys == (DEFAULT_TRANSACTION, "audit", "other")
    assert harvested.build_kwargs["_Derived_v1_default"] == 2


def test_harvester_sorts_inherited_facts_by_field_order() -> None:
    class BaseOriginal:
        first: int = field(default=1)
        second: int = field(default=2)

    base_harvested = harvest_lifecycle_definition(BaseOriginal)
    reversed_definition = {
        "version": 1,
        "fields": tuple(reversed(base_harvested.field_facts)),
        "tx_keys": base_harvested.tx_keys,
    }

    class GeneratedBase:
        __yidl_lifecycle_generated__ = True
        __yidl_lifecycle_definition__ = reversed_definition

    class Derived(GeneratedBase):
        third: int = field(default=3)

    harvested = harvest_lifecycle_definition(Derived)

    assert [fact["field_name"] for fact in harvested.field_facts] == [
        "first",
        "second",
        "third",
    ]


def test_harvester_rejects_managed_to_unmanaged_override() -> None:
    class BaseOriginal:
        value: int = managed(default=1)

    class GeneratedBase:
        __yidl_lifecycle_generated__ = True
        __yidl_lifecycle_definition__ = harvest_lifecycle_definition(
            BaseOriginal,
        ).lifecycle_definition

    class Derived(GeneratedBase):
        value: int = field(default=2)

    with pytest.raises(
        LifecycleDefinitionError,
        match="managed lifecycle field cannot be overridden as field",
    ):
        harvest_lifecycle_definition(Derived)


def test_harvester_rejects_managed_transaction_group_change() -> None:
    class BaseOriginal:
        value: int = managed("audit", default=1)

    class GeneratedBase:
        __yidl_lifecycle_generated__ = True
        __yidl_lifecycle_definition__ = harvest_lifecycle_definition(
            BaseOriginal,
        ).lifecycle_definition

    class Derived(GeneratedBase):
        value: int = managed("other", default=2)

    with pytest.raises(
        LifecycleDefinitionError,
        match="cannot change transaction key",
    ):
        harvest_lifecycle_definition(Derived)


def test_harvester_rejects_malformed_inherited_lifecycle_metadata() -> None:
    class GeneratedBase:
        __yidl_lifecycle_generated__ = True
        __yidl_lifecycle_definition__ = {
            "version": 1,
            "fields": (),
            "tx_keys": ("audit", DEFAULT_TRANSACTION),
        }

    class Derived(GeneratedBase):
        value: int = field(default=1)

    with pytest.raises(
        LifecycleDefinitionError,
        match="transaction key indexes are invalid",
    ):
        harvest_lifecycle_definition(Derived)


def test_harvester_collects_transaction_method_markers() -> None:
    class Counter:
        count: int = managed(default=1)
        audit_count: int = managed("audit", default=10)

        @commit_order_key(DEFAULT_TRANSACTION)
        def _default_key(self) -> tuple[int]:
            return (self.count,)

        @validate_commit(DEFAULT_TRANSACTION)
        def _validate_default(self) -> bool:
            return self.count >= 0

        @before_commit(DEFAULT_TRANSACTION)
        def _before_default(self) -> None:
            return None

        @after_commit(DEFAULT_TRANSACTION)
        def _after_default(self) -> None:
            return None

        @after_rollback("audit")
        def _after_audit_rollback(self) -> None:
            return None

    harvested = harvest_lifecycle_definition(Counter)

    assert [
        (
            fact["method_kind"],
            fact["method_name"],
            fact["tx_key_key"],
            fact["declaration_order"],
        )
        for fact in harvested.transaction_method_facts
    ] == [
        ("commit_order_key", "_default_key", DEFAULT_TRANSACTION, 10),
        ("validate_commit", "_validate_default", DEFAULT_TRANSACTION, 20),
        ("before_commit", "_before_default", DEFAULT_TRANSACTION, 30),
        ("after_commit", "_after_default", DEFAULT_TRANSACTION, 40),
        ("after_rollback", "_after_audit_rollback", "audit", 50),
    ]
    assert harvested.lifecycle_definition["transaction_methods"] == (
        harvested.transaction_method_facts
    )


def test_harvester_rejects_transaction_marker_unknown_group() -> None:
    class Counter:
        count: int = managed(default=1)

        @after_commit("audit")
        def _after_audit(self) -> None:
            return None

    with pytest.raises(
        LifecycleDefinitionError,
        match=r"Counter\._after_audit: transaction marker references unknown group 'audit'",
    ):
        harvest_lifecycle_definition(Counter)


def test_harvester_rejects_duplicate_commit_order_key_provider() -> None:
    class Counter:
        count: int = managed(default=1)

        @commit_order_key(DEFAULT_TRANSACTION)
        def _first_key(self) -> tuple[int]:
            return (self.count,)

        @commit_order_key(DEFAULT_TRANSACTION)
        def _second_key(self) -> tuple[int]:
            return (self.count,)

    with pytest.raises(
        LifecycleDefinitionError,
        match="Counter._second_key: multiple commit order key providers",
    ):
        harvest_lifecycle_definition(Counter)


def test_transaction_marker_rejects_non_callable_target() -> None:
    with pytest.raises(
        LifecycleDefinitionError,
        match="transaction method marker target must be callable",
    ):
        after_commit(DEFAULT_TRANSACTION)(1)
