from __future__ import annotations

from collections.abc import Mapping
from pathlib import Path

import black

from support.golden_case import run_multi_source_case
from yidl.concept_parser import compile_yidl_files
from yidl.generation.data_def_sys import emit_concept_runtime_source

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


def _tags_factory() -> list[str]:
    return []


def _example_v2_factory(v1: int) -> int:
    return v1 + 2


def _example_v3_factory(v2: int, v1: int, v4: int) -> int:
    return v1 + v2 + v4 + 2


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
    _assert_diagnostics(namespace)

    prettier_namespace: dict[str, object] = {}
    exec(decorator_prettier_source, prettier_namespace)
    _assert_schema(prettier_namespace)
    _assert_refined_view(prettier_namespace)
    _assert_diagnostics(prettier_namespace)

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
        defaults={"Example.v4": 4},
        default_factories={
            "Example.v2": _example_v2_factory,
            "Example.v3": _example_v3_factory,
        },
    )
    pretty_classes = output_prettier_namespace["build_generated_dataclasses"](
        defaults={"Example.v4": 4},
        default_factories={
            "Example.v2": _example_v2_factory,
            "Example.v3": _example_v3_factory,
        },
    )

    example = classes["Example"](10)
    pretty_example = pretty_classes["Example"](10)
    assert example.v2 == 12
    assert example.v3 == 28
    assert example.v4 == 4
    assert pretty_example.v2 == 12
    assert pretty_example.v3 == 28
    assert pretty_example.v4 == 4
    assert list(classes["Example"].__dataclass_fields__) == ["v1", "v3", "v4", "v2"]
    assert "locals()" not in output_source
    assert output_source.index("v2 = _yidl_default_factories['Example.v2']") < (
        output_source.index("v3 = _yidl_default_factories['Example.v3']")
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


def _container(namespace: Mapping[str, object]) -> object:
    builder = namespace["new_builder"]()
    facade = namespace["DataclassFacade"]
    field = namespace["InstanceField"]
    facades = namespace["FacadesCollection"]
    fields = namespace["FieldsCollection"]

    builder.add(
        facades,
        facade(
            class_id="Example",
            class_name="Example",
            class_order=20,
            module_name="generated_dataclasses",
            match_args=("v1", "v3", "v2"),
        ),
    )
    builder.add(
        fields,
        field(
            field_id="Example.v1",
            field_owner="Example",
            field_name="v1",
            field_order=10,
            annotation="int",
        ),
    )
    builder.add(
        fields,
        field(
            field_id="Example.v3",
            field_owner="Example",
            field_name="v3",
            field_order=20,
            annotation="int",
            has_default_factory=True,
            default_factory=_example_v3_factory,
        ),
    )
    builder.add(
        fields,
        field(
            field_id="Example.v4",
            field_owner="Example",
            field_name="v4",
            field_order=25,
            annotation="int",
            has_default=True,
            init=False,
            repr=False,
            compare=False,
        ),
    )
    builder.add(
        fields,
        field(
            field_id="Example.v2",
            field_owner="Example",
            field_name="v2",
            field_order=30,
            annotation="int",
            has_default_factory=True,
            default_factory=_example_v2_factory,
        ),
    )
    return namespace["build_container"](builder)


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
    facades = namespace["FacadesCollection"]
    facade = namespace["DataclassFacade"]
    fields = namespace["FieldsCollection"]
    field = namespace["InstanceField"]

    def _tags_factory() -> list[str]:
        return []

    def _total_factory(count: int, tags: list[str]) -> int:
        return count + len(tags)

    builder.add(
        facades,
        facade(
            class_id="Widget",
            class_name="Widget",
            class_order=10,
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
            field_id="Widget.tags",
            field_owner="Widget",
            field_name="tags",
            field_order=20,
            annotation="list[str]",
            has_default_factory=True,
            default_factory=_tags_factory,
        ),
    )
    builder.add(
        fields,
        field(
            field_id="Widget.total",
            field_owner="Widget",
            field_name="total",
            field_order=30,
            annotation="int",
            has_default_factory=True,
            default_factory=_total_factory,
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
            has_default_factory=True,
            default_factory=_tags_factory,
            init=False,
        ),
    )
    container = namespace["build_container"](builder)

    assert [
        record.field_name
        for record in container.InitDefaultFactoryGuardFields.sequence()
    ] == ["tags", "total"]
    assert [
        (record.action_field_name, record.factory_param_names)
        for record in container.ZeroArgDefaultFactoryActions.sequence()
    ] == [("tags", ()), ("hidden", ())]
    assert [
        (
            record.action_field_name,
            record.factory_param_names,
            record.action_eval_order,
        )
        for record in container.ParameterizedDefaultFactoryActions.sequence()
    ] == [
        ("total", ("count", "tags"), 1),
    ]
    assert [
        (
            record.dependency_owner,
            record.consumer_field_id,
            record.consumer_eval_order,
            record.provider_field_id,
            record.provider_name,
            record.provider_init,
            record.provider_has_default,
            record.provider_has_default_factory,
            record.param_name,
            record.param_order,
        )
        for record in container.DefaultFactoryDeps.sequence()
    ] == [
        (
            "Widget",
            "Widget.total",
            1,
            "Widget.count",
            "count",
            True,
            False,
            False,
            "count",
            0,
        ),
        (
            "Widget",
            "Widget.total",
            1,
            "Widget.tags",
            "tags",
            True,
            False,
            True,
            "tags",
            1,
        ),
    ]
    assert [
        (record.eval_field_id, record.eval_field_name, record.eval_order)
        for record in container.InitEvaluationSteps.sequence()
    ] == [
        ("Widget.tags", "tags", 0),
        ("Widget.total", "total", 1),
        ("Widget.hidden", "hidden", 2),
    ]
    assert list(container.Diagnostics.sequence()) == []


def _assert_diagnostics(namespace: Mapping[str, object]) -> None:
    _assert_diagnostic_message(
        namespace,
        _diagnostic_builder_unknown_dependency(namespace),
        "field unknown default_factory unknown dependency 'missing'",
    )
    _assert_diagnostic_message(
        namespace,
        _diagnostic_builder_unsupported_parameter(namespace),
        "field unsupported default_factory has unsupported parameter 'items'",
    )
    _assert_diagnostic_message(
        namespace,
        _diagnostic_builder_cycle(namespace),
        "default_factory dependency cycle: Cycle.a -> Cycle.b -> Cycle.a",
    )
    _assert_diagnostic_message(
        namespace,
        _diagnostic_builder_invalid_initvar(namespace),
        "init-only field scratch with init=False must specify default or default_factory",
    )


def _assert_diagnostic_message(
    namespace: Mapping[str, object],
    builder: object,
    expected: str,
) -> None:
    diagnostic_error = namespace["AssemblyDiagnosticError"]
    try:
        namespace["build_container"](builder)
    except diagnostic_error as exc:
        assert str(exc) == expected
    else:
        raise AssertionError(f"expected diagnostic {expected!r}")


def _diagnostic_builder_unknown_dependency(namespace: Mapping[str, object]) -> object:
    def _unknown_factory(missing: object) -> object:
        return missing

    builder, field, _ = _diagnostic_builder(namespace, "Unknown")
    builder.add(
        namespace["FieldsCollection"],
        field(
            field_id="Unknown.unknown",
            field_owner="Unknown",
            field_name="unknown",
            field_order=10,
            annotation="object",
            has_default_factory=True,
            default_factory=_unknown_factory,
        ),
    )
    return builder


def _diagnostic_builder_unsupported_parameter(
    namespace: Mapping[str, object],
) -> object:
    def _unsupported_factory(*items: object) -> tuple[object, ...]:
        return items

    builder, field, _ = _diagnostic_builder(namespace, "Unsupported")
    builder.add(
        namespace["FieldsCollection"],
        field(
            field_id="Unsupported.unsupported",
            field_owner="Unsupported",
            field_name="unsupported",
            field_order=10,
            annotation="object",
            has_default_factory=True,
            default_factory=_unsupported_factory,
        ),
    )
    return builder


def _diagnostic_builder_cycle(namespace: Mapping[str, object]) -> object:
    def _cycle_a(b: object) -> object:
        return b

    def _cycle_b(a: object) -> object:
        return a

    builder, field, fields = _diagnostic_builder(namespace, "Cycle")
    builder.add(
        fields,
        field(
            field_id="Cycle.a",
            field_owner="Cycle",
            field_name="a",
            field_order=10,
            annotation="object",
            has_default_factory=True,
            default_factory=_cycle_a,
        ),
    )
    builder.add(
        fields,
        field(
            field_id="Cycle.b",
            field_owner="Cycle",
            field_name="b",
            field_order=20,
            annotation="object",
            has_default_factory=True,
            default_factory=_cycle_b,
        ),
    )
    return builder


def _diagnostic_builder_invalid_initvar(namespace: Mapping[str, object]) -> object:
    builder = namespace["new_builder"]()
    facades = namespace["FacadesCollection"]
    fields = namespace["FieldsCollection"]
    facade = namespace["DataclassFacade"]
    initvar = namespace["InitVarField"]
    builder.add(facades, facade(class_id="InitOnly", class_name="InitOnly"))
    builder.add(
        fields,
        initvar(
            field_id="InitOnly.scratch",
            field_owner="InitOnly",
            field_name="scratch",
            field_order=10,
            field_kind="initvar",
            annotation="object",
            init=False,
        ),
    )
    return builder


def _diagnostic_builder(
    namespace: Mapping[str, object],
    class_id: str,
) -> tuple[object, object, object]:
    builder = namespace["new_builder"]()
    facades = namespace["FacadesCollection"]
    fields = namespace["FieldsCollection"]
    facade = namespace["DataclassFacade"]
    field = namespace["InstanceField"]
    builder.add(facades, facade(class_id=class_id, class_name=class_id))
    return builder, field, fields


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
