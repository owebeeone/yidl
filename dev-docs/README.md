# Developer Documentation

## Release preparation

- [Release process](../RELEASE.md): configured GEARU route and publication order.
- [Publishing preparation](YidlPublishing.md): current dependency/license setup,
  local checks and remaining hosted publication gates.
- [0.1.0 release plan](YidlReleasePlan.md): current milestones, scope, evidence,
  release gates and separate publication authorization.
- [Documentation and website plan](YidlDocumentationPlan.md): detailed public
  page/example/site requirements; see the publishing record for current checks.
- [Documentation shortcomings](YidlDocShortcomings.md): consumer evidence and
  recipe/reference inventory; classifications must be preserved.
- [Release follow-ups](YidlReleaseFollowUps.md): unresolved cleanup, adjacent
  ownership and optional work that must not disappear during consolidation.

## Canonical contracts

- [Design summary](YidlDesignSummary.md): canonical semantic/design reference.
- [Coding rules](YidlCodingRules.md): definitive implementation/process rules.
- [Repository instructions](../AGENTS.md): operational shorthand.
- [Public documentation](../docs/): current guides, examples and reference;
  publishing the site is a separate operation.

Lifecycle behavior belongs to `yidl-lifecycle`; its historical presence in the
design summary does not authorize restoring it to the generic compiler.
Release planning does not override the canonical contracts.

## Cross-project work still in use

- [Generated-code cache plan](YidlGeneratedCodeCachePlan.md) and
  [input audit](YidlGeneratedCodeCacheInputAudit.md): retained here because the
  cache project's active index references them. Shared caching and the Lifecycle
  adapter have local implementations; the newest owning checkpoint distinguishes
  completed draft review from release adoption and platform qualification.
  YIDL core remains independent of the cache. Older status statements in these
  documents are snapshots, not the current release verdict.

## Deferred writing

- [Paper draft](paper/paper-draft.md), [evidence index](paper/evidence-index.md),
  and [research gaps](paper/research-gaps.md): unfinished research material,
  outside the 0.1.0 release gates. This task does not abandon or complete it.

## History

[Archive disposition](history/README.md) records the documents moved in this
consolidation and what replaced or superseded them. Earlier grammar, merge,
extraction and lifecycle documents remain historical background.

Archived files and existing references are preserved as-is, by explicit operator
instruction. No link-repair sweep was performed. Archiving an old plan/review
does not close its outstanding obligations or authorize source deletion.
