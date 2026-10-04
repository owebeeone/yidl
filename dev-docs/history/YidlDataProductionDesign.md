# YIDL Data Production Design

## Purpose

The current DDS/container layer defines schema, stores decoration-time input
records, exposes computed views, and runs matchers. It does not yet describe
how capsule/facade behavior produces the resource graph that the Astichi build
mapper consumes.

This document specifies the next layer: **data productions**. A production is a
generated operation that reads records or matcher results, creates new records,
applies a merge policy, and stores the result in a `DDSContainerBuilder` before
freeze.

The immediate proving target is `scratch/ae_concept_3.py`: a rewrite of
`scratch/ae_concept_2.py` that uses DDS records, generated values, matchers,
and production APIs instead of its scratch-only `Fragment`, `ResourceKind`,
`DeriveRule`, and `RecordStore` types.

## Boundary

The V1 container stays boring:

- validates records and collection membership
- enforces cardinality and identity
- stores concrete records
- exposes frozen named views
- does not infer lifecycle or capsule semantics

The production layer owns semantics:

- which source records are scanned
- which matcher results are scanned
- what target records are created
- whether duplicate identities are ignored, rejected, or replaced
- operation ordering
- target-port membership and ordering
- whether a production group runs once or, in a future slice, to a fixpoint

This keeps the container reusable while allowing capsules/facades to contribute
more code-generation behavior.

## Relationship To `ae_concept_2.py`

`ae_concept_2.py` has these scratch concepts:

- `PropertySpec` -> current DDS `PropertySpec`
- `ResourceKind` -> current DDS `RecordSpec` / `UnionSpec` plus
  `CollectionSpec`
- `ResourceRecord` -> current generated record instances
- `DeriveRule` -> new production spec
- `Fragment` -> new production fragment / merge unit
- `RecordStore` -> current `DDSContainerBuilder` plus production runner
- `TargetPort` and `Order` -> new port-address and ordered-child query model
- `MergePolicy` -> new production write policy

The core behavior to preserve is:

1. Start with input records for class, feature, field, and facade facts.
2. Derive class-name and parent resources.
3. Derive class-body components such as slots and `__init__`.
4. Derive nested resources such as slot items, init params, and init body
   statements.
5. Allow later fragments to replace specific derived records, for example a
   managed-field init assignment replacing the generic field assignment.
6. Render or build by walking ordered children at a target port.

## Production Records

Production outputs are ordinary DDS records in concrete collections.

Example record shapes for the `ae_concept_3.py` sketch:

```python
Name = dds.property("Name", str, storage_name="name")
RuntimeValue = dds.property("RuntimeValue", object, storage_name="runtime_value")
TargetPort = dds.property("TargetPort", object, storage_name="target_port")
Order = dds.property("Order", int, default=0, storage_name="order")
Template = dds.property("Template", object, storage_name="template")

ClassNames = dds.collection("ClassNames", ClassName, cardinality=dds.many, identity=Name)
ClassParents = dds.collection("ClassParents", ParentClass, cardinality=dds.many)
ClassComponents = dds.collection("ClassComponents", ClassComponent, cardinality=dds.many)
SlotItems = dds.collection("SlotItems", SlotItem, cardinality=dds.many, identity=Name)
InitParams = dds.collection("InitParams", InitParam, cardinality=dds.many, identity=Name)
InitBodyItems = dds.collection("InitBodyItems", InitBodyItem, cardinality=dds.many, identity=Name)
```

Record shapes are intentionally normal DDS shapes. No special "resource
record" superclass is needed.

## Port Model

`ae_concept_2.py` sorts records by `TargetPort` and `Order`. DDS needs this as
a real concept.

### Port Spec

A port is a semantic object that identifies a build destination.

```python
ClassNamePort = dds.port("Class.name", cardinality=dds.single)
ClassParentsPort = dds.port("Class.parents", cardinality=dds.many)
ClassBodyPort = dds.port("Class.body", cardinality=dds.many)
SlotsItemsPort = dds.port("Slots.items", cardinality=dds.many)
InitParamsPort = dds.port("Init.params", cardinality=dds.many)
InitBodyPort = dds.port("Init.body", cardinality=dds.many)
```

Ports are semantic objects, not strings or enums. They own cardinality and can
validate target usage. Port cardinality reuses the same `single` / `many`
behavior objects as collection cardinality, but it constrains the number of
children at one `PortAddress`; it does not constrain the size of the backing
collection.

### Port Address

A port address combines a port with the identity of the owner instance:

```python
ClassBodyPort.of("runtime")
SlotsItemsPort.of(("runtime", "slots"))
InitParamsPort.of(("runtime", "__init__"))
```

The address is stored in a `TargetPort` property on produced records.
Owner identities used in generated source must be source-renderable, such as
strings, ints, or tuples of source-renderable values, or must be provided
through an explicit source-name map.

### Ordered Children

The generated runtime needs a query equivalent to:

```python
for child in container.children_at(ClassBodyPort.of("runtime")):
    ...
```

Required behavior:

- select records whose `TargetPort` equals the requested address
- sort by `Order`, then target-collection write order for deterministic ties
- enforce single-port cardinality at write time, with lookup-time validation
  as a defensive fallback
- return concrete produced records

The first implementation exposes a generic `children_at(port_address)` helper.
Later generated modules can expose named parameterized views if that proves
clearer or faster.

## Merge Policies

The current builder rejects duplicate identities. Production needs explicit
policies because some capsule behavior is intentionally default-then-override.

Policies are semantic behavior objects:

```python
AddIfAbsent
ReplaceExisting
RejectDuplicate
```

No enum or string policy names.

### Add If Absent

Used for defaults. If no record exists at the target collection identity, add
the new record. If a record already exists, do nothing.

This lets a base capsule provide a generic resource that a later capsule can
replace.

### Replace Existing

Used for intentional overrides. If the identity exists, replace it. If it does
not exist, add it.

This models cases like:

- generic `InitAssignment(name -> name)`
- managed override `InitAssignment(name -> working_name)`

### Reject Duplicate

Fails if the identity already exists. Used as the default strict behavior and
for cases where two providers should not write the same identity.

The container's existing duplicate-identity behavior is still the default for
ordinary input insertion. Production policies are explicit and local to
production execution.

`add(...)` remains the ordinary input-insertion surface. `write(...)` is the
production-oriented primitive for explicit merge policy. Both should share the
same internal duplicate/cardinality helper.

## Production Specs

A production scans one source sequence and writes records to one target
collection.

Conceptual shape:

```python
dds.production(
    "InitFieldProvidesParam",
    source=InitFields,
    target=InitParams,
    when=(),
    identity=source.prop(Name),
    values={
        Name: source.prop(Name),
        TargetPort: literal(InitParamsPort.of(("runtime", "__init__"))),
        Order: call("field-order", field_order),
        Template: literal(RequiredInitParamTemplate),
    },
    policy=AddIfAbsent,
)
```

The model is:

- name
- source sequence
- target collection
- Eq-only source conditions
- target identity expression
- target property value expressions
- merge policy
- optional origin/diagnostic label

The output is a real record in a target collection.

If `identity=` is omitted, V1 derives the identity from
`values[target.identity]` when that value is present. Keyed target collections
reject if neither form supplies the identity. If both are supplied, the values
must agree. Unkeyed target collections must omit `identity=`.

## Source Sequences

The production source may be one of:

1. A concrete collection view.
2. A computed collection view.
3. A matcher-result sequence.
4. A later explicit joined/correlated sequence, if real YIDL needs it.

V1 should support 1-3. Joins should stay out until a concrete lifecycle case
needs them.

### Collection Source

Scans records:

```python
for field in builder.records(InitFields):
    ...
```

### Matcher Source

Scans matcher results:

```python
for result in container.matchers.InitParamTemplate.sequence():
    ...
```

The result exposes:

- `resource`: the selected `MatcherGeneratedValue`
- `rule`: diagnostic rule name
- `score`: diagnostic score
- `records`: concrete input records
- `values`: extracted matcher tuple

Matcher productions are how rule selection becomes concrete build resources.

## Value Expressions

Production values need a small expression system. It should stay explicit and
source-emittable.

Required V1 expressions:

- `literal(value)` — source-renderable literal or semantic object provided by
  the generated module
- `read(property)` — read a property from the source record
- `call(name, func)` — call an emitted/imported helper
- `match.resource()` — selected `MatcherGeneratedValue` from a matcher source
- `match.record(input_name)` — a concrete input record from a matcher result
- `match.value(index)` — positional matcher tuple value, mostly diagnostic

`ComputedValue` exists today for in-memory transform specs. Production V1
should not expose a second public value-expression family. Add source-emission
behavior to the existing value-expression model where practical. Helper calls
must receive source names during generated operation emission.

## Production Groups

Operation order must be explicit. The production layer should define ordered
groups:

```python
dds.production_group("ClassShell", ClassNameProduction, ParentProduction)
dds.production_group("Constructs", SlotsProduction, InitMethodProduction)
dds.production_group("FieldChildren", SlotItemProduction, InitParamProduction)
dds.production_group("Overrides", ManagedInitAssignmentOverride)
```

V1 default: run each group once, in declaration order.

Slice 3 groups are write-once declarations. Ordered group insertion,
extension, or replacement is a later fragment-merge concern.

Fixpoint execution is explicitly deferred. A future fixpoint group would rerun
until no production writes change the builder, but V1 does not define that
behavior.

For `ae_concept_3.py`, explicit groups are preferable to implicit global
fixpoint evaluation:

1. Inputs are collected.
2. Class shell resources are produced.
3. Enabled features produce construct shells (`Slots`, `InitMethod`).
4. Fields produce children (`SlotItem`, `InitParam`, default
   `InitAssignment`).
5. Managed fields replace specific assignments and produce managed-name
   records.

## Generated Runner

The generated DDS module should expose a runner around the builder:

```python
def build_container(builder):
    run_class_shell(builder)
    run_constructs(builder)
    run_field_children(builder)
    run_overrides(builder)
    return builder.freeze()
```

or:

```python
DDS_OPERATIONS = (
    run_class_shell,
    run_constructs,
    run_field_children,
    run_overrides,
)
```

The exact packaging can be settled during implementation. The invariant is
that operation semantics are emitted as source/AST, while the container remains
storage and query infrastructure.

Generated operation code may call low-level builder primitives:

- `builder.records(collection)`
- `builder.matching(collection, *conditions)`
- `builder.add(collection, record)`
- `builder.write(collection, record, policy=...)`
- `builder.children_at(port_address)` only after enough produced records exist

Operations read the builder state at the start of each production. Writes from
earlier groups and earlier productions in the same group are visible; records
written by the current production are not rescanned by that same production.
`builder.children_at(...)` follows the same read-stability rule.

Ordinary input code should keep using `add(...)` unless it is intentionally
applying a merge policy.

The frozen container should expose the same ordered-port query for the build
mapper:

```python
for item in container.children_at(InitBodyPort.of(("runtime", "__init__"))):
    ...
```

## Matcher Productions

The matcher layer is now complete enough to feed productions.

Example:

```python
InitParamTemplate = dds.matcher("InitParamTemplate")
field = InitParamTemplate.input("field", InitFields)
InitParamTemplate.default(from_astichi_code("... required param ..."))
InitParamTemplate.rule(
    when=(field.prop(DefaultStatus).eq(DefaultProvided),),
    resource=from_astichi_code("... defaulted param ..."),
)

dds.production(
    "InitParamResources",
    source=InitParamTemplate.results(),
    target=InitParams,
    identity=match.record("field").prop(Name),
    values={
        Name: match.record("field").prop(Name),
        TargetPort: literal(InitParamsPort.of(("runtime", "__init__"))),
        Order: call("field-order", field_order),
        Template: match.resource(),
    },
    policy=ReplaceExisting,
)
```

This bridges rule selection and resource production:

- matcher decides which generated value applies
- production decides where that generated value goes
- build mapper later consumes ordered children at ports

`from_astichi_code(...)` is the public helper exported by
`yidl.generation`; examples use that helper directly.

V1 matcher productions should use a temporary read-only snapshot of the
builder, conceptually `builder._snapshot()`, and run the existing generated
container matcher runtime over that snapshot. The snapshot helper stays private
until builder-phase matcher pressure justifies a public API.

## Definition Extension And Fragment Pressure

`ae_concept_2.py` has `Fragment.merge(...)`. The first implemented DDS answer
is direct definition extension: contributors call `ensure_*` helpers on one
`DataDefinitionSystem`, and `dds.extend(...)` applies those contributors in
order.

This lets independently authored capsule-like contributors share:

- record/union/collection definitions, when defining a new concept
- computed collections
- matchers and matcher rules
- productions
- production groups
- port declarations

Direct-extension merge rules:

1. Semantic objects merge by identity and full definition, not by incidental
   string labels alone.
2. Duplicate definitions of the same semantic object must either be identical
   or reject.
3. New matcher rules append to the target matcher.
4. Production groups are write-once and may be reused only with the identical
   production sequence.
5. Replacement behavior applies to produced records at decoration time, not to
   definition objects unless explicitly declared.

A separate production fragment object remains deferred. Add it only when direct
extension becomes awkward, for example if contributors need ordered insertion
into an existing production group without owning the whole group.

## Source Emission Requirements

Everything needed at decoration time must be emitted into a normal Python
module.

The generated module must contain or import:

- runtime DDS descriptors
- generated record classes
- port objects and port-address constructors
- matcher runtime classes
- generated operation functions
- helper functions used by `call(...)` expressions
- `MatcherGeneratedValue` constructors where matcher resources are embedded

The generated decorator or field-spec functions must not invoke the Python
parser. Astichi composables are predeclared/generated values; `to_generator()`
compiles cached Astichi source when the build mapper asks for it.

## `ae_concept_3.py` Target Shape

The scratch rewrite should demonstrate the following without bespoke scratch
record-store classes:

1. Define DDS properties for names, feature flags, field kind, defaults,
   target ports, order, templates, and managed names.
2. Define input collections for class, feature, field, and facade records.
3. Define derived collections for class-name, parent, class body component,
   slot item, init method, init param, init body item, and managed names.
4. Define port objects for class name, class parents, class body, slots items,
   init params, and init body.
5. Define computed collections for slot fields, init fields, and managed
   fields.
6. Define productions equivalent to `class_shell_fragment()`,
   `init_fragment()`, and `managed_fragment()`.
7. Run production groups over a builder populated with sample input records.
8. Freeze the container.
9. Render a debug view by walking `children_at(port_address)` and the derived
   collections.
10. Use at least one matcher production to choose a `MatcherGeneratedValue`
    template for init params or init assignments.

The scratch file should expose API pressure. If a step requires bespoke code
that looks like a mini container or mini matcher, that is a DDS API gap.

## Implementation Slices

### Slice 1: Merge Policies And Builder Write

- Add production merge policy objects.
- Add builder write primitive that accepts a policy.
- Keep ordinary `add(...)` behavior unchanged.
- Tests: identity add-if-absent, replacement, duplicate rejection.

### Slice 2: Port Objects And Ordered Children

- Add `PortSpec` and `PortAddress`.
- Add target-port/order query support.
- Tests: multi-port ordering, single-port conflict, owner identity separation.

### Slice 3: Collection Productions

- Add production specs over collection/computed collection sources.
- Generate operation code that runs productions over a builder.
- Tests: derive records from fields into init params/slot names.

### Slice 4: Matcher Productions

- Add production source over matcher results, first through a read-only
  snapshot/frozen view so the existing matcher runtime is reused.
- Add value expressions for selected resource and matched records.
- Tests: matcher-selected generated values become ordered target resources.

The implementation plan splits this into Slice 4a for frozen/snapshot matcher
sources and Slice 4b for builder-phase matcher sources, if 4b is needed.

### Slice 5: Definition Extension

- Add direct `DataDefinitionSystem.extend(...)` and idempotent `ensure_*`
  helpers for shared semantic definitions.
- Keep a separate fragment object deferred until direct extension demonstrates
  real limits.
- Tests: independent contributors share schema/matchers without
  duplicating the whole base graph.

## Non-Goals For This Layer

- No lifecycle-specific names such as `managed` or `PublishedStore` in the
  generic DDS production API.
- No arbitrary predicate language; Eq-only matching remains the rule.
- No enum/string policy tags.
- No parser calls in decoration-time generated code.
- No Astichi workaround layer. If a generated value cannot be composed cleanly,
  improve Astichi or the build mapper.
