# Pre-implementation design review

This document defines the design-review stage that must happen before routine feature-by-feature implementation proceeds.

The purpose of this stage is empirical model verification. Before scaling up the YIDL compiler and parity effort, we need evidence that the proposed generated architecture can actually represent the lifecycle surface, that the hand-crafted generated example is a sound target, and that the approach does not carry obvious performance regressions across supported Python versions.

This stage is intentionally exploratory. It does **not** define the final normative implementation. It exists to discover design stress, representability gaps, and performance surprises early enough to change direction safely.

For **how** that evidence is gathered first — scenario matrix, adapters, behavioral and performance runners, outputs under `docs/validation/` — follow **`dev-docs/PRE_IMPL_STUDY_DESIGN.md`**.

PRE_IMPL is a hard gate for the main feature cycle in `dev-docs/PROCESS.md`. Routine per-feature implementation work must not begin until this stage is complete. Bootstrap infrastructure may land during this stage, but it does not count as waiving the gate.

## Goals

1. Validate the hand-crafted generated example in `example/generated_factory_sample.py` as a serious architectural target rather than a purely illustrative sketch.
2. Review the field/helper kinds in `pyrolyze.lifecycle` and determine whether each is representable in the current YIDL model.
3. Build preliminary hand-crafted/generated-shape field-type probes where needed to test representability of difficult features.
4. Exercise the generated-shape approach empirically through validation tests and performance checks outside the main source/test paths.
5. Surface design issues before the project becomes committed to a generator structure that is too rigid or too ad hoc.

## Non-goals

- Defining the final production implementation of all field helpers.
- Treating the preliminary hand-crafted field-type probes as normative API or source layout.
- Moving validation experiments into the main `src/` or `tests/` trees prematurely.

## Scope of review

The pre-implementation review should cover at least:

1. **Generated example viability**
   Review `example/generated_factory_sample.py` against `docs/YIDLDesign.md` and identify whether its stores/views/proxy/init/commit patterns are sufficient, missing key semantics, or misleading.

2. **Field/helper representability**
   Review the field/helper kinds in `pyrolyze.lifecycle` and classify each as:
   - readily representable in the current model
   - representable with known generator/runtime work
   - representable only with design changes
   - currently unclear / needs empirical probe

3. **Corner-case pressure**
   Identify which helpers or behaviors are most likely to challenge the model:
   - view semantics
   - init/default/default_factory ordering
   - initvar injection
   - tx-group interactions
   - binding/owned lifecycle sequencing
   - commit hooks / validators
   - local_store / instance-homed behavior

4. **Python-version behavior**
   Run empirical validation on multiple Python versions using `uv` installations to detect major compatibility or performance surprises early.

## Development-only `_yidl.py` bootstrap contract

The first enabling step of the pre-implementation review is a temporary `_yidl.py` bootstrap path. This is a development container and empirical execution path, not the intended long-term delivery model.

The intended long-term model remains ahead-of-time compilation to generated Python and importing the generated module. The `_yidl.py` bootstrap path is deliberately slow and unsupported; it exists to make day-1 empirical validation possible.

### Canonical wrapper form

During this bootstrap phase, the canonical source container is:

```python
import yidl

yidl.embed("""
... YIDL source ...
""", yidl.global_args, globals())
```

Use this exact wrapper form in development-only `_yidl.py` files. Avoid dynamic string construction, multiple embed calls, aliases, or broader mixed-Python patterns during the bootstrap phase.

### Source file naming

Development-only YIDL source containers should be named with the suffix `_yidl.py`.

This suffix is chosen because it is importable by normal Python tooling during the bootstrap phase. It is not a claim that `_yidl.py` is the final or preferred delivery format for YIDL.

### `embed()` contract

For the bootstrap phase, `yidl.embed(source, args, module_globals)` has the following contract:

1. **Compile input**
   The first argument is the authoritative embedded YIDL source string.

2. **Execution**
   The YIDL compiler frontend compiles that source and `exec`s the generated Python using the provided globals dict from the source module.

3. **Arguments**
   The second argument is a special YIDL args object used for the testing/development environment. For now this is `yidl.global_args`.

4. **Globals mutation**
   The generated source executes with the caller-provided module globals as its globals dict. This is expected to populate the module with generated names and other still-to-be-designed generated artifacts.

5. **Return value**
   `embed()` returns `None`.

6. **Idempotence expectation**
   Repeated imports of the same module are expected to be idempotent in normal Python import semantics. The bootstrap path should not require import-order tricks or multiple-pass initialization to stabilize.

7. **Compile failure**
   Compilation failures should raise an appropriate compiler exception with the best available line number and message. The exception path should be improved as needed so line mismatches remain diagnosable.

### `.py` container source-preservation behavior

When the compiler frontend sees a `.py` source container for embedded YIDL, it should set:

`yidl.global_args.pass_source_only = True`

In that mode, the bootstrap path should also preserve source-location metadata by writing:

- `YIDL = "<original source string>"`
- `YIDL_PY_LINE = <line number of the first YIDL source line in the Python file>`

`YIDL_PY_LINE` is the 1-based line offset of the first embedded YIDL line inside the `_yidl.py` file. This exists to support diagnostics, line remapping, and later debugging of line-number mismatches.

### Status and warning text

Every `_yidl.py` development container should carry a prominent warning comment near the top to make the status of this path explicit.

Recommended wording:

```python
# yidl.embed is the SLOW and UNSUPPORTED path.
# Compile this YIDL file ahead of time and import the generated module instead.
```

This warning is intentional. Users of the bootstrap path are choosing a temporary development mechanism, not a stable supported runtime workflow.

### Accepted bootstrap risks

The bootstrap contract intentionally accepts several temporary risks:

- use of `globals()` as the generated execution environment
- a mutable `yidl.global_args` channel for development/testing behavior
- import-time compile/exec cost
- a Python wrapper format that is not the intended long-term YIDL delivery model

These are accepted only because the path is explicitly temporary, slow, and unsupported.

### What may change later

The following are explicitly expected to change after the bootstrap phase:

- replacement of runtime compile-on-load with ahead-of-time compilation
- reduction or elimination of `globals()` dependence
- narrowing or removal of `yidl.global_args`
- movement from `_yidl.py` containers toward a cleaner long-term source format
- richer compiler exceptions such as an improved `YidlCompileError` carrying source-line context

## Required outputs

The design review stage should produce:

1. A reviewed and, if needed, corrected hand-crafted generated example in `example/generated_factory_sample.py`.
2. A written representability assessment covering lifecycle field/helper kinds and notable edge cases.
3. Preliminary hand-crafted/generated-shape probes for difficult helper kinds where simple review is not enough.
4. Validation tests under `docs/validation/`.
5. Performance checks under `docs/validation/`.
6. Recorded findings in feature or review docs when the model appears insufficient.

## Validation artifact location

Empirical validation work for this stage should live under `docs/validation/`, not in the main source or parity test trees.

That area may contain:

- validation-only hand-crafted/generated-shape probes
- validation tests
- performance tests / scripts
- notes on Python-version behavior

Keep these artifacts clearly marked as validation work. They are intended to de-risk the architecture, not to silently become the production implementation.

## Suggested structure under `docs/validation/`

Suggested categories:

- `docs/validation/generated_example/`
  Validation focused on `example/generated_factory_sample.py`.
- `docs/validation/field_representability/`
  Probes for helper/field kinds that stress the model.
- `docs/validation/perf/`
  Performance checks and Python-version comparison scripts/tests.

Exact filenames can evolve, but validation artifacts should remain outside `src/` and `tests/` until promoted deliberately.

## Recommended process

1. **Implement the `_yidl.py` bootstrap path**
   Build the temporary fake compile-on-load machinery described above so empirical YIDL work can run immediately.

2. **Review the generated factory sample**
   Audit `example/generated_factory_sample.py` as if it were the first real generated target.

3. **Review lifecycle field/helper kinds**
   Walk the `pyrolyze.lifecycle` helper surface and map each kind to the current YIDL model.

4. **Mark representability status**
   For each helper kind, record whether it is already representable, needs targeted generator/runtime work, or appears to require design changes.

5. **Build empirical probes**
   For helper kinds or interactions that are unclear, build small hand-crafted/generated-shape probes under `docs/validation/`.

6. **Run empirical tests**
   Add validation tests for the generated example and the representability probes under `docs/validation/`.

7. **Run performance checks**
   Use `uv`-managed Python installations to compare behavior and rough performance across selected Python versions.

8. **Summarize findings**
   Record inadequacies, trade-offs, and recommendations before the main implementation process depends on them.

## Python versions

Python-version strategy is still preliminary and should be treated as part of this review stage.

At minimum:

- choose a small initial set of Python versions to compare with `uv`
- run the validation/performance checks for the generated example path on those versions
- record any semantic or performance deltas large enough to influence design decisions

The exact version matrix can evolve, but version assumptions should not remain implicit.

## Decision rule

Do not treat successful hand-crafted parity work alone as sufficient readiness for broader implementation. The project should first establish that:

1. the generated example is credible,
2. the lifecycle helper surface appears representable in the model,
3. difficult helpers have at least preliminary empirical probes where needed,
4. no major Python-version surprises have already invalidated the approach.

If this stage reveals major representability or performance concerns, classify them using the normal design-issue categories:

- `implementation_bug`
- `design_gap`
- `design_conflict`

and update the follow-on plans before feature work continues.

## Relationship to the main process

This review stage comes before routine feature-slice work becomes the dominant mode.

After the review stage:

- the main process in `dev-docs/PROCESS.md` should reference this document
- the code generator should advance continuously with each feature slice
- empirical validation under `docs/validation/` may continue when a slice raises new representability or performance concerns
