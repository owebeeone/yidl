from __future__ import annotations

from support.golden_case import run_case
from yidl.generation.data_def_sys import AddIfAbsent
from yidl.generation.data_def_sys import DataDefinitionSystem
from yidl.generation.data_def_sys import REQUIRED
from yidl.generation.data_def_sys import emit_container_runtime_source
from yidl.generation.data_def_sys import from_astichi_code
from yidl.generation.data_def_sys import match
from yidl.generation.data_def_sys import read


PLAIN_FIELD = "plain"
MANAGED_FIELD = "managed"
PLAIN_GETTER = from_astichi_code("{'getter': 'plain'}")
MANAGED_GETTER = from_astichi_code("{'getter': 'managed'}")


def define_base_schema(dds: DataDefinitionSystem) -> None:
    name = dds.ensure_property("Name", str, default=REQUIRED, storage_name="name")
    kind = dds.ensure_property("Kind", str, default=PLAIN_FIELD, storage_name="kind")
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
    field = dds.ensure_record("Field", name, kind, order)
    getter = dds.ensure_record("Getter", name, target_port, order, template)
    fields = dds.ensure_collection(
        "Fields",
        field,
        cardinality=dds.many,
        identity=name,
    )
    dds.ensure_collection(
        "Getters",
        getter,
        cardinality=dds.many,
        identity=name,
    )
    dds.ensure_computed_collection("GetterFields", source=fields)
    dds.ensure_port("Class.body", cardinality=dds.many)
    dds.ensure_port_index(target=target_port, order=order)


def define_plain_getters(dds: DataDefinitionSystem) -> None:
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
    field = dds.ensure_record(
        "Field",
        name,
        dds.ensure_property("Kind", str, default=PLAIN_FIELD, storage_name="kind"),
        order,
    )
    fields = dds.ensure_collection(
        "Fields",
        field,
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
    matcher = dds.ensure_matcher("PropertyGetterTemplate")
    matcher.ensure_input("field", getter_fields)
    matcher.default(PLAIN_GETTER)
    production = dds.production(
        "FieldProvidesPropertyGetter",
        source=matcher.results(),
        target=getters,
        values={
            name: match.record("field").prop(name),
            target_port: class_body.of("runtime"),
            order: match.record("field").prop(order),
            template: match.resource(),
        },
        policy=AddIfAbsent,
    )
    dds.ensure_production_group("PropertyGetters", production)


def define_managed_getters(dds: DataDefinitionSystem) -> None:
    name = dds.ensure_property("Name", str, default=REQUIRED, storage_name="name")
    kind = dds.ensure_property("Kind", str, default=PLAIN_FIELD, storage_name="kind")
    order = dds.ensure_property("Order", int, default=0, storage_name="order")
    field = dds.ensure_record("Field", name, kind, order)
    fields = dds.ensure_collection(
        "Fields",
        field,
        cardinality=dds.many,
        identity=name,
    )
    getter_fields = dds.ensure_computed_collection("GetterFields", source=fields)
    matcher = dds.ensure_matcher("PropertyGetterTemplate")
    field_input = matcher.ensure_input("field", getter_fields)
    matcher.rule(
        when=(field_input.prop(kind).eq(MANAGED_FIELD),),
        resource=MANAGED_GETTER,
        name="managed-getter",
    )


def _build_dds() -> DataDefinitionSystem:
    return DataDefinitionSystem().extend(
        define_base_schema,
        define_plain_getters,
        define_managed_getters,
    )


def render_case() -> str:
    return emit_container_runtime_source(_build_dds())


def validate_case(source: str) -> None:
    namespace = {}
    exec(source, namespace)

    builder = namespace["new_builder"]()
    field = namespace["Field"]
    fields = namespace["FieldsCollection"]
    class_body = namespace["ClassBodyPort"]

    builder.add(fields, field(name="count", kind=PLAIN_FIELD, order=0))
    builder.add(fields, field(name="owner", kind=MANAGED_FIELD, order=1))
    container = namespace["build_container"](builder)

    getters = container.children_at(class_body.of("runtime"))

    assert [getter.name for getter in getters] == ["count", "owner"]
    assert [getter.template for getter in getters] == [PLAIN_GETTER, MANAGED_GETTER]
    assert "class PropertyGetterTemplateMatcher" in source
    assert "def run_field_provides_property_getter(builder):" in source
    assert source.index("from itertools import product") < source.index("_NameProperty")
    assert source.index("from yidl.generation.data_def_sys import") < source.index(
        "_NameProperty"
    )
    assert source.index("from_astichi_code") < source.index("_NameProperty")
    assert source.count("from itertools import product") == 1
    assert source.count("from yidl.generation.data_def_sys import") == 1
    assert "DataDefinitionSystem()" not in source
    assert "dds.ensure_" not in source


if __name__ == "__main__":
    raise SystemExit(
        run_case("dds_definition_extensions.py", render_case, validate_case)
    )
