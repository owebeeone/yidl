from __future__ import annotations

from support.golden_case import run_case
from yidl.generation.data_def_sys import DataDefinitionSystem
from yidl.generation.data_def_sys import REQUIRED
from yidl.generation.data_def_sys import emit_container_runtime_source


def _build_dds() -> DataDefinitionSystem:
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
    dds.collection("Components", component, cardinality=dds.many, identity=name)
    dds.port("Class.body", cardinality=dds.many)
    dds.port("Class.name", cardinality=dds.single)
    dds.port_index(target=target_port, order=order)
    return dds


def render_case() -> str:
    return emit_container_runtime_source(_build_dds())


def validate_case(source: str) -> None:
    namespace = {}
    exec(source, namespace)

    builder = namespace["new_builder"]()
    component = namespace["Component"]
    components = namespace["ComponentsCollection"]
    class_body = namespace["ClassBodyPort"]
    class_name = namespace["ClassNamePort"]

    runtime_body = class_body.of("runtime")
    builder.add(components, component(name="late", target_port=runtime_body, order=20))
    builder.add(components, component(name="early", target_port=runtime_body, order=10))
    builder.add(components, component(name="tie", target_port=runtime_body, order=10))

    assert [record.name for record in builder.children_at(runtime_body)] == [
        "early",
        "tie",
        "late",
    ]

    container = builder.freeze()
    assert [record.name for record in container.children_at(runtime_body)] == [
        "early",
        "tie",
        "late",
    ]
    assert "RuntimePort(" in source
    assert "RuntimePortIndex(" in source
    assert "def children_at(self, port_address):" in source

    builder = namespace["new_builder"]()
    builder.add(
        components,
        component(name="class-name", target_port=class_name.of("runtime"), order=0),
    )
    try:
        builder.add(
            components,
            component(name="duplicate-name", target_port=class_name.of("runtime"), order=1),
        )
    except ValueError as error:
        assert "single port" in str(error)
    else:
        raise AssertionError("expected single-port conflict")


if __name__ == "__main__":
    raise SystemExit(run_case("dds_port_children.py", render_case, validate_case))
