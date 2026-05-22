# YIDL Better Merge Proposals

## Purpose

This document captures proposals for improving YIDL concept merge and production
extension ergonomics. The immediate pressure comes from the transactional
lifecycle YIDL fixture, where `lifecycle_base.yidl` still has to name feature
specific apply edges for `managed`, `transient`, `owned`, and `binding`.

The goal is not to change lifecycle behavior. The goal is to let feature YIDL
files add their own lowering into a shared production skeleton, and then reduce
the repeated boilerplate that appears once that layering is clean.

## Current Baseline

Current transactional lifecycle YIDL source size:

| File | LOC |
| --- | ---: |
| `tests/data/yidl/yidl_transactional_lifecycle/lifecycle_core.yidl` | 1363 |
| `tests/data/yidl/yidl_transactional_lifecycle/lifecycle_managed.yidl` | 1313 |
| `tests/data/yidl/yidl_transactional_lifecycle/lifecycle_owned.yidl` | 1160 |
| `tests/data/yidl/yidl_transactional_lifecycle/lifecycle_transient.yidl` | 778 |
| `tests/data/yidl/yidl_transactional_lifecycle/lifecycle_default_factories.yidl` | 581 |
| `tests/data/yidl/yidl_transactional_lifecycle/lifecycle_base.yidl` | 514 |
| Total | 5709 |

The main smell is not that `lifecycle_owned.yidl` is large. It currently owns a
real amount of behavior: binding validation, owned scalar/map storage,
transaction prepare/apply/rollback, facade properties, default factory lowering,
and computed facts.

The bigger merge smell is that `lifecycle_base.yidl` knows about later feature
concepts through explicit apply edges such as `owned_prepare_commit`,
`binding_properties`, and `transient_rollback`. DDS record/family/matcher merge
is working; composable production extension is the missing layer.

All LOC estimates below are approximate and based on the current 5709 LOC
fixture. They are useful for prioritization, not for promises.

## Proposal 1: Production Phases And Production Extensions

Add named insertion points to composable productions. A base production defines
the skeleton and phase order. Feature concepts extend those phases with
additional apply edges.

Base production:

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

Feature extension:

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

Anchored phase extension:

```yidl
production ClassProduction(lifecycle_class: Classes) -> composable {
    root ClassDef = ClassBundle { ... }

    phase state_slots { ... }
    phase locals { ... }
    phase init_assignments { ... }
    phase facade_properties { ... }
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

### Lowering

- A `phase` lowers to an ordered list of normal `apply` declarations.
- `extend production Name { phase X { ... } }` records a production extension,
  not a replacement production.
- Concept merge gathers production extensions from the concept closure and
  flattens them into the target production before assembly validation.
- V0 phase order is owned by the base production.
- The next phase-ordering slice adds `after` and `order`.
- A phase with `after ANCHOR` may create a new phase if `ANCHOR` exists.
- Omitted `order` means `0`.
- Same numeric `order` falls through to declaration order: deterministic concept
  closure order, then source order.
- Inside one phase, body fragments merge in deterministic concept-closure order
  and source order.
- V0 should reject extension of a missing production or a missing phase unless
  the phase declaration supplies a valid `after` anchor.
- V0 should keep apply names globally unique in the merged assembly edge map.

### Why It Matters

This fixes the layering problem directly. `lifecycle_base.yidl` can define
"there is a state slot phase" without knowing which feature fields need slots.
Owned, binding, transient, and future field kinds can add their own apply edges
without editing the base production.

### Estimated Size Impact

| Scope | Estimated reduction |
| --- | ---: |
| `lifecycle_base.yidl` | 100-200 LOC |
| Total lifecycle YIDL | 3-8% |

This is mainly an architecture and locality fix. It will reduce base-file
coupling more than total line count.

Anchored phase ordering should remove most empty placeholder phases from
`lifecycle_core.yidl` after the first production-extension refactor. The
additional reduction is modest in raw LOC, but important for mergeability:
features can introduce `after locals order 20` style phases without making core
name every future lowering site.

## Proposal 2: Phase Context Defaults

Most lifecycle apply declarations repeat the same `from` and `where` clauses:

```yidl
from field: OwnedFields
where FieldOwner == ClassId
```

Allow a phase block or phase extension block to set a default iteration context:

```yidl
extend production ClassProduction {
    phase state_slots from field: OwnedFields where FieldOwner == ClassId {
        apply owned_current_state_slots using OwnedCurrentStateSlotContributions
        apply owned_working_state_slots using OwnedWorkingStateSlotContributions
        apply owned_staged_state_slots using OwnedStagedStateSlotContributions
    }
}
```

Per-apply `from` and `where` clauses remain legal and override the phase
defaults.

### Lowering

The parser stores optional phase-level `from` and `where` defaults. During
flattening, any apply without an explicit `from` or `where` inherits the phase
defaults before normal validation.

### Estimated Size Impact

| Scope | Estimated reduction |
| --- | ---: |
| Production-heavy files | 150-300 LOC |
| Total lifecycle YIDL | 3-5% |

This compounds well with production phases because feature files will contain
many short apply declarations inside the same context.

## Proposal 3: Contribution Families

Lifecycle has many contribution groups where every member shares target,
ordering, bindings, and only changes the selected resource or a few bind values.

Current style:

```yidl
contribution OwnedCurrentInitAssignment = OwnedScalarStateAssignment { ... }
contribution OwnedCurrentDefaultAssignment = OwnedScalarStateAssignment { ... }
contribution OwnedMapCurrentInitAssignment = OwnedMapStateAssignment { ... }
contribution OwnedMapCurrentDefaultAssignment = OwnedMapStateAssignment { ... }
```

Proposed family style:

```yidl
contribution family OwnedCurrentAssignment {
    as OwnedCurrentInitAssignment
    target state_init_body { build /ClassDef/StateInit }
    order FieldOrder
    ident init_value_name = FieldName
    external field_name = FieldName
    external state_slot = CurrentSlotName

    variant scalar_init = OwnedScalarStateAssignment
        when Init == True and BindingShape == "scalar" and HasDefaultFactory == False

    variant scalar_default = OwnedScalarStateAssignment
        when Init == False and BindingShape == "scalar"
             and HasDefault == True and HasDefaultFactory == False

    variant map_init = OwnedMapStateAssignment
        when Init == True and BindingShape == "map" and HasDefaultFactory == False

    variant map_default = OwnedMapStateAssignment
        when Init == False and BindingShape == "map"
             and HasDefault == True and HasDefaultFactory == False
}
```

The family would lower to ordinary contribution declarations and matcher rules.
It is sugar, not new runtime semantics.

### Estimated Size Impact

| Scope | Estimated reduction |
| --- | ---: |
| `lifecycle_owned.yidl` | 150-250 LOC |
| `lifecycle_managed.yidl` | 150-300 LOC |
| Total lifecycle YIDL | 6-10% |

This is the first proposal that materially reduces feature-file size.

## Proposal 4: Match-Selected Contribution Blocks

Contribution families still name variants explicitly. A smaller step is to allow
matcher rules to inline simple contribution declarations:

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

    rule map when BindingShape == "map" -> contribution OwnedMapPrepareCommitBranch {
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

### Lowering

The compiler creates anonymous or generated-name contribution specs from the
inline blocks, then emits ordinary matcher rules pointing to those specs.

### Estimated Size Impact

| Scope | Estimated reduction |
| --- | ---: |
| Files with many one-off contributions | 100-200 LOC |
| Total lifecycle YIDL | 2-4% |

This is less powerful than contribution families but easier to implement.

## Proposal 5: `at` Ordering Sugar

Many contributions repeat:

```yidl
index FieldOrder
order FieldOrder
```

or just:

```yidl
order FieldOrder
```

Add:

```yidl
at FieldOrder
```

For indexed contributions, `at X` means `index X` and `order X`. For
non-indexed contributions, `at X` means `order X`. If both `index` and `order`
are explicitly needed with different values, keep the long form.

### Estimated Size Impact

| Scope | Estimated reduction |
| --- | ---: |
| Total lifecycle YIDL | 50-120 LOC |
| Total lifecycle YIDL | 1-2% |

This is small but low risk and improves readability.

## Proposal 6: Reusable Bind Groups

Many contributions repeat the same binding set:

```yidl
ident property_getter_name = FieldName
ident property_setter_name = FieldName
ident property_setter_target_name = FieldName
external field_name = FieldName
external current_slot = CurrentSlotName
external working_slot = WorkingSlotName
```

Add named bind groups:

```yidl
bind group WorkingPropertyBinds {
    ident property_getter_name = FieldName
    ident property_setter_name = FieldName
    ident property_setter_target_name = FieldName
    external field_name = FieldName
    external current_slot = CurrentSlotName
    external working_slot = WorkingSlotName
}

contribution OwnedWorkingFacadeProperty = OwnedWorkingProperty {
    as OwnedWorkingFacadeProperty
    target working_facade_properties { build /ClassDef }
    at FieldOrder
    use binds WorkingPropertyBinds
    external tx_index = TxIndex
}
```

### Lowering

Bind groups are syntactic expansion inside a contribution declaration. They do
not create runtime objects.

### Estimated Size Impact

| Scope | Estimated reduction |
| --- | ---: |
| `lifecycle_owned.yidl` | 80-150 LOC |
| `lifecycle_managed.yidl` | 100-180 LOC |
| Total lifecycle YIDL | 4-7% |

This is especially useful for facade property contributions and default factory
contributions.

## Proposal 7: Shape Families For Scalar/Map Variants

Owned and binding fields duplicate logic across scalar and map shapes:

- validation helper
- state assignment
- property setter
- default factory evaluation
- prepare commit branch

Add an explicit shape family construct:

```yidl
shape family BindingShape {
    scalar when BindingShape == "scalar"
    map when BindingShape == "map"
}

contribution family OwnedWorkingProperty by BindingShape {
    common {
        as OwnedWorkingFacadeProperty
        target working_facade_properties { build /ClassDef }
        at FieldOrder
        external current_slot = CurrentSlotName
        external working_slot = WorkingSlotName
        external tx_index = TxIndex
    }

    scalar -> OwnedWorkingProperty
    map -> OwnedMapWorkingProperty
}
```

### Lowering

This lowers to multiple contribution variants plus matcher rules, using the
shape family's conditions. It is a domain-neutral mechanism: any discriminator
property could define a shape family.

### Estimated Size Impact

| Scope | Estimated reduction |
| --- | ---: |
| `lifecycle_owned.yidl` | 120-250 LOC |
| Future retained-resource features | High |
| Total lifecycle YIDL | 4-8% |

This overlaps with contribution families. If contribution families are powerful
enough, shape families may be unnecessary.

## Proposal 8: Operation Fact Refinement Helpers

Feature files currently add small Python snippets to compute indexed records,
for example owned fields indexed by transaction group. Those snippets are
reasonable, but their boilerplate is repeated:

- load records
- filter by owner/kind
- derive tx index
- write output rows

Add a small declarative helper for common "join and project" computed facts:

```yidl
computed record IndexedOwnedFields
    from field: OwnedFields
    join tx_group: TxGroups
        where TxOwner == FieldOwner and TxGroupKey == field.TxGroupKey
    identity FieldId
    set TxIndex = tx_group.TxIndex
    set CurrentSlotName = field.CurrentSlotName
    set WorkingSlotName = field.WorkingSlotName
    set StagedSlotName = field.StagedSlotName
```

### Lowering

This lowers to the same kind of operation body currently hand-written in YIDL
code snippets. It should only cover simple projection/join cases. General graph
algorithms should remain Python snippets.

### Estimated Size Impact

| Scope | Estimated reduction |
| --- | ---: |
| Current lifecycle YIDL | 50-150 LOC |
| Future derived-fact-heavy features | Medium |
| Total lifecycle YIDL | 1-3% |

This is not the main LOC reducer today, but it keeps future fact computation
from drifting into repetitive Python snippets.

## Proposal 9: Use Astichi Defaulted Block Holes And Elif Targets

The lifecycle YIDL still uses pass/body placeholder contributions to guarantee
valid empty Python blocks. This produces both YIDL noise and generated `pass`
noise.

Astichi now supports the needed source forms directly. Use defaulted block holes
for optional statement regions:

```python
def _prepare_commit_tx_0_fields(self):
    with astichi_hole(prepare_commit_fields_body) as astichi_fallback:
        pass
```

If the hole receives no contributions, Astichi emits the fallback suite. If the
hole receives contributions, Astichi discards the fallback and emits the ordered
payloads.

Use additive `elif` targets for generated dispatch chains:

```python
def _prepare_commit_for_index(self, tx_index):
    if False:
        pass
    elif astichi_elif(prepare_commit_dispatch_branches):
        pass
    else:
        raise KeyError(tx_index)
```

and branch payloads:

```python
def astichi_elif():
    astichi_import(tx_index)
    if tx_index == astichi_bind_external(tx_index_value):
        self._prepare_commit_tx_0_fields()
```

### Lowering

No new YIDL syntax is required. This is an authored-resource cleanup: YIDL
templates should use Astichi's current defaulted-block and clause-target marker
forms.

### Measured Size Impact

| Scope | Estimated reduction |
| --- | ---: |
| Touched lifecycle YIDL files | 306 LOC |
| Total lifecycle YIDL | 5.1% |
| Generated source readability | High |

This is more about generated quality than authored LOC, but it removed a class
of placeholder contributions and simplified transaction dispatch resources.

## Proposal 10: Feature Split Cleanup

`lifecycle_owned.yidl` currently contains both binding and owned behavior. Split
it into:

- `lifecycle_binding.yidl`
- `lifecycle_owned.yidl extends lifecycle_binding.yidl`

This is not a line-count optimization. It is a cohesion and reviewability
cleanup.

### Estimated Size Impact

| Scope | Estimated reduction |
| --- | ---: |
| Total lifecycle YIDL | 0-2% |
| `lifecycle_owned.yidl` file size | 300-500 LOC moved |

This should happen after production phases, otherwise `lifecycle_base.yidl`
would still need to know both binding and owned apply edges.

## Combined Estimate

| Proposal set | Expected total reduction |
| --- | ---: |
| Production phases only | 3-8% |
| Phases plus phase context defaults | 6-12% |
| Add contribution families and bind groups | 15-25% |
| Add shape families or equivalent macro sugar | 20-30% |
| Add computed fact helpers and empty-hole defaults | 22-35% |

The realistic first target should be:

1. Production phases and extensions.
2. Phase context defaults.
3. Contribution families or inline contribution blocks.
4. Bind groups.

That sequence first fixes the merge model, then attacks the largest repeated
authoring patterns.

## Recommended First Slice

Implement production phases without any sugar:

- grammar for `phase` inside composable productions
- grammar for `extend production`
- parser storage for production extension specs
- merge-time flattening
- static validation after flattening
- golden test proving a feature concept can add an apply edge into an inherited
  production without editing the base concept

Acceptance criterion:

`lifecycle_base.yidl` no longer names owned or binding apply edges directly, but
the generated lifecycle output remains unchanged.

This would prove the important architectural point even if total LOC barely
moves in the first slice.
