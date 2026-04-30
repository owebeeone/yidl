from __future__ import annotations

from dataclasses import is_dataclass

import pytest

from yidl.generation.data_def_sys import ComputedValue
from yidl.generation.data_def_sys import DataDefinitionSystem
from yidl.generation.data_def_sys import REQUIRED


def test_record_spec_generates_plain_slotted_record_class() -> None:
    dds = DataDefinitionSystem()
    init = dds.property("Init", bool, default=True, storage_name="init")
    default = dds.property("Default", object, default=REQUIRED, storage_name="default")
    field_spec = dds.record("FieldSpec", init, default)
    field_record = field_spec.record_class()

    record = field_record(default=3)

    assert not is_dataclass(record)
    assert field_record.__dds_record_spec__ is field_spec
    assert field_record.__slots__ == ("init", "default", "_dds_frozen")
    assert record.init is True
    assert record.default == 3
    assert field_spec.values_of(record) == {
        init: True,
        default: 3,
    }

    with pytest.raises(AttributeError, match="immutable"):
        record.init = False


def test_record_class_validates_required_unknown_and_typed_values() -> None:
    dds = DataDefinitionSystem()
    init = dds.property("Init", bool, default=True, storage_name="init")
    name = dds.property("Name", str, default=REQUIRED, storage_name="name")
    field_spec = dds.record("FieldSpec", init, name)
    field_record = field_spec.record_class()

    with pytest.raises(TypeError, match="missing required value"):
        field_record()

    with pytest.raises(TypeError, match="Init must be bool"):
        field_record(init="yes", name="count")

    with pytest.raises(TypeError, match="unexpected values"):
        field_record(name="count", extra=True)


def test_collection_spec_turns_equality_condition_into_lookup_key() -> None:
    dds = DataDefinitionSystem()
    name = dds.property("Name", str, default=REQUIRED, storage_name="name")
    init = dds.property("Init", bool, default=True, storage_name="init")
    field_spec = dds.record("FieldSpec", name, init)
    fields = dds.collection("Fields", field_spec, cardinality=dds.many, identity=name)

    record = fields.record(name="label", init=False)
    condition = init.eq(False)

    assert condition.matches(record)
    assert condition.lookup_key(fields) == fields.lookup_key(init, False)
    assert fields.identity_of(record) == "label"
    assert set(fields.fact_keys(record)) == {
        fields.lookup_key(name, "label"),
        fields.lookup_key(init, False),
    }


def test_transform_spec_derives_collection_records_without_holding_data() -> None:
    dds = DataDefinitionSystem()
    name = dds.property("Name", str, default=REQUIRED, storage_name="name")
    init = dds.property("Init", bool, default=True, storage_name="init")
    field_spec = dds.record("FieldSpec", name, init)
    fields = dds.collection("Fields", field_spec, cardinality=dds.many, identity=name)

    init_field_spec = dds.record("InitField", name)
    init_fields = dds.collection(
        "InitFields",
        init_field_spec,
        cardinality=dds.many,
        identity=name,
    )
    transform = dds.transform(
        "FieldsToInitFields",
        source=fields,
        target=init_fields,
        when=(init.eq(True),),
        values={name: name.read()},
    )

    count = fields.record(name="count", init=True)
    label = fields.record(name="label", init=False)

    derived = transform.derive(count)

    assert transform in dds.transforms
    assert derived is not None
    assert derived.name == "count"
    assert transform.derive(label) is None


def test_transform_spec_can_compute_new_properties() -> None:
    dds = DataDefinitionSystem()
    name = dds.property("Name", str, default=REQUIRED, storage_name="name")
    managed = dds.property("Managed", bool, default=False, storage_name="managed")
    working_name = dds.property(
        "WorkingName",
        str,
        default=REQUIRED,
        storage_name="working_name",
    )
    field_spec = dds.record("FieldSpec", name, managed)
    fields = dds.collection("Fields", field_spec, cardinality=dds.many, identity=name)
    managed_names_spec = dds.record("ManagedNames", name, working_name)
    managed_names = dds.collection(
        "ManagedNames",
        managed_names_spec,
        cardinality=dds.many,
        identity=name,
    )
    transform = dds.transform(
        "ManagedFieldNames",
        source=fields,
        target=managed_names,
        when=(managed.eq(True),),
        values={
            name: name.read(),
            working_name: ComputedValue(
                "working-name",
                lambda source: f"_{name.value_from(source)}_working",
            ),
        },
    )

    derived = transform.derive(fields.record(name="owner", managed=True))

    assert derived is not None
    assert managed_names.identity_of(derived) == "owner"
    assert derived.working_name == "_owner_working"
