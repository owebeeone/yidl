"""Astichi-backed callable wrapper generation."""

from __future__ import annotations

from collections.abc import Callable, Mapping, Sequence
from dataclasses import dataclass, field
import inspect
import textwrap
from typing import TYPE_CHECKING, Any, Protocol

if TYPE_CHECKING:
    from astichi import Composable
    from astichi.builder import BuilderHandle


class PropertySpec(Protocol):
    """Resolved provider-side property information for one parameter."""

    property_name: str


class PropertyProvider(Protocol):
    """Ordered source that can resolve a callable parameter name."""

    provider_name: str
    arg_name: str

    def find(self, parameter_name: str) -> PropertySpec | None:
        """Return the matching property spec for ``parameter_name`` if present."""

    def accessor_for(self, spec: PropertySpec) -> "AccessorComposable":
        """Return the Astichi value expression for ``spec``."""


@dataclass(frozen=True, slots=True)
class AccessorComposable:
    """Provider-supplied Astichi value expression plus edge-local overlays."""

    composable: Composable | None = None
    arg_names: Mapping[str, str] = field(default_factory=dict)
    bind: Mapping[str, object] = field(default_factory=dict)
    reference_segments: tuple[str, ...] | None = None

    def __post_init__(self) -> None:
        if (self.composable is None) == (self.reference_segments is None):
            raise ValueError(
                "AccessorComposable requires exactly one of `composable` or "
                "`reference_segments`"
            )
        if self.reference_segments is not None and not self.reference_segments:
            raise ValueError("reference_segments must not be empty")


@dataclass(frozen=True, slots=True)
class ResolvedWrapperParameter:
    """One callable parameter resolved to a provider/property pair."""

    parameter_name: str
    provider: PropertyProvider
    spec: PropertySpec


class UnresolvedWrapperForParameters(ValueError):
    """Raised when a callable parameter cannot be resolved by any provider."""


class DuplicateWrapperProviderArguments(ValueError):
    """Raised when multiple providers claim the same wrapper argument name."""


def inspect_function_parameters(function: Callable[..., Any]) -> tuple[str, ...]:
    """Return ordered callable parameter names for wrapper resolution."""

    names: list[str] = []
    signature = inspect.signature(function)
    for parameter in signature.parameters.values():
        if parameter.kind not in (
            inspect.Parameter.POSITIONAL_OR_KEYWORD,
            inspect.Parameter.KEYWORD_ONLY,
        ):
            raise TypeError(
                "wrapper_for requires named parameters only; "
                "positional-only, *args, and **kwargs are not supported"
            )
        names.append(parameter.name)
    return tuple(names)


def resolve_wrapper_parameters(
    function: Callable[..., Any],
    providers: Sequence[PropertyProvider],
) -> tuple[ResolvedWrapperParameter, ...]:
    """Resolve callable parameter names against ordered providers."""

    parameter_names = inspect_function_parameters(function)
    resolved: list[ResolvedWrapperParameter] = []
    unresolved_names: list[str] = []

    for parameter_name in parameter_names:
        for provider in providers:
            spec = provider.find(parameter_name)
            if spec is None:
                continue
            resolved.append(
                ResolvedWrapperParameter(
                    parameter_name=parameter_name,
                    provider=provider,
                    spec=spec,
                )
            )
            break
        else:
            unresolved_names.append(parameter_name)

    if unresolved_names:
        provider_names = tuple(provider.provider_name for provider in providers)
        raise UnresolvedWrapperForParameters(
            "Unable to resolve parameters for provided function - "
            f"missing names {tuple(unresolved_names)!r} from providers {provider_names!r}"
        )

    return tuple(resolved)


def generate_wrapper_factory(
    providers: Sequence[PropertyProvider],
    resolved_parameters: Sequence[ResolvedWrapperParameter],
) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
    """Build and return the generated ``generate(function) -> wrapper`` factory."""

    _validate_provider_arg_names(providers)

    astichi = _import_astichi()
    builder = astichi.build()
    builder.add.Root(_piece(_ROOT_SRC))

    for order, provider in enumerate(providers):
        builder.add.ProviderParam[order](
            _piece(_PROVIDER_PARAM_SRC),
            keep_names=[provider.arg_name],
        )
        builder.Root.wrapper_params.add.ProviderParam[order](
            order=order,
            arg_names={"provider_arg": provider.arg_name},
        )

    func_arg_piece = _piece(_FUNCTION_ARG_SRC)
    for order, resolved in enumerate(resolved_parameters):
        accessor = resolved.provider.accessor_for(resolved.spec)
        if accessor.reference_segments is not None:
            builder.add.FunctionArg[order](
                _piece(_function_ref_segments_arg_src(len(accessor.reference_segments))),
                keep_names=[accessor.reference_segments[0]],
            )
            segment_bindings = {
                f"segment_{index}": segment
                for index, segment in enumerate(accessor.reference_segments)
            }
            builder.Root.function_params.add.FunctionArg[order](
                order=order,
                arg_names={"param_name": resolved.parameter_name},
                bind={**segment_bindings, **dict(accessor.bind)},
            )
            continue
        builder.add.FunctionArg[order](func_arg_piece)
        builder.add.Accessor[order](accessor.composable)
        builder.FunctionArg[order].value_expr.add.Accessor[order](
            order=0,
            arg_names=accessor.arg_names,
            bind=accessor.bind,
        )
        builder.Root.function_params.add.FunctionArg[order](
            order=order,
            arg_names={"param_name": resolved.parameter_name},
        )

    materialized = builder.build().materialize()
    source = materialized.emit(provenance=False)
    namespace: dict[str, object] = {}
    exec(compile(source, "<yidl.codegen.wrapper>", "exec"), namespace)
    generate = namespace["generate"]
    if not callable(generate):
        raise TypeError("generated wrapper factory is not callable")
    return generate


def wrapper_for(
    function: Callable[..., Any],
    providers: Sequence[PropertyProvider],
) -> Callable[..., Any]:
    """Return a generated wrapper whose args are the provider arg names."""

    resolved_parameters = resolve_wrapper_parameters(function, providers)
    generate = generate_wrapper_factory(providers, resolved_parameters)
    return generate(function)


def _validate_provider_arg_names(providers: Sequence[PropertyProvider]) -> None:
    seen: dict[str, str] = {}
    duplicates: list[str] = []
    for provider in providers:
        previous = seen.get(provider.arg_name)
        if previous is None:
            seen[provider.arg_name] = provider.provider_name
            continue
        duplicates.append(provider.arg_name)
    if duplicates:
        raise DuplicateWrapperProviderArguments(
            "duplicate provider arg_name values are not allowed: "
            f"{tuple(duplicates)!r}"
        )


def _import_astichi() -> Any:
    import astichi

    return astichi


def _piece(src: str) -> Composable:
    return _import_astichi().compile(textwrap.dedent(src).strip() + "\n")


def _function_ref_segments_arg_src(segment_count: int) -> str:
    if segment_count <= 0:
        raise ValueError("segment_count must be positive")
    expr = "astichi_ref(external=segment_0)"
    for index in range(1, segment_count):
        expr += f".astichi_ref(external=segment_{index})"
    return (
        "astichi_funcargs(\n"
        f"    param_name__astichi_arg__={expr},\n"
        ")\n"
    )


_ROOT_SRC = """
def generate(function):
    def wrapper(wrapper_params__astichi_param_hole__):
        return function(astichi_hole(function_params))
    return wrapper
"""


_PROVIDER_PARAM_SRC = """
def astichi_params(provider_arg__astichi_arg__):
    pass
"""


_FUNCTION_ARG_SRC = """
astichi_funcargs(
    param_name__astichi_arg__=astichi_hole(value_expr),
)
"""
