# YIDL user documentation and website plan

Date: 2026-10-12. Status: detailed documentation plan; page content, examples,
site configuration and publication have not been implemented by this task.

## 1. Objective and boundary

Produce a coherent user documentation set for the current YIDL language and
supported YIDL/Astichi generation route. A reader should be able to build a small
generator, inspect its output, extend it and diagnose assembly failures without
reading the Dataclass experiment transcript or compiler implementation.

The user supplied
[SDAX Hamilton](https://owebeeone.github.io/sdax-hamilton/): user Markdown docs
rendered as an HTML site with navigation, search, readable code and GitHub Pages
publication, as an example of the desired website delivery. This is not a
requirement to mimic its content, navigation or visual design. The reference
site's local `mkdocs.yml`, user pages, documentation
requirements and Pages workflow were inspected; its live homepage returned HTTP
200 and uses the Material theme. Its domain-specific API/content is not a YIDL
template.

**This task creates this plan only.** The existing
[shortcomings inventory](YidlDocShortcomings.md) remains unchanged. Dataclass
work, its agents and all compiler/runtime code remain untouched. No configuration,
example, test, workflow, Git commit, push or publication is performed here.

The proposed subsequent work is confined to YIDL user docs, runnable documentation
examples, their verification harness, documentation dependencies/configuration,
documentation CI and associated planning/evidence. It requires its own activation
and scoped brief. Astichi, Lifecycle, Undoable, Dataclass and SDAX Hamilton are
reference-only dependencies/projects. A documentation plan does not authorize
implementation changes in them or in YIDL's compiler. Discoveries that require
such changes must be filed separately, with evidence and demonstrated impact.

## 2. Audience, starting points and success criteria

| Reader | What they must be able to do |
| --- | --- |
| New generator author | Install a qualified environment and generate a real plain Python class from a small YIDL concept |
| Author extending a generator | Compose concepts/resources, specialize matchers and wire ordered contributions without guessing inheritance or binding behavior |
| Author debugging a failure | Identify whether the failure is syntax, facts, matcher selection, addressing, binding, materialization or generated behavior |
| Experienced Astichi user | Understand the YIDL fact/matcher/assembly layer and find exact bridges to the supported stitching surfaces |
| Maintainer or another LLM | Locate the supported contract, copy executable recipes and recognize unsupported or experimental features |

Acceptance requires all of the following:

- One complete, independently executed quick start from public docs alone.
- A visible current-language route, separated from older transducer/frontend
  material and Lifecycle consumer architecture.
- Every D01–D28 and A01–A10 inventory item assigned to pages and verification.
- Recipes that connect desired Python, input facts, YIDL declarations, bindings,
  targets and actual generated output.
- Explicit matching/data-extraction cases from section 5.3, including multiple
  sources, property ownership, evaluated values and parameter assembly.
- Relevant standalone recipes paired with qualified Dataclass, Lifecycle or
  Undoable excerpts under section 5.4, without making those projects prerequisites.
- Qualified SDK/Python/backend versions, plus explicit unsupported boundaries.
- A strictly built, navigable HTML artifact with checked internal links/anchors,
  working search, readable code and correctly resolved project-site paths.
- Publication instructions and a reviewed Pages workflow; publication itself is
  a separately authorized action after the site is reviewable.

No example count, successful build or review verdict is a substitute for those
outcomes. A page describing an unresolved mechanism must not present an
experimental workaround as an established general contract.

## 3. Website model

### 3.1 Tooling and source ownership

Use **MkDocs with Material** as the proposed implementation, supported by the
reference site's mechanism rather than mandated by its appearance. Authored
user pages live under `docs/`. `dev-docs/` remains the home of plans, findings,
historical reviews and internal design work; it is not the public navigation tree.
User docs may cite specific stable developer references when appropriate, but
must explain the usable contract without requiring those references.

Planned infrastructure files:

| File or directory | Purpose |
| --- | --- |
| `mkdocs.yml` | Site identity, explicit navigation, extensions, theme and inclusion rules |
| `docs-requirements.txt` or equivalent dedicated docs lock | Documentation tools isolated from runtime dependencies; resolved versions recorded for reproducible builds |
| `.github/workflows/docs.yml` | Pull-request validation and an authorized default-branch Pages deployment path |
| `docs/index.md` | Public homepage and clear next steps |
| `docs/start/`, `concepts/`, `guides/`, `reference/`, `examples/`, `troubleshooting/`, `contributing/` | Public page groups described below |
| `examples/documentation/` | Self-contained runnable example projects; final placement must respect the existing canonical harness |
| `tests/` documentation verification additions | Existing-harness integration and narrow link/diagnostic checks, rather than another duplicated success suite |

Use one authored source for each contract/example. Mechanically include or extract
example code and generated output where practical. Do not maintain an untested
Markdown version beside a divergent executable version.

### 3.2 Proposed presentation capabilities

- Material light/dark palettes, section navigation and a page table of contents.
- Search suggestions/highlighting, heading permalinks and copyable code blocks.
- Homepage buttons for Quick Start, Concepts and Reference.
- Short introductions explaining reader outcome and supported status.
- Explicit compatibility/current-version information near installation and APIs.
- Previous/next navigation, repository/edit links and a clear contributing route.
- Optional collapsible diagnostics and tabs for source/generated output or backend
  variants when they make comparison easier; not required for every snippet.

Navigation tracking/instant navigation can follow the reference configuration
after HTML checks. SDAX Hamilton is a hosting/build example; YIDL's content,
navigation and appearance follow its own readers' needs. Do not copy project
metadata, license, dependency versions or API assumptions. Determine YIDL's repository URL, Pages
base path and licensing from its own repository before configuring them.

### 3.3 Information architecture

Keep the top-level choices task-oriented:

1. Home
2. Start Here
3. Concepts
4. Guides and Recipes
5. Reference
6. Examples
7. Troubleshooting
8. Contributing

The homepage explains which section to choose; it does not require a reader to
understand DDS before seeing a useful generated class. Reference pages provide
precise contracts; guides explain how to apply them. Tutorials stay short and
progressive. Troubleshooting starts from observed symptoms.

## 4. Page specifications

Each row defines what a document will contain, not its finished prose. Proposed
paths are relative to YIDL's repository root. Headings and paths should stabilize
before multi-author work to avoid link churn.

### 4.1 Home and Start Here

| Page | Required contents | Required example/evidence | Inventory |
| --- | --- | --- | --- |
| `docs/index.md` — YIDL | What YIDL generates, intended authors, its relationship to Astichi, current support/status, one small input/output preview and routes into tutorials/reference; distinguish generic language from consumer field policies | Preview comes from the tested quick start, not independently maintained code | D01, D02, D06, D25 |
| `docs/start/install.md` — Installation and supported environment | Qualified Python/YIDL/Astichi tuple, installation source and dependencies, fresh environment, import/version checks, backend selection versus fallback, and release versus development docs | Independently installed qualified packages; no sibling/editable import leakage; verify release availability before giving package commands | D23, D26, D27 |
| `docs/start/first-generator.md` — Generate your first class | A complete non-Lifecycle concept, properties/record/collection, resources and wiring; compile concept, emit runtime, populate facts, freeze, run assembly and execute generated AST | A plain two-field slotted class; source filenames, commands and expected behavior; explain every generated stage | D01–D06, D21 |
| `docs/start/project-layout.md` — Split and regenerate a project | Logical source-map keys, module/import/export names, two-file layout, package resources, generated-base authority, check/write regeneration and clean rerun | The quick start split into base and extension; missing import/export and stale-base cases | D12, D13, D20, A09 |
| `docs/start/inspect-output.md` — Inspect and check generated code | Authored bindings, runtime base, model source, final AST and execution; readable output versus behavioral truth; supported inspection entrypoints | Trace the quick start into its actual generated constructor and direct slots | D02, D22, D28 |

### 4.2 Concepts

| Page | Required contents | Required example/evidence | Inventory |
| --- | --- | --- | --- |
| `docs/concepts/model.md` — Definitions, facts and instances | Vocabulary for concept, property, record, collection, resource, matcher, contribution, production and assembly; distinguish generated fact classes from generated user classes; definition/build/runtime phases | Diagram annotated with real quick-start objects and their owners | D01–D04, A04 |
| `docs/concepts/generation-pipeline.md` — From declarations to Python | Parsing, normalization, fact production, matching, build graph, binding, materialization, final compilation and execution; where errors and caching occur | Ordered trace of one successful class and one failed binding; no invented trace command | D02, D22, D24–D27 |
| `docs/concepts/surfaces-and-shapes.md` — Resources and insertion surfaces | Statement suites, scalar expressions, parameters, arguments and tuple elements; resources versus build instances; empty source versus no match versus pass | Tested zero/one/multiple contribution table and resulting Python/AST shape | D05, D11, D15, D19, A07 |
| `docs/concepts/composition.md` — Inheritance and specialization | What each declaration category inherits/merges/reuses; named conflict rules; matcher defaults/rules/weights; shared resources and consumer adapters | Base plus extension with one intentional production/default conflict and corrected specialization | D13–D15, A01, A09 |
| `docs/concepts/binding-and-ownership.md` — Names, values and build state | Identifier versus path/literal binding, lexical scopes/hygiene, runtime captures, frozen data versus composable/build state, cache and failure ownership | Scope/capture diagram and two independent class generations with different defaults | D07–D10, D23, D24, A02, A08 |

### 4.3 Guides and recipes

| Page | Required contents | Required example/evidence | Inventory |
| --- | --- | --- | --- |
| `docs/guides/classes-and-methods.md` | Building plain class shells, slots, methods, properties, decorators and conditional omission; direct accesses and namespace/capture installation | Plain class plus specialized getter/setter; zero-field and disabled-method variants | D05, D06, D10, D11, D23, A07 |
| `docs/guides/constructors-and-calls.md` | Required/defaulted/factory parameters, keyword-only partition, annotation captures, constructor body stores and call arguments; factory policy belongs to the consumer | Signature and emitted body for a constructor, plus a named-call argument recipe with positional/keyword forms | D06, D08–D11, A06 |
| `docs/guides/expressions-and-order.md` | Tuple operands, ordered expression contributions, nested reads, short-circuit behavior, equality raw results and evaluation order; explain supported alternatives | Tuple comparison plus three-operand short-circuit case with non-bool result/getter trace; original nested pattern remains separately classified | D05, D16–D19 |
| `docs/guides/scopes-and-targets.md` | Local/outer names, keep/import/export/pass, identifier demands, reference paths, transparent Store/AugStore/Delete targets and failed binding diagnosis | Constructor parameter rewrite and nested attribute assignment/deletion; one Load-as-target failure | D07–D10, D16, A08 |
| `docs/guides/extending-concepts.md` | Extend resources/matchers without duplicating inherited production/default names; weighting and unique build identities; distinguish reuse from replacement | Two independent consumers of a neutral comparison concept; the second changes read paths and has no dataclass metadata | D13–D15, D21, A01, A09 |
| `docs/guides/fact-production.md` | Schema-only DDS, concrete/computed sources, operations and production phases, callable analysis facts and matcher snapshots; consumer normalization versus generic DDS | A small operation creates facts later consumed by assembly; explicit write policy and unavailable-provider example | D04, D16, A04–A06 |
| `docs/guides/matching-and-data-flow.md` | Stepwise property selection from one/multiple inputs, combinations versus keyed lookup, filters/rules, matched records/evaluated values, scope/ambiguity and projection into identifiers, bindings and constructor/call parameters | All section 5.3 cases and a complete two-collection flow from input rows to emitted parameters; annotated qualified consumer excerpt | D04, D14, D16, D22, A01–A06 |
| `docs/guides/shared-resources.md` | Packaged authoritative resources, logical import paths, digests, source maps, checked-in emitted bases, build-time reuse versus runtime dependencies | Minimal packaged two-consumer regeneration and missing authority failure; actual Undoable work is not a prerequisite | D12, D20, D23, D24, A09 |
| `docs/guides/debugging-assembly.md` | Narrow a failure; inspect facts, selected contribution, identity/index, evaluated target and remaining demands; trace causes through layers; choose supported alternatives before alleging a compiler defect | An unbound path, duplicate build name and missing target worked through with actual supported inspection | D15–D17, D20–D22, D26, D28 |

### 4.4 Reference

| Page | Required contents | Required evidence | Inventory |
| --- | --- | --- | --- |
| `docs/reference/language.md` — Language syntax | Exact current grammar for modules/imports/exports, properties, records, collections, resources, matchers, contributions, productions and assemblies; delimiters, expressions and constraints | Parser-backed smallest positive/negative cases for each surface; separate older transducer syntax | D03, D12–D14, D21, A07 |
| `docs/reference/data-model.md` — DDS and containers | Property semantic/storage names, generated constructors/types/defaults, concrete/union records, identities/cardinality, computed views, ordered queries, ports and write policies | Qualified runtime/generated schema examples and duplicate/cardinality diagnostics | D04, D16, A04, A05 |
| `docs/reference/matchers.md` — Matcher contracts | Generic versus contribution matchers; input tuple/context, property qualification and visible-name conflicts, evaluated fields, rule names/conditions/scores/defaults/ties, original records versus extracted tuple values, inheritance and snapshots | Source-derived contracts plus the section 5.3 matrix, including overlapping/default/no-match and multi-input cases | D14, D16, A01, A04 |
| `docs/reference/assembly.md` — Contributions and builds | Resources versus production sources, as/index/order/target, root mappings and paths, bindings, contextual records, nested assembly, empty suppression, diagnostic contributions and exported entrypoints | A shape/address compatibility table and captured error reproductions | D05, D11, D15–D17, D21, D22, A02, A08 |
| `docs/reference/generated-values.md` — Resource values | Public wrapper factories and accepted domains; literals/imports/code/templates, nested template edges, compile/cache timing, evaluated values and invalid objects | Verified constructor/signature/domain tables; source-emission and composable-consumption examples | D05, D23, D24, A02, A03 |
| `docs/reference/astichi-bridge.md` — Stitching boundary | YIDL-facing contract for holes, identifiers, literals, reference paths, scopes and target contexts; maps to Astichi-owned marker reference; SDK/backend limits | Tested marker-position table and cross-links to Astichi, avoiding divergent copies of its full reference | D05, D07–D10, D19, D25–D27, A07, A08 |
| `docs/reference/apis-and-cli.md` — Supported API entrypoints | Concept parsing/compilation, runtime emission, builder/assembly/AST execution and the actual CLI; distinguish current concept generation from legacy frontend routes | Public signatures and subprocess/help walkthroughs; do not teach `yidl-compile` as a concept compiler without proof | D02, D21, D22, D26 |
| `docs/reference/compatibility.md` — Versions and supported behavior | Qualified Python/SDK/backend matrix, feature status, known unsupported arrangements, observed limitations versus defects, legacy/material migration notes and consumer boundaries | Every supported cell linked to executed evidence; absent cells labeled unqualified | D17, D19, D23–D27, A06–A09 |
| `docs/reference/caching-and-performance.md` | Template, executable code, class/value caches distinguished; ownership/invalidation; cold/repeated generation versus hot access and memory; what native selection does and does not imply | Small isolated capture/cache cases; measurements only if actually run; no hypothetical speed claims | D24–D27, A08 |

### 4.5 Examples, troubleshooting and contribution

| Page | Required contents | Required evidence | Inventory |
| --- | --- | --- | --- |
| `docs/examples/index.md` — Runnable examples | Catalog ordered from minimal to composed examples; purpose, prerequisites, run command, qualified tuple and generated-output link for each | All catalog entries execute independently and have explicit expected outcomes | D01–D06, D12, D21, D27, D28 |
| `docs/examples/generated-gallery.md` | Rich contrasting fields/classes, declaration-to-output views, factory and specialized accessor wiring, deletion example; identify inspection versus independent oracle roles | Canonical sources and mechanically produced readable goldens with behavior checks before refresh | D06–D10, D18, D23, D28, A06, A10 |
| `docs/troubleshooting/index.md` | Symptom index for syntax error, inherited symbol/default conflict, duplicate instance, missing assembly export, unresolved hole/bind/target, native finalization, AST context and surviving marker/runtime mismatch | Each entry points to the smallest reproduced case, cause/status, remedy and corresponding reference | D03, D08, D09, D11, D13–D22, D27 |
| `docs/contributing/documentation.md` | Page ownership, evidence requirements, recipe/golden harness, source inclusion, compatibility qualification, terminology, link/style checks and handling unsupported findings | A documented contributor can add one verified recipe without modifying compiler code | D22, D26, D28, A10 |
| `docs/contributing/site-publication.md` | Local HTML preview/build, CI boundaries, Pages settings/base path, authorized publication, rollback of a bad site artifact, release/development labeling and ownership | Clean strict build/artifact check; controlled deployment walkthrough after authorization | D12, D20, D26, D27, A09 |

## 5. Example and evidence design

### 5.1 Required example projects

These are intentions and expected outcomes, not finished source code:

| Example | Shape and outcome |
| --- | --- |
| First class | Two plain fields, generated slots/constructor, real instance behavior and inspectable direct stores |
| Split project | Base plus imported extension; stable logical source names; regenerated base matches authority |
| Surface shapes | Zero/one/several statements, parameters, keyword-only parameters, tuple elements and scalar expressions, with actual output |
| Bound names | Identifier parameter/annotation, nested path read, opaque capture and outer lexical reference, all distinguished |
| Target contexts | Ordinary and transparent assignment, augmented assignment and deletion; preserve a Load-context negative case |
| Empty facilities | Zero fields, no constructor, disabled methods and suppression; distinguish empty source from pass |
| Inherited specialization | Base matcher default, child weighted rule, conflicting default/production and unique reusable contributions |
| Ordered operands | Two owners with repeated field names; reordered facts; explicit owner/index/order and stable output |
| Nested composition investigation | Small original failed chain isolated from Dataclass; correct cause or explicit limitation established before publishing a recipe |
| Short-circuit semantics | Falsey non-bool result, final raw result, shared/nonreflexive operands and observable getter/callback order |
| Produced facts | An operation derives callable/argument facts; later assembly reads a qualified snapshot |
| Matching and parameter flow | Two collections and several properties; related-row filtering, rule selection, named record/evaluated-value projection and emitted constructor/call parameters; section 5.3 specifies the individual cases |
| Independent captures | Same template reused for two classes with different names/defaults/callbacks; no hostile repr or generation callback execution |
| Shared authority | Two minimal consumers import one packaged resource; source digest change/missing source causes precise regeneration failure |
| Rich field gallery | Several contrasting fields and multiple classes; remove a field and its local policy; diagnose a remaining legitimate dependency |

Reuse existing canonical success coverage where its inputs and ownership fit;
do not reproduce the same successful assertions in another bespoke suite. Narrow
tests own invalid syntax, diagnostics, unsupported shapes and recognition.
Documentation examples must be small enough to explain individually. A large
consumer fixture can supplement a tutorial but cannot substitute for a minimal
recipe.

### 5.2 Qualification contract

Each runnable example records:

- Purpose and whether it describes supported, experimental or unsupported behavior.
- Source authority, entry file and logical import/source map.
- Required packages, exact qualified versions and Python patches/backends.
- Run command, expected output/behavior and generated artifact location.
- How the behavioral expectation was independently established.
- Relevant negative case and verified diagnostic/remedy when applicable.

Use fresh installed environments for public usability and package-boundary claims.
Do not rely on an unrelated neighboring project, a warm imported template or
unpublished SDK modifications. Test both relevant backends/minors before calling
a recipe generally supported; otherwise state the narrower qualification.

When a page needs output, prefer extraction from the example/golden authority to
manual copy. Define stable extraction markers and verify drift. A test that merely
asserts the documentation repeats the generated output is not semantic evidence.

### 5.3 Matching, property extraction and parameter granularity

This matrix is required coverage, not an optional interpretation of a broad
"multi-input matching" heading. Use "property" for a declared value on a record
and "collection" for a record source. Explain a row/column analogy where useful,
without implying SQL-style matching or automatic joins.

| Case | What the explanation and executable example must establish |
| --- | --- |
| M01 — one input, one/several properties | Which collection/record supplies each value; semantic property versus generated storage name; selecting a subset without confusing property order with parameter order |
| M02 — multiple inputs | Input alias and tuple order, combinations considered, empty input behavior and a condition that relates rows by owner/key; do not describe combinations as a keyed join |
| M03 — computed sources and lookup | Filtered/computed views versus keyed lookup; scalar/composite identity keys, missing key/default behavior and when lookup is preferable to enumerating combinations |
| M04 — property ownership and ambiguity | Two inputs with different and overlapping property names; supported explicit property references; contribution-language duplicate-visible-name diagnostics; distinguish the DDS Python API from YIDL syntax and do not invent qualified syntax |
| M05 — conditions and selection | One condition, combined conditions, broad/narrow rules, weights, defaults, no match and equal-score ambiguity; explain generic and contribution matcher differences |
| M06 — evaluated fields | Derive one match value from properties on several records, evaluated-field input order/type and the emission contract for callable evaluators; distinguish derived values from original stored properties |
| M07 — result projection | Retrieve a named original matched input's property versus a positional extracted/evaluated tuple value; record the tuple schema and out-of-range/missing-input diagnostics |
| M08 — context and scope | Current input values versus enclosing production context, nested lookup/visibility and owner filters; unavailable values, shadowing or collisions must be explained by the actual supported contract |
| M09 — parameters and bindings | Follow selected values into identifier/path/literal bindings, annotation/default/factory captures and positional/keyword/keyword-only parameters or arguments; declaration, match and emitted parameter order are separate |
| M10 — output identity and order | Keep record identity, target owner, contribution build name, index, order and target address distinct; show repeated field names in different owners and a deliberate duplicate target |

The worked example for `matching-and-data-flow.md` should use small class/field
collections with at least two owners and several contrasting properties. Show
the source records, candidate combinations or lookup, relationship filter,
selected rule/result, extracted values, resolved contribution bindings and final
generated Python parameters/body. Include one unrelated record filtered out and
one failed property/parameter reference. Use observable values so the reader can
track a value through the entire pipeline.

Starting implementation evidence to audit and adapt, all in YIDL:

- `tests/data/gold_src/yidl_update_a_multi_source_from.py`: assembly over two
  sources, owner relationship, selected contribution and generated output.
- `tests/generation/test_matcher.py`: multi-input evaluated fields, tuple-based
  resolution and rule/default behavior.
- `tests/generation/test_data_matcher_productions.py`: named matched-record reads
  and extracted tuple index diagnostics.
- `tests/data/gold_src/dds_composite_identity_lookup.py`: composite identity
  lookup and projection into produced records.
- `tests/generation/test_yidl_lark_update_a_diagnostics.py`: duplicate visible
  values and unknown contribution value diagnostics.

These inspected sources/tests establish concrete documentation starting points;
they were not rerun by this planning amendment. Documentation authors must
qualify the selected examples and their actual public route. A Python API feature
must not be advertised as available YIDL syntax merely because both are in YIDL.

### 5.4 Standalone recipes paired with real consumer snippets

Relevant guide pages should contain a compact **Used in practice** excerpt after
the smallest standalone explanation. The excerpt should make the same mechanism
recognizable in a real project, not replace the standalone example with a large
consumer implementation or turn this into three consumer API manuals.

| Consumer | Suitable excerpts | Primary page owners |
| --- | --- | --- |
| YIDL Dataclass | Constructor parameter assembly, field-local comparison selection, annotation/callback captures and direct generated field reads | Constructors/calls, matching/data flow, expressions/order and generated gallery |
| YIDL Lifecycle | Dependent-factory argument assembly, matching field policies to specialized accessors and ordered initialization contributions | Fact production, classes/methods, scopes/targets and matching/data flow |
| YIDL Undoable | Selection of transactional access/guard resources and history-aware reads; neutral comparison reuse only after the relevant integration is qualified | Classes/methods, extending concepts, shared resources and generated gallery |

Each excerpt must show or clearly link the complete chain:

1. The consumer requirement and the relevant declarations/input facts.
2. The selected matcher/rule and why it is selected.
3. The original-record/property or evaluated value that supplies each input.
4. Identifier/external bindings, parameters/arguments and destination/order.
5. The authored YIDL/Astichi fragment and the actual generated Python.
6. The resulting behavior and its qualified verification.

Reference the owning repository, stable path and exact revision or release, with
a navigable source link. Preserve attribution/licensing. Prefer mechanically
extracted authoritative snippets with drift checks; if a snippet is simplified,
label it adapted and give it its own executable qualification. Never imply that
a fragment copied from a live working tree is a stable supported contract.

Keep the consumer projects reference-only: read committed examples/resources or
qualified artifacts without editing them, regenerating their bases, changing
their agents or waiting for their full projects to finish. Dataclass excerpts
must wait only for the specific feature/revision they illustrate to be verified;
until then use the standalone recipe or an explicitly labeled planned excerpt.
Undoable's future comparison integration is not required to explain its existing
transaction guards. Consumer semantics are explained briefly as context, while
the generic YIDL mechanism remains the page's subject.

Qualification records include consumer/SDK versions, actual source/extraction
boundaries, facts/bindings and generated output, expected behavior and the check
that supports it. The gallery must not promote unaccepted experimental remedies
or let passing simple values substitute for callback/scope correctness.

## 6. Inventory closure matrix

This is the minimum coverage assignment. Page groups can cover several entries,
but every ID needs a disposition and executable evidence or an explicit
investigation/unsupported status.

| IDs | Lead pages/work packet | Closure obligation |
| --- | --- | --- |
| D01, D02, D06 | Home, first generator, model, pipeline | One readable end-to-end route; distinguish definitions/facts/models and show desired/generated Python |
| D03, D04 | Language, data model, first generator | Correct grammar and semantic/storage names; smallest rejected counterparts |
| D05, D11 | Surfaces/shapes, constructors, assembly | Zero/one/many compatibility matrix; explicit empty/suppressed behavior |
| D07, D08, D09, D10 | Scopes/targets, constructors, Astichi bridge | Name/attribute/annotation/capture separation; lexical and target-context recipes |
| D12 | Project layout, shared resources | Qualified virtual imports and packaged regeneration without cwd dependence |
| D13, D14, D15 | Composition, extending concepts, matchers | Production/default conflicts and resource-versus-instance identity explained with corrected cases |
| D16, D17 | Assembly, ordered operands, debugging | Addressing/index/order facts; original nested failure classified rather than silently replaced |
| D18, D19 | Expressions/order, surfaces, compatibility | Raw callback/short-circuit semantics and backend-qualified expression carriers |
| D20, D21, D22 | Project layout, API/CLI, troubleshooting | Regeneration/exports and symptom-to-fact/resource/target diagnostic path |
| D23, D24 | Binding/ownership, generated values, caching | Captures, accepted binding domains, independent builds/cache lifetime verified |
| D25, D26, D27 | Pipeline, compatibility, caching/performance | Generation/hot-access separation, parsing-policy applicability, actual backend/version evidence |
| D28 | Generated gallery, documentation contribution | Readable canonical output plus independent behavior; failures/refresh procedure preserved |
| A01, A02, A03 | Matchers, matching/data flow, assembly, generated values | Section 5.3 input/property/result granularity, weights/snapshots, nested edge environments and wrapper/import/literal contract |
| A04, A05, A06 | Fact production, matching/data flow, data model, constructors | Section 5.3 combinations/lookup/projection/parameters, phase/write/snapshot/cardinality and consumer dependency boundaries |
| A07, A08 | Classes/methods, surfaces, Astichi bridge, ownership | Qualified compound constructs and deferred/copy/materialization/failure contract |
| A09, A10 | Shared resources, project layout, gallery | Authority/dependency reproducibility and local policy removal versus remaining references |

Do not mark an item closed by creating its heading. Preserve the original symptom,
locate existing documentation, explain the missing bridge and record verification.
An anticipated item may close with a clear supported contract and example; it
does not need a manufactured historical failure.

## 7. Execution order and future author work packets

No agents are dispatched by this plan. The following packets are proposed for a
later authorized documentation run. Each writer owns named pages/examples; shared
glossary/navigation changes have one coordinator to prevent overlapping edits.

| Stage | Work and deliverable | Dependency and gate |
| --- | --- | --- |
| P0 — qualify the brief | Audit existing docs, current language/API routes, version/backend tuple, installation and legacy CLI; assign each inventory ID; freeze terminology and page paths | No broad compiler prerequisite; reproduce supported route first; unresolved contracts recorded separately |
| P1 — reader entry and site shell | Home/Start Here drafts, explicit navigation and docs-only Material build skeleton | Quick start executes; missing placeholders must not be advertised as completed docs |
| P2 — binding and shape foundations | Concepts plus syntax/data model/scopes/constructor/shape recipes | Tested zero/one/many and negative cases; records/resources/methods distinguished |
| P3 — composition and debugging | Inheritance/matcher/addressing pages, section 5.3 matching/data-flow matrix, expression/control-flow recipes and troubleshooting | Original conflicts and nested pattern disposition; complete two-source parameter flow and semantic/backend checks before publishing alternatives |
| P4 — advanced data/resource ownership | Operations/snapshots/generated values, captures/caching/shared packaging and compatibility | Public contracts backed by examples; no silent migration of consumer policies into DDS |
| P5 — assembled reader/site verification | Gallery and qualified section 5.4 consumer excerpts; contributor/publication pages; migrate obsolete public material; strict HTML/links and public-doc-only walkthrough | All inventory IDs and M01–M10 have dispositions; excerpt provenance/drift checked; no consumer edits or unpublished SDK dependence |
| P6 — review and publication readiness | Settled documentation/example/site artifact review, corrections and reproducible publishing instructions | Independent content/authoring and evidence/site checks; deploy only after publication authorization |

Suggested author packets after P0:

- **Reader entry:** Home, Start Here and the shared vocabulary; owns the smallest
  complete example and installation qualification.
- **Bindings and surfaces:** shape/reference/target recipes and their negative
  examples; owns the compatibility table and lexical diagrams.
- **Composition:** inheritance/matchers/addressing and neutral reuse; owns rule
  conflict, ordered operands and M01–M10 data-flow coverage with Data and ownership.
- **Data and ownership:** DDS operations/generated values/captures/caches and
  package boundaries; owns advanced contract qualification.
- **Diagnostics:** symptom lookup and inspection walkthroughs, coordinated with
  the packet that owns each remedy rather than rewriting its contract.
- **Consumer excerpt curation:** coordinate read-only, qualified Dataclass,
  Lifecycle and Undoable snippets with the relevant guide owners; own provenance,
  extraction/drift checks and the link from real use back to standalone recipes.
- **Site integration:** navigation, source inclusion, HTML/link/accessibility
  checks and Pages workflow; owns infrastructure only, not compiler changes.

Pages that depend on an unresolved contract wait for a qualified disposition;
independent foundation pages can continue. Plans and earlier reviews never expand
the component scope. If a reproduction finds an actual compiler defect, file a
separate issue/proposal and retain a documented supported alternative where one
exists. Do not turn optional cleanup into a documentation prerequisite.

## 8. GitHub Pages build and publication plan

### 8.1 Local and CI build

Follow the reference's docs-only dependency separation and Material build model.
The later implementation should provide a documented local preview and strict
HTML build into a disposable output directory. Runtime examples install their
own qualified dependencies separately from the site builder.

Pull-request checks should:

1. Verify extracted snippets/output are current and execute affected canonical
   examples plus their narrow negative checks.
2. Build the site strictly with every promised navigation page present.
3. Check internal links, anchors, assets and project-base-path URLs. Treat external
   URL availability separately so transient outages do not rewrite contracts.
4. Check for leaked machine paths, credentials and accidental developer/validation
   artifact publication.
5. Retain an inspectable site artifact/preview without publishing the PR.

`mkdocs build --strict` is one gate, not a claim to verify every external link,
anchor, runnable snippet or website behavior. The implementation must identify
the additional checks actually used.

### 8.2 Public source selection

Existing `docs/` includes design documents and validation Python/artifacts. Before
publication, classify each existing page as current user reference, historical
design, internal validation or migration candidate. Preserve originals and
authority; do not delete/relocate material as incidental cleanup.

Use an explicit public inclusion strategy that excludes validation code/logs and
internal evidence from the output, not merely from the navigation. Verify the
resulting artifact manifest. If build-tool exclusion features are used, test their
actual behavior for Markdown and static assets. Any proposed move of canonical
material must be separately reviewed for link/authority consequences.

### 8.3 Authorized deployment

Prepare a workflow patterned after SDAX Hamilton: pull requests build only;
authorized default-branch runs upload the site artifact; a separate Pages job
uses the Pages environment and the required scoped token permissions. Serialize
deployments and avoid cancelling an in-flight publish. Pin/verify action versions
when implementing; do not blindly copy reference hashes as a timeless requirement.

Before the first deployment, verify repository URL/visibility, Pages eligibility,
Actions configuration, site base path, environment controls and required access.
Publication settings and a public site must not be changed merely because this
plan exists. The future authorized run should retain the deployed revision,
artifact identity and live smoke results, and document how to restore a prior
known-good documentation artifact if a deployment is bad.

A branch/development status banner is required initially. Do not describe `main`
docs as a supported release contract unless they match a qualified release. Start
with one coherent qualified site; add multi-version hosting only when actual
release/support needs justify it, rather than as an initial prerequisite.

## 9. Documentation review and acceptance

Reviewers assess two complementary concerns on the same settled revision:

- **Content and authoring:** read public entry docs cold, follow the quick start
  and an extension/debugging task without private design notes, check vocabulary,
  navigation, exact contracts, all inventory assignments and M01–M10. Follow
  properties from different input records into generated parameters; check that
  real consumer excerpts explain rather than obscure the generic mechanism.
- **Evidence and website:** audit examples/diagnostics/version/backend claims,
  source/output ownership, unresolved classifications, package isolation, HTML
  artifact selection, links/search/base paths and deployment boundaries.

Requirement provenance and authorized scope are checked on both concerns. A
reference project's deployment mechanism or a reviewer preference does not
authorize new compiler work. Preserve findings and specific corrections; do not
declare an unresolved nested-composition mechanism fixed because the flat example
passes. A redesign of documentation structure can precede another authoring pass
if readers cannot find or apply the model.

The final handoff should include the public docs/site artifact, runnable examples,
qualified compatibility table, inventory closure/disposition register, build and
publication instructions, and remaining limitations. The result should be usable
by another agent from the public documentation, with no hidden transcript context.

## 10. Decisions already made and remaining qualification

**Established by the user and reference inspection:** plan page contents rather
than write them now; use the shortcomings inventory; publish user docs as an HTML
GitHub Pages site comparable to SDAX Hamilton; preserve Dataclass isolation.
SDAX Hamilton is an example of website delivery, not a required content/style
template. MkDocs Material is the proposed tooling. The operator also requires
granular matching/property/parameter flow and qualified real-consumer snippets
alongside standalone recipes, as recorded in sections 5.3 and 5.4.

**Resolve during P0, without broadening scope:** qualified current language route
and installation source, supported SDK/backend tuple, legacy CLI treatment,
remaining nested-expression contract, stable page paths and exact public inclusion
rules. Verify repository metadata and deployment permission before activation.

**Not delivered or authorized here:** documentation content, executable recipes,
new test/site infrastructure, compiler fixes, agent dispatch or public deployment.
This plan names their proposed boundaries and acceptance criteria so a subsequent
run can be scoped and reviewed explicitly.
