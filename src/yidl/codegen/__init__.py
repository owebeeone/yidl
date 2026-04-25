"""Generic code generation helpers for YIDL."""

from yidl.codegen.wrapper import (
    AccessorComposable,
    DuplicateWrapperProviderArguments,
    PropertyProvider,
    PropertySpec,
    ResolvedWrapperParameter,
    UnresolvedWrapperForParameters,
    generate_wrapper_factory,
    inspect_function_parameters,
    resolve_wrapper_parameters,
    wrapper_for,
)

__all__ = [
    "AccessorComposable",
    "DuplicateWrapperProviderArguments",
    "PropertyProvider",
    "PropertySpec",
    "ResolvedWrapperParameter",
    "UnresolvedWrapperForParameters",
    "generate_wrapper_factory",
    "inspect_function_parameters",
    "resolve_wrapper_parameters",
    "wrapper_for",
]
