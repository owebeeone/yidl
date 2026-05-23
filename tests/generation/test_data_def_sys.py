from __future__ import annotations

from dataclasses import is_dataclass
import inspect

import pytest

from yidl.generation.data_def_sys import ComputedValue
from yidl.generation.data_def_sys import DataDefinitionSystem
from yidl.generation.data_def_sys import REQUIRED
from yidl.generation.data_schema import DataDefinitionSystem as SchemaDataDefinitionSystem


def test_record_spec_generates_plain_slotted_record_class() -> None:
    dds = DataDefinitionSystem()
    init = dds.property("Init", bool, default=True, storage_name="init")
    default = dds.property("Default", object, default=REQUIRED, storage_name="default")
    field_spec = dds.record("FieldSpec", init, default)
    field_record = field_spec.record_class()

    record = field_record(default=3)

    assert not is_dataclass(record)
    assert field_record.__name__ == "FieldSpec"
    assert field_record.__dds_record_spec__.name == "FieldSpec"
    assert field_record.__slots__ == ("init", "default")
    assert inspect.get_annotations(field_record, eval_str=True) == {
        "init": bool,
        "default": object,
    }
    assert record.init is True
    assert record.default == 3
    assert repr(record) == "FieldSpec(init=True, default=3)"
    assert field_spec.values_of(record) == {
        init: True,
        default: 3,
    }
    signature = inspect.signature(field_record)
    assert list(signature.parameters) == ["init", "default"]
    assert signature.parameters["init"].default is True
    assert signature.parameters["default"].default is inspect.Parameter.empty
    assert signature.parameters["init"].annotation is bool
    assert signature.parameters["default"].annotation is object

    with pytest.raises(AttributeError, match="immutable"):
        record.init = False


def test_data_schema_module_exposes_same_schema_facade() -> None:
    assert issubclass(DataDefinitionSystem, SchemaDataDefinitionSystem)


def test_record_spec_generates_empty_record_class() -> None:
    dds = DataDefinitionSystem()
    empty_spec = dds.record("Empty")
    empty_record = empty_spec.record_class()

    record = empty_record()

    assert empty_record.__name__ == "Empty"
    assert empty_record.__dds_record_spec__.name == "Empty"
    assert empty_record.__slots__ == ()
    assert repr(record) == "Empty()"


def test_record_class_validates_required_unknown_and_typed_values() -> None:
    dds = DataDefinitionSystem()
    init = dds.property("Init", bool, default=True, storage_name="init")
    name = dds.property("Name", str, default=REQUIRED, storage_name="name")
    field_spec = dds.record("FieldSpec", init, name)
    field_record = field_spec.record_class()

    with pytest.raises(TypeError, match="required keyword-only argument: 'name'"):
        field_record()

    with pytest.raises(TypeError, match="Init must be bool"):
        field_record(init="yes", name="count")

    with pytest.raises(TypeError, match="unexpected keyword argument 'extra'"):
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


def test_union_collection_accepts_variant_records_and_indexes_variant_facts() -> None:
    dds = DataDefinitionSystem()
    name = dds.property("Name", str, default=REQUIRED, storage_name="name")
    init = dds.property("Init", bool, default=True, storage_name="init")
    tx_key = dds.property("TxKey", str, default=REQUIRED, storage_name="tx_key")
    field_specs = dds.union("FieldSpecs")
    plain_field = field_specs.variant("PlainField", name, init)
    managed_field = field_specs.variant("ManagedField", name, tx_key)
    fields = dds.collection("Fields", field_specs, cardinality=dds.many, identity=name)

    plain = plain_field.record(name="count")
    managed = managed_field.record(name="owner", tx_key="main")

    assert field_specs in dds.unions
    assert field_specs.variants == (plain_field, managed_field)
    assert fields.identity_of(plain) == "count"
    assert fields.identity_of(managed) == "owner"
    assert set(fields.fact_keys(plain)) == {
        fields.lookup_key(name, "count"),
        fields.lookup_key(init, True),
    }
    assert set(fields.fact_keys(managed)) == {
        fields.lookup_key(name, "owner"),
        fields.lookup_key(tx_key, "main"),
    }

    with pytest.raises(TypeError, match="create a concrete variant record"):
        fields.record(name="label")


def test_union_collection_identity_must_exist_on_all_variants() -> None:
    dds = DataDefinitionSystem()
    name = dds.property("Name", str, default=REQUIRED, storage_name="name")
    tx_key = dds.property("TxKey", str, default=REQUIRED, storage_name="tx_key")
    field_specs = dds.union("FieldSpecs")
    field_specs.variant("PlainField", name)
    field_specs.variant("ManagedField", name, tx_key)

    with pytest.raises(ValueError, match="must exist on all variants"):
        dds.collection("Fields", field_specs, cardinality=dds.many, identity=tx_key)


def test_collection_accepts_composite_identity_properties() -> None:
    dds = DataDefinitionSystem()
    tx_key = dds.property("TxKey", str, default=REQUIRED, storage_name="tx_key")
    phase = dds.property("Phase", str, default=REQUIRED, storage_name="phase")
    tx_index = dds.property("TxIndex", int, default=REQUIRED, storage_name="tx_index")
    tx_key_record = dds.record("TxKeyRecord", tx_key, phase, tx_index)
    tx_keys = dds.collection(
        "TxKeys",
        tx_key_record,
        cardinality=dds.many,
        identity=(tx_key, phase),
    )

    record = tx_keys.record(tx_key="main", phase="commit", tx_index=0)

    assert tx_keys.identity_of(record) == ("main", "commit")
    assert tx_keys.identity == (tx_key, phase)


def test_union_collection_composite_identity_must_exist_on_all_variants() -> None:
    dds = DataDefinitionSystem()
    name = dds.property("Name", str, default=REQUIRED, storage_name="name")
    phase = dds.property("Phase", str, default=REQUIRED, storage_name="phase")
    field_specs = dds.union("FieldSpecs")
    field_specs.variant("PlainField", name)
    field_specs.variant("ManagedField", name, phase)

    with pytest.raises(ValueError, match="must exist on all variants"):
        dds.collection(
            "Fields",
            field_specs,
            cardinality=dds.many,
            identity=(name, phase),
        )


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


def test_transform_spec_can_read_from_union_source_variants() -> None:
    dds = DataDefinitionSystem()
    name = dds.property("Name", str, default=REQUIRED, storage_name="name")
    init = dds.property("Init", bool, default=True, storage_name="init")
    tx_key = dds.property("TxKey", str, default=REQUIRED, storage_name="tx_key")
    field_specs = dds.union("FieldSpecs")
    plain_field = field_specs.variant("PlainField", name, init)
    managed_field = field_specs.variant("ManagedField", name, tx_key)
    fields = dds.collection("Fields", field_specs, cardinality=dds.many, identity=name)
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

    derived = transform.derive(plain_field.record(name="count"))

    assert derived is not None
    assert derived.name == "count"
    assert transform.derive(managed_field.record(name="owner", tx_key="main")) is None


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
