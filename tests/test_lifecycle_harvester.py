from __future__ import annotations

import pytest

from yidl.runtime.lifecycle import LifecycleDefinitionError
from yidl.runtime.lifecycle import MISSING
from yidl.runtime.lifecycle import classvar
from yidl.runtime.lifecycle import field
from yidl.runtime.lifecycle import harvest_lifecycle_definition
from yidl.runtime.lifecycle import initvar
from yidl.runtime.lifecycle import managed
from yidl.runtime.transaction_yidl import DEFAULT_TRANSACTION


def test_harvests_phase_a_compatible_facts() -> None:
    class Counter:
        plain: int = field(default=3)
        optional: str | None = field(default=None)
        tags: list[str] = field(default_factory=list)
        seed: int = initvar(default=2)
        KIND: str = classvar(default="counter")
        count: int = managed(default=1)
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
        "tx_groups_param_name": "_Counter_tx_groups",
    }
    assert [
        (
            fact["field_name"],
            fact["field_kind"],
            fact["field_order"],
            fact["default_value_param_name"],
            fact["tx_group_key"],
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
    assert harvested.tx_groups == (DEFAULT_TRANSACTION, "audit")
    assert harvested.lifecycle_definition["version"] == 1
    assert harvested.lifecycle_definition["fields"] == harvested.field_facts
    assert harvested.build_kwargs["_Counter_lifecycle_definition"] is (
        harvested.lifecycle_definition
    )
    assert harvested.build_kwargs["_Counter_annotations"] == Counter.__annotations__
    assert harvested.build_kwargs["_Counter_tx_groups"] == (
        DEFAULT_TRANSACTION,
        "audit",
    )
    assert harvested.build_kwargs["_Counter_optional_default"] is None
    assert harvested.build_kwargs["_Counter_tags_default_factory"] is list


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


def test_harvester_ignores_init_false_initvar() -> None:
    class Counter:
        seed: int = initvar(init=False, default=2)
        plain: int = field(default=3)

    harvested = harvest_lifecycle_definition(Counter)

    assert [fact["field_name"] for fact in harvested.field_facts] == ["plain"]
    assert "_Counter_seed_default" not in harvested.build_kwargs


def test_harvester_rejects_reserved_class_body_names() -> None:
    class Counter:
        _y_state: int = 1

    with pytest.raises(LifecycleDefinitionError, match="Counter._y_state"):
        harvest_lifecycle_definition(Counter)


def test_harvester_preserves_first_transaction_group_order() -> None:
    class Counter:
        audit: int = managed("audit", default=1)
        plain: int = field(default=2)
        other: int = managed("other", default=3)
        audit_again: int = managed("audit", default=4)

    harvested = harvest_lifecycle_definition(Counter)

    assert harvested.tx_groups == (DEFAULT_TRANSACTION, "audit", "other")

