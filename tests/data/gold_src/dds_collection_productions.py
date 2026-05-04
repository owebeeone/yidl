from __future__ import annotations

from support.golden_case import run_case
from yidl.generation.data_def_sys import AddIfAbsent
from yidl.generation.data_def_sys import DataDefinitionSystem
from yidl.generation.data_def_sys import REQUIRED
from yidl.generation.data_def_sys import call
from yidl.generation.data_def_sys import emit_container_runtime_source
from yidl.generation.data_def_sys import read


def field_order(field: object) -> int:
    return field.order * 10


def _build_dds() -> DataDefinitionSystem:
    dds = DataDefinitionSystem()
    name = dds.property("Name", str, default=REQUIRED, storage_name="name")
    init = dds.property("Init", bool, default=True, storage_name="init")
    order = dds.property("Order", int, default=0, storage_name="order")
    target_port = dds.property(
        "TargetPort",
        object,
        default=REQUIRED,
        storage_name="target_port",
    )
    field = dds.record("Field", name, init, order)
    component = dds.record("Component", name, target_port, order)
    fields = dds.collection("Fields", field, cardinality=dds.many, identity=name)
    init_fields = dds.computed_collection(
        "InitFields",
        source=fields,
        when=(init.eq(True),),
    )
    components = dds.collection(
        "Components",
        component,
        cardinality=dds.many,
        identity=name,
    )
    class_body = dds.port("Class.body", cardinality=dds.many)
    dds.port_index(target=target_port, order=order)
    production = dds.production(
        "InitFieldProvidesComponent",
        source=init_fields,
        target=components,
        values={
            name: read(name),
            target_port: class_body.of("runtime"),
            order: call("field-order", field_order),
        },
        policy=AddIfAbsent,
    )
    dds.production_group("FieldChildren", production)
    return dds


def render_case() -> str:
    return emit_container_runtime_source(
        _build_dds(),
        evaluator_names=((field_order, "field_order"),),
    )


def validate_case(source: str) -> None:
    namespace = {"field_order": field_order}
    exec(source, namespace)

    builder = namespace["new_builder"]()
    field = namespace["Field"]
    fields = namespace["FieldsCollection"]
    class_body = namespace["ClassBodyPort"]

    builder.add(fields, field(name="label", init=True, order=2))
    builder.add(fields, field(name="count", init=True, order=1))
    builder.add(fields, field(name="skip", init=False, order=0))
    container = namespace["build_container"](builder)

    runtime_body = class_body.of("runtime")

    assert [record.name for record in container.children_at(runtime_body)] == [
        "count",
        "label",
    ]
    assert [record.order for record in container.children_at(runtime_body)] == [10, 20]
    assert "def run_init_field_provides_component(builder):" in source
    assert "def run_operations(builder):" in source
    assert "def build_container(builder):" in source
    assert "builder.write(ComponentsCollection" in source
    assert "field_order(source)" in source
    assert "dds.production(" not in source


if __name__ == "__main__":
    raise SystemExit(
        run_case("dds_collection_productions.py", render_case, validate_case)
    )
