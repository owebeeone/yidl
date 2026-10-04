# YIDL Current Gaps 2

This document replaces the first source-gap review after the lifecycle work
became executable. It records what the current code does, what is still missing,
and what should stay stable while cleanup happens.

It is a gap list, not a design override. `dev-docs/YidlDesignSummary.md`
remains the semantic authority and `dev-docs/YidlCodingRules.md` remains the
implementation-rules authority. Historical material under `dev-docs/history/`
is source archaeology only.

## 1. Current Working System

The working lifecycle system now lives in `../yidl-lifecycle` and uses `yidl`
as the generic concept/DDS/assembly substrate.

Current flow:

1. Lifecycle authors write normal Python classes and decorate them with
   `yidl_lifecycle.lifecycle.lifecycle`.
2. Field declarations are markers from `yidl_lifecycle.lifecycle_markers`:
   `field`, `initvar`, `classvar`, `const`, `static`, `managed`, `owned`,
   `binding`, `local_store`, and `transient`.
3. Transaction method markers are `commit_order_key`, `validate_commit`,
   `before_commit`, `after_commit`, and `after_rollback`.
4. `yidl_lifecycle.lifecycle_harvester.harvest_lifecycle_definition(...)`
   validates the class and produces immutable facts for class layout, fields,
   transaction groups, default factories, freeze/thaw functions, binding shape,
   and transaction hooks.
5. `yidl_lifecycle.lifecycle._build_lifecycle_container(...)` writes those
   facts into the generated concept runtime from
   `yidl_lifecycle._generated_lifecycle_base`.
6. The generated runtime builds an Astichi composable module. The decorator
   compiles and executes that module, calls `build_lifecycle_class(...)`, and
   returns a generated plain Python class.
7. `../yidl-lifecycle/src/yidl_lifecycle/yidl/*.yidl` are the source layers for
   the generated lifecycle base. `_generated_lifecycle_base.py` is the committed
   generated runtime artifact and must continue to be regenerated without
   source change.

The generated class currently supports the main/current/working facade model,
lazy secondary facades, weakrefable facades, a slotted state object, lifecycle
metadata, transaction helper methods, direct property accessors, default
factory evaluation, field-level commit/rollback paths, and user-method
preservation through inheritance from the user class.

## 2. Current Feature Coverage

Implemented and covered by `../yidl-lifecycle/tests`:

1. Plain stored fields from explicit `field(...)`, bare annotations, and simple
   class-body defaults.
2. Constructor participation through `init=True` / `init=False`.
3. `initvar` values as constructor/default-factory inputs, including
   `init=False` initvars with defaults or factories.
4. `classvar` materialization on generated class and facade views.
5. `const` read-only values.
6. `static` lazy/write-once values.
7. `managed` transactional current/working values, including multi-group
   transactions, commit, rollback, `freeze`, `thaw`, and optional-`None`
   freeze/thaw skip behavior.
8. `transient` current defaults plus transaction-local working overlays and
   `working_default_factory`.
9. `local_store` as shared non-transactional instance storage visible through
   every facade.
10. `binding` scalar and map validation/storage through the default binding
    runtime.
11. `owned` scalar and map transaction commit/rollback paths.
12. Transaction order key, validation, before/after commit hooks, and
    after-rollback hooks by transaction group.
13. Transaction manager grouping, nesting, validation, commit-only, rollback,
    enlist/drop, and multi-group aggregate errors.
14. Default binding containers with CPython lifetime cleanup, plus an explicit
    refcount alternate runtime in `bindings_refcount.py`.
15. Golden coverage for emitted decorator/runtime source and representative
    generated lifecycle output.
16. Layering tests that prove partial lifecycle YIDL layers expose only their
    expected record surfaces.

## 3. Current Generic YIDL Substrate

The active generic substrate in `src/yidl` is the recorded concept / DDS /
assembly path:

1. `src/yidl/concept_parser.py` parses standalone `.yidl` concept modules.
2. `src/yidl/capsule/recorded_builder.py` records concept plans and replays
   them into the DDS/container/matcher system.
3. `src/yidl/generation/*` owns data definitions, containers, matchers,
   generated values, production operations, assembly specs, assembly runtime,
   and source emission.
4. `src/yidl/generation/assembly_source.py` emits runtime source for concept
   modules, including assembly metadata and `build_<AssemblyName>(...)`
   functions.
5. `../yidl-lifecycle/src/yidl_lifecycle/yidl/*.yidl` exercises this path as
   the first real product consumer.

The older indentation parser / `yidl-compile` / `YIDLTransformer` path is not
part of the working lifecycle system and should now be treated as retirement
material.

## 4. Missing Design Features

These are the remaining design features or decisions before calling YIDL
lifecycle complete.

1. **Runtime constants home.** The design summary still names
   `yidl.runtime.constants.VOID` / `UNSPECIFIED`, but current lifecycle code
   uses sentinels from `yidl.sentinel_maker` and generated runtime imports.
   Decide whether public sentinel constants move into `yidl`, stay
   lifecycle-local, or remain generator-internal.
2. **Final public API boundary.** `yidl` currently exports old parser symbols
   and transaction names. `yidl-lifecycle` exports the working decorator and
   marker surface. The intended public, semi-public, and private exports need
   one explicit map.
3. **Generic YIDL CLI.** `yidl-compile` still targets the old `LCKind`
   dataclass API-generation prototype. It does not generate the current
   lifecycle system and should either be deleted or replaced by a command that
   compiles concept modules / regenerates lifecycle artifacts.
4. **Regeneration command.** `../yidl-lifecycle` now exposes
   `yidl-lifecycle-regenerate-base`. Run it without arguments to verify that
   `src/yidl_lifecycle/_generated_lifecycle_base.py` matches the checked-in
   `src/yidl_lifecycle/yidl/*.yidl` layers; run it with `--write` to refresh
   the committed generated base. This command should remain the supported
   no-diff guard for lifecycle YIDL cleanup.
5. **Derived fields.** `derived` is still in the design summary but not in the
   current lifecycle marker surface or generated lifecycle layers.
6. **Lifecycle helper parameter strictness.** Current markers allow some
   positional spellings, such as `managed("group")`, while the design summary
   says helper calls are keyword-only. Ratify current ergonomic behavior or
   tighten it.
7. **Compare semantics.** `compare` is harvested for managed/owned/transient and
   identity guard generation exists for managed assignment, but the full
   helper-by-helper compare matrix should be rechecked against generated output.
8. **Initvar closure semantics.** Current initvars support default-factory
   injection, but retained initvar and post-init hook/validator consumption
   semantics are not yet complete against the full design summary.
9. **Callable injection registry.** Current factories support `cls`, `self`,
   earlier fields, and initvars in generated call sites. Hook/validator
   signatures are currently ordinary user methods without the full
   `current`/`working`/`previous`/`tx_key` injection registry.
10. **Resource transducer shapes.** Scalar and map binding/owned behavior exists.
    List and richer container shapes still need final transducer rules.
11. **Global owned evict-last policy.** Owned commit/rollback works for covered
    cases, but the design direction for global per-commit-step eviction across
    shared resource graphs is not ratified.
12. **Rollback error aggregation.** The transaction manager aggregates some
    multi-group failures, but generated field rollback cleanup should be
    checked against the design requirement for best-effort per-field
    `ExceptionGroup` behavior.
13. **Cross-group visibility.** Multi-group transactions exist, but visibility
    and barrier rules for reading one group while another has active working
    state remain undefined.
14. **Facade lifetime edge cases.** Weakrefable facades and cached secondary
    facades are covered. Refcounted-facade mode and reconstruction topology
    remain design-only unless explicitly dropped.
15. **Annotation-driven behavior.** Optional-`None` detection is implemented
    for freeze/thaw, but broader annotation-driven compare or container policy
    remains out of scope or undecided.
16. **Generated/source naming contract.** Current slots use names such as
    `_y_<field>_current` and `_y_<field>_working`, not the exact flat templates
    in the design summary. Either update the summary to the working naming
    scheme or plan a generation-compatible rename.
17. **Parser boundary wording.** `concept_parser.py` is the active `.yidl`
    parser. The old `lexer.py` / `parser.py` indentation syntax should be
    removed from active design language once source cleanup lands.
18. **Test matrix ownership.** Both `yidl` and `yidl-lifecycle` carry the shared
    golden/versioned test harness shape. Decide whether `yidl.testing` is the
    supported common home or whether lifecycle should own its own harness copy.

## 5. Must Preserve During Cleanup

Cleanup must not change these artifacts or behavior:

1. `../yidl-lifecycle/src/yidl_lifecycle/yidl/*.yidl`.
2. `../yidl-lifecycle/src/yidl_lifecycle/_generated_lifecycle_base.py`.
3. The ability of `yidl_lifecycle.lifecycle.lifecycle` to build generated
   classes from the committed generated lifecycle base.
4. `../yidl-lifecycle/tests/test_yidl_goldens.py` and its materialized
   decorator/generator assertions.
5. `../yidl-lifecycle/tests/test_lifecycle_yidl_layering.py`, because it proves
   the current YIDL layers compose in the intended order.
6. The generic substrate imported by lifecycle generation:
   `src/yidl/concept_parser.py`, `src/yidl/capsule/recorded_builder.py`,
   `src/yidl/generation/*`, and any runtime modules those imports require.

## 6. Recommended Next Decisions

1. Accept `../yidl-lifecycle` as the current canonical lifecycle package.
2. Retire the old `yidl` indentation parser / CLI false start from active
   source, after removing its exports and tests.
3. Add one supported regeneration command for `_generated_lifecycle_base.py`
   and make the no-diff check part of the lifecycle verification path.
4. Update `YidlDesignSummary.md` to reference the current lifecycle package
   split and the recorded concept / assembly path as implemented reality.
5. Work remaining lifecycle features as small gaps against the current
   generated-layer system, not against the old parser/compiler prototype.
