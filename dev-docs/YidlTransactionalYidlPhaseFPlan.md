# YIDL Transactional Base Phase F Plan

## Scope

Phase F implements transaction protocol extensions for already-managed
fields:

- commit order keys
- commit validators
- before-commit hooks
- after-commit hooks
- after-rollback hooks

This is separate from new field kinds because it changes the transaction
runtime contract for fields that already exist. Public commit/rollback call
patterns remain unchanged from Phase A: users still call `begin(...)`,
`validate(...)`, `commit_only(...)`, `commit(...)`, and `rollback(...)` on a
generated facade.

## Goals

1. Make Phase A protocol stubs fact-driven.
2. Add a user-facing hook/validator marker surface based on class methods.
3. Generate specialized code for known validators and hooks; do not introduce
   generic runtime descriptor tables.
4. Preserve multi-transaction-group behavior.
5. Define and test hook failure and cleanup behavior.
6. Keep validator/hook diagnostics class- and method-specific.

## Non-Goals

1. Do not implement owned or binding fields.
2. Do not add transient semantics.
3. Do not introduce post-init chaining.
4. Do not add `current_setter_policy`; that remains a later decorator-option
   phase.
5. Do not change the public transaction runtime API without a focused review.
6. Do not support explicit user-supplied hook order values in Phase F.

## User Surface

Phase F uses method decorators attached to methods in the decorated class body.
Inline callbacks on `managed(...)` are deliberately out of scope because they
are too narrow for cross-field validation, multi-field commit ordering, and
future inheritance behavior.

The runtime marker functions should be imported from `yidl.runtime.lifecycle`
beside the existing field markers:

```python
from yidl.runtime.lifecycle import after_commit
from yidl.runtime.lifecycle import after_rollback
from yidl.runtime.lifecycle import before_commit
from yidl.runtime.lifecycle import commit_order_key
from yidl.runtime.lifecycle import lifecycle
from yidl.runtime.lifecycle import managed
from yidl.runtime.lifecycle import validate_commit
from yidl.runtime.transaction_yidl import DEFAULT_TRANSACTION


@lifecycle
class Counter:
    count: int = managed(default=1)
    audit_count: int = managed("audit", default=10)

    @commit_order_key(DEFAULT_TRANSACTION)
    def _default_commit_order(self) -> tuple[object, ...]:
        return (self.count,)

    @validate_commit(DEFAULT_TRANSACTION)
    def _validate_count(self) -> bool:
        return self.count >= 0

    @before_commit(DEFAULT_TRANSACTION)
    def _before_default_commit(self) -> None:
        self.events.append(("before", "default"))

    @after_commit(DEFAULT_TRANSACTION)
    def _after_default_commit(self) -> None:
        self.events.append(("after", "default"))

    @after_rollback("audit")
    def _after_audit_rollback(self) -> None:
        self.events.append(("rollback", "audit"))
```

Decorator call shape:

```python
@validate_commit(tx_group=DEFAULT_TRANSACTION)
def method(self) -> bool | None: ...
```

Each marker should also accept the transaction group as the first positional
argument for consistency with `managed("audit", ...)`.

`validate_commit` methods may return `True`/`None` for success or `False` for
failure. Raising an exception is also a failure. Hook methods return values are
ignored.

## Candidate Facts

```text
CommitOrderKeyProvider
CommitValidator
BeforeCommitHook
AfterCommitHook
AfterRollbackHook
```

Minimum fact columns:

```text
HookOwner / ValidatorOwner / ProviderOwner
HookMethodName / ValidatorMethodName / ProviderMethodName
TxGroupKey
DeclarationOrder
```

The first slice can use separate records for each kind. If implementation
reveals large duplication, a shared "transaction method marker" family may be
introduced, but only if the generated YIDL stays readable.

Generated internal protocol methods:

```python
commit_order_key_for(tx_group=DEFAULT_TRANSACTION)
requires_validation_for(tx_group=DEFAULT_TRANSACTION)
validate_commit_for(tx_group=DEFAULT_TRANSACTION)
_commit_transaction(tx_id, tx_group=DEFAULT_TRANSACTION)
_rollback_transaction(tx_id, tx_group=DEFAULT_TRANSACTION)
```

These methods are the internal `TransactionManager` context protocol. They are
not new public facade APIs.

## Runtime Contract

`requires_validation_for(tx_group)` returns `True` when at least one
`validate_commit` method exists for `tx_group`. The existing
`TransactionManager.enlist(...)` path uses this to decide whether the state
object is added to the transaction's validator set.

`validate_commit_for(tx_group)` runs validators for the group in deterministic
order. If any validator raises, the exception is collected by
`LifecycleTransaction.validate_commit()`. If a validator returns `False`, the
existing `YidlValidatorReturnedFalse` path is used. `None` and `True` are
success.

`commit_order_key_for(tx_group)` returns:

- the first declared key provider result for the group, when one exists
- `()` otherwise

Phase F allows at most one commit order key provider per transaction group.
Multiple providers for the same group are rejected by the harvester.

`_commit_transaction(tx_id, tx_group)` remains the internal method that applies
working values to current values. Phase F extends its generated body:

1. validate the `tx_id` still owns the group's working values
2. run `before_commit` hooks for the group
3. apply the field commits
4. clear the group's working values / tx id
5. run `after_commit` hooks for the group
6. return the default facade

`_rollback_transaction(tx_id, tx_group)` remains the internal method that
clears working values. Phase F extends its generated body:

1. validate the `tx_id` still owns the group's working values
2. clear the group's working values / tx id
3. run `after_rollback` hooks for the group
4. return the default facade

## Failure Semantics

Phase F must preserve cleanup before propagating hook failures.

| Site | Failure rule |
| --- | --- |
| `validate_commit` raises or returns `False` | `TransactionManager.commit(...)` rolls back and re-raises. No current values are changed. |
| `before_commit` raises | Commit is aborted, working values are rolled back, and the exception is raised to the caller. |
| field commit body raises | Working values are rolled back where possible, and the exception is raised to the caller. |
| `after_commit` raises | Commit remains committed; working values stay cleared; exception is raised to the caller. |
| `after_rollback` raises | Rollback remains complete; working values stay cleared; exception is raised to the caller. |

The current `transaction_yidl.py` cleanup behavior must be reviewed during
implementation. If the existing `commit_only()` / `rollback()` paths can leave
transaction manager state uncleared when a context hook raises, Phase F should
fix that in a focused runtime change before adding generated hook calls.

## Ordering

Hook and validator order is deterministic:

1. inherited declarations in merged field/method order
2. local declarations in class-body definition order
3. stable method name as a final tie breaker only if declaration order is not
   available

Phase F does not support explicit `order=` keyword arguments. Therefore
"ordering collision" is not a Phase F diagnostic.

## Diagnostics

- hook/validator/commit-order marker applied to a non-callable class member
- marker references an unknown transaction group
- multiple commit order key providers for one transaction group
- method marker inherited metadata is malformed
- method marker name collides with a generated lifecycle helper/reserved name
- unsupported decorator call shape

Validator methods themselves do not "reference providers" at harvest time; they
are normal generated method calls. Provider-name dependency diagnostics remain
part of the default-factory feature, not Phase F.

## Verification

Use goldens for success paths:

- validation failure prevents commit and rolls back working values
- before/after hooks fire in deterministic order
- rollback hooks fire only on rollback
- multi-group hooks are isolated
- commit order key provider changes multi-context commit ordering

Use focused tests for diagnostics and transaction runtime cleanup.

Suggested fixture:

```python
events: list[tuple[str, str]] = []


@lifecycle
class Counter:
    count: int = managed(default=1)
    audit_count: int = managed("audit", default=10)

    @validate_commit(DEFAULT_TRANSACTION)
    def _validate_default(self) -> bool:
        return self.count >= 0

    @before_commit(DEFAULT_TRANSACTION)
    def _before_default(self) -> None:
        events.append(("before", "default"))

    @after_commit(DEFAULT_TRANSACTION)
    def _after_default(self) -> None:
        events.append(("after", "default"))

    @after_rollback("audit")
    def _after_audit_rollback(self) -> None:
        events.append(("rollback", "audit"))
```

Expected behavior:

- changing `count` to a non-negative value commits and records before/after
  events
- changing `count` to a negative value fails validation, rolls back the working
  value, and does not run before/after commit hooks
- rolling back an `"audit"` transaction records only the audit rollback event

## Parity Note

Phase J targets lifecycle parity. If `pyrolyze.lifecycle` has a specific
validator/hook failure rule that conflicts with this plan, capture the
divergence before implementing rather than silently matching the old behavior.

## Roll-Build

Suggested tag prefix:

```text
txphaseF-hooks/
```

Suggested slices:

1. F1: add method-marker classes/functions, harvesting, diagnostics, and focused
   tests. No generated hook code yet.
2. F2: harden `transaction_yidl.py` cleanup semantics with focused runtime
   tests.
3. F3: add YIDL facts and generated validator / commit-order methods.
4. F4: add before/after commit and rollback hook generation.
5. F5: refresh goldens and run the lifecycle/golden/full regression scope.
