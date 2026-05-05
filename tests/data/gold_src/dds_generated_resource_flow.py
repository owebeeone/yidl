from __future__ import annotations

from support.golden_case import run_case
from yidl.generation.data_def_sys import AddIfAbsent
from yidl.generation.data_def_sys import DataDefinitionSystem
from yidl.generation.data_def_sys import REQUIRED
from yidl.generation.data_def_sys import emit_container_runtime_source
from yidl.generation.data_def_sys import from_astichi_code
from yidl.generation.data_def_sys import from_import
from yidl.generation.data_def_sys import match


PLAIN_TEMPLATE = from_astichi_code(
    """
    astichi_comment("plain property template")
    {"template": "plain"}
    """
)
IMPORTED_TEMPLATE = from_import("math", "sqrt")


def _build_dds() -> DataDefinitionSystem:
    dds = DataDefinitionSystem()
    name = dds.property("Name", str, default=REQUIRED, storage_name="name")
    kind = dds.property("Kind", str, default="plain", storage_name="kind")
    template = dds.property(
        "Template",
        object,
        default=REQUIRED,
        storage_name="template",
    )

    field = dds.record("Field", name, kind)
    template_component = dds.record("TemplateComponent", name, template)
    fields = dds.collection("Fields", field, cardinality=dds.many, identity=name)
    template_components = dds.collection(
        "TemplateComponents",
        template_component,
        cardinality=dds.many,
        identity=name,
    )

    matcher = dds.matcher("PropertyTemplate")
    field_input = matcher.input("field", fields)
    matcher.default(PLAIN_TEMPLATE)
    matcher.rule(
        name="imported-template",
        when=(field_input.prop(kind).eq("imported"),),
        resource=IMPORTED_TEMPLATE,
    )

    production = dds.production(
        "PropertyTemplateProvidesComponent",
        source=matcher.results(),
        target=template_components,
        values={
            name: match.record("field").prop(name),
            template: match.resource(),
        },
        policy=AddIfAbsent,
    )
    dds.production_group("PropertyTemplates", production)
    return dds


def render_case() -> str:
    return emit_container_runtime_source(_build_dds())


def _render_selected_templates(container: object) -> tuple[str, ...]:
    rendered: list[str] = []
    for record in container.TemplateComponents.sequence():
        rendered.append(
            record.template.to_generator().materialize().emit(provenance=False).strip()
        )
    return tuple(rendered)


def validate_case(source: str) -> None:
    namespace: dict[str, object] = {}
    exec(source, namespace)

    builder = namespace["new_builder"]()
    field = namespace["Field"]
    fields = namespace["FieldsCollection"]

    builder.add(fields, field(name="count", kind="plain"))
    builder.add(fields, field(name="owner", kind="imported"))
    container = namespace["build_container"](builder)

    records = tuple(container.TemplateComponents.sequence())
    assert [record.name for record in records] == ["count", "owner"]
    assert records[0].template == PLAIN_TEMPLATE
    assert records[1].template == IMPORTED_TEMPLATE

    rendered = _render_selected_templates(container)
    assert rendered[0] == "{'template': 'plain'}"
    assert rendered[1] == "from math import sqrt\nsqrt"

    assert "from_import('math', 'sqrt')" in source
    assert "astichi_comment(\"plain property template\")" in source
    assert "source.resource" in source
    assert source.index("from_import") < source.index("_NameProperty")


if __name__ == "__main__":
    raise SystemExit(
        run_case("dds_generated_resource_flow.py", render_case, validate_case)
    )
