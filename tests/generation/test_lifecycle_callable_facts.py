from __future__ import annotations

import pytest

from yidl.capsule.lifecycle_concepts import LifecycleCallableFactsConcept
from yidl.generation.lifecycle_facts import CURRENT_FACADE
from yidl.generation.lifecycle_facts import INITVAR
from yidl.generation.lifecycle_facts import analyze_callable


def test_callable_fact_analyzer_rejects_varargs() -> None:
    def bad(current, *args):
        return (current, args)

    with pytest.raises(TypeError, match=r"Example.bad: unsupported \*args"):
        analyze_callable(
            name="bad",
            source_label="Example.bad",
            role="validator",
            callable_obj=bad,
        )


def test_callable_fact_analyzer_rejects_unknown_injection() -> None:
    def bad(unregistered):
        return unregistered

    with pytest.raises(
        TypeError,
        match=r"Example.bad: unknown injection parameter 'unregistered'",
    ):
        analyze_callable(
            name="bad",
            source_label="Example.bad",
            role="validator",
            callable_obj=bad,
        )


def test_callable_fact_analyzer_rejects_noncallable() -> None:
    with pytest.raises(TypeError, match=r"Example.value: callable object is not callable"):
        analyze_callable(
            name="value",
            source_label="Example.value",
            role="validator",
            callable_obj=object(),
        )


def test_callable_fact_analyzer_result_validates_against_dds_records() -> None:
    def make_default(seed="fallback"):
        return seed

    runtime = LifecycleCallableFactsConcept.runtime().load()
    namespace = runtime.namespace
    builder = runtime.new_builder()
    builder.add(
        namespace["CallableDeclarationsCollection"],
        namespace["CallableDeclaration"](
            name="make_default",
            source_label="Example.make_default",
            callable_object=make_default,
            callable_role="default_factory",
            allowed_injections=("seed",),
        ),
    )

    container = runtime.build_container(builder)
    spec = container.CallableSpecs.one()
    param = container.CallableParams.one()
    injection = container.CallableInjections.one()

    assert spec.name == "make_default"
    assert param.param_name == "seed"
    assert injection.injection_kind == INITVAR
    assert injection.required is False


def test_callable_fact_analyzer_accepts_current_injection() -> None:
    def validate(current):
        return current is not None

    result = analyze_callable(
        name="validate",
        source_label="Example.validate",
        role="validator",
        callable_obj=validate,
    )

    assert result.params == (
        {
            "callable_name": "validate",
            "param_name": "current",
            "param_kind": "POSITIONAL_OR_KEYWORD",
            "param_order": 0,
        },
    )
    assert result.injections == (
        {
            "callable_name": "validate",
            "param_name": "current",
            "injection_kind": CURRENT_FACADE,
            "required": True,
        },
    )
