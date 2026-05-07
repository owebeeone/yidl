from __future__ import annotations

from support.golden_case import run_case
from yidl.concept_parser import compile_yidl_files
from yidl.generation.data_def_sys import emit_container_runtime_source


YIDL_SOURCE = """
module lark_v2_vertical

concept LarkV2Vertical {
    property Name: str
    property Kind: str = "plain"
    property Template: object

    family FieldSpecs {
        common Name, Kind
        variant PlainField {}
        variant ManagedField {}
    }

    family ComponentSpecs {
        variant Component {
            Name
            Template
        }
    }

    collection Fields: FieldSpecs identity Name many
    collection Components: Component identity Name many

    resource TemplateBind = code `{"field_name": record.name}` {
        keep record
    }
    resource TemplateKeepNames = code `("field_name",)`

    resource PlainTemplate = template $[
        {"getter": "plain"}
    ]$

    resource ManagedTemplate = template $[
        {"getter": field_name}
    ]$ {
        keep field_name
        edge bind = TemplateBind
        edge keep_names = TemplateKeepNames
    }

    matcher FieldTemplate(field: Fields) {
        default PlainTemplate
        rule managed when field.Kind == "managed" -> ManagedTemplate
    }

    production FieldTemplateComponents from FieldTemplate.results() to Components {
        identity match.record("field").Name
        policy AddIfAbsent
        set Name = match.record("field").Name
        set Template = match.resource()
    }
}
"""


def _build_dds() -> object:
    module = compile_yidl_files(
        {"lark_v2_vertical.yidl": YIDL_SOURCE},
        "lark_v2_vertical.yidl",
    )
    return module.concepts["LarkV2Vertical"].plan.build_data_definition()


def render_case() -> str:
    return emit_container_runtime_source(_build_dds())


def validate_case(source: str) -> None:
    namespace: dict[str, object] = {}
    exec(source, namespace)

    builder = namespace["new_builder"]()
    field = namespace["PlainField"]
    fields = namespace["FieldsCollection"]

    builder.add(fields, field(name="count", kind="plain"))
    builder.add(fields, field(name="owner", kind="managed"))
    container = namespace["build_container"](builder)

    records = tuple(container.Components.sequence())
    assert [record.name for record in records] == ["count", "owner"]
    assert records[0].template.template.source == '{"getter": "plain"}'
    assert records[1].template.template.source == '{"getter": field_name}'
    assert records[1].template.bind_for(records[1]) == {"field_name": "owner"}
    assert records[1].template.keep_names_for(records[1]) == ("field_name",)
    assert "astichi_template(" in source
    assert "source.resource" in source
    assert "source.records[0].name" in source


if __name__ == "__main__":
    raise SystemExit(
        run_case("yidl_lark_v2_vertical.py", render_case, validate_case)
    )
