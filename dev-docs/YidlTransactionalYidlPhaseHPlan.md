# YIDL Transactional Base Phase H Plan

## Scope

Phase H defines and implements `owned` fields.

Owned fields are separate from binding because they involve lifecycle-aware
object ownership, child references, and transaction interaction.

## Goals

1. Define ownership facts and marker frontend.
2. Support owned values that are already lifecycle-generated instances.
3. Define weak/strong ownership policy.
4. Define transaction propagation or enlistment behavior.
5. Detect obvious ownership cycles.

## Non-Goals

1. Do not auto-wrap arbitrary child objects in the first slice.
2. Do not implement binding fields.
3. Do not solve distributed ownership or cross-process lifetimes.

## Initial Proof

```python
@lifecycle
class Child:
    value: int = managed(default=1)

@lifecycle
class Parent:
    child: Child = owned(default_factory=Child)
```

Open design point: should parent transaction begin implicitly begin child
transactions, or should child state enlist independently when changed?

## Diagnostics

- non-lifecycle child where lifecycle child is required
- ownership cycle
- transaction group mismatch
- ambiguous child transaction policy

## Verification

Use a golden for a narrow success path and focused tests for diagnostics.

## Roll-Build

Suggested tag prefix:

```text
txphaseH-owned/
```
