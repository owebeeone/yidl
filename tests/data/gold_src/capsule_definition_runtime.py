from __future__ import annotations

from support.golden_case import run_case
from yidl.capsule.definition import capsule
from yidl.capsule.definition import concept
from yidl.generation.data_def_sys import AddIfAbsent
from yidl.generation.data_def_sys import DataDefinitionSystem
from yidl.generation.data_def_sys import REQUIRED
from yidl.generation.data_def_sys import call
from yidl.generation.data_def_sys import from_astichi_code
from yidl.generation.data_def_sys import match
from yidl.generation.data_def_sys import read


PLAIN_FIELD = "plain"
MANAGED_FIELD = "managed"
PLAIN_GETTER = from_astichi_code("{'getter': 'plain'}")
MANAGED_GETTER = from_astichi_code("{'getter': 'managed'}")


def getter_order_for(result: object) -> int:
    return 100 + result.records[0].order


def define_class_concepts(dds: DataDefinitionSystem) -> None:
    name = dds.ensure_property("Name", str, default=REQUIRED, storage_name="name")
    init = dds.ensure_property("Init", bool, default=True, storage_name="init")
    kind = dds.ensure_property("Kind", str, default=PLAIN_FIELD, storage_name="kind")
    order = dds.ensure_property("Order", int, default=0, storage_name="order")
    target_port = dds.ensure_property(
        "TargetPort",
        object,
        default=REQUIRED,
        storage_name="target_port",
    )
    template = dds.ensure_property(
        "Template",
        object,
        default=REQUIRED,
        storage_name="template",
    )
    field = dds.ensure_record("FieldInput", name, init, kind, order)
    init_component = dds.ensure_record(
        "InitComponent",
        name,
        target_port,
        order,
        template,
    )
    getter = dds.ensure_record("Getter", name, target_port, order, template)
    fields = dds.ensure_collection(
        "Fields",
        field,
        cardinality=dds.many,
        identity=name,
    )
    dds.ensure_collection(
        "InitComponents",
        init_component,
        cardinality=dds.many,
        identity=name,
    )
    dds.ensure_collection("Getters", getter, cardinality=dds.many, identity=name)
    dds.ensure_computed_collection("InitFields", source=fields, when=(init.eq(True),))
    dds.ensure_computed_collection("GetterFields", source=fields)
    dds.ensure_port("Class.body", cardinality=dds.many)
    dds.ensure_port_index(target=target_port, order=order)


def define_init_components(dds: DataDefinitionSystem) -> None:
    name = dds.ensure_property("Name", str, default=REQUIRED, storage_name="name")
    target_port = dds.ensure_property(
        "TargetPort",
        object,
        default=REQUIRED,
        storage_name="target_port",
    )
    order = dds.ensure_property("Order", int, default=0, storage_name="order")
    template = dds.ensure_property(
        "Template",
        object,
        default=REQUIRED,
        storage_name="template",
    )
    init_fields = dds.ensure_computed_collection(
        "InitFields",
        source=dds.ensure_collection(
            "Fields",
            dds.ensure_record(
                "FieldInput",
                name,
                dds.ensure_property("Init", bool, default=True, storage_name="init"),
                dds.ensure_property(
                    "Kind",
                    str,
                    default=PLAIN_FIELD,
                    storage_name="kind",
                ),
                order,
            ),
            cardinality=dds.many,
            identity=name,
        ),
        when=(
            dds.ensure_property("Init", bool, default=True, storage_name="init").eq(
                True
            ),
        ),
    )
    init_components = dds.ensure_collection(
        "InitComponents",
        dds.ensure_record("InitComponent", name, target_port, order, template),
        cardinality=dds.many,
        identity=name,
    )
    class_body = dds.ensure_port("Class.body", cardinality=dds.many)
    production = dds.production(
        "InitFieldProvidesComponent",
        source=init_fields,
        target=init_components,
        values={
            name: read(name),
            target_port: class_body.of("runtime"),
            order: read(order),
            template: "init-field-component",
        },
        policy=AddIfAbsent,
    )
    dds.ensure_production_group("InitComponents", production)


def define_getters(dds: DataDefinitionSystem) -> None:
    name = dds.ensure_property("Name", str, default=REQUIRED, storage_name="name")
    kind = dds.ensure_property("Kind", str, default=PLAIN_FIELD, storage_name="kind")
    order = dds.ensure_property("Order", int, default=0, storage_name="order")
    target_port = dds.ensure_property(
        "TargetPort",
        object,
        default=REQUIRED,
        storage_name="target_port",
    )
    template = dds.ensure_property(
        "Template",
        object,
        default=REQUIRED,
        storage_name="template",
    )
    fields = dds.ensure_collection(
        "Fields",
        dds.ensure_record(
            "FieldInput",
            name,
            dds.ensure_property("Init", bool, default=True, storage_name="init"),
            kind,
            order,
        ),
        cardinality=dds.many,
        identity=name,
    )
    getter_fields = dds.ensure_computed_collection("GetterFields", source=fields)
    getters = dds.ensure_collection(
        "Getters",
        dds.ensure_record("Getter", name, target_port, order, template),
        cardinality=dds.many,
        identity=name,
    )
    class_body = dds.ensure_port("Class.body", cardinality=dds.many)
    matcher = dds.ensure_matcher("GetterTemplate")
    field_input = matcher.ensure_input("field", getter_fields)
    matcher.default(PLAIN_GETTER)
    matcher.rule(
        when=(field_input.prop(kind).eq(MANAGED_FIELD),),
        resource=MANAGED_GETTER,
        name="managed-getter",
    )
    production = dds.production(
        "FieldProvidesGetter",
        source=matcher.results(),
        target=getters,
        values={
            name: match.record("field").prop(name),
            target_port: class_body.of("runtime"),
            order: call("getter-order", getter_order_for),
            template: match.resource(),
        },
        policy=AddIfAbsent,
    )
    dds.ensure_production_group("Getters", production)


def _definition():
    return capsule(
        "ClassConcepts",
        concept("class-concepts", define_class_concepts),
        concept("init-components", define_init_components),
        concept("getters", define_getters),
    )


def render_case() -> str:
    return _definition().emit_runtime_source(
        evaluator_names=((getter_order_for, "getter_order_for"),),
    )


def validate_case(source: str) -> None:
    runtime = _definition().load_runtime(
        evaluator_names=((getter_order_for, "getter_order_for"),),
        runtime_globals={"getter_order_for": getter_order_for},
    )
    namespace = runtime.namespace
    builder = runtime.new_builder()
    field = namespace["FieldInput"]
    fields = namespace["FieldsCollection"]
    class_body = namespace["ClassBodyPort"]

    builder.add(fields, field(name="count", init=True, kind=PLAIN_FIELD, order=0))
    builder.add(fields, field(name="owner", init=True, kind=MANAGED_FIELD, order=1))
    builder.add(fields, field(name="cache", init=False, kind=PLAIN_FIELD, order=2))
    container = runtime.build_container(builder)

    body_records = container.children_at(class_body.of("runtime"))

    assert [type(record).__name__ for record in body_records] == [
        "InitComponent",
        "InitComponent",
        "Getter",
        "Getter",
        "Getter",
    ]
    assert [record.name for record in body_records] == [
        "count",
        "owner",
        "count",
        "owner",
        "cache",
    ]
    assert [record.order for record in body_records] == [0, 1, 100, 101, 102]
    assert [record.name for record in container.InitFields.sequence()] == [
        "count",
        "owner",
    ]
    assert [
        result.resource
        for result in container.matchers.GetterTemplate.sequence()
    ] == [
        PLAIN_GETTER,
        MANAGED_GETTER,
        PLAIN_GETTER,
    ]
    assert "class GetterTemplateMatcher" in source
    assert "def run_field_provides_getter(builder):" in source
    assert source.index("from itertools import product") < source.index("_NameProperty")
    assert "DataDefinitionSystem()" not in source


if __name__ == "__main__":
    raise SystemExit(
        run_case("capsule_definition_runtime.py", render_case, validate_case)
    )
