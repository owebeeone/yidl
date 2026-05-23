# YIDL Transactional Base Phase D Plan

## Scope

Phase D proves lifecycle feature-YIDL layering.

Phase B deliberately kept the decorator as a Python frontend over the Phase A
monolithic lifecycle concept. Phase C added parameterized default-factory
support inside that same monolithic concept. Phase D now splits the lifecycle
YIDL source into layered concepts without changing lifecycle semantics.

This is a structural refactor, not a behavior phase.

## Goals

1. Split the lifecycle concept into files with meaningful ownership.
2. Prove that feature concepts extend base concepts by adding facts, computed
   facts, matcher rules, productions, and contributions.
3. Keep the decorator frontend stable while changing the YIDL source layout.
4. Preserve generated output parity for the current monolithic behavior,
   including Phase B managed fields and Phase C parameterized default
   factories.
5. Provide a fixture that composes the base layer, managed layer, and
   default-factory layer.

## Non-Goals

1. Do not add new lifecycle semantics solely for the split.
2. Do not introduce export enforcement.
3. Do not introduce whole-symbol override syntax or new YIDL grammar. If
   matcher merge cannot express the split, stop and discuss before introducing
   either.
4. Do not change the public decorator API.
5. Do not rename the generated runtime module imported by the decorator.

## Naming And Compatibility

The decorator continues to import:

```python
from yidl.runtime import _generated_lifecycle_base
```

Phase D must preserve that import path. The generated runtime module remains:

```text
src/yidl/runtime/_generated_lifecycle_base.py
```

To keep the source entry point aligned with that module name, the combined YIDL
entry file remains named `lifecycle_base.yidl`. It becomes the composition file
that imports the feature layers. The old monolithic contents are split into
layer files.

Golden fixture directories may use a Phase D name, but the production runtime
module name and decorator import path do not change.

## Candidate File Layout

```text
tests/data/yidl/yidl_transactional_lifecycle/lifecycle_core.yidl
tests/data/yidl/yidl_transactional_lifecycle/lifecycle_managed.yidl
tests/data/yidl/yidl_transactional_lifecycle/lifecycle_default_factories.yidl
tests/data/yidl/yidl_transactional_lifecycle/lifecycle_base.yidl
```

The split should mirror the field-kind boundaries already exposed by the Phase
B harvester:

- `lifecycle_core.yidl`: classes, facade exposure, plain fields, initvars,
  classvars, constructor shape, common facade base, and core lifecycle metadata
- `lifecycle_managed.yidl`: transaction keys, managed fields, current and
  working facades, transaction-state slots, begin/validate/commit/rollback
  behavior, and managed property contributions
- `lifecycle_default_factories.yidl`: Phase C computed default-factory
  dependency records, evaluation-step records, diagnostics, operations, and
  constructor rewiring contributions
- `lifecycle_base.yidl`: imports the selected layers using the existing YIDL
  concept-import mechanism and exposes the final assembly used by the
  decorator

`lifecycle_core.yidl` may expose a core-only assembly, named
`LifecycleCoreModule`, for focused goldens. The decorator-facing
`LifecycleModule` assembly belongs only to `lifecycle_base.yidl`, so feature
layers can add matcher rules and the final composition point can decide which
collections and productions participate.

The existing `tests/data/yidl/yidl_update_a_dataclasses_split/` fixture is the
model for cross-file concept import and merge behavior. Phase D should use the
same import/merge machinery, not a new composition mechanism.

Future feature layers should follow the same pattern. For example, a transient
field slice can become a sibling `lifecycle_transient.yidl` layer without
moving core or managed behavior again.

## Layering Contract

Layer files are additive.

The managed layer may add:

- field-family variants or companion collections for managed fields
- transaction-group collections and computed transaction-index collections
- resources, productions, contributions, and matcher rules for managed
  behavior

The default-factory layer may add:

- default-factory dependency and evaluation-step collections
- computed operations for dependency extraction, topological ordering, and
  diagnostics
- init-parameter and init-body contributions selected by matcher rules

Layers must not replace an imported resource, matcher, contribution,
production, operation, or assembly wholesale. If the split requires replacement
rather than matcher-rule merge or additive production wiring, Phase D stops and
the missing YIDL composition surface is designed separately.

## Phase C Dependency

Phase C has landed in the current branch, so Phase D includes
`lifecycle_default_factories.yidl` in the split and in verification.

If this plan is ever backported before Phase C, the backport should split only
`core + managed + base`; the default-factory layer then becomes a small
follow-up after Phase C lands.

## Verification

Use goldens for success paths:

- core-only generated output works for plain fields, initvars, classvars, the
  default facade, and common facade-base materialization through
  `LifecycleCoreModule`
- combined generated output matches the monolithic managed behavior from Phase
  B
- combined generated output matches the parameterized default-factory behavior
  from Phase C
- the decorator imports `yidl.runtime._generated_lifecycle_base` unchanged and
  uses the generated artifact built from the split `lifecycle_base.yidl`
- inherited generated classes still work after the split, including more than
  one generated base level

The existing Phase B and Phase C runtime tests should pass unchanged against the
split YIDL layout:

- `test_lifecycle_markers.py`
- `test_lifecycle_harvester.py`
- `test_lifecycle_decorator.py`
- `yidl_transactional_phase_b_decorator`
- `yidl_transactional_phase_c_default_factories`

Focused tests should cover failure modes that goldens cannot express cleanly:

- compiling a core-only fixture that declares a managed field fails with a
  diagnostic that names the missing managed layer or missing managed field
  support
- compiling a combined fixture with a required layer import removed fails with
  a diagnostic that points at the unresolved resource, collection, matcher, or
  production

Do not duplicate detailed success-path assertions in bespoke tests when the
golden already owns the generated source shape.

## Performance Check

Phase D should not introduce a large parse-and-emit regression merely because
one YIDL source file became several imported files.

During the roll-build, run a lightweight before/after timing probe for the
Phase B or Phase C lifecycle golden. If split layout parse + emit time regresses
by more than about 50%, stop and inspect the import/merge path before tagging
the final slice. This is a guardrail, not a public benchmark.

## Roll-Build

Phase D is a roll-build candidate.

Suggested tag prefix:

```text
txphaseD-layering/
```

Suggested slices:

1. `D1-source-split`: create `lifecycle_core.yidl`,
   `lifecycle_managed.yidl`, `lifecycle_default_factories.yidl`, and the
   combined `lifecycle_base.yidl` entry without changing generated behavior.
2. `D2-core-golden`: add a core-only golden proving plain/initvar/classvar and
   default-facade behavior.
3. `D3-combined-golden`: move the Phase B and Phase C lifecycle goldens to the
   split layout and prove generated output parity.
4. `D4-decorator-import`: update generated runtime artifact production so
   `src/yidl/runtime/_generated_lifecycle_base.py` is still produced from the
   split `lifecycle_base.yidl`; the decorator import remains unchanged.
5. `D5-failure-and-inheritance`: add missing-layer diagnostics, inherited
   generated-class checks, and the lightweight parse/emit timing check.

Stop if concept merge cannot express the split without whole-symbol override
syntax or new YIDL grammar.
