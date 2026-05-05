"""Recorded capsule concept builder.

This module is the first slice of the recorded capsule authoring API.  It only
records property definitions and dependency references; later slices will add
records, collections, ports, matchers, and productions.
"""

from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass
import itertools
import re
from typing import Final

from yidl.generation.data_def_sys import DataDefinitionSystem
from yidl.generation.data_def_sys import REQUIRED


ValueTypeSpec = type[object] | tuple[type[object], ...]


class _DefaultOmitted:
    """Sentinel meaning a property default was not supplied."""

    __slots__ = ()

    def __repr__(self) -> str:
        return "DEFAULT_OMITTED"


_DEFAULT_OMITTED: Final = _DefaultOmitted()


_SCALAR_DEFAULT_TYPES: Final = (bool, int, str, float, complex)
_BUILDER_IDS = itertools.count(1)


@dataclass(frozen=True, slots=True)
class PropertyHandle:
    """Symbolic handle for a property defined by a concept plan."""

    owner_id: int
    owner_name: str
    name: str
    value_type: ValueTypeSpec
    default: object
    storage_name: str
    sequence: int


@dataclass(frozen=True, slots=True)
class CapsuleConceptPlan:
    """Immutable recorded capsule concept plan."""

    name: str
    owner_id: int
    dependencies: tuple[CapsuleConceptPlan, ...]
    properties: tuple[PropertyHandle, ...]

    @property
    def props(self) -> PlanPropertyReferences:
        return PlanPropertyReferences(self)

    def apply(self, dds: DataDefinitionSystem) -> None:
        context = ReplayContext(dds)
        context.apply_plan(self)


class CapsuleConceptBuilder:
    """Mutable builder that records capsule concept operations."""

    __slots__ = (
        "_built",
        "_dependencies",
        "_owner_id",
        "_properties",
        "_property_order",
        "name",
        "props",
    )

    def __init__(
        self,
        name: str,
        *,
        requires: Iterable[CapsuleConceptPlan] = (),
    ) -> None:
        _require_label(name, "concept name")
        self.name = name
        self._owner_id = next(_BUILDER_IDS)
        self._dependencies = tuple(requires)
        for dependency in self._dependencies:
            if not isinstance(dependency, CapsuleConceptPlan):
                raise TypeError("concept dependencies must be CapsuleConceptPlan")
        self._properties: dict[str, PropertyHandle] = {}
        self._property_order: list[PropertyHandle] = []
        self._built = False
        self.props = BuilderPropertyDefinitions(self)

    def build(self) -> CapsuleConceptPlan:
        self._built = True
        return CapsuleConceptPlan(
            name=self.name,
            owner_id=self._owner_id,
            dependencies=self._dependencies,
            properties=tuple(self._property_order),
        )

    def apply(self, dds: DataDefinitionSystem) -> None:
        raise TypeError("build the capsule concept before replaying it")

    def use(self, plan: CapsuleConceptPlan) -> PlanReferenceNamespace:
        if not isinstance(plan, CapsuleConceptPlan):
            raise TypeError("builder.use(...) requires a CapsuleConceptPlan")
        if plan not in _dependency_closure(self._dependencies):
            raise ValueError(
                f"concept {plan.name!r} is not in the dependency closure for "
                f"{self.name!r}"
            )
        return PlanReferenceNamespace(plan)

    def _define_property(
        self,
        name: str,
        value_type: ValueTypeSpec,
        default: object,
        *,
        storage_name: str | None,
    ) -> PropertyHandle:
        if self._built:
            raise RuntimeError(f"concept {self.name!r} has already been built")
        _require_name(name, "property name")
        resolved_storage_name = (
            _to_snake_case(name) if storage_name is None else storage_name
        )
        _require_name(resolved_storage_name, "property storage name")
        if name in self._properties:
            raise ValueError(
                f"property {name!r} is already defined in concept {self.name!r}"
            )
        resolved_default = _resolve_default(value_type, default)
        handle = PropertyHandle(
            owner_id=self._owner_id,
            owner_name=self.name,
            name=name,
            value_type=value_type,
            default=resolved_default,
            storage_name=resolved_storage_name,
            sequence=len(self._property_order),
        )
        self._properties[name] = handle
        self._property_order.append(handle)
        return handle


class BuilderPropertyDefinitions:
    """Attribute surface for recording property definitions."""

    __slots__ = ("_builder",)

    def __init__(self, builder: CapsuleConceptBuilder) -> None:
        self._builder = builder

    def __getattr__(self, name: str) -> PropertyDefinition:
        _require_name(name, "property name")
        return PropertyDefinition(self._builder, name)


class PropertyDefinition:
    """Callable property-definition handle for one property name."""

    __slots__ = ("_builder", "_name")

    def __init__(self, builder: CapsuleConceptBuilder, name: str) -> None:
        self._builder = builder
        self._name = name

    def __call__(
        self,
        value_type: ValueTypeSpec,
        default: object = _DEFAULT_OMITTED,
        *,
        storage_name: str | None = None,
    ) -> PropertyHandle:
        return self._builder._define_property(
            self._name,
            value_type,
            default,
            storage_name=storage_name,
        )


class PlanReferenceNamespace:
    """Read-only namespace of handles exported by a concept plan."""

    __slots__ = ("_plan", "props")

    def __init__(self, plan: CapsuleConceptPlan) -> None:
        self._plan = plan
        self.props = PlanPropertyReferences(plan)


class PlanPropertyReferences:
    """Read-only property-handle namespace for one concept plan."""

    __slots__ = ("_by_name", "_plan")

    def __init__(self, plan: CapsuleConceptPlan) -> None:
        self._plan = plan
        self._by_name = {prop.name: prop for prop in plan.properties}

    def __getattr__(self, name: str) -> PropertyHandle:
        try:
            return self._by_name[name]
        except KeyError as exc:
            raise AttributeError(
                f"concept {self._plan.name!r} exports no property {name!r}"
            ) from exc


class ReplayContext:
    """Replay state for a single concept-plan application."""

    __slots__ = ("_applied_plan_ids", "_dds", "_property_owners")

    def __init__(self, dds: DataDefinitionSystem) -> None:
        self._dds = dds
        self._applied_plan_ids: set[int] = set()
        self._property_owners: dict[str, PropertyHandle] = {}

    def apply_plan(self, plan: CapsuleConceptPlan) -> None:
        if plan.owner_id in self._applied_plan_ids:
            return
        for dependency in plan.dependencies:
            self.apply_plan(dependency)
        for prop in plan.properties:
            self._apply_property(prop)
        self._applied_plan_ids.add(plan.owner_id)

    def _apply_property(self, prop: PropertyHandle) -> None:
        existing = self._property_owners.get(prop.name)
        if existing is not None:
            raise ValueError(
                f"property {prop.name!r} is already owned by concept "
                f"{existing.owner_name!r}; concept {prop.owner_name!r} must "
                "reference it instead of redefining it"
            )
        self._dds.ensure_property(
            prop.name,
            prop.value_type,
            default=prop.default,
            storage_name=prop.storage_name,
        )
        self._property_owners[prop.name] = prop


def capsule_concept(
    name: str,
    *,
    requires: Iterable[CapsuleConceptPlan] = (),
) -> CapsuleConceptBuilder:
    """Create a recorded capsule concept builder."""

    return CapsuleConceptBuilder(name, requires=requires)


def _dependency_closure(
    plans: Iterable[CapsuleConceptPlan],
) -> tuple[CapsuleConceptPlan, ...]:
    seen: set[int] = set()
    ordered: list[CapsuleConceptPlan] = []

    def visit(plan: CapsuleConceptPlan) -> None:
        if plan.owner_id in seen:
            return
        seen.add(plan.owner_id)
        for dependency in plan.dependencies:
            visit(dependency)
        ordered.append(plan)

    for plan in plans:
        visit(plan)
    return tuple(ordered)


def _resolve_default(value_type: ValueTypeSpec, default: object) -> object:
    if default is not _DEFAULT_OMITTED:
        return default
    if isinstance(value_type, type) and value_type in _SCALAR_DEFAULT_TYPES:
        return value_type()
    return REQUIRED


def _require_name(value: str, label: str) -> None:
    if not isinstance(value, str) or not value.isidentifier():
        raise ValueError(f"{label} must be a valid identifier: {value!r}")


def _require_label(value: str, label: str) -> None:
    if not isinstance(value, str) or not value:
        raise ValueError(f"{label} must be a non-empty string")


def _to_snake_case(name: str) -> str:
    return re.sub(r"(?<!^)(?=[A-Z])", "_", name).lower()


__all__ = [
    "CapsuleConceptBuilder",
    "CapsuleConceptPlan",
    "PropertyHandle",
    "capsule_concept",
]
