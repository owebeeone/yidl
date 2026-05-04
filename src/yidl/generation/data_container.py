"""Decoration-time containers for DDS records."""

from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import Iterable, Iterator

from yidl.generation.data_schema import CollectionSpec
from yidl.generation.data_schema import ComputedCollectionSpec
from yidl.generation.data_schema import DataDefinitionSystem
from yidl.generation.data_schema import PortAddress
from yidl.generation.data_schema import PortIndexSpec
from yidl.generation.data_schema import PropertyEquals
from yidl.generation.matcher import NOT_PROVIDED


class WritePolicy(ABC):
    """Record merge behavior for explicit builder writes."""

    __slots__ = ("name", "requires_identity")

    def __init__(self, name: str, *, requires_identity: bool) -> None:
        self.name = name
        self.requires_identity = requires_identity

    @abstractmethod
    def resolve_existing(
        self,
        *,
        existing: object,
        new_record: object,
        collection_name: str,
        identity: object,
    ) -> object:
        raise NotImplementedError

    def __repr__(self) -> str:
        return self.name


class _AddIfAbsentPolicy(WritePolicy):
    __slots__ = ()

    def __init__(self) -> None:
        super().__init__("AddIfAbsent", requires_identity=True)

    def resolve_existing(
        self,
        *,
        existing: object,
        new_record: object,
        collection_name: str,
        identity: object,
    ) -> object:
        return existing


class _ReplaceExistingPolicy(WritePolicy):
    __slots__ = ()

    def __init__(self) -> None:
        super().__init__("ReplaceExisting", requires_identity=True)

    def resolve_existing(
        self,
        *,
        existing: object,
        new_record: object,
        collection_name: str,
        identity: object,
    ) -> object:
        return new_record


class _RejectDuplicatePolicy(WritePolicy):
    __slots__ = ()

    def __init__(self) -> None:
        super().__init__("RejectDuplicate", requires_identity=False)

    def resolve_existing(
        self,
        *,
        existing: object,
        new_record: object,
        collection_name: str,
        identity: object,
    ) -> object:
        if existing is new_record:
            return existing
        raise ValueError(
            f"duplicate identity {identity!r} in collection {collection_name!r}"
        )


AddIfAbsent = _AddIfAbsentPolicy()
ReplaceExisting = _ReplaceExistingPolicy()
RejectDuplicate = _RejectDuplicatePolicy()


class RuntimeProperty:
    """Emitted-runtime property descriptor."""

    __slots__ = ("default", "name", "storage_name", "value_type")

    def __init__(
        self,
        name: str,
        value_type: type[object] | tuple[type[object], ...],
        *,
        default: object,
        storage_name: str,
    ) -> None:
        self.name = name
        self.value_type = value_type
        self.default = default
        self.storage_name = storage_name

    def eq(self, value: object) -> RuntimePropertyEquals:
        return RuntimePropertyEquals(self, value)

    def value_from(self, record: object) -> object:
        return getattr(record, self.storage_name)

    def validate(self, value: object) -> object:
        if self.value_type is object:
            return value
        if not isinstance(value, self.value_type):
            raise TypeError(
                f"{self.name} must be {_type_name(self.value_type)}, "
                f"got {type(value).__name__}"
            )
        return value

    def __repr__(self) -> str:
        return self.name


class RuntimePropertyEquals:
    """Eq-only emitted-runtime condition."""

    __slots__ = ("property", "value")

    def __init__(self, property: RuntimeProperty, value: object) -> None:
        self.property = property
        self.value = value

    def matches(self, record: object) -> bool:
        actual = getattr(record, self.property.storage_name, NOT_PROVIDED)
        return actual == self.value


class RuntimeRecord:
    """Emitted-runtime record descriptor."""

    __slots__ = ("_record_class", "name", "properties")

    def __init__(self, name: str, properties: tuple[RuntimeProperty, ...]) -> None:
        self.name = name
        self.properties = properties
        self._record_class: type[object] | None = None

    def bind_record_class(self, record_class: type[object]) -> type[object]:
        record_spec = getattr(record_class, "__dds_record_spec__", None)
        if record_spec is not self:
            raise TypeError(f"{record_class.__name__} is not bound to record {self.name}")
        self._record_class = record_class
        return record_class

    def require_property(self, prop: RuntimeProperty) -> None:
        if prop not in self.properties:
            raise ValueError(f"record {self.name!r} has no property {prop.name!r}")

    def record_class(self) -> type[object]:
        if self._record_class is None:
            raise TypeError(f"record {self.name!r} has no bound runtime class")
        return self._record_class

    def record(self, **values: object) -> object:
        return self.record_class()(**values)

    def validate_record(self, record: object) -> None:
        if getattr(type(record), "__dds_record_spec__", None) is not self:
            raise TypeError(f"expected {self.name} record, got {type(record).__name__}")

    def values_of(self, record: object) -> dict[RuntimeProperty, object]:
        self.validate_record(record)
        return {
            prop: prop.value_from(record)
            for prop in self.properties
        }

    def __repr__(self) -> str:
        return self.name


class RuntimeUnion:
    """Emitted-runtime union descriptor."""

    __slots__ = ("name", "variants")

    def __init__(self, name: str, variants: tuple[RuntimeRecord, ...]) -> None:
        self.name = name
        self.variants = variants

    def require_property(self, prop: RuntimeProperty) -> None:
        if not any(prop in variant.properties for variant in self.variants):
            raise ValueError(f"union {self.name!r} has no variant with property {prop.name!r}")

    def record_spec_for(self, record: object) -> RuntimeRecord:
        record_spec = getattr(type(record), "__dds_record_spec__", None)
        for variant in self.variants:
            if record_spec is variant:
                return variant
        raise TypeError(f"expected {self.name} variant record, got {type(record).__name__}")

    def validate_record(self, record: object) -> None:
        self.record_spec_for(record)

    def __repr__(self) -> str:
        return self.name


class RuntimeCollection:
    """Emitted-runtime concrete collection descriptor."""

    __slots__ = ("_allows_multiple", "_system", "identity", "name", "record_shape")

    def __init__(
        self,
        name: str,
        record_shape: RuntimeRecord | RuntimeUnion,
        *,
        allows_multiple: bool,
        identity: RuntimeProperty | None = None,
    ) -> None:
        self.name = name
        self.record_shape = record_shape
        self.identity = identity
        self._allows_multiple = allows_multiple
        self._system: RuntimeContainerSpec | None = None

    @property
    def cardinality(self) -> RuntimeCollection:
        return self

    @property
    def record_spec(self) -> RuntimeRecord | RuntimeUnion:
        return self.record_shape

    @property
    def system(self) -> RuntimeContainerSpec | None:
        return self._system

    def allows_multiple(self) -> bool:
        return self._allows_multiple

    def record(self, **values: object) -> object:
        if isinstance(self.record_shape, RuntimeUnion):
            raise TypeError(
                f"collection {self.name!r} uses union {self.record_shape.name!r}; "
                "create a concrete variant record instead"
            )
        return self.record_shape.record(**values)

    def identity_of(self, record: object) -> object:
        self.record_shape.validate_record(record)
        if self.identity is None:
            return None
        return self.identity.value_from(record)

    def fact_keys(self, record: object) -> tuple[tuple[RuntimeProperty, object], ...]:
        record_spec = (
            self.record_shape.record_spec_for(record)
            if isinstance(self.record_shape, RuntimeUnion)
            else self.record_shape
        )
        return tuple((prop, prop.value_from(record)) for prop in record_spec.properties)

    def __repr__(self) -> str:
        return self.name


class RuntimeComputedCollection:
    """Emitted-runtime computed collection descriptor."""

    __slots__ = ("_system", "conditions", "name", "source")

    def __init__(
        self,
        name: str,
        *,
        source: CollectionViewSpec,
        when: tuple[RuntimePropertyEquals, ...],
    ) -> None:
        self.name = name
        self.source = source
        self.conditions = when
        self._system: RuntimeContainerSpec | None = None

    @property
    def identity(self) -> RuntimeProperty | None:
        return self.source.identity

    @property
    def record_shape(self) -> RuntimeRecord | RuntimeUnion:
        return self.source.record_shape

    @property
    def record_spec(self) -> RuntimeRecord | RuntimeUnion:
        return self.source.record_spec

    @property
    def system(self) -> RuntimeContainerSpec | None:
        return self._system

    def identity_of(self, record: object) -> object:
        return self.source.identity_of(record)

    def matches(self, record: object) -> bool:
        if _is_computed_collection(self.source) and not self.source.matches(record):
            return False
        self.record_shape.validate_record(record)
        return all(condition.matches(record) for condition in self.conditions)

    def __repr__(self) -> str:
        return self.name


class RuntimePort:
    """Emitted-runtime build destination."""

    __slots__ = ("_allows_multiple", "name")

    def __init__(self, name: str, *, allows_multiple: bool) -> None:
        self.name = name
        self._allows_multiple = allows_multiple

    @property
    def cardinality(self) -> RuntimePort:
        return self

    def allows_multiple(self) -> bool:
        return self._allows_multiple

    def of(self, owner_identity: object) -> RuntimePortAddress:
        return RuntimePortAddress(self, owner_identity)

    def __repr__(self) -> str:
        return self.name


class RuntimePortAddress:
    """Emitted-runtime owner-scoped port target."""

    __slots__ = ("owner_identity", "port")

    def __init__(self, port: RuntimePort, owner_identity: object) -> None:
        self.port = port
        self.owner_identity = owner_identity

    def __eq__(self, other: object) -> bool:
        return (
            isinstance(other, RuntimePortAddress)
            and self.port is other.port
            and self.owner_identity == other.owner_identity
        )

    def __repr__(self) -> str:
        return f"{self.port.name}.of({self.owner_identity!r})"


class RuntimePortIndex:
    """Emitted-runtime properties used for ordered port-child queries."""

    __slots__ = ("order", "target")

    def __init__(self, *, target: RuntimeProperty, order: RuntimeProperty) -> None:
        self.target = target
        self.order = order


class RuntimeContainerSpec:
    """Emitted-runtime schema descriptor for one generated container module."""

    __slots__ = ("collections", "computed_collections", "matchers", "port_index", "ports")

    def __init__(
        self,
        *,
        collections: tuple[RuntimeCollection, ...],
        computed_collections: tuple[RuntimeComputedCollection, ...] = (),
        matchers: tuple[object, ...] = (),
        ports: tuple[RuntimePort, ...] = (),
        port_index: RuntimePortIndex | None = None,
    ) -> None:
        self.collections = collections
        self.computed_collections = computed_collections
        self.matchers = matchers
        self.ports = ports
        self.port_index = port_index
        for collection in (*collections, *computed_collections):
            collection._system = self


ConcreteCollectionSpec = CollectionSpec | RuntimeCollection
ComputedCollectionViewSpec = ComputedCollectionSpec | RuntimeComputedCollection
CollectionViewSpec = ConcreteCollectionSpec | ComputedCollectionViewSpec


class DDSContainerBuilder:
    """Mutable record holder for one decoration run."""

    __slots__ = (
        "_frozen",
        "_identity_indexes",
        "_next_write_order",
        "_records",
        "_system",
        "_write_orders",
    )

    def __init__(self, system: DataDefinitionSystem | RuntimeContainerSpec) -> None:
        self._system = system
        self._records: dict[ConcreteCollectionSpec, list[object]] = {
            collection: []
            for collection in system.collections
        }
        self._identity_indexes: dict[ConcreteCollectionSpec, dict[object, object]] = {
            collection: {}
            for collection in system.collections
            if collection.identity is not None
        }
        self._write_orders: dict[int, int] = {}
        self._next_write_order = 0
        self._frozen = False

    @property
    def system(self) -> DataDefinitionSystem | RuntimeContainerSpec:
        return self._system

    def add(self, collection: ConcreteCollectionSpec, record: object) -> DDSContainerBuilder:
        return self.write(collection, record, policy=RejectDuplicate)

    def write(
        self,
        collection: ConcreteCollectionSpec,
        record: object,
        *,
        policy: WritePolicy = RejectDuplicate,
    ) -> DDSContainerBuilder:
        if not isinstance(policy, WritePolicy):
            raise TypeError(
                f"write policy must be a WritePolicy, got {type(policy).__name__}"
            )
        self._require_mutable()
        self._require_concrete_collection(collection)
        collection.record_shape.validate_record(record)
        self._validate_port_record(record)
        records = self._records[collection]
        identity_index = self._identity_indexes.get(collection)
        if identity_index is None and policy.requires_identity:
            raise ValueError(
                f"{policy.name} requires an identity for collection {collection.name!r}"
            )
        identity = collection.identity_of(record) if identity_index is not None else None
        existing = (
            identity_index.get(identity)
            if identity_index is not None
            else None
        )
        if not collection.cardinality.allows_multiple() and records and existing is None:
            if any(existing_record is record for existing_record in records):
                return self
            raise ValueError(f"single collection {collection.name!r} already has a record")
        if identity_index is not None:
            if existing is not None:
                replacement = policy.resolve_existing(
                    existing=existing,
                    new_record=record,
                    collection_name=collection.name,
                    identity=identity,
                )
                if replacement is existing:
                    return self
                self._validate_single_port(replacement, replacing=existing)
                self._replace_write_order(existing, replacement)
                records[records.index(existing)] = replacement
                identity_index[identity] = replacement
                return self
            identity_index[identity] = record
        elif any(existing is record for existing in records):
            return self
        self._validate_single_port(record)
        records.append(record)
        self._remember_write_order(record)
        return self

    def record(self, collection: ConcreteCollectionSpec, **values: object) -> object:
        record = collection.record(**values)
        self.add(collection, record)
        return record

    def records(self, collection: CollectionViewSpec) -> tuple[object, ...]:
        if _is_computed_collection(collection):
            return tuple(_CollectionView(self._frozen_container(), collection).sequence())
        self._require_concrete_collection(collection)
        return tuple(self._records[collection])

    def matching(
        self,
        collection: CollectionViewSpec,
        *conditions: PropertyEquals,
    ) -> tuple[object, ...]:
        return tuple(
            record
            for record in self.records(collection)
            if all(condition.matches(record) for condition in conditions)
        )

    def by_identity(self, collection: CollectionViewSpec, value: object) -> object | None:
        return _CollectionView(self._frozen_container(), collection).by_identity(value)

    def children_at(self, port_address: PortAddress | RuntimePortAddress) -> tuple[object, ...]:
        return self._frozen_container().children_at(port_address)

    def freeze(self) -> DDSContainer:
        self._frozen = True
        return self._frozen_container()

    def _frozen_container(self) -> DDSContainer:
        records = {
            collection: tuple(items)
            for collection, items in self._records.items()
        }
        identity_indexes = {
            collection: dict(index)
            for collection, index in self._identity_indexes.items()
        }
        return DDSContainer(
            self._system,
            records=records,
            identity_indexes=identity_indexes,
            write_orders=dict(self._write_orders),
        )

    def _remember_write_order(self, record: object) -> None:
        self._write_orders[id(record)] = self._next_write_order
        self._next_write_order += 1

    def _replace_write_order(self, existing: object, replacement: object) -> None:
        order = self._write_orders.pop(id(existing), self._next_write_order)
        self._write_orders[id(replacement)] = order
        if order == self._next_write_order:
            self._next_write_order += 1

    def _validate_port_record(self, record: object) -> None:
        port_index = _system_port_index(self._system)
        if port_index is None:
            return
        target = getattr(record, port_index.target.storage_name, NOT_PROVIDED)
        if target is NOT_PROVIDED:
            return
        if not _is_port_address(target):
            raise TypeError(
                f"{port_index.target.name} must be a PortAddress, "
                f"got {type(target).__name__}"
            )
        order = getattr(record, port_index.order.storage_name, NOT_PROVIDED)
        if order is NOT_PROVIDED:
            raise ValueError(
                f"port-indexed record with {port_index.target.name!r} "
                f"must also define {port_index.order.name!r}"
            )
        port_index.order.validate(order)

    def _validate_single_port(
        self,
        record: object,
        *,
        replacing: object | None = None,
    ) -> None:
        port_index = _system_port_index(self._system)
        if port_index is None:
            return
        target = getattr(record, port_index.target.storage_name, NOT_PROVIDED)
        if target is NOT_PROVIDED or target.port.cardinality.allows_multiple():
            return
        for records in self._records.values():
            for existing in records:
                if existing is record or existing is replacing:
                    continue
                existing_target = getattr(
                    existing,
                    port_index.target.storage_name,
                    NOT_PROVIDED,
                )
                if existing_target == target:
                    raise ValueError(f"single port {target!r} already has a child")

    def _require_mutable(self) -> None:
        if self._frozen:
            raise RuntimeError("DDSContainerBuilder is frozen")

    def _require_concrete_collection(self, collection: ConcreteCollectionSpec) -> None:
        if collection not in self._records:
            raise ValueError("collection belongs to another data-definition system")


class DDSContainer:
    """Immutable resolved DDS data for one decoration run."""

    __slots__ = ("_identity_indexes", "_records", "_system", "_write_orders", "matchers")

    def __init__(
        self,
        system: DataDefinitionSystem | RuntimeContainerSpec,
        *,
        records: dict[ConcreteCollectionSpec, tuple[object, ...]],
        identity_indexes: dict[ConcreteCollectionSpec, dict[object, object]],
        write_orders: dict[int, int] | None = None,
    ) -> None:
        self._system = system
        self._records = records
        self._identity_indexes = identity_indexes
        self._write_orders = {} if write_orders is None else write_orders
        self.matchers = _MatcherViewNamespace(self)

    @property
    def system(self) -> DataDefinitionSystem | RuntimeContainerSpec:
        return self._system

    def view(self, collection: CollectionViewSpec) -> _CollectionView:
        self._require_collection(collection)
        return _CollectionView(self, collection)

    def records(self, collection: CollectionViewSpec) -> tuple[object, ...]:
        return tuple(self.view(collection).sequence())

    def matching(
        self,
        collection: CollectionViewSpec,
        *conditions: PropertyEquals,
    ) -> tuple[object, ...]:
        return tuple(
            record
            for record in self.view(collection).sequence()
            if all(condition.matches(record) for condition in conditions)
        )

    def by_identity(self, collection: CollectionViewSpec, value: object) -> object | None:
        return self.view(collection).by_identity(value)

    def children_at(self, port_address: PortAddress | RuntimePortAddress) -> tuple[object, ...]:
        if not _is_port_address(port_address):
            raise TypeError(
                f"port_address must be a PortAddress, got {type(port_address).__name__}"
            )
        port_index = _system_port_index(self._system)
        if port_index is None:
            raise ValueError("data-definition system has no port index")
        children: list[object] = []
        for records in self._records.values():
            for record in records:
                target = getattr(record, port_index.target.storage_name, NOT_PROVIDED)
                if target == port_address:
                    children.append(record)
        if (
            not port_address.port.cardinality.allows_multiple()
            and len(children) > 1
        ):
            raise ValueError(f"single port {port_address!r} has multiple children")
        return tuple(
            sorted(
                children,
                key=lambda record: (
                    getattr(record, port_index.order.storage_name),
                    self._write_orders.get(id(record), 0),
                ),
            )
        )

    def __getattr__(self, name: str) -> _CollectionView:
        collection = _collection_named(self._system, name)
        if collection is None:
            raise AttributeError(name)
        return self.view(collection)

    def _require_collection(self, collection: CollectionViewSpec) -> None:
        if _is_concrete_collection(collection) and collection not in self._records:
            raise ValueError("unknown collection")
        if (
            _is_computed_collection(collection)
            and collection not in self._system.computed_collections
        ):
            raise ValueError("unknown computed collection")


class _CollectionView:
    __slots__ = ("_collection", "_container")

    def __init__(self, container: DDSContainer, collection: CollectionViewSpec) -> None:
        self._container = container
        self._collection = collection

    @property
    def collection(self) -> CollectionViewSpec:
        return self._collection

    @property
    def container(self) -> tuple[object, ...]:
        return tuple(self.sequence())

    def sequence(self) -> Iterator[object]:
        if _is_concrete_collection(self._collection):
            yield from self._container._records.get(self._collection, ())
            return
        for record in self._container.view(self._collection.source).sequence():
            if all(condition.matches(record) for condition in self._collection.conditions):
                yield record

    def one(self) -> object | None:
        records = tuple(self.sequence())
        if len(records) > 1:
            raise ValueError(f"collection {self._collection.name!r} has multiple records")
        if not records:
            return None
        return records[0]

    def by_identity(self, value: object) -> object | None:
        if self._collection.identity is None:
            raise ValueError(f"collection {self._collection.name!r} has no identity")
        if _is_concrete_collection(self._collection):
            return self._container._identity_indexes.get(self._collection, {}).get(value)
        record = self._container.view(self._collection.source).by_identity(value)
        if record is None:
            return None
        if not all(condition.matches(record) for condition in self._collection.conditions):
            return None
        return record

    def contains(self, value: object) -> bool:
        return self.by_identity(value) is not None

    def __iter__(self) -> Iterator[object]:
        return self.sequence()


class _MatcherViewNamespace:
    __slots__ = ("_container", "_runtimes")

    def __init__(self, container: DDSContainer) -> None:
        self._container = container
        self._runtimes: dict[str, _ContainerMatcherRuntime] = {}

    def __getattr__(self, name: str) -> _ContainerMatcherRuntime:
        existing = self._runtimes.get(name)
        if existing is not None:
            return existing
        for matcher in getattr(self._container.system, "matchers", ()):
            if matcher.name == name:
                runtime = _ContainerMatcherRuntime(self._container, matcher.runtime())
                self._runtimes[name] = runtime
                return runtime
        raise AttributeError(name)


class _ContainerMatcherRuntime:
    __slots__ = ("_container", "_runtime")

    def __init__(self, container: DDSContainer, runtime: object) -> None:
        self._container = container
        self._runtime = runtime

    @property
    def matcher(self) -> object:
        return self._runtime.matcher

    def resolve(self, *records: object) -> object:
        return self._runtime.resolve(*records)

    def sequence(self) -> Iterator[object]:
        sequences: list[Iterable[object]] = [
            self._container.view(input_spec.source).sequence()
            for input_spec in self._runtime.matcher.inputs
        ]
        yield from self._runtime.sequence(*sequences)


def _collection_named(
    system: DataDefinitionSystem | RuntimeContainerSpec,
    name: str,
) -> CollectionViewSpec | None:
    for collection in system.collections:
        if collection.name == name:
            return collection
    for collection in system.computed_collections:
        if collection.name == name:
            return collection
    return None


def _is_concrete_collection(collection: CollectionViewSpec) -> bool:
    return isinstance(collection, (CollectionSpec, RuntimeCollection))


def _is_computed_collection(collection: CollectionViewSpec) -> bool:
    return isinstance(collection, (ComputedCollectionSpec, RuntimeComputedCollection))


def _is_port_address(value: object) -> bool:
    return isinstance(value, (PortAddress, RuntimePortAddress))


def _system_port_index(
    system: DataDefinitionSystem | RuntimeContainerSpec,
) -> PortIndexSpec | RuntimePortIndex | None:
    if isinstance(system, RuntimeContainerSpec):
        return system.port_index
    return system.port_index_spec


def _type_name(value_type: type[object] | tuple[type[object], ...]) -> str:
    if isinstance(value_type, tuple):
        return " or ".join(item.__name__ for item in value_type)
    return value_type.__name__


__all__ = [
    "AddIfAbsent",
    "CollectionViewSpec",
    "DDSContainer",
    "DDSContainerBuilder",
    "RejectDuplicate",
    "ReplaceExisting",
    "RuntimeCollection",
    "RuntimeComputedCollection",
    "RuntimeContainerSpec",
    "RuntimePort",
    "RuntimePortAddress",
    "RuntimePortIndex",
    "RuntimeProperty",
    "RuntimePropertyEquals",
    "RuntimeRecord",
    "RuntimeUnion",
    "WritePolicy",
]
