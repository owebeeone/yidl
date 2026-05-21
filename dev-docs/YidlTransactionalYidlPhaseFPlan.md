# YIDL Transactional Base Phase F Plan

## Scope

Phase F implements transaction protocol extensions: commit order keys,
validators, hooks, and optional current-setter policy.

This is separate from new field kinds because it changes the transaction
runtime contract for already-managed fields.

## Goals

1. Make Phase A protocol stubs fact-driven.
2. Generate specialized code for known validators and hooks.
3. Preserve multi-transaction-group behavior.
4. Define hook failure behavior.
5. Optionally add `current_setter_policy`.

## Non-Goals

1. Do not implement owned or binding fields.
2. Do not add transient semantics.
3. Do not introduce post-init chaining.
4. Do not change the transaction runtime API without a focused review.

## Candidate Facts

```text
CommitOrderKeyProvider
CommitValidator
BeforeCommitHook
AfterCommitHook
AfterRollbackHook
CurrentSetterPolicy
```

Candidate generated methods:

```python
commit_order_key_for(tx_group=DEFAULT_TRANSACTION)
requires_validation_for(tx_group=DEFAULT_TRANSACTION)
validate_commit_for(tx_group=DEFAULT_TRANSACTION)
_commit_transaction(tx_id, tx_group=DEFAULT_TRANSACTION)
_rollback_transaction(tx_id, tx_group=DEFAULT_TRANSACTION)
```

## Ordering

Hook and validator order must be deterministic. Prefer explicit order facts
derived from field declaration order unless a later API introduces explicit
order.

## Diagnostics

- validator references unknown provider
- hook references unknown transaction group
- multiple commit validators for one group if the model allows only one
- invalid current setter policy
- hook ordering collision if deterministic ordering cannot be established

## Verification

Use goldens for success paths:

- validation failure prevents commit
- before/after hooks fire in order
- rollback hooks fire only on rollback
- multi-group hooks are isolated
- optional current setter policy stages through working when enabled

Use focused tests for diagnostics.

## Roll-Build

Suggested tag prefix:

```text
txphaseF-hooks/
```
