# YIDL Grammar Update A Plan

## Status

Draft plan. This document captures the next grammar direction after the Lark V2
resource/matcher/production work. It is not an implementation promise for the
whole lifecycle generator. The immediate goal is to define enough syntax to
represent scope-oriented Astichi assembly inputs without hard-coding the current
golden-test loop in Python.

Stability boundary for this update:

- The only Astichi assembler module Update A may depend on is
  `astichi.assembler.scope`. `astichi.assembler.production`,
  `astichi.assembler.runner`, and the rest of `astichi.assembler.client` are
  experimental and must not leak into the YIDL grammar or the Update A
  lowering.
- If a follow-up needs those modules, it gets its own grammar update; do not
  smuggle their concepts in through Update A grammar holes.

Out of scope for Update A (deferred to Update B, captured in the appendix):

- `seed` records on collections.
- Collection merge policies and primary-key/identity diagnostics for seed
  merging.

## Motivation

YIDL currently has resources, matchers, and data productions. That is enough to
select an Astichi resource from facts and write derived records into
collections. It is not enough to describe how selected resources are attached
to an Astichi build scope.

Astichi has a stable `astichi.assembler.scope` module. For this plan, only that
module is in scope:

- `AssemblyScope`
- `ComposableResource`
- `DemandSelector`
- `as_composable(...)`
- `as_external_value(...)`
- `as_identifier(...)`
- `find_candidates(...)`
- `require_one(...)`

The missing YIDL grammar surface is a way to say:

- this selected template is a build contribution
- this generated class/function/module is its own composable production/scope
- it should be registered with this builder name and optional index
- it should target a compatible demand by name and optional path selectors
- it supplies external values or identifier spellings demanded by that
  contribution
- those values come from the current source/assembly tuple

## Existing Compiler Boundary

YIDL compile time defines:

- schemas
- resources
- matchers
- productions
- composable production/scope rules
- assembly entrypoints

Decorator/runtime input provides:

- actual class records
- actual field records
- actual facade records
- transaction manager/group records
- user helper parameters and callable references

The grammar must not require decorator-time facts to be embedded in the YIDL
source.

## Terminology Choice: `contribution`

Update A uses `contribution` rather than `component`.

Rationale:

- `component` already overloads in this codebase with `concept`,
  `CapsuleConceptBuilder`, and informal "UI/runtime/build component" usage.
- `contribution` reads as "selectable assembly contribution" — exactly the
  semantics of "a `ComposableResource` (or external/identifier resource) plus
  the demand it should attach to". It is a precise noun that does not collide
  with existing surfaces.
- Matcher rules that select assembly items will be described as selecting
  contributions, which lines up with the bridge to `ComposableResource`
  documented under Feature A2.

The grammar still allows future synonyms if they prove necessary, but the
plan-level term is `contribution`.

## Feature A1: Contribution Declarations

Add a selectable assembly contribution distinct from a plain `resource`.

```yidl
contribution InitParam = InitParamTemplate {
    index FieldOrder
    order FieldOrder

    target params {
        build /Root/InitMethod
    }

    ident field_name = FieldName
}
```

The example above assumes the assembly tuple makes `FieldOrder` and `FieldName`
visible in the current value stack. All value expressions inside the
contribution body are evaluated against the blended value stack produced by the
assembly path that selected the contribution (see "Value Stack Context" below).

Lowering:

- `InitParamTemplate` is an existing YIDL `resource` whose generated value is a
  `MatcherGeneratedValue` (DDS) that resolves to an `astichi.Composable`.
- More generally, the contribution right-hand side may be either a plain
  `resource` or a `production ... -> composable`. The right-hand side supplies
  the composable artifact; the contribution declaration supplies how that
  artifact is attached.
- The contribution declaration combines the resolved composable with
  builder-side metadata to produce a `ComposableResource` at runtime:
  - `ComposableResource.composable` ← resolved composable from the right-hand
    side.
  - `ComposableResource.build_name` ← the contribution's declared name on the
    left of `=` (here `InitParam`). Override with an optional `as` clause
    (see below) when the YIDL-level name and the builder instance name need to
    differ.
  - `ComposableResource.build_index` ← `index` value (must lower to
    `int | tuple[int, ...] | None`; absent means `None`).
  - `ComposableResource.order` ← `order` value (must lower to `int`; absent
    means `0`).
- `target params { ... }` lowers to `DemandSelector(name="params", ...)`.
- Inside `target`, `build`/`owner` lower to `DemandSelector.build_match` and
  `DemandSelector.owner_match`.
- `ident field_name = ...` lowers to an identifier-binding resource via
  `as_identifier(...)` whose `DemandSelector.name` is the left-hand side
  (`field_name`).
- `external value_name = ...` lowers to an external-value resource via
  `as_external_value(...)` with the same name-mapping rule.

### Value Stack Context

A contribution is evaluated against a stack of visible values, conceptually
matching the `DataStack` model used by the scratch Astichi examples. Assembly
edges push the selected input records and production values into that stack
before evaluating matcher conditions, contribution metadata, path indexes, and
binding expressions.

The authored surface does not expose record structure. A contribution does not
ask for `field.FieldName` or `cls.ClassOrder`; it asks for `FieldName` and
`ClassOrder`. If two visible records would publish the same name with different
meanings, the concept/input designer must disambiguate upstream by renaming or
projecting the records before they are pushed.

For V0, authored YIDL must treat duplicate visible names in one assembly value
frame as invalid input shape unless an upstream projection has deliberately
removed or renamed one side. Implementations may use stack ordering internally,
but the language does not expose shadowing or qualified record references as a
disambiguation feature.

Value expressions inside `index`, `order`, path indexes, `external`, and
`ident` may use these value-stack forms:

- `Name` — a visible value in the current data stack.
- literals and tuples of visible values.

V0 rules:

- V0 contribution bodies address values by bare visible names. There is no
  qualified input-root syntax in the authored grammar.
- Qualified forms such as `field.Order`, `cls.ClassOrder`, and
  `match.record("field").Order` are not escape hatches. They leak source record
  structure into assembly logic and should be rejected in contribution value
  expressions.
- The `source.<Property>` form (which exists in `production_decl` value
  expressions) does not appear in contribution bodies. Contributions are not
  sourced from a single named collection; they are evaluated against a
  blended assembly value stack.
- The compiler must validate at lowering time that every referenced value name
  can be provided by every assembly path that can select the contribution.
  Unknown value names raise a YIDL-level diagnostic naming the contribution,
  assembly edge, matcher, and bad reference. If multiple pushed records expose
  the same name, V0 reports that as an ambiguous visible name unless the
  upstream producer has projected the tuple to a non-conflicting shape.

Optional `as` clause for builder-name override:

```yidl
contribution InitParamForGroupA = InitParamTemplate {
    as InitParam
    index FieldOrder
    ...
}
```

`as` exists for the case where two contributions need distinct YIDL-level
names but should both register under the same builder instance name (or vice
versa). When omitted, the builder instance name equals the contribution's
declared name. `as` does not change the contribution declaration name, the
right-hand side resource/production, the selected matcher result, or the target
demand. It only sets the builder instance name passed to Astichi.

Cardinality and at-most-one rules:

- At most one `as` clause per contribution.
- At most one `index` clause per contribution.
- At most one `order` clause per contribution.
- `target` cardinality is **exactly one matching hole** in the inventory at
  apply time. Zero or more than one matches is a diagnostic, not a silent
  fan-out. Multi-instantiation is a future feature; do not infer it from
  selector ambiguity.

Value-type rules:

- `index` value expressions must lower to `int` or `tuple[int, ...]` at
  apply time. Other types raise a YIDL-level diagnostic before the value is
  passed to `ComposableResource`.
- `order` value expressions must lower to `int`. Default `0` if absent.

## Feature A2: Matchers Select, Productions Span

Current matchers select resources for supplied input records. Composable
production assembly needs matchers to select contributions for supplied input
records. Matchers do **not** own collection spanning.

```yidl
matcher InitParamContribution(field: Fields) -> contribution {
    rule init when Init == True -> InitParam
}
```

Selection-kind typing:

- `matcher` declarations gain an optional `-> resource` (default) or
  `-> contribution` annotation that fixes the kind of every rule's RHS.
- `-> resource` matchers (the existing default) must target plain
  `resource` declarations and may be used as data-production sources.
- `-> contribution` matchers must target `contribution` declarations and may
  only be used by inline `apply` edges or top-level `assemble` edges.
- Mixing kinds inside one matcher is a YIDL-level diagnostic.
- Using a `-> contribution` matcher as a data-production source (or vice
  versa) is a YIDL-level diagnostic at the use site, not a runtime failure.

Matcher input contract:

`matcher_input_list` may declare multiple inputs. That means the matcher can
resolve a contribution for that tuple shape; it does not mean the matcher
iterates the Cartesian product of those collections.
The input names (`field`, `facade`, `cls`, etc.) identify tuple slots for
assembly validation. Rule conditions read the blended value stack built from
those slots, not dotted properties on the slot names.

A contribution matcher still selects at most one contribution for a supplied
tuple. It inherits the existing matcher rule ordering, scoring, and equal-score
overlap diagnostics. If one tuple needs to produce several contributions, that
is a multi-contribution selection feature and is outside V0.

Matcher defaults preserve the existing runtime precedence: rules are considered
first according to the current score/order rules, and the default is selected
only when no rule matches. Update A adopts the arrow spelling
`default -> ContributionName` for consistency with rule RHS syntax.

```yidl
matcher ManagedGetterContribution(field: Fields, facade: Facades) -> contribution {
    rule managed when Kind == "managed"
                 -> ManagedGetter
}
```

An assembly edge supplies tuples to the matcher:

```yidl
assemble ManagedGetterContributions(facade: Facades)
    from field: Fields
    where FieldFacadeId == FacadeId
    using ManagedGetterContribution
```

The assembly edge owns spanning and joins. The matcher owns treatment selection
for each supplied tuple. Legacy data-production lowering can keep its
current implementation helpers, but Update A must not expose matcher iteration
as the assembly model.

Compile-time validation (binds A1 and A2 together):

- Every visible value name inside a contribution body must be supplied by the
  assembly tuple that can select that contribution.
- Unknown value names raise a YIDL-level diagnostic that names the
  contribution, assembly edge, matcher, and offending reference. Name
  collisions are resolved before values enter the authored assembly surface, not
  by qualified refs in contribution expressions.
- When the same contribution can be selected from multiple matchers (e.g.
  one rule per matcher pointing at the same contribution declaration), the
  validator must succeed against every selecting assembly value stack, or
  reject the configuration explicitly.

Bridge from contribution selection to `ComposableResource`:

- A `-> contribution` matcher selects a contribution declaration, not a raw
  generated template.
- The contribution's right-hand side resolves to the underlying
  `GeneratedValue`/`astichi.Composable`; the contribution declaration supplies
  `build_name`, `build_index`, `order`, the `DemandSelector`, and the bound
  external/identifier resources.
- Existing DDS resource matchers stay unchanged. Contribution matchers add a
  typed wrapper path for assembly-side selection.

The compiler may add a new contribution wrapper type alongside the existing
generated value hierarchy. The important behavior is that assembly lowering can
distinguish a raw template from an attachable `ComposableResource` plan.

## Feature A3: Build And Owner Selectors

Target selection should use Astichi path selectors for disambiguating demands.
YIDL exposes the selector syntax directly through structural tokens, not a
contextual regex.

Examples:

```yidl
target class_body {
    build /Root
}

target body {
    build /Root/InitMethod
    owner /Point/__init__
}
```

Grammar shape (structural, not contextual):

- A `path` is a sequence of `("/" path_segment)+` produced by the standard
  Lark lexer.
- A `path_segment` is either `CNAME path_index?` or one Astichi path operator
  segment (`.`, `?`, `*`, `+`).
- A `path_index` is `"[" contribution_value_expr ("," contribution_value_expr)* "]"`.
  V0 enables this only for instance-family names, e.g.
  `/Root/GetterEntry[FieldOrder]`.
- `build` and `owner` accept a `path`, never a free string.

Why structural tokens:

- Avoids contextual tokenization (Lark terminals are global; a "token starting
  with `/` only when after `build` or `owner`" rule does not compose with the
  rest of the lexer).
- Matches the existing grammar's `port_address_expr`, `tuple_expr`, etc.
- Makes interpolation grammar explicit rather than hiding it inside a regex.

Path-selector contract for V0:

- `build` and `owner` are optional; omitted means `None` (no restriction).
- Every `build` and `owner` selector is interpreted against the demand inventory
  of the composable production scope whose `apply` edge selected the
  contribution. The path is rooted at that `AssemblyScope`, not at the module
  entrypoint and not at the source YIDL concept. For example, `build /ClassDef`
  inside a contribution selected by an `apply` in `ClassProduction` means the
  `ClassDef` build instance in that class-production scope.
- For a production-backed contribution, the contribution's own `target` selector
  is evaluated in the parent scope where the contribution is attached. Selectors
  inside the referenced composable production are evaluated later in that
  child production's own scope.
- The rendered path text (after stripping the leading `/`) must parse with
  `astichi.pathmatch.parse_path_selector(...)`.
- Literal name segments, indexed instance-family segments, and Astichi operator
  segments (`.`, `?`, `*`, `+`) are supported in V0.
- Indexed segments render with Astichi's existing instance-family spelling
  (`Name[1]`, `Name[1,2]`). Each index expression must lower to `int`.
- After parsing, individual path parts must not contain Astichi reserved
  selector characters (`. ? * + /`) except when the whole part is a single
  reserved character used as a path operator.
- Explicit `/*` is legal but discouraged; generated YIDL should not emit it
  unless it carries intent.

Static selector validation:

- V0 must build a conservative static inventory for every composable production
  scope. The inventory includes the production root instance and every build
  instance that can be introduced by earlier `apply` entries in declaration
  order. For indexed instance-family segments, validation checks the base family
  name; the concrete index values are still evaluated at runtime.
- For every assembly edge that can select a contribution, every literal segment
  in the contribution's `build` and `owner` selectors must be reachable in that
  production scope's static inventory before that edge runs. Astichi operator
  segments (`.`, `?`, `*`, `+`) are validated by parsing, but they are not
  treated as literal build instance names.
- V0 must also validate target demand existence against the static Astichi
  demand inventory. YIDL obtains that inventory by asking Astichi to describe
  resource/composable holes and bindings. Runtime `require_one(...)`
  diagnostics remain required after path indexes and decorator-time conditions
  are evaluated, but missing literal parents and impossible demand names must be
  caught before code generation.
- A child contribution that targets a build instance created by another
  contribution must appear in a later `apply` entry in the same production, or
  in a child production whose root/path already contains that instance. Swapping
  such entries is a V0 validation error, not an incidental runtime failure.

Interpolation:

- **V0 supports only instance-family path indexes.** It forbids interpolation in
  path segment names; `/Root/{FieldName}` remains out of scope.
- A follow-up plan defines the interpolation grammar. Open issues that the
  follow-up must resolve before enabling interpolation:
  - Which YIDL value expressions are admissible inside `{...}` (the full
    `value_expr` is too broad; needs a safe subset).
  - Which runtime types are admissible (must `int` for `[…]` indices; must
    render as `CNAME` for path segments).
- The grammar may parse but reject interpolation in V0 with a stable
  diagnostic so existing error messages stay forward-compatible.

## Feature A4: Binding Specifiers

Contributions need to satisfy Astichi demands from the current YIDL context.

```yidl
contribution ManagedGetter = ManagedGetterTemplate {
    index FieldOrder
    order FieldOrder

    target class_body {
        build /Root
    }

    ident field_name = FieldName
    external current_slot = CurrentSlot
    external working_slot = WorkingSlot
}
```

Semantics:

- `ident <name> = <value_expr>` supplies a Python identifier spelling through
  `as_identifier(...)`. The left-hand side is the demand name passed to the
  selector.
- `external <name> = <value_expr>` supplies an external bind value through
  `as_external_value(...)`. The left-hand side is the demand name passed to
  the selector.
- `ident` and `external` are separate binding namespaces. The same spelling may
  appear once in each namespace when a template demands both an identifier and a
  string/object value for the same logical value.
- For both forms, V0 cardinality on the demand match is one record. Ambiguous
  matches raise a YIDL-level diagnostic.

Naming note:

- The keyword for identifier bindings is `ident`, not `identifier`. This
  avoids collision with the existing `identity` clause on `collection_decl`,
  which means a primary-key property and is unrelated.

Possible later extension (deferred):

```yidl
external current_slot {
    value CurrentSlot
    target { build /Root/ManagedGetter[FieldOrder] }
}
```

This needs disambiguating binding selectors and is deferred from V0. The indexed
path spelling itself is already part of V0.

## Feature A5: Filling Internal Holes (Sugar Over A1)

Some selected contributions expose child holes that must be filled by another
generated-value expression.

```yidl
contribution GetterEntry = GetterEntryTemplate {
    index Order
    order Order

    target getter_entries {
        build /Root
    }

    external getter_name = Name

    fill getter_value with Template {
        as GetterValue
        index Order
    }
}
```

Semantics:

- `fill` is **sugar** for declaring a sibling contribution whose
  `DemandSelector.name` is the named hole and whose `build_match` is
  auto-prefixed with the parent's build path (so the author does not have to
  rewrite `/Root/GetterEntry[Order]` by hand).
- Lowering for the example above is equivalent to declaring an additional
  contribution that targets `getter_value` and prepends the just-added
  `/Root/GetterEntry[Order]` to the parent's `build_match`.
- The same `AssemblyScope` / `DemandSelector` machinery applies; nothing
  about `fill` requires new runtime API on `astichi.assembler.scope`.

V0 status:

- **`fill` is deferred from V0.** V0 covers the underlying mechanism: a sibling
  contribution with an explicit indexed target. `fill` is the convenience layer
  added once the explicit form is exercised by the vertical golden.

Explicit V0 form for the current vertical shape:

```yidl
contribution GetterEntry = GetterEntryTemplate {
    as GetterEntry
    index FieldOrder
    order FieldOrder

    target getter_entries {
        build /Root
    }

    external getter_name = FieldName
}

contribution PlainGetterValue = PlainTemplate {
    as GetterValue
    index FieldOrder

    target getter_value {
        build /Root/GetterEntry[FieldOrder]
    }
}

contribution ManagedGetterValue = ManagedTemplate {
    as GetterValue
    index FieldOrder

    target getter_value {
        build /Root/GetterEntry[FieldOrder]
    }

    external field_name = FieldName
}
```

The current golden can then use one contribution matcher to add
`GetterEntry[FieldOrder]` instances and a second contribution matcher to add
`GetterValue[FieldOrder]` instances. The generic assembly runner applies the
entry matcher before the value matcher; the loop shape is generic and no longer
hand-coded around getter entries.

## Feature A6: Composable Productions And Assembly Edges

Assembly edges need a deterministic application order. Child contributions can
target holes created by parent contributions, so "run every assembly edge in
arbitrary order" is not implementable.

V0 also needs more than one build scope. A generated module, class, and function
can each be a separate Astichi build. The result of one scope is a composable
artifact that can be contributed into another scope.

Update A uses `production ... -> composable` for a named scope/artifact. This
keeps `facade` available for its original role: ordinary input data rows that
drive repeated expansion. A composable production is generic; it is enough to
build a class, a method, a helper function, or a module as separate Astichi
scopes.

Update A uses `assemble` for reusable assembly edges and inline `apply ... using
...` for local assembly edges that span input collections and call contribution
matchers. This keeps the roles crisp:

- matchers select which contribution applies to one supplied tuple
- assembly edges decide which tuples exist
- composable productions decide where child assembly edges run and in what
  order
- facade records are just data that composable productions may span over

```yidl
matcher InitParamSelection(field: Fields, facade: Facades) -> contribution {
    rule required when Init == True
                    and HasDefault == False
                    -> RequiredInitParam
    rule defaulted when Init == True
                     and HasDefault == True
                     -> DefaultInitParam
}

production InitMethodProduction(facade: Facades) -> composable {
    root InitMethod = InitMethodTemplate

    apply params
        from field: Fields
        where FieldOwner == ClassId
        using InitParamSelection

    apply assignments
        from field: Fields
        where FieldOwner == ClassId
        using InitAssignSelection
}

matcher InitMethodSelection(facade: Facades) -> contribution {
    default -> InitMethod
}

production ClassProduction(facade: Facades) -> composable {
    root ClassDef = ClassShell {
        ident class_name = ClassName
        external module_name = ModuleName
    }

    apply init_method using InitMethodSelection
    apply repr_method using ReprMethodSelection
}

contribution InitMethod = InitMethodProduction {
    target methods {
        build /ClassDef
    }
}

contribution ClassDef = ClassProduction {
    index ClassOrder
    order ClassOrder

    target module_body {
        build /Root
    }
}

matcher ClassSelection(facade: Facades) -> contribution {
    default -> ClassDef
}

production ModuleProduction -> composable {
    root Root = ModuleRoot

    apply classes
        from facade: Facades
        using ClassSelection
}
```

An assembly entrypoint names the top-level composable production to build:

```yidl
assembly GetterModule = ModuleProduction
```

Semantics:

- Each `production ... -> composable` invocation creates one `AssemblyScope`.
- `root <instance_name> = <resource>` creates the initial root in that scope.
  Optional root binding members use the same `ident`/`external` syntax as
  contributions.
- `assemble <Name>(...) from ... where ... using <Matcher>` declares an
  explicit, reusable assembly edge. It supplies tuples to a `-> contribution`
  matcher.
- `apply <name> ... using <Matcher>` inside a composable production declares an
  inline assembly edge owned by that production. This is the normal authoring
  form. The inline name is the merge key and diagnostic name; it is not a target
  demand name. The selected contribution's `target` block still decides which
  Astichi demand/hole is filled.
- `apply <name>` without `using` references a top-level `assemble` declaration.
- The optional top-level `assemble` context inputs, such as
  `(facade: Facades)`, must be supplied by the current composable production
  invocation. Inline `apply` edges inherit the containing composable
  production's input context. Context inputs do not iterate.
- The optional `from` inputs span decorator/runtime collection rows. If several
  `from` inputs are declared, the assembly edge owns that product and any `where`
  join/filter expression.
- Multi-source `from` is part of V0. The V0 lowering model is simple and
  explicit: compute the product of all `from` source sequences, push the
  production context and current source tuple into the value stack, evaluate
  `where`, then call the contribution matcher for surviving tuples.
- `where` clauses on inline `apply` edges and top-level `assemble` declarations
  use the same blended value-stack name resolution as contribution bodies and
  contribution matcher rules. Bare names such as `FieldOwner` and `ClassId` are
  visible when supplied by the production context or current `from` tuple.
  Qualified input-property forms such as `field.FieldOwner` are rejected in
  Update A authored assembly conditions.
- An assembly edge with context inputs and no `from` inputs runs once for the
  supplied context tuple.
- `apply <name> ... using <Matcher>` or `apply <assemble_name>` runs an
  assembly edge in the current composable-production scope. It is not
  legal for `apply` to name a matcher directly without the `using` form.
- `apply foo where ... using Bar` is legal and creates an inline edge with no
  `from` inputs. `apply foo where ...` without `using` is illegal; a top-level
  assembly-edge reference is the bare form `apply foo`.
- Inline `apply` edge names are local to their containing composable production.
  Top-level `assemble` names live in the concept-level assembly-edge namespace.
  Therefore `apply refresh using RefreshSelection` and a top-level
  `assemble refresh ...` can coexist; `apply refresh using ...` creates the
  inline edge, while bare `apply refresh` references the top-level edge.
- A `contribution` right-hand side may be either a plain `resource` or a
  composable `production`. Resource-backed contributions wrap the resource
  composable. Production-backed contributions first build the referenced
  production in its own `AssemblyScope`, then wrap the production result as the
  contributed composable.
- A production-backed contribution evaluates the referenced composable
  production using the assembly-edge tuple that selected the
  contribution. The referenced production's input names must be satisfiable
  from that tuple.
- The referenced composable production receives only its declared input
  bindings. Extra records in the selecting assembly tuple may be used by the
  contribution metadata itself, but they are not pushed into the child
  production's value stack unless that production declares them as inputs.
- Production-backed contributions are composition units, not separate Python
  modules. Free Python names inside a child production remain free in the final
  generated source after Astichi composition. YIDL must not insert isolation that
  breaks lexical/global visibility expected by the final output; names that are
  not provided by the final generated context still need ordinary Astichi/YIDL
  binding or keep-name handling.
- Production-backed contributions form a static production dependency graph.
  For each composable production `P`, every `apply` edge that can select a
  contribution whose right-hand side is composable production `Q` adds a
  dependency edge `P -> Q`. V0 rejects cycles in that graph during concept
  assembly/validation, not when a decorator-time input happens to exercise the
  cycle. Conditions are not used to prove cycles impossible in V0.
- `apply` entries run in declaration order. This is how parent contributions
  create addressable holes before child contributions target them.
- Fine-grained merge/override points are intentionally exposed: concepts can
  add new inline `apply` edges to a composable production, replace or extend
  matcher rules that select contributions, or introduce alternative
  production-backed contributions without changing the facade data shape. The
  same-name inline `apply` merge/replace policy is still a separate decision;
  V0 should diagnose accidental duplicate edge keys until that policy exists.
- A contribution's applicable production scopes are inferred from assembly edges
  whose matchers can select that contribution. V0 does not add an explicit
  `for production ...` grouping form. Validation and diagnostics must report the
  inferred selecting production/apply edges when a contribution cannot be applied
  consistently across all of them.
- V0 supports named composable productions and one top-level assembly
  entrypoint. Imported assembly fragments, conditional phases, and facade-data
  convenience sugar are later work.

## Proposed Grammar Sketch

This is not final Lark grammar; it captures the intended surface for V0.
The `production ... -> composable` branch is the new scope-building production
form. Existing collection-writing data productions keep their current grammar;
the `-> composable` marker keeps the two production forms disambiguated.

```lark
concept_member: ...
              | contribution_decl
              | assemble_decl
              | composable_production_decl
              | assembly_decl

contribution_decl: "contribution" CNAME "=" composable_ref contribution_options
contribution_options: "{" contribution_member* "}"
contribution_member: "as" CNAME
                   | "index" contribution_value_expr
                   | "order" contribution_value_expr
                   | target_decl
                   | bind_decl

target_decl: "target" CNAME target_options?
target_options: "{" target_option* "}"
target_option: "build" path
             | "owner" path

bind_decl: ("external" | "ident") CNAME "=" contribution_value_expr

path: ("/" path_segment)+
path_segment: CNAME path_index?
            | "." | "?" | "*" | "+"
path_index: "[" contribution_value_expr ("," contribution_value_expr)* "]"

?contribution_value_expr: literal_expr
                        | value_ref
                        | contribution_tuple_expr
value_ref: CNAME
contribution_tuple_expr: "(" contribution_value_expr ","
                         (contribution_value_expr ("," contribution_value_expr)*)? ")"

matcher_decl: "matcher" CNAME "(" matcher_input_list? ")" matcher_kind?
              "{" matcher_default? matcher_rule* "}"
matcher_kind: "->" "resource"        -> matcher_kind_resource
            | "->" "contribution"    -> matcher_kind_contribution
matcher_default: "default" "->" matcher_result_ref
matcher_rule: "rule" CNAME "when" condition_expr "->" matcher_result_ref weight_clause?
matcher_result_ref: resource_ref_expr

assemble_decl: "assemble" CNAME assemble_context? assemble_from?
               where_clause? "using" CNAME
assemble_context: "(" matcher_input_list? ")"
assemble_from: "from" matcher_input_list
where_clause: "where" condition_expr

composable_production_decl: "production" CNAME production_input_list?
                            "->" "composable" "{" production_member* "}"
production_input_list: "(" matcher_input_list? ")"
production_member: root_decl
                 | apply_decl
apply_decl: "apply" CNAME apply_tail?
apply_tail: assemble_from? where_clause? "using" CNAME
root_decl: "root" CNAME "=" resource_ref root_options?
root_options: "{" bind_decl* "}"

assembly_decl: "assembly" CNAME "=" qname
composable_ref: qname
```

Notes:

- `path` uses structural `/` tokens, not a regex terminal. The lexer keeps `/`
  as an ordinary token; the grammar gives it meaning only inside `build`,
  `owner`, and (post-V0) interpolated path segments.
- `path_segment` supports Astichi path operators in V0 so authored paths can
  use the same selector language as `astichi.pathmatch.parse_path_selector`.
- `path_index` supports only integer-producing contribution expressions in V0.
  Full string interpolation for segment names is deferred.
- In the concrete Lark grammar, `value_ref` is a lookup in the current blended
  value stack. It is not a dotted input-record reference.
- `as` is at most once per contribution. So is each of `index`, `order`,
  and `target`. A contribution must have exactly one `target` declaration after
  validation. `bind_decl` may repeat, but the same `(binding kind, demand name)`
  pair may not be declared twice; `ident field_name = ...` and
  `external field_name = ...` are distinct binding kinds.
- `matcher_kind` defaults to `matcher_kind_resource` to preserve current
  matcher semantics.
- `matcher_default` uses `default -> Name` in Update A. The legacy no-arrow
  spelling is not part of the Update A grammar surface.
- Matcher rule and default RHS names resolve according to `matcher_kind`:
  `-> resource` matchers select resources, and `-> contribution` matchers select
  contribution declarations. Kind mismatches are diagnostics. Existing resource
  matcher forms such as `match.resource()` remain valid only for `-> resource`
  matchers.
- `assemble` names a top-level contribution assembly edge. Its `using` matcher
  must be a `-> contribution` matcher.
- The union of context inputs and `from` inputs must satisfy the `using`
  matcher's inputs by name and collection type. For top-level `assemble`, the
  context is the explicit `assemble_context`; for inline `apply`, the context
  is the containing composable production's input list. V0 rejects missing,
  duplicate, and extra matcher inputs.
- `where` expressions on top-level `assemble` declarations and inline `apply`
  edges use the same condition expression model as matcher rules and the same
  blended value-stack name resolution as contribution bodies. They are evaluated
  by the assembly edge before the matcher is called.
- Inline `apply <name> ... using <Matcher>` has the same `from` and `where`
  semantics as a top-level `assemble`, but its context is inherited from the
  containing composable production. It lowers as an assembly edge named
  `<ProductionName>.<name>` unless an implementation chooses an equivalent
  internal key. The `apply` name is an edge name, not a target/hole name.
- `apply <name>` with no `using` resolves to a top-level `assemble`
  declaration. This is the reusable or explicitly named assembly-edge form.
- In `root <instance_name> = <resource>`, the left-hand side is the builder
  instance name and the right-hand side is the resource reference. A spelling
  like `root HashMethod = HashMethod` is legal but stylistically easy to
  misread; examples should prefer distinct template names when practical.
- `production ... -> composable` input lists use the same input names and
  collection types as matchers so contribution RHS production references can be
  validated against the selecting assembly tuple.
- `composable_ref` resolves against resources or composable productions.
  Ambiguous names are rejected.
- `production apply` with no inline `using` must resolve to an `assemble`
  declaration. Inline `apply` must resolve its `using` matcher.
- `apply <name> where ...` with no `using` is invalid because the non-using form
  is only the bare top-level assembly-edge reference.
- `assembly` names a zero-input composable production entrypoint. Its right-hand
  side must resolve to a composable production, not a plain resource.
- Seeds and merge-policy syntax do not appear here; see the Update B appendix.

## V0 Implementation Slice

The smallest useful implementation should prove one vertical path:

1. Parse `contribution` declarations.
2. Parse `target` with structural build/owner selectors, including literal
   names, Astichi operator segments, and indexed instance-family segments such
   as `/Root/GetterEntry[FieldOrder]`.
3. Parse `external` and `ident` bindings, with values restricted to named
   value-stack refs (`FieldOrder`), literals, and tuples.
4. Parse the optional matcher kind annotation; default to `resource`.
5. Parse `assemble` declarations and inline production `apply` edges with
   context inputs, source-span inputs, an optional `where` filter, and a
   `using` matcher.
6. Parse `production <Name> -> composable` declarations with one root, optional
   root bindings, and ordered `apply` entries. Inline `apply` entries are
   ordered members of the production that contains them.
7. Parse `assembly <Name> = <Production>` entrypoints.
8. Validate every referenced value name inside a contribution body against the
   blended value stack produced by each assembly path that can select it.
9. Validate every top-level `assemble` declaration and inline `apply` edge
   against its `using` matcher: context inputs plus `from` inputs must satisfy
   the matcher inputs exactly by name and collection type, and the matcher must
   be `-> contribution`.
10. Validate `where` clauses and matcher rule conditions against the blended
   value stack for their assembly edge. Reject qualified input-property forms in
   authored Update A assembly conditions.
11. Validate contribution selectors against each production scope where the
   contribution can be selected: literal `build`/`owner` path segments must be
   reachable before the selecting `apply` edge runs, and target demand names must
   be possible in the static Astichi demand inventory.
12. Validate production-backed contributions against the selected assembly
   tuple: every referenced composable production input must be supplied by an
   input of the same name and compatible collection type. Extra selected tuple
   inputs do not become visible inside the referenced composable production.
13. Build the static composable-production dependency graph from `apply` edges,
   contribution matchers, and production-backed contribution right-hand sides.
   Reject cycles before code generation. In an incremental builder API, validate
   at the point an added edge becomes fully resolved; otherwise validate at
   concept-finalization time after forward references are resolved.
14. Lower contribution declarations into an internal assembly-contribution
   object that resolves the contribution's right-hand side resource or
   composable production and wraps its composable into a `ComposableResource`
   at apply time.
15. Lower each top-level `assemble` declaration and inline `apply` edge into an
    executable assembly edge that binds production-context inputs, spans
    `from` inputs, evaluates `where`, calls the `-> contribution` matcher for
    each surviving tuple, and applies the selected contribution.
16. Use `astichi.assembler.scope` only:
   - build one `AssemblyScope` per composable production invocation
   - add that production's root resource
   - apply root external and identifier resources
   - run each production `apply` by invoking either its inline assembly edge or
     the named top-level assembly edge with the current production
     context
   - apply selected `ComposableResource`s one matcher result at a time
   - apply that contribution's external and identifier resources immediately
     after its composable is attached
   - build the production scope into a composable artifact for parent scopes
17. Exercise explicit indexed child placement in the Lark V2 vertical golden:
    one assembly edge creates parent `GetterEntry[...]` instances, then a
    second assembly edge creates child `GetterValue[...]` instances
    targeted at `/Root/GetterEntry[FieldOrder]`.
18. Replace the remaining hand-written assembly loop in the Lark V2 vertical
    golden with the generic assembly runner used by the contribution tests.

V0 explicitly defers:

- multi-target expansion (target cardinality stays at exactly one)
- `fill` sugar
- string interpolation in `build` / `owner` path segment names
- binding selectors inside `external` / `ident`
- seeds and merge policies (Update B)
- facade-data convenience sugar beyond ordinary collections and composable
  productions

## Diagnostics

Diagnostics must name:

- contribution declaration name and location
- assembly edge name and current tuple, when applicable. Inline edges should
  render as `<ProductionName>.<apply_name>`.
- composable production name and current production input bindings, when
  applicable
- selected matcher and rule when applicable
- failed inline `apply where` or top-level `assemble where` expression, when
  applicable
- target demand name
- rendered `build` selector (after path-index expression evaluation in V0)
- rendered `owner` selector
- the underlying Astichi candidate error from `require_one(...)`

When a `build` (or `owner`) selector resolves to **zero matching holes**, the
diagnostic must include the unfiltered candidate set so the author can see why
the filter excluded them:

- the holes that matched the demand `name` before the path filter ran
- each candidate's `build_path`, `code_owner`, and source location
- the rendered selector that filtered them out

When static selector validation fails before code generation, the diagnostic
must name the contribution, selecting `apply` edge, containing composable
production, unavailable path segment or demand name, and the apply entries that
were available before the failing edge. This is the error used for a child target
such as `/InitMethod/PostInitCall` when the apply that can create `PostInitCall`
has not run yet.

When a `target` (or binding) selector resolves to **more than one** matching
hole, the diagnostic must:

- list every matching record with build/owner/source-location coordinates
- name the contribution and the selector that produced the ambiguity
- avoid surfacing `require_one`'s low-level message without YIDL context

Matcher kind mismatches (e.g. using a `-> contribution` matcher as a
data-production source) report at the use site and name both the matcher and
the context that rejected it.

Matcher default diagnostics use the Update A arrow grammar. `default Foo` is a
syntax error in this surface; use `default -> Foo`. Defaults follow existing
matcher precedence: they are used only when no rule matches.

Production dependency cycles report during concept validation. The diagnostic
must list the production cycle and the edges that created it, including the
`apply` edge, matcher/rule or default, selected contribution, and
production-backed contribution RHS for each hop.

Using a matcher name directly in `production apply` without `using` is a
diagnostic. `apply SomeMatcher` resolves as a top-level assembly-edge reference;
`apply some_edge using SomeMatcher` creates an inline assembly edge.
Inline `apply` names and top-level `assemble` names are separate namespaces, so
same spelling is not itself a conflict; diagnostics should render inline edges
with the containing production prefix.

If an `as <Name>` clause exactly repeats the contribution declaration name, the
compiler should warn or reject it as redundant. `as` is for overriding the
builder instance name, not for restating the default.

## Decisions And Open Questions

V0 decisions:

1. `target name` is required. A contribution cannot target any compatible
   demand using only `build` / `owner`.
2. `as <Name>` accepts only a literal `CNAME`. Generated builder-family names
   are deferred.
3. Generic composable production syntax is part of V0. `facade` remains an
   ordinary data collection concept, not a build-scope declaration.
4. Bare value-stack references (`FieldOrder`) are the authored
   contribution-body syntax. Qualified record references such as `field.Order`,
   `cls.ClassOrder`, and `match.record("field").Order` are not part of the
   authored grammar.
5. Indexed path segments (`ClassDef[ClassOrder]`) are V0. String
   interpolation in segment names remains deferred.
6. Matchers do not span collections. Inline `apply` edges and top-level
   `assemble` declarations own iteration, joins, and production-context
   binding for contribution assembly.
7. Matcher defaults use arrow syntax: `default -> Name`.
8. `where` clauses use blended value-stack resolution with bare names, not
   qualified input-property references.
9. Build/owner selectors are scope-local to the composable production whose
   `apply` selected the contribution, and V0 validates reachable literal path
   segments and target demand names before code generation.
10. Production-backed contribution cycles are rejected during concept validation.

Post-V0:

1. Path-template interpolation grammar for segment names: which
   `contribution_value_expr` subset is allowed and which runtime types may
   render as `CNAME`.
2. Whether `external` and `ident` need disambiguating `target` blocks once
   real examples produce ambiguous demand names.
3. Whether `fill` should auto-prefix the parent's full build path or only the
   immediately added contribution name.
4. Whether inline `apply` edges and top-level `assemble` declarations need
   indexed or lookup-backed source sugar for performance and readability, e.g.
   `from field: Fields by FieldOwner == ClassId`. Multi-source product plus
   `where` is V0; indexed lookup is an optimization/sugar layer, not matcher
   semantics.
5. Whether value-stack construction needs declarative projection/renaming
   syntax on `from` sources. V0 assumes the concept/input designer provides
   non-conflicting visible names upstream.
6. The exact merge/replace policy for same-key inline `apply` edges across
   composed concepts. V0 can support distinct added edges and matcher-rule
   extension, but duplicate edge keys should be explicit diagnostics until the
   policy is designed.

## Sugar Candidates Surfaced By Dataclass Example

The dataclasses example is implementable with the V0 core, but it is too noisy.
These are syntax candidates, not required semantics for the first slice.

Strong candidates:

1. **Production-local path aliases.** Repeated paths inside one composable
   production want a local alias, e.g. `path Class = /ClassDef`.
2. **`at <expr>`.** Most repeated contributions use the same expression for
   `index` and `order`; `at FieldOrder` can lower to both clauses.
3. **Shared production/matcher predicates.** Joins such as
   `FieldOwner == ClassId` belong on inline `apply ... where` or top-level
   `assemble where`; treatment predicates such as `DecoratorInit == True` may
   still want a shared
   `where { ... }` or `given { ... }` block inside a matcher.
4. **Combined identifier/string binding.** A compact form such as
   `ident+external field_name = FieldName` would cover the common case
   where a template needs both a Python identifier and the string spelling.
5. **For-each contribution sugar.** A contribution declared
   `for facade: Facades` could replace matchers that only have a `default`
   rule.

Larger or deferred candidates:

1. **Multi-contribution rule RHS.** Useful for four ordering methods, but it
   changes selection result count and should not be smuggled into V0.
2. **Multi-target contribution fan-out.** Useful for the same order-value body
   targeting `lt`, `le`, `gt`, and `ge`; deferred with multi-target expansion.
3. **Lookup/indexed source sugar.** Production-bound inputs solve the first
   class/field use case by binding `facade` inside
   `production ClassProduction(facade: Facades)`. General lookup syntax should
   be production/source syntax, for example an indexed `from field: Fields by
   FieldOwner == ClassId`, rather than a matcher runtime feature.
4. **Top-level assembly edges.** Top-level `assemble` remains useful for
   reusable or externally merged edges, but most examples should use inline
   `apply ... using ...` for locality.
5. **Topological apply scheduling.** The current model keeps explicit apply
   order. Scheduling from demand availability may be possible later, but it
   would need cycle diagnostics and deterministic tie-breaking.
6. **Inline one-off contributions.** Convenient for isolated cases, but less
   important once path aliases, `at`, and multi-contribution RHS exist.
7. **Concept composition examples.** Large examples should eventually split
   into `DataclassInit`, `DataclassRepr`, `DataclassEq`, etc. The existing
   `extends` model is the right direction; the example should demonstrate it
   once the core assembly grammar stabilizes.
8. **Declarative diagnostics for semantic combinations.** Rules such as
   `order=True` requiring `eq=True` should move out of front-end comments and
   into YIDL diagnostics once that surface is ready.

Update B (seeds + merge policy):

1. Should seed records be allowed at top level as well as inside concepts?
2. How should imported concepts contribute seeds when multiple concepts define
   the same default record?
3. Do seed policies belong on each seed block, the target collection, or both?

## Appendix: Deferred to Update B (Seeds + Merge Policy)

Seeds and collection merge policies are captured here for context but are
**not part of Update A**. They do not appear in the V0 grammar sketch, are not
referenced from Update A diagnostics, and Update A code must not depend on
their existence.

Update B will own its own grammar plan, lowering, and diagnostics. Splitting
this work out keeps Update A focused on the assembly bridge to
`astichi.assembler.scope` and lets seed semantics (especially `MergeFields`)
be designed without blocking the assembly vertical.

### B1: Seed Records

YIDL should support pre-populating input collections with default records.
These are not decorator-time facts baked into the generated output. They are
seed data written into generated compiler input before user/decorator data is
merged.

Example:

```yidl
collection Facades: FacadeSpec identity FacadeId many

seed Facades policy AddIfAbsent {
    set FacadeId = "main"
    set Role = "main"
    set StateRef = "self._state"
}
```

Use cases:

- default `Main` facade
- default transaction key
- default transaction manager record
- standard helper/facade support records
- overridable default contributions

Semantics:

- seeds write ordinary records into ordinary collections
- seeds run before decorator/user input
- seeds require a target collection with identity
- seeds must declare or inherit a merge policy
- decorator/user input can add or override seeded rows according to policy

### B2: Merge Policy And Primary Keys

Seed records require identity. In relational terms, the collection needs a
primary key. YIDL already has collection identity; grammar and diagnostics
should treat that as the primary key for seed/merge purposes.

Required policies:

- `AddIfAbsent`: default seed; later user data can replace if it writes with a
  replace policy.
- `ReplaceExisting`: explicit override or late concept layer wins.
- `RejectDuplicate`: duplicate identity is an error.

Likely needed policy:

- `MergeFields`: later partial records override provided fields while
  retaining existing values from the seeded record. This has a deeper
  requirement: the runtime must know which fields were explicitly provided
  versus defaulted. Update B must decide whether to land `MergeFields` in the
  same slice as the simpler policies or defer it again.

Seed syntax should reject collections without identity unless a future policy
explicitly supports append-only seeds.

### B Grammar Sketch (Reference Only)

```lark
seed_decl: "seed" qname seed_options? "{" seed_member* "}"
seed_options: "policy" qname
seed_member: "set" property_ref "=" value_expr
```

Note: `seed_member` is grammatically similar to the existing collection-writing
data-production assignment form (`set property_ref = value_expr`). Update B can
reuse that parser path if convenient.
