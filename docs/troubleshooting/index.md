# Troubleshooting by symptom

Start with an explicit backend, fresh process, versions and import origins.
Retain chained exceptions and distinguish setup failures from generated behavior.

| Symptom | Likely layer / next check | Remedy or status |
| --- | --- | --- |
| No `astichi` module | Installation | Install explicit Astichi dependency; current metadata omits it |
| No `yidl.concept_parser` | Artifact/import origin | Rebuild current candidate; avoid stale local dist wheel |
| Unexpected COMMA in record | Grammar | Use whitespace-separated record entries |
| Missing imported source/export | Source map/symbols | Supply all texts under stable logical keys and export the concept |
| Wrong keyword/type in fact | Generated schema | Use storage names and emitted record types |
| Duplicate identity/cardinality | Input facts | Fix identity or choose an explicit write policy; port cardinality is per address |
| Already inherited production | Concept composition | New production name and selecting matcher; no silent override |
| Duplicate matcher default/rule | Concept composition | Keep inherited default; add distinct specialization rule |
| Duplicate visible value | Contribution input scope | Avoid semantic-name collision; do not invent qualified binding syntax |
| Duplicate instance name | Build identity | Distinguish contribution `as`/numeric index while sharing resources |
| External binding already queued | Binding/build instance | Check instance identity and cause chain, not just target hole |
| Missing `build_Foo` | Assembly export | Declare `assembly Foo = Production`; inspect actual emitted names |
| Unbound `term_path` | Bind/target | Minimize original nested pattern; D17 remains unresolved |
| Failed target `next_term` | Live build graph | Check selected destination, mapped roots and indices; unresolved D17 |
| Failed to target `stores` | Wrapped error | Inspect exception cause; binding collision can look like target failure |
| Mandatory holes remain | Materialization | Wire explicit empty params/pass; no-match/suppression alone is insufficient |
| AST Load used as target | Resource shape | Use ordinary target or qualified transparent target wrapper |
| Marker survives / NameError | Marker position/capture | Check supported AST position, unresolved demand and namespace |
| Native finalization failure | Backend/materialization | Verify binary/package tuple, preserve original failure; Python success is bounded evidence |
| Output uses old resource | Regeneration/import cache | Regenerate authority and start new process |
| Golden matches but callback wrong | Verification | Independent behavior assertions, traces and raw-result checks before refresh |

[Debugging assembly](../guides/debugging-assembly.md) shows facts, matcher results,
paths and outputs to inspect. [Compatibility](../reference/compatibility.md)
distinguishes confirmed gaps, known limitations and unqualified arrangements.
No generic trace flag or native recovery guarantee is invented by this guide.
