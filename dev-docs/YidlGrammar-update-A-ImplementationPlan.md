# YIDL Grammar Update A Implementation Plan

## Status

Implementation plan for `YidlGrammar-update-A-plan.md`. This document is
deliberately fine-grained. It describes the order of code changes, the runtime
shape, validation points, and the success-test strategy.

Core testing rule for this update:

- Successful behavior is covered by golden fixtures under `tests/data/gold_src`
  and `tests/data/goldens/materialized`.
- Bespoke unit tests are for parser recognition, narrow helper mechanics, and
  diagnostics/failure cases that do not belong in a golden.
- Do not duplicate the same success-path assertion in both a unit test and a
  golden fixture. If a behavior produces generated source or assembled code, the
  canonical success test is a golden.

## Working Boundaries

Update A may depend on:

- the existing Lark parser in `src/yidl/concept_grammar.lark`
- the existing compiler in `src/yidl/concept_parser.py`
- generated DDS container/runtime emission in
  `src/yidl/generation/container_runtime_source.py`
- generated value helpers in `src/yidl/generation/matcher_values.py`
- only `astichi.assembler.scope` from the Astichi assembler layer
- `astichi.pathmatch.parse_path_selector(...)`

Update A must not depend on:

- `astichi.assembler.production`
- `astichi.assembler.runner`
- `astichi.assembler.client`
- seed records or seed merge policies
- multi-target contribution fan-out
- string interpolation in path segment names
- explicit binding target blocks for `ident` / `external`

## Intended End State

At the end of V0, a `.yidl` file can define:

- contribution declarations that wrap resources or composable productions
- contribution matchers with `matcher ... -> contribution`
- path-addressed targets using `build /Root/Child[FieldOrder]`
- `ident` and `external` bindings driven by the assembly value stack
- composable productions using `production Name(...) -> composable`
- inline assembly edges using `apply name ... using Matcher`
- top-level reusable assembly edges using `assemble Name(...) ... using Matcher`
- assembly entrypoints using `assembly Name = Production`

The generated compiler path can:

- emit normal DDS compiler source
- emit assembly metadata/runtime code
- build a container from decorator/runtime input records
- run an assembly entrypoint from that container
- produce final Astichi-rendered Python source without hand-written YIDL-specific
  assembly loops in golden fixtures

## Implementation Shape

### New Internal Modules

Add small modules rather than growing `concept_parser.py` further:

- `src/yidl/generation/assembly_plan.py`
  - compile-time immutable spec objects
  - static validation helpers
  - dependency graph helpers
- `src/yidl/generation/assembly_runtime.py`
  - runtime `DataStack`
  - assembly edge execution
  - composable production execution
  - bridge to `astichi.assembler.scope`
- `src/yidl/generation/assembly_source.py`
  - source emission for assembly specs into generated compiler modules
  - import/name analysis for assembly runtime helpers and resources

Keep `concept_parser.py` responsible for parsing and symbol resolution, but move
non-trivial assembly behavior into those modules as soon as it is more than a
few lines.

### Core Spec Types

Define these in `assembly_plan.py`:

```python
@dataclass(frozen=True, slots=True)
class ValueRef:
    name: str

@dataclass(frozen=True, slots=True)
class LiteralValueRef:
    value: object

@dataclass(frozen=True, slots=True)
class TupleValueRef:
    values: tuple[ContributionValueExpr, ...]

ContributionValueExpr = ValueRef | LiteralValueRef | TupleValueRef

@dataclass(frozen=True, slots=True)
class EqualConditionSpec:
    left: ContributionValueExpr
    right: ContributionValueExpr

@dataclass(frozen=True, slots=True)
class AndConditionSpec:
    terms: tuple["ConditionSpec", ...]

ConditionSpec = EqualConditionSpec | AndConditionSpec

@dataclass(frozen=True, slots=True)
class PathSegmentSpec:
    name: str
    indexes: tuple[ContributionValueExpr, ...] = ()
    is_operator: bool = False

@dataclass(frozen=True, slots=True)
class PathSelectorSpec:
    segments: tuple[PathSegmentSpec, ...]

@dataclass(frozen=True, slots=True)
class TargetSpec:
    demand_name: str
    build: PathSelectorSpec | None = None
    owner: PathSelectorSpec | None = None

@dataclass(frozen=True, slots=True)
class BindingSpec:
    kind: Literal["ident", "external"]
    demand_name: str
    value: ContributionValueExpr

@dataclass(frozen=True, slots=True)
class ContributionSpec:
    name: str
    rhs_name: str
    rhs_kind: Literal["resource", "production"]
    build_name: str
    index: ContributionValueExpr | None
    order: ContributionValueExpr | None
    target: TargetSpec
    bindings: tuple[BindingSpec, ...]
```

Matcher and production specs:

```python
@dataclass(frozen=True, slots=True)
class MatcherInputSpec:
    name: str
    collection_name: str

@dataclass(frozen=True, slots=True)
class ContributionMatcherRuleSpec:
    name: str
    condition: ConditionSpec
    contribution_name: str
    weight: float

@dataclass(frozen=True, slots=True)
class ContributionMatcherSpec:
    name: str
    inputs: tuple[MatcherInputSpec, ...]
    default_contribution_name: str | None
    rules: tuple[ContributionMatcherRuleSpec, ...]

@dataclass(frozen=True, slots=True)
class AssemblySourceSpec:
    input_name: str
    collection_name: str

@dataclass(frozen=True, slots=True)
class AssemblyEdgeSpec:
    name: str
    qualified_name: str
    context_inputs: tuple[MatcherInputSpec, ...]
    from_inputs: tuple[AssemblySourceSpec, ...]
    where: ConditionSpec | None
    matcher_name: str
    is_inline: bool

@dataclass(frozen=True, slots=True)
class RootBindingSpec:
    kind: Literal["ident", "external"]
    demand_name: str
    value: ContributionValueExpr

@dataclass(frozen=True, slots=True)
class ApplySpec:
    name: str
    edge_name: str
    is_inline: bool

@dataclass(frozen=True, slots=True)
class ComposableProductionSpec:
    name: str
    inputs: tuple[MatcherInputSpec, ...]
    root_name: str
    root_resource_name: str
    root_bindings: tuple[RootBindingSpec, ...]
    apply_entries: tuple[ApplySpec, ...]

@dataclass(frozen=True, slots=True)
class AssemblyEntryPointSpec:
    name: str
    production_name: str

@dataclass(frozen=True, slots=True)
class AssemblyPlan:
    contributions: tuple[ContributionSpec, ...]
    contribution_matchers: tuple[ContributionMatcherSpec, ...]
    composable_productions: tuple[ComposableProductionSpec, ...]
    assembly_edges: tuple[AssemblyEdgeSpec, ...]
    assemblies: tuple[AssemblyEntryPointSpec, ...]
```

`ConditionSpec` should initially support only `==` and `and`, mirroring the
current condition grammar. It should be expressed in terms of
`ContributionValueExpr`, not the old `source.*` / `match.record(...)` forms.

### Compiled Concept Additions

Extend `YidlCompiledConcept` with:

```python
contributions: Mapping[str, ContributionSpec]
contribution_matchers: Mapping[str, ContributionMatcherSpec]
composable_productions: Mapping[str, ComposableProductionSpec]
assembly_edges: Mapping[str, AssemblyEdgeSpec]
assemblies: Mapping[str, AssemblyEntryPointSpec]
```

Keep the existing `matchers` mapping for DDS/resource matchers. Contribution
matchers are not DDS matchers because their RHS is not a `GeneratedValue`; they
select `ContributionSpec` objects.

## Slice 0: Pre-Flight Cleanup

Goal: make the current tree ready for grammar work without behavioral change.

Steps:

1. Review `YidlGrammar-update-A-plan.md` for duplicate lines introduced during
   editing. Clean obvious duplicate headings or repeated bullets without changing
   semantics.
2. Confirm `tests/data/gold_src/yidl_lark_v2_vertical.py` is the active vertical
   golden that still contains the hand-written assembly loop.
3. Add this implementation plan as the adjacent planning document.
4. Do not modify parser behavior in this slice.

Tests:

- No new tests required.
- Optional sanity command: `pytest tests/test_yidl_goldens.py -k yidl_lark_v2_vertical`.

## Slice 1: Grammar Surface

Goal: parse the complete Update A surface into Lark trees.

Files:

- `src/yidl/concept_grammar.lark`
- `tests/generation/test_yidl_lark_parser.py`

Grammar changes:

1. Add symbol kinds:
   - `contribution`
   - `assembly`
2. Add concept members:
   - `contribution_decl`
   - `assemble_decl`
   - `composable_production_decl`
   - `assembly_decl`
3. Keep existing data production grammar:
   - `production Name from ... to ... { ... }`
4. Add composable production grammar:
   - `production Name(input: Collection, ...) -> composable { ... }`
5. Add contribution grammar:
   - `contribution Name = composable_ref { ... }`
   - `as Name`
   - `index contribution_value_expr`
   - `order contribution_value_expr`
   - exactly one `target`
   - repeated `ident` / `external`
6. Add path grammar:
   - leading `/`
   - `CNAME`
   - indexed segments
   - operator segments `.`, `?`, `*`, `+`
7. Add contribution value expression grammar:
   - literal
   - bare `CNAME`
   - tuple, including one-element tuple with trailing comma
8. Update matcher grammar:
   - optional `-> resource`
   - optional `-> contribution`
   - `default -> resource_ref_expr`
   - rule RHS still uses `resource_ref_expr` at parse time
9. Add assembly edge grammar:
   - top-level `assemble Name(context?) from? where? using Matcher`
   - inline `apply name from? where? using Matcher`
   - bare `apply name` as top-level edge reference
10. Add assembly entrypoint:
    - `assembly Name = qname`

Migration rule:

- Update existing YIDL test sources from `default Resource` to
  `default -> Resource`.
- Update existing matcher conditions in YIDL test sources from `input.Property`
  to bare value names where they are authored in Update A-compatible grammar.
- Direct Python API tests that construct `MatcherSpec` by hand do not need this
  migration.

Parser diagnostics to cover with unit tests:

- no-arrow `default Resource` is rejected
- `apply edge where Foo == True` without `using` is rejected
- bad path segment with reserved characters is rejected
- string interpolation in path segment names is rejected or parsed-then-rejected
  with a stable diagnostic

Success tests:

- Add a golden fixture `tests/data/gold_src/yidl_update_a_parse_surface.py`.
- It compiles a `.yidl` source containing every new syntactic form and emits a
  small generated Python summary of the parsed/lowered surface.
- The materialized golden should include only deterministic data structures:
  contribution names, target names, rendered path specs, matcher kinds,
  production names, apply names, and assembly entrypoints.

## Slice 2: Assembly IR Lowering

Goal: lower parsed Update A trees into `assembly_plan.py` specs without executing
assembly yet.

Files:

- `src/yidl/concept_parser.py`
- `src/yidl/generation/assembly_plan.py`
- `tests/data/gold_src/yidl_update_a_parse_surface.py`

Parser/compiler changes:

1. Add local maps to `_ConceptCompiler`:
   - `_local_contributions`
   - `_local_contribution_matchers`
   - `_local_composable_productions`
   - `_local_assembly_edges`
   - `_local_assemblies`
2. Extend `YidlCompiledConcept`.
3. Change concept compilation to support forward references:
   - Pass 1: properties, families, records, collections, resources.
   - Pass 2: contributions, matchers, data productions, composable productions,
     assembly edges, assembly entrypoints.
   - Pass 3: validation that requires all symbols.
4. Keep existing data-production lowering unchanged.
5. Resource matchers:
   - default `matcher` kind is `resource`
   - lower into existing DDS `MatcherHandle`
   - RHS must resolve to resource or existing `match.resource()` where currently
     allowed
6. Contribution matchers:
   - lower into `ContributionMatcherSpec`
   - RHS must resolve to contribution declarations
   - reject `match.resource()`
   - preserve existing precedence model: sorted rules first, default on miss
7. Contributions:
   - RHS resolves to resource or composable production
   - ambiguous RHS name is a diagnostic
   - `as` sets `build_name`
   - absent `as` uses contribution declaration name
   - exactly one `target`
   - repeated `as`, `index`, `order`, or `target` is a diagnostic
   - duplicate binding with same `(kind, demand_name)` is a diagnostic
   - same demand name in `ident` and `external` is allowed
8. Composable productions:
   - root resource must resolve to a resource
   - inline `apply ... using ...` lowers to an `AssemblyEdgeSpec` with qualified
     name `<ProductionName>.<apply_name>`
   - bare `apply name` stores an `ApplySpec` reference to a top-level edge
9. Assembly entrypoints:
   - RHS must resolve to a composable production
   - entrypoint production must have zero inputs

Value expression lowering:

1. Lower bare `Name` to `ValueRef("Name")`.
2. Lower literals to `LiteralValueRef`.
3. Lower tuples to `TupleValueRef`.
4. Reject:
   - `field.Name`
   - `source.Name`
   - `match.record(...)`
   - `match.resource()`
   - `lookup(...)`
   - ports
5. Use separate helpers for contribution values and legacy data-production
   values. Do not accidentally route Update A expressions through
   `_production_value`.

Success tests:

- Extend `yidl_update_a_parse_surface.py` golden to assert the IR summary after
  symbol resolution.
- Do not add a second success unit test for the same IR summary.

Failure tests:

- `tests/generation/test_yidl_lark_update_a_diagnostics.py`
  - unknown contribution RHS
  - ambiguous resource/production RHS
  - contribution matcher selecting a resource
  - resource matcher selecting a contribution
  - duplicate target
  - duplicate binding pair
  - no-arrow default
  - qualified value ref in contribution body

## Slice 3: Value Stack And Condition Evaluation

Goal: implement the common value model used by contribution metadata, matcher
rules, path indexes, bindings, and assembly `where`.

Files:

- `src/yidl/generation/assembly_runtime.py`
- `src/yidl/generation/assembly_plan.py`
- `src/yidl/concept_parser.py`

Runtime objects:

```python
@dataclass(frozen=True, slots=True)
class DataStack:
    value_dicts: tuple[Mapping[str, object], ...] = ()
    parent: DataStack | None = None

    def push(self, *value_dicts: Mapping[str, object]) -> DataStack: ...
    def get(self, name: str) -> object: ...
```

Compile-time helpers:

1. For each collection input, compute the visible property names from its record
   shape.
2. For a value stack frame, merge production context input property names and
   current `from` tuple property names.
3. Reject duplicate visible names in the same assembly value frame.
4. Parent stack lookup is allowed for outer production values, but duplicate
   names in the same frame remain invalid.
5. Validate each contribution against every assembly path that can select it.

Runtime helpers:

1. Convert each generated record object into a mapping from YIDL property name to
   stored value.
2. Evaluate:
   - `ValueRef`
   - `LiteralValueRef`
   - `TupleValueRef`
   - equality conditions
   - `and` conditions
3. Type-check:
   - `index`: `int | tuple[int, ...] | None`
   - `order`: `int`
   - `ident`: valid Python identifier string
   - path index elements: `int`
   - `external`: Astichi assembler external value type

Success tests:

- Add `tests/data/gold_src/yidl_update_a_multi_source_from.py`.
- The YIDL source should include:
  - two input collections
  - one production context input
  - one `from a: A, b: B`
  - `where Owner == Id and Kind == "selected"`
  - a contribution that binds values from both records
- The golden should emit:
  - generated compiler source
  - example output source produced by running the assembly
- The validation function should execute the example output and assert the
  filtered/product behavior.

Failure tests:

- duplicate visible name across two `from` sources
- unknown value name in contribution metadata
- unknown value name in `where`
- non-int index expression
- non-int order expression
- invalid identifier binding value

## Slice 4: Path Parsing And Selector Rendering

Goal: lower structural path tokens into Astichi selector tuples and validate
literal path reachability.

Files:

- `src/yidl/generation/assembly_plan.py`
- `src/yidl/generation/assembly_runtime.py`
- `src/yidl/concept_parser.py`

Parsing/lowering:

1. Strip the authored leading `/` when rendering for
   `astichi.pathmatch.parse_path_selector`.
2. Render literal segment `Root` as `Root`.
3. Render indexed segment `GetterEntry[FieldOrder]` by evaluating the index at
   runtime and producing `GetterEntry[10]`.
4. Render multi-index segment as `Name[1,2]`.
5. Render operators as their literal single-character segment.
6. Reject interpolation in segment names.

Runtime:

1. Before each candidate lookup, render `build_match` and `owner_match` from the
   current `DataStack`.
2. Call `parse_path_selector(rendered_text)`.
3. Pass the tuple into `find_candidates(..., build_match=..., owner_match=...)`.
4. Wrap `ValueError` from Astichi path parsing in a YIDL diagnostic that names
   the contribution and selector.

Static validation:

1. Build a conservative `StaticScopeInventory` per composable production.
2. Seed each inventory with the root instance name.
3. Walk `apply` entries in declaration order.
4. For each contribution that can be selected by that apply:
   - check literal path segments against currently reachable build names
   - check target demand name against known static demands from resource
     descriptions
   - add the contribution's build-name family to the reachable inventory after
     the apply
5. For production-backed contributions:
   - validate the target in the parent scope
   - validate the referenced production separately in its own scope
6. Treat indexed path segments as their base family name for static validation.
7. Treat operators as selectors, not literal build instance names.

Astichi inventory source:

- Use `GeneratedValue.to_generator().describe()` or equivalent Astichi
  composable description APIs to inspect holes, external binds, identifier
  demands, and production records.
- Do not import experimental Astichi assembler modules for this.

Success tests:

- Add `tests/data/gold_src/yidl_update_a_scope_paths.py`.
- It should prove:
  - `/Root`
  - `/Root/GetterEntry[FieldOrder]`
  - a single operator segment such as `/Root/*` if useful
  - bindings applied to the newly inserted composable instance
- The golden output should include final executable Python source, not only an
  IR summary.

Failure tests:

- unreachable literal build path
- missing target demand name
- child-target apply before parent-creating apply
- invalid path selector
- ambiguous target match at runtime

## Slice 5: Assembly Runtime In Memory

Goal: execute assembly specs directly from `YidlCompiledConcept` and a built DDS
container before generating source for assembly.

Files:

- `src/yidl/generation/assembly_runtime.py`
- `src/yidl/concept_parser.py`
- `tests/data/gold_src/yidl_lark_v2_vertical.py`

Public helper:

```python
def run_assembly(
    concept: YidlCompiledConcept,
    entrypoint: str,
    container: object,
    *,
    unroll: bool | str = "auto",
) -> astichi.Composable:
    ...
```

Runtime algorithm:

1. Resolve the `AssemblyEntryPointSpec`.
2. Invoke the target `ComposableProductionSpec` with an empty context.
3. For each composable production invocation:
   - create `AssemblyScope(astichi.build())`
   - resolve and add root resource with `scope.add(root_name, root.to_generator())`
   - bind root `ident` and `external` entries with a selector narrowed to the
     root build path
   - execute `apply` entries in declaration order
   - return `scope.build()`
4. For each inline assembly edge:
   - create the product of all `from` collection sequences from the container
   - push context mappings and current tuple mappings into a `DataStack`
   - evaluate `where`
   - call the contribution matcher
   - apply the selected contribution if any
5. For each top-level assembly edge reference:
   - use the current production context to satisfy its context inputs
   - run it in the current scope
6. Contribution matcher runtime:
   - sort rules using existing score/order semantics
   - evaluate rule conditions against the `DataStack`
   - return the first matching contribution
   - return default only when no rule matches
7. Contribution application:
   - resource RHS: resolve `GeneratedValue.to_generator()`
   - production RHS: recursively build the referenced composable production with
     only the input bindings it declares
   - evaluate `index` and `order`
   - create `as_composable(...)`
   - render selector
   - call `find_candidates(...)`
   - call `require_one(...)`
   - apply selected composable candidate
8. Binding application:
   - after adding the composable contribution, compute the newly attached build
     path from the target candidate build path plus
     `ComposableResource.instance_name`
   - apply each `ident`/`external` binding with `name=<demand_name>` and
     `build_match=<newly_attached_path>`
   - this provides V0's implicit "bind the thing just added" behavior without
     adding binding selector syntax
9. Root binding application:
   - same mechanism, with `build_match=(root_name,)`
10. Diagnostics:
    - wrap `require_one(...)` failures with contribution, edge, matcher, tuple,
      demand name, rendered path, and current inventory candidate details.

Success tests:

- Update or add `tests/data/gold_src/yidl_update_a_vertical_getters.py`.
- It should replace the hand-written loop from the current
  `yidl_lark_v2_vertical.py` with `run_assembly(...)`.
- Keep multi-source output:
  - `compiler.py`
  - `example_output.py`
- The validation should execute `example_output.py` and assert `GETTERS` and
  `getter_for(...)`.

Failure tests:

- missing selector match
- ambiguous selector match
- missing binding demand after adding a contribution
- production-backed contribution input not supplied

## Slice 6: Generated Compiler Assembly Source

Goal: generated compiler source contains enough assembly metadata/runtime glue to
run an assembly entrypoint without the original `YidlCompiledConcept` object.

Files:

- `src/yidl/generation/assembly_source.py`
- `src/yidl/generation/container_runtime_source.py`
- `src/yidl/generation/data_def_sys.py`
- `tests/data/gold_src/yidl_update_a_vertical_getters.py`

Emission API:

Add a new concept-level emitter rather than overloading DDS-only emission. Keep
the emitter independent of `concept_parser.py` by passing generation-owned
objects:

```python
def emit_concept_runtime_source(
    system: DataDefinitionSystem,
    *,
    resources: Mapping[str, GeneratedValue],
    assembly_plan: AssemblyPlan,
) -> str:
    ...
```

The emitted source should include:

- existing DDS runtime source
- generated resource constructors needed by assembly
- serialized assembly specs
- assembly runtime helper imports
- public functions:
  - `new_builder()`
  - `build_container(builder)`
  - `build_assembly(entrypoint, container, *, unroll="auto")`
  - one convenience function per assembly entrypoint, e.g.
    `build_GetterModule(container, *, unroll="auto")`

Keep `emit_container_runtime_source(system)` intact for existing tests.

Source emission details:

1. Add constructor/source rendering for every `assembly_plan.py` spec type.
2. Reuse `constructor_expr_for(...)` for generated resources.
3. Ensure emitted imports include:
   - `astichi`
   - `AssemblyScope`, `as_composable`, `as_external_value`, `as_identifier`,
     `find_candidates`, `require_one`
   - YIDL assembly runtime helpers
4. Avoid embedding absolute filesystem paths.
5. Preserve source provenance already carried by `from_astichi_code`.
6. Emit deterministic ordering:
   - specs sorted by declaration order where semantics require it
   - maps rendered in declaration order

Success tests:

- Convert `yidl_update_a_vertical_getters.py` so the example output imports or
  executes the generated `compiler.py` and calls the emitted assembly function.
- The golden must fail if the fixture still manually loops over selected records
  and calls `output.instance(...).target(...).add(...)`.
- Keep `compiler.py` and `example_output.py` as two materialized outputs.

Failure tests:

- compile emitted compiler source with `ast.parse` and `compile` already happens
  in `tests/test_yidl_goldens.py`.
- Add direct diagnostics only for source emission cases that cannot be expressed
  as successful generated output.

## Slice 7: Production-Backed Contributions And Scope Nesting

Goal: prove module -> class -> method style composition.

Files:

- `src/yidl/generation/assembly_runtime.py`
- `src/yidl/generation/assembly_plan.py`
- `src/yidl/generation/assembly_source.py`

Behavior:

1. Production-backed contribution target is resolved in the parent scope.
2. The referenced production is built in a fresh child `AssemblyScope`.
3. Only declared child production inputs are pushed into the child value stack.
4. Extra records from the selecting tuple remain available to contribution
   metadata but not to child production internals.
5. Free Python names inside child production output remain free in final emitted
   source after Astichi composition.
6. Static cycle graph rejects `P -> Q -> P` before code generation.

Success tests:

- Add `tests/data/gold_src/yidl_update_a_nested_productions.py`.
- The YIDL source should produce:
  - module root with a sentinel/global helper
  - class production
  - method production
  - field-driven method body contributions
- The example output should execute and prove the method sees module-level free
  names in the final source.

Failure tests:

- production dependency cycle
- child production references an undeclared input
- extra selecting tuple value is not visible in child production unless declared
- `assembly Name = Resource` rejected

## Slice 8: Inline And Top-Level Edge Semantics

Goal: prove the namespace and reuse rules for `apply`.

Behavior:

1. Inline edge key is `<ProductionName>.<apply_name>`.
2. Top-level `assemble` key is concept-level `assemble_name`.
3. `apply name using Matcher` always creates an inline edge.
4. bare `apply name` always references a top-level edge.
5. `apply name where ...` without `using` is invalid.
6. Same spelling can exist as inline and top-level without conflict.
7. Duplicate inline edge names in the same production are diagnostics in V0.

Success tests:

- Add `tests/data/gold_src/yidl_update_a_apply_namespaces.py`.
- Use a top-level `assemble emit` and an inline `apply emit using ...` in the
  same concept.
- The final output should prove the bare reference and inline edge both ran in
  their intended positions.

Failure tests:

- duplicate inline apply name in one production
- bare apply to undefined top-level assemble
- `apply name where ...` with no `using`

## Slice 9: Static Validation Completeness

Goal: make validation errors deterministic before code generation.

Files:

- `src/yidl/generation/assembly_plan.py`
- `src/yidl/generation/assembly_runtime.py`
- `tests/generation/test_yidl_lark_update_a_diagnostics.py`

Validation pass order:

1. Resolve all names and kinds.
2. Validate matcher input lists.
3. Validate contribution value refs against every selecting value stack.
4. Validate `where` value refs against each assembly edge stack.
5. Validate duplicate visible names per assembly value frame.
6. Validate path selector syntax.
7. Validate static path reachability in apply order.
8. Validate target demand existence.
9. Validate production-backed contribution inputs.
10. Validate production dependency graph cycles.
11. Validate assembly entrypoint zero-input production.

Diagnostic content:

- file/source location where available
- contribution name
- matcher and rule/default when applicable
- production name
- apply edge qualified name
- top-level assemble name when applicable
- current value names available
- bad value reference
- rendered selector or static path segment
- inferred production/apply edges that can select a contribution

Failure test list:

- no-arrow matcher default
- matcher kind mismatch
- `match.resource()` in contribution matcher
- qualified value ref in contribution value
- qualified value ref in `where`
- duplicate value names in one assembly frame
- missing contribution value name
- missing `where` value name
- non-int path index
- invalid `as` cardinality
- missing target declaration
- duplicate target declaration
- unreachable build path
- missing demand
- child target before parent apply
- production cycle
- assembly entrypoint with inputs
- assembly entrypoint pointing at resource

## Slice 10: Migrate Current Vertical Golden

Goal: the current Lark V2 vertical golden exercises Update A lowering instead of
manual Astichi assembly.

Current fixture:

- `tests/data/gold_src/yidl_lark_v2_vertical.py`

Required edits:

1. Update `YIDL_SOURCE`:
   - matcher defaults use `default -> PlainTemplate`
   - matcher rule conditions use bare value names if the matcher is authored in
     the new value-stack condition model
   - add `OutputRoot` as root resource
   - add `GetterEntry` contribution
   - add selected `GetterValue` contributions
   - add contribution matchers
   - add composable `ModuleProduction`
   - add `assembly GetterModule = ModuleProduction`
2. Replace `_render_example_output_source(...)` hand loop with generated
   assembly API:
   - execute `compiler.py`
   - build container from field records
   - call emitted `build_GetterModule(container)`
   - emit commented Python source
3. Keep output files:
   - `compiler.py`
   - `example_output.py`
4. Keep validation assertions:
   - generated compiler contains Astichi template constructors
   - generated output has source comment from `OutputRoot`
   - `GETTERS` has `count` and `owner`
   - `getter_for("owner")` returns the managed getter value
5. Remove evidence of hand-coded assembly:
   - no fixture loop over `container.Components.sequence()` that calls
     `output.add(...)`
   - no fixture calls to `output.instance(...).target(...).add(...)`

Success test:

- Existing golden case `yidl_lark_v2_vertical.py` remains the canonical vertical
  success test after migration.

## Slice 11: Reduced Dataclass Golden

Goal: prove the grammar can express the shape shown in `scratch/dataclasses_example.yidl`
without committing a huge stdlib clone yet.

Add:

- `tests/data/gold_src/yidl_update_a_dataclass_smoke.py`

Scope:

- one facade collection
- one fields collection
- module production
- class production
- `__init__`
- `__eq__`
- `__hash__`
- multi-source or context-plus-source joins using `where FieldOwner == ClassId`

Do not include:

- full ordering method matrix
- `slots`
- weakref slots
- every dataclass validation
- sugar forms not in V0

Success assertions:

- generated class initializes fields
- equality uses selected compare fields
- hash uses selected hash fields
- class-level globals/sentinels remain visible in generated methods

This golden is not the lifecycle target. It is a readability and architecture
smoke test for nested productions and facade/field joins.

## Golden Test Policy

For every V0 success behavior:

1. Add or extend a fixture under `tests/data/gold_src`.
2. The fixture must call `run_case(...)` or `run_multi_source_case(...)`.
3. The fixture's `render_case()` must perform the real compile/lower/emit path.
4. The fixture's `validate_case(...)` should execute generated output when the
   output is executable.
5. Materialized output lives under `tests/data/goldens/materialized`.
6. Generated outputs must be deterministic and formatted as stable Python source.
7. Do not place success-only assertions in bespoke unit tests when a golden
   already captures the generated output.

Recommended new/updated goldens:

- `yidl_update_a_parse_surface.py`
- `yidl_update_a_multi_source_from.py`
- `yidl_update_a_scope_paths.py`
- `yidl_update_a_vertical_getters.py` or migrated `yidl_lark_v2_vertical.py`
- `yidl_update_a_nested_productions.py`
- `yidl_update_a_apply_namespaces.py`
- `yidl_update_a_dataclass_smoke.py`

Golden regeneration:

- Use the existing versioned golden harness.
- Keep multi-file outputs as directories, matching the current
  `yidl_lark_v2_vertical` pattern.
- Regenerate only after the validation function passes locally.

## Bespoke Unit Test Policy

Use bespoke unit tests for:

- syntax errors
- symbol errors
- validation diagnostics
- narrow helper functions such as path rendering and cycle detection
- invalid value types
- explicit rejection of deferred syntax

Do not use bespoke unit tests for:

- "this YIDL source produces this working generated compiler"
- "this assembly produces this Python module"
- "this nested production emits these methods"

Those are success paths and should be goldens.

## Implementation Order Summary

Recommended order:

1. Slice 1: grammar parse.
2. Slice 2: IR lowering.
3. Slice 3: value stack.
4. Slice 4: path rendering and static selector validation.
5. Slice 5: in-memory assembly runtime.
6. Slice 6: generated compiler assembly source.
7. Slice 7: production-backed nesting.
8. Slice 8: apply namespace semantics.
9. Slice 9: diagnostic completeness.
10. Slice 10: migrate current vertical golden.
11. Slice 11: reduced dataclass smoke golden.

The first implementation milestone is not "all validators complete." It is:

- parse Update A syntax
- lower contribution specs
- run a resource-backed contribution assembly in memory
- prove with a golden that the old getter loop has become generic

After that, tighten validation and source emission until the migrated vertical
golden no longer contains any hand-written assembly loop.

## Rollback Points

Each slice should leave the tree in a coherent state:

- Grammar parse can land before lowering if new constructs raise
  "lowering not implemented" diagnostics.
- IR specs can land before runtime if success goldens emit deterministic IR
  summaries.
- In-memory runtime can land before generated compiler emission if its success
  golden still emits final Python source.
- Generated compiler emission should land only once it can replace the fixture
  hand loop.

Avoid broad refactors while moving through these rollback points. The existing
parser is already large; isolate new assembly behavior into new modules rather
than turning `concept_parser.py` into the assembly runtime.
