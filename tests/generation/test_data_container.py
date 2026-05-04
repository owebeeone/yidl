from __future__ import annotations

import pytest

from yidl.generation.data_def_sys import DataDefinitionSystem
from yidl.generation.data_def_sys import REQUIRED
from yidl.generation.data_def_sys import from_literal


def test_container_exposes_concrete_computed_and_matcher_views() -> None:
    dds = DataDefinitionSystem()
    name = dds.property("Name", str, default=REQUIRED, storage_name="name")
    init = dds.property("Init", bool, default=True, storage_name="init")
    kind = dds.property("Kind", str, default=REQUIRED, storage_name="kind")
    field_specs = dds.union("FieldSpecs")
    plain_field = field_specs.variant("PlainField", name, init)
    managed_field = field_specs.variant("ManagedField", name, init, kind)
    fields = dds.collection("Fields", field_specs, cardinality=dds.many, identity=name)
    init_fields = dds.computed_collection(
        "InitFields",
        source=fields,
        when=(init.eq(True),),
    )
    managed_init_fields = dds.computed_collection(
        "ManagedInitFields",
        source=init_fields,
        when=(kind.eq("managed"),),
    )
    class_input_spec = dds.record("ClassInput", name)
    class_input = dds.collection(
        "ClassInput",
        class_input_spec,
        cardinality=dds.single,
        identity=name,
    )
    matcher = dds.matcher("InitGetter")
    field = matcher.input("field", init_fields)
    count_resource = from_literal("count")
    matcher.rule(
        name="count",
        when=(field.prop(name).eq("count"),),
        resource=count_resource,
    )

    count = plain_field.record(name="count", init=True)
    label = plain_field.record(name="label", init=False)
    owner = managed_field.record(name="owner", init=True, kind="managed")
    builder = dds.container_builder()
    builder.add(fields, count)
    builder.add(fields, label)
    builder.add(fields, owner)
    builder.record(class_input, name="Example")

    container = builder.freeze()

    assert tuple(container.Fields.sequence()) == (count, label, owner)
    assert tuple(container.InitFields.sequence()) == (count, owner)
    assert tuple(container.ManagedInitFields.sequence()) == (owner,)
    assert container.Fields.by_identity("count") is count
    assert container.InitFields.by_identity("label") is None
    assert container.InitFields.contains("owner")
    assert not container.ManagedInitFields.contains("count")
    assert container.ClassInput.one().name == "Example"

    results = tuple(container.matchers.InitGetter.sequence())

    assert len(results) == 1
    assert results[0].resource is count_resource
    assert results[0].records == (count,)


def test_container_builder_enforces_cardinality_identity_and_record_shape() -> None:
    dds = DataDefinitionSystem()
    name = dds.property("Name", str, default=REQUIRED, storage_name="name")
    value = dds.property("Value", int, default=REQUIRED, storage_name="value")
    item_spec = dds.record("Item", name, value)
    other_spec = dds.record("Other", name)
    items = dds.collection("Items", item_spec, cardinality=dds.many, identity=name)
    single_item = dds.collection(
        "SingleItem",
        item_spec,
        cardinality=dds.single,
        identity=name,
    )
    builder = dds.container_builder()
    first = items.record(name="count", value=1)
    duplicate = items.record(name="count", value=2)

    builder.add(items, first)
    builder.add(items, first)

    with pytest.raises(ValueError, match="duplicate identity"):
        builder.add(items, duplicate)
    with pytest.raises(TypeError, match="expected Item record"):
        builder.add(items, other_spec.record(name="other"))

    builder.add(single_item, single_item.record(name="only", value=1))
    with pytest.raises(ValueError, match="single collection"):
        builder.add(single_item, single_item.record(name="second", value=2))

    container = builder.freeze()
    with pytest.raises(RuntimeError, match="frozen"):
        builder.add(items, items.record(name="label", value=3))

    assert tuple(container.Items.sequence()) == (first,)
