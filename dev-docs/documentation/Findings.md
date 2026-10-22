# Findings outside the documentation implementation scope

2026-10-23. These observations do not authorize compiler, dependency or release
changes. Existing supported routes were checked before suggesting remediation.

| Observation and evidence | Classification / practical impact | Suggested owning action | Blocks this documentation? |
| --- | --- | --- | --- |
| pyproject lists Lark but concept imports Astichi; original local venv collection failed ModuleNotFoundError | Confirmed packaging defect: bare install is incomplete for current concept route | Separately qualify/depend on supported Astichi artifact range in packaging work | No: explicit Astichi 1.1.3 plus current YIDL wheel runs standalone examples |
| Existing ignored dist wheel lacked concept_parser; freshly built wheel imports/runs it | Confirmed stale local artifact, not current compiler failure | Rebuild/identify exact candidate artifacts during release qualification | No; fresh temporary artifact used, old dist untouched |
| Legacy yidl-compile invokes old lexer/parser and helper emitter | Confirmed distinct surface, not a defect from this task | Owner decides long-term CLI disposition separately | No: Python concept API documented and tested |
| Nested indexed scalar expression propagation failures in original D17 | Observed unresolved mechanism; cause not demonstrated here | Minimal owning investigation before a normative nested-chain claim | No: limitation explicit; ordinary class/method nesting is separately demonstrated |
| Live Lifecycle type annotations fail in separate task's baseline | Known failing arrangement, fix being qualified elsewhere | Keep separate scoped fix and independent acceptance | No: fixed-revision excerpts/string route; no changing bytes promoted |
| New tutorial needed composite numeric indices for two owners, explicit empty payloads for mandatory holes | Confirmed authoring constraints of tested route, not asserted compiler defect | Teach separation of identities and empty/suppressed behavior | No: documented working forms pass |
| Compound insertion, native handle/failure ownership, universal edge environments and full factory-provider matrix not exercised | Qualification limitations, not asserted missing features | Expand recipes only with focused evidence and separate product authorization if required | No; listed individually in public compatibility and inventory |
| Material upstream in maintenance mode through 2027-05-05 | Docs maintenance opportunity; current 9.7.7/1.6.1 build works | Evaluate future migration when useful; do not replace selected tooling incidentally | No |
| No selected project license in inspected root | Release/publication decision remains owner-owned | Resolve licensing as part of separately activated release work | Does not prevent local reviewable docs artifact; no deployment performed |

Existing cross-platform reports and consumer package checkpoints remain their own
evidence. Known Python Lifecycle source-hygiene and Windows cache diagnostics
failures were not silently recast as universal success or fixed here.
