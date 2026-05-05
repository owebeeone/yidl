# Graph Closure Detailed Plan

## Goal

Add a narrow graph reachability derivation for initvar retention and similar
dependency classifications.

Critical review status: `reachable_collection(...)` is deferred as a public DDS
API. V1 reachability lowers to `dds.operation(...)`. Promote a graph-specific
API only after a second use case proves it is not lifecycle-specific sugar.

This feature should not become a general fixpoint engine unless another
non-lifecycle use case proves the need.

## Problem

Initvars are constructor-only unless a late consumer needs their value after the
initial constructor assignment phase. Callable facts can tell us which callable
consumes which initvar, but the lifecycle generator still needs to know:

- which initvars are retained
- which initvars are constructor-only
- which initvars are unused
- whether dependency cycles exist

Current computed collections can filter records but cannot traverse dependency
edges.

## Operation-First API

```python
InitvarEdges = dds.collection("InitvarEdges", InitvarEdge)

dds.operation(
    "BuildRetainedInitVars",
    inputs=(LateInitvarConsumers, InitvarEdges),
    outputs=(RetainedInitVars,),
    resource=BuildRetainedInitVarsOperation,
)
```

A later fluent helper may wrap this shape:

```python
concept.operations.reachable(...)
```

Do not add `dds.reachable_collection(...)` as a V1 DDS-core API.

### Edge Record Shape

```python
InitvarEdge = dds.record(
    "InitvarEdge",
    Consumer,
    InitVarName,
    SourceLabel,
)
```

`Consumer` and `InitVarName` are source-renderable identities, usually strings.

### Derived Views

```python
ConstructorOnlyInitVars = dds.computed_collection(
    "ConstructorOnlyInitVars",
    source=InitVars,
    when=(not_in(Name, RetainedInitVars),),
)

UnusedInitVars = dds.computed_collection(
    "UnusedInitVars",
    source=InitVars,
    when=(not_in(Name, UsedInitVars),),
)
```

If `not_in(...)` is too much expression surface, implement these as ordinary
productions that build lookup sets in generated source.

## Exact Reachability Semantics

V1 should use this rule:

- roots are identity values
- edges are directed from `from_property` to `to_property`
- output is every reached `to_property`
- traversal is breadth-first or depth-first; output order is stable by first
  discovery, then source order
- cycles are allowed only if they do not require ordering; for initvars, cycles
  should reject because they imply invalid dependency structure
- max traversal depth defaults to number of edges plus one

For initvar retention, roots are late consumers, not all consumers. This means:

- constructor-only default factory consumer does not retain an initvar
- commit hook consumer does retain an initvar
- state copy/freeze/thaw consumer may retain depending on phase

## Expected Use Case

Input:

```python
InitVars:
    seed
    owner
    session

CallableFacts:
    default_count consumes seed
    commit_owner consumes owner
    after_commit_session consumes session
```

Late consumers:

```python
commit_owner
after_commit_session
```

Edges:

```python
commit_owner -> owner
after_commit_session -> session
default_count -> seed
```

Output:

```python
RetainedInitVars:
    owner
    session

ConstructorOnlyInitVars:
    seed
```

## Expected Generated Source Golden

Expected excerpt for
`tests/data/goldens/materialized/dds_lifecycle_initvar_closure.py`:

```python
def build_retained_initvars(ctx):
    roots = [
        record.consumer
        for record in ctx.records(LateInitvarConsumersCollection)
    ]
    edges_by_consumer = {}
    for edge in ctx.records(InitvarEdgesCollection):
        edges_by_consumer.setdefault(edge.consumer, []).append(edge)

    seen = set()
    queue = list(roots)
    while queue:
        consumer = queue.pop(0)
        for edge in edges_by_consumer.get(consumer, ()):
            initvar_name = edge.initvar_name
            if initvar_name in seen:
                continue
            seen.add(initvar_name)
            ctx.write(
                RetainedInitVarsCollection,
                RetainedInitVar(name=initvar_name, source_label=edge.source_label),
                policy=AddIfAbsent,
            )


def build_constructor_only_initvars(ctx):
    retained = {
        record.name
        for record in ctx.records(RetainedInitVarsCollection)
    }
    for initvar in ctx.records(InitVarsCollection):
        if initvar.name in retained:
            continue
        ctx.write(
            ConstructorOnlyInitVarsCollection,
            ConstructorOnlyInitVar(
                name=initvar.name,
                source_label=initvar.source_label,
            ),
            policy=AddIfAbsent,
        )


def run_operations(ctx):
    build_retained_initvars(ctx)
    build_constructor_only_initvars(ctx)
    return ctx.freeze()
```

The golden must prove:

- graph traversal is generated source
- no generic recursive/fixpoint runtime is introduced
- retained and constructor-only classifications are ordinary records
- output order is deterministic

## Cycle Handling

For V1 initvar closure, cycles should reject if they involve generated ordering
requirements.

Simple visited-set cycles that only repeat already-retained initvars do not need
to reject. Example:

```text
A -> seed
A -> A
```

This should terminate. But a dependency graph that says initvar `a` requires
`b` and `b` requires `a` for initialization order should reject. If that case is
not represented yet, do not add cycle diagnostics prematurely.

## Diagnostics

Required diagnostics:

- root references unknown consumer if strict mode is enabled
- edge references unknown initvar
- cycle in ordering dependency graph, once ordering edges exist
- unused initvar

Unused initvars can be emitted by set difference:

```python
used = {edge.initvar_name for edge in InitvarEdges}
unused = InitVars - used
```

## Implementation Notes

Start with an aggregate generated operation. Avoid a generic graph runtime
object. A `concept.operations.reachable(...)` helper is acceptable only if it
lowers to that same operation model.

If the implementation starts to require:

- arbitrary node types
- multiple edge labels
- recursive fixpoint groups
- query optimization

stop and move graph closure back into a lifecycle-specific concept until a
second generic use case appears.

## Test Plan

Bespoke:

- `test_reachable_collection_direct_edges`
- `test_reachable_collection_transitive_edges`
- `test_reachable_collection_deterministic_order`
- `test_reachable_collection_unknown_target_diagnostic`

Goldens:

- `tests/data/gold_src/dds_lifecycle_initvar_closure.py`
- `tests/data/goldens/materialized/dds_lifecycle_initvar_closure.py`

The golden should include:

- three initvars
- one constructor-only initvar
- two retained initvars
- unused initvar diagnostic in a bespoke failure fixture
