# P1 Implementation Roadmap

Current build order and acceptance gates for the first lifecycle-generation
phase.

## 1. Minimum Delivery Surface

1. Plain Python generated lifecycle class skeleton.
2. Main/current/working facades.
3. One internal state/store object.
4. Public runtime constants `VOID` and `UNSPECIFIED`.
5. `VOID` slot initialization.
6. Tx metadata and default transaction begin/commit/rollback path using
   existing YIDL-owned transaction runtime names where practical.
7. Virtual field mapper.
8. Astichi lowering from semantic refs to flat physical names.
9. Callable injection lowerer for the section 6 registry in
   `../YidlDesignSummary.md`.
10. Generated-library shape: compiled YIDL emits functions/decorators that
    generate the target class.
11. Three-way parity for the supported subset under `LC_PARITY_IMPL`.

## 2. Build Order

1. Virtual field mapper.
2. Astichi lowering from virtual refs to flat physical names.
3. Callable injection / wrapper lowerer.
4. Minimal generated class skeleton.
5. Generated-library wrapper that calls the skeleton generator.
6. One generated `managed_scalar` slice.
7. Comprehensive hand-crafted baseline and focused slice target in parallel.
8. Expand helper families following the field staircase.
9. Fit grammar after layout, refs, callables, and operations are stable.

## 3. Field Staircase

1. `managed` default tx.
2. `managed` advanced: `freeze`, `thaw`, `initial_working`.
3. `const` / `static`.
4. `local_store` / `derived`.
5. Multi-group tx.
6. `transient` with `working_default_factory`.
7. `binding` refcount cleanup.
8. `owned` transactional ownership cleanup.
9. `initvar` injection.
10. `commit_order_key`, `commit_validator`, hooks.

## 4. Test Tracks

1. `LC_PARITY_IMPL=lifecycle`: YIDL-owned reference backend, using copied
   `test-deps/` code or rewritten reference helpers. It must not import
   `pyrolyze`.
   1. This backend is tests-only.
   2. `src/yidl/`, generated code, and public runtime/API modules must not
      import it.
   3. Copied lifecycle/freezable reference files must be excluded from pip
      packages.
2. `LC_PARITY_IMPL=handcrafted`: generated-shape hand-crafted baseline.
3. `LC_PARITY_IMPL=generated`: current compiler output.
4. `tests/baseline/_impl_switch.py` owns backend switching and must not load
   any `pyrolyze` package module.
5. Python-version validation uses `uv run --python <version>` over the active
   support sweep.

## 5. Completion Rules Per Slice

1. Feature design note exists when the slice introduces new semantics.
2. Runtime behavior needed by the slice is YIDL-owned or explicitly deferred;
   no slice may import or depend on `pyrolyze`.
3. Comprehensive baseline is advanced when the feature can interact with other
   helpers.
4. Focused slice shape exists when the emitted structure needs isolated review.
5. Generator continues emitting runnable output for the supported subset.
6. Unsupported features fail explicitly.
7. No unresolved `design_gap` or `design_conflict` affects the claimed
   completion.

## 6. Design Escalation

Use these classifications before coding around failures:

1. `implementation_bug`: design is coherent; implementation missed it.
2. `design_gap`: behavior is under-specified.
3. `design_conflict`: design conflicts with required behavior or emitted
   shape.

## 7. Deferred / Open

1. Cross-group visibility rules.
2. Global evict-last ratification.
3. Resource single/list/map specialization for `binding` and `owned`, while
   preserving their transaction split.
4. Transaction-group tying.
5. Final migration away from `_yidl.py` bootstrap.
