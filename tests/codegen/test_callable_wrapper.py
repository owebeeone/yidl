from __future__ import annotations

from dataclasses import dataclass
import inspect
import textwrap

import astichi
import pytest

from yidl.codegen import (
    AccessorComposable,
    DuplicateWrapperProviderArguments,
    UnresolvedWrapperForParameters,
    inspect_function_parameters,
    resolve_wrapper_parameters,
    wrapper_for,
)


def _piece(src: str) -> astichi.Composable:
    return astichi.compile(textwrap.dedent(src).strip() + "\n")


@dataclass(frozen=True, slots=True)
class DictPropertySpec:
    property_name: str


@dataclass(frozen=True, slots=True)
class DictPropertyProvider:
    provider_name: str
    arg_name: str
    property_names: dict[str, str]

    def find(self, parameter_name: str) -> DictPropertySpec | None:
        property_name = self.property_names.get(parameter_name)
        if property_name is None:
            return None
        return DictPropertySpec(property_name=property_name)

    def accessor_for(self, spec: DictPropertySpec) -> AccessorComposable:
        return AccessorComposable(
            composable=_piece(
                """
                astichi_pass(provider, outer_bind=True)[
                    astichi_bind_external(property_key)
                ]
                """
            ),
            arg_names={"provider": self.arg_name},
            bind={"property_key": spec.property_name},
        )


@dataclass(frozen=True, slots=True)
class AttrPropertySpec:
    property_name: str


@dataclass(frozen=True, slots=True)
class AttrPropertyProvider:
    provider_name: str
    arg_name: str
    property_names: dict[str, str]

    def find(self, parameter_name: str) -> AttrPropertySpec | None:
        property_name = self.property_names.get(parameter_name)
        if property_name is None:
            return None
        return AttrPropertySpec(property_name=property_name)

    def accessor_for(self, spec: AttrPropertySpec) -> AccessorComposable:
        return AccessorComposable(
            reference_segments=(self.arg_name, spec.property_name),
        )


@dataclass(frozen=True, slots=True)
class ClassContext:
    class_name: str


def test_inspect_function_parameters_returns_ordered_named_parameters() -> None:
    names = inspect_function_parameters(lambda init, default: (init, default))

    assert names == ("init", "default")


def test_inspect_function_parameters_rejects_non_named_shapes() -> None:
    def bad_varargs(*args: object) -> bool:
        return bool(args)

    def bad_kwargs(**kwargs: object) -> bool:
        return bool(kwargs)

    def bad_positional_only(init: bool, /) -> bool:
        return init

    with pytest.raises(TypeError, match="named parameters only"):
        inspect_function_parameters(bad_varargs)

    with pytest.raises(TypeError, match="named parameters only"):
        inspect_function_parameters(bad_kwargs)

    with pytest.raises(TypeError, match="named parameters only"):
        inspect_function_parameters(bad_positional_only)


def test_resolve_wrapper_parameters_uses_first_matching_provider() -> None:
    first = DictPropertyProvider(
        provider_name="FieldSpec",
        arg_name="spec",
        property_names={"init": "init"},
    )
    second = DictPropertyProvider(
        provider_name="Fallback",
        arg_name="fallback",
        property_names={"init": "fallback_init"},
    )

    resolved = resolve_wrapper_parameters(lambda init: init, (first, second))

    assert resolved[0].provider is first
    assert resolved[0].spec.property_name == "init"


def test_wrapper_for_rejects_unresolved_parameters() -> None:
    provider = DictPropertyProvider(
        provider_name="FieldSpec",
        arg_name="spec",
        property_names={"init": "init"},
    )

    with pytest.raises(UnresolvedWrapperForParameters, match="missing names .*default"):
        wrapper_for(lambda init, default: (init, default), (provider,))


def test_wrapper_for_rejects_duplicate_provider_arg_names() -> None:
    first = DictPropertyProvider(
        provider_name="FieldSpec",
        arg_name="ctxt",
        property_names={"init": "init"},
    )
    second = AttrPropertyProvider(
        provider_name="ClassContext",
        arg_name="ctxt",
        property_names={"class_name": "class_name"},
    )

    with pytest.raises(DuplicateWrapperProviderArguments, match="duplicate provider arg_name"):
        wrapper_for(lambda init, class_name: (init, class_name), (first, second))


def test_wrapper_for_builds_astichi_generated_wrapper_across_multiple_providers() -> None:
    spec_provider = DictPropertyProvider(
        provider_name="FieldSpec",
        arg_name="spec",
        property_names={
            "init": "init",
            "default": "default",
        },
    )
    cls_provider = AttrPropertyProvider(
        provider_name="ClassContext",
        arg_name="cls_ctx",
        property_names={"class_name": "class_name"},
    )

    def func(init: bool, default: object, class_name: str) -> tuple[bool, object, str]:
        return (init, default, class_name)

    wrapper = wrapper_for(func, (spec_provider, cls_provider))

    assert tuple(inspect.signature(wrapper).parameters) == ("spec", "cls_ctx")
    assert wrapper({"init": True, "default": 0}, ClassContext(class_name="Counter")) == (
        True,
        0,
        "Counter",
    )
