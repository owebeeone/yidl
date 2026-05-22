# YIDL Better Merge Plan

## Purpose

This plan turns the better-merge proposals into an implementation sequence for
YIDL. Astichi already supports the source features that make the YIDL side
simpler:

```python
with astichi_hole(name) as astichi_fallback:
    ...

elif astichi_elif(name):
    pass
```

Adopting those Astichi forms inside lifecycle resources is covered separately by
`dev-docs/YidlAstichiHoleAdoptionPlan.md`. This document focuses on the YIDL
grammar and concept-merge changes: production phases, production extensions, and
feature-local apply edges.

The YIDL goal is broader: feature concepts should be able to extend inherited
composable productions without requiring the base concept to know every future
field kind. This is the missing layer between current DDS/matcher merge and a
fully feature-layered lifecycle generator.

## Plan Split

There are now two related plans:

- `dev-docs/YidlAstichiHoleAdoptionPlan.md`: no new YIDL syntax; updates YIDL
  Astichi resources to use defaulted block holes and additive `elif` targets.
- this document: adds YIDL production phases and production extensions so
  feature concepts can merge apply edges into inherited productions.

The Astichi adoption plan should make the lifecycle resources easier to read and
remove fallback/pass noise. It does not solve base-production coupling. This
plan solves that coupling.

## Current Problem

The transactional lifecycle YIDL split proves that records, families, computed
collections, matchers, and contributions merge well enough to build a real
decorator. The remaining coupling sits in composable productions.

`tests/data/yidl/yidl_transactional_lifecycle/lifecycle_base.yidl` still names
feature-specific apply edges:

```yidl
apply binding_state_slots
    from field: BindingFields
    where FieldOwner == ClassId
    using BindingStateSlotContributions

apply owned_current_state_slots
    from field: OwnedFields
    where FieldOwner == ClassId
    using OwnedCurrentStateSlotContributions

apply transient_rollback
    from field: IndexedTransientFields
    where FieldOwner == ClassId
    using TransientRollbackContributions
```

That means the base lifecycle production is not actually feature-neutral. It
knows about binding, owned, transient, managed, and every later feature must
edit the base production before it can lower into the generated class.

## Target Architecture

YIDL should separate three responsibilities:

1. Base productions define the generated code skeleton and phase order.
2. Feature concepts define facts, resources, contributions, and matchers.
3. Feature concepts extend named production phases with apply edges.

Matchers continue to decide which contribution resource is selected for a
record. Production phases decide where those selected contributions are allowed
to run in the assembly pipeline.

## Syntax Overview

### Production phases

```yidl
production ClassProduction(lifecycle_class: Classes) -> composable {
    root ClassDef = ClassBundle { ... }

    phase state_slots {
        apply plain_state_slots
            from field: PlainFields
            where FieldOwner == ClassId
            using PlainStateSlotContributions
    }

    phase init_params {
        apply plain_init_params
            from field: PlainFields
            where FieldOwner == ClassId
            using PlainInitParamContributions
    }

    phase facade_properties {
        apply plain_properties
            from field: PlainFields
            where FieldOwner == ClassId
            using PlainPropertyContributions
    }

    phase tx_prepare_fields {
    }
}
```

A `phase` is an ordered group of `apply` edges inside a composable production.
The phase name is a stable extension point.

### Anchored phase ordering

The first production-phase slice required the base production to predeclare
every phase name. That proves the merge model, but it still makes the base
production anticipate future features. The next phase-ordering feature should
let a feature introduce a new phase relative to an existing phase:

```yidl
production ClassProduction(lifecycle_class: Classes) -> composable {
    root ClassDef = ClassBundle { ... }

    phase state_slots { ... }
    phase locals { ... }
    phase init_assignments { ... }
    phase properties { ... }
}

extend production ClassProduction {
    phase retained_initvar_slots after state_slots order 20 {
        apply retained_initvar_state_slots
            from initvar: RetainedInitVars
            where FieldOwner == ClassId
            using RetainedInitVarStateSlotContributions
    }

    phase default_factory_evals after locals order 20 {
        apply default_factory_evals
            from step: DefaultFactoryEvaluationSteps
            where EvalOwner == ClassId
            using DefaultFactoryEvalContributions
    }
}
```

`after` defines an anchor phase. `order` sorts phases within the same anchor
bucket. If `order` is omitted, it defaults to `0`.

Same numeric order falls through to declaration order; it is not a conflict and
not an unordered bucket. Declaration order means deterministic concept closure
order, then source order within a concept/file.

Example:

```yidl
phase locals { ... }

phase b after locals order -10 { ... }
phase a after locals { ... }
phase d after locals order 0 { ... }
phase c after locals order 20 { ... }
```

Flattened phase order:

```text
locals
b   # after locals, order -10
a   # after locals, order 0, declared before d
d   # after locals, order 0
c   # after locals, order 20
```

This matches the Astichi-style ordering rule: explicit order is the primary
key, and declaration order is the deterministic fallback within the same order.

### Production extensions

```yidl
extend production ClassProduction {
    phase state_slots {
        apply owned_current_state_slots
            from field: OwnedFields
            where FieldOwner == ClassId
            using OwnedCurrentStateSlotContributions

        apply owned_working_state_slots
            from field: OwnedFields
            where FieldOwner == ClassId
            using OwnedWorkingStateSlotContributions
    }

    phase tx_prepare_fields {
        apply owned_prepare_commit
            from field: IndexedOwnedFields
            where FieldOwner == ClassId
            using OwnedPrepareCommitContributions
    }
}
```

`extend production` does not replace the production. It contributes additional
apply edges to named phases on an inherited or local production.

### Phase context defaults

Feature extensions often repeat the same `from` and `where` clauses. Allow a
phase block to supply defaults:

```yidl
extend production ClassProduction {
    phase state_slots from field: OwnedFields where FieldOwner == ClassId {
        apply owned_current_state_slots using OwnedCurrentStateSlotContributions
        apply owned_working_state_slots using OwnedWorkingStateSlotContributions
        apply owned_staged_state_slots using OwnedStagedStateSlotContributions
    }
}
```

Semantics:

- an `apply` without `from` inherits the phase-level `from`
- an `apply` without `where` inherits the phase-level `where`
- overriding is per clause, not merged
- an explicit `where` on an apply replaces the phase default `where`
- an explicit `from` on an apply replaces the phase default `from`

No implicit `and` is applied between phase and apply conditions in V0. If the
author wants a combined condition, the apply must spell out the full condition.

## Grammar Sketch

Current grammar:

```lark
composable_production_member: root_decl
                            | apply_decl
```

Proposed grammar:

```lark
member: import_decl
      | use_decl
      | property_decl
      | record_decl
      | union_decl
      | collection_decl
      | family_decl
      | port_decl
      | resource_decl
      | matcher_decl
      | production_decl
      | composable_production_decl
      | composable_production_extension_decl
      | assemble_decl
      | assembly_decl
      | operation_decl
      | computed_collection_decl
      | filter_decl

composable_production_decl:
    "production" CNAME composable_production_inputs?
    "->" "composable" "{"
        composable_production_member*
    "}"

composable_production_member: root_decl
                            | apply_decl
                            | phase_decl

phase_decl:
    "phase" CNAME phase_position? phase_context? "{"
        apply_decl*
    "}"

phase_position: phase_anchor phase_order?
              | phase_order
phase_anchor: "after" CNAME
phase_order: "order" SIGNED_INT

phase_context: assemble_from? where_clause?

composable_production_extension_decl:
    "extend" "production" qname "{"
        phase_extension_decl*
    "}"

phase_extension_decl:
    "phase" CNAME phase_position? phase_context? "{"
        apply_decl*
    "}"
```

Notes:

- `qname` in `extend production qname` allows extending an imported production
  explicitly if needed.
- Resolution for `extend production qname` follows normal YIDL symbol lookup:
  local visible production names first, then explicit alias-qualified imports.
  Ambiguous unqualified imported names reject. Parent-file import aliases do not
  leak through concept inheritance.
- V0 should usually extend by local visible name, for example
  `extend production ClassProduction`.
- Top-level `apply` directly under a production remains legal for migration.
  If top-level applies and phases are mixed, the compiler preserves source order
  by lowering contiguous top-level apply runs to compiler-internal phases at
  their original positions.
- V0 should reject root declarations inside production extensions.

## IR Changes

Current `ComposableProductionSpec` stores:

```python
name
inputs
root
applies
```

Add explicit phases:

```python
ProductionPhaseSpec:
    name: str
    anchor_name: str | None
    order: int
    context_from_inputs: tuple[AssemblyInputSpec, ...]
    context_condition: AssemblyConditionSpec | None
    applies: tuple[ApplySpec, ...]
    source_order: int

ComposableProductionSpec:
    name: str
    inputs: tuple[AssemblyInputSpec, ...]
    root: RootSpec
    phases: tuple[ProductionPhaseSpec, ...]
```

For compatibility, parser lowering can wrap legacy top-level applies in an
implicit compiler-internal phase:

```text
__body__
```

That implicit name cannot be written by authors and cannot be referenced from
`extend production`. It exists only as a migration bridge while source files are
converted. If a production mixes explicit phases and top-level applies, each
contiguous top-level apply run is wrapped in an internal source-order phase so
the flattened apply order remains exactly the authored order.

Add extension specs:

```python
ProductionExtensionSpec:
    target_name: str
    phases: tuple[ProductionPhaseExtensionSpec, ...]
    declaring_concept_name: str
    source_order: int

ProductionPhaseExtensionSpec:
    phase_name: str
    anchor_name: str | None
    order: int | None
    context_from_inputs: tuple[AssemblyInputSpec, ...]
    context_condition: AssemblyConditionSpec | None
    applies: tuple[ApplySpec, ...]
    source_order: int
```

The final `YidlCompiledConcept` should expose only flattened productions to the
runtime emitter. Extension specs are compiler-time data.

## Merge Semantics

### Production identity

There is still exactly one composable production named `ClassProduction` in the
merged concept. Extensions do not create new callable productions.

### Extension collection

When compiling a concept:

1. Build the concept closure in the existing deterministic order.
2. Collect inherited production definitions.
3. Collect local production definitions.
4. Collect all production extension specs in closure order and source order.
5. Apply extensions to the visible target production.
6. Validate the flattened result.

Extension collection dedupes by concept identity plus extension source identity
before flattening. This prevents diamond imports from applying the same
extension twice while still rejecting two distinct extensions that define the
same final apply edge name.

### Phase ordering

Implemented V0 keeps phase order owned by the base production: extensions can
only target already-declared phases. The next ordering slice relaxes that rule
by allowing an extension to introduce a phase with `after`.

Every phase has:

- a name
- an optional anchor phase name
- an integer order; omitted means `0`
- a declaration ordinal from deterministic concept closure order and source
  order

Flattening uses a recursive bucket model:

1. collect root phases, meaning phases with no anchor
2. sort root phases by `(order, declaration_order)`; because omitted `order`
   is `0`, ordinary root phases naturally use declaration order
3. for each emitted phase:
   - emit this phase's applies
   - emit phases anchored `after` this phase, sorted by
     `(order, declaration_order)`

If two phases in the same bucket have the same numeric order, declaration order
is the tie-break. This is intentional, not an ambiguity.

Phase body fragments for the same phase name are merged in declaration order.
Applies inside each fragment keep source order. Re-declaring an existing phase
extends that phase; if the redeclaration restates `after` or `order`, the
values must match the original phase metadata.

### Missing phase

In implemented V0, extending a missing phase is a compile-time error:

```text
production ClassProduction has no phase 'tx_close_fields'
```

With anchored ordering, a missing phase remains an error when no `after` anchor
is supplied. A phase extension with an anchor may create a new phase, but the
anchor itself must resolve:

```yidl
extend production ClassProduction {
    phase tx_close_fields after tx_rollback_fields order 20 {
        ...
    }
}
```

If `tx_close_fields` does not exist, it is created. If `tx_rollback_fields` does
not exist, compilation rejects.

### Apply names

Apply edge names remain unique in the merged assembly edge map. If two
extensions add the same apply name, compilation rejects with a diagnostic naming
both concepts if provenance is available.

### Context input visibility

An extension apply is validated against the target production's inputs plus its
own `from` inputs.

Example:

```yidl
extend production ClassProduction {
    phase state_slots from field: OwnedFields where FieldOwner == ClassId {
        apply owned_current_state_slots using OwnedCurrentStateSlotContributions
    }
}
```

Visible value names:

- `ClassId` from `lifecycle_class: Classes`, inherited from the target
  production input
- `FieldOwner` from `field: OwnedFields`, inherited from the phase context

Feature files do not get access to parent file aliases or private import names
unless those symbols are visible through normal concept merge/import rules.

## Validation

Validation should happen after flattening.

Required diagnostics:

- extension target production is missing
- extension target is not a composable production
- extension phase is missing and the extension did not provide an `after` anchor
- phase anchor is missing
- phase anchor graph has a cycle
- repeated phase metadata conflicts with the original `after` or `order`
- duplicate phase name in one production
- duplicate apply name after flattening
- phase-level `where` without phase-level or apply-level inputs able to satisfy
  its names
- apply matcher is missing
- apply input collection is missing
- apply where condition references names outside the production context and
  apply context
- contribution selected by an extension apply cannot target a reachable path in
  the target production's scope

Inherited productions should not be fully revalidated in every child concept.
Only validate:

- local production definitions
- local extensions
- inherited extensions as applied to a locally visible production if the local
  concept changes the production closure

## Runtime And Emitter Impact

The runtime assembly engine should not need to understand extensions. The
compiler should flatten extensions into ordinary production apply lists before
calling the existing source emitter.

The generated decorator source should still contain:

```python
ASSEMBLY_PRODUCTIONS = {...}
ASSEMBLY_EDGES = {...}
```

with no separate production-extension runtime table.

This keeps production extension a compile-time language feature.

## Lifecycle Refactor Shape

### Base after phases

`lifecycle_base.yidl` now points the final assembly at the inherited
`CoreModuleProduction`. The first lifecycle refactor uses explicit placeholder
phases in `lifecycle_core.yidl`, which proves production extension but still
requires core to name many future extension points.

Anchored phase ordering should shrink that skeleton to broad ordered bands:

```yidl
production ClassProduction(lifecycle_class: Classes) -> composable {
    root ClassDef = ClassBundle { ... }

    phase state_slots {
        apply plain_state_slots
            from field: PlainFields
            where FieldOwner == ClassId
            using PlainStateSlotContributions
    }

    phase init_params {
        apply plain_init_params
            from field: PlainFields
            where FieldOwner == ClassId
            using PlainInitParamContributions

        apply initvar_params
            from field: InitVarFields
            where FieldOwner == ClassId
            using InitVarParamContributions
    }

    phase state_init_assignments {
        apply plain_init_assignments
            from field: PlainFields
            where FieldOwner == ClassId
            using PlainInitAssignmentContributions
    }

    phase facade_properties {
        apply plain_properties
            from field: PlainFields
            where FieldOwner == ClassId
            using PlainPropertyContributions
    }

    phase tx_helpers {}
    phase tx_dispatch {}
    phase tx_fields {}
}
```

### Managed extension

```yidl
extend production ClassProduction {
    phase managed_state_slots after state_slots order 20
        from field: ManagedFields
        where FieldOwner == ClassId {
        apply managed_current_state_slots using ManagedCurrentStateSlotContributions
        apply managed_working_state_slots using ManagedWorkingStateSlotContributions
        apply managed_staged_state_slots using ManagedStagedStateSlotContributions
    }

    phase managed_init_params after init_params order 20
        from field: ManagedFields
        where FieldOwner == ClassId {
        apply managed_init_params using ManagedInitParamContributions
    }

    phase managed_tx_prepare_fields after tx_fields order 20
        from field: IndexedTransactionalFields
        where FieldOwner == ClassId {
        apply managed_prepare_commit using ManagedPrepareCommitContributions
    }
}
```

### Owned extension

```yidl
extend production ClassProduction {
    phase owned_state_slots after state_slots order 30
        from field: OwnedFields
        where FieldOwner == ClassId {
        apply owned_current_state_slots using OwnedCurrentStateSlotContributions
        apply owned_working_state_slots using OwnedWorkingStateSlotContributions
        apply owned_staged_state_slots using OwnedStagedStateSlotContributions
    }

    phase owned_facade_properties after facade_properties order 30
        from field: IndexedOwnedFields
        where FieldOwner == ClassId {
        apply owned_default_properties using OwnedDefaultFacadePropertyContributions
        apply owned_current_properties using OwnedCurrentFacadePropertyContributions
        apply owned_working_properties using OwnedWorkingFacadePropertyContributions
    }

    phase owned_tx_prepare_fields after tx_fields order 30
        from field: IndexedOwnedFields
        where FieldOwner == ClassId {
        apply owned_prepare_commit using OwnedPrepareCommitContributions
    }
}
```

## LOC And Mergeability Impact

Current lifecycle source total after Astichi hole adoption: about 5709 LOC.

Expected reductions:

| Change | Direct LOC impact | Mergeability impact |
| --- | ---: | --- |
| Astichi defaulted block holes and elif targets | measured 306 LOC / 5.1% | Handled by `YidlAstichiHoleAdoptionPlan.md`; removes fallback/pass noise before merge refactor |
| Production phases/extensions | 100-200 LOC | Removes feature apply edges from `lifecycle_base.yidl` |
| Phase context defaults | 150-300 LOC | Compresses repeated `from`/`where` clauses in feature extensions |
| Split `binding` out of `lifecycle_owned.yidl` | 0-2% total | Makes feature ownership clear; reduces review size |
| Inline contribution blocks | 100-200 LOC | Reduces one-off contribution names |
| Bind groups | 200-330 LOC | Reduces repeated ident/external binding maps |
| `at` ordering sugar | 50-120 LOC | Removes repeated index/order pairs |

Combined likely reduction after the practical first wave:

```text
10-18% total lifecycle YIDL reduction
```

With inline contribution blocks and bind groups fully applied:

```text
15-25% total lifecycle YIDL reduction
```

The bigger win is not raw LOC. The bigger win is that new field kinds stop
requiring edits to `lifecycle_base.yidl`.

## Implementation Slices

### Y1: Parse Production Phases

Add `phase` parsing inside composable productions.

Deliverables:

- grammar accepts phase blocks
- parser creates phase specs
- legacy top-level applies still parse
- runtime/emitter receives flattened applies equivalent to today's behavior

Focused tests:

- one production with two phases emits same assembly order as explicit applies
- duplicate phase name rejects
- root inside a phase rejects
- top-level applies and phases can coexist during migration

Golden:

- small YIDL fixture with `phase state_slots` and `phase properties`
- generated decorator source should be identical to the non-phase equivalent
  except for source ordering if the fixture intentionally changes it

### Y2: Parse And Store Production Extensions

Add `extend production Name { phase X { apply ... } }`.

Deliverables:

- grammar accepts production extension declarations
- parser stores extension specs
- extension target can be local or inherited
- extension root declarations reject

Focused tests:

- extension of missing production rejects
- extension of missing phase rejects
- extension can target inherited production
- extension apply can use inherited matcher

No lifecycle refactor yet.

### Y3: Flatten Extensions During Concept Merge

Implement merge-time flattening.

Deliverables:

- merged `YidlCompiledConcept.composable_productions` contains flattened
  productions only
- generated runtime source has no production-extension table
- deterministic order: base applies, inherited extensions, local extensions

Focused tests:

- base concept declares production phase
- feature concept extends phase
- combined concept output includes both applies in expected order
- diamond import does not duplicate extension applies

Golden:

- multi-file fixture:
  - `base.yidl`
  - `feature_a.yidl`
  - `feature_b.yidl`
  - `combined.yidl`
- generated output should prove both feature extensions lower into one class
  without base knowing either feature.

### Y4: Phase Context Defaults

Add `from` and `where` defaults on phase blocks and phase extension blocks.

Deliverables:

- `phase name from x: X where ... { apply a using M }`
- apply-level `from` overrides phase-level `from`
- apply-level `where` overrides phase-level `where`
- no implicit condition merging

Focused tests:

- inherited context lowers to equivalent explicit apply
- explicit apply `where` replaces phase `where`
- missing input in phase `where` rejects

Lifecycle use:

- convert repeated managed/owned/transient phase extension blocks to use phase
  context defaults.

### Y5: Refactor Lifecycle To Feature Extensions

Move feature-specific apply edges out of `lifecycle_base.yidl`.

Deliverables:

- `lifecycle_base.yidl` declares phases only
- `lifecycle_managed.yidl` extends phases for managed behavior
- `lifecycle_transient.yidl` extends phases for transient behavior
- `lifecycle_owned.yidl` extends phases for owned and binding behavior
- generated lifecycle output remains semantically equivalent

Verification:

```bash
PYTHONPATH=../astichi/src uv run --with pytest --with black pytest tests/test_yidl_goldens.py -q
PYTHONPATH=../astichi/src uv run --with pytest pytest tests/test_lifecycle_decorator.py -q
```

Expected result:

- no generated behavior change except cleanup already covered by
  `YidlAstichiHoleAdoptionPlan.md`
- `lifecycle_base.yidl` LOC drops
- feature changes become local to feature files

### Y6: Split Binding Into A Separate Feature File

After phase extensions are working, split retained-resource behavior:

- `lifecycle_binding.yidl`
- `lifecycle_owned.yidl extends lifecycle_binding.yidl`

Deliverables:

- binding markers/facts/resources/matchers move to `lifecycle_binding.yidl`
- owned only contains transactional retained-resource ownership behavior
- base imports the top-level lifecycle concept, not every feature file

Verification:

- lifecycle H owned/binding goldens still pass
- generated source remains equivalent

### Y7: Anchored Phase Ordering

Add `after` and `order` to phase declarations.

Deliverables:

- `phase NAME order N { ... }`
- `phase NAME after ANCHOR order N { ... }`
- omitted `order` defaults to `0`
- same order falls through to declaration order
- anchored phase declarations can create new phases
- extension of an existing phase remains legal

Focused tests:

- root phases with omitted `order` emit in declaration order
- root phases with explicit `order` sort by `(order, declaration_order)`
- `after locals order 20` emits after `locals`
- same-order anchored phases emit in declaration order
- missing anchor rejects
- anchor cycle rejects
- redeclaring an existing phase with conflicting order rejects

Lifecycle use:

- replace the current explicit empty placeholder phases with broad core phase
  bands plus feature-created anchored phases
- preserve generated lifecycle goldens except for decorator metadata describing
  phase names/order

### Y8: Inline Contribution Blocks

Add matcher-rule inline contribution syntax:

```yidl
matcher OwnedPrepareCommitContributions(field: IndexedOwnedFields) -> contribution {
    rule scalar when BindingShape == "scalar" -> contribution OwnedPrepareCommitBranch {
        as OwnedPrepareCommit
        target prepare_commit_fields_body {
            build /ClassDef/PrepareCommitFields[TxIndex]
        }
        order FieldOrder
        external working_slot = WorkingSlotName
        external staged_slot = StagedSlotName
    }
}
```

Lowering:

- compiler generates an internal contribution name
- matcher rule points to that generated contribution
- downstream assembly sees ordinary contribution specs

Validation:

- inline contribution body follows the same rules as named contributions
- generated names are deterministic and stable for goldens
- duplicate explicit names reject if the syntax allows optional names

### Y9: Bind Groups

Add reusable bind groups:

```yidl
bind group WorkingPropertyBinds {
    ident property_getter_name = FieldName
    ident property_setter_name = FieldName
    ident property_setter_target_name = FieldName
    external field_name = FieldName
    external current_slot = CurrentSlotName
    external working_slot = WorkingSlotName
}
```

Use:

```yidl
contribution OwnedWorkingFacadeProperty = OwnedWorkingProperty {
    as OwnedWorkingFacadeProperty
    target working_facade_properties { build /ClassDef }
    order FieldOrder
    use binds WorkingPropertyBinds
    external tx_index = TxIndex
}
```

Lowering:

- `use binds Name` expands into bind declarations before contribution
  validation
- local binds after `use binds` may override or duplicate only if the duplicate
  is exactly equal; otherwise reject

### Y10: `at` Ordering Sugar

Add:

```yidl
at FieldOrder
```

Lowering:

- contribution with indexed target: `index FieldOrder` and `order FieldOrder`
- contribution without indexed target: `order FieldOrder`
- explicit `index` or `order` alongside `at` rejects in V0

This should be implemented after the larger merge changes so it does not hide
semantic diffs during the production-extension refactor.

## Deferred Ideas

### Contribution families

Contribution families may still be useful, but they blend matching/routing into
contribution definitions. Prefer inline contribution blocks first because they
keep routing inside matchers.

### Shape families

Do not implement scalar/map shape families yet. The idea is too close to a
lifecycle-specific discriminator macro. Re-evaluate after inline contribution
blocks and bind groups.

### `before` phase anchors

Do not implement `before ANCHOR` in the first anchored phase slice. It is
definable, but it creates a second ordering intuition: `before foo order 20`
means farther from or closer to `foo` depending on how the reader thinks about
the bucket. Prefer `after` anchors and, when something must run before a broad
phase, anchor it after the previous broad phase. Revisit only when a real
example cannot be expressed cleanly with `after`.

### Declarative computed fact joins

Do not implement a relational mini-language yet. Python operation snippets are
still the right escape hatch for computed facts until repeated join/project
patterns appear across multiple domains.

## Roll-Build Candidate

This plan is a roll-build candidate once the repository is clean. The Astichi
runtime support for defaulted block holes and `astichi_elif` targets already
exists. The YIDL source adoption of those features is deliberately split into
`YidlAstichiHoleAdoptionPlan.md` and can run immediately before this plan or as
its own smaller roll-build.

Suggested tag prefix:

```text
better-merge/
```

Suggested checkpoints:

- `better-merge/start`
- `better-merge/Y1-phases`
- `better-merge/Y2-extension-parse`
- `better-merge/Y3-extension-merge`
- `better-merge/Y4-phase-context`
- `better-merge/Y5-lifecycle-refactor`
- `better-merge/Y6-binding-split`
- `better-merge/Y7-anchored-phase-order`

Y8-Y10 should be a second roll-build because they are ergonomic sugar rather
than the core merge-model fix. Y7 is a merge-model improvement: it removes the
need for base productions to predeclare every future feature phase.

## Acceptance Criteria

The better-merge model is proven when:

- a feature YIDL file can add an apply edge into an inherited production without
  editing the base production
- lifecycle base no longer names owned, binding, or transient apply edges
  directly
- generated lifecycle behavior remains stable under goldens
- feature split cleanup is possible without making base imports more coupled
- optional generated-code block cleanup is handled by
  `YidlAstichiHoleAdoptionPlan.md`, so this plan can focus on production merge
  semantics
