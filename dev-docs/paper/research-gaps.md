# Research gaps and next evidence

For [paper-draft.md](paper-draft.md), prepared 2026-10-03 and revised 2026-10-23.
This is an evidence agenda, not authorization for product edits, new experiments,
submission or publication. Claim/validation IDs refer to [evidence-index.md](evidence-index.md).

## What this revision establishes

The contribution is now bounded: per-field facts select a setter policy for an
explicit hole in an existing lazy-property recipe, with scoped bindings and
phase ordering preserving getter/factory reuse. The case is traced end to end
and compared with AHEAD's actual refinement account. No stronger novelty,
expressiveness or maintainability claim depends on implementing AHEAD here.

Fresh generation is no longer wholly unreproduced. V7 checks the canonical
string-annotation fixture under explicit Python lowering with persistent cache
off: behavior, source shape, fresh decoration and exact raw/formatted output
all passed. V8 checks the revised complete example. V6 retains the unchanged
runtime-annotation failure, and V4/V5 remain historical. Dataclass and Undoable
add related object-model applications and attributed installed-package evidence;
they do not demonstrate an unrelated domain. No whole product suite or benchmark
was run for this revision.

## Remaining publication evidence

1. **Self-contained artifact (C16, V6–V9).** Package a clean, pinned reproduction
   of the qualified route with source/resource hashes, dependencies and selected
   backend. Document its annotation requirements and failures separately from
   historical outcomes. Current source imports plus installed version metadata
   are not original-wheel identity. The central example succeeds without SDK
   repair; wider packaging/native/annotation shortcomings are separate findings,
   not prerequisites for this prose deliverable.

2. **Composition contracts (C4/C6/C7/C8).** Consolidate the implemented merge,
   diamond identity, filtering, resource precedence, phase context replacement
   and fallback-scope contracts into a compact semantic account. Audit negative
   coverage before broadening claims to all selector surfaces. No commutativity,
   hygiene theorem or general semantic-preservation result is established.

3. **Case boundaries (C12/C15/C23).** Preserve a current-versus-original Lifecycle
   contract matrix, especially initialization, ownership/cleanup, derived caches,
   initial working state, sidecars and shared transaction completion. Current integration acceptance was not re-audited; the entry point has
   changed since the earlier snapshot (D8). Attribute Dataclass/Undoable acceptance to their exact owning
   checkpoints and exclusions; their results do not establish Lifecycle's full
   suite or unrelated-domain generality.

4. **Human ownership and methods (C19/C20/C21).** Recover development model/tool
   versions, dates, representative sessions and human semantic/review decisions.
   The paper preparation itself used AI-assisted evidence selection and writing.
   Human authors must verify technical/bibliographic claims, choose authorship
   and approve the artifact. Recheck the intended future venue call and current
   AI policy before submission; the 2026 call is historical. Formatting, page
   budget and anonymization remain unfinished.

## Optional strengthening, tied to stronger claims

5. **Comparative extension task (C13/C18).** If claiming improved edit locality or
   effort, implement an equivalent extension in a close prior framework or
   compare documented maintenance tasks with matched contracts. The present
   AHEAD source comparison supports synthesis positioning, not an advantage.
   No comparative implementation is required for the current bounded claim.

6. **Performance (C10/C17/C23).** If retaining quantitative benefit claims in a
   future version, measure concept compilation, declaration specialization and
   instance execution separately on pinned artifacts. Use equivalent behavior,
   alternated order, repetitions and raw samples. Include startup, memory and
   transactions. Existing workloads and old Dataclass measurements must retain
   their provenance; corrected final paths are not measured speedups.

7. **Generality and usability (C1/C9/C14/C19/C21).** An unrelated domain would test
   broader reuse; a controlled change task could test comprehension and review
   cost. Neither is required to describe this implementation. Cross-language,
   self-hosting and FastAPI/protobuf ideas remain proposals. AI authoring benefits
   stay attributed observations/hypotheses, not measured results or a newly
   required productivity study.
