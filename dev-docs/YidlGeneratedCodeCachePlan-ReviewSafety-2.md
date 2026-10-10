# YIDL Generated Code Cache Plan — SAFETY Review

**Review object:** `yidl/dev-docs/YidlGeneratedCodeCachePlan.md`, controlling proposed DRAFT, and the two documentation-index links. Round 2 replacement Safety review.

**Exact baseline tuple:**
- YIDL: `1731f1de64422463356201aa65b4925b97b752c9`
- YIDL Lifecycle: `c2502f1a7a565624f20cf930fde92f581b123e9f`

**Date:** 2026-10-10  
**Independence:** Independent, adversarial, read-only. Prior-round filed reports and remediation plan were read; no current-round report from the other axis was requested or read. Pyrolyze working-tree changes and runtime implementation acceptance were excluded.

**Verdict: GO** for the proposed plan only. Open severity counts: P0: 0; P1: 0; P2: 0; P3: 0. Inherited Safety P2-1 is closed at the document-review level. This verdict does not accept an implementation, default activation, performance claims, or an API freeze.

**Report filename:** `YidlGeneratedCodeCachePlan-ReviewSafety-2.md`

## Prior-finding closure table

| ID | Disposition claimed | Verified on corrected text | Status |
| --- | --- | --- | --- |
| Safety P2-1 | Require coherent immutable producer provenance; bypass editable/source/unverifiable installations; invalidate lost epochs and prohibit publication under an old identity. | Independently retraced both original sequences. Fingerprint-then-replacement cannot publish replacement code under the original identity under lines 70–91. Already-loaded-old-module/new-disk cannot establish provenance by rehashing or package labels under lines 77–89. Both sequences are explicit future acceptance cases at lines 210–212. | Closed for the plan; implementation proof remains required. |

This fresh reviewer replaces the previous same-axis reviewer. Closure is based on retracing the original counterexamples, not adopting the remediation author's conclusion.

## Changed-range analysis

Compared YIDL `a3222bb44e2a5709dde9a680bca1ff6ab62eba96` with the reviewed revision using pinned `git diff`.

The operative plan changes are:
- Former lines 62–70 become current lines 62–94: process-lifetime dependency hashing is replaced with verified immutable producer epochs, explicit admission restrictions, loaded/deferred dependency provenance, and publication/hit checks.
- Three acceptance rows are added at current lines 210–212 for replacement, already-loaded dependency divergence, and unverifiable installations.

The two documentation-index links are unchanged. Lifecycle's revision is unchanged. The commit additionally files prior review evidence, remediation, and prompts; those are not runtime changes.

The amendment changes cache admission and compatibility assumptions, justifying fresh reviewers. It narrows acceleration eligibility without narrowing ordinary generation support: uncertain installations must continue uncached. No change outside the stated disposition introduced a concrete Safety defect. **New architectural root causes identified: none.** The inherited root remains a bounded correction, not a redesign finding.

## 0. Evidence base

Inspection used only permitted read commands. Repository bytes were read with `git -C <repo> show <exactSHA>:<path>`, optionally numbered or selected with `nl` and `sed`. No files were modified, no git mutations occurred, and no builds or tests ran.

At both start and end:
- `git -C yidl rev-parse HEAD` returned `1731f1de64422463356201aa65b4925b97b752c9`.
- `git -C yidl-lifecycle rev-parse HEAD` returned `c2502f1a7a565624f20cf930fde92f581b123e9f`.

Evidence read:
- Process `review-loop/SKILL.md` and canonical `references/review-prompt-template.md`.
- Workspace `AGENTS.md` and both repositories' pinned `AGENTS.md`.
- YIDL plan, complete text; particularly lines 61–97, 101–132, 137–167, and 202–218.
- Filed prior Safety and Consistency reports and `YidlGeneratedCodeCachePlan-RemPlan-1.md`.
- YIDL `YidlCodingRules.md`, complete text; `YidlDesignSummary.md:897–920,1039–1048`.
- YIDL `dev-docs/README.md:16–18`; Lifecycle `dev-docs/README.md:21–24`.
- Lifecycle `lifecycle.py`, including harvesting, compilation, execution, binding, lazy generation import, and exception boundaries at lines 35–65, 77–126, and 167–180.
- Lifecycle `lifecycle_harvester.py:31–205,295–410,548–666`.
- Lifecycle `_generated_lifecycle_base.py`, imports, builder templates around lines 3091–3123, transaction contributions around 3542–3659, and assembly entrypoints at 4834–4860. Long generated lines caused output truncation; no conclusion relies on unread portions.
- YIDL `data_schema.py:1672–1843`, package initializer, and `pyproject.toml`.
- `git diff` of the plan and YIDL index between the prior and current revisions; commit-wide `git diff --stat`.

External documentation and unrelated project changes were not inspected. Timing statements remain unverified motivation.

## 2. Invariant analysis

**Producer provenance: original replacement attack fails under the amendment.**  
The original sequence fingerprints G1, imports G2 on a miss, publishes under D1, restores G1, then obtains a poisoned hit in a fresh process. The lazy import boundary still exists at Lifecycle `lifecycle.py:77–81,167–170`; the code evidence supporting the attack has not disappeared. What changed is authorization: source/editable producers cannot read or write persistent entries, and cache-enabled producers must bind deferred imports to an immutable snapshot. Replacement invalidates the epoch, and lines 85–89 forbid publishing another epoch's output under D1. A final disk rehash that misses the intervening replacement is insufficient evidence under these rules.

**Already-loaded provenance: the reverse attack also fails.**  
Loading G1, replacing disk files with G2, and identifying the producer from G2 disk hashes would mislabel G1 output. Lines 77–83 require provenance for already-loaded dependencies as well as deferred imports and explicitly reject package labels as proof. Missing or conflicting provenance forces bypass. Lines 210–211 preserve both historical sequences as implementation acceptance obligations.

**Trust precedes marshal decoding.**  
An attacker replaces an entry and recomputes its checksum. Integrity alone cannot admit it: lines 148–152 explicitly distinguish corruption detection from trust, prohibit unmarshalling untrusted entries, and require platform-specific checks before persistence is enabled. A symlink or traversal route into attacker-controlled storage is expressly rejected. The plan does not claim checksums authenticate executable artifacts.

**Malformed and oversized entries must reject without replacing producer behavior.**  
A truncated payload, mismatched declared length, oversized header, incompatible interpreter entry, or non-code decoded value is covered by lines 137–142 and acceptance line 213. Bounds and envelope validation precede unmarshalling; code-object validation follows it. Concrete limits and bounded-read mechanics remain implementation work, not permission to perform unlimited reads.

**Identity and inherited changes remain generation inputs.**  
Two same-named definitions with different inherited layouts or transaction ordering must not collide merely because their names agree. The plan requires ordered normalization, complete generation contributions, inherited layouts, transaction indices, and unknown-shape bypass. Harvester lines 65–85, 112–164, and 295–410 demonstrate why these dimensions matter. The amendment does not substitute installation provenance for definition fingerprints.

**Live values remain freshly bound, with producer-specific exclusions.**  
Lifecycle rebuilds current builder arguments from harvested defaults, factories, freeze/thaw functions, annotations, and transaction keys (`lifecycle_harvester.py:133–178`). A hit must use those current arguments in a fresh namespace rather than retain old objects. The second consumer cannot assume identical exclusion rules: data-record defaults enter generation at `data_schema.py:1742–1744,1765–1767`. The plan requires separate audits and explicitly forbids excluding values that affect generated code.

**Crash, concurrency, and reentry constraints remain explicit.**  
Two same-key misses may both generate; each must publish a complete entry by same-directory atomic replacement. A crash before replacement permits the prior complete entry or a miss, not a partial valid hit. Lines 154–160 forbid mixed entries and cache I/O locks around generation/execution callbacks and assign same-key reentry, recursion, cleanup ownership, and bounded failure behavior to implementation proof. No stronger crash-durability guarantee is asserted.

**Bypass preserves errors rather than masking them.**  
An unverifiable installation must still harvest, validate, generate, execute, and bind normally. Cache storage failure cannot convert a producer exception into success. Lines 93–97 preserve existing diagnostic boundaries, which are concrete in Lifecycle's separate generation, execution, and class-build handlers. Narrowed admission therefore removes acceleration, not supported behavior.

**Portability is gated, not presumed.**  
Interpreter identity and compilation settings are keyed; uncertain platform trust must bypass. The sibling cache package is not claimed to ship already: current sdist inclusion names `src/yidl`, and the plan requires packaging verification. Eager parser imports in `yidl.__init__` support the stated lightweight-package motivation without proving its eventual import cost.

## 3. Risks and next action

Remaining obligations include an implementable immutable-snapshot proof, complete producer dependency/input tables, descriptor-safe platform trust checks, concrete decoding limits, reentry handling, publication fault behavior, and packaging evidence. A manifest or installation version alone must not be promoted into provenance proof. If safe installed-cache admission cannot be established, the specified outcome is bypass, not weaker verification.

**Next action:** Complete checkpoint 1's generation-versus-binding and provenance/trust proofs for both consumers before implementing persistent cache admission.
