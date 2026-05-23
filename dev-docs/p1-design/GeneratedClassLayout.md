# Generated Class Layout

Current P1 layout decisions for generated lifecycle classes.

## 1. Scope

1. Generated lifecycle classes are plain Python classes, not dataclasses.
2. User-facing YIDL source names lifecycle concepts only; flattened storage
   names are compiler internals.
3. The hand-crafted reference may use explicit store objects for readability.
   The generator target collapses virtual stores and runtime state into the
   single state/store object through the field mapper.

## 2. Runtime Objects

| Object | Role | Ownership |
|---|---|---|
| Main facade | Public instantiated user surface | Strong ref to the state/store object; strong refs to live secondary facades |
| Secondary facade | Lazy view such as `current` / `working` | Strong ref to the state/store object; no strong refs to other facades |
| State/store object | Single internal physical object, not public API | Owns flat slots, tx state, weak facade cache, runtime scratch, cleanup aggregation |
| Transaction manager | Active tx orchestration | Existing YIDL-owned runtime surface; preserve current names/semantics where practical |

Construction budget:

1. Generated construction allocates the main facade and one state/store object.
2. User `__init__` may allocate whatever user code requires.
3. Secondary facades are created on demand.

## 3. Facade Topology

1. Every facade holds a strong reference to the state/store object.
2. The state/store object holds weak references to all facades.
3. The main facade holds strong references to every currently materialized
   secondary facade.
4. Secondary facades do not hold strong references to each other.
5. Access to a secondary facade goes through a state/store-owned accessor:
   1. Return the live weakref target if it exists.
   2. Recreate the facade from the state/store object if the weakref is dead.
   3. If recreating the main facade, repopulate its strong links to any other
      live secondary facades found in the weak cache.

## 4. Store Rules

1. The state/store object holds lifecycle values, flattened physical state,
   tx control state, weak facade refs, and runtime scratch.
2. The state/store object is not public API and must not expose direct client
   behavior.
3. The state/store object may define private generated helpers such as
   `_y_fetch_or_create_facade_current()` when the helper naturally belongs
   beside the stored state.
4. The generated path does not allocate a separate runtime state object or
   separate physical store objects for virtual stores.
5. Generated hot paths prefer slotted flat storage and direct attribute access.
6. Store slots use public runtime constant `VOID` for runtime "not
   initialized" state.
7. Spec/decorator omitted-parameter state uses public runtime constant
   `UNSPECIFIED`, not database absent-value terminology.
8. `VOID` and `UNSPECIFIED` live in `yidl.runtime.constants`.
9. Both constants are singleton instances of slotted sentinel types;
   constructing the concrete type again returns the same object.
10. Generated private helper methods, flattened slots, helper closures, and
   scratch state all use the reserved `_y_*` collision domain.

## 5. Per-Class Metadata

| Metadata | Shape | Purpose |
|---|---|---|
| `tx_index_to_group` | tuple | `tx_index -> tx_key` |
| `tx_key_to_index` | frozen mapping | `tx_key -> tx_index` |
| `commit_order_key_field_by_group` | 0-or-1 mapping | Enforce at-most-one order key per group |
| `commit_validator_field_by_group` | 0-or-1 mapping | Enforce at-most-one validator per group |
| Hook runners | per-group lists | Before/after commit and after rollback execution |

## 6. Generated State Scratch

1. Factory-resolution stack for cycle detection.
2. Deferred commit-cleanup queue.
3. Rollback error aggregation list.
4. `ever_committed` flag for managed `initial_working` semantics.

## 7. Current Open Points

1. Whether global evict-last across an entire commit step is ratified, or
   whether P1 keeps the reference's per-context cleanup drain.
2. Cross-group visibility while another group has an active working overlay.
3. Refcounted-facade mode remains out of P1 unless explicitly reintroduced.
