from __future__ import annotations

from support.golden_case import run_case
from yidl.capsule.lifecycle_concepts import LifecycleCallableFactsConcept
from yidl.generation.lifecycle_facts import CURRENT_FACADE
from yidl.generation.lifecycle_facts import INITVAR
from yidl.generation.lifecycle_facts import TX_KEY
from yidl.generation.lifecycle_facts import WORKING_FACADE


def render_case() -> str:
    return LifecycleCallableFactsConcept.emit_runtime_source()


def validate_current(current):
    return current is not None


def validate_working(working, tx_key):
    return working is not None and bool(tx_key)


def make_default(seed="fallback"):
    return seed


def validate_case(source: str) -> None:
    namespace: dict[str, object] = {}
    exec(source, namespace)

    builder = namespace["new_builder"]()
    declaration = namespace["CallableDeclaration"]
    declarations = namespace["CallableDeclarationsCollection"]
    builder.add(
        declarations,
        declaration(
            name="validate_current",
            source_label="Example.validate_current",
            callable_object=validate_current,
            callable_role="commit_validator",
        ),
    )
    builder.add(
        declarations,
        declaration(
            name="validate_working",
            source_label="Example.validate_working",
            callable_object=validate_working,
            callable_role="commit_validator",
        ),
    )
    builder.add(
        declarations,
        declaration(
            name="make_default",
            source_label="Example.make_default",
            callable_object=make_default,
            callable_role="default_factory",
            allowed_injections=("seed",),
        ),
    )

    container = namespace["build_container"](builder)
    specs = tuple(container.CallableSpecs.sequence())
    params = tuple(container.CallableParams.sequence())
    injections = tuple(container.CallableInjections.sequence())

    assert [spec.name for spec in specs] == [
        "validate_current",
        "validate_working",
        "make_default",
    ]
    assert [
        (param.callable_name, param.param_name, param.param_kind, param.param_order)
        for param in params
    ] == [
        ("validate_current", "current", "POSITIONAL_OR_KEYWORD", 0),
        ("validate_working", "working", "POSITIONAL_OR_KEYWORD", 0),
        ("validate_working", "tx_key", "POSITIONAL_OR_KEYWORD", 1),
        ("make_default", "seed", "POSITIONAL_OR_KEYWORD", 0),
    ]
    assert [
        (
            injection.callable_name,
            injection.param_name,
            injection.injection_kind,
            injection.required,
        )
        for injection in injections
    ] == [
        ("validate_current", "current", CURRENT_FACADE, True),
        ("validate_working", "working", WORKING_FACADE, True),
        ("validate_working", "tx_key", TX_KEY, True),
        ("make_default", "seed", INITVAR, False),
    ]

    assert "from yidl.generation.lifecycle_facts import analyze_callable" in source
    assert "ctx.records(CallableDeclarationsCollection)" in source
    assert "CallableParam(**param)" in source
    assert "inspect" not in source
    assert "dds.operation(" not in source
    assert "astichi_" not in source
    assert "pyrolyze" not in source


if __name__ == "__main__":
    raise SystemExit(
        run_case("dds_lifecycle_callable_facts.py", render_case, validate_case)
    )
