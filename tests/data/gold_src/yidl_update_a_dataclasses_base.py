from __future__ import annotations

from collections.abc import Mapping
from pathlib import Path

import black

from support.golden_case import run_multi_source_case
from yidl.concept_parser import compile_yidl_files
from yidl.generation.assembly_runtime import AssemblyDiagnosticError
from yidl.generation.data_def_sys import emit_concept_runtime_source


YIDL_PATH = Path(
    "tests/data/yidl/yidl_update_a_dataclasses_split/dataclasses_base.yidl"
)


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
    assert "InstanceField" in decorator_namespace
    assert "FacadesCollection" in decorator_namespace
    assert "FieldsCollection" in decorator_namespace
    assert "ASSEMBLY_RESOURCES" in decorator_namespace
    assert "ASSEMBLY_CONTRIBUTIONS" in decorator_namespace
    assert "ASSEMBLY_MATCHERS" in decorator_namespace
    assert "build_DataclassModule" in decorator_namespace
    _assert_diagnostic(decorator_namespace)

    prettier_decorator_namespace: dict[str, object] = {}
    exec(decorator_prettier_source, prettier_decorator_namespace)
    assert (
        prettier_decorator_namespace["build_DataclassModule"](
            _container(prettier_decorator_namespace),
        ).emit_commented()
        == source
    )
    _assert_diagnostic(prettier_decorator_namespace)

    generated_namespace: dict[str, object] = {}
    exec(source, generated_namespace)
    prettier_namespace: dict[str, object] = {}
    exec(prettier_source, prettier_namespace)

    defaults = {
        "Widget.level": 7,
        "Widget.hidden": "secret",
    }
    default_factories = {"Widget.tags": list}

    classes = generated_namespace["build_generated_dataclasses"](
        defaults=defaults,
        default_factories=default_factories,
    )
    pretty_classes = prettier_namespace["build_generated_dataclasses"](
        defaults=defaults,
        default_factories=default_factories,
    )
    widget_class = classes["Widget"]
    pretty_widget_class = pretty_classes["Widget"]
    first = widget_class(3)
    same = widget_class(3, tags=["different"])
    different = widget_class(4)
    overridden = widget_class(3, 8)

    assert first.count == 3
    assert first.level == 7
    assert first.tags == []
    assert first.hidden == "secret"
    assert overridden.level == 8
    first.tags.append("a")
    assert widget_class(3).tags == []
    assert repr(first) == "Widget(count=3, level=7, tags=['a'])"
    assert first == same
    assert first != different
    assert hash(first) == hash((3, 7))
    assert widget_class.__match_args__ == ("count", "level", "tags")
    assert widget_class.__dataclass_fields__["count"]["type"] == "int"
    assert widget_class.__dataclass_fields__["level"]["default"] == 7
    assert widget_class.__dataclass_fields__["tags"]["default_factory"] is list
    assert repr(pretty_widget_class(3)) == "Widget(count=3, level=7, tags=[])"

    try:
        first.count = 9
    except generated_namespace["FrozenInstanceError"] as exc:
        assert "cannot assign to field 'count'" in str(exc)
    else:
        raise AssertionError("expected frozen assignment to fail")


def _assert_diagnostic(namespace: Mapping[str, object]) -> None:
    try:
        namespace["build_DataclassModule"](_invalid_container(namespace))
    except AssemblyDiagnosticError as exc:
        assert str(exc) == (
            "field conflict cannot specify both default and default_factory"
        )
    else:
        raise AssertionError("expected default/default_factory diagnostic")


def _compile_concept() -> object:
    return compile_yidl_files(
        {YIDL_PATH.as_posix(): YIDL_PATH.read_text(encoding="utf-8")},
        YIDL_PATH.as_posix(),
    ).concepts["DataclassesBase"]


def _output_source(decorator_source: str) -> str:
    namespace: dict[str, object] = {}
    exec(decorator_source, namespace)
    return namespace["build_DataclassModule"](
        _container(namespace),
    ).emit_commented()


def _container(namespace: Mapping[str, object]) -> object:
    builder = namespace["new_builder"]()
    facade = namespace["DataclassFacade"]
    field = namespace["InstanceField"]
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
            match_args=("count", "level", "tags"),
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
            field_id="Widget.level",
            field_owner="Widget",
            field_name="level",
            field_order=20,
            annotation="int",
            has_default=True,
        ),
    )
    builder.add(
        fields,
        field(
            field_id="Widget.tags",
            field_owner="Widget",
            field_name="tags",
            field_order=30,
            annotation="list[str]",
            has_default_factory=True,
            compare=False,
        ),
    )
    builder.add(
        fields,
        field(
            field_id="Widget.hidden",
            field_owner="Widget",
            field_name="hidden",
            field_order=40,
            annotation="str",
            has_default=True,
            init=False,
            repr=False,
            compare=False,
        ),
    )
    return builder.freeze()


def _invalid_container(namespace: Mapping[str, object]) -> object:
    builder = namespace["new_builder"]()
    facade = namespace["DataclassFacade"]
    field = namespace["InstanceField"]
    facades = namespace["FacadesCollection"]
    fields = namespace["FieldsCollection"]

    builder.add(facades, facade(class_id="Broken", class_name="Broken"))
    builder.add(
        fields,
        field(
            field_id="Broken.conflict",
            field_owner="Broken",
            field_name="conflict",
            field_order=10,
            annotation="object",
            has_default=True,
            has_default_factory=True,
        ),
    )
    return builder.freeze()


def _prettier_source(source: str) -> str:
    return black.format_str(source, mode=black.FileMode())


if __name__ == "__main__":
    raise SystemExit(
        run_multi_source_case(
            "yidl_update_a_dataclasses_base.py",
            render_case,
            validate_case,
        )
    )
