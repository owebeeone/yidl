# YIDL code generation requirements and trade-offs

This document is the prerequisite design guide for the YIDL code generator. The generator must evolve during every feature slice, but it must do so with a stable sense of direction. The goal is to avoid drifting into an implementation that merely emits working Python while gradually coding the project into an architectural corner.

This document should be read alongside:

- `docs/YIDLDesign.md`
- `dev-docs/PROCESS.md`
- `dev-docs/CODING_RULES.md`
- `dev-docs/RuntimeExtractionPlan.md`
- `dev-docs/PRE_IMPL_DESIGN_REVIEW.md`

## 1. Purpose

The code generator has to bridge four concerns cleanly:

1. **Author-facing schema** — field helper declarations and decorator-harvested metadata.
2. **YIDL semantics** — transducers, surfaces, stores, phases, and behavior snippets.
3. **Generated Python shape** — stores, views, proxy, commit/rollback logic, helper closures, and initialization order.
4. **Runtime integration** — the minimum protocol required by `pyrolyze.lifecycle.TransactionManager` and related public runtime types.

The generator is not a final “after parity” phase. It is a first-class implementation path that must track the supported subset throughout development.

During the bootstrap phase, the compiler frontend may also support a temporary `_yidl.py` embedded-source container contract as described in `dev-docs/PRE_IMPL_DESIGN_REVIEW.md`. That path is development-only, slow, and unsupported; it exists to accelerate empirical validation, not to define the long-term delivery model.

## 2. Primary requirements

The generator must satisfy all of the following:

1. **Incremental viability**
   The generator must be able to emit runnable code for the currently supported subset of YIDL features during each feature cycle, even if unsupported features still exist elsewhere in the spec.

2. **Stable emitted architecture**
   The generated code should converge toward the architecture described in `docs/YIDLDesign.md`: explicit stores, views/facades, proxy, generated init path, generated commit/rollback sequencing, and Python-level storage/layout choices such as slotted generated stores/classes where the design calls for them.

3. **Subset-friendly operation**
   Unsupported transducers or behaviors must fail clearly and locally. The generator should not require “all features complete” before it can emit useful output for a supported slice.

4. **Deterministic output shape**
   Equivalent inputs should produce predictably structured Python. Deterministic ordering matters for review, test stability, and future caching.

5. **Reviewable intermediate forms**
   The project must maintain enough intermediate structure that a developer can inspect:
   - harvested schema/spec data
   - parsed YIDL AST
   - transformed behavior/snippet representation
   - emitted Python source or equivalent render plan

6. **No silent architectural regressions**
   The generator must not drift into reproducing runtime descriptor-table behavior just because it is expedient. If a shortcut materially changes the intended architecture, it is a design issue.

7. **Runtime boundary discipline**
   Generated output should rely on public runtime protocol only, unless a feature design doc explicitly approves a temporary exception.

8. **Parity traceability**
   For each supported slice, it must be possible to explain which YIDL elements, generator stages, generated structures, and tests provide coverage.

9. **Container/diagnostic continuity**
   The frontend must preserve enough metadata from temporary `_yidl.py` containers to support line remapping and diagnostics, including embedded source preservation and Python-file line offsets where required by the bootstrap contract.

## 3. Per-slice generator obligations

Each feature iteration must advance the generator, not only the hand-crafted baseline. At minimum, every completed slice should leave behind:

1. YIDL spec updates for the slice.
2. Hand-crafted/generated-shape baseline updates for readability and target-shape discussion.
3. Generator updates so the current supported subset can still emit code.
4. At least one test or verification path that exercises generated output for the supported subset.

The generator work for a slice may be narrow. It does not need to emit every feature immediately, but it must not be left behind indefinitely.

## 4. Architecture decisions the generator must preserve

Unless explicitly revised through design review, generator work should preserve these directions:

1. **Harvest first, then compile**
   Helper calls and decorator harvest produce a spec-like input which is then compiled into generated code. Avoid blending runtime reflection and generated execution in ways that obscure the seam.

2. **Generated classes over generic descriptor tables**
   Prefer explicit emitted stores/views/proxy methods over recreating a generic runtime dispatch layer.

3. **Context-aware snippet lowering**
   Abstract YIDL behavior snippets should lower through a contextual transformation step, not through string substitution hacks.

4. **Phase-sensitive generation**
   Construction, execution, commit, rollback, and metadata/class-generation concerns should remain distinguishable in the pipeline.

5. **Generated sequencing is part of semantics**
   Initialization order, binding “evict last”, commit ordering hooks, and view routing are semantic obligations, not formatting details.

6. **Layout choices belong to generated design, not source style**
   Python implementation details such as `__slots__` belong in emitted-architecture and runtime-design decisions, not as general coding-style requirements for YIDL source or docs.

## 5. Trade-offs to prefer

When forced to choose, prefer:

- explicit intermediate representations over magical direct emission
- local unsupported-feature failures over broad partial miscompilation
- deterministic emitted shape over clever compactness
- generator transparency over premature optimization
- architecture-preserving duplication over premature abstraction
- public runtime integration over private-runtime convenience
- feature-subset vertical slices over large speculative generator rewrites

## 6. Trade-offs to avoid

The generator should avoid these failure modes:

- **all-or-nothing enablement** — needing the whole lifecycle feature matrix before generation is useful
- **hand-crafted drift** — treating hand-written baseline code as the real implementation and leaving the generator perpetually behind
- **string-template sprawl** — burying semantics across ad hoc string concatenation without inspectable structure
- **runtime backsliding** — reintroducing descriptor-table or decoration-time machinery because it is easier than emitting the intended shape
- **silent unsupported behavior** — generating something plausible for a feature the generator does not actually understand
- **feature-local hacks** — solving a slice with a generator special case that cannot generalize
- **hidden coupling** — making emitted code depend on undeclared naming, ordering, or closure conventions
- **premature freezing** — overcommitting to low-level generation internals before the requirements are clear

## 7. Required generator design topics

Before generator work becomes routine in each feature cycle, this document and related design notes should address at least:

1. **Input contract**
   What exact structure does the harvester produce for codegen?

2. **IR boundaries**
   Which intermediate forms exist between harvested spec, parsed YIDL, transformed snippet AST, and final Python text?

3. **Unsupported subset behavior**
   How does the generator signal “this slice is not implemented yet” without blocking supported slices?

4. **Emission strategy**
   What is emitted as Python source, what is emitted as factories/helpers, and what is left to runtime support?

5. **Verification strategy**
   How do we compare generated output against the hand-crafted baseline shape and behavioral tests?

6. **Debuggability**
   How can a developer inspect generated artifacts when a slice fails?

7. **Determinism**
   What ordering guarantees are imposed on fields, helper emission, closures, methods, and class names?

8. **Migration path**
   How and when can the hand-crafted baseline shrink as generator coverage grows?

## 8. Suggested initial implementation posture

The safest posture is:

1. keep the hand-crafted baseline as a readable target,
2. require the generator to emit a supported subset every cycle,
3. keep unsupported features explicit,
4. let early slices refine the generator design through documented trade-off decisions,
5. treat major generator shortcuts as design questions, not just implementation details.

## 9. Open decisions to resolve early

These should be answered early in generator planning:

1. What is the canonical IR for stores/surfaces/behaviors before final emission?
2. Should field helper emission and class/factory emission share one pipeline or be staged separately?
3. What is the minimal end-to-end generated slice that must always stay green in CI?
4. What generated artifacts are committed, if any, versus inspected only in tests?
5. How are unsupported features reported to developers and tests?

## 10. Maintenance

Update this document when:

- a new generator stage is introduced
- an important trade-off is chosen
- a feature requires a previously unplanned generator mechanism
- design review changes the intended emitted architecture
