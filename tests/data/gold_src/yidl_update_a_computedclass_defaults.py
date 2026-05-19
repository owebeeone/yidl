from __future__ import annotations

from collections.abc import Mapping
from pathlib import Path

import black

from support.golden_case import run_multi_source_case
from yidl.concept_parser import compile_yidl_files
from yidl.generation.data_def_sys import emit_concept_runtime_source
from yidl_update_a_dataclasses_split import _container

BASE_FIXTURE_DIR = Path("tests/data/yidl/yidl_update_a_dataclasses_split")
FEATURE_FIXTURE_DIR = Path("tests/data/yidl/yidl_update_a_computedclass_defaults")
YIDL_PATHS = (
    BASE_FIXTURE_DIR / "dataclasses_base.yidl",
    BASE_FIXTURE_DIR / "dataclasses_initvar_base.yidl",
    BASE_FIXTURE_DIR / "dataclasses_classvar_base.yidl",
    BASE_FIXTURE_DIR / "dataclasses_combined.yidl",
    FEATURE_FIXTURE_DIR / "computedclass_default_factory_params.yidl",
    FEATURE_FIXTURE_DIR / "computedclass_defaults.yidl",
)
ENTRY_PATH = FEATURE_FIXTURE_DIR / "computedclass_defaults.yidl"


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
    output_source = sources["generated_output.py"]
    output_prettier_source = sources["generated_output_prettier.py"]

    namespace: dict[str, object] = {}
    exec(decorator_source, namespace)
    _assert_schema(namespace)
    _assert_refined_view(namespace)

    prettier_namespace: dict[str, object] = {}
    exec(decorator_prettier_source, prettier_namespace)
    _assert_schema(prettier_namespace)
    _assert_refined_view(prettier_namespace)

    assert (
        prettier_namespace["build_DataclassModule"](
            _container(prettier_namespace)
        ).emit_commented()
        == output_source
    )

    generated_namespace: dict[str, object] = {}
    exec(output_source, generated_namespace)
    output_prettier_namespace: dict[str, object] = {}
    exec(output_prettier_source, output_prettier_namespace)

    classes = generated_namespace["build_generated_dataclasses"](
        defaults={
            "Widget.level": 7,
            "Widget.hidden": "secret",
            "Widget.scale": 1,
            "Widget.kind": "widget",
        },
        default_factories={"Widget.tags": list},
    )
    pretty_classes = output_prettier_namespace["build_generated_dataclasses"](
        defaults={
            "Widget.level": 7,
            "Widget.hidden": "secret",
            "Widget.scale": 1,
            "Widget.kind": "widget",
        },
        default_factories={"Widget.tags": list},
    )

    assert repr(classes["Widget"](3, scale=5)) == "Widget(count=3, level=7, tags=[])"
    assert (
        repr(pretty_classes["Widget"](3, scale=5))
        == "Widget(count=3, level=7, tags=[])"
    )


def _compile_concept() -> object:
    sources = {path.as_posix(): path.read_text(encoding="utf-8") for path in YIDL_PATHS}
    return compile_yidl_files(sources, ENTRY_PATH.as_posix()).concepts[
        "ComputedClassDefaults"
    ]


def _output_source(decorator_source: str) -> str:
    namespace: dict[str, object] = {}
    exec(decorator_source, namespace)
    return namespace["build_DataclassModule"](
        _container(namespace),
    ).emit_commented()


def _assert_schema(namespace: Mapping[str, object]) -> None:
    assert "DefaultFactoryInitAction" in namespace
    assert "DefaultFactoryDep" in namespace
    assert "InitEvaluationStep" in namespace
    assert "ComputedClassDiagnostic" in namespace
    assert "DefaultFactoryInitActionsCollection" in namespace
    assert "DefaultFactoryDepsCollection" in namespace
    assert "InitEvaluationStepsCollection" in namespace
    assert "DiagnosticsCollection" in namespace
    assert "InitDefaultFactoryGuardFieldsCollection" in namespace
    assert "ZeroArgDefaultFactoryActionsCollection" in namespace
    assert "ParameterizedDefaultFactoryActionsCollection" in namespace


def _assert_refined_view(namespace: Mapping[str, object]) -> None:
    builder = namespace["new_builder"]()
    fields = namespace["FieldsCollection"]
    field = namespace["InstanceField"]
    actions = namespace["DefaultFactoryInitActionsCollection"]
    action = namespace["DefaultFactoryInitAction"]

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
            field_id="Widget.tags",
            field_owner="Widget",
            field_name="tags",
            field_order=20,
            annotation="list[str]",
            has_default_factory=True,
        ),
    )
    builder.add(
        fields,
        field(
            field_id="Widget.hidden",
            field_owner="Widget",
            field_name="hidden",
            field_order=30,
            annotation="str",
            has_default_factory=True,
            init=False,
        ),
    )
    builder.add(
        actions,
        action(
            action_id="Widget.tags",
            action_owner="Widget",
            action_field_id="Widget.tags",
            action_field_name="tags",
            action_field_order=20,
            action_kind="zero_arg",
        ),
    )
    builder.add(
        actions,
        action(
            action_id="Widget.total",
            action_owner="Widget",
            action_field_id="Widget.total",
            action_field_name="total",
            action_field_order=30,
            action_kind="parameterized",
            factory_param_names=("count",),
        ),
    )

    container = namespace["build_container"](builder)

    assert [
        record.field_name
        for record in container.InitDefaultFactoryGuardFields.sequence()
    ] == ["tags"]
    assert [
        record.action_field_name
        for record in container.ZeroArgDefaultFactoryActions.sequence()
    ] == ["tags"]
    assert [
        record.action_field_name
        for record in container.ParameterizedDefaultFactoryActions.sequence()
    ] == ["total"]


def _prettier_source(source: str) -> str:
    return black.format_str(source, mode=black.FileMode())


if __name__ == "__main__":
    raise SystemExit(
        run_multi_source_case(
            "yidl_update_a_computedclass_defaults.py",
            render_case,
            validate_case,
        )
    )
