# YIDL Generated Code Cache Plan — Consistency Review

**Review object:** Proposed `yidl/dev-docs/YidlGeneratedCodeCachePlan.md` and the two developer-documentation index links.  
**Exact baseline tuple:** YIDL `1731f1de64422463356201aa65b4925b97b752c9`; YIDL Lifecycle `c2502f1a7a565624f20cf930fde92f581b123e9f`.  
**Date:** 2026-10-10.  
**Independence:** Replacement round-2 Consistency reviewer, independent, adversarial and read-only. Prior filed reports and remediation plan were read; no current-round peer report was requested or read.  
**Report filename:** `YidlGeneratedCodeCachePlan-ReviewConsistency-2.md`.

**Verdict: GO** for the draft plan only. Severity counts: P0: 0; P1: 0; P2: 0; P3: 0. This does not accept implementation, freeze an API, establish performance, or authorize activation.

## Prior-finding closure table

| ID | Disposition claimed | Verified on corrected tree | Status |
| --- | --- | --- | --- |
| Consistency: none | Prior report returned GO without findings. | Rechecked generation/binding dependencies, package boundaries and acceptance obligations against the amended admission policy. | No inherited findings. |
| Safety P2-1, contextual retrace only | Require coherent producer provenance; bypass editable/source/unverifiable installations; invalidate lost epochs. | Retraced fingerprint → replacement → deferred import → restoration, and already-loaded-old-module/new-disk cases. Plan lines 70–89 prohibit persistent use or publication under these conditions; lines 210–212 require corresponding acceptance cases. | Consistency objection removed; originating closure belongs to Safety. |

## Changed-range analysis

`git diff a3222bb44e2a5709dde9a680bca1ff6ab62eba96 1731f1de64422463356201aa65b4925b97b752c9 -- dev-docs/YidlGeneratedCodeCachePlan.md dev-docs/README.md` showed two plan hunks and no index change.

Original lines 62–67 now expand into lines 62–91: process-lifetime hashing is replaced by verified immutable epochs, explicit admission restrictions, transitive/native provenance, and same-epoch checks before accepting hits or publishing misses. Three acceptance rows were added at lines 210–212. These changes match remediation 1’s disposition.

The amendment materially narrows compatibility policy, but does not change generated semantics, artifact ownership or binding interfaces. No new architectural root cause was identified.

## 0. Evidence base

Both `git -C yidl rev-parse HEAD` and `git -C yidl-lifecycle rev-parse HEAD` returned the exact baseline tuple at review start and end. Repository evidence was read through `git show <exactSHA>:<path>`, with `nl`, `sed` and file listings. No writes, builds, tests or git mutations occurred.

Authority read: workspace `AGENTS.md`, both pinned repository `AGENTS.md` files, process `review-loop/SKILL.md`, and its canonical `references/review-prompt-template.md`.

Pinned evidence examined:

- YIDL plan, including identity/admission lines 61–97, fingerprint/binding requirements, checkpoints and acceptance matrix; prior Consistency/Safety reports and `YidlGeneratedCodeCachePlan-RemPlan-1.md`.
- YIDL `YidlCodingRules.md:25–130,141–179`; `YidlDesignSummary.md:880–1007,1038–1048`.
- Documentation links: YIDL `dev-docs/README.md:16–18`; Lifecycle `dev-docs/README.md:21–24`.
- Lifecycle `lifecycle.py:35–180`; harvester generation/binding, inheritance, callable-signature and annotation paths, particularly `31–270,360–410,436–666`.
- Lifecycle `_generated_lifecycle_base.py`: runtime import at line 1, assembly imports at `3091–3094`, and entrypoints at `4834–4860`.
- YIDL `assembly_runtime.py:12–19,113–188`; `matcher_values.py` deferred generator and resource construction paths.
- YIDL `data_schema.py:1–35,678–687,1531–1548,1664–1843`; both package initializers and `pyproject.toml` files.

Pyrolyze changes, external references and current-round peer evidence were excluded. Timing statements were not independently verified.

## 2. Invariant analysis

**Admission is narrower, not contradictory.** “Compatible warm entry” requires the admission and epoch checks, not merely matching bytecode metadata. A source checkout cannot use that row to override explicit bypass at lines 70–75 and 212. The generator-change “miss” row cannot authorize publication when provenance is lost: lines 85–89 require uncached behavior instead.

**The original replacement counterexample is no longer permitted.** The current lazy import boundary remains real (`lifecycle.py:77–80,167–170`). However, editable/source producers cannot read or write persistence, and enabled installations must bind deferred imports and loaded dependencies to the request’s immutable snapshot. Restoring disk bytes cannot repair an unverifiable epoch or legitimize replacement-generated code under its old identity. This is a textual retrace, not an executed fault test.

**Complete identity is required but not yet demonstrated.** Lifecycle’s generated base depends on YIDL assembly machinery, which imports Astichi. Hashing Lifecycle alone is insufficient. Amended lines 77–83 explicitly cover transitive code, templates and native dependencies and reject package labels as proof. The narrower audit file list does not supersede that requirement.

**Deferred Lifecycle generation is structurally supported.** Harvesting precedes `_generate_lifecycle_ast`; compilation/execution and current-class binding follow (`lifecycle.py:40–64`). The heavy generated module is imported by the generation path, not harvesting. A hit can skip that path while preserving current namespace, class and builder arguments. Callable signatures, annotation-derived shape, inherited layouts and transaction indices still require fingerprint contributions; rebinding their live objects alone is insufficient, as the plan recognizes.

**The second consumer requires actual import-boundary work.** `RecordSpec.record_class()` reaches materialization and code execution (`data_schema.py:678–681,1672–1676,1815–1827`). Defaults are embedded into templates at `1742–1744,1765–1767`; they cannot inherit Lifecycle’s runtime-only classification. Module-level template compilation also means callback counts alone cannot prove template-free request construction. The plan assigns both dependency auditing and import-overhead proof rather than claiming current code already satisfies them.

**The lightweight package boundary remains coherent.** `yidl.__init__` eagerly imports lexer/parser modules. A sibling top-level `yidl_cache` can avoid that initializer for cache operations without making all consumers lightweight. Current sdist inclusion names `src/yidl`, not the proposed sibling; explicit packaging verification is therefore necessary and already required.

**Acceptance remains satisfiable but conditional.** The amended policy does not guarantee cache admission for ordinary editable development environments; Lifecycle’s `pyproject.toml:31–33` explicitly selects editable dependencies. Such environments must exercise bypass, while positive warm-hit evidence requires a separately established admissible installation. Neither bypass-only results nor unproven installed-package provenance can satisfy the positive hit gates. No implementation feasibility or speedup is established by this draft review.

## 3. Risks and next action

Residual obligations are a concrete immutable-snapshot mechanism, complete generation-input tables, second-consumer template separation, platform trust checks, packaging and diagnostic parity. These remain implementation gates, not evidence of defects in the amended proposed contract.

**Next action:** Complete checkpoint 1 with explicit admission/provenance proof and generation-versus-binding tables for both consumers before implementing persistent caching.
