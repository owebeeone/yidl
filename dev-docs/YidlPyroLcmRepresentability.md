# YIDL Pyro LCM Representability

This document records the Slice 7 probe from
`dev-docs/YidlPyroCloseTheGapPlan.md`. It checks whether the field declaration
shapes used by Pyro's `context_state_lcm` work-in-progress can be represented by
the current YIDL transactional lifecycle model without editing Pyro code beyond
the earlier `tx_key` naming cleanup.

The executable probe is `tests/test_lifecycle_pyro_lcm_representability.py`.
It mirrors the relevant declaration shapes with YIDL's `@lifecycle` decorator
and dummy support classes; it does not import or mutate Pyro.

## Summary

The field model is representable under the normalized YIDL lifecycle surface.
The old Pyro `managed_context` decorator name and direct `_state` access are not
ported as compatibility APIs. The YIDL replacement for transaction-manager
access is `_y_get_transaction_manager()`.

## Representability Table

| Pyro LCM Shape | Representative Source | YIDL Probe Shape | Status | Notes |
| --- | --- | --- | --- | --- |
| Base owner const | `context_state_lcm/_base.py` `owner: Any = const()` | `LcmStateMgrBase.owner: object = const()` | Representable | Constructor-supplied const field. |
| Constructor-only render context inputs | `context_base.py` `render_context_state_mgr` / `render_context` initvars | `initvar(default=None)` fields | Representable | Initvars remain constructor inputs and are not facade properties. |
| Derived initvar from `cls` and other initvars | `context_base.py` `_resolved_render_context_state_mgr` | `initvar(init=False, default_factory=...)` | Representable | Uses the Phase C provider model. |
| Owner-derived const factories using `self` | `_generation_tracker_key`, `_context_kind`, `_owner_type_name` style fields | `const(default_factory=..., allow_self_factory=True)` | Representable | The factory can read already-initialized owner state through the default facade. |
| Transaction-manager bootstrap lookup | `_transaction_manager_bootstrap_bad_program` | `const(default_factory=lambda self: self._y_get_transaction_manager(), allow_self_factory=True)` | Representable with normalized API | YIDL does not expose or mutate `self._state.transaction_manager`; the generated helper is the supported access surface. |
| Managed pass-state field with `compare="identity"` | `children_state = managed(..., compare="identity", tx_key=PASS_TX_KEY)` | `managed(default_factory=dict, compare="identity", tx_key=PASS_TX_KEY)` | Representable | `compare` is accepted as no-op compatibility metadata in this slice. Equality semantics are not implemented. |
| Managed tuple pass-state fields | `ui_state`, `own_ui_state`, `own_ui_entries_state` | `managed(default_factory=tuple, tx_key=PASS_TX_KEY)` | Representable | Factory classes with optional constructor defaults are treated as zero-argument factories. |
| Managed `init=False` class factory | `ComponentCallSlotContextStateMgr._call_state` | `managed(default_factory=FrozenComponentCallInvocationState, init=False, tx_key=PASS_TX_KEY)` | Representable | Constructor default parameters on factory classes are not interpreted as provider dependencies. |
| Transient pass-local fields | `_staged_call_site_ids`, `_staged_post_commit_callbacks` | `transient(default_factory=tuple, tx_key=PASS_TX_KEY)` | Representable | Probe verifies transaction-local access and rollback clearing. |
| Local scratch storage | `_call_site_context_manager`, `_runtime_locals_by_slot_id` | `local_store(default_factory=...)` | Representable | Probe verifies the object is shared and not rolled back. |
| Explicit transaction manager constructor parameter | `RenderContextStateMgr(... transaction_manager=TransactionManager(...))` | Generated lifecycle constructor `transaction_manager=...` | Representable | YIDL keeps this as an explicit constructor boundary. |
| `managed_context` decorator spelling | Pyro WIP classes | YIDL `@lifecycle` | Intentionally normalized | Old decorator naming is not a compatibility requirement. |
| Direct `self._state.transaction_manager` access | Pyro WIP methods | `self._y_get_transaction_manager()` | Intentionally normalized | Any remaining Pyro methods should be rewritten to the generated helper when ported. |

## Probe Assertions

The test verifies:

- constructors for the mirrored base/context/slot/component classes work
- `PASS_TX_KEY` is present in the generated transaction-key mapping
- owner-derived const factories evaluate correctly
- `_y_get_transaction_manager()` returns the constructor-supplied manager
- managed pass-state fields can be staged and committed
- local-store values survive rollback unchanged
- transient pass-local fields can be initialized inside a transaction and are
  cleared on rollback
- class-style default factories with optional constructor parameters are
  treated as zero-argument factories

## Remaining Normalization

This probe does not port arbitrary Pyro methods. It only proves the field model
and the generated transaction-manager access boundary are sufficient for those
methods to be rewritten against YIDL lifecycle facades.

`compare="identity"` is accepted for source compatibility, but it does not yet
change generated equality or comparison behavior. That remains a future feature
only if a consumer needs it.
