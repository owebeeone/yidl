# FieldSpec helpers × YIDL design gaps

This document is the companion gap register for
`dev-docs/FieldSpecYIDLDesignMatrix.md`.

Use the matrix for compact coverage signals. Use this document for the actual
gap analysis and remediation options.

Each gap entry includes:

- a tagged heading for stable reference
- the shortcoming
- recommendations
- one preferred recommendation
- notes on whether the gap is primarily frontend/grammar, codegen, or
  runtime/class-model

Tie-breaking should prefer consistency with:

- `pyrolyze.lifecycle` behavior
- `dev-docs/RuntimeExtractionPlan.md`
- the split YIDL design docs

## GAP-TG — transaction-group semantics still need completion details

Shortcoming:

`tx_group` and related multi-group semantics now have explicit ownership in the
split design docs, but the completion details remain thin. In particular,
visibility across groups and cross-group interaction rules are still open.

Recommendations:

1. Add an explicit transaction-groups section to
   `docs/YIDLRuntimeClassModel.md` defining visibility, isolation, commit order,
   and rollback behavior across groups.
2. Add a source/frontend note in `docs/YIDLFrontendDesign.md` describing where
   `tx_group` enters the harvested/spec model.
3. Leave `tx_group` implicit and rely on commit-path notes scattered across the
   docs.

Preferred:

1. Add the dedicated runtime/class-model section plus a short frontend note.

Reason:

This matches lifecycle more faithfully and reduces ambiguity in both codegen and
field-helper coverage. It is primarily a runtime/class-model completion gap,
with a small frontend/spec consequence.

Generated example fix:

- extend or annotate `example/generated_factory_sample.py` so group-aware commit
  behavior is either illustrated minimally or explicitly marked out of scope for
  the sample

## GAP-STATIC-CLASS-SURFACE — static/class-like helpers are weakly owned

Shortcoming:

`static` and `classvar` are not comfortably explained by the instance-centric
store/view/proxy model. The design currently reads as if instance layout is the
default answer, which leaves class-timed or class-scoped behavior underdefined.

Recommendations:

1. Add a dedicated class-surface subsection to
   `docs/YIDLRuntimeClassModel.md` explaining which helper kinds are instance
   backed vs class backed.
2. Expand `docs/YIDLFrontendDesign.md` to state whether these helpers are
   represented as ordinary transducers, special harvested metadata, or explicit
   non-v1 exclusions.
3. Treat `static` and `classvar` as deferred and keep the docs intentionally
   vague for now.

Preferred:

1. Add the explicit class-surface subsection and note the harvested/spec shape.

Reason:

These helpers are too central to leave as a fuzzy exception. This is mostly a
runtime/class-model gap with a secondary frontend/spec mapping gap.

Generated example fix:

- add a minimal note or sample fragment clarifying whether the generated sample
  currently excludes class-backed helpers or how they would be emitted

## GAP-INJECTABLE-REGISTRY — injectable factory/hook names are not centrally specified

Shortcoming:

The lifecycle reference has concrete injectable-name behavior (`self`,
`current`, `working`, `tx_group`, `previous`, initvar names), but the split YIDL
design docs do not yet define one authoritative registry of what names exist in
which contexts.

Recommendations:

1. Add a dedicated injectable-name registry section to
   `docs/YIDLFrontendDesign.md` and cross-reference it from
   `docs/YIDLCodegenDesign.md`.
2. Encode the rules only in code and leave the design docs high level.
3. Infer injectables ad hoc from transducer behavior during codegen.

Preferred:

1. Add the registry section in the frontend doc and cross-reference it from
   codegen.

Reason:

This is primarily a frontend/grammar/spec mapping issue that directly affects
codegen. Leaving it implicit will create inconsistent mapping rules.

Generated example fix:

- annotate the sample factory to show which captured locals correspond to
  injectable names and which are not part of the source-level injectable
  contract

## GAP-INIT-ORDERING — init ordering across field kinds is still too generic

Shortcoming:

The 3-phase init rule exists, but the design still does not fully specify
global ordering across published, working, hidden, and instance-homed concerns
for cases like `initvar`, `default_factory`, `working_default_factory`, and
derived/local-store interactions.

Recommendations:

1. Add a phases-by-field-kind table to `docs/YIDLRuntimeClassModel.md`.
2. Add a companion source/spec note in `docs/YIDLFrontendDesign.md` if some of
   this ordering must be expressed or constrained in YIDL source.
3. Leave ordering as “declaration order plus best effort” and let codegen own
   the details informally.

Preferred:

1. Add the phases-by-field-kind table, with a frontend note only where source
   expression is required.

Reason:

Lifecycle behavior depends heavily on ordering, and this is exactly the kind of
gap that can become a grammar/source-mapping problem if left vague. It is
primarily a runtime/class-model gap with possible frontend consequences.

Generated example fix:

- make the sample’s init order and dependency assumptions more explicit, either
  in code structure or short comments

## GAP-COMMIT-PIPELINE — validators, order keys, hooks, and writes need one explicit pipeline

Shortcoming:

Commit-sensitive features are individually visible, but the design still lacks
one explicit commit pipeline covering:

- ordering keys
- validators
- before/after hooks
- store writes
- rollback mirror behavior
- evict-last interaction

Recommendations:

1. Add one explicit commit pipeline section/table to
   `docs/YIDLRuntimeClassModel.md`.
2. Add a codegen note in `docs/YIDLCodegenDesign.md` about how that pipeline is
   emitted deterministically.
3. Keep these as separate helper-specific notes and rely on implementation
   convention.

Preferred:

1. Add the explicit runtime pipeline and the codegen emission note.

Reason:

Lifecycle is already a strong tie-breaker here: a deterministic pipeline is the
only safe direction. This is both a runtime/class-model and codegen gap.

Generated example fix:

- add or annotate sample commit logic so the order of validation, writes, and
  cleanup is explicit rather than implied

## GAP-BINDING-OWNED-MERGE — binding and owned semantics are too compressed

Shortcoming:

The matrix can map `binding` and `owned` onto similar design areas, but the
difference between them is still too compressed to count as well-covered. The
evict-last rule exists, but ownership-vs-binding merge behavior is still thin.

Recommendations:

1. Add a dedicated subsection in `docs/YIDLRuntimeClassModel.md` describing the
   runtime semantics of binding/owned-style fields and how they differ.
2. Add a codegen note in `docs/YIDLCodegenDesign.md` about how these semantics
   lower into emitted commit/update steps.
3. Treat `owned` as an implementation alias of `binding` until later.

Preferred:

1. Add explicit runtime semantics and codegen lowering notes.

Reason:

Lifecycle distinguishes them enough that collapsing them too early is risky.
This is mostly a runtime/class-model gap with supporting codegen consequences.

Generated example fix:

- extend the sample or a nearby companion sample fragment to show one
  resource-sensitive update path with explicit evict-last staging

## GAP-ANNOTATION-DRIVEN-BEHAVIOR — annotation-driven compare and related ambient rules are under-specified

Shortcoming:

Some lifecycle behavior is not purely helper-parameter-driven. Annotation-driven
compare behavior and similar ambient semantics are easy to miss if the design is
read as “transducers only.”

Recommendations:

1. Add a short ambient-semantics section to `docs/YIDLFrontendDesign.md`
   clarifying which annotation-driven behaviors are harvested.
2. Add a cross-reference in `docs/YIDLCodegenDesign.md` for how harvested
   ambient semantics reach generation.
3. Ignore annotation-driven behavior until later and rely only on explicit
   helper params.

Preferred:

1. Add the ambient-semantics note and the codegen cross-reference.

Reason:

Lifecycle uses these behaviors, and they are exactly the kind of source-mapping
gap that can otherwise vanish from coverage. This is primarily a
frontend/grammar/spec gap.

Generated example fix:

- annotate the sample input assumptions so it is clear which behaviors come from
  explicit helper params and which would come from harvested ambient metadata

## GAP-MRO-MERGE — field-spec MRO merge rules are too lightly documented

Shortcoming:

The harvester boundary mentions MRO, but the design does not yet say enough
about how inherited field-spec attributes compose or override one another.

Recommendations:

1. Add explicit MRO-composition rules to `docs/YIDLFrontendDesign.md`.
2. Add a short generator/codegen note only if MRO composition constrains emitted
   structure.
3. Leave MRO merge as an implementation detail of the harvester.

Preferred:

1. Add the explicit frontend rule, with codegen notes only if needed.

Reason:

This is mostly a harvested/spec-mapping issue, and lifecycle already provides a
behavioral reference for tie-breaking.

Generated example fix:

- no major sample expansion required; a note is enough unless the sample is used
  to demonstrate inheritance directly

## GAP-COMBINATORIAL-PRECEDENCE — cross-helper interactions are not yet first-class

Shortcoming:

The matrix identifies several multi-helper interaction risks, but the design
docs still mostly describe helpers in isolation. That creates ambiguity in
precedence, ordering, and combined semantics.

Recommendations:

1. Add an explicit precedence/ordering subsection to
   `docs/YIDLRuntimeClassModel.md` and reference it from
   `docs/YIDLCodegenDesign.md`.
2. Extend the grammar/frontend only if some combinations require explicit source
   declarations such as dependencies or restrictions.
3. Leave combinations to implementation-defined behavior until later.

Preferred:

1. Add explicit precedence/ordering rules first; extend the frontend only where
   the source must express intent.

Reason:

Most of these look like runtime/class-model ambiguities first, not grammar
features by default. But some may become grammar gaps if dependency expression
is required.

Generated example fix:

- add or annotate a small combined-case example where ordering matters, or
  explicitly state that the sample remains single-composition-only
