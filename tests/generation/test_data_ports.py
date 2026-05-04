from __future__ import annotations

import pytest

from yidl.generation.data_def_sys import DataDefinitionSystem
from yidl.generation.data_def_sys import REQUIRED


def _port_shape() -> tuple[DataDefinitionSystem, object, object, object, object]:
    dds = DataDefinitionSystem()
    name = dds.property("Name", str, default=REQUIRED, storage_name="name")
    target_port = dds.property(
        "TargetPort",
        object,
        default=REQUIRED,
        storage_name="target_port",
    )
    order = dds.property("Order", int, default=0, storage_name="order")
    component = dds.record("Component", name, target_port, order)
    note = dds.record("Note", name)
    components = dds.collection(
        "Components",
        component,
        cardinality=dds.many,
        identity=name,
    )
    notes = dds.collection("Notes", note, cardinality=dds.many, identity=name)
    class_body = dds.port("Class.body", cardinality=dds.many)
    class_name = dds.port("Class.name", cardinality=dds.single)
    dds.port_index(target=target_port, order=order)
    return dds, components, notes, class_body, class_name


def test_children_at_returns_ordered_records_for_one_port_owner() -> None:
    dds, components, notes, class_body, _ = _port_shape()
    builder = dds.container_builder()
    runtime_body = class_body.of("runtime")
    other_body = class_body.of("other")
    late = components.record(name="late", target_port=runtime_body, order=20)
    early = components.record(name="early", target_port=runtime_body, order=10)
    tie = components.record(name="tie", target_port=runtime_body, order=10)
    other = components.record(name="other", target_port=other_body, order=0)
    note = notes.record(name="ignored")

    builder.add(components, late)
    builder.add(notes, note)
    builder.add(components, early)
    builder.add(components, tie)
    builder.add(components, other)

    assert builder.children_at(runtime_body) == (early, tie, late)
    container = builder.freeze()
    assert container.children_at(runtime_body) == (early, tie, late)


def test_single_port_rejects_second_child_at_same_owner() -> None:
    dds, components, _, _, class_name = _port_shape()
    builder = dds.container_builder()
    runtime_name = class_name.of("runtime")

    builder.add(
        components,
        components.record(name="name-1", target_port=runtime_name, order=0),
    )

    with pytest.raises(ValueError, match="single port"):
        builder.add(
            components,
            components.record(name="name-2", target_port=runtime_name, order=1),
        )


def test_port_index_validates_target_values_at_write_time() -> None:
    dds, components, _, _, _ = _port_shape()
    builder = dds.container_builder()

    with pytest.raises(TypeError, match="PortAddress"):
        builder.add(
            components,
            components.record(name="bad", target_port="Class.body", order=0),
        )


def test_port_index_rejects_invalid_definition_shapes() -> None:
    dds = DataDefinitionSystem()
    target = dds.property("TargetPort", str, default=REQUIRED, storage_name="target")
    order = dds.property("Order", int, default=0, storage_name="order")

    with pytest.raises(TypeError, match="value_type=object"):
        dds.port_index(target=target, order=order)

    with pytest.raises(ValueError, match="port name"):
        dds.port("", cardinality=dds.many)

