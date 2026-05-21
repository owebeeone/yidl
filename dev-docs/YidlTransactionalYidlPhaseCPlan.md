# YIDL Transactional Base Phase C Plan

## Status

Draft high-level plan.

Phase C begins lifecycle feature expansion after Phase A proves generated
transactional behavior and Phase B proves the decorator frontend plus
inheritance path. Phase C should move toward `pyrolyze.lifecycle` parity, but
it should still advance in narrow slices. The main rule is that each new
semantic feature must be expressed as facts, computed facts, matchers,
contributions, and generated source, not as a generic runtime descriptor
engine.

## Goals

1. Add lifecycle field kinds and hooks intentionally excluded from Phase A/B.
2. Preserve generated-code performance characteristics.
3. Keep transaction behavior source-specialized to known fields and groups.
4. Extend the fact model without breaking Phase B decorator harvesting.
5. Add feature-level diagnostics before adding broad runtime behavior.
6. Decide whether transaction support should split into feature YIDL layers.

## Non-Goals

1. Do not do all lifecycle parity in one slice.
2. Do not patch `pyrolyze.lifecycle`.
3. Do not replace generated properties with descriptor tables.
4. Do not introduce broad user `__init__` / `__post_init__` chaining unless
   parameterized default factories are proven insufficient.
5. Do not optimize with JIT/cache machinery before the generated source shape
   is stable.

## Phase C Feature Order

Recommended order:

1. parameterized default factories for lifecycle fields
2. strict reserved-name and attribute-write diagnostics
3. transaction validators, commit order keys, and transaction hooks
4. `transient` fields
5. `owned` fields
6. `binding` fields
7. optional current-setter policy
8. feature-YIDL split and composition proof

The order keeps the constructor/evaluation model stable before adding more
field kinds and transaction hook semantics.

## C1: Parameterized Default Factories

Phase B may support zero-argument default factories. Phase C should add
parameterized factories for lifecycle construction:

```python
@lifecycle
class Example:
    v1: int
    v2: int = managed(default_factory=lambda v1: v1 + 2)
    v3: int = managed(default_factory=lambda v2, v1: v1 + v2 + 2)
```

Requirements:

- discover factory parameter names
- determine provider availability from init parameters, initvars, and earlier
  computed values
- topologically order default evaluations
- reject unknown providers
- reject cycles
- support inherited provider fields where semantics are clear
- keep the generated boundary unpacked:

```python
_Example_v2_default_factory=<callable>
_Example_v3_default_factory=<callable>
```

Generated code should call factories directly with named arguments:

```python
v2 = _Example_v2_default_factory(v1=v1)
v3 = _Example_v3_default_factory(v2=v2, v1=v1)
```

Do not use `locals()` for factory argument binding.

## C2: Reserved Names And Attribute Discipline

Phase A/B intentionally avoid solving arbitrary writes to user-class
`__dict__`. Phase C should make the policy explicit.

Diagnostics:

- decorated class declares `_y_state`
- decorated class declares generated state/helper names
- field name collides with facade exposure name (`default`, `current`,
  `working`) unless explicitly allowed
- generated slot name collision
- generated method/property collision

Runtime enforcement options:

1. strict generated `__setattr__` / `__delattr__` gates on facade classes
2. diagnostics only for classes with `__dict__`
3. hybrid: strict for known lifecycle fields, permissive for unrelated attrs

The first Phase C slice should pick one policy and test it directly.

## C3: Transaction Validators, Order Keys, And Hooks

Phase A emits protocol stubs:

```python
commit_order_key_for
requires_validation_for
validate_commit_for
_commit_transaction
_rollback_transaction
```

Phase C should make those protocol methods fact-driven.

Candidate facts:

```text
CommitOrderKeyProvider
CommitValidator
BeforeCommitHook
AfterCommitHook
AfterRollbackHook
```

Generated behavior:

- `commit_order_key_for(tx_group)` returns generated tuple values for the
  active group
- `requires_validation_for(tx_group)` is true when validators exist for that
  group
- `validate_commit_for(tx_group)` calls generated validators
- before/after hooks run in deterministic order
- hook failures follow the transaction runtime's existing exception strategy

Diagnostics:

- validator references unknown field/facade
- hook targets unknown transaction group
- hook order collision if deterministic ordering cannot be established

## C4: `transient` Fields

`transient` fields are state-backed but not committed transaction state.

Questions to lock before implementation:

- Is transient state per backing state object or per facade?
- Does transient state reset on rollback?
- Does transient state participate in default_factory providers?
- Is transient visible from current and working facades?

Likely Phase C policy:

- transient fields live in the backing state
- reads/writes are visible through all facades
- they do not enlist transactions
- they are excluded from commit/rollback
- they can be constructor/default_factory providers

This makes them close to plain fields, but semantically marked for later
diagnostics and generated API documentation.

## C5: `owned` Fields

`owned` fields likely need lifecycle-aware child object management.

Requirements:

- owner field facts
- child lifecycle detection
- weak/strong ownership policy
- transaction propagation policy
- commit/rollback interaction

Initial slice should be conservative:

- support owned values that are already lifecycle-generated instances
- reject ambiguous ownership cycles
- do not auto-wrap arbitrary child objects

Useful proof:

```python
@lifecycle
class Child:
    value: int = managed(default=1)

@lifecycle
class Parent:
    child: Child = owned(default_factory=Child)
```

Open design point: whether parent transaction begin should implicitly begin
child transactions or whether the child should enlist independently.

## C6: `binding` Fields

`binding` fields connect values across objects or facades.

This is the most likely Phase C feature to require extra design before code.
It should not be started until owned field ownership semantics are clear.

Requirements to define:

- binding source and target facts
- read-through vs copied value semantics
- transaction group mapping between source and target
- cycle detection
- diagnostic reporting for reference loops

The implementation should prefer computed facts that resolve binding graphs
before code generation.

## C7: Current Setter Policy Option

Phase A uses:

```python
obj.current.count = 5  # raises
```

Phase C can add a class-wide or field-level option:

```text
current_setter_policy = "raise" | "stage_working"
```

Generated behavior for `"stage_working"`:

- current setter delegates to the working/default setter path
- active transaction is still required
- current getter remains committed-only

Diagnostics:

- invalid policy name
- policy set where no managed fields exist, if considered suspicious

## C8: Feature-YIDL Split

After Phase B proves the decorator path and Phase C has at least one extension
feature, split the monolithic lifecycle concept if it helps maintainability.

Candidate files:

```text
tests/data/yidl/yidl_transactional_lifecycle/lifecycle_base.yidl
tests/data/yidl/yidl_transactional_lifecycle/lifecycle_transactions.yidl
tests/data/yidl/yidl_transactional_lifecycle/lifecycle_default_factories.yidl
tests/data/yidl/yidl_transactional_lifecycle/lifecycle_hooks.yidl
tests/data/yidl/yidl_transactional_lifecycle/lifecycle_combined.yidl
```

The split should prove that:

- base plain/init/classvar semantics remain usable alone
- managed transaction support can layer over base fields
- default-factory dependency facts can refine the base init model
- hook features can add matcher rules without replacing base productions

Do not split just for aesthetics. Split when feature-level override/merge
behavior needs to be demonstrated.

## Test Strategy

Use the existing successful coverage shape:

- golden-source tests for successful end-to-end behavior
- focused tests for parser/frontend/diagnostic mechanics
- no duplicate success-path assertions in unit tests and goldens

Suggested goldens:

```text
tests/data/gold_src/yidl_transactional_phase_c_default_factories.py
tests/data/gold_src/yidl_transactional_phase_c_hooks.py
tests/data/gold_src/yidl_transactional_phase_c_owned.py
```

Each golden should produce:

```text
decorator.py
decorator_prettier.py
generated_output.py
generated_output_prettier.py
```

Focused diagnostic tests should cover:

- default_factory cycle
- unknown factory provider
- reserved generated name
- invalid current setter policy
- invalid hook group
- owned/binding cycle

## Implementation Slices

### Slice C1: Parameterized Factory Facts

Deliverables:

- dependency fact schema
- computed operation for dependency graph and evaluation order
- generated constructor assignments without `locals()`

Verification:

- factories run in topological order
- unknown provider diagnostic
- cycle diagnostic

### Slice C2: Reserved Name Diagnostics

Deliverables:

- frontend/generated-name registry
- reserved-name diagnostic tests
- optional strict facade `__setattr__` policy decision

Verification:

- `_y_state` collision rejects
- generated slot/helper collision rejects

### Slice C3: Validators And Hooks

Deliverables:

- validator/hook facts
- generated protocol method bodies
- hook ordering

Verification:

- validation failure rolls back
- before/after hooks fire in expected order
- multi-group hook isolation

### Slice C4: Transient Fields

Deliverables:

- transient field facts
- generated slots/properties
- constructor/default support

Verification:

- transient writes do not enlist transactions
- rollback does not alter transient value under the chosen policy

### Slice C5: Owned Fields

Deliverables:

- owned field facts
- generated ownership accessors
- initial lifecycle-child support

Verification:

- owned child creation
- ownership cycle diagnostic
- transaction interaction according to the selected policy

### Slice C6: Binding Fields

Deliverables:

- binding graph facts
- graph validation operation
- generated read/write behavior for a narrow binding case

Verification:

- simple binding works
- cycle rejects
- transaction group mismatch reports clearly

### Slice C7: Feature Split Proof

Deliverables:

- split YIDL files for at least one extension feature
- combined fixture importing/merging the feature
- docs update describing the layering model

Verification:

- base-only fixture still works
- combined fixture matches monolithic behavior
- inherited/merged matcher rules select the intended behavior

## Roll-Build Candidate Assessment

Phase C should not be one roll-build. Each feature should be its own
roll-build candidate after its source shape is reviewed.

Suggested tag prefixes by feature:

```text
txphaseC-factories/
txphaseC-diagnostics/
txphaseC-hooks/
txphaseC-transient/
txphaseC-owned/
txphaseC-binding/
txphaseC-split/
```

Stop after any feature that reveals a mismatch in the fact model or
transaction protocol.

## Open Questions

1. Does parameterized default_factory support eliminate the need for
   post-init-like hooks?
2. Should `transient` be transaction-local, state-local, or facade-local?
3. Should owned child transactions be implicit or explicit?
4. Can binding semantics stay generic enough, or does binding need a narrower
   lifecycle-specific feature design?
5. Should lifecycle transaction support become a feature YIDL before or after
   hooks land?
6. What compatibility target with `pyrolyze.lifecycle` is required before the
   old implementation can be replaced?
