# Research gaps and next evidence

For [paper-draft.md](paper-draft.md), prepared 2026-10-03. This list requests
evidence, not product edits, submission, contact, or publication. Claim and
validation IDs refer to [evidence-index.md](evidence-index.md).

## Required before a submission-ready paper

1. **Reproducible generation (V4/V5).** Resolve the fresh lazy-decoration
   failures without assuming a root cause from this draft. Ambient
   auto/native-rust lacked `build_lifecycle_class`; explicit Python failed a
   `field_name` binding candidate. Pin dirty source, generated-base provenance,
   dependencies, native binary identity/capabilities and engine selection.
   Demonstrate fresh generation, exact golden comparison, and behavioral checks
   on the same pinned state. V3 artifact execution alone is insufficient.

2. **Novelty comparison (C18).** Implement one concrete example in a close prior
   framework, especially AHEAD or another feature/rule-based generator with
   explicit code bindings. Compare fact derivation, specialization, feature
   collision/override contracts, phase ordering, diagnostics and scope hygiene.
   Identify the smallest defensible new contribution. A vocabulary change and
   combined implementation do not establish a new paradigm by themselves.

3. **Composition semantics (C4/C6/C7/C8).** Write a compact semantic account of
   concept closure, diamond identity, computed filters, selector precedence,
   contribution/operation overlap handling, phase-context replacement, and
   fallback binding scope. Audit which contracts have negative tests and which
   remain undocumented. Do not generalize resource-matcher overlap rejection
   to all matcher types or claim commutativity, hygiene soundness, or semantic
   preservation without additional evidence.

4. **Lifecycle contract (C12/C15).** Create an accepted current-versus-original
   semantic matrix from markers, resources, active tests and application
   boundaries. Separate intentional differences from unsupported/deferred
   features and defects. Include init/post-init, binding/reference ownership,
   close/deactivation, lazy policy, derived cache, initial_working, sidecars,
   transaction tokens, hook failures and shared completion. Stale copied skip
   strings cannot supply this matrix. Record the exact integration checkpoint
   and remaining scaffolding; manager unification is not complete.

5. **Evaluation and performance (C17).** Use the three-stage plan in the evidence
   index after generation is reproducible. Preserve raw repetitions and all
   configurations; alternate order and avoid deadline truncation. Compare
   equivalent behavior and a similarly specialized baseline. Include startup,
   generated size, memory, transactions and resource lifetime, not only
   constructor throughput. Historical numbers need full source/environment
   manifests or must remain historical observations.

6. **AI methods provenance and human ownership (C19/C20).** Recover tool/model
   versions, use dates, representative sessions, design decisions, rejected
   suggestions, coding/testing/review involvement, and evidence of substantive
   human contributions. Human authors must verify all technical and bibliographic
   claims, choose authorship/affiliations, and approve the final work. The
   current ACM research-methods requirement applies to significant AI-assisted
   implementation, regardless of writing-assistance disclosure rules.

## Experiments that would strengthen the architecture argument

7. **Independent domain (C9/C14).** Build a bounded second domain whose facts and
   policies differ materially from object/lifecycle fields. Show reusable core
   mechanisms, any core changes, domain-specific algorithms, and limitations.
   FastAPI/protobuf examples in the log are proposals, not results. A
   cross-language target or self-hosting exercise is optional future work, not
   a prerequisite disguised as implemented evidence.

8. **Change isolation and usability (C1/C19).** Record comparable maintenance
   tasks against the old and generated architectures: edits required, contract
   violations, review burden, comprehension and regressions. Treat human
   usability and LLM authoring as distinct questions. The auto-binding
   motivation is attributed practitioner evidence (C21); its broader benefit
   for LLM authoring remains a hypothesis, outside this paper's evaluation
   commitment. The five-week account does not itself establish improved
   productivity or that LLMs understand YIDL better.

9. **Artifact and venue readiness (C16/C20).** Produce a self-contained,
   anonymizable artifact with clean reproducible dependencies, source/golden
   checks and bounded runtime examples. Expand the primary-literature review;
   retrieve and read the staging/hygiene texts currently limited by access.
   Check the intended future Onward! call and current ACM policy again,
   then format and assess page count. The 2026 deadline has passed. No
   submission is authorized by this drafting task.

The strongest present claim is an inspectable implementation of fact-driven
selection and phased, scoped Python assembly, demonstrated through a
substantial lifecycle package and canonical artifacts. Fresh generation,
comparative novelty, generality, performance and AI benefits remain separate
evidence obligations.
