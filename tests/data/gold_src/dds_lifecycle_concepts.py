from __future__ import annotations

from support.golden_case import run_case
from yidl.capsule.lifecycle_concepts import CONST_KIND
from yidl.capsule.lifecycle_concepts import GET_OPERATION
from yidl.capsule.lifecycle_concepts import LifecycleConcept
from yidl.capsule.lifecycle_concepts import MAIN_FACADE
from yidl.capsule.lifecycle_concepts import MANAGED_KIND
from yidl.capsule.lifecycle_concepts import PROPERTY_PHASE
from yidl.capsule.lifecycle_concepts import render_lifecycle_module


def _build_container():
    runtime = LifecycleConcept.runtime().load()
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
            order=0,
            tx_group="default",
        ),
    )
    builder.add(
        namespace["FieldsCollection"],
        namespace["ConstField"](
            name="label",
            kind=CONST_KIND,
            order=1,
        ),
    )
    container = runtime.build_container(builder)
    return namespace, container


def render_case() -> str:
    namespace, container = _build_container()

    tx_group = container.TxGroups.by_identity("default")
    assert tx_group.tx_index == 0
    contribution = container.OperationContributions.by_identity(
        (MAIN_FACADE, "count", PROPERTY_PHASE)
    )
    assert contribution.operation_kind == GET_OPERATION
    assert contribution.field_name == "count"
    assert contribution.current_slot == "_count_current"
    assert contribution.working_slot == "_count_working"
    assert container.OperationContributions.by_identity(
        (MAIN_FACADE, "label", PROPERTY_PHASE)
    ).published_slot == "_label_value"

    return render_lifecycle_module(container, namespace)


def validate_case(source: str) -> None:
    namespace: dict[str, object] = {}
    exec(source, namespace)

    example = namespace["Example"](count=1, label="x")
    assert example.count == 1
    assert example.label == "x"
    example.count = 2
    assert example.count == 2
    assert example._state._count_current == 1
    assert example._state._count_working == 2
    try:
        example.label = "y"
    except AttributeError:
        pass
    else:
        raise AssertionError("const property should not have a setter")

    assert "class ExampleState:" in source
    assert "class Example:" in source
    assert "_NO_WORKING_VALUE = object()" in source
    assert "__slots__ = ('_count_current', '_count_working', '_label_value')" in source
    assert "__slots__ = ('_state',)" in source
    assert "@count.setter" in source
    assert "@label.setter" not in source
    assert "pyrolyze" not in source
    assert "astichi_" not in source


if __name__ == "__main__":
    raise SystemExit(run_case("dds_lifecycle_concepts.py", render_case, validate_case))
