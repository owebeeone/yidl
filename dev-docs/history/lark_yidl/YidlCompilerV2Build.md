# YIDL Lark Compiler V2 Build Slices

## Goal

Implement the Lark-backed YIDL compiler V2 in narrow vertical slices. The first
priority is resource syntax, resource lowering, and resource flow because that
is the highest-risk part of the compiler and the foundation for matchers,
productions, and operations.

This document is an implementation sequence. Broader architecture and feature
motivation live in `dev-docs/YidlArchitecturePosition.md` and
`dev-docs/lark_yidl/YidlCompilerV2Plan.md`.

## Build Rule

Each slice should land with:

- focused tests first
- implementation scoped to the slice
- diagnostics for unsupported follow-on surfaces
- no changes to the older indentation parser unless deliberately shared
- no lifecycle-specific shortcuts in the Lark compiler core

## Slice 1: Snippet Lexing And Parse Shape

### Goal

Teach the Lark grammar to accept canonical V2 resource syntax. Lowering may
still reject unsupported members after parse shape is proven.

### Syntax

````yidl
resource R = code `lambda s: s + 1`

resource R = code $[
def f():
    return 1
]$ {
    keep f
}

resource T = template ```python
def f():
    return 1
``` {
    edge keep_names = KeepNamesResource
}
````

Supported snippet forms:

- escaped string literal
- inline single backticks
- `$(`...`)$`
- `$[`...`]$`
- triple backtick fence without a language tag
- triple backtick fence with a language tag such as `python`

### Tests

Add focused parser tests for:

- inline backtick snippets
- `$(` and `$[` inline snippets
- `$(` and `$[` block snippets
- triple backtick snippets with and without `python`
- `#` inside snippets is preserved as snippet text, not a YIDL comment
- snippet option block parses `keep`
- snippet option block parses `edge arg_names`, `edge bind`, and
  `edge keep_names`
- unterminated snippets produce the clearest practical syntax error

## Slice 2: Code Resource Lowering

### Goal

Lower:

```yidl
resource R = code <snippet> { keep Name, Other }
```

to:

```python
from_astichi_code(
    source,
    file_name=...,
    line_number=...,
    offset=...,
    keep_names=(...),
)
```

### Implementation

- add `_local_resources` to the concept compiler
- lower `code` resource declarations into generated values
- preserve source text
- preserve `file_name`, `line_number`, and `offset`
- lower static `keep` names to `keep_names`
- keep old `astichi_code` unsupported unless an explicit alias is cheaper than
  rejecting it cleanly

### Tests

Add focused compiler tests for:

- source text preservation
- dedent/strip behavior through `from_astichi_code(...)`
- keep names preservation
- generated value `to_generator()` compiles
- source metadata is sane for inline and block snippets
- empty snippet reports the resource name

## Slice 3: Template Resource Lowering

### Goal

Lower:

```yidl
resource T = template <snippet> {
    keep StaticName
    edge arg_names = ArgNamesResource
    edge bind = BindResource
    edge keep_names = KeepNamesResource
}
```

to:

```python
astichi_template(
    from_astichi_code(source, keep_names=(...)),
    arg_names=ArgNamesResource,
    bind=BindResource,
    keep_names=KeepNamesResource,
)
```

### Implementation

- lower template source through `from_astichi_code(...)`
- lower static `keep` names on the template source
- resolve `edge arg_names`, `edge bind`, and `edge keep_names` to generated
  resources
- reject unknown edge names
- reject edge targets that are not generated resources
- keep old `astichi_template` unsupported unless an explicit alias is cheap

### Tests

Add focused compiler tests for:

- template without edges
- template with static `keep`
- template with `arg_names`
- template with `bind`
- template with resource-valued `keep_names`
- unknown edge resource diagnostic
- invalid edge target diagnostic

## Slice 4: Resource Expression Lowering

### Goal

Introduce a resource-expression lowerer so resource-consuming grammar surfaces
do not special-case named resource references.

### Implementation

Support:

- declared resource references
- imported resource references, where current import support is sufficient
- wrong-kind rejection
- matcher-selected resources only in contexts where matcher results exist

Keep this separate from general value-expression lowering so resource consumer
sites can reject non-resource values cleanly.

### Tests

Add focused tests for:

- direct resource expression
- imported resource expression
- unknown resource diagnostic
- wrong-kind symbol diagnostic
- `match.resource()` rejected outside matcher-result context

## Slice 5: Matcher Lowering

### Goal

Lower matcher rules that select resources.

### Syntax

```yidl
matcher PropertyTemplate(field: Fields) {
    default -> PlainGetter
    rule managed when field.Kind == "managed" -> ManagedGetter
    rule weighted when field.Kind == "owned" -> OwnedGetter weight 10
}
```

### Implementation

- resolve matcher input collections
- lower matcher inputs
- resolve default and rule targets through the resource-expression lowerer in
  selector-target mode
- lower rule conditions
- preserve rule names and weights
- reject `match.resource()` as a matcher rule target

### Tests

Add focused tests for:

- input collection resolution
- default resource resolution
- rule resource resolution
- rule condition lowering
- weighted rules
- undefined resource diagnostic
- undefined matcher input property diagnostic
- `match.resource()` rejected as a selector target

## Slice 6: Matcher-Result Production

### Goal

Allow matcher-selected resources to flow into records.

### Syntax

```yidl
production ToComponents from PropertyTemplate.results() to Components {
    identity match.record("field").Name
    set Name = match.record("field").Name
    set Template = match.resource()
}
```

### Implementation

- lower matcher-result sources
- lower `match.resource()` as a resource-valued production expression
- lower `match.record("input").Property`
- lower identity expressions
- lower write policy if already needed by the target golden
- require target collection to accept the assigned properties

### Tests

Add focused tests for:

- matcher-result production source
- `match.resource()` assignment
- `match.record("field").Property` assignment
- identity expression lowering
- missing target value diagnostics
- invalid matcher input name diagnostics

## Slice 7: Operation Resource Consumption

### Goal

Prove that operation resource consumers are not named-resource-only.

### Syntax

```yidl
operation BuildClass
inputs(Fields, Components)
outputs(GeneratedClasses)
using BuildClassResource {
    ordered(SourceOrder)
}
```

### Implementation

- lower operation `using` through the resource-expression lowerer
- support direct resource references
- support resource-valued records where the runtime operation model already
  consumes them
- lower ordered input properties
- keep diagnostics option unsupported unless needed by the vertical golden

### Tests

Add focused tests for:

- operation using a direct resource
- operation resource-expression resolution
- ordered property validation
- resource-valued records produced by matcher-result production and consumed by
  an operation
- diagnostics option unsupported diagnostic

## Slice 8: Golden Vertical

### Goal

Prove the V2 compiler with one complete `.yidl` case equivalent to an existing
Python builder golden.

### Required Shape

The case should include:

- properties
- schema family and variants
- collection
- `code` resources
- `template` resource with edge resources
- matcher
- production from matcher results
- emitted runtime source
- runtime validation through generated builder/container

### Tests

Add a golden under `tests/data/gold_src/` and route it through the existing
golden harness.

Validation should execute emitted source and assert runtime behavior, not only
string contents.

## Deferred Until After Slice 8

Defer these until the resource-flow vertical is proven:

- direct `record` lowering if not needed by the vertical
- direct `union` lowering
- computed collections
- ports beyond what is required by the vertical
- diagnostics declaration lowering
- strict export enforcement
- selective `from "...yidl" import ...` support
- CLI/disk-backed compilation

## Rationale

The unique V2 risk is resource syntax and flow:

```text
resource declaration
-> matcher selection
-> production storage
-> operation consumption
```

Records, ports, computed collections, diagnostics, and CLI support are
important, but they are less central to proving the new architecture. Build the
resource-flow spine first.
