# YIDL Pyrolyze Lifecycle Parity Plan

## Purpose

This document turns the remaining `pyrolyze.lifecycle` parity gaps into an
implementation roadmap for the YIDL transactional lifecycle.

Phases A-H established the floor:

- generated slotted state and facade classes
- current/default/working facades
- transaction manager integration
- managed fields with current/working/staged state
- parameterized `default_factory`
- transient fields
- transaction hooks and validators in the narrowed YIDL form
- owned/binding fields in their narrowed form
- MRO field merge and generated-class peeling

The remaining work is no longer about proving that YIDL can generate the
transactional lifecycle. It is about deciding which pieces of the old
`pyrolyze.lifecycle` API should be preserved, which should be replaced by
generated-code equivalents, and which should stay deliberately unported.

## Source Baseline

Relevant source areas:

- old implementation: `pyrolyze/src/pyrolyze/lifecycle.py`
- YIDL decorator frontend: `yidl/src/yidl/runtime/lifecycle.py`
- YIDL harvester: `yidl/src/yidl/runtime/lifecycle_harvester.py`
- YIDL marker definitions: `yidl/src/yidl/runtime/lifecycle_markers.py`
- YIDL binding support: `yidl/src/yidl/runtime/bindings.py`
- YIDL lifecycle source: `yidl/tests/data/yidl/yidl_transactional_lifecycle`

Phase J already owns productionization:

- generated lifecycle module import instead of decorator-time `exec`
- packaging policy for generated YIDL artifacts
- running the full ported parity suite as a replacement-readiness gate
- performance benchmark baselines

This document covers the semantic parity work that should happen before Phase J
can be useful.

The main old lifecycle test corpus is:

- `pyrolyze/tests/test_api_lifecycle.py`

Porting that file's lifecycle tests is now a first-class workstream in this
plan, not a final Phase J afterthought.

## Parity Categories

### Category A: Missing Field Kinds

The old implementation exposes field helpers that the YIDL transactional path
does not yet model:

- `const(...)`
- `static(...)`

The near-term parity target is only `const` and `static`.

`const` is the smallest: initialize once, expose read-only properties.

`static` is larger: write-once or lazy first-read behavior. It needs a sentinel
state and clear setter semantics.

`local_store` and `derived` are deliberately deferred. They are useful old
helpers, but they are not currently needed for the YIDL transactional lifecycle
replacement path and they both become more coherent once close/teardown and
cache invalidation policy have a concrete consumer.

### Category B: Deferred Close Protocol

The old implementation has a teardown path:

- rollback or clean open transaction state
- run per-field close hooks
- mark instance closed
- reject future operations after close

The YIDL transactional path has no generated `close()` method or closed flag.
For now this is explicitly deferred.

Close should only be revisited if a concrete consumer needs deterministic
teardown before object collection. Tests that only assert old `close()` behavior
should be ported as documented unsupported/deferred cases, not as failing YIDL
requirements.

### Category C: Initvar Closure

The old implementation does more with initvars than the current transactional
harvester:

- reject unused initvars
- retain initvars when later runtime consumers need them
- normalize retained initvars via `to_frozen()` where appropriate

YIDL currently has retained initvar storage only where Phase G needed it for
transient working default factories. The feature should become general rather
than transient-specific.

### Category D: Callable Injection

Old factories and hooks support named argument injection. Important injectable
names include:

- `self`
- `current`
- `working`
- `previous`
- `tx_key` / `tx_key` depending on final naming
- retained initvars

Current YIDL support is split:

- normal `default_factory` supports field/self-style dependencies and initvars
  from Phase C
- transient `working_default_factory` proves broader
  `self/current/working/initvar`-style injection can be generated
- transaction hooks currently call methods on the default facade without
  broader injection

The parity feature should unify this into one computed fact model for callable
parameter binding.

### Category E: Initial Working Values

The old `managed(...)` supports `initial_working=...` and tracks whether a value
has ever committed.

YIDL has no `ever_committed` flag and no pre-first-commit working visibility
rule. This is a real semantic gap, but it should come after callable injection
and the core commit/rollback invalidation rules are stable.

### Category F: Managed Sidecars

The old implementation can carry independent per-field state:

- `state_factory`
- `state_copy`
- `field_state`

This supports mutable working state for fields where a shallow current/working
slot is not sufficient.

YIDL has no equivalent. This is a larger field-kind extension, not a small
compatibility patch.

### Category G: Previous Snapshot For `after_commit`

The old implementation captures previous values and passes them to
after-commit hooks.

YIDL after-commit hooks currently do not receive a previous snapshot. The
missing piece is not only a function argument; the transaction prepare/apply
pipeline must capture the snapshot at the correct point and make it available
to the hook runner.

### Category H: Binding Parity Decision

Phase H deliberately chose narrowed binding support:

- `binding(...)` is plain stored `BindingBase` validation
- `owned(...)` is managed plus `BindingBase`/`BindingDict` validation and
  accepted-on-commit behavior
- YIDL binding support relies on Python intrinsic references

The old implementation includes explicit `inc_ref()` / `dec_ref()`, deferred
cleanup ordering, and transaction-overlay binding behavior.

This is the one category that still contains a major design choice. Do not
quietly drift into the old model. Either keep the narrowed YIDL model, or
create a future binding-parity phase with a concrete consumer requirement.

### Category I: Pyrolyze Lifecycle Test Porting

The old test file `pyrolyze/tests/test_api_lifecycle.py` is the practical parity
spec. It should be ported into YIDL in waves.

The port is not a blind copy. Each test must be classified:

- **supported**: YIDL should pass with equivalent behavior.
- **narrowed**: YIDL intentionally supports a narrower behavior; adapt the test
  to the YIDL contract and document the old behavior that is omitted.
- **deferred**: behavior is desirable but assigned to a later parity category.
- **rejected**: behavior belongs to deliberately unported legacy machinery.

The porting work should preserve test intent and names where practical so future
diffs against the old test corpus remain reviewable.

## Deliberately Not Ported

These old implementation details should not be reintroduced unless a specific
consumer requires them:

- `LCKind` class lattice
- `_generate_kind_helpers()`
- runtime ftable / descriptor engine
- sparse record/dict value stores
- `managed_context` decorator name and `LifecycleContext` inheritance model
- public low-level `lifecycle_field(...)` author API
- user `__init__` / `__post_init__` chaining on lifecycle classes
- `unmanaged_store` container as a separate concept

The YIDL implementation replaces these with generated fields, generated
properties, explicit slotted state, and feature-layered YIDL concepts.

## Roadmap

### P0: Pyrolyze Test Inventory And Parity Harness Skeleton

Goal: define the parity target before adding more semantics.

Deliverables:

- an inventory of every lifecycle test in
  `pyrolyze/tests/test_api_lifecycle.py`
- a classification table: supported, narrowed, deferred, rejected
- a YIDL parity test module that starts with currently supported behavior
- a compatibility table listing supported, narrowed, deferred, and rejected
  old features
- no new generated behavior

Suggested fixture categories:

- construction and plain/managed field access
- begin/commit/rollback
- hooks/validators in currently supported narrowed form
- owned/binding narrowed behavior
- MRO merge

Why first: it prevents future work from accidentally claiming broad parity when
the YIDL behavior is intentionally narrower.

Suggested output files:

- `yidl/tests/test_lifecycle_pyrolyze_parity.py`
- `yidl/dev-docs/YidlPyrolyzeLifecycleTestInventory.md`

The inventory should include one row per old test:

| Old test | YIDL status | Owner slice | Notes |
| --- | --- | --- | --- |
| `test_...` | supported/narrowed/deferred/rejected | P0/P1/etc. | concise reason |

Do not skip large groups silently. If a test depends on close, explicit
`lifecycle_field(...)`, runtime ftable internals, or old binding refcounts, mark
that in the inventory.

### P1: `const(...)`

Goal: add the simplest missing field kind.

Semantics:

- initialized during construction from an explicit constructor value,
  default, or default_factory
- readable on default/current/working facades, unless a narrower facade policy
  is chosen
- no setter on any facade after initialization
- no transaction state
- no close behavior

Implementation shape:

- marker in `lifecycle_markers.py`
- harvester fact support
- YIDL family variant in the lifecycle concept
- computed collection `ConstFields`
- state slot or class-level storage decision pinned in the plan
- property contributions for facades
- init parameter/default handling

Recommended storage:

- store const values on the generated state object for instance-level consts
- expose read-only properties on facade base or relevant facades

Verification:

- golden source for const field
- runtime test that assignment raises
- MRO override test
- default_factory dependency test if the marker supports factories

### P2: `static(...)`

Goal: add write-once/lazy field behavior.

Semantics:

- constructor values count as the first write
- if no constructor value is supplied, the slot starts as `VOID`
- `static(default=...)` initializes lazily on first read
- `static(default_factory=...)` runs lazily on first read
- explicit first assignment is allowed before any default/default_factory read
- default/current/working facades expose the same static value
- subsequent assignment raises

Recommended V0:

- store per instance in state
- one value slot with `VOID` as the unset sentinel
- no transaction state
- no close behavior

Verification:

- default path
- lazy factory path
- first assignment path
- second assignment raises
- transaction begin/commit does not affect static value

### Deferred: `local_store(...)`

Status: deferred until a concrete consumer needs non-transactional scratch
state or deterministic teardown.

Old behavior:

- non-transactional
- stored on state
- readable/writable through lifecycle views
- not transactionally committed or rolled back
- reset by the old close protocol

Reasons to defer:

- current YIDL consumers do not need it
- close/teardown is explicitly deferred
- adding it now would increase the parity surface without exercising the core
  transactional replacement path

When revived, the V0 should pin whether default/current/working facades all
share the same state slot or whether the field is exposed only on the default
facade.

Inventory handling:

- mark old `local_store` construction/access tests deferred
- mark old close-cleanup tests deferred with the close protocol

### Deferred: `derived(...)`

Status: deferred until a concrete consumer needs generated cached values.

Old behavior:

- cached value held outside the transactional current/working records
- getter/setter shared by lifecycle views
- reset on commit, rollback, and close

Reasons to defer:

- current YIDL consumers do not need it
- derived invalidation policy should be designed with real dependency/caching
  requirements, not as a speculative port
- close invalidation is part of old behavior, and close is deferred

When revived, the V0 should choose between:

- broad invalidation on every commit/rollback
- explicit declared dependencies
- a factory-backed read-only property
- the old writable-cache shape

Inventory handling:

- mark old `derived` cache tests deferred
- mark old close-invalidation tests deferred with the close protocol

### P3: Broad Initvar Retention

Goal: move retained initvar support out of the transient-only path.

Semantics:

- harvester computes which initvars are consumed by runtime callables
- consumed initvars are stored on state
- unused initvars are rejected unless explicitly marked as allowed/discarded
- retained values are frozen/normalized if parity requires old `to_frozen()`
  behavior

Consumers:

- default factories that run after construction
- working default factories
- hooks
- validators
- deferred derived factories, if `derived` is revived later

Verification:

- unused initvar diagnostic
- retained initvar used by transient working factory
- retained initvar used by hook or transient/default factory
- initvar not exposed as normal property

### P4: General Callable Injection

Goal: unify callable parameter binding across factories, hooks, validators, and
future derived fields.

Injected names:

- `self`
- `current`
- `working`
- `previous`
- `tx_key` or `tx_key` after naming is pinned
- retained initvars
- field/provider names already supported by default-factory dependency logic

Implementation shape:

- harvester records callable parameter names and callable kind
- YIDL computed operation validates injectable names and emits argument rows
- Astichi resources use generated keyword args, not `locals()`
- unsupported `*args`, `**kwargs`, positional-only parameters reject

Recommended naming:

- generated state and transaction internals should use `tx_key`
- old API compatibility may still accept `tx_key` as a callable parameter name
  if the old hook surface is preserved

Verification:

- default_factory receives field provider
- working_default_factory receives `self`, `current`, `working`, initvar
- before-commit hook receives `self`, `current`, `working`, `tx_key`
- commit validator receives supported injected names
- unsupported callable signatures reject at decorator time

### P5: `initial_working`

Goal: support pre-first-commit working value visibility for managed fields.

Dependencies:

- managed transaction path from Phase F-1
- callable injection if `initial_working` can be a callable in the selected
  parity surface

Semantics:

- state tracks `_y_ever_committed`
- before first successful commit, working facade read may return
  `initial_working`
- after first commit, normal current/working semantics apply
- rollback before first commit restores the initial-working visibility rule
  only if old parity requires it; otherwise pin a simpler generated rule

Verification:

- initial working visible in active transaction before first commit
- normal current visible outside transaction
- after first commit, initial working no longer applies
- inheritance/override behavior

### P6: Previous Snapshot For `after_commit`

Goal: provide old-style `previous` data to after-commit hooks.

Dependencies:

- callable injection
- stable commit prepare/apply pipeline

Implementation shape:

- capture previous values during prepare or immediately before apply
- store a snapshot object or generated lightweight record for the transaction
  index/key
- pass `previous` to after-commit hook argument rows
- clear snapshot after hooks complete

Recommended V0:

- snapshot current facade values for fields in the committed transaction key
- do not snapshot unrelated transaction keys
- snapshot object is read-only from user code

Verification:

- after-commit sees old and new values
- rollback does not call after-commit
- multi-key transaction only snapshots relevant fields
- hook exceptions still follow Phase F contract

### P7: Managed Sidecars

Goal: support advanced mutable managed field state.

Dependencies:

- callable injection if state factories are injectable
- snapshot/invalidation decisions

Semantics to pin:

- `state_factory`
- `state_copy`
- `field_state`
- commit/rollback interaction
- deterministic cleanup if a future close protocol is added

Recommended approach:

- do not start this until a concrete consumer exists
- if implemented, make it a feature YIDL layer over managed fields
- add a dedicated state slot family separate from current/working/staged value
  slots

Verification:

- mutable working state does not mutate current state before commit
- commit applies copied/frozen state
- rollback drops working sidecar state
- rollback drops sidecar state
- close-specific cleanup remains deferred

### P8: Binding Parity Decision

Goal: decide whether narrowed Phase H binding support is enough.

Two acceptable outcomes:

1. **Keep narrowed YIDL binding.**
   - document that explicit `inc_ref()` / `dec_ref()` parity is intentionally
     unsupported
   - keep relying on intrinsic Python references
   - add cycle-avoidance tests if needed

2. **Create full binding-parity phase.**
   - restore explicit refcount protocol
   - add transaction overlay binding staging
   - add deferred cleanup ordering against owned fields
   - add close integration only if the close protocol is later revived

Do not implement outcome 2 without a real consumer. It is a large semantic
surface and can easily complicate the generated model.

## Smaller Gaps

These should be folded into the closest semantic phase or Phase J:

- `current_setter_policy="stage_working"` decorator option
- `compare=` knob exposed on helpers
- at-most-one `commit_validator` per transaction key/group in the harvester
- stdlib `InitVar[...]` / `ClassVar[...]` annotation recognition, if desired
- runtime lazy factory cycle guard
- field-declared hook callables, if method decorators are insufficient
- importable generated module packaging

Suggested placement:

| Gap | Suggested owner |
| --- | --- |
| `current_setter_policy` | managed/transaction phase after P5 |
| `compare=` | marker/harvester compatibility slice |
| commit-validator uniqueness | P4 or a small harvester diagnostic slice |
| stdlib annotation recognition | frontend compatibility slice |
| runtime lazy cycle guard | P4 depending on callable shape |
| field-declared hooks | P4 |
| importable generated module | Phase J |

## Roll-Build Strategy

Do not roll all parity categories together. The semantic surface is too broad.

Recommended roll-build sequence:

### Roll 1: Low-risk missing fields

Tag prefix:

```text
parity-fields1/
```

Slices:

1. P0 test inventory and parity harness skeleton
2. P1 `const`
3. P2 `static`

Reason: proves new field-kind layering without close/invalidation complexity.

### Deferred Roll: Local Store And Derived

Tag prefix:

```text
parity-deferred-local-derived/
```

Slices:

1. `local_store`, only with a concrete consumer
2. `derived`, only with a concrete consumer

Reason: both are deliberately deferred. Do not start this roll as part of the
near-term parity path.

### Roll 2: Injection and initvar closure

Tag prefix:

```text
parity-injection/
```

Slices:

1. P3 broad retained initvars
2. P4 general callable injection
3. commit-validator uniqueness diagnostic

Reason: callable injection needs retained initvars and is needed by hooks,
validators, and some future factory shapes.

### Roll 3: Transaction-history behavior

Tag prefix:

```text
parity-tx-history/
```

Slices:

1. P5 `initial_working`
2. P6 previous snapshot for `after_commit`

Reason: both require transaction boundary state beyond current/working/staged
values.

### Roll 4: Optional advanced parity

Tag prefix:

```text
parity-advanced/
```

Slices:

1. P7 managed sidecars, only with a concrete consumer
2. P8 full binding parity, only if narrowed Phase H support fails real use

Reason: both are large and should not block replacing the old implementation
for supported cases.

## Golden Test Shape

Successful behavior should use the existing YIDL golden/materialized harness.

For each semantic roll:

- add one new YIDL feature file if the feature is a layer
- add one new golden source case that materializes:
  - generated decorator source
  - generated decorator prettier source
  - generated user-output source
  - generated user-output prettier source
- runtime assertions should execute both unpretty and pretty generated output
- bespoke tests should cover only harvester diagnostics, parser mechanics, and
  cases the golden harness cannot express cleanly

Avoid duplicating success assertions in bespoke tests when a golden already
materializes and executes the same scenario.

## Porting `pyrolyze.lifecycle` Tests

Port the old lifecycle tests incrementally, but keep the inventory complete from
P0 onward.

Primary source:

- `pyrolyze/tests/test_api_lifecycle.py`

Suggested destination:

- `yidl/tests/test_lifecycle_pyrolyze_parity.py`

Porting rules:

1. Keep old test names where practical, prefixed or grouped only when needed.
2. Replace old imports with the YIDL lifecycle surface.
3. For supported behavior, preserve the original assertion intent.
4. For narrowed behavior, adapt the assertion and cite the narrow contract in a
   short comment.
5. For deferred behavior, add an inventory row but do not add a skipped test
   unless it adds useful executable documentation.
6. For rejected behavior, add an inventory row explaining the replacement YIDL
   model.

Initial classification hints:

| Old behavior cluster | Initial YIDL status |
| --- | --- |
| construction, plain fields, managed transactions | supported |
| transaction manager begin/commit/rollback behavior | supported or narrowed |
| hooks/validators without injection | supported |
| hooks/validators with old injection forms | deferred to P4 |
| unused initvar diagnostics | deferred to P3 if missing in harvester |
| `const` / `static` | deferred to P1/P2 |
| `local_store` / `derived` | deferred with no active roll |
| `initial_working` | deferred to P5 |
| previous snapshot in `after_commit` | deferred to P6 |
| managed sidecars | deferred to P7 |
| explicit binding refcount behavior | narrowed or deferred to P8 |
| `close()` behavior | deferred, no active owner |
| `lifecycle_field(...)` low-level API | rejected |
| runtime ftable/descriptors internals | rejected |

## Performance Guardrails

The old implementation is slow because it routes behavior through runtime
descriptor tables. The YIDL replacement should preserve generated direct-field
paths.

For each parity roll, inspect generated output for:

- no dict-backed generic field access on hot getters/setters
- no `locals()` for factory/hook args
- no transaction manager call on ordinary current/default reads
- no per-access signature inspection
- no per-access hook table lookup if the target can be generated directly

Run the constructor/access performance harness after major field-kind additions,
especially `static`, retained-initvar injection, and managed sidecars.

## Open Decisions

These should be resolved before their owning roll starts:

1. `static` lazy factory timing and first-assignment behavior.
2. Whether default/current/working facades all expose `const`, `static`, and
   future deferred field kinds.
3. Whether hook injection accepts the old parameter name `tx_key`, the newer
   internal name `tx_key`, or both.
4. Shape of the previous snapshot object.
5. Whether full old binding refcount parity is needed.

## Recommended Next Step

Start with Roll 1:

1. inventory and classify `pyrolyze/tests/test_api_lifecycle.py`
2. create the parity harness skeleton and compatibility table
3. implement `const`
4. implement `static`

This is the lowest-risk way to make measurable parity progress. It exercises
new field-kind layering and generated output without entangling previous
snapshots, managed sidecars, or binding redesign.
