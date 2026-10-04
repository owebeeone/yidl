# YIDL Astichi Build Mapper

Design note for the isolated generation engine that maps YIDL generation inputs
onto an Astichi build graph.

## 1. Purpose

The current init-only capsule emitter proved the target generated surface, but
it is intentionally not the long-term architecture. YIDL needs a small,
isolated build-mapping library that takes reusable Astichi composable resources,
construct surfaces, spec-shaped inputs, filters/selectors, and rules, then
builds the Astichi graph generically.

The goal is to stop writing feature-specific emitters. A feature should add
generation tools; the mapper connects them.

## 2. Ownership Boundary

`yidl/generation` owns the generation interface contract.

Hard rules:

1. `yidl/generation` must not depend on `yidl.capsule` or any other current
   core capsule infrastructure.
2. All API shapes and interfaces for defining generator inputs must live in
   `yidl/generation`.
3. Other packages, including `yidl.capsule`, may derive from, adapt into, or
   wrap the `yidl/generation` interfaces.
4. Dependency direction is one-way:

```text
yidl.capsule / lifecycle semantics
        -> yidl.generation interfaces
        -> Astichi
```

Never:

```text
yidl.generation -> yidl.capsule
```

This keeps the mapper reusable for future YIDL input sources and for generated
surfaces that do not naturally fit the current capsule implementation.

## 3. Non-Goals

1. The mapper does not know lifecycle semantics.
2. The mapper does not know what `managed`, `field_spec`, `init`, `default`,
   or `__slots__` mean.
3. The mapper does not parse YIDL source.
4. The mapper does not create per-field Astichi composables from source text.
5. The mapper does not replace Astichi. It prepares and wires Astichi build
   graphs, then lets Astichi own composition, hygiene, and materialization.

## 4. Astichi Improvement Preference

YIDL is Astichi's first real production use case. The mapper should expose
Astichi gaps instead of burying them in YIDL-specific code.

Rules:

1. If the mapper needs a Python construct that Astichi does not model yet,
   prefer adding the missing Astichi surface.
2. Do not compensate for missing Astichi support with long-term string
   formatting, feature-specific AST surgery, or semantic shortcuts in YIDL.
3. Constructs such as exceptions, `match`, `elif`, `else`, and `for`-`else`
   are valid reasons to extend Astichi when they become generation needs.
4. Temporary workarounds must be documented as stopgaps and must not become
   the stable mapper architecture.

## 5. Core Model

The mapper input model is self-contained and should include these concepts.

### 5.1 Resource

A reusable Astichi composable resource.

Examples:

- factory root shell
- class metadata assignment
- method shell
- parameter payload
- assignment body payload
- class variable shell such as `__slots__ = (astichi_hole(items),)`
- slot item expression payload

Resources are registered once and reused. Runtime generator paths must bind or
specialize them structurally, not reparse fresh source per field.

### 5.2 Construct

A generated Python construct with named surfaces.

Examples:

- class construct
- method construct
- class variable construct
- slots construct
- helper function construct

The construct is not semantic by itself. It exposes surfaces that rules can
target.

The human-facing fluent spelling for slots can explain the shape:

```python
builder.classvar.add.Main.named("__slots__").items
```

That means:

- facade/class target: `Main`
- construct kind: class variable
- construct name: `__slots__`
- target surface: `items`

The mapper itself must not synthesize that attribute chain. It should carry the
same information as data, then lower it through Astichi's named/data-driven
builder API.

### 5.3 Surface

A named insertion target exposed by a construct.

Examples:

- `class_defs`
- `class_methods`
- `method_params`
- `method_body`
- `items` on `__slots__`

Surfaces map to Astichi holes/ports. The mapper owns the symbolic surface
model; Astichi owns the final port mechanics.

### 5.4 Spec Shape

A collection of resolved input records and named properties.

The mapper should treat specs structurally:

- spec name
- stable order
- property values
- optional derived properties supplied by the caller

The mapper must not depend on concrete capsule classes for this. A capsule can
adapt its own spec instances into mapper-owned spec records.

### 5.5 Selector / Filter

A rule predicate over spec records.

Examples:

- every `field_spec`
- `field_spec` where `init is True`
- fields with defaults
- fields that participate in slots

Selectors operate on mapper-owned spec/property interfaces.

### 5.6 Component Recipe

A declaration for a reusable construct component and its repeated entries.

Examples:

- slots component inserted into the class component bus
- init method component inserted into the class component bus
- parameter entries inserted into the init method's parameter target
- assignment body entries inserted into the init method's body target

Conceptual shape:

```python
ComponentRecipe(
    name="slots",
    component_resource="SlotsComponent",
    component_target="class_components",
    component_order=0,
    entry_target="slot_entries",
    entry_resource="SlotEntry",
    requires=("slot_names",),
    rules=...
)
```

The recipe records how to run the Astichi builder from data. It does not know
YIDL lifecycle semantics; it only knows named resources, named targets,
required bit collections, entry rules, orders, binds, and identifier maps.

Where Astichi provides canonical class/function/component recipes, the mapper
should use those recipe names and standardized hole names instead of duplicating
interface metadata in YIDL.

### 5.7 Rule

A declaration that says:

1. which spec records to select
2. which resource to emit
3. which surface to target
4. how to order contributions
5. how to bind spec properties or constants into the resource
6. how to pass identifier bindings such as `arg_names`

Rules are the replacement for bespoke feature-specific emitter loops.

## 6. Mapper Pipeline

The mapper should run a deterministic pipeline:

1. Receive a `GenerationPlan` made of resources, constructs, surfaces, spec
   records, and rules.
2. Validate that every rule references existing resources and surfaces.
3. Evaluate selectors over resolved spec records.
4. Expand component recipes and, for each selected record, create a
   contribution intent:
   - source resource
   - target surface
   - order
   - external binds
   - identifier binds
   - keep names if required
5. Build the Astichi graph generically from those contribution intents.
6. Materialize through Astichi.
7. Return generated source, AST, or both depending on caller needs.

No step should need special knowledge of a lifecycle helper.

## 7. Astichi Builder API Requirement

The mapper should use Astichi's data-driven builder API, not the fluent
attribute API.

The fluent API remains useful documentation for humans:

```python
builder.Root.body.add.Step(order=0)
```

The mapper should call the named equivalent:

```python
builder.instance("Root").target("body").add("Step", order=0)
```

or, when it already holds a normalized target reference:

```python
builder.target(
    root_instance=target.root_instance,
    ref_path=target.ref_path,
    target_name=target.name,
    leaf_path=target.leaf_path,
).add(
    source.name,
    indexes=source.indexes,
    order=contribution.order,
    bind=contribution.bind,
    arg_names=contribution.arg_names,
    keep_names=contribution.keep_names,
)
```

This keeps YIDL generation data-driven and prevents the mapper from turning
spec data into Python attribute names.

## 8. Parser-Free Runtime Rule

The mapper must support the YIDL coding rule that generated decorator and
generated field-spec/helper runtime paths do not invoke the Python parser.

Therefore:

1. Resources are compiled or constructed at module/build time, not per field
   inside generated runtime paths.
2. Per-spec variation flows through binds, identifier binds, rule ordering, or
   structural AST specialization.
3. A repeated literal such as a slot name should be emitted by a reusable
   resource plus a property bind, not by parsing `"'field_name'"` for every
   field.

## 9. Slots Example

The slots construct should not be hard-coded in the init-only emitter.

Conceptual inputs:

```text
construct Main.classvar("__slots__").surface("items")

rule over field_spec where participates_in_slots:
    emit SlotItemResource
    target Main.__slots__.items
    order field_order
    bind slot_name = field_spec.FieldName
```

The class variable resource owns the class-body shape:

```python
__slots__ = (astichi_hole(items),)
```

The item resource owns one tuple item:

```python
astichi_bind_external(slot_name)
```

The mapper expands the rule over selected spec records and wires each item into
the `items` surface. The slots feature contributes resources and rules; the
mapper performs the build.

## 10. Init-Only Migration Target

The current init-only emitter has hand-coded loops such as:

- hoist annotation locals
- hoist default locals
- emit parameter payloads
- emit assignment body payloads
- insert pass body for empty init

Those loops are acceptable as discovery scaffolding only. The migration target
is to express each as resources plus rules:

- rule over init fields -> annotation local resource
- rule over defaulted fields -> default local resource
- rule over init fields -> param resource
- rule over init fields -> assignment resource from parameter
- rule over non-init fields -> assignment resource from default local
- fallback rule when method body has no contributions -> pass resource

The engine should provide the generic "selected record to contribution" path;
the init-only capsule should only declare the resources, properties, filters,
and rule wiring.

## 11. Suggested Package Shape

Initial package:

```text
src/yidl/generation/
  __init__.py
  model.py
  rules.py
  mapper.py
  astichi_adapter.py
```

Responsibilities:

- `model.py`: resource, construct, surface, spec record, property reference,
  contribution intent, generation plan.
- `rules.py`: selector/filter and rule declarations.
- `mapper.py`: deterministic rule evaluation and plan validation.
- `astichi_adapter.py`: narrow adapter that turns contribution intents into
  Astichi builder operations.

The adapter is the only layer that should import Astichi directly.

## 12. First Implementation Slice

The first slice should be deliberately small:

1. Define mapper-owned records for resources, surfaces, spec records, and
   rules.
2. Support simple "for each selected spec record, emit this resource to this
   surface" rules.
3. Support `bind`, `arg_names`, `keep_names`, and deterministic `order`.
4. Rebuild the existing init-only generated source through the mapper without
   changing output.
5. Add `__slots__` as the first new class variable construct using the same
   mapper path.

Success coverage should use YIDL goldens for generated source and runtime tests
for the generated class behavior. Bespoke tests should focus on mapper
validation and failure diagnostics.
