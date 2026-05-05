"""Recorded capsule concept builder.

This module contains the first recorded capsule authoring surface. It records
schema operations and replays them into the existing DDS implementation.
"""

from __future__ import annotations

from abc import ABC
from abc import abstractmethod
from collections.abc import Iterable
from collections.abc import Sequence
from dataclasses import dataclass
import itertools
import re
from typing import Final
from typing import Generic
from typing import TypeVar

from yidl.generation.data_def_sys import CollectionCardinality
from yidl.generation.data_def_sys import CollectionSpec
from yidl.generation.data_def_sys import ComputedCollectionSpec
from yidl.generation.data_def_sys import DataDefinitionSystem
from yidl.generation.data_def_sys import PortSpec
from yidl.generation.data_def_sys import PropertyEquals
from yidl.generation.data_def_sys import PropertySpec
from yidl.generation.data_def_sys import REQUIRED
from yidl.generation.data_def_sys import RecordSpec


ValueTypeSpec = type[object] | tuple[type[object], ...]
HandleKey = tuple[int, int]
NamedHandle = TypeVar(
    "NamedHandle",
    "PropertyHandle",
    "RecordHandle",
    "CollectionHandle",
    "ComputedCollectionHandle",
)


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

    def eq(self, value: object) -> PropertyEqualsHandle:
        _validate_property_value(self, value)
        return PropertyEqualsHandle(self, value)


@dataclass(frozen=True, slots=True)
class PropertyEqualsHandle:
    """Symbolic property equality condition."""

    property: PropertyHandle
    value: object


@dataclass(frozen=True, slots=True)
class RecordHandle:
    """Symbolic handle for a record defined by a concept plan."""

    owner_id: int
    owner_name: str
    name: str
    properties: tuple[PropertyHandle, ...]
    sequence: int


@dataclass(frozen=True, slots=True)
class RecordExtensionOperation:
    """Recorded record-extension operation."""

    record: RecordHandle
    properties: tuple[PropertyHandle, ...]
    sequence: int


class RecordedCollectionCardinality(ABC):
    """Recorded collection cardinality behavior."""

    __slots__ = ()

    @abstractmethod
    def resolve(self, dds: DataDefinitionSystem) -> CollectionCardinality:
        """Resolve this recorded cardinality for a concrete DDS."""


class RecordedSingleCardinality(RecordedCollectionCardinality):
    """Recorded single-cardinality behavior."""

    __slots__ = ()

    def resolve(self, dds: DataDefinitionSystem) -> CollectionCardinality:
        return dds.single


class RecordedManyCardinality(RecordedCollectionCardinality):
    """Recorded many-cardinality behavior."""

    __slots__ = ()

    def resolve(self, dds: DataDefinitionSystem) -> CollectionCardinality:
        return dds.many


@dataclass(frozen=True, slots=True)
class CollectionHandle:
    """Symbolic handle for a collection defined by a concept plan."""

    owner_id: int
    owner_name: str
    name: str
    record: RecordHandle
    cardinality: RecordedCollectionCardinality
    identity: PropertyHandle | None
    sequence: int


@dataclass(frozen=True, slots=True)
class ComputedCollectionHandle:
    """Symbolic handle for a computed collection defined by a concept plan."""

    owner_id: int
    owner_name: str
    name: str
    source: CollectionHandle | ComputedCollectionHandle
    conditions: tuple[PropertyEqualsHandle, ...]
    sequence: int


@dataclass(frozen=True, slots=True)
class PortHandle:
    """Symbolic handle for a port defined by a concept plan."""

    owner_id: int
    owner_name: str
    name: str
    cardinality: RecordedCollectionCardinality
    sequence: int


@dataclass(frozen=True, slots=True)
class PortIndexOperation:
    """Recorded port-index operation."""

    target: PropertyHandle
    order: PropertyHandle


@dataclass(frozen=True, slots=True)
class CapsuleConceptPlan:
    """Immutable recorded capsule concept plan."""

    name: str
    owner_id: int
    dependencies: tuple[CapsuleConceptPlan, ...]
    properties: tuple[PropertyHandle, ...]
    record_definitions: tuple[RecordHandle, ...]
    record_extensions: tuple[RecordExtensionOperation, ...]
    collection_definitions: tuple[CollectionHandle, ...]
    computed_collection_definitions: tuple[ComputedCollectionHandle, ...]
    port_definitions: tuple[PortHandle, ...]
    port_index_definition: PortIndexOperation | None

    @property
    def props(self) -> PlanHandleReferences[PropertyHandle]:
        return PlanHandleReferences(self, "property", self.properties)

    @property
    def records(self) -> PlanHandleReferences[RecordHandle]:
        return PlanHandleReferences(self, "record", self.record_definitions)

    @property
    def collections(self) -> PlanHandleReferences[CollectionHandle]:
        return PlanHandleReferences(
            self,
            "collection",
            self.collection_definitions,
        )

    @property
    def computed(self) -> PlanHandleReferences[ComputedCollectionHandle]:
        return PlanHandleReferences(
            self,
            "computed collection",
            self.computed_collection_definitions,
        )

    @property
    def ports(self) -> PlanPortReferences:
        return PlanPortReferences(self)

    def apply(self, dds: DataDefinitionSystem) -> None:
        context = ReplayContext(dds)
        context.apply_plan(self)


class CapsuleConceptBuilder:
    """Mutable builder that records capsule concept operations."""

    __slots__ = (
        "_built",
        "_collection_order",
        "_collections",
        "_computed_collection_order",
        "_computed_collections",
        "_dependencies",
        "_owner_id",
        "_port_index",
        "_port_order",
        "_ports",
        "_properties",
        "_property_order",
        "_record_extensions",
        "_record_order",
        "_records",
        "collections",
        "computed",
        "many",
        "name",
        "ports",
        "props",
        "records",
        "single",
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
        self._records: dict[str, RecordHandle] = {}
        self._record_order: list[RecordHandle] = []
        self._record_extensions: list[RecordExtensionOperation] = []
        self._collections: dict[str, CollectionHandle] = {}
        self._collection_order: list[CollectionHandle] = []
        self._computed_collections: dict[str, ComputedCollectionHandle] = {}
        self._computed_collection_order: list[ComputedCollectionHandle] = []
        self._ports: dict[str, PortHandle] = {}
        self._port_order: list[PortHandle] = []
        self._port_index: PortIndexOperation | None = None
        self._built = False
        self.single = RecordedSingleCardinality()
        self.many = RecordedManyCardinality()
        self.props = BuilderPropertyDefinitions(self)
        self.records = BuilderRecordDefinitions(self)
        self.collections = BuilderCollectionDefinitions(self)
        self.computed = BuilderComputedCollectionDefinitions(self)
        self.ports = BuilderPortDefinitions(self)

    def build(self) -> CapsuleConceptPlan:
        self._built = True
        return CapsuleConceptPlan(
            name=self.name,
            owner_id=self._owner_id,
            dependencies=self._dependencies,
            properties=tuple(self._property_order),
            record_definitions=tuple(self._record_order),
            record_extensions=tuple(self._record_extensions),
            collection_definitions=tuple(self._collection_order),
            computed_collection_definitions=tuple(
                self._computed_collection_order
            ),
            port_definitions=tuple(self._port_order),
            port_index_definition=self._port_index,
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

    def extend_record(
        self,
        record: RecordHandle,
        *properties: PropertyHandle,
    ) -> None:
        self._require_unbuilt()
        if not isinstance(record, RecordHandle):
            raise TypeError("extend_record(...) requires a RecordHandle")
        self._record_extensions.append(
            RecordExtensionOperation(
                record=record,
                properties=_unique_property_handles(properties),
                sequence=len(self._record_extensions),
            )
        )

    def port_index(self, *, target: PropertyHandle, order: PropertyHandle) -> None:
        self._require_unbuilt()
        if not isinstance(target, PropertyHandle):
            raise TypeError("port_index target must be a PropertyHandle")
        if not isinstance(order, PropertyHandle):
            raise TypeError("port_index order must be a PropertyHandle")
        if self._port_index is not None:
            raise ValueError(f"concept {self.name!r} already defines a port index")
        self._port_index = PortIndexOperation(target=target, order=order)

    def _define_property(
        self,
        name: str,
        value_type: ValueTypeSpec,
        default: object,
        *,
        storage_name: str | None,
    ) -> PropertyHandle:
        self._require_unbuilt()
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

    def _define_record(
        self,
        name: str,
        properties: Sequence[PropertyHandle],
    ) -> RecordHandle:
        self._require_unbuilt()
        _require_name(name, "record name")
        if name in self._records:
            raise ValueError(
                f"record {name!r} is already defined in concept {self.name!r}"
            )
        handle = RecordHandle(
            owner_id=self._owner_id,
            owner_name=self.name,
            name=name,
            properties=_unique_property_handles(properties),
            sequence=len(self._record_order),
        )
        self._records[name] = handle
        self._record_order.append(handle)
        return handle

    def _define_collection(
        self,
        name: str,
        record: RecordHandle,
        *,
        cardinality: RecordedCollectionCardinality,
        identity: PropertyHandle | None,
    ) -> CollectionHandle:
        self._require_unbuilt()
        _require_name(name, "collection name")
        if not isinstance(record, RecordHandle):
            raise TypeError("collection record must be a RecordHandle")
        if not isinstance(cardinality, RecordedCollectionCardinality):
            raise TypeError(
                "collection cardinality must be builder.single or builder.many"
            )
        if identity is not None and not isinstance(identity, PropertyHandle):
            raise TypeError("collection identity must be a PropertyHandle")
        if name in self._collections or name in self._computed_collections:
            raise ValueError(
                f"collection {name!r} is already defined in concept {self.name!r}"
            )
        handle = CollectionHandle(
            owner_id=self._owner_id,
            owner_name=self.name,
            name=name,
            record=record,
            cardinality=cardinality,
            identity=identity,
            sequence=len(self._collection_order),
        )
        self._collections[name] = handle
        self._collection_order.append(handle)
        return handle

    def _define_computed_collection(
        self,
        name: str,
        *,
        source: CollectionHandle | ComputedCollectionHandle,
        conditions: Sequence[PropertyEqualsHandle],
    ) -> ComputedCollectionHandle:
        self._require_unbuilt()
        _require_name(name, "computed collection name")
        if not isinstance(source, CollectionHandle | ComputedCollectionHandle):
            raise TypeError("computed collection source must be a collection handle")
        resolved_conditions = tuple(conditions)
        for condition in resolved_conditions:
            if not isinstance(condition, PropertyEqualsHandle):
                raise TypeError(
                    "computed collection conditions must be property equality handles"
                )
        if name in self._collections or name in self._computed_collections:
            raise ValueError(
                f"collection {name!r} is already defined in concept {self.name!r}"
            )
        handle = ComputedCollectionHandle(
            owner_id=self._owner_id,
            owner_name=self.name,
            name=name,
            source=source,
            conditions=resolved_conditions,
            sequence=len(self._computed_collection_order),
        )
        self._computed_collections[name] = handle
        self._computed_collection_order.append(handle)
        return handle

    def _define_port(
        self,
        name: str,
        *,
        cardinality: RecordedCollectionCardinality,
    ) -> PortHandle:
        self._require_unbuilt()
        _require_label(name, "port name")
        if not isinstance(cardinality, RecordedCollectionCardinality):
            raise TypeError("port cardinality must be builder.single or builder.many")
        if name in self._ports:
            raise ValueError(
                f"port {name!r} is already defined in concept {self.name!r}"
            )
        handle = PortHandle(
            owner_id=self._owner_id,
            owner_name=self.name,
            name=name,
            cardinality=cardinality,
            sequence=len(self._port_order),
        )
        self._ports[name] = handle
        self._port_order.append(handle)
        return handle

    def _require_unbuilt(self) -> None:
        if self._built:
            raise RuntimeError(f"concept {self.name!r} has already been built")


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


class BuilderRecordDefinitions:
    """Attribute surface for recording record definitions."""

    __slots__ = ("_builder",)

    def __init__(self, builder: CapsuleConceptBuilder) -> None:
        self._builder = builder

    def __getattr__(self, name: str) -> RecordDefinition:
        _require_name(name, "record name")
        return RecordDefinition(self._builder, name)


class RecordDefinition:
    """Callable record-definition handle for one record name."""

    __slots__ = ("_builder", "_name")

    def __init__(self, builder: CapsuleConceptBuilder, name: str) -> None:
        self._builder = builder
        self._name = name

    def __call__(self, *properties: PropertyHandle) -> RecordHandle:
        return self._builder._define_record(self._name, properties)


class BuilderCollectionDefinitions:
    """Attribute surface for recording collection definitions."""

    __slots__ = ("_builder",)

    def __init__(self, builder: CapsuleConceptBuilder) -> None:
        self._builder = builder

    def __getattr__(self, name: str) -> CollectionDefinition:
        _require_name(name, "collection name")
        return CollectionDefinition(self._builder, name)


class CollectionDefinition:
    """Callable collection-definition handle for one collection name."""

    __slots__ = ("_builder", "_name")

    def __init__(self, builder: CapsuleConceptBuilder, name: str) -> None:
        self._builder = builder
        self._name = name

    def __call__(
        self,
        record: RecordHandle,
        *,
        cardinality: RecordedCollectionCardinality,
        identity: PropertyHandle | None = None,
    ) -> CollectionHandle:
        return self._builder._define_collection(
            self._name,
            record,
            cardinality=cardinality,
            identity=identity,
        )


class BuilderComputedCollectionDefinitions:
    """Attribute surface for recording computed collection definitions."""

    __slots__ = ("_builder",)

    def __init__(self, builder: CapsuleConceptBuilder) -> None:
        self._builder = builder

    def __getattr__(self, name: str) -> ComputedCollectionDefinition:
        _require_name(name, "computed collection name")
        return ComputedCollectionDefinition(self._builder, name)


class ComputedCollectionDefinition:
    """Callable computed-collection definition for one collection name."""

    __slots__ = ("_builder", "_name")

    def __init__(self, builder: CapsuleConceptBuilder, name: str) -> None:
        self._builder = builder
        self._name = name

    def __call__(
        self,
        *,
        source: CollectionHandle | ComputedCollectionHandle,
        when: Sequence[PropertyEqualsHandle] = (),
    ) -> ComputedCollectionHandle:
        return self._builder._define_computed_collection(
            self._name,
            source=source,
            conditions=when,
        )


class BuilderPortDefinitions:
    """Attribute surface for recording dotted port paths."""

    __slots__ = ("_builder",)

    def __init__(self, builder: CapsuleConceptBuilder) -> None:
        self._builder = builder

    def __getattr__(self, name: str) -> PortPathDefinition:
        _require_name(name, "port path component")
        return PortPathDefinition(self._builder, (name,))


class PortPathDefinition:
    """Callable dotted-port definition path."""

    __slots__ = ("_builder", "_parts")

    def __init__(
        self,
        builder: CapsuleConceptBuilder,
        parts: tuple[str, ...],
    ) -> None:
        self._builder = builder
        self._parts = parts

    def __getattr__(self, name: str) -> PortPathDefinition:
        _require_name(name, "port path component")
        return PortPathDefinition(self._builder, (*self._parts, name))

    def __call__(self, *, cardinality: RecordedCollectionCardinality) -> PortHandle:
        return self._builder._define_port(
            ".".join(self._parts),
            cardinality=cardinality,
        )


class PlanReferenceNamespace:
    """Read-only namespace of handles exported by a concept plan."""

    __slots__ = ("collections", "computed", "ports", "props", "records")

    def __init__(self, plan: CapsuleConceptPlan) -> None:
        self.props = PlanHandleReferences(plan, "property", plan.properties)
        self.records = PlanHandleReferences(plan, "record", plan.record_definitions)
        self.collections = PlanHandleReferences(
            plan,
            "collection",
            plan.collection_definitions,
        )
        self.computed = PlanHandleReferences(
            plan,
            "computed collection",
            plan.computed_collection_definitions,
        )
        self.ports = PlanPortReferences(plan)


class PlanHandleReferences(Generic[NamedHandle]):
    """Read-only handle namespace for one concept plan and handle kind."""

    __slots__ = ("_by_name", "_kind", "_plan")

    def __init__(
        self,
        plan: CapsuleConceptPlan,
        kind: str,
        handles: Iterable[NamedHandle],
    ) -> None:
        self._plan = plan
        self._kind = kind
        self._by_name = {handle.name: handle for handle in handles}

    def __getattr__(self, name: str) -> NamedHandle:
        try:
            return self._by_name[name]
        except KeyError as exc:
            raise AttributeError(
                f"concept {self._plan.name!r} exports no {self._kind} {name!r}"
            ) from exc


class PlanPortReferences:
    """Read-only port-handle namespace for one concept plan."""

    __slots__ = ("_by_name", "_plan")

    def __init__(self, plan: CapsuleConceptPlan) -> None:
        self._plan = plan
        self._by_name = {port.name: port for port in plan.port_definitions}

    def __getattr__(self, name: str) -> PortHandle | PlanPortPathReferences:
        _require_name(name, "port path component")
        if name in self._by_name:
            return self._by_name[name]
        return PlanPortPathReferences(self._plan, self._by_name, (name,))


class PlanPortPathReferences:
    """Read-only dotted-port reference path."""

    __slots__ = ("_by_name", "_parts", "_plan")

    def __init__(
        self,
        plan: CapsuleConceptPlan,
        by_name: dict[str, PortHandle],
        parts: tuple[str, ...],
    ) -> None:
        self._plan = plan
        self._by_name = by_name
        self._parts = parts

    def __getattr__(self, name: str) -> PortHandle | PlanPortPathReferences:
        _require_name(name, "port path component")
        parts = (*self._parts, name)
        port_name = ".".join(parts)
        if port_name in self._by_name:
            return self._by_name[port_name]
        return PlanPortPathReferences(self._plan, self._by_name, parts)


class ReplayContext:
    """Replay state for a single concept-plan application."""

    __slots__ = (
        "_applied_plan_ids",
        "_collection_name_owners",
        "_collection_specs",
        "_computed_collection_specs",
        "_dds",
        "_port_index_owner",
        "_port_owners",
        "_port_specs",
        "_property_owners",
        "_property_specs",
        "_record_owners",
        "_record_specs",
    )

    def __init__(self, dds: DataDefinitionSystem) -> None:
        self._dds = dds
        self._applied_plan_ids: set[int] = set()
        self._property_owners: dict[str, PropertyHandle] = {}
        self._record_owners: dict[str, RecordHandle] = {}
        self._collection_name_owners: dict[
            str,
            CollectionHandle | ComputedCollectionHandle,
        ] = {}
        self._port_index_owner: PortIndexOperation | None = None
        self._port_owners: dict[str, PortHandle] = {}
        self._property_specs: dict[HandleKey, PropertySpec] = {}
        self._record_specs: dict[HandleKey, RecordSpec] = {}
        self._collection_specs: dict[HandleKey, CollectionSpec] = {}
        self._computed_collection_specs: dict[
            HandleKey,
            ComputedCollectionSpec,
        ] = {}
        self._port_specs: dict[HandleKey, PortSpec] = {}

    def apply_plan(self, plan: CapsuleConceptPlan) -> None:
        if plan.owner_id in self._applied_plan_ids:
            return
        for dependency in plan.dependencies:
            self.apply_plan(dependency)
        for prop in plan.properties:
            self._apply_property(prop)
        for record in plan.record_definitions:
            self._apply_record(record)
        for extension in plan.record_extensions:
            self._apply_record_extension(extension)
        for collection in plan.collection_definitions:
            self._apply_collection(collection)
        for collection in plan.computed_collection_definitions:
            self._apply_computed_collection(collection)
        for port in plan.port_definitions:
            self._apply_port(port)
        if plan.port_index_definition is not None:
            self._apply_port_index(plan.port_index_definition)
        self._applied_plan_ids.add(plan.owner_id)

    def _apply_property(self, prop: PropertyHandle) -> None:
        existing = self._property_owners.get(prop.name)
        if existing is not None:
            raise ValueError(
                f"property {prop.name!r} is already owned by concept "
                f"{existing.owner_name!r}; concept {prop.owner_name!r} must "
                "reference it instead of redefining it"
            )
        spec = self._dds.ensure_property(
            prop.name,
            prop.value_type,
            default=prop.default,
            storage_name=prop.storage_name,
        )
        self._property_owners[prop.name] = prop
        self._property_specs[_handle_key(prop)] = spec

    def _apply_record(self, record: RecordHandle) -> None:
        existing = self._record_owners.get(record.name)
        if existing is not None:
            raise ValueError(
                f"record {record.name!r} is already owned by concept "
                f"{existing.owner_name!r}; concept {record.owner_name!r} must "
                "reference it instead of redefining it"
            )
        spec = self._dds.ensure_record(
            record.name,
            *(self._resolve_property(prop) for prop in record.properties),
        )
        self._record_owners[record.name] = record
        self._record_specs[_handle_key(record)] = spec

    def _apply_record_extension(self, extension: RecordExtensionOperation) -> None:
        record = self._resolve_record(extension.record)
        record.extend_properties(
            *(self._resolve_property(prop) for prop in extension.properties)
        )

    def _apply_collection(self, collection: CollectionHandle) -> None:
        self._require_collection_name_available(collection)
        spec = self._dds.ensure_collection(
            collection.name,
            self._resolve_record(collection.record),
            cardinality=collection.cardinality.resolve(self._dds),
            identity=(
                None
                if collection.identity is None
                else self._resolve_property(collection.identity)
            ),
        )
        self._collection_name_owners[collection.name] = collection
        self._collection_specs[_handle_key(collection)] = spec

    def _apply_computed_collection(self, collection: ComputedCollectionHandle) -> None:
        self._require_collection_name_available(collection)
        spec = self._dds.ensure_computed_collection(
            collection.name,
            source=self._resolve_collection_source(collection.source),
            when=tuple(
                self._resolve_condition(condition)
                for condition in collection.conditions
            ),
        )
        self._collection_name_owners[collection.name] = collection
        self._computed_collection_specs[_handle_key(collection)] = spec

    def _apply_port(self, port: PortHandle) -> None:
        existing = self._port_owners.get(port.name)
        if existing is not None:
            raise ValueError(
                f"port {port.name!r} is already owned by concept "
                f"{existing.owner_name!r}; concept {port.owner_name!r} must "
                "reference it instead of redefining it"
            )
        spec = self._dds.ensure_port(
            port.name,
            cardinality=port.cardinality.resolve(self._dds),
        )
        self._port_owners[port.name] = port
        self._port_specs[_handle_key(port)] = spec

    def _apply_port_index(self, operation: PortIndexOperation) -> None:
        if self._port_index_owner is not None:
            raise ValueError("port index is already owned by another concept")
        self._dds.ensure_port_index(
            target=self._resolve_property(operation.target),
            order=self._resolve_property(operation.order),
        )
        self._port_index_owner = operation

    def _resolve_property(self, prop: PropertyHandle) -> PropertySpec:
        try:
            return self._property_specs[_handle_key(prop)]
        except KeyError as exc:
            raise ValueError(
                f"unresolved property handle {prop.name!r} from concept "
                f"{prop.owner_name!r}"
            ) from exc

    def _resolve_record(self, record: RecordHandle) -> RecordSpec:
        try:
            return self._record_specs[_handle_key(record)]
        except KeyError as exc:
            raise ValueError(
                f"unresolved record handle {record.name!r} from concept "
                f"{record.owner_name!r}"
            ) from exc

    def _resolve_collection_source(
        self,
        collection: CollectionHandle | ComputedCollectionHandle,
    ) -> CollectionSpec | ComputedCollectionSpec:
        if isinstance(collection, CollectionHandle):
            try:
                return self._collection_specs[_handle_key(collection)]
            except KeyError as exc:
                raise ValueError(
                    f"unresolved collection handle {collection.name!r} from "
                    f"concept {collection.owner_name!r}"
                ) from exc
        try:
            return self._computed_collection_specs[_handle_key(collection)]
        except KeyError as exc:
            raise ValueError(
                f"unresolved computed collection handle {collection.name!r} from "
                f"concept {collection.owner_name!r}"
            ) from exc

    def _resolve_condition(
        self,
        condition: PropertyEqualsHandle,
    ) -> PropertyEquals:
        return self._resolve_property(condition.property).eq(condition.value)

    def _require_collection_name_available(
        self,
        collection: CollectionHandle | ComputedCollectionHandle,
    ) -> None:
        existing = self._collection_name_owners.get(collection.name)
        if existing is not None:
            raise ValueError(
                f"collection {collection.name!r} is already owned by concept "
                f"{existing.owner_name!r}; concept {collection.owner_name!r} "
                "must reference it instead of redefining it"
            )


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


def _unique_property_handles(
    properties: Sequence[PropertyHandle],
) -> tuple[PropertyHandle, ...]:
    by_name: dict[str, PropertyHandle] = {}
    for prop in properties:
        if not isinstance(prop, PropertyHandle):
            raise TypeError("expected PropertyHandle")
        existing = by_name.get(prop.name)
        if existing is not None and existing != prop:
            raise ValueError(f"duplicate property handle {prop.name!r}")
        by_name[prop.name] = prop
    return tuple(by_name.values())


def _validate_property_value(prop: PropertyHandle, value: object) -> None:
    if prop.value_type is object:
        return
    if not isinstance(value, prop.value_type):
        if isinstance(prop.value_type, tuple):
            expected = " or ".join(item.__name__ for item in prop.value_type)
        else:
            expected = prop.value_type.__name__
        raise TypeError(
            f"{prop.name} must be {expected}, got {type(value).__name__}"
        )


def _handle_key(
    handle: PropertyHandle
    | RecordHandle
    | CollectionHandle
    | ComputedCollectionHandle
    | PortHandle,
) -> HandleKey:
    return (handle.owner_id, handle.sequence)


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
    "CollectionHandle",
    "ComputedCollectionHandle",
    "PortHandle",
    "PropertyHandle",
    "RecordHandle",
    "capsule_concept",
]
