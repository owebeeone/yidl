from __future__ import annotations

from support.golden_case import run_case
from yidl.capsule.lifecycle_concepts import BEFORE_COMMIT_HOOK
from yidl.capsule.lifecycle_concepts import DEFAULT_FACTORY
from yidl.capsule.lifecycle_concepts import INITVAR_KIND
from yidl.capsule.lifecycle_concepts import LifecycleInitvarClosureConcept
from yidl.capsule.lifecycle_concepts import render_lifecycle_module


def default_count(seed="fallback"):
    return seed


def retain_owner(owner):
    return owner


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
        namespace["InitVarField"](
            name="seed",
            kind=INITVAR_KIND,
            order=0,
            source_label="Example.seed",
        ),
    )
    builder.add(
        namespace["FieldsCollection"],
        namespace["InitVarField"](
            name="owner",
            kind=INITVAR_KIND,
            order=1,
            source_label="Example.owner",
        ),
    )
    builder.add(
        namespace["CallableDeclarationsCollection"],
        namespace["CallableDeclaration"](
            name="default_count",
            source_label="Example.default_count",
            callable_object=default_count,
            callable_role=DEFAULT_FACTORY,
            allowed_injections=("seed",),
        ),
    )
    builder.add(
        namespace["CallableDeclarationsCollection"],
        namespace["CallableDeclaration"](
            name="retain_owner",
            source_label="Example.retain_owner",
            callable_object=retain_owner,
            callable_role=BEFORE_COMMIT_HOOK,
            allowed_injections=("owner",),
        ),
    )

    container = runtime.build_container(builder)
    assert [record.name for record in container.ConstructorOnlyInitVars.sequence()] == [
        "seed",
    ]
    assert [record.name for record in container.RetainedInitVars.sequence()] == [
        "owner",
    ]
    return render_lifecycle_module(container, namespace)


def validate_case(source: str) -> None:
    namespace: dict[str, object] = {}
    exec(source, namespace)

    example = namespace["Example"](seed="token", owner="owner-value")
    assert example._state._owner_retained == "owner-value"
    assert not hasattr(example._state, "_seed_retained")
    assert not hasattr(namespace["Example"], "seed")
    assert not hasattr(namespace["Example"], "owner")

    assert "def __init__(self, *, seed, owner):" in source
    assert "class ExampleState:" in source
    assert "__slots__ = ('_owner_retained',)" in source
    assert "self._owner_retained = owner" in source
    assert "self._state = ExampleState(owner=owner)" in source
    assert "_seed_retained" not in source
    assert "@property" not in source
    assert "pyrolyze" not in source
    assert "astichi_" not in source


if __name__ == "__main__":
    raise SystemExit(
        run_case("dds_lifecycle_initvar_storage.py", render_case, validate_case)
    )
