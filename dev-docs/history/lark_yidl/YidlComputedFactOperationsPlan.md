# YIDL Computed Fact Operations Plan

## Status

Draft design and implementation plan.

This plan covers the next YIDL capability needed by the layered dataclass-like
compiler: deriving new fact collections from existing fact collections with
Astichi-backed Python code, while keeping implementation selection inside the
normal concept/matcher merge model.

The immediate proof case is an extension to `default_factory` semantics for a
dataclass-like decorator. Zero-argument factories keep the stdlib meaning;
factories with named parameters become computed defaults whose parameters are
resolved from the init value environment:

```python
@computedclass
class Example:
    v1: int
    v3: int = field(default_factory=lambda v2, v1: v1 + v2 + 2)
    v2: int = field(default_factory=lambda v1: v1 + 2)
```

The generic feature is not hard-coded `default_factory` handling. The generic
feature is:

- run an Astichi-backed operation over existing collections
- let that operation write derived records into output collections
- select or override the operation implementation through matchers
- let later YIDL matchers, productions, and assemblies consume those derived
  records as ordinary facts

## Motivation

YIDL is intentionally fact/resource/matcher driven. Some facts are supplied by
the decorator/runtime input, but many useful facts are computed from those
inputs:

- callable parameter facts from a function signature
- dependency edges between computed defaults
- topological init/evaluation order
- validation diagnostics
- normalized records derived from user-facing shorthand
- closure facts for lifecycle initvars and callable injections

These are algorithms, not grammar. They are better implemented as Python code
that runs during the generated decorator/container build than as a larger YIDL
expression language.

The current codebase already has most of the ingredients:

- `operation Name inputs(...) outputs(...) using Resource` exists in the Lark
  grammar.
- Generated DDS operations receive a `ctx` object and can read/write
  collections.
- Operation bodies are Astichi code resources today.
- `astichi_pyimport(...)` lets an operation body call helper functions from an
  external Python module.
- Concept merging already gives matcher rules the role of behavior extension
  and override.

The missing part is a clean way for operations to have matcher-selected
implementations, so feature concepts can add more specific operation bodies
without replacing base operations.

## Current Operation Surface

The current grammar has direct-resource operations:

```yidl
operation BuildItems inputs(Items) outputs(Items) using BuildItemsBody {
    ordered(Order)
}
```

The operation body is a code resource:

```yidl
resource BuildItemsBody = code $[
    for item in ctx.records(ItemsCollection):
        ctx.write(ItemsCollection, Item(name=item.name), policy=RejectDuplicate)
]$ {
    keep ctx, ItemsCollection, Item, RejectDuplicate
}
```

Current properties:

- The body is static: one resource is selected at YIDL compile/lowering time.
- The body is Astichi code, not a string naming a Python function.
- The body can inline the algorithm or import a helper function with
  `astichi_pyimport(...)`.
- The body can write output facts through `ctx.write(...)` or `ctx.add(...)`.

Current gap:

- `using match.resource()` is rejected for operations.
- There is no operation-level matcher binding such as "for each facade, choose
  the most specific operation implementation and run it".

## Design Goal

Add matcher-selectable computed fact operations without making operation
algorithms part of YIDL syntax.

The YIDL source should be able to say:

```yidl
operation BuildDefaultFactoryFacts
    from facade: Facades
    inputs(Facades, Fields)
    outputs(DefaultFactoryDeps, InitEvaluationSteps, Diagnostics)
    using matcher DefaultFactoryFactOperations
```

The selected implementation remains an Astichi code resource:

```yidl
resource DefaultFactoryFactsBody = code $[
    from inspect import signature

    fields = [
        field for field in ctx.records(FieldsCollection)
        if field.field_owner == facade.class_id
    ]
    by_name = {field.field_name: field for field in fields}
    graph = {}

    for field in fields:
        if not field.has_default_factory:
            continue
        graph.setdefault(field.field_id, set())
        for order, param in enumerate(
            signature(field.default_factory).parameters.values()
        ):
            provider = by_name.get(param.name)
            if provider is None:
                ctx.write(
                    DiagnosticsCollection,
                    Diagnostic(
                        diagnostic_id=f"{field.field_id}.{param.name}",
                        diagnostic_owner=facade.class_id,
                        diagnostic_message=(
                            f"field {field.field_name} default_factory "
                            f"unknown dependency {param.name!r}"
                        ),
                    ),
                    policy=ReplaceExisting,
                )
                continue
            graph[field.field_id].add(provider.field_id)
            ctx.write(
                DefaultFactoryDepsCollection,
                DefaultFactoryDep(
                    dependency_owner=facade.class_id,
                    consumer_field_id=field.field_id,
                    provider_field_id=provider.field_id,
                    provider_name=provider.field_name,
                    param_name=param.name,
                    param_order=order,
                ),
                policy=RejectDuplicate,
            )

    # Topologically sort `graph` and write InitEvaluationStep records here.
]$ {
    keep ctx, facade, FieldsCollection, DefaultFactoryDepsCollection
    keep InitEvaluationStepsCollection, DiagnosticsCollection
    keep DefaultFactoryDep, InitEvaluationStep, Diagnostic
    keep RejectDuplicate, ReplaceExisting, signature
}
```

The matcher chooses the implementation:

```yidl
matcher DefaultFactoryFactOperations(facade: Facades) -> operation {
    default -> DefaultFactoryFactsBody
}
```

A feature concept can add a more specific rule:

```yidl
concept CachedDefaults extends ComputedClassDefaultFactoryParams {
    resource CachedDefaultFactoryFactsBody = code $[
        ...
    ]$

    matcher DefaultFactoryFactOperations(facade: Facades) -> operation {
        rule cached when UsesCachedDefaults == True -> CachedDefaultFactoryFactsBody
    }
}
```

`ComputedClassDefaultFactoryParams` is the feature concept introduced by the
`computedclass_default_factory_params.yidl` proof fixture.

The normal matcher rule score handles specificity. A feature layer should not
replace the operation declaration; it adds a more specific matcher rule that
selects a different implementation resource.

## Terminology

Use "computed fact operation" for this feature.

Avoid "external fact producer" as the primary name. The implementation may call
external Python helpers, but the YIDL-level object is still an Astichi-backed
operation in the generated decorator.

Avoid "computed collection" as the main syntax term. The output is an ordinary
collection populated by an operation. A later slice can decide whether to add a
distinct computed-collection declaration.

Before the matcher-selected operation slice lands, update broader design docs
such as `dev-docs/YidlDesignSummary.md` to use "computed fact operation"
consistently.

## Proposed Grammar

### Operation Declaration

Extend `operation_decl`.

Current:

```lark
operation_decl: "operation" CNAME operation_io "using" resource_ref_expr operation_options?
operation_io: "inputs" "(" qname_list? ")" "outputs" "(" qname_list? ")"
```

Proposed:

```lark
operation_decl: direct_operation_decl | matcher_operation_decl
direct_operation_decl: "operation" CNAME operation_io "using" resource_ref_expr operation_options?
matcher_operation_decl: "operation" CNAME operation_from operation_io "using" "matcher" CNAME operation_options?
operation_from: "from" matcher_input
```

Direct `using ResourceName` keeps the current behavior.

`using matcher MatcherName` means:

- the named matcher must be an operation matcher
- the matcher is evaluated over the operation's one V0 `from` input
- the selected resource is run as the operation body for each selected match
  result

V0 deliberately keeps `from` exclusive to matcher-selected operations. A
direct-resource operation with a `from` clause must reject during lowering. If a
future feature needs direct per-record operations, it should get an explicit
syntax and runtime contract rather than inheriting this matcher dispatch
surface by accident.

### Matcher Kind

Extend `matcher_kind`.

Current:

```lark
matcher_kind: "->" "resource" -> matcher_kind_resource
            | "->" "contribution" -> matcher_kind_contribution
```

Proposed:

```lark
matcher_kind: "->" "resource" -> matcher_kind_resource
            | "->" "contribution" -> matcher_kind_contribution
            | "->" "operation" -> matcher_kind_operation
```

An operation matcher selects code resources. It is a separate kind for
validation and generated-runtime clarity, even though the selected payload is
still a resource.

Rule/default RHS remains `resource_ref_expr` in V0, but `match.resource()` stays
rejected inside matcher rule RHS. Operation matchers select concrete resources,
not nested matcher results.

### Computed Collection Refinement

Add a top-level filter declaration:

```lark
concept_member: ... | computed_collection_filter_decl
computed_collection_filter_decl: "filter" qname "where" condition_expr
```

The referenced `qname` must resolve to an inherited or local computed
collection. The filter's `condition_expr` uses the same value-stack condition
syntax as computed collection declarations and can only reference properties
visible on the computed collection's source record.

Lowering appends the filter condition to the referenced computed collection's
condition set. It is not a new collection and it does not replace the inherited
computed collection.

## Operation Runtime Semantics

### Operation Ordering

V0 uses the existing DDS operation/production ordering contract. Operations and
productions run in the sequence emitted by the current data-definition system
runner, and existing production groups remain the sequencing mechanism when a
concept needs an explicit group.

The default-factory proof must declare or group `BuildDefaultFactoryFacts`
before any later operation or assembly reads `DefaultFactoryDeps` or
`InitEvaluationSteps`. No new `before` or `after` operation option is added in
this plan.

### Direct Resource Operation

This remains unchanged:

```yidl
operation BuildItems inputs(Items) outputs(Items) using BuildItemsBody
```

The generated function is still shaped like:

```python
def run_build_items(builder):
    ctx = DDSOperationContext(builder, "BuildItems", ordered_inputs={...})
    astichi_hole(operation_body)
```

The resource body sees `ctx` and any names kept by the resource.

Direct-resource operations must not declare `from` in V0. A direct operation
body runs once for the whole operation and receives `ctx` only, plus any names
kept by its resource.

### Operation Execution Errors

Add a generated/runtime `OperationExecutionError` for unexpected operation body
failures. It should wrap ordinary exceptions with operation name and dispatch
tuple context while preserving the original exception as `__cause__`.
Structured decorator diagnostics such as `AssemblyDiagnosticError` are not
wrapped.

### Matcher-Selected Operation

For:

```yidl
operation BuildDefaultFactoryFacts
    from facade: Facades
    inputs(Facades, Fields)
    outputs(DefaultFactoryDeps, InitEvaluationSteps, Diagnostics)
    using matcher DefaultFactoryFactOperations
```

The generated operation should behave like:

```python
def run_build_default_factory_facts(builder):
    ctx = DDSOperationContext(builder, "BuildDefaultFactoryFacts", ordered_inputs={...})
    for facade in ctx.records(FacadesCollection):
        selected = select DefaultFactoryFactOperations for facade
        if selected is not None:
            run selected operation body with ctx and facade visible
```

This is only the semantic sketch. Slice 4 pins the V0 generated-source shape as
static body functions plus inline `if`/`elif` dispatch. The semantic contract
is:

- `from` inputs create the selection tuple.
- each selected body runs once per matched tuple.
- the body sees `ctx`.
- each `from` input name is visible as a Python local using the YIDL input name
  (`facade`, `field`, etc.).
- the selected resource must keep `ctx` and every `from` input name; missing
  keeps reject during lowering with a diagnostic naming the operation, matcher,
  resource, and missing local.
- input/output collection classes and record classes are available when listed
  in the resource `keep` set, matching current operation-resource behavior.
- writes are performed through `ctx.write(...)` or `ctx.add(...)`.

The operation `from` clause reuses the same grammar as assembly `from`, but it
does not mean "assembly value stack". In an operation, `from` creates Python
locals for the selected operation body. If a later `where` clause is added, the
condition uses the same blended value-stack name resolution as assembly, but
the operation body still receives plain Python locals.

Operation matcher selection reuses the same rule-selection algorithm as
contribution matchers: score is condition count multiplied by weight, highest
score wins, default fires only when no rule matches, and no default means no
body runs for that tuple.

If the selected resource has empty source, V0 treats it as a no-op for that
tuple. This mirrors empty-resource suppression for contributions and gives
feature concepts an explicit way to override a broad inherited operation rule
with "do nothing".

Expected user errors should be written as diagnostic records by the operation
body. Unexpected exceptions are caught by the generated dispatch wrapper and
re-raised with operation name plus the current `from` tuple context, so failures
do not surface as context-free `NameError` or `TypeError` exceptions.
Structured decorator diagnostics such as `AssemblyDiagnosticError` must pass
through unchanged.

The `ordered(...)` operation option keeps its current meaning: it controls the
order returned by `ctx.records(...)` for matching input collections. It does not
add a separate matcher dispatch ordering rule. If the `from` collection is one
of the ordered inputs, dispatch naturally follows that ordered
`ctx.records(...)` sequence.

### Input And Matcher Compatibility

For V0 matcher-selected operations:

- exactly one `from` input is supported.
- every `from` collection must also appear in `inputs(...)`.
- the operation matcher inputs must exactly match the operation `from` inputs
  by input name and collection name.
- direct `inputs(...)` collections remain the full operation read set; `from`
  is the subset used for matcher dispatch and local binding.

### No `from` Clause

If `using matcher` is used without `from`, V0 should reject it. A later slice
can define a zero-input matcher context if needed.

Direct-resource operations always omit `from` in V0.

### Multiple `from` Inputs

Post-V0 should support the same tuple semantics as assembly `from`:

- `from facade: Facades` iterates each facade row.
- `from facade: Facades, field: Fields` iterates the Cartesian product, with an
  optional `where` extension deferred unless needed.

V0 rejects multi-source `from` explicitly with a "multi-source operation from
is not implemented" diagnostic. Do not leave it ambiguous.

### Where Clause

The first useful extension is:

```yidl
operation BuildFieldFacts
    from facade: Facades, field: Fields
    where FieldOwner == ClassId
    inputs(Facades, Fields)
    outputs(...)
    using matcher FieldFactOperations
```

This should reuse value-stack condition resolution from assembly edges:

- bare names resolve through the blended value stack
- qualified input refs are not required for normal authoring
- upstream designers are responsible for avoiding name collisions

This can be V0+1 if the initial proof case only needs one `from` input.

## Operation Matcher Merge Semantics

Operation matchers merge like contribution matchers:

- inherited operation matcher rules are visible in child concepts
- child concepts may add rules
- feature concepts may add rules
- diamond inheritance dedupes the exact same inherited rule
- duplicate rule names from distinct sources reject
- duplicate defaults reject unless inherited as the exact same default
- input names merge parents-first
- duplicate input names must reference the same collection name

Rule ordering uses the existing matcher model:

- score is condition count multiplied by weight
- highest score wins
- default fires only if no rule matches

The implementation should share the contribution-matcher merge and selection
shape where possible. Operation matchers get their own spec type for type
clarity, but tie-breaking, no-match behavior, diamond dedupe, and duplicate
diagnostics should match contribution matchers.

This is important for the base/default-factory model. The base concept can
provide a broad default implementation, and feature concepts can select a more
specific implementation without replacing the base operation.

## Default Factory Proof Model

### User-Facing Python Concept

Suggested decorator name:

```python
@computedclass
class Example:
    v1: int
    v3: int = field(default_factory=lambda v2, v1: v1 + v2 + 2)
    v2: int = field(default_factory=lambda v1: v1 + 2)
```

The name `computedclass` deliberately avoids claiming strict stdlib
`dataclass` compatibility. It can still reuse the familiar `default_factory`
field option by extending its semantics:

- zero-argument factories behave like stdlib dataclass factories
- named-parameter factories are dependency-injected computed defaults
- the base dataclass-like YIDL records primitive facts and stable keys
- a feature YIDL layer computes dependency/order/diagnostic facts from those
  primitive facts

Slice 5 proves this through the existing golden-test frontend/builder style,
not by shipping a production decorator. A real `@computedclass` decorator can
be added after the YIDL operation and generated-code behavior is proven.

### Feature Layering Contract

The parameterized-`default_factory` proof must be implemented as a feature YIDL
layer over the split dataclass base, not as a rewrite of the base concept.

The base dataclass-like concept remains responsible for:

- stable facade and field identities
- field ownership and declaration order
- ordinary field/default/default-factory facts that are primitive inputs
- the normal stdlib-like zero-argument `default_factory` behavior
- extension points in the field fact shape so feature concepts can add or
  overlay more field facts without replacing the base source

The feature concept is responsible for:

- adding the parameterized-factory primitive facts that the frontend can supply
  but should not interpret
- adding derived fact collections such as `DefaultFactoryDeps` and
  `InitEvaluationSteps`
- adding the computed fact operation that inspects factory signatures and writes
  derived records
- refining named computed-collection views exposed by the base concept when a
  feature needs to narrow which source records reach inherited productions
- adding more-specific matcher rules that replace or suppress the base
  zero-argument factory handling only where the field uses named-parameter
  factory semantics
- leaving the base dataclass fixture compilable and useful on its own

The frontend requirement is intentionally small: it should provide primitive
values that cannot be derived inside YIDL, such as the factory object and stable
record identities. It should not precompute dependency edges, topological
evaluation order, or parameter diagnostics. Those are feature-layer computed
facts.

For V0, feature-specific primitive facts that are not already present in the
base field record/family should be represented with a feature-owned companion
collection keyed by `FieldId`. Current YIDL inheritance can add variants to an
inherited family, but it should not be treated as supporting new common
properties on an inherited record/family in this slice. Direct common-property
extension can be designed later if a feature needs it.

### Computed Collection Refinement

Base concepts should expose named computed collections for important production
inputs instead of applying directly over broad source collections whenever that
input set is a likely feature extension point. A feature concept can then
refine the named view without replacing the production.

For example, the base dataclass concept can define:

```yidl
computed collection InitDefaultFactoryGuardFields: Fields from Fields
    where HasDefaultFactory == True
```

and use it in the init production:

```yidl
apply default_factory_guards
    from field: InitDefaultFactoryGuardFields
    where FieldOwner == ClassId
    using DefaultFactoryGuardContributions
```

A feature concept can add a narrowing filter when the narrowing predicate is
already visible on the source record:

```yidl
filter InitDefaultFactoryGuardFields
    where FieldKind == "field"
```

The effective view is the source collection filtered by the conjunction of the
base condition and all inherited feature filters:

```text
Fields where HasDefaultFactory == True
       and FieldKind == "field"
```

V0 computed-collection refinement rules:

- refinement is monotonic: filters accumulate with `and`
- a feature may narrow a computed collection, but it may not widen it
- the collection name, source collection, record type, identity, and
  cardinality must match the inherited computed collection
- changing source/type/cardinality is a compile-time error
- duplicate inherited filters in diamonds dedupe by condition identity
- if no feature adds a filter, the base computed collection is unchanged

This requires a small YIDL merge policy addition. Today computed collections
exist, but same-name definitions are accepted only when they are identical.
This slice should add an explicit refinement surface rather than treating
different computed-collection declarations as overrides.

Computed-collection refinement is intentionally limited to facts visible on
the computed collection's source record. If a feature needs to filter by
derived data stored in another collection, it should either produce a
feature-owned work-item collection keyed with the needed values or wait for a
join-style collection/view feature.

This distinction matters for parameterized `default_factory`. Whether a factory
is zero-argument or parameterized is computed from the callable signature by
`BuildDefaultFactoryFacts`; it is not a primitive `Fields` fact. Therefore the
proof should not filter a `Fields` view by a synthetic `DefaultFactoryKind`
unless that value has deliberately been added as primitive frontend data. The
preferred proof shape is operation-derived action/work-item collections.

### Input Facts

Use the inherited dataclass-like field facts:

```yidl
property HasDefaultFactory: bool = False
property DefaultFactory: object = None
```

These already exist in the split dataclass base. The feature YIDL must not
redeclare them; it gives them additional semantics when the factory callable
has named parameters. Any new feature-specific primitive input that is not
already in the base should use a companion collection keyed by `FieldId`.

Init-only temporary values use the existing layered field-family model:

- `FieldKind == "initvar"`
- `Init == False` means the value is not supplied by the caller and must be
  computed from a default or `default_factory`
- `HasDefault == True` or `HasDefaultFactory == True`
- not stored on `self`
- visible to later init computations

### Derived Facts

Add ordinary YIDL records/collections:

```yidl
property DependencyOwner: str
property ConsumerFieldId: str
property ProviderFieldId: str
property ProviderName: str
property ParamName: str
property ParamOrder: int

record DefaultFactoryDep {
    DependencyOwner
    ConsumerFieldId
    ProviderFieldId
    ProviderName
    ParamName
    ParamOrder
}

collection DefaultFactoryDeps: DefaultFactoryDep identity (ConsumerFieldId, ParamName) many

property EvalOwner: str
property EvalFieldId: str
property EvalName: str
property EvalOrder: int

record InitEvaluationStep {
    EvalOwner
    EvalFieldId
    EvalName
    EvalOrder
}

collection InitEvaluationSteps: InitEvaluationStep identity EvalFieldId many
```

Default-factory signature classification should be represented as
operation-derived action rows:

```yidl
property ActionOwner: str
property ActionFieldId: str
property ActionFieldName: str
property ActionFieldOrder: int
property ActionKind: str                 # zero_arg | parameterized
property ActionEvalOrder: int = 0

record DefaultFactoryInitAction {
    ActionOwner
    ActionFieldId
    ActionFieldName
    ActionFieldOrder
    ActionKind
    ActionEvalOrder
}

collection DefaultFactoryInitActions:
    DefaultFactoryInitAction identity ActionFieldId many

computed collection ZeroArgDefaultFactoryActions:
    DefaultFactoryInitActions from DefaultFactoryInitActions
    where ActionKind == "zero_arg"

computed collection ParameterizedDefaultFactoryActions:
    DefaultFactoryInitActions from DefaultFactoryInitActions
    where ActionKind == "parameterized"
```

These action collections are the bridge between signature analysis and code
generation. They avoid requiring base `Fields` filters to see facts that only
exist after the computed operation runs. `ActionEvalOrder` should be populated
by `BuildDefaultFactoryFacts` and mirror the corresponding
`InitEvaluationStep.EvalOrder` for parameterized actions. For zero-argument
actions it can remain `0` because declaration order still controls the
stdlib-like guard placement.

Diagnostics should use local diagnostic rows until Slice 6 adds the converter
operation:

```yidl
property DiagnosticId: str
property DiagnosticOwner: str
property DiagnosticMessage: str
property DiagnosticOrder: int = 0

record Diagnostic {
    DiagnosticId
    DiagnosticOwner
    DiagnosticMessage
    DiagnosticOrder
}

collection Diagnostics: Diagnostic identity DiagnosticId many
```

### Computed Fact Operation

```yidl
resource DefaultFactoryFactsBody = code $[
    from inspect import Parameter, signature

    fields = [
        field for field in ctx.records(FieldsCollection)
        if field.field_owner == facade.class_id
    ]
    by_name = {field.field_name: field for field in fields}
    by_id = {field.field_id: field for field in fields}
    graph = {}
    diagnostics = []

    def diagnostic(field, suffix, message):
        diagnostics.append(
            Diagnostic(
                diagnostic_id=f"{field.field_id}.{suffix}",
                diagnostic_owner=facade.class_id,
                diagnostic_message=message,
            )
        )

    for field in fields:
        if not field.has_default_factory:
            continue
        graph.setdefault(field.field_id, set())
        for order, param in enumerate(signature(field.default_factory).parameters.values()):
            if param.kind in (Parameter.VAR_POSITIONAL, Parameter.VAR_KEYWORD):
                diagnostic(
                    field,
                    param.name,
                    (
                        f"field {field.field_name} default_factory "
                        f"has unsupported parameter {param.name!r}"
                    ),
                )
                continue
            provider = by_name.get(param.name)
            if provider is None:
                diagnostic(
                    field,
                    param.name,
                    (
                        f"field {field.field_name} default_factory "
                        f"unknown dependency {param.name!r}"
                    ),
                )
                continue
            graph[field.field_id].add(provider.field_id)
            ctx.write(
                DefaultFactoryDepsCollection,
                DefaultFactoryDep(
                    dependency_owner=facade.class_id,
                    consumer_field_id=field.field_id,
                    provider_field_id=provider.field_id,
                    provider_name=provider.field_name,
                    param_name=param.name,
                    param_order=order,
                ),
                policy=RejectDuplicate,
            )

    visiting = set()
    visited = set()
    order = []

    def visit(field_id, path):
        if field_id in visited:
            return
        if field_id in visiting:
            cycle = path[path.index(field_id):] + [field_id]
            names = " -> ".join(
                f"{facade.class_name}.{by_id[item].field_name}"
                for item in cycle
            )
            diagnostic(by_id[field_id], "cycle", f"default_factory dependency cycle: {names}")
            return
        visiting.add(field_id)
        for provider_id in sorted(graph.get(field_id, ())):
            if provider_id in graph:
                visit(provider_id, [*path, provider_id])
        visiting.remove(field_id)
        visited.add(field_id)
        order.append(field_id)

    for field_id in sorted(graph):
        visit(field_id, [field_id])

    for eval_order, field_id in enumerate(order):
        field = by_id[field_id]
        ctx.write(
            InitEvaluationStepsCollection,
            InitEvaluationStep(
                eval_owner=facade.class_id,
                eval_field_id=field.field_id,
                eval_name=field.field_name,
                eval_order=eval_order,
            ),
            policy=RejectDuplicate,
        )

    for item in diagnostics:
        ctx.write(DiagnosticsCollection, item, policy=ReplaceExisting)
]$ {
    keep ctx, facade, FieldsCollection, DefaultFactoryDepsCollection
    keep InitEvaluationStepsCollection, DiagnosticsCollection
    keep DefaultFactoryDep, InitEvaluationStep, Diagnostic
    keep Parameter, RejectDuplicate, ReplaceExisting, signature
}

matcher DefaultFactoryFactOperations(facade: Facades) -> operation {
    default -> DefaultFactoryFactsBody
}

operation BuildDefaultFactoryFacts
    from facade: Facades
    inputs(Facades, Fields)
    outputs(DefaultFactoryDeps, InitEvaluationSteps, Diagnostics)
    using matcher DefaultFactoryFactOperations
```

### Inline Algorithm Contract

For the first proof, the default-factory dependency algorithm should live
directly in the Astichi operation snippet. The snippet may import standard
library helpers such as `inspect.signature`, but it should not call a
project-local helper library.

Responsibilities of the inline operation body:

- filter fields owned by `facade`
- inspect `DefaultFactory` signatures
- reject unsupported parameter kinds
- resolve parameter names against visible init values and init-only temporary
  values
- emit dependency records
- topologically sort computed values
- emit evaluation-step records
- emit diagnostics for unknown names and cycles

If the inline body becomes too large after the proof is working, a later
refactor can extract the algorithm to a helper function without changing the
YIDL operation model. That should be treated as an implementation cleanup, not
as the first design target.

### Write Policy Convention

Use these write policies in the proof and generated examples:

- structural derived facts such as `DefaultFactoryDeps` and
  `InitEvaluationSteps` use `RejectDuplicate`; a duplicate means the operation
  emitted contradictory structure
- diagnostics use `ReplaceExisting`; rerunning an operation should converge on
  the same user-facing diagnostic rows

## Dependency And Ordering Semantics

### Visibility

A `default_factory` callable can depend on values that are visible in the init
environment:

- explicit `__init__` parameters already supplied by the caller
- fields with earlier or reordered computed defaults
- init-only fields (`FieldKind == "initvar"`) with a default or
  `default_factory`

It cannot depend on:

- classvars unless the concept explicitly exposes them as providers
- stored fields with `Init == False` and no default or `default_factory`
- unknown names

### Topological Evaluation

Prefer reordering internal evaluation over rejecting declaration-order
dependencies.

For:

```python
v1: int
v3: int = field(default_factory=lambda v2, v1: v1 + v2 + 2)
v2: int = field(default_factory=lambda v1: v1 + 2)
```

The derived order is:

1. `v1` is supplied by the caller
2. `v2` is computed from `v1`
3. `v3` is computed from `v2` and `v1`

The generated `__init__` signature can stay declaration/user order. The
generated init body uses `InitEvaluationSteps` to decide where default-factory
computations run.

### Cycle Diagnostics

Cycle detection belongs in the computed fact operation body, not in YIDL
grammar.

Example diagnostic:

```text
default_factory dependency cycle: Example.v2 -> Example.v3 -> Example.v2
```

The diagnostic should include enough identity to point back to the owning class
and field. In the YIDL output model, `DiagnosticOwner` carries the owning class
identity and `DiagnosticId` carries the field-specific identity; a later
validation operation can turn those diagnostic rows into decorator-time errors.

## Generated Init Shape

The base operation facts should drive normal YIDL assembly. A rough generated
init body for the example:

```python
def __init__(self, v1: int, v3=_HAS_DEFAULT_FACTORY, v2=_HAS_DEFAULT_FACTORY):
    if v2 is _HAS_DEFAULT_FACTORY:
        v2 = _yidl_default_factories["Example.v2"](v1=v1)
    if v3 is _HAS_DEFAULT_FACTORY:
        v3 = _yidl_default_factories["Example.v3"](v2=v2, v1=v1)
    self.v1 = v1
    self.v2 = v2
    self.v3 = v3
```

The feature reuses the existing `_yidl_default_factories` parameter mechanism
for both zero-argument and parameterized factories. The dictionary values are
the original callables; the feature decides how to call them from their
signatures and derived dependency facts. Do not introduce a parallel
`_yidl_parameterized_factories` bucket in this slice.

YIDL should not hard-code this shape. It should be assembled from facts:

- `DefaultFactoryDeps` supplies call arguments
- `InitEvaluationSteps` supplies computation order
- field matchers choose assignment/no-assignment behavior for stored fields,
  initvars, and classvars

## Implementation Plan

### Slice 1: Document Existing Operation Contract

Audit existing direct-resource operation coverage and add narrow tests only
where the contract is not already covered by DDS goldens:

- operation body receives `ctx`
- operation body can call `ctx.records(...)`
- operation body can write output records
- `astichi_pyimport(...)` works inside operation bodies

Do not spend this slice re-testing full operation success paths already owned
by materialized goldens. The goal is to create enough local safety before
changing operation parsing and runtime dispatch.

### Slice 2: Add Operation Matcher Grammar And Specs

Add parser/lowering support for:

```yidl
matcher Name(input: Collection) -> operation { ... }
```

Add a new compiled spec:

```python
@dataclass(frozen=True, slots=True)
class OperationRuleSpec:
    name: str
    condition: AssemblyConditionSpec
    resource_name: str
    weight: float


@dataclass(frozen=True, slots=True)
class OperationMatcherSpec:
    name: str
    inputs: tuple[AssemblyInputSpec, ...]
    default_resource_name: str | None
    rules: tuple[OperationRuleSpec, ...]
```

This can reuse most contribution matcher parsing/merge machinery, but should
remain a distinct spec type so generated operation source can validate and emit
it cleanly.

Validation:

- RHS must resolve to a code resource
- selected resources must be usable as operation bodies
- duplicate rule/default/input merge semantics match contribution matchers
- from-import kind `matcher` must recognize operation matchers
- empty code resources are legal operation matcher targets and mean no-op for
  the selected tuple

### Slice 3: Add Matcher-Selected Operation Declarations

Extend operation grammar with:

```yidl
operation Name from input: Collection inputs(...) outputs(...) using matcher MatcherName
```

For V0, support one `from` input.

Validation:

- `using matcher` requires an operation matcher
- matcher input set must exactly match the operation `from` input set by input
  name and collection name
- every `from` collection must also appear in `inputs(...)`
- direct `using ResourceName` remains unchanged and rejects `from` in V0
- direct operations still reject `match.resource()`
- `using matcher` without `from` rejects in V0
- generated resources selected by operation matchers must keep `ctx` and every
  `from` input name
- validate the changed Lark grammar before committing this slice

### Slice 4: Generate Operation Body Dispatch

Extend generated container runtime source so matcher-selected operations emit:

- a top-level operation runner function
- per-selected-resource body functions
- a selection loop over `ctx.records(<from collection>)`
- inline `if`/`elif` rule dispatch in descending matcher score order
- direct Python condition expressions rendered from operation matcher
  conditions
- exception wrapping that preserves structured diagnostics

Do not introduce a runtime selector helper in V0. The generated source should
be static and inspectable in goldens. A helper can be extracted later if
multiple operation matchers make the generated dispatch too repetitive.

#### Naming And Holes

Use stable operation/body indexes so generated source and Astichi holes are
deterministic:

- operation runner: existing `_operation_func_name(operation)` convention,
  e.g. `run_build_default_factory_facts`
- body hole: `operation_body_{operation_index}_{body_index}`
- body function:
  `_operation_{operation_index}_body_{body_index}_{resource_slug}`

`resource_slug` is derived from the selected resource name by stripping a
trailing `Body` suffix when present and converting the remaining PascalCase or
CamelCase name to snake_case. For example, `DefaultFactoryFactsBody` becomes
`default_factory_facts`.

`body_index` is assigned over distinct non-empty selected resources in the
operation matcher closure after diamond dedupe. The default resource and rule
resources participate in the same index sequence. Empty resources remain
selectable, but they do not get a body hole or body function.

For example:

```python
def _operation_0_body_0_default_factory_facts(ctx, facade):
    astichi_hole(operation_body_0_0)


def _operation_0_body_1_cached_default_factory_facts(ctx, facade):
    astichi_hole(operation_body_0_1)
```

The generated Astichi builder should attach each selected resource to its
matching body hole using the same pattern direct operations use today, just
with the two-part body index. Empty resources are omitted from that attachment
step.

#### Runner Shape

V0 supports exactly one `from` input, so the body function signature is always
`(ctx, <from_name>)`.

The operation runner shape should be:

```python
def run_build_default_factory_facts(builder):
    ctx = DDSOperationContext(
        builder,
        "BuildDefaultFactoryFacts",
        ordered_inputs={FacadesCollection: (ClassOrderProperty,)},
    )

    for facade in ctx.records(FacadesCollection):
        try:
            if facade.disable_default_factory_facts == True:
                pass
            elif facade.uses_cached_defaults == True:
                _operation_0_body_1_cached_default_factory_facts(ctx, facade)
            else:
                _operation_0_body_0_default_factory_facts(ctx, facade)

        except AssemblyDiagnosticError:
            raise
        except Exception as exc:
            raise OperationExecutionError(
                "operation 'BuildDefaultFactoryFacts' failed for "
                f"facade={facade!r}"
            ) from exc
```

The branch rules are:

- emit rule branches in descending score order, using the same score definition
  as contribution matchers: condition count multiplied by weight
- break equal-score ties by first-seen order across the merged concept closure
- an empty-resource rule emits `pass`, not fallthrough
- a non-empty rule calls the selected body function
- if a default resource exists, emit it as the final `else`
- if no default resource exists, either omit the final `else` or emit
  `else: pass`

#### Condition Rendering

Render operation matcher conditions directly to Python expressions in the
runner. Do not call `evaluate_condition(...)` at runtime in V0.

For the single `from` input, condition value names resolve against that input
record's storage attributes. Use the existing storage-name conversion already
used by generated records, e.g. `UsesCachedDefaults` renders as
`uses_cached_defaults`:

```yidl
rule cached when UsesCachedDefaults == True -> CachedDefaultFactoryFactsBody
```

renders as:

```python
elif facade.uses_cached_defaults == True:
    _operation_0_body_1_cached_default_factory_facts(ctx, facade)
```

The renderer should support the same condition spec shapes already used by
assembly/contribution matchers:

- `EqConditionSpec`
- `AndConditionSpec`
- `ValueRef`
- `LiteralValueRef`
- `TupleValueRef`

Missing value names should be compile-time validation errors, not generated
runtime `AttributeError`s.

#### Emitter Integration

Add a new emitter path beside the existing direct-operation emitter:

```python
def _emit_matcher_operation_lines(operation, matcher, *, operation_index, ...):
    ...
```

`_emit_aggregate_operation_lines(...)` should continue to handle direct
resource operations. The operation-emission dispatcher chooses
`_emit_matcher_operation_lines(...)` when the lowered operation spec has an
operation matcher binding, otherwise it uses the existing direct-operation
path.

#### Ordering And Context

The runner must call `ctx.records(<from_collection>)`, not raw builder access,
so existing `ordered(...)` operation options still apply. If the `from`
collection is included in `ordered_inputs`, dispatch follows that order.

The outer `run_operations(builder)` ordering remains unchanged. Matcher-selected
operations are still ordinary `OperationSpec` steps for production-group
sequencing.

`ctx` and the `from` input name must be kept names for inserted operation body
resources. Slice 3 should validate those keeps before code generation.

#### Exceptions And Imports

Generated code should preserve structured diagnostics:

- `AssemblyDiagnosticError` is re-raised unchanged
- unexpected exceptions are wrapped in `OperationExecutionError` with operation
  name and current `from` tuple context

Slice 4 must make both exception classes available in generated container
source. Define `OperationExecutionError` next to `AssemblyDiagnosticError` in
`yidl.generation.assembly_runtime`, then re-export both through
`yidl.generation.data_def_sys` so the existing
`astichi_pyimport(module=yidl.generation.data_def_sys, ...)` source prefix
remains the only runtime import style used by `container_runtime_source.py`.

### Slice 4.5: Add Computed Collection Refinement

Implement the `filter <ComputedCollection> where <Condition>` surface before
Slice 5a depends on it.

Parser/lowering work:

- add `computed_collection_filter_decl` to the Lark grammar
- lower the target `qname` to a local or inherited computed collection
- lower `condition_expr` using the same property/value condition machinery as
  computed collection declarations
- validate that referenced properties are visible on the computed collection's
  source record

Merge/runtime work:

- represent inherited filters separately enough to dedupe diamonds
- combine base computed-collection conditions and all refinement filters with
  logical `and`
- reject attempts to change source collection, record type, identity, or
  cardinality
- keep identical redefinitions accepted only when they are truly identical;
  use `filter` for refinement

Tests:

- parser accepts a simple filter declaration
- filter over inherited computed collection narrows the emitted/runtime view
- duplicate diamond filters dedupe
- wrong target kind rejects
- unknown property in filter rejects
- source/type/cardinality-changing redeclarations reject

### Slice 5a: Add Default Factory Fact Schema

Create a new feature-layer YIDL fixture that extends the split dataclass model
without editing the existing base fixture. Use a new sibling fixture directory,
for example `tests/data/yidl/yidl_update_a_computedclass_defaults/`, importing
the split dataclass base files rather than adding these files to
`tests/data/yidl/yidl_update_a_dataclasses_split/`. This avoids unrelated churn
in the existing split dataclasses golden and proves the feature is layered.

The fixture should have a shape like:

```text
tests/data/yidl/yidl_update_a_computedclass_defaults/
  computedclass_default_factory_params.yidl
  computedclass_defaults.yidl
```

`computedclass_default_factory_params.yidl` is the feature layer. It imports or
extends the dataclass base concepts and adds:

- `DefaultFactoryInitActions`
- `ZeroArgDefaultFactoryActions`
- `ParameterizedDefaultFactoryActions`
- `DefaultFactoryDeps`
- `InitEvaluationSteps`
- computed-collection refinements for default-factory init work
- diagnostic rows consumed by the Slice 6 converter operation

It uses inherited `HasDefaultFactory` and `DefaultFactory` facts from the
dataclass base. It should not redeclare those properties. If a later proof needs
additional primitive factory metadata, add it in a feature-owned companion
collection keyed by `FieldId` unless common-property extension has been
implemented by then.

The base dataclass fixture should expose named computed collections for
feature-sensitive init inputs before this slice consumes them. At minimum, base
init generation should avoid applying the default-factory guard directly over
raw `Fields`; it should apply over a named view such as
`InitDefaultFactoryGuardFields`. Feature filters over that view may use only
facts visible on `Fields`. Signature-derived classification uses
`DefaultFactoryInitActions` and its derived action views instead.

`computedclass_defaults.yidl` is the combined proof concept. It imports the
feature layer and any required base dataclass layers, then exposes the final
assembly used by the golden. The existing dataclass base/split fixtures should
continue to compile and generate their current output independently.

This slice should compile and emit the generated decorator/runtime source, but
does not need to run the computed operation yet.

### Slice 5b: Add Default Factory Fact Operation

Add `BuildDefaultFactoryFacts` inside
`computedclass_default_factory_params.yidl`, not in the dataclass base, and
prove it writes derived facts:

- one `DefaultFactoryInitAction` row for each factory field
- `ActionKind == "zero_arg"` for factories with no signature parameters
- `ActionKind == "parameterized"` for factories with named parameters
- `ActionEvalOrder` populated for parameterized factory actions
- dependency rows for named factory parameters
- evaluation-step rows in topological order
- diagnostics rows for unknown dependencies and unsupported parameter kinds

This slice should test the operation at the fact level. It should not yet
require generated `__init__` to consume the facts.

### Slice 5c: Consume Computed Facts In Init Generation

Rewire init generation so generated `__init__` consumes
`DefaultFactoryInitActions`, `DefaultFactoryDeps`, and `InitEvaluationSteps`.
Prefer computed-collection refinement plus feature-owned action/work-item
collections over replacing the inherited init production. The base dataclass
concept should keep its stdlib-like behavior for ordinary fields and
zero-argument factories.

The first success fixture should prove:

```python
v1: int
v3: int = field(default_factory=lambda v2, v1: v1 + v2 + 2)
v2: int = field(default_factory=lambda v1: v1 + 2)
```

Expected runtime behavior:

- `Example(10).v2 == 12`
- `Example(10).v3 == 24`
- generated source evaluates `v2` before `v3`
- public field metadata remains declaration order unless the concept says
  otherwise

The proof fixture must sequence `BuildDefaultFactoryFacts` before any operation
or assembly that consumes `DefaultFactoryDeps` or `InitEvaluationSteps`.

The expected YIDL rewiring shape is:

- use `ZeroArgDefaultFactoryActions` for inherited/stdlib-like zero-argument
  factory guards
- use `ParameterizedDefaultFactoryActions` and `InitEvaluationSteps` for
  parameterized factory evaluation
- add a `DefaultFactoryEval` resource that emits
  `field_name = _yidl_default_factories["Owner.field"](call_args...)` guarded
  by `_HAS_DEFAULT_FACTORY`
- add a `DefaultFactoryEvalContribution` targeting the init method body and
  ordered by `EvalOrder`
- add call-argument contributions driven by `DefaultFactoryDeps`, ordered by
  `ParamOrder`
- add a matcher over `InitEvaluationSteps` to select evaluation contributions
- update inherited init assignment behavior so fields with named-parameter
  factories are computed before assignment, while stored/initvar/classvar
  assignment policy still comes from the field-kind matchers
- add skip or replacement rules only for the parameterized factory cases that
  the feature owns; broad base rules should remain broad so later features can
  layer on the same mechanism

Replacing the whole inherited init production should be treated as a fallback,
not the preferred proof shape. If an inherited production cannot consume the
action views cleanly, first prefer adding a narrow base extension point or
feature-owned work-item collection before replacing the production.

This is intentionally separate from Slice 5b: 5b proves the derived facts, and
5c proves generated code consumes them correctly.

### Slice 6: Diagnostics

Add failure fixtures:

- unknown dependency name
- unsupported callable parameter kind
- cycle between computed defaults
- `FieldKind == "initvar"` and `Init == False` without default or
  `default_factory`
- duplicate dependency records

The diagnostics should be generated by YIDL resources or by the computed fact
operation writing diagnostic rows. For V0, Slice 5b may leave diagnostics as
rows only. Slice 6 owns the new converter operation that reads those rows and
raises `AssemblyDiagnosticError` at decorator/build time; there is no existing
diagnostic-row converter to reuse.

Do not let raw inline-operation exceptions leak as the final decorator error
unless the generated dispatch wrapper has wrapped the exception with operation
name and current `from` tuple context.

### Slice 7: Multi-Source And Where

If needed after the first proof, add:

```yidl
operation Name
    from facade: Facades, field: Fields
    where FieldOwner == ClassId
    inputs(...)
    outputs(...)
    using matcher MatcherName
```

This should reuse assembly value-stack and condition semantics.

## Test Strategy

Use golden tests for successful end-to-end behavior:

- a separate feature YIDL file layered over the dataclass base
- a combined proof YIDL file that imports/extends the feature layer
- generated decorator source
- generated decorator prettier source
- generated output source
- generated output prettier source
- runtime behavior of generated class

The golden should make the layering visible in the source fixture. The base
dataclass YIDL should remain independently compilable, while the computed-class
fixture proves the feature layer can add primitive field facts, derived
collections, operations, and matcher overrides without changing the base file.

Use focused parser/compiler tests for:

- grammar acceptance
- computed-collection filter/refinement acceptance
- computed-collection refinement rejects source/type/cardinality changes
- computed-collection refinement dedupes inherited diamond filters
- invalid `using matcher`
- wrong matcher kind
- missing matcher
- duplicate operation matcher rule
- inherited operation matcher merge
- unsupported multi-source `from` if deferred

Use focused operation-algorithm tests for graph behavior:

- topological order
- cycle detection
- unknown parameter names
- allowed init-only temporary providers

These focused tests should invoke the operation against synthetic collections
and assert derived facts. End-to-end runtime behavior such as
`Example(10).v3 == 24` belongs in the golden fixture, not in duplicate bespoke
tests.

Do not duplicate full success assertions between bespoke tests and goldens. The
golden should own success-path source shape.

## Non-Goals

This plan does not add a YIDL graph algorithm language.

This plan does not make `default_factory` a core YIDL keyword.

This plan does not require operation bodies to be named Python functions in
YIDL syntax. The first proof keeps the default-factory algorithm inline in an
Astichi snippet. Later concepts may still call Python helpers from snippets when
the algorithm is large enough to justify extraction.

This plan does not replace the existing direct-resource operation surface.

This plan does not define a full stdlib-compatible dataclass replacement.
`computedclass` deliberately diverges from `dataclass`.

## Deferred Questions

The following questions are intentionally deferred. V0 decisions are stated in
the body of this plan.

### Zero-Input Operation Matchers

Should `using matcher` support no `from` clause by evaluating a matcher once
against an empty tuple?

Recommendation: reject in V0. Add only when a real fixture needs it.

### Existing Operation Options

The current `diagnostics` operation option is parsed but not implemented. This
plan should not depend on it. A later diagnostics slice can connect operation
output diagnostics to decorator-time errors.

### Evaluation Order And Signature Order

Should `InitEvaluationSteps` affect only body computation order, or also
generated `__init__` parameter order?

Recommendation: body computation order only. Signature order should remain a
separate dataclass/decorator policy.
