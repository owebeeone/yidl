# End-user documentation review checkpoint

Date: 2026-10-23. Status: **initial dual review NO-GO; first bounded
documentation correction implemented and verified, independent re-verdicts pending**.

## Operator authority and boundary

The operator requested a review cycle of the delivered documentation covering
technical accuracy and fitness for end users. Readers will not know YIDL or its
capabilities. Terminology must be introduced early, and readers need a general
architecture overview before the recommended installation-to-large-example
route depends on unexplained concepts. This augments the earlier plan's reader
outcomes; it does not authorize compiler, metadata or dependency implementation.

The review and any bounded remediation may change public YIDL documentation,
navigation, narrowly necessary examples/docs tooling and associated evidence.
Runtime/compiler behavior, generated product bases, adjacent repositories,
workspace metadata, registry/site release and archive/history reference repair
remain outside scope. Astichi Python 3.11 remains a proposal by explicit user
direction. The earlier file-view navigation concern was resolved by using the
served browser preview; no link defect is presumed from that report.

## Settled object

- YIDL HEAD: `e98a22cc987342e1326384ee77cac6198b8bc647`.
- Full delivered documentation range:
  `43dd01b04f012d6e5877b88e9442461c38447a37..e98a22cc987342e1326384ee77cac6198b8bc647`.
- Initial documentation commit:
  `8bf33765868d9c2e50476fc7a1698c3f0b2c4f08`, followed by the three-file Python
  minimum wording correction at the reviewed HEAD.
- Reference compiler/runtime bytes match
  `ee5ded0854aa5b1fc0ddfa7213b765009b63bb95`. New installed-example evidence
  uses CPython 3.12.12 and published Astichi 1.1.3 with explicit Python selection.
  Declared Python 3.12+ is distinct from that exact executed tuple.

The controlling documents at the reviewed HEAD are
`dev-docs/YidlDocumentationPlan.md`, `dev-docs/YidlDocShortcomings.md`, and the
creation brief `dev-docs/documentation/Review.md`, supplemented by the direct
operator reader-outcome requirements above. The earlier plan GO does not accept
the delivered pages. Existing evidence and inventory records are inputs, not
substitutes for independent accuracy and end-user usability assessment.

## Review process

Dual gate: a user-facing documentation surface and its executable guidance.
Exactly two fresh peer-blind reviewers assess the same committed object:

- Consistency: technical accuracy, contracts, examples and evidence boundaries.
- Safety, with Surface duty: cold end-user reading route, terminology,
  architecture, task completion and harmful misunderstandings.

Both independently check original requirement provenance, necessity and component
authorization. Both verify YIDL HEAD at start and end. Only lane-owner review
documents may appear as new YIDL working files during review; concurrent cache,
Undoable and workspace work is excluded.

Canonical review-loop prompts are filed as
[Consistency](EndUserDocs-PromptConsistency.md) and
[Safety](EndUserDocs-PromptSafety.md). Their SHA-256 values are respectively
`8434ef331da6edb5a6a1cf83627908492799014307550eec3c5a3d181a38e4a4`
and `7623f3384e53c3b317953312aa3db54f44ea786e09b425d298b0e451a4a7a4b4`.

Reviewers inspect sources and existing local rendered pages without source/Git
changes, execution of examples, tests, builds or installs. They distinguish
source-traced tasks and reported implementation evidence from independently
executed verification. No third Surface reviewer is permitted.

## Initial verdicts and remediation

[Consistency](EndUserDocs-ReviewConsistency.md) returned **NO-GO**, two P2 and one
P3. [Safety](EndUserDocs-ReviewSafety.md) returned **NO-GO**, one P2 and three P3.
Reports are filed verbatim; both verified the same starting/ending HEAD.

Both independently identified the same two roots: the primary novice route uses
the model before teaching it, and the outside-checkout instructions retain
checkout-relative paths. The second root is P2 in the merged verdict despite
the Safety axis assigning P3. The other three roots are nonblocking excerpt,
help/defaults and cleanup gaps. No implementation defect or dependency project
is required to remedy them.

[Remediation round 1](EndUserDocs-RemPlan-1.md) maps every original finding to one
disposition and closure check in a single bounded documentation patch. Acceptance
is **NO-GO** while either blocking root remains open. Original reviewers must
verify their counterexamples; the author cannot self-close. P3-only findings
are nonblocking. The two-remediation-round cap and architectural-root stop apply.
No public deployment or release follows merely from a successful site build.

## First correction returned for settlement

The [author's remediation response](EndUserDocs-Remediation-1.md) maps every
original finding and provides separately identified literal-walkthrough,
example, rendered-route and help evidence. The beginner route now introduces
model and stages before installation/full tutorial; the corrected external
directory and cleanup instructions were executed with installed packages.
Excerpt provenance, example/canonical and strict site checks are reported.

The patch changes prose/navigation, pinned excerpt boundaries and the tutorial
example's help presentation only. Existing option names/actions/defaults and all
compiler/runtime/metadata bytes remain unchanged. This is a local correction of
the reviewed learning/interface presentation, not a new product architecture,
language contract or platform premise. The original two reviewers will recheck
their exact counterexamples, closure tables and changed range on a new committed
tuple. These implementer results do not self-close any finding.
