from __future__ import annotations

import pytest

from yidl.capsule.recorded_builder import capsule_concept
from yidl.generation.data_def_sys import REQUIRED


def test_schema_family_lowers_to_union_variants() -> None:
    builder = capsule_concept("FieldFamily")
    name = builder.props.Name(str, REQUIRED)
    source_order = builder.props.SourceOrder(int, 0)
    kind = builder.props.Kind(object, REQUIRED)
    tx_group = builder.props.TxGroup(str, "default")
    default = builder.props.Default(object, REQUIRED)

    field_specs = builder.schema_family("FieldSpecs")
    field_specs.common(name, source_order, kind)
    plain = field_specs.variant("PlainField", default)
    managed = field_specs.variant("ManagedField", tx_group, default)
    builder.collections.Fields(field_specs.handle, cardinality=builder.many, identity=name)

    dds = builder.build().build_data_definition()

    assert [union.name for union in dds.unions] == ["FieldSpecs"]
    assert [record.name for record in dds.records] == ["PlainField", "ManagedField"]
    assert [prop.name for prop in plain.properties] == [
        "Name",
        "SourceOrder",
        "Kind",
        "Default",
    ]
    assert [prop.name for prop in managed.properties] == [
        "Name",
        "SourceOrder",
        "Kind",
        "TxGroup",
        "Default",
    ]
    assert dds.collections[0].record_shape is dds.unions[0]


def test_extending_concept_references_schema_family_symbols() -> None:
    base_builder = capsule_concept("BaseFamily")
    name = base_builder.props.Name(str, REQUIRED)
    kind = base_builder.props.Kind(object, REQUIRED)
    fields = base_builder.schema_family("FieldSpecs")
    fields.common(name, kind)
    fields.variant("PlainField")
    fields_collection = base_builder.collections.Fields(
        fields.handle,
        cardinality=base_builder.many,
        identity=name,
    )
    base = base_builder.build()

    child_builder = capsule_concept("ChildFamily", extends=(base,))
    base_refs = child_builder.use(base)
    initialized = child_builder.computed.InitFields(
        source=base_refs.collections.Fields,
        when=(base_refs.props.Kind.eq("init"),),
    )
    child_builder.collections.InitFieldsMirror(
        base_refs.families.FieldSpecs,
        cardinality=child_builder.many,
        identity=base_refs.props.Name,
    )
    child = child_builder.build()

    dds = child.build_data_definition()

    assert [collection.name for collection in dds.collections] == [
        fields_collection.name,
        "InitFieldsMirror",
    ]
    assert dds.computed_collections[0].name == initialized.name
    assert dds.collections[1].record_shape is dds.unions[0]


def test_schema_family_incompatible_redefinition_rejects() -> None:
    base_builder = capsule_concept("BaseFamily")
    base_builder.props.Name(str, REQUIRED)
    base = base_builder.build()

    child_builder = capsule_concept("ChildFamily", extends=(base,))
    child_builder.props.Name(int, REQUIRED)
    child = child_builder.build()

    with pytest.raises(ValueError, match="property 'Name' is already owned"):
        child.build_data_definition()


def test_schema_family_replay_is_idempotent() -> None:
    builder = capsule_concept("FieldFamily")
    name = builder.props.Name(str, REQUIRED)
    fields = builder.schema_family("FieldSpecs")
    fields.common(name)
    fields.variant("PlainField")
    plan = builder.build()

    dds = plan.build_data_definition()
    plan.apply(dds)

    assert [union.name for union in dds.unions] == ["FieldSpecs"]
    assert [record.name for record in dds.records] == ["PlainField"]
