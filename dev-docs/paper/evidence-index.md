# Evidence index for the YIDL/Astichi paper

Prepared 2026-10-03 for [paper-draft.md](paper-draft.md). This index distinguishes
implementation inspection, checked-in tests/artifacts, bounded execution,
historical measurements, practitioner accounts, and proposals. A cited test was
**inspected**, not freshly run, unless a V entry says otherwise.

## Source and snapshot conventions

Every path below is relative to the root of the repository identified by its
prefix. `Y:` means YIDL, `A:` Astichi, `L:` yidl-lifecycle, and `P:` Pyrolyze.
These prefixes are evidence labels, not literal filesystem prefixes. For
example, `L:src/yidl_lifecycle/lifecycle.py` is relative to the yidl-lifecycle
repository root. Commands state their owning repository. Sibling references in
commands are relative to that root. No workstation path is required.

| Repository | Inspected HEAD | Working-state qualification |
| --- | --- | --- |
| Y | `95a6e3e52fc3d710d25c5d59315e791a3ed75cc4` | Dirty: lifecycle extraction, historical-doc moves, log and other changes |
| A | `387ca5e1da76204ee60922094734c13ee36383c0` | Native implementation/binaries are additional environment state; HEAD is insufficient to identify the installed binary |
| L | `1439d2fdc3776754cce2f4f8ff38dcc78ddc53c4` | Dirty: preferred lazy naming, mutable policy, generated base, fixtures/goldens, docs and tests |
| P | `5af937343ef3e557667d96bbf6830acce555353a` | Integration source/docs include local and ignored development material |

The bounded execution environment was CPython **3.12.12**, Darwin **arm64**,
using the existing workspace interpreter. Ambient lower-engine request was
`auto`; a selection-only check reported `native-rust`, no fallback reason.
The native extension build identity was not captured. No dependency installation
or binary rebuild was performed. This is a working-checkout observation, not a
reproducible release manifest.

Selected SHA-256 values distinguish content beyond HEAD:

| Source | SHA-256 |
| --- | --- |
| Y:`src/yidl/concept_parser.py` | `03eb7bc8a71f16989ad70a1c78e18626eabf092b5ab441402fcb7ac01cb5eed2` |
| Y:`src/yidl/generation/matcher.py` | `64524ec70af45cdc763960becbbc63241a28a6e8ae885660883873f6ed44558a` |
| Y:`MetaSquaredLog.md` | `8daef6e2455eb76ee1fcfd40daf0e52889983cbdf796b11bbcbde50b17befcce` |
| A:`src/astichi/assembler/scope.py` | `2dff9066bc563f7711f6165e3795a10620ec7c787e0ae4936a023e9776a7aadb` |
| L:`src/yidl_lifecycle/yidl/lifecycle_const_static.yidl` | `8aafd3c1cb4aacdc216b0ca8251425693b4444d267fb4416d3d0cc29b3164d3c` |
| L:`src/yidl_lifecycle/_generated_lifecycle_base.py` | `97b4598e15e0a7275dbcf989f3d9aaec3cab794f5b58a358ab438ae72f9f49fd` |
| L:`tests/data/goldens/materialized/yidl_transactional_parity_fields1/generated_output.py` | `c72589221aaa9178b11fae2fb09798f76281bc5f5c0c81c7fb44a85d47df68ed` |
| P:`src/pyrolyze/lifecycle.py` | `49aedc68a51571e5315281e26f40007dce24aa073c78534ab94b0a5d784e7afe` |

## Claim map

| ID | Major claim and best local evidence | Strength / boundary |
| --- | --- | --- |
| C1 | Motivation and exploratory detour: Y:`MetaSquaredLog.md`, section “2026-05-24 — The Five-Week Detour And AI-Assisted Architecture”; Y:`dev-docs/history/YidlArchitecturePosition.md`; P:`src/pyrolyze/lifecycle.py` (`LCKind`, `_FieldTables`, `LifecycleContextState`) | Practitioner narrative plus inspectable architecture. No controlled productivity data, causal time comparison, or claim of historical impossibility. |
| C2 | Generic concept-driven compiler: Y:`src/yidl/concept_parser.py` (`YidlCompiledConcept`, `compile_yidl_files`); Y:`src/yidl/capsule/recorded_builder.py`; Y:`src/yidl/generation/data_schema.py`; Y:`src/yidl/generation/assembly_runtime.py` | Implemented generic vocabulary. Architecture-position document supplies intent; source supplies implementation. Earlier lifecycle modules remain in YIDL. |
| C3 | Typed properties, records/families, collections, identities, filtered computed views and write policies: Y:`src/yidl/generation/data_schema.py` (`DataDefinitionSystem`, `RecordSpec`, `ComputedCollectionSpec`); Y:`src/yidl/generation/data_container.py` (`WritePolicy`, `DDSContainerBuilder`, `RuntimeComputedCollection`); Y:`tests/generation/test_data_write_policy.py`, `test_recorded_schema_family.py`, `test_data_container.py`; Y:`tests/data/gold_src/dds_composite_identity_lookup.py` | Source and checked-in tests; V2 directly checks a small typed-record selection. Generated slotted records are distinct from application dataclasses. No general incremental inference claim. |
| C4 | Resource matcher score/selection: Y:`src/yidl/generation/matcher.py` (`MatcherRuleSpec.score`, `MatcherRuntime._select`, `sequence`, `_validate_no_equal_score_overlaps`); Y:`tests/generation/test_matcher.py`, especially `test_more_specific_rule_wins_over_less_specific_rule`, `test_equal_score_overlapping_rules_reject_before_runtime` | Generic resource matcher has explicit overlap rejection. Do not infer identical static overlap checks for every contribution/operation matcher; those have separate paths. Cartesian-product and cache behavior are implementation details, not scaling results. |
| C5 | Derived records and imperative aggregate operations: Y:`src/yidl/generation/container_runtime_source.py` (production emission, aggregate-operation emission, operation runner); Y:`src/yidl/generation/data_container.py` (`DDSOperationContext`); Y:`tests/data/gold_src/dds_matcher_productions.py`, `dds_ordered_aggregate_operation.py`, `dds_generated_resource_flow.py`; Y:`tests/generation/test_yidl_operation_matchers.py` | Selected resources route into facts and operations. Production runner is explicitly ordered, not a demonstrated fixed-point logic engine. Operations retain arbitrary Python algorithm bodies. |
| C6 | Current imports and constrained concept merge: Y:`src/yidl/concept_parser.py` (`_merge_named_maps`, `_combine_contribution_matchers`, `_combine_operation_matchers`, `_merge_production_extensions`); Y:`tests/generation/test_yidl_lark_parser.py` (`test_yidl_lark_from_import_concept_extends`, `test_yidl_lark_diamond_inheritance_dedupes_inherited_maps`, matcher-rule and filter diamond tests); Y:`tests/data/gold_src/yidl_imported_concepts.py`, `yidl_update_a_dataclasses_split.py` | Current code/tests supersede gaps in Y:`dev-docs/history/lark_yidl/YidlImportAndConceptMergePlan.md` and its detailed companion. No blanket last-writer override or commutativity claim; export metadata is not a demonstrated privacy guarantee. |
| C7 | Contributions, production extension, phases and context semantics: Y:`src/yidl/concept_parser.py` (`_flatten_production_extensions`, `_order_production_phases`); Y:`src/yidl/generation/assembly_plan.py`; Y:`src/yidl/generation/assembly_runtime.py` (`_apply_resource_to_target`, `_binding_requests`); Y:`tests/generation/test_yidl_lark_parser.py` (`test_yidl_lark_phase_after_order_creates_ordered_phases`, missing-anchor/cycle/conflicting-order tests, `test_yidl_lark_phase_context_apply_from_overrides_phase_from`, `test_yidl_lark_phase_context_apply_where_replaces_phase_where`); Y:`dev-docs/history/YidlBetterMergePlan.md` | Implemented phase flattening and explicit context replacement. Historical plan explains the coupling problem; do not present its old “missing layer” statement as current. |
| C8 | Astichi holes, fallbacks, identifiers, external binding, scopes, emission and provenance: A:`docs/reference/public-api.md`, `marker-holes.md`, `marker-binds-and-exports.md`, `scoping-hygiene.md`, `descriptor-api.md`, `assembler-scope.md`, `materialize-and-emit.md`; A:`src/astichi/assembler/scope.py`; A:`tests/data/gold_src/hygiene_scope_collision.py`, `function_parameter_scope_hygiene.py`, `descriptor_bind_identifier.py`, `bind_external_literal.py`, `provenance_absorb_roundtrip.py`; A:`docs/reference/snippets/statement/defaulted_block_hole_filled/`, `scope/colliding_locals_two_inserts/` | Current reference, source and canonical fixtures; V1 is an executed filled-hole example. No formal hygiene theorem or universal semantic preservation. Marker-bearing source is parsed, not directly run as ordinary marker functions. |
| C9 | Substantial downstream lifecycle package and secondary examples: L:`README.md`; L:`src/yidl_lifecycle/yidl/lifecycle_core.yidl`, `lifecycle_default_factories.yidl`, `lifecycle_managed.yidl`, `lifecycle_transient.yidl`, `lifecycle_owned.yidl`, `lifecycle_const_static.yidl`, `lifecycle_local_store.yidl`, `lifecycle_base.yidl`; Y:`tests/data/gold_src/yidl_update_a_dataclasses_split.py`, `yidl_update_a_computedclass_defaults.py` | Feature inheritance and package boundary are inspectable. Dataclass/computed-class fixtures are secondary examples, not independent mature applications. L:`lifecycle.py::_field_record_type` still dispatches domain kinds. |
| C10 | Three timing stages and direct AST execution: Y:`src/yidl/concept_parser.py` module boundary and `compile_yidl_files`; L:`src/yidl_lifecycle/regenerate_lifecycle_base.py`; L:`src/yidl_lifecycle/lifecycle.py` (`lifecycle`, `_generate_lifecycle_ast`, `_build_lifecycle_container`); L:`src/yidl_lifecycle/_generated_lifecycle_base.py`; A:`docs/reference/public-api.md` (`to_executable_ast`) | Actual frontend calls Python `compile` on AST, executes it, then calls the class builder. This does not establish absence of all parsing at every import/template boundary; parser-free path assertions need instrumentation. |
| C11 | Before/after storage, facades and transaction split: P:`src/pyrolyze/lifecycle.py` (`Record`, `LCKind`, `_FieldTables`, `BindingBase`, `LifecycleContextState`); L:`src/yidl_lifecycle/lifecycle_harvester.py` (`harvest_lifecycle_definition`, `_field_fact`, `_validate_override`); L:`src/yidl_lifecycle/yidl/lifecycle_core.yidl` (`ClassBundle`); L:`src/yidl_lifecycle/transaction_yidl.py`; L:`tests/data/goldens/materialized/yidl_transactional_phase_b_decorator/generated_output.py` | Original already has abstractions; replacement emits direct storage and methods while retaining manager/user-library costs. Object topology is source-backed; no memory or throughput reduction measured here. |
| C12 | Intentional/deferred lifecycle differences and cleanup boundaries: L:`src/yidl_lifecycle/lifecycle_markers.py` signatures; L:`src/yidl_lifecycle/yidl/lifecycle_core.yidl` (generated constructor and binding properties); L:`src/yidl_lifecycle/bindings.py`, `bindings_refcount.py`; L:`tests/lifecycle/test_api_lifecycle.py` deferred-name inventory and `_skip_reason`; P:`src/pyrolyze/runtime/context_lcm.py` deactivation methods; P:`dev-docs/PytoLifecyleIntegPlan.md` | No strict superset claim; no user init/post-init chaining or generic close protocol; default generated binding differs from original transaction/explicit-refcount behavior. Marker surface lacks derived cache, initial_working, sidecars. Cleanup is still application/resource-specific. |
| C13 | Lazy/static alias and mutable setter composition: L:`src/yidl_lifecycle/lifecycle_markers.py` (`lazy`, `static = lazy`); L:`src/yidl_lifecycle/yidl/lifecycle_core.yidl` (`Mutable`); L:`src/yidl_lifecycle/yidl/lifecycle_const_static.yidl` (`StaticDefaultFactoryProperty`, `MutableLazyAssignment`, `MutableLazySetter`, `LazySetterContributions`, `lazy_setters` phase); L:`tests/data/gold_src/yidl_transactional_parity_fields1.py` (`_fixture_class`, `_assert_config_class`, `_assert_source_shape`); matching `generated_output.py` and `generated_output_prettier.py` | Uncommitted implementation and canonical artifacts. V3 executed generated-class assertions. No invalidation/recomputation added; current/working assignment is nontransactional. Frontend reproduction qualification V4/V5 applies. |
| C14 | Cross-language, containment, FastAPI/protobuf and self-description are proposals: Y:`MetaSquaredLog.md`, including “Meta3, Self Description, And Runtime Boundaries”; Y:`dev-docs/history/YidlArchitecturePosition.md`, “Concept Composition” and “Generality Checks” | Design possibilities, not implemented target backends or applications. Native Astichi implementation is not a YIDL cross-language output result. |
| C15 | Partial LCM integration and completion boundaries: P:`src/pyrolyze/runtime/context.py`; P:`src/pyrolyze/runtime/context_lcm.py`; P:`src/pyrolyze/runtime/context_bare_refactor_lcm.py`; P:`src/pyrolyze/runtime/context_state_lcm/`; P:`dev-docs/PytoLifecyleIntegPlan.md`, `PytoLifecyleIntegI0Findings.md`; P:`tests/data/lcm_integration/README.md`, `shared_completion.py`, `baselines/shared_completion.json`, `transaction_failures.py`; P:`tests/test_lcm_integration_characterization.py` | Default selector is LCM, migration target is decomposed LCM, and manager unification is later. Characterization records present behavior/debt, not approval or final acceptance. Not rerun for this paper. |
| C16 | Source-shape plus behavioral and boundary verification: L:`tests/test_yidl_goldens.py`; L:`tests/data/gold_src/support/golden_case.py`; Y:`src/yidl/testing/versioned_test_harness.py`; L:`tests/data/gold_src/`; L:`tests/lifecycle/test_api_lifecycle.py`; P:`tests/data/lcm_integration/README.md` | Golden harness validates/compares emitted sources and may write actual-results artifacts. It was inspected, not invoked wholesale. V3 checks existing artifacts in memory. Test presence/counts are not a correctness proof. |
| C17 | Performance evidence: A:`dev-docs/AstichiPerfAnal.md`; A:`dev-docs/AstichiPerformanceAnalysisAndOptions.md`; A:`dev-docs/perf-refactor/FullSelfNativeRustAstPlan-F6-handoff-perf.md`, `EngineSelectionContract.md`; A:`src/astichi/lower_engine/native.py`; A:`docs/validation/perf/yidl_lifecycle_import_baseline.py`; L:`tests/data/perf/README.md`, `run_lifecycle_constructor_perf_comparison.py`; L:`tests/test_lifecycle_decorator.py` (`test_lifecycle_generated_class_constructor_throughput_comparison`, `_make_dataclass_perf_class`, `_measure_constructor_throughput`) | Historical phases/workloads differ. No fresh timing, aggregate speedup, or application-performance result. Fixture excludes generation; dataclass loop is a materially different implementation. Gated normal-suite skip is explicit. |
| C18 | Architectural synthesis situated in related work | Primary-source map below supports antecedents; no exhaustive novelty search or head-to-head implementation comparison. The proposed distinction is this combination and its concrete composition behavior. |
| C19 | Significant AI involvement, evidence selection and limits | Y:`MetaSquaredLog.md` practitioner account; current drafting task and bounded commands; official ACM policy below | Model/tool/version/session inventory for development remains missing. Human ownership and detailed relevant-methods account required; no measured LLM comprehension/productivity advantage. |
| C20 | Audience and publication constraints | Official Onward! Papers 2026 call and ACM authorship policy, checked 2026-10-03 | Audience framing only; 2026 deadline passed. Future call not verified; no submission, author list, approval, or contact authorized. |

## Supplement: SQLAlchemy comparison (C22)

Added 2026-10-04 from readable official SQLAlchemy 2.0 documentation:
[Declarative Mapping Styles](https://docs.sqlalchemy.org/en/20/orm/declarative_styles.html),
[Session Basics](https://docs.sqlalchemy.org/en/20/orm/session_basics.html), and
[Transactions and Connection Management](https://docs.sqlalchemy.org/en/20/orm/session_transaction.html).
These support base/decorator mapping interfaces, unit-of-work change tracking,
flush versus commit, rollback expiration, and explicit nested savepoints.

Local comparison evidence: L:`src/yidl_lifecycle/transaction_yidl.py`,
`GroupTransactionManager.begin`, `commit`, `rollback`, and
`TransactionManager._get_group_manager`, `_normalize_groups`, `commit`, and
`rollback`; L:`src/yidl_lifecycle/yidl/lifecycle_managed.yidl`, transaction-key
derivation and field-to-key indexing; L:`src/yidl_lifecycle/yidl/lifecycle_core.yidl`,
current/working facade structure. Source inspection establishes separate
per-key manager state, counted same-key nesting, and sequential multi-group
completion. No fresh execution or SQLAlchemy/lifecycle parity experiment was
performed for this prose comparison. This is prior-art positioning, not a
performance ranking, an atomicity claim, or a claim that SQLAlchemy cannot
coordinate multiple databases or sessions. The proposed ability to generate
SQLAlchemy mappings/integration or another transaction policy is an application
of the generic generator model (C2/C14), not an implemented SQLAlchemy backend
or a demonstrated estimate of implementation effort.

## Supplement: nested composition and auto-binding motivation

The section 4.2 revision was inspected and written on 2026-10-04. Its additional
source evidence supplements C7–C9:

- **C7:** Y:`src/yidl/generation/assembly_runtime.py`,
  `_apply_production_contribution`, inserts a nested production root into the
  enclosing scope and then applies the child edges with a mapped root path.
  Y:`tests/data/gold_src/yidl_update_a_nested_productions.py` declares module,
  class, and method composition and validates the generated method's behavior.
- **C8:** A:`docs/reference/snippets/composition/nested_three_stage_trace/recipe.py`
  reuses prior build results in subsequent builds and supplies a trace binding
  at the outer level. A:`docs/reference/snippets/composition/staged_unroll_indexed_edges/recipe.py`
  adds indexed contributions to an earlier composition. A:`docs/reference/assembler-scope.md`
  describes inventory-driven resolution and missing/ambiguous candidate checks;
  A:`docs/reference/scoping-hygiene.md` distinguishes intentional sharing from
  collision handling. These sources support reusable nested composition, not a
  general associativity theorem. Recipes and fixtures were inspected, not
  freshly executed for this prose revision.
- **C9:** L:`src/yidl_lifecycle/yidl/lifecycle_core.yidl`,
  `CoreClassDefinition`, `CoreModuleProduction`, and `CoreClassProduction`,
  supply the concrete nested-production example.
  L:`src/yidl_lifecycle/yidl/lifecycle_local_store.yidl` supplies the inherited
  feature phases and property identifier/external mappings.
- **C21 — authoring motivation:** In the author's 2026-10-04 design discussion,
  the author reported that earlier YIDL required imperative binding steps and
  that auto binding made authoring declarative and easier for an LLM to generate.
  The author also requested keeping the broader LLM benefit as a hypothesis,
  rather than adding a measurement program. This is attributed practitioner
  evidence, not an independently reproduced historical comparison or a causal
  result. Difficulty generating binding instructions is distinct from difficulty
  reading the resulting composition declarations.

## Discrepancies and exclusions

**D1 — lifecycle compatibility.** Y:`dev-docs/YidlDesignSummary.md` is designated
canonical by its AGENTS file, but its original P1 reference/15-helper
descriptions include user initialization, explicit retain/release, close,
derived-cache invalidation, sidecars, and initial_working ambitions that do not
describe the present extracted marker surface. The paper uses current L source
and tests for implemented semantics. This is recorded evidence divergence, not
an edit to or replacement of the existing summary.

**D2 — stale skips.** L:`tests/lifecycle/test_api_lifecycle.py::_skip_reason`
contains an “unimplemented local_store” explanation, while
L:`src/yidl_lifecycle/yidl/lifecycle_local_store.yidl` and the canonical
`yidl_transactional_lifecycle_local_store` fixture exist. It also groups names
by historical terms. Do not use all skip strings as a current feature matrix.

**D3 — test porting.** The explicit old-test name list plus generated skipped
test functions preserve a coverage inventory; active tests sometimes normalize
old semantic expectations. A historical name containing commit/release is not
proof that old binding release semantics are active. The supplied **267 passed,
46 skipped** is a prior reported run, with no raw log or complete environment
manifest supplied to this draft. It was not independently reproduced.

**D4 — teardown comment.** L:`bindings.py::BindingBase.__del__` has a comment
promising immediate teardown. Source presence demonstrates the finalizer,
not that guarantee. The paper intentionally makes no portable prompt-cleanup
claim and points to explicit Pyrolyze deactivation paths.

**D5 — historical implementation gaps.** Import/merge and better-merge plans
describe missing mechanisms later covered by current compiler code and tests.
The old string-builder pipeline in Y:`docs/YIDLDesign.md` is explicitly
historical. Astichi performance notes labeled “current” describe earlier
workloads; newer native documents and current source prevent treating those
labels as current measurements.

**D6 — integration counts and readiness.** P integration notes include several
different checkpoint/focused/full-suite results and known failures. They have
not been conflated into a paper-wide success count. Default use of LCM and
passing construction characterization do not prove the decomposed migration is
finished or all publication/resource contracts are satisfied.

**D7 — matcher overlap scope.** Resource matcher static overlap checks are
directly inspectable. Contribution and operation selectors use separate
weighted-condition dispatch. A claim that all selector surfaces have the same
ambiguity analysis needs a separate audit; the draft restricts its rejection
claim to the generic resource matcher.

## Bounded execution record

**V0 — scope.** All three new files are under Y:`dev-docs/paper/`. Source reads,
git inspection, and in-memory probes were used. No golden harness, fixture
regenerator, complete product suite, dependency installation, or benchmark
timing was run. These limits avoid generating or modifying the user's existing
artifacts. A pre-write status/diff fingerprint was captured outside the
repository for the final preservation check; it is not a research artifact or
a snapshot of every ignored file.

The final check found unchanged tracked-diff fingerprints in Y, A, L and P.
Only the three paper files were added by this task. Three new untracked
Pyrolyze I3a review documents also appeared concurrently; they were left alone.
The parent checkout's fingerprint changed as its submodule dirty-state reporting
changed, so no claim of a frozen whole-workspace snapshot is made.

**V1 — Astichi worked example passed.** The complete first Python block in
paper section 4.1 was executed with bytecode writes disabled. `ast.unparse(tree)`
printed:

```python
def choose_value():
    return 'generated'
```

This was an ambient-engine check. An independent check subsequently identified
ambient selection as auto/native-rust. The empty-hole result is supported by
the existing unfilled reference fixture; it was not separately run in V1.

**V2 — DDS matcher worked example passed.** The complete program in section 5
was executed using `field.record(...)` to construct typed records. Both resource
identity assertions passed. This does not invoke the full emitted
parameter-production fixture or establish production/operation performance.

Both V1 and V2 can be rerun from the Y repository root without writing files by
extracting their blocks into an in-memory interpreter:

```sh
PYTHONDONTWRITEBYTECODE=1 \
PYTHONPATH=src:../astichi/src:../yidl-lifecycle/src \
  ../.venv/bin/python -B - <<'PY'
from pathlib import Path
import re
text = Path('dev-docs/paper/paper-draft.md').read_text()
blocks = re.findall(r'```python\n(.*?)\n```', text, re.S)
exec(compile(blocks[0], '<paper-astichi>', 'exec'), {})
exec(compile(blocks[1], '<paper-dds>', 'exec'), {})
print('Astichi and DDS examples passed')
PY
```

**V3 — canonical lifecycle artifact checks passed.** This exact probe executes
the canonical generated-class assertion function against existing outputs.
It intentionally omits `_assert_decorator_frontend`, `render_case`, and
`run_case`: no generation, formatting, golden rewriting, or actual-results
directories are involved. Both outputs passed on CPython 3.12.12.

From the L repository root:

```sh
PYTHONDONTWRITEBYTECODE=1 \
PYTHONPATH=src:../yidl/src:../astichi/src:tests/data/gold_src \
  ../.venv/bin/python -B - <<'PY'
import ast
import runpy
from pathlib import Path
case = runpy.run_path(
    'tests/data/gold_src/yidl_transactional_parity_fields1.py',
    run_name='paper_inspection',
)
root = Path('tests/data/goldens/materialized/yidl_transactional_parity_fields1')
for name in ('generated_output.py', 'generated_output_prettier.py'):
    source = (root / name).read_text()
    ast.parse(source)
    namespace = {}
    exec(source, namespace)
    case['_assert_generated_class'](namespace)
    print('canonical generated-class assertions passed:', name)
PY
```

**V4/V5 — fresh decoration failed.** The declarations below were attempted in
two fresh processes. V4 used ambient auto/native-rust selection and reached
`LifecycleDefinitionError: Config: lifecycle class build failed:
'build_lifecycle_class'` (underlying `KeyError`). V5 set
`ASTICHI_LOWER_ENGINE=python` and failed during AST generation: contribution
`StaticDefaultFieldProperty` could not target `facade_properties`, with a failed
binding request `field_name` and zero candidates. V4's process first ran the
small filled-hole example; V5 did not. Whether that distinction matters is
unknown. Neither failure is a complete engine-parity experiment.

```python
from yidl_lifecycle.lifecycle import lifecycle, lazy, static

assert static is lazy
calls = []

def make_cache(seed):
    calls.append(seed)
    return [seed]

@lifecycle
class Config:
    seed: int = lazy(default=2, mutable=True)
    cache: list[int] = lazy(default_factory=make_cache, mutable=True)
```

The intended subsequent checks (not reached) were first-access provider
capture, no recomputation after provider change, replacement through another
facade, and assignment-before-read bypass. Those semantics are instead supported
by source and the broader V3 canonical artifact assertions. No code was fixed,
no fixture was regenerated, and no root cause or blame is assigned. The exact
failure pair, selected-source hashes, and missing native build identity must
accompany any future attempt to reproduce it.

## Performance evidence and reproducible measurement plan

| Existing source | Workload/conditions actually described | Permitted use |
| --- | --- | --- |
| A:`dev-docs/AstichiPerformanceAnalysisAndOptions.md` | 2026-05-20 seven-field split dataclass fixture; Python 3.12; source emission; uninstrumented and cProfile work differ; 8–23 second discrepancy acknowledged | Historical motivation for avoiding repeated graph rebuild; not a current lifecycle timing or resolved speedup |
| A:`dev-docs/AstichiPerfAnal.md` | LCM import, eight decorated classes, direct executable AST; 5.268 seconds decorator work, 4.597 assembly, 0.660 materialization; 5.72 seconds unprofiled import; missing full revision/hardware manifest | Historical phase split only |
| A:`dev-docs/perf-refactor/FullSelfNativeRustAstPlan-F6-handoff-perf.md` | Eight-class self-native sample, tag `rust-fsn/f6-handoff-perf`; eight CPython AST constructions; `copy_python_ast` 0.030 seconds; explicitly noise-sensitive | Historical counter-shape observation; not whole-import throughput or a guaranteed timing improvement |
| L:`tests/data/perf/README.md` and comparison test | Checked-in generated fixture; groups 5/10/15 imply 15/30/45 total fields; slotted dataclass with loop-based post-init versus generated parameterized factories; sequential lifecycle-first runs, shared deadline, batch retention/drop | Constructor probe only; no generation time, application speed, or equal-code superiority |

After generation failures are resolved and an artifact release is pinned:

1. Record all repository SHAs and dirty patches/content, Python/platform/CPU,
   dependency versions, selected engine/capabilities, native binary hash and
   build flags, and opt-in generated-AST cache state. Separate process startup,
   first import, and warm reuse.
2. Use the documented import profiler in fresh processes for each requested
   engine, preserving its selection event and counters. From A:

   ```sh
   PYTHONDONTWRITEBYTECODE=1 ../.venv/bin/python -B \
     docs/validation/perf/yidl_lifecycle_import_baseline.py --engine python
   PYTHONDONTWRITEBYTECODE=1 ../.venv/bin/python -B \
     docs/validation/perf/yidl_lifecycle_import_baseline.py \
     --engine native --require-native-counters
   ```

   The explicit native path requires self-native production capabilities and
   must report failure rather than silently relabel Python work. Read the
   script's own path setup and instrumentation before interpreting counters.
3. Run the existing constructor probe from L without regeneration:

   ```sh
   PYTHONDONTWRITEBYTECODE=1 PYTEST_ADDOPTS='-p no:cacheprovider' \
   PYTHONPATH=src:../yidl/src:../astichi/src \
     ../.venv/bin/python -B tests/data/perf/run_lifecycle_constructor_perf_comparison.py
   ```

   This is the documented tooling with cache/bytecode writes disabled. Retain
   raw results for every size. Audit deadline truncation and order bias; the
   existing test is not a paper-quality statistical harness.
4. Design a separate approved measurement harness with alternating/randomized
   baseline order, equal budgets, warmups, at least 10 independent repetitions,
   all raw samples, and median/spread. Include the existing dataclass workload,
   a comparably specialized handwritten baseline, and the original lifecycle
   only where behavioral configurations are equivalent. Do not retrofit that
   harness into product tests for this writing task.
5. Measure concept compilation separately from decoration and construction.
   Include scaling in field count, contribution count, inheritance/phase depth,
   matcher input combinations, and dependency density. Then measure application
   transactions, facade access, retained memory and resource retirement in
   end-to-end workloads. No break-even point or amortized gain is claimed until
   those costs and use counts are known.

## Primary-source related work map

All sources were checked online on 2026-10-03. Comparisons in the paper are
bounded interpretations, not claims endorsed by these sources.

| Area | Primary publication / official project source | What it supports; retrieval boundary |
| --- | --- | --- |
| Generative programming | Czarnecki & Eisenecker, 2000, [author lab book record](https://gsd.uwaterloo.ca/publications/view/86.html); 1999, [Components and Generative Programming](https://gsd.uwaterloo.ca/sites/default/files/esec99.pdf) | System-family models and selection/assembly antecedents. Author-hosted paper retrieved; book record/abstract checked, not full book read. |
| Feature composition | Batory, Sarvela & Rauschmayer, 2004, [Scaling Step-Wise Refinement](https://www.cs.utexas.edu/~schwartz/ATS/fopdocs/AHEAD-Theory.pdf); [official AHEAD tools](https://www.cs.utexas.edu/~schwartz/ATS/fopdocs/) | Feature increments and composition are established; closer than a decorator-only baseline. Does not establish YIDL equivalence or novelty. |
| Workbenches | Fowler, 2005, [Language Workbenches](https://martinfowler.com/articles/languageWorkbench.html) | Primary design account; YIDL has not demonstrated integrated workbench tooling. |
| Model-driven engineering | Schmidt, 2006, [Model-Driven Engineering](https://www.dre.vanderbilt.edu/~schmidt/PDF/GEI.pdf) | Models and transformations as engineering artifacts. Does not validate YIDL's quality or portability. |
| Partial evaluation | Jones, Gomard & Sestoft, 1993, [author book site](https://studwww.itu.dk/people/sestoft/pebook/) | Program specialization given known input. Indexed author-site content retrieved; direct open failed. No claim of reading the entire book. |
| Explicit staging | Taha & Sheard, 1997, [author publication list](https://www.cs.rice.edu/CS/PLT/Publications/MultiStage/) | Publication identity/explicit-staging antecedent. Linked paper retrieval failed; a detailed formal comparison remains open. No unverified DOI copied into the draft. |
| Hygiene and syntax | Kohlbecker et al., 1986, [publisher record](https://doi.org/10.1145/319838.319859), [author-hosted scan](https://prl.khoury.northeastern.edu/img/kffd-tr-1986.pdf); [Racket Syntax Model](https://docs.racket-lang.org/reference/syntax-model.html) | Established capture/binding problem and explicit scopes. Scan has no extracted text; official Racket scope reference was readable. No theorem transferred to Astichi. |
| Decorator compiler | [Python dataclasses](https://docs.python.org/3/library/dataclasses.html) | Methods generated from annotated declarations; close application-level antecedent, not the entire framework comparison. |
| Structured model compiler | [Pydantic architecture](https://pydantic.dev/docs/validation/latest/internals/architecture/) | Collection of declarations, core-schema boundary, validation/serialization engine. No performance or expressiveness ranking. |

## Publication and AI policy verification

The [Onward! Papers 2026 call](https://2026.splashcon.org/track/splash-2026-onward--papers)
was directly readable. It welcomes exploratory implementation and worked
examples with validation, requires double-blind review and PDF in 10-point
SIGPLAN `acmart`, and limits the initial main body to 13 pages excluding
references. Accepted/revised main bodies may reach 17 pages. Its May 15, 2026
submission deadline has passed. These are 2026 audience/format facts, not a
verified future submission opportunity.

The [ACM authorship policy](https://www.acm.org/publications/policies/new-acm-policy-on-authorship)
canonical page returned 403. Indexed text on ACM's official publishing host
verified the May 14, 2026 revision, substantive human contribution/accountability,
the research-methods disclosure requirement, and writing-assistance distinction.
[Official MMSys 2027 guidance](https://2027.acmmmsys.org/research-track.html)
directly reproduces the relevant policy. Sole writing assistance no longer
requires disclosure; AI used in research or relevant implementation/artifacts
requires a detailed methods account. This project needs that account regardless
of its drafting assistance. No author names, institutional roles, approvals,
or conference-specific MMSys requirements have been invented or imported.

The draft's AI methods paragraph is explicitly incomplete: the practitioner log
supports substantial involvement, but the exact development models, versions,
dates, prompts, review history, and contribution allocation need human-supplied
or preserved documentary evidence before submission.
