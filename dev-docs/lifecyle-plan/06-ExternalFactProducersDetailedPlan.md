# External Fact Producers Detailed Plan

## Goal

Convert facts derived from Python objects into DDS records without embedding
Python introspection logic in DDS core.

Critical review status: `dds.fact_producer(...)` is not a V1 DDS-core API. Fact
producers lower to `dds.operation(...)` with declared inputs, declared outputs,
and a generated analyzer resource.

This feature is needed for:

- callable signature analysis
- annotation shape analysis
- harvested MRO layer data
- helper argument normalization
- later resource-policy inspection

## Problem

Lifecycle decisions depend on Python objects:

- a hook callable's accepted parameter names
- whether an annotation is mapping-like
- which base classes already carry generated field metadata
- whether a default factory consumes initvars

DDS should not know how to call `inspect.signature` or parse typing objects.
However, the results of those analyses must become records so matchers and
productions can use them.

## Operation-First API

V1 should use generated operations with source-emittable analyzer resources.
Only add a public `fact_producer(...)` helper if multiple analyzers converge on
the same shape.

### Generated Operation API

```python
dds.operation(
    "ProduceCallableFacts",
    inputs=(CallableDeclarations,),
    outputs=(CallableSpecs, CallableParams, CallableInjections),
    resource=CallableAnalyzer,
)
```

Optional concept-layer helper:

```python
concept.operations.fact_producer(
    "CallableFacts",
    source=CallableDeclarations,
    outputs=(CallableSpecs, CallableParams, CallableInjections),
    resource=CallableAnalyzer,
)
```

The helper must lower to `dds.operation(...)`. Do not add
`dds.fact_producer(...)` as a V1 DDS-core API.

## Callable Fact Records

```python
CallableDeclaration = dds.record(
    "CallableDeclaration",
    Name,
    SourceLabel,
    CallableObject,
    CallableRole,
)

CallableSpec = dds.record(
    "CallableSpec",
    Name,
    SourceLabel,
    CallableRole,
    AcceptsVarArgs,
    AcceptsVarKwargs,
)

CallableParam = dds.record(
    "CallableParam",
    CallableName,
    ParamName,
    ParamKind,
    ParamOrder,
)

CallableInjection = dds.record(
    "CallableInjection",
    CallableName,
    ParamName,
    InjectionKind,
    Required,
)
```

The callable analyzer should reject `*args` and `**kwargs` for lifecycle
callable injection unless a future design explicitly supports them.

## Annotation Shape Records

Do not implement annotation shape analysis until binding/owned mapping support
is the next blocker. When needed, use records:

```python
AnnotationShape = dds.record(
    "AnnotationShape",
    FieldName,
    IsMapping,
    IsSequence,
    KeyType,
    ValueType,
    ElementType,
)
```

This keeps annotation analysis out of the binding/owned code generator.

## Analyzer Resource Shape

An analyzer is a generated resource that emits a function or imported helper.

```python
CallableAnalyzer = from_astichi_code(
    """
    astichi_pyimport(module="inspect", names=("signature",))

    def analyze_callable(name, source_label, role, callable_obj):
        sig = signature(callable_obj)
        ...
        return callable_spec, callable_params, callable_injections
    """
)
```

If the analyzer is a library helper:

```python
CallableAnalyzer = from_import(
    "yidl.generation.lifecycle_facts",
    "analyze_callable",
)
```

The second option is better for complex introspection. The generated source then
contains an import, not a huge analyzer body.

## Expected Use Case

Commit validator:

```python
builder.add(
    CallableDeclaration(
        name="validate_default",
        source_label="Example.validate_default",
        callable_role=COMMIT_VALIDATOR,
        callable_object=validate_default,
    )
)
```

Generated operation:

```python
ProduceCallableFacts.run(builder)
```

Result:

```python
CallableParam(
    callable_name="validate_default",
    param_name="current",
    param_kind=POSITIONAL_OR_KEYWORD,
    param_order=0,
)

CallableInjection(
    callable_name="validate_default",
    param_name="current",
    injection_kind=CURRENT_FACADE,
    required=True,
)
```

Later matcher:

```python
CallableRunnerTemplate.rule.current_only(
    when=(callable_fact.prop(InjectionSignature).eq(CURRENT_ONLY),),
    resource=CurrentOnlyRunnerTemplate,
)
```

## Expected Generated Source Golden

Expected excerpt for
`tests/data/goldens/materialized/dds_lifecycle_callable_facts.py`:

```python
from yidl.generation.lifecycle_facts import analyze_callable


def produce_callable_facts(ctx):
    for declaration in ctx.records(CallableDeclarationsCollection):
        result = analyze_callable(
            name=declaration.name,
            source_label=declaration.source_label,
            role=declaration.callable_role,
            callable_obj=declaration.callable_object,
        )
        ctx.write(
            CallableSpecsCollection,
            result.spec,
            policy=ReplaceExisting,
        )
        for param in result.params:
            ctx.write(
                CallableParamsCollection,
                param,
                policy=RejectDuplicate,
            )
        for injection in result.injections:
            ctx.write(
                CallableInjectionsCollection,
                injection,
                policy=RejectDuplicate,
            )


def run_operations(ctx):
    produce_callable_facts(ctx)
    return ctx.freeze()
```

The golden must prove:

- analyzer is imported or emitted once
- analyzer output is normal DDS records
- downstream code does not inspect signatures directly
- no dependency on `pyrolyze`

## Diagnostics

Callable analyzer diagnostics:

- unsupported `*args`
- unsupported `**kwargs`
- unknown injection parameter
- duplicate parameter names
- positional-only parameter where not allowed
- callable is not callable

Annotation analyzer diagnostics:

- unsupported annotation form
- mapping missing key/value type when required
- field helper requires mapping but annotation is scalar

The analyzer can either raise direct user diagnostics or emit diagnostic records.
For V1 callable analysis, direct errors are acceptable if the message includes
callable name and source label.

## Implementation Notes

Do not put `inspect.signature` or typing-shape logic into DDS core. DDS only
knows that a generated operation reads records and writes records.

Potential implementation path:

1. Add generic generated operation resource support if not already available.
2. Implement callable analyzer as a library helper.
3. Add generated operation that calls the helper and writes output records.
4. Add matchers over the output records.

## Test Plan

Bespoke:

- `test_callable_fact_producer_rejects_varargs`
- `test_callable_fact_producer_rejects_unknown_injection_name`
- `test_callable_fact_producer_emits_param_records`
- `test_callable_fact_producer_emits_injection_records`

Goldens:

- `tests/data/gold_src/dds_lifecycle_callable_facts.py`
- `tests/data/goldens/materialized/dds_lifecycle_callable_facts.py`

The golden should include:

- callable accepting `current`
- callable accepting `working` and `tx_group`
- default factory accepting an initvar
- generated matcher selecting a runner template based on produced facts
