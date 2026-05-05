# Actual Feature Enumeration

## Purpose

This document crisply enumerates the features actually being added after the
critical review. It separates DDS-core additions from fluent/concept-layer
additions.

## DDS Core / Generation Features

### DDS-1: Composite Collection Identity

Allow a collection identity to be one property or a tuple of properties.

API:

```python
Items = dds.collection("Items", ItemRecord, identity=Name)

SpecialDeclarations = dds.collection(
    "SpecialDeclarations",
    SpecialDeclaration,
    identity=(SpecialKind, TxGroup),
)
```

Runtime behavior:

```python
identity = record.name
identity = (record.special_kind, record.tx_group)
```

Required support:

- `builder.matching(...)`
- `builder.write(...)`
- `DDSContainer.matching(...)`
- generated source emission
- duplicate diagnostics

### DDS-2: Keyed Lookup Value Expression

Add a value expression that reads a record from a keyed collection and returns a
property from the matched record.

API:

```python
lookup(TxGroups, key=source.prop(TxGroup), value=TxIndex)
```

Optional default:

```python
lookup(TxGroups, key=source.prop(TxGroup), value=TxIndex, default=-1)
```

Default should be rare. Missing lookup is usually a design error.

### DDS-3: Ordered Source Sequences

Allow productions and operations to request stable source ordering.

API options:

```python
LayerFields.ordered(LayerIndex, SourceOrder)
```

or:

```python
dds.operation(
    "MergeFieldSpecs",
    inputs=(LayerFields,),
    outputs=(MergedFields,),
    order_by=(LayerIndex, SourceOrder),
    resource=MergeFieldSpecsOperation,
)
```

Semantics:

- sort by listed properties
- tie-break by collection write order
- reject absent order property unless explicitly configured as nullable

### DDS-4: Aggregate Generated Operation

Add a generated operation over declared inputs and outputs.

API:

```python
dds.operation(
    "ProduceCallableFacts",
    inputs=(CallableDeclarations,),
    outputs=(CallableSpecs, CallableParams, CallableInjections),
    resource=ProduceCallableFactsOperation,
)
```

Operation resource contract:

```python
def run_operation(ctx):
    for record in ctx.records(InputCollection):
        ctx.write(OutputCollection, output_record, policy=ReplaceExisting)
```

Generated operation context must expose:

- `records(collection)`
- `matching(collection, identity)`
- `write(collection, record, policy=...)`
- optionally `children_at(port_address)` if needed

V1 execution uses production-group declaration order. Productions and aggregate
operations can share a group; each step observes current builder state and
writes records for later steps.

This single feature covers:

- layered merge
- transaction index derivation
- callable fact production
- annotation fact production
- graph closure
- validation diagnostics

### DDS-5: Generated Resource Unification

Generalize matcher generated values so the same source-emittable object can be
used by matchers, productions, operations, and final renderers.

API:

```python
from_astichi_code(source, ...)
from_astichi_template(source, ...)
from_literal(value)
from_import(module, name)
```

Required behavior:

- deterministic `to_generator()` with caching
- source expression emission
- Astichi import consolidation via `astichi_pyimport(...)`
- storage in generated record fields
- use as matcher result resource
- use as aggregate operation resource

## Fluent / Concept Layer Features

### FLUENT-1: Schema Family Builder

Provide a data-driven authoring layer over unions.

API:

```python
fields = concept.schema_family("FieldSpecs")
fields.common(Name, Annotation, SourceOrder, SourceLabel)
fields.variant("ManagedField", Kind, TxGroup, Default)
fields.variant("InitVarField", Default, DefaultFactory)
```

Lowering:

```python
FieldSpecs = dds.union("FieldSpecs")
ManagedField = FieldSpecs.variant(
    "ManagedField",
    Name,
    Annotation,
    SourceOrder,
    SourceLabel,
    Kind,
    TxGroup,
    Default,
)
```

### FLUENT-2: Concept Extension And Symbol Access

Concepts can extend other concepts and access previously defined symbols.

API:

```python
builder = CapsuleConceptBuilder("ManagedFieldConcept")
Core = builder.extends(LifecycleCoreConcept)

Name = Core.props.Name
FieldSpecs = Core.unions.FieldSpecs
ManagedField = FieldSpecs.variant("ManagedField", Core.props.TxGroup)
```

Rules:

- one concept defines a symbol
- extending concepts reference the symbol
- incompatible redefinition rejects
- identical replay is idempotent

### FLUENT-3: Aggregate Operation Helpers

Provide convenience helpers that lower to `dds.operation(...)`.

Examples:

```python
concept.operations.layered_merge(...)
concept.operations.distinct_index(...)
concept.operations.reachable(...)
concept.operations.fact_producer(...)
concept.operations.validate(...)
```

These helpers are not DDS-core APIs.

### FLUENT-4: Diagnostic Concept

Provide a reusable concept that defines diagnostic records and a final gate.

API:

```python
Diagnostics = builder.extends(DiagnosticsConcept)

builder.operations.validate(
    "ValidateUnusedInitvars",
    source=UnusedInitVars,
    message=...,
)
```

Lowering:

- diagnostic records
- validation aggregate operation
- final gate operation

### FLUENT-5: Resource Declaration Namespace

Concept builders should declare resources by stable semantic name.

API:

```python
builder.resources.ManagedGetter(
    from_astichi_template("...")
)

ManagedGetter = builder.resources.ManagedGetter
```

Generated source uses stable resource names where possible.

### FLUENT-6: YIDL File Import And Composition

`.yidl` files compile to concept plans. A file can import concepts, properties,
records, resources, matchers, and ports from another `.yidl` file.

The first parser implementation should use Lark and lower parsed modules into
recorded concept/DDS builder calls. Lark is a definition-stage dependency only;
generated decorator/runtime code must not invoke it.

Example:

```text
import "./lifecycle-core.yidl" as core

concept ManagedFields extends core.LifecycleCore {
    use core.Name
    use core.FieldSpecs
    ...
}
```

Imports are declarative. They do not execute Python.

## Explicitly Not Added

These are not actual features for the first implementation:

- `dds.layered_merge(...)`
- `dds.distinct_indexed_collection(...)`
- `dds.reachable_collection(...)`
- `dds.fact_producer(...)`
- DDS-level diagnostics engine
- DDS-level state/facade model
- DDS-level lifecycle operation matrix
- DDS-level callable inspection
- DDS-level annotation inspection

They may exist as fluent helpers or lifecycle concepts that lower to aggregate
operations.

## Feature-To-Golden Map

| Feature | Golden |
| --- | --- |
| DDS-1 + DDS-2 | `dds_composite_identity_lookup.py` |
| DDS-3 | `dds_ordered_source_sequence.py` |
| DDS-4 | `dds_ordered_aggregate_operation.py` |
| DDS-5 | `dds_generated_resource_flow.py` |
| FLUENT-1 + FLUENT-2 | `dds_fluent_schema_family.py` |
| FLUENT-3 + FLUENT-4 | `dds_lifecycle_validation_operation.py` |
| FLUENT-5 | `dds_resource_namespace.py` |
| FLUENT-6 | `yidl_imported_concepts.py` |
| Lifecycle concepts | `dds_lifecycle_concepts.py` |
| Lifecycle staircase | `dds_lifecycle_managed_const_staircase.py` |

Lifecycle success goldens should then consume these features rather than
reasserting their mechanics.
