"""Declarative data-definition system for rule-driven generation.

The data-definition system describes record shapes, collections, equality
lookup facts, and collection derivations.  It intentionally does not store
runtime records.  Record classes generated from this schema are plain slotted
containers, not dataclasses.
"""

from __future__ import annotations

from collections.abc import Callable, Mapping, Sequence
import re


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
        "_properties",
        "_records",
        "_transforms",
        "many",
        "single",
    )

    def __init__(self) -> None:
        self._properties: dict[str, PropertySpec] = {}
        self._records: dict[str, RecordSpec] = {}
        self._collections: dict[str, CollectionSpec] = {}
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
    def collections(self) -> tuple[CollectionSpec, ...]:
        return tuple(self._collections.values())

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
        spec = RecordSpec(self, name, properties)
        self._records[name] = spec
        return spec

    def collection(
        self,
        name: str,
        record: RecordSpec,
        *,
        cardinality: CollectionCardinality,
        identity: PropertySpec | None = None,
    ) -> CollectionSpec:
        _require_name(name, "collection name")
        if name in self._collections:
            raise ValueError(f"collection {name!r} is already defined")
        if record.system is not self:
            raise ValueError("collection record belongs to another data-definition system")
        if identity is not None:
            record.require_property(identity)
        spec = CollectionSpec(
            system=self,
            name=name,
            record=record,
            cardinality=cardinality,
            identity=identity,
        )
        self._collections[name] = spec
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

    def record_class(self) -> type[object]:
        if self._record_class is None:
            self._record_class = _make_record_class(self)
        return self._record_class

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
        if record_spec is not self:
            raise TypeError(f"expected {self.name} record, got {type(record).__name__}")

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


class CollectionSpec:
    """Schema for a singular or repeated record collection."""

    __slots__ = ("_record_spec", "cardinality", "identity", "name", "system")

    def __init__(
        self,
        *,
        system: DataDefinitionSystem,
        name: str,
        record: RecordSpec,
        cardinality: CollectionCardinality,
        identity: PropertySpec | None,
    ) -> None:
        self.system = system
        self.name = name
        self._record_spec = record
        self.cardinality = cardinality
        self.identity = identity

    @property
    def record_spec(self) -> RecordSpec:
        return self._record_spec

    def record_instance(self, **values: object) -> object:
        return self._record_spec.record(**values)

    def record(self, **values: object) -> object:
        return self.record_instance(**values)

    def identity_of(self, record: object) -> object:
        self._record_spec.validate_record(record)
        if self.identity is None:
            return None
        return self.identity.value_from(record)

    def lookup_key(self, prop: PropertySpec, value: object) -> LookupKey:
        self._record_spec.require_property(prop)
        prop.validate(value)
        return LookupKey(self, prop, value)

    def fact_keys(self, record: object) -> tuple[LookupKey, ...]:
        self._record_spec.validate_record(record)
        return tuple(
            self.lookup_key(prop, prop.value_from(record))
            for prop in self._record_spec.properties
        )

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


def _make_record_class(spec: RecordSpec) -> type[object]:
    storage_names = tuple(prop.storage_name for prop in spec.properties)
    slots = (*storage_names, "_dds_frozen")

    def __init__(self: object, **values: object) -> None:
        remaining = dict(values)
        for prop in spec.properties:
            if prop.storage_name in remaining:
                raw_value = remaining.pop(prop.storage_name)
            elif prop.default is not REQUIRED:
                raw_value = prop.default
            else:
                raise TypeError(
                    f"missing required value for {spec.name}.{prop.storage_name}"
                )
            object.__setattr__(self, prop.storage_name, prop.validate(raw_value))
        if remaining:
            names = tuple(sorted(remaining))
            raise TypeError(f"unexpected values for {spec.name}: {names!r}")
        object.__setattr__(self, "_dds_frozen", True)

    def __setattr__(self: object, name: str, value: object) -> None:
        if getattr(self, "_dds_frozen", False):
            raise AttributeError(f"{spec.name} records are immutable")
        object.__setattr__(self, name, value)

    def __repr__(self: object) -> str:
        values = ", ".join(
            f"{prop.storage_name}={getattr(self, prop.storage_name)!r}"
            for prop in spec.properties
        )
        return f"{spec.name}Record({values})"

    namespace = {
        "__dds_record_spec__": spec,
        "__init__": __init__,
        "__module__": __name__,
        "__repr__": __repr__,
        "__setattr__": __setattr__,
        "__slots__": slots,
    }
    return type(f"{spec.name}Record", (), namespace)


def _coerce_value_expression(value: ValueExpression | object) -> ValueExpression:
    if isinstance(value, ValueExpression):
        return value
    return LiteralValue(value)


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
    "ComputedValue",
    "DataDefinitionSystem",
    "LookupKey",
    "ManyCollectionCardinality",
    "PropertyEquals",
    "PropertySpec",
    "REQUIRED",
    "ReadProperty",
    "RecordSpec",
    "RequiredValue",
    "SingleCollectionCardinality",
    "TransformSpec",
]
