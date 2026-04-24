from __future__ import annotations

import pytest

from yidl.capsule import CapsuleSpecInstance
from yidl.capsule.spec_lambda import (
    SpecContext,
    inspect_names,
    spec_compute,
    spec_filter,
)


def test_inspect_names_returns_ordered_named_parameters() -> None:
    names = inspect_names(lambda field_name, default: (field_name, default))

    assert names == ("field_name", "default")


def test_spec_compute_reads_values_from_spec_instance() -> None:
    spec = CapsuleSpecInstance.from_values(
        "field_spec",
        field_name="count",
        default=0,
    )

    result = spec_compute(spec, lambda field_name, default: f"{field_name}={default}")

    assert result == "count=0"


def test_spec_context_filter_returns_boolean_result() -> None:
    spec = CapsuleSpecInstance.from_values(
        "field_spec",
        init=True,
        default=0,
    )
    context = SpecContext.from_spec_instance(spec)

    assert context.filter(lambda init, default: init and default == 0) is True


def test_spec_compute_rejects_unknown_property_name() -> None:
    spec = CapsuleSpecInstance.from_values("field_spec", field_name="count")

    with pytest.raises(ValueError, match="unknown spec property 'missing'"):
        spec_compute(spec, lambda missing: missing)


def test_inspect_names_rejects_non_named_parameter_shapes() -> None:
    def bad_varargs(*args: object) -> bool:
        return bool(args)

    def bad_kwargs(**kwargs: object) -> bool:
        return bool(kwargs)

    def bad_positional_only(name: str, /) -> str:
        return name

    with pytest.raises(TypeError, match="named parameters only"):
        inspect_names(bad_varargs)

    with pytest.raises(TypeError, match="named parameters only"):
        inspect_names(bad_kwargs)

    with pytest.raises(TypeError, match="named parameters only"):
        inspect_names(bad_positional_only)


def test_spec_filter_requires_boolean_result() -> None:
    spec = CapsuleSpecInstance.from_values("field_spec", init=True)

    with pytest.raises(TypeError, match="spec filter must return bool"):
        spec_filter(spec, lambda init: 1 if init else 0)
