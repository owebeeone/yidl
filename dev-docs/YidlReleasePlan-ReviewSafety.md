# YIDL 0.1.0 Release Plan — Safety-AXIS REVIEW

**Review object:** `dev-docs/YidlReleasePlan.md` at `1ae6c0bb85d5b7cb449131dc31002af840a7f758`; planning baseline, not implemented or accepted.  
**Baseline:** YIDL `1ae6c0bb85d5b7cb449131dc31002af840a7f758`; reference-only tuple: Astichi `ce47c629973d8e5a6340ceaa89b0bc3e8788d5fe`, yidl-lifecycle `ee5ba633efdeac9fbdd74cfe67ecd975eab8a26d`, yidl-cache `a4ae595e0f9835a86dadec3bedebd383ebf9ae2f`, yidl-dataclass `202b01c879eb0ffb724158efe783b379fe522031`, yidl_undoable `ca68b8271841931506297db316911fe0ed3ad332`, GEARU `de51c0667ea44916d07f7364b7850b23981c5e4c`. YIDL and GEARU evidence was read through `git show` at these revisions. The other reference repositories were not inspected.  
**Date:** 2026-10-23  
**Axis:** Safety — publication sequencing, artifact identity, compatibility qualification, recovery, irreversible operations and authorized scope. Independent, adversarial, read-only. The other axis runs in parallel; nothing here relies on it. Filed verbatim by the lane owner.

**Verdict: GO** — zero P0, P1, P2 or P3 findings. This verdict accepts the plan’s safety structure at the draft-plan gate only; it does not qualify release artifacts or authorize execution or publication.

---

## 0. Evidence base

Read and inspected:

- The complete mechanically generated Safety review prompt and the review-loop skill.
- Workspace `AGENTS.md` and `AGENTS_GWZ.md`.
- At the fixed YIDL revision:
  - `dev-docs/YidlReleasePlan.md`, lines 1–212.
  - `AGENTS.md`, including read-only review, semantic-change consultation, dependency boundaries and process rules.
  - `dev-docs/YidlCodingRules.md`, especially sections 1–4 and 7–9.
  - `dev-docs/YidlDesignSummary.md`, particularly purpose/reference ownership, section 26 and 26.1, section 30 and the decision ledger.
  - `dev-docs/YidlDocumentationPlan.md`, particularly installation qualification, scope, consumer isolation, execution gates, public artifact selection, deployment and recovery.
  - `dev-docs/YidlDocShortcomings.md`, particularly its evidence limits, supported-route observations and D20–D28/A09.
  - `pyproject.toml` and `src/yidl/cli.py` as packaging and legacy-entry-point evidence.
- At the fixed GEARU revision:
  - `README.md`.
  - `docs/Configuration.md`.
  - `docs/ReleaseProcess.md`.
  - `pyproject.toml`, `src/gearu/cli.py`, and focused `src/gearu/release.py` inspection, including lines 342–498.

Verification:

- At both the start and end, YIDL HEAD equaled `1ae6c0bb85d5b7cb449131dc31002af840a7f758`.
- At both boundaries, the current plan SHA-256 equaled `93a09256b8076afd8473fe5bd62367746e3495c03bb51a8cd57257ca839eed2a`.
- The reviewed commit’s diff statistic showed one added file: the 212-line release plan.
- No files were modified. No builds, installs, tests, network operations or Git mutations were performed. No peer prompt or current-round report was read. No agents were spawned.

The plan’s historical test results were assessed as explicitly bounded evidence, not independently reproduced.

## Problem, requirement provenance, and scope

The operator requested preparation for an initial YIDL 0.1.0 release, a phased plan, documentation consolidation, preservation of archival references, and use of GEARU. The later authorization to commit the plan does not authorize its implementation or release.

The observed release-readiness problems have concrete support: package metadata omits Astichi, the installed CLI points to the older transducer workflow, the existing Python matrix is broader than the freshly reported verification, and public documentation and packaging qualification remain incomplete. These are appropriate subjects for release preparation rather than reasons to introduce new compiler capabilities.

The plan confines proposed implementation to YIDL and requires a later brief to identify allowed files and components (lines 16–27 and 204–208). Neighboring projects and workspace infrastructure remain reference-only. GEARU configuration and workflow qualification are justified by the operator’s explicit tool selection; modifying GEARU is expressly excluded.

The necessity check holds:

- Phase 1 requires trying the existing standalone route before dependency or infrastructure work.
- The passing explicit Python route is treated as evidence for a narrower qualification path; the mismatched native installation does not become authority to repair Astichi.
- A supported Python workflow can satisfy first use without a new CLI.
- Consumer projects, cache adoption, broad Lifecycle work and research publication do not become release prerequisites.
- External blockers require evidence and a separate proposal, rather than silently expanding implementation scope.

Existing documentation requirements supply provenance for the site and inventory work. They permit explicit limitations and qualified alternatives rather than requiring implementation of every mechanism discussed in the inventory.

No unsupported prerequisite or unauthorized component expansion was established. Optional external shortcomings are not current-deliverable blockers; no new external defect is asserted by this review.

## 2. Invariant analysis

| Invariant attacked | Counterexample considered and result |
| --- | --- |
| A plan or tool choice cannot authorize irreversible operations | Attempted to derive permission to commit, tag, push or publish from Phase 4 or GEARU adoption. Lines 182–198 explicitly deny that inference and require applicable authorization for each operation. |
| The selected tool must support the proposed release shape | GEARU creates and checks a temporary candidate, prepares the local commit/tag, and performs optional external steps. Registry publication belongs in the repository workflow. The plan requires qualification of both configuration and workflow before publication; it does not rely on GEARU directly uploading Python packages. |
| The approved candidate must remain the publication object | Considered a stale workspace build or later release preparation being substituted for reviewed artifacts. Phase 3 requires one exact candidate tuple with revision, dependencies and artifacts; Phase 4 presents final artifacts and requires publication of the exact approved artifacts. A substituted candidate would fail those gates. Workflow qualification must preserve that identity. |
| Workspace success cannot establish installed-package support | The baseline expressly distinguishes workspace tests from isolated installation. Phases 1 and 3 require wheel and sdist inspection, external installation, and execution without sibling or editable import assistance. |
| One backend or interpreter cannot qualify another | The plan requires evidence for each advertised Python/backend/platform configuration and permits narrowing unsupported claims. The controlling documentation plan additionally distinguishes requested backend selection from actual execution and fallback. |
| Candidate dependencies cannot silently require adjacent-project repairs | The plan allows existing published or candidate artifacts to establish feasibility, but requires separate treatment of unmet external dependencies. No upstream repair is authorized by a failed local environment. |
| Existing public behavior cannot disappear as incidental cleanup | Legacy API/CLI dispositions must be explicit. Removal or replacement requires ratification; classification is not permission to delete. |
| Failed release steps cannot justify replacing published identity | Considered failed checks, successful local preparation followed by failed push, and successful push followed by failed GitHub Release creation. GEARU’s pinned process documents bounded retries; the plan requires workflow qualification and forbids moving published tags or replacing published versions. Recovery that changes released contents must return for a new version and applicable authorization. |
| Documentation deployment cannot expose arbitrary repository contents | Phase 2 retains the detailed documentation plan, whose public-source selection requires explicit inclusion, artifact-manifest verification and exclusion of validation/internal material. Its deployment section also requires retained artifact identity and restoration instructions. |
| Review must not turn archival defects into repair authority | The plan explicitly excludes historical-reference repair, including failures introduced by archival moves. These do not become release-preparation implementation tasks through this review. |

These attacks did not establish a concrete failure sequence permitted by the plan’s gates. The gates still need implementation and evidence; their future deliverables are not missing implementation defects at this review stage.

## 3. Risks and next action

Actual release readiness remains unproved: licensing, registry ownership/version availability, dependency resolution, installed artifacts, the advertised support matrix and the GEARU-backed workflow all await qualification. In particular, GEARU’s own checks do not automatically establish the identity of packages built by a later publication workflow. The required workflow qualification must demonstrate that the approved candidate is the one published.

The next action is for the lane owner to file this report and merge the two independent verdicts. This review is finished. Any subsequent implementation requires the separately scoped activation brief already required by the plan.