# YIDL Contribution Boilerplate Reduction Plan

## Purpose

Production phases solved the lifecycle merge problem: feature concepts can now
insert their own apply edges without forcing `lifecycle_core.yidl` to predeclare
every future feature phase.

The next source-size pressure is lower level. Lifecycle feature files still
contain many nearly identical contribution wrappers. They differ in one resource
or one slot binding, but repeat the same ordering, target, and name bindings.

This plan specifies a small YIDL syntax layer to reduce that contribution
boilerplate without changing matcher semantics or Astichi assembly behavior.

## Current Pressure

After anchored production phases and owned binding-validation consolidation, the
transactional lifecycle files still have substantial repeated contribution
shape:

| File | Approximate current LOC |
| --- | ---: |
| `tests/data/yidl/yidl_transactional_lifecycle/lifecycle_core.yidl` | 1339 |
| `tests/data/yidl/yidl_transactional_lifecycle/lifecycle_managed.yidl` | 1463 |
| `tests/data/yidl/yidl_transactional_lifecycle/lifecycle_owned.yidl` | 1205 |
| `tests/data/yidl/yidl_transactional_lifecycle/lifecycle_transient.yidl` | 871 |
| `tests/data/yidl/yidl_transactional_lifecycle/lifecycle_default_factories.yidl` | 595 |

Typical repeated contribution body:

```yidl
contribution OwnedWorkingFacadeProperty = OwnedWorkingProperty {
    as OwnedWorkingFacadeProperty
    index FieldOrder
    order FieldOrder

    target working_facade_properties {
        build /ClassDef
    }

    ident property_getter_name = FieldName
    ident property_setter_target_name = FieldName
    ident property_setter_name = FieldName
    external current_slot = CurrentSlotName
    external working_slot = WorkingSlotName
    external field_name = FieldName
    external tx_index = TxIndex
}
```

The repeated parts are:

- `index FieldOrder` plus `order FieldOrder`
- target block paths such as `target ... { build /ClassDef }`
- property-name binds
- slot-name binds
- transaction-index binds

The matcher still needs to select the right contribution. This plan does not
replace matchers. It makes the selected contribution declarations shorter.

## Non-Goals

- Do not change Astichi resource or assembly semantics.
- Do not change matcher rule scoring or merge semantics.
- Do not add parameterized macros or a general template language inside YIDL.
- Do not make contribution declarations inherit arbitrary state from nearby
  matchers or phases.
- Do not hide resource selection. The contribution source remains explicit.
- Do not implement contribution families until the smaller features have been
  applied and measured.

## Feature 1: `at` Ordering Sugar

### Syntax

```yidl
contribution OwnedRollback = OwnedRollbackBranch {
    as OwnedRollback
    at FieldOrder

    target rollback_fields_body {
        build /ClassDef/RollbackFields[TxIndex]
    }

    external working_slot = WorkingSlotName
    external staged_slot = StagedSlotName
}
```

### Semantics

`at X` is exactly:

```yidl
index X
order X
```

It is intentionally not an order-only construct. If a contribution needs only an
order or needs different index/order expressions, it must use the existing long
form.

### Validation

The compiler rejects:

- `at` repeated in the same contribution or preset
- `at` combined with explicit `index`
- `at` combined with explicit `order`
- `at` in a diagnostic contribution

Diagnostic example:

```text
contribution 'OwnedRollback' cannot combine at with index
```

### Expected Impact

Small but very low risk:

- `lifecycle_owned.yidl`: roughly 30-60 LOC
- `lifecycle_managed.yidl`: roughly 40-70 LOC
- total lifecycle YIDL: roughly 1-2%

## Feature 2: Bind Groups

### Syntax

Bind groups are named top-level concept members:

```yidl
bind group FieldPropertyNameBinds {
    ident property_getter_name = FieldName
    ident property_setter_target_name = FieldName
    ident property_setter_name = FieldName
}

bind group OwnedWorkingSlotBinds {
    external current_slot = CurrentSlotName
    external working_slot = WorkingSlotName
    external field_name = FieldName
    external tx_index = TxIndex
}
```

They are used inside a contribution:

```yidl
contribution OwnedWorkingFacadeProperty = OwnedWorkingProperty {
    as OwnedWorkingFacadeProperty
    at FieldOrder

    target working_facade_properties {
        build /ClassDef
    }

    use binds FieldPropertyNameBinds
    use binds OwnedWorkingSlotBinds
}
```

### Semantics

A bind group is a source-level expansion of `ident` and `external` bind
declarations.

Expansion happens while compiling the contribution:

```yidl
use binds FieldPropertyNameBinds
```

is treated as if the bind group's declarations appeared at that point.

Bind group contents are ordered. This matters only for deterministic generated
source and diagnostics; binding lookup is still keyed by `(kind, name)`.

### Visibility And Merge

Bind groups are concept members.

- A concept can use local bind groups.
- A concept can use inherited bind groups from `extends`.
- A concept can use imported bind groups if explicit from-import support is
  added for this symbol kind.
- V0 does not support bind-group extension. A bind group is defined once.
- Defining a local bind group with the same name as an inherited bind group is a
  normal duplicate-symbol error.

This mirrors resources more than matchers: bind groups are not selected or
merged by rules.

### Validation

After expansion, existing contribution validation runs unchanged.

The compiler rejects:

- missing bind group
- bind-group cycles
- repeated `(kind, name)` binding after expansion
- `use binds` inside a diagnostic contribution

Example:

```yidl
bind group A {
    use binds B
}

bind group B {
    use binds A
}
```

Diagnostic:

```text
bind group cycle: A -> B -> A
```

### Expected Impact

Useful for property and default-factory contribution blocks:

- `lifecycle_owned.yidl`: roughly 80-140 LOC
- `lifecycle_managed.yidl`: roughly 80-160 LOC
- `lifecycle_transient.yidl`: roughly 50-100 LOC
- total lifecycle YIDL: roughly 4-7%

## Feature 3: Contribution Presets

### Syntax

Contribution presets collect reusable contribution metadata:

```yidl
contribution preset ClassFieldContribution {
    at FieldOrder
    target state_init_body {
        build /ClassDef
    }
}

contribution preset WorkingFacadePropertyContribution {
    at FieldOrder
    target working_facade_properties {
        build /ClassDef
    }
    use binds FieldPropertyNameBinds
}
```

They are used inside contributions:

```yidl
contribution OwnedWorkingFacadeProperty = OwnedWorkingProperty {
    as OwnedWorkingFacadeProperty
    use preset WorkingFacadePropertyContribution
    use binds OwnedWorkingSlotBinds
}

contribution OwnedMapWorkingFacadeProperty = OwnedMapWorkingProperty {
    as OwnedWorkingFacadeProperty
    use preset WorkingFacadePropertyContribution
    use binds OwnedWorkingSlotBinds
}
```

### Semantics

A contribution preset is a source-level expansion of contribution members.

Allowed preset members:

- `as`
- `at`
- `index`
- `order`
- `target`
- `ident`
- `external`
- `use binds`
- `use preset`

Forbidden preset members:

- `diagnostic`
- contribution source/resource

Expansion happens before validation. The final expanded contribution is a normal
`ContributionSpec`.

### Conflict Policy

V0 is strict: repeated metadata is rejected after expansion.

For example, this is invalid:

```yidl
contribution preset OrderedField {
    at FieldOrder
}

contribution Example = SomeResource {
    use preset OrderedField
    order OtherOrder
}
```

Diagnostic:

```text
contribution 'Example' cannot combine preset order with explicit order
```

This deliberately avoids override semantics in V0. If a contribution needs a
different value, use a smaller preset or write the long form.

### Visibility And Merge

Contribution presets are concept members.

- A concept can use local presets.
- A concept can use inherited presets from `extends`.
- V0 does not support preset extension.
- Duplicate preset definitions reject.

### Diagnostic Contributions

Diagnostic contributions are special and cannot target holes or define
index/order. V0 should reject `use preset` inside diagnostic contributions.

If a later slice needs diagnostic presets, they should be restricted to
diagnostic-safe members only and validated separately.

### Expected Impact

This removes most of the non-semantic wrapper repetition:

- `lifecycle_owned.yidl`: roughly 120-220 LOC
- `lifecycle_managed.yidl`: roughly 150-250 LOC
- `lifecycle_transient.yidl`: roughly 80-150 LOC
- total lifecycle YIDL: roughly 6-10%

## Feature 4: Contribution Families

Contribution families are more powerful but should be deferred until after
`at`, bind groups, and presets have been applied.

### Candidate Syntax

```yidl
contribution family OwnedCurrentInitAssignments {
    common {
        as OwnedCurrentInitAssignment
        at FieldOrder
        target state_init_body {
            build /ClassDef
        }
        external field_name = FieldName
        external state_slot = CurrentSlotName
    }

    variant scalar_init = OwnedScalarStateAssignment
        when Init == True
             and BindingShape == "scalar"
             and HasDefaultFactory == False {
        ident init_value_name = FieldName
    }

    variant scalar_default = OwnedScalarStateAssignment
        when Init == False
             and BindingShape == "scalar"
             and HasDefault == True
             and HasDefaultFactory == False {
        ident init_value_name = DefaultValueParamName
    }

    variant map_init = OwnedMapStateAssignment
        when Init == True
             and BindingShape == "map"
             and HasDefaultFactory == False {
        ident init_value_name = FieldName
    }

    variant map_default = OwnedMapStateAssignment
        when Init == False
             and BindingShape == "map"
             and HasDefault == True
             and HasDefaultFactory == False {
        ident init_value_name = DefaultValueParamName
    }
}
```

The family lowers to:

- generated contribution declarations for each variant
- a generated contribution matcher with matching rules

### Why Deferred

Contribution families do change how matcher declarations are authored. The
smaller features do not. They only expand existing contribution bodies.

Implement families only if the first three features leave enough repetition to
justify a new matcher-adjacent surface.

## Grammar Sketch

### New top-level members

```lark
member: ...
      | bind_group_decl
      | contribution_preset_decl
      | contribution_family_decl

bind_group_decl:
    "bind" "group" CNAME "{"
        bind_group_member*
    "}"

bind_group_member:
    bind_decl
  | contribution_use_binds

contribution_preset_decl:
    "contribution" "preset" CNAME "{"
        contribution_preset_member*
    "}"

contribution_preset_member:
    contribution_as
  | contribution_at
  | contribution_index
  | contribution_order
  | target_decl
  | bind_decl
  | contribution_use_binds
  | contribution_use_preset
```

### Existing contribution member extension

```lark
contribution_member:
    contribution_as
  | contribution_at
  | contribution_index
  | contribution_order
  | target_decl
  | bind_decl
  | contribution_use_binds
  | contribution_use_preset
  | contribution_diagnostic

contribution_at:
    "at" contribution_value_expr

contribution_use_binds:
    "use" "binds" qname

contribution_use_preset:
    "use" "preset" qname
```

### Deferred family grammar

```lark
contribution_family_decl:
    "contribution" "family" CNAME "{"
        contribution_family_member*
    "}"

contribution_family_member:
    contribution_family_common
  | contribution_family_variant

contribution_family_common:
    "common" "{"
        contribution_preset_member*
    "}"

contribution_family_variant:
    "variant" CNAME "=" resource_ref_expr
    "when" condition_expr
    "{"
        contribution_preset_member*
    "}"
```

Parser implementation note: `contribution preset` and `contribution family`
must be parsed before ordinary `contribution CNAME = ...` declarations, because
`preset` and `family` are otherwise valid `CNAME` tokens.

## IR Sketch

Add compiler-time specs:

```python
@dataclass(frozen=True)
class ContributionBindGroupSpec:
    name: str
    members: tuple[ContributionBindGroupMemberSpec, ...]

@dataclass(frozen=True)
class ContributionPresetSpec:
    name: str
    members: tuple[ContributionPresetMemberSpec, ...]
```

These should not be emitted into runtime assembly source. They are expanded into
ordinary `ContributionSpec` objects during concept compilation.

`ContributionSpec` itself does not need a new runtime field for `at`; the parser
lowers `at` to `index` and `order`.

## Expansion Order

For a contribution:

1. Start with an empty contribution member list.
2. Expand each `use preset` member in source order.
3. Expand each `use binds` member in source order.
4. Append ordinary local members in source order.
5. Validate the expanded result using existing contribution validation.

Nested expansion is depth-first at the use site.

Example:

```yidl
contribution preset P {
    use binds A
    target state_init_body { build /ClassDef }
}

contribution X = R {
    use preset P
    use binds B
}
```

Expanded order:

```text
A members
target state_init_body
B members
```

Binding key conflicts are detected after expansion.

## Name Resolution

Resolution order for bind groups and presets:

1. local concept declarations
2. inherited declarations from concept closure
3. explicit imports, once import support for these kinds exists

Parent-file import aliases do not leak through inheritance.

If two inherited concepts define distinct bind groups or presets with the same
name, the child concept must reject as ambiguous unless the definitions are the
same object through diamond dedupe.

## Validation Summary

Required diagnostics:

- duplicate bind group name
- duplicate preset name
- missing bind group
- missing preset
- bind-group cycle
- preset cycle
- `at` repeated
- `at` combined with `index` or `order`
- repeated `as`
- repeated target name
- repeated `(kind, name)` binding after expansion
- `use binds` in diagnostic contribution
- `use preset` in diagnostic contribution
- preset expands to a member invalid for the contribution kind
- contribution family variant generates a duplicate contribution or matcher name

## Lifecycle Application Plan

### Slice CBR-1: `at`

Implement `at` and apply it to lifecycle contributions where the current source
has exactly:

```yidl
index FieldOrder
order FieldOrder
```

or:

```yidl
index EvalOrder
order EvalStatementOrder
```

Only the first case should use `at`. The second must remain explicit because the
index and order differ.

Tests:

- parser success for `at`
- parser rejects `at` plus `index`
- parser rejects `at` plus `order`
- lifecycle goldens unchanged except generated decorator source metadata

### Slice CBR-2: Bind Groups

Add bind groups and apply them first to property-name binds:

```yidl
bind group FieldPropertyNameBinds {
    ident property_getter_name = FieldName
    ident property_setter_target_name = FieldName
    ident property_setter_name = FieldName
}
```

Then apply slot groups in `lifecycle_owned.yidl`, where the source repetition is
most obvious.

Tests:

- parser success for local bind group
- inherited bind group use
- missing bind group diagnostic
- duplicate binding after expansion diagnostic
- bind-group cycle diagnostic
- lifecycle owned golden
- full lifecycle decorator tests

### Slice CBR-3: Contribution Presets

Add contribution presets and apply them to repeated target/order shapes:

```yidl
contribution preset DefaultFacadePropertyContribution {
    at FieldOrder
    target default_facade_properties {
        build /ClassDef
    }
    use binds FieldPropertyNameBinds
}
```

Apply first to `lifecycle_owned.yidl`, then to `lifecycle_managed.yidl`, then
`lifecycle_transient.yidl`.

Tests:

- local preset use
- inherited preset use
- missing preset diagnostic
- preset cycle diagnostic
- repeated target after expansion diagnostic
- lifecycle goldens

### Slice CBR-4: Reassess Contribution Families

After CBR-1 through CBR-3, re-count lifecycle source size and inspect remaining
duplication.

Only implement contribution families if the remaining duplication is still
mostly "same contribution wrapper plus matcher rule."

## Roll-Build Candidate?

Yes, but keep the first roll-build narrow:

1. `at` syntax and tests
2. bind groups and tests
3. contribution presets and tests
4. lifecycle application to one feature file, probably `lifecycle_owned.yidl`

Do not include contribution families in the first roll-build. They are a larger
surface and should be justified by post-preset source counts.

