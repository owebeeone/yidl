# Executable Architecture Through Facts and Scoped Code Composition: YIDL and Astichi

**First technical paper draft — intended audience: Onward! Papers.**

Prepared 2026-10-03. This is an exploratory implementation paper, not a
submission-ready manuscript. Authorship, affiliations, and human approval remain
unset. The implementation snapshot includes uncommitted work. Claim identifiers
such as C3 point to [the evidence index](evidence-index.md); outstanding research
requirements appear in [the research gaps](research-gaps.md).

## Abstract

Framework behavior often spans declarations, dependency analysis, storage,
dispatch, inheritance, and resource lifetime. A handwritten implementation can
support these concerns yet make their relationships difficult to inspect and
extend. We explore an alternative in which part of the framework architecture
becomes compiler input. YIDL packages typed properties, record families,
collections, resources, selection rules, fact derivations, and phased assembly
into mergeable concepts. Astichi supplies a complementary mechanism for
composing Python AST fragments through holes, explicit identifier and external
bindings, fallback bodies, and composition scopes. Domain packages select and
assemble specialized code while retaining imperative algorithms and ordinary
runtime libraries where needed. The motivating application is the replacement
of Pyrolyze's handwritten lifecycle framework by the downstream
`yidl-lifecycle` package. A mutable lazy field provides a concrete example of
policy selection replacing a fallback setter while reusing the getter. Source
inspection, canonical generated artifacts, and bounded artifact execution
support the architectural account; fresh decoration failures in the inspected
working checkout limit reproducibility. We distinguish the implemented
composition mechanisms from cross-language and self-description proposals,
and separate the architecture from an AI-assisted development account that is
currently a practitioner observation rather than a productivity experiment.

## 1. Problem: making framework relationships inspectable

Consider a field whose value is initialized on first access, whose factory
depends on another field, and whose setter may either reject replacement or
allow it. The implementation involves more than an accessor: the constructor
must establish an uninitialized state; factory arguments must be resolved;
inheritance must preserve compatible declarations; the setter must implement
the selected policy; and the emitted names must refer to the correct state.
Transactional fields add current and working views, enlistment, publication,
rollback, and hooks. These relationships can become spread across decorators,
descriptor tables, state objects, and runtime control flow.

The motivating practitioner reports that `pyrolyze.lifecycle` had become too
large and entangled for the agents then available to extend reliably. The
resulting exploration moved through lifecycle-specific generation, a
template-oriented IDL, decorator compilation, fact tables, matcher-selected
resources, and production assembly. Astichi emerged because composing code
safely was itself a substantial problem. The account in `MetaSquaredLog.md`
describes this as a five-week detour. It is evidence of the practitioner's
experience and rationale, not measured elapsed development effort, a comparison
against unaided engineers, or evidence that the approach was impossible before
LLMs. [C1]

The question for this paper is architectural: **can a framework expose its
variation and assembly relationships as explicit compiler data, without trying
to replace every algorithm with declarations?** Our exploratory answer is a
two-part system. YIDL records and derives domain facts and chooses resources;
Astichi composes the selected code while tracking names and scopes. The
resulting code is an inspectable artifact between the architecture and its
runtime behavior. [C2–C8]

The proposed contribution is the implemented combination and its lifecycle
case study: a fact-oriented compiler description, explicit feature composition
and ordering, and scoped Python code assembly. We do not claim the invention
of generative programming, hygienic macros, staged specialization, or
model-driven engineering. Establishing what distinguishes this combination
from prior systems remains part of the research agenda.

## 2. System model and boundaries

YIDL is already a generic concept-driven compiler framework. Its core objects
describe schemas, facts, derivations, resources, and assembly; they are not
restricted to lifecycle field kinds. It has a standalone `.yidl` frontend backed
by Lark and programmatic data-definition and recorded-concept interfaces.
`yidl-lifecycle` supplies domain declarations and a Python class harvester on
top of those mechanisms. Dataclass-related and computed-class fixtures provide
additional examples, although they do not yet constitute independent,
production-scale domain validation. [C2, C9]

```mermaid
flowchart LR
    D[Domain concept definitions] --> G[YIDL concept compilation]
    G --> R[Reusable compiler runtime and resource plans]
    U[Author declarations] --> H[Domain harvester]
    H --> F[Typed facts and derived collections]
    R --> F
    F --> S[Matcher selection and phased productions]
    S --> A[Astichi scoped assembly and materialization]
    A --> O[Inspectable Python source or executable AST]
    O --> C[Class construction]
    C --> I[Instances and ordinary runtime libraries]
```

This diagram distinguishes data flow from timing. Concept compilation builds a
compiler for a domain. The generated compiler runtime subsequently specializes
author declarations. In the lifecycle application, specialization occurs when
the decorator runs; it can therefore be part of application import latency.
The final instance executes generated methods and runtime library calls rather
than interpreting the full concept model on every access. [C10]

The boundary is deliberate but incomplete as an ideal. Lifecycle meaning lives
primarily in the downstream feature layers and harvester; Astichi knows about
Python syntax and composition, not lifecycle transactions. YIDL still contains
earlier lifecycle-related capsules and validation examples, and the downstream
frontend contains a field-kind-to-record dispatch. Package extraction is
evidence of separation, not proof that every domain-specific remnant or every
central dispatch has disappeared. [C2, C9]

## 3. YIDL mechanisms and composition semantics

### 3.1 Schemas and facts

A property describes a typed semantic column, with a default and storage name.
A record groups properties into a fact shape. A family is an open union of
record variants, so a feature can extend an inherited family. Collections
describe fact tables with cardinality and optional identity, including composite
identities. The data-definition schema and the populated container are distinct
objects. Generated record classes are plain slotted Python containers. [C3]

Collection identity supplies a place to define conflict behavior. Explicit
builder writes use `RejectDuplicate`, `AddIfAbsent`, or `ReplaceExisting`.
`AddIfAbsent` retains the existing record; `ReplaceExisting` chooses the new
record. `RejectDuplicate` rejects a different record at an existing identity,
while allowing reinsertion of the same object. These are fact-write policies,
not a universal rule that the last feature overrides everything. [C3]

Computed collections are filtered views over a source collection, with support
for additional filters. They do not automatically imply a general incremental
dependency engine. In particular, compiler-side computed facts must not be
confused with a lifecycle `derived` cache field: the former is implemented,
while the latter is not exposed in the current lifecycle marker surface. [C3,
C12]

### 3.2 Resource selection and derivation

Resources can represent code or templates, imported values, and literals.
Selection is separated from declaration: a matcher examines input records and
chooses a resource. Resource-valued results can travel through productions into
later facts, rather than having to be consumed immediately. The system also
supports contribution matchers for assembly and operation matchers for compiler
passes. [C4, C5]

For the generic resource matcher, a rule's score is the number of equality
conditions multiplied by its weight. Matching rules are considered in
descending score order. A default supplies a result when no rule matches;
without a matching rule or default there is no result. The result records the
selected resource, rule, score, input records, and inspected values. The
implementation rejects potentially overlapping equal-score rules for this
matcher surface rather than treating textual order as the intended precedence.
Multiple input sequences are traversed as a Cartesian product. This is useful
for small compiler fact sets, but requires attention to scaling. [C4]

A data production derives records into a target collection using an explicit
write policy. The canonical `dds_matcher_productions.py` fixture filters input
fields, selects required or defaulted parameter resources, and records selected
resources in parameter components. Aggregate operations cover work that is
less naturally expressed as one record mapping. They receive a
`DDSOperationContext` with record queries and writes; declared ordering can
control input traversal. The transaction-key fixture uses an imperative `seen`
set and counter to derive ordered unique transaction keys. This is an
intentional combination of declarative boundaries and imperative algorithms,
not a claim that every compiler algorithm has become a rule. [C5]

### 3.3 Concept merge and inheritance

`concept Child extends base.Parent` composes compiler definitions into a shared
semantic model. Schema families can gain variants, computed views can gain
filters, and matcher rules can accumulate. Resources, contributions,
productions, edges, and assemblies become available through the compiled
concept's merged maps. Concept inheritance is distinct from Python inheritance
of classes decorated by a domain frontend. [C6]

Merge is constrained. For ordinary named maps, the compiler deduplicates an
identical inherited object reached through a diamond, rejects distinct
same-named inherited definitions, and rejects a local redefinition of an
inherited name. Matcher merge has specialized behavior: compatible input names
are combined, differing sources for the same input reject, conflicting defaults
reject, and distinct duplicate rule names reject. Production extensions are
also deduplicated through shared inherited identities. Consequently, composition
is neither arbitrary replacement nor a demonstrated commutative algebra over
all features. Exact closure order and extension contracts matter. [C6]

The historical import/merge plans describe gaps that have since acquired
implementations and tests. They explain the design trajectory; they are not
current feature inventories. Export metadata is likewise not evidence of a
complete privacy system, and concept containment is a proposal rather than the
implemented core composition operator. [C6, C14]

### 3.4 Phased assembly

YIDL uses “production” for two related roles: deriving data records and building
composable output. A composable production declares a root and applications of
contributions. Contributions associate a resource with a target, instance
identity/index, order, and identifier or external bindings. Target selectors
refer to build paths and/or code owners. The assembly runtime translates these
requests into Astichi resource and binding requests. [C7]

Named phases group applications in a composable production. A feature can extend
an extensible inherited phase or introduce a phase anchored `after` another
phase. The implementation orders roots and siblings by numeric `order`, using
declaration order for ties, and traverses anchored descendants after their
anchor. It detects missing anchors, self-anchors, cycles, and conflicting phase
metadata. The phases are flattened into ordered applications before assembly;
they are not a runtime transaction scheduler. [C7]

Phase context also has defined replacement behavior: an application-level
`from` overrides the phase source context, and an application-level `where`
replaces the phase predicate. Assuming predicates are always conjoined would
misread the current semantics. The parser tests make this distinction explicit.
[C7]

Named phases let the base specify an assembly skeleton while a feature adds
slots, parameters, properties, or commit bodies at declared boundaries. They
reduce one source of coupling: the base need not enumerate every future
feature's apply edge. They do not remove dependencies among features or prove
that every combination is valid.

## 4. Astichi: composing code with explicit names and scopes

Astichi compiles marker-bearing, syntactically valid Python source into
composables. Marker syntax belongs to the source DSL; it is not a runtime
`astichi.markers` library that an application executes. Builders register
resources, instantiate contributions, connect holes, and bind demands. Final
materialization consumes composition markers and produces Python source or a
caller-owned executable `ast.Module`. Python's `compile` still turns that AST
into executable code. [C8, C10]

Holes have structural roles: statement blocks, expressions, parameters, call
arguments, and clauses are not interchangeable textual substitutions. A
defaulted block hole has an authored fallback suite. If nothing is inserted at
that site, materialization selects the fallback. If contributions fill the
site, they replace the fallback suite. Demands inside a discarded fallback are
inactive. Additive contributions and whole-fallback replacement are thus
compatible: replacing a fallback does not imply a general arbitrary AST rewrite
facility. [C8]

Identifier demands and external bindings solve different problems. An identifier
demand chooses a Python name and its relationship to bindings; an external
binding supplies a value used during specialization. In lifecycle resources,
`astichi_ref(external=state_slot)` denotes a selected attribute path, while
getter/setter name demands supply declarations and references. Cross-scope
sharing uses import/export/pass markers or explicit builder wiring.
`outer_bind=True` requests the immediate outer binding. Keeping a spelling is
another explicit policy, not a general escape from name resolution. [C8]

Each root and inserted contribution has a composition scope in addition to
ordinary Python lexical scopes. Independently introduced same-spelled locals
are renamed apart when necessary, with corresponding references rewritten.
Unresolved identifier demands reject; duplicate final function parameter names
reject rather than being repaired by renaming a public signature. Explicit
sharing is necessary when two fragments are intended to refer to the same
local. These are composition contracts with tests, not a formal proof of hygiene
for every possible Python construct. [C8]

The assembler layer exposes inventory-based candidate selection by demand name,
build path, and code owner. A caller can require exactly one candidate and obtain
missing/ambiguous diagnostics. Provenance and round-trip facilities help inspect
generated source, but do not preserve hidden builder semantics after arbitrary
edits: source remains authoritative. [C8]

### 4.1 A small executable example

This complete example selects an inserted body over a fallback:

```python
import astichi

root = astichi.compile('''def choose_value():
    with astichi_hole(body) as astichi_fallback:
        return "fallback"
''')
builder = astichi.build()
builder.add.Root(root)
builder.add.Chosen(astichi.compile('return "generated"\n'))
builder.Root.body.add.Chosen()
tree = builder.build().to_executable_ast()
namespace = {}
exec(compile(tree, "<example>", "exec"), namespace)
assert namespace["choose_value"]() == "generated"
```

The inspected output is the ordinary function `choose_value` returning
`'generated'`. Leaving the hole unfilled selects the fallback according to the
reference contract. The filled example was executed during drafting without
writing generated files. It illustrates structural substitution; meaningful
binding and hygiene claims additionally rely on the canonical scope fixtures.
[C8, V1]

### 4.2 Nested composition and declarative auto binding

An Astichi composition can itself become a component of another composition.
`build()` returns a composable, rather than requiring immediate conversion to
plain Python source. A subsequent builder can register that result, insert it
into a larger structure, and connect demands or holes carried by the earlier
composition. This permits partially stitched pieces to remain useful generator
components. In the canonical three-stage trace recipe, leaf fragments form a
middle component, that component is reused twice in a larger component, and an
outer build supplies the shared trace binding before materialization. A second
recipe adds indexed contributions to a loop carried through an earlier build.
These are concrete examples of composition across successive builds. [C8]

This supports an associative intuition: a group of contributions can be packaged
as one reusable component and participate in further composition. The inspected
examples establish this ability to compose compositions; they do not establish
a general associativity law under arbitrary regrouping. Hole roles, contribution
order, composition scopes, and declared binding relationships remain part of
the component contract. In particular, an immediate-outer binding is relative
to its enclosing scope. Nested composition therefore retains structure rather
than treating every grouping as interchangeable. [C8]

YIDL exposes this capability at the production level. A contribution's source
can be another production, not only a single code resource. In lifecycle,
`CoreModuleProduction` selects `CoreClassDefinition`, whose source is
`CoreClassProduction`, and targets the module skeleton's `function_body` hole.
The class production has its own root and contributions for state slots,
constructor parameters and assignments, facade properties, and transaction
methods. The assembly implementation inserts the child production's root into
the enclosing graph, then applies its internal contributions at the resulting
build path. It can therefore continue filling the class while composing the
module, without an intermediate source-text round trip. A separate canonical
YIDL fixture exercises a module containing a class production containing a
method contribution. [C7, C9]

Concept inheritance adds a second level of composability: feature concepts
extend the schemas, selection rules, and production phases that describe this
assembly. For example, the local-store concept extends the class production
with state-slot, initialization, and property phases. These levels let a feature
contribute to a larger generator without restating the complete generator.
Composition levels and production phases describe assembly structure and
ordering; they do not necessarily introduce additional execution stages. [C6,
C7, C9, C10]

Auto binding makes this structure declarative at the YIDL authoring boundary.
The author supplies the selected resource, target constraints, and bindings;
the assembly runtime and Astichi's inventory-based resolution establish the
concrete connections. For example, the local-store property contribution maps
the getter name, setter target, and setter name to the field's name, and its
storage reference to the field's value-slot name. It declares a destination
hole under the class root rather than spelling out every concrete builder edge
and rebinding operation. Automatic resolution realizes the declared relationship;
it does not infer the domain policy or make equal spellings imply intentional
sharing. Missing or ambiguous required candidates produce diagnostics. This
resolution is distinct from hygiene, which handles accidental collisions among
independent local bindings. [C7, C8, C9]

The author's motivation was to remove imperative binding steps from earlier
YIDL authoring: the author reports that declarative auto binding made the
language substantially easier for an LLM to generate. That is a practitioner
account of the design change, not a measured general advantage. The broader
LLM-authoring benefit remains a hypothesis. For a reader constructing a
generator, the practical model is a hierarchy of reusable composition recipes:
facts and matchers select behavior, contributions declare how it participates,
and the composition machinery resolves the specified connections. Following
those declarations into generated code still requires tracing several sources;
declarative authoring does not itself make the whole assembly immediately
obvious. [C7–C9, C21]

## 5. Worked selection example: from a fact to a policy

The following complete program uses the generic DDS interface, independently
of lifecycle, to select a required or defaulted resource:

```python
from yidl.generation.data_def_sys import DataDefinitionSystem, from_literal

dds = DataDefinitionSystem()
name = dds.property("Name", str)
defaulted = dds.property("Defaulted", bool, default=False)
field = dds.record("Field", name, defaulted)
fields = dds.collection("Fields", field, cardinality=dds.many, identity=name)
required = from_literal("required")
optional = from_literal("defaulted")

matcher = dds.matcher("Parameter")
source = matcher.input("field", fields)
matcher.default(required)
matcher.rule(
    name="defaulted",
    when=(source.prop(defaulted).eq(True),),
    resource=optional,
)
runtime = matcher.runtime()
a = runtime.resolve(field.record(name="count", defaulted=False))
b = runtime.resolve(field.record(name="label", defaulted=True))
assert a.resource is required
assert b.resource is optional
```

This example was executed during drafting. Here resources are literal values to
keep selection visible. In the canonical parameter-production fixture they are
Astichi resources, and a production carries `match.resource()` into parameter
facts associated with an owner-scoped initialization port. Ordering then yields
`count` followed by `label`, while an `init=False` field is filtered out. The
fixture connects schema, selection, derivation, and ordered assembly data;
merely templating two functions would not express that intermediate relationship.
[C3–C5, V2]

## 6. Lifecycle case study

### 6.1 Architectural before and after

The original lifecycle implementation already has abstractions. It includes
`LCKind` hierarchies, field specifications, helper parameter policies, getter
and setter tables, close hooks, transaction managers, and record snapshots.
Calling it simply “hard-coded” would obscure both its capabilities and the
actual change. Its central module coordinates kind semantics, decoration,
storage, injection, views, and runtime transactions through interconnected
Python machinery. [C1, C11]

The replacement relocates significant field variation into compiler inputs:

| Concern | Handwritten reference | YIDL lifecycle application |
| --- | --- | --- |
| Field meaning | Kind hierarchy and handler construction | Marker/harvester facts and schema variants |
| Policy selection | Kind and helper dispatch across tables | Matchers over field/default/dependency facts |
| Class construction | Handwritten decorator and state machinery | Phased class productions using reusable resources |
| Field execution | Generic records and selected handler tables | Generated properties and direct state-slot code |
| Transactions | Runtime transaction/state coordination | Generated participant methods plus ordinary manager library |
| Extension contract | Coordinated edits to runtime and tables | Family/matcher/phase contributions plus frontend updates where needed |

This is a redistribution of architectural responsibility, not the elimination
of imperative code. `lifecycle_core.yidl` defines the structural skeleton;
default-factory, managed, transient, owned, const/static, and local-store layers
extend it through the current inheritance chain. The final base assembles the
module. Feature resources still contain ordinary Python algorithms, and the
harvester and transaction manager remain handwritten support code. [C9, C11]

The harvester merges inherited lifecycle declarations, validates overrides and
factory signatures, and records class, field, and transaction-method facts.
Factory/default objects are passed into the generated class builder through
named keyword bindings. Derived default-factory facts make dependency arguments
and evaluation order available to assembly. The output defines a slotted state
class, facade classes, properties, and transaction participant methods. A main
facade owns the state and retains materialized secondary facades; state-to-facade
references are weak. Current and working facades are created on demand. Runtime
manager calls and user factories remain runtime costs. [C9–C11]

### 6.2 Mutable lazy fields as a feature composition

The current preferred marker is `lazy`; `static` is its exact function alias.
Both retain internal field kind `"static"`. The parity-fields fixture includes:

```python
mutable_number: int = lazy(default=42, mutable=True)
mutable_items: list[int] = lazy(
    default_factory=make_mutable_items,
    mutable=True,
)
```

Here `make_mutable_items(mutable_number)` records its argument and returns a
list containing that value. A fact with `Mutable == True` selects a setter
contribution through this actual YIDL excerpt:

```yidl
matcher LazySetterContributions(field: StaticFields) -> contribution {
    rule mutable when Mutable == True -> MutableLazySetter
}

extend production CoreClassProduction {
    phase lazy_setters after properties_static
        from field: StaticFields
        where FieldOwner == ClassId {
        apply lazy_setters using LazySetterContributions
    }
}
```

The selected `MutableLazySetter` targets `lazy_setter_body` inside the indexed
`StaticFieldProperty` instance. Its resource assigns through the selected state
slot and explicitly shares the enclosing setter's `state` and `value` names.
The three lazy property variants—unset, default value, and default factory—each
offer the same fallback setter hole. The fallback allows the first assignment
and otherwise raises. Insertion replaces that suite with unrestricted
assignment. Getter selection remains governed by the existing default/factory
matchers. [C13]

The resulting semantics are specific. With no constructor override or prior
assignment, the factory reads providers at first access and caches its result.
Changing `mutable_number` before first reading `mutable_items` affects that
first computation. Changing it afterward does not invalidate the cached list.
Assigning directly to `mutable_items` replaces its value without rerunning the
factory. Assignment before its first read bypasses the factory entirely.
Replacement through current or working facades is immediate and
nontransactional. The stored object's contents are not recursively frozen.
Neither transaction completion nor provider changes imply automatic
recomputation. [C13]

The canonical fixture checks source shape and runtime results in raw and
formatted output, including aliasing, repeated assignment, inheritance, and
factory call counts. During drafting its generated-class assertions passed
against both checked-in outputs. Fresh decorator generation of a smaller lazy
example failed in the current checkout, as detailed below. Thus the example
demonstrates source-level policy composition and artifact behavior, with a
present reproducibility qualification on the frontend path. [V3–V5]

### 6.3 Compatibility is a contract to delimit

This is an improved replacement aimed at simpler composition, not a demonstrated
strict behavioral superset of the original framework. The current decorator
does not chain user `__init__` or `__post_init__`. There is no generic generated
lifecycle `close` protocol. Binding fields use plain nontransactional storage
and intrinsic Python references rather than the original transactional,
explicit-reference-count semantics. The package also has an alternate
explicit-refcount support library; its presence does not make that the default
generated binding behavior. [C12]

Lifecycle `derived` cache invalidation, managed `initial_working`, and managed
sidecar field state are not exposed by current markers. Some original tests
were ported or normalized, while other cases have explicit deferred/rejected
status. Copied test names and skip explanations can preserve old terminology or
stale feature status. For example, a skip reason says local-store fields are
unimplemented even though a current layer and canonical fixture implement
them. Test counts cannot establish all original semantics or justify importing
the stronger promises of the old design summary into this paper. [C12, D1–D3]

Resource cleanup remains part of Pyrolyze through binding/effect deactivation,
subscription and resource-specific retirement, and explicit application paths.
Rollback of generated field state does not replace all teardown. Intrinsic
references and `__del__` do not guarantee prompt external cleanup across cycles,
Python implementations, or shutdown. A support-code comment promising immediate
teardown is not sufficient evidence for such a guarantee. [C12, D4]

### 6.4 Integration boundary

Pyrolyze's switchable context surface currently defaults to the monolithic LCM
path. That path already uses the extracted lifecycle library but retains
mirroring and manual publication machinery. A decomposed LCM path is the
ongoing migration target. Current integration documents separate holder
replacement from later manager unification and retain existing completion
boundaries. Integration is therefore neither absent nor complete. [C15]

The bounded shared-completion fixture observes that generated instances on the
same manager/key cannot complete independently: nested commit reduces depth,
direct child commit publishes both participants, and child rollback discards
both. These observations limit what a shared manager proves about isolation.
They do not establish savepoints, outer atomicity, or a general failure
containment scheme. The migration is an application of explicit boundary
contracts, and its unfinished state is part of the case study. [C15]

## 7. Evidence and evaluation

### 7.1 What was inspected and executed

This draft is based on the existing local checkout of four repositories,
including their dirty working state, on 2026-10-03. Current source and tests
take precedence over historical plans. The evidence index records repository
revisions, selected source hashes, claim locations, discrepancies, and exact
bounded checks. No product code, tests, historical documents, or goldens were
edited or regenerated for this paper. [V0]

The checks give deliberately different strengths of evidence:

| Observation | Result during drafting | What it establishes |
| --- | --- | --- |
| Filled Astichi fallback example | Passed | One structural composition and AST execution |
| Generic DDS resource matcher example | Passed | Default/rule selection over typed records |
| Canonical parity-fields generated-class assertions | Passed for raw and formatted checked-in outputs | Artifact runtime behavior for that fixture |
| Fresh lazy decorator, `auto` selecting `native-rust` | Failed at class build: missing `build_lifecycle_class` | Current generation path not reproduced |
| Same fresh lazy declarations, explicit `python` lower engine | Failed targeting a property contribution; missing `field_name` candidate | Python fallback does not resolve the present gap |
| Prior reported complete lifecycle suite | 267 passed, 46 skipped; not rerun here | Provenance supplied with the task, not a new measurement |

The failures were not diagnosed to a root cause and do not license a conclusion
that lazy policy semantics are wrong, that a particular engine alone is at
fault, or that the prior reported suite result was false. They prevent this
draft from claiming that its working dependency combination currently
regenerates the demonstrated lifecycle artifacts. Artifact execution and fresh
generation must both be part of a future reproducible release. [V1–V5]

Canonical goldens make output structure reviewable, while behavioral assertions
check what the output does. Narrow parser/matcher tests cover collisions,
ambiguity, filtering, ordering, and diagnostics. Neither golden equality nor a
passing behavior fixture proves general semantic preservation. Expected output
can encode a mistaken policy; review must inspect the domain contract as well
as generated code. [C16]

### 7.2 Three distinct performance questions

**Compiler-generation time** includes parsing YIDL definitions, resolving
concepts, and producing a reusable domain compiler/runtime. **Decorator or
class-generation time** includes harvesting declarations, deriving facts,
selecting and assembling resources, materializing AST, compiling/executing it,
and invoking the class builder. **Per-instance runtime** includes allocating
facade/state objects, initializing fields, resolving factories, accessing views,
and transaction/resource work. Moving policy to generation can reduce repeated
interpretation while imposing substantial startup cost. [C10, C17]

Historical performance documents illustrate this distinction, not a current
speed claim. `AstichiPerfAnal.md` reports 5.268 seconds of decorator work for
eight classes in an LCM import workload, including 4.597 seconds of assembly
and 0.660 seconds of executable-AST materialization. Its unprofiled import
observation is 5.72 seconds. The document predates subsequent performance work
and does not pin a full environment manifest. An earlier analysis dated
2026-05-20 concerns a different seven-field dataclass workload, reporting
roughly 23–24 seconds for source-emitting decorator assembly and an unresolved
8–23 second discrepancy between measurement approaches. These workloads and
conditions must not be merged into a speedup ratio. [C17]

Newer native handoff documentation reports a post-F6 eight-class sample with
one CPython AST construction per class and about 0.030 seconds in the
`copy_python_ast` counter. It explicitly treats that time as noise-sensitive,
not a guaranteed import-wall reduction. Current source includes lower-engine
selection and capability gates; an importable native extension alone does not
establish equivalent behavior or a measured speedup. [C17]

The lifecycle constructor comparison uses checked-in generated classes and
slotted dataclasses at group sizes 5, 10, and 15, each with equally many plain,
count, and factory-derived fields. The “derived” label in this microbenchmark
does not refer to the unsupported lifecycle derived-cache marker. Generation
cost is excluded from its timed loop. Moreover, the dataclass `__post_init__`
uses a loop with dynamic attribute access, while lifecycle factory lowering is
specialized. This is a comparison of those implementations, not an equal-code
lower bound or application-wide performance evidence. [C17]

No new throughput numbers are reported here. A reproducible evaluation should
first resolve the generation failures and pin source plus native binary state;
then measure all three stages separately, alternate baseline order, retain
individual repetitions, and report dispersion and cold/warm conditions.
Equivalent observable workloads and a carefully specialized handwritten
baseline are needed alongside the existing comparison. Application evaluation
must include transactions, views, factory patterns, memory, cleanup, and
end-to-end rendering. The evidence index gives documented entry points and
the gaps document prioritizes this work.

## 8. Related work and the bounded novelty question

**Generative programming.** Czarnecki and Eisenecker describe system-family
models and automated selection/assembly of components. YIDL continues that
tradition by representing variation as facts and selected resources. Its
contribution cannot be the broad idea of generating specialized systems from
domain models. The present comparison concerns how compiler facts, named
production phases, and scoped Python composition interact. [Generative
Programming](https://gsd.uwaterloo.ca/publications/view/86.html),
[Components and Generative Programming](https://gsd.uwaterloo.ca/sites/default/files/esec99.pdf).

**Feature-oriented composition.** AHEAD models step-wise refinement and
composition of feature increments. YIDL's mergeable feature layers are close
in motivation. Selection by facts and extension of named assembly phases give
this implementation a particular shape, but we have not established an
expressiveness or modularity advantage over AHEAD. Neither an algebraic
equivalence nor novelty follows merely from a different notation. [Scaling
Step-Wise Refinement](https://www.cs.utexas.edu/~schwartz/ATS/fopdocs/AHEAD-Theory.pdf).

**Language workbenches and model-driven engineering.** Fowler's workbench
account combines semantic models, languages, generation, and editing support;
Schmidt describes domain models and transformation machinery for managing
platform complexity. YIDL's compiler input is an executable semantic model in
this broad sense. It currently offers textual/programmatic authoring and
generated-code inspection, without demonstrating the integrated editor tooling
associated with a full workbench. [Language
Workbenches](https://martinfowler.com/articles/languageWorkbench.html),
[Model-Driven Engineering](https://www.dre.vanderbilt.edu/~schmidt/PDF/GEI.pdf).

**Staging and partial evaluation.** Jones, Gomard, and Sestoft explain
specializing a program given part of its input; Taha and Sheard's multi-stage
work makes staging explicit. YIDL separates domain compilation, declaration
specialization, and instance execution. It is reasonable to interpret the
architecture as staging known policy, but the current evidence does not show
that it is an automatic partial evaluator of the original lifecycle runtime,
nor that it provides MetaML's type-safety results. [Partial Evaluation and
Automatic Program Generation](https://studwww.itu.dk/people/sestoft/pebook/),
[author-maintained multi-stage publication list](https://www.cs.rice.edu/CS/PLT/Publications/MultiStage/).

**Hygienic macros and AST quotation.** Hygienic expansion addresses accidental
capture in generated syntax; Racket provides explicit syntax objects, scopes,
and phases. Astichi applies explicit composition scopes, demands, and structural
holes to Python snippets. Its contracts should be compared against that
literature, not presented as the invention of hygiene. We have not proved
equivalence to Scheme/Racket binding models or a typed quotation calculus.
[Hygienic Macro Expansion](https://doi.org/10.1145/319838.319859),
[Racket Syntax Model](https://docs.racket-lang.org/reference/syntax-model.html).

**Decorator and model compilers.** Python dataclasses already generate methods
from annotated fields. Pydantic separates collected model information from a
core schema consumed by its validation/serialization engine. These demonstrate
that declaration compilation and structured intermediate representations are
established techniques. YIDL's scope is a reusable vocabulary for building such
domain compilers; `yidl-lifecycle` is one application of it. No benchmark or
feature comparison here establishes superiority over either library.
[Python dataclasses](https://docs.python.org/3/library/dataclasses.html),
[Pydantic architecture](https://pydantic.dev/docs/validation/latest/internals/architecture/).

**Declarative mappings and transactions.** SQLAlchemy is prior art for both
declarative object mappings and coordinated transactional changes. Its
declarative API constructs table and mapper structures from class declarations,
using either a base class or a decorator. Its Session records changes across
mapped objects as a unit of work, flushes pending changes to the database, and
coordinates database commit or rollback. Flushing can occur before commit;
rollback commonly expires persistent object state so it can be reloaded. These
are established mechanisms for connecting declarations to runtime behavior and
managing changes across objects. [SQLAlchemy declarative mapping
styles](https://docs.sqlalchemy.org/en/20/orm/declarative_styles.html),
[Session basics](https://docs.sqlalchemy.org/en/20/orm/session_basics.html). [C22]

Lifecycle's transaction model instead organizes in-memory field state through
current and working facades. A field's transaction key assigns it to a group,
allowing fields on the same instance to participate in different groups. Each
key has its own active transaction, enlisted participants, and nesting depth;
completion can address a selected key or several keys. The current multi-key
manager processes groups sequentially, without establishing atomic completion
across them. Repeated begins for one key share a transaction with counted
nesting, whereas SQLAlchemy's explicit nested transactions can use database
savepoints. These differences concern state representation and completion
boundaries. The YIDL case study describes how declarations generate storage,
facades, and participant methods that cooperate with the handwritten manager;
it does not claim to originate unit-of-work transactions. These choices belong
to the lifecycle application rather than restricting YIDL's generator model.
A different concept could generate SQLAlchemy mappings and integration code,
or code implementing a different transaction policy. That is a possible
application, not an implemented and evaluated SQLAlchemy backend here. [SQLAlchemy
transactions and savepoints](https://docs.sqlalchemy.org/en/20/orm/session_transaction.html).
[C9, C11, C14, C15, C22]

The supportable position is therefore an exploratory architectural synthesis
with a substantial downstream application. A sharper novelty claim needs a
comparative example implemented in a close prior system, especially one with
feature layers, rule-driven generation, and explicit code bindings. [C18]

## 9. AI-assisted development and methods provenance

The architecture contribution and the development account answer different
questions. The first asks what the implementation makes explicit. The second
asks how assistance affected its construction. The practitioner account reports
significant AI involvement in model exploration, implementation, generated-code
inspection, testing, and revision, including discarded directions and human
disagreement with suggested abstractions. This is a retrospective account, not
a controlled causal study. No claim of better LLM understanding, faster
development, or reduced error rates has been measured here. [C1, C19]

During preparation of this draft, a Codex assistant selected and read local
implementation, reference, test, golden, and historical sources; retrieved
primary literature and official policies; ran the bounded checks listed above;
and drafted the manuscript and evidence documents. The checks used the existing
environment and in-memory execution, without regeneration or product edits.
Source artifacts and primary publications, rather than AI output, are the
evidence for technical claims. This is also an AI-assisted evidence-selection
process, so human review must check omissions and interpretations.

Before submission, this methods account needs the actual development tool/model
inventory and dates, preserved session or commit evidence, examples of accepted
and rejected suggestions, test and review practices, and the human decisions
that established domain semantics. Those details are not inferred from package
metadata or invented here. Named human authors must have substantive
contributions and accept responsibility for every claim and artifact. [C19]

On 2026-10-03, the official ACM authorship policy, updated May 14, 2026, was
checked through indexed official content; the canonical page denied direct
fetching. It distinguishes writing assistance, for which disclosure alone is
no longer required, from AI used in research and relevant artifact construction,
which requires a detailed methods account. Responsibility remains with human
authors. Official MMSys guidance reproduces the relevant policy text; its
conference-specific rules are not imported into Onward!. [ACM policy](https://www.acm.org/publications/policies/new-acm-policy-on-authorship),
[official reproduction](https://2027.acmmmsys.org/research-track.html).

The intended audience values exploratory implementations and substantial worked
examples, but still requires validation. The checked 2026 Onward! call specifies
double-blind review, 10-point SIGPLAN `acmart` formatting, a self-contained main
body of at most 13 pages initially, and PDF submission. Its 2026 submission
deadline has passed. This Markdown draft targets that audience, not an open
submission window; a future call must be checked afresh. [Onward! Papers 2026
call](https://2026.splashcon.org/track/splash-2026-onward--papers). [C20]

## 10. Limitations and open directions

The implementation has one substantial application, related object-model
fixtures, and a migration still exposing boundary issues. This is insufficient
to establish domain-independent usability. More explicit architecture can make
relationships inspectable while also adding indirection and a new language to
learn. Human comprehension and ease of LLM authoring are distinct questions;
the LLM-authoring benefit is retained as a hypothesis rather than an evaluation
commitment in this paper. [C9, C18, C19, C21]

Fact typing, identity policies, matcher diagnostics, and scoped assembly constrain
composition, but do not prove the domain model correct or generated programs
safe. Imperative operation bodies and runtime libraries can still introduce
hidden coupling. Same-manager/key completion is not participant isolation;
garbage collection is not a resource-retirement protocol; and current artifact
success does not repair fresh generation failures. [C12, C15, V3–V5]

Cross-language backends, self-hosting or Meta3/Meta-N descriptions of the
compiler, named concept containment, and FastAPI/protobuf-style applications
appear in the design log as future tests of the approach. The inspected system
generates Python. Native Rust implementation work on Astichi is a compiler
implementation choice, not a demonstrated Rust target language for YIDL domain
output. The proposals need target semantics, capability checks, boundary
contracts, and independent examples before becoming results. [C14]

## 11. Conclusions

YIDL and Astichi expose a workable architectural division: schemas and facts
describe a domain, matchers select policies and resources, derivations prepare
assembly data, concept extensions contribute feature behavior, and phased,
scoped composition produces inspectable Python. The lifecycle application makes
that division concrete. Mutable lazy storage shows a setter policy selected
and inserted without duplicating the lazy getter, while the broader package
demonstrates generated storage, facades, and transaction participation.

The evidence supports an exploratory compiler architecture and artifact-level
case study. It leaves reproducible fresh generation, sharper comparison with
prior work, broader-domain reuse, lifecycle integration, and measured human/AI
benefits unresolved. Those limits define the next experiments rather than
weakening the distinction between an implemented mechanism and a proposal.

## References

1. Krzysztof Czarnecki and Ulrich W. Eisenecker. *Generative Programming:
   Methods, Tools, and Applications*. Addison-Wesley, 2000. [Author laboratory
   record](https://gsd.uwaterloo.ca/publications/view/86.html).
2. Krzysztof Czarnecki and Ulrich W. Eisenecker. *Components and Generative
   Programming*. ESEC/FSE, 1999, pp. 2–19. [Author-hosted
   paper](https://gsd.uwaterloo.ca/sites/default/files/esec99.pdf).
3. Don Batory, Jacob Neal Sarvela, and Axel Rauschmayer. *Scaling Step-Wise
   Refinement*. IEEE Transactions on Software Engineering 30(6), 2004,
   pp. 355–371. [Author-hosted
   paper](https://www.cs.utexas.edu/~schwartz/ATS/fopdocs/AHEAD-Theory.pdf).
4. Martin Fowler. *Language Workbenches: The Killer-App for Domain Specific
   Languages?* 2005. [Author
   essay](https://martinfowler.com/articles/languageWorkbench.html).
5. Douglas C. Schmidt. *Model-Driven Engineering*. IEEE Computer 39(2), 2006,
   pp. 25–31. [Author-hosted paper](https://www.dre.vanderbilt.edu/~schmidt/PDF/GEI.pdf).
6. Neil D. Jones, Carsten K. Gomard, and Peter Sestoft. *Partial Evaluation
   and Automatic Program Generation*. Prentice Hall, 1993. [Author book
   site](https://studwww.itu.dk/people/sestoft/pebook/).
7. Walid Taha and Tim Sheard. *Multi-Stage Programming with Explicit
   Annotations*. PEPM, 1997. [Author-maintained publication
   list](https://www.cs.rice.edu/CS/PLT/Publications/MultiStage/).
8. Eugene Kohlbecker, Daniel P. Friedman, Matthias Felleisen, and Bruce Duba.
   *Hygienic Macro Expansion*. LFP, 1986, pp. 151–161.
   [Publisher record](https://doi.org/10.1145/319838.319859).
9. Racket project. *Syntax Model*. [Official
   reference](https://docs.racket-lang.org/reference/syntax-model.html).
10. Python project. *dataclasses — Data Classes*. [Official
    reference](https://docs.python.org/3/library/dataclasses.html).
11. Pydantic project. *Architecture*. [Official
    documentation](https://pydantic.dev/docs/validation/latest/internals/architecture/).
12. ACM. *Policy on Authorship*. Updated May 14, 2026. [Official
    policy](https://www.acm.org/publications/policies/new-acm-policy-on-authorship).
13. Onward! Papers 2026. *Call for Papers*. [Official
    call](https://2026.splashcon.org/track/splash-2026-onward--papers).
14. SQLAlchemy project. *Declarative Mapping Styles*, *Session Basics*, and
    *Transactions and Connection Management*. SQLAlchemy 2.0 documentation.
    [Declarative mappings](https://docs.sqlalchemy.org/en/20/orm/declarative_styles.html),
    [Session basics](https://docs.sqlalchemy.org/en/20/orm/session_basics.html),
    [Transactions](https://docs.sqlalchemy.org/en/20/orm/session_transaction.html).

Online sources checked 2026-10-03; SQLAlchemy sources checked 2026-10-04.
This first-pass bibliography verifies
publication identities and the bounded comparisons above; it is not a complete
novelty review. Retrieval limits are recorded in the evidence index.
