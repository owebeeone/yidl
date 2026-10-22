# YIDL End-User Documentation — CONSISTENCY-AXIS REVIEW, ROUND 2

**Review object:** Complete delivered YIDL end-user documentation, examples and documentation tooling at `ae2a44f3632b551af3a169d0684ee7c16f7df55c`.
**Baseline:** Previous reviewed revision `e98a22cc987342e1326384ee77cac6198b8bc647`; full delivered range begins at `43dd01b04f012d6e5877b88e9442461c38447a37`. Tracked sources and the actual committed diff were inspected. Required HEAD held at start and end.
**Date:** 2026-10-23
**Axis:** Consistency and technical accuracy against requirements, implementation and evidence. Independent, adversarial, read-only. The other axis runs in parallel; nothing here relies on its current report. Filed verbatim by the lane owner.

**Verdict: GO** — both original P2 findings and the original P3 finding are closed. No new blocking or nonblocking findings were established in the changed range.

---

## Prior-finding closure table

The first three rows retain this reviewer’s original IDs. Related prior Safety findings are included to account for the complete remediation patch; these observations do not substitute for that reviewer’s independent re-verdict.

| ID | Disposition claimed | Verified on corrected tree | Status |
| --- | --- | --- | --- |
| Consistency P2-1 | Teach the architecture and vocabulary before full source; correct the novice route. | Re-traced README, homepage primary button, Start Here/footer order and direct tutorial entry. Purpose, author inputs, responsibilities, generated products, facts versus instance values and stages precede the complete source. Served tutorial places complete declarations sixth and complete driver seventh among block listings. | Closed |
| Consistency P2-2 | Correct paths after changing into an external tutorial copy. | Re-traced the original directory-change counterexample against `install.md:55–87`. Interpreter location is captured before `cd`; the copied script is addressed as `generate.py`. Independently compared literal recorded commands with current Markdown; they match exactly. Recorded execution establishes expected observations and external output placement. | Closed |
| Consistency P3-1 | Include the decisive selection and projection evidence. | Served Lifecycle block includes the complete matcher and default selection. Its pinned source/excerpt hashes and exact selection were independently verified. Served evaluated-field block includes both original-record assertions and the extracted tuple assertion through line 305. | Closed |
| Safety P2-1 | Correct the shared novice-foundation root. | The same public-route and terminology checks above address the original architectural counterexample. Simple extension guidance identifies input facts/slots, authored resources and instance arguments separately. | Counterexample no longer present on this axis |
| Safety P3-1 | Correct the shared external-path root. | The corrected sequence preserves interpreter access across `cd` and addresses the copied script at its actual location. | Counterexample no longer present on this axis |
| Safety P3-2 | Describe option effects and defaults. | Parser help additions, recorded help and the public option table agree about scenario effects, false defaults and the current-directory-relative output default. Existing option names/actions/defaults remain unchanged. | Counterexample no longer present on this axis |
| Safety P3-3 | Document bounded cleanup while retaining authority. | Creation and cleanup destinations agree. External cleanup removes generated output and returns to the checkout; repository cleanup is explicitly limited to walkthrough-owned directories. Recorded cleanup retains original/copied authored sources. | Counterexample no longer present on this axis |

## Changed-range analysis

The actual range contains 22 changed paths:

- Eleven public-documentation, navigation, excerpt and example-help paths.
- Five remediation response/evidence paths.
- Six preserved original-review and owner-audit paths.

The corrections reuse the existing model and pipeline pages, move them into the beginner sequence, scaffold the tutorial before its full listings, correct the external-directory procedure, add cleanup/default guidance and extend two excerpt boundaries.

The sole changed Python example contains presentation changes: module description, argparse formatter and option help. An independent AST comparison, excluding those presentation additions, found the script unchanged. Generation logic, assertions, option actions, defaults and output writing remain the same.

No compiler/runtime source, metadata, dependency requirements, canonical model outputs, product bases, consumer repositories, platform contracts or deployment configuration changed in this range. Navigation changes affect ordering and labels within the existing site.

**NEW ARCHITECTURAL root causes: none established.** The new architecture prose explains the existing implementation; it does not introduce a new architecture or materially change the previous review premises. The patch remains within the merged dispositions and authorized documentation scope.

## 0. Evidence base

This focused continuation retains the first review’s complete documentation/source inspection and independently re-traces the corrected counterexamples.

Read in full on the corrected tree:

- README, homepage, model, generation stages, installation, first-generator tutorial and output-inspection page.
- Navigation configuration and complete changed example.
- Both prior review reports, merged remediation plan, author response and all four remediation evidence files.
- Changed excerpt metadata and the evaluated-field inclusion.
- Actual changed-range file inventory and relevant diffs.

Rechecked source relationships against the unchanged declarations, driver, evaluated-field test and pinned Lifecycle source.

Independent read-only checks established:

- Required HEAD at both start and end; status contained only the two lane-owner round-two prompts.
- Seven local preview routes returned HTTP 200.
- Homepage primary button and footer lead to the model; subsequent footers lead through generation stages, installation and first generator.
- The rendered tutorial’s short excerpts match their exact declaration selections.
- Complete declarations and complete driver match current source and appear after introductory explanation, field tracing and the stage table.
- Both corrected advanced excerpts appear in served code blocks.
- The changed Lifecycle excerpt matches its pinned committed source, whole-source hash and refreshed excerpt hash.
- Recorded build, first-use, help, external-run and cleanup shell blocks match the current public Markdown exactly.
- Every authored-source hash retained in `LiteralWalkthrough.json` matches current bytes.
- Normalized script AST is unchanged apart from description/help/formatter presentation.

The supplied remediation evidence records successful literal execution outside the workspace, installed package origins, removed ambient Python overrides, expected Point observations, output locations and cleanup retention. It separately records the installed example catalog, canonical checks, provenance checks and site build/check results.

Those executions were **not rerun by this reviewer**. No product code, examples, tests, builds, installations, cleanup commands or Git mutations were executed. Served HTML was inspected through read-only HTTP and parsing; visual rendering and interactive search were not independently repeated in this round.

## Problem, requirement provenance, and scope

The operator requires accurate documentation that teaches an ordinary Python developer what YIDL does before relying on substantial generator machinery. The initial defects were a teaching-sequence failure and a literal external-directory path failure, with a smaller excerpt-completeness defect.

The corrections address those observed problems directly. The model now explains the author’s inputs and the two generated products; the pipeline explains preparation, generation and use; the tutorial connects one field through declarations, resource binding and placement before presenting full source. The external procedure now resolves paths consistently with the directory change.

The scope remains public YIDL documentation, navigation, example help, excerpts and narrowly necessary evidence. Compiler/runtime source, metadata, dependency projects and generated product bases remain reference-only.

No new blocking prerequisite or scope expansion is asserted. The existing installed-wheel route remains sufficient. Packaging repair, a new CLI, native work, broader version/platform qualification and publication remain separate matters. The patch neither implements them nor uses their deferral to conceal a misleading instruction.

## 2. Invariant analysis

The following attacks did not establish new defects:

- **Architecture versus implementation:** The generator-library/application-code distinction agrees with concept compilation, runtime emission, fact population, assembly and final AST execution. The stages do not confuse class generation with instance construction.
- **Fact names versus values:** The introduction and tutorial consistently distinguish semantic `FieldName`, storage spelling `field_name`, emitted identifier `x` and the later instance value `3`.
- **Responsibility boundaries:** Application policy owns selected fields, slots and resulting behavior. YIDL owns declared inputs, selection, bindings, destinations and order. Astichi owns structural composition and naming/scope mechanics.
- **Template compilation timing:** Revised prose explicitly permits lazy template compilation during generation and distinguishes final AST compilation. It introduces no parser-free or wholly native claim.
- **Extension authority:** The documented simple change coordinates field facts, slot input and assertions. Resource behavior changes point to authored `.yidl`; generated output remains derived.
- **External path resolution:** The command uses the captured installed interpreter after changing directory, reads the copied authority beside the script and writes under the explicit external output destination.
- **Help/default parity:** Presentation agrees with the unchanged parser behavior. “Choose at most one” remains user guidance rather than a newly claimed enforcement mechanism.
- **Cleanup ownership:** Guidance conditions removal on walkthrough ownership and retains authored inputs. It does not add a product cleanup API or prescribe deleting shared build directories.
- **Excerpt fidelity and completeness:** The corrected blocks now show the semantic evidence originally missing, while retaining exact owning revisions and provenance.
- **Qualification and publication:** CPython 3.12+ remains the installation minimum; 3.12.12 remains executed evidence. The POSIX procedure does not claim Windows/native qualification. Documentation acceptance does not assert release or deployment readiness.

## Learning path and architecture/terminology analysis

The corrected reading order resolves the original learning defect.

The README and homepage begin with Python code-generation purpose and recognizable capabilities. The primary beginner route introduces the model before installation and the complete example. Start Here and footer navigation reinforce that same sequence.

The model supplies concrete meanings for facts, properties, records, collections, DDS, resources, holes, matchers, bindings, contributions, productions and assemblies. It separately explains AST, composable, materialization and hygiene through their roles. These terms are connected to the Point example rather than presented as an isolated glossary.

The pipeline then places those parts into preparation, per-generation work and application execution. Direct tutorial entry also supplies that distinction before its excerpts. Its one-field walkthrough and operation/result table precede both full source listings.

A reader can now decide where a simple change belongs: generation inputs and slot policy, authored resource/rules, or ordinary constructor arguments. Experienced readers retain an explicit direct-run anchor after installation.

This conclusion rests on the actual prose and served ordering, not merely the presence of links or successful site checks. It establishes closure of the documented counterexample; it is not a substitute for future usability feedback from real readers.

## 3. Risks and next action

**Review status: complete, not blocked.** All three original Consistency findings are closed, and the bounded remediation introduced no established new defects.

Residual limitations are unchanged: recorded runtime execution was inspected rather than independently repeated, and visual/interactive browser behavior was not re-exercised in this round. No broader backend, Python-minor, platform or release qualification is inferred.

The next action is for the lane owner to combine the two independent re-verdicts and record documentation acceptance if both permit it. This report requires no further remediation or broader implementation work.