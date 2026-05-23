# YIDL DDS Lifecycle Gap Closure Plan

## Objective

Close the lifecycle gaps identified in `dev-docs/YidlDdsGapsVLifecycle.md` with
the smallest useful set of DDS extensions.

The objective is not to add one feature per lifecycle helper. The objective is
to build enough generic DDS capability that lifecycle helpers, facades, stores,
transaction keys, callable injection, and operation methods can be described
as data, matchers, productions, ports, and generated resources.

This plan treats `pyrolyze/src/pyrolyze/lifecycle.py` as behavioral reference
only. The generated YIDL system must not depend on it.

Detailed feature plans live under `dev-docs/lifecyle-plan/`. That directory
uses the requested spelling and expands each feature with fluent API examples,
expected use cases, generated-source golden shape, diagnostics, and tests.

Astichi template-surface assumptions are backed by active Astichi goldens.
`astichi/tests/data/gold_src/class_head.py` proves class-head expression holes,
including multiple bases. `astichi/tests/data/gold_src/lifecycle_template_surfaces.py`
proves the lifecycle-shaped combination of class heads, slots, parameter holes,
call-argument holes, `astichi_ref(...)._`, dynamic property names,
`astichi_pyimport(...)`, and `astichi_comment(...)` rendered through
`emit_commented()`.

The detailed-plan review consolidated several originally proposed public DDS
features. `layered_merge(...)`, `distinct_indexed_collection(...)`,
`reachable_collection(...)`, `fact_producer(...)`, and a diagnostics engine are
not initial DDS-core APIs. They are patterns built from aggregate generated
operations, composite identities, keyed lookups, ordered sources, generated
resources, and lifecycle concept records.

The final crisp feature enumeration is
`dev-docs/lifecyle-plan/11-ActualFeatureEnumerationDetailedPlan.md`. The YIDL
file grammar proposal is
`dev-docs/lifecyle-plan/12-YidlGrammarProposalDetailedPlan.md`.

## Consolidation Rule

The 24 lifecycle gaps reduce to a small number of reusable capabilities:

1. Composite identities and keyed lookup.
2. Ordered source sequences.
3. Aggregate generated operations.
4. Source-emittable semantic resources.
5. Fluent schema-family and concept ergonomics.
6. Validation and diagnostics as ordinary concept records and gates.
7. External fact producers as aggregate generated operations.
8. Lifecycle concepts built from existing ports, matchers, productions, and
   generated resources.

Only the first four are DDS/generation-layer extensions. The fifth is fluent
layer work. The sixth through eighth are lifecycle concept patterns.

## Existing Features To Reuse

Do not duplicate these concepts:

- `PropertySpec`, `RecordSpec`, `UnionSpec`, `CollectionSpec`, and
  `ComputedCollectionSpec` remain the data model.
- `DDSContainerBuilder.write(...)`, merge policies, and production groups
  remain the mutation and generated-operation model.
- `PortSpec`, `PortAddress`, `children_at(...)`, and ordered children remain
  the destination graph model.
- `MatcherSpec`, evaluated fields, matcher result sources, and generated matcher
  runtime source remain the rule-selection model.
- `MatcherGeneratedValue` / Astichi template values remain the implementation
  basis for source-emittable resources. The public API should be factory
  functions, not a family of public resource classes.
- Recorded capsule concepts remain the definition composition model.

Lifecycle should be built by extending and composing these surfaces. New APIs
must be justified as generic data-production capabilities, not lifecycle helper
shortcuts.

## Consolidated New DDS Feature Set

The actual DDS additions after review are:

1. Composite collection identities.
2. Keyed lookup value expressions.
3. Ordered source sequences for productions and generated operations.
4. Aggregate generated operations with declared input/output collections.
5. Generated resource unification and source emission through matcher,
   production, and record values.

Everything else in this section is a planned use of those features, or fluent
layer sugar that lowers to those features.

### Feature 1: Schema Families

#### Problem

Lifecycle declarations are not one uniform record shape. Stored fields,
constructor-only initvars, classvars, hooks, validators, order keys, and
resource fields all share some facts but also carry variant-specific facts.

Current DDS has `UnionSpec`, but the lifecycle generator needs a convenient and
consistent way to define common properties, variant properties, and common
computed views over those variants.

#### API Direction

Use fluent/concept-layer ergonomics over current union/schema declarations
rather than adding a parallel `FieldSpec` system:

```python
FieldSpecs = concept.schema_family("FieldSpecs")

FieldSpecs.common(Name, Annotation, DeclarationOrder, SourceLabel)

ManagedField = FieldSpecs.variant(
    "ManagedField",
    Kind,
    TxKey,
    Default,
    DefaultFactory,
    InitialWorking,
    Freeze,
    Thaw,
)

InitVarField = FieldSpecs.variant(
    "InitVarField",
    Init,
    Default,
    DefaultFactory,
)
```

This lowers to ordinary `dds.union(...)` and `UnionSpec.variant(...)` calls.
`UnionSpec.common(...)` is not a required DDS-core addition. Add it only if the
concept-builder helper becomes awkward or duplicated in multiple concept
builders.

#### What This Covers

- Gap 1: kind semantics can be expressed as field-family facts and concept
  contributions instead of new DDS kind classes.
- Gap 3: field-spec variants across declaration spaces.
- Gap 16: classvars as a field-family variant.
- Gap 17: hook/validator/order-key declarations as declaration variants.

#### What It Does Not Cover

Schema families do not perform MRO merge, transaction indexing, callable
inspection, or operation generation. They only make declaration facts coherent.

#### Tests

Use bespoke tests for union/common-property validation and duplicate property
definition failures.

Use goldens for success cases:

- A generated runtime module with a field family containing managed, initvar,
  classvar, and hook variants.
- Computed views over that family, such as `StoredFields`, `InitFields`,
  `ClassMaterializedFields`, and `HookFields`.

### Feature 2: Layered Collection Merge

#### Problem

Lifecycle class decoration must merge inherited declarations from base classes
with declarations on the current class. It needs deterministic layer order,
identity-based replacement, and override validation.

Current DDS collections are per-container. Existing merge policies govern writes
inside a builder, but there is no source model for layered inherited inputs.

#### API Direction

Represent layered merge as an aggregate generated operation. Do not add a
public `dds.layered_merge(...)` in V1. If two separate concepts later need the
same surface and the operation pattern becomes repetitive, add a fluent concept
helper that still lowers to `dds.operation(...)`:

```python
dds.operation(
    "MergeFieldSpecs",
    inputs=(LayerFields,),
    outputs=(MergedFields,),
    order_by=(LayerIndex, SourceOrder),
    resource=MergeFieldSpecsOperation,
)
```

The lower-level implementation can be built on the current production/write
machinery:

- Each layer supplies a sequence of source records.
- The merge production writes to the target collection using an explicit merge
  policy.
- The merge policy can call a validation resource before replacing a record.
- Merge diagnostics include base record, derived record, identity, and layer.

V1 should support only linear layer order. Diamond/MRO collection is allowed as
an input concern, but layered merge receives an already-ordered sequence of
layers.

#### What This Covers

- Gap 4: MRO merge and override validation.
- Gap 18: override diagnostics and source provenance.
- Part of Gap 22: generated decorator can feed harvested base-class records
  into the same merge mechanism.

#### What It Does Not Cover

Layered merge does not inspect Python classes or collect MRO data. A decorator
or helper concept supplies the ordered layers.

#### Tests

Bespoke:

- layer order is deterministic
- same identity in later layer replaces only through policy
- incompatible override rejects with a targeted diagnostic
- identical duplicate can be idempotent only when policy allows it

Golden:

- Base class fields plus derived class fields produce one merged field view.
- Derived override changes a property and drives different generated output.

### Feature 3: Indexed And Keyed Derivations

#### Problem

Lifecycle needs stable derived keys:

- transaction key name to transaction index
- field to transaction index
- at-most-one validator per transaction key
- at-most-one order key per transaction key
- grouped hook lists
- later: grouped state slots and facade-specific target addresses

Current DDS can filter collections but cannot derive a distinct ordered index or
perform keyed lookup as a value expression.

#### API Direction

Use composite identity, keyed lookup, ordered source sequences, and aggregate
generated operations. Do not add a public distinct-index DSL in V1:

```python
dds.operation(
    "BuildTxKeys",
    inputs=(TransactionalFields,),
    outputs=(TxKeys,),
    order_by=(SourceOrder,),
    resource=BuildTxKeysOperation,
)
```

Add keyed lookup value expressions:

```python
tx_index = lookup(
    TxKeys,
    key=source.prop(TxKey),
    value=TxIndex,
)
```

Add tuple-key support using existing property values:

```python
SpecialDecls = dds.collection(
    "SpecialDecls",
    SpecialDecl,
    identity=(SpecialKind, TxKey),
)
```

If tuple identity is not currently supported, add it as an extension to
collection identity rather than a lifecycle-only uniqueness check.

#### What This Covers

- Gap 5: transaction key indexing.
- Gap 17: special per-transaction declaration uniqueness.
- Gap 13: managed/transient templates can bind integer transaction indices.
- Gap 23: direct hot paths can use generated indices rather than table lookup.

#### What It Does Not Cover

This is not a general SQL join engine. V1 supports distinct ordered values,
identity lookup, and tuple identity only.

#### Tests

Bespoke:

- distinct values receive stable dense indices
- first appearance/order rule is deterministic
- lookup rejects missing key unless a default is explicitly provided
- tuple identity duplicate rejection works

Golden:

- Fields with three transaction keys generate `TxKeys` and field records
  containing bound `tx_index`.
- Validators/order keys keyed by transaction key reject duplicates while hooks
  remain ordered many-record declarations.

### Feature 4: Graph And Closure Derivations

#### Problem

Initvars and future dependency features require transitive closure:

- callable consumes initvar
- field operation consumes callable
- operation phase consumes field
- late consumer forces initvar retention
- unused initvar becomes a diagnostic

Current computed collections handle filters, not graph reachability.

#### API Direction

Use an aggregate generated operation when initvar closure becomes the next
blocker. Do not add a public `reachable_collection(...)` in V1:

```python
InitvarEdges = dds.collection("InitvarEdges", InitvarEdge)

dds.operation(
    "BuildRetainedInitVars",
    inputs=(LateInitvarConsumers, InitvarEdges),
    outputs=(RetainedInitVars,),
    resource=BuildRetainedInitVarsOperation,
)
```

V1 graph derivation should be acyclic or bounded. Do not add a generic fixpoint
engine unless a second use case requires it.

#### What This Covers

- Gap 11: initvar dependency closure.
- Part of Gap 12: default/factory dependency ordering if needed.
- Part of Gap 14: binding/owned mapping dependencies if future features need
  graph semantics.

#### What It Does Not Cover

Graph derivation does not analyze callable signatures. It consumes callable fact
records produced elsewhere.

#### Tests

Bespoke:

- reachability includes direct and transitive targets
- cycles reject or are bounded with a clear error
- unused nodes are detectable by set difference

Golden:

- Initvars with direct and late consumers produce retained and constructor-only
  classifications in generated source.

### Feature 5: Semantic Generated Resources

#### Problem

Lifecycle generation needs source-emittable resources for:

- Astichi templates
- state references
- receiver and facade bindings
- helper functions
- callables and callable wrappers
- resource policies
- support imports
- runtime constants and sentinels

Current matcher generated values are enough for Astichi snippets, but lifecycle
needs the same resource model in production values, record fields, and operation
contributions.

#### API Direction

Do not add multiple resource models. Extend the current generated-value surface
so it can be used consistently wherever a source-emittable resource is needed.

The public V1 surface is factory functions:

```python
from_astichi_code(source, ...)
from_astichi_template(source, ...)
from_literal(value)
from_import(module, name)
```

Concrete names such as `GeneratedValue`, `AstichiCodeValue`,
`AstichiTemplateValue`, `ImportedSymbolValue`, and `LiteralGeneratedValue` are
implementation/protocol names only. If renaming `MatcherGeneratedValue` is too
disruptive, keep it internally and make the factories return a compatible
generated-resource object. The important behavior is:

- the value can be emitted into generated source
- the value can produce an Astichi composable when the consumer needs a
  composable
- imports are represented with `astichi_pyimport(...)` at point of use and are
  consolidated by Astichi
- generated values are cacheable and deterministic

Lifecycle-specific semantic objects such as `StateRef`, `Receiver`, and
`ResourcePolicy` should be ordinary generated resources or records, not DDS
core types.

#### What This Covers

- Gap 7: semantic state refs and physical naming.
- Gap 19: runtime source emission of semantic resources.
- Gap 21: multi-facade template binding.
- Gap 22: generated helper/decorator support resources.
- Gap 8 and Gap 9: operation templates as selected resources.

#### What It Does Not Cover

Generated resources do not decide which template wins. Matchers and productions
still make selection decisions.

#### Tests

Bespoke:

- generated resource cache behavior
- import consolidation through Astichi in expression and statement holes
- resource values can be stored in records and emitted by production source

Golden:

- Matchers select Astichi template resources.
- Productions store those resources in operation contribution records.
- A final class-rendering snippet consumes the resources and emits a clean
  module with consolidated imports.

### Feature 6: Validation And Diagnostics

#### Problem

Lifecycle has many invalid states:

- invalid helper parameter combinations
- duplicate field names
- duplicate validators/order keys
- invalid overrides
- illegal callable signatures
- unused initvars
- missing transaction keys
- invalid state transitions

Current DDS raises some direct exceptions, but generated lifecycle needs a
consistent validation story with useful source context.

#### API Direction

Use validation productions before adding a complex diagnostic framework.

Add a standard diagnostic record shape:

```python
Diagnostic = dds.record(
    "Diagnostic",
    Severity,
    Category,
    Message,
    SourceLabel,
    FieldName,
    ConceptName,
)
```

Add a final gate:

```python
container.raise_diagnostics()
```

or generated runner support:

```python
run_validations(builder)
raise_if_diagnostics(builder)
```

V1 should support direct exception raising from validation productions if that
is smaller, but the record shape should be defined early so validations can be
made source-visible later.

#### What This Covers

- Gap 2: helper parameter validation.
- Gap 4: override validation diagnostics.
- Gap 17: special declaration conflict diagnostics.
- Gap 18: provenance and readable failures.
- Gap 24: testable failure surfaces.

#### What It Does Not Cover

Runtime lifecycle errors, such as no active transaction, still live in generated
runtime methods. Diagnostic records primarily cover decoration-time generation
failures.

#### Tests

Bespoke:

- validation production writes a diagnostic
- final gate raises a clear error
- source label and field name appear in diagnostics
- direct exception and diagnostic-record modes do not both fire for the same
  validation

Goldens:

- A valid generated module includes no diagnostic runtime baggage unless needed.
- A diagnostic-producing source fixture can be a bespoke failure test rather
  than a success golden.

### Feature 7: External Fact Producers

#### Problem

Some lifecycle facts are derived from Python objects:

- callable signatures
- annotation shapes
- helper function arguments
- MRO layer records
- field declaration source labels

DDS should not grow Python introspection as core schema behavior, but these
facts must become records so matchers and productions can use them.

#### API Direction

Use aggregate generated operations for fact producers:

```python
dds.operation(
    "ProduceCallableFacts",
    inputs=(CallableDeclarations,),
    outputs=(CallableSpecs, CallableParams, CallableInjections),
    resource=CallableAnalyzerResource,
)
```

This can initially be implemented as an ordinary generated operation that calls
a source-emittable helper. The DDS API should remain about inputs and outputs,
not about `inspect.signature` details.

Do not add a public `dds.fact_producer(...)` API in V1. Use the aggregate
operation directly. If multiple analyzers later need the same fluent shape, add
`concept.operations.fact_producer(...)` as concept-layer sugar that lowers to
`dds.operation(...)`.

#### What This Covers

- Gap 10: callable injection.
- Gap 14: annotation-shape facts.
- Gap 22: decorator/helper harvesting.
- Gap 4: MRO layer harvesting, if modeled as input facts.

#### What It Does Not Cover

Fact producers do not select templates. They only produce records used by
matchers, productions, and validations.

#### Tests

Bespoke:

- callable analyzer rejects unsupported signatures
- annotation analyzer produces mapping/scalar facts
- fact producer output records validate against DDS shapes

Golden:

- Generated decorator-time source includes a callable analyzer helper and
  consumes its records in matcher/production output.

## Lifecycle Concepts Built Without New DDS Core

Several gaps should not become new DDS features. They should be expressed as
recorded concepts using the features above.

### State, Store, And Facade Topology

Use schema families, ports, generated resources, and operation contributions:

- State class is a class concept with state-role records.
- Facades are class concept instances with facade-role records.
- Stores are state refs and slot records.
- Receiver/state/facade bindings are generated resources.

No new DDS core API is needed beyond source-emittable resources and ports.

### Operation Matrix And Runtime Pipelines

Represent operation behavior as records:

- `OperationContribution`
- `RuntimePhase`
- `PhaseContribution`
- `MethodBodyComponent`

Then use existing matchers and productions to select templates and insert them
into method-body ports. Do not add a DDS "operation engine" until the record
and port model fails.

### Helper Library And Decorator Generation

Use module-level ports and generated resources:

- imports
- support classes
- helper functions
- decorators
- generated runtime container/matcher classes

This is a recorded concept concern. DDS only needs to be able to carry and emit
the resources.

### Runtime Performance Shape

Represent optimization choices as facts and matcher-selected templates:

- direct slot templates
- table lookup templates
- shared helper templates
- unrolled phase templates

Do not add optimization modes to DDS core.

## Gap-To-Feature Map

| Gap | Primary feature | Secondary feature |
| --- | --- | --- |
| Kind semantics | Schema families | Generated resources |
| Helper parameter policy | Validation/diagnostics | Schema families |
| FieldSpec variants | Schema families | Layered merge |
| MRO merge | Layered merge | Validation/diagnostics |
| Transaction indexing | Indexed derivations | Generated resources |
| State/store/facade topology | Lifecycle concepts over ports | Generated resources |
| StateRef/naming | Generated resources | Indexed derivations |
| Operation matrix | Lifecycle concepts over ports | Generated resources |
| Runtime phases | Lifecycle concepts over ports | Validation/diagnostics |
| Callable injection | External fact producers | Graph derivations |
| Initvar closure | Graph derivations | External fact producers |
| Default/factory ordering | Lifecycle operation records | Graph derivations |
| Transient/working semantics | Indexed derivations | Operation records |
| Binding/owned policies | External fact producers | Generated resources |
| Cleanup/rollback | Operation records | Validation/diagnostics |
| Classvar materialization | Schema families | Module/class ports |
| Special tx declarations | Indexed/keyed derivations | Validation/diagnostics |
| Diagnostics/provenance | Validation/diagnostics | Layered merge |
| Source emission | Generated resources | Astichi imports |
| Builder-phase matcher views | Existing snapshot model first | Defer builder views |
| Multi-facade binding | Generated resources | Lifecycle concepts over ports |
| Helper/decorator library | Module-level concepts | Generated resources |
| Performance shape | Matcher-selected templates | Indexed derivations |
| Lifecycle parity tests | Goldens | Bespoke diagnostics |

## Explicit Non-Features

Do not add these unless a later slice proves they are necessary:

- A lifecycle-specific DDS engine.
- A second matcher runtime.
- A second production API for matcher productions.
- A general SQL-like join/query language.
- A general fixpoint engine.
- A Python-introspection subsystem inside DDS core.
- A state/facade model inside DDS core.
- A field-kind class hierarchy mirroring `pyrolyze.lifecycle`.
- String enum tags for policies, ports, operation kinds, or resource kinds.

## Implementation Slices

The canonical roll-build order lives in
`dev-docs/lifecyle-plan/14-ImplementationSlicingDetailedPlan.md` for the
initial consolidated build and continues in
`dev-docs/lifecyle-plan/15-PostSlice14LifecycleParityDetailedPlan.md` for
post-slice-14 lifecycle parity. This plan does not duplicate the slice lists to
avoid drift. Gap closure by slice, golden targets, and parser work are defined
there.

## Lifecycle Staircase Data Model

The first generated lifecycle staircase should use records like these. Names are
illustrative; the implementation should follow current DDS naming conventions.

### Declaration Records

- `FieldSpec` union variants: managed, const, static, initvar, classvar, hook,
  validator, order key.
- `MergedField`.
- `TransactionalField`.
- `TxKey`.
- `SpecialDeclaration`.

### Derived Fact Records

- `FieldStorageRef`.
- `FieldOperationFact`.
- `CallableSpec`.
- `CallableParam`.
- `InitvarDependency`.
- `ResourcePolicy`.

### Output Contribution Records

- `ClassComponent`.
- `StateSlot`.
- `FacadeProperty`.
- `InitParam`.
- `InitStatement`.
- `OperationContribution`.
- `PhaseContribution`.
- `Diagnostic`.

These are lifecycle concept records, not DDS core objects.

## Runtime Operation Model

Use current ports and productions to assemble runtime methods.

Recommended ports:

- `Module.body`
- `Class.body`
- `Class.slots`
- `Class.__init__.params`
- `Class.__init__.body`
- `Property.getter`
- `Property.setter`
- `Operation.validate`
- `Operation.before_commit`
- `Operation.commit`
- `Operation.after_commit`
- `Operation.rollback`
- `Operation.close`

The port list can be encoded in lifecycle concepts. DDS only needs generic port
objects and ordered child lookup.

## Helper Surface Model

Helper function generation should be delayed until the core lifecycle staircase
works. Before then, helper calls may be represented by direct record creation in
tests and scratch drivers.

When helper generation starts:

- helper signatures should use Astichi parameter holes
- helper bodies should write field-spec records
- fixed/scrubbed/exposed parameters should be represented as helper parameter
  records or concept declarations
- helper functions should not invoke the Python parser at decoration time

## Testing Plan

Follow the project testing shape:

- Goldens for successful generated source and generated runtime scaffolding.
- Bespoke tests for narrow mechanics, validation errors, and diagnostics.
- Runtime tests only when generated classes need behavioral verification.

Canonical feature goldens are listed in
`dev-docs/lifecyle-plan/11-ActualFeatureEnumerationDetailedPlan.md`. Slice-level
goldens are listed in `dev-docs/lifecyle-plan/14-ImplementationSlicingDetailedPlan.md`
and `dev-docs/lifecyle-plan/15-PostSlice14LifecycleParityDetailedPlan.md`.

Lifecycle-flavored goldens such as layered merge, transaction indexing,
callable facts, initvar closure, and resource hooks remain useful, but they
should consume the canonical primitives rather than define additional DDS-core
surfaces.

Avoid duplicating the same success-path assertions in bespoke tests.

Astichi success-path coverage belongs in Astichi goldens. Lifecycle goldens may
assume the surfaces proved by `class_head.py` and
`lifecycle_template_surfaces.py`; add a new Astichi golden only when lifecycle
needs a new Astichi marker interaction.

## Design Summary Updates

Update `dev-docs/YidlDesignSummary.md` when a slice changes a canonical point:

- Schema family / field-spec union model.
- Layered MRO merge model.
- Transaction group indexing.
- Generated resource model.
- Diagnostics model.
- Callable fact model.
- Initvar closure model.
- Generated lifecycle staircase.

Do not maintain archived history docs.

## Stop Conditions

Stop and redesign before coding around the issue if any slice requires:

- parser calls in generated decorator or helper runtime paths
- helper-specific bespoke code for behavior that should be a matcher/resource
- a second matcher engine
- a second production runner
- string tags instead of semantic policy/resource objects
- lifecycle state/facade behavior embedded in DDS core
- copying large pieces of `pyrolyze.lifecycle`

## Expected Result

After these slices, DDS should have only a few new generic capabilities:

- composite collection identities
- keyed lookup value expressions
- ordered source sequences
- aggregate generated operations
- unified generated resources

Schema-family ergonomics, layered merge, distinct indexing, optional graph
closure, validation diagnostics, and external fact producers should be fluent or
lifecycle concept patterns built on those generic capabilities, not separate DDS
core engines.

The lifecycle implementation should then be a set of recorded concepts and
generated resources, not a special-purpose code generator. That is the key
constraint that keeps the design from turning into another large monolithic
lifecycle file.
