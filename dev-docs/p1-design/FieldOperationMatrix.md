# Field Operation Matrix

Current P1 operation model by helper family.

## 1. Core Operation Columns

1. Default/proxy get.
2. Current get.
3. Working get.
4. Working set.
5. Tx join / ensure working.
6. Default resolution.
7. Working-default resolution.
8. Commit.
9. Rollback.
10. Node cleanup / resource release.
11. Validator / order-key / hook participation.
12. Binding / ownership cleanup.

## 2. Helper Operation Summary

| Helper | Key operations |
|---|---|
| `managed` | Resolve default, read current/working, ensure working on set, thaw on working promotion, freeze on commit |
| `const` | Resolve once, read current, reject mutation |
| `static` | Resolve once, enforce single-write |
| `binding` | Non-transactional retained resource; retain/accept/release on replacement or node lifetime release |
| `owned` | Transaction-aware ownership value; working overlay plus release/dec-ref ownership policy |
| `transient` | Tx-scoped working/default behavior; cleanup on commit/rollback |
| `local_store` | Direct instance/native get/set |
| `derived` | Cached compute; reset on commit/rollback invalidation |
| `initvar` | Constructor capture; optional retained storage; callable injection |
| `classvar` | Class materialization; no instance store |
| `commit_order_key` | Current value read for commit ordering |
| `commit_validator` | Callable invoked during validation |
| `on_before_commit` | Hook before field commits |
| `on_after_commit` | Hook after successful commit |
| `on_after_rollback` | Hook after rollback |

## 3. Managed Special Rules

1. `initial_working` belongs to managed-like overlay behavior.
2. Before the first successful commit, while a transaction is active and no
   explicit working value exists, managed reads can surface `initial_working`.
3. After first commit, working reads resolve from current/default and normal
   thaw-on-write behavior.
4. Managed does not use `working_default_factory`.

## 4. Transient Special Rules

1. `working_default_factory` belongs to transient.
2. It materializes the working value on first working access during an active
   transaction.
3. `initial_working` is not part of transient helper exposure.

## 5. Commit / Rollback / Node Cleanup

1. P1 defaults to reference validate-first commit ordering.
2. Remaining hook/write/cleanup ordering is proposed until ratified.
3. Rollback is best-effort across fields mutated during the active transaction
   window. This intentionally diverges from the current reference path that
   stops on first per-field rollback error.
4. Facades, state/store objects, and transactions do not expose public
   `close()`.
5. Binding cleanup follows stage -> update -> evict immediately on replacement
   or when node lifetime reaches zero.
6. Owned cleanup follows stage -> update -> evict through the commit/rollback
   ownership pipeline.

## 6. Open Interactions

1. Cross-group read visibility while another group has active working state.
2. Global evict-last traversal across a whole commit step.
3. Single/list/map specialization for binding and owned resources, preserving
   that binding is non-transactional and owned is transaction-aware.
