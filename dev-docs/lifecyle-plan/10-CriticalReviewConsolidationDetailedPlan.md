# Critical Review And Consolidation Detailed Plan

## Purpose

This document reviews the detailed lifecycle DDS plan set and consolidates the
proposed features into the smallest practical API surface.

The earlier detailed plans intentionally explored several named APIs:

- `UnionSpec.common(...)`
- `dds.layered_merge(...)`
- `dds.distinct_indexed_collection(...)`
- `dds.reachable_collection(...)`
- `dds.fact_producer(...)`
- diagnostic record/gate APIs

After review, most of those should not become initial DDS-core APIs. They are
useful patterns, but they can be represented by fewer generic primitives.

## Review Finding

The detailed plans correctly identify lifecycle requirements, but several
feature documents promoted use-case-specific conveniences into apparent DDS
features. That would create API bloat and multiple ways to express the same
operation.

The underlying common pattern is:

1. read one or more source collections in deterministic order
2. compute zero or more output records
3. write output records with merge policies
4. optionally call source-emittable helper resources
5. optionally write diagnostics as ordinary records

That pattern covers:

- layered merge
- transaction group indexing
- callable fact production
- annotation shape production
- graph reachability
- validation diagnostics
- lifecycle operation contribution generation

Therefore the missing generic feature is not five separate APIs. It is an
aggregate generated operation over declared inputs and outputs.

## Consolidated DDS Features

The actual DDS/generation-layer feature set should be:

1. Composite collection identity.
2. Keyed lookup value expression.
3. Ordered source sequences.
4. Aggregate generated operation.
5. Unified generated resource emission.

Everything else moves to the fluent/concept layer.

## Consolidated Fluent/Concept Features

The fluent layer may provide convenience helpers:

1. Schema-family helpers over existing unions.
2. Layered merge helper lowering to aggregate operation.
3. Distinct-index helper lowering to aggregate operation.
4. Reachability helper lowering to aggregate operation.
5. Fact-producer helper lowering to aggregate operation.
6. Diagnostic concept helper defining records and gates.
7. Lifecycle class/facade/state concept helpers.
8. YIDL file import and concept composition.

These helpers are acceptable because they do not add a second runtime model.
They lower to the same DDS concepts.

## Rejected Initial DDS APIs

### `UnionSpec.common(...)`

Rejected as an initial DDS-core API.

Reason: common properties are authoring sugar. The concept builder can record a
family with common properties and replay ordinary `UnionSpec.variant(...)`
calls. If multiple independent fluent builders need common properties and the
helper becomes duplicated, `UnionSpec.common(...)` can be promoted later.

Replacement:

```python
fields = concept.schema_family("FieldSpecs")
fields.common(Name, Annotation, SourceOrder)
fields.variant("ManagedField", Kind, TxGroup)
```

Lowering:

```python
FieldSpecs = dds.union("FieldSpecs")
ManagedField = FieldSpecs.variant(
    "ManagedField",
    Name,
    Annotation,
    SourceOrder,
    Kind,
    TxGroup,
)
```

### `dds.layered_merge(...)`

Rejected as an initial DDS-core API.

Reason: layered merge is an aggregate operation with ordered input and custom
write policy. It does not need special DDS syntax.

Replacement:

```python
dds.operation(
    "MergeFieldSpecs",
    inputs=(LayerFields,),
    outputs=(MergedFields,),
    order_by=(LayerIndex, SourceOrder),
    resource=MergeFieldSpecsOperation,
)
```

The fluent lifecycle layer may offer:

```python
lifecycle.layered_merge(...)
```

but it lowers to `dds.operation(...)`.

### `dds.distinct_indexed_collection(...)`

Rejected as an initial DDS-core API.

Reason: distinct indexing is also an aggregate operation. The only core pieces
needed are ordered source iteration and composite/key lookup support.

Replacement:

```python
dds.operation(
    "BuildTxGroups",
    inputs=(TransactionalFields,),
    outputs=(TxGroups,),
    order_by=(SourceOrder,),
    resource=BuildTxGroupsOperation,
)
```

The fluent layer may provide:

```python
concept.operations.distinct_index(...)
```

as sugar.

### `dds.reachable_collection(...)`

Rejected as an initial DDS-core API.

Reason: graph reachability is needed only after callable/initvar facts exist.
It should first be an aggregate operation. A public graph derivation API should
wait for a second use case.

Replacement:

```python
dds.operation(
    "BuildRetainedInitVars",
    inputs=(LateInitvarConsumers, InitvarEdges),
    outputs=(RetainedInitVars,),
    resource=BuildRetainedInitVarsOperation,
)
```

### `dds.fact_producer(...)`

Rejected as an initial DDS-core API.

Reason: fact production is just an aggregate operation that calls an analyzer
resource and writes output records.

Replacement:

```python
dds.operation(
    "ProduceCallableFacts",
    inputs=(CallableDeclarations,),
    outputs=(CallableSpecs, CallableParams, CallableInjections),
    resource=CallableAnalyzerOperation,
)
```

### DDS Diagnostic Engine

Rejected as an initial DDS-core API.

Reason: diagnostics are records plus a gate. DDS should support ordinary records
and generated operations well enough that a diagnostics concept can be built on
top.

Replacement:

```python
DiagnosticsConcept = concept.extends(...)
Diagnostics = DiagnosticsConcept.collections.Diagnostics
RaiseDiagnostics = DiagnosticsConcept.resources.RaiseDiagnosticsOperation
```

## Actual Core Additions In Detail

### 1. Composite Identity

Current collections need to support identities containing more than one
property:

```python
SpecialDeclarations = dds.collection(
    "SpecialDeclarations",
    SpecialDeclaration,
    identity=(SpecialKind, TxGroup),
)
```

Runtime identity:

```python
key = (record.special_kind, record.tx_group)
```

This replaces multiple special uniqueness APIs.

### 2. Keyed Lookup

Productions and operations need a source-emittable lookup expression:

```python
lookup(TxGroups, key=source.prop(TxGroup), value=TxIndex)
```

This replaces ad hoc transaction-index binding logic.

### 3. Ordered Source Sequences

Generated operations need deterministic source iteration:

```python
source = LayerFields.ordered(LayerIndex, SourceOrder)
```

or:

```python
dds.operation(..., order_by=(LayerIndex, SourceOrder))
```

This replaces specialized merge/index traversal APIs.

### 4. Aggregate Generated Operations

Add a generic generated operation:

```python
dds.operation(
    "OperationName",
    inputs=(InputCollectionA, InputCollectionB),
    outputs=(OutputCollection,),
    resource=OperationResource,
)
```

The operation resource emits code that receives a builder or operation context,
reads declared inputs, and writes declared outputs. The declared inputs/outputs
are validation and source-emission metadata.

This replaces:

- fact producer
- graph closure
- layered merge
- distinct index
- diagnostics validation helper

### 5. Unified Generated Resources

Generated resources must be usable in:

- matcher resources
- production value expressions
- aggregate operation resources
- record fields
- final renderers

This is an extension/generalization of the current matcher generated-value
surface, not a new resource family.

## Remaining Ambiguities And Decisions

### Does `dds.operation(...)` Receive Builder Or A Narrow Context?

Decision: generated operation resources receive a narrow operation context in
their public contract, but V1 may implement that context as a builder wrapper.

Example generated source:

```python
def run_merge_field_specs(ctx):
    for record in ctx.records(LayerFieldsCollection):
        ...
        ctx.write(MergedFieldsCollection, merged, policy=ReplaceExisting)
```

This avoids exposing the full builder forever while keeping implementation
simple.

### Should Operation Resources Be Astichi Or Python Callables?

Decision: operation resources are generated resources. They may be backed by
Astichi code or by an imported helper. Runtime decorator paths must use emitted
source or imported helpers; they must not compile source dynamically.

### How Do Operations Interleave With Productions?

Decision: V1 executes productions and aggregate operations in production-group
order. Within a group, declaration order is the execution order. A group may
contain both record-to-record productions and aggregate operations. Each
production or operation observes the builder state at the start of that step
and writes to the same builder for later steps in the group.

There is no separate operation scheduler in V1.

### What Is The Source Render Entry Point?

Decision: rendering is a concept-provided generated resource:

```python
runtime.render_module(container, *, class_name="Example")
```

The exact runtime class can change, but the shape is stable: final rendering
consumes a frozen container and returns an Astichi composable or materialized
source. Renderers are not hidden inside DDS containers.

### What Is Idempotent Concept Replay?

Decision: concept replay is idempotent only for structurally identical
definitions. For properties, records, collections, ports, resources, matchers,
productions, and operations, identical means the semantic declaration has the
same name, same dependencies, same target collections/ports, same rule
conditions, same resource identity, same ordering, and same policy.

Two identical declarations replay once. Two same-named but different
declarations reject. Matcher rules are not accumulated by accident: a rule name
is an identity inside its matcher.

### Are Diagnostics Records Required In Every Generated Module?

Decision: no. Diagnostics are included only when a concept uses them. Valid
generated modules should not carry diagnostic machinery unless a validation
operation exists.

### Is Graph Closure A First-Class Feature?

Decision: not yet. Use aggregate operations. Promote graph closure only after a
second non-initvar use case appears.

## Updated Roll-Build Order

The canonical slice order lives in
`14-ImplementationSlicingDetailedPlan.md`. This review establishes the
consolidated feature set; the slicing document owns the sequence.

## Updated Golden Strategy

The canonical feature-to-golden map lives in
`11-ActualFeatureEnumerationDetailedPlan.md`, with slice-level usage in
`14-ImplementationSlicingDetailedPlan.md`.

Older proposed goldens for layered merge, distinct index, fact producer, and
reachable collection remain valid as lifecycle/concept goldens only if they
show lowering through aggregate operations.
