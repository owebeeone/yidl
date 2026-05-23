# YIDL DDS Gaps Vs Lifecycle Kinds

## Purpose

This document compares the current YIDL data-definition, matcher, production, and
recorded concept machinery against the behavior currently implemented by the
reference lifecycle backend in `pyrolyze/src/pyrolyze/lifecycle.py`.

The reference lifecycle module is read-only context. YIDL should not depend on
that implementation. The goal here is to identify which lifecycle concepts are
already expressible with the current DDS stack and which ones need an extension
before the lifecycle helper surface can be rebuilt as a generated YIDL system.

The canonical YIDL architecture remains `dev-docs/YidlDesignSummary.md`. This
document is a focused gap analysis for the lifecycle kind functions.

## Current DDS Coverage

The current YIDL generation substrate already has several pieces needed for the
lifecycle rewrite:

- Schema declarations: properties, records, unions, collections, computed
  collections, and collection cardinality.
- Containers: a builder that accumulates records, applies write policies, and
  freezes into runtime container views.
- Ports: semantic port objects with owner addresses and ordering.
- Matchers: Eq-only rule matching over fixed value tuples, evaluated fields,
  descending specificity, value-tuple caching, and generated runtime source.
- Generated values: matcher resources can carry Astichi compile inputs or
  Astichi template values so matched resources can lower into source.
- Productions: collection, computed collection, and matcher-result sources can
  write records into target collections using merge policies.
- Recorded concepts: capsule-like concepts can replay schema, matcher,
  production, and resource declarations into a DDS.
- Early class-generation concepts: class shell, slots, init, property, and
  frozen-property concepts have enough shape to prove that fields can drive
  generated class components.

This is enough to model simple class bodies, slots, initializer parameters,
property methods, and rule-selected template resources. It is not yet enough to
model the full lifecycle backend without either adding DDS features or pushing a
large amount of behavior into bespoke Python code. The second option should be
avoided unless the behavior is genuinely outside the reusable generation model.

## Lifecycle Reference Surface

The lifecycle reference exposes these user-facing helper families:

- `managed`
- `const`
- `static`
- `binding`
- `owned`
- `transient`
- `local_store`
- `derived`
- `initvar`
- `classvar`
- `commit_order_key`
- `commit_validator`
- `on_before_commit`
- `on_after_commit`
- `on_after_rollback`
- `lifecycle_field`
- `managed_context`

Internally, these helpers are not just field flags. The reference decomposes
them across kind mixins and storage/operation dimensions:

- Stored fields, non-stored declarations, constructor-only declarations, and
  class-materialized declarations.
- Current-record storage, local-store storage, derived-store storage, and
  declaration storage.
- Overlay, immutable, retained-resource, transient, local-like, derived, and
  hook operational behavior.
- Transaction groups, transaction indices, current and working records, and
  commit/rollback/close hooks.
- Callable injection for hooks, validators, order keys, defaults, factories,
  freeze/thaw, state copy, and state factory functions.

Any DDS-based lifecycle generator needs to represent those facts as data and
rule-selected resources. It should not reproduce the existing lifecycle module
as one large handwritten code generator.

## Helper Matrix

| Helper | Main lifecycle facts | Current DDS coverage | Main gaps |
| --- | --- | --- | --- |
| `managed` | Stored current/working value, transaction key, compare mode, default/factory, initial working, freeze/thaw, state factory/copy | Field-like records, matchers, property/init snippets | Transaction indexing, state refs, operation pipeline, callable injection, init phase ordering |
| `const` | Stored once at construction or default, immutable after init, value comparison | Frozen property templates and init fields | Immutable write diagnostics, default/factory phase, class/facade state routing |
| `static` | Stored once lazily or explicitly, immutable after first assignment | Property templates can be selected | Single-write runtime state, lazy default factory, setter template variants |
| `binding` | Retained external resource, accept/retain/release behavior, scalar/map shape | Matchers can select resource policy templates | Annotation shape facts, cleanup phases, refcount operation resources |
| `owned` | Owned resource lifecycle, close/release on replacement/commit/rollback | Same as binding at selection level | Distinct resource policy, rollback/close aggregation, evict-last semantics |
| `transient` | Transaction-scoped scratch value, working default factory, active transaction required | Can filter fields and choose templates | Active transaction facts, tx-indexed working storage, runtime phase resources |
| `local_store` | Non-transactional auxiliary store, reset/close behavior | Can produce local-store field records | Store topology, close/reset operation phases, facade routing |
| `derived` | Derived store, reset on commit/rollback, user setter/getter behavior | Can select property templates | Dependency/invalidation model, reset phase contributions |
| `initvar` | Constructor-only value, may be retained if a late consumer needs it | Init parameter records and parameter templates | Dependency closure, retained initvar storage, unused initvar diagnostics |
| `classvar` | Class body materialization, optional default/default_factory(cls) | Class body ports and snippets | Class-materialized value resources, helper signature policy |
| `commit_order_key` | One per transaction key, callable injection, sort key | Matcher resources and records can represent callables | At-most-one keyed validation, tx-group index, generated runner injection |
| `commit_validator` | One per transaction key, callable injection, validation phase | Same as order key | Validation phase, ExceptionGroup policy, callable injection |
| Hook helpers | Many per transaction key, callable injection, before/after/rollback phases | Records and ordered ports can represent contributions | Runtime hook runners, phase ordering, rollback error aggregation |
| `lifecycle_field` | Low-level escape hatch with explicit kind and parameters | Unions/variants can represent low-level records | Kind resource model, parameter validation, diagnostics |
| `managed_context` | Decorator, MRO merge, state/facade classes, helper functions | Class concepts can emit class shells | Generated library/decorator surface, MRO merge, multi-facade topology |

## Gap 1: Kind Semantics Are Not First-Class Data

The reference backend has kind classes such as `ManagedKind`, `ConstKind`,
`BindingKind`, `OwnedKind`, `TransientKind`, and hook declaration kinds. Those
kinds own helper parameters, storage behavior, operation behavior, validation,
and override rules.

Current DDS records can store properties such as `Kind`, `Init`, `Frozen`, or
`Default`, but there is no first-class object that says "this kind contributes
these helper parameters, these operation resources, this storage topology, and
these validations".

### Proposal A: KindConcept Records

Add a recorded concept layer for kind definitions:

- `KindSpec` records describe helper name, declaration space, storage policy,
  operation policy, default compare mode, default transaction behavior, and
  validation resources.
- Helper concepts produce `KindSpec` records and field-spec variant records.
- Matchers select operation templates from `KindSpec` plus field facts.

This makes kind inheritance in the old lifecycle module become concept merging
in YIDL. It also gives a place for helper parameter policy and operation policy
without adding custom code for every helper.

### Proposal B: Kind Semantics As Concept Extensions Only

Keep DDS core neutral. Each helper concept contributes ordinary properties,
matchers, productions, and template resources. The fact that those together form
a "kind" exists only in the recorded concept plan.

This avoids a new `KindSpec` API, but it risks scattering kind semantics across
many matchers and productions. It is acceptable only if the recorded concept
builder gives a clean way to inspect what a helper contributes.

## Gap 2: Helper Parameter Policy

The lifecycle helper functions have explicit parameter policies:

- Parameters exposed to users.
- Parameters fixed by a helper, such as `init=False` for hook declarations.
- Parameters scrubbed or rejected for certain helpers.
- Parameters that map to generated `FieldSpec` properties.

Current DDS property defaults are not enough to generate helper signatures,
validate illegal helper arguments, or scrub parameters from a lower-level
surface.

### Proposal A: Helper Signature Resources

Add helper-signature records:

- `HelperSpec`
- `HelperParam`
- `ExposedParam`
- `FixedParam`
- `ScrubbedParam`
- `ParamToProperty`

The generated helper function is then produced by a standard helper-function
concept. Parameter holes can emit the function signature, and body productions
can convert supplied values into DDS field records.

### Proposal B: Helper Surface Concepts

Keep helper signatures outside the DDS schema but inside recorded concepts.
Each helper concept owns an Astichi template for the helper function and binds
it to field-record construction resources.

This is simpler for the first helper rewrite, but the helper parameter policy
must remain declarative. If the body becomes bespoke Python per helper, this
option should be rejected.

## Gap 3: FieldSpec Variants Across Declaration Spaces

The lifecycle module does not have one uniform field shape. There are stored
fields, constructor-only initvars, classvars, metadata declarations, hooks, and
special validator/order-key declarations.

Current DDS supports unions and variants, but the ergonomics for a shared field
family are still low-level. Lifecycle needs common identity and common
properties across variants, plus variant-specific properties and validation.

### Proposal A: Union-Based FieldSpecs

Use a single union for field specs:

- `FieldSpecs = dds.union("FieldSpecs")`
- Variants: `ManagedField`, `ConstField`, `BindingField`, `InitVarField`,
  `ClassVarField`, `HookField`, and so on.
- Common properties: `Name`, `Annotation`, `DeclarationOrder`,
  `DeclarationSpace`, `SourceLabel`.
- Variant properties: transaction key, factory callables, resource policy,
  hook phase, class materialization, and storage mode.

Computed collections then select `InitFields`, `StoredFields`, `HookFields`,
`ClassMaterializedFields`, and similar views.

### Proposal B: Normalize From Helper-Specific Collections

Let each helper write to a helper-specific collection first, then add a
normalizing production that writes a common `ResolvedField` collection.

This gives helper concepts more independence and can make diagnostics clearer.
The cost is that cross-helper validation, such as duplicate field names, must
run after normalization.

## Gap 4: MRO Merge And Override Validation

`managed_context` merges specs across the class MRO and validates overrides.
Kinds can define whether one declaration may override another. Annotation
narrowing also matters.

Current DDS containers model one set of records. They do not model layered
inputs from base classes, class declaration order, or kind-specific override
resolution.

### Proposal A: Layered Collection Merge

Add a merge production over ordered container layers:

- Source layers: base classes from oldest to newest, then the current class.
- Merge key: field name and declaration space.
- Merge policy: replace, reject, or validate with an override resource.
- Output: `MergedFieldSpecs`.

This belongs in the YIDL generation layer, not in pyrolyze. It can also support
future facade and store merging.

### Proposal B: Pre-Merge Outside DDS, Validate Inside DDS

Harvest and merge inherited records in ordinary Python before creating the DDS
container. DDS then validates the already-merged output.

This is quicker but less aligned with the goal that generated decorators own the
complete semantic pipeline. It should only be used as a temporary bridge if the
layered merge API is too much for the first lifecycle slice.

## Gap 5: Transaction Group Indexing

The reference backend maps transaction key names to dense indices. Hot runtime
code can then use integer transaction slots instead of repeatedly looking up
hashable group names.

Current DDS can filter and produce records, but it does not have a stable
"distinct values to ordered indices" facility.

### Proposal A: Distinct Indexed Collection

Add a computed collection or production:

```python
TxKeys = dds.distinct_indexed_collection(
    "TxKeys",
    source=ManagedFields,
    value=TxKey,
    order=DeclarationOrder,
)
```

It emits records containing `TxKeyName`, `TxIndex`, and stable ordering. Later
productions join fields to the matching `TxIndex`.

### Proposal B: Tx Index As A Generated Resource

Keep indexed groups outside normal records and provide an index resource:

```python
tx_index = resources.distinct_index(TxKey, source=ManagedFields)
```

Templates bind `tx_index(field.tx_key)` into generated code. This may be
lighter if transaction indexing is the only distinct-index use case.

## Gap 6: State, Store, And Facade Topology

The lifecycle design requires a state class and multiple possible facades. State
owns field storage. Facades expose behavior and should not own the stored field
state. Main, current, and working facades may share some simple field templates
but managed fields usually need facade-specific logic.

Current class concepts can generate one class with slots, init, and properties.
They do not yet model a graph of related generated classes and state stores.

### Proposal A: State And Facade Concepts

Introduce recorded concepts:

- `StateConcept`: state class, slots, transaction arrays, local/derived stores,
  and cleanup queues.
- `FacadeConcept`: facade class name, parent, body, properties, methods, and
  receiver-to-state binding.
- `StoreConcept`: current store, working store, local store, derived store, and
  class-materialized store.

Ports stay generic: class body, slots items, init params, init body, property
methods, and lifecycle operation methods.

### Proposal B: Role-Based ClassConcept

Extend the existing class concept with a `ClassRole` property: state, main
facade, current facade, working facade, helper module, or support class.

This reuses the current class-generation surface, but every template must bind
through semantic resources such as `StorageRoot`, `Receiver`, and `StateRef`.

## Gap 7: Semantic StateRef And Physical Naming

The design summary calls for semantic references such as published value,
current value, working value, retained value, local store value, derived cache,
and transaction state. Current examples often bind string paths such as
`storage_path` or `working_path`.

String paths are easy to emit but are too weak for lifecycle. They make it hard
to retarget the same template to state classes, direct classes, or facades.

### Proposal A: StateRef Resources

Add source-emittable `StateRef` resources:

- `PublishedValue(field)`
- `CurrentValue(field, tx_index)`
- `WorkingValue(field, tx_index)`
- `RetainedValue(field)`
- `LocalStoreValue(field)`
- `DerivedValue(field)`

Astichi templates receive these refs and lower them through a `StateNaming`
resource. This keeps physical naming in one place.

### Proposal B: Naming Productions First

Before full `StateRef` objects, add productions that write explicit naming
records:

- `PublishedSlot`
- `CurrentSlot`
- `WorkingSlot`
- `LocalStoreSlot`
- `DerivedSlot`

Templates bind those generated names. This is less semantic, but it may be a
shorter path to validating the state/facade layout.

## Gap 8: Operation Matrix

Each lifecycle kind contributes behavior for reads, writes, constructor init,
commit, rollback, close, validation, hook execution, default resolution, and
working promotion.

Current DDS productions mostly create data records. They do not yet provide a
standard operation matrix that says "for this field and this phase, select this
template and bind these resources".

### Proposal A: Operation Contribution Records

Introduce operation contribution collections:

- `GetContributions`
- `SetContributions`
- `InitContributions`
- `CommitContributions`
- `RollbackContributions`
- `CloseContributions`
- `ValidateContributions`
- `HookContributions`

Matchers select resources into those collections. Later class/method concepts
consume the ordered contributions and insert Astichi templates into method body
ports.

### Proposal B: One Concept Per Runtime Operation

Create concepts such as `GetterConcept`, `SetterConcept`, `CommitConcept`, and
`RollbackConcept`. Each concept owns its matchers and templates.

This keeps operations modular and may fit the recorded concept builder well. It
still needs shared records for ordering and diagnostics.

## Gap 9: Runtime Pipeline Phases

Transaction commit is not a flat list of statements. The reference path has
validation, sorting by commit order key, before hooks, field commits, after
hooks, rollback behavior, and cleanup.

Current production groups order decoration-time record generation. They are not
the same as generated runtime operation phases.

### Proposal A: Runtime Phase Model

Add phase records:

- `RuntimePhase`
- `PhaseContribution`
- `PhaseOrder`
- `PhaseFailurePolicy`

Generated methods iterate or unroll phases in deterministic order. This makes
commit, rollback, close, and initialization share a common pipeline mechanism.

### Proposal B: Phase-Specific Method Templates

Keep the phase model implicit in method concepts. For example,
`CommitMethodConcept` has body ports for validation, before hooks, field commit,
after hooks, and cleanup.

This is simpler for first codegen, but it is less reusable if managed, owned,
binding, and future lifecycle features all need to add phases independently.

## Gap 10: Callable Injection

Lifecycle callables may accept names such as `self`, `current`, `working`,
`previous`, `tx_key`, and initvars. The reference implementation inspects
signatures and builds callable runners.

Current DDS matchers can use evaluated fields, but there is no standardized
callable-analysis record set or generated wrapper model.

### Proposal A: Callable Analysis Records

Add a callable analyzer that emits records:

- `CallableSpec`
- `CallableParam`
- `CallableInjection`
- `CallableRunner`
- `CallableError`

These records can be matched to select wrapper resources. The analyzer runs at
decoration time and is source-emittable as part of the generated decorator.

### Proposal B: Callable Wrapper Concept

Keep signature analysis as a specialized YIDL subsystem and expose only wrapper
resources to DDS:

- The subsystem receives callables and available injection facts.
- It returns Astichi templates or generated values for the runner.
- DDS records store the selected runner resource.

This avoids overloading DDS with Python `inspect` details while still keeping
callable injection out of kind-specific handwritten code.

## Gap 11: Initvar Dependency Closure

Initvars are constructor-only unless a late consumer needs the value. Defaults,
factories, hooks, validators, and state-copy functions may request initvars.
Unused or unresolved initvars should be diagnosed.

Current computed collections can filter records. They do not compute graph
reachability or transitive dependency closure.

### Proposal A: Graph Closure Collections

Add a graph computation facility:

- Nodes: initvars and callable resources.
- Edges: callable consumes initvar, field consumes callable, operation consumes
  field.
- Output: retained initvars, constructor-only initvars, unused initvars, and
  invalid dependency cycles.

This is reusable for derived-field invalidation and future owned-resource
dependency graphs.

### Proposal B: Specialized InitvarDependencyConcept

Build initvar dependency analysis as a YIDL concept first. It writes derived
collections such as `RetainedInitVars` and `UnusedInitVars`.

If another feature needs graph closure, the specialized analyzer can be
generalized later.

## Gap 12: Default And Factory Ordering

The reference initializer resolves explicit constructor values, defaults,
default factories, initial working values, state factories, and local/derived
store initialization in a precise order. Some paths need cycle detection.

Current DDS can produce init parameter and init body snippets. It does not yet
define a reusable generated init-phase engine.

### Proposal A: Init Phase Contributions

Model initialization as runtime phase contributions:

- Pull constructor values.
- Resolve default values.
- Run default factories.
- Initialize state slots.
- Initialize working values.
- Initialize local and derived stores.
- Materialize class-level declarations.

Each field kind contributes to the phases it needs.

### Proposal B: Ordered Init Body Production

Generate straight-line `__init__` code from ordered field records. Add a shared
cycle-stack template where needed.

This is likely sufficient for the first YIDL lifecycle target, as long as the
ordering records are explicit and tested with goldens.

## Gap 13: Transient And Managed Working Semantics

Managed fields have current and working values. Transient fields are
transaction-scoped scratch values. Initial working values and working default
factories have restrictions tied to transaction state and first-commit state.

Current matchers can choose templates from properties, but the facts needed by
these rules are not standardized.

### Proposal A: Standard Working-State Facts

Add field facts:

- `HasCurrentValue`
- `HasWorkingValue`
- `HasInitialWorking`
- `HasWorkingDefaultFactory`
- `RequiresActiveTransaction`
- `RequiresFirstCommit`
- `PromotesToWorking`
- `UsesThaw`
- `UsesFreeze`

Operation matchers consume these facts instead of hardcoding helper names.

### Proposal B: WorkingStoreConcept

Create a `WorkingStoreConcept` that owns transaction-scoped storage templates.
Managed and transient helper concepts extend it with their specific rules.

This matches the desire for concept inheritance by behavior rather than by a
single helper class hierarchy.

## Gap 14: Binding And Owned Resource Policies

`binding` and `owned` fields need retained resource semantics. They may be
scalar or mapping-like, and mapping fields must handle duplicate values and
per-key retain/release behavior.

Current DDS can store a kind and select a template. It does not derive container
shape facts from annotations or standardize retain/release policy resources.

### Proposal A: Annotation Shape Facts

Add an annotation-shape analyzer that emits facts:

- `IsMapping`
- `IsSequence`
- `KeyType`
- `ValueType`
- `ElementType`
- `AcceptsNone`

Binding and owned matchers then choose scalar or mapping templates from the same
resource-policy facts.

### Proposal B: Explicit Resource Shape Parameters First

Let helper parameters declare the shape explicitly for the initial generator:

- `resource_shape="scalar"`
- `resource_shape="mapping"`

Annotation-derived shape can be added later. This reduces early analysis work,
but it weakens the user-facing type-driven model.

## Gap 15: Cleanup, Evict-Last, And Rollback Aggregation

Retained-resource fields need cleanup on replacement, commit, rollback, and
close. The design summary also points toward better rollback error aggregation
than the old reference path in some areas.

Current DDS has no runtime cleanup queue or failure aggregation model.

### Proposal A: Cleanup Phase Contributions

Represent cleanup as runtime operation phases:

- `StageRetain`
- `StageRelease`
- `CommitPromote`
- `EvictLast`
- `RollbackRelease`
- `CloseRelease`

Owned and binding concepts contribute to those phases. The rollback method owns
the error aggregation policy.

### Proposal B: State-Level Cleanup Queue

Add a cleanup queue to the generated state class and emit helper methods for
enqueue, apply, and rollback.

This isolates complex cleanup mechanics from field templates, but it is more
runtime infrastructure than the current DDS has.

## Gap 16: ClassVar Materialization

`classvar` declarations materialize values on the managed class, not on
instances. Defaults and default factories may need class context.

Current class body ports can emit class assignments, but there is no dedicated
class-materialized declaration space.

### Proposal A: ClassMaterializedSpec Collection

Add a `ClassMaterializedSpecs` collection with records containing name,
annotation, default/factory, declaration order, and materialization template.

Productions write class body components from those records.

### Proposal B: ClassVar As A FieldSpec Variant

Represent classvars as a `FieldSpecs` union variant with
`DeclarationSpace="class"`. Matchers then route it to class body ports rather
than instance slots or init.

This is preferable if classvars share override and MRO behavior with fields.

## Gap 17: Special Per-Transaction Declarations

Commit order keys and commit validators are at-most-one per transaction key.
Hooks are many per transaction key and phase.

Current write policies can reject duplicate identities, but the model for
special declaration uniqueness is not explicit.

### Proposal A: Keyed Special Collections

Add special collections keyed by `(SpecialKind, TxKey)`:

- `CommitOrderKeys`
- `CommitValidators`
- `HookDeclarations`

`CommitOrderKeys` and `CommitValidators` use strict duplicate rejection.
`HookDeclarations` allows many records ordered by declaration order.

### Proposal B: Validation Productions

Keep raw hook/validator records in one declaration collection and add validation
productions that scan for conflicts and produce diagnostics.

This is useful if diagnostics need to mention every conflicting declaration,
but it is more work than strict keyed writes.

## Gap 18: Diagnostics And Provenance

The lifecycle reference raises detailed `TypeError` and runtime errors for
invalid helper usage, duplicate declarations, invalid signatures, unknown
transaction keys, unused initvars, and illegal state transitions.

Current DDS errors are useful for core mechanics but are not a complete
diagnostic system for a generated lifecycle library.

### Proposal A: Diagnostic Records

Add diagnostic records with fields such as category, severity, source label,
helper name, field name, concept name, and message. Validation productions write
diagnostics; a final gate rejects errors.

### Proposal B: Source Metadata On Every Semantic Record

Require field/helper records to carry enough source metadata for direct error
messages. Raise exceptions immediately during validation and production writes.

This is simpler and probably enough for V1, but diagnostics must be consistent
and specific.

## Gap 19: Runtime Source Emission Of Semantic Resources

Lifecycle generation needs source-emittable resources for helpers, templates,
callables, imported support classes, sentinels, transaction constants, and
runtime utility functions.

Astichi now has `astichi_pyimport(...)` for consolidated imports, and matcher
resources can carry Astichi compile inputs. The remaining issue is choosing a
general resource model rather than passing raw Python objects through generated
source.

### Proposal A: GeneratedResource Protocol

Generalize current matcher generated values into source-emittable resources:

- Literal resources.
- Astichi code resources.
- Astichi template resources.
- Import-backed symbol resources.
- Runtime helper resources.

All matcher and production resources use the same protocol.

### Proposal B: Keep Current Generated Values And Add Source Maps

Keep `from_astichi_code(...)` and Astichi template values as the only generated
resource mechanism for now. Require all other objects to be passed by explicit
source-name maps.

This is less elegant but smaller. It should not block adding semantic imports at
the point of use with `astichi_pyimport(...)`.

## Gap 20: Builder-Phase Matcher Views

Some lifecycle productions may need to select resources while other records are
still being produced. Current matcher-result productions work best over frozen
or snapshot views.

### Proposal A: Strict Group Snapshots

Keep production groups strict:

- A group sees records produced by earlier groups.
- A production sees a stable snapshot at the start of that production.
- Later productions in the same group may see earlier writes only if explicitly
  allowed.

This reduces complexity and should be tried first.

### Proposal B: Builder-Phase Matcher Source

Add matcher sources that read directly from the in-progress builder. This is
more flexible but risks creating a second matcher runtime model. It should be
introduced only if strict snapshots cannot express the lifecycle generator.

## Gap 21: Multi-Facade Template Binding

Property and method templates must work against different receivers. A direct
class may use `self` as the state owner. A facade should usually route through
its backing state object.

Current snippets can use bound names, but the concept model needs a standard
way to describe receiver, state root, current facade, working facade, and main
facade.

### Proposal A: Receiver Resources

Add semantic resources:

- `Receiver`
- `StateRoot`
- `CurrentFacade`
- `WorkingFacade`
- `MainFacade`

Templates bind through these resources rather than spelling `self` paths
directly.

### Proposal B: Facade-Specific Matchers

Make facade role a matcher input. The property/method matcher can select a
different template for direct class, main facade, current facade, or working
facade.

This is necessary for managed fields if one template cannot express both direct
and facade access cleanly.

## Gap 22: Generated Helper Library And Decorator

The final system needs to emit a usable helper/decorator library: helper
functions, field spec records, managed-context decorator, support classes, and
generated lifecycle class builders.

Current concepts mostly prove class-component generation, not whole-module
generation.

### Proposal A: GeneratedLibraryConcept

Add a module-level concept with ports:

- Imports.
- Sentinels and support values.
- Support classes.
- Helper functions.
- Decorators.
- Generated runtime container and matcher classes.

This makes "the generated decorator" a product of the same DDS production
system.

### Proposal B: Start With Decorator-Only Emission

Emit only the `managed_context` equivalent first, while helpers remain ordinary
Python wrappers that create DDS records.

This may be a practical stepping stone, but it should not become the permanent
architecture if helper signatures are meant to be generated.

## Gap 23: Runtime Performance Shape

The reference lifecycle backend stores tables of callables and descriptors.
The YIDL target should move toward direct slot access and unrolled methods where
that improves clarity and runtime cost.

Current DDS can generate records and snippets, but the optimization policy is
not represented.

### Proposal A: Optimization Facts

Add facts such as:

- `UseDirectSlot`
- `UseTableLookup`
- `UnrollOperation`
- `UseSharedHelper`

Matchers select the implementation style based on field count, kind, and
facade role.

### Proposal B: Direct-First Generated Code

Generate direct source for the first lifecycle target. Add table-based fallback
only where a feature requires it.

This is consistent with YIDL's goal of readable generated source, but tests
must keep behavior parity with the reference backend.

## Gap 24: Test Coverage For Lifecycle Parity

The existing pyrolyze tests exercise many lifecycle behaviors. YIDL needs its
own generated-code goldens and runtime parity tests. The goal is not to copy the
reference implementation, but the observable lifecycle contract must remain
stable.

### Proposal A: YIDL Lifecycle Golden Staircase

Create YIDL-owned goldens in increasing complexity:

1. Plain managed field with init and property.
2. Frozen/const/static variants.
3. Multiple transaction keys.
4. Transient and local-store fields.
5. Binding/owned scalar resources.
6. Binding/owned mapping resources.
7. Initvar dependency and retention.
8. Hooks, validators, and order keys.
9. Multi-facade state routing.

Success paths should use goldens. Bespoke tests should focus on diagnostics and
small mechanics.

### Proposal B: Reference Parity Harness

For selected cases, run the reference backend and generated YIDL backend against
the same scenario and compare observable state transitions.

This is useful for confidence, but the generated YIDL code should have its own
source goldens so the implementation shape remains reviewable.

## Cross-Cutting Extension Priorities

The gaps above overlap. A practical build order should avoid adding one-off
features for every helper. The highest-leverage DDS extensions appear to be:

1. Field-spec union/variant ergonomics and normalized field records.
2. Transaction group distinct indexing.
3. State/facade/store concepts with semantic receiver and state refs.
4. Operation contribution records and runtime phase ports.
5. Callable analysis records or a callable-wrapper subsystem.
6. Initvar dependency closure.
7. Cleanup/resource policy resources for binding and owned fields.
8. Generated helper/decorator library concept.

The first lifecycle slice should probably stop before full binding/owned
resource semantics. The point of the first slice is to prove that fields,
transaction indexing, state storage, init, and property methods can be produced
without bespoke per-helper code.

## Non-Goals For The First Lifecycle Slice

These are important but should not block the first generated lifecycle
staircase:

- Full MRO override validation for every kind.
- Binding and owned mapping semantics.
- Complete callable injection for all hook/default/factory surfaces.
- Rollback `ExceptionGroup` policy for every cleanup path.
- Full helper library generation.
- Automatic annotation-shape analysis.
- Optimized table-vs-unrolled selection.

Each of these needs an explicit slice when it becomes the next blocker.

## Recommended Next Analysis Step

The next concrete design step is to define the smallest generated lifecycle
staircase:

1. One state class.
2. One direct managed facade.
3. Managed and const fields.
4. Constructor parameters and defaults.
5. One transaction key index.
6. Current/working slot refs.
7. Getter, setter, commit, and rollback method bodies.

That staircase should identify which of the proposed extensions are truly
required immediately and which can remain deferred.
