# StateRef Naming Plan

P1 plan for semantic state references and flat physical slot naming.

## 1. Goal

1. Helper snippets should be written against semantic state locations.
2. Generated hot paths should use direct flattened names.
3. The mapping between those two layers must be centralized and testable.

## 2. StateRef Contract

Each concrete `StateRef` is an ABC instance, not an enum value.

1. It identifies the semantic target.
2. It exposes field and tx coordinates when relevant.
3. It lowers through `StateNaming.slot_name(ref)`.
4. It may provide dynamic `get(state)`, `set(state, value)`, and
   `exists(state)` as a fallback for helper/runtime compatibility.

## 3. P1 Ref Types

| Ref | Coordinates | Meaning |
|---|---|---|
| `PublishedValueRef` | `field` | Current/published value |
| `WorkingValueRef` | `field`, `tx_index` for transaction-aware fields | Working value routed through tx state |
| `CurrentFieldStateRef` | `field` | Current runtime sidecar |
| `WorkingFieldStateRef` | `field`, `tx_index` for transaction-aware fields | Working sidecar routed through tx state |
| `WorkingPresentRef` | `tx_index` | Active working overlay flag |
| `WorkingTxIdRef` | `tx_index` | Active tx id for stale checks |
| `InitvarConstructionRef` | `field` | Constructor-phase initvar home |
| `InitvarRetainedRef` | `field` | Retained initvar home |

## 4. Default Flat Slot Templates

| Ref | Template |
|---|---|
| `PublishedValueRef` | `_y_pv_{field}` |
| `WorkingValueRef` | `_y_wv_t{tx_index}_{field}` |
| `CurrentFieldStateRef` | `_y_cfs_{field}` |
| `WorkingFieldStateRef` | `_y_wfs_t{tx_index}_{field}` |
| `WorkingPresentRef` | `_y_wp_t{tx_index}` |
| `WorkingTxIdRef` | `_y_wtx_t{tx_index}` |
| `InitvarConstructionRef` | `_y_ivc_{field}` |
| `InitvarRetainedRef` | `_y_ivr_{field}` |

## 5. Naming Rules

1. `StateNaming` owns every emitted physical slot name.
2. Emission sites do not hand-roll f-strings for state names.
3. `tx_index` in a physical name is the stable integer, not the group name.
4. For transaction-aware field refs, `tx_index` names the field's transaction
   group; it does not imply multiple indexed working stores.
5. Physical names are compiler-internal and never appear in user source.
6. `_y_*` is reserved for generator internals.

## 6. Descriptor Usage

1. Field descriptors carry semantic refs.
2. Field descriptors may cache lowered slot names after mapping.
3. Dynamic accessors are for external helpers and transitional scaffolding,
   not hot-path generated code.
