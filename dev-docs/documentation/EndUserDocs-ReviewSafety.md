[COMPLETE] 
# YIDL End-User Documentation — SAFETY-AXIS REVIEW

**Review object:** Delivered YIDL end-user documentation, examples and documentation tooling at `e98a22cc987342e1326384ee77cac6198b8bc647`; reviewed 2026-10-23.

**Baseline:** Documentation range `43dd01b04f012d6e5877b88e9442461c38447a37..e98a22cc987342e1326384ee77cac6198b8bc647`. Sources were read from the unchanged tracked checkout, with exact HEAD verified at the beginning and end. Compiler/runtime source and dependencies were reference-only.

**Date:** 2026-10-23

**Axis:** Safety and human end-user fitness, including the Surface mandate. Independent, adversarial, read-only. The other axis runs in parallel; nothing here relies on it. Filed verbatim by the lane owner.

**Verdict: NO-GO** — one P2 finding blocks acceptance; three P3 findings identify bounded first-use/interface defects. I pre-commit to GO on a revision that resolves P2-1 as specified, subject to checking the resulting reading route and absence of regressions.

---

## 0. Evidence base

The review began with the workspace and repository instructions, the complete assigned review prompt, and the required tuple checks. Initial HEAD matched the review object. Initial status contained only the two untracked review prompts.

Cold public reading preceded developer plans, inventory, implementation and verification evidence. The reading order began with:

- `docs/index.md:1–44`, root README and public navigation.
- `docs/start/first-generator.md:1–64`, followed through its installation prerequisite.
- `docs/start/install.md:1–67`, project layout and output inspection.
- The separately offered model/pipeline route.
- Extension through composition, extending-concepts and project layout.
- Debugging through debugging-assembly and the symptom index.

All authored current public prose under Start Here, Concepts, Guides, Reference, Examples, Troubleshooting and Contributing was inspected. Included example authorities inspected in full included:

- `example/documentation/classes.yidl:1–133`
- `example/documentation/generate.py:1–134`
- `captures.py`, `control_flow.py` and `comparison.py`
- `tests/data/gold_src/documentation_classes.py`
- All seven documentation model snapshots
- The imported-concepts and scope-path canonical fixtures

After cold inspection, the complete documentation plan and shortcomings inventory were read: `dev-docs/YidlDocumentationPlan.md:1–503` and `dev-docs/YidlDocShortcomings.md:1–795`. The activated brief, Inventory, Findings, Verification, ExampleEvidence and PythonMinimumCorrection records were inspected. Reference checks included the release-plan boundaries, coding rules, design-summary sections 26/26.1, legacy CLI argument declarations, example verification script, site hook, site checker and documentation workflow.

`git diff --stat` showed the delivered 63-file documentation change. The targeted name-only comparison for `src` and `pyproject.toml` returned no changes.

A fresh hidden browser tab was used only for the local preview. Actual rendered inspection covered home, the primary tutorial, the model diagram, composition, project layout and debugging. Search was exercised with keyboard input and returned matching documents; the model was discoverable through search. The diagram rendered, code blocks were readable, and the observed navigation and footer destinations matched the committed configuration. Preliminary field-setting observations were not treated as search failures; actual keyboard input established that search works.

No tests, builds, installs, examples, product commands, Git mutations or file/report writes were performed. Runtime success statements below refer to recorded evidence, not independently repeated execution. CLI help behavior was source-traced from argument declarations; product `--help` was not executed because the permitted-command boundary prohibited product execution.

Final HEAD remained `e98a22cc987342e1326384ee77cac6198b8bc647`. Final status contained the original review prompts and a lane-owner review checkpoint under `dev-docs/documentation/`; no tracked change appeared. The checkpoint contents and the other reviewer’s prompt/report were not read.

## Problem, requirement provenance, and scope

The original outcome is usable documentation for Python developers who do not know YIDL: install, understand its capabilities, author or extend a generator, inspect the products and diagnose failures without learning the compiler implementation or consumer history.

The operator subsequently made the learning requirement explicit: terminology must be introduced early, and an accessible general architecture overview must precede reliance on the large tutorial. This is direct task authority, not an editorial preference inferred from the plan. The plan independently requires short progressive tutorials and conceptual separation of definitions, fact records and generated user objects.

The observed problem is an ordering and explanation gap in the delivered beginner route. Useful conceptual material exists, but the primary route asks the newcomer to consume the complete generator before supplying that foundation. P2-1 records the concrete failure.

No dependency or infrastructure expansion is necessary to correct these findings. The recorded fresh-wheel route, explicit published Astichi dependency and explicit Python backend demonstrate an existing supported approach. The outside-checkout command error is in its public presentation, not evidence that isolation is impossible.

Authorized corrections are confined to YIDL public prose/navigation and narrowly necessary documentation examples/help. Compiler/runtime behavior, runtime metadata, generated product bases, Astichi, consumers and other projects remain reference-only. Existing model/pipeline content can be connected and clarified locally; no particular new page, diagram, framework or replacement tool is required.

Packaging metadata, legacy CLI disposition, unresolved nested scalar composition, broader backend/platform qualification and resource-wheel reproduction remain separately recorded limitations or follow-ups. They do not block this documentation outcome and do not authorize implementation work.

## 1. Findings

### [P2-1] The recommended beginner route requires the generator model before teaching it

**Location:** `docs/index.md:3–16,29–44`; `mkdocs.yml:63–75`; `docs/start/first-generator.md:20–51`; supporting alternative content at `docs/concepts/model.md:15–35` and `docs/concepts/generation-pipeline.md:3–17`.

**Violated invariant:** The operator explicitly requires early terminology and an accessible architecture overview before relying on a large tutorial. A Python reader must understand what they author, what the compiler generates, what facts describe, what assembly produces and what runs later before being asked to interpret the complete machinery.

**Cold reproduction:**

1. Open home. The opening description depends on “records,” “Astichi resources,” “assembly,” “bind,” “concept/DDS,” “stitching” and “hygiene.”
2. Follow the primary “Generate your first class” button. Its prerequisite is installation; neither the model nor pipeline is introduced as beginner preparation.
3. After installation, return to the tutorial. Before the full source, the reader receives a command, output filenames and a paragraph relying on schema, normalization, consumer policy and DDS.
4. The page then presents the complete 133-line declaration file. Its short explanation follows the file.
5. It presents the complete 134-line driver before the numbered stage explanation.
6. The ordinary footer route proceeds through project layout and inspection before reaching Definitions and facts. The tutorial’s explicit continuation goes to the more advanced data-flow guide.

**Concrete consequence:** A newcomer can reproduce the canned result but reaches the first authoring task without the conceptual basis for choosing between schema declarations, input facts, resource templates and production wiring. For example, the tutorial requires the reader to distinguish `FieldName`, `FieldRow(field_name="x")`, identifier binding and `Point(3,4)` while those relationships are only explained later or on an optional branch. That distinction determines whether a change belongs in the generator library, generation inputs or generated class.

The alternative model route is real and useful: it explicitly distinguishes `FieldRow` from `Point` and includes a rendered relationship diagram. It does not cure the primary route’s sequencing. Its compact definitions also depend on “generated value,” “composable,” “roots,” “bindings” and “DDS” without first translating those into the Python reader’s task. The pipeline table provides stage names and failures, but begins with those same abstractions.

**Required correction:** Establish a clearly recommended novice foundation before the complete tutorial source. Using existing pages or concise introductory material, explain:

- What kinds of Python-generation work YIDL supports.
- What the author supplies and what YIDL and Astichi respectively do.
- The difference between the generated schema/assembly library and generated application code.
- Where facts, selection, binding and assembly fit, using a small concrete example.
- Which steps happen during generator preparation, each generation and later execution.

Introduce the necessary vocabulary through those relationships. Preserve a direct quick route for experienced readers. No specific page or diagram is mandated.

**Closure/regression check:** Repeat a cold home-to-first-result walkthrough without developer notes. Before encountering either complete source file, a Python reader should be able to explain the two generated products, place a field-name input versus an instance value, identify Astichi’s role and select the correct authority for a simple extension. Check the primary button route, Start Here order and alternative conceptual route together.

### [P3-1] The outside-checkout instructions retain paths that cease to exist after the instructed directory change

**Location:** `docs/start/install.md:50–60`.

**Violated invariant:** A documented isolated first-use route must resolve its interpreter and script from the stated working directory.

**Reproduction:** Follow the text by copying `example/documentation/` to an otherwise empty directory and running from that copy. The displayed command still addresses `build/example-env/bin/python` and `example/documentation/generate.py` relative to that new directory. The copied example directory contains neither the installed environment nor that repository-relative script layout.

**Impact:** The advertised isolation step fails at path resolution before YIDL runs. The user must infer how to retain access to the original interpreter and address the copied script. This obscures the package-isolation claim with a setup error.

The recorded verification does establish a viable route: `verify_examples.py` passes `sys.executable` and a resolved copied script path. It does not execute the displayed public command.

**Required correction:** Provide a directory-consistent outside-checkout procedure that preserves access to the installed interpreter and addresses the copied `generate.py`. Use portable explanation or task-specific shell variables rather than committing machine-specific paths.

**Closure/regression check:** Follow the exact public steps in a fresh directory outside the checkout, with no sibling source or ambient Python-path assistance. Confirm the command reaches the expected Point observations and writes only its stated output directory. This review established the mismatch by source/path tracing; it did not execute that procedure.

### [P3-2] The tutorial command does not expose its option defaults

**Location:** `example/documentation/generate.py:110–115`; `docs/start/first-generator.md:58–64`; `docs/examples/index.md:8–22`.

**Violated invariant:** Under the Surface contract, each option must have a stated default and a usable cold description.

**Reproduction:** Inspect the parser declarations. `--out` defaults to `build/documentation`; the three scenario switches default to false. None has a help description or default-displaying formatter. The public prose describes scenario effects but does not state the output default. The shown commands instead use destinations such as `build/first`.

**Impact:** A reader running the script without `--out`, or using its help to discover the interface, cannot learn the default write destination from that interface. Scenario switches appear without explanatory summaries in generated help.

**Required correction:** State the output default and default scenario, and supply meaningful option descriptions through help or the adjacent public command reference. Explain that the destination is relative to the current working directory.

**Closure/regression check:** Inspect the resulting help and public command documentation cold. Every option’s effect and default must be identifiable without reading `main()`. A narrow help/interface check is sufficient; duplicate generator behavior tests are unnecessary.

### [P3-3] Installation and generated outputs have no documented cleanup lifecycle

**Location:** `docs/start/install.md:14–24`; `docs/start/first-generator.md:6–18`; `docs/start/inspect-output.md:1–18`.

**Violated invariant:** The Surface mandate requires the removal/undo half of an installation or creation lifecycle to be documented with the creation route.

**Reproduction:** Follow the first-day route through environment creation, installation and output generation, then look for how to undo that experiment. The route explains creation of the environment, wheel directory and generated Python files, but supplies no cleanup/removal guidance.

**Impact:** The beginner must guess which artifacts are disposable and whether removing generated modules or the example environment affects authored authority. This is especially relevant because the documentation correctly distinguishes several kinds of generated and authored files.

**Required correction:** Document the bounded cleanup operation for the tutorial environment and generated outputs, with clear ownership boundaries. Ordinary environment/directory removal is sufficient; no new YIDL uninstall or cleanup command is required.

**Closure/regression check:** From the first-use pages, identify how to remove the experiment while retaining authored `.yidl` and Python source. Check that cleanup guidance addresses only artifacts created by the documented route.

## 2. Invariant analysis

The following attacks did not establish additional findings:

- **Generated facts confused with user-instance values:** The model page, data-flow guide and inspection table explicitly distinguish them. The defect is when readers encounter that explanation, not a contrary semantic claim.
- **Literal binding confused with arbitrary captures:** Ownership and generated-value pages clearly reject arbitrary object serialization. The capture recipe uses independent namespaces and assertions concerning object identity and callback timing.
- **Editing the wrong authority:** Project layout, shared resources and the gallery identify authored resources as authority and generated bases as derived. They warn against repairing generated imports and explain coordinated field-policy removal.
- **Cache mistaken for live class/value state:** The cache table and pipeline distinguish unbound template caching, frozen facts, final AST, completed classes and runtime results. Broad thread/native recovery guarantees are expressly absent.
- **Successful flat composition presented as a repair of the original nested failure:** D17 remains unresolved throughout the public status and inventory. The comparison recipe is explicitly bounded.
- **Overbroad qualification:** Installation now states CPython 3.12+, while 3.12.12 remains reproduction evidence. New examples are qualified for the installed Python route; original cross-host/native results are not transferred to them.
- **Legacy command presented as the current compiler:** README, installation context and API reference direct users to the Python concept API. The legacy command’s different purpose is explicit.
- **Accidental release or deployment:** The documentation workflow has read permission and build/artifact operations, with no deployment job. Publication guidance preserves a separate authorization boundary.
- **Documentation acceptance used to demand dependency changes:** Findings and verification retain packaging and infrastructure limitations separately and provide the explicit installed-wheel alternative.
- **Control-flow/conditional-scope rule regression:** The delivered diff contains no C-style or Rust source changes requiring migration under those rules.

Recorded example execution and canonical snapshots support the bounded successful route. They do not establish that the presentation teaches a newcomer; that remains the acceptance issue in P2-1.

## Learning path and architecture/terminology analysis

The home page successfully shows a recognizable desired Python result before asking readers to study the implementation. The tutorial also names its two output files and eventually lists the generation stages. The data-flow guide makes owner, identity, ordering, storage spelling and runtime value distinctions concrete.

The difficulty is that the entry route gives priority to complete source and verification commentary over explanation of the system. Statements about canonical assertions, source authority and qualification are useful maintenance evidence, but do not answer the newcomer’s earlier questions about the generator’s parts and responsibilities.

The existing model page is a sound starting resource rather than something to discard. Its diagram renders, its fact-versus-instance example is useful, and it is available from the home route table, sidebar and search. It needs to participate explicitly in beginner preparation and explain its remaining prerequisite vocabulary.

For extension, the public composition route identifies naming conflicts and the imported-concepts example demonstrates compatible schema extension. More advanced method/resource specialization still assumes the vocabulary acquired from the large tutorial. That reinforces P2-1; it does not establish a separate compiler or inheritance defect.

For debugging, the public guide supplies useful layer distinctions and warns that a target error can wrap a binding collision. A Python reader can find named attributes and reference material, but the guide is principally a checklist rather than a worked first failure. That is a residual learning limitation below a separate finding here; correcting the foundational route should be assessed before prescribing more diagnostic scaffolding.

## Surface walkthrough

**Purpose and entry:** Home shows generated Point code and offers an obvious first-result button. The “Start Here” sidebar begins with installation. Both are navigable, but neither puts the conceptual foundation before the complete tutorial.

**Install:** The fresh-environment route explicitly installs Astichi and selects the Python backend. Import-origin and actual-engine checks are supplied. The outside-checkout command has the path mismatch in P3-1.

**Use once:** The in-checkout tutorial command, output filenames and expected Point behavior are stated. Successful execution is supported by the recorded installed-package evidence, not rerun here.

**Options/help:** The tutorial parser’s effects and defaults were inspected without executing product code. Missing public defaults/help descriptions are P3-2. No new concept CLI, trace flag or universal write flag is invented by the documentation.

**Extend:** The rendered composition page links to the split-source example; those links were followed. The full example and its ownership explanation are present. Concept and matcher terminology are assumed, making the foundational ordering material.

**Diagnose:** The rendered debugging page and symptom route are discoverable. The guidance correctly separates binding, identity and target failures and preserves exception causes.

**Undo/remove:** The first-use route provides no corresponding cleanup guidance, as recorded in P3-3.

**Rendered presentation:** Home, tutorial code and the model diagram were visually inspected. Search returned results after actual keyboard input. No broken-link or search defect was reproduced. Narrow-screen behavior and every external destination were not independently exercised.

## 3. Risks and next action

The review is **complete**, not blocked. It is a read-only acceptance assessment of the specified revision.

The material has substantial correct foundations and an evidenced standalone route. Acceptance is blocked by the direct novice-first requirement, not by missing compiler capability, a demanded dependency repair or a prescribed documentation format.

The next action is a localized documentation remediation pass addressing P2-1, with the bounded path, defaults and cleanup corrections alongside it, followed by a fresh cold-reader check of the resulting public route. No broader runtime, packaging, dependency, consumer or release changes are implied.