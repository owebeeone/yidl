from __future__ import annotations

from collections.abc import Mapping
from pathlib import Path

import black

from support.golden_case import run_multi_source_case
from yidl.concept_parser import compile_yidl_files
from yidl.generation.data_def_sys import emit_concept_runtime_source


YIDL_PATH = Path("tests/data/yidl/dataclasses_example.yidl")


def render_case() -> Mapping[str, str]:
    concept = _compile_concept()
    decorator_source = emit_concept_runtime_source(
        concept.plan.build_data_definition(),
        resources=concept.resources,
        assembly_plan=concept,
    )
    output_source = _output_source(decorator_source)
    return {
        "decorator.py": decorator_source,
        "decorator_prettier.py": _prettier_source(decorator_source),
        "generated_output.py": output_source,
        "generated_output_prettier.py": _prettier_source(output_source),
    }


def validate_case(sources: Mapping[str, str]) -> None:
    decorator_source = sources["decorator.py"]
    decorator_prettier_source = sources["decorator_prettier.py"]
    source = sources["generated_output.py"]
    prettier_source = sources["generated_output_prettier.py"]

    decorator_namespace: dict[str, object] = {}
    exec(decorator_source, decorator_namespace)
    assert "DataclassFacade" in decorator_namespace
    assert "DataclassField" in decorator_namespace
    assert "FacadesCollection" in decorator_namespace
    assert "FieldsCollection" in decorator_namespace
    assert "ASSEMBLY_RESOURCES" in decorator_namespace
    assert "ASSEMBLY_CONTRIBUTIONS" in decorator_namespace
    assert "ASSEMBLY_MATCHERS" in decorator_namespace
    assert "build_DataclassModule" in decorator_namespace

    prettier_decorator_namespace: dict[str, object] = {}
    exec(decorator_prettier_source, prettier_decorator_namespace)
    assert (
        prettier_decorator_namespace["build_DataclassModule"](
            _container(prettier_decorator_namespace),
        ).emit_commented()
        == source
    )

    generated_namespace: dict[str, object] = {}
    exec(source, generated_namespace)
    prettier_namespace: dict[str, object] = {}
    exec(prettier_source, prettier_namespace)

    widget_class = generated_namespace["Widget"]
    pretty_widget_class = prettier_namespace["Widget"]
    first = widget_class(3, "x")
    same = widget_class(3, "x")
    different = widget_class(4, "x")

    assert repr(first) == "Widget(count=3, label='x')"
    assert first == same
    assert first != different
    assert hash(first) == hash((3, "x"))
    assert widget_class.__match_args__ == ("count", "label")
    assert widget_class.__dataclass_fields__["count"]["type"] == "int"
    assert repr(pretty_widget_class(3, "x")) == "Widget(count=3, label='x')"

    try:
        first.count = 9
    except generated_namespace["FrozenInstanceError"] as exc:
        assert "cannot assign to field 'count'" in str(exc)
    else:
        raise AssertionError("expected frozen assignment to fail")


def _compile_concept() -> object:
    return compile_yidl_files(
        {YIDL_PATH.as_posix(): YIDL_PATH.read_text(encoding="utf-8")},
        YIDL_PATH.as_posix(),
    ).concepts["DataclassSubstitute"]


def _output_source(decorator_source: str) -> str:
    namespace: dict[str, object] = {}
    exec(decorator_source, namespace)
    return namespace["build_DataclassModule"](
        _container(namespace),
    ).emit_commented()


def _container(namespace: Mapping[str, object]) -> object:
    builder = namespace["new_builder"]()
    facade = namespace["DataclassFacade"]
    field = namespace["DataclassField"]
    facades = namespace["FacadesCollection"]
    fields = namespace["FieldsCollection"]

    builder.add(
        facades,
        facade(
            class_id="Widget",
            class_name="Widget",
            module_name="generated_dataclasses",
            decorator_frozen=True,
            dataclass_params={"frozen": True},
            match_args=("count", "label"),
        ),
    )
    builder.add(
        fields,
        field(
            field_id="Widget.count",
            field_owner="Widget",
            field_name="count",
            field_order=10,
            annotation="int",
        ),
    )
    builder.add(
        fields,
        field(
            field_id="Widget.label",
            field_owner="Widget",
            field_name="label",
            field_order=20,
            annotation="str",
        ),
    )
    return builder.freeze()


def _prettier_source(source: str) -> str:
    return black.format_str(source, mode=black.FileMode())


if __name__ == "__main__":
    raise SystemExit(
        run_multi_source_case(
            "yidl_update_a_dataclasses_example.py",
            render_case,
            validate_case,
        )
    )
