# YIDL Fluent DDS Examples

Status: superseded by `dev-docs/YidlRecordedCapsuleBuilderDesign.md` and
`dev-docs/YidlRecordedCapsuleDataDrivenApiProposal.md`. This document captures
the earlier live-wrapper direction; the current direction is recorded capsule
builders and immutable concept plans.

## Purpose

The current DDS and capsule APIs are capable but too low-level for capsule
extension work. They expose the right mechanics, but end users of the capsule
layer currently have to hand-wire too many pieces:

- repeated `dds.ensure_property(...)` boilerplate
- repeated `dds.ensure_record(...)` / `ensure_collection(...)` calls
- manual `load_runtime(...)` value-name, evaluator-name, and runtime-global
  aggregation
- manual capsule dependency ordering, such as adding property concepts before
  frozen property overrides

This document proposes a thin fluent layer above the existing DDS model. The
underlying DDS objects remain the source of truth; the fluent layer is an API
for declaring capsule-owned schema and runtime bundles compactly and reliably.

## Non-Goals

1. Do not replace `DataDefinitionSystem`, records, collections, ports,
   productions, matchers, or generated values.
2. Do not create parallel schema types.
3. Do not make generated decorator/runtime paths invoke the Python parser.
4. Do not use strings or enums as semantic behavior values where the existing
   DDS uses objects.
5. Do not require callers to manually pick value names, evaluator names, or
   globals when those are already declared by the contributing capsule concept.

## Current Pain

Today a simple field property is declared like this:

```python
def frozen_prop(dds: DataDefinitionSystem) -> PropertySpec:
    return dds.ensure_property(
        "Frozen",
        bool,
        default=False,
        storage_name="frozen",
    )
```

This is too much ceremony for a concept author. In ordinary capsule code the
intent should be visible as a semantic declaration, not as repeated plumbing.

Likewise, composing a property capsule with a frozen override currently needs
manual runtime bundle wiring:

```python
definition = build_property_capsule_definition("PropertyConcepts").extend(
    concept("frozen-property-overrides", define_frozen_property_overrides),
)
runtime = definition.load_runtime(
    evaluator_names=PROPERTY_EVALUATOR_NAMES,
    value_names=(
        *PROPERTY_TEMPLATE_VALUE_NAMES,
        *FROZEN_PROPERTY_TEMPLATE_VALUE_NAMES,
    ),
    runtime_globals={
        **PROPERTY_EVALUATOR_GLOBALS,
        **PROPERTY_TEMPLATE_GLOBALS,
        **FROZEN_PROPERTY_TEMPLATE_GLOBALS,
    },
)
```

That is not a scalable end-user surface. The concept that contributes a rule or
template should also contribute its runtime emission bundle and dependencies.

## Superseded Live DDS Layer

This earlier draft assumed a live wrapper around a `DataDefinitionSystem`. That
is no longer the preferred model. The current direction is a recorded
`CapsuleConceptBuilder` that builds an immutable concept plan and replays later
into a concrete DDS.

### Property Declaration

Property declaration should default from the name and type:

```python
Frozen = fdds.add_property.Frozen(bool)
Name = fdds.add_property.Name(str, default=REQUIRED)
Kind = fdds.add_property.Kind(str, default="plain")
```

Defaults:

1. `storage_name` defaults to snake/lower form of the property name.
2. `default` defaults to `value_type()` when that call is safe and meaningful.
   Examples: `bool() -> False`, `int() -> 0`, `str() -> ""`.
3. Required properties are explicit: `default=REQUIRED`.
4. For `object`, callable defaults, and unknown construction semantics, require
   the caller to pass `default=...` explicitly.

The fluent layer should not silently guess a mutable default. Mutable defaults
must still be explicit and validated according to existing DDS rules.

### Records And Extension Points

A root class schema concept can declare a shared record once:

```python
FieldInput = fdds.add_record.FieldInput(Name, Init, Kind, Defaulted, DefaultValue, Order)
```

A dependent concept can extend that record:

```python
Frozen = fdds.add_property.Frozen(bool)
fdds.extend_record.FieldInput(Frozen)
```

This replaces ad hoc helpers like `extend_field_input_record(...)` with a
first-class concept-extension surface. The underlying implementation can still
call `RecordSpec.extend_properties(...)`.

Rules:

1. Records are defined once by an owning concept.
2. Extension points must be declared intentionally by the owning concept or
   by a root schema capsule.
3. A concept may extend only declared extension points.
4. Extending a record after the generated record class has been materialized is
   an implementation error.
5. Diamond composition is allowed when the same property extension is reached
   through multiple dependency paths; identical extensions coalesce.
6. Conflicting property definitions reject.

### Collections, Computed Collections, And Ports

Fluent declarations should mirror existing DDS nouns:

```python
Fields = fdds.add_collection.Fields(FieldInput, cardinality=fdds.many, identity=Name)
InitFields = fdds.add_computed_collection.InitFields(
    source=Fields,
    when=(Init.eq(True),),
)
ClassBody = fdds.add_port.Class.body(cardinality=fdds.many)
ClassName = fdds.add_port.Class.name(cardinality=fdds.single)
```

The exact attribute path syntax can be refined, but the API should avoid raw
string repetition in ordinary concept code.

### Matchers And Rules

The matcher API should remain object-based, but fluent DDS should reduce setup:

```python
PropertyTemplate = fdds.add_matcher.PropertyTemplate()
field = PropertyTemplate.input.field(Fields)
PropertyTemplate.default(PLAIN_PROPERTY)
PropertyTemplate.rule.managed(
    when=(field.prop(Kind).eq(MANAGED_FIELD),),
    resource=MANAGED_PROPERTY,
)
```

A separate frozen concept should be able to reopen the same matcher and add
more specific rules:

```python
PropertyTemplate = fdds.use_matcher.PropertyTemplate()
field = PropertyTemplate.input.field(Fields)
PropertyTemplate.rule.readonly_plain(
    when=(field.prop(Frozen).eq(True), field.prop(Kind).eq(PLAIN_FIELD)),
    resource=READONLY_PROPERTY,
)
```

This is the intended override model: more-specific rules contributed by a
composed concept win through the existing matcher scoring semantics. It is not
Python subclass override.

### Productions

Productions can become easier to read without changing semantics:

```python
fdds.add_production.Property(
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

This should lower to the existing `dds.production(...)` and
`dds.ensure_production_group(...)` calls.

## Capsule Runtime Bundles

A concept should carry the runtime emission facts it introduces:

```python
PropertyConcept = capsule_concept(
    "property-productions",
    define_property_productions,
    values=PROPERTY_TEMPLATE_VALUE_NAMES,
    globals=PROPERTY_TEMPLATE_GLOBALS,
    evaluators=PROPERTY_EVALUATOR_NAMES,
)

FrozenPropertyOverrides = capsule_concept(
    "frozen-property-overrides",
    define_frozen_property_overrides,
    requires=(PropertyConcept,),
    values=FROZEN_PROPERTY_TEMPLATE_VALUE_NAMES,
    globals=FROZEN_PROPERTY_TEMPLATE_GLOBALS,
)
```

Then runtime loading becomes:

```python
runtime = FrozenPropertyCapsule.runtime().load()
```

or:

```python
runtime = capsule_runtime(FrozenPropertyCapsule).load()
```

The loader should compute transitive closure over concept dependencies,
compose concepts once, and aggregate:

- evaluator name maps
- value name maps
- runtime globals
- generated-value resources
- concept contributors

A caller should not manually splice these maps for ordinary capsule use.

## Capsule Dependencies And Inheritance

Capsules should declare concept dependencies explicitly:

```python
FrozenPropertyCapsule = capsule("FrozenPropertyCapsule").uses(
    FrozenFieldSchema,
    PropertyCapsule,
    FrozenPropertyOverrides,
)
```

Dependency rules:

1. If a concept needs a matcher/record/collection owned by another concept, it
   declares that dependency.
2. The capsule runtime builder orders concepts by dependency closure.
3. Diamond dependencies coalesce by concept identity/name.
4. Re-declaring the same property/record/collection identically is allowed only
   through the owning concept or an explicit extension point.
5. Conflicting declarations reject early with a capsule-composition diagnostic.

For the frozen/property case:

1. `PropertyCapsule` owns the base `PropertyTemplate` matcher and writable
   property rules.
2. `FrozenFieldSchema` owns the `Frozen` property and extends `FieldInput`.
3. `FrozenPropertyOverrides` depends on both and adds read-only matcher rules.
4. A user selecting frozen properties should not have to remember to include
   property first; the frozen capsule/concept should pull that in itself.

## Suggested End-State Example

```python
class_schema = capsule("class-field-schema").define(lambda dds: (
    dds.add_property.Name(str, default=REQUIRED),
    dds.add_property.Init(bool),
    dds.add_property.Kind(str, default="plain"),
    dds.add_record.FieldInput(Name, Init, Kind),
    dds.add_collection.Fields(FieldInput, cardinality=dds.many, identity=Name),
))

property_capsule = capsule("property").requires(class_schema).define(
    define_property_productions,
    values=PROPERTY_TEMPLATE_VALUE_NAMES,
    globals=PROPERTY_TEMPLATE_GLOBALS,
    evaluators=PROPERTY_EVALUATOR_NAMES,
)

frozen_capsule = capsule("frozen").requires(property_capsule).define(lambda dds: (
    dds.add_property.Frozen(bool),
    dds.extend_record.FieldInput(Frozen),
    define_frozen_property_overrides(dds),
), values=FROZEN_PROPERTY_TEMPLATE_VALUE_NAMES, globals=FROZEN_PROPERTY_TEMPLATE_GLOBALS)

runtime = frozen_capsule.runtime().load()
```

The exact syntax is negotiable. The important point is that dependency closure,
runtime-bundle aggregation, and common DDS declarations are encapsulated.

## Implementation Notes

1. Start by adding metadata fields to `CapsuleConcept` for dependencies and
   runtime bundle contributions.
2. Add a runtime builder object that aggregates concept dependencies and calls
   the current `CapsuleDefinition.load_runtime(...)` underneath.
3. Add the fluent DDS wrapper after the runtime-bundle problem is solved, so it
   can reuse existing concept ordering and diagnostics.
4. Keep existing low-level DDS APIs available. The fluent API is a higher layer,
   not a replacement for the schema engine.
5. Use the existing golden tests as behavior anchors. Success behavior should
   keep using the goldens harness; bespoke tests should focus on dependency
   closure, duplicate concept coalescing, and conflict diagnostics.

## Open Questions

1. Should fluent declarations be attribute-only (`add_property.Frozen(bool)`) or
   also data-driven (`add_property("Frozen", bool)`) for generated definitions?
   Both may be needed, but the data-driven form is required eventually.
2. Should concept dependencies be named by object identity, stable concept id,
   or both?
3. Should record extension points be opt-in on each record, or should every
   record be extendable until materialized?
4. Should default derivation from type constructors be limited to known scalar
   types only?
5. Should runtime bundle aggregation reject duplicate source names even when
   values are identical, or coalesce identical pairs?
