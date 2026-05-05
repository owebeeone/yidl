# YIDL Design Summary Gaps Against Current Source

This review compares `dev-docs/YidlDesignSummary.md` with the current
`src/yidl/` tree. It records concepts that exist in source but are missing,
only mentioned in passing, or not clearly classified in the summary.

This document is a gap list, not a design override. Paths are relative to the
`yidl` repository root. The review includes the current working tree, including
the active `src/yidl/capsule/getter_concepts.py` slice.

## Summary Assessment

`YidlDesignSummary.md` is strongest for P1 lifecycle semantics: facades,
virtual/physical stores, transaction field behavior, sentinel intent, callable
injection, Astichi ownership, and the DDS/container/matcher substrate.

The main missing area is the implemented capsule/codegen substrate that now
sits between DDS and final class generation. Several source modules also still
represent older frontend/compiler experiments. The summary should classify
these explicitly as canonical, compatibility, prototype, or retirement-bound
so future work does not accidentally treat all source surfaces as equally
normative.

## Gap 1. Source-Layer Status Map

Source currently contains multiple layers with different maturity:

- Frontend/prototype parser and CLI: `src/yidl/lexer.py`,
  `src/yidl/parser.py`, `src/yidl/cli.py`, `src/yidl/ast_tx.py`.
- Generation substrate: `src/yidl/generation/*`.
- Capsule/codegen substrate: `src/yidl/capsule/*`,
  `src/yidl/codegen/wrapper.py`.
- Runtime support: `src/yidl/runtime/*`.
- Test support shipped under package namespace:
  `src/yidl/testing/versioned_test_harness.py`.

The summary's package section says these categories exist, but it does not
state which current modules are the intended path and which are legacy
scaffolding. That is especially important because both the older fluent
capsule builder and the newer DDS-native capsule definition path exist at the
same time.

Needed summary addition: a source-status table that classifies each package or
module family as canonical, compatibility/prototype, or pending retirement.

## Gap 2. Sentinel Families And Homes

The summary defines the long-term `VOID` and `UNSPECIFIED` split and states
that `src/yidl/runtime/constants.py` owns public sentinel constants. Current
source has several sentinel families instead:

- `src/yidl/capsule/core.py`: `UNSPECIFIED`.
- `src/yidl/generation/data_schema.py`: `REQUIRED`.
- `src/yidl/generation/matcher.py`: `NOT_PROVIDED`.
- `src/yidl/cli.py`: generated `_MissingType` / `MISSING`.

There is currently no `src/yidl/runtime/constants.py`.

Needed summary addition: explain the allowed non-runtime sentinel families,
their homes, and whether they are permanent subsystem sentinels or migration
scaffolding. Also clarify the migration path from the current capsule
`UNSPECIFIED` to the future runtime `UNSPECIFIED`, if they are intended to
become the same public object.

## Gap 3. Existing Frontend AST Shape

Section 27.3 says the parser outputs transducer, behavior, code, and marker
nodes. Current source has a more concrete and different AST:

- `StoreNode` and `SurfaceNode` with property dictionaries.
- `InputNode` with type/default expressions.
- `CompileAssertNode`.
- `InlineActionNode` and `BlockActionNode`.
- `BehaviorNode` with names, property dictionary, action list, and optional
  raw `CodeNode`.
- `TransducerNode` with options, inputs, compile asserts, and behaviors.

The lexer also defines the current `%%` raw-Python fence behavior, indentation
tracking, and structural-comment stripping.

Needed summary addition: either document this AST as the current frontend
contract, or mark it as legacy parser scaffolding distinct from the P1 grammar
plan.

## Gap 4. CLI API-Generation Prototype

`src/yidl/cli.py` implements a real command-line compiler surface:

- Script entry point `yidl-compile`.
- `map_type_hint(...)` mapping YIDL type syntax such as `@object(...)`,
  `@lambda`, `@str`, `@bool`, `@id`, and `@type`.
- `generate_api(...)` emitting dataclass-style `LCKind` / `LC*` classes.
- Helper function emission from `fieldhelper` or `classhelper` options.
- Generated `_MissingType` / `MISSING` sentinel.

This does not match the P1 summary's long-term generated-class model, and the
summary does not say whether this CLI is still supported, a bootstrap
experiment, or a dead-end prototype.

Needed summary addition: classify `yidl-compile` and the `LCKind` generation
shape. If it remains supported, describe how it relates to the P1 transducer
model; if not, call out its retirement path.

## Gap 5. Store-Operation AST Transformer

`src/yidl/ast_tx.py` contains `YIDLTransformer`, which rewrites Python snippet
calls such as `store.read()`, `store.write(...)`, and `store.has()` through an
alias map into concrete attribute reads, writes, and missing-sentinel checks.

The summary discusses Astichi lowering and future virtual field mapping, but
does not place this transformer in the architecture.

Needed summary addition: state whether `YIDLTransformer` is obsolete
pre-Astichi scaffolding, a still-supported compatibility lowerer, or a concept
to fold into the virtual-ref lowering model.

## Gap 6. Original Fluent Capsule Model

`src/yidl/capsule/core.py` defines a separate dataclass model:

- `CapsuleFacade`.
- `CapsuleProperty`.
- `CapsuleSpec`.
- `CapsuleMethod` and `CapsuleMethodSurface`.
- `CapsuleSpecValue` and `CapsuleSpecInstance`.
- `YidlCapsule.compose(...)`.
- `CapsuleBuilder` fluent namespaces for facade, property, spec, and method
  construction.

`src/yidl/capsule/base_capsule.py` and
`src/yidl/capsule/init_only_capsule.py` build on this model. The summary's
decision ledger says the original fluent capsule builder remains prototype
code, but the body does not document its concepts or the compatibility
expectations around exported APIs.

Needed summary addition: document the fluent capsule model as prototype or
compatibility surface, including whether exports from `yidl.capsule` are
stable during the DDS-native transition.

## Gap 7. Init-Only Capsule Decorator

`src/yidl/capsule/init_only_capsule.py` implements a substantial decorator
prototype:

- `field_spec(...)` marker values.
- `InitOnlyFieldSpec`, `ResolvedInitField`, and `InitOnlyClassDefinition`.
- `class_definition_from_class(...)` harvesting annotations and field specs.
- `compile_capsule(...)` / `compile_init_only_capsule(...)`.
- `emit_init_only_factory_source(...)` and runtime materialization.
- `render_init_only_class(...)` AST fallback/source renderer.
- Generated wrapper attributes such as `__yidl_class_definition__`,
  `__yidl_factory_source__`, and `__wrapped__`.

It also has behavior rules not called out in the summary, such as rejecting
`init=False` fields without defaults at decoration time and stripping field
spec markers from the wrapped class.

Needed summary addition: classify this decorator path and document the
observable behavior that tests rely on, or explicitly mark it as replaceable
prototype output.

## Gap 8. DDS-Native Capsule Definition Runtime

`src/yidl/capsule/definition.py` introduces the newer capsule path:

- `CapsuleConcept`: a named contributor over `DataDefinitionSystem`.
- `CapsuleDefinition`: an ordered set of concepts that builds a DDS.
- `CapsuleRuntime`: loaded generated DDS runtime with `new_builder()` and
  `build_container(...)` helpers.
- `emit_runtime_source(...)` and `load_runtime(...)`, including
  `evaluator_names`, `value_names`, and controlled `exec(...)` loading.

The decision ledger mentions `CapsuleDefinition`, but the summary lacks a
body section explaining the model, lifecycle, and boundaries.

Needed summary addition: add a capsule-definition section covering contributor
ordering, direct DDS extension, runtime source emission/loading, and the
relationship between `CapsuleRuntime` and later Astichi class assembly.

## Gap 9. Canonical Class-Shaped Capsule Schema

`src/yidl/capsule/class_concepts.py` defines a reusable schema for class-shaped
generation:

- Common properties: `Name`, `Init`, `Kind`, `Defaulted`, `DefaultValue`,
  `Order`, `TargetPort`, `Template`, `SourceName`, `TargetName`,
  `RuntimeValue`.
- Records: `ClassValue`, `FieldInput`, `Component`, `InitParam`,
  `InitAssignment`.
- Collections: `ClassValues`, `Fields`, `Components`, `InitParams`,
  `InitAssignments`.
- Computed collection: `InitFields`.
- Ports: `Class.name`, `Class.body`, `Init.params`, `Init.body`.
- Port index over target/order properties.

The DDS section explains records, collections, computed collections, and ports
generically, but the summary does not document this specific class-generation
schema as a reusable semantic layer.

Needed summary addition: describe the class-shaped capsule schema and its
invariants. In particular, `Kind` is currently a string-valued field with
default `"plain"`; that should be reconciled with the no-passive-tags design
rule if it is not merely temporary.

## Gap 10. Concrete Capsule Production Slices

Current source contains concrete DDS/Astichi production slices:

- `src/yidl/capsule/init_concepts.py`: `__init__` method, required/defaulted
  parameter templates, assignment templates, `InitParamTemplate` matcher, and
  the `"Class"` production group.
- `src/yidl/capsule/slots_concepts.py`: `__slots__` class variable emission,
  slot item records/collection/port, and the `"Slots"` production group.
- `src/yidl/capsule/getter_concepts.py`: property getter templates selected
  by `GetterTemplate`, `plain` vs `managed` field kind constants, evaluator
  naming for `getter_order_for(...)`, and getter edge binding.

The summary mentions build-mapper seams, but not these feature slices or the
pattern they establish for adding future field concepts.

Needed summary addition: define the capsule-slice pattern: concept
contributor, template resources, production group, value/evaluator names,
optional matcher selection, and build-plan/edge-plan contribution.

## Gap 11. Build Mapper Edge Model

`src/yidl/capsule/build_mapper.py` implements the first DDS-to-Astichi mapper:

- `RuntimePortRef` resolves a generated runtime port and owner identity.
- `TemplateEdgePlan` maps a produced record to an Astichi template edge,
  including template/order attributes, `arg_names`, `bind`, and `keep_names`.
- `ChildPortPlan` maps child records from a runtime port into a parent hole,
  with an optional owner selector.
- `CapsuleClassBuildPlan` defines class name/body ports, root class template,
  class name binding, class body hole, class body edge, and child ports.
- `build_class_source(...)` materializes one class source module from a
  container and generated runtime namespace.

The decision ledger names this seam, but the summary has no normative section
for edge planning, owner identity, instance naming, or mapper constraints.

Needed summary addition: promote the build-mapper model into the body of the
summary, including what is stable and what is intentionally narrow for now.

## Gap 12. Callable Wrapper Provider API

`src/yidl/codegen/wrapper.py` implements a generic provider-based wrapper
generator:

- `PropertySpec` and `PropertyProvider` protocols.
- `AccessorComposable`, either as an Astichi composable or as reference path
  segments.
- Ordered provider resolution by callable parameter name.
- Duplicate provider-argument rejection.
- Generated wrapper functions whose signature is the provider argument list.

Section 23 describes the lifecycle callable-injection model, but not this
implemented lower-level provider API.

Needed summary addition: explain whether `codegen.wrapper` is the canonical
implementation substrate for section 23, a narrower helper for capsule work,
or an interim prototype. If canonical, document provider ordering and
`AccessorComposable` semantics.

## Gap 13. Runtime Binding Container Semantics

Sections 15, 18, and 19 cover binding/owned cleanup at a policy level. Current
runtime source has more concrete container behavior:

- `src/yidl/runtime/bindings.py` is the default CPython-oriented runtime.
  It uses `BindingBase.__del__` for `_close()` and provides
  `BindingDict`/`BindingList` with lazy copy-on-write views over frozen
  snapshots.
- `FrozenBindingDict` and `FrozenBindingList` are immutable snapshot objects
  in the default runtime but are not themselves `BindingBase`.
- `src/yidl/runtime/bindings_refcount.py` is the alternate explicit
  `inc_ref`/`dec_ref` runtime. Its frozen snapshots subclass `BindingBase`,
  COW views retain/release snapshots, and writes retain new values before
  releasing old values.

Needed summary addition: document `BindingDict`, `BindingList`, frozen
snapshot, `freeze()`, and `cow_from_frozen(...)` semantics, including which
runtime is default and what behavior the explicit-refcount variant is meant
to preserve.

## Gap 14. Transaction Manager Multi-Group API Edges

The transaction section covers independent groups and nested begin counts.
Current source also defines concrete API behavior that is not fully captured:

- `TransactionManager.begin()` with no explicit group normalizes to the
  default group plus all configured non-default groups.
- Multi-group `begin(...)` returns a private scope object whose context exit
  commits or rolls back groups in reverse order.
- Multi-group `validate(...)`, `commit(...)`, `commit_only(...)`, and
  `rollback(...)` aggregate failures, while single-group paths preserve the
  underlying exception shape.
- `active_transaction` and `begin_count` are compatibility properties for the
  default group.

Needed summary addition: document these API edges or mark them as temporary
runtime compatibility behavior that generated code should avoid relying on.

## Gap 15. Runtime Source Emission Facade

`src/yidl/generation/data_def_sys.py` is a compatibility facade over the
schema, container, matcher, matcher-value, and runtime-source modules. It also
adds matcher storage to `DataDefinitionSystem` and exposes
`emit_container_runtime_source(...)`.

The summary documents the DDS concepts, but not the re-export/facade layer or
its stability. This matters because many capsule modules import from
`yidl.generation.data_def_sys`, not directly from the split implementation
modules.

Needed summary addition: state whether `data_def_sys.py` is the public
generation API, a compatibility aggregation module, or a temporary import
bridge.

## Gap 16. Source-Emittable Names For Values And Evaluators

Runtime source emission depends on named external bindings:

- `value_names` maps `MatcherGeneratedValue` or other values to source
  reference paths.
- `evaluator_names` maps computed callables such as `getter_order_for(...)`
  to source reference paths.
- The emission path validates reference paths before rendering.

The DDS section mentions source emission and generated/importable evaluator
names, but the summary does not describe this as a general contract used by
capsule definitions and production slices.

Needed summary addition: document `SourceNameMap` as the source-emission
contract for non-literal values and callables, including allowed path shapes
and failure behavior when a name is missing.

## Gap 17. Versioned Golden/Test Harness As Package Surface

`src/yidl/testing/versioned_test_harness.py` defines a real package-level test
support API:

- Golden source/materialized output directories.
- Runtime tag and actual-results directory layout.
- `regen-goldens`, `run-tests`, and `run-tests-all` CLI subcommands.
- `uv` environment creation and editable package installation.
- Parallel multi-version test execution and summarized reporting.

Section 28 mentions Python-version validation with `uv`, but it does not
describe the harness as a source module or identify which functions are stable
for tests.

Needed summary addition: either document the harness as canonical test support
or mark it as private even though it is under `src/yidl/testing`.

## Gap 18. Public Export Shape

Current package exports are narrower and different from some summary examples:

- `src/yidl/__init__.py` exports lexer/parser AST names and the transaction
  manager, but not `embed`, `global_args`, `VOID`, or runtime constants.
- `src/yidl/runtime/__init__.py` exports transaction and binding containers,
  but not sentinel constants.
- `src/yidl/capsule/__init__.py` exports both old fluent capsule objects and
  newer DDS-native concept/build-mapper objects.

Needed summary addition: define intended public, semi-public, and private
exports for the current phase. The `_yidl.py` bootstrap section should also
state whether `embed` / `global_args` are future-only, missing work, or
superseded by current compiler entry points.

## Covered Areas With No Major Gap Found

These source areas are already represented well enough in the summary:

- Broad DDS schema/container/matcher model in section 26.1.
- P1 lifecycle transaction concepts at the policy level.
- Binding/owned cleanup policy at the stage/update/evict level.
- Astichi/YIDL ownership boundary.
- Testing preference for golden/integration-style coverage.

The gaps above are mostly about implemented substrate details and source
surface classification, not contradictions in the main P1 lifecycle model.
