# Init-Detection Study Results (MVP)

Status: results record for the simplified MVP described in
`OptimalReferencePlan.md §Phase 3`. This document captures empirical
numbers for the four candidate init-detection mechanisms and the
recommendation that follows. It is the data record that the optimal
reference work and `PRE_IMPL_STUDY_IMPL_PLAN.md` consume.

## TL;DR — decision (2026-04-17): **VOID sentinel, locked in**

The MVP init-detection mechanism is the **VOID sentinel**: each data
slot is initialised to a module-level `_VOID = object()` at
construction; the access primitive checks `if self.fX is _VOID:` and
fills the slot on miss. See §A.2 "Appendix A — Generated Python source
per candidate" for the exact shape.

This closes out the pre-implementation init-detection study. No
further micro-benchmark sweeps are planned against this axis until a
working end-to-end system exists with realistic read-life patterns.

Rationale from §1–§10:

- On the warm path all four mechanisms sit within ~10–30 ns/field
  across Python 3.12–3.15a5. The absolute spread between the best
  (`tryexcept`) and the second-tier (`void`/`gen-counter`) is only
  ~7–15 ns/field of synthetic micro-benchmark headroom.
- `tryexcept` only wins once ~15–60 warm `get_all()` calls per
  instance have amortised its cold-path `AttributeError` pile-up
  (§10.3). Short-lived instances never reach break-even; a 1%
  hot-path miss rate wipes out its advantage (§10.5).
- In this bench the "init" payload is a trivial constant
  assignment (`self.fX = 42 + i`). Any mechanism-level win only
  pays back if real init is materially more expensive than the
  detection branch itself *and* frequently skipped — unknown until
  the real workload exists.
- `void` is the simplest primitive to code-generate (single
  sentinel comparison, no bitmask/generation bookkeeping, no
  exception handler), sits second on the cold path behind
  `tryexcept`, and is well within the warm-path band.
- The init-detection site is a localised, mechanical code-gen
  template, so swapping mechanisms later (if a real workload shows
  `tryexcept` or bitmask would help) is cheap — compared to the
  cost of locking in `tryexcept` now and later discovering the real
  workload sits below its break-even.

**Revisit triggers** — re-open this study only if we observe:
- measured init-payload cost per field materially above the
  detection branch cost (≫ ~30 ns),
- measured reads-per-instance-per-lifetime distribution that is
  either strongly long-lived (favours `tryexcept`) or
  construct-and-read-once and allocation-dominated (favours
  fresh-store swap, cf. `OptimalReferencePlan.md §85`),
- measured hot-path miss rate — if nonzero, re-check `tryexcept`
  math; if high, VOID stays the right call regardless.

**Consumers**: `OptimalReferencePlan.md` and
`PRE_IMPL_STUDY_IMPL_PLAN.md` should treat VOID as the init-detection
mechanism going forward; other sections of this document (§1–§10) are
kept as the empirical record behind this choice, not as a
recommendation to re-derive.

## 1. What was measured

Bench: `yidl/docs/validation/perf/init_detection_mvp.py`.

- One slotted single-field store class per candidate mechanism.
- Hot path only: the field is initialised before timing begins, so
  every measured `get()` call exercises the **success branch** of the
  init-detection primitive plus a slot read.
- Bound method captured outside the loop so attribute lookup overhead
  is constant across candidates.
- `time.perf_counter_ns()` at batch boundaries; `gc.disable()` inside
  the timed region; 3 warm-up batches discarded; 21 measurement
  batches; primary statistic is the median ns / `get()` call.
- The returned value is XOR-folded into an accumulator that the loop
  cannot dead-code-eliminate.

Candidates:

- **bitmask** — slot per field plus an `int` bitmask; `mask & 1`
  test, slot read on hit.
- **void** — slot per field initialised to a module-level `_VOID`
  sentinel; identity test against `_VOID`, slot read on hit.
- **tryexcept** — slot per field with no init; `try: return self.f0
  except AttributeError:` lazily fills it.
- **gen-counter** — slot per field plus a per-field generation int;
  equality test against the store-level generation int, slot read on
  hit.

## 2. Numbers

All four interpreters from `version_matrix.py` were swept (3.15 via
the `0a5` alpha published through `uv`). Measured ns / `get()` call
(lower is better):

| Mechanism    | 3.12.12 | 3.13.12 | 3.14.3 | 3.15.0a5 |
|--------------|---------|---------|--------|----------|
| bitmask      | 42.31   | 61.62   | 48.68  | 29.23    |
| void         | 39.72   | 55.05   | 47.30  | 23.23    |
| **tryexcept**| **31.36** | **39.83** | **36.40** | **18.99** |
| gen-counter  | 36.68   | 49.22   | 46.51  | 25.90    |

Per-batch spread (max − min as a percentage of the median total batch
time) was single-digit on most rows; outliers on the older
interpreters were 21.4% (3.13 bitmask) and 25.7% (3.14 tryexcept).
On 3.15.0a5 the spread tightens dramatically to 1.9–7.2% — most likely
a side-effect of the smaller per-call cost making each batch finish
in less wall-clock time and reducing OS-noise window. Either way,
medians remain comfortably separated.

## 3. Decision rule applied

`OptimalReferencePlan.md §Phase 3` defines:

- gap ≥ 15% across the top two candidates → clear winner; record and
  proceed to optimal-reference work.
- gap < 15% → run the bulk-clear tie-breaker (separate file, added
  on demand).
- per-Python-version anomaly → investigate before scaling.

Computed gaps (winner vs runner-up):

- 3.12 → tryexcept beats gen-counter by 17.0%.
- 3.13 → tryexcept beats gen-counter by 23.6%.
- 3.14 → tryexcept beats gen-counter by 27.8%.
- 3.15.0a5 → tryexcept beats **void** by 22.4%.

All four rows clear the 15% threshold and the **same candidate wins
on every interpreter**. The decision rule says: clear winner; record;
proceed.

Ranking by interpreter (best to worst):

- 3.12 / 3.13 / 3.14: `tryexcept << gen-counter < void < bitmask`
- 3.15.0a5: `tryexcept << void < gen-counter < bitmask`

The runner-up flipping from `gen-counter` to `void` on 3.15 is the
most interesting movement in the matrix. `void` got a bigger
relative speedup than `gen-counter` (≈ 51% faster on 3.15 vs 3.14
for `void`, vs ≈ 44% for `gen-counter`). The candidate identity of
the winner is unaffected, but if a future interpreter narrows the
top-two gap below 15%, the relevant runner-up to compare against may
no longer be `gen-counter`.

## 4. Recommendation

**Adopt `try/except AttributeError` as the default init-detection
primitive for the optimal reference codegen** for the case the
benchmark covers — single-field hot-path get-or-init.

**Keep `gen-counter` as the secondary mechanism** for stores that
need O(1) bulk invalidation. The MVP does not measure bulk-clear
cost, but `try/except` has no inherent bulk-clear story and would
have to fall back to per-field `delattr(...)`. The structural
asymmetry is what justifies preserving `gen-counter` as a recognised
secondary mechanism rather than dropping it; not its hot-path
ns/op number.

**Bitmask is consistently the slowest** despite the theoretical
appeal of one masked int dominating cache behaviour. The extra
`& 1`, the slot read, the slot write to update the bitmask on the
init taken-branch, and the slot read again on subsequent calls cost
more than a `try` setup that succeeds without raising.

## 5. Caveats and what this does not measure

The MVP is deliberately scoped. Concretely it does not measure:

- bulk invalidation — the structural advantage of `gen-counter` over
  `try/except`. Decided to defer rather than build a tie-breaker
  because the hot-path gap was already ≥ 15%.
- the init taken-branch — every measured call hits the success
  branch; first-call init cost is amortised away.
- the failure case for `try/except` — if even ~0.1% of calls hit
  `AttributeError` the picture flips dramatically. The optimal
  reference must guarantee init has run before any hot-path access,
  or this recommendation is invalid.
- multi-field stores — interaction with cache lines, slot layout,
  and bitmask width is not exercised.
- access patterns other than tight-loop reads — no writes, no
  interleaved reads/writes, no real workload mix.

These caveats are the exact items §Phase 3 lists as triggering a
re-test, and any future deviation from "single-field, hot-path,
init-already-run" should re-open the question rather than assume the
recommendation transfers.

## 6. Triggers for revisit

Re-run the MVP (and consider promoting to the elaborate
facade-over-store shape preserved in `OptimalReferencePlan.md §Phase
3 (locked plan)`) if any of the following becomes true:

- a later Python 3.15 build (beta / RC / final) shows a `try/except`
  regression that closes the top-two gap below 15%, or any future
  interpreter row drops `tryexcept` from first place.
- the optimal reference grows a feature whose access pattern hits
  the failure branch of `try/except` non-negligibly (any branch that
  can leave a field unset across multiple hot-path accesses).
- a downstream consumer needs O(1) bulk invalidation for the
  field — promote that store to `gen-counter` instead of forcing
  `try/except` everywhere.
- multi-field benchmarks ever materially disagree with this
  ranking — that would be a sign that bitmask's hypothesised
  cache-locality story is real at scale, and would justify the
  larger study.

## 7. How to reproduce

From the repo root:

```sh
uv run --python 3.12 python yidl/docs/validation/perf/init_detection_mvp.py
uv run --python 3.13 python yidl/docs/validation/perf/init_detection_mvp.py
uv run --python 3.14 python yidl/docs/validation/perf/init_detection_mvp.py
uv run --python 3.15 python yidl/docs/validation/perf/init_detection_mvp.py
```

Switching `--python` versions with `uv run` rebuilds `.venv`. After
sweeping the matrix, restore the project's pinned interpreter with
`uv sync --python 3.12` (or whichever version the project requires
at the time of the run).

Expected printed lines per run: one row per candidate plus a
trailing decision summary identifying the winner, the runner-up, the
gap, and whether the gap clears the 15% threshold.

## 8. Provenance

- Bench file: `yidl/docs/validation/perf/init_detection_mvp.py`.
- Plan section that specified the bench shape, decision rule,
  metrics, and integration with the broader study:
  `OptimalReferencePlan.md §Phase 3` (MVP form).
- Broader study integration: `PRE_IMPL_STUDY_IMPL_PLAN.md §Phase 4`
  defers the init-detection mechanism choice to this document.
- Python version matrix:
  `yidl/docs/validation/perf/version_matrix.py`.

All four rows of `version_matrix.py` are now populated. The 3.15
column was measured against `cpython-3.15.0a5` from the `uv` Python
distribution. Re-run on later 3.15 alphas / betas / RCs as they
become available and amend §2 in place; only re-open the decision
if a future row drops `tryexcept` from first place or closes the
top-two gap below 15%.

## 9. Update — 10-field shape with uniform accumulator

The bench in `init_detection_mvp.py` was reshaped after §1–§8 were
written:

- **10 fields per store** (was 1) — exercises a representative
  per-call workload rather than measuring the primitive in
  isolation.
- **Uniform per-field accumulator** — every candidate's `get_all`
  now does `x += self.fX` after the init-detection check on every
  field, then returns `x`. Previously the bench returned `self.f0`
  to defeat DCE without reading the other slots.
- **Code generation moved to `astichi`** — each candidate's class
  is composed via `astichi.build()` / `astichi.compile()`; per-field
  blocks are produced by a single `astichi_for(...)` loop with
  tuple-target decomposition, and the per-field attribute paths
  flow through `astichi_ref(external=...)`. The emitted Python
  source is identical to what the original hand-written templates
  produced (and is reproduced in §A below).

The accumulator change is the meaningful one for the numbers. It
adds one full `LOAD_ATTR + BINARY_OP + STORE_FAST` per field for
`bitmask`, `void`, and `gen-counter`, but only the
`BINARY_OP + STORE_FAST` for `tryexcept` — because `tryexcept`'s
init-detection check IS a `LOAD_ATTR`, the very same load doubles
as the accumulator read. That's a real-workload property, not a
bench quirk, and it widens `tryexcept`'s lead.

### Numbers (median ns / field, lower is better)

| Mechanism    | 3.12.12 | 3.13.12 | 3.14.3 | 3.15.0a5 |
|--------------|---------|---------|--------|----------|
| bitmask      | 23.54   | 36.26   | 30.30  | 15.02    |
| void         | 21.08   | 30.76   | 27.61  | 14.26    |
| **tryexcept**| **13.95** | **21.02** | **18.25** | **11.73** |
| gen-counter  | 17.67   | 31.47   | 28.38  | 14.35    |

Per-field — multiply by `N_FIELDS = 10` for ns/`get_all()`. Spreads
are single-digit on most rows; the largest outlier is 22.7%
(`gen-counter` on 3.12).

### Decision rule on the new shape

| Interpreter | Winner    | Runner-up   | Gap   |
|-------------|-----------|-------------|-------|
| 3.12.12     | tryexcept | gen-counter | 26.7% |
| 3.13.12     | tryexcept | void        | 46.3% |
| 3.14.3      | tryexcept | void        | 51.2% |
| 3.15.0a5    | tryexcept | void        | 21.5% |

Every row clears 15%, and `tryexcept` wins on every interpreter.
The recommendation in §4 stands and is now stronger: the lead
under realistic per-call workloads (check + use the value) is
larger than under primitive-isolation timing.

The §2 numbers are preserved unchanged as the historical record
for the single-field, primitive-isolation shape.

## Appendix A — Generated Python source per candidate

The four candidate classes below are the exact `_GEN_SRC` strings
produced by the `astichi`-driven builders in
`init_detection_mvp.py` for `N_FIELDS = 10`. The emitted source is
**identical across Python versions** — only the bytecode the
interpreter compiles it to differs. Code is shown verbatim for
review and as a regression diff target.

### A.1 `BitmaskStore`

```python
class BitmaskStore:
    __slots__ = ('f0', 'f1', 'f2', 'f3', 'f4', 'f5', 'f6', 'f7', 'f8', 'f9', '_mask')

    def __init__(self):
        self._mask = 0

    def get_all(self):
        m = self._mask
        x = 0
        if not m & 1:
            self.f0 = 42
            m |= 1
        x += self.f0
        if not m & 2:
            self.f1 = 43
            m |= 2
        x += self.f1
        if not m & 4:
            self.f2 = 44
            m |= 4
        x += self.f2
        if not m & 8:
            self.f3 = 45
            m |= 8
        x += self.f3
        if not m & 16:
            self.f4 = 46
            m |= 16
        x += self.f4
        if not m & 32:
            self.f5 = 47
            m |= 32
        x += self.f5
        if not m & 64:
            self.f6 = 48
            m |= 64
        x += self.f6
        if not m & 128:
            self.f7 = 49
            m |= 128
        x += self.f7
        if not m & 256:
            self.f8 = 50
            m |= 256
        x += self.f8
        if not m & 512:
            self.f9 = 51
            m |= 512
        x += self.f9
        self._mask = m
        return x
```

### A.2 `VoidStore`

```python
class VoidStore:
    __slots__ = ('f0', 'f1', 'f2', 'f3', 'f4', 'f5', 'f6', 'f7', 'f8', 'f9')

    def __init__(self):
        self.f0 = _VOID
        self.f1 = _VOID
        self.f2 = _VOID
        self.f3 = _VOID
        self.f4 = _VOID
        self.f5 = _VOID
        self.f6 = _VOID
        self.f7 = _VOID
        self.f8 = _VOID
        self.f9 = _VOID

    def get_all(self):
        x = 0
        if self.f0 is _VOID:
            self.f0 = 42
        x += self.f0
        if self.f1 is _VOID:
            self.f1 = 43
        x += self.f1
        if self.f2 is _VOID:
            self.f2 = 44
        x += self.f2
        if self.f3 is _VOID:
            self.f3 = 45
        x += self.f3
        if self.f4 is _VOID:
            self.f4 = 46
        x += self.f4
        if self.f5 is _VOID:
            self.f5 = 47
        x += self.f5
        if self.f6 is _VOID:
            self.f6 = 48
        x += self.f6
        if self.f7 is _VOID:
            self.f7 = 49
        x += self.f7
        if self.f8 is _VOID:
            self.f8 = 50
        x += self.f8
        if self.f9 is _VOID:
            self.f9 = 51
        x += self.f9
        return x
```

### A.3 `TryExceptStore`

```python
class TryExceptStore:
    __slots__ = ('f0', 'f1', 'f2', 'f3', 'f4', 'f5', 'f6', 'f7', 'f8', 'f9')

    def get_all(self):
        x = 0
        try:
            x += self.f0
        except AttributeError:
            self.f0 = 42
            x += self.f0
        try:
            x += self.f1
        except AttributeError:
            self.f1 = 43
            x += self.f1
        try:
            x += self.f2
        except AttributeError:
            self.f2 = 44
            x += self.f2
        try:
            x += self.f3
        except AttributeError:
            self.f3 = 45
            x += self.f3
        try:
            x += self.f4
        except AttributeError:
            self.f4 = 46
            x += self.f4
        try:
            x += self.f5
        except AttributeError:
            self.f5 = 47
            x += self.f5
        try:
            x += self.f6
        except AttributeError:
            self.f6 = 48
            x += self.f6
        try:
            x += self.f7
        except AttributeError:
            self.f7 = 49
            x += self.f7
        try:
            x += self.f8
        except AttributeError:
            self.f8 = 50
            x += self.f8
        try:
            x += self.f9
        except AttributeError:
            self.f9 = 51
            x += self.f9
        return x
```

### A.4 `GenCounterStore`

```python
class GenCounterStore:
    __slots__ = ('f0', 'f1', 'f2', 'f3', 'f4', 'f5', 'f6', 'f7', 'f8', 'f9', '_f0_gen', '_f1_gen', '_f2_gen', '_f3_gen', '_f4_gen', '_f5_gen', '_f6_gen', '_f7_gen', '_f8_gen', '_f9_gen', '_store_gen')

    def __init__(self):
        self._store_gen = 1
        self._f0_gen = 0
        self._f1_gen = 0
        self._f2_gen = 0
        self._f3_gen = 0
        self._f4_gen = 0
        self._f5_gen = 0
        self._f6_gen = 0
        self._f7_gen = 0
        self._f8_gen = 0
        self._f9_gen = 0

    def get_all(self):
        g = self._store_gen
        x = 0
        if self._f0_gen != g:
            self.f0 = 42
            self._f0_gen = g
        x += self.f0
        if self._f1_gen != g:
            self.f1 = 43
            self._f1_gen = g
        x += self.f1
        if self._f2_gen != g:
            self.f2 = 44
            self._f2_gen = g
        x += self.f2
        if self._f3_gen != g:
            self.f3 = 45
            self._f3_gen = g
        x += self.f3
        if self._f4_gen != g:
            self.f4 = 46
            self._f4_gen = g
        x += self.f4
        if self._f5_gen != g:
            self.f5 = 47
            self._f5_gen = g
        x += self.f5
        if self._f6_gen != g:
            self.f6 = 48
            self._f6_gen = g
        x += self.f6
        if self._f7_gen != g:
            self.f7 = 49
            self._f7_gen = g
        x += self.f7
        if self._f8_gen != g:
            self.f8 = 50
            self._f8_gen = g
        x += self.f8
        if self._f9_gen != g:
            self.f9 = 51
            self._f9_gen = g
        x += self.f9
        return x
```

## 10. Update — Cold-path measurement and break-even analysis

The §1–§9 numbers measure the **warm path** (every field already
initialised, so the init-detection branch is the success branch). The
warm bench amortises the cold-path cost away. This section measures it
explicitly and works out where each mechanism actually sits once
construction and first-use cost are counted.

### 10.1 What changed in the bench

`yidl/docs/validation/perf/init_detection_mvp.py` now runs two phases.

- **Warm bench** — unchanged from §9: `N=1_000_000`, 3 warm-ups, 21
  batches; per-field hot-path cost.
- **Cold bench** — `n_instances=10_000`, 2 warm-ups, 11 batches.
  Each batch:
  1. Allocates `n` fresh instances and times the construction loop.
  2. Calls `inst.get_all()` exactly once on each fresh instance and
     times that loop. Every per-field check is on the cold branch.
  3. `gc.disable()` over both windows; `gc.collect()` between batches
     so each batch starts with a clean heap.

Reported per row:
- `construct` — median ns per `factory()` call.
- `first_call` — median ns per first `get_all()` (and per-field).
- `total` — `construct + first_call`, the per-instance cost to obtain
  one fully-initialised store with one full read pass.
- `tryexcept_pays_off@K` — number of additional warm `get_all()` calls
  per instance after which `tryexcept`'s larger setup cost (10 cold
  `AttributeError`s) is repaid by its faster warm path:
  `K = (tryexcept_total − this_total) /
       (N_FIELDS · (this_warm − tryexcept_warm))`.
  `inf` would mean the alternative's warm path is no slower than
  `tryexcept`'s, so the cold investment never amortises.

### 10.2 Cold-bench results (median ns/instance, ns/field)

| candidate    | py 3.12         | py 3.13         | py 3.14         | py 3.15a5       |
|--------------|-----------------|-----------------|-----------------|-----------------|
| bitmask      | 49 + 374 = 423  | 62 + 616 = 679  | 65 + 470 = 535  | 41 + 211 = 253  |
| void         | 91 + 250 = 341  | 128 + 395 = 523 | 123 + 340 = 464 | 71 + 161 = 232  |
| tryexcept    | 28 + 2368 = 2396| 38 + 2788 = 2826| 33 + 2609 = 2641| 23 + 2137 = 2160|
| gen-counter  | 94 + 260 = 354  | 143 + 417 = 560 | 132 + 373 = 505 | 81 + 174 = 255  |

`construct` numbers confirm the structural predictions:
- `tryexcept.__init__` is empty → cheapest construct (~23–38 ns).
- `bitmask.__init__` writes one slot (`self._mask = 0`) → second
  cheapest (~41–65 ns).
- `void.__init__` writes 10 slots, `gen-counter.__init__` writes 11
  slots → 90–143 ns each.

`first_call` numbers isolate the cold-path branch. For three of the
four candidates the cold branch is a take-the-`if` plus one or two
attribute writes, and per-field cost is ~2× the warm number (~25–62 ns
on every Python). For `tryexcept` the cold branch is an
`AttributeError` raise + handler frame + slot write: per-field cost is
210–280 ns, i.e. ~5–13× a normal cold-path branch and ~12–20× its own
warm-path cost.

This is what the user's intuition was pointing at: the exception
object **does** cost something, and on the cold path it is the
dominant term.

### 10.3 Break-even (warm calls per instance until tryexcept wins)

| candidate    | py 3.12 | py 3.13 | py 3.14 | py 3.15a5 |
|--------------|---------|---------|---------|-----------|
| bitmask      | 20      | 14      | 18      | 57        |
| void         | 29      | 24      | 23      | 60        |
| gen-counter  | 54      | 22      | 21      | 60        |

Reading the table:
- On 3.13/3.14, **~14–24 warm calls/instance** is enough for
  `tryexcept` to recoup the AttributeError pile-up against the next
  best mechanism.
- On 3.12 the warm-path advantage of `tryexcept` is similar but the
  cold delta is smaller, so break-even slips out to ~20–54 calls.
- On 3.15a5 the alternatives' warm paths got dramatically faster
  (CPython tier-2/JIT optimisations on `LOAD_ATTR`/`STORE_ATTR`)
  while `tryexcept`'s cold path improved less; break-even shifts to
  ~60 calls/instance.

### 10.4 What this changes about the recommendation

`tryexcept` remains the warm-path winner on every Python version we
test (§9), but the cold-path cost reframes the decision rule:

- For long-lived stores that receive many reads per instance
  (≫ ~60 `get_all()` calls), `tryexcept` is unambiguously best on
  every supported version.
- For ephemeral stores that receive only a handful of reads before
  being discarded, `void` (or `gen-counter`) is competitive or better
  — the cold-path investment never amortises within the instance's
  lifetime.
- The decision rule from §9 ("clear winner, ≥15% gap on warm bench")
  still selects `tryexcept`, but should now be qualified: the
  recommendation assumes the YIDL workload is read-dominated. If a
  future shape is "construct-and-read-once", revisit with the cold
  bench in hand.

### 10.5 Caveat (still applies from §9)

The `tryexcept` numbers depend on never throwing on the hot path. If a
field can be missing under steady-state operation — for example
because it is conditionally initialised, or because invalidation
re-undoes a slot — every such miss costs another ~210–280 ns on the
cold-branch path. A workload that misses 1% of the time pays
roughly the warm cost twice over.

### A.5 How the source is generated

Each candidate is composed by `astichi`:

- a parent class shell (with `astichi_hole(...)` slots and any
  candidate-specific preamble such as `m = self._mask` or
  `g = self._store_gen`),
- one contribution per hole, each wrapping its per-field block in
  an `astichi_for(...)` loop with a tuple-decomposition target so
  every per-field literal (`bit = 1<<i`, `payload = 42+i`, the
  attribute path string) is bound to its own loop variable,
- per-field attribute paths produced via
  `astichi_ref(external=field).astichi_v` (LHS) and
  `astichi_ref(external=field)` (RHS), which lower to the
  corresponding `self.fX` attribute chain at materialize time.

`builder.build(unroll=True).materialize().emit(provenance=False)`
unrolls every loop, lowers every reference, and emits the source
shown above. The same `_GEN_SRC` is exec'd into each Python
interpreter under test.
