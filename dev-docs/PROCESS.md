# Development process: YIDL lifecycle baseline + continuous generator

End state: a YIDL spec fully describes field helpers + decorator behavior; the generator continuously emits the currently supported subset during development; parity with `pyrolyze.lifecycle` for the exercised surface.

## Support code review

1. Analyze `pyrolyze/src/pyrolyze/lifecycle.py` for **runtime** code (transaction orchestration, shared protocols, exceptions) vs **decoration-time** code (`managed_context`, `LCKind`, descriptor tables). Identify tests that exercise the runtime surface.
2. Enumerate runtime support features and **correlate** which **field helpers** (`managed`, `binding`, …) depend on each.
3. Record findings and adoption phases in **`dev-docs/RuntimeExtractionPlan.md`** (living document; update when lifecycle changes).

Details, tables, and test-porting notes: **`RuntimeExtractionPlan.md`**.

## Current phase constraint

During this phase, do **not** edit files under `pyrolyze/`.

`pyrolyze.lifecycle` is a read-only reference backend for support-code review, parity comparison, representability review, and lifecycle-bug discovery only. If reference behavior is wrong, document it and use the normalized lifecycle-only skip path; do not “fix” the issue by patching `pyrolyze/` during this phase.

## Pre-implementation design review

Before routine feature-slice implementation becomes the dominant workflow, complete the empirical design review described in **`dev-docs/PRE_IMPL_DESIGN_REVIEW.md`**.

**First concrete PRE_IMPL work:** execute the matrix study in **`dev-docs/PRE_IMPL_STUDY_DESIGN.md`** — scenario matrix, shared harness, behavioral and performance checks comparing reference `pyrolyze.lifecycle` to hand-crafted generated strategies under `docs/validation/`. That document is where we validate the mechanisms we will use to achieve lifecycle semantics in a comparable matrix.

That review (and the study) is the place to:

- implement the development-only `_yidl.py` fake compile-on-load bootstrap path as the first enabling step, so empirical YIDL work can run on day 1
- validate `example/generated_factory_sample.py` as an architectural target
- review whether `pyrolyze.lifecycle` field/helper kinds are representable in the current model
- create preliminary hand-crafted/generated-shape probes for difficult helpers where needed
- run validation and performance checks under `docs/validation/`
- explore Python-version behavior using `uv`-managed installations

This review stage is intentionally empirical and non-normative. Its purpose is to challenge the model before routine implementation pressure makes design drift harder to correct.

The `_yidl.py` bootstrap path is an enabling deliverable of this stage. It provides the temporary fake compile-on-load machinery needed to embed YIDL source in Python containers during development. It is **not** a prerequisite for starting the **PRE_IMPL Study Design** matrix (reference lifecycle vs hand-crafted generated strategies in `docs/validation/`); land bootstrap when probes or workflows need YIDL-in-container, in line with **`dev-docs/impl-docs/pre_impl_design.md`** ordering.

PRE_IMPL is a hard gate. Routine per-feature implementation work must not begin until this stage is complete. Any bootstrap work that lands before PRE_IMPL completion is provisional and does not waive the gate for the main feature cycle.

## Generator prerequisite

Before routine per-feature generator work proceeds, maintain a detailed generator requirements/design document in **`dev-docs/CodegenRequirements.md`**.

That document defines the requirements, trade-offs to prefer, trade-offs to avoid, and open design decisions for the code generator. It exists to prevent feature-by-feature implementation pressure from pushing the generator into an accidental architecture.

Update **`CodegenRequirements.md`** whenever a slice:

- introduces a new generator stage or intermediate representation
- chooses a meaningful codegen trade-off
- requires a new unsupported-feature strategy
- changes the intended emitted architecture

## Design escalation path

The first slices are expected to challenge the adequacy of the current design. We must not automatically classify every failure as an implementation bug. Some failures will indicate that the YIDL model, compiler pipeline, or generated-shape assumptions need revision before more code is written.

Classify significant failures into one of three buckets:

1. **implementation_bug** — the design is still coherent; the parser, hand-crafted baseline, support code, or tests failed to implement it correctly.
2. **design_gap** — the design does not specify the behavior precisely enough; multiple reasonable implementations exist.
3. **design_conflict** — the design as written appears incompatible with required behavior, with another part of the design, or with the intended generated architecture.

Treat a failure as a potential **design_gap** or **design_conflict** when any of the following hold:

- the same workaround pattern appears in more than one feature slice
- a feature cannot be expressed cleanly in YIDL without leaking Python/runtime internals into the spec
- the hand-crafted/generated-shape target must rely on private or decoration-time machinery that the eventual generator should not depend on
- passing tests would require behavior that is inconsistent across surfaces, stores, initialization phases, or transaction phases
- the intended generated code shape drifts materially from `docs/YIDLDesign.md`
- the smallest apparent remedy is “add another mode/flag/hook” rather than clarifying the model

When a slice hits a possible design issue, stop feature work long enough to produce a short design precis in `dev-docs/<feature_slug>/design.md` containing:

1. **Symptom** — what failed, under which backend(s), and in what scenario.
2. **Why this may be design, not implementation** — which model assumption appears strained.
3. **Minimal reproduction** — the smallest code/test shape that demonstrates the problem.
4. **Design tension** — which desired properties are in conflict.
5. **Options** — 2-3 plausible remedies.
6. **Recommendation** — preferred direction and its tradeoffs.
7. **Decision needed** — whether work should pause pending review.

Do not check off the feature in `IMPL_PROGRESS.md` while a `design_gap` or `design_conflict` remains unresolved.

Temporary workarounds are allowed only when they are explicitly labeled as temporary, linked to the precis, and do not silently redefine the intended architecture.

## Test strategy

Coverage is tracked at two levels throughout the project:

1. **Comprehensive baseline** — a shared “all-up” baseline context/class and companion tests that accumulate cross-feature interactions as the baseline grows.
2. **Per-feature slice** — focused hand-crafted/generated-shape code and tests for the current helper or behavior under review.

The comprehensive baseline exists because lifecycle field specs are not independent: defaults, views, tx groups, hooks, bindings, and initvar injection can interact in ways that isolated tests will miss. Per-feature tests remain required so each slice has a small, reviewable target and a clear generator contract.

Code generation is also tracked continuously. The hand-crafted baseline is a target shape and debugging aid, not a substitute for advancing the generator.

## Per-feature cycle

For each row in `IMPL_PROGRESS.md` (in order), after the pre-implementation design review has completed and established a credible starting direction, and without editing files under `pyrolyze/` during this phase:

1. Extend **`spec/lifecycle_baseline.yidl`** with the transducers / behaviors needed for the slice
  a. run the yidl compiler skeleton and confirm it is correctly parsed into the AST
  b. if parsing, modeling, or emitted-shape work reveals a possible `design_gap` or `design_conflict`, stop and record the issue using the **Design escalation path** before continuing
2. Add **`dev-docs/<feature_slug>/design.md`**: support code required, mapping to YIDL hooks, exit criteria for this slice, generator implications for the supported subset, and any known **reference-backend** (`pyrolyze.lifecycle`) bugs that affect parity. If the slice touches shared runtime, update **`RuntimeExtractionPlan.md`** and note any **`pyrolyze/tests/test_api_lifecycle.py`** cases to port into `tests/baseline/test_<feature_slug>.py`.
3. Before substantial implementation proceeds, confirm whether the slice remains in `implementation_bug` territory or requires design review. If the issue remains a `design_gap` or `design_conflict`, pause coding until the direction is agreed.
4. Identify which runtime pieces for the slice still live only in `pyrolyze.lifecycle`, then copy, re-home, or redevelop the required subset into YIDL-owned runtime modules unless the feature design doc records an explicit deferral.
5. Augment the **comprehensive hand-crafted baseline** in **`src/yidl/handcrafted/lifecycle_sample.py`** with the code shape you expect the generator to emit as the global baseline grows.
6. Add or extend a **feature-focused hand-crafted baseline shape** for the slice under **`src/yidl/handcrafted/slices/<feature_slug>.py`** so the intended generated structure is reviewable in isolation, even when the comprehensive baseline already covers it transitively.
7. Update the **generator** so it continues to emit runnable output for the currently supported subset, including this slice if the required generator design decisions are ready. Unsupported parts must fail explicitly rather than silently degrading.
8. Add or extend generator verification for the slice: generated source/shape checks, generated-runtime execution, or other agreed proof that the generated subset still works.
9. Add **`tests/baseline/test_<feature_slug>.py`**: include focused per-feature assertions and, where the slice has meaningful interactions, coverage against the comprehensive baseline class as well. Implementation is selected by **`LC_PARITY_IMPL`** (`lifecycle` | `handcrafted` | `generated`).
10. If the reference backend has a confirmed bug for this behavior, register a **normalized lifecycle-only skip** through the shared baseline test support (same mechanism, preferably same code library/helpers, for all such skips). Document the bug and scope in **`dev-docs/<feature_slug>/design.md`**; do not scatter ad hoc `pytest.skip` logic through individual tests.
11. Run tests with **`LC_PARITY_IMPL=lifecycle`** (reference behavior, minus documented lifecycle-only skips).
12. Run tests with **`LC_PARITY_IMPL=handcrafted`** (baseline implementation).
13. Run tests with **`LC_PARITY_IMPL=generated`** (compiler/generated implementation for the currently supported subset).
14. Run any additional agreed generator verification for the current supported subset.
15. Confirm **exit criteria** in `CODING_RULES.md` before checking the box in `IMPL_PROGRESS.md`.

## After all boxes are checked

- Expand generator coverage until the generated path can replace the remaining hand-crafted baseline for the exercised surface.
- Replace or shrink hand-maintained `lifecycle_sample.py` with generated output in CI.
- Long term: optional path toward a generated `lifecycle`-equivalent module inside pyrolyze (separate rollout).

## Environment variable

| Value | Meaning |
|-------|---------|
| `lifecycle` (default) | Tests build contexts with `@managed_context` / helpers from `pyrolyze.lifecycle`. |
| `handcrafted` | Tests use types/factories from `yidl.handcrafted.lifecycle_sample` + `yidl.baseline.lc_baseline`. |
| `generated` | Tests use the YIDL compiler/generated path for the currently supported subset. Unsupported features must fail explicitly rather than silently falling back. |

Example:

```bash
LC_PARITY_IMPL=lifecycle uv run --with pytest pytest tests/baseline -q
LC_PARITY_IMPL=handcrafted uv run --with pytest pytest tests/baseline -q
LC_PARITY_IMPL=generated uv run --with pytest pytest tests/baseline -q
```
