# PRE_IMPL — design checklist

This document captures **what must be designed** for the pre-implementation
stage described in `dev-docs/PRE_IMPL_DESIGN_REVIEW.md`.

Its purpose is to keep PRE_IMPL centered on the right question:

**Is `example/generated_factory_sample.py` a credible generated target,
semantically and performance-wise, strongly enough to let dominant feature work
begin?**

It complements `PRE_IMPL_DESIGN_REVIEW.md`; the normative process and bootstrap
contract details remain there.

**Gate:** Routine per-feature work in `dev-docs/PROCESS.md` must not dominate
until PRE_IMPL outputs are satisfied. See PRE_IMPL for the hard gate and
required outputs list.

**Study execution (matrix):** `dev-docs/PRE_IMPL_STUDY_DESIGN.md` — scenario
matrix, harness layout, behavioral vs performance layers, staged helper
coverage, and exit criteria for validating mechanisms against lifecycle
semantics.

---

## 1. Generated factory sample: empirical credibility

This is the first question of PRE_IMPL.

Design / review:

- **`example/generated_factory_sample.py` is the empirical target** — treat it
  as the first serious candidate generated shape, not as a loose illustration.
- **Audit against `docs/YIDLDesign.md`** — stores, views, proxy, init phases,
  commit/rollback, closure capture, physical/logical store separation, and any
  layout expectations described there.
- **Credibility decision** — decide whether the sample is credible enough to be
  the first real generator target.
- **Gap list** — for each gap, classify it as:
  - must be corrected before PRE_IMPL is complete
  - acceptable deferral to the first feature slice
  - mismatch in `YIDLDesign.md` rather than in the sample
- **Target-shape reconciliation** — update the sample or `YIDLDesign.md` so
  they do not silently disagree.

This section is the center of PRE_IMPL. Other PRE_IMPL questions exist
primarily to support this empirical review.

---

## 2. Performance and empirical review

Design:

- **What to measure** — at minimum, decide what empirical checks matter for the
  generated factory sample:
  - import/compile cost
  - cold vs warm load
  - generated object construction smoke
  - any obvious commit/rollback hot-path smoke worth measuring in PRE_IMPL
- **Version set** — choose a small Python version matrix to exercise under
  `uv`.
- **Thresholds / judgments** — record what counts as “acceptable for PRE_IMPL”
  versus “serious enough to trigger design concern.” Qualitative thresholds are
  acceptable if written down.
- **Validation location** — performance checks and empirical sample validation
  belong under `docs/validation/`.

The point here is not full benchmarking. It is to discover whether the
generated sample shape has obvious semantic or performance problems before
broader implementation begins.

---

## 3. Representability of `pyrolyze.lifecycle` in the YIDL model

Design (written artifact):

- **Per-helper classification** — for each lifecycle field helper and important
  edge case, assign one of:
  - *readily representable*
  - *representable with known generator+runtime work*
  - *needs design change*
  - *unclear → empirical probe*
- **Corner cases** — map PRE_IMPL corner-case pressure
  (views, init/default/default_factory ordering, initvar injection, tx groups,
  binding/owned sequencing, hooks/validators, local_store / homed fields) to
  YIDL constructs or an explicit “not in v1” decision.

Store this as a durable doc and link it from PRE_IMPL / PROCESS when complete.

---

## 4. Empirical probes and validation layout

Design:

- **Layout under `docs/validation/`** — use the suggested split where helpful:
  `generated_example/`, `field_representability/`, `perf/`. Define what each
  subtree may import and how tests are invoked (for example `uv run`, pytest
  from repo root).
- **Probe pattern** — decide the smallest repeatable shape for difficult-helper
  probes (one stress axis per probe vs one large file).
- **Promotion** — probes stay under `docs/validation/` until deliberately
  promoted; no silent drift into `src/` or `tests/baseline/`.

---

## 5. Minimal bootstrap machinery needed for PRE_IMPL

Bootstrap is an enabler for empirical review, not the conceptual center of
PRE_IMPL.

Design:

- **`embed(source, args, module_globals)`** — semantics per
  `PRE_IMPL_DESIGN_REVIEW.md` § `embed()` contract: compile input, `exec` into
  the caller’s `globals`, return `None`, idempotent import behavior, compile
  failures as a proper exception with line/message strategy.
- **`yidl.global_args`** — which flags exist for bootstrap (at minimum
  `pass_source_only` for `.py` containers), mutability rules, and expectations
  for concurrent use.
- **`.py` / `_yidl.py` path** — when `pass_source_only` is set, how `YIDL` and
  `YIDL_PY_LINE` are injected into the module namespace for diagnostics; whether
  the compiler or the embed wrapper computes the 1-based line offset.
- **Canonical wrapper** — enforce the documented
  `yidl.embed("""...""", yidl.global_args, globals())` shape and document what
  is out of bounds during PRE_IMPL (dynamic string construction, multiple embed
  calls, aliases).
- **Minimal frontend pipeline** — parse embedded YIDL string → typed AST (and
  any agreed IR) → what gets `exec`’d for day-one validation. This can be
  subset-only if documented.
- **Source container detection** — how the frontend knows it is compiling from
  a `_yidl.py` / `.py` embed vs a standalone `.yidl` file.
- **Compile errors** — minimal exception type and fields for failures.
- **Sunset** — one short paragraph on what success for PRE_IMPL implies for
  shrinking or removing this path later.

---

## 6. Forward references needed for the first real generator

Design only what blocks empirical validation and the first post-PRE_IMPL slice:

- **Harvester / spec shape** — short note on what inputs the first real
  generator will assume (for example spec dict shape, field list), even if the
  harvester is not implemented in PRE_IMPL.
- **First generated subset** — what the first real generator is expected to
  emit immediately after PRE_IMPL, assuming the generated factory sample
  survives review.

Do not let this section expand into full generator design;
`CodegenRequirements.md` owns that broader work.

---

## 7. PRE_IMPL completion (“done”) checklist

Align PRE_IMPL **Decision rule** with **Required outputs**:

| Required output (PRE_IMPL) | Design / completion question |
|----------------------------|-------------------------------|
| Reviewed `example/generated_factory_sample.py` | Is it **credible** as the first codegen target? List required follow-ups. |
| Performance checks | Version matrix run for the generated sample path; deltas noted if they affect design. |
| Written representability assessment | Classification table complete? Every *unclear* row either has a probe or a documented deferral. |
| Preliminary probes | Which *unclear* rows are covered under `docs/validation/`? |
| Validation tests | How are they run locally / in CI? |
| Recorded findings | One summary: open risks, `design_gap` / `design_conflict` candidates, recommendations before dominant feature work. |

Do not treat hand-crafted parity alone as sufficient readiness.

---

## 8. Relationship to `CodegenRequirements.md`

PRE_IMPL is **empirical / model credibility first**, and bootstrap enablement
second. `dev-docs/CodegenRequirements.md` captures broader generator IR, stages,
determinism, and migration. During PRE_IMPL, only decide or stub what blocks
empirical validation, bootstrap, or representability; full answers to every
CodegenRequirements topic may extend past PRE_IMPL if documented.

---

## 9. After PRE_IMPL

Per `dev-docs/PROCESS.md`, the next ordered implementation slice is
`managed_single_group`, using the full per-feature cycle (YIDL spec, design
notes, handcrafted baseline + slices, generator, three-way `LC_PARITY_IMPL`,
exit criteria in `dev-docs/CODING_RULES.md`).
