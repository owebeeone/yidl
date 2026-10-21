# YIDL documentation shortcomings: consumer experience inventory

Date: 2026-10-12. This is a precursor to documentation and executable examples,
not the documentation itself, a compiler defect list, or an implementation plan.
It records what was difficult to understand during YIDL Dataclass generation,
what the recorded attempts did about it, and adjacent subjects likely to confuse
another author. It preserves mistakes as well as successful alternatives.

## Scope and evidence limits

The requested deliverable is this file only. Dataclass implementation, agents,
SDK source, generated bases, examples, tests and workspace configuration are
unchanged by this documentation task. Future documentation work needs its own
scope; these observations do not authorize compiler changes.

The relevant consumer baseline is installed **YIDL 0.1.0 / Astichi 1.1.3**, with
Python and native-rust selections. YIDL reference revision is
`9d374f88445c426a56d5dd1f96fad112d1ec5417`; original Astichi reference revision is
`1c47f781d3804130fdd61cbee07a3b2e4529158a`. SDK prototypes from the earlier,
out-of-scope compiler detour are not the evidence for these supported routes.

Dataclass Stage A was committed at
`9fdcd7cfa8c8bea4e343965f48dab7ed9382e30a`. Later comparison evidence was read
from the ongoing consumer's recorded Stage B attempts, through approximately
10:17 UTC on this date. That work was not stopped or redirected. A passing
focused attempt is not final product, portability or performance acceptance.
The source of an experimental remedy can still change after this snapshot.

**Classification matters:**

- **Observed, remedied:** a recorded failure and a subsequently passing bounded
  case, or a supported alternative verified by the consumer's existing evidence.
- **Observed, unresolved mechanism:** the failed pattern is real, but its exact
  cause or general supported contract still needs an owning investigation.
  A working alternative does not explain or repair the failed mechanism.
- **Experienced ambiguity:** an authoring or architecture misunderstanding, with
  source/reference evidence rather than a dedicated failing test.
- **Anticipated:** an adjacent question worth documenting; no claim that this
  experiment exercised it or found a defect.

These are candidate documentation shortcomings, not an assertion that every
fact is absent from every existing document. Some facts are already in the
canonical summaries but were hard to discover or apply together. Documentation
agents should assess missing content, ambiguous wording, missing examples and
discoverability separately.

## Existing material that should be connected, not duplicated blindly

- [YidlDesignSummary.md](YidlDesignSummary.md), sections 26 and 26.1: Astichi
  markers, ownership, DDS records/collections/ports, matchers, generated values
  and operations. Much of the vocabulary exists here.
- [YidlCodingRules.md](YidlCodingRules.md), sections 4 and 5: resource-driven
  composition, parsing boundaries and generator architecture.
- [README.md](README.md): distinguishes generic YIDL work from older
  Lifecycle-specific descriptions and historical plans.
- Owning implementation references: `src/yidl/concept_parser.py`,
  `src/yidl/generation/assembly_runtime.py`, `assembly_source.py`,
  `container_runtime_source.py`, `matcher_values.py` and
  `src/yidl/capsule/`. These are inspection targets, not substitutes for a guide.

Paths into other projects below are explicitly paired with their repository
name and are relative to that repository's root. They are not filesystem
dependencies or instructions to use a neighboring checkout for regeneration.

## Priority map

| Priority | IDs | Needed outcome |
| --- | --- | --- |
| First | D01–D06 | An author can get from desired Python to a correctly wired minimal generator |
| First | D07–D15 | An author can resolve binding, empty-surface, inheritance and name failures |
| First | D16–D22 | An author can diagnose nested composition, preserve semantics and reproduce generation |
| Next | D23–D28 | Supported SDK boundaries, captures, caches, versions and evidence are understandable |
| Next | A01–A10 | Adjacent facilities have explicit contracts before authors must discover them by trial |

## Experienced issues and recorded remedies

### D01. Three different meanings of a class or model

**Classification:** experienced ambiguity.

The consumer's user model, the generated DDS fact records, and YIDL's
concept/production definitions are different things. Lifecycle-oriented class,
facade and store descriptions made it harder to identify which parts belong to
the generic language and which belong to a consumer. A plain dataclass generator
does not need Lifecycle's state/facade architecture.

**Resolution:** the consumer defines immutable normalization facts, fills the
generated DDS builder, and assembles a separate plain Python model. The canonical
developer index already says Lifecycle-specific behavior belongs in Lifecycle.

**Needed documentation:** a vocabulary diagram with a tiny end-to-end example;
label definition-time objects, decoration-time facts and runtime instances. Show
that generated DDS records are not the generated user class. Use a non-Lifecycle
example early in the language guide.

### D02. The complete path from a YIDL file to an executable class

**Classification:** experienced ambiguity; supported route verified.

Reading isolated APIs did not make the execution sequence obvious. In particular,
compiling a concept is not constructing an instance, emitting a runtime base is
not assembling a user's class, and compiling the final AST is not parsing fresh
method text.

**Verified route:** `compile_yidl_files(source_map, entry_name)` selects a compiled
concept; `emit_concept_runtime_source` receives its data definition/resources/
assembly metadata; the emitted module exposes `new_builder()` and named assembly
functions. Populate its concrete collections, freeze facts, call the generated
`build_<assembly>`, obtain `to_executable_ast()`, then compile/execute with the
consumer's captures. The original-SDK feasibility probe passed this route.

**Needed documentation:** one complete runnable example with every intermediate
object and emitted file shown. State when source parsing, template compilation,
binding, materialization and user factory execution happen. Evidence: Dataclass
repository `docs/validation/baseline/original_sdk_probe.py` and
`original-sdk-results.json`.

### D03. Basic grammar cannot be inferred from Python, YAML or similar DSLs

**Classification:** observed, remedied.

A record declaration using comma-separated property names failed with
`Unexpected token Token('COMMA', ',')`, expecting `RBRACE` or `CNAME`. The
consumer corrected it to the supported separate property entries. Regeneration
subsequently passed. This was a syntax/setup correction, not a product behavior
RED or a compiler defect.

**Needed documentation:** copyable grammar examples for `module`, `import`,
`export concept`, `property`, `record`, `collection`, resource delimiters,
contribution, matcher, production and assembly. Explicitly distinguish block
entries from expression/list syntax. Include an incorrect comma example and the
parser diagnostic. Evidence: Dataclass Stage A
`docs/validation/stage-a/a01-compose-attempt-setup.log` and current core resource
at the Stage A revision.

### D04. Semantic property names versus generated storage names

**Classification:** experienced ambiguity; reference contract already exists.

`FieldName` in a YIDL property is not the constructor keyword `field_name` in its
generated fact record. A fact's identity, owner and order are also not the Python
field's value. These distinctions are documented in section 26.1, but need an
author-facing bridge.

**Resolution:** inspect the emitted record schema and populate its concrete
record using generated storage names. Keep identity, owner, ordering and actual
captured values as separate facts.

**Needed documentation:** annotate a property declaration, generated constructor,
builder insertion and matcher read side by side. Include unknown-keyword/type
failure examples and rules for explicit storage-name customization. Do not imply
that a union record itself is instantiated instead of its concrete variant.

### D05. Resource shape must match the receiving surface

**Classification:** observed across multiple attempts; partly remedied.

Statement bodies, scalar expressions, argument payloads and parameter payloads
are not interchangeable just because all are Python snippets. The comparison
work tried ordinary expression payloads, `astichi_funcargs` carriers and nested
expression holes. A form working in one context/backend was not enough proof for
another context.

**Recorded alternatives:** constructor parameter contributions use small authored
function signatures; statement contributions fill named method-body holes;
comparison tuple reads use expression resources at tuple insertion sites. Later
Python-backend expression carriers needed the correction in D19.

**Needed documentation:** a tested compatibility table for each hole/port kind,
resource form and supported backend. Show zero, one and several contributions,
including parameters, keyword-only parameters, call arguments, tuple elements,
statement suites and a scalar expression. Explain `code` versus `template` and
when `astichi_funcargs` is appropriate. Do not turn one failed arrangement into a
blanket claim that expression composition is unsupported.

### D06. Recipes should start with the desired generated Python

**Classification:** experienced authoring difficulty.

Knowing marker definitions did not answer how to generate a direct assignment,
a default-factory branch, a tuple, a short-circuit comparison or an optional
method. Reconstructing the recipe from unrelated examples introduced avoidable
assumptions.

**Resolution:** working consumer resources now supply concrete examples, but the
knowledge should not require reading the whole Dataclass implementation.

**Needed documentation:** for each recipe, show desired Python, input facts,
authored resource, contribution bindings, matcher selection, target wiring and
final generated output. Include a direct slot constructor, specialized property,
defaulted/keyword-only parameter, method suppression, ordered tuple and nested
attribute read. Small examples should precede combined feature examples.

### D07. Identifier demands do not automatically specialize attribute names

**Classification:** observed, remedied.

The original feasibility probe incorrectly assumed that an attribute spelling
such as `self.field__astichi_arg__` acted like an identifier demand. The corrected
route uses the actual reference surface:

```python
self.astichi_ref(external=field_name)
```

Binding the path to `count` produces direct `self.count` access. A standalone
original-SDK probe verified direct specialization under both backend selections.

**Needed documentation:** distinguish `Name`, parameter identifier, attribute
path and literal replacement. Show `ident` versus `external` wiring and nested
paths such as `self.payload.rank`; document accepted path syntax and validation.
Evidence: Dataclass `docs/validation/baseline/original-sdk-results.json`.

### D08. Reference binding inside parameter annotations was the wrong recipe

**Classification:** observed, remedied for the consumer; general cause unproven.

A global `astichi_ref` in a parameter annotation survived generation as a call,
causing `NameError`. The working constructor uses identifier demands for captured
annotation/default names:

```python
def astichi_params(param_name__astichi_arg__: annotation_name__astichi_arg__):
    pass
```

The consumer captures the real annotation object and binds its generated name.
This avoids serializing the annotation or repairing the resulting AST.

**Needed documentation:** a parameter/return-annotation recipe with real object
captures and emitted signatures. State where reference markers are supported;
investigate the failed annotation pattern before calling it a contract violation.
Evidence: Dataclass Stage A `sdk-observations.md`,
`a01-green-attempt-green.log` and `a01-identifier-captures-setup.log`.

### D09. Assignment, augmented assignment and deletion need target context

**Classification:** observed, remedied in bounded cases.

An `astichi_pass` expression used directly as an assignment target yielded a
Load-context node, rejected by Python AST compilation. Stage A used an ordinary
authored identifier target plus identifier binding. Later comparison composition
exposed a backend-sensitive factory target/capture failure; the current core uses
the transparent target form around the passed parameter:

```python
astichi_pass(param_name__astichi_arg__, outer_bind=True)._ = factory_name__astichi_arg__()
```

Direct slot stores use the documented transparent attribute target:

```python
astichi_pass(self, outer_bind=True).astichi_ref(external=slot_name)._ = value
```

These snippets illustrate the recorded forms; the surrounding bindings and
scopes are required. Neither is permission to manipulate AST contexts manually.

**Needed documentation:** positive/negative Load, Store, AugStore and Delete
recipes, including a local parameter and nested attribute. Explain `._` and
`.astichi_v`, and when an ordinary target is sufficient. Evidence: Stage A
`a02-green-attempt-green.log`; Stage B `b03-python-transparent-target-green.log`
is a failed attempt, followed by the passing `b03-python-static-expression-green.log`.
Do not mislabel that intermediate file's name as a passing result.

### D10. Cross-scope names, keeps and captures are distinct mechanisms

**Classification:** experienced ambiguity.

I needed to distinguish preserving an identifier spelling, referring to an outer
lexical value, importing a scoped binding and installing a runtime object in the
execution namespace. `keep` is not a substitute for supplying a missing binding;
an outer reference is not an assignment target automatically.

**Working pattern:** resources keep deliberate public names such as `self`,
method names and selected capture identifiers. Contributions use
`astichi_pass(..., outer_bind=True)` where their reads refer to the containing
method. The consumer supplies callbacks/defaults under deterministic private
names in a fresh namespace.

**Needed documentation:** a scope diagram before and after hygiene; contrast
`keep`, `ident`, `external`, `astichi_import`, `astichi_export` and `astichi_pass`.
Show two contributions using the same local spelling without accidental sharing,
and an intentionally shared outer local. State each marker's legal AST positions.

### D11. Empty selections require explicit treatment

**Classification:** observed, remedied.

Zero-field constructors, disabled slots/init and missing store contributions
initially failed selected-native assembly with `scope.build requires native
materialization but the native materializer did not produce a composable`.
The consumer added explicit empty parameter/statement contributions and matchers.
Its layout corpus subsequently passed.

An empty-source resource is also a distinct suppression mechanism: current
`assembly_runtime._is_empty_resource_contribution` detects empty source and skips
that contribution. A `pass` snippet is not identical to an empty-source resource.

**Needed documentation:** distinguish no match, suppressed contribution, empty
expression/parameter list and a syntactically valid empty suite. Show zero-field
classes and disabled methods on each supported backend. Evidence: Stage A
`a03-red.log`, `a03-corrected-green.log`, `sdk-observations.md` and the empty
resources/matchers in its core resource.

### D12. Logical source maps, imports and package resources need one recipe

**Classification:** experienced ambiguity; supported route recorded.

YIDL imports resolve within the supplied source map, not automatically through a
consumer's working directory or arbitrary sibling repository. Splitting a shared
comparison module required stable logical keys and matching import spellings.

**Working arrangement:** keys such as `shared/comparison.yidl` and
`dataclass/dataclass_comparison.yidl`; the consumer imports
`../shared/comparison.yidl`. Packaged resources are read through
`importlib.resources` and the emitted runtime includes the selected resources.

**Needed documentation:** a two-file and a three-file project, virtual source-map
keys, aliases, exports, relative imports and a packaged regeneration command.
Include missing import/export diagnostics. Explain module names versus source-map
paths and which one identifies the entry file. No undocumented cwd/sibling-path
fallback should be taught as the standard route.

### D13. Concept inheritance does not silently replace named productions

**Classification:** observed, remedied.

An extending consumer supplied `ClassProduction` when it was already inherited.
Compilation raised `composable production 'ClassProduction' is already inherited
by concept 'DataclassComparison'`.

**Remedy:** introduce a distinctly named consumer production,
`DataclassClassProduction`, and select it through the class contribution matcher.
The later inherited-rule regeneration passed. This was a consumer naming and
extension error, not a missing compiler feature.

**Needed documentation:** an extension matrix for properties, records,
collections, resources, productions, assemblies and matchers: merge, reuse,
specialize, conflict or unsupported replacement. Show the actual error followed
by this indirection through a matcher. Evidence: Stage B
`b01-compose-setup.log` and `b01-extended-rules-setup.log`.

### D14. Inherited matcher defaults are not ordinary method overrides

**Classification:** observed, remedied.

Adding a different default to inherited `ClassContributions` produced
`contribution matcher 'ClassContributions' extended by concept 'DataclassComparison': duplicate default`.
The merger allows an identical default name but rejects a conflicting default;
duplicate rule names are checked separately.

**Remedy:** retain the inherited default and add distinctly named matching rules
for `UseSlots == True` and `UseSlots == False` selecting the consumer contribution.
Regeneration then passed. The neutral comparison example later uses more heavily
weighted, distinctly named rules to specialize operand reads.

**Needed documentation:** a base-plus-child example showing default fallback,
rule specialization, weights, duplicate defaults/rules and overlapping rules.
Explain whether unmatched, equally weighted and multiply matched cases fail or
select, with executable evidence. Evidence: Stage B
`b01-compose-corrected-setup.log`, `b01-extended-rules-setup.log`; owning merger
`src/yidl/concept_parser.py`, `_combine_contribution_matchers`.

### D15. Resource reuse is different from build-instance name reuse

**Classification:** observed, remedied in the later backend case.

Several disabled ordering methods reused an implicit contribution name,
`EmptyOrder`. Python-backend assembly failed with
`build: duplicate instance name: EmptyOrder`.

**Remedy:** use distinct disabled contributions (`NoLt`, `NoLe`, `NoGt`, `NoGe`)
while sharing the same pass resource. The corrected Python-backend case eventually
passed after the additional D19 correction.

**Needed documentation:** separate resource name, contribution name, `as` build
name, index and fully qualified build path. Show how two insertions can share a
resource but need distinct destination instance identities. Evidence: Stage B
`b03-python-route-corrected-green.log` is a failed attempt; final bounded pass is
`b03-python-static-expression-green.log`.

### D16. Identity, owner filters, index, order and target paths need separation

**Classification:** experienced ambiguity; indexed failures observed.

An operand's collection identity, its class owner, its insertion index, its
sorting order and the build path used to reach its parent are separate controls.
It was not safe to infer that declaration order or a field identifier alone
would give the intended nested assembly.

**Working flat pattern:** comparison operands carry distinct identities, a
`CmpOwner`, and `CmpOperandOrder`; production edges filter by owner; contributions
use explicit index/order and target the relevant method hole. The neutral
consumer proves nested Python attribute reads, not arbitrary nested build graphs.

**Needed documentation:** a worked build tree annotated with `/Root`, class,
method and indexed child addresses. Explain the legal index types, path-index
evaluation, cardinality and tie order. Include two classes with overlapping field
names and reordered input records. Separate syntactic path validity from finding
the intended live destination. See `assembly_runtime.evaluate_index`,
`evaluate_path_index` and target resolution.

### D17. Nested expression binding/target propagation remains unexplained

**Classification:** observed, unresolved mechanism; alternative available.

Attempts to assemble equality as a nested indexed expression chain failed in
different ways: an unbound `term_path`, a failed target `next_term`, and a generic
native-materialization failure. Trying another expression carrier or backend did
not establish the original nested pattern as working.

**Recorded alternative:** replace the nested chain with flat ordered statement
contributions, one per selected operand. D18 records its bounded semantic tests.
This avoids the failed arrangement; it does not prove the binding/target system
incorrect or explain why the nested arrangement lost its wiring.

**Needed documentation/investigation:** a minimal nested scalar-expression example
with local and external bindings, root mappings, indexed siblings and a trace of
binding application. Reproduce the original pattern separately and identify
author error, unsupported surface or defect before making a normative statement.
Evidence: Stage B `b01-chain-route-attempt.log`,
`b01-chain-route-corrected-attempt.log`, `b01-chain-python-route-attempt.log`,
`b01-variadic-expression-route-attempt.log` and `b02-flat-steps-green.log`.

### D18. A supported alternative must preserve raw comparison semantics

**Classification:** observed, remedied for the focused equality corpus.

Changing expression shape can alter getter order, short-circuiting, truth
conversion, callbacks and the raw object returned by `__eq__`. Python 3.12's
tuple-style dataclass equality differs from the self shortcut and short-circuit
field comparisons used on 3.13/3.14. Replacing the latter with unconditional
tuple reads or a generic boolean aggregator would not be equivalent.

**Recorded flat resources:**

```python
comparison_result = self.field == other.field
if not comparison_result:
    return comparison_result
# Further selected operands follow in order.
# The final operand is returned directly, without an extra truth conversion.
```

The real resources bind individual direct read paths and preserve scopes; this
fragment is an explanatory sketch. Focused independent std differential tests
for false, final and shared operand cases passed on the three supported minors.
The final product/benchmark gates were still outstanding at this snapshot.

**Needed documentation:** show a nested-expression recipe if supported and a
semantically justified flat alternative. Include falsey non-bool comparison
results, getter/callback traces, shared/nonreflexive operands and empty operands.
Do not call a template workaround correct merely because simple integer values
compare correctly. Evidence: Stage B `b02-red.log`,
`b02-flat-corrected-green.log`, `b02-minor314-green.log`, `b02-minor312-green.log`.

### D19. Bare reference expressions and backend-sensitive expression carriers

**Classification:** observed; bounded alternative passed, general contract open.

A bare statement containing `astichi_ref` was rejected with a diagnostic saying
it is value-form only. An `astichi_funcargs` carrier and transparent-target
attempt also did not complete the Python comparison case. In one failed attempt,
the cache still contained the default-factory sentinel, so successful compilation
would not have been sufficient evidence.

**Later passing arrangement:** the read resources use a static expression such
as `self.<bound-path> if True else None`, rather than a bare reference statement;
factory stores also use the appropriate transparent passed-parameter target.
`b03-python-static-expression-green.log` records the bounded Python pass.

**Needed documentation:** the minimal supported scalar-expression carrier,
why a bare reference is rejected, and whether `astichi_funcargs` belongs at this
tuple surface. Validate both backends and inspect emitted source/bytecode before
claiming the static wrapper has no runtime overhead. The combined passing attempt
does not isolate every intermediate failure's cause.

### D20. Regeneration is part of the edit/run cycle

**Classification:** observed, remedied.

An initial flat-step test still executed a generated base containing the earlier
`NextTail` machinery because the authored resource change had not been regenerated.
After regeneration, the same focused tests passed.

**Needed documentation:** distinguish authoritative `.yidl`, checked-in emitted
runtime and final model output. Show check-by-default regeneration, explicit
`--write`, source digests and stale-output diagnostics. Explain when a new process
is required to discard imported generated modules or cached templates. Evidence:
Stage B `b02-flat-steps-green.log` (failed attempt),
`b02-flat-regenerate-setup.log`, `b02-flat-corrected-green.log`.

### D21. A production does not automatically export the expected build function

**Classification:** observed, remedied.

The neutral comparison fixture looked up `build_NeutralModule` and got `KeyError`.
Its concept needed the corresponding assembly declaration:

```text
assembly NeutralModule = NeutralProduction
```

The completed neutral fixture subsequently generated and executed under the
recorded native 3.12 and Python 3.13 selections. It demonstrates inherited nested
operand read specialization without Dataclass metadata.

**Needed documentation:** the relationship between `export concept`, production,
assembly and emitted `build_<assembly>` entrypoints. Include the minimum complete
concept and show available exports before execution. Evidence: Stage B
`b04-neutral-complete-setup.log`, `b04-neutral-native-green.log`,
`b04-neutral-python313-green.log`; Dataclass `tests/data/yidl/comparison_neutral.yidl`.

### D22. Errors need a route back to facts, resource and target

**Classification:** observed diagnostic difficulty, not a request to patch errors.

Failures arrived at several different layers: parser comma errors, inherited
symbol/default conflicts, duplicate build instances, unresolved binding demands,
contribution target errors, generic native finalization failure, Python AST
compile errors, runtime NameError and independent behavior mismatches. The same
surface symptom does not establish the same cause.

**Current practice:** retain the traceback and cause chain, inspect the generated
base/model, narrow to a canonical case, and distinguish setup from product
behavior. That worked, but required reading implementation internals.

**Needed documentation:** a troubleshooting decision tree keyed by those exact
diagnostics. Show supported inspection APIs or commands for selected matchers,
contribution identity/index, evaluated target address, bindings, unresolved ports
and emitted output. Verify each inspection command before documenting it; do not
invent a trace flag. Include the distinction between absent binding, binding to
the wrong instance and a target that was never constructed.

### D23. Arbitrary Python captures are not SDK external literal bindings

**Classification:** experienced boundary ambiguity; consumer capture remedy verified.

Callbacks, opaque defaults, annotations and context objects should not be
serialized through `.bind(...)` as if they were supported literals. Their `repr`
must not become executable method text, and generation must not invoke them to
discover a value.

**Verified route:** put real objects under deterministic private identifiers in a
fresh consumer execution namespace, or ordinary authored builder captures; bind
the identifier/path strings through existing SDK surfaces. Stage A owner installed
probes verified independent hostile-repr defaults and copied Field ownership.

**Needed documentation:** a literal/type-domain table for external binding and
YIDL generated-value factories, plus a callable/opaque-default capture recipe.
Separate declaration metadata, generation bindings, function globals/closures
and instance storage. Evidence: Dataclass Stage A `owner_installed_probe.py`,
`owner-installed-results.json`; `ConsumerOnlyGenerationAmendment.md`.

### D24. Template caching, generated-code caching and live state are different

**Classification:** experienced ambiguity; partial behavior verified.

`MatcherGeneratedValue.to_generator()` already lazily compiles and caches an
unbound composable. That is different from persisting a complete unresolved
template, caching final executable AST/bytecode, caching a completed class, or
memoizing a runtime value. Confusing these contributed to the SDK detour.

**Resolution:** use the existing source-based template cache and independent
per-class builds/captures. The baseline probe verified repeated wrapper access
returns its cached template; owner capture probes verified the bounded class
isolation case. This is not a complete cache/thread-safety proof.

**Needed documentation:** a lifecycle/ownership diagram for each cache, keys,
invalidation, clone/bind behavior and permitted sharing. Show first and second
generation with different names/defaults/callbacks. Explain effects of editing
resources after import, reusing a frozen fact container and reusing a wrapper.
Current reference: `matcher_values.py`, `MatcherGeneratedValue.to_generator`.

### D25. Generation performance is separate from instance field performance

**Classification:** experienced architectural misunderstanding.

I incorrectly treated parser-free decoration and wholly Rust-owned generation as
prerequisites for direct slots and specialized accessor performance. Those are
stronger implementation preferences. The original SDK generates direct field
access even though its supported generation route can parse source.

**Remedy:** stop the SDK detour, test original installed packages, and resume
consumer-only generation. The probe established core feasibility, not complete
feature support or benchmark results.

**Needed documentation:** separate cold/repeated generation, emitted-code shape,
hot method/access execution and memory measurements. State what “native” means:
actual YIDL/Astichi composition or a selected backend is not a promise that every
operation executes in Rust. Do not infer a compiler prerequisite from a desired
runtime property. Evidence: Dataclass `dev-docs/ScopeCorrection.md`,
`OutsideScopeFindings.md` and baseline results.

### D26. Parsing policy and scope applicability need explicit explanation

**Classification:** experienced ambiguity; apparent documentation tension.

The coding rules restrict parsing in generated decorator paths and prefer
precompiled templates; the design summary also describes lazy source compilation
inside generated-value wrappers. “Precompiled” can mean several different things.
The summary's preference for improving Astichi also does not authorize another
consumer task to edit that dependency.

**Resolution in this task:** the operator explicitly limited work to consumers
and allowed the original supported source-generation/cache route. No artifact
API or native-restoration facility was required. This does not silently amend
YIDL's own implementation rules.

**Needed documentation:** identify the protected interval, distinction between
authored build-time source and ad hoc runtime source, current implementation and
future direction, owning repository and effective versions. Reconcile wording
with demonstrated execution. Explicitly say a dependency improvement needs task
authorization and supported-route feasibility testing first. Relevant texts:
`YidlCodingRules.md` section 4; `YidlDesignSummary.md` section 26.1 item 19.

### D27. Backend/version evidence is essential to a reusable recipe

**Classification:** observed across the comparison work.

A recipe passing selected-native 3.12 did not establish Python-backend or 3.13
behavior. One 3.13 attempt also failed because the consumer captured a stdlib
private recursive-repr helper under a name absent on that minor. That was a
consumer/stdlib compatibility error, not a YIDL matching failure.

**Remedy:** verify package versions/import origins and selected backend, distinguish
fallback, and use version-appropriate helpers. Core owner installed checks passed
three minors under both backends without prototype capabilities. Later comparison
cases retained their separate failed attempts and passing bounded results.

**Needed documentation:** label example versions/backends, actual selection versus
requested configuration, compatibility limits and helper ownership. Show how to
verify installed origins without treating workspace imports as package evidence.
Evidence: Stage A `owner-backend-confirmation.json`; Stage B
`b01-chain-route-attempt.log`, `b03-python-route-red.log` and subsequent results.

### D28. Inspectable goldens are not an independent behavioral oracle

**Classification:** experienced verification need; supporting harness already exists.

The generated output needed to be readable enough to locate surviving markers,
bad targets and missing fields. A golden matching yesterday's output would not
prove that output matches the intended Python behavior.

**Working approach:** canonical inputs produce bindings, emitted runtime base,
formatted model source and behavior observations. Std dataclasses supply a
separate oracle for the compatible subset; narrow tests check failures and
callback semantics. The quote/deletion fixtures place field policies beside their
declarations and verify removed fields do not leave detached policy behind.

**Needed documentation:** the existing explicit-root golden harness recipe,
snapshot refresh procedure after independent assertions, and source/behavior
roles. Use contrasting multi-field examples, plus minimal examples for diagnosis.
Separate setup failures, expected behavior RED, failed intended-GREEN and passing
verification; an artifact's filename is not its verdict. Evidence: Dataclass
`tests/support/golden_case.py`, comparison fixtures and stage increment ledgers.

## Anticipated questions requiring documentation, not asserted defects

### A01. Matcher inputs, scores and overlapping conditions

Clarify input tuple order, same-named property resolution across several input
records, missing values, computed fields, default fallback, weights and ties.
Show an inherited broad rule, a narrower higher-weight rule, equal-weight overlap
and no match. The neutral fixture used weighted specialization, but this inventory
does not establish every matcher case. Distinguish contribution matchers from
generic DDS matchers rather than assuming identical contracts.

### A02. Nested template edge values and evaluation environments

Explain `edge_arg_names`, external edge bindings, preserved names and self/data
expressions: when evaluated, which record/builtin scope is visible, whether they
produce literal data or another generated value, and whether results are retained.
Provide one nested template whose bindings depend on two records and a diagnostic
example for an unavailable provider. No new evaluation/caching semantics are
proposed here.

### A03. Generated-value wrappers and imports

Document accepted domains and contracts for `from_literal`, `from_import`,
`from_astichi_code`, `from_astichi_template` and any public wrapper composition.
Separate Python literals, import references, templates and arbitrary Python
objects. Show when an import executes and where it is emitted. Include nested
literal containers, rejected objects and empty resources. Raw Python objects or
raw composables should not be assumed to satisfy the matcher resource contract.

### A04. Operations, productions, transforms and snapshots

Explain data-producing operations versus composable-producing assembly; phase
ordering; concrete/computed/matcher-result sources; builder writes and policies;
and the point at which matcher views are evaluated against a stable snapshot.
Show a signature-analysis operation producing dependency facts later consumed by
assembly. Do not imply that DDS itself understands field-factory dependencies or
provides a general reachability API; section 26.1 explicitly separates those roles.

### A05. Collection and port cardinality, lookup and merge policies

Show single/many collections, tuple identities, duplicate insertion, replacement,
add-if-absent, computed views and ordered reads. Contrast the size of a collection
with cardinality at one port address. Include two records targeting the same port
and one record participating in several views. Explain whether queries or writes
can derive new records and where mutation is legal before/after freezing.

### A06. Declarative factory arguments and dependency ordering

Provide a consumer recipe for turning callable signatures into facts and emitting
specialized calls: positional-only, positional/keyword, keyword-only, optional
providers, class/instance providers and unknown/variadic parameters. Explain which
part is consumer policy versus a YIDL facility. Include dependency order independent
of constructor parameter order and unavailable-provider/cycle diagnostics. These
are anticipated Dataclass concerns at this snapshot, not completed Stage C claims.

### A07. Control-flow and compound construct recipes

Document nested `if`/`elif`/`else`, `try`/`except`/`finally`, loops with `else`,
`with`, decorators, comprehensions and supported version-specific constructs.
Explain insertion boundaries, empty suites, parameters and lexical references
inside each. Include two interacting constructs rather than promising all Python
syntax from a single successful class example. Scope compiler limitations by
version; no facility is asserted missing merely because it was not exercised.

### A08. Deferred builds, copies, materialization and failure ownership

Explain which operations return new composables versus retain mutable build
state; when deferred edges/bindings are applied; whether repeated materialization
is supported; and what remains usable after failed binding or target resolution.
Give the supported diagnostic route for stale or foreign handles and engine
closure. Distinguish ordinary source-based ownership from the unaccepted artifact
prototype. Do not promise native failure isolation without tests.

### A09. Packaging and sharing one authoritative resource

Show two independent consumers extending one packaged YIDL asset, with explicit
authority, logical import keys, source digests and build/runtime dependency
boundaries. Explain checked-in generated bases, wheel/sdist contents and clean
regeneration when the authority is absent or changed. The neutral comparison
fixture is evidence of inheritance/read specialization; actual Undoable packaging
integration remained later work at this snapshot.

### A10. Local declarations, cross-references and safe removal

Document the boundary between field-local policy and legitimate scoped dependency
references. Removing a field should remove its policy with that declaration;
remaining named consumers should report a missing dependency, not silently change
meaning. Provide a before/after field deletion example and a failing retained
reference. This is both an authoring requirement and a documentation exercise;
do not invent a declarativity score from a successful golden.

## Evidence registry for later documentation agents

All entries in this table belong to repository **`yidl-dataclass`**. Each path is
relative to that repository's root. Its Stage A revision is recorded above;
Stage B artifacts were an in-progress snapshot, not an accepted release.

| Path | SHA-256 of inspected bytes |
| --- | --- |
| `docs/validation/stage-a/sdk-observations.md` | `86d7dcd8b08c1604951f96290c47312ca8df18b577c199b6cf07c4b2aa683b58` |
| `docs/validation/baseline/original-sdk-results.json` | `32293b56ab2309c83a17efefec70d3a259ccbb5bdb2454857b7872eace590d92` |
| `docs/validation/stage-b/b01-compose-setup.log` | `536f97bf3f37c6b2a546c475a9dd2892f1af32cbec8dd3adbecbb1614ef9355c` |
| `docs/validation/stage-b/b01-compose-corrected-setup.log` | `6834d8fd4fe3499fac4f9c296ca1453c09f7fcf555fb684c8c64c7d880744b19` |
| `docs/validation/stage-b/b01-chain-route-attempt.log` | `537ab1a7b83d966ab6f86068ff572e93dd6f7ecf7bca1ee34bfe01b9132be7f8` |
| `docs/validation/stage-b/b01-variadic-expression-route-attempt.log` | `28d74e9458bc60d63c0261d1a388bd9a0f450e083f23f9b4b83c31faf7dfb28d` |
| `docs/validation/stage-b/b02-flat-corrected-green.log` | `4a07fee0cbfe63fba40e0ae8f9269c89fc7a8bbed0d00e0447e9f70b7915b062` |

Some successful setup/standalone commands emit an empty log. Their empty-log
digest is not proof of success; inspect `increments.jsonl` for the command,
backend environment/context, runtime, time and exit code. JUnit and independent
assertions supply additional evidence where recorded. Failed attempts and label
corrections must remain visible when a recipe is promoted.

## How to turn this inventory into documentation work

For each ID, the assigned agent should:

1. Locate existing authoritative material and decide whether the gap is missing
   content, ambiguity, missing example or poor navigation. Record that decision.
2. Verify the current supported contract and minimal example against the declared
   SDK/version/backend tuple. Keep an unresolved mechanism unresolved until its
   cause is demonstrated; do not quietly endorse an experimental workaround.
3. Produce the appropriate reference clarification, runnable recipe, failure
   example and generated output. Assign generic language material to YIDL and
   stitching mechanics to Astichi documentation, with cross-links rather than
   copying divergent contracts.
4. Preserve the original failed arrangement where useful, explaining exactly why
   the corrected form differs. Include zero/one/multiple and interacting cases
   when the subject depends on cardinality, nesting or inheritance.
5. Check discoverability from the user starting point, not only consistency with
   a long design summary. A reader should not need this experiment transcript.
6. Record closure as documentation plus executable evidence, or an explicit
   unsupported contract with a verified alternative. Compiler changes, policy
   changes and broader remediation require separate authorization.

No ID is closed by this precursor. No agent dispatch, SDK fix, documentation
rewrite or interruption of Dataclass implementation is requested by its creation.
