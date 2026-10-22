# YIDL End-User Documentation — CONSISTENCY-AXIS REVIEW

**Review object:** Delivered YIDL end-user documentation, examples and documentation tooling at `e98a22cc987342e1326384ee77cac6198b8bc647`, including changes since `43dd01b04f012d6e5877b88e9442461c38447a37`. Documentation acceptance review, not release acceptance.
**Baseline:** YIDL HEAD was the required revision at both start and end. Public documentation and implementation were read from tracked working-tree files, with no tracked changes reported. Consumer provenance was checked against the exact committed objects named in the snippet manifest.
**Date:** 2026-10-23
**Axis:** Consistency and technical accuracy against controlling requirements, implementation and recorded evidence. Independent, adversarial, read-only. The other axis runs in parallel; nothing here relies on it. Filed verbatim by the lane owner.

**Verdict: NO-GO** — two P2 findings block acceptance; one P3 finding is nonblocking. I pre-commit to GO on a revision that resolves P2-1 and P2-2 as specified, provided those corrections introduce no new contradictions.

---

## 0. Evidence base

Read public documentation cold before consulting the plan, shortcomings inventory or implementation:

- Root `README.md`, all public pages under `docs/start/`, `docs/concepts/`, `docs/guides/`, `docs/reference/`, `docs/examples/`, `docs/troubleshooting/` and `docs/contributing/`, plus `docs/index.md` and `mkdocs.yml`.
- The complete first-generator declarations and driver: `example/documentation/classes.yidl:1–133` and `generate.py:1–134`.
- Complete capture, control-flow and comparison recipes; canonical wrapper `tests/data/gold_src/documentation_classes.py`; all seven canonical model outputs.
- Complete `dev-docs/YidlDocumentationPlan.md:1–503` and `dev-docs/YidlDocShortcomings.md:1–795`.
- Applicable repository/workspace instructions, the complete coding rules and release plan, and relevant design-summary semantic sections, especially §26.1 and the source-container boundary.
- Documentation activation review, inventory, outside-scope findings, verification record, example evidence and Python-minimum correction.
- Documentation inclusion/checking/provenance/example-verification scripts, pinned dependencies, build-only workflow and consumer snippet manifest.

Targeted implementation inspection covered:

- Concept compiler entrypoints and compiled-concept metadata.
- Current complete language grammar.
- Generated record constructors and immutability, collection identity/cardinality, ordering, computed views, lookup and freeze.
- Generic matcher input order, scoring, overlap validation, tuple extraction, original records and evaluated fields.
- Generated-value factories, accepted literal domain, template-edge evaluation and lazy caching.
- Assembly index/order evaluation, contribution selection, empty-resource suppression and diagnostic helpers.
- Matcher-result production snapshots and aggregate-operation emission.
- Legacy CLI implementation.
- Canonical import, multi-source, lookup and matcher-production fixtures, and the cited multi-input evaluated-field test.

Independent read-only checks:

- `git rev-parse HEAD` and `git status --porcelain=v1` at start and end; required HEAD held. Only lane-owner review artifacts were untracked.
- Inspected the delivered change inventory: 63 changed files.
- Recomputed stored excerpt hashes and independently compared all fourteen excerpts and their whole-source hashes with the named consumer Git objects. All matched.
- Read seven local preview routes through HTTP GET; all returned 200, without unresolved inclusion tokens.
- Parsed served code blocks: the first tutorial’s complete declarations/driver and all fourteen consumer excerpts matched their source authorities.

No tests, builds, installations, examples or product code were executed during this review. Recorded passing executions are evidence supplied with the delivery, not independently rerun results. Browser rendering, visual responsiveness and interactive search were not independently exercised; served HTML was inspected instead.

## Problem, requirement provenance, and scope

The requested outcome is usable end-user documentation for Python developers who do not already know YIDL, DDS, Astichi or the matching/binding/assembly vocabulary. The operator explicitly supplemented the original plan with an early understandable purpose, architecture and vocabulary requirement. The earlier plan GO authorized creation; it did not accept the delivered learning experience.

The observed problems are localized: the primary introductory route reaches substantial declarations before supplying the prerequisite mental model, and the installation page gives a command incompatible with its stated changed working directory.

Authorized remedies remain within public prose, navigation, inclusion boundaries and narrowly necessary documentation verification. Compiler/runtime source, package metadata, generated product bases and adjacent repositories are reference-only. No dependency or infrastructure expansion is necessary.

The existing supported route has concrete feasibility evidence: a freshly built current YIDL wheel, explicitly installed published Astichi 1.1.3, CPython 3.12.12 and the Python backend completed the documented standalone examples. Missing dependency metadata does not justify making packaging repair, a new CLI, native work or a registry release prerequisites for these documentation corrections.

The inventory’s limited dispositions are generally honest. Broader target-context qualification, unresolved nested-expression propagation, native ownership/recovery, provider matrices and two-consumer packaging remain limitations rather than silently expanded implementation requirements.

## 1. Findings

### [P2-1] The primary novice route relies on unexplained architecture before the large example

**Location:** `README.md:3–17`; `docs/index.md:3–16,29–44`; `mkdocs.yml` Start Here ordering; `docs/start/first-generator.md:20–39`. Relevant existing foundations: `docs/concepts/model.md:15–35` and `generation-pipeline.md:3–28`.

**Violated invariant:** The operator requires an accessible general architecture and early vocabulary before depending on the installation-to-large-example sequence. The plan also requires a readable end-to-end route without consulting implementation or experiment transcripts.

**Reproduction:** Start with the README’s installation/first-generator links, or the homepage’s primary “Generate your first class” button. The tutorial introduces “schema,” “resources,” “normalized,” “consumer” and “DDS,” then expands the complete 133-line concept before explaining its parts. It next expands the complete 134-line driver before giving the ordered stage explanation. It provides no preceding link to the model or pipeline.

The homepage does offer an optional model link, and that page contains useful definitions and a diagram. This is positive evidence, but the advertised first-use route does not bring those explanations into the sequence before requiring them. DDS is not expanded there; “composable,” Astichi stitching and hygiene are also used without an introductory explanation appropriate to an ordinary Python reader.

**Impact:** Readers can run a supplied program while remaining unable to distinguish generator definitions, generated fact records, per-generation input facts, assembled Python and user instances. Understanding or modifying the first example requires backtracking or inference—the architecture misunderstanding this task explicitly seeks to correct.

**Required correction:** Establish a clearly signposted conceptual introduction before the substantial tutorial listing. Explain YIDL’s purpose, the YIDL/Astichi/consumer boundary, the major artifacts and stages, and the essential vocabulary in ordinary Python terms. Reuse the existing model/pipeline content where appropriate. Preserve the quick execution route for experienced readers; no particular page path, diagram or additional framework is required.

**Closure check:** Follow both README and homepage novice routes cold. Before encountering the full concept/driver, a Python developer should be able to identify what the author supplies, what YIDL generates, what facts describe, what Astichi contributes, and when the final class and instances exist. Check prose against the actual tutorial and implementation, then inspect the rendered route. Link/build success alone does not close this finding.

### [P2-2] The outside-checkout installation command retains checkout-relative paths

**Location:** `docs/start/install.md:50–60`.

**Violated invariant:** Commands must agree with their stated working directory and demonstrate the advertised standalone installed route.

**Reproduction/state sequence:**

1. Build the environment under the repository as instructed.
2. Copy `example/documentation/` into an otherwise empty external directory.
3. Change into that copy, as lines 52–53 instruct.
4. Run the command at lines 58–59.

The command still addresses `build/example-env/bin/python` and `example/documentation/generate.py` relative to the new directory. Neither exists in the stated otherwise empty copy. Even if the reader manually fixes the interpreter reference, the copied script is `generate.py` in the stated working directory rather than the nested repository-relative path.

This is established from the path relationships; product execution was prohibited during this review.

**Impact:** The explicitly advertised isolation/reproduction step fails before reaching YIDL. The existing evidence verifier successfully uses an interpreter and script path resolved before changing directory, so its passing result does not validate this literal public command.

**Required correction:** Make the command and working directory agree. Explain how to retain the installed interpreter’s usable location across the directory change and address the copied script correctly. Keep machine-specific absolute paths out of committed examples. Alternatively, label the existing command as a separate repository-root invocation and supply the actual external invocation.

**Closure check:** Execute the corrected public sequence literally from a fresh external directory using installed packages, without sibling imports or ambient `PYTHONPATH`. Confirm the expected observations and output location, and record the qualified environment.

### [P3-1] Extraction boundaries omit the semantic evidence the adjacent prose promises

**Location:** `docs/_snippets/consumers.json:134–143`, used by `docs/examples/consumers.md:76–83`; and `docs/guides/matching-and-data-flow.md:84–90`.

**Violated invariant:** Mechanically faithful excerpts must still include the portion needed to demonstrate the described selection/result contract. The plan’s §5.4 requires the selected matcher/rule and why it is selected.

**Reproduction:**

- The Lifecycle `lifecycle_rule` excerpt contains a preceding closing brace and only the matcher’s opening declaration. It omits the actual `default -> ManagedDefaultFacadeProperty`, present immediately afterward in the pinned source.
- The multi-input recipe selects `test_matcher.py:245–303`, omitting lines 304–305, which assert the second original record and the extracted `(True,)` tuple—the precise distinction introduced immediately above it.

The served blocks reproduce these boundaries exactly. Hash/provenance checks pass because the truncated selections are authentic.

**Impact:** The page claims to show a real selection/projection chain but omits its decisive evidence. Readers must inspect the owning source to establish the missing relationship.

**Required correction:** Extend selections through the relevant semantic unit: the Lifecycle matcher’s selection/body and the evaluated-field test’s final original-record/tuple assertions. Refresh affected stored hashes where necessary.

**Closure check:** Verify provenance, then inspect rendered excerpts for the promised selection and both original-record/extracted-value observations. Retain the consumer’s exact revision and qualification boundary.

## 2. Invariant analysis

The following attacks did not establish defects:

- **Current versus legacy frontend:** Documentation correctly separates the braced concept compiler from the transducer CLI. The documented Python entrypoints match implementation.
- **Stage ownership:** Tutorial declarations, driver and outputs agree about generated schema/library versus final Python model. Assembly naming correctly produces `build_Module`.
- **Fact naming and ordering:** Semantic `FieldName` versus storage `field_name`, owner filters, separate identities, composite numeric build indices and explicit insertion order agree with source and outputs.
- **Empty behavior:** No match, empty-source suppression, empty parameter payload and `pass` remain distinct. Zero-field and omitted-init outputs support that explanation.
- **Generic matching:** Input tuple order, extracted tuple schema, scoring, overlap validation and original-record projection match the inspected implementation.
- **Captures and caches:** The capture recipe installs live objects in separate namespaces; its assertions address identity and callback timing. Documentation does not confuse the unbound template cache with a completed-class or runtime-value cache.
- **Qualification:** The corrected CPython 3.12+ minimum is distinct from the executed 3.12.12 tuple. New recipes are not promoted to native or cross-platform acceptance.
- **Unresolved mechanisms:** Flat comparison success is not represented as a repair of D17, universal dataclass equivalence or universal scalar-carrier support.
- **Public output and deployment boundary:** Configuration explicitly excludes historical design/validation/snippet-storage content. Workflow permissions and steps implement build/artifact retention without deployment.
- **Source ownership:** Canonical snapshots supplement independent assertions rather than acting as the sole behavioral oracle. Consumer snippets match fixed committed authority; no live consumer checkout is required for the site build.

## Learning path and architecture/terminology analysis

The existing material provides useful foundations. The model page distinguishes definitions, records and user classes; the pipeline page separates parsing, fact production, matching, assembly, materialization and execution. The two-owner guide concretely explains identity, ownership, bindings and order. These are suitable foundations to retain.

The acceptance gap is their relationship to the first-use route. That route presents runnable machinery before establishing enough vocabulary to explain it. Its early status/evidence language also receives more prominence than the mental model needed to read the tutorial.

P2-1 therefore calls for an introductory bridge and reading sequence, not a larger reference manual or prescribed redesign. P3-1 separately concerns the completeness of advanced explanatory evidence.

## 3. Risks and next action

**Review status: complete, not blocked.** Required HEAD remained unchanged. No files were written and no current peer review was read or requested.

Residual limitations are the absence of independent runtime reruns and visual/interactive browser checks. Existing qualification records support the bounded implemented route; they do not establish broader platform support.

The next action is a documentation-only correction pass addressing the two P2 findings, preferably also the excerpt-boundary P3, followed by focused review of the revised novice route and literal external-directory instructions. No compiler, dependency, consumer or release work is required by this verdict.