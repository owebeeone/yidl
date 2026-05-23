from __future__ import annotations

import pytest

from yidl.capsule.lifecycle_concepts import COMMIT_ORDER_KEY
from yidl.capsule.lifecycle_concepts import COMMIT_VALIDATOR
from yidl.capsule.lifecycle_concepts import LifecycleResourceHooksConcept
from yidl.capsule.lifecycle_concepts import OWNED_KIND


def _runtime():
    return LifecycleResourceHooksConcept.runtime().load()


def _validator(*, current):
    return current


def _add_class_input(builder: object, namespace: object) -> None:
    builder.add(
        namespace["ClassInputsCollection"],
        namespace["ClassInput"](
            class_name="Example",
            state_class_name="ExampleState",
        ),
    )


def test_duplicate_commit_validator_rejects_per_transaction_group() -> None:
    runtime = _runtime()
    namespace = runtime.namespace
    validators = namespace["CommitValidatorsCollection"]
    record = namespace["CommitValidator"]
    builder = runtime.new_builder()
    builder.add(
        validators,
        record(
            name="validate_a",
            source_label="Example.validate_a",
            callable_object=_validator,
            callable_role=COMMIT_VALIDATOR,
            tx_key="default",
            order=0,
            callable_path="validate_a",
        ),
    )

    with pytest.raises(ValueError, match=r"duplicate identity 'default'"):
        builder.add(
            validators,
            record(
                name="validate_b",
                source_label="Example.validate_b",
                callable_object=_validator,
                callable_role=COMMIT_VALIDATOR,
                tx_key="default",
                order=1,
                callable_path="validate_b",
            ),
        )


def test_duplicate_commit_order_key_rejects_per_transaction_group() -> None:
    runtime = _runtime()
    namespace = runtime.namespace
    order_keys = namespace["CommitOrderKeysCollection"]
    record = namespace["CommitOrderKey"]
    builder = runtime.new_builder()
    builder.add(
        order_keys,
        record(
            name="order_a",
            source_label="Example.order_a",
            callable_object=_validator,
            callable_role=COMMIT_ORDER_KEY,
            tx_key="default",
            order=0,
            callable_path="order_a",
        ),
    )

    with pytest.raises(ValueError, match=r"duplicate identity 'default'"):
        builder.add(
            order_keys,
            record(
                name="order_b",
                source_label="Example.order_b",
                callable_object=_validator,
                callable_role=COMMIT_ORDER_KEY,
                tx_key="default",
                order=1,
                callable_path="order_b",
            ),
        )


def test_unsupported_resource_policy_rejects_during_operation() -> None:
    runtime = _runtime()
    namespace = runtime.namespace
    builder = runtime.new_builder()
    _add_class_input(builder, namespace)
    builder.add(
        namespace["FieldsCollection"],
        namespace["OwnedField"](
            name="resource",
            kind=OWNED_KIND,
            annotation_path="object",
            defaulted=True,
            default_value=None,
            order=0,
            tx_key="",
            release_path="release_resource",
            resource_policy="mystery",
        ),
    )

    with pytest.raises(
        TypeError,
        match=r"unsupported resource policy 'mystery' for field 'resource'",
    ):
        runtime.build_container(builder)
