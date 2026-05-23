# YIDL Data Container Design

## Purpose

The data-definition system (DDS) defines data shapes and data operations. It
does not hold decoration-time data.

`DDSContainer` is the decoration-time holder for records that conform to a
generated DDS specification module. It is intentionally small: a typed fact
store with stable query and write primitives plus generated named collection
views. It is not the semantic interpreter for every DDS operation.

The specification phase should be able to emit a normal Python module. That
module contains:

- generated record classes
- generated union descriptors for heterogeneous record sets
- generated collection/property descriptors
- generated computed-collection descriptors for named filtered views
- generated operation functions for filters, derived properties, and derived
  collections

At decoration time, YIDL imports or uses that generated module, populates a
container with actual class/field/facade records, runs the generated operation
functions, freezes the result, evaluates rule-point providers against the
resolved data, and then feeds the selected Astichi resources to the build
mapper.

## Phase Split

Specification phase:

- defines `PropertySpec`, `RecordSpec`, `CollectionSpec`, and operation specs
- generates Python source or AST for record classes and operation functions
- may precompile Astichi templates used by operation generation
- does not hold data for a particular decorated class

Decoration phase:

- creates one container builder for one decorated class
- inserts actual input records collected from the decorated class and active
  facades/capsules
- calls generated operation functions from the spec module
- freezes to an immutable resolved container
- queries the frozen data through generated named collection views
- evaluates rule-point providers and match tuples
- uses resolved providers to select Astichi generation resources

This keeps YIDL's decorator path deterministic and avoids parser calls over
fresh per-field source during decoration.

## Boundary

DDS/specification module owns semantics:

- what record classes exist
- which named unions group record variants
- what collections exist
- which Eq-only filters are meaningful
- which computed collections are named views over stored collections
- which derived properties exist
- which derived collection records are produced
- which operation order is required

`DDSContainerBuilder` owns mutable decoration-time data:

- actual record values
- collection membership
- single-vs-many cardinality enforcement
- identity indexes
- equality fact indexes
- primitive add/query APIs used by generated operation functions

`DDSContainer` owns immutable resolved data:

- final records
- final identity indexes
- final fact indexes
- generated named collection views
- read-only query APIs consumed by operation functions, rule providers, and the
  Astichi build mapper

The container must not define schema or infer generation semantics. It is bound
to one generated DDS specification and rejects records or collections from
another specification.

## Record Unions

Some YIDL inputs are one logical collection with multiple concrete record
shapes. Field specifiers are the first important case: `classvar`,
`transient`, `initvar`, `local`, `binding`, `owned`, `managed`, and
`transaction_manager` are all field specifier inputs, but they do not all carry
the same properties.

DDS models this as a union:

```python
FieldSpecs = dds.union("FieldSpecs")

PlainField = FieldSpecs.variant("PlainField", Name, Annotation, Default, Init)
ManagedField = FieldSpecs.variant("ManagedField", Name, Annotation, TxKey)
ClassVarField = FieldSpecs.variant("ClassVarField", Name, Annotation, Default)

Fields = dds.collection("Fields", FieldSpecs, cardinality=dds.many, identity=Name)
```

The capitalized names are property specifiers. The lower-case constructor
keywords on generated records are storage names and values:

```python
field = PlainField.record(name="count", annotation=int, default=0, init=True)
```

Rules for unions:

- each variant is a concrete record spec with its own generated record class
- a collection may accept either one concrete record spec or one union
- collection identity for a union must exist on every variant
- facts are indexed from the actual variant record that was stored
- querying a property that only exists on some variants is allowed; variants
  without that property simply do not contribute matching facts
- creating a record through a union collection is rejected; callers must create
  a concrete variant record

This avoids one giant sparse `FieldSpec` record while preserving one natural
`Fields` collection for rules that operate over all fields.

## Generated Operation Functions

The container should not expose APIs such as:

```python
container.apply_transform(transform)
```

That makes the container an interpreter for DDS semantics. Instead, DDS emits
operation functions that use container primitives:

```python
def derive_init_fields(container):
    for field in container.matching(Fields, Init.eq(True)):
        container.add(InitFields, InitField(name=field.name))
```

For a richer operation:

```python
def derive_managed_names(container):
    for field in container.matching(Fields, IsManaged.eq(True)):
        container.add(
            ManagedNames,
            ManagedName(
                name=field.name,
                working_name="_" + field.name + "_working",
                current_name="_" + field.name + "_current",
            ),
        )
```

The spec module can expose a single generated runner:

```python
def build_container(builder):
    derive_field_kind_facts(builder)
    derive_init_fields(builder)
    derive_slot_names(builder)
    return builder.freeze()
```

or a tuple of operation functions:

```python
DDS_OPERATIONS = (
    derive_field_kind_facts,
    derive_init_fields,
    derive_slot_names,
)
```

The exact packaging is an implementation decision. The rule is that semantics
live in generated operation code, while the container supplies storage and
lookup primitives.

## Computed Collections

Some named data sets should not be materialized as stored collections. They are
just stable, named filters over another collection.

Examples:

- fields that belong in the generated `__init__` signature
- fields that contribute `__slots__`
- fields that belong to transaction id `1`
- managed fields visible on a given facade

DDS should model these as computed collections:

```python
InitSignatureFields = dds.computed_collection(
    "InitSignatureFields",
    source=Fields,
    when=(Init.eq(True),),
)

TxOneFields = dds.computed_collection(
    "TxOneFields",
    source=Fields,
    when=(TxId.eq(1),),
)
```

A computed collection:

- has a name
- has a source collection
- has Eq-only filter conditions
- is not stored as its own record set
- is evaluated by querying the final container facts
- returns source records, not new records

The generated spec module should expose computed collections as named views on
the final container:

```python
dds_container = builder.build()

for field in dds_container.InitSignatureFields.sequence():
    ...

for field in dds_container.TxOneFields.sequence():
    ...
```

The public/internal generation-facing API should prefer named views over
descriptor-passing calls. Lower-level descriptor APIs may still exist privately
for generated implementation code.

The generated implementation of a computed collection can be a direct filtered
generator over the source collection:

```python
class TxOneFieldsView:
    def sequence(self):
        return (
            field
            for field in self._container.Fields.container
            if hasattr(field, "tx_id") and field.tx_id == 1
        )
```

This is often more direct than maintaining a generic fact index. If a computed
collection becomes hot, the generated implementation can switch to an indexed
lookup without changing the view API.

Computed collections are different from derived collections:

- **computed collection**: named view over existing records
- **derived collection**: generated operation creates new records and stores
  them in the container builder

Use computed collections when the target is only a selection. Use derived
collections when new record shape, new identity, or new values are needed.

## Record Creation

Records should be creatable through generated collection/record descriptors:

```python
field = Fields.record(name="count", init=True)
builder.add(Fields, field)
```

The builder may also provide a convenience method:

```python
field = builder.record(Fields, name="count", init=True)
builder.add(Fields, field)
```

The second form is only shorthand for the generated record class. It must not
create ad hoc record shapes.

Open decision: whether `builder.add(Fields, name="count", init=True)` should be
allowed. The safer first surface is explicit record construction, because it
makes generated record types visible in tests and diagnostics.

## Mutability Model

Use a build/freeze model.

`DDSContainerBuilder` is mutable:

- insert input records
- insert derived records from generated operations
- update fact indexes as records are added
- reject invalid data immediately

`DDSContainer` is immutable:

- no `add`
- no replacement
- no lazy operation execution
- query-only access

This avoids an always-mutable list of field values. All decoration-time inputs
and derived facts are finalized before the Astichi build mapper reads them.

## Final Container Contract

The final container is the only object consumed by the Astichi build mapper.
It must be deterministic and read-only.

Required behavior:

- stores a reference to the generated DDS specification module or schema object
- exposes generated named views for every concrete and computed collection
- exposes records in stable insertion/order policy defined by each view
- exposes identity lookup for collections that declare identity
- may expose Eq-only fact lookup as an implementation detail
- rejects mutation APIs
- never runs generated operations lazily during queries

Required generated view API:

```python
container.Fields.sequence()
container.InitSignatureFields.sequence()
container.ClassInput.one()
container.Fields.by_identity("count")
container.InitSignatureFields.contains("count")
```

View behavior:

- `sequence()` returns a generator or iterable of records in stable order
- `one()` returns the only record, returns `None` for no record, and rejects
  multiple records
- `by_identity(value)` returns the matching record or `None`
- `contains(value)` checks whether the identity exists in the view

For concrete collection views, `sequence()` returns all stored records for that
collection.

For computed collection views, `sequence()` returns source collection records
that match the computed collection's generated filter.

For computed collection `by_identity(...)`, the view should first resolve the
identity against the source collection and then verify that the record belongs
to the computed view.

No read API should mutate indexes, run derivation code, or observe newly added
records after freeze.

## Collection Storage

For `single` collections:

- at most one record may be present
- insertion of a different second record rejects
- insertion of the identical record is idempotent

For `many` collections:

- records are keyed by collection identity when the collection declares one
- duplicate identity with the identical record is idempotent
- duplicate identity with a different record rejects unless a later explicit
  operation policy allows replacement
- collections without identity may append records, but they should not be used
  for generation resources that need stable override or lookup behavior

Replacement is not a default container behavior. If capsule merging needs
replacement, the generated operation function should call an explicit primitive
such as `replace(...)` or use a later merge-policy layer.

## Facts And Lookup

Every stored record may contribute equality facts for its collection:

```python
Fields.Name == "count"
Fields.Init == True
```

The first generated view implementation does not have to build a generic fact
index. For simple computed collections, generated direct attribute filters are
acceptable and preferred:

```python
(field for field in container.Fields.container if field.init is True)
```

If later profiles show a hot lookup, the generated collection view can use an
index behind the same `sequence()` / `by_identity()` API.

Low-level generic APIs may exist for generated operation code:

- `records(collection_descriptor) -> tuple[object, ...]`
- `matching(collection_descriptor, *conditions) -> tuple[object, ...]`
- `by_identity(collection_descriptor, value) -> object | None`

Those APIs are not the preferred surface for the build mapper. The generated
named views are.

When generic matching is used, it must remain Eq-only. Richer concepts should be
materialized into derived properties or derived records first.

## Derived Properties

Derived properties are generated operations that add queryable facts. They are
not arbitrary predicates embedded inside rule matching.

Example intent:

```python
def derive_field_kind_facts(container):
    for field in container.records(Fields):
        container.add_fact(Fields, field, IsManaged, isinstance(field.kind, ManagedKind))
```

Then later generated operations can query:

```python
for field in container.ManagedFields.sequence():
    ...
```

Open implementation question: whether derived properties should be stored as:

- overlay facts attached to an existing record identity, or
- separate derived records in a companion collection.

The first version should choose the simpler representation that keeps Eq lookup
stable and diagnostics clear.

## Filters

Filters are generated operation code or computed collection views over container
records, not DDS data mutation.

The DDS defines filter conditions during specification. The generated module can
compile them into named view implementations:

```python
container.InitSignatureFields.sequence()
```

or use lower-level matching internally:

```python
container.matching(Fields, Init.eq(True), DefaultStatus.eq(DefaultProvided))
```

That separation matters:

- DDS remains schema and operation definition
- named filters are reusable by multiple operation functions and build-mapper
  paths
- the generated spec module holds executable semantics
- each decorated class gets an independent container instance
- no global schema object is mutated by decoration-time data

## Relationship To The Rule Engine

`DDSContainer` is not the full capsule/rule engine.

The next layer evaluates rule points over the final container. A rule point is a
named decision site such as:

- property getter provider
- property setter provider
- init parameter provider
- class body component provider
- field assignment provider

Capsules contribute providers to rule points. A provider has:

- a target rule point
- a matcher over one or more named collection views
- an Astichi composable or generated operation resource
- a precedence/override policy
- a binding strategy that maps the match tuple into Astichi binds, identifier
  binds, keep names, and target ports

Rule matching should return a first-class match tuple:

```python
ResolvedProvider(
    rule_point=PropertyGetter,
    provider=ManagedGetter,
    match=(field, facade, tx_key),
)
```

That tuple is how the later build mapper knows which concrete field/facade/tx
records to use when satisfying the selected Astichi composable's requirements.

Example conceptual provider setup:

```python
PropertyGetter.default(DefaultGetter)

PropertyGetter.when(
    ManagedFields,
    WorkingFacades,
).provide(ManagedWorkingGetter)
```

After the rule point resolves a provider, the build mapper can inspect the
selected composable's `describe()` result and use the provider's binding
strategy to connect the match tuple to Astichi resources.

The rule engine still needs:

- rule fragments
- capsule/facade merge behavior
- operation ordering
- replacement/add-if-absent policies
- resource records for Astichi build ports
- ordered multi-port expansion
- single-port conflict detection

Those features can be generated as operation functions or live in a layer that
coordinates operation functions. The container should stay as the stable
resolved-data object and generated-view surface they operate on.

## Initial Test Shape

Use focused unit tests for this module. There is no source-output golden surface
yet because the container itself does not emit code.

Initial tests should cover:

- adding and reading records from many collections
- single collection cardinality enforcement
- identity lookup and duplicate identity rejection
- generated concrete collection view `sequence()` / `one()`
- generated computed collection view `sequence()`
- computed collection `by_identity(...)` membership check
- a generated-style operation function that derives records from one collection
  into another
- freezing and rejecting mutation after freeze
- rejecting records or collections from another DDS specification
