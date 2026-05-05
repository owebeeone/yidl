"""Recorded capsule concept builder.

This module contains the first recorded capsule authoring surface. It records
schema operations and replays them into the existing DDS implementation.
"""

from __future__ import annotations

from abc import ABC
from abc import abstractmethod
from collections.abc import Callable
from collections.abc import Iterable
from collections.abc import Mapping
from collections.abc import Sequence
from dataclasses import dataclass
import itertools
import re
from types import MappingProxyType
from typing import Any
from typing import Final
from typing import Generic
from typing import TypeVar

from yidl.generation.data_def_sys import CollectionCardinality
from yidl.generation.data_def_sys import CollectionSpec
from yidl.generation.data_def_sys import ComputedCollectionSpec
from yidl.generation.data_def_sys import DataDefinitionSystem
from yidl.generation.data_def_sys import MatcherCondition
from yidl.generation.data_def_sys import MatcherGeneratedValue
from yidl.generation.data_def_sys import MatcherInputSpec
from yidl.generation.data_def_sys import MatcherResultSource
from yidl.generation.data_def_sys import MatcherSpec
from yidl.generation.data_def_sys import PortSpec
from yidl.generation.data_def_sys import PropertyEquals
from yidl.generation.data_def_sys import PropertySpec
from yidl.generation.data_def_sys import REQUIRED
from yidl.generation.data_def_sys import RecordSpec
from yidl.generation.data_def_sys import match as dds_match
from yidl.generation.data_schema import ValueExpression


ValueTypeSpec = type[object] | tuple[type[object], ...]
HandleKey = tuple[int, int]
NamedHandle = TypeVar(
    "NamedHandle",
    "PropertyHandle",
    "RecordHandle",
    "CollectionHandle",
    "ComputedCollectionHandle",
    "MatcherHandle",
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

    def read(self) -> RecordedReadProperty:
        return RecordedReadProperty(self)


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

    def of(self, owner_identity: object) -> RecordedPortAddress:
        return RecordedPortAddress(self, owner_identity)


@dataclass(frozen=True, slots=True)
class RecordedPortAddress:
    """Symbolic owner-scoped port address."""

    port: PortHandle
    owner_identity: object


@dataclass(frozen=True, slots=True)
class PortIndexOperation:
    """Recorded port-index operation."""

    target: PropertyHandle
    order: PropertyHandle


@dataclass(frozen=True, slots=True)
class MatcherHandle:
    """Symbolic handle for a matcher defined by a concept plan."""

    owner_id: int
    owner_name: str
    name: str
    sequence: int


@dataclass(frozen=True, slots=True)
class MatcherInputHandle:
    """Symbolic handle for one matcher input."""

    owner_id: int
    owner_name: str
    matcher: MatcherHandle
    name: str
    source: CollectionHandle | ComputedCollectionHandle
    sequence: int

    def prop(self, property: PropertyHandle) -> MatcherScopedPropertyHandle:
        if not isinstance(property, PropertyHandle):
            raise TypeError("matcher input properties must be PropertyHandle")
        return MatcherScopedPropertyHandle(self, property)


@dataclass(frozen=True, slots=True)
class MatcherScopedPropertyHandle:
    """Symbolic matcher-input property reference."""

    input: MatcherInputHandle
    property: PropertyHandle

    def eq(self, value: object) -> MatcherConditionHandle:
        _validate_property_value(self.property, value)
        return MatcherConditionHandle(self, value)


@dataclass(frozen=True, slots=True)
class MatcherConditionHandle:
    """Symbolic matcher rule condition."""

    ref: MatcherScopedPropertyHandle
    value: object


@dataclass(frozen=True, slots=True)
class MatcherDefaultOperation:
    """Recorded matcher default resource."""

    matcher: MatcherHandle
    resource: MatcherGeneratedValue
    sequence: int


@dataclass(frozen=True, slots=True)
class MatcherRuleOperation:
    """Recorded matcher rule."""

    matcher: MatcherHandle
    name: str
    conditions: tuple[MatcherConditionHandle, ...]
    resource: MatcherGeneratedValue
    weight: float
    sequence: int


@dataclass(frozen=True, slots=True)
class MatcherResultSourceHandle:
    """Symbolic source over matcher results."""

    matcher: MatcherHandle


@dataclass(frozen=True, slots=True)
class RecordedMatchResource:
    """Symbolic value expression for a matcher-selected resource."""


@dataclass(frozen=True, slots=True)
class RecordedMatchTupleValue:
    """Symbolic value expression for one matcher tuple value."""

    index: int


@dataclass(frozen=True, slots=True)
class RecordedMatchRecordProperty:
    """Symbolic value expression for a property on a matcher input record."""

    input_name: str
    property: PropertyHandle


@dataclass(frozen=True, slots=True)
class RecordedReadProperty:
    """Symbolic source-record property read."""

    property: PropertyHandle


RecordedValueExpression = (
    RecordedMatchResource
    | RecordedMatchTupleValue
    | RecordedMatchRecordProperty
    | RecordedPortAddress
    | RecordedReadProperty
    | ValueExpression
    | object
)


@dataclass(frozen=True, slots=True)
class ProductionValueOperation:
    """Recorded target property assignment for a production."""

    property: PropertyHandle
    expression: RecordedValueExpression


@dataclass(frozen=True, slots=True)
class ProductionHandle:
    """Symbolic handle for a production defined by a concept plan."""

    owner_id: int
    owner_name: str
    name: str
    source: CollectionHandle | ComputedCollectionHandle | MatcherResultSourceHandle
    target: CollectionHandle
    conditions: tuple[PropertyEqualsHandle, ...]
    identity: RecordedValueExpression | None
    values: tuple[ProductionValueOperation, ...]
    policy: object
    sequence: int


@dataclass(frozen=True, slots=True)
class ProductionGroupOperation:
    """Recorded production-group membership."""

    name: str
    productions: tuple[ProductionHandle, ...]
    sequence: int


@dataclass(frozen=True, slots=True)
class RuntimeHelperOperation:
    """Runtime helper needed by generated container source."""

    name: str
    value: Callable[..., object]


@dataclass(frozen=True, slots=True)
class CapsuleRuntime:
    """Loaded generated DDS runtime for a capsule concept plan."""

    definition: object
    source: str
    namespace: Mapping[str, object]

    def __getitem__(self, name: str) -> object:
        return self.namespace[name]

    def get(self, name: str, default: Any = None) -> object:
        return self.namespace.get(name, default)

    def new_builder(self) -> object:
        builder_factory = self.namespace["new_builder"]
        if not callable(builder_factory):
            raise TypeError("generated runtime new_builder is not callable")
        return builder_factory()

    def build_container(self, builder: object) -> object:
        build_container = self.namespace["build_container"]
        if not callable(build_container):
            raise TypeError("generated runtime build_container is not callable")
        return build_container(builder)


@dataclass(frozen=True, slots=True)
class CapsuleConceptPlan:
    """Immutable recorded capsule concept plan."""

    name: str
    owner_id: int
    extensions: tuple[CapsuleConceptPlan, ...]
    properties: tuple[PropertyHandle, ...]
    record_definitions: tuple[RecordHandle, ...]
    record_extensions: tuple[RecordExtensionOperation, ...]
    collection_definitions: tuple[CollectionHandle, ...]
    computed_collection_definitions: tuple[ComputedCollectionHandle, ...]
    port_definitions: tuple[PortHandle, ...]
    port_index_definition: PortIndexOperation | None
    matcher_definitions: tuple[MatcherHandle, ...]
    matcher_inputs: tuple[MatcherInputHandle, ...]
    matcher_defaults: tuple[MatcherDefaultOperation, ...]
    matcher_rules: tuple[MatcherRuleOperation, ...]
    production_definitions: tuple[ProductionHandle, ...]
    production_groups: tuple[ProductionGroupOperation, ...]
    runtime_helpers: tuple[RuntimeHelperOperation, ...]

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

    @property
    def matchers(self) -> PlanHandleReferences[MatcherHandle]:
        return PlanHandleReferences(self, "matcher", self.matcher_definitions)

    def apply(self, dds: DataDefinitionSystem) -> None:
        context = ReplayContext(dds)
        context.apply_plan(self)

    def build_data_definition(self) -> DataDefinitionSystem:
        dds = DataDefinitionSystem()
        self.apply(dds)
        return dds

    def emit_runtime_source(self) -> str:
        return self.runtime().emit_source()

    def runtime(self) -> RecordedConceptRuntimeLoader:
        return RecordedConceptRuntimeLoader(self)


class CapsuleConceptBuilder:
    """Mutable builder that records capsule concept operations."""

    __slots__ = (
        "_built",
        "_collection_order",
        "_collections",
        "_computed_collection_order",
        "_computed_collections",
        "_extensions",
        "_matcher_defaults",
        "_matcher_inputs",
        "_matcher_order",
        "_matcher_rules",
        "_matchers",
        "_owner_id",
        "_port_index",
        "_port_order",
        "_ports",
        "_production_groups",
        "_production_order",
        "_productions",
        "_properties",
        "_property_order",
        "_record_extensions",
        "_record_order",
        "_records",
        "_runtime_helpers",
        "collections",
        "computed",
        "matchers",
        "many",
        "name",
        "ports",
        "productions",
        "props",
        "records",
        "runtime",
        "single",
    )

    def __init__(
        self,
        name: str,
        *,
        extends: Iterable[CapsuleConceptPlan] = (),
    ) -> None:
        _require_label(name, "concept name")
        self.name = name
        self._owner_id = next(_BUILDER_IDS)
        self._extensions = tuple(extends)
        for extension in self._extensions:
            if not isinstance(extension, CapsuleConceptPlan):
                raise TypeError("concept extensions must be CapsuleConceptPlan")
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
        self._matchers: dict[str, MatcherHandle] = {}
        self._matcher_order: list[MatcherHandle] = []
        self._matcher_inputs: list[MatcherInputHandle] = []
        self._matcher_defaults: list[MatcherDefaultOperation] = []
        self._matcher_rules: list[MatcherRuleOperation] = []
        self._productions: dict[str, ProductionHandle] = {}
        self._production_order: list[ProductionHandle] = []
        self._production_groups: list[ProductionGroupOperation] = []
        self._runtime_helpers: list[RuntimeHelperOperation] = []
        self._built = False
        self.single = RecordedSingleCardinality()
        self.many = RecordedManyCardinality()
        self.props = BuilderPropertyDefinitions(self)
        self.records = BuilderRecordDefinitions(self)
        self.collections = BuilderCollectionDefinitions(self)
        self.computed = BuilderComputedCollectionDefinitions(self)
        self.ports = BuilderPortDefinitions(self)
        self.matchers = BuilderMatcherDefinitions(self)
        self.productions = BuilderProductionDefinitions(self)
        self.runtime = BuilderRuntimeHelpers(self)

    def build(self) -> CapsuleConceptPlan:
        self._built = True
        return CapsuleConceptPlan(
            name=self.name,
            owner_id=self._owner_id,
            extensions=self._extensions,
            properties=tuple(self._property_order),
            record_definitions=tuple(self._record_order),
            record_extensions=tuple(self._record_extensions),
            collection_definitions=tuple(self._collection_order),
            computed_collection_definitions=tuple(
                self._computed_collection_order
            ),
            port_definitions=tuple(self._port_order),
            port_index_definition=self._port_index,
            matcher_definitions=tuple(self._matcher_order),
            matcher_inputs=tuple(self._matcher_inputs),
            matcher_defaults=tuple(self._matcher_defaults),
            matcher_rules=tuple(self._matcher_rules),
            production_definitions=tuple(self._production_order),
            production_groups=tuple(self._production_groups),
            runtime_helpers=tuple(self._runtime_helpers),
        )

    def apply(self, dds: DataDefinitionSystem) -> None:
        raise TypeError("build the capsule concept before replaying it")

    def use(self, plan: CapsuleConceptPlan) -> PlanReferenceNamespace:
        if not isinstance(plan, CapsuleConceptPlan):
            raise TypeError("builder.use(...) requires a CapsuleConceptPlan")
        if plan not in _extension_closure(self._extensions):
            raise ValueError(
                f"concept {plan.name!r} is not in the extension closure for "
                f"{self.name!r}"
            )
        return PlanReferenceNamespace(plan)

    def use_matcher(self, matcher: MatcherHandle) -> MatcherEditor:
        self._require_unbuilt()
        if not isinstance(matcher, MatcherHandle):
            raise TypeError("use_matcher(...) requires a MatcherHandle")
        if matcher.owner_id != self._owner_id and not _handle_owner_in_plans(
            matcher.owner_id,
            _extension_closure(self._extensions),
        ):
            raise ValueError(
                f"matcher {matcher.name!r} is not in the extension closure for "
                f"{self.name!r}"
            )
        return MatcherEditor(self, matcher)

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

    def _define_matcher(self, name: str) -> MatcherEditor:
        self._require_unbuilt()
        _require_name(name, "matcher name")
        if name in self._matchers:
            raise ValueError(
                f"matcher {name!r} is already defined in concept {self.name!r}"
            )
        handle = MatcherHandle(
            owner_id=self._owner_id,
            owner_name=self.name,
            name=name,
            sequence=len(self._matcher_order),
        )
        self._matchers[name] = handle
        self._matcher_order.append(handle)
        return MatcherEditor(self, handle)

    def _define_matcher_input(
        self,
        matcher: MatcherHandle,
        name: str,
        source: CollectionHandle | ComputedCollectionHandle,
    ) -> MatcherInputHandle:
        self._require_unbuilt()
        _require_name(name, "matcher input name")
        if not isinstance(source, CollectionHandle | ComputedCollectionHandle):
            raise TypeError("matcher input source must be a collection handle")
        handle = MatcherInputHandle(
            owner_id=self._owner_id,
            owner_name=self.name,
            matcher=matcher,
            name=name,
            source=source,
            sequence=len(self._matcher_inputs),
        )
        self._matcher_inputs.append(handle)
        return handle

    def _define_matcher_default(
        self,
        matcher: MatcherHandle,
        resource: MatcherGeneratedValue,
    ) -> None:
        self._require_unbuilt()
        if not isinstance(resource, MatcherGeneratedValue):
            raise TypeError("matcher default resource must be MatcherGeneratedValue")
        self._matcher_defaults.append(
            MatcherDefaultOperation(
                matcher=matcher,
                resource=resource,
                sequence=len(self._matcher_defaults),
            )
        )

    def _define_matcher_rule(
        self,
        matcher: MatcherHandle,
        name: str,
        *,
        conditions: Sequence[MatcherConditionHandle],
        resource: MatcherGeneratedValue,
        weight: float,
    ) -> None:
        self._require_unbuilt()
        _require_label(name, "matcher rule name")
        if not isinstance(resource, MatcherGeneratedValue):
            raise TypeError("matcher rule resource must be MatcherGeneratedValue")
        resolved_conditions = tuple(conditions)
        for condition in resolved_conditions:
            if not isinstance(condition, MatcherConditionHandle):
                raise TypeError("matcher rule conditions must be matcher conditions")
        self._matcher_rules.append(
            MatcherRuleOperation(
                matcher=matcher,
                name=name,
                conditions=resolved_conditions,
                resource=resource,
                weight=weight,
                sequence=len(self._matcher_rules),
            )
        )

    def _define_production(
        self,
        name: str,
        *,
        source: CollectionHandle | ComputedCollectionHandle | MatcherResultSourceHandle,
        target: CollectionHandle,
        conditions: Sequence[PropertyEqualsHandle],
        identity: RecordedValueExpression | None,
        values: dict[PropertyHandle, RecordedValueExpression],
        policy: object,
    ) -> ProductionEditor:
        self._require_unbuilt()
        _require_name(name, "production name")
        if not isinstance(
            source,
            CollectionHandle | ComputedCollectionHandle | MatcherResultSourceHandle,
        ):
            raise TypeError("production source must be a collection or matcher result")
        if not isinstance(target, CollectionHandle):
            raise TypeError("production target must be a collection handle")
        if name in self._productions:
            raise ValueError(
                f"production {name!r} is already defined in concept {self.name!r}"
            )
        resolved_conditions = tuple(conditions)
        for condition in resolved_conditions:
            if not isinstance(condition, PropertyEqualsHandle):
                raise TypeError("production conditions must be property equality handles")
        resolved_values = tuple(
            ProductionValueOperation(prop, expression)
            for prop, expression in values.items()
        )
        handle = ProductionHandle(
            owner_id=self._owner_id,
            owner_name=self.name,
            name=name,
            source=source,
            target=target,
            conditions=resolved_conditions,
            identity=identity,
            values=resolved_values,
            policy=policy,
            sequence=len(self._production_order),
        )
        self._productions[name] = handle
        self._production_order.append(handle)
        return ProductionEditor(self, handle)

    def _define_production_group(
        self,
        name: str,
        productions: Sequence[ProductionHandle],
    ) -> None:
        self._require_unbuilt()
        _require_name(name, "production group name")
        resolved_productions = tuple(productions)
        for production in resolved_productions:
            if not isinstance(production, ProductionHandle):
                raise TypeError("production group entries must be production handles")
        for index, group in enumerate(self._production_groups):
            if group.name != name:
                continue
            additions = tuple(
                production
                for production in resolved_productions
                if production not in group.productions
            )
            if not additions:
                return
            self._production_groups[index] = ProductionGroupOperation(
                name=name,
                productions=(*group.productions, *additions),
                sequence=group.sequence,
            )
            return
        self._production_groups.append(
            ProductionGroupOperation(
                name=name,
                productions=resolved_productions,
                sequence=len(self._production_groups),
            )
        )

    def _define_runtime_helper(
        self,
        value: Callable[..., object],
        *,
        name: str | None,
    ) -> None:
        self._require_unbuilt()
        if not callable(value):
            raise TypeError("runtime helper must be callable")
        resolved_name = _runtime_helper_name(value, name)
        self._runtime_helpers.append(
            RuntimeHelperOperation(name=resolved_name, value=value)
        )

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


class BuilderMatcherDefinitions:
    """Attribute surface for recording matcher definitions."""

    __slots__ = ("_builder",)

    def __init__(self, builder: CapsuleConceptBuilder) -> None:
        self._builder = builder

    def __getattr__(self, name: str) -> MatcherDefinition:
        _require_name(name, "matcher name")
        return MatcherDefinition(self._builder, name)


class MatcherDefinition:
    """Callable matcher-definition handle for one matcher name."""

    __slots__ = ("_builder", "_name")

    def __init__(self, builder: CapsuleConceptBuilder, name: str) -> None:
        self._builder = builder
        self._name = name

    def __call__(self) -> MatcherEditor:
        return self._builder._define_matcher(self._name)


class MatcherEditor:
    """Mutable editor for rules and inputs on a recorded matcher handle."""

    __slots__ = ("_builder", "_matcher", "input", "rule")

    def __init__(
        self,
        builder: CapsuleConceptBuilder,
        matcher: MatcherHandle,
    ) -> None:
        self._builder = builder
        self._matcher = matcher
        self.input = MatcherInputDefinitions(builder, matcher)
        self.rule = MatcherRuleDefinitions(builder, matcher)

    @property
    def handle(self) -> MatcherHandle:
        return self._matcher

    def default(self, resource: MatcherGeneratedValue) -> None:
        self._builder._define_matcher_default(self._matcher, resource)

    def results(self) -> MatcherResultSourceHandle:
        return MatcherResultSourceHandle(self._matcher)


class MatcherInputDefinitions:
    """Attribute surface for recording matcher inputs."""

    __slots__ = ("_builder", "_matcher")

    def __init__(
        self,
        builder: CapsuleConceptBuilder,
        matcher: MatcherHandle,
    ) -> None:
        self._builder = builder
        self._matcher = matcher

    def __getattr__(self, name: str) -> MatcherInputDefinition:
        _require_name(name, "matcher input name")
        return MatcherInputDefinition(self._builder, self._matcher, name)


class MatcherInputDefinition:
    """Callable matcher-input definition for one input name."""

    __slots__ = ("_builder", "_matcher", "_name")

    def __init__(
        self,
        builder: CapsuleConceptBuilder,
        matcher: MatcherHandle,
        name: str,
    ) -> None:
        self._builder = builder
        self._matcher = matcher
        self._name = name

    def __call__(
        self,
        source: CollectionHandle | ComputedCollectionHandle,
    ) -> MatcherInputHandle:
        return self._builder._define_matcher_input(
            self._matcher,
            self._name,
            source,
        )


class MatcherRuleDefinitions:
    """Attribute surface for recording named matcher rules."""

    __slots__ = ("_builder", "_matcher")

    def __init__(
        self,
        builder: CapsuleConceptBuilder,
        matcher: MatcherHandle,
    ) -> None:
        self._builder = builder
        self._matcher = matcher

    def __getattr__(self, name: str) -> MatcherRuleDefinition:
        _require_label(name, "matcher rule name")
        return MatcherRuleDefinition(self._builder, self._matcher, name)


class MatcherRuleDefinition:
    """Callable matcher-rule definition."""

    __slots__ = ("_builder", "_matcher", "_name")

    def __init__(
        self,
        builder: CapsuleConceptBuilder,
        matcher: MatcherHandle,
        name: str,
    ) -> None:
        self._builder = builder
        self._matcher = matcher
        self._name = name

    def __call__(
        self,
        *,
        when: Sequence[MatcherConditionHandle],
        resource: MatcherGeneratedValue,
        weight: float = 1.0,
    ) -> None:
        self._builder._define_matcher_rule(
            self._matcher,
            self._name.replace("_", "-"),
            conditions=when,
            resource=resource,
            weight=weight,
        )


class BuilderProductionDefinitions:
    """Attribute surface for recording production definitions."""

    __slots__ = ("_builder",)

    def __init__(self, builder: CapsuleConceptBuilder) -> None:
        self._builder = builder

    def __getattr__(self, name: str) -> ProductionDefinition:
        _require_name(name, "production name")
        return ProductionDefinition(self._builder, name)


class ProductionDefinition:
    """Callable production-definition handle for one production name."""

    __slots__ = ("_builder", "_name")

    def __init__(self, builder: CapsuleConceptBuilder, name: str) -> None:
        self._builder = builder
        self._name = name

    def __call__(
        self,
        *,
        source: CollectionHandle | ComputedCollectionHandle | MatcherResultSourceHandle,
        target: CollectionHandle,
        values: dict[PropertyHandle, RecordedValueExpression],
        policy: object,
        when: Sequence[PropertyEqualsHandle] = (),
        identity: RecordedValueExpression | None = None,
    ) -> ProductionEditor:
        return self._builder._define_production(
            self._name,
            source=source,
            target=target,
            conditions=when,
            identity=identity,
            values=values,
            policy=policy,
        )


class ProductionEditor:
    """Mutable editor for a recorded production handle."""

    __slots__ = ("_builder", "_production")

    def __init__(
        self,
        builder: CapsuleConceptBuilder,
        production: ProductionHandle,
    ) -> None:
        self._builder = builder
        self._production = production

    @property
    def handle(self) -> ProductionHandle:
        return self._production

    def in_group(self, name: str) -> None:
        self._builder._define_production_group(name, (self._production,))


class BuilderRuntimeHelpers:
    """Runtime helper declarations for a concept builder."""

    __slots__ = ("_builder",)

    def __init__(self, builder: CapsuleConceptBuilder) -> None:
        self._builder = builder

    def evaluator(
        self,
        value: Callable[..., object],
        *,
        name: str | None = None,
    ) -> None:
        self._builder._define_runtime_helper(value, name=name)


class RecordedMatchRecordAccessor:
    """Symbolic matcher input record accessor."""

    __slots__ = ("_input_name",)

    def __init__(self, input_name: str) -> None:
        _require_name(input_name, "matcher input name")
        self._input_name = input_name

    def prop(self, property: PropertyHandle) -> RecordedMatchRecordProperty:
        if not isinstance(property, PropertyHandle):
            raise TypeError("match.record(...).prop(...) requires PropertyHandle")
        return RecordedMatchRecordProperty(self._input_name, property)


class RecordedMatchExpressionFactory:
    """Factory for symbolic matcher-result production expressions."""

    __slots__ = ()

    def resource(self) -> RecordedMatchResource:
        return RecordedMatchResource()

    def record(self, input_name: str) -> RecordedMatchRecordAccessor:
        return RecordedMatchRecordAccessor(input_name)

    def value(self, index: int) -> RecordedMatchTupleValue:
        if index < 0:
            raise ValueError("matcher tuple value index must be non-negative")
        return RecordedMatchTupleValue(index)


match = RecordedMatchExpressionFactory()


class PlanReferenceNamespace:
    """Read-only namespace of handles exported by a concept plan."""

    __slots__ = ("collections", "computed", "matchers", "ports", "props", "records")

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
        self.matchers = PlanHandleReferences(plan, "matcher", plan.matcher_definitions)
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


class RecordedConceptRuntimeLoader:
    """Runtime loader for a recorded concept plan."""

    __slots__ = ("_plan",)

    def __init__(self, plan: CapsuleConceptPlan) -> None:
        self._plan = plan

    def emit_source(self) -> str:
        return self._plan.build_data_definition().emit_container_runtime_source(
            evaluator_names=self._evaluator_names(),
        )

    def load(
        self,
        *,
        runtime_globals: Mapping[str, object] | None = None,
    ) -> CapsuleRuntime:
        helpers = self._runtime_helpers()
        source = self._plan.build_data_definition().emit_container_runtime_source(
            evaluator_names=tuple((helper.value, helper.name) for helper in helpers),
        )
        namespace: dict[str, object] = {
            helper.name: helper.value
            for helper in helpers
        }
        namespace.update(runtime_globals or {})
        exec(compile(source, f"<yidl.recorded_capsule.{self._plan.name}>", "exec"), namespace)
        return CapsuleRuntime(
            definition=self._plan,
            source=source,
            namespace=MappingProxyType(namespace),
        )

    def _evaluator_names(self) -> tuple[tuple[object, str], ...]:
        return tuple(
            (helper.value, helper.name)
            for helper in self._runtime_helpers()
        )

    def _runtime_helpers(self) -> tuple[RuntimeHelperOperation, ...]:
        by_name: dict[str, RuntimeHelperOperation] = {}
        for plan in _extension_closure((*self._plan.extensions, self._plan)):
            for helper in plan.runtime_helpers:
                existing = by_name.get(helper.name)
                if existing is None:
                    by_name[helper.name] = helper
                    continue
                if existing.value is not helper.value:
                    raise ValueError(
                        f"runtime helper {helper.name!r} is already registered "
                        "with a different value"
                    )
        return tuple(by_name.values())


class ReplayContext:
    """Replay state for a single concept-plan application."""

    __slots__ = (
        "_applied_plan_ids",
        "_collection_name_owners",
        "_collection_specs",
        "_computed_collection_specs",
        "_dds",
        "_matcher_input_specs",
        "_matcher_owners",
        "_matcher_specs",
        "_port_index_owner",
        "_port_owners",
        "_port_specs",
        "_production_owners",
        "_production_specs",
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
        self._matcher_owners: dict[str, MatcherHandle] = {}
        self._production_owners: dict[str, ProductionHandle] = {}
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
        self._matcher_specs: dict[HandleKey, MatcherSpec] = {}
        self._matcher_input_specs: dict[HandleKey, MatcherInputSpec] = {}
        self._production_specs: dict[HandleKey, object] = {}

    def apply_plan(self, plan: CapsuleConceptPlan) -> None:
        if plan.owner_id in self._applied_plan_ids:
            return
        for extension in plan.extensions:
            self.apply_plan(extension)
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
        for matcher in plan.matcher_definitions:
            self._apply_matcher(matcher)
        for input_handle in plan.matcher_inputs:
            self._apply_matcher_input(input_handle)
        for default in plan.matcher_defaults:
            self._apply_matcher_default(default)
        for rule in plan.matcher_rules:
            self._apply_matcher_rule(rule)
        for production in plan.production_definitions:
            self._apply_production(production)
        for group in plan.production_groups:
            self._apply_production_group(group)
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

    def _apply_matcher(self, matcher: MatcherHandle) -> None:
        existing = self._matcher_owners.get(matcher.name)
        if existing is not None:
            raise ValueError(
                f"matcher {matcher.name!r} is already owned by concept "
                f"{existing.owner_name!r}; concept {matcher.owner_name!r} must "
                "reference it instead of redefining it"
            )
        spec = self._dds.ensure_matcher(matcher.name)
        self._matcher_owners[matcher.name] = matcher
        self._matcher_specs[_handle_key(matcher)] = spec

    def _apply_matcher_input(self, input_handle: MatcherInputHandle) -> None:
        matcher = self._resolve_matcher(input_handle.matcher)
        spec = matcher.ensure_input(
            input_handle.name,
            self._resolve_collection_source(input_handle.source),
        )
        self._matcher_input_specs[_handle_key(input_handle)] = spec

    def _apply_matcher_default(self, operation: MatcherDefaultOperation) -> None:
        self._resolve_matcher(operation.matcher).default(operation.resource)

    def _apply_matcher_rule(self, operation: MatcherRuleOperation) -> None:
        matcher = self._resolve_matcher(operation.matcher)
        matcher.rule(
            when=tuple(
                self._resolve_matcher_condition(condition)
                for condition in operation.conditions
            ),
            resource=operation.resource,
            weight=operation.weight,
            name=operation.name,
        )

    def _apply_production(self, production: ProductionHandle) -> None:
        existing = self._production_owners.get(production.name)
        if existing is not None:
            raise ValueError(
                f"production {production.name!r} is already owned by concept "
                f"{existing.owner_name!r}; concept {production.owner_name!r} "
                "must reference it instead of redefining it"
            )
        spec = self._dds.production(
            production.name,
            source=self._resolve_production_source(production.source),
            target=self._resolve_collection(production.target),
            when=tuple(
                self._resolve_condition(condition)
                for condition in production.conditions
            ),
            identity=(
                None
                if production.identity is None
                else self._resolve_value_expression(production.identity)
            ),
            values={
                self._resolve_property(value.property): self._resolve_value_expression(
                    value.expression
                )
                for value in production.values
            },
            policy=production.policy,
        )
        self._production_owners[production.name] = production
        self._production_specs[_handle_key(production)] = spec

    def _apply_production_group(self, group: ProductionGroupOperation) -> None:
        self._dds.ensure_production_group(
            group.name,
            *(
                self._production_specs[_handle_key(production)]
                for production in group.productions
            ),
        )

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

    def _resolve_collection(self, collection: CollectionHandle) -> CollectionSpec:
        try:
            return self._collection_specs[_handle_key(collection)]
        except KeyError as exc:
            raise ValueError(
                f"unresolved collection handle {collection.name!r} from "
                f"concept {collection.owner_name!r}"
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

    def _resolve_matcher(self, matcher: MatcherHandle) -> MatcherSpec:
        try:
            return self._matcher_specs[_handle_key(matcher)]
        except KeyError as exc:
            raise ValueError(
                f"unresolved matcher handle {matcher.name!r} from concept "
                f"{matcher.owner_name!r}"
            ) from exc

    def _resolve_matcher_input(
        self,
        input_handle: MatcherInputHandle,
    ) -> MatcherInputSpec:
        try:
            return self._matcher_input_specs[_handle_key(input_handle)]
        except KeyError as exc:
            raise ValueError(
                f"unresolved matcher input {input_handle.name!r} from concept "
                f"{input_handle.owner_name!r}"
            ) from exc

    def _resolve_condition(
        self,
        condition: PropertyEqualsHandle,
    ) -> PropertyEquals:
        return self._resolve_property(condition.property).eq(condition.value)

    def _resolve_matcher_condition(
        self,
        condition: MatcherConditionHandle,
    ) -> MatcherCondition:
        return self._resolve_matcher_input(condition.ref.input).prop(
            self._resolve_property(condition.ref.property)
        ).eq(condition.value)

    def _resolve_production_source(
        self,
        source: CollectionHandle | ComputedCollectionHandle | MatcherResultSourceHandle,
    ) -> CollectionSpec | ComputedCollectionSpec | MatcherResultSource:
        if isinstance(source, MatcherResultSourceHandle):
            return self._resolve_matcher(source.matcher).results()
        return self._resolve_collection_source(source)

    def _resolve_value_expression(
        self,
        expression: RecordedValueExpression,
    ) -> ValueExpression | object:
        if isinstance(expression, RecordedMatchResource):
            return dds_match.resource()
        if isinstance(expression, RecordedMatchTupleValue):
            return dds_match.value(expression.index)
        if isinstance(expression, RecordedMatchRecordProperty):
            return dds_match.record(expression.input_name).prop(
                self._resolve_property(expression.property)
            )
        if isinstance(expression, RecordedPortAddress):
            return self._resolve_port(expression.port).of(expression.owner_identity)
        if isinstance(expression, RecordedReadProperty):
            return self._resolve_property(expression.property).read()
        return expression

    def _resolve_port(self, port: PortHandle) -> PortSpec:
        try:
            return self._port_specs[_handle_key(port)]
        except KeyError as exc:
            raise ValueError(
                f"unresolved port handle {port.name!r} from concept "
                f"{port.owner_name!r}"
            ) from exc

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
    extends: Iterable[CapsuleConceptPlan] = (),
) -> CapsuleConceptBuilder:
    """Create a recorded capsule concept builder."""

    return CapsuleConceptBuilder(name, extends=extends)


def _extension_closure(
    plans: Iterable[CapsuleConceptPlan],
) -> tuple[CapsuleConceptPlan, ...]:
    seen: set[int] = set()
    ordered: list[CapsuleConceptPlan] = []

    def visit(plan: CapsuleConceptPlan) -> None:
        if plan.owner_id in seen:
            return
        seen.add(plan.owner_id)
        for extension in plan.extensions:
            visit(extension)
        ordered.append(plan)

    for plan in plans:
        visit(plan)
    return tuple(ordered)


def _handle_owner_in_plans(
    owner_id: int,
    plans: Iterable[CapsuleConceptPlan],
) -> bool:
    return any(plan.owner_id == owner_id for plan in plans)


def _runtime_helper_name(
    value: Callable[..., object],
    name: str | None,
) -> str:
    if name is not None:
        _require_name(name, "runtime helper name")
        return name
    inferred = getattr(value, "__name__", None)
    if not isinstance(inferred, str) or not inferred or inferred == "<lambda>":
        raise ValueError("runtime helper name is required")
    _require_name(inferred, "runtime helper name")
    return inferred


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
    | PortHandle
    | MatcherHandle
    | MatcherInputHandle
    | ProductionHandle,
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
    "CapsuleRuntime",
    "CollectionHandle",
    "ComputedCollectionHandle",
    "MatcherHandle",
    "PortHandle",
    "PropertyHandle",
    "RecordHandle",
    "capsule_concept",
    "match",
]
