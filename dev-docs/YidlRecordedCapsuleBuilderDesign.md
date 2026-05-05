# YIDL Recorded Capsule Builder Design

## Purpose

Move capsule authoring from functions that mutate a live `DataDefinitionSystem`
to replayable concept plans. The goal is to make capsule definitions reusable,
composable, dependency-aware, and less boilerplate-heavy while still lowering to
the existing DDS/container/matcher implementation.

The current underlying DDS remains the execution target. This design changes how
capsule concepts are authored and composed.

## Core Idea

A capsule concept is a recorded operation graph, not a callback:

```python
PropertyBuilder = capsule_concept("property")

Name = PropertyBuilder.props.Name(str, REQUIRED)
Kind = PropertyBuilder.props.Kind(str, "plain")

FieldInput = PropertyBuilder.records.FieldInput(Name, Kind)
Fields = PropertyBuilder.collections.Fields(FieldInput, identity=Name)

PropertyTemplate = PropertyBuilder.matchers.PropertyTemplate()
field = PropertyTemplate.input.field(Fields)
PropertyTemplate.default(from_astichi_code("... plain property ..."))
PropertyTemplate.rule.managed(
    when=(field.prop(Kind).eq(MANAGED_FIELD),),
    resource=from_astichi_code("... managed property ..."),
)
```

No live DDS is needed while this code runs. The concept stores symbolic handles
and replayable operations. Applying the concept to a concrete DDS resolves those
handles into real DDS objects.

## Why This Exists

The function-based API does not scale:

1. Every feature repeats low-level `ensure_*` calls.
2. `load_runtime(...)` requires the caller to manually aggregate runtime values,
   evaluators, and globals from every concept.
3. Dependencies are implicit. A frozen-property override needs the property
   matcher, but the caller currently has to remember to include property first.
4. Concept declarations are not reusable as data. They are functions that can be
   called, not inspectable plans that can be merged, inherited, or replayed.

Recorded builders make concepts first-class data.

## Terms

1. **Concept builder**: mutable authoring object that records operations for one
   concept.
2. **Concept plan**: frozen recorded operation graph produced by the builder.
3. **Symbolic handle**: placeholder for a DDS object before replay, such as a
   property, record, collection, port, matcher, production, or matcher input.
4. **Replay context**: concrete DDS plus handle-resolution table used when a
   concept plan is applied.
5. **Runtime bundle**: values, globals, evaluators, and imports contributed by a
   concept for generated runtime source emission.

## Minimal API Shape

### Concept Creation

```python
PropertyBuilder = capsule_concept("property")
PropertyConcept = PropertyBuilder.build()

FrozenBuilder = capsule_concept("frozen", requires=(PropertyConcept,))
FrozenConcept = FrozenBuilder.build()
```

The builder and built concept are separate public types. The builder records
operations and cannot be replayed. Only a built concept plan can be applied,
loaded, or used as a dependency by runtime assembly. Building freezes the plan;
a concept plan is immutable.

### Properties

```python
Name = PropertyBuilder.props.Name(str, REQUIRED)
Kind = PropertyBuilder.props.Kind(str, "plain")
Frozen = FrozenBuilder.props.Frozen(bool)
```

Rules:

1. Second positional argument means `default`.
2. `storage_name` defaults from the property name.
3. `bool`, `int`, `str`, and similar scalar types may default to `type()` when
   the default is omitted.
4. `REQUIRED` remains explicit.
5. The symbolic property handle is reusable across records, matchers, and
   productions in the same recorded graph.

### Records And Extensions

```python
FieldInput = PropertyBuilder.records.FieldInput(Name, Kind)
FrozenBuilder.extend_record.FieldInput(Frozen)
```

Rules:

1. Record definitions create symbolic record handles.
2. Record extension operations target an existing record by symbolic name.
3. Extension operations require the target record to exist in this concept or a
   dependency at replay time.
4. Identical repeated extensions coalesce.
5. Conflicting record definitions reject.

### Collections And Computed Collections

```python
Fields = PropertyBuilder.collections.Fields(
    FieldInput,
    cardinality=PropertyBuilder.many,
    identity=Name,
)

InitFields = PropertyBuilder.computed.InitFields(
    source=Fields,
    when=(Init.eq(True),),
)
```

The handles lower to `dds.ensure_collection(...)` and
`dds.ensure_computed_collection(...)` during replay.

### Ports

```python
ClassBody = PropertyBuilder.ports.Class.body(cardinality=PropertyBuilder.many)
```

Port attribute paths create stable semantic names such as `Class.body`.

### Matchers

```python
PropertyTemplate = PropertyBuilder.matchers.PropertyTemplate()
field = PropertyTemplate.input.field(Fields)
PropertyTemplate.default(from_astichi_code("... plain property ..."))
PropertyTemplate.rule.managed(
    when=(field.prop(Kind).eq(MANAGED_FIELD),),
    resource=from_astichi_code("... managed property ..."),
)
```

A dependent concept can reopen the matcher:

```python
PropertyTemplate = FrozenBuilder.use_matcher.PropertyTemplate()
field = PropertyTemplate.input.field(Fields)
PropertyTemplate.rule.readonly_plain(
    when=(field.prop(Frozen).eq(True), field.prop(Kind).eq(PLAIN_FIELD)),
    resource=READONLY_PROPERTY,
)
```

The override behavior is still matcher scoring. The frozen rule wins because it
has more matched conditions than the base property rule.

### Productions

```python
PropertyBuilder.productions.Property(
    source=PropertyTemplate.results(),
    target=Components,
    values={
        Name: match.record("field").prop(Name),
        TargetPort: ClassBody.of("runtime"),
        Order: call("property-order", property_order_for),
        Template: match.resource(),
    },
    policy=AddIfAbsent,
).in_group("Properties")
```

Productions are recorded and replayed into the current DDS production API.

### Resources And Runtime Bundle

Concept builders record generated values where they are used. A template
resource should be the value passed into the matcher rule/default, not a named
resource plus side tables:

```python
PropertyTemplate.rule.managed(
    when=(field.prop(Kind).eq(MANAGED_FIELD),),
    resource=from_astichi_code(
        "@property\n"
        "def field_name__astichi_arg__(self):\n"
        "    return self.astichi_ref(external=working_path)\n"
        "\n"
        "@field_name__astichi_arg__.setter\n"
        "def field_name__astichi_arg__(self, value):\n"
        "    self.astichi_ref(external=working_path)._ = value\n"
    ),
)
```

The concept plan captures the generated value from the rule. Runtime emission
then reconstructs the value inline or hoists it to a generated private binding.
Ordinary callers should not manually pass value maps, evaluator maps, or globals
to `load_runtime(...)`. See `dev-docs/YidlRecordedCapsuleResourceModel.md` for
the resource model.

## Replay Model

Replay proceeds in dependency order:

1. Resolve dependency closure.
2. Topologically order concepts.
3. Create a fresh `DataDefinitionSystem`.
4. Replay property definitions.
5. Replay record and record-extension definitions.
6. Replay collections, computed collections, and ports.
7. Replay matchers and matcher rules.
8. Replay productions and groups.
9. Aggregate generated values and runtime helpers.
10. Emit/load the generated runtime source using the existing emitter.

Replay must be deterministic. Declaration order is preserved where the existing
DDS cares about order.

## Dependency And Diamond Rules

1. Dependencies are concept objects, not strings.
2. A concept can depend on another concept directly.
3. Diamond dependencies coalesce by concept identity.
4. Replaying the same concept twice is a no-op after the first replay.
5. Re-declaring identical schema objects is allowed only when the replayed
   operation is the same operation from the same concept graph or an explicit
   coalesced dependency.
6. Conflicting declarations reject with a capsule-composition diagnostic.

## Property/Frozen Example

Base property concept:

```python
PropertyBuilder = capsule_concept("property")

Name = PropertyBuilder.props.Name(str, REQUIRED)
Kind = PropertyBuilder.props.Kind(str, "plain")
Order = PropertyBuilder.props.Order(int, 0)
Template = PropertyBuilder.props.Template(object, REQUIRED)
TargetPort = PropertyBuilder.props.TargetPort(object, REQUIRED)

FieldInput = PropertyBuilder.records.FieldInput(Name, Kind, Order)
Fields = PropertyBuilder.collections.Fields(FieldInput, cardinality=PropertyBuilder.many, identity=Name)
Components = PropertyBuilder.collections.Components(...)
ClassBody = PropertyBuilder.ports.Class.body(cardinality=PropertyBuilder.many)

PropertyTemplate = PropertyBuilder.matchers.PropertyTemplate()
field = PropertyTemplate.input.field(Fields)
PropertyTemplate.default(from_astichi_code("... plain property ..."))
PropertyTemplate.rule.managed(
    when=(field.prop(Kind).eq(MANAGED_FIELD),),
    resource=from_astichi_code("... managed property ..."),
)
```

Frozen extension:

```python
PropertyConcept = PropertyBuilder.build()

FrozenBuilder = capsule_concept("frozen", requires=(PropertyConcept,))

FrozenProp = FrozenBuilder.props.Frozen(bool)
FrozenBuilder.extend_record.FieldInput(FrozenProp)

PropertyTemplate = FrozenBuilder.use_matcher.PropertyTemplate()
field = PropertyTemplate.input.field(Fields)
PropertyTemplate.rule.readonly_plain(
    when=(field.prop(FrozenProp).eq(True), field.prop(Kind).eq(PLAIN_FIELD)),
    resource=from_astichi_code("... readonly property ..."),
)
PropertyTemplate.rule.readonly_managed(
    when=(field.prop(FrozenProp).eq(True), field.prop(Kind).eq(MANAGED_FIELD)),
    resource=from_astichi_code("... readonly managed property ..."),
)
```

Runtime use:

```python
FrozenConcept = FrozenBuilder.build()
runtime = FrozenConcept.runtime().load()
```

This should automatically include the property concept, frozen schema extension,
read-only matcher rules, and all generated values/runtime helpers discovered
from the concept plan.

## Implementation Slices

### Slice 1: Recorded Properties, Generated Values, And Runtime Helpers

- Add separate `CapsuleConceptBuilder` and immutable `CapsuleConceptPlan` types.
- Support recorded property definitions.
- Support generated-value discovery and runtime helper aggregation.
- Replay properties into a live DDS.
- Add bespoke tests for dependency closure and duplicate/conflicting property
  definitions.

### Slice 2: Records, Record Extensions, Collections, Ports

- Add symbolic handles for records, collections, computed collections, and
  ports.
- Replay them into the existing DDS.
- Replace `extend_field_input_record(...)` usage with recorded
  `extend_record.FieldInput(...)`.
- Keep success behavior under the existing goldens.

### Slice 3: Matchers And Productions

- Record matcher definitions, matcher inputs, defaults, rules, productions,
  and groups.
- Rebuild property/frozen concepts using recorded builders.
- Golden `capsule_property_concepts.py` should remain the main success test.

### Slice 4: Runtime Loader Object

- Add a loader/builder object above `CapsuleDefinition.load_runtime(...)`.
- It aggregates dependency closure, discovered generated values, and runtime helpers automatically.
- Low-level `load_runtime(...)` remains as an escape hatch.

## Design Constraints

1. Do not remove the low-level DDS API.
2. Do not rewrite the generated container/matcher implementation.
3. Do not make concept authoring depend on Python source parsing.
4. Do not allow user-facing capsule setup to require manual generated-value
   or runtime-helper aggregation.
5. Prefer recorded object handles over raw strings in concept definitions.
6. Preserve existing goldens unless the generated source intentionally improves.

## Decisions

1. Builder and plan are separate public types. A `CapsuleConceptBuilder` records
   operations. A `CapsuleConceptPlan` is built from it and is the only object
   that can be replayed, loaded, or used as a stable dependency.
2. A concept builder does not run. It must be built before use. The built concept
   plan is immutable.
3. Generated values should be discovered from recorded operations; if emission
   hoists them, generated binding names are private implementation details.
4. The data-driven equivalent of attribute syntax needs a separate proposal.
   See `dev-docs/YidlRecordedCapsuleDataDrivenApiProposal.md`.

## Record Extension Issue

The open design issue is whether every record should be extendable by default,
or whether the owning concept must explicitly declare extension points. The
problem is not mechanics; `RecordSpec.extend_properties(...)` can append fields
before the generated record class is materialized. The problem is ownership and
diagnostics.

If all records are extendable, any dependent concept can do this:

```python
FrozenBuilder.extend_record.FieldInput(Frozen)
```

That is convenient, but it can accidentally mutate records that were meant to be
closed implementation details. A typo can also create confusing delayed replay
errors if the target record only appears in a different dependency branch.

If extension points are explicit, the owning concept writes something like:

```python
PropertyBuilder.records.FieldInput(Name, Kind).allow_extensions()
```

or:

```python
PropertyBuilder.extension_points.FieldInput()
```

Then dependent concepts can extend only declared extension points. That produces
better diagnostics and clearer ownership, but it adds one more declaration to
the base concept.

For the property/frozen case, `FieldInput` should be an extension point because
field kinds will keep adding semantic flags and properties (`Frozen`, managed
state, transaction metadata, ownership metadata, etc.). Internal records such as
produced component records may not need to be open by default.

Recommendation: require explicit extension points for public/shared records, and
allow a temporary V1 escape hatch only for current migration code.
