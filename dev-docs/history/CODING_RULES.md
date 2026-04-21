# YIDL ↔ lifecycle parity — coding rules

## a) Where files live

| Kind | Location |
|------|----------|
| YIDL spec (grows per feature) | `spec/lifecycle_baseline.yidl` |
| Per-feature design notes | `dev-docs/<feature_slug>/design.md` (slug matches `IMPLEMENTATION_ORDER` in `lifecycle_field_catalog.py`, e.g. `managed_single_group`) |
| Comprehensive hand-crafted “generated” baseline | `src/yidl/handcrafted/lifecycle_sample.py` (single module augmented each cycle; split only if it becomes unmanageable) |
| Feature-focused hand-crafted baseline shape | `src/yidl/handcrafted/slices/<feature_slug>.py` |
| Baseline context class(es) under test | `src/yidl/baseline/lc_baseline.py` — `LCBaseline` and any sibling classes referenced from tests |
| Shared parity test utilities | `tests/baseline/conftest.py`, `tests/baseline/_impl_switch.py` |
| Parity tests | `tests/baseline/test_<feature_slug>.py` |
| Catalog of lifecycle helpers / order | `dev-docs/lifecycle_field_catalog.py`, checklist `dev-docs/IMPL_PROGRESS.md` |
| Runtime vs codegen split + test porting | `dev-docs/RuntimeExtractionPlan.md` |
| Generator requirements / trade-offs | `dev-docs/CodegenRequirements.md` |
| Pre-implementation empirical review | `dev-docs/PRE_IMPL_DESIGN_REVIEW.md` |
| Validation-only experiments/tests/perf | `docs/validation/` |

**Runtime ownership direction:** YIDL is intended to become the authoritative implementation and runtime owner for this system. The relevant lifecycle transaction/runtime semantics should be re-homed into YIDL-owned runtime modules over time so `pyrolyze` can eventually depend on YIDL, not the other way around.

**Current phase constraint:** during this phase, do **not** edit files in `pyrolyze/`. This is a hard process/coding rule for the current phase, not a suggestion. Treat `pyrolyze.lifecycle` as a read-only reference backend used for parity comparison, bug discovery, and selective lifecycle-only skips.

**Per-feature runtime re-home rule:** `pyrolyze.lifecycle` may be used as the read-only reference backend for this phase, but it is not the long-term implementation dependency. On a per-feature basis, any runtime behavior needed by the slice must be copied, re-homed, or redeveloped into YIDL-owned runtime modules unless that work is explicitly deferred in the feature design doc.

**Imports:** Hand-crafted code should call the same public pyrolyze APIs the generated module will eventually rely on (no private `pyrolyze.lifecycle` symbols unless explicitly agreed in the feature design doc).

**Reference backend bugs:** `pyrolyze.lifecycle` is the reference, not an oracle. When parity work uncovers a confirmed lifecycle bug, document it in the feature design doc and use one normalized lifecycle-only skip mechanism from the shared baseline test helpers. Prefer one shared helper/library path for all such skips so backend-specific exceptions are centralized and auditable.

**Continuous code generation:** the generator is part of the implementation path for every slice. Hand-crafted baseline code is a readable target and debugging aid, not permission to defer generator work until the end.

**Validation separation:** empirical model-verification work for the generated example, representability probes, and performance checks belongs under `docs/validation/`, not the main `src/` or parity `tests/` trees, unless and until it is deliberately promoted.

**Bootstrap container policy:** during the pre-implementation phase, development-only YIDL source containers should use the `_yidl.py` suffix and the canonical `yidl.embed(..., yidl.global_args, globals())` wrapper described in `dev-docs/PRE_IMPL_DESIGN_REVIEW.md`. This path is slow and unsupported; normal use should compile YIDL ahead of time and import the generated Python.

## b) Code style

- Match surrounding yidl code: type hints and no machine-specific paths in committed files.
- Hand-crafted “generated” code should **look like** future compiler output: one factory or one module, spec dict, explicit stores/views/proxy where applicable—avoid reintroducing descriptor tables from today’s `lifecycle.py`.
- Maintain both levels of coverage: the comprehensive baseline should accumulate interaction behavior, and each feature should have a focused hand-crafted/generated-shape target that is small enough to review on its own.
- The generator should continue to emit the currently supported subset throughout development; unsupported features must fail explicitly and locally.
- Tests: prefer explicit assertions over golden strings unless testing codegen output.

## b1) Design guard rails

Do not treat every parity failure as a coding bug. YIDL baseline work is expected to surface weaknesses in the design, especially in early slices.

Use these classifications consistently in feature design notes:

- `implementation_bug`
- `design_gap`
- `design_conflict`

A patch should be presumed to require design discussion, not just coding, when any of the following are true:

- it introduces a new generic flag, callback, mode, or escape hatch to make one slice pass
- it requires special-case behavior in more than one feature
- it changes the conceptual meaning of an already-completed slice
- it depends on private `pyrolyze.lifecycle` machinery that the generated implementation should not inherit
- it materially changes the generated architecture described in `docs/YIDLDesign.md`
- it changes the generator pipeline, emission strategy, or unsupported-feature behavior without updating `dev-docs/CodegenRequirements.md`

For `design_gap` and `design_conflict` cases:

- record a short precis in `dev-docs/<feature_slug>/design.md`
- present 2-3 remedy options, not just one implementation path
- do not merge the workaround as if it were the settled architecture
- do not check off the feature in `IMPL_PROGRESS.md` until the design issue is resolved or explicitly deferred

Prefer clarifying or simplifying the model over adding ad hoc switches. A narrow, coherent baseline is better than broad support implemented through accumulating exceptions.

## c) Exit criteria (per feature)

A feature is **done** when all of the following hold:

1. **YIDL** — `spec/lifecycle_baseline.yidl` contains the transducer(s) / inputs / surfaces needed for this slice (even if the compiler does not consume them yet).
2. **Design** — `dev-docs/<feature_slug>/design.md` describes support code, hooks in the YIDL transducer, how the hand-crafted Python uses `TransactionManager` / views, generator implications for the slice, any confirmed `pyrolyze.lifecycle` bug that requires lifecycle-only skips, and any `design_gap` / `design_conflict` discovered during the slice.
3. **Codegen requirements** — `dev-docs/CodegenRequirements.md` reflects any new generator stage, trade-off, unsupported-feature rule, or emitted-architecture decision introduced by the slice.
4. **Design status** — no unresolved `design_gap` or `design_conflict` remains for the slice unless it is explicitly deferred with documented rationale and does not invalidate the slice’s claimed completion.
5. **YIDL runtime ownership** — any runtime component needed by the slice has a YIDL-owned implementation or an explicitly documented deferral in the feature design doc; the slice is not considered done solely because it works against `pyrolyze.lifecycle`.
6. **Hand-crafted baseline** — `src/yidl/handcrafted/lifecycle_sample.py` (or agreed module) implements the slice in generated shape inside the comprehensive baseline.
7. **Hand-crafted feature shape** — a focused hand-crafted/generated-shape target exists for the slice at `src/yidl/handcrafted/slices/<feature_slug>.py` when needed to keep the intended emitted structure reviewable in isolation.
8. **Generator** — the generator still emits runnable output for the currently supported subset, and the slice has advanced or at least preserved generator support intentionally rather than leaving it behind.
9. **Tests / verification** — `tests/baseline/test_<feature_slug>.py` encodes behavior with both slice-focused coverage and comprehensive-baseline interaction coverage where relevant; it passes with `LC_PARITY_IMPL=lifecycle`, `LC_PARITY_IMPL=handcrafted`, and `LC_PARITY_IMPL=generated`, and the agreed generator verification for the supported subset passes as well.
10. **Lifecycle skip normalization** — if the `lifecycle` backend is skipped for a confirmed reference bug, that skip is implemented through the shared parity test helper mechanism rather than bespoke per-test logic.
11. **Reference** — `LCBaseline` (or documented sibling) exposes the same observable surface the tests use for the handcrafted path.

Until the handcrafted backend exists, tests may `pytest.skip` for `LC_PARITY_IMPL=handcrafted` **only** if the skip message names the blocking prerequisite feature.

Lifecycle-only skips for confirmed reference bugs should identify the bug succinctly, apply only to the `lifecycle` backend, and be routed through shared helpers in `tests/baseline/` so the same mechanism is reused across all slices.

A test failure is not sufficient evidence that the implementation is wrong. If the failure suggests architectural drift or model ambiguity, classify it first, then decide whether code changes should proceed.
