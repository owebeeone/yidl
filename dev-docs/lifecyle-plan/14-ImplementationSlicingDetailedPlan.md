# Implementation Slicing Detailed Plan

## Purpose

Define the roll-build order for lifecycle gap closure after consolidation.

Each slice should land as a small working increment with:

- the generic DDS/fluent feature
- the minimum lifecycle concept usage that pressures it
- generated-source golden coverage for success paths
- bespoke tests only for narrow mechanics and failure diagnostics

## Slice 0: Baseline And Proof Check

Confirm current implemented surfaces before changing code:

- DDS container/write/collection behavior
- matcher generated runtime
- generated values and current factories such as `from_literal(...)` and
  `from_astichi_code(...)`
- production groups and ports
- recorded capsule concept replay
- Astichi goldens `class_head.py` and `lifecycle_template_surfaces.py`

No feature code should land in this slice. The outcome is a short branch or PR
note naming what is reused.

## Slice 1: Composite Identity And Keyed Lookup

Add tuple identity support where collections, builder writes, frozen containers,
and generated runtime source need it.

Add keyed lookup value expressions:

```python
lookup(TxGroups, key=source.prop(TxGroup), value=TxIndex)
```

Goldens:

- `dds_composite_identity_lookup.py`

Bespoke tests:

- duplicate tuple identity rejects
- missing lookup rejects unless default is explicit
- generated lookup source is deterministic

## Slice 2: Ordered Source Sequences

Add stable ordering for production and operation inputs:

```python
LayerFields.ordered(LayerIndex, SourceOrder)
```

or the equivalent operation input declaration.

Tie-break by collection write order. Do not use Python object identity as an
ordering fallback.

Goldens:

- `dds_ordered_source_sequence.py`

Bespoke tests:

- absent order property rejects
- ties preserve write order

## Slice 3: Aggregate Generated Operations

Add the generic operation surface:

```python
dds.operation(
    "BuildTxGroups",
    inputs=(TransactionalFields,),
    outputs=(TxGroups,),
    order_by=(SourceOrder,),
    resource=BuildTxGroupsOperation,
)
```

This is the single mechanism used for:

- layered merge
- distinct transaction indexing
- callable fact production
- validation record production
- graph closure if needed later

Do not add public DDS shortcuts such as `dds.layered_merge(...)` or
`dds.distinct_indexed_collection(...)` in this slice. Those may become fluent
helpers after multiple concepts prove the shape.

Goldens:

- `dds_ordered_aggregate_operation.py`
- first scratch lifecycle data flow deriving transaction groups

Bespoke tests:

- generated operation can read inputs and write outputs
- operation write policy errors include operation name and target collection

## Slice 4: Generated Resource Unification

Generalize generated values so resources can be used by matchers, productions,
operations, and final renderers.

Required resource forms:

- Astichi code/template resources
- Python literal resources
- imported symbol resources through `from_import(...)` for consumers outside an
  Astichi template

Inside Astichi templates, prefer `astichi_pyimport(...)` at point of use so
Astichi can consolidate imports.

Generated resource templates should include `astichi_comment(...)` where the
comment improves inspectability.

Goldens:

- `dds_generated_resource_flow.py`
- matcher-selected resource stored in a record and consumed by a renderer

Bespoke tests:

- resource caching is deterministic
- invalid source-emission fails with a focused diagnostic

## Slice 5: Fluent Schema Family And Concept Ergonomics

Add the recorded/fluent layer needed to define lifecycle field families without
boilerplate.

This layer should lower to existing DDS unions, records, collections, matchers,
resources, and operations. It should not introduce a second schema system.

Goldens:

- `dds_fluent_schema_family.py`

Bespoke tests:

- one concept defines a symbol
- extending concepts can reference it
- incompatible redefinition rejects
- identical replay is idempotent

## Slice 6: Lark-Based YIDL Parser

Create the `.yidl` parser using Lark.

The parser is definition-stage only. It must not appear in generated decorators,
generated field-spec functions, or decorator-time runtime paths.

Rationale: this slice lands after the DDS/fluent surfaces it lowers into
(Slices 1-5) and before lifecycle concepts that may be authored in `.yidl`
(Slices 8+). Slices 7-11 may still use Python concept builders while the YIDL
surface proves out; the parser slice exists to ensure `.yidl` can define the
same concepts data-driven.

Work:

- transcribe `12-YidlGrammarProposalDetailedPlan.md` into a `.lark` grammar
- parse `.yidl` files into a small YIDL module AST
- add symbol resolution for imports, exports, concepts, families, matchers,
  productions, operations, and resources
- lower the checked AST into recorded concept/DDS builder calls
- keep parser errors, symbol-resolution errors, and DDS replay errors distinct

Goldens:

- `yidl_imported_concepts.py`

Bespoke tests:

- syntax error includes line/column
- undefined symbol diagnostic
- imported symbol cannot be redefined
- extended family resolves properties through extending concept first, then
  owning concept

## Slice 7: Diagnostics As Concepts

Define diagnostic records and final validation gates in the concept layer.

Do not add a DDS-level diagnostics engine unless direct validation productions
become duplicated across unrelated concepts.

Goldens:

- `dds_lifecycle_validation_operation.py`
- valid lifecycle output contains no diagnostic baggage

Bespoke tests:

- duplicate field diagnostic
- invalid override diagnostic
- missing template binding diagnostic

## Slice 8: Lifecycle Concept Assembly

Build the first lifecycle concept set from the generic pieces:

- field-family concept
- state class concept
- facade class concept
- property concept
- transaction index concept
- operation contribution concept

Use `extends` for concept composition.

Goldens:

- `dds_lifecycle_concepts.py`

The golden must prove class source is assembled from contribution records, not
from an ad hoc class generator.

## Slice 9: Lifecycle Staircase

Build the first end-to-end lifecycle subset:

- managed field
- const/read-only field
- state class
- direct facade class
- `__slots__`
- init params and body
- property getter/setter
- simple commit
- simple rollback

Goldens:

- `dds_lifecycle_managed_const_staircase.py`

Runtime check:

- construct generated class
- get managed and const values
- set managed value
- rollback working value
- commit working value
- const setter is absent/read-only

## Slice 10: External Fact Producers

Add generated operations that turn Python-object facts into DDS records without
embedding introspection in DDS core.

Start with callable signature facts because hooks, validators, defaults, and
initvar retention all need them.

Goldens:

- `dds_lifecycle_callable_facts.py`

Bespoke tests:

- accepted callable signatures
- rejected callable signatures
- analyzer output validates against DDS record shapes

## Slice 11: Resource Fields And Hooks

Extend the staircase to binding/owned resources and lifecycle hooks.

Work:

- resource policy records and templates
- cleanup phase contributions
- hook/validator/order-key callable facts
- transaction-group keyed validation
- rollback aggregation once cleanup paths exist

Goldens:

- `dds_lifecycle_resource_hooks.py`

Bespoke tests:

- duplicate validator/order-key diagnostics
- cleanup phase ordering
- unsupported resource policy diagnostics

## Post-Slice-14 Lifecycle Parity Continuation

The roll-build has continued beyond the initial consolidated slices. The
detailed continuation lives in
`15-PostSlice14LifecycleParityDetailedPlan.md`.

That continuation owns the parity slices for:

- generated decorator and helper surface
- default and factory initialization
- full callable injection matrix
- transaction manager and active transaction semantics
- commit/rollback pipeline parity
- advanced managed value semantics
- static/transient/local-store/derived/classvar field kinds
- binding and owned resource semantics
- multi-facade state routing
- MRO merge and override parity
- runtime parity harness

## Deferred Slice: Graph Closure

Do not build graph closure until initvar retention or another concrete feature
requires it.

When needed, graph closure should be an aggregate generated operation first. A
public `reachable_collection(...)` helper is allowed only after repeated use
proves the helper is worth adding.

## Verification Commands

Use focused tests during each slice, then run the relevant golden suite.

Typical commands:

```bash
uv run --with pytest pytest tests/generation/<focused-test-file>.py -q
uv run --with pytest pytest tests/generation/test_data_container.py -q
```

For Astichi surface work:

```bash
uv run --with pytest pytest tests/test_ast_goldens.py -q
```

## Roll-Build Rule

Do not implement several slices in isolation and integrate later. Each slice
must immediately pressure the next lifecycle scratch/staircase driver. If a
slice cannot be used by the driver, it is probably too abstract or the wrong
surface.

## Renderer Entry Point

Lifecycle rendering should be modeled as a generated resource on the runtime or
concept bundle:

```python
runtime.render_module(container, *, class_name="Example")
```

The renderer consumes a frozen container and returns an Astichi composable or
materialized source. DDS containers should not know how to render lifecycle
classes directly.

Renderer implementation is incremental: Slice 4 proves resources can be
consumed, Slice 8 proves contribution-record assembly, and Slice 9 stabilizes
the `runtime.render_module(...)` signature for the staircase module.
