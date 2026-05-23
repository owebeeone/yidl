from __future__ import annotations

from support.golden_case import run_case
from yidl.capsule.lifecycle_concepts import AFTER_COMMIT_HOOK
from yidl.capsule.lifecycle_concepts import BEFORE_COMMIT_HOOK
from yidl.capsule.lifecycle_concepts import DEFAULT_FACTORY
from yidl.capsule.lifecycle_concepts import INITVAR_KIND
from yidl.capsule.lifecycle_concepts import LifecycleInitvarClosureConcept
from yidl.capsule.lifecycle_concepts import current_slot_for_result
from yidl.capsule.lifecycle_concepts import property_order_for
from yidl.capsule.lifecycle_concepts import published_slot_for_result
from yidl.capsule.lifecycle_concepts import working_slot_for_result


def render_case() -> str:
    return LifecycleInitvarClosureConcept.emit_runtime_source()


def default_count(seed="fallback"):
    return seed


def before_owner(owner):
    return owner is not None


def after_session(session):
    return session


def validate_case(source: str) -> None:
    namespace: dict[str, object] = {
        "current_slot_for_result": current_slot_for_result,
        "property_order_for": property_order_for,
        "published_slot_for_result": published_slot_for_result,
        "working_slot_for_result": working_slot_for_result,
    }
    exec(source, namespace)

    builder = namespace["new_builder"]()
    builder.add(
        namespace["ClassInputsCollection"],
        namespace["ClassInput"](
            class_name="Example",
            state_class_name="ExampleState",
        ),
    )
    fields = namespace["FieldsCollection"]
    initvar = namespace["InitVarField"]
    declarations = namespace["CallableDeclarationsCollection"]
    declaration = namespace["CallableDeclaration"]
    hooks = namespace["HookDeclarationsCollection"]
    hook = namespace["HookDeclaration"]

    for order, name in enumerate(("seed", "owner", "session")):
        builder.add(
            fields,
            initvar(
                name=name,
                kind=INITVAR_KIND,
                order=order,
                source_label=f"Example.{name}",
            ),
        )

    builder.add(
        declarations,
        declaration(
            name="default_count",
            source_label="Example.default_count",
            callable_object=default_count,
            callable_role=DEFAULT_FACTORY,
            allowed_injections=("seed",),
        ),
    )
    builder.add(
        hooks,
        hook(
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
    builder.add(
        hooks,
        hook(
            name="after_session",
            source_label="Example.after_session",
            callable_object=after_session,
            callable_role=AFTER_COMMIT_HOOK,
            tx_key="default",
            phase=AFTER_COMMIT_HOOK,
            order=1,
            allowed_injections=("session",),
            callable_path="after_session",
        ),
    )

    container = namespace["build_container"](builder)

    assert [
        (edge.consumer, edge.initvar_name, edge.source_label)
        for edge in container.InitvarEdges.sequence()
    ] == [
        ("default_count", "seed", "Example.default_count"),
        ("before_owner", "owner", "Example.before_owner"),
        ("after_session", "session", "Example.after_session"),
    ]
    assert [
        (record.consumer, record.source_label)
        for record in container.LateInitvarConsumers.sequence()
    ] == [
        ("before_owner", "Example.before_owner"),
        ("after_session", "Example.after_session"),
    ]
    assert [
        (record.name, record.source_label)
        for record in container.RetainedInitVars.sequence()
    ] == [
        ("owner", "Example.before_owner"),
        ("session", "Example.after_session"),
    ]
    assert [
        (record.name, record.source_label)
        for record in container.ConstructorOnlyInitVars.sequence()
    ] == [
        ("seed", "Example.seed"),
    ]

    assert "def run_build_initvar_edges(builder):" in source
    assert "def run_build_retained_init_vars(builder):" in source
    assert "def run_build_constructor_only_init_vars(builder):" in source
    assert "queue = list(roots)" in source
    assert "unused lifecycle initvar declarations" in source
    assert "reachable_collection" not in source
    assert "pyrolyze" not in source


if __name__ == "__main__":
    raise SystemExit(
        run_case("dds_lifecycle_initvar_closure.py", render_case, validate_case)
    )
