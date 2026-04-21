# YIDL P1 Design Pack

This directory is the current design surface for the next YIDL lifecycle
implementation phase.

Historical/exploratory design notes live under `dev-docs/history/`. They are
not required reading for P1 decisions. Current decisions should be consolidated
here.

## Canonical Summary

`YidlDesignSummary.md`

Short, dense, decision-oriented summary of the whole P1 design. This should be
the only required read for understanding the current direction.

It should cover:

- generated class/facade/state/store model
- field value homes
- transaction identity and per-tx state
- facade weakref/star topology
- virtual field mapping and flat lowering
- callable injection/wrapper lowering
- per-helper field operation model
- grammar mapping boundary
- P1 implementation order

## Drill-Down Documents

These documents expand the summary by component.

| Document | Purpose |
|---|---|
| `GeneratedClassLayout.md` | Main facade, secondary facades, `YidlState`, stores, weakref cache, and transaction manager integration. |
| `LifecycleStoreClassifications.md` | Field value homes, hidden initvar homes, tx-indexed control state, and runtime scratch structures. |
| `StateRefNamingPlan.md` | Semantic state references, flat slot naming, and dynamic accessor fallback. |
| `VirtualFieldMapper.md` | Virtual surface declarations and Astichi lowering from semantic paths to collapsed physical names. |
| `CallableInjectionLowering.md` | `default_factory`, `working_default_factory`, `freeze`, `thaw`, validators, hooks, initvars, and generated wrapper calls. |
| `FieldOperationMatrix.md` | Per-helper operations: facade get/set, tx join, commit, rollback, close, hooks, and special behavior. |
| `GrammarMappingPlan.md` | How YIDL syntax maps onto field specs, operations, refs, callables, and generated runtime structures. |
| `P1ImplementationRoadmap.md` | Ordered build plan, test strategy, acceptance gates, and deferred items. |

## P1 Working Assumptions

- YIDL source expresses lifecycle semantics, not flattened storage names.
- Generated code may use flat direct state fields for speed.
- Virtual field refs provide a readable semantic layer for helper code and
  tests.
- Astichi lowers virtual refs into collapsed physical names for optimized
  generated output.
- Thin dynamic accessors remain available for external libraries and transitional
  helper code.
- Field descriptors carry semantic refs and may cache lowered names.
- Transaction groups are independent; each field belongs to exactly one tx id.
- Class metadata includes immutable tx-name `<->` tx-id mappings for utilities.
- The main facade owns strong refs to live secondary facades.
- `YidlState` owns weak refs to facades and recreates them as needed.

## First Concrete Subsystems

Build and validate these before broad lifecycle codegen:

1. Virtual field mapper.
2. Astichi lowering for virtual refs to flat names.
3. Callable injection/wrapper lowerer.
4. Minimal generated class skeleton using those pieces.
5. One lifecycle field slice over the skeleton.

## History Policy

Use `dev-docs/history/` as source material only.

When a historical note contains a still-current decision, copy the decision into
`YidlDesignSummary.md` or the relevant P1 drill-down document. Do not require
future readers to reconstruct current design by reading history.
