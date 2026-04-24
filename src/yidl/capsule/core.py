"""Core YIDL capsule model and fluent builder."""

from __future__ import annotations

from dataclasses import dataclass, field
import re
from typing import Any


class UnspecifiedType:
    """Singleton sentinel for omitted capsule defaults."""

    __slots__ = ()
    _instance: UnspecifiedType | None = None

    def __new__(cls) -> UnspecifiedType:
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __repr__(self) -> str:
        return "UNSPECIFIED"


UNSPECIFIED = UnspecifiedType()


@dataclass(frozen=True, slots=True)
class CapsuleFacade:
    name: str
    default: bool = False


@dataclass(frozen=True, slots=True)
class CapsuleProperty:
    name: str
    property_name: str
    value_type: Any
    default: Any = UNSPECIFIED


@dataclass(frozen=True, slots=True)
class CapsuleSpec:
    name: str
    property_names: tuple[str, ...] = ()


@dataclass(frozen=True, slots=True)
class CapsuleMethodSurface:
    name: str


@dataclass(frozen=True, slots=True)
class CapsuleMethod:
    facade_name: str
    name: str
    surfaces: tuple[CapsuleMethodSurface, ...] = ()


@dataclass(frozen=True, slots=True)
class CapsuleSpecValue:
    property_name: str
    value: Any


@dataclass(frozen=True, slots=True)
class CapsuleSpecInstance:
    spec_name: str
    values: tuple[CapsuleSpecValue, ...] = ()

    @classmethod
    def from_values(cls, spec_name: str, **values: Any) -> CapsuleSpecInstance:
        return cls(
            spec_name=spec_name,
            values=tuple(
                CapsuleSpecValue(property_name=name, value=value)
                for name, value in values.items()
            ),
        )

    def get(self, property_name: str, default: Any = UNSPECIFIED) -> Any:
        for value in self.values:
            if value.property_name == property_name:
                return value.value
        return default


@dataclass(frozen=True, slots=True)
class YidlCapsule:
    facades: tuple[CapsuleFacade, ...] = ()
    properties: tuple[CapsuleProperty, ...] = ()
    specs: tuple[CapsuleSpec, ...] = ()
    methods: tuple[CapsuleMethod, ...] = ()

    @classmethod
    def null(cls) -> YidlCapsule:
        return cls()

    def compose(self, other: YidlCapsule) -> YidlCapsule:
        return YidlCapsule(
            facades=_merge_named(self.facades, other.facades, key=lambda facade: facade.name),
            properties=_merge_named(
                self.properties,
                other.properties,
                key=lambda prop: prop.name,
            ),
            specs=_merge_specs(self.specs, other.specs),
            methods=_merge_methods(self.methods, other.methods),
        )


@dataclass(slots=True)
class _FacadeAdder:
    _builder: CapsuleBuilder

    def __getattr__(self, name: str) -> _NamedFacadeAdder:
        return _NamedFacadeAdder(self._builder, name)


@dataclass(slots=True)
class _NamedFacadeAdder:
    _builder: CapsuleBuilder
    _name: str

    def __call__(self, *, default: bool = False) -> None:
        self._builder._add_facade(self._name, default=default)


@dataclass(slots=True)
class _PropertyAdder:
    _builder: CapsuleBuilder

    def __getattr__(self, name: str) -> _NamedPropertyAdder:
        return _NamedPropertyAdder(self._builder, name)


@dataclass(slots=True)
class _NamedPropertyAdder:
    _builder: CapsuleBuilder
    _name: str

    def __call__(
        self,
        value_type: Any,
        *,
        default: Any = UNSPECIFIED,
        property_name: str | None = None,
    ) -> None:
        self._builder._add_property(
            self._name,
            value_type,
            default=default,
            property_name=property_name,
        )


@dataclass(slots=True)
class _SpecAdder:
    _builder: CapsuleBuilder

    def __getattr__(self, name: str) -> _SpecChain:
        self._builder._ensure_spec(name)
        return _SpecChain(self._builder, name)


@dataclass(slots=True)
class _SpecChain:
    _builder: CapsuleBuilder
    _spec_name: str

    def __getattr__(self, property_name: str) -> _SpecChain:
        self._builder._add_spec_property(self._spec_name, property_name)
        return self


@dataclass(slots=True)
class _FacadeBuilderNamespace:
    add: _FacadeAdder


@dataclass(slots=True)
class _PropertyBuilderNamespace:
    add: _PropertyAdder


@dataclass(slots=True)
class _SpecBuilderNamespace:
    add: _SpecAdder


@dataclass(slots=True)
class _MethodAdder:
    _builder: CapsuleBuilder

    def __getattr__(self, facade_name: str) -> _MethodFacadeAdder:
        return _MethodFacadeAdder(self._builder, facade_name)


@dataclass(slots=True)
class _MethodFacadeAdder:
    _builder: CapsuleBuilder
    _facade_name: str

    def named(self, method_name: str) -> _MethodSurfaceChain:
        self._builder._ensure_method(self._facade_name, method_name)
        return _MethodSurfaceChain(self._builder, self._facade_name, method_name)


@dataclass(slots=True)
class _MethodSurfaceChain:
    _builder: CapsuleBuilder
    _facade_name: str
    _method_name: str

    def __getattr__(self, surface_name: str) -> _MethodSurfaceChain:
        self._builder._add_method_surface(self._facade_name, self._method_name, surface_name)
        return self


@dataclass(slots=True)
class _MethodBuilderNamespace:
    add: _MethodAdder


@dataclass(slots=True)
class CapsuleBuilder:
    _facades: dict[str, CapsuleFacade] = field(default_factory=dict)
    _properties: dict[str, CapsuleProperty] = field(default_factory=dict)
    _specs: dict[str, list[str]] = field(default_factory=dict)
    _methods: dict[tuple[str, str], list[str]] = field(default_factory=dict)
    facade: _FacadeBuilderNamespace = field(init=False)
    property: _PropertyBuilderNamespace = field(init=False)
    spec: _SpecBuilderNamespace = field(init=False)
    method: _MethodBuilderNamespace = field(init=False)

    def __post_init__(self) -> None:
        self.facade = _FacadeBuilderNamespace(_FacadeAdder(self))
        self.property = _PropertyBuilderNamespace(_PropertyAdder(self))
        self.spec = _SpecBuilderNamespace(_SpecAdder(self))
        self.method = _MethodBuilderNamespace(_MethodAdder(self))

    @classmethod
    def from_capsule(cls, capsule: YidlCapsule) -> CapsuleBuilder:
        builder = cls()
        builder._facades = {facade.name: facade for facade in capsule.facades}
        builder._properties = {prop.name: prop for prop in capsule.properties}
        builder._specs = {
            spec.name: list(spec.property_names)
            for spec in capsule.specs
        }
        builder._methods = {
            (method.facade_name, method.name): [surface.name for surface in method.surfaces]
            for method in capsule.methods
        }
        return builder

    def _add_facade(self, name: str, *, default: bool) -> None:
        self._facades[name] = CapsuleFacade(name=name, default=default)

    def _add_property(
        self,
        name: str,
        value_type: Any,
        *,
        default: Any,
        property_name: str | None,
    ) -> None:
        resolved_property_name = (
            _to_snake_case(name) if property_name is None else property_name
        )
        existing = next(
            (
                prop
                for prop in self._properties.values()
                if prop.property_name == resolved_property_name and prop.name != name
            ),
            None,
        )
        if existing is not None:
            raise ValueError(
                f"property_name {resolved_property_name!r} already used by "
                f"{existing.name!r}",
            )
        self._properties[name] = CapsuleProperty(
            name=name,
            property_name=resolved_property_name,
            value_type=value_type,
            default=default,
        )

    def _ensure_spec(self, name: str) -> None:
        self._specs.setdefault(name, [])

    def _add_spec_property(self, spec_name: str, property_name: str) -> None:
        if property_name not in self._properties:
            raise ValueError(f"unknown property {property_name!r} for spec {spec_name!r}")
        names = self._specs.setdefault(spec_name, [])
        if property_name not in names:
            names.append(property_name)

    def _ensure_method(self, facade_name: str, method_name: str) -> None:
        self._methods.setdefault((facade_name, method_name), [])

    def _add_method_surface(self, facade_name: str, method_name: str, surface_name: str) -> None:
        surfaces = self._methods.setdefault((facade_name, method_name), [])
        if surface_name not in surfaces:
            surfaces.append(surface_name)

    def build(self) -> YidlCapsule:
        return YidlCapsule(
            facades=tuple(self._facades.values()),
            properties=tuple(self._properties.values()),
            specs=tuple(
                CapsuleSpec(name=name, property_names=tuple(property_names))
                for name, property_names in self._specs.items()
            ),
            methods=tuple(
                CapsuleMethod(
                    facade_name=facade_name,
                    name=method_name,
                    surfaces=tuple(CapsuleMethodSurface(name=surface_name) for surface_name in surface_names),
                )
                for (facade_name, method_name), surface_names in self._methods.items()
            ),
        )


def build() -> CapsuleBuilder:
    return CapsuleBuilder()


def build_from(capsule: YidlCapsule) -> CapsuleBuilder:
    return CapsuleBuilder.from_capsule(capsule)


def _to_snake_case(name: str) -> str:
    return re.sub(r"(?<!^)(?=[A-Z])", "_", name).lower()


def _merge_named[T](
    left: tuple[T, ...],
    right: tuple[T, ...],
    *,
    key: Any,
) -> tuple[T, ...]:
    merged: dict[Any, T] = {}
    order: list[Any] = []
    for item in left + right:
        item_key = key(item)
        existing = merged.get(item_key)
        if existing is None:
            merged[item_key] = item
            order.append(item_key)
            continue
        if existing != item:
            raise ValueError(f"incompatible capsule merge for {item_key!r}")
    return tuple(merged[item_key] for item_key in order)


def _merge_specs(left: tuple[CapsuleSpec, ...], right: tuple[CapsuleSpec, ...]) -> tuple[CapsuleSpec, ...]:
    merged: dict[str, list[str]] = {}
    order: list[str] = []
    for spec in left + right:
        if spec.name not in merged:
            merged[spec.name] = list(spec.property_names)
            order.append(spec.name)
            continue
        names = merged[spec.name]
        for property_name in spec.property_names:
            if property_name not in names:
                names.append(property_name)
    return tuple(
        CapsuleSpec(name=name, property_names=tuple(property_names))
        for name, property_names in ((name, merged[name]) for name in order)
    )


def _merge_methods(
    left: tuple[CapsuleMethod, ...],
    right: tuple[CapsuleMethod, ...],
) -> tuple[CapsuleMethod, ...]:
    merged: dict[tuple[str, str], list[str]] = {}
    order: list[tuple[str, str]] = []
    for method in left + right:
        method_key = (method.facade_name, method.name)
        if method_key not in merged:
            merged[method_key] = [surface.name for surface in method.surfaces]
            order.append(method_key)
            continue
        surface_names = merged[method_key]
        for surface in method.surfaces:
            if surface.name not in surface_names:
                surface_names.append(surface.name)
    return tuple(
        CapsuleMethod(
            facade_name=facade_name,
            name=method_name,
            surfaces=tuple(CapsuleMethodSurface(name=surface_name) for surface_name in merged[(facade_name, method_name)]),
        )
        for facade_name, method_name in order
    )


__all__ = [
    "CapsuleBuilder",
    "CapsuleFacade",
    "CapsuleMethod",
    "CapsuleMethodSurface",
    "CapsuleProperty",
    "CapsuleSpec",
    "CapsuleSpecInstance",
    "CapsuleSpecValue",
    "UNSPECIFIED",
    "UnspecifiedType",
    "YidlCapsule",
    "build",
    "build_from",
]
