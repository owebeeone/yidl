from __future__ import annotations

from support.golden_case import run_case
from yidl.capsule.lifecycle_concepts import CONST_KIND
from yidl.capsule.lifecycle_concepts import LifecycleStaircaseConcept
from yidl.capsule.lifecycle_concepts import MANAGED_KIND
from yidl.capsule.lifecycle_concepts import render_lifecycle_module


def render_case() -> str:
    runtime = LifecycleStaircaseConcept.runtime().load()
    namespace = runtime.namespace
    builder = runtime.new_builder()
    builder.add(
        namespace["ClassInputsCollection"],
        namespace["ClassInput"](
            class_name="Example",
            state_class_name="ExampleState",
        ),
    )
    builder.add(
        namespace["FieldsCollection"],
        namespace["ManagedField"](
            name="count",
            kind=MANAGED_KIND,
            annotation_path="int",
            defaulted=True,
            default_value=0,
            order=0,
            tx_key="default",
        ),
    )
    builder.add(
        namespace["FieldsCollection"],
        namespace["ConstField"](
            name="label",
            kind=CONST_KIND,
            annotation_path="str",
            defaulted=True,
            default_value="x",
            order=1,
        ),
    )
    container = runtime.build_container(builder)
    assert [record.name for record in container.MethodStatements.sequence()] == [
        "commit_count",
        "rollback_count",
    ]
    return render_lifecycle_module(container, namespace)


def validate_case(source: str) -> None:
    namespace: dict[str, object] = {}
    exec(source, namespace)

    example = namespace["Example"]()
    assert example.count == 0
    assert example.label == "x"

    example.count = 2
    assert example.count == 2
    example.rollback()
    assert example.count == 0

    example.count = 3
    example.commit()
    assert example.count == 3
    assert example._state._count_current == 3
    assert example._state._count_working is namespace["_NO_WORKING_VALUE"]

    try:
        example.label = "y"
    except AttributeError:
        pass
    else:
        raise AssertionError("const label should be read-only")

    assert "def commit(self):" in source
    assert "def rollback(self):" in source
    assert "@count.setter" in source
    assert "@label.setter" not in source
    assert "count: int=0" in source
    assert "label: str='x'" in source
    assert "pyrolyze" not in source
    assert "astichi_" not in source


if __name__ == "__main__":
    raise SystemExit(
        run_case(
            "dds_lifecycle_managed_const_staircase.py",
            render_case,
            validate_case,
        )
    )
