# Lifecycle Store Classifications

Current value-home and generated-state classification for P1 lifecycle helpers.

## 1. Field Value Homes

| Helper | Value homes | Normalized homes | Notes |
|---|---:|---|---|
| `managed` | 2 | `PublishedStore.<field>`, `WorkingStore.<field>` | Transactional current/working overlay; field carries at most one `tx_index` |
| `const` | 1 | `PublishedStore.<field>` | Read-only after construction/default |
| `static` | 1 | `PublishedStore.<field>` | Per-instance write-once |
| `binding` | 1 | `PublishedStore.<field>` | Non-transactional retained resource; retain/release on replacement and node teardown |
| `owned` | 2 | `PublishedStore.<field>`, `WorkingStore.<field>` | Transaction-aware ownership value; release/dec-ref policy; field carries at most one `tx_index` |
| `transient` | 2 | `PublishedStore.<field>`, `WorkingStore.<field>` | Transactional working value exists only during active tx; field carries at most one `tx_index` |
| `local_store` | 1 | `InstanceStore.<field>` | Native instance home; non-transactional |
| `derived` | 1 | `DerivedCache.<field>` | Cached; reset on commit/rollback invalidation |
| `initvar` | 1-2 | `HiddenStore.construction.<name>`, optional `HiddenStore.retained.<name>` | Retained only when post-init consumer needs it |
| `classvar` | 1 | class attribute | No instance value slot |
| `commit_order_key` | 1 | `PublishedStore.<field>` | Per-instance value plus group metadata |
| `commit_validator` | 1 | `PublishedStore.<field>` | Per-instance callable plus group metadata |
| `on_before_commit` | 0 | class runner metadata | Declaration-only |
| `on_after_commit` | 0 | class runner metadata | Declaration-only |
| `on_after_rollback` | 0 | class runner metadata | Declaration-only |

## 2. Sidecars

1. `CurrentFieldState.<field>` exists only when `state_factory` is configured.
2. `WorkingFieldState.<field>` exists only when `state_copy` or working-side
   state is required on a transaction-aware field. The field's `tx_index`
   controls transaction routing.
3. Sidecars are state data; behavior belongs in generated code or runtime
   helpers.

## 3. Per-Tx Control State

| State | Purpose |
|---|---|
| Working-present flag | Whether this tx key has an active working overlay |
| `working_tx_id[tx_index]` | Active transaction id for stale overlay checks |
| Working value namespace | Singular sparse or flat storage; transaction-aware value fields carry at most one `tx_index` |

## 4. Runtime Scratch

1. Factory-resolution stack.
2. Deferred cleanup queue.
3. Rollback error aggregation list.
4. Optional validation/order scratch if generated code needs temporary
   collection.

## 5. Class-Backed Vs Instance-Backed Helpers

1. `classvar`, hook declarations, and hook metadata are class-backed.
2. `commit_order_key` and `commit_validator` have per-instance values plus
   class metadata.
3. `static` is per-instance, not class-backed.
4. The generator must not infer class-backed storage merely from write-once
   behavior.

## 6. Transaction Mapping

1. Transaction-aware value fields may belong to at most one `tx_index`.
2. P1 transactional value helpers are `managed`, `owned`, and `transient`.
3. Each class has implicit `DEFAULT_TRANSACTION`.
4. Non-default groups are explicit and mapped to stable integer ids.
5. Generated hot paths for transaction-aware value fields carry the field's
   `tx_index` directly.
6. Class metadata exists for utilities, diagnostics, and non-generated helper
   compatibility.
