# YIDL Generated Code Cache Plan — Consistency Review

**Review object:** `yidl/dev-docs/YidlGeneratedCodeCachePlan.md`, proposed implementation plan, and the two developer-documentation index links.
**Exact baseline tuple:** YIDL `a3222bb44e2a5709dde9a680bca1ff6ab62eba96`; YIDL Lifecycle `c2502f1a7a565624f20cf930fde92f581b123e9f`.
**Date:** 2026-10-10.
**Independence:** Independent, adversarial, read-only Consistency review. No other reviewer's report was requested or read.
**Verdict: GO** for the draft plan only. Severity counts: P0: 0; P1: 0; P2: 0; P3: 0. This does not accept implementation, freeze an API, authorize activation, or verify the reported performance measurements.

## 0. Evidence base

Inspection used `git rev-parse`, `git status --short`, and pinned `git show` reads, with `nl`, `sed`, and `rg` for locations and dependency tracing. No files were modified; no builds, tests, or git mutations were run.

Both repositories' HEADs matched the exact baseline tuple at the beginning and end. Final status showed two untracked review-prompt documents in YIDL and no changes in Lifecycle. Those prompt documents were not read.

Process authority read: `review-loop/SKILL.md` and `references/review-prompt-template.md`.

Repository evidence, with paths relative to their owning repositories:

- YIDL `AGENTS.md`; `dev-docs/YidlCodingRules.md`, particularly sections 2–6 and 8–9; `dev-docs/YidlDesignSummary.md`, particularly sections 26, 26.1, and 27.3.
- YIDL plan lines 1–201 and `dev-docs/README.md` working-material link; Lifecycle `AGENTS.md` and `dev-docs/README.md` lines 15–24.
- Lifecycle `src/yidl_lifecycle/lifecycle.py` lines 35–180: harvesting, generation, compilation/execution, binding, lazy generated-module import, and diagnostic boundaries.
- Lifecycle `lifecycle_harvester.py` lines 31–270 and 359–743: generation facts, live builder arguments, transaction indexing, callable signatures, annotation decisions, inheritance, and validation.
- Lifecycle `_generated_lifecycle_base.py` imports, module-root/builder templates around lines 3091–3123, and assembly entrypoints at lines 4834–4860.
- YIDL `src/yidl/generation/assembly_runtime.py` lines 1–200 and `matcher_values.py` lines 19–188: assembly dependencies, value evaluation, and deferred resource compilation.
- YIDL `data_schema.py` lines 1–35, 109–184, 641–705, and 1531–1843; `data_def_sys.py` lines 1–77.
- Both package initializers and `pyproject.toml` files: eager YIDL parser imports, distribution configuration, dependencies, and declared Python matrix.

Pyrolyze working-tree changes, adjacent reports, and external references were not inspected. The timing statements therefore remain reported motivation, not independently established evidence.

## 2. Invariant analysis

**Generation and binding are separable for Lifecycle.** The current decorator harvests before generating, executes module code in a fresh namespace, then supplies the current class and `build_kwargs` to `build_lifecycle_class` (`lifecycle.py:40–64`). The proposed insertion point preserves that shape. Defaults, factories, freeze/thaw functions, annotations, metadata, and transaction keys already have live binding channels (`lifecycle_harvester.py:56–60,133–178`). This supports the proposal without proving every such value is generation-independent.

**The fingerprint rules withstand the concrete dependency attacks.** Factory signature changes affect generated parameter names; annotation changes affect binding shape and optional-None decisions; inherited facts and transaction-method ordering affect generation. The plan expressly requires these contributions to be audited and keyed, preserves meaningful ordering, and forbids excluding live objects merely because they are rebound (plan lines 77–103). Unknown shapes must bypass caching rather than receive guessed identities. I found no clause permitting the obvious name-only or runtime-value-only stale-code counterexamples.

**Complete generation identity extends beyond the Lifecycle repository.** The generated base imports YIDL assembly machinery; that machinery imports Astichi. Consequently, hashing only Lifecycle templates or package versions would be insufficient. Plan lines 63–67 require the *complete* generation dependency revision and invalidation after unversioned edits; lines 82–89 explicitly make the listed audit inputs non-exhaustive. The narrower Lifecycle file list does not supersede that requirement. Dependency enumeration remains checkpoint work, not an established proof.

**Deferred Lifecycle generation is structurally supported.** `_generated_lifecycle_base_module()` is called from the composable-building path, not harvesting (`lifecycle.py:77–80,167–170`). A hit can therefore skip this generation entrypoint. Hash acquisition must inspect dependency bytes without importing that module, as the plan requires. No existing code was treated as already implementing this behavior.

**The second consumer is real but materially different.** `RecordSpec.record_class()` reaches AST materialization and module-code execution (`data_schema.py:678–681,1672–1676,1815–1827`). Record defaults are embedded into property and constructor templates, unlike Lifecycle's live builder arguments (`1735–1767`). The plan requires a separate dependency table and permits default exclusion only after proof. A representative schema using supported builtin types and explicitly normalized defaults can satisfy the proposed proof without changing generated classes into dataclasses or widening existing type support.

**A lightweight cache package does not imply lightweight consumers.** YIDL's initializer eagerly imports its parser. A separate top-level `yidl_cache` avoids that initializer when reading artifacts. However, `data_schema.py` currently compiles templates during module import, and generated record code imports the broader `data_def_sys` facade. A second-consumer implementation must address template loading to meet the request-construction requirement; callback-count evidence alone would not establish that gate. The plan requires template-free request construction and import-overhead measurement, rather than claiming the current module already satisfies them. This is implementation work, not an unsatisfiable architectural requirement.

**Diagnostics and acceptance gates are compatible with current contracts.** Lifecycle distinguishes harvesting, AST generation, AST execution, and class-building failures. The plan explicitly retains current diagnostic boundaries and prohibits cache fallback from swallowing producer errors. Its successful-behavior gates use canonical coverage, while cache faults and mechanics receive focused tests. The distribution inclusion check is necessary because the current source-distribution list includes `src/yidl`, not the proposed sibling package; the plan explicitly requires that packaging change to be verified.

**Scope and documentation agree.** Both index entries label caching as proposed and unimplemented. The plan preserves ownership direction, structural AST generation, plain generated classes, and Lifecycle-owned adapters. Its performance target is explicitly unproven and is not an activation criterion.

## 3. Risks and next action

No concrete consistency defect met the finding threshold. Remaining implementation risks are dependency-inventory completeness, embedded-value normalization, second-consumer template loading, diagnostic parity, and platform trust-policy feasibility. No performance or runtime-safety proof follows from this review.

**Next action:** Complete checkpoint 1's generation-versus-binding tables for both consumers, including transitive YIDL/Astichi dependencies and the data-record import boundary, before implementing the shared cache.
