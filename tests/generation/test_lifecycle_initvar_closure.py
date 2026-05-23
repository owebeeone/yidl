from __future__ import annotations

import pytest

from yidl.capsule.lifecycle_concepts import BEFORE_COMMIT_HOOK
from yidl.capsule.lifecycle_concepts import INITVAR_KIND
from yidl.capsule.lifecycle_concepts import LifecycleInitvarClosureConcept


def _runtime():
    return LifecycleInitvarClosureConcept.runtime().load()


def _add_class_input(builder, namespace) -> None:
    builder.add(
        namespace["ClassInputsCollection"],
        namespace["ClassInput"](
            class_name="Example",
            state_class_name="ExampleState",
        ),
    )


def _add_initvar(builder, namespace, name: str, *, order: int = 0) -> None:
    builder.add(
        namespace["FieldsCollection"],
        namespace["InitVarField"](
            name=name,
            kind=INITVAR_KIND,
            order=order,
            source_label=f"Example.{name}",
        ),
    )


def _add_before_hook(
    builder,
    namespace,
    *,
    name: str,
    callable_object,
    allowed_injections: tuple[str, ...],
) -> None:
    builder.add(
        namespace["HookDeclarationsCollection"],
        namespace["HookDeclaration"](
            name=name,
            source_label=f"Example.{name}",
            callable_object=callable_object,
            callable_role=BEFORE_COMMIT_HOOK,
            tx_key="default",
            phase=BEFORE_COMMIT_HOOK,
            allowed_injections=allowed_injections,
            callable_path=name,
        ),
    )


def test_initvar_closure_rejects_unknown_requested_initvar() -> None:
    def before_missing(missing):
        return missing

    runtime = _runtime()
    namespace = runtime.namespace
    builder = runtime.new_builder()
    _add_class_input(builder, namespace)
    _add_before_hook(
        builder,
        namespace,
        name="before_missing",
        callable_object=before_missing,
        allowed_injections=("missing",),
    )

    with pytest.raises(
        TypeError,
        match=r"unknown lifecycle initvar 'missing' requested by callable 'before_missing'",
    ):
        runtime.build_container(builder)


def test_initvar_closure_rejects_unused_initvar() -> None:
    runtime = _runtime()
    namespace = runtime.namespace
    builder = runtime.new_builder()
    _add_class_input(builder, namespace)
    _add_initvar(builder, namespace, "unused")

    with pytest.raises(
        TypeError,
        match=r"unused lifecycle initvar declarations: 'unused'",
    ):
        runtime.build_container(builder)


def test_initvar_closure_marks_hook_initvar_as_retained() -> None:
    def before_owner(owner):
        return owner

    runtime = _runtime()
    namespace = runtime.namespace
    builder = runtime.new_builder()
    _add_class_input(builder, namespace)
    _add_initvar(builder, namespace, "owner")
    _add_before_hook(
        builder,
        namespace,
        name="before_owner",
        callable_object=before_owner,
        allowed_injections=("owner",),
    )

    container = runtime.build_container(builder)

    assert [record.name for record in container.RetainedInitVars.sequence()] == [
        "owner",
    ]
    assert tuple(container.ConstructorOnlyInitVars.sequence()) == ()
