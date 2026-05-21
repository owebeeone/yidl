# YIDL Transactional Base Phase I Plan

## Scope

Phase I defines and implements `binding` fields.

Binding is likely the most graph-heavy lifecycle feature. It should not start
until owned-field semantics are understood, because both features create
relationships between lifecycle objects.

## Goals

1. Define binding source and target facts.
2. Resolve binding graphs before source generation.
3. Detect cycles and transaction group mismatches.
4. Generate a narrow read/write binding case.

## Non-Goals

1. Do not implement broad reactive dataflow.
2. Do not allow ambiguous binding cycles.
3. Do not infer binding semantics from arbitrary Python descriptors.

## Design Questions

- Is a binding a read-through reference or a copied value?
- Which side owns transaction enlistment?
- Can binding cross transaction groups?
- How are current and working facades exposed through a binding?
- How are reference loops diagnosed?

## Verification

Use computed graph facts for validation and a golden for one simple binding.
Focused tests should cover cycles and mismatched groups.

## Roll-Build

Suggested tag prefix:

```text
txphaseI-binding/
```
