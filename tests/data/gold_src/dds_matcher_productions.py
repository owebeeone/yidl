from __future__ import annotations

from support.golden_case import run_case
from yidl.generation.data_def_sys import AddIfAbsent
from yidl.generation.data_def_sys import DataDefinitionSystem
from yidl.generation.data_def_sys import REQUIRED
from yidl.generation.data_def_sys import emit_container_runtime_source
from yidl.generation.data_def_sys import from_astichi_code
from yidl.generation.data_def_sys import match
from yidl.generation.data_def_sys import read


REQUIRED_TEMPLATE = from_astichi_code("{'param': 'required'}")
DEFAULTED_TEMPLATE = from_astichi_code("{'param': 'defaulted'}")


def _build_dds() -> DataDefinitionSystem:
    dds = DataDefinitionSystem()
    name = dds.property("Name", str, default=REQUIRED, storage_name="name")
    init = dds.property("Init", bool, default=True, storage_name="init")
    defaulted = dds.property(
        "Defaulted",
        bool,
        default=False,
        storage_name="defaulted",
    )
    order = dds.property("Order", int, default=0, storage_name="order")
    target_port = dds.property(
        "TargetPort",
        object,
        default=REQUIRED,
        storage_name="target_port",
    )
    template = dds.property(
        "Template",
        object,
        default=REQUIRED,
        storage_name="template",
    )
    field = dds.record("Field", name, init, defaulted, order)
    param = dds.record("ParamComponent", name, target_port, order, template, defaulted)
    fields = dds.collection("Fields", field, cardinality=dds.many, identity=name)
    init_fields = dds.computed_collection(
        "InitFields",
        source=fields,
        when=(init.eq(True),),
    )
    params = dds.collection("Params", param, cardinality=dds.many, identity=name)
    init_params = dds.port("Init.params", cardinality=dds.many)
    dds.port_index(target=target_port, order=order)

    matcher = dds.matcher("InitParamTemplate")
    field_input = matcher.input("field", init_fields)
    matcher.default(REQUIRED_TEMPLATE)
    matcher.rule(
        when=(field_input.prop(defaulted).eq(True),),
        resource=DEFAULTED_TEMPLATE,
        name="defaulted-param",
    )

    production = dds.production(
        "InitParamTemplateProvidesParam",
        source=matcher.results(),
        target=params,
        values={
            name: match.record("field").prop(name),
            target_port: init_params.of(("Example", "__init__")),
            order: match.record("field").prop(order),
            template: match.resource(),
            defaulted: match.value(0),
        },
        policy=AddIfAbsent,
    )
    dds.production_group("FieldChildren", production)
    return dds


def render_case() -> str:
    return emit_container_runtime_source(_build_dds())


def validate_case(source: str) -> None:
    namespace: dict[str, object] = {}
    exec(source, namespace)

    builder = namespace["new_builder"]()
    field = namespace["Field"]
    fields = namespace["FieldsCollection"]
    init_params = namespace["InitParamsPort"]

    builder.add(fields, field(name="count", init=True, defaulted=False, order=1))
    builder.add(fields, field(name="label", init=True, defaulted=True, order=2))
    builder.add(fields, field(name="skip", init=False, defaulted=True, order=0))
    container = namespace["build_container"](builder)

    runtime_params = init_params.of(("Example", "__init__"))
    children = container.children_at(runtime_params)

    assert [record.name for record in children] == ["count", "label"]
    assert [record.template for record in children] == [
        REQUIRED_TEMPLATE,
        DEFAULTED_TEMPLATE,
    ]
    assert [record.defaulted for record in children] == [False, True]
    assert "snapshot = builder._snapshot()" in source
    assert "snapshot.matchers.InitParamTemplate.sequence()" in source
    assert "source.resource" in source
    assert "source.records[0].name" in source
    assert "source.values[0]" in source
    assert source.index("from itertools import product") < source.index("_NameProperty")
    assert source.index("from yidl.generation.data_def_sys import") < source.index(
        "_NameProperty"
    )
    assert source.index("from_astichi_code") < source.index("_NameProperty")
    assert source.count("from itertools import product") == 1
    assert source.count("from yidl.generation.data_def_sys import") == 1
    assert "dds.matcher_production" not in source
    assert "dds.production(" not in source


if __name__ == "__main__":
    raise SystemExit(
        run_case("dds_matcher_productions.py", render_case, validate_case)
    )
