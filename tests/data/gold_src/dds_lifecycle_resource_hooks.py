from __future__ import annotations

from support.golden_case import run_case
from yidl.capsule.lifecycle_concepts import AFTER_COMMIT_HOOK
from yidl.capsule.lifecycle_concepts import AFTER_ROLLBACK_HOOK
from yidl.capsule.lifecycle_concepts import BEFORE_COMMIT_HOOK
from yidl.capsule.lifecycle_concepts import COMMIT_ORDER_KEY
from yidl.capsule.lifecycle_concepts import COMMIT_VALIDATOR
from yidl.capsule.lifecycle_concepts import LifecycleResourceHooksConcept
from yidl.capsule.lifecycle_concepts import MANAGED_KIND
from yidl.capsule.lifecycle_concepts import OWNED_KIND
from yidl.capsule.lifecycle_concepts import render_lifecycle_module
from yidl.generation.lifecycle_facts import CURRENT_FACADE


def render_case() -> str:
    runtime = LifecycleResourceHooksConcept.runtime().load()
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
            tx_group="default",
        ),
    )
    builder.add(
        namespace["FieldsCollection"],
        namespace["OwnedField"](
            name="resource",
            kind=OWNED_KIND,
            annotation_path="object",
            defaulted=True,
            default_value=None,
            order=1,
            tx_group="",
            release_path="release_resource",
            resource_policy="owned_scalar",
        ),
    )
    builder.add(
        namespace["CommitValidatorsCollection"],
        namespace["CommitValidator"](
            name="validate_default",
            source_label="Example.validate_default",
            callable_object=validate_default,
            callable_role=COMMIT_VALIDATOR,
            tx_group="default",
            order=0,
            callable_path="validate_default",
        ),
    )
    builder.add(
        namespace["CommitOrderKeysCollection"],
        namespace["CommitOrderKey"](
            name="order_default",
            source_label="Example.order_default",
            callable_object=order_default,
            callable_role=COMMIT_ORDER_KEY,
            tx_group="default",
            order=0,
            callable_path="order_default",
        ),
    )
    for hook_name, role, path, order in (
        ("before_default", BEFORE_COMMIT_HOOK, "before_default", 10),
        ("after_default", AFTER_COMMIT_HOOK, "after_default", 20),
        ("rollback_default", AFTER_ROLLBACK_HOOK, "rollback_default", 30),
    ):
        builder.add(
            namespace["HookDeclarationsCollection"],
            namespace["HookDeclaration"](
                name=hook_name,
                source_label=f"Example.{hook_name}",
                callable_object=globals()[path],
                callable_role=role,
                tx_group="default",
                phase=role,
                order=order,
                callable_path=path,
            ),
        )

    container = runtime.build_container(builder)
    assert [
        (record.callable_name, record.param_name, record.injection_kind)
        for record in container.CallableInjections.sequence()
    ] == [
        ("validate_default", "current", CURRENT_FACADE),
        ("order_default", "current", CURRENT_FACADE),
        ("before_default", "current", CURRENT_FACADE),
        ("after_default", "current", CURRENT_FACADE),
        ("rollback_default", "current", CURRENT_FACADE),
    ]
    assert [record.name for record in container.HookMethodStatements.sequence()] == [
        "validate_default",
        "before_commit_before_default",
        "after_commit_after_default",
        "after_rollback_rollback_default",
    ]
    assert [
        (record.name, record.param_name)
        for record in container.MethodCallArguments.sequence()
    ] == [
        ("validate_default", "current"),
        ("before_commit_before_default", "current"),
        ("after_commit_after_default", "current"),
        ("after_rollback_rollback_default", "current"),
    ]
    assert [record.name for record in container.ResourceCleanupStatements.sequence()] == [
        "close_resource",
    ]
    return render_lifecycle_module(container, namespace)


EVENTS: list[object] = []


def validate_default(*, current):
    EVENTS.append("validate")
    assert current.count == 2


def order_default(*, current):
    EVENTS.append("order")
    return current.count


def before_default(*, current):
    EVENTS.append("before")
    assert current.count == 2


def after_default(*, current):
    EVENTS.append("after")
    assert current.count == 2


def rollback_default(*, current):
    EVENTS.append("rollback")
    assert current.count == 2


def release_resource(value):
    EVENTS.append(("release", value))


def validate_case(source: str) -> None:
    namespace = {
        "after_default": after_default,
        "before_default": before_default,
        "release_resource": release_resource,
        "rollback_default": rollback_default,
        "validate_default": validate_default,
    }
    exec(source, namespace)

    resource = object()
    example = namespace["Example"](resource=resource)
    example.count = 2
    example.commit()
    assert EVENTS == ["before", "validate", "after"]
    assert example.count == 2

    EVENTS.clear()
    example.count = 4
    example.rollback()
    assert EVENTS == ["rollback"]
    assert example.count == 2

    EVENTS.clear()
    example.close()
    assert EVENTS == [("release", resource)]

    assert "def close(self):" in source
    assert "before_default(current=self)" in source
    assert "validate_default(current=self)" in source
    assert "after_default(current=self)" in source
    assert "rollback_default(current=self)" in source
    assert "release_resource(value)" in source
    assert "def order_default" not in source
    assert "pyrolyze" not in source
    assert "astichi_" not in source


if __name__ == "__main__":
    raise SystemExit(
        run_case("dds_lifecycle_resource_hooks.py", render_case, validate_case)
    )
