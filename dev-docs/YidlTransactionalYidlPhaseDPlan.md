# YIDL Transactional Base Phase D Plan

## Scope

Phase D proves lifecycle feature-YIDL layering.

Phase B deliberately kept the decorator as a Python frontend over the Phase A
monolithic lifecycle concept. Phase C may add one substantial feature. Phase D
should split the lifecycle YIDL into layered concepts only when the merge and
override behavior is worth proving.

## Goals

1. Split the lifecycle concept into files with meaningful ownership.
2. Prove that feature concepts extend base concepts by adding facts, computed
   facts, matcher rules, productions, and contributions.
3. Keep the decorator frontend stable while changing the YIDL source layout.
4. Preserve generated output parity for the Phase B base behavior.
5. Provide a fixture that composes at least one feature layer with the base.

## Non-Goals

1. Do not add new lifecycle semantics solely for the split.
2. Do not introduce export enforcement.
3. Do not use inheritance to replace whole imported behavior unless matcher
   merge cannot express the feature.
4. Do not change the public decorator API.

## Candidate File Layout

```text
tests/data/yidl/yidl_transactional_lifecycle/lifecycle_core.yidl
tests/data/yidl/yidl_transactional_lifecycle/lifecycle_managed.yidl
tests/data/yidl/yidl_transactional_lifecycle/lifecycle_default_factories.yidl
tests/data/yidl/yidl_transactional_lifecycle/lifecycle_combined.yidl
```

The initial split should be conservative:

- `lifecycle_core.yidl`: classes, facades, plain fields, initvars, classvars,
  constructor shape, common facade base
- `lifecycle_managed.yidl`: transaction groups, managed fields, current and
  working facades, commit/rollback branches
- `lifecycle_default_factories.yidl`: Phase C computed factory dependencies, if
  Phase C has landed
- `lifecycle_combined.yidl`: imports/extends the selected layers

## Verification

Use goldens to prove:

- core-only generated output works for plain/initvar/classvar
- combined generated output matches the monolithic Phase B managed behavior
- the decorator can import the combined generated artifact
- inherited generated classes still work after the split

Focused tests should cover import/merge mechanics only when the golden cannot
show a failure clearly.

## Roll-Build

Phase D is a roll-build candidate after the exact file split is reviewed.

Suggested tag prefix:

```text
txphaseD-layering/
```

Stop if concept merge cannot express the split without whole-symbol override
syntax.
