"""Core YIDL capsule model and fluent builder."""

from __future__ import annotations

from dataclasses import dataclass, field
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
    value_type: Any
    default: Any = UNSPECIFIED


@dataclass(frozen=True, slots=True)
class CapsuleSpec:
    name: str
    property_names: tuple[str, ...] = ()


@dataclass(frozen=True, slots=True)
class YidlCapsule:
    facades: tuple[CapsuleFacade, ...] = ()
    properties: tuple[CapsuleProperty, ...] = ()
    specs: tuple[CapsuleSpec, ...] = ()


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

    def __call__(self, value_type: Any, *, default: Any = UNSPECIFIED) -> None:
        self._builder._add_property(self._name, value_type, default=default)


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
class CapsuleBuilder:
    _facades: dict[str, CapsuleFacade] = field(default_factory=dict)
    _properties: dict[str, CapsuleProperty] = field(default_factory=dict)
    _specs: dict[str, list[str]] = field(default_factory=dict)
    facade: _FacadeBuilderNamespace = field(init=False)
    property: _PropertyBuilderNamespace = field(init=False)
    spec: _SpecBuilderNamespace = field(init=False)

    def __post_init__(self) -> None:
        self.facade = _FacadeBuilderNamespace(_FacadeAdder(self))
        self.property = _PropertyBuilderNamespace(_PropertyAdder(self))
        self.spec = _SpecBuilderNamespace(_SpecAdder(self))

    def _add_facade(self, name: str, *, default: bool) -> None:
        self._facades[name] = CapsuleFacade(name=name, default=default)

    def _add_property(self, name: str, value_type: Any, *, default: Any) -> None:
        self._properties[name] = CapsuleProperty(
            name=name,
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

    def build(self) -> YidlCapsule:
        return YidlCapsule(
            facades=tuple(self._facades.values()),
            properties=tuple(self._properties.values()),
            specs=tuple(
                CapsuleSpec(name=name, property_names=tuple(property_names))
                for name, property_names in self._specs.items()
            ),
        )


def build() -> CapsuleBuilder:
    return CapsuleBuilder()


__all__ = [
    "CapsuleBuilder",
    "CapsuleFacade",
    "CapsuleProperty",
    "CapsuleSpec",
    "UNSPECIFIED",
    "UnspecifiedType",
    "YidlCapsule",
    "build",
]
