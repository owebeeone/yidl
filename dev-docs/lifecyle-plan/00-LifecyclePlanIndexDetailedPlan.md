# Lifecycle DDS Detailed Plan Index

## Purpose

This directory expands `dev-docs/YidlDdsGapsVLifecyclePlan.md` into detailed
implementation plans. Each document defines one feature or feature cluster with:

- exact intended semantics
- fluent API examples
- expected use case
- expected generated-source golden shape
- validation and diagnostics
- test coverage
- implementation notes

The directory name intentionally follows the requested path
`dev-docs/lifecyle-plan/`.

## Source Documents

- `dev-docs/YidlDdsGapsVLifecycle.md`: lifecycle gap analysis.
- `dev-docs/YidlDdsGapsVLifecyclePlan.md`: minimal DDS feature consolidation.
- `dev-docs/YidlDesignSummary.md`: canonical YIDL design summary.
- `pyrolyze/src/pyrolyze/lifecycle.py`: read-only behavioral reference.

History docs are not part of the active design source.

## Detailed Plans

1. `01-SchemaFamiliesDetailedPlan.md`
   - Union/variant ergonomics for lifecycle field declarations.
   - Common properties, variant records, and normalized field views.

2. `02-LayeredMergeDetailedPlan.md`
   - Ordered inherited-layer merge for field declarations.
   - Override policies and override diagnostics.

3. `03-IndexedKeyedDerivationsDetailedPlan.md`
   - Distinct indexed collections.
   - Tuple identity and keyed lookup expressions.
   - Transaction group indexing and special declaration uniqueness.

4. `04-GeneratedResourcesDetailedPlan.md`
   - Unified source-emittable resources.
   - Astichi code/template resources, imports, and semantic resources such as
     state references.

5. `05-DiagnosticsDetailedPlan.md`
   - Validation production shape.
   - Diagnostic records and final failure gate.

6. `06-ExternalFactProducersDetailedPlan.md`
   - Callable signature and annotation-shape fact producers.
   - Generated analyzer operations without DDS-core introspection.

7. `07-GraphClosureDetailedPlan.md`
   - Reachability and closure derivations.
   - Initvar retention and unused-initvar classification.

8. `08-LifecycleConceptsDetailedPlan.md`
   - How the lifecycle generator uses existing ports, matchers, productions,
     and generated resources without adding lifecycle-specific DDS core.

9. `09-LifecycleStaircaseDetailedPlan.md`
   - A concrete roll-build sequence for the first generated lifecycle subset.
   - Expected class-source golden and runtime behavior checks.

10. `10-CriticalReviewConsolidationDetailedPlan.md`
    - Critical review of the detailed plan set.
    - Consolidates feature-specific proposals into the minimal actual DDS and
      fluent-layer additions.

11. `11-ActualFeatureEnumerationDetailedPlan.md`
    - Crisp enumeration of the features actually being added to DDS and to the
      fluent/concept layer.

12. `12-YidlGrammarProposalDetailedPlan.md`
    - Proposed `.yidl` grammar covering DDS declarations, resources, matchers,
      productions, operations, concept composition, and imports between YIDL
      files.

13. `13-AstichiIntegrationDetailedPlan.md`
    - Astichi surfaces required by the lifecycle generator.
    - Required golden proof cases, including comment emission and class-head
      composition.

14. `14-ImplementationSlicingDetailedPlan.md`
    - Suggested implementation slices after consolidation.
    - Each slice states the DDS/fluent feature, Astichi proof/golden pressure,
      and lifecycle use that should land with it.

15. `15-PostSlice14LifecycleParityDetailedPlan.md`
    - Roll-build continuation after the current `lcb/slice-14-call-arguments`
      baseline.
    - Detailed parity slices for decorator/helper generation, defaults,
      callable injection, transaction behavior, advanced field kinds, resource
      cleanup, multi-facade routing, MRO override parity, and runtime parity
      harness coverage.

## Minimal New DDS Surface

After critical review, the complete lifecycle plan should add no more core DDS
primitives than these:

- composite collection identity
- keyed lookup value expressions
- ordered source sequences for generated operations
- aggregate generated operations over declared inputs and outputs
- generated resource unification and source emission

These items belong in the fluent/concept layer, not DDS core:

- schema-family ergonomics over `UnionSpec`
- layered merge as an aggregate operation pattern
- distinct indexing as an aggregate operation pattern
- graph reachability as an aggregate operation pattern
- diagnostic record/gate concepts
- external fact producers as aggregate operations
- state/facade topology
- state references
- helper surfaces
- operation phases
- method bodies
- commit/rollback pipelines
- resource cleanup semantics

## Design Guardrails

- Do not create a lifecycle-specific DDS engine.
- Do not copy the `pyrolyze.lifecycle` kind hierarchy.
- Do not add a second matcher runtime.
- Do not add a second production runner.
- Do not introduce string enum tags where semantic objects are intended.
- Do not use the Python parser in generated decorator or generated field-spec
  runtime paths.
- Use goldens for success-path generated source.
- Use bespoke tests only for narrow mechanics and failure modes.

## Roll-Build Expectation

Each feature should be built and tested in an isolated step, then immediately
used by the lifecycle scratch/staircase driver. The canonical slice order lives
in `14-ImplementationSlicingDetailedPlan.md` for the initial consolidated
build and continues in `15-PostSlice14LifecycleParityDetailedPlan.md` for
post-slice-14 lifecycle parity.

Do not wait until every feature is complete before using it. The scratch
driver should pressure each feature as soon as it lands.

Astichi integration should be proved with goldens only for successful generated
source shapes. Bespoke tests remain appropriate for Astichi parser/marker
failure modes, but lifecycle should not duplicate success-path Astichi coverage
with hand-written unit assertions.
