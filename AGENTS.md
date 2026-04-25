# AGENTS

## Scope
This file defines repository-specific coding instructions for `yidl`.

## Active docs
- `dev-docs/YidlDesignSummary.md` is the canonical semantic/design summary.
- `dev-docs/YidlCodingRules.md` is the definitive implementation/coding-rules
  document.
- `dev-docs/history/` is archival only.

## Agent requests: review vs edit
- When the user asks to **review**, **verify**, or **analyze** (or similar: assess, report, check), respond with **read-only analysis** only. **Do not** change files, run refactors, or “fix” docs or code unless they **explicitly** ask for edits, fixes, implementation, or an update.
- If analysis surfaces a problem, describe it and wait for direction rather than patching the tree unprompted.

## Design Rules
- Prefer **`abc.ABC`** with **`@abstractmethod`** for explicit shared contracts when
  nominal inheritance is practical. Prefer **`typing.Protocol`** only when an ABC
  is awkward (e.g. typing third-party or existing types you must not subclass).
- Do not introduce enums without explicit project-owner approval. Do not work
  around this with magic strings, magic integers, sentinel strings, or other
  passive tags when the concept has semantics. Semantic concepts should be
  represented by objects/classes that can own behavior, validation, lowering,
  and documentation.
- In compiler-only, parser/frontend, IR, spec, and other non-generated support paths, strongly prefer `@dataclass` for classes that primarily hold state.
- Prefer `frozen=True` for those dataclasses when mutation is not required by the design.
- Generated YIDL classes must not use `@dataclass` in this phase. Generated classes should be emitted as plain undecorated Python. Tests may still use dataclasses where helpful.
- In tests, strongly prefer dataclasses for named structured test state over unnamed tuples or ad hoc lists.
- Be careful not to blur YIDL-generated object-model semantics with Python dataclass semantics. YIDL is defining its own generated structures, and handwritten support code should not quietly force dataclass behavior into generated output.
- Keep type annotations complete and precise so IDE inference and static reasoning remain strong.
- Organize modules by cohesive responsibility and change boundary.
- Keep generic/shared modules limited to neutral abstractions, stable data carriers, and utilities that are genuinely shared across subsystems.
- Keep subsystem-specific concrete implementations with the subsystem that owns their behavior.
- Promote a concrete implementation into a shared module only when there is clear multi-consumer reuse or it defines a stable cross-cutting concept.
- Split modules when doing so improves change isolation, testing, or architectural clarity; do not split so aggressively that closely related behavior becomes scattered across tiny files.
- Plans do not override sound architectural separation. If implementation reveals that a planned module boundary is wrong or overly coupled, stop widening the mistake, update the plan/docs, and adopt the cleaner boundary instead.
- YIDL is intended to become authoritative for its own runtime/compiler behavior. Do not design YIDL modules around long-term dependence on `pyrolyze.lifecycle`.

## Paths in version control
- Do not store absolute filesystem paths in any committed file; use paths relative to this repository (the `yidl` submodule root).
- Do not treat scratch or generated validation artifacts as stable dependency locations for committed source unless the docs explicitly promote them into the supported surface.
- Validation-only experiments, probes, and performance checks belong under `docs/validation/` until deliberately promoted.

## Current Phase Constraint
- During the current phase, do not edit files under `pyrolyze/`.
- Treat `pyrolyze.lifecycle` as a read-only reference backend for parity comparison, representability review, and lifecycle-bug discovery only.
- If `pyrolyze.lifecycle` behavior is wrong for a covered case, document it and use the normalized lifecycle-only skip path rather than patching `pyrolyze/`.

## Development Process (TDD)
Use a strict red/green/refactor workflow for behavior changes.

1. Red: Add or update tests first to express the expected behavior, then run the smallest relevant test target and confirm it fails.
2. Green: Implement the minimal code change required to make the failing test pass.
3. Refactor: Improve structure and readability while preserving behavior.
4. Verify targeted scope: Re-run the focused test subset.
5. Verify full regression: Run the full relevant regression scope before finalizing.

## Test coverage shape
- Prefer canonical fixture, `gold_src`, golden, snapshot, or integration-style
  coverage for successful end-to-end behavior when that harness already exists.
- Keep bespoke unit tests focused on narrow mechanics, recognition/parsing
  checks, diagnostics, and failure modes the canonical harness does not express
  cleanly.
- Avoid duplicating the same success-path assertions in both bespoke tests and
  canonical output tests.

## Test file naming
- Test **file** and **module** names should describe **behavior or the surface under
  test**, not ephemeral process labels (phase numbers, impl-plan step ids, ticket
  ids, dates). Plans and phases change; names should stay meaningful over time.
- Prefer **stable, coarse scope** in the filename when the file is mainly wiring,
  harness, or smoke over several cases (e.g. `test_study_harness.py`). Put finer
  scenario or API detail in **test function names** and docstrings, not a long
  filename that duplicates them.
- When one file is **one focused behavioral story**, a more specific module name
  is appropriate—still semantic, still no process ids.

## Test-Led Semantics Guardrail
- Do not change public semantics, runtime semantics, code-generation semantics, or source-container semantics merely to make a test pass without user consultation.
- If a red test reveals that the desired behavior would require a real semantic change rather than a bug fix or missing coverage, stop and ask before implementing it.
- It is acceptable to tighten tests, fix test assumptions, or fix correctness bugs that clearly match the existing design intent.
- It is not acceptable to quietly redefine semantics to satisfy a convenient test expectation.

## Roll-Build Method
- When the user asks for a phased rollout using the roll-build method, start from a clean git tree and tag that point before implementation begins.
- Use the requested start tag name when one is given. If none is given, ask or use a clearly scoped phase-start tag name.
- An unqualified `roll-build` means: run all phases for that plan in sequence, committing and tagging each completed phase, and continue into the next phase without stopping for chat unless the guardrails below require a pause.
- Implement one phase at a time.
- After a phase is complete, only commit and tag it if:
  - the phase goal is actually met
  - focused verification passes
  - the remaining ambiguities are minor and non-blocking
- Tag completed phases using the naming scheme the user requested. If a phase is only partially complete, use an explicit partial tag name rather than pretending the phase is done.
- If there are no more phases, or if confidence drops because of material ambiguity or instability, stop and wait instead of forcing the next phase.
- If work starts cycling on the same persistent bug or bug family, stop, report the cycle clearly, and ask for direction.

## When To Push Back On Roll-Build
- Push back when the next phase has too many unresolved ambiguities to produce a trustworthy checkpoint.
- Push back when the requested phase is too large or too coupled to complete safely as one checkpoint.
- Push back when implementation reveals facts that materially break the current design or plan assumptions.
- Push back when the resulting checkpoint would be misleadingly partial, unstable, or hard to recover from.

## Test Commands
- Focused tests: `uv run --with pytest pytest <test-path> -q`
- Full suite: `uv run --with pytest pytest -q`
