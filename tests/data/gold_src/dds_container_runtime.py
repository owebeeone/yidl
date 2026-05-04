from __future__ import annotations

from support.golden_case import run_case
from yidl.generation.data_def_sys import DataDefinitionSystem
from yidl.generation.data_def_sys import REQUIRED
from yidl.generation.data_def_sys import emit_container_runtime_source
from yidl.generation.data_def_sys import from_literal


CountResource = from_literal({"resource": "count"})


def _build_dds() -> DataDefinitionSystem:
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
    dds.computed_collection(
        "ManagedInitFields",
        source=init_fields,
        when=(kind.eq("managed"),),
    )
    class_input_spec = dds.record("ClassInput", name)
    dds.collection(
        "ClassInput",
        class_input_spec,
        cardinality=dds.single,
        identity=name,
    )
    matcher = dds.matcher("InitGetter")
    field = matcher.input("field", init_fields)
    matcher.rule(
        name="count",
        when=(field.prop(name).eq("count"),),
        resource=CountResource,
    )
    return dds


def render_case() -> str:
    return emit_container_runtime_source(_build_dds())


def validate_case(source: str) -> None:
    namespace = {}
    exec(source, namespace)

    builder = namespace["new_builder"]()
    plain_field = namespace["PlainField"]
    managed_field = namespace["ManagedField"]
    class_input = namespace["ClassInput"]
    fields = namespace["FieldsCollection"]
    class_inputs = namespace["ClassInputCollection"]

    count = plain_field(name="count", init=True)
    label = plain_field(name="label", init=False)
    owner = managed_field(name="owner", init=True, kind="managed")
    builder.add(fields, count)
    builder.add(fields, label)
    builder.add(fields, owner)
    builder.add(class_inputs, class_input(name="Example"))

    container = builder.freeze()
    results = tuple(container.matchers.InitGetter.sequence())

    assert tuple(container.InitFields.sequence()) == (count, owner)
    assert tuple(container.ManagedInitFields.sequence()) == (owner,)
    assert container.Fields.by_identity("count") is count
    assert container.ClassInput.one().name == "Example"
    assert len(results) == 1
    assert results[0].resource == CountResource
    assert results[0].records == (count,)
    assert "class InitGetterMatcher" in source
    assert "class _GeneratedMatcherNamespace" in source
    assert "dds =" not in source
    assert "DataDefinitionSystem()" not in source
    assert "dds.property(" not in source
    assert "dds.record(" not in source
    assert "dds.union(" not in source
    assert "dds.collection(" not in source
    assert "dds.computed_collection(" not in source
    assert "RuntimeProperty(" in source
    assert "RuntimeContainerSpec(" in source
    assert "astichi_hole" not in source


if __name__ == "__main__":
    raise SystemExit(run_case("dds_container_runtime.py", render_case, validate_case))
