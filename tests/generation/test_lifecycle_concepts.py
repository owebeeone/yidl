from __future__ import annotations

import pytest

from yidl.capsule.lifecycle_concepts import CONST_KIND
from yidl.capsule.lifecycle_concepts import LifecycleConcept
from yidl.capsule.lifecycle_concepts import MAIN_FACADE
from yidl.capsule.lifecycle_concepts import MANAGED_KIND
from yidl.capsule.lifecycle_concepts import PROPERTY_PHASE
from yidl.capsule.lifecycle_concepts import render_lifecycle_module


def _runtime():
    return LifecycleConcept.runtime().load()


def test_lifecycle_operation_contribution_identity_is_stable() -> None:
    runtime = _runtime()
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
    container = runtime.build_container(builder)

    contribution = container.OperationContributions.by_identity(
        (MAIN_FACADE, "count", PROPERTY_PHASE)
    )

    assert contribution.name == "count"
    assert contribution.current_slot == "_count_current"
    assert contribution.working_slot == "_count_working"


def test_lifecycle_scaffold_requires_one_class_input() -> None:
    runtime = _runtime()
    builder = runtime.new_builder()

    with pytest.raises(ValueError, match="expected exactly one lifecycle class input"):
        runtime.build_container(builder)


def test_lifecycle_renderer_rejects_missing_class_role() -> None:
    runtime = _runtime()
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
        namespace["ConstField"](
            name="label",
            kind=CONST_KIND,
            order=0,
        ),
    )
    container = runtime.build_container(builder)

    with pytest.raises(ValueError, match="expected exactly one record"):
        render_lifecycle_module(container, namespace, class_roles=("missing",))
