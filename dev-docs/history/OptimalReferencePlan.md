# Optimal Hand-Crafted Reference Plan

## Purpose

This document is the execution plan for producing one credible hand-crafted
"optimal model" reference file for the YIDL generated lifecycle shape, and for
the init-detection research that feeds it.

It exists because:

- `pyrolyze.lifecycle` is the functionality YIDL must reproduce.
- Before writing the lifecycle `.yidl` spec (`yidl/spec/lifecycle_baseline.yidl`),
  we need a single concrete hand-crafted target shape the spec can be written
  against.
- The design decisions that shape that target are dispersed across
  `YidlMultiFacadeModelSchemaDesign.md`, `PRE_IMPL_STUDY_DESIGN.md`,
  `AstichiYidlUseCases.md`, `example/generated_factory_sample.py`, and
  `docs/validation/generated_example/managed_owned_generated_example.py`; those
  sources disagree with one another on several non-trivial points.
- The init-detection axis is a real unknown (per `YidlMultiFacadeModelSchemaDesign.md`
  §9) and should be resolved empirically before being baked into the reference.

This plan is scoped. It does not try to cover every lifecycle helper kind, the
full `.yidl` grammar, or the full generator. It produces the smallest artifact
set that forces every non-trivial optimal-model decision and locks them into a
runnable reference.

Read alongside:

- `dev-docs/YidlMultiFacadeModelSchemaDesign.md` — the origin document for the
  optimal model (naming, `YidlState`, virtual stores, lazy facades, weakref
  topology, init-detection research item).
- `dev-docs/PRE_IMPL_STUDY_DESIGN.md` — scenario matrix, study subject layout,
  Stage A / Stage C helper classification.
- `dev-docs/PRE_IMPL_STUDY_IMPL_PLAN.md` — ordered study phases; this plan
  slots into Phase 3 (generated strategy) and Phase 5/6 (shape-extension and
  runtime-pressure) at the minimum helper set.
- `dev-docs/AstichiYidlUseCases.md` — what Astichi is and is not responsible
  for; relevant because Phase 2 of this plan deliberately dogfoods Astichi V1.
- `docs/YIDLRuntimeClassModel.md` — normative runtime model that the
  reference must embody.

## Execution order

The execution order is **(3) bench → (2) reference → (1) design note**.

Rationale:

- (3) is the only axis with a real empirical answer; picking it from paper
  would risk having to rewrite both code and docs later.
- (2) is easier to nail as a running artifact than as prose, and it forces
  every structural decision into something testable.
- (1) is a consolidation job once the decisions exist in code and bench
  results.

Parts of (2) that do not touch init-detection may run in parallel with (3).

## Phase 3 — Init-detection bench

Goal: pick the init-detection mechanism for the optimal reference, with
empirical evidence.

### Candidates

Five candidate implementations of identical surface. Each holds `K` fields in
one slotted "store" class; only the init-detection mechanism differs.

- **Bitmask** — one `int` per physical store, one bit per field. Check:
  `mask & (1<<k)`. Set: `mask |= (1<<k)`. Bulk clear: `mask = 0` (hits the
  CPython small-int cache; constant cost, independent of prior field count).
- **VOID sentinel** — module-level `VOID` object, one slot per field. Check:
  `slot is not VOID`. Set: `slot = value` (may stay as-is; VOID indicates
  uninit). Bulk clear: per-slot `slot = VOID` loop, or fresh-store swap.
- **Optimistic try/except** — slot left unset (slotted class → `AttributeError`
  on first read). Check: read in `try`; on `AttributeError`, run init and
  retry. Bulk clear: `delattr` per slot (expensive with slots), or pair with
  fresh-store swap.
- **Generation counter** — one `int` generation counter per store, one `int`
  tag slot per field. Check: `slot_gen == store_gen`. Set: write value and
  `slot_gen = store_gen`. Bulk clear: `store_gen += 1` — O(1), independent of
  field count; no per-field touch. Room to pack multi-bit per-slot state
  (e.g. `{unset, working-set, dirty, validated}`) by widening the tag
  without changing architecture.
- **Fresh-store swap** — `self.__y_working = _YWorkingStore()` at
  commit/rollback. Pair with VOID sentinel for per-slot init detection inside
  the fresh store. Measures allocator cost as the upper bound for "zero
  per-field bookkeeping, let Python pay". Included as a ceiling reference
  rather than a prediction.

### Dismissed candidates (recorded, not benched)

- **Descriptor swap / non-data descriptors** — `__slots__` exposes data
  descriptors for every slot; non-data descriptors cannot be shadowed by
  instance `__dict__` when there is no `__dict__`. Combined with the fact
  that one of the locked design decisions is slotted stores, there is no
  win path.
- **`__class__` mutation post-init** — only helps if all fields initialize
  together, which defeats lazy init; incompatible with the 3-phase init
  rule's per-field ordering.
- **`dict` proxy with `setdefault` / `__contains__`** — ruled out on
  expected hot-path cost; not a realistic candidate for generated code that
  targets native attribute access.
- **Per-field lazy property in pure Python** — the property call overhead
  alone exceeds the try/except slot-read cost. Strictly worse than the
  try/except candidate and offers nothing the try/except candidate does
  not.

### Bench shape — realistic facade-over-store model

Plain slot access is not the shipped shape, so measuring it is not useful.
The bench must replicate the shape of generated code:

- A facade class with `Pn` `@property` fields (getter + setter per field).
- Each property delegates into a storage object with `Sn` slotted fields
  (`Sn >= Pn`; typically `Sn ≈ 3 * Pn` to reflect published + working +
  hidden virtual stores).
- Each property body touches a **fixed random fan-out** of store fields:
  - getter reads `Rn` store fields (with init-check on each)
  - setter reads `Rn` store fields and writes `Wn` store fields
- The `Rn` / `Wn` field sets for each property are chosen **once at class
  generation time** by a seeded PRNG and captured as closure constants
  inside the property body. No RNG runs inside property bodies during
  measurement.
- Every property body performs at least one store access (even a setter
  that would logically be pure write still reads at least one init-check).
  This prevents degenerate zero-work paths.

### Driver model

One step of the driver loop:

```
step(prng):
    prop_idx = prng.next_uint() % Pn
    op      = prng.next_uint() & 1     # 0 = read, 1 = write
    if op == 0:
        sink = getattr(facade, prop_name[prop_idx])
    else:
        setattr(facade, prop_name[prop_idx], value)
```

- PRNG is a fast seeded xorshift implemented in inline Python, not
  `random.Random` (whose overhead would swamp the measurement).
- Seeds are fixed per scenario so every run is deterministically
  reproducible across candidates and Python versions.
- `value` is a constant chosen per scenario; the bench does not measure
  `repr`/coercion cost.
- Driver work per step must be small compared to the property body, so
  the xorshift is inlined into the step loop and budget-tested
  separately.

### Scenarios

Each scenario runs the driver for a fixed step count under a specific
initial state. The bench must include:

1. **S1 — Construction cost.** One `facade = Facade(...)` per iteration.
   Measures 3-phase init amortized over `Pn` fields plus store allocation.
2. **S2 — Hot steady state.** All store fields initialized. Driver runs
   mixed reads and writes with `Rn` / `Wn` per property call. Primary hot
   path; most representative of steady-state performance.
3. **S3 — Cold first-touch cascade.** Starts with stores fully
   uninitialized. Driver runs until all fields have been touched at least
   once. Measures amortized lazy-init overhead; the per-step distribution
   should be inspected (first touches are expensive, later steps are hot).
4. **S4 — Transaction read-then-write.** Simulates an active transaction:
   getters read through the "working then fallback published" path;
   setters write to the working store only. Exercises the second store
   alongside the first, with init-state lookups on both.
5. **S5a — Commit traversal with visits.** Iterate only set fields in the
   working store and read each. Bitmask uses `mask & -mask` bit-walk
   (cost scales with set bits). VOID sentinel, try-except, generation
   counter, and fresh-store-swap candidates must scan all `Sn` slots.
   Normalize by set-bit count so the bit-walk advantage is visible.
6. **S5b — Bulk clear.** End-of-transaction invalidation of all working
   values in a single operation; no per-field action. Measures
   `mask = 0` vs per-slot `slot = VOID` loop vs `delattr` loop vs
   `store_gen += 1` vs fresh-store swap.

Scenarios S2, S5a and S5b are all non-negotiable. Without S5b the bench
cannot measure the class of operation that makes bitmask and generation
counter structurally different from VOID sentinel and try/except.

### Sweep dimensions

The bench sweeps:

- **Candidate mechanism**: all five.
- **`Pn` (facade property count)**: at least `{4, 16, 64}`.
- **`Sn` (store slot count)**: at least `{Pn, 2*Pn, 4*Pn}` where `Sn >= Pn`.
- **`Rn_max` (max reads per property body)**: at least `{1, 2, 4, 8}`.
- **`Wn_max` (max writes per property body)**: at least `{0, 1, 2, 4}`.
- **Python version**: per `docs/validation/perf/version_matrix.py` — do
  not hard-code versions in the bench.

Purpose of the sweep is not runtime calibration. It is to:

1. Pick a winning mechanism under realistic facade-over-store conditions.
2. Pick the numeric budget for the class-time assertion (see `Class-time
   budget assertion` below).

If the full product of sweep dimensions is too large to run per
development iteration, define one "canonical" point (e.g.
`Pn=16, Sn=48, Rn_max=4, Wn_max=2`) that every candidate runs in short
iterations, and run the full product at phase exit.

### Harness code generation — astichi-first

The bench's candidate classes, property bodies, and step drivers are
constructed by generating Python source and `exec`-ing it into a local
namespace. The generator uses Astichi V1 where it reaches:

- One property-template Composable per mechanism (its body contains the
  mechanism-specific init-check and read/write primitives as holes).
- Per-property bind injects the fixed `Rn` / `Wn` field index lists.
- Additive compose to assemble all `Pn` properties into one class body.

Where Astichi V1 does not reach (e.g. full class-body skeleton, store
slot list generation, driver loop assembly), the harness falls back to
plain f-string / `textwrap.dedent` source generation and logs the
shortfall in the findings note. Same policy as Phase 2.

This dogfooding is intentional. Measuring under a class shape that
generated YIDL code will actually emit is more valuable than measuring
isolated store objects. Any astichi shortfall surfaced here directly
informs V2 deferred-features.

### Class-time budget assertion

Whichever mechanism wins, the generator enforces its upper limits at
class-generation time, not at runtime:

- The bench sweep determines the budget empirically (for bitmask: the
  highest `Sn` per physical store where the cost curve stays flat; for
  generation counter: the highest `Sn` where per-slot tag memory remains
  acceptable; for VOID sentinel / try-except: per-store field count
  alone).
- The generated factory function asserts, once at class construction,
  that the highest bit index assigned (bitmask) or the field count
  (other mechanisms) stays within the recorded budget.
- On failure the generator raises immediately with a clear diagnostic
  naming the store, the observed field count, and the budget. This is a
  hard fail, not a fallback to a slower path. If a user hits it, they
  file a bug; we then decide deliberately whether to raise the budget,
  split the store, or switch that store's mechanism — rather than silently
  accumulating slow stores.
- Zero runtime cost: the assertion executes once per class definition at
  `exec` time, alongside the other class-time validations.

This replaces any notion of a soft "stay under N fields" runtime cliff.
There is no soft cliff in the generated code, only a hard budget chosen
from empirical evidence and enforced deterministically.

### Metrics

#### Measurement primitive

`time.perf_counter_ns()`. Not `perf_counter()` — float seconds loses
precision for sub-µs operations. Overhead of `perf_counter_ns()` is
50–100ns per call; negligible because it is only called at batch
boundaries, not per step.

#### Batch structure

For each `(mechanism, Pn, Sn, Rn_max, Wn_max, scenario, Python version)`:

1. Candidate class is built once and reused across all batches within
   the scenario. Class construction cost is measured separately as S1.
2. `N` = batch size = number of steps timed per batch. Chosen per
   scenario so one first-measurement batch runs ~100ms wall-clock.
   Typical ranges: `N ∈ {1e5, 1e6, 1e7}` depending on per-op cost.
3. Warm-up: 3 batches, results discarded. Lets CPython 3.11+ adaptive
   specialiser reach steady state on the property and setter bytecode.
4. Measurement: `B = 21` batches on the canonical sweep point,
   `B = 101` at phase-exit full sweep.
5. Per batch: `gc.disable()` →
   `t0 = perf_counter_ns()` → driver loop for `N` steps →
   `t1 = perf_counter_ns()` → `gc.collect(); gc.enable()`.
   GC is disabled inside the timed region and forced between batches
   so GC pauses cannot contaminate per-batch timings.

#### Per-batch normalisation

Per-batch wall-clock is normalised to a per-unit cost:

- **S1** (construct): `ns_per_construction = (t1 - t0) / N`.
- **S2, S3, S4** (driver loops): `ns_per_step = (t1 - t0) / N`.
- **S5a** (traversal): `ns_per_visited_field = (t1 - t0) / total_visits`,
  where `total_visits` is the sum across all traversal calls in the
  batch of the set-field count observed at each call. Normalising by
  visit count is what makes bitmask's bit-walk advantage visible as a
  per-visit speedup rather than being hidden inside traversal-duration
  differences.
- **S5b** (bulk clear): `ns_per_clear = (t1 - t0) / N`.

#### Statistics reported

Computed across the `B` per-batch normalised values for each scenario:

- **Median** — primary statistic; robust to GC spikes.
- **p95** — tail cost; primarily meaningful on S3 (cold first-touch).
- **Min** — sanity check. A large median/min ratio signals either GC
  contamination that escaped the GC policy or residual
  first-specialisation bump that warm-up did not absorb.
- **Steps per second** — derived: `1e9 / median_ns_per_step`. Used in
  summary tables only.

Means are not reported. They mislead under GC spikes even with the
above policy.

At phase exit, the full sweep is run 3 times. Report
`median_of_medians` plus `max_min_spread_pct` (max median minus min
median across the 3 runs, as a percentage of the median_of_medians).

#### Dead-code-elimination prevention

Every read result must be consumed in a way the interpreter cannot
elide:

- **Writes**: `facade.prop_i = value` — already observable via store
  mutation; no extra machinery needed.
- **Reads**: XOR-fold into a running integer accumulator carried by
  the driver, and feed that accumulator into the next step's `prop_idx`
  so there is a real data dependency. Preferred over
  `self._sink = value` because it avoids per-step attribute writes
  and allocator pressure.
- **Property bodies**: must return the actual store value on the
  initialised path. The VOID-sentinel variant is especially vulnerable
  to short-circuit bugs — `slot is not VOID and slot` returns `False`
  for falsy values rather than the value; the correct pattern is
  explicit `if slot is VOID: init(); return slot`. The harness must
  assert this invariant on each generated property body.

#### Scenario × metric summary

| Scenario | Primary metric | Normalisation unit |
|----------|----------------|--------------------|
| S1 Construct | median `ns_per_construction` | per `Facade(...)` |
| S2 Hot steady state | median `ns_per_step` | per driver step |
| S3 Cold first-touch | median `ns_per_step` plus p95 | per driver step |
| S4 Transaction R/W | median `ns_per_step` | per driver step |
| S5a Commit traversal | median `ns_per_visited_field` | per set field visited |
| S5b Bulk clear | median `ns_per_clear` | per clear operation |

Allocation counts and GC-pressure breakdowns are not first-pass
metrics. They are deferred to a second pass only if first-pass
wall-clock differences turn out to be allocator-dominated.

### Integration with the PRE_IMPL study harness

This bench lives inside the PRE_IMPL study scaffolding but owns a disjoint
slice of the perf workload. To keep responsibilities un-mixed:

- **Perf scaffold ownership** — `docs/validation/perf/` and its
  `README.md` are owned by `PRE_IMPL_STUDY_IMPL_PLAN.md §0a`. This bench
  adds files under that scaffold; it does not re-scaffold.
- **Python version matrix** — `docs/validation/perf/version_matrix.py`
  (`VERSION_MATRIX`) is owned by `PRE_IMPL_STUDY_IMPL_PLAN.md §0b` and
  already exists. The bench **imports** it; hard-coding Python versions
  anywhere in bench code is a review-time failure.
- **Scenario contract** — the PRE_IMPL semantic `StudySubject` contract
  in `docs/validation/study/contract.py` is **not** reused here. This
  bench compares init-detection mechanisms on a synthetic facade-over-store
  shape, not study subjects. Candidate classes are generated in-process
  by the bench; they do not register as `StudySubject` implementations.
- **Disjoint from Phase 4 macro-bench** — the Stage A macro-bench
  (`StageAPerformanceMatrixPlan.md`) compares `lifecycle` vs
  `generated_strategy_a` end-to-end and also lands under
  `docs/validation/perf/`. The two benches must be clearly named so neither
  is mistaken for the other: `init_detection_bench.py` /
  `init_detection_findings.md` for this plan;
  `stage_a_*.py` / `stage_a_findings.md` for Phase 4.
- **Mechanism choice flows one way** — the winner from this bench feeds
  `OptimalReferencePlan.md §Phase 2` (the optimal reference) and via that,
  `PRE_IMPL_STUDY_IMPL_PLAN.md §Phase 3` (`generated_strategy_a`). Phase 4
  **consumes** the winning mechanism; it does not re-evaluate it.

### Output

- `docs/validation/perf/init_detection_bench.py` — the bench runners and
  candidate-class generators.
- `docs/validation/perf/init_detection_findings.md` — short findings
  note: raw numbers per candidate × scenario × `(Pn, Sn, Rn_max, Wn_max)`
  × Python version, per-scenario winner, recommended pick, the chosen
  class-time budget value with rationale, any astichi-harness shortfalls
  logged, explicit caveats. This file becomes the init-detection
  section of the Phase 1 design note.

### Out of scope for this bench

- "One big physical store with multiple virtual namespaces" vs
  "three separate physical stores" (`YidlMultiFacadeModelSchemaDesign.md`
  §14). This is a separate probe and should not inflate the init-detection
  matrix. Revisit after the reference lands.
- Multi-group transaction cost. Not relevant to init detection.
- Cross-facade attribute routing cost. Covered later by the full study
  harness when the reference becomes a study subject.

### Exit gate

Phase 3 is complete when:

- All five candidates run under all six scenarios (S1, S2, S3, S4,
  S5a, S5b) across the Python matrix at a minimum on the canonical
  sweep point and at phase exit on the full sweep product.
- `init_detection_findings.md` exists and records a single recommended
  mechanism plus a chosen numeric budget for the class-time assertion,
  both with rationale traceable to measured numbers.
- Any surprises (Python-version cliffs, unexpected per-scenario losers,
  allocator-dominated regressions) are documented explicitly, not omitted.
- Any Astichi V1 shortfalls encountered while generating candidate
  classes are logged in the findings note and cross-referenced into
  the Astichi V2 deferred-features register.

## Phase 2 — Optimal hand-crafted reference

Goal: produce one hand-crafted Python file that embodies every optimal-model
decision for the minimum forcing helper set, with parity tests against the
lifecycle reference.

### Helper set

Five fields, covering Stage A (managed core) plus one Stage C
(runtime-pressure) item:

1. `managed_scalar` — plain managed int. Exercises managed baseline,
   commit, rollback.
2. `managed_with_thaw` — managed with `freeze` / `thaw` callables. Exercises
   thaw-on-read (copy-on-read) and freeze-on-commit.
3. `managed_depends_on_other` — `default_factory(self)` referencing an
   earlier-initialized field. Exercises 3-phase init ordering and
   declaration order.
4. `binding_scalar` — `BindingBase`-derived resource. Exercises evict-last
   on overwrite, commit, and rollback.
5. `local_store_scalar` — native-homed on the main proxy. Exercises
   native-homing and the virtual-vs-physical store split.

This is deliberately the smallest set that forces every non-trivial
optimal-model axis. Validators, hooks, init-vars, classvars, and
multi-group transactions are explicitly deferred.

### Locked design decisions

These are fixed at plan time (no per-case bikeshedding during Phase 2
implementation):

| Axis | Decision |
|------|----------|
| Internal name prefix | `__y_*` (supersedes `__kild_*` drift in `managed_owned_generated_example.py`). |
| Runtime anchor | One `YidlState` per main-facade instance; holds transaction manager, per-field runtime-state records, rollback error list. |
| Const metadata | Baked into closure captures in the generated factory; not stored on `YidlState`. |
| Virtual store split | One slotted `_YPublishedStore`, one `_YWorkingStore`, one `_YHiddenStore` per generated class; each carries every field of that virtual scope as a named slot. No per-field store objects. |
| Physical store layout | Not collapsed to one slotted object in this reference. The virtual-vs-physical collapse (schema §14) is a later probe. |
| Facade allocation | Main proxy eagerly allocates state and stores. `current` and `working` facades are allocated lazily on first attribute access via cached property on main. |
| Back-references | Secondary facades hold `weakref.ref(main)` back to the main proxy. `YidlState` is held via strong ref from main; secondary facades resolve state through the main weakref. No strong cycles. |
| Init detection | Mechanism picked by Phase 3. Reference code parameterises the `has_value` / `set_flag` primitives so the pick is a mechanical swap until Phase 3 lands. |

These decisions replace the dispersed positions in the prior hand-crafted
examples and constitute the concrete target shape for the eventual `.yidl`.

### Astichi use in Phase 2

Phase 2 deliberately dogfoods Astichi V1 for one well-scoped role: the
per-field property / setter / helper template.

In scope for Astichi use:

- One managed-field template Composable; bound five times (once per field
  where applicable) using V1 scoped bind and hygiene.
- One binding-field template Composable; bound once.
- One local-store template Composable; bound once.

Out of scope for Astichi use in this phase (hand-paste instead, log
shortfall if encountered):

- `astichi_for` over the harvested field list. V2 Phase 2 (loop unroll) is
  not landed; replaced with manual multi-compose.
- Match/case hole shape. Not needed by the reference (specialization per
  field is the point; no runtime kind dispatch).
- Phase-3-aware `__init__` body stitching. Hand-pasted.
- `@astichi_insert` composition across class bodies where V1 does not yet
  reach. Hand-pasted.

If the per-field template use exposes an Astichi V1 shortfall, record it in
`astichi/dev-docs/V2ProgressRegister.md` (or the V2 deferred-features list)
and fall back to hand-paste for the reference. The shortfall log itself is
valuable study output.

### Artifacts

- `docs/validation/generated_example/optimal_reference.py` — the reference
  class and its per-class helpers (`_YPublishedStore`, `_YWorkingStore`,
  `_YHiddenStore`, `YidlState`, `_CurrentFacade`, `_WorkingFacade`, main
  proxy, factory entry point).
- `docs/validation/study/optimal_reference_backend.py` — `StudySubject`
  wrapper so the reference can be driven by the existing scenario harness
  alongside `lifecycle_backend.py` and `generated_strategy_a_backend.py`.
- `docs/validation/study/test_optimal_reference.py` — parity tests against
  the lifecycle reference for Stage A scenarios and the `binding_scalar`
  runtime-pressure case.

### Decision scratch

While Phase 2 is in flight, any design choice not covered by the locked
table above should be recorded as it is made, either as an inline comment
in `optimal_reference.py` or as a short entry in a sibling
`optimal_reference_scratch.md`. Phase 1 consumes these.

### Exit gate

Phase 2 is complete when:

- `optimal_reference.py` builds a main-facade class plus lazy
  `current` / `working` facades with no strong reference cycles.
- All five fields implement their transducer semantics: read, write, commit,
  rollback, and (for `binding_scalar`) evict-last on overwrite and rollback.
- The parity test passes for every Stage A scenario against the lifecycle
  reference, plus the `binding_scalar` runtime-pressure scenario.
- Every deviation from the locked decision table is explicitly recorded as
  a scratch entry with a reason.

## Phase 1 — Consolidation design note

Goal: write the design note once the decisions are visible in runnable
code and bench results.

### Artifact

- `dev-docs/OptimalHandCraftedReferenceDesign.md` — the durable record of
  the target shape.

### Content

- The six locked decisions, each with a short rationale and a pointer to
  the reference file section that demonstrates it.
- The init-detection section, folded in from
  `init_detection_findings.md` with any edits needed to fit the doc voice.
- An explicit list of deferred items (validators, hooks, init-vars,
  multi-group transactions, classvars, virtual-to-physical store collapse,
  refcounted main facade).
- A cross-reference table linking each decision back to the source doc(s)
  it came from (`YidlMultiFacadeModelSchemaDesign.md` section, relevant
  `PRE_IMPL_STUDY_DESIGN.md` clause, any `FieldSpecYIDLDesignMatrixGaps.md`
  entry) so future readers know where the decision lineage lives.

### Exit gate

Phase 1 is complete when:

- Every Phase 2 scratch entry is either folded into the design note or
  explicitly discarded with a reason.
- Every source doc that disagreed with the reference shape is either
  updated or annotated with a pointer to the new design note.
- The Phase 3 findings file is linked (or inlined) and is no longer
  duplicated as a living document.

## Relationship to the lifecycle `.yidl` work

Writing `yidl/spec/lifecycle_baseline.yidl` beyond the current stores /
surfaces declarations is deferred until this plan completes. Once Phase 1
lands:

- The `.yidl` transducers for `managed`, `binding`, and `local_store` are
  written to emit the shape `optimal_reference.py` demonstrates.
- Grammar shortfalls that surface during that work (virtual stores, lazy
  facades, init-detection sentinel, weakref topology, per-field mask
  namespace) feed back into `YidlMultiFacadeModelSchemaDesign.md` §15
  (open holes) and into the grammar design pass.
- Astichi shortfalls that surface (match-case holes, loop unroll pressure,
  statement-list replacement in init bodies, cross-class insertion) feed
  back into `astichi/dev-docs/V2ProgressRegister.md` or the V2
  deferred-features tracker.

That is the forcing-function stage. It is not in scope for this plan.

## Anti-scope

To keep this plan bounded:

- No new lifecycle helper kinds beyond the five listed above.
- No attempt to resolve the single/list/map binding-owned container-shape
  question (`YidlMultiFacadeModelSchemaDesign.md` §15.1).
- No commit pipeline design (validators, order keys, hooks).
- No lazy facade refcount topology design beyond the weakref back-ref rule
  already stated.
- No codegen work in `src/yidl/` — the reference stays under
  `docs/validation/` until deliberately promoted.
- No edits to `pyrolyze/` under any phase.
