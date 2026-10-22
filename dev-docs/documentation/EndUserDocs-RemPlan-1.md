# End-user documentation remediation — round 1

Date: 2026-10-23. Status: **one bounded correction implemented and verified;
independent acceptance pending**.

## Authority and reviewed object

The operator requested accuracy and fitness-for-purpose review of the delivered
end-user documentation, specifically early vocabulary and a general architecture
overview before relying on a large example. They subsequently instructed work
to continue after the conversation closed.

Initial review object: `e98a22cc987342e1326384ee77cac6198b8bc647`, full docs
range from `43dd01b04f012d6e5877b88e9442461c38447a37`.
[Consistency](EndUserDocs-ReviewConsistency.md) returned NO-GO with two P2 and
one P3; [Safety](EndUserDocs-ReviewSafety.md) returned NO-GO with one P2 and
three P3. Both reports are filed verbatim, including the Safety report's original
transport prefix. Neither reviewer saw the other's current-round report.

There is independent convergence on two roots: the beginner route reaches full
machinery before its conceptual foundation, and the outside-checkout command
retains paths that fail after the stated directory change. The latter is P2 in
the merged gate despite the second axis's lower severity. These are two blocking
roots, not three separate defects. Three additional bounded nonblocking roots
concern excerpts, option help/defaults and cleanup guidance.

## Deliverable and component boundary

Produce one cohesive YIDL documentation patch. Allowed components: public prose,
README/navigation, a concise beginner architecture introduction or equivalent
reuse of existing pages, tutorial example help text, excerpt selections/hashes,
and narrowly necessary docs verification/evidence. Keep the CPython 3.12+
minimum wording and distinguish the exact historical executed environment.

Do not change compiler/runtime behavior, package metadata, generated product
bases, dependencies, adjacent repositories, historical evidence or archive
references. Existing source examples remain authorities; no new generator
feature, CLI, packaging repair, native work or universal support claim is needed.
No template/framework migration or general documentation redesign is authorized.

The current model and pipeline pages are useful material to reuse. The correction
must satisfy the reader outcomes through actual reading order and explanation,
not merely add another optional link or glossary. Preserve a short direct route
for experienced readers. No particular new filename or diagram is prescribed.

## Disposition and closure map

| Original finding | Disposition | Closure check |
| --- | --- | --- |
| Consistency P2-1: unexplained architecture before full example | Fix beginner foundation and route; same correction as Safety P2-1. | From README and home, before full source, explain purpose/capabilities, author inputs, YIDL/Astichi/application responsibilities, both generated products, facts versus instance values, and preparation/generation/execution stages. Recheck rendered primary navigation and tutorial entry. |
| Safety P2-1: recommended route assumes generator model | Fix through the shared beginner foundation above. | Repeat the original cold route and simple extension-authority decision; definitions and relationships must precede their use, without private developer notes. |
| Consistency P2-2: external-directory command uses checkout-relative paths | Correct the literal procedure and working-directory context; same root as Safety P3-1. | Execute the exact public steps in a fresh external directory using installed packages, no ambient sibling/PYTHONPATH assistance; verify expected observations and confined outputs. |
| Safety P3-1: external-directory path mismatch | Close through the shared path correction above; merged severity P2. | Preserve usable interpreter access across the directory change and call the copied script at its actual location. |
| Consistency P3-1: excerpt boundaries omit promised selection/result evidence | Extend pinned semantic units and refresh their excerpt hashes, preserving exact owner revisions. | Existing provenance checks pass; rendered Lifecycle matcher includes its selection/body, and the evaluated-field excerpt includes both original records and extracted tuple assertions. |
| Safety P3-2: tutorial options lack discoverable defaults/effects | Add meaningful help or adjacent command reference with output location, default scenario and switch behavior. | Inspect help cold; effects/defaults and current-directory-relative output must be clear without reading parser source. A narrow help check suffices; no duplicated generator success tests. |
| Safety P3-3: no cleanup lifecycle | Add bounded cleanup guidance beside first-use creation, distinguishing generated/environment artifacts from authored source. | Demonstrate how to remove only the tutorial experiment while retaining authored YIDL/Python inputs. No new cleanup/uninstall product command. |

Every finding has one disposition. Included P3 corrections are part of this
single bounded documentation patch, not new work packages. Contested findings
need an evidence-based written disposition. The author cannot self-close findings.

## Verification, re-review and landing

1. Read the full reports and controlling brief/plan. Record changed components
   before editing. Preserve original reports/prompts and old evidence manifests.
2. Revise the beginner exposition and navigation against actual existing
   semantics; improve the tutorial's scaffolding before large listings.
3. Validate the exact corrected external procedure, help and cleanup with
   disposable output, the existing provenance checker, strict site/link/search
   checks and applicable existing example/canonical checks. Do not broaden the
   qualified backend/Python/platform claim. Add separately identified remediation
   evidence rather than overwrite historical execution records.
4. Return one uncommitted patch, exact paths, results and limitations. The lane
   owner settles one new committed review tuple using the existing scoped GWZ
   commit authorization. The author performs no Git mutations or publication.
5. Re-verdict each axis's original counterexamples on the corrected tuple with
   prior-finding closure tables and changed-range analysis. Local exposition,
   navigation, path and help corrections retain product semantics; any materially
   changed shared interface/architecture, authority or compatibility contract
   requires replacement reviewers under the review-loop rule. Exactly two
   reviewers per revision; no third Surface reviewer.

Initial full review: one revision, two axes. First remediation round: one of at
most two. Acceptance remains NO-GO until the relevant reviewers verify closure
of both blocking roots. No site deployment, tag or registry release follows
from docs acceptance. The earlier commit/push request applies to reviewable docs
and audit evidence, not publication of an unaccepted correction as a release.

The [returned patch and evidence](EndUserDocs-Remediation-1.md) supply the
literal external-directory/cleanup execution, revised public help, complete
pinned excerpts, rendered beginner route and existing example/site checks.
These support re-review without changing either original report. No product
semantics, existing option actions/defaults, dependency or platform contract
changed. Local prose/navigation/interface presentation corrections retain the
original review premises; use focused re-verdicts by the original two reviewers.
The author has not self-closed findings or granted acceptance.
