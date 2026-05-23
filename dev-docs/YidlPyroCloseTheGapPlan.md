# YIDL/Pyro Lifecycle Close-The-Gap Plan

## Purpose

This plan closes the practical gap between the current YIDL transactional
lifecycle and the work-in-progress lifecycle usage under:

- `pyrolyze/src/pyrolyze/runtime/context_state_lcm/context_base.py`
- `pyrolyze/src/pyrolyze/runtime/context_state_lcm/*.py`

The goal is not full historical `pyrolyze.lifecycle` parity. The goal is to
make the current Pyro LCM usage representable by the YIDL lifecycle model
without reintroducing the old runtime descriptor engine.

This plan is roll-buildable: each slice has a bounded goal, expected changes,
verification, and a stop condition.

## Hard Constraint

During this plan, edits under `pyrolyze/` are allowed only for the canonical
transaction naming cleanup:

- remove `tx_key`
- replace it with `tx_key`
- update related plural and derived names

This includes the Slice 1 rename inside the legacy
`pyrolyze/src/pyrolyze/lifecycle.py` implementation. It does not authorize any
other Pyro behavior change.

If any later slice appears to require a `pyrolyze/` source change that is not
part of the `tx_key` to `tx_key` cleanup, the rollout must stop and discuss
that change explicitly before proceeding.

YIDL files, YIDL tests, YIDL generated goldens, and YIDL dev docs may change as
needed by the slices.

## Related Inputs

Discussion inputs:

- `yidl/scratch/PyroYidlGapsDiscussion.md`
- `yidl/dev-docs/YidlPyrolyzeLifecycleParityPlan.md`
- `yidl/dev-docs/YidlDesignSummary.md`
- `yidl/dev-docs/YidlCodingRules.md`

Relevant implementation areas:

- `yidl/src/yidl/runtime/lifecycle.py`
- `yidl/src/yidl/runtime/lifecycle_harvester.py`
- `yidl/src/yidl/runtime/lifecycle_markers.py`
- `yidl/src/yidl/runtime/transaction_yidl.py`
- `yidl/tests/data/yidl/yidl_transactional_lifecycle/`
- `pyrolyze/src/pyrolyze/runtime/context_state_lcm/`
- `pyrolyze/src/pyrolyze/lifecycle.py`

## Non-Goals

These are deliberately outside this plan unless a slice hits a stop condition
and the user explicitly expands the scope:

- full old `pyrolyze.lifecycle` parity
- generated `close()` protocol
- `derived`
- full binding parity with explicit old-style `inc_ref()` / `dec_ref()`
- broad `_state` compatibility with the old lifecycle state object
- implicit user `__init__` chaining without a separate decision
- production packaging of generated lifecycle modules

## Naming Decision: `tx_key`

`tx_key` is a bad name for the concept. The value is a hashable transaction
key. This checkout and its submodules can be migrated directly.

There should be no long-term compatibility alias for `tx_key`.

Canonical names:

| Old | New |
| --- | --- |
| `tx_key` | `tx_key` |
| `tx_keys` | `tx_keys` |
| `tx_key_key` | `tx_key` |
| `tx_key_set` | `tx_key_set` |
| `__yidl_tx_key_to_index__` | `__yidl_tx_key_to_index__` |
| `TxKeys` | `TxKeys` |
| `TxKeyKey` | `TxKey` |

Do not blindly rename unrelated English uses of "group" unless they are part of
the transaction-key surface. For example, a class name such as
`GroupTransactionManager` can be evaluated during the rename, but the key goal
is to remove `tx_key` terminology. If leaving a non-`tx_key` "group" name
makes generated code read incorrectly, rename it in the same slice and document
the reason in the commit message.

## Roll-Build Rules

Before starting the roll-build:

1. Start from a clean git tree for the repository being changed.
2. Create a start tag with the requested prefix.
3. Implement one slice at a time.
4. Commit and tag only when the slice goal is met and focused verification
   passes.
5. Stop instead of forcing progress if a slice reveals a semantic change that
   contradicts this plan.

Recommended tag prefix for this plan:

```text
pyro-gap/
```

Suggested tags:

- `pyro-gap/start`
- `pyro-gap/01-tx-key`
- `pyro-gap/02-field-matrix`
- `pyro-gap/03-callable-injection-core`
- `pyro-gap/04-self-factory-policy`
- `pyro-gap/05-local-store`
- `pyro-gap/06-transaction-manager-access`
- `pyro-gap/07-lcm-representability`

## Verification Strategy

Use canonical YIDL fixtures and generated source goldens for success-path
behavior. Use focused tests for narrow mechanics and diagnostics.

Each semantic slice should prefer:

- a YIDL fixture under `yidl/tests/data/yidl/` when generated output changes
- materialized golden output under `yidl/tests/data/goldens/materialized/`
- a focused runtime test when the behavior is hard to see from generated source
- a diagnostic test for rejected factory signatures or unsupported constructs

Avoid duplicating full success-path assertions in bespoke tests when the golden
harness already owns the generated source shape.

Each semantic slice after Slice 2 must either include
`dev-docs/YidlLifecycleFieldKindMatrix.md` in its diff or state in the commit
notes why the slice did not change matrix semantics.

Generated artifacts must be regenerated through the YIDL generation pipeline,
not hand-edited. The expected regeneration path is:

```bash
uv run python -m yidl.testing.versioned_test_harness regen-goldens
```

If a slice changes the generated lifecycle base module, regenerate
`src/yidl/runtime/_generated_lifecycle_base.py` from the lifecycle YIDL source
using the existing lifecycle generation path before refreshing goldens. A slice
may use a narrower focused command while iterating, but the committed artifact
diff must be reproducible from the source YIDL and checked-in gold-source
fixtures.

## Slice 1: Canonical `tx_key` Rename

### Goal

Remove `tx_key` terminology across YIDL, Pyro, tests, docs, generated
goldens, and fixtures. `tx_key` becomes the only accepted spelling.

This is the only slice that may edit `pyrolyze/`.

### Expected Edits

YIDL runtime:

- rename marker fields and function parameters from `tx_key` to `tx_key`
- rename transaction manager method parameters from `tx_key` to `tx_key`
- rename internal variables and class metadata:
  - `tx_keys` to `tx_keys`
  - `tx_key_set` to `tx_key_set`
  - `__yidl_tx_key_to_index__` to `__yidl_tx_key_to_index__`
- update generated code templates in lifecycle YIDL sources
- update generated materialized goldens

Pyrolyze source:

- rename lifecycle marker kwargs and runtime transaction names from
  `tx_key` to `tx_key`
- include the legacy implementation module `pyrolyze/src/pyrolyze/lifecycle.py`
  in the rename; there is no surviving `tx_key=` compatibility alias in this
  checkout
- update `PASS_TX_KEY` style constants if they are transaction-key constants,
  for example `PASS_TX_KEY`
- preserve transaction-key values such as `"context_pass"`; only the identifier
  spelling changes unless a value is demonstrably wrong
- update lifecycle WIP declarations such as:
  - `managed(..., tx_key=PASS_TX_KEY)`
  - `transient(..., tx_key=PASS_TX_KEY)`
- do not remove `compare="identity"` from Pyro WIP declarations in this slice;
  YIDL representability handles that keyword as compatibility metadata later in
  this plan

Docs and tests:

- update YIDL docs and scratch docs where they describe the current surface
- update tests to use `tx_key`
- keep archival history docs only if they are explicitly historical and the
  test grep allows them; otherwise prefer updating them too to avoid confusion

### Search Checklist

After the slice, these searches should either produce no results or only
explicitly accepted historical references:

```bash
rg -n "tx_key|tx_keys|TxKey|TxKeys|tx key|tx keys" .
```

The target is no active source, fixture, or golden use of `tx_key`.

Expected high-signal rename targets include:

- `tx_key_to_index` and `__yidl_tx_key_to_index__`
- generated operation names such as `tx_keys_params`
- generated records/resources such as `TxKeysBuilderParamContributions`
- transaction hook marker kwargs:
  - `commit_order_key(..., tx_key=...)`
  - `validate_commit(..., tx_key=...)`
  - `before_commit(..., tx_key=...)`
  - `after_commit(..., tx_key=...)`
  - `after_rollback(..., tx_key=...)`

Regenerate affected YIDL goldens and the generated lifecycle base module from
source after the rename. Do not patch generated artifacts by hand.

### Verification

Focused YIDL verification:

```bash
uv run --with pytest pytest tests -q
```

If the full YIDL suite is too slow for the checkpoint, at minimum run:

```bash
uv run --with pytest pytest tests/test_lifecycle*.py tests/test_*yidl* -q
```

Pyrolyze verification should run the smallest lifecycle/context tests available
in the parent checkout. If this fails for reasons unrelated to the rename, stop
and report the failure rather than making additional Pyro changes.

### Stop Conditions

Stop if:

- a non-rename Pyro behavior change appears necessary
- the rename exposes ambiguity between transaction key and another "group"
  concept
- generated output still accepts `tx_key=` as a public compatibility alias

## Slice 2: Field-Kind Matrix And Transaction Infrastructure Clarification

### Goal

Create a precise field-kind matrix so the next semantic slices do not keep
rediscovering lifecycle dimensions.

### Expected Edits

Add `dev-docs/YidlLifecycleFieldKindMatrix.md` with a matrix covering at least:

- `field`
- `initvar`
- `classvar`
- `const`
- `static`
- `managed`
- `transient`
- `owned`
- `binding`
- `local_store` as planned in this document

Columns should include:

- stored in state?
- constructor parameter?
- settable after construction?
- default/default_factory support?
- retained initvar support?
- transaction current/working/staged state?
- facade visibility
- factory evaluation timing
- commit/rollback behavior
- teardown/close behavior, even if currently none

Every listed kind must have a row. `local_store` should be marked
`planned (Slice 5)` until the implementation lands.

Clarify that `transaction_manager` is generated infrastructure:

- constructor accepts `transaction_manager=None`
- state stores `_y_transaction_manager`
- facade methods delegate to that manager
- it is not a user field marker in this plan

Document `transaction_manager` as a sidebar or infrastructure row with user
field columns marked N/A where appropriate.

### Verification

Docs-only slice. Verify:

```bash
test -f dev-docs/YidlLifecycleFieldKindMatrix.md
rg -n "field|initvar|classvar|const|static|managed|transient|owned|binding|local_store" dev-docs/YidlLifecycleFieldKindMatrix.md
```

### Stop Conditions

Stop if the matrix reveals an unowned field kind needed before `local_store` or
callable injection. Do not implement that kind opportunistically in this slice.

## Slice 3: Callable Injection Core Fact Model

### Goal

Unify callable argument discovery for lifecycle factories so ordinary
`default_factory` paths can consume the same kind of computed argument metadata
that transient working factories already proved.

This slice does not enable unsafe `self` factories yet.

### Semantics

Factory argument names fall into these classes:

- provider names: fields, initvars, classvars, and retained initvars
- special names: `cls`
- rejected names: unknown parameters, positional-only parameters, `*args`,
  `**kwargs`
- deferred special name: `self`

`cls` resolves to the immediate original decorated user class for this
lifecycle layer, as passed to `build_lifecycle_class`. It does not mean
`type(self)`, and it does not resolve to a generated facade class. Patterns such
as `type(self.owner)` are `self` factory cases, not `cls` cases.

Provider names are dependency-tracked:

- normal stored fields can depend on earlier or dependency-ordered providers
- retained initvars can be providers when they have a value source
- classvars are read through the generated instance as `self.NAME` where that is
  already the canonical generated shape, but the dependency is still tracked as
  class-level

Value-source rules for retained initvars:

- `initvar(default=...)` provides the default when no caller value is supplied
- `initvar(default_factory=...)` provides the factory result
- `initvar(init=False, default=...)` provides the default
- `initvar(init=False, default_factory=...)` provides the factory result
- `initvar()` with no default and no factory is not a provider and should
  produce a targeted `LifecycleDefinitionError` if another factory references it

Callable injection sets are related but not identical across factory kinds:

| Callable context | Allowed special names in this slice | Provider names | Explicitly rejected/deferred |
| --- | --- | --- | --- |
| normal `default_factory` for `field`, `const`, `static`, and `initvar` | `cls` | fields, classvars, initvars with value sources, retained initvars | `self` until Slice 4; `current`; `working`; unknown names |
| transient `working_default_factory` | existing supported names remain supported | existing retained-initvar/provider support remains supported | no broadening in this slice beyond shared signature diagnostics |
| transaction hooks/validators | unchanged | unchanged | broader injection deferred |
| `local_store(default_factory=...)` | not implemented until Slice 5 | none in Slice 5 | no injection in Slice 5; future extension deferred |

### Expected Edits

YIDL runtime and harvester:

- centralize callable signature inspection for lifecycle factories
- carry argument metadata into the lifecycle fact model
- identify `cls` as a safe special argument
- reject unsupported signatures with targeted `LifecycleDefinitionError`
- when rejecting `self`, make the diagnostic point at the Slice 4 opt-in
  concept rather than reporting it as merely unknown

YIDL source:

- update default-factory computed fact operations so normal factory args and
  transient working factory args use one conceptual model, even if the generated
  YIDL records remain separate for now

Tests/goldens:

- add a fixture with a const or initvar factory using `cls`
- add diagnostic tests for:
  - unknown provider name
  - positional-only factory parameter
  - `*args`
  - `**kwargs`
  - `self` without the explicit policy from Slice 4

### Verification

Focused tests:

```bash
uv run --with pytest pytest tests -q
```

Generated golden review should show direct keyword calls rather than
`locals()`-based lookup.

Update `dev-docs/YidlLifecycleFieldKindMatrix.md` if the callable metadata
changes any factory-timing or provider columns.

### Stop Conditions

Stop if:

- this requires changing the public marker API beyond adding documented factory
  metadata
- any factory needs an injection name outside the documented reserved set
- implementation requires globally reordering constructor phases rather than
  adding the computed callable metadata

Do not add `self` support in this slice.

## Slice 4: Explicit `self` Factory Policy

### Goal

Allow the Pyro LCM owner-derived factories that take `self` without making
normal dependency analysis unsound by default.

### Semantics

`self` in an ordinary lifecycle factory is rejected unless the field explicitly
opts into late/trusted factory ordering.

Canonical marker option:

```python
const(default_factory=build_value, allow_self_factory=True)
field(default_factory=build_value, allow_self_factory=True)
initvar(init=False, default_factory=build_late_value, allow_self_factory=True)
```

`allow_self_factory` is the committed spelling for this plan. The initvar
example above is a value-producing late factory, not a discarded-result
bootstrap hook.

When `allow_self_factory=True`:

- `self` is injected as the generated default facade under construction
- all explicit non-`self` parameters still create dependency edges
- `self` itself creates no dependency edges
- self-allowed factories are scheduled after non-self factories
- within the self-allowed batch, explicit dependency edges win over declaration
  order
- declaration order breaks ties only when there is no explicit dependency edge
  ordering two factories
- reading a field through `self` that was not made available by explicit
  parameters/dependencies is author error and may observe an uninitialized or
  sentinel value depending on the field storage shape

This is intentionally weaker than full dependency discovery. The opt-in makes
that weakness visible.

### Expected Edits

YIDL marker/runtime:

- add a boolean marker property for allowing `self` factories
- carry the property through `FieldDecl` and harvested facts
- reject `self` parameters when the property is false

YIDL source:

- add contribution lowering for `self` keyword args in normal default factories
- schedule self-allowed factories using explicit dependencies plus declaration
  order

Tests/goldens:

- const factory using `self.owner`
- initvar `init=False` factory using `self` where the result is consumed by a
  later field
- diagnostic for `self` without opt-in
- runtime test showing that declaration-order tie-breaking is deterministic
  when there is no explicit dependency edge

Update `dev-docs/YidlLifecycleFieldKindMatrix.md` for the new self-factory
policy.

### Stop Conditions

Stop if `self` support appears to require implicit user `__init__` chaining or
old `_state` compatibility. Those are separate decisions.

## Slice 5: Minimal `local_store`

### Goal

Support the `slot_expr_slot_context.py` storage shape without introducing a
close protocol.

### Semantics

`local_store` is lifecycle-owned, non-transactional scratch storage:

- stored in generated state
- initialized during construction
- supports `default` and zero-argument `default_factory`
- not staged
- not committed
- not rolled back
- exposed through every facade as the same object
- reads from default/current/working return the same object
- mutating the object does not enlist a transaction
- rollback does not restore the object's prior state
- no generated close/deactivate hook in this slice
- the consumer is responsible for any required teardown of the local-store value

Proposed marker:

```python
local_store(default_factory=dict)
```

Rejected in this slice:

- `tx_key=`
- `working_default_factory=`
- staged/working options
- injected factory parameters

Unsupported options should fail at marker construction or harvesting with a
targeted error.

### Expected Edits

YIDL runtime:

- add `local_store` marker
- add harvester support
- include local-store fields in metadata merge

YIDL source:

- add `LocalStoreFields` computed/refined collection
- add state slot contribution
- add constructor initialization contribution
- add property contribution
- ensure local-store fields do not participate in transaction helper phases
- update `dev-docs/YidlLifecycleFieldKindMatrix.md` to mark `local_store` as
  implemented with the shared-object/no-rollback semantics above

Tests/goldens:

- fixture with `local_store(default_factory=dict)`
- runtime assertion that mutating the dict does not enlist a transaction
- runtime assertion that commit/rollback leaves the local store untouched
- generated output golden showing no current/working/staged slots for the field
- diagnostic tests for rejected options such as `tx_key=`

### Verification

Focused lifecycle tests and goldens:

```bash
uv run --with pytest pytest tests -q
```

### Stop Conditions

Stop if the first real consumer requires deterministic close/teardown. That is
not part of minimal `local_store`.

## Slice 6: Transaction Manager Access Surface

### Goal

Make transaction-manager access explicit enough that Pyro LCM code does not need
the old `_state.transaction_manager` object model.

### Semantics

Generated lifecycle classes already accept a transaction manager and store it in
the generated state. This slice exposes a deliberate access surface without
making `_state` a general compatibility object.

Canonical generated surface:

```python
self._y_get_transaction_manager()
```

Use the reserved `_y_` namespace. Do not generate `_transaction_manager`; the
WIP already owns that property name, and user code can implement it as a shim
that delegates to `_y_get_transaction_manager()`.

This slice provides read access only. Post-construction transaction-manager
replacement is not supported unless a later decision explicitly adds a setter.

### Expected Edits

YIDL runtime/source:

- add generated helper for transaction manager access:
  `self._y_get_transaction_manager()`
- keep `_y_state._y_transaction_manager` as the storage location
- avoid broad `_state` compatibility
- audit current reserved-name diagnostics for `_y_` helper collisions
- add a collision diagnostic/test for `_y_get_transaction_manager` unless an
  existing generated-helper collision test already covers it; if the existing
  test is sufficient, the slice commit notes should cite that test

Tests/goldens:

- fixture proving generated code can read the transaction manager from a factory
  or method through `_y_get_transaction_manager()`
- diagnostic for `_y_get_transaction_manager` collision unless the audit proves
  existing coverage is already sufficient

Update `dev-docs/YidlLifecycleFieldKindMatrix.md` if the infrastructure sidebar
changes.

### Stop Conditions

Stop if supporting the WIP requires `self._state.transaction_manager` exactly.
That is old lifecycle compatibility and needs a separate explicit decision.

## Slice 7: Pyro LCM Representability Probe

### Goal

Check whether the `context_state_lcm` declarations can be represented by YIDL
without editing Pyro code beyond the Slice 1 naming cleanup.

This is a probe slice. It may produce tests or docs rather than production code.

The representability fixture uses YIDL `@lifecycle`, not the legacy Pyro
`@managed_context` decorator. `managed_context` is treated as old decorator
naming, not a blocker for field-model representability.

### Expected Work

Create a focused representability test or scratch fixture that mirrors the field
declarations from:

- `context_base.py`
- `_base.py`
- `slot_expr_slot_context.py`

The fixture should cover:

- const factories using `self`
- the exact `initvar(init=False, default_factory=...)` shape from
  `_resolved_render_context_state_mgr`
- initvar factories using `cls` and retained initvars
- managed fields with non-default `tx_key`
- managed fields that pass `compare="identity"`; this should be accepted as
  no-op compatibility metadata unless a later plan gives `compare` semantics
- transient fields with non-default `tx_key`
- local-store fields
- transaction-manager constructor parameter
- the bootstrap factory shape that currently tries to install or retrieve a
  transaction manager, so the probe records whether `_y_get_transaction_manager`
  is sufficient or a bootstrap policy is required

Do not attempt to port all methods or custom `__init__` classes in this slice.

Create or update a checked-in representability table, for example:

```text
dev-docs/YidlPyroLcmRepresentability.md
```

The table should record each mirrored shape, whether it is representable, and a
short reason for any partial failure. The Decision Gate should refer to this
artifact rather than relying on informal notes.

If `compare=` is not already accepted by the time this probe runs, this slice
owns adding it as no-op marker metadata for representability. Do not implement
equality semantics in this plan.

### Verification

The fixture should compile, materialize generated code, and run enough runtime
checks to prove:

- constructor works
- transaction manager key exists
- managed pass-state fields can be staged and committed
- local-store fields survive commit/rollback unchanged
- owner-derived consts evaluate correctly
- the representability table records pass/fail for every fixture case

### Stop Conditions

Stop if `ComponentCallSlotContextStateMgr` or another decorated class with a
meaningful handwritten `__init__` must be ported directly. That requires the
custom-init policy below.

Stop if any required Pyro LCM shape in the representability table is marked
`not representable` and the relevant Decision Gate has not been resolved for
that case. Do not tag the slice green with an unresolved required row.

## Decision Gate: Custom `__init__` And Bootstrap Policy

This plan does not silently enable implicit user `__init__` chaining.

If the representability probe shows that handwritten `__init__` support is
required, pause and decide between these options:

1. Refactor the Pyro class into lifecycle fields/default factories. This would
   require a non-rename Pyro change, so it must be discussed before editing.
   This is likely the cheapest path if the WIP author is comfortable changing
   the WIP source.
2. Add an explicit YIDL bootstrap hook marker, for example `bootstrap(...)`.
   This keeps construction generated and makes the side-effect boundary visible.
3. Support controlled user `__init__` chaining. This reopens a previously
   rejected lifecycle design and needs a separate plan.
4. Keep that class out of lifecycle decoration.

The current preferred direction is option 2 if a generated bootstrap escape
hatch becomes necessary. Do not silently bless discarded-result
`initvar(init=False, default_factory=...)` side effects as the bootstrap
mechanism without a separate decision; that pattern may still be useful for
value-producing retained initvars, but it is too implicit as a general
side-effect hook.

## Expected Final State

After the roll-build completes through Slice 7:

- `tx_key` is gone from active code and generated output
- `tx_key` is the only transaction-key spelling
- lifecycle field-kind semantics are documented in a matrix
- normal factories support safe `cls` injection
- `self` factories are supported only with explicit opt-in and late/trusted
  ordering
- minimal `local_store` exists
- transaction manager access has a deliberate generated surface
- the Pyro LCM field declarations are representable by YIDL without relying on
  the old lifecycle descriptor engine

## Open Follow-Ups After This Plan

Possible future work after this plan:

- custom bootstrap hook, if Slice 7 proves it is needed
- deterministic owned/binding teardown tests for `grip.Drip`
- full Pyro lifecycle test inventory follow-through
- generated lifecycle module packaging
- close/deactivate protocol, only if a concrete consumer requires it
- `derived`, only if a concrete consumer requires it
