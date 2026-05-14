# YIDL Lark Compiler V2 Plan

## Goal

Implement and test lowering for the Lark-backed `.yidl` compiler so concept
modules can define generated resources, matchers, productions, operations, and
snippet-backed Astichi stitching through the same recorded concept plan path
used by the existing hand-authored builder tests.

This plan is for `src/yidl/concept_grammar.lark` and
`src/yidl/concept_parser.py`. It does not replace the older indentation-based
transducer parser in `src/yidl/parser.py`.

## Current State

The Lark grammar already accepts the syntax for:

- `resource` declarations with `literal`, `import`, `astichi_code`, and
  `astichi_template` forms
- `matcher` declarations with inputs, defaults, rules, conditions, and weights
- `production` declarations from collections or matcher results
- `operation` declarations with input/output collections and resources
- `computed collection`, `port`, and `diagnostics` declarations
- value expressions such as `source.Name`, `match.resource()`,
  `match.record("field").Name`, `match.value(0)`, `lookup(...)`,
  `Port.of(...)`, and tuples

The compiler currently lowers only:

- concept imports and `extends`
- `property`
- `family` and family variants
- `collection`

Every other concept member is recognized by the grammar but rejected by the
compiler with `lowering is not implemented yet`.

V2 should replace author-facing `astichi_code` and `astichi_template` keywords
with `code` and `template`. `from_astichi_code(...)` and
`astichi_template(...)` remain the internal Python helper names. If the old
grammar spellings remain accepted during migration, they should be treated as
compatibility aliases, not canonical YIDL syntax.

## Non-Goals

1. Do not add arbitrary Python execution at YIDL definition time.
2. Do not make the Lark grammar indentation-sensitive.
3. Do not move lifecycle/transducer `%%` behavior snippets into the Lark path.
4. Do not introduce a second resource model separate from
   `from_astichi_code(...)`, `astichi_template(...)`, `from_import(...)`, and
   `from_literal(...)`.
5. Do not expose generated slot names or `_y_*` internals in YIDL source.

## Compiler Model

The V2 compiler should lower each parsed concept into a recorded
`CapsuleConceptPlan`.

The Lark compiler should maintain per-concept symbol tables for:

- properties
- records
- schema families
- collections
- computed collections
- ports
- resources
- matchers
- productions
- operations

Names should resolve in this order where applicable:

1. local concept definitions
2. extended concept definitions
3. imported module aliases

Imported references should remain alias-qualified in source, such as
`core.Name` or `core.LifecycleCore`. Do not infer across all imports unless the
grammar explicitly asks for an alias or a `use` surface.

## Resource Flow Rule

Every place that consumes a generated resource should consume a resource
expression, not a special-case named-resource-only reference.

Resource expressions include:

- a declared resource name, such as `PlainGetter`
- an imported resource name, such as `core.PlainGetter`
- a matcher-selected resource, such as `match.resource()`, when the surrounding
  grammar is in a matcher-result context
- a resource-valued property read, when a prior production stored
  `match.resource()` into a collection record

This does not mean matcher rule targets are dynamic. A matcher rule still points
at a declared/imported resource because the matcher is the selector. The rule
target is the value being selected, not a consumer of an already-selected
resource.

The important rule is downstream uniformity: once a grammar surface says it
needs a resource, it should be possible to feed that resource from a matcher
result through the normal dataflow path, rather than needing a separate
matcher-specific API.

## Phase 1: Resource Lowering

### Scope

Lower:

```text
resource Name = literal <value_expr>
resource Name = import "module.path".Symbol
resource Name = code <snippet> resource_options?
resource Name = template <snippet> resource_options?
```

Snippet literals support these forms:

````text
"escaped one-line source"
$(raw source)$
$[raw source]$
`inline raw source`
```
raw block source
```
```python
raw block source
```
````

The `$(`...`)$` and `$[`...`]$` delimiters are interchangeable. They may be
single-line or multi-line. Backtick forms are also supported for authoring
ergonomics: single backticks are inline-only, and triple-backtick fences are
multi-line blocks with an optional language tag such as `python`.

````text
resource Inc = code $(lambda s: s + 1)$

resource AlsoInc = code `lambda s: s + 1`

resource UsesRuntimeName = code $[
def get(self):
    return _NO_WORKING_VALUE
]$ {
    keep _NO_WORKING_VALUE
}

resource ManagedTemplateKeepNames = code $(("_NO_WORKING_VALUE",))$

resource ManagedTemplate = template $[
def get(self):
    return _NO_WORKING_VALUE
]$ {
    keep _NO_WORKING_VALUE
    edge keep_names = ManagedTemplateKeepNames
}

resource Getter = code $[
def get(self):
    """Docstrings are fine inside raw snippets."""
    return self.value
]$

resource Getter = code $(
def get(self):
    """This delimiter form is also valid."""
    return self.value
)$

resource BacktickGetter = code ```python
def get(self):
    return self.value
```
````

Raw snippet bodies do not perform escape processing. For multi-line snippets,
the closing delimiter should appear alone on a line after optional whitespace.
The captured body excludes the delimiters and any triple-backtick language tag,
then is passed to the existing generated-value helpers, which dedent and strip
the source.

Snippet compile inputs must be preserved. The lowerer should pass these inputs
to each `from_astichi_code(...)` call it creates:

- `file_name`: the `.yidl` path being compiled
- `line_number`: the first authored source line inside the snippet body
- `offset`: the column where a single-line snippet body starts, otherwise `0`
- static `keep_names`: names that Astichi must preserve while compiling that
  specific snippet

`file_name`, `line_number`, and `offset` are compiler-supplied source metadata.
Static `keep_names` is author-supplied compile metadata written as `keep ...`
inside the resource option block.

`astichi_template(...)` also has resource-valued edge options. Its
`arg_names=...`, `bind=...`, and `keep_names=...` options must resolve to other
generated resources, not to inline literal lists. This matches the existing
`astichi_template(template, *, arg_names=..., bind=..., keep_names=...)` API,
where each edge option is a `MatcherGeneratedValue` that can be evaluated per
record.

The first implementation should support:

- `code <snippet> { keep Name, Other }` for static compile keeps
- `template <snippet> { keep Name edge keep_names = KeepResource }` for a
  template with both static source keeps and resource-valued edge keeps
- `template <snippet> { edge arg_names = ArgNamesResource edge bind =
  BindResource edge keep_names = KeepNamesResource }` for the full template
  edge surface

Names in static keep lists are Python identifiers and lower to strings. Names
assigned to template edge options are YIDL resource references.

### Design

1. Add `_local_resources` to `_ConceptCompiler`.
2. Add resource handles to `YidlCompiledConcept` if the recorded builder already
   has an appropriate resource handle type; otherwise store generated values in
   the compiler-local resource table only until the recorded builder needs a
   stable public handle.
3. Map resource expressions to existing generated-value constructors:
   1. `literal` -> `from_literal(value)` for generated resources, or raw literal
      only when the consuming API requires a plain value.
   2. `import "pkg.mod".Name` -> `from_import("pkg.mod", "Name")`.
   3. `code <snippet> resource_options?` ->
      `from_astichi_code(..., keep_names=(...))`.
   4. `template <snippet> resource_options?` ->
      `astichi_template(from_astichi_code(..., keep_names=static_keep_names),
      arg_names=<resource>, bind=<resource>, keep_names=<resource>)`.
   5. `astichi_code <snippet> resource_options?`, if retained, ->
      deprecated alias for `code <snippet> resource_options?`.
   6. `astichi_template <snippet> resource_options?`, if retained, ->
      deprecated alias for `template <snippet> resource_options?`.
4. Preserve source metadata using `file_name`, `line_number`, and `offset`.
   For quoted strings and single-line raw snippets, `offset` should point at
   the first character of authored snippet text. For multi-line raw snippets,
   `line_number` should point at the first body line and `offset` should be
   `0`.
5. Preserve static `keep` names from resource option blocks when constructing
   `from_astichi_code(...)` values.
6. Resolve resource-valued template edge options, including `keep_names`, to
   generated resources before calling `astichi_template(...)`.
7. Reject empty Astichi source through the existing generated-value helper.

### Tests

Add focused tests in `tests/generation/test_yidl_lark_parser.py`:

- resource literal lowers to a generated literal value
- resource import lowers to an imported generated value
- resource `code` lowers to a value whose `to_generator()` compiles
- raw `$(...)$` and `$[...]$` snippets preserve source and compile
- generated values preserve `file_name`, `line_number`, `offset`, and explicit
  `keep` resource options
- resource `template` lowers to an `AstichiTemplateValue`
- template `keep_names=SomeResource` resolves to
  `astichi_template(..., keep_names=SomeResource)`
- static `keep ...` remains on the template's
  `from_astichi_code(...)` value and does not replace the resource-valued
  template `keep_names`
- empty Astichi resource reports a symbol error with the resource name

Add a golden case under `tests/data/gold_src/` only after the resource can be
consumed by a matcher or operation. Avoid a standalone golden that only
duplicates the focused resource assertions.

## Phase 2: Record, Union, Port, And Computed Collection Lowering

### Scope

Lower the grammar surfaces that complete the basic DDS shape:

```text
record Field { Name Kind }
union FieldSpecs { variant PlainField { Name Kind } }
computed collection ManagedFields: Fields from Fields where source.Kind == "managed"
port ClassBody "class-body" many
```

### Design

1. Lower `record` to `builder.records.<Name>(...)`.
2. Lower `union` to the recorded schema-family/union mechanism only if the
   builder has a direct union surface. If not, keep `family` as the canonical
   user-facing union surface and reject `union` with a precise diagnostic until
   a direct recorded API exists.
3. Lower `computed collection` to `builder.computed_collections.<Name>(...)`.
4. Lower `port` to `builder.ports.<Name>(cardinality=...)`.
5. Teach symbol resolution to distinguish concrete collections from computed
   collections.
6. Preserve current behavior that collection identity in the compiler slice is
   single-property only unless composite identity lowering is explicitly added.

### Tests

Focused tests:

- record property resolution, including inherited properties
- computed collection condition lowering from `source.Property == literal`
- port cardinality lowering for `single` and `many`
- unsupported direct `union` behavior if no builder API exists
- composite identity either lowers correctly or gives a local unsupported
  diagnostic

Golden tests:

- one `.yidl` source that defines a base collection plus a computed collection
  and emits runtime source matching the existing DDS runtime style
- one `.yidl` source with ports if port runtime source is already covered by
  existing goldens

## Phase 3: Value Expression Lowering

### Scope

Implement typed expression lowerers for value expressions and resource
expressions.

Value expressions:

- literals
- qualified names
- `source.Property`
- `match.resource()`
- `match.record("input").Property`
- `match.value(index)`
- `lookup(collection, key=..., value=Property, default=...)`
- `Port.of(value)`
- tuples
- equality conditions joined by `and`

Resource expressions:

- declared resource references
- imported resource references
- `match.resource()` in matcher-result production contexts
- resource-valued property reads from source records

### Design

1. Introduce small dataclasses for parser-lowered expression intent if direct
   lowering from Lark trees becomes hard to test.
2. Keep condition lowering separate from value lowering:
   1. conditions must lower to property equality handles or matcher conditions
   2. values must lower to recorded value expressions
3. Require every property referenced by `source.Property` to exist on the
   relevant source collection shape.
4. Require matcher record names in `match.record("name")` to match declared
   matcher input names.
5. Require tuple elements to be individually lowerable.
6. Keep resource-expression lowering separate from general value-expression
   lowering so type checks can reject non-resource values at resource consumer
   sites.
7. Make unsupported expressions fail with the grammar surface name and source
   reference rather than a generic tree error.

### Tests

Focused tests:

- each value expression lowers to the expected recorded value expression
- `and` condition preserves all equality terms
- unknown source property reports the property name
- unknown matcher input reports the input name
- invalid `match.value(-1)` remains syntax-invalid or symbol-invalid with a
  stable diagnostic
- resource consumer sites accept direct resources and matcher-selected
  resources when the surrounding context provides a matcher result
- resource consumer sites reject non-resource expressions with a local
  diagnostic

## Phase 4: Matcher Lowering

### Scope

Lower:

```text
matcher PropertyTemplate(field: Fields) {
    default -> PlainGetter
    rule managed when field.Kind == "managed" -> ManagedGetter weight 10
}
```

### Design

1. Resolve matcher input collection names.
2. Lower inputs through `builder.matchers.<Name>().input.<input_name>(...)`.
3. Resolve default and rule resources through the resource-expression lowerer
   in selector-target mode: declared and imported resources are valid, but
   `match.resource()` is not, because this matcher is the selector producing
   the match result.
4. Lower rule conditions using matcher input property references.
5. Preserve rule names and weights.
6. Store matcher handles in `_local_matchers` for productions.

### Tests

Focused tests:

- matcher input collection resolution
- default resource resolution
- rule condition lowering
- weighted rule lowering
- undefined resource diagnostic
- undefined matcher input property diagnostic

Golden tests:

- Lark `.yidl` equivalent of the existing matcher runtime golden, using
  `code` resources instead of Python builder calls

## Phase 5: Production Lowering

### Scope

Lower:

```text
production PropertyTemplateToClassBody
from PropertyTemplate.results() ordered(Name)
to ClassComponents {
    identity match.record("field").Name
    policy ReplaceExisting
    set Name = match.record("field").Name
    set Template = match.resource()
}
```

### Design

1. Support collection sources and matcher-result sources.
2. Resolve `ordered(...)` properties against the source record shape.
3. Resolve target collection and require it to be concrete.
4. Resolve write policy names to existing policy objects.
5. Lower `identity` and `set` value expressions through the Phase 3 lowerer.
6. Store production handles in `_local_productions` for operation grouping if
   grouping is added later.

### Tests

Focused tests:

- collection-source production
- matcher-result production
- identity expression lowering
- value assignment lowering
- policy resolution for `RejectDuplicate`, `ReplaceExisting`, and `AddIfAbsent`
- missing required target values reports all missing names
- matcher-result productions reject `where` conditions if the runtime API does
  not support them

Golden tests:

- Lark `.yidl` equivalent of an existing matcher-production golden
- verify emitted runtime source reconstructs resources before properties that
  reference them

## Phase 6: Operation Lowering

### Scope

Lower:

```text
operation BuildClass
inputs(Fields, ClassComponents)
outputs(GeneratedClasses)
using BuildClassResource {
    ordered(SourceOrder)
}
```

### Design

1. Resolve input collections and computed collections.
2. Resolve output collections as concrete collections.
3. Resolve operation `using` through the resource-expression lowerer, not by a
   named-resource-only lookup. A direct operation body is a normal resource
   reference; a data-driven operation should consume resource-valued records
   produced earlier by matcher-result productions.
4. Lower `ordered(...)` properties and require them to exist on every input
   collection that needs ordering.
5. Parse `diagnostics` options only if diagnostics lowering exists; otherwise
   reject with a precise diagnostic.

### Tests

Focused tests:

- operation with inputs and outputs
- operation with only inputs or only outputs if the runtime API allows it
- operation resource-expression resolution
- ordered property validation
- diagnostics option unsupported diagnostic until implemented

Golden tests:

- Lark `.yidl` equivalent of an existing ordered aggregate operation golden

## Phase 7: Import And Export Semantics

### Scope

Complete import behavior for the full symbol surface.

### Design

1. Enforce exports for imported modules unless a test-only private mode is
   explicitly introduced.
2. Implement `from "file.yidl" import kind Name as Alias`.
3. Add imported symbol tables for each supported symbol kind.
4. Keep absolute import rejection.
5. Preserve import-cycle detection.

### Tests

Focused tests:

- alias imports for resources, collections, and concepts
- selective imports with and without `as`
- non-exported symbol rejection
- import cycle diagnostic
- absolute import path rejection

Golden tests:

- multi-file Lark `.yidl` source using imported resources and schema
  extensions

## Phase 8: Diagnostics And Source Locations

### Scope

Make parser and lowering errors actionable.

### Design

1. Carry source path, line, and column into lowering diagnostics.
2. Prefer `YidlSyntaxError` only for grammar parse failures.
3. Use `YidlSymbolError` for unresolved names, unsupported grammar surfaces,
   type errors, and semantic conflicts.
4. Include the symbol kind and name in every lowering failure.
5. Keep error messages stable enough for tests, but avoid asserting entire
   paragraphs.

### Tests

Focused tests:

- syntax error includes path, line, and column
- undefined resource includes resource name and reference name
- unsupported feature includes exact grammar member name
- nested import error includes imported path context

## Phase 9: CLI And Fixture Integration

### Scope

Expose the V2 compiler through the existing CLI or a narrow internal helper
only after the lowering path is useful end-to-end.

### Design

1. Add a helper that compiles `.yidl` files from disk using relative imports.
2. Keep the existing in-memory `compile_yidl_files(...)` API for tests.
3. Add CLI coverage only if there is already a supported command boundary for
   concept modules.
4. Do not make CLI work a blocker for compiler correctness.

### Tests

Focused tests:

- disk-backed relative import resolution
- CLI smoke test only if command support is added

## Test Strategy

Use a layered test strategy:

1. Parser shape tests verify grammar acceptance and syntax diagnostics.
2. Focused compiler tests verify one lowering behavior at a time.
3. Golden source tests verify end-to-end runtime source emission for successful
   behavior.
4. Runtime validation inside golden cases should execute emitted source and use
   generated builders/containers, not only assert strings.

Prefer canonical golden coverage for success paths once a feature reaches
runtime emission. Keep bespoke unit tests for:

- unresolved names
- unsupported syntax
- expression recognition
- edge-case validation
- diagnostics

Focused command:

```sh
uv run --with pytest pytest tests/generation/test_yidl_lark_parser.py -q
```

Golden command:

```sh
uv run --with pytest pytest tests/test_yidl_goldens.py -q
```

Full relevant regression:

```sh
uv run --with pytest pytest -q
```

## Implementation Order

1. Resource lowering.
2. Basic shape lowering: records, computed collections, and ports.
3. Value and condition expression lowering.
4. Matcher lowering.
5. Production lowering.
6. Operation lowering.
7. Import/export enforcement for all supported symbols.
8. Source-location diagnostics.
9. CLI or disk fixture integration.

Each phase should land with:

- at least one red focused test before implementation
- implementation limited to the phase surface
- focused tests passing
- golden coverage when the feature emits runtime source
- no changes to the older indentation parser unless a shared helper is being
  extracted deliberately

## Open Questions

1. Should `template` resource option blocks allow only `keep` and `edge ...`
   entries initially, or should they also support named reusable option groups?
2. Should top-level `resource` and `property` declarations be globally reusable
   outside concepts, or remain parsed but unsupported until a clear module-level
   symbol model is implemented?
3. Should direct `union` be supported as separate syntax, or should `family`
   remain the only user-facing union surface for now?
4. Should composite collection identity lower in this pass, or should it remain
   a follow-up after single-identity resource stitching works?
5. Should import `export` enforcement be strict immediately, or should tests
   first preserve the current permissive behavior while the lowering surface is
   still incomplete?

## Completion Criteria

The V2 Lark compiler is useful when a `.yidl` concept module can:

1. import a base concept
2. extend a schema family
3. declare Astichi-backed resources
4. choose resources with a matcher
5. produce records into a collection
6. run an aggregate operation that consumes those resources
7. emit runtime source equivalent to an existing Python builder golden
8. execute that emitted source in a validation test

At that point, Lark `.yidl` is no longer only a schema grammar. It becomes a
working source format for snippet-backed generated Python composition.
