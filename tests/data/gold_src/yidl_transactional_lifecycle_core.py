from __future__ import annotations

from collections.abc import Callable
from collections.abc import Mapping
from pathlib import Path

import black

from support.golden_case import run_multi_source_case
from yidl.concept_parser import compile_yidl_files
from yidl.generation.data_def_sys import emit_concept_runtime_source
from yidl.runtime.transaction_yidl import DEFAULT_TRANSACTION


YIDL_PATH = Path("tests/data/yidl/yidl_transactional_lifecycle/lifecycle_core.yidl")


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

    decorator_namespace: dict[str, object] = {}
    exec(decorator_source, decorator_namespace)
    assert "LifecycleClass" in decorator_namespace
    assert "PlainField" in decorator_namespace
    assert "InitVarField" in decorator_namespace
    assert "ClassVarField" in decorator_namespace
    assert "ManagedField" not in decorator_namespace
    assert "build_LifecycleCoreModule" in decorator_namespace
    assert "build_LifecycleModule" not in decorator_namespace

    prettier_decorator_namespace: dict[str, object] = {}
    exec(decorator_prettier_source, prettier_decorator_namespace)
    assert (
        prettier_decorator_namespace["build_LifecycleCoreModule"](
            _container(prettier_decorator_namespace),
        ).emit_commented()
        == output_source
    )

    generated_namespace: dict[str, object] = {}
    exec(output_source, generated_namespace)
    output_prettier_namespace: dict[str, object] = {}
    exec(output_prettier_source, output_prettier_namespace)

    _assert_generated_class(generated_namespace)
    _assert_generated_class(output_prettier_namespace)


def _compile_concept() -> object:
    return compile_yidl_files(
        {YIDL_PATH.as_posix(): YIDL_PATH.read_text(encoding="utf-8")},
        YIDL_PATH.as_posix(),
    ).concepts["LifecycleCore"]


def _output_source(decorator_source: str) -> str:
    namespace: dict[str, object] = {}
    exec(decorator_source, namespace)
    return namespace["build_LifecycleCoreModule"](
        _container(namespace),
    ).emit_commented()


def _container(namespace: Mapping[str, object]) -> object:
    builder = namespace["new_builder"]()
    lifecycle_class = namespace["LifecycleClass"]
    classes = namespace["ClassesCollection"]
    fields = namespace["FieldsCollection"]
    plain_field = namespace["PlainField"]
    initvar_field = namespace["InitVarField"]
    classvar_field = namespace["ClassVarField"]

    builder.add(
        classes,
        lifecycle_class(
            class_id="Counter",
            class_name="Counter",
            class_order=10,
            module_name="generated_lifecycle_core",
            state_class_name="Counter_State",
            facade_base_class_name="Counter_FacadeBase",
            current_facade_class_name="Counter_Current",
            working_facade_class_name="Counter_Working",
            lifecycle_definition_param_name="_Counter_lifecycle_definition",
            annotations_param_name="_Counter_annotations",
            tx_groups_param_name="_Counter_tx_groups",
        ),
    )
    builder.add(
        fields,
        plain_field(
            field_id="Counter.plain",
            field_owner="Counter",
            field_name="plain",
            field_order=10,
            field_kind="field",
            annotation="int",
            has_default=True,
            default_value_param_name="_Counter_plain_default",
            value_slot_name="_y_plain_value",
        ),
    )
    builder.add(
        fields,
        initvar_field(
            field_id="Counter.seed",
            field_owner="Counter",
            field_name="seed",
            field_order=20,
            field_kind="initvar",
            annotation="int",
            has_default=True,
            default_value_param_name="_Counter_seed_default",
        ),
    )
    builder.add(
        fields,
        classvar_field(
            field_id="Counter.KIND",
            field_owner="Counter",
            field_name="KIND",
            field_order=30,
            field_kind="classvar",
            has_default=True,
            default_value_param_name="_Counter_KIND_default",
        ),
    )
    return namespace["build_container"](builder)


def _assert_generated_class(namespace: Mapping[str, object]) -> None:
    class Counter:
        def user_method(self) -> str:
            return "user"

    lifecycle_definition = {"fields": ("plain",)}
    annotations = {"plain": "int", "seed": "int"}
    generated = namespace["build_lifecycle_class"](
        Counter,
        _Counter_lifecycle_definition=lifecycle_definition,
        _Counter_annotations=annotations,
        _Counter_tx_groups=(DEFAULT_TRANSACTION,),
        _Counter_plain_default=3,
        _Counter_seed_default=2,
        _Counter_KIND_default="counter",
    )

    assert generated.__name__ == "Counter"
    assert generated.__qualname__ == Counter.__qualname__
    assert generated.__module__ == __name__
    assert generated.__annotations__ is annotations
    assert generated.__yidl_lifecycle_generated__ is True
    assert generated.__yidl_lifecycle_user_class__ is Counter
    assert generated.__yidl_lifecycle_definition__ is lifecycle_definition
    assert generated.__yidl_tx_index_to_key__ == (DEFAULT_TRANSACTION,)
    assert generated.__yidl_tx_key_to_index__ == {DEFAULT_TRANSACTION: 0}

    counter = generated()
    assert isinstance(counter, Counter)
    assert counter.user_method() == "user"
    assert counter.default is counter

    current = counter.current
    working = counter.working
    assert current is counter.current
    assert working is counter.working
    assert current.default is counter
    assert working.default is counter
    assert current.current is current
    assert working.working is working

    assert generated.KIND == "counter"
    assert counter.KIND == "counter"
    assert counter.plain == 3
    assert current.plain == 3
    assert working.plain == 3

    current.plain = 4
    assert counter.plain == 4
    assert working.plain == 4

    working.plain = 5
    assert counter.plain == 5
    assert current.plain == 5

    explicit = generated(plain=7, seed=9)
    assert explicit.plain == 7
    assert not hasattr(explicit, "seed")
    assert not hasattr(explicit, "count")
    assert not hasattr(explicit._y_state, "_y_KIND_value")

    with counter.begin(DEFAULT_TRANSACTION):
        pass


def _assert_raises(
    exception_type: type[BaseException],
    func: Callable[[], object],
) -> None:
    try:
        func()
    except exception_type:
        return
    raise AssertionError(f"expected {exception_type.__name__}")


def _prettier_source(source: str) -> str:
    return black.format_str(source, mode=black.FileMode())


if __name__ == "__main__":
    raise SystemExit(
        run_multi_source_case(
            "yidl_transactional_lifecycle_core.py",
            render_case,
            validate_case,
        )
    )
