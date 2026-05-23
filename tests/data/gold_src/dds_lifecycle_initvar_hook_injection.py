from __future__ import annotations

from support.golden_case import run_case
from yidl.capsule.lifecycle_concepts import BEFORE_COMMIT_HOOK
from yidl.capsule.lifecycle_concepts import INITVAR_KIND
from yidl.capsule.lifecycle_concepts import LifecycleInitvarClosureConcept
from yidl.capsule.lifecycle_concepts import MANAGED_KIND
from yidl.capsule.lifecycle_concepts import render_lifecycle_module


def render_case() -> str:
    runtime = LifecycleInitvarClosureConcept.runtime().load()
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
        namespace["InitVarField"](
            name="owner",
            kind=INITVAR_KIND,
            annotation_path="str",
            order=1,
            source_label="Example.owner",
        ),
    )
    builder.add(
        namespace["HookDeclarationsCollection"],
        namespace["HookDeclaration"](
            name="before_owner",
            source_label="Example.before_owner",
            callable_object=before_owner,
            callable_role=BEFORE_COMMIT_HOOK,
            tx_key="default",
            phase=BEFORE_COMMIT_HOOK,
            order=0,
            allowed_injections=("owner",),
            callable_path="before_owner",
        ),
    )

    container = runtime.build_container(builder)
    assert [record.name for record in container.RetainedInitVars.sequence()] == [
        "owner",
    ]
    assert [
        (record.name, record.param_name, record.target_name)
        for record in container.MethodCallArguments.sequence()
    ] == [
        ("before_commit_before_owner", "owner", "_owner_retained"),
    ]
    return render_lifecycle_module(container, namespace)


EVENTS: list[object] = []


def before_owner(*, owner):
    EVENTS.append(owner)


def validate_case(source: str) -> None:
    namespace = {"before_owner": before_owner}
    exec(source, namespace)

    example = namespace["Example"](owner="owner-value")
    example.count = 3
    example.commit()

    assert EVENTS == ["owner-value"]
    assert example.count == 3
    assert example._state._owner_retained == "owner-value"

    assert "owner: str" in source
    assert "before_owner(owner=state._owner_retained)" in source
    assert "current=self" not in source
    assert "@owner.setter" not in source
    assert "pyrolyze" not in source
    assert "astichi_" not in source


if __name__ == "__main__":
    raise SystemExit(
        run_case(
            "dds_lifecycle_initvar_hook_injection.py",
            render_case,
            validate_case,
        )
    )
