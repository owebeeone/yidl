# YIDL Architecture Position

## Purpose

YIDL V1 exists to replace the handwritten lifecycle implementation with
generated specialized Python while keeping the underlying architecture broadly
usable for other decorator/compiler-style systems.

The immediate forcing use case is `pyrolyze/lifecycle.py`: it has reached a
complexity and performance ceiling. New behavior tends to add more coupling to
one large runtime module, and construction paths remain too generic for
high-rate object creation and teardown. YIDL should move that complexity to
definition time and emit direct, readable, class-specific runtime code.

## Core Thesis

YIDL is not only a template IDL. It is a concept-driven compiler framework.

The core shape is:

```text
concepts
-> typed facts
-> resource declarations
-> matcher selection
-> productions
-> operations
-> specialized generated output
```

Templates are important, but they are not the center. Concepts, facts, and
resources are the center.

## Core Model

YIDL's reusable compiler vocabulary is:

- `property`: typed semantic column
- `record`: fact shape
- `family`: open union of related record variants
- `collection`: fact table
- `resource`: generated/source-emittable value
- `matcher`: conditional selector over facts, usually selecting resources
- `production`: derivation rule that writes new facts from existing facts
- `operation`: materialization or compiler pass over collections/resources
- `concept`: reusable package of schema, resources, rules, and operations

This model is deliberately fact-oriented. It should describe the semantic data
that drives generation before materializing Python code.

## V1 Forcing Use Case

The lifecycle implementation is the first serious validation target.

YIDL V1 should make it possible to express lifecycle behavior as concept facts
and resources rather than as one large hand-maintained Python control surface.
The generated lifecycle classes should use direct specialized code:

- direct slots and state assignments
- direct constructor paths
- direct property bodies
- direct commit/rollback/cleanup paths
- precomputed transaction key metadata
- no reflection or generic field interpretation in hot construction paths

The current lifecycle runtime proved the semantics. YIDL should make those
semantics maintainable and fast.

## Mechanism Vs Meaning

The core architecture line is:

```text
YIDL core owns mechanisms.
Concept packages own domain meaning.
```

The core should not know what a `ManagedField` is. But the core must provide
enough mechanisms for a lifecycle concept to define managed fields cleanly.

Generic mechanisms include:

- schema families and extension
- resource declaration and composition
- resource-valued expressions
- matchers
- productions
- ordered operation assembly
- diagnostics
- source provenance
- generated-code materialization

Lifecycle meaning includes:

- managed/current/working field semantics
- transaction keys
- current and working facades
- commit and rollback behavior
- initvar behavior
- lifecycle hook names and ordering

Some mechanisms may first appear because lifecycle needs them. That is fine.
The test is not whether multiple domains already use the mechanism. The test is
whether the feature is a general way to define, derive, route, or assemble
compiler facts/resources rather than a hard-coded shortcut for one lifecycle
behavior.

## Resource Flow

Resources are first-class data.

Every place that consumes a generated resource should consume a resource
expression, not a named-resource-only reference.

Resource expressions include:

- declared resources
- imported resources
- matcher-selected resources such as `match.resource()` in matcher-result
  contexts
- resource-valued fields previously written by productions

Matchers do not own all resources. A matcher is a selector over facts. It
chooses among resources, and productions can route the selected resource into
later collections for operations to consume.

## Concept Composition

V1 primarily uses merge-style composition.

`extends` should mean that one concept contributes schema, resources, matchers,
productions, and operations into the same semantic graph as another concept.
This is already a powerful abstraction: it allows later concepts to add new
variants, policies, resources, and generation behavior without rewriting the
base concept.

Containment is a likely future direction, but it is not required for V1.
Containment would let a concept own a named sub-concept and wire inputs/outputs
between subgraphs. That is useful for larger compiler systems, but merge is the
minimum composition operator needed to replace lifecycle.

## Generality Checks

Lifecycle is the forcing use case, but YIDL design should be checked against
nearby domains to avoid lifecycle-specific core architecture.

Useful comparison domains:

- datatrees and hierarchical constructor generation
- Pydantic-style validation/model compilers
- SQLAlchemy-style mapping compilers
- sdax and dependency-discovery async execution graphs
- dependency-injection resolver compilers
- XML/DTD and binary parser/serializer compilers
- C++ binding descriptor compilers
- parser-generator plus semantic/tooling layers

These systems share the same broad shape:

```text
author declarations
-> harvested facts
-> derived facts
-> selected resources
-> specialized runtime/API/code/config output
```

Datatrees is a useful secondary design check because it is close enough to
lifecycle to keep the model grounded, but different enough to expose accidental
lifecycle assumptions.

## Performance Position

YIDL should keep a hard split between definition-time richness and runtime
specialization.

Definition time can use rich generic machinery:

- concepts
- fact graphs
- matchers
- productions
- operation planning
- diagnostics

Generated runtime output should be boring and direct:

- stable function signatures
- slotted state where appropriate
- direct attribute access
- direct assignments
- precomputed ordering
- no hot-path reflection
- no generic metadata interpreter unless explicitly requested

This is one of the main reasons YIDL exists. It should offer framework-level
ergonomics while emitting code that looks closer to careful handwritten Python
for the specific declared case.

## Astichi Boundary

Code stitching is the hard part of this architecture.

YIDL should not become a string-template framework. Generated resources should
flow through Astichi-backed values so composition can preserve:

- hygiene
- imports
- source provenance
- `keep_names`
- holes and edge bindings
- readable emitted Python

YIDL is the concept/fact compiler. Astichi is the code materialization engine.

## Design Guardrails

1. Do not hard-code lifecycle semantics in YIDL core.
2. Do not make the core too weak to express lifecycle cleanly.
3. Keep resources first-class and routable through matchers, productions, and
   operations.
4. Keep concepts as the home for domain meaning.
5. Prefer generated specialized code over runtime interpretation on hot paths.
6. Keep source provenance and diagnostics as first-class compiler concerns.
7. Treat merge composition as V1's core composition model; defer containment
   until the merged model is proven.
8. Use secondary domains, especially datatrees, as architecture checks.

## V1 Success Criteria

YIDL V1 is successful when:

1. a meaningful lifecycle subset is expressed as concepts, facts, and resources
2. generated lifecycle code passes parity tests for that subset
3. generated construction paths are materially faster than the generic runtime
4. adding a lifecycle behavior lands as a concept/resource/rule contribution,
   not as another branch in a central runtime monolith
5. the core mechanisms remain recognizable as useful outside lifecycle

The long-term vision is broad, but V1 should prove it through lifecycle.
