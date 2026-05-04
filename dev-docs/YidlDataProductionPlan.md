# YIDL Data Production Implementation Plan

## Goal

Implement the data-production layer described in
`dev-docs/YidlDataProductionDesign.md` with small, test-first slices. The goal
is to make `scratch/ae_concept_3.py` possible: a DDS-backed rewrite of
`scratch/ae_concept_2.py` that uses current records, collections, computed
views, matchers, generated values, and production APIs instead of scratch-only
resource-store classes.

The production layer must extend the current DDS/container/matcher system. It
must not duplicate existing concepts with parallel names or parallel runtime
paths when one existing surface can be extended.

## Existing Surfaces To Reuse

Use these as the base implementation points:

- `DataDefinitionSystem` remains the schema entry point.
- `PropertySpec`, `RecordSpec`, `UnionSpec`, `CollectionSpec`, and
  `ComputedCollectionSpec` remain the data-shape model.
- `TransformSpec.derive(...)` remains a limited in-memory helper and
  compatibility surface. V1 production implementation should not route through
  it; `production(...)` is the public generated-operation surface. Do not grow
  `transform(...)` and `production(...)` into two overlapping APIs.
- `DDSContainerBuilder.add(...)`, `.records(...)`, `.matching(...)`, and
  `.freeze()` remain the mutation/query primitives.
- `DDSContainer` remains immutable after freeze and exposes named views.
- `MatcherSpec` and `MatcherResult` remain the rule-selection surface.
- `MatcherGeneratedValue` remains the only matcher resource type.
- `container_runtime_source.emit_container_runtime_source(...)` remains the
  generated module emitter. Add production emission there or in a cohesive
  helper module called by it; do not create a second unrelated emitter.

## Cross-Slice Constraints

1. No new enums or string policy tags. Merge policies, ports, sources, and
   value expressions are semantic objects/classes.
2. No parser calls in generated decorator/field-spec runtime paths.
3. No lifecycle-specific names in generic DDS production APIs.
4. Ordinary input insertion keeps the current strict `add(...)` behavior.
   Replacement only occurs through explicit production/write policy.
5. Generated code tests use the existing `tests/data/gold_src` and
   `tests/data/goldens/materialized` harness for success-path emitted source.
   Bespoke tests should not duplicate those source-shape assertions.
6. Bespoke unit tests are reserved for narrow mechanics and failure modes:
   invalid policies, duplicate definitions, cardinality errors, and API
   validation.
7. Keep implementation compact. Prefer one focused production module plus
   narrow hooks in `data_schema.py`, `data_container.py`, and
   `container_runtime_source.py`.
8. Generated modules and generated decorator/field-spec functions must not
   import or depend on `pyrolyze`.
9. `scratch/ae_concept_3.py` is a rolling API-pressure driver. Start it as a
   skeleton in Slice 1 and expand it each slice instead of waiting until
   slices 1-4 are complete.
10. Generated operation source must use constructs that round-trip across the
    supported Python 3.12-3.15 sweep.
11. Runtime objects that are semantic values, such as ports, port addresses,
    policies, and generated-value resources, must be emitted through stable
    generated bindings or explicit source-name maps. Do not invent ad hoc
    object literal rendering for arbitrary Python objects.
12. Owner identity values passed to `PortSpec.of(...)` must be
    source-renderable, such as strings, ints, or tuples of source-renderable
    values, or must be present in an explicit source-name map.

## Slice 1: Merge Policies And Builder Write

### Purpose

Allow generated operations to intentionally add-if-absent, replace, or reject
duplicate identities without weakening `DDSContainerBuilder.add(...)`.

This maps directly to `ae_concept_2.py`'s `MergePolicy`, `AddIfAbsent`, and
`ReplaceExisting`.

### APIs

Add policy objects:

```python
AddIfAbsent
ReplaceExisting
RejectDuplicate
```

Exact exported singleton/class naming can be settled during implementation,
but the behavior objects should own the write decision:

```python
replacement = policy.merge(existing, new_record)
```

Add builder primitive:

```python
builder.write(collection, record, *, policy=RejectDuplicate)
```

Behavior:

- validates collection belongs to the builder's DDS
- validates record shape
- `RejectDuplicate`: same as current `add(...)` behavior. For keyed
  collections it rejects duplicate identity; for unkeyed many collections it
  allows append and only relies on cardinality/idempotence checks.
- `AddIfAbsent`: first record wins; later same identity does nothing
- `ReplaceExisting`: new record replaces old record for that identity
- `AddIfAbsent` and `ReplaceExisting` require a collection identity
- idempotent write of the identical object remains harmless. Identical means
  the same object by `is`, matching current `add(...)` behavior. A different
  object with the same identity still rejects under `RejectDuplicate`.

`builder.add(...)` should call or share the same internal write helper with
`RejectDuplicate` semantics, rather than maintaining a separate duplicate
implementation.

`add(...)` remains the ordinary input-insertion surface. `write(...)` is the
production-oriented primitive for explicit merge policy. Neither surface is
deprecated.

### Generated Runtime

Emit runtime policy objects from the same module that exports runtime
container types. Generated modules should import those objects rather than
redeclare them by hand.

### Concept 3 Relation

This enables managed override behavior:

- base production writes `InitAssignment(name -> name)` with `AddIfAbsent`
- managed production writes `InitAssignment(name -> working_name)` with
  `ReplaceExisting`

### Tests

Bespoke tests:

- `write(..., policy=AddIfAbsent)` keeps first identity
- `write(..., policy=ReplaceExisting)` replaces same identity
- `write(..., policy=RejectDuplicate)` rejects duplicate identity for a
  different object
- `write(..., policy=RejectDuplicate)` accepts a second write of the same
  object by identity
- `add(...)` behavior is unchanged
- write after `freeze()` rejects
- `AddIfAbsent` / `ReplaceExisting` on a collection without identity reject
- `RejectDuplicate` on an unkeyed many collection preserves current append
  behavior

Golden tests:

- Add `tests/data/gold_src/dds_write_policy.py`.
- It emits a runtime container module, writes two records to the same
  identity through generated builder methods, validates replace/add-if-absent
  behavior after executing the generated source, and asserts generated source
  imports/reuses runtime policy objects.

## Slice 2: Port Objects And Ordered Children

### Purpose

Represent build destinations as first-class semantic objects and support
ordered child lookup by target port.

This maps to `ae_concept_2.py`'s `PortSpec`, `PortAddress`,
`TargetPort`, `Order`, and `RecordStore.children_at(...)`.

### APIs

Add schema-time port definition to `DataDefinitionSystem`:

```python
ClassBodyPort = dds.port("Class.body", cardinality=dds.many)
ClassNamePort = dds.port("Class.name", cardinality=dds.single)
```

Add objects:

```python
class PortSpec:
    name: str
    cardinality: CollectionCardinality
    def of(self, owner_identity: object) -> PortAddress: ...

class PortAddress:
    port: PortSpec
    owner_identity: object
```

Reuse the existing `single`/`many` cardinality behavior objects. Do not create
a second port-cardinality enum.

Add runtime counterparts if source emission needs them:

```python
RuntimePort
RuntimePortAddress
```

Expose ports in generated modules as normal bindings:

```python
ClassBodyPort = RuntimePort("Class.body", cardinality=many)
```

Port objects, port addresses, and policy singletons are semantic runtime
objects. Source emission must reference generated bindings for them or receive
an explicit source-name mapping. Arbitrary Python object literals are not a
supported representation for these values.

Add child lookup:

```python
builder.children_at(port_address)
container.children_at(port_address)
```

The query needs to know which properties represent target port and order. Avoid
hard-coding property names globally. V1 uses one port index per DDS:

```python
dds.port_index(target=TargetPort, order=Order)
```

The index reuses ordinary DDS properties instead of creating a special hidden
record shape. The target property is declared with `value_type=object`, and
the port index is responsible for narrowing valid stored values to
`PortAddress`.

Behavior:

- select stored records that expose the configured target-port property
- compare to the requested `PortAddress`
- sort by configured order property, then target-collection write order
- ignore records that do not expose the configured target-port property
- validate at write time that configured target-property values are
  `PortAddress` instances
- enforce `single` port cardinality at write time, with lookup-time checking
  as a defensive fallback
- owner identity scopes addresses, so two owners can use the same port safely

### Generated Runtime

Generated source must emit ports, port addresses, and child lookup support.
Success tests should assert generated modules do not rebuild source-time DDS
objects with `dds.port(...)`.

### Concept 3 Relation

This enables debug/build traversal:

```python
container.children_at(ClassBodyPort.of("runtime"))
container.children_at(InitParamsPort.of(("runtime", "__init__")))
```

### Tests

Bespoke tests:

- port objects reject invalid names
- port address equality and owner separation
- `children_at(...)` returns ordered children
- single-port conflict rejects or reports clearly
- records without target-port property are ignored by `children_at(...)`
- records with non-`PortAddress` target values reject at write time

Golden tests:

- Add `tests/data/gold_src/dds_port_children.py`.
- It emits a runtime module with ports, creates records targeted to multiple
  owners/ports, runs generated source, and validates ordered `children_at(...)`
  output.

## Slice 3: Collection Productions

### Purpose

Turn source records into derived target records by running generated
operations over a builder.

This maps to `ae_concept_2.py`'s `DeriveRule` over ordinary source records.

### APIs

Use `dds.production(...)` as the public generated-operation surface. Do not
extend `transform(...)` into a second public runner API. Existing
`TransformSpec.derive(...)` remains available for in-memory tests and
compatibility callers that do not need emission, but the V1 production
implementation does not route through it. Production owns emitted operation
behavior.

```python
production = dds.production(
    "SlotFieldProvidesSlotItem",
    source=SlotFields,
    target=SlotItems,
    when=(),
    identity=read(Name),
    values={
        Name: read(Name),
        TargetPort: literal(SlotsItemsPort.of(("runtime", "slots"))),
        Order: call("field-order", field_order),
        Template: literal(SlotItemTemplate),
    },
    policy=AddIfAbsent,
)
```

The production `identity=` expression supplies the value for the target
collection's declared identity property. It cannot name or imply a different
identity than the target collection uses. If `identity=` is omitted, V1 derives
identity from `values[target.identity]` when present; otherwise keyed target
collections reject.

If both `identity=` and `values[target.identity]` are provided, they must
evaluate to the same value. If the target collection has no identity,
`identity=` must be omitted and only `RejectDuplicate` append/cardinality
semantics are available.

Value expressions should build on current `ValueExpression`, `ReadProperty`,
`LiteralValue`, and `ComputedValue`, but Slice 3 must add a source-emission
contract for every expression used by productions:

- `literal(value)` -> source-renderable literal or `value_names` binding
- `read(property)` -> `source.<storage_name>`
- `call(name, func)` -> emitted/imported helper call using a source name map
- identity expression lowering
- port-address literal lowering through generated port objects

The name `call(...)` is used for production value helpers to avoid confusion
with computed collections.

Add basic production groups in this slice:

```python
dds.production_group("ClassShell", ClassNameProduction, ParentProduction)
dds.production_group("FieldChildren", SlotItemProduction, InitParamProduction)
```

The full `ae_concept_3.py` group list may also include construct and override
groups. The Slice 3 example shows only the minimum group surface needed to
prove generated production execution.

V1 groups run once in declaration order. Fixpoint groups are explicitly
deferred.

Read stability is simple in V1: production groups run sequentially, and each
production reads the builder state at the moment that production starts. It can
see writes from earlier groups and earlier productions in the same group. A
production does not rescan records it writes during that same production.
`builder.children_at(...)` observes the same per-production read rule. Any
recursive/fixpoint behavior is deferred.

### Generated Runtime

Emit operation functions:

```python
def run_slot_field_provides_slot_item(builder):
    for source in builder.records(SlotFieldsCollection):
        record = SlotItem(...)
        builder.write(SlotItemsCollection, record, policy=AddIfAbsent)
```

Emit a generated runner:

```python
def build_container(builder):
    run_class_shell(builder)
    run_field_children(builder)
    return builder.freeze()
```

or a stable `run_operations(builder)` plus `new_builder()` wrapper. Choose the
smallest surface that supports goldens and `ae_concept_3.py`.

### Concept 3 Relation

This enables:

- class input -> class name resource
- class input -> parent resource
- feature input -> slots component
- feature input -> init method component
- field input -> slot item
- field input -> init param
- field input -> default init assignment
- field input -> managed names

### Tests

Bespoke tests:

- production validates source/target belong to the same DDS
- production target must be concrete, not union
- production rejects missing target property values
- computed source collection can feed production
- generated operation order is declaration/group order
- value expressions emit source for literals, property reads, helper calls,
  and port-address values

Golden tests:

- Add `tests/data/gold_src/dds_collection_productions.py`.
- It emits a module with generated operations, executes the module, populates
  input fields/features, runs the operation runner, freezes, and validates
  derived records and generated source shape.

## Slice 4: Matcher Productions

### Purpose

Let matcher results produce concrete resource records. This is how rule
selection becomes ordered build data.

This maps to `ae_concept_2.py` cases where a derived record's `Template`
depends on a function like `_param_template(...)`, but uses the real matcher
system instead of a bespoke callback.

### Slice 4a APIs: Frozen-View Matcher Source

Add matcher production source support through the unified production API. The
V1 spelling is:

```python
dds.production(
    "InitParamTemplateResources",
    source=InitParamTemplate.results(),
    target=InitParams,
    ...
)
```

Do not add `dds.matcher_production(...)` in V1. A matcher-result sequence is a
source object for `production(...)`, not a second production API.

Add matcher-result value expressions:

```python
match.resource()
match.record("field").prop(Name)
match.value(0)
```

Do not duplicate matcher tuple extraction logic. Reuse `MatcherResult.records`
and `MatcherResult.values`.

Input names are unique per matcher; `match.record("field")` resolves by that
existing input name.

### Slice 4a Generated Runtime

First support matcher productions over a stable resolved view. This can be a
frozen container or an equivalent read-only snapshot produced between
production groups. The generated operation scans the existing generated
container matcher wrapper:

```python
for result in container.matchers.InitParamTemplate.sequence():
    field = result.records[0]
    record = InitParam(
        name=field.name,
        template=result.resource,
        ...
    )
    builder.write(InitParamsCollection, record, policy=ReplaceExisting)
```

The preferred V1 implementation is a temporary snapshot created from the
builder and read through the existing generated container/matcher runtime. That
keeps matcher evaluation on one runtime path. Writes made by the matcher
production are not visible to the matcher sequence being scanned.

Slice 4a should add an internal builder snapshot helper, conceptually
`builder._snapshot()`, that returns a read-only `DDSContainer` over the current
builder state without freezing the builder. Keep this helper private until 4b
pressure proves a public API is useful.

### Slice 4b APIs: Builder-Phase Matcher Source

Builder-phase matcher execution is a separate decision. Before implementing it,
choose and document one read-stability model:

1. snapshot/freeze between production groups
2. view-through-builder collection access
3. direct matcher source wrapper over in-progress builder records

Do not accidentally ship a second matcher runtime. If 4a's snapshot model is
enough for `ae_concept_3.py`, defer 4b.

### Concept 3 Relation

This enables:

- required vs defaulted init param generated values
- managed vs plain assignment generated values
- later property getter/setter provider selection

### Tests

Bespoke tests:

- matcher production requires a matcher from the same DDS
- matcher production can read a matched input record
- matcher production can use `result.resource`
- no match produces no output record
- builder-phase matcher execution is either explicitly unsupported or covered
  by the chosen 4b read-stability model

Golden tests:

- Add `tests/data/gold_src/dds_matcher_productions.py`.
- It defines a matcher returning two different `MatcherGeneratedValue`
  resources, emits source, executes it, runs operations, and validates target
  records contain the selected generated values.

## Slice 5: Definition Extension

### Purpose

Support capsule/facade inheritance and composition by merging definition-time
contributions without copying a whole graph.

This maps to `ae_concept_2.py`'s `Fragment.merge(...)`.

### APIs

The rolling `ae_concept_3.py` pressure test reached the first composition
need: independently authored contributors must be able to share schema,
ports, matchers, and production groups without passing around a giant registry
object.

The V1 implementation uses direct extension rather than a separate fragment
object:

```python
dds.extend(base_schema, init_capsule, managed_capsule)
```

Contributors use `ensure_*` helpers to reuse identical semantic definitions
and reject incompatible duplicates. Introduce a production fragment object only
if direct extension later becomes awkward.

V1 merge rules:

- duplicate semantic definitions must be identical or reject
- matcher rules append to existing matchers
- Slice 3 `production_group(...)` is write-once. Ordered group insertion,
  extension, or replacement is a Slice 5 concern and must be deterministic.
- decoration-time replacement is still handled by production write policies,
  not by mutating definition objects

### Concept 3 Relation

This enables:

- base class shell fragment
- init capsule fragment
- managed-field fragment
- later facade/capsule combinations

### Tests

Bespoke tests:

- duplicate incompatible property/record/collection definitions reject
- identical shared definitions do not duplicate
- rules append to an existing matcher
- `extend(...)` applies contributors in order

Golden tests:

- Add `tests/data/gold_src/dds_definition_extensions.py` to show independent
  contributors sharing schema and matchers while emitting ordinary generated
  runtime source.

## `ae_concept_3.py` Rolling Work Item

Create `scratch/ae_concept_3.py` during Slice 1 and keep expanding it.

It should:

1. Define the same conceptual input data as `ae_concept_2.py`.
2. Use DDS properties, records, unions, collections, computed collections,
   ports, productions, and matchers.
3. Run productions through generated-style builder APIs.
4. Freeze a `DDSContainer`.
5. Render the same debug structure as `ae_concept_2.py` by using
   `children_at(...)` and ordinary collection views.
6. Avoid defining scratch-only record stores, scratch-only rule engines, or
   scratch-only matcher logic.

If `ae_concept_3.py` needs a local helper that looks generic, stop and decide
whether it belongs in DDS production instead.

Per-slice expected growth:

- Slice 1: define input/output record shapes and exercise write policies.
- Slice 2: add ports and ordered child rendering.
- Slice 3: replace hand-written derivation with collection productions and
  production groups.
- Slice 4a: use matcher productions for at least one generated-value template.
- Slice 4b: only if builder-phase matching is needed.

## Verification Strategy

Run after each slice from the `yidl` repository root:

```bash
uv run --with pytest pytest tests/generation/test_data_write_policy.py -q
uv run --with pytest pytest tests/test_yidl_goldens.py -q
```

Expected focused test files by slice:

- Slice 1: `tests/generation/test_data_write_policy.py`
- Slice 2: `tests/generation/test_data_ports.py`
- Slice 3: `tests/generation/test_data_productions.py`
- Slice 4: `tests/generation/test_data_matcher_productions.py`
- Slice 5, if triggered: `tests/generation/test_data_fragments.py`

Run before declaring a slice done:

```bash
uv run --with pytest pytest -q
```

Python-version matrix validation remains the broader project-level check once
the feature is stable enough to sweep. Any slice that emits generated operation
source must stay compatible with the supported Python 3.12-3.15 sweep.

Each slice that changes generated source must also update
`dev-docs/YidlDesignSummary.md` if any §26.1 statement becomes stale.

## Diagnostics

Production errors should be explicit and local:

- invalid policy object
- collection or matcher from another DDS
- target production collection without required identity
- identity expression mismatch, including `identity=` disagreeing with
  `values[target.identity]`
- missing identity value
- write-policy duplicate/replacement failure
- non-`PortAddress` target value in a port-indexed production
- single-port cardinality conflict
- source-emission failure for a value expression

Use direct `TypeError` / `ValueError` messages with production name,
collection name, and property/port name where available. If a failure exposes
a design hole rather than an implementation bug, stop and classify it before
coding around it. Significant failures should follow the project-level
diagnostic categories in `dev-docs/YidlDesignSummary.md` instead of becoming
opaque runtime errors.

Produced-record provenance metadata is out of V1. Debugging relies on
production-level error messages and generated source inspection until a real
traceability use case requires stored provenance.

## Code-Bloat Guardrails

Before adding any new class or public method, check whether it is one of these
existing concepts with missing behavior:

- `transform(...)` vs `production(...)`
- `ValueExpression` vs a new value-expression tree
- `CollectionSpec` / `ComputedCollectionSpec` vs a new source-sequence type
- `MatcherSpec` / `MatcherResult` vs a new matcher-result wrapper
- `CollectionCardinality` vs a new cardinality enum/tag
- `DDSContainerBuilder.add(...)` vs a new write helper
- `emit_container_runtime_source(...)` vs a separate source emitter

New APIs are acceptable when they name a genuinely new semantic concept:

- merge policy
- port / port address
- production group
- matcher-result source expression
- definition fragment

They are not acceptable when they only repackage existing DDS data shapes under
another vocabulary.
