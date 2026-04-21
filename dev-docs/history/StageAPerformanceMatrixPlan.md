# Stage A Performance Matrix Plan

## Purpose

This document is the locked execution plan for the Stage A performance review
(`PRE_IMPL_STUDY_IMPL_PLAN.md §Phase 4`). It promotes the informal sketch in
`PRE_IMPL_STUDY_DESIGN.md §5, §9, §10` to the same level of rigor applied to
the init-detection micro-bench in `OptimalReferencePlan.md §Phase 3`, so the
Stage A comparison between `lifecycle` and `generated_strategy_a` produces
decision-quality numbers on first run.

It exists because:

- `PRE_IMPL_STUDY_DESIGN.md §9` deliberately defers tool choice, batch
  structure, GC policy, DCE prevention, and per-scenario normalisation to
  PRE_IMPL. Without a locked plan, Phase 4 will be improvised per-runner and
  the numbers will not be comparable across iterations, candidates, or Python
  versions.
- Phase 4's scenario matrix is large (operations × field shapes × access
  patterns × 2+ subjects × Python matrix). Without a canonical-point
  discipline the full product is not runnable per iteration.
- The init-detection micro-bench and the Stage A macro-bench will share the
  `docs/validation/perf/` tree; without naming and reporting discipline they
  will be confused for each other in findings.

This plan is scoped to **Stage A**. It does not cover Stage B / C / D helper
sets, multi-group transactions, binding resources, or any helper that is not
already listed in `PRE_IMPL_STUDY_DESIGN.md §6.1`.

Read alongside:

- `dev-docs/PRE_IMPL_STUDY_DESIGN.md` — §5 operations/field shapes/access
  patterns, §9 perf mechanism, §10 Python matrix; this plan fills in every
  deferred choice.
- `dev-docs/PRE_IMPL_STUDY_IMPL_PLAN.md` — §0a perf scaffold, §0b version
  matrix, §0c scenario contract, §Phase 4 exit gate; this plan is the
  detailed spec for Phase 4.
- `dev-docs/OptimalReferencePlan.md` §Phase 3 — init-detection micro-bench;
  uses the same tree but measures a different thing. This plan and that
  plan must both produce clearly-labelled findings files so neither is
  mistaken for the other.
- `docs/validation/study/CONTRACT.md` — existing semantic harness contract;
  the perf harness reuses `StudySubject` and adds a parallel perf-scenario
  surface rather than overloading `ScenarioFn`.
- `docs/validation/perf/version_matrix.py` — authoritative Python version
  matrix; this plan imports it.

## Relationship to other plans

| Decision | Owned by |
|----------|----------|
| Python version matrix values | `docs/validation/perf/version_matrix.py` (PRE_IMPL §0b). This plan imports, never hard-codes. |
| Perf scaffold layout under `docs/validation/perf/` | PRE_IMPL §0a. This plan adds files under that scaffold. |
| `StudySubject` surface | `study/CONTRACT.md` (PRE_IMPL §0c). This plan does not modify it. |
| Init-detection-mechanism choice | `OptimalReferencePlan.md §Phase 3`. This plan consumes the winner via the strategy-A factory; it does **not** re-evaluate init detection. |
| Stage A scenario matrix (operations, field shapes, access patterns) | `PRE_IMPL_STUDY_DESIGN.md §5, §6.1`. This plan turns those into timed scenarios. |
| What "acceptable performance" means for Stage A | `PRE_IMPL_STUDY_DESIGN.md §13`. This plan produces numbers; the go/no-go judgment stays in the PRE_IMPL findings. |

## Execution order

Within `PRE_IMPL_STUDY_IMPL_PLAN.md`:

- §0a, §0b, §0c, §0d must already be complete (perf scaffold, version matrix,
  scenario contract, adapter skeletons).
- §Phase 2 must have the lifecycle reference classes for Stage A.
- §Phase 3 must have `generated_strategy_a` implementing Stage A, with its
  init-detection mechanism set by `OptimalReferencePlan.md §Phase 3` findings.
- This plan drives §Phase 4a, 4b, 4c.

Within this plan the order is **(1) harness → (2) canonical-point sweep →
(3) full-matrix sweep → (4) findings**. Step (2) is the primary development
loop; step (3) runs once at phase exit.

## Subjects under test

Stage A subjects:

- **`lifecycle`** — `docs/validation/study/lifecycle_backend.py` wrapping
  `pyrolyze.lifecycle` reference classes. Semantic ground truth.
- **`generated_strategy_a`** — `docs/validation/study/generated_strategy_a_backend.py`
  wrapping the first generated-only hand-crafted class, shaped by
  `OptimalReferencePlan.md §Phase 2`.

Future strategy variants (`generated_strategy_b`, etc.) are added by copying
their adapter into the tree (per `PRE_IMPL_STUDY_DESIGN.md §3`) and registering
them with the perf runner; no other plan edits required. This plan does not
author them.

## Scenario model

### Semantic vs perf scenarios

Semantic scenarios already exist as `ScenarioFn = Callable[[StudySubject], ScenarioResult]`
in `docs/validation/study/contract.py`. They run end-to-end once, asserting on
`ScenarioResult.value`. They are the correctness layer.

Perf scenarios have a different shape because timing a single call is not
statistically useful and because setup cost must be excluded from the timed
region:

```python
@dataclass(frozen=True)
class PerfScenario:
    key: str                          # stable identifier used in reports
    operation: str                    # one of OPERATIONS; see §below
    field_shape: str                  # one of FIELD_SHAPES; see §below
    access_pattern: str               # one of ACCESS_PATTERNS; see §below
    setup: Callable[[StudySubject], PerfState]
    step: Callable[[PerfState], int]   # returns DCE-resisting sink integer
    teardown: Callable[[PerfState], None] = lambda _: None
    steps_per_batch: int              # N; sized so one batch ≈ 100ms wall
```

`PerfState` is a mutable dataclass specific to each scenario carrying the
class under test, live instance(s), transaction manager, any pre-populated
input arrays, and the running XOR accumulator (see DCE prevention below).

`step(state)` must return an `int` derived from observed program state so the
driver can XOR-fold into the accumulator. Writes must produce an observable
post-condition the accumulator reads (e.g. the next-step input depends on the
last-step output). See `Dead-code-elimination prevention`.

### Operations

Per `PRE_IMPL_STUDY_DESIGN.md §5.1`, Stage A exercises seven operations. This
plan locks each as a named `operation` string:

| `operation` | Description | Timed region |
|-------------|-------------|--------------|
| `construct` | `cls(transaction_manager=txm)` | One construction per step. Instance discarded after `step` returns the DCE sink. |
| `committed_read` | Read a field outside any active transaction | One attribute read per step |
| `working_read` | Read a field inside an active transaction after a prior write | One attribute read per step |
| `managed_write` | Assign a field inside an active transaction | One attribute write per step |
| `commit` | Commit a transaction that wrote one field | One full `with txm.begin(): ctx.value = X` round-trip per step |
| `rollback` | Roll back a transaction that wrote one field | One full `with txm.begin() as tx: ctx.value = X; tx.rollback()` (or equivalent) per step |
| `default_factory_init` | Construct an instance where at least one field is `default_factory(self)`-initialised | One construction per step, exercising 3-phase init |

`commit` and `rollback` are intentionally full round-trips rather than "just
the commit call", because the cost of `begin()` + one write + `commit()` is
the unit the generated model is trying to make cheap. Sub-phase timings
(begin-only, write-only, commit-only) are not worth the harness complexity at
Stage A; they become interesting only if the combined number reveals a cliff.

### Field shapes

Per `PRE_IMPL_STUDY_DESIGN.md §5.2` and `§6.1`, Stage A covers four shapes.
This plan locks each:

| `field_shape` | Definition |
|---------------|------------|
| `scalar_1` | One managed `int` field (`value`) |
| `scalar_2` | Two managed `int` fields (`a`, `b`); all per-field ops touch `a` |
| `dependent_init` | Two fields where the second's `default_factory(self)` reads the first; perf scenarios hitting `default_factory_init` and `construct` must use this shape |
| `commit_rollback` | One managed `int` field, same as `scalar_1`; dedicated label so `commit` and `rollback` operations report under a shape name rather than reusing `scalar_1` and causing ambiguity in the report |

### Access patterns

Per `PRE_IMPL_STUDY_DESIGN.md §5.3`, Stage A defines five access patterns.
This plan locks each as a driver behaviour:

| `access_pattern` | Driver behaviour | Relevant operations |
|------------------|------------------|---------------------|
| `hot_read` | Same instance, same field, read repeatedly | `committed_read`, `working_read` |
| `hot_write_in_tx` | Same instance inside one long-lived transaction, same field, assign repeatedly; transaction reused across the batch, not re-opened per step | `managed_write` |
| `many_short_tx` | Same instance, re-open a transaction per step, write once, commit | `commit`, `rollback` |
| `repeated_construct` | New instance per step, no transaction; per-step class reused (class build cost excluded) | `construct`, `default_factory_init` |
| `read_heavy_mixed` | Same instance, 9 reads per 1 write, no transaction; used only as a sanity check that the mix doesn't reveal a cliff not seen in the single-op scenarios | `committed_read` + `managed_write` mix |

Not every `(operation, field_shape, access_pattern)` triple is meaningful.
`PerfScenario` declares its triple explicitly and the harness rejects
nonsensical combinations (e.g. `construct` with `hot_read`).

### Canonical matrix

The Stage A canonical matrix is the cross-product filtered to the meaningful
triples. For each triple, one `PerfScenario` is defined per relevant
operation:

```
(construct,             repeated_construct,  scalar_1)
(construct,             repeated_construct,  scalar_2)
(default_factory_init,  repeated_construct,  dependent_init)
(committed_read,        hot_read,            scalar_1)
(committed_read,        hot_read,            scalar_2)
(working_read,          hot_read,            scalar_1)
(managed_write,         hot_write_in_tx,     scalar_1)
(managed_write,         hot_write_in_tx,     scalar_2)
(commit,                many_short_tx,       commit_rollback)
(rollback,              many_short_tx,       commit_rollback)
(committed_read+write,  read_heavy_mixed,    scalar_1)
```

Eleven scenarios. With 2 subjects (lifecycle, generated_strategy_a) and the
4-entry Python matrix, the canonical product is 88 runs per `B` batches.
Acceptable per development iteration.

## Sweep dimensions

- **Subject**: `{lifecycle, generated_strategy_a}` always. Additional
  strategies register via adapter and appear alongside without plan changes.
- **Python version**: full `VERSION_MATRIX` from `version_matrix.py`. Phase-4
  development iterations may target a single version via `--python-key`;
  phase-exit full sweep runs all four.
- **Scenarios**: the eleven triples above.
- **Batch size `N`**: sized per scenario so one first-measurement batch runs
  ~100ms. Determined once at harness write time, captured as a constant in
  the scenario definition; not swept.

This plan does **not** sweep field counts, fan-out sizes, or store layouts
— those are init-detection micro-bench concerns and belong to
`OptimalReferencePlan.md §Phase 3`. Stage A measures the end-to-end shape
the generator will actually emit, not mechanism-space.

## Harness code organisation

All paths under `yidl/docs/validation/perf/`:

- `version_matrix.py` — already exists; owned by PRE_IMPL §0b. Imported.
- `perf_contract.py` — `PerfScenario`, `PerfState` dataclasses, typing, and
  the invariant-enforcement helpers (triple validation, DCE assertions).
- `stage_a_scenarios.py` — the eleven scenario definitions above; each one
  builds a `PerfState` in `setup`, defines a tight `step`, and declares its
  `steps_per_batch`.
- `runner.py` — batch execution (warm-up, measurement, `gc` policy,
  `perf_counter_ns` boundaries) and per-batch normalisation. Produces
  `PerfBatchResult` per batch and `PerfScenarioResult` per scenario.
- `stats.py` — median / p95 / min / steps-per-second computation, inter-run
  variance (`median_of_medians`, `max_min_spread_pct`).
- `report.py` — writes a machine-readable JSON file and a human-readable
  markdown table per run; comparison table (subject × scenario) generated at
  phase exit.
- `stage_a_main.py` — CLI entry point. Flags: `--subject`, `--scenario-key`,
  `--python-key`, `--runs` (default 1 for dev, 3 at phase exit),
  `--output-dir`.

Adapter-facing scenarios live in `stage_a_scenarios.py` and only reference
`StudySubject` plus the shared `PerfScenario`/`PerfState` contract. Subject
implementations stay in `docs/validation/study/*_backend.py` (semantic
harness tree). No perf-specific code in the subject adapters.

## Metrics

### Measurement primitive

`time.perf_counter_ns()`. Same choice as the init-detection micro-bench
(`OptimalReferencePlan.md §Phase 3 Metrics`). Rationale is identical: float
seconds loses precision for sub-µs operations, and the 50–100 ns call
overhead is negligible at batch boundaries. Using the same primitive across
both benches means micro-bench numbers can be compared against Stage A
sub-operation budgets without unit conversion.

### Batch structure

For each `(subject, scenario_key, python_version)`:

1. Subject's `build_class()`, `build_transaction_manager()`,
   `make_instance()` are called in `scenario.setup(subject)`. The returned
   `PerfState` is reused across all batches within this scenario run.
   Class construction and instance construction costs are **not** in the
   timed region except for `construct` / `default_factory_init` scenarios,
   which explicitly time them by building a new instance inside `step`.
2. `N = scenario.steps_per_batch` steps per batch, sized for ~100ms per
   first-measurement batch. Typical ranges: `N ∈ {1e4, 1e5, 1e6}` depending
   on per-op cost (macro-bench operations are µs-scale, so `N` is lower than
   the micro-bench's `1e6 – 1e7`).
3. Warm-up: 3 batches, results discarded. Allows CPython 3.12+ adaptive
   specialiser to reach steady state on the `step` bytecode.
4. Measurement: `B = 21` batches per scenario on canonical-point iterations,
   `B = 101` at phase-exit full sweep.
5. Per batch: `gc.disable()` →
   `t0 = perf_counter_ns()` → driver loop for `N` steps →
   `t1 = perf_counter_ns()` → `gc.collect(); gc.enable()`.

Same GC discipline as the init-detection bench. Stage A operations allocate
more (instances, tx objects, committed values), so GC-driven variance is
larger; the between-batch `gc.collect()` is what stabilises it.

### Per-batch normalisation

Every Stage A scenario reports `ns_per_step = (t1 - t0) / N`. There is no
need for the per-visited-field normalisation the init-detection bench uses
for its `S5a` commit-traversal scenario; Stage A's `commit` scenario times
the whole `begin + write + commit` round-trip as its step.

For `construct` and `default_factory_init` specifically, the step includes
the instance allocation itself, so `ns_per_step` is also `ns_per_construction`
for those scenarios.

For `read_heavy_mixed`, the step is one read-or-write (9:1 ratio baked into
the `step` body). `ns_per_step` is reported as the blended average; the
harness also records the split read/write count per batch for auditing.

### Statistics reported

Computed across the `B` per-batch `ns_per_step` values per scenario:

- **Median** — primary statistic; robust to GC spikes.
- **p95** — tail cost; primarily meaningful on `construct` and
  `default_factory_init` where cold cache effects show up on first-touch.
- **Min** — sanity check. Large `median/min` ratio signals either GC
  contamination or residual first-specialisation bump that warm-up did not
  absorb.
- **Steps per second** — derived: `1e9 / median_ns_per_step`. Used in
  summary tables only.

Means are not reported. Same rationale as the init-detection bench.

At phase exit, `--runs 3` is used and the report includes
`median_of_medians` plus `max_min_spread_pct`
(`(max_median - min_median) / median_of_medians * 100`) per
`(subject, scenario, python_version)` cell.

### Dead-code-elimination prevention

Every `step` body must produce an observable dependency chain that CPython
cannot elide. The harness enforces three invariants at scenario-registration
time:

1. **Return is a real integer read from program state.** The `step` signature
   requires returning `int`. A constant-returning step is rejected at
   registration by an assertion that runs a 3-step canary through `step` and
   checks that at least two distinct values are observed under an input
   perturbation injected by the harness.
2. **Next-step input depends on previous-step sink.** The runner carries an
   integer accumulator `acc` across steps. Each `step(state)` reads
   `state.acc`, derives the operation's input from it
   (e.g. `value_to_write = (state.acc & 0xFFFF) | 1`), and updates
   `state.acc ^= returned_int`. This creates a true data dependency so
   reads cannot be lifted out of the loop and writes cannot be coalesced.
3. **Reads actually touch instance state.** For `hot_read` scenarios, the
   `setup` must write a non-trivial value that changes `acc`'s parity on
   read; the harness asserts that the parity of `acc` after the warm-up
   batches is non-deterministic across seeds.

Writes do not need extra DCE machinery — the post-write state is observable
via the instance — but invariant (2) applies to writes as well: the next
value written depends on the previous value read back in a subsequent step
within the same batch.

`step` bodies are intentionally tight and free of allocations beyond what
the operation itself requires. Allocation-heavy helpers (list/dict
comprehensions inside `step`) are a registration-time failure.

### Scenario × metric summary

| Operation | Primary metric | Secondary | Notes |
|-----------|----------------|-----------|-------|
| `construct` | median `ns_per_step` | p95 | Step includes allocation |
| `default_factory_init` | median `ns_per_step` | p95 | 3-phase init cost visible here |
| `committed_read` | median `ns_per_step` | — | Hot-loop; most representative |
| `working_read` | median `ns_per_step` | — | Exercises tx-overlay path |
| `managed_write` | median `ns_per_step` | — | In-tx hot write |
| `commit` | median `ns_per_step` | p95 | Step = full round-trip |
| `rollback` | median `ns_per_step` | p95 | Step = full round-trip |
| `read_heavy_mixed` | blended median `ns_per_step` | split counts | Sanity scenario |

Allocation counts and GC-pressure breakdowns are deferred to a second pass;
same policy as the init-detection bench.

## Reporting format

Per run (single `--subject --scenario-key --python-key` invocation):

- Machine-readable JSON under
  `docs/validation/perf/results/stage_a/<python_key>/<subject>__<scenario_key>.json`
  containing raw per-batch `ns_per_step` values, warm-up discard count, batch
  count, timestamp, Python version, subject version / git SHA if available,
  and computed statistics.
- Human-readable markdown appended to
  `docs/validation/perf/results/stage_a/<python_key>/SUMMARY.md` (one row per
  `(subject, scenario)`).

Per phase-exit full sweep:

- `docs/validation/perf/results/stage_a/SWEEP_<UTC_TIMESTAMP>.md` with:
  - A comparison table `subject × scenario` of median `ns_per_step` per
    Python version.
  - A "ratio" table `generated_strategy_a / lifecycle` per scenario per
    Python version so regressions and wins are one glance away.
  - Inter-run variance summary (`median_of_medians`, `max_min_spread_pct`).
  - Flagged rows where `max_min_spread_pct > 15%` (noise threshold to
    revisit) or where `generated_strategy_a / lifecycle > 1.5` (suspected
    perf regression to investigate).

## Findings note

At phase exit, `docs/validation/perf/stage_a_findings.md` is written with:

- The sweep headline: one sentence per Python version saying whether
  `generated_strategy_a` reaches performance parity with `lifecycle` on the
  hot-path scenarios (`hot_read`, `hot_write_in_tx`) and within an explicit
  tolerance on the tx round-trip scenarios (`commit`, `rollback`).
- Per-Python-version results tables (copied from the sweep report).
- Any cliffs, surprises, or allocator-dominated regressions, with
  reproduction commands.
- Explicit caveats: scenarios not run, strategies not yet landed, pyrolyze
  version used for the reference.
- A go / adjust / stop recommendation for `PRE_IMPL_STUDY_IMPL_PLAN §Phase 4c`.

This note is the Phase 4 input to `PRE_IMPL_STUDY_IMPL_PLAN §Phase 8`
consolidation.

## Out of scope

- Stage B / C / D helper sets (`const`, `static`, `local_store`, `derived`,
  `multi_group_tx`, `transient`, `binding`, `owned`, all injection/hook
  cases). They have their own phases and their own perf extensions to be
  authored then.
- Variance in generator knobs (field count, fan-out, virtual-store layout).
  The init-detection micro-bench owns mechanism-space sweeps; Stage A
  measures one fixed generator output shape.
- Tool migration to `pyperf`, `pytest-benchmark`, etc. Deliberately
  single-dependency (`time`, `gc`, standard library only) for reproducibility
  across the Python matrix. Revisit at end of PRE_IMPL if per-batch variance
  proves intractable.
- Cross-platform comparison. Runs on one development machine; the numbers
  are comparative (within one sweep), not absolute.
- Cold import/compile cost. `PRE_IMPL_STUDY_DESIGN §9` calls out the
  separation; Phase 4 measures steady-state only. Cold-start cost gets its
  own probe if it becomes a concern.

## Exit gate

Phase 4 (as governed by this plan) is complete when:

- `perf_contract.py`, `stage_a_scenarios.py`, `runner.py`, `stats.py`,
  `report.py`, and `stage_a_main.py` exist under
  `docs/validation/perf/` and implement the contracts above.
- All eleven canonical scenarios run against both `lifecycle` and
  `generated_strategy_a` on every entry of `VERSION_MATRIX` at `--runs 3`.
- `docs/validation/perf/results/stage_a/SWEEP_<TIMESTAMP>.md` exists with
  the comparison and ratio tables.
- `docs/validation/perf/stage_a_findings.md` exists and contains a
  go / adjust / stop recommendation consistent with
  `PRE_IMPL_STUDY_IMPL_PLAN §Phase 4c`.
- Any scenario where `max_min_spread_pct > 15%` across the 3 runs is either
  stabilised (more warm-up batches, larger `N`, or a documented harness fix)
  or flagged in the findings note with explicit caveats.
- Any YIDL-owned runtime gap surfaced while implementing
  `generated_strategy_a` for this matrix is cross-referenced into the
  Phase 6 runtime-pressure discussion
  (`PRE_IMPL_STUDY_IMPL_PLAN §Phase 6b`).

## Anti-scope

To keep this plan bounded and avoid Phase 4 scope creep:

- No changes to `docs/validation/study/contract.py` (the `StudySubject`
  ABC). Perf needs a parallel `PerfScenario` surface, not a modified
  semantic contract.
- No edits under `pyrolyze/`. Lifecycle is the read-only reference.
- No promotion of any `docs/validation/perf/` artifact into `src/yidl/`
  until PRE_IMPL is closed.
- No benchmarking tool dependency beyond the standard library.
- No alternate runtime (free-threaded, PyPy, GraalPy) sweep. Python-version
  matrix only.
