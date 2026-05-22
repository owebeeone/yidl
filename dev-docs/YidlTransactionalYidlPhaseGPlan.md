# YIDL Transactional Base Phase G Plan

## Scope

Phase G defines and implements `transient` fields using the same semantics as
the current `pyrolyze.lifecycle` transient support.

The important parity point is that transient is not "no state". It has a
non-working default/current value and a transaction-local working overlay. The
working overlay is visible through the default and working facades while the
transaction is active, is never visible through the current facade, and is
discarded on both commit and rollback.

Relevant current sources:

- `dev-docs/YidlDesignSummary.md` section 3 describes `transient` as
  tx-scoped scratch whose working value exists only while the group is open.
- `dev-docs/YidlDesignSummary.md` sections 16, 17, and 22 describe rollback
  cleanup, `working_default_factory`, and callable injection.
- `dev-docs/YidlTransactionalYidlPhaseF-1Plan.md` defines the `tx_key` /
  `tx_index` lane model, staged managed commits, and facade caching that
  transient must fit into.
- `dev-docs/YidlTransactionalYidlPhaseDPlan.md` says transient should be a
  sibling feature layer, not a rewrite of lifecycle core or managed.
- `pyrolyze/src/pyrolyze/lifecycle.py` is the parity reference for transient
  getter/setter and factory behavior. Use it read-only.
- `pyrolyze/tests/test_api_lifecycle.py` contains the behavioral parity cases
  for transient visibility, cleanup, working factories, cycles, and initvar
  injection.

## Goals

1. Lock transient storage semantics.
2. Add marker, harvester facts, YIDL facts, generated slots, and properties.
3. Define interaction with default factories.
4. Define visibility across default/current/working facades.
5. Keep the implementation as a feature YIDL layer on top of the Phase D split
   lifecycle base unless a missing YIDL surface is discovered and discussed.

## Non-Goals

1. Do not add owned or binding fields.
2. Do not add new transaction-manager protocol unless transient cannot be
   expressed using the F-1 `tx_key` / `tx_index` lane model.
3. Do not use transient as a generic scratch namespace.
4. Do not add validator/hook semantics beyond cleanup ordering. Phase F/F-1
   already owns validator and hook mechanics.

## F-1 Constraints

Phase G must not reintroduce `tx_group` as the YIDL lifecycle model term. Use:

- `tx_key` for the user-facing hashable transaction identity.
- `tx_index` for generated class-local dispatch and storage indexes.

Transient working storage is keyed by the same `tx_index` as managed fields. It
should not render transaction key literals into generated source. The generated
source should derive the lane with:

```python
tx_index = self.__yidl_tx_key_to_index__[tx_key]
```

Transient does not need managed's staged commit slot because transient never
publishes working values to current/default storage. Commit and rollback both
clear transient working state.

## Pyrolyze-Parity Semantics

Use the `pyrolyze.lifecycle` transient model:

1. A transient field has a non-working current/default value.
2. It also has one transaction-local working slot per field, associated with
   one `tx_index`.
3. The working slot is `VOID` when absent.
4. The current facade always reads the non-working current/default value.
5. The default and working facades read the working slot if it is present.
6. If the working slot is absent and the corresponding `tx_key` is active, the
   default and working facades materialize a working value and enlist the
   object in that transaction. A `working_default_factory`, when present, owns
   the materialized value. Otherwise the materialized value starts as the
   current/default value.
7. If no active transaction exists, reads fall back to the non-working
   current/default value.
8. Writing through the default or working facade requires an active transaction
   for the field's `tx_key` and writes the working slot.
9. Writing through the current facade is rejected.
10. Commit discards the working slot. It does not publish the transient value to
    current/default storage.
11. Rollback discards the working slot.

This keeps transient different from `managed`: a managed read remains
observational and should not enlist the object, while a transient read during an
active transaction creates transaction-local scratch state. Managed publishes
staged working values to current on commit; transient keeps its current/default
value and discards the working overlay.

## Resolved Behavior Matrix

- Storage scope:
  - non-working value lives in state-owned current/default storage.
  - working overlay lives in per-`tx_index` state-owned working storage.
  - facade-local storage is rejected for Phase G.
- Cleanup:
  - commit clears the working overlay.
  - rollback clears the working overlay.
  - neither operation mutates the non-working current/default value.
  - if Phase F hooks are present, before-commit hooks may observe the active
    working overlay; after-commit and after-rollback hooks run after transient
    cleanup and observe current/default values.
- Writes:
  - default and working setters require an active transaction.
  - no active transaction raises `RuntimeError`.
  - current setter rejects.
- Reads:

  | Action | default facade | current facade | working facade |
  | --- | --- | --- | --- |
  | read active tx | working value or working default, else current/default | current/default only | working value or working default, else current/default |
  | read no active tx | current/default | current/default | current/default |
  | write active tx | set working value and enlist | reject | set working value and enlist |
  | write no active tx | reject | reject | reject |

- Default-factory interaction:
  - A transient field may have `default` / `default_factory` for the
    non-working fallback value.
  - The non-working `default_factory` is resolved during construction and
    stored in current/default storage. It may use the normal factory injection
    names `self`, `current`, `working`, plus construction-time initvars, but
    does not by itself require retained initvar storage.
  - A transient field may have `working_default_factory` for tx-scoped working
    materialization.
  - `working_default_factory` runs on first default/working facade read during
    an active transaction when the working slot is `VOID`.
  - `working_default_factory` may use the same injected names as
    `pyrolyze.lifecycle`: `self`, `current`, `working`, and retained initvars.
  - Any factory or hook that can run after `__init__` and references an initvar
    requires that initvar to be retained on the state backing object.
  - `init=True` transient fields should have constructor parameters only for
    their non-working default value; they do not pre-populate tx-scoped working
    state.
  - `init=False` transient fields with `working_default_factory` are allowed.
  - Transient values should not be providers for construction-time
    `default_factory` because their working values do not exist until a
    transaction is active.

## Marker Surface Sketch

The frontend shape should be explicit:

```python
@lifecycle
class Counter:
    count: int = managed(default=0)
    temp_buffer: list[int] = transient(working_default_factory=list)
    pass_items: list[int] | None = transient(
        default=None,
        working_default_factory=lambda self, current, working, seed: [
            seed,
            self.count,
            current.count,
            working.count,
        ],
    )
```

The user-facing marker should live beside `field`, `managed`, and `classvar` in
`yidl.runtime.lifecycle`.

YIDL should use the Phase F-1 term `tx_key`. If a compatibility wrapper later
accepts pyrolyze's `tx_group` name, it should normalize that value into the same
`tx_key` fact before lowering.

## Retained Initvar Providers

Phase C treats most initvars as locals only. Phase G follows the pyrolyze
constructor-only model:

- construction-only consumers, such as eager transient `default_factory`, can
  use initvars without retaining them on state.
- late consumers, such as transient `working_default_factory`, must retain any
  referenced initvars on the state backing class.

Rules:

- Retained initvars get generated state slots, for example
  `_y_seed_initvar`.
- Retained initvars never get facade accessors. This includes both
  `init=True` and `init=False` initvars.
- Retained initvars are not lifecycle fields, are not transactional, and are
  not cleared by commit or rollback.
- `init=True` retained initvars are initialized from the generated constructor
  argument.
- `init=False` retained initvars must have a `default` or `default_factory`;
  the generated constructor computes that value and stores it on state.
- An `init=False` initvar with no source is rejected if any retained transient
  factory references it.
- Initvars that are not referenced by retained/transient factories keep the
  Phase C local-only behavior.

The dependency graph for late transient factories must include retained
initvars as provider nodes. Unknown provider names and unsupported initvar
provider shapes should surface as decorator-time lifecycle diagnostics, not as
generated-source `NameError`s.

## Lowered Shape Sketch

For a default transaction transient named `temp_buffer` that has a non-working
default and a `working_default_factory` using an initvar provider named `seed`:

```python
class Counter_State:
    __slots__ = (
        ...
        "_y_seed_initvar",
        "_y_temp_buffer_current",
        "_y_temp_buffer_working",
    )

def __init__(...):
    ...
    self._y_seed_initvar = seed
    self._y_temp_buffer_current = _Counter_temp_buffer_default
    self._y_temp_buffer_working = VOID

def _y_get_temp_buffer_current(self):
    return self._y_state._y_temp_buffer_current

def _y_get_temp_buffer_working(self):
    state = self._y_state
    if state._y_temp_buffer_working is not VOID:
        return state._y_temp_buffer_working
    if not state._y_has_active_tx(0):
        return state._y_temp_buffer_current
    state._y_ensure_enlisted_tx(0)
    state._y_temp_buffer_working = (
        _Counter_temp_buffer_working_default_factory(
            self=state._y_get_default_facade(),
            current=state._y_get_current_facade(),
            working=state._y_get_working_facade(),
            seed=state._y_seed_initvar,
        )
    )
    return state._y_temp_buffer_working

def _y_set_temp_buffer_working(self, value):
    state = self._y_state
    state._y_ensure_enlisted_tx(0)
    state._y_temp_buffer_working = value

def _rollback_tx_0_fields(self):
    ...
    self._y_temp_buffer_working = VOID

def _apply_prepared_commit_tx_0_fields(self):
    ...
    self._y_temp_buffer_working = VOID
```

If `working_default_factory` is absent, an active default/working getter still
materializes the working slot by assigning the current/default value. This gives
transient a consistent "read starts transaction-local state" contract. Mutable
current/default values may alias until a future copy/thaw policy is introduced;
Phase G records that as a follow-up rather than adding implicit copying.

## Suggested Fixture

Use a new golden source and materialized output:

```text
tests/data/gold_src/yidl_transactional_phase_g_transient.py
tests/data/goldens/materialized/yidl_transactional_phase_g_transient/
```

The fixture should include:

- `transient(working_default_factory=list)` for mutable tx-scoped state.
- a transient `working_default_factory` that references an `init=False`
  initvar with a default, proving retained initvar storage is generated.
- one transient with a literal non-working default.
- one transient without `working_default_factory` whose active read enlists the
  object and materializes the working slot from the current/default value.
- one transient with a non-working `default_factory` that references an initvar
  and is resolved during construction.
- a default transaction field and a non-default `tx_key` field.
- commit and rollback assertions proving both clear transient working state.
- current facade assertions proving current does not see active working state.
- assertions that current/default values survive transient commit and rollback.
- assertions that retained initvars have no facade accessors.
- generated-source checks that no transaction key literals are used for branch
  dispatch.

## Verification

Goldens should show successful generated source and runtime behavior for the
chosen policy. Focused tests should cover invalid combinations.

Minimum focused tests:

- writing transient without an active transaction raises.
- reading a `working_default_factory` transient during an active transaction
  materializes once and enlists the state.
- reading a transient without `working_default_factory` during an active
  transaction materializes once from the current/default value and enlists the
  state.
- reading the same transient without an active transaction returns the
  non-working current/default value and does not materialize working state.
- commit clears transient working state.
- rollback clears transient working state.
- current facade never exposes active transient working state.
- non-working `default_factory` can consume construction-time initvars without
  retaining them when there is no late consumer.
- retained initvars used by transient factories are stored on state and are not
  exposed as facade properties.
- `initvar(init=False)` without `default` or `default_factory` is rejected when
  referenced by a transient factory.
- a transaction-method marker still cannot introduce a new `tx_key`; keys come
  from lifecycle fields or inherited metadata.

## Parity Constraint

Phase J replacement-readiness should include transient behavior. Phase G should
therefore avoid semantics that cannot plausibly map to the supported
`pyrolyze.lifecycle` transient surface. If parity requires a different
behavior than the recommended direction above, update this plan before
implementation.

## Roll-Build

Suggested tag prefix:

```text
txphaseG-transient/
```

### Slice G1: Marker And Harvesting

Add the `transient(...)` marker beside `field`, `managed`, `initvar`, and
`classvar`.

Deliverables:

- marker accepts `default`, `default_factory`, `working_default_factory`,
  `init`, and `tx_key`.
- harvester emits transient field facts and factory-callable facts.
- unsupported signatures for `default_factory` and `working_default_factory`
  produce decorator-time diagnostics.
- `tx_group` is not introduced into the YIDL fact model.

Verification:

- focused marker/harvester tests.
- no generated output changes are required unless the marker is wired into the
  golden fixture in this slice.

### Slice G2: Transient Feature YIDL Facts

Add a `lifecycle_transient.yidl` feature layer on top of the Phase D split.

Deliverables:

- transient field facts compile through the existing split YIDL model.
- computed facts identify transient non-working storage, working slots,
  `tx_index`, retained initvar providers, and factory injection demands.
- inherited lifecycle fields and transaction keys still merge as before.

Verification:

- compile/golden check for the new feature YIDL layer.
- focused diagnostic for a transient transaction key mismatch if the field
  overrides an inherited field's `tx_key`.

### Slice G3: Non-Working Storage And Constructor Defaults

Generate the current/default side of transient state.

Deliverables:

- state class has a non-working storage slot for each transient field.
- literal `default` values and eager `default_factory` values initialize that
  slot during construction.
- transient `default_factory` supports construction-time initvar injection.
- transient `default_factory` supports the normal factory injection names
  `self`, `current`, and `working`.
- current facade reads the non-working value.
- current facade setter rejects.

Verification:

- golden output shows current/default slots and constructor assignment.
- runtime assertions prove current/default values exist before any transaction.

### Slice G4: Working Overlay And Working Factories

Generate default/working facade overlay access.

Deliverables:

- state class has a working slot per transient field.
- default and working facades read the working value when present.
- default and working facades materialize missing working values on active
  reads, using `working_default_factory` when present and current/default
  fallback otherwise.
- default and working setters require an active transaction and write the
  working slot.
- `working_default_factory` materializes only while the corresponding `tx_key`
  is active.
- `working_default_factory` receives injected `self`, `current`, `working`, and
  retained initvars.
- retained initvars get state slots but no facade accessors.

Verification:

- golden output shows the overlay getter/setter shape.
- runtime assertions match pyrolyze's transient visibility tests.
- focused diagnostics cover unsupported `working_default_factory` signatures
  and `initvar(init=False)` without a source when referenced by a late factory.

### Slice G5: Commit/Rollback Cleanup And Multi-Key Coverage

Wire transient cleanup into Phase F-1 transaction lanes.

Deliverables:

- commit clears transient working slots without publishing them to current.
- rollback clears transient working slots.
- cleanup is emitted per `tx_index`.
- before-commit hooks, if present, run before transient cleanup; after-commit
  and after-rollback hooks run after transient cleanup.
- generated dispatch derives `tx_index` from runtime `tx_key`; no transaction
  key literals are rendered into branch conditions.
- non-default `tx_key` transient fields work independently of the default key.

Verification:

- golden output shows cleanup in commit/rollback helpers.
- runtime assertions prove commit and rollback reset to current/default values.
- runtime assertions cover at least one non-default `tx_key`.

### Slice G6: Phase Golden And Parity Assertions

Complete the end-to-end transient fixture.

Deliverables:

- `tests/data/gold_src/yidl_transactional_phase_g_transient.py`
- materialized decorator and generated-output goldens.
- prettier variants for human inspection.
- targeted focused tests for invalid combinations not covered by the golden.

Verification:

- focused transient tests pass.
- full YIDL test suite passes.
