from __future__ import annotations

import pytest

from yidl.generation.data_def_sys import DataDefinitionSystem
from yidl.generation.data_def_sys import REQUIRED
from yidl.generation.data_def_sys import from_literal


def test_ensure_property_reuses_identical_definition() -> None:
    dds = DataDefinitionSystem()
    first = dds.ensure_property("Name", str, default=REQUIRED, storage_name="name")
    second = dds.ensure_property("Name", str, default=REQUIRED, storage_name="name")

    assert second is first


def test_ensure_property_rejects_incompatible_definition() -> None:
    dds = DataDefinitionSystem()
    dds.ensure_property("Name", str, default=REQUIRED, storage_name="name")

    with pytest.raises(ValueError, match="defined differently"):
        dds.ensure_property("Name", int, default=REQUIRED, storage_name="name")


def test_ensure_record_collection_and_port_reuse_identical_definitions() -> None:
    dds = DataDefinitionSystem()
    name = dds.ensure_property("Name", str, default=REQUIRED, storage_name="name")
    record = dds.ensure_record("Field", name)
    collection = dds.ensure_collection(
        "Fields",
        record,
        cardinality=dds.many,
        identity=name,
    )
    port = dds.ensure_port("Class.body", cardinality=dds.many)

    assert dds.ensure_record("Field", name) is record
    assert (
        dds.ensure_collection(
            "Fields",
            record,
            cardinality=dds.many,
            identity=name,
        )
        is collection
    )
    assert dds.ensure_port("Class.body", cardinality=dds.many) is port


def test_ensure_record_and_collection_reject_incompatible_definitions() -> None:
    dds = DataDefinitionSystem()
    name = dds.ensure_property("Name", str, default=REQUIRED, storage_name="name")
    value = dds.ensure_property("Value", int, default=0, storage_name="value")
    field = dds.ensure_record("Field", name)
    dds.ensure_collection("Fields", field, cardinality=dds.many, identity=name)

    with pytest.raises(ValueError, match="record 'Field'.*defined differently"):
        dds.ensure_record("Field", name, value)
    with pytest.raises(ValueError, match="collection 'Fields'.*defined differently"):
        dds.ensure_collection("Fields", field, cardinality=dds.single, identity=name)


def test_ensure_matcher_allows_rules_from_multiple_contributors() -> None:
    dds = DataDefinitionSystem()
    name = dds.ensure_property("Name", str, default=REQUIRED, storage_name="name")
    field = dds.ensure_record("Field", name)
    fields = dds.ensure_collection(
        "Fields",
        field,
        cardinality=dds.many,
        identity=name,
    )

    matcher = dds.ensure_matcher("Getter")
    field_input = matcher.ensure_input("field", fields)
    matcher.default(from_literal("default"))

    same_matcher = dds.ensure_matcher("Getter")
    same_field_input = same_matcher.ensure_input("field", fields)
    same_matcher.rule(
        when=(same_field_input.prop(name).eq("count"),),
        resource=from_literal("count"),
        name="count",
    )

    assert same_matcher is matcher
    assert same_field_input is field_input
    assert [rule.name for rule in matcher.rules] == ["count"]


def test_extend_runs_definition_contributors_in_order() -> None:
    dds = DataDefinitionSystem()
    calls: list[str] = []

    def base(system: DataDefinitionSystem) -> None:
        calls.append("base")
        system.ensure_property("Name", str, default=REQUIRED, storage_name="name")

    def child(system: DataDefinitionSystem) -> None:
        calls.append("child")
        name = system.ensure_property(
            "Name",
            str,
            default=REQUIRED,
            storage_name="name",
        )
        system.ensure_record("Field", name)

    returned = dds.extend(base, child)

    assert returned is dds
    assert calls == ["base", "child"]
    assert [record.name for record in dds.records] == ["Field"]
