# Documentation plan review and activated brief

2026-10-23 — focused single-agent gate: **GO**. This is a documentation-plan
review; it does not accept release readiness or unsupported compiler contracts.

Reviewed the complete `YidlDocumentationPlan.md` and `YidlDocShortcomings.md`,
canonical design summary sections 26–30 and applicable coding rules, release
plan and its accepted planning checkpoint. The plan connects reader outcomes to
all D01–D28/A01–A10 and M01–M10 through concrete reference, recipe, negative and
output evidence. The inventory correctly distinguishes author errors, bounded
remedies, unresolved mechanisms and anticipated questions. No substantive
plan blocker requires a decision before documentation creation.

## Scope and requirement provenance

The operator explicitly activated creation after this review passed. Allowed:
public `docs/`, root README, runnable documentation examples and canonical-harness
integration, docs-only dependencies/configuration, build-only CI and associated
evidence here. Preserve existing `example/` organization. All compiler/runtime
source, runtime metadata, generated product bases, adjacent repositories,
workspace configuration, release plan and paper remain reference-only. No Git
publication or deployment. Archived/history references and originals remain
unchanged. This brief supersedes the precursor plan's plan-only status for this
run; it does not change the original plan or authorize product work.

The plan's publication-workflow proposal is narrowed by the current operator's
explicit build-only authorization. Site deployment instructions can describe a
future separately authorized action; no deploy job is enabled. GEARU remains the
selected future release tool. A review GO does not prove packaging is ready.

## Feasibility evidence

- Existing local environment lacked Astichi. Existing ignored `dist/` wheel
  could not import `yidl.concept_parser`. Building the current YIDL checkout into
  a temporary wheel and explicitly installing published Astichi 1.1.3 provides
  a viable isolated route. Runtime metadata was not modified.
- The current multi-source golden ran against those installed packages with
  `ASTICHI_LOWER_ENGINE=python`; focused parser, matcher-result and contribution
  diagnostics: 108 passed on CPython 3.12.12. The pytest check uses repository
  source via its configured pythonpath; the standalone golden used installed
  packages. These are distinct evidence boundaries.
- MkDocs 1.6.1 and Material 9.7.7 installed separately. Upstream supports pip
  installation and explicit exclusions. Material is in maintenance mode through
  2027-05-05; migration is optional future work, not a prerequisite or authority
  to replace the selected tool.

## Findings and dispositions

Installation metadata missing Astichi and stale local distribution artifacts are
confirmed setup hazards: teach an explicit dependency/current-wheel route and
import-origin checks. Packaging repair needs separate authorization. Neither
blocks docs. Legacy CLI is a transducer helper generator, not the braced concept
compiler: document its actual help/API and use the Python concept route.

D17 nested expression propagation remains unresolved; no blanket defect or
promised nested-chain recipe. D19 expression carriers need individual backend
qualification. A06 signature/provider behavior belongs to consumers. Live-type
Lifecycle annotations remain limited pending separate fix qualification.
Cross-platform operational results do not automatically qualify these examples.
