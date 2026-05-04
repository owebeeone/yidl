"""Declarative data-definition system for rule-driven generation.

The data-definition system describes record shapes, collections, equality
lookup facts, and collection derivations.  It intentionally does not store
runtime records.  Record classes generated from this schema are plain slotted
containers, not dataclasses.
"""

from __future__ import annotations

from collections.abc import Callable, Mapping, Sequence
import re
import textwrap

import astichi


class RequiredValue:
    """Sentinel meaning a property has no default and must be supplied."""

    __slots__ = ()

    def __repr__(self) -> str:
        return "REQUIRED"


REQUIRED = RequiredValue()


class DataDefinitionSystem:
    """Schema container for generation data definitions."""

    __slots__ = (
        "_collections",
        "_computed_collections",
        "_port_index",
        "_ports",
        "_production_groups",
        "_productions",
        "_properties",
        "_records",
        "_transforms",
        "_unions",
        "many",
        "single",
    )

    def __init__(self) -> None:
        self._properties: dict[str, PropertySpec] = {}
        self._records: dict[str, RecordSpec] = {}
        self._unions: dict[str, UnionSpec] = {}
        self._collections: dict[str, CollectionSpec] = {}
        self._computed_collections: dict[str, ComputedCollectionSpec] = {}
        self._ports: dict[str, PortSpec] = {}
        self._port_index: PortIndexSpec | None = None
        self._productions: dict[str, ProductionSpec] = {}
        self._production_groups: dict[str, ProductionGroupSpec] = {}
        self._transforms: dict[str, TransformSpec] = {}
        self.single = SingleCollectionCardinality()
        self.many = ManyCollectionCardinality()

    @property
    def properties(self) -> tuple[PropertySpec, ...]:
        return tuple(self._properties.values())

    @property
    def records(self) -> tuple[RecordSpec, ...]:
        return tuple(self._records.values())

    @property
    def unions(self) -> tuple[UnionSpec, ...]:
        return tuple(self._unions.values())

    @property
    def collections(self) -> tuple[CollectionSpec, ...]:
        return tuple(self._collections.values())

    @property
    def computed_collections(self) -> tuple[ComputedCollectionSpec, ...]:
        return tuple(self._computed_collections.values())

    @property
    def ports(self) -> tuple[PortSpec, ...]:
        return tuple(self._ports.values())

    @property
    def productions(self) -> tuple[ProductionSpec, ...]:
        return tuple(self._productions.values())

    @property
    def production_groups(self) -> tuple[ProductionGroupSpec, ...]:
        return tuple(self._production_groups.values())

    @property
    def port_index_spec(self) -> PortIndexSpec | None:
        return self._port_index

    @property
    def transforms(self) -> tuple[TransformSpec, ...]:
        return tuple(self._transforms.values())

    def property(
        self,
        name: str,
        value_type: type[object] | tuple[type[object], ...],
        *,
        default: object = REQUIRED,
        storage_name: str | None = None,
    ) -> PropertySpec:
        _require_name(name, "property name")
        resolved_storage_name = _to_snake_case(name) if storage_name is None else storage_name
        _require_name(resolved_storage_name, "property storage name")
        if name in self._properties:
            raise ValueError(f"property {name!r} is already defined")
        existing_storage = next(
            (
                prop
                for prop in self._properties.values()
                if prop.storage_name == resolved_storage_name
            ),
            None,
        )
        if existing_storage is not None:
            raise ValueError(
                f"property storage name {resolved_storage_name!r} is already used "
                f"by {existing_storage.name!r}"
            )
        spec = PropertySpec(
            system=self,
            name=name,
            value_type=value_type,
            default=default,
            storage_name=resolved_storage_name,
        )
        if default is not REQUIRED:
            spec.validate(default)
        self._properties[name] = spec
        return spec

    def record(self, name: str, *properties: PropertySpec) -> RecordSpec:
        _require_name(name, "record name")
        if name in self._records:
            raise ValueError(f"record {name!r} is already defined")
        if name in self._unions:
            raise ValueError(f"record {name!r} conflicts with an existing union")
        spec = RecordSpec(self, name, properties)
        self._records[name] = spec
        return spec

    def union(self, name: str) -> UnionSpec:
        _require_name(name, "union name")
        if name in self._unions:
            raise ValueError(f"union {name!r} is already defined")
        if name in self._records:
            raise ValueError(f"union {name!r} conflicts with an existing record")
        spec = UnionSpec(self, name)
        self._unions[name] = spec
        return spec

    def collection(
        self,
        name: str,
        record: RecordSpec | UnionSpec,
        *,
        cardinality: CollectionCardinality,
        identity: PropertySpec | None = None,
    ) -> CollectionSpec:
        _require_name(name, "collection name")
        if name in self._collections or name in self._computed_collections:
            raise ValueError(f"collection {name!r} is already defined")
        if record.system is not self:
            raise ValueError("collection record shape belongs to another data-definition system")
        if identity is not None:
            record.require_identity_property(identity)
        spec = CollectionSpec(
            system=self,
            name=name,
            record=record,
            cardinality=cardinality,
            identity=identity,
        )
        self._collections[name] = spec
        return spec

    def computed_collection(
        self,
        name: str,
        *,
        source: CollectionSpec | ComputedCollectionSpec,
        when: Sequence[PropertyEquals] = (),
    ) -> ComputedCollectionSpec:
        _require_name(name, "computed collection name")
        if name in self._collections or name in self._computed_collections:
            raise ValueError(f"collection {name!r} is already defined")
        if source.system is not self:
            raise ValueError("computed collection source belongs to another data-definition system")
        for condition in when:
            source.record_shape.require_property(condition.property)
        spec = ComputedCollectionSpec(
            system=self,
            name=name,
            source=source,
            conditions=tuple(when),
        )
        self._computed_collections[name] = spec
        return spec

    def container_builder(self) -> DDSContainerBuilder:
        from yidl.generation.data_container import DDSContainerBuilder

        return DDSContainerBuilder(self)

    def port(self, name: str, *, cardinality: CollectionCardinality) -> PortSpec:
        _require_label(name, "port name")
        if name in self._ports:
            raise ValueError(f"port {name!r} is already defined")
        spec = PortSpec(system=self, name=name, cardinality=cardinality)
        self._ports[name] = spec
        return spec

    def port_index(self, *, target: PropertySpec, order: PropertySpec) -> PortIndexSpec:
        if self._port_index is not None:
            raise ValueError("port index is already defined")
        if target.system is not self or order.system is not self:
            raise ValueError("port index properties must belong to this data-definition system")
        if target.value_type is not object:
            raise TypeError("port index target property must have value_type=object")
        if order.value_type is not int:
            raise TypeError("port index order property must have value_type=int")
        spec = PortIndexSpec(system=self, target=target, order=order)
        self._port_index = spec
        return spec

    def production(
        self,
        name: str,
        *,
        source: CollectionSpec | ComputedCollectionSpec | MatcherResultSource,
        target: CollectionSpec,
        when: Sequence[PropertyEquals] = (),
        identity: ValueExpression | object | None = None,
        values: Mapping[PropertySpec, ValueExpression | object] | None = None,
        policy: object | None = None,
    ) -> ProductionSpec:
        from yidl.generation.data_container import RejectDuplicate
        from yidl.generation.data_container import WritePolicy

        _require_name(name, "production name")
        if name in self._productions:
            raise ValueError(f"production {name!r} is already defined")
        if source.system is not self or target.system is not self:
            raise ValueError("production source and target must belong to the same data-definition system")
        if isinstance(target.record_shape, UnionSpec):
            raise ValueError("production target collections must use a concrete record")
        resolved_policy = RejectDuplicate if policy is None else policy
        if not isinstance(resolved_policy, WritePolicy):
            raise TypeError(
                f"production policy must be a WritePolicy, got {type(resolved_policy).__name__}"
            )
        if isinstance(source, MatcherResultSource):
            if when:
                raise ValueError("matcher-result productions do not support property when= conditions")
        else:
            for condition in when:
                source.record_shape.require_property(condition.property)
        resolved_values = {
            prop: _resolve_production_value_expression(
                source,
                _coerce_value_expression(expr),
            )
            for prop, expr in (values or {}).items()
        }
        for prop in resolved_values:
            target.record_shape.require_property(prop)
        identity_expression = (
            None
            if identity is None
            else _resolve_production_value_expression(
                source,
                _coerce_value_expression(identity),
            )
        )
        if target.identity is not None and identity_expression is None:
            identity_expression = resolved_values.get(target.identity)
        elif target.identity is None and identity_expression is not None:
            raise ValueError("identity= requires a target collection identity")
        if target.identity is not None and identity_expression is not None:
            resolved_values.setdefault(target.identity, identity_expression)
        missing = [
            prop.name
            for prop in target.record_shape.properties
            if prop.default is REQUIRED and prop not in resolved_values
        ]
        if missing:
            names = ", ".join(missing)
            raise ValueError(f"missing required target value: {names}")
        spec = ProductionSpec(
            system=self,
            name=name,
            source=source,
            target=target,
            conditions=tuple(when),
            identity=identity_expression,
            values=tuple(
                ProductionValue(prop, expression)
                for prop, expression in resolved_values.items()
            ),
            policy=resolved_policy,
        )
        self._productions[name] = spec
        return spec

    def production_group(
        self,
        name: str,
        *productions: ProductionSpec,
    ) -> ProductionGroupSpec:
        _require_name(name, "production group name")
        if name in self._production_groups:
            raise ValueError(f"production group {name!r} is already defined")
        for production in productions:
            if production.system is not self:
                raise ValueError("production group entries must belong to the same data-definition system")
        spec = ProductionGroupSpec(system=self, name=name, productions=tuple(productions))
        self._production_groups[name] = spec
        return spec

    def transform(
        self,
        name: str,
        *,
        source: CollectionSpec,
        target: CollectionSpec,
        when: Sequence[PropertyEquals] = (),
        values: Mapping[PropertySpec, ValueExpression] | None = None,
    ) -> TransformSpec:
        _require_name(name, "transform name")
        if name in self._transforms:
            raise ValueError(f"transform {name!r} is already defined")
        if source.system is not self or target.system is not self:
            raise ValueError("transform collections must belong to this data-definition system")
        resolved_values = values or {}
        for condition in when:
            source.record_spec.require_property(condition.property)
        for prop in resolved_values:
            target.record_spec.require_property(prop)
        spec = TransformSpec(
            system=self,
            name=name,
            source=source,
            target=target,
            conditions=tuple(when),
            values=tuple(
                TransformValue(prop, _coerce_value_expression(expr))
                for prop, expr in resolved_values.items()
            ),
        )
        self._transforms[name] = spec
        return spec


class PropertySpec:
    """Semantic property designator."""

    __slots__ = ("default", "name", "storage_name", "system", "value_type")

    def __init__(
        self,
        *,
        system: DataDefinitionSystem,
        name: str,
        value_type: type[object] | tuple[type[object], ...],
        default: object,
        storage_name: str,
    ) -> None:
        self.system = system
        self.name = name
        self.value_type = value_type
        self.default = default
        self.storage_name = storage_name

    def eq(self, value: object) -> PropertyEquals:
        self.validate(value)
        return PropertyEquals(self, value)

    def read(self) -> ReadProperty:
        return ReadProperty(self)

    def validate(self, value: object) -> object:
        if self.value_type is object:
            return value
        if not isinstance(value, self.value_type):
            raise TypeError(
                f"{self.name} must be {_type_name(self.value_type)}, "
                f"got {type(value).__name__}"
            )
        return value

    def value_from(self, record: object) -> object:
        return getattr(record, self.storage_name)

    def __repr__(self) -> str:
        return self.name


class RecordSpec:
    """Schema for one generated record class."""

    __slots__ = ("_record_class", "name", "properties", "system")

    def __init__(
        self,
        system: DataDefinitionSystem,
        name: str,
        properties: Sequence[PropertySpec],
    ) -> None:
        self.system = system
        self.name = name
        self.properties = _unique_properties(system, properties)
        self._record_class: type[object] | None = None

    def require_property(self, prop: PropertySpec) -> None:
        if prop.system is not self.system:
            raise ValueError(f"property {prop.name!r} belongs to another data-definition system")
        if prop not in self.properties:
            raise ValueError(f"record {self.name!r} has no property {prop.name!r}")

    def require_identity_property(self, prop: PropertySpec) -> None:
        self.require_property(prop)

    def record_class(self) -> type[object]:
        if self._record_class is None:
            self._record_class = _make_record_class(self)
        return self._record_class

    def bind_record_class(self, record_class: type[object]) -> type[object]:
        record_spec = getattr(record_class, "__dds_record_spec__", None)
        if record_spec is not self:
            raise TypeError(f"{record_class.__name__} is not bound to record {self.name}")
        self._record_class = record_class
        return record_class

    def record(self, **values: object) -> object:
        return self.record_class()(**values)

    def values_of(self, record: object) -> dict[PropertySpec, object]:
        self.validate_record(record)
        return {
            prop: prop.value_from(record)
            for prop in self.properties
        }

    def validate_record(self, record: object) -> None:
        record_spec = getattr(type(record), "__dds_record_spec__", None)
        if not _record_specs_match(record_spec, self):
            raise TypeError(f"expected {self.name} record, got {type(record).__name__}")

    def __repr__(self) -> str:
        return self.name


class UnionSpec:
    """Named union of concrete record variants."""

    __slots__ = ("_variants", "name", "system")

    def __init__(self, system: DataDefinitionSystem, name: str) -> None:
        self.system = system
        self.name = name
        self._variants: dict[str, RecordSpec] = {}

    @property
    def variants(self) -> tuple[RecordSpec, ...]:
        return tuple(self._variants.values())

    def variant(self, name: str, *properties: PropertySpec) -> RecordSpec:
        if name in self._variants:
            raise ValueError(f"union {self.name!r} already has variant {name!r}")
        spec = self.system.record(name, *properties)
        self._variants[name] = spec
        return spec

    def require_property(self, prop: PropertySpec) -> None:
        if prop.system is not self.system:
            raise ValueError(f"property {prop.name!r} belongs to another data-definition system")
        if not any(prop in variant.properties for variant in self.variants):
            raise ValueError(f"union {self.name!r} has no variant with property {prop.name!r}")

    def require_identity_property(self, prop: PropertySpec) -> None:
        if prop.system is not self.system:
            raise ValueError(f"property {prop.name!r} belongs to another data-definition system")
        missing = [
            variant.name
            for variant in self.variants
            if prop not in variant.properties
        ]
        if missing:
            names = ", ".join(missing)
            raise ValueError(
                f"union {self.name!r} identity property {prop.name!r} "
                f"must exist on all variants; missing from: {names}"
            )

    def record_spec_for(self, record: object) -> RecordSpec:
        record_spec = getattr(type(record), "__dds_record_spec__", None)
        for variant in self.variants:
            if _record_specs_match(record_spec, variant):
                return variant
        raise TypeError(f"expected {self.name} variant record, got {type(record).__name__}")

    def validate_record(self, record: object) -> None:
        self.record_spec_for(record)

    def __repr__(self) -> str:
        return self.name


class CollectionCardinality:
    """Behavior object for collection cardinality."""

    __slots__ = ()

    def allows_multiple(self) -> bool:
        raise NotImplementedError


class SingleCollectionCardinality(CollectionCardinality):
    __slots__ = ()

    def allows_multiple(self) -> bool:
        return False

    def __repr__(self) -> str:
        return "single"


class ManyCollectionCardinality(CollectionCardinality):
    __slots__ = ()

    def allows_multiple(self) -> bool:
        return True

    def __repr__(self) -> str:
        return "many"


class PortSpec:
    """Semantic build destination."""

    __slots__ = ("cardinality", "name", "system")

    def __init__(
        self,
        *,
        system: DataDefinitionSystem,
        name: str,
        cardinality: CollectionCardinality,
    ) -> None:
        self.system = system
        self.name = name
        self.cardinality = cardinality

    def of(self, owner_identity: object) -> PortAddress:
        return PortAddress(self, owner_identity)

    def __repr__(self) -> str:
        return self.name


class PortAddress:
    """One owner-scoped port target."""

    __slots__ = ("owner_identity", "port")

    def __init__(self, port: PortSpec, owner_identity: object) -> None:
        self.port = port
        self.owner_identity = owner_identity

    def __eq__(self, other: object) -> bool:
        return (
            isinstance(other, PortAddress)
            and self.port is other.port
            and self.owner_identity == other.owner_identity
        )

    def __repr__(self) -> str:
        return f"{self.port.name}.of({self.owner_identity!r})"


class PortIndexSpec:
    """Configured properties used for ordered port-child queries."""

    __slots__ = ("order", "system", "target")

    def __init__(
        self,
        *,
        system: DataDefinitionSystem,
        target: PropertySpec,
        order: PropertySpec,
    ) -> None:
        self.system = system
        self.target = target
        self.order = order


class CollectionSpec:
    """Schema for a singular or repeated record collection."""

    __slots__ = ("_record_shape", "cardinality", "identity", "name", "system")

    def __init__(
        self,
        *,
        system: DataDefinitionSystem,
        name: str,
        record: RecordSpec | UnionSpec,
        cardinality: CollectionCardinality,
        identity: PropertySpec | None,
    ) -> None:
        self.system = system
        self.name = name
        self._record_shape = record
        self.cardinality = cardinality
        self.identity = identity

    @property
    def record_spec(self) -> RecordSpec | UnionSpec:
        return self._record_shape

    @property
    def record_shape(self) -> RecordSpec | UnionSpec:
        return self._record_shape

    def record_instance(self, **values: object) -> object:
        if isinstance(self._record_shape, UnionSpec):
            raise TypeError(
                f"collection {self.name!r} uses union {self._record_shape.name!r}; "
                "create a concrete variant record instead"
            )
        return self._record_shape.record(**values)

    def record(self, **values: object) -> object:
        return self.record_instance(**values)

    def identity_of(self, record: object) -> object:
        self._record_shape.validate_record(record)
        if self.identity is None:
            return None
        return self.identity.value_from(record)

    def lookup_key(self, prop: PropertySpec, value: object) -> LookupKey:
        self._record_shape.require_property(prop)
        prop.validate(value)
        return LookupKey(self, prop, value)

    def fact_keys(self, record: object) -> tuple[LookupKey, ...]:
        record_spec = _record_spec_for_shape(self._record_shape, record)
        return tuple(
            self.lookup_key(prop, prop.value_from(record))
            for prop in record_spec.properties
        )

    def __repr__(self) -> str:
        return self.name


class ComputedCollectionSpec:
    """Named filtered view over another collection source."""

    __slots__ = ("conditions", "name", "source", "system")

    def __init__(
        self,
        *,
        system: DataDefinitionSystem,
        name: str,
        source: CollectionSpec | ComputedCollectionSpec,
        conditions: tuple[PropertyEquals, ...],
    ) -> None:
        self.system = system
        self.name = name
        self.source = source
        self.conditions = conditions

    @property
    def record_spec(self) -> RecordSpec | UnionSpec:
        return self.source.record_spec

    @property
    def record_shape(self) -> RecordSpec | UnionSpec:
        return self.source.record_shape

    @property
    def identity(self) -> PropertySpec | None:
        return self.source.identity

    def identity_of(self, record: object) -> object:
        return self.source.identity_of(record)

    def lookup_key(self, prop: PropertySpec, value: object) -> LookupKey:
        return self.source.lookup_key(prop, value)

    def fact_keys(self, record: object) -> tuple[LookupKey, ...]:
        return self.source.fact_keys(record)

    def matches(self, record: object) -> bool:
        if isinstance(self.source, ComputedCollectionSpec) and not self.source.matches(record):
            return False
        self.record_shape.validate_record(record)
        return all(condition.matches(record) for condition in self.conditions)

    def __repr__(self) -> str:
        return self.name


class MatcherResultSource:
    """Production source over all results from a matcher."""

    __slots__ = ("matcher", "name", "system")

    def __init__(self, matcher: object) -> None:
        self.matcher = matcher
        self.name = f"{getattr(matcher, 'name')}.results"
        self.system = getattr(matcher, "system")

    def __repr__(self) -> str:
        return self.name


class LookupKey:
    """Hashable key used by an equality-only rule index."""

    __slots__ = ("collection", "property", "value")

    def __init__(
        self,
        collection: CollectionSpec,
        property: PropertySpec,
        value: object,
    ) -> None:
        self.collection = collection
        self.property = property
        self.value = value

    def __eq__(self, other: object) -> bool:
        return (
            isinstance(other, LookupKey)
            and self.collection is other.collection
            and self.property is other.property
            and self.value == other.value
        )

    def __hash__(self) -> int:
        return hash((id(self.collection), id(self.property), self.value))

    def __repr__(self) -> str:
        return f"{self.collection}.{self.property} == {self.value!r}"


class PropertyEquals:
    """Equality-only condition over one property."""

    __slots__ = ("property", "value")

    def __init__(self, property: PropertySpec, value: object) -> None:
        self.property = property
        self.value = value

    def matches(self, record: object) -> bool:
        if not hasattr(record, self.property.storage_name):
            return False
        return self.property.value_from(record) == self.value

    def lookup_key(self, collection: CollectionSpec) -> LookupKey:
        return collection.lookup_key(self.property, self.value)

    def __repr__(self) -> str:
        return f"{self.property} == {self.value!r}"


class ValueExpression:
    """Expression used by transform specs to compute target values."""

    __slots__ = ()

    def evaluate(self, source: object) -> object:
        raise NotImplementedError


class LiteralValue(ValueExpression):
    __slots__ = ("value",)

    def __init__(self, value: object) -> None:
        self.value = value

    def evaluate(self, source: object) -> object:
        del source
        return self.value


class ReadProperty(ValueExpression):
    __slots__ = ("property",)

    def __init__(self, property: PropertySpec) -> None:
        self.property = property

    def evaluate(self, source: object) -> object:
        return self.property.value_from(source)


class ComputedValue(ValueExpression):
    """Named callback for derived values.

    This is intentionally explicit.  It gives callback-based derivations a
    semantic label instead of hiding them as anonymous rule-engine code.
    """

    __slots__ = ("func", "name")

    def __init__(self, name: str, func: Callable[[object], object]) -> None:
        _require_label(name, "computed value name")
        self.name = name
        self.func = func

    def evaluate(self, source: object) -> object:
        return self.func(source)

    def __repr__(self) -> str:
        return self.name


class MatchResource(ValueExpression):
    """Resource selected by a matcher result."""

    __slots__ = ()

    def evaluate(self, source: object) -> object:
        return source.resource


class MatchTupleValue(ValueExpression):
    """Value from a matcher result tuple."""

    __slots__ = ("index",)

    def __init__(self, index: int) -> None:
        if index < 0:
            raise ValueError("matcher tuple value index must be non-negative")
        self.index = index

    def evaluate(self, source: object) -> object:
        return source.values[self.index]


class MatchRecordProperty(ValueExpression):
    """Property read from one matcher input record."""

    __slots__ = ("input_index", "input_name", "property")

    def __init__(
        self,
        input_name: str,
        property: PropertySpec,
        *,
        input_index: int | None = None,
    ) -> None:
        _require_name(input_name, "matcher input name")
        self.input_name = input_name
        self.property = property
        self.input_index = input_index

    def bind(self, input_index: int) -> MatchRecordProperty:
        return MatchRecordProperty(
            self.input_name,
            self.property,
            input_index=input_index,
        )

    def evaluate(self, source: object) -> object:
        if self.input_index is None:
            raise RuntimeError("matcher record expression is not bound to an input")
        return self.property.value_from(source.records[self.input_index])


class _MatchRecordAccessor:
    __slots__ = ("input_name",)

    def __init__(self, input_name: str) -> None:
        _require_name(input_name, "matcher input name")
        self.input_name = input_name

    def prop(self, property: PropertySpec) -> MatchRecordProperty:
        return MatchRecordProperty(self.input_name, property)


class _MatchExpressionFactory:
    __slots__ = ()

    def resource(self) -> MatchResource:
        return MatchResource()

    def record(self, input_name: str) -> _MatchRecordAccessor:
        return _MatchRecordAccessor(input_name)

    def value(self, index: int) -> MatchTupleValue:
        return MatchTupleValue(index)


match = _MatchExpressionFactory()


def literal(value: object) -> LiteralValue:
    return LiteralValue(value)


def read(prop: PropertySpec) -> ReadProperty:
    return ReadProperty(prop)


def call(name: str, func: Callable[[object], object]) -> ComputedValue:
    return ComputedValue(name, func)


class TransformValue:
    __slots__ = ("expression", "property")

    def __init__(self, property: PropertySpec, expression: ValueExpression) -> None:
        self.property = property
        self.expression = expression


class TransformSpec:
    """Specification for deriving target collection records from source records."""

    __slots__ = ("conditions", "name", "source", "system", "target", "values")

    def __init__(
        self,
        *,
        system: DataDefinitionSystem,
        name: str,
        source: CollectionSpec,
        target: CollectionSpec,
        conditions: tuple[PropertyEquals, ...],
        values: tuple[TransformValue, ...],
    ) -> None:
        self.system = system
        self.name = name
        self.source = source
        self.target = target
        self.conditions = conditions
        self.values = values

    def matches(self, source: object) -> bool:
        self.source.record_spec.validate_record(source)
        return all(condition.matches(source) for condition in self.conditions)

    def derive(self, source: object) -> object | None:
        if isinstance(self.target.record_shape, UnionSpec):
            raise ValueError("transform target collections must use a concrete record shape")
        if not self.matches(source):
            return None
        values = {
            item.property.storage_name: item.property.validate(
                item.expression.evaluate(source)
            )
            for item in self.values
        }
        return self.target.record(**values)

    def lookup_keys(self) -> tuple[LookupKey, ...]:
        return tuple(
            condition.lookup_key(self.source)
            for condition in self.conditions
        )

    def __repr__(self) -> str:
        return self.name


class ProductionValue:
    __slots__ = ("expression", "property")

    def __init__(self, property: PropertySpec, expression: ValueExpression) -> None:
        self.property = property
        self.expression = expression


class ProductionSpec:
    """Specification for generated builder operations."""

    __slots__ = (
        "conditions",
        "identity",
        "name",
        "policy",
        "source",
        "system",
        "target",
        "values",
    )

    def __init__(
        self,
        *,
        system: DataDefinitionSystem,
        name: str,
        source: CollectionSpec | ComputedCollectionSpec | MatcherResultSource,
        target: CollectionSpec,
        conditions: tuple[PropertyEquals, ...],
        identity: ValueExpression | None,
        values: tuple[ProductionValue, ...],
        policy: object,
    ) -> None:
        self.system = system
        self.name = name
        self.source = source
        self.target = target
        self.conditions = conditions
        self.identity = identity
        self.values = values
        self.policy = policy

    def matches(self, source: object) -> bool:
        if isinstance(self.source, MatcherResultSource):
            return True
        self.source.record_shape.validate_record(source)
        return all(condition.matches(source) for condition in self.conditions)

    def make_record(self, source: object) -> object | None:
        if not self.matches(source):
            return None
        values = {
            item.property.storage_name: item.property.validate(
                item.expression.evaluate(source)
            )
            for item in self.values
        }
        return self.target.record(**values)

    def __repr__(self) -> str:
        return self.name


class ProductionGroupSpec:
    """Ordered set of productions run as one generated operation group."""

    __slots__ = ("name", "productions", "system")

    def __init__(
        self,
        *,
        system: DataDefinitionSystem,
        name: str,
        productions: tuple[ProductionSpec, ...],
    ) -> None:
        self.system = system
        self.name = name
        self.productions = productions


class _DdsPropertyDefinition:
    __slots__ = ("default", "name", "storage_name", "value_type")

    def __init__(
        self,
        name: str,
        value_type: type[object] | tuple[type[object], ...],
        *,
        default: object,
        storage_name: str | None,
    ) -> None:
        self.name = name
        self.value_type = value_type
        self.default = default
        self.storage_name = storage_name


def dds_property(
    name: str,
    value_type: type[object] | tuple[type[object], ...],
    *,
    default: object = REQUIRED,
    storage_name: str | None = None,
) -> _DdsPropertyDefinition:
    return _DdsPropertyDefinition(
        name,
        value_type,
        default=default,
        storage_name=storage_name,
    )


def dds_record_spec(name: str, *properties: _DdsPropertyDefinition) -> RecordSpec:
    dds = DataDefinitionSystem()
    resolved = [
        dds.property(
            prop.name,
            prop.value_type,
            default=prop.default,
            storage_name=prop.storage_name,
        )
        for prop in properties
    ]
    return dds.record(name, *resolved)


def _compile_template(source: str) -> astichi.Composable:
    return astichi.compile(textwrap.dedent(source).strip() + "\n")


_RECORD_CLASS = _compile_template(
    """
from yidl.generation.data_def_sys import REQUIRED, dds_property, dds_record_spec

class record_class_name__astichi_arg__:
    __slots__ = astichi_bind_external(slot_names)
    __dds_record_spec__ = dds_record_spec(
        astichi_bind_external(record_name),
        astichi_hole(property_specs),
    )
    astichi_hole(body)
"""
)

_EMPTY_RECORD_CLASS = _compile_template(
    """
from yidl.generation.data_def_sys import dds_record_spec

class record_class_name__astichi_arg__:
    __slots__ = ()
    __dds_record_spec__ = dds_record_spec(astichi_bind_external(record_name))

    def __init__(self):
        pass

    def __repr__(self):
        return astichi_bind_external(record_name) + "()"
"""
)

_REQUIRED_PROPERTY_SPEC = _compile_template(
    """
dds_property(
    astichi_bind_external(property_name),
    astichi_ref(external=value_type_path),
    default=REQUIRED,
    storage_name=astichi_bind_external(storage_name),
)
"""
)

_DEFAULTED_PROPERTY_SPEC = _compile_template(
    """
dds_property(
    astichi_bind_external(property_name),
    astichi_ref(external=value_type_path),
    default=astichi_bind_external(default_value),
    storage_name=astichi_bind_external(storage_name),
)
"""
)

_FIELD_ANNOTATION = _compile_template(
    """
field_name__astichi_arg__: astichi_ref(external=value_type_path)
"""
)

_INIT_METHOD = _compile_template(
    """
def __init__(self, params__astichi_param_hole__):
    astichi_hole(body)
"""
)

_REQUIRED_PARAM = _compile_template(
    """
def astichi_params(*, field_name__astichi_arg__: astichi_ref(external=value_type_path)):
    pass
"""
)

_DEFAULTED_PARAM = _compile_template(
    """
def astichi_params(
    *,
    field_name__astichi_arg__: astichi_ref(external=value_type_path)
    = astichi_bind_external(default_value),
):
    pass
"""
)

_VALIDATE_TYPE = _compile_template(
    """
if not isinstance(
    astichi_pass(field_name, outer_bind=True),
    astichi_ref(external=value_type_path),
):
    raise TypeError(
        astichi_bind_external(error_prefix)
        + type(astichi_pass(field_name, outer_bind=True)).__name__
    )
"""
)

_INIT_ASSIGN = _compile_template(
    """
object.__setattr__(
    astichi_pass(self, outer_bind=True),
    astichi_bind_external(field_name_literal),
    astichi_pass(field_name, outer_bind=True),
)
"""
)

_SETATTR_METHOD = _compile_template(
    """
def __setattr__(self, name, value):
    if name in astichi_bind_external(frozen_names):
        raise AttributeError(astichi_bind_external(error_message))
    object.__setattr__(self, name, value)
"""
)

_REPR_METHOD = _compile_template(
    """
def __repr__(self):
    pieces = []
    astichi_hole(parts)
    return astichi_bind_external(record_name) + "(" + ", ".join(pieces) + ")"
"""
)

_REPR_PART = _compile_template(
    """
astichi_pass(pieces, outer_bind=True).append(
    astichi_bind_external(label)
    + repr(astichi_pass(self, outer_bind=True).astichi_ref(external=field_path))
)
"""
)


def _make_record_class(spec: RecordSpec) -> type[object]:
    class_name = spec.name
    namespace: dict[str, object] = {"__name__": __name__}
    composable = _materialize_record_class(spec, namespace=namespace)
    return _execute_record_class(composable, class_name, namespace)


def _emit_record_class_source(spec: RecordSpec) -> str:
    return _materialize_record_class(spec).emit(provenance=False)


def _materialize_record_class(
    spec: RecordSpec,
    *,
    namespace: dict[str, object] | None = None,
) -> astichi.Composable:
    class_name = spec.name
    if not spec.properties:
        return (
            _EMPTY_RECORD_CLASS
            .bind(
                record_name=class_name,
            )
            .bind_identifier(record_class_name=class_name)
            .with_keep_names([class_name])
            .materialize()
        )

    builder = astichi.build()
    builder.add.Root(
        _RECORD_CLASS.bind(
            record_name=spec.name,
            slot_names=tuple(prop.storage_name for prop in spec.properties),
        ),
        arg_names={"record_class_name": class_name},
        keep_names=[class_name],
    )
    builder.add.InitMethod(_INIT_METHOD)
    builder.add.SetAttrMethod(
        _SETATTR_METHOD.bind(
            frozen_names=tuple(prop.storage_name for prop in spec.properties),
            error_message=f"{spec.name} records are immutable",
        ),
        keep_names=["AttributeError", "object"],
    )
    builder.add.ReprMethod(_REPR_METHOD.bind(record_name=class_name))

    body_base_order = len(spec.properties)
    builder.Root.body.add.InitMethod(order=body_base_order)
    builder.Root.body.add.SetAttrMethod(order=body_base_order + 1)
    builder.Root.body.add.ReprMethod(order=body_base_order + 2)

    for order, prop in enumerate(spec.properties):
        _add_record_property(builder, namespace, order, prop)

    return builder.build().materialize()


def _add_record_property(
    builder: astichi.BuilderHandle,
    namespace: dict[str, object] | None,
    order: int,
    prop: PropertySpec,
) -> None:
    value_type_path = _value_type_ref_path(prop.value_type)
    property_spec = _REQUIRED_PROPERTY_SPEC
    property_bind: dict[str, object] = {
        "property_name": prop.name,
        "storage_name": prop.storage_name,
        "value_type_path": value_type_path,
    }
    if prop.default is not REQUIRED:
        property_spec = _DEFAULTED_PROPERTY_SPEC
        property_bind["default_value"] = prop.default

    builder.add.PropertySpec[order](
        property_spec.bind(property_bind),
        keep_names=[
            "REQUIRED",
            "dds_property",
            *_value_type_keep_names(prop.value_type),
        ],
    )
    builder.Root.property_specs.add.PropertySpec[order](order=order)

    builder.add.FieldAnnotation[order](
        _FIELD_ANNOTATION.bind(value_type_path=value_type_path),
        arg_names={"field_name": prop.storage_name},
        keep_names=_value_type_keep_names(prop.value_type),
    )
    builder.Root.body.add.FieldAnnotation[order](order=order)

    param_piece = _REQUIRED_PARAM
    param_bind: dict[str, object] = {"value_type_path": value_type_path}
    if prop.default is not REQUIRED:
        param_piece = _DEFAULTED_PARAM
        param_bind["default_value"] = prop.default
    builder.add.Param[order](
        param_piece.bind(param_bind),
        arg_names={"field_name": prop.storage_name},
        keep_names=[
            prop.storage_name,
            *_value_type_keep_names(prop.value_type),
        ],
    )
    builder.InitMethod.params.add.Param[order](order=order)

    if prop.value_type is not object:
        builder.add.TypeCheck[order](
            _VALIDATE_TYPE.bind(
                error_prefix=(
                    f"{prop.name} must be {_type_name(prop.value_type)}, got "
                ),
                value_type_path=value_type_path,
            ),
            arg_names={"field_name": prop.storage_name},
            keep_names=[
                "TypeError",
                "isinstance",
                "type",
                *_value_type_keep_names(prop.value_type),
            ],
        )
        builder.InitMethod.body.add.TypeCheck[order](order=order)

    builder.add.InitAssign[order](
        _INIT_ASSIGN.bind(
            field_name_literal=prop.storage_name,
        ),
        arg_names={"field_name": prop.storage_name},
        keep_names=["object"],
    )
    builder.InitMethod.body.add.InitAssign[order](order=order)

    builder.add.ReprPart[order](
        _REPR_PART.bind(
            field_path=prop.storage_name,
            label=f"{prop.storage_name}=",
        ),
        keep_names=["repr"],
    )
    builder.ReprMethod.parts.add.ReprPart[order](order=order)


def _execute_record_class(
    composable: astichi.Composable,
    class_name: str,
    namespace: dict[str, object],
) -> type[object]:
    code = compile(composable.tree, f"<yidl.dds.{class_name}>", "exec", dont_inherit=True)
    exec(code, namespace)
    record_class = namespace[class_name]
    if not isinstance(record_class, type):
        raise TypeError(f"generated {class_name} is not a class")
    return record_class


def _value_type_ref_path(value_type: type[object] | tuple[type[object], ...]) -> str:
    if isinstance(value_type, tuple):
        raise ValueError("tuple value-type emission is not implemented yet")
    if value_type.__module__ != "builtins":
        raise ValueError(
            f"cannot emit non-builtin value type {value_type.__module__}.{value_type.__qualname__}"
        )
    return value_type.__qualname__


def _value_type_keep_names(value_type: type[object] | tuple[type[object], ...]) -> tuple[str, ...]:
    return (_value_type_ref_path(value_type),)


def _record_specs_match(candidate: object, expected: RecordSpec) -> bool:
    if not isinstance(candidate, RecordSpec):
        return False
    if candidate.name != expected.name:
        return False
    if len(candidate.properties) != len(expected.properties):
        return False
    return all(
        _property_specs_match(left, right)
        for left, right in zip(candidate.properties, expected.properties, strict=True)
    )


def _property_specs_match(candidate: PropertySpec, expected: PropertySpec) -> bool:
    if candidate.name != expected.name:
        return False
    if candidate.storage_name != expected.storage_name:
        return False
    if candidate.value_type is not expected.value_type:
        return False
    if candidate.default is REQUIRED or expected.default is REQUIRED:
        return candidate.default is expected.default
    return candidate.default == expected.default


def _record_spec_for_shape(
    shape: RecordSpec | UnionSpec,
    record: object,
) -> RecordSpec:
    if isinstance(shape, UnionSpec):
        return shape.record_spec_for(record)
    shape.validate_record(record)
    return shape


def _coerce_value_expression(value: ValueExpression | object) -> ValueExpression:
    if isinstance(value, ValueExpression):
        return value
    return LiteralValue(value)


def _resolve_production_value_expression(
    source: CollectionSpec | ComputedCollectionSpec | MatcherResultSource,
    expression: ValueExpression,
) -> ValueExpression:
    if isinstance(source, MatcherResultSource):
        return _resolve_matcher_result_expression(source, expression)
    if isinstance(expression, _MATCH_EXPRESSIONS):
        raise ValueError("match expressions require source=matcher.results()")
    if isinstance(expression, ReadProperty):
        source.record_shape.require_property(expression.property)
    return expression


def _resolve_matcher_result_expression(
    source: MatcherResultSource,
    expression: ValueExpression,
) -> ValueExpression:
    if isinstance(expression, ReadProperty):
        raise ValueError(
            "matcher-result productions must read input records with "
            "match.record(...).prop(...)"
        )
    if isinstance(expression, MatchRecordProperty):
        input_spec = _matcher_input_named(source.matcher, expression.input_name)
        input_spec.source.record_shape.require_property(expression.property)
        return expression.bind(input_spec.index)
    if isinstance(expression, MatchTupleValue):
        tuple_length = len(source.matcher.tuple_schema)
        if expression.index >= tuple_length:
            raise ValueError(
                f"matcher tuple value index {expression.index} is out of range "
                f"for matcher {source.matcher.name!r}"
            )
    return expression


_MATCH_EXPRESSIONS = (MatchResource, MatchRecordProperty, MatchTupleValue)


def _matcher_input_named(matcher: object, name: str) -> object:
    for input_spec in matcher.inputs:
        if input_spec.name == name:
            return input_spec
    raise ValueError(f"matcher {matcher.name!r} has no input {name!r}")


def _unique_properties(
    system: DataDefinitionSystem,
    properties: Sequence[PropertySpec],
) -> tuple[PropertySpec, ...]:
    seen: set[PropertySpec] = set()
    storage_names: set[str] = set()
    resolved: list[PropertySpec] = []
    for prop in properties:
        if prop.system is not system:
            raise ValueError(f"property {prop.name!r} belongs to another data-definition system")
        if prop in seen:
            continue
        if prop.storage_name in storage_names:
            raise ValueError(f"duplicate storage name {prop.storage_name!r}")
        seen.add(prop)
        storage_names.add(prop.storage_name)
        resolved.append(prop)
    return tuple(resolved)


def _require_name(value: str, label: str) -> None:
    if not isinstance(value, str) or not value.isidentifier():
        raise ValueError(f"{label} must be a valid identifier: {value!r}")


def _require_label(value: str, label: str) -> None:
    if not isinstance(value, str) or not value:
        raise ValueError(f"{label} must be a non-empty string")


def _to_snake_case(name: str) -> str:
    return re.sub(r"(?<!^)(?=[A-Z])", "_", name).lower()


def _type_name(value_type: type[object] | tuple[type[object], ...]) -> str:
    if isinstance(value_type, tuple):
        return " or ".join(item.__name__ for item in value_type)
    return value_type.__name__


__all__ = [
    "CollectionCardinality",
    "CollectionSpec",
    "ComputedCollectionSpec",
    "ComputedValue",
    "DataDefinitionSystem",
    "LookupKey",
    "MatchRecordProperty",
    "MatchResource",
    "MatchTupleValue",
    "MatcherResultSource",
    "ManyCollectionCardinality",
    "PortAddress",
    "PortIndexSpec",
    "PortSpec",
    "ProductionGroupSpec",
    "ProductionSpec",
    "ProductionValue",
    "PropertyEquals",
    "PropertySpec",
    "REQUIRED",
    "ReadProperty",
    "RecordSpec",
    "RequiredValue",
    "SingleCollectionCardinality",
    "TransformSpec",
    "UnionSpec",
    "call",
    "dds_property",
    "dds_record_spec",
    "literal",
    "match",
    "read",
]
