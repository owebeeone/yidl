# YIDL Recorded Capsule Builder Implementation Plan

## Objective

Implement the recorded capsule builder model from
`dev-docs/YidlRecordedCapsuleBuilderDesign.md`.

The practical goal is to make capsule definitions replayable data instead of
functions that mutate a live `DataDefinitionSystem`. A concept should describe
what it contributes, what it extends, and what generated runtime values it
needs. Applying that concept should lower into the current DDS, matcher,
production, and runtime-source layers.

The objective is not to create a second schema system, matcher engine,
container model, production runner, or source emitter. If the current layer owns
the right concept but has an awkward API, fix that layer. The recorded builder
is an authoring/replay layer over the current implementation.

The target user-facing shape is:

```python
PropertyBuilder = capsule_concept("property")

Name = PropertyBuilder.props.Name(str, REQUIRED)
Kind = PropertyBuilder.props.Kind(str, "plain")
FieldInput = PropertyBuilder.records.FieldInput(Name, Kind)
Fields = PropertyBuilder.collections.Fields(FieldInput, identity=Name)

PropertyTemplate = PropertyBuilder.matchers.PropertyTemplate()
field = PropertyTemplate.input.field(Fields)
PropertyTemplate.rule.managed(
    when=(field.prop(Kind).eq(MANAGED_FIELD),),
    resource=from_astichi_code("... managed property ..."),
)

PropertyConcept = PropertyBuilder.build()
runtime = PropertyConcept.runtime().load()
```

## Current State

The current implementation has the needed lower layers:

1. `DataDefinitionSystem`, properties, records, unions, collections, computed
   collections, port indexes, productions, and production groups.
2. `DDSContainerBuilder`, write policies, computed collections, matcher-backed
   sources, and generated container runtime source.
3. `MatcherSpec`, matcher tuple extraction, generated matcher runtime source,
   `MatcherGeneratedValue`, `from_astichi_code(...)`, `from_literal(...)`, and
   `constructor_expr_for(...)`.
4. Recorded capsule primitives in `yidl.capsule.recorded_builder`, including
   `CapsuleConceptBuilder`, `CapsuleConceptPlan`, `CapsuleRuntime`, and
   `runtime().load()`.
5. Concrete recorded concept modules for class, slots, init, property, and frozen
   behavior.

The missing layer is not another code generator. The missing layer is a
recorded authoring surface that can replay into these current APIs, compute
extension closure, and discover generated values from matcher-selected
resources without manual side tables.

## Non-Negotiable Constraints

1. Reuse the current DDS, matcher, production, container, and capsule runtime
   implementations.
2. Do not introduce `ConceptPropertySpec`, `ConceptMatcherSpec`, or similar
   duplicate semantic objects.
3. Do not make generated decorator or field-spec runtime paths invoke the Python
   parser.
4. Do not require concept users to pass manual `value_names`,
   `runtime_globals`, or template globals for generated values discoverable
   from recorded matcher resources and production operands.
5. `from_astichi_code(...)` and `from_literal(...)` remain the generated-value
   authoring surface for V1.
6. A `CapsuleConceptBuilder` records operations and cannot run.
7. A built `CapsuleConceptPlan` is immutable and is the only object that can be
   replayed, used as a extension, or loaded.
8. Prefer golden tests for successful generated behavior. Use bespoke tests for
   mechanics, failures, and diagnostics.
9. It is acceptable to break internal tests while removing boilerplate, provided
   the final behavior remains covered by existing semantics/goldens or by
   intentionally updated goldens.
10. Data-driven builder forms are deferred until a concrete migration requires
    them.

## Stop Conditions

Stop and fix an existing layer instead of adding a recorded-builder workaround
when any of these appear:

1. A recorded operation needs to duplicate validation already present in
   `DataDefinitionSystem` or `MatcherSpec`.
2. Runtime source emission requires manual value maps for generated values that
   are already reachable from matcher rules/defaults or production expressions.
3. A concept API needs a data-driven spelling of an existing fluent DDS action.
   Add the data-driven spelling beside the existing layer rather than building
   a separate concept-only path.
4. A source-generation issue is really an Astichi marker/API gap. Fix Astichi
   instead of hard-coding source strings in YIDL.
5. A plan object starts carrying behavior that belongs to `DataDefinitionSystem`,
   `MatcherSpec`, `ProductionSpec`, or `CapsuleRuntime`.

## Layer Mapping

Recorded operations should replay to existing targets:

| Recorded operation | Existing target |
|---|---|
| `props.Name(str, REQUIRED)` | `DataDefinitionSystem.ensure_property(...)` |
| `records.FieldInput(...)` | `DataDefinitionSystem.ensure_record(...)` |
| `extend_record.FieldInput(...)` | `RecordSpec.extend_properties(...)` |
| `collections.Fields(...)` | `DataDefinitionSystem.ensure_collection(...)` |
| `computed.InitFields(...)` | `DataDefinitionSystem.ensure_computed_collection(...)` |
| `ports.Class.body(...)` | `DataDefinitionSystem.ensure_port(...)` |
| `matchers.PropertyTemplate()` | `DataDefinitionSystem.ensure_matcher(...)` |
| matcher default/rule | `MatcherSpec.default(...)` and `MatcherSpec.rule(...)` |
| `productions.Property(...)` | `DataDefinitionSystem.production(...)` |
| `.in_group("Properties")` | `DataDefinitionSystem.ensure_production_group(...)` |
| `runtime().load()` | recorded runtime source emission plus `CapsuleRuntime` |

If a method does not exist but the semantic object already does, add the method
to the existing layer.

## Core Architecture

### Builder And Plan

`CapsuleConceptBuilder` is mutable and records operations. It must not replay,
load, or emit.

`CapsuleConceptPlan` is immutable and contains:

1. concept identity and name
2. extension plans
3. typed recorded operations
4. runtime helper declarations
5. stable diagnostics metadata

Only plans can be extensions.

### Symbolic Handles

The builder returns symbolic handles for every future DDS object:

1. property handle
2. record handle
3. collection handle
4. computed collection handle
5. port handle
6. matcher handle
7. matcher input handle
8. production handle

Handles should be inert immutable references. They can carry owner concept id,
semantic name/path, target kind, and declaration sequence. They must not carry
DDS behavior.

Replay resolves handles through a `ReplayContext`:

```python
context.resolve(NameHandle) -> PropertySpec
context.resolve(FieldsHandle) -> CollectionSpec
context.resolve(PropertyTemplateHandle) -> MatcherSpec
```

Direct handle reuse is the preferred API. Data-driven lookup by name/path is a
separate ergonomic surface and should be added only where needed.

### Definition Ownership And Reference Handles

Only one concept defines a DDS entity. Other concepts reference that entity
through a extension handle namespace:

```python
PropertyConcept = PropertyBuilder.build()

FrozenBuilder = capsule_concept("frozen", extends=(PropertyConcept,))
Property = FrozenBuilder.use(PropertyConcept)

Name = Property.props.Name
Kind = Property.props.Kind
Fields = Property.collections.Fields
FieldInput = Property.records.FieldInput
PropertyTemplate = FrozenBuilder.use_matcher(Property.matchers.PropertyTemplate)
```

`builder.use(plan)` returns read-only handles exported by `plan`. It does not
record new definitions. Replay validates that `plan` is in the extension
closure and resolves the handle to the original owner operation.

For V1, all handles recorded by a built plan are exported. A later private/public
visibility model can narrow that if concept boundaries need it.

Redefinition is not reference. If a dependent concept writes
`FrozenBuilder.props.Name(str, REQUIRED)`, that is a new property-definition
operation and should reject during build/replay when another concept already owns
the semantic `Name` property. The only automatic coalescing is replaying the
same owner operation through extension diamonds.

### Operation Log

The builder records typed operations, not callbacks. V1 operations:

1. property definition
2. record definition
3. record extension
4. collection definition
5. computed collection definition
6. port definition
7. matcher definition
8. matcher input definition
9. matcher default
10. matcher rule
11. production definition
12. production group membership
13. runtime helper declaration

Replay orders operations by semantic category, then by declaration order within
the category. That gives deterministic output without depending on the order a
concept author happened to mention a downstream object.

### Extension Closure

Extension rules:

1. Extensions are plans, not strings.
2. Replay computes transitive closure before touching a DDS.
3. Diamond extensions coalesce by plan identity.
4. Replaying the same plan twice is a no-op in the same replay context.
5. Conflicting declarations reject with a capsule-composition diagnostic.

## Matched Resources And Generated Values

Matcher resources are values, not names. The concept author writes:

```python
PropertyTemplate.default(from_astichi_code("... plain property ..."))
PropertyTemplate.rule.managed(
    when=(field.prop(Kind).eq(MANAGED_FIELD),),
    resource=from_astichi_code("... managed property ..."),
)
```

`match.resource()` in a production means "the generated value selected by the
matcher result." It must carry the original `MatcherGeneratedValue` object
through to the generated runtime. There should be no public resource registry,
no `*_VALUE_NAMES`, and no `*_GLOBALS` for these values.

Implementation requirements:

1. Recorded matcher defaults/rules retain the `MatcherGeneratedValue` operand.
2. Recorded productions retain `match.resource()` as a value expression that
   reads the selected generated value from the matcher result.
3. Runtime emission discovers generated values by walking matcher defaults,
   matcher rules, production values, and any future generated-value operands.
4. Existing `constructor_expr_for(...)` emits the source expression needed to
   reconstruct a `MatcherGeneratedValue`.
5. If the emitter hoists repeated values, hoisting names are private and
   deterministic.

V1 can keep `MatcherGeneratedValue` as the generated-value type. If we need a
more general value later, it should extend the current matcher value model, not
create a concept-only resource type.

## Runtime Helpers

Generated values are discoverable. Other helpers are not always discoverable and
need explicit registration:

```python
builder.runtime.evaluator(property_order_for)
builder.runtime.evaluator(property_order_for, name="property_order_for")
```

Rules:

1. Explicit `name=` wins.
2. Name inference is allowed only when deterministic.
3. Duplicate same-name same-object helpers coalesce.
4. Duplicate same-name different-object helpers reject.
5. Helpers aggregate through extension closure.

The runtime loader should pass these helpers through the current runtime source
emission path rather than inventing a second generated module loader.

## Record Extension Policy

V1 should use the current extension capability but not hide ownership problems.

Recommended behavior:

1. `extend_record.FieldInput(Frozen)` succeeds when `FieldInput` exists in the
   concept or extension closure.
2. Replay rejects extension after the record class has been materialized.
3. Identical repeated extensions coalesce.
4. Conflicting property definitions reject through existing DDS validation.
5. Explicit extension points remain the likely long-term API, but V1 may use a
   permissive migration path while replacing current concept code.

## Implementation Slices

### Slice 1: Concept Plans, Properties, Extensions

Goal: introduce the recorded builder and immutable plan with the smallest replay
surface.

APIs:

```python
builder = capsule_concept("property")
Name = builder.props.Name(str, REQUIRED)
plan = builder.build()

child = capsule_concept("child", extends=(plan,))
Parent = child.use(plan)
SameName = Parent.props.Name
plan.apply(dds)
```

Implement:

1. `CapsuleConceptBuilder`
2. `CapsuleConceptPlan`
3. property symbolic handles
4. recorded property operations
5. replay context
6. extension closure and diamond coalescing
7. property conflict diagnostics
8. read-only extension reference namespaces through `builder.use(plan)`

Reuse/fix:

1. Replay calls `DataDefinitionSystem.ensure_property(...)`.
2. Do not create a new property spec type.
3. If the current capsule contributor API cannot host plans cleanly, replace the
   contributor call path with plan replay rather than wrapping callbacks.

Tests:

1. Bespoke: builder cannot be replayed directly.
2. Bespoke: plan is immutable after build.
3. Bespoke: extension closure replays parent before child.
4. Bespoke: diamond extension replays once.
5. Bespoke: replaying the same owner property operation through a extension
   diamond coalesces.
6. Bespoke: conflicting property declarations reject.
7. Bespoke: `builder.use(parent).props.Name` references the parent-owned
   property without recording a new property operation.
8. Bespoke: redefining a extension-owned property in a child concept rejects,
   even if the spelling and type match.

Goldens:

No success golden is required in this slice unless it exposes generated runtime
source more cleanly than bespoke tests.

### Slice 2: Records, Extensions, Collections, Computed Collections, Ports

Goal: express the class/field schema shape without matchers or productions.

APIs:

```python
FieldInput = builder.records.FieldInput(Name, Kind)
Fields = builder.collections.Fields(FieldInput, cardinality=builder.many, identity=Name)
InitFields = builder.computed.InitFields(source=Fields, when=(Init.eq(True),))
ClassBody = builder.ports.Class.body(cardinality=builder.many)

Parent = child.use(parent_plan)
child.extend_record(Parent.records.FieldInput, Frozen)
```

Implement:

1. record, collection, computed collection, and port handles
2. recorded operations for each object
3. replay for record extension through `RecordSpec.extend_properties(...)`
4. dotted port path proxy
5. extension reference namespaces for records, collections, computed
   collections, and ports

Reuse/fix:

1. Replay calls existing DDS `ensure_record`, `ensure_collection`,
   `ensure_computed_collection`, and `ensure_port`.
2. Keep `RecordSpec.extend_properties(...)`; do not add another extension layer.
3. If port cardinality or port-index emission is awkward, fix the existing port
   layer.

Tests:

1. Bespoke: record extension resolves through extension handles.
2. Bespoke: unknown extension target rejects.
3. Bespoke: extending after record-class materialization rejects.
4. Bespoke: port dotted path lowers to stable semantic port object.
5. Bespoke: extension-owned record/collection/port handles can be used in child
   concepts without redefining the target entity.

Goldens:

Use `tests/data/gold_src/capsule_property_concepts.py` or a narrow new golden
only when the slice changes generated runtime source.

### Slice 3: Matchers, Rules, Matched Resources, Productions

Goal: make property/frozen concepts expressible with recorded builders and
inline generated resources.

APIs:

```python
PropertyTemplate = builder.matchers.PropertyTemplate()
field = PropertyTemplate.input.field(Fields)

PropertyTemplate.default(from_astichi_code("... plain property ..."))
PropertyTemplate.rule.managed(
    when=(field.prop(Kind).eq(MANAGED_FIELD),),
    resource=from_astichi_code("... managed property ..."),
)

builder.productions.Property(
    source=PropertyTemplate.results(),
    target=Components,
    values={Template: match.resource()},
    policy=AddIfAbsent,
).in_group("Properties")

Parent = child.use(parent_plan)
ParentTemplate = child.use_matcher(Parent.matchers.PropertyTemplate)
```

Implement:

1. matcher and matcher-input handles
2. matcher default and rule operations
3. `match.resource()`, `match.record("field")`, and `match.value(index)` value
   expressions using the existing matcher-result source model
4. production and production-group operations
5. replay to existing `MatcherSpec` and `DataDefinitionSystem.production(...)`
6. generated-value discovery from matcher defaults/rules and production
   operands
7. generated runtime emission without manual value maps for discovered
   generated values

Reuse/fix:

1. Use existing `MatcherSpec` rule/default APIs.
2. Use existing `MatcherGeneratedValue`, `from_astichi_code(...)`,
   `from_literal(...)`, and `constructor_expr_for(...)`.
3. Fix `container_runtime_source` or matcher value emission if source emission
   still requires explicit name maps for discoverable generated values.
4. Do not introduce `ConceptResource`, `builder.resources.astichi_code(...)`, or
   a named resource registry.

Tests:

1. Bespoke: generated values in matcher defaults/rules are discovered.
2. Bespoke: identical generated values dedupe if the emitter hoists them.
3. Bespoke: discovered generated values emit source without explicit value maps.
4. Bespoke: matcher rule replay preserves specificity/score behavior.
5. Bespoke: production replay preserves target/source validation.
6. Bespoke: `match.resource()` carries the matched generated value, not a string
   name.
7. Bespoke: a child concept can add rules to a extension-owned matcher through
   `use_matcher(...)` without redefining the matcher.

Goldens:

1. Update `tests/data/gold_src/capsule_property_concepts.py` to use recorded
   property/frozen builders.
2. Keep generated behavior stable: writable plain/managed properties get
   setters; frozen plain/managed properties do not.
3. Prefer this golden over duplicating success-path assertions in bespoke tests.

### Slice 4: Runtime Loader And Helper Aggregation

Goal: replace user-facing manual runtime assembly with concept-plan loading.

APIs:

```python
builder.runtime.evaluator(property_order_for)
builder.runtime.evaluator(property_order_for, name="property_order_for")

runtime = ConceptPlan.runtime().load()
```

Implement:

1. concept runtime loader object
2. extension closure aggregation
3. evaluator/helper aggregation
4. generated-value aggregation from the replayed concept graph
5. direct delegation to `emit_container_runtime_source(...)`

Reuse/fix:

1. Reuse or extend `CapsuleRuntime` unless a concrete limitation appears.
2. Delegate directly to `emit_container_runtime_source(...)`; do not reintroduce
   the removed callback-based capsule bridge.
3. Do not make a second generated runtime namespace type unless `CapsuleRuntime`
   cannot serve the plan.

Tests:

1. Bespoke: helper name inference when reliable.
2. Bespoke: explicit helper name override.
3. Bespoke: duplicate helper name with different value rejects.
4. Bespoke: extension helper aggregation coalesces duplicate same helper.
5. Bespoke: generated values discovered from extension concepts are available
   during runtime source emission.

Goldens:

Existing capsule property/frozen goldens should no longer manually pass
generated-value maps or runtime globals for matcher resources.

### Slice 5: Migrate Concrete Concepts And Delete Boilerplate

Goal: move concrete capsule concepts to the recorded builder and remove manual
aggregation code.

Targets:

1. `src/yidl/capsule/class_concepts.py`
2. `src/yidl/capsule/slots_concepts.py`
3. `src/yidl/capsule/init_concepts.py`
4. `src/yidl/capsule/property_concepts.py`
5. `src/yidl/capsule/frozen_concepts.py`
6. `src/yidl/capsule/base_capsule.py`
7. `src/yidl/capsule/init_only_capsule.py`

Approach:

1. Migrate one concept at a time.
2. Delete helper functions made redundant by the recorded builder.
3. Avoid dual implementations unless a temporary compatibility shim keeps the
   transition smaller.
4. Prefer fewer library lines over preserving internal helper APIs.
5. Keep generated semantics stable under goldens.

Tests:

1. Existing focused capsule/generation tests.
2. Existing golden suite.
3. Python-version sweep.

## Deferred Work: Data-Driven Builder Forms

This work is intentionally deferred. Add function-call equivalents for dynamic
concept authoring only when concrete migration or rule-driven concept authoring
requires them.

Possible APIs:

```python
builder.props.define("Frozen", bool, default=False)
builder.records.define("FieldInput", Name, Kind)
builder.matchers.define("PropertyTemplate")
builder.ports.define("Class.body", cardinality=builder.many)
```

Rules:

1. Attribute syntax and data-driven syntax must record the same operation type.
2. Data-driven syntax is not a new semantic layer.
3. Do not implement this speculatively.
4. The extension reference namespace comes first; data-driven lookup should not
   be used to paper over missing owner/reference semantics.

## Verification Strategy

Focused tests:

```bash
PYTHONPATH=../astichi/src uv run --with pytest pytest tests/capsule tests/generation -q
```

Golden tests:

```bash
PYTHONPATH=../astichi/src uv run --with pytest pytest tests/test_yidl_goldens.py -q
```

Full suite:

```bash
PYTHONPATH=../astichi/src uv run --with pytest pytest -q
```

Version sweep:

```bash
PYTHONPATH=../astichi/src uv run python -m yidl.testing.versioned_test_harness run-tests-all --pytest-args -q
PYTHONPATH=../astichi/src uv run python -m yidl.testing.versioned_test_harness run-tests --python 3.15 --pytest-args -q
```

## Golden Coverage Shape

Use goldens for successful generated behavior:

1. property/frozen concept runtime source
2. slots/init/property class sketch behavior
3. matched resource propagation into component records
4. generated runtime source that reconstructs `from_astichi_code(...)` values
5. extension-driven concept loading

Use bespoke tests for:

1. builder immutability
2. extension conflicts
3. invalid handle resolution
4. duplicate helper names
5. generated-value discovery/dedupe mechanics
6. record extension timing diagnostics

## Diagnostics

The plan should produce explicit errors for:

1. replaying a builder instead of a plan
2. conflicting property/record/collection/port declarations
3. extending a missing or closed record
4. unresolved symbolic handles
5. duplicate runtime helper names with different values
6. generated value operands that cannot be emitted by the existing matcher value
   source machinery
7. matcher resource expressions that are strings or registry names when a
   `MatcherGeneratedValue` is required

Diagnostics should name the concept and recorded operation where possible.

## Risks And Mitigations

1. **Recorded handles become a second DDS.**
   Keep handles inert. They resolve to DDS objects and never validate behavior
   independently of DDS except for handle ownership checks.

2. **Runtime loader duplicates `CapsuleRuntime`.**
   Extend/reuse `CapsuleRuntime` first. Add a new type only if the old one
   cannot represent concept-plan loading without worse code.

3. **Generated resource handling grows a registry.**
   Reject public registries. Use value operands and existing
   `MatcherGeneratedValue` construction. Hoisting is private source-emitter
   implementation detail.

4. **Concept migration leaves two full systems.**
   Temporary compatibility is acceptable. Final concept modules should converge
   on one authoring style.

5. **Data-driven forms create another API surface too early.**
   Add them only when a concrete migration or rule-driven concept needs dynamic
   names.

6. **Astichi gaps leak into YIDL as string workarounds.**
   Stop and fix Astichi marker/lowering surfaces when a generated snippet needs
   syntax the current Astichi API should be able to express.

## Done Criteria

1. Property/frozen concepts are authored through recorded builders.
2. Frozen depends on property and loads it automatically.
3. Dependent concepts reference parent-owned properties, records, collections,
   ports, and matchers through extension handle namespaces rather than
   redefining them.
4. Matcher resources use inline `from_astichi_code(...)` values, not manual
   value-name/global tables.
5. `match.resource()` carries selected generated values through productions.
6. `ConceptPlan.runtime().load()` is the ordinary runtime-loading path.
7. Low-level DDS APIs remain available where they reduce code.
8. Concrete concept modules delete redundant manual aggregation code.
9. Goldens prove generated behavior remains stable or intentionally improves.
10. Full focused tests, golden tests, full suite, and version sweep pass.
