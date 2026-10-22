# YIDL 0.1.0 Release Plan

Date: 2026-10-23. Status: planning baseline; release preparation is not yet
implemented or accepted. Target: an initial 0.1.0 alpha of the generic YIDL
compiler, with a bounded, reproducible supported surface.

## Scope and authorization

The current task delivers this plan, a consolidated developer index, a current
follow-up register, and archival moves within `dev-docs/` in the `yidl`
repository. It does not implement the phases below. Archival moves preserve
document bytes and existing references; no reference-repair sweep is included,
as explicitly directed by the operator. No commit, tag, push, or publication is
authorized by this documentation task.

Proposed release-preparation changes belong to YIDL: package metadata, public
documentation, runnable examples, narrowly necessary API/entry-point decisions,
and release verification. Astichi, yidl-lifecycle, yidl-cache, yidl-dataclass,
yidl_undoable, Pyrolyze and the GWZ workspace are reference-only. Changes to any
of those projects need separate authorization. A plan or discovered problem is
not authorization to widen implementation scope.

Functionality is a credible release candidate. Freeze new features while
qualifying what exists. Optional cleanup, a new CLI, caching, broader Lifecycle
semantics, and research claims must not become release prerequisites by default.
Changing or removing an existing public surface requires an explicit supported
surface decision; this plan does not select deletion.

## Baseline and evidence limits

- The inspected YIDL tree was clean at `39d3d53` before this documentation task.
  Package metadata and `yidl.__version__` already say `0.1.0`; this alone proves
  neither a published release nor registry availability.
- On CPython 3.12.12, the workspace environment with
  `ASTICHI_LOWER_ENGINE=python` passed 299 tests with 2 skips, including generated
  source comparisons. Command, from the YIDL repository:

  ```sh
  ASTICHI_LOWER_ENGINE=python PYTHONDONTWRITEBYTECODE=1 \
    PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 ../.venv/bin/python -m pytest \
    -q -p no:cacheprovider --maxfail=3 --tb=short
  ```

  The harness writes ignored actual-results artifacts. This is workspace
  verification, not an isolated install or a supported-version matrix.
- YIDL's own environment cannot import `yidl.concept_parser`: Astichi is absent.
  `pyproject.toml` declares Lark but not the Astichi dependency imported by the
  active compiler. This confirms a packaging gap; it does not show the compiler
  is unusable through the supported workspace route.
- The default workspace test run fails because the loaded Astichi native
  extension lacks a method expected by its Python code. The explicit Python
  route passes. Native compatibility needs a qualified dependency tuple before
  diagnosing a YIDL defect or proposing dependency/infrastructure changes.
- `yidl-compile` is the installed `yidl.cli:main` entry point for the old
  indentation/transducer helper generator, not the current concept compiler.
  Top-level package exports also expose that older parser surface.
- There is no root README, license file, changelog, public landing page, or
  documentation-site configuration in the inspected tree. Public design docs
  describe earlier compiler behavior. The detailed documentation plan exists,
  but its page and site deliverables have not been implemented.
- Python 3.12, 3.13 and 3.14 are listed in the test matrix; only 3.12 was freshly
  verified here. Platforms, installed wheels, sdists and native support are not
  qualified by this assessment. The two skips must be classified before release.

## Requirement provenance and execution shape

| Requirement | Source |
| --- | --- |
| Initial 0.1.0 release preparation and usable documentation | Operator's release direction |
| Phased milestones, one goal per step, foundational first | Standing planning instructions |
| Scope boundaries, feasibility before dependency changes, separate findings | Standing scope instructions and repository rules |
| Preserve current semantic and coding authorities | `AGENTS.md`, `YidlDesignSummary.md`, `YidlCodingRules.md` |
| Public docs/site requirements and example inventory | Existing `YidlDocumentationPlan.md` and `YidlDocShortcomings.md`; not new compiler requirements |
| No archive-reference repairs | Operator's explicit instruction in this task |

Each step is one goal with an aspirational change budget below 500 lines.
Budgets are sizing targets, not reasons to weaken acceptance. Split a large
reference page into cohesive steps before implementation rather than packing an
entire reference manual into one step. Dependencies below support independent
authoring where the supported contract is settled.

## Phase 1 — An installable, explicitly bounded release surface

Milestone: a new user can install the candidate and run the current compiler
through one supported workflow without sibling checkouts.

| Step | One goal and deliverable | Dependency | Target |
| --- | --- | --- | --- |
| 1.1 | Record the supported language/API/generated-artifact boundary and dispositions for legacy exports and `yidl-compile` | Baseline | <500 LOC |
| 1.2 | Qualify the smallest standalone install/import route using existing published or candidate Astichi artifacts, then declare the demonstrated dependency range and required package metadata/resources | 1.1 | <500 LOC |
| 1.3 | Provide one executable non-Lifecycle first-generator example from concept source through facts, assembly and generated-class behavior | 1.1, 1.2 | <500 LOC |
| 1.4 | Record the supported Python/backend/platform tuple and reproduce an isolated smoke run against it | 1.2, 1.3 | <500 LOC |

Acceptance:

- Review `compile_yidl_files`, emitted runtime source, recorded builders and
  assembly execution against actual imports and call sites. Explicitly classify
  supported, legacy, private, experimental and historical surfaces.
- A supported Python workflow is sufficient if it meets the actual use case;
  writing a new CLI is a choice, not an assumed prerequisite. Document the
  existing CLI honestly. Ratify removal/replacement before changing it.
- Test the existing install route before changing Astichi or building new
  infrastructure. A mismatched local native binary is not proof that an upstream
  fix is necessary. An unmet external dependency is recorded as a blocker with
  evidence and a separate proposal.
- Build and inspect wheel and sdist contents, including the grammar and other
  runtime resources. Install outside the workspace with no editable packages,
  sibling source paths or ambient import-path assistance; compile and execute
  the first-generator example.
- Select licensing with the project owner; do not invent a license. Confirm
  distribution ownership and whether the target version already exists before
  treating the candidate as publishable.

## Phase 2 — Documentation that teaches the released compiler

Milestone: users can install, author and debug a small generator from public
documentation, with tested examples and a usable reading order.

The active `YidlDocumentationPlan.md` remains the detailed page/site work map;
`YidlDocShortcomings.md` remains its evidence inventory. This release plan
controls milestone ordering and release gates, rather than duplicating those
documents or treating optional recipes as new compiler features.

| Step | One goal and deliverable | Dependency | Target |
| --- | --- | --- | --- |
| 2.1 | Publish the README, public landing page and installation/first-generator walkthrough using Phase 1's exact commands | Phase 1 | <500 LOC |
| 2.2 | Document current module/concept and fact-schema authoring with runnable grammar examples | 1.1; independent of 2.3 | <500 LOC per cohesive page |
| 2.3 | Document resource matching, binding, contribution/production ordering and assembly through a complete data-flow example | 1.3; independent of 2.2 | <500 LOC per cohesive page |
| 2.4 | Document supported Python APIs, generated-code dependencies, regeneration, compatibility, diagnostics and known limitations | 1.1, 1.4 | <500 LOC per cohesive page |
| 2.5 | Produce a strictly built, navigable documentation-site artifact with runnable examples and the existing inventory's coverage/disposition matrix | 2.1–2.4 | <500 LOC per cohesive tooling step |

Acceptance:

- Current braced Lark concept syntax is the main path. Reconcile outdated public
  architecture/API claims, including the unavailable `yidl.embed(...)` path,
  rather than presenting historical designs as implemented behavior.
- Distinguish the generic compiler from Lifecycle, Dataclass, Undoable and cache
  packages. Explain facts, templates and generated user objects separately.
- Demonstrate generated output and runtime assertions from the same authored
  example. Prefer the canonical fixture/golden harness over duplicated tests.
- Account for every D01–D28 and A01–A10 inventory item as documented, explicitly
  limited/deferred, or separately blocked with evidence. An unresolved mechanism
  is not a verified workaround, and a proposed example is not a required feature.
- Use the existing MkDocs/Material proposal as the delivery plan, not a reason
  to copy another project's metadata or widen scope. Qualify the site toolchain;
  publication follows Phase 4.
- Check active public navigation, examples and new links. Historical references
  and references to archived documents are excluded from repair, including any
  failures introduced by this task's archival moves.

## Phase 3 — A reproducible release candidate

Milestone: one exact candidate tuple has a reviewable evidence record and no
unresolved blockers for its advertised scope.

| Step | One goal and deliverable | Dependency | Target |
| --- | --- | --- | --- |
| 3.1 | Execute the regression/generated-output and installed-artifact matrix for each advertised Python/backend/platform configuration | Phases 1, 2 | <500 LOC of harness/evidence changes |
| 3.2 | Prepare 0.1.0 release notes, compatibility/support policy and the remaining issue dispositions | 3.1 | <500 LOC |
| 3.3 | Review the candidate against its requirements, scope, package contents and executable documentation | 3.1, 3.2 | <500 LOC of checklist/evidence |

Acceptance:

- Record dependency versions, backend selection, operating system, candidate
  revision and artifacts. Test both wheel and sdist installation and run the
  published quickstart in a fresh environment outside GWZ.
- Explain skips and any unsupported configurations. A passing local Python run
  cannot stand in for native or cross-platform qualification. Either demonstrate
  an advertised configuration or explicitly bound the release claim.
- Record related consumer evidence when available without changing their
  repositories or making their whole feature roadmaps prerequisites.
- No unexplained source/golden drift, hidden sibling dependency, wrong installed
  command promise, missing package resource, or undocumented breaking decision.
- Keep defects, unsupported features, hypotheses and optimization opportunities
  distinct. Reviewer checks include requirement provenance and authorization,
  not only technical correctness.
- Core packaging and first-use documentation are release gates. Cache adoption,
  broad prototype cleanup, performance claims and research publication are not.

## Phase 4 — Publish the reviewed candidate

Milestone: the exact approved artifacts and documentation are publicly usable.
This phase describes future actions; it grants no Git or publication permission.

**Selected release tooling: GEARU**, explicitly selected by the operator.
Prepare and verify the YIDL release configuration and workflow through GEARU
before publication. Use GEARU for the authorized release operations; do not
substitute an ad hoc release script. This selection does not authorize changes
to GEARU itself or execute a release.

| Step | One goal and deliverable | Dependency | Target |
| --- | --- | --- | --- |
| 4.1 | Present the final artifacts, release notes, support tuple and remaining limitations for publication authorization | Phase 3 | <500 LOC |
| 4.2 | Perform only the separately authorized publication operations and verify the consumer-facing install/docs route | 4.1 approval | <500 LOC |

Tagging, committing, pushing, registry upload, GitHub release creation and site
deployment are distinct operations and require the authorization applicable to
each. Never move a published tag or replace an already published version. Verify
the published package from a fresh consumer environment and the deployed docs
against the approved candidate; record the result and any discrepancy.

## Immediate next execution boundary

The next implementation brief should activate Phase 1 in YIDL only and name its
allowed files/components. It should resolve legacy CLI/API and licensing choices
with concrete evidence, then perform the smallest standalone feasibility test.
Do not start compiler refactors, dependency fixes, or adjacent-project work just
because this plan names them as possible findings.

See `YidlReleaseFollowUps.md` for retained concerns outside the release gates and
`history/README.md` for this task's archival disposition. The older release TODO
audit is superseded as an execution checklist, not represented as completed.
