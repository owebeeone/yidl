# YIDL Release Follow-Ups

Date: 2026-10-23. Current disposition register consolidated from older cleanup,
gap and release-audit documents. This is not an implementation authorization or
a fresh verification of every historical claim. The release plan owns release
gates; the semantic and coding documents remain authoritative.

## Confirmed release concerns

| Observation and evidence | Practical impact | Suggested action | Blocks 0.1.0? |
| --- | --- | --- | --- |
| `pyproject.toml` omits Astichi; importing the concept compiler in YIDL's own environment fails | A user cannot rely on declared dependencies to run the active compiler | Qualify a standalone install and declare demonstrated requirements in Phase 1 | Yes |
| `src/yidl/cli.py` and top-level exports expose the old transducer parser | Product entry points can imply the wrong supported compiler | Decide and document compatibility/legacy status; deletion or replacement is not preapproved | Yes, an honest disposition is needed; a new CLI is optional |
| Public docs describe old behavior; README, license and release material are absent | First use and distribution terms are unclear | Deliver the current quickstart, supported contract and owner-selected license | Yes |
| Default workspace run reaches a mismatched Astichi native API; explicit Python suite passes | Native claims are not qualified by this environment | Try the supported artifact tuple before proposing upstream work; qualify or bound native support | Only for configurations advertised by the candidate |

## Source cleanup retained for separate consideration

The archived cleanup recommendation's broad deletion set has not been executed
and is not automatically accepted by this consolidation.

- **Legacy parser/CLI/transformer:** `lexer.py`, `parser.py`, `cli.py` and
  `ast_tx.py`, their tests and old example may be retired after a public-surface
  and consumer-usage decision. Their presence is confirmed; deleting them is an
  optional implementation choice rather than a requirement for a new command.
- **Capsule prototype:** `capsule/init_only_capsule.py` still has executing tests
  in the passing suite. Its supposed redundancy is a hypothesis requiring import
  and semantic-coverage review. Do not remove it or its tests on the basis of an
  old recommendation.
- **Generic test harness ownership:** possible overlap with consumers remains an
  architectural question. Retain current canonical generation/golden coverage;
  source cleanup and test renaming are not release gates by themselves.

## Lifecycle-specific historical gaps

The former current-gaps snapshot mixed generic compiler issues with Lifecycle's
feature roadmap. The following remain follow-up questions for the owning project,
not newly confirmed defects or YIDL 0.1.0 prerequisites:

- Sentinel constants ownership, generated slot naming versus the old summary,
  and public/helper parameter conventions need a current contract comparison.
- Derived fields, retained-initvar/post-init consumption and full callable-hook
  injection need review against the current Lifecycle implementation before any
  missing-feature claim. The canonical summary already records later initvar
  support, so the older gap list cannot establish current absence.
- Compare policy, richer binding/owned container shapes, resource eviction order,
  rollback aggregation, cross-group visibility, refcounted facade behavior and
  broader annotation-driven policy were unresolved or limited in the snapshot.
  Reproduce a concrete failure or confirm an accepted omission before proposing
  changes. Preserve existing generated-layer and transaction behavior.
- Lifecycle regeneration has an owning command; its existence is not an open
  generic YIDL feature request. Consumer-specific no-diff checks belong in that
  project's work and may provide release evidence without expanding this task.

No adjacent files were changed here. These questions are demonstrably outside
the generic release's current scope; no evidence here shows them blocking it.

## Cache status and ownership

The YIDL cache plan and input audit stay active because `yidl-cache` still
references them as the cross-project plan. They do not create a core dependency.
The later owning `yidl-cache/dev-docs/CacheLocationPolicyCheckpoint.md` records
completed Code, State and Surface draft reviews with no open findings, while
distinguishing draft acceptance from adoption and settled-tree/default-on release
acceptance. Local verification does not establish Linux/Windows qualification.

Suggested improvement: in a separately scoped cache documentation task, reconcile
older status paragraphs against that checkpoint and identify remaining adoption,
platform and publication gates. This consolidation does not rewrite those
contracts or repair their references. Cache release status does not block the
generic YIDL release because the core does not depend on it.

## Superseded concept and unfinished research

- The old one-root Undo/Redo concept is superseded by the separate
  `yidl_undoable` design and accepted local-runtime checkpoint. Its earlier names
  and nesting limitations are background, not the current API. This does not
  assert that every later helper or publication action is complete.
- Paper drafting and its evidence/research inventory remain deferred, not
  abandoned. Novelty, performance and usability claims need their own evidence;
  they are not required to release the bounded compiler.
