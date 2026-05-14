from __future__ import annotations

from collections.abc import Mapping

import astichi

from support.golden_case import run_multi_source_case
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
        astichi_bind_external(field_name)
        {"getter": field_name}
    ]$ {
        keep field_name
        edge bind = TemplateBind
        edge keep_names = TemplateKeepNames
    }

    resource OutputRoot = code $[
        from __future__ import annotations

        astichi_comment("this is from {__file__}:{__line__}")

        GETTERS = {**astichi_hole(getter_entries)}


        def getter_for(name: str) -> dict[str, str]:
            return GETTERS[name]
    ]$

    resource GetterEntryBind = code `{"getter_name": record.name}` {
        keep record
    }
    resource GetterEntry = template $[
        {astichi_bind_external(getter_name): astichi_hole(getter_value)}
    ]$ {
        edge bind = GetterEntryBind
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


def _compile_concept() -> object:
    module = compile_yidl_files(
        {"lark_v2_vertical.yidl": YIDL_SOURCE},
        "lark_v2_vertical.yidl",
    )
    return module.concepts["LarkV2Vertical"]


def _build_dds() -> object:
    return _compile_concept().plan.build_data_definition()


def render_case() -> Mapping[str, str]:
    concept = _compile_concept()
    compiler_source = emit_container_runtime_source(concept.plan.build_data_definition())
    return {
        "compiler.py": compiler_source,
        "example_output.py": _render_example_output_source(
            compiler_source,
            concept.resources,
        ),
    }


def _render_example_output_source(
    compiler_source: str,
    resources: Mapping[str, object],
) -> str:
    namespace: dict[str, object] = {}
    exec(compiler_source, namespace)

    builder = namespace["new_builder"]()
    plain_field = namespace["PlainField"]
    managed_field = namespace["ManagedField"]
    fields = namespace["FieldsCollection"]

    builder.add(fields, plain_field(name="count", kind="plain"))
    builder.add(fields, managed_field(name="owner", kind="managed"))
    container = namespace["build_container"](builder)

    records = tuple(container.Components.sequence())

    output = astichi.build()
    output_root = resources["OutputRoot"]
    getter_entry = resources["GetterEntry"]
    output.add("Root", output_root.to_generator())

    for index, record in enumerate(records):
        entry_name = f"GetterEntry{index}"
        value_name = f"GetterValue{index}"
        output.add(entry_name, getter_entry.to_generator())
        output.add(value_name, record.template.to_generator())
        output.instance(entry_name).target("getter_value").add(
            value_name,
            arg_names=record.template.arg_names_for(record),
            bind=record.template.bind_for(record),
            keep_names=record.template.keep_names_for(record),
        )
        output.instance("Root").target("getter_entries").add(
            entry_name,
            order=index,
            arg_names=getter_entry.arg_names_for(record),
            bind=getter_entry.bind_for(record),
            keep_names=getter_entry.keep_names_for(record),
        )

    return output.build().emit_commented()


def validate_case(sources: Mapping[str, str]) -> None:
    compiler_source = sources["compiler.py"]
    example_output_source = sources["example_output.py"]

    namespace: dict[str, object] = {}
    exec(compiler_source, namespace)

    builder = namespace["new_builder"]()
    plain_field = namespace["PlainField"]
    managed_field = namespace["ManagedField"]
    fields = namespace["FieldsCollection"]

    builder.add(fields, plain_field(name="count", kind="plain"))
    builder.add(fields, managed_field(name="owner", kind="managed"))
    container = namespace["build_container"](builder)

    records = tuple(container.Components.sequence())
    assert [record.name for record in records] == ["count", "owner"]
    assert records[0].template.template.source == '{"getter": "plain"}'
    assert records[1].template.template.source == (
        "astichi_bind_external(field_name)\n"
        '{"getter": field_name}'
    )
    assert records[1].template.bind_for(records[1]) == {"field_name": "owner"}
    assert records[1].template.keep_names_for(records[1]) == ("field_name",)

    output_namespace: dict[str, object] = {}
    exec(example_output_source, output_namespace)
    assert output_namespace["GETTERS"] == {
        "count": {"getter": "plain"},
        "owner": {"getter": "owner"},
    }
    assert output_namespace["getter_for"]("owner") == {"getter": "owner"}

    assert "astichi_template(" in compiler_source
    assert "source.resource" in compiler_source
    assert "source.records[0].name" in compiler_source
    assert "# this is from lark_v2_vertical.yidl:46" in example_output_source
    assert "GETTERS = {'count': {'getter': 'plain'}, 'owner': {'getter': 'owner'}}" in (
        example_output_source
    )


if __name__ == "__main__":
    raise SystemExit(
        run_multi_source_case("yidl_lark_v2_vertical.py", render_case, validate_case)
    )
