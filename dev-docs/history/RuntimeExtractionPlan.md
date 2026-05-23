# Runtime extraction plan (`pyrolyze.lifecycle`)

This document satisfies **PROCESS.md § Support code review**: separate **transaction / protocol runtime** from **class decoration and descriptor tables**, map runtime pieces to **field helpers**, and outline how YIDL hand-crafted + generated code should adopt and eventually own them.

**Source file:** `pyrolyze/src/pyrolyze/lifecycle.py` (monorepo submodule root).

---

## 1. Runtime vs decoration-time (conceptual split)

| Bucket | Role | Likely fate with YIDL |
|--------|------|------------------------|
| **R1 — Transaction orchestration** | `TransactionManager`, `GroupTransactionManager`, `LifecycleTransaction`, `_MultiGroupTransactionScope`; enlist / validate / commit / rollback across groups | **Re-home into YIDL-owned runtime modules** with semantics preserved; generated proxy + YIDL runtime transaction manager stay the integration point. |
| **R2 — Shared protocols & data** | `BindingBase`, `DEFAULT_TRANSACTION`, `LifecycleValidatorReturnedFalse`, `Record`, `_RecordSnapshot`, `MISSING` | **Re-home the necessary runtime pieces into YIDL-owned modules**; `Record` may disappear inside generated code (replaced by slotted stores) but **semantics** (sparse working, current snapshot) remain. |
| **R3 — Context state machine** | `LifecycleContextState` + `_ManagedContextBase`: `__get_field__` / views, `ensure_working_record*`, `commit` / `rollback` / `close`, hook runners, factory runners, `defer_commit_cleanup` | **Today:** one big class driven by `__class_ftable_*__` built at decorate time. **Target:** same **observable behavior** with implementation either (a) thin runtime + generated `_lc_commit` on the proxy, or (b) shrunk state class calling into generated methods. |
| **D1 — Decoration / compilation** | `managed_context`, `lifecycle_field`, `LCKind` hierarchy, `FieldSpec` merge, `_build_view_class`, descriptor `LifecycleField`, `_build_class_tables`, hook / validator **compilation** (`_compile_hook_runner`, `_compile_factory_runner`) | **Shrink or replace** by YIDL harvester + codegen; not imported from generated modules except for bootstrap during migration. |
| **D2 — Cross-cutting helpers** | `_compile_injected_runner`, initvar resolution, constructor-only resolution, `type_annotations.is_annotation_narrower_or_equal` | **Partially extract**: injection rules become spec for codegen; small runtime may remain for validators/hooks until inlined. |

---

## 2. Runtime features × field helpers

Legend: **needs** = generated or hand-crafted code must cooperate with this runtime behavior.

| Runtime feature | What it does | Field helpers / specs that need it |
|-----------------|--------------|-------------------------------------|
| **TM: single group begin/commit** | `with txm.begin():` binds validate+commit on exit | All transactional fields: `managed`, `binding`, `owned`, `transient`, `derived` (reset), metadata used at commit |
| **TM: multi-group** | `begin(PUBLISH, PASS)`, per-group managers, independent dirty sets | Any helper with non-default `tx_key`; `transient`, `commit_order_key`, `commit_validator`, hooks per group |
| **Enlist + tx_id (“dirty”)** | When a working overlay is created, `TransactionManager.enlist(context, tx_key)` runs; stale-tx checks. (No separate `mark_dirty` on the manager—unlike some design sketches.) | `managed`, `binding`, `owned`, `transient` (writes promote working) |
| **Validate → commit order → apply** | `LifecycleTransaction.validate_commit`, `commit_order`, `apply_commits` → `context._commit_transaction` | All dirty contexts; **`commit_order_key`** (sorting), **`commit_validator`** (gate) |
| **Record overlay** | Sparse `working` `Record` vs `current` `Record`; `get_field` / `set_working_field` routing | `managed`, `binding`, `owned`, `transient`; **`local_store`** / **`derived`** use alternate storage hooks inside same state machine |
| **Factory runners** | `default_factory`, `working_default_factory` with cycle detection and injected params | `managed`, `static`, `transient`, `initvar` consumers, etc. |
| **Initvar + injection** | `_construction_initvars`, `_retained_initvars`, `_initvar_resolve_from_state` into hooks/factories/validators | **`initvar`**, **`on_*`**, **`commit_validator`**, factories with extra param names |
| **Hook tables** | `before_commit` / `after_commit` / `after_rollback` instance methods + compiled declarative runners; `defer_commit_cleanup` for binding release ordering | **`on_before_commit`**, **`on_after_commit`**, **`on_after_rollback`**, **`binding`**, **`owned`** |
| **Binding protocol** | `inc_ref` / `dec_ref` / `accepted` / `_close` sequencing on set/commit/rollback | **`binding`**, **`owned`** |
| **Views** | `current` / `working` / default mode on `_ManagedContextBase` subclasses | All fields with different surface semantics (`managed` read-only on current, etc.) |
| **Close** | `close()` rolls back open working, runs close hooks | **`local_store`**, **`derived`**, resource fields |

---

## 3. Suggested adoption plan (phased)

1. **Phase A — Reference-only comparison**  
   YIDL parity tests import **`TransactionManager`**, **`BindingBase`**, **`DEFAULT_TRANSACTION`**, and exceptions from **`pyrolyze.lifecycle`** (see `tests/baseline/_impl_switch.py`) only as a read-only reference backend during this phase. No files under `pyrolyze/` are edited; lifecycle defects remain documented reference bugs and are handled through lifecycle-only skips where needed.

2. **Phase B — Document the context protocol**  
   Freeze a short **protocol checklist** (methods `TransactionManager` calls on contexts: `_commit_transaction`, `_rollback_transaction`, `validate_commit_for`, `commit_order_key_for`, etc.) derived from `GroupTransactionManager` + `LifecycleTransaction`. Generated `Bar` and later YIDL-owned runtime modules must satisfy this without relying on `LifecycleContextState` internals.

3. **Phase C — YIDL-owned runtime modules, slice by slice**  
   Re-home **R1 + R2** and a **minimal** context interface into small YIDL-owned runtime modules with **no** `managed_context` / `LCKind`. This move should happen per feature slice as required runtime pieces become understood and tested, rather than as one large late extraction. The initial practical move is to lift/copy the relevant `TransactionManager` behavior from `lifecycle.py` into YIDL-owned runtime modules, preserve the known semantics, and then evolve from that owned baseline. The target direction is that YIDL becomes authoritative and `pyrolyze` can later depend on YIDL for lifecycle runtime behavior.

   For multi-group behavior, the intended policy is **separate by default**. YIDL should not invent richer cross-group semantics unless they are made explicit. If an application needs groups to coordinate, the runtime may expose tools that let application code tie groups explicitly rather than inferring coupling automatically.

4. **Phase D — Generated commit path**  
   Replace generic `__class_ftable_commit_field__` dispatch with per-class `_lc_commit` / `_lc_rollback` emitted from YIDL; runtime semantics are then supplied by YIDL-owned runtime modules rather than remaining anchored in `pyrolyze.lifecycle`.

---

## 4. Pyrolyze tests to mine for YIDL baseline

Primary file: **`pyrolyze/tests/test_api_lifecycle.py`** (~2k lines). It already covers:

- `managed`, `binding`, `owned`, `transient`, `local_store`, `derived`, `const`, `static`, `initvar`, `classvar`
- `commit_order_key`, `commit_validator`, `on_before_commit`, `on_after_commit`, `on_after_rollback`
- Multi-group `TransactionManager`, factory injection, cycles, validation failures, stale working records

**Adaptation strategy for `yidl/tests/baseline/`**

| Goal | Suggestion |
|------|------------|
| Avoid copying 2k lines | For each `IMPL_PROGRESS` slug, **port one focused test class** (or construct minimal equivalent) from `test_api_lifecycle.py`. |
| Dual backend | Same test body; fixture builds **either** `@managed_context` class **or** handcrafted factory output (see `LC_PARITY_IMPL`). |
| Reference bugs | If `pyrolyze.lifecycle` is wrong for a covered behavior, register a **lifecycle-only skip** through shared helpers in `tests/baseline/`; document the bug in the feature design doc instead of adding bespoke skip logic in the test body. |
| CI Python version | YIDL tests use `_impl_switch` stub loader so **3.10** can load `lifecycle` without `pyrolyze.api`; full `test_api_lifecycle.py` may require newer Python in upstream CI. |

When porting, grep `test_api_lifecycle.py` for the feature name (e.g. `transient`, `commit_validator`) and copy the smallest test that asserts public behavior.

---

## 5. Maintenance

When `lifecycle.py` gains a new field kind or TM behavior:

1. Update **`dev-docs/lifecycle_field_catalog.py`**.
2. Add a row to **§2** (this file) if a **new runtime feature** is required.
3. Extend **`spec/lifecycle_baseline.yidl`** and **`IMPL_PROGRESS.md`** per PROCESS.
