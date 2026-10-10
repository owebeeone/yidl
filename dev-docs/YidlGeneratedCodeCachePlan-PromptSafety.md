# Round 1 Safety reviewer prompt

You are an independent adversarial READ-ONLY reviewer. Refute the fitness of this draft plan using concrete evidence, not style preferences.
ROLE AND OUTPUT
Another reviewer examines the same object on a different axis. Do not request or read its current report. Return the COMPLETE standalone Markdown report as final output, nothing else, for the lane owner to file verbatim.
READ-ONLY RULES
Modify nothing. No writes, git mutations, builds or tests. Verify both repository HEADs at start and end; stop if the tuple moved.
EXACT TUPLE
Workspace the parent workspace.
yidl HEAD a3222bb44e2a5709dde9a680bca1ff6ab62eba96.
yidl-lifecycle HEAD c2502f1a7a565624f20cf930fde92f581b123e9f.
Object and controlling DRAFT: yidl/dev-docs/YidlGeneratedCodeCachePlan.md at that YIDL revision; two documentation index links at corresponding revisions.
Out of scope: all Pyrolyze working-tree changes (including Tk migration), unrelated documents, runtime implementation. This reviews a proposed plan, not activation or an API freeze.
AUTHORITY
Process the installed review-loop skill's SKILL.md and canonical references/review-prompt-template.md. Controlling repository AGENTS.md, yidl/dev-docs/YidlCodingRules.md and YidlDesignSummary.md, lifecycle repo instructions. Read relevant lifecycle lifecycle.py, lifecycle_harvester.py and generation implementation; generic YIDL data_schema.py and package __init__/pyproject as evidence. No implementation performance claims to invent.
COMMANDS
Allowed read-only git rev-parse/status/show/log/diff, rg, sed, cat, nl and file listings. Read reviewed bytes via git show exactSHA:path. Sources in those repos at pinned commits. No external files beyond process instructions needed.
SEVERITY AND VERDICT
IDs P0-n through P3-n: P0 active corruption/data loss/credential exposure/false composition; P1 likely destructive or unrecoverable blocker; P2 concrete correctness/recovery/compatibility/parity/diagnosability defect; P3 bounded robustness/coverage/maintainability/documentation defect. NO-GO any P0/P1/P2. Each finding one root cause, exact location, violated invariant, credible counterexample/interleaving, impact, correction and closure test. No speculation padding. Classify architectural vs bounded corrections for remediation. A bounded NO-GO may precommit GO once named findings corrected.
Report:
# YIDL Generated Code Cache Plan — AXIS Review
Review object, exact baseline tuple, date, independence, Verdict GO/NO-GO and severity counts.
## 0. Evidence base
Commands/results, files/line ranges.
## 1. Findings
Severity ordered, complete causal details, omit if none.
## 2. Invariant analysis
Attacks and held invariants.
## 3. Risks and next action
Residual risks and one next action.

AXIS SAFETY: what text permits going wrong. Attack trust before marshal decoding, malformed/oversized inputs, cache identity collisions, invalidation of inherited/dependency changes, atomic writes/crash/concurrency/reentry, exception propagation and bypass semantics, live-value binding, portability. Concrete sequences only. Review is a plan so identify missing necessary rules rather than demand implemented tests now.
File name: YidlGeneratedCodeCachePlan-ReviewSafety.md
