# Documentation inventory disposition

2026-10-23. This register accounts for the original experienced and anticipated
items. **Documented** means the supported bounded route is taught with indicated
executable evidence. **Limited** means the unresolved or unqualified part is
explicitly retained; it is not closed as an implementation feature. No heading
or site build is treated as proof of runtime support. The original inventory
and plan remain unchanged.

Paths below are relative to the YIDL repository. All public pages are under
`docs/`; actual command/tuple results are in `ExampleEvidence.json` and
`Verification.md`. Canonical success assertions remain in their owning examples,
not duplicated in a new bespoke suite.

| ID | Observation / documentation bridge | Public owner and evidence | Disposition |
| --- | --- | --- | --- |
| D01 | Definitions, fact classes, user classes confused | concepts/model; tutorial shows ClassRow/FieldRow vs Point | Documented |
| D02 | Complete compiler/library/fact/AST path missing | start/first-generator; installed generate.py and canonical output | Documented |
| D03 | Record commas rejected | reference/language exact grammar; parser and diagnostics tests | Documented |
| D04 | Semantic versus storage spelling | reference/data-model, matching/data-flow; FieldName → field_name → x | Documented |
| D05 | Resource/receiving shape mismatch | concepts/surfaces-and-shapes; zero/one/many params/statements and existing fixtures | Limited: not a universal scalar/argument/tuple/backend matrix |
| D06 | Desired Python-to-resource bridge | first-generator, gallery; direct stores/signature/slots verified | Documented for tutorial; rich cases reference qualified consumers |
| D07 | Attribute spelling mistaken for demand | scopes-and-targets; external slot path produces direct self.x | Documented |
| D08 | Reference annotation survived | constructors-and-calls; fixed Dataclass identifier capture excerpts | Limited: failed marker arrangement/live Lifecycle fix not promoted |
| D09 | Load context used as target | scopes-and-targets, bridge; tutorial transparent Store and existing diagnostics | Limited: broad AugStore/Delete matrix not freshly qualified |
| D10 | Keeps, outer references, object captures confused | binding-and-ownership; executable captures.py + tutorial | Documented bounded capture and outer-read route |
| D11 | Empty selection failed mandatory surfaces | surfaces-and-shapes; empty and disabled canonical modes | Documented with explicit fillers; no-match differs from suppression |
| D12 | Source maps/imports/package resources unclear | project-layout/shared-resources; imported-concepts standalone fixture | Limited: generic source-map route verified, new resource-wheel experiment not supplied |
| D13 | Duplicate inherited production | composition/extending-concepts; existing parser extension diagnostics | Documented |
| D14 | Inherited default not override | composition/matchers; matcher/parser tests and fixed consumer rules | Documented |
| D15 | Resource versus instance-name reuse | assembly/debugging; two-owner tutorial and cause-chain observation | Documented bounded identity remedy |
| D16 | Identity/owner/index/order/path confused | matching/data-flow/assembly; two owners, composite numeric index, reversed rows | Documented; canonical indexed selector fixture supports path explanation |
| D17 | Nested scalar binding propagation unresolved | expressions-and-order/compatibility/troubleshooting | Limited: original mechanism unresolved, no claim repaired by flat pattern |
| D18 | Flat alternative must preserve raw semantics | expressions-and-order; fixed consumer comparison provenance and original inventory evidence | Documented bounded comparison.py raw-result/order/empty recipe; not universal dataclass equivalence |
| D19 | Bare scalar reference/carrier ambiguity | surfaces/bridge/compatibility | Limited: no blanket expression support or no-overhead claim |
| D20 | Stale generated base after resource change | project-layout/inspect-output; clear authority/regeneration/process lifetime | Documented; no invented generic write CLI |
| D21 | Missing assembly export | first-generator/API/assembly; build_Module executed | Documented |
| D22 | Errors opaque across stages | pipeline/debugging/troubleshooting; metadata, facts/results, selector helpers | Documented supported inspection; no invented tracing facility |
| D23 | Opaque Python objects treated as literals | generated-values/ownership; hostile repr and two namespace captures | Documented and executable |
| D24 | Template/class/value caches confused | caching-and-performance; wrapper identity + independent captures | Documented bounded sharing; native/thread safety remains unqualified |
| D25 | Generation cost confused with hot access | home/pipeline/performance; direct store output | Documented without benchmark claims |
| D26 | Protected parser interval/ownership unclear | pipeline/performance/compatibility; actual source route qualified | Documented without changing implementation policy |
| D27 | Backend/version origin evidence missing | install/compatibility; installed package evidence with explicit selected Python | Documented narrow tuple; no universal cross-platform claims |
| D28 | Goldens mistaken for behavioral oracle | inspect-output/gallery/contributing; tutorial behavior before snapshots | Documented |
| A01 | Input order, weights, defaults and overlap | matchers/data-flow; matcher suite including two-input evaluated field | Documented distinction between generic DDS and contribution selection |
| A02 | Nested edge environments | generated-values + vertical fixture | Limited: one-record edge evaluation explicit; no unverified general two-record nested edge recipe |
| A03 | Wrapper/import/literal domains | generated-values; matcher suite and captures.py rejection | Documented actual astichi_template factory (not assumed from_astichi_template alias) |
| A04 | Operations/producers/snapshots | fact-production/data-flow; callable facts, projection fixtures and operations tests | Documented generic/consumer boundary |
| A05 | Collection/port cardinality, lookup, policy | data-model; composite lookup, write/port/computed tests in 239-check scope | Documented |
| A06 | Factory argument/provider/dependency policy | constructors/fact-production/consumers; callable fact fixture and fixed consumer facts | Limited: no universal provider/cycle resolver, consumer cases not all independently rerun |
| A07 | Compound construct surfaces | classes-and-methods/bridge/language exact grammar | Documented control_flow.py exact interacting constructs/zero-one-many; other positions/minors unqualified |
| A08 | Deferred state/copy/materialization failures | ownership/assembly/performance/compatibility | Limited: no broad foreign-handle/native recovery/repeated-materialization contract |
| A09 | One packaged authority across consumers | project-layout/shared-resources/fixed consumer provenance | Limited: no new two-consumer wheel/sdist resource-sharing experiment |
| A10 | Local policy removal and retained references | gallery/consumers; exact fixed field-removal fixture link | Limited: consumer-specific deletion evidence, no new generic removal API |

## M01–M10

`guides/matching-and-data-flow.md` owns the full granular map. M01/M02/M08/M09/M10
are demonstrated by the two-owner tutorial; M03 by composite lookup; M04/M05/M07
by existing matcher/projection/diagnostic coverage; M06 includes the exact existing
multi-input evaluated-field test and explains emitted evaluator_names separately.
Every referenced current source test was in the executed generation suite. This
is not a claim that generic DDS and contribution-language qualification syntax
are interchangeable. Nested two-record template edges remain A02 limited.

## Reading/site disposition

Thirty-four authored public pages provide the task-oriented route. Existing
`docs/YIDL*.md` design files and all `docs/validation/` content remain in place and
are explicitly excluded from site output. Plans/reviews/history are outside the
public docs tree. No archival references were repaired. Frozen consumer snippet
metadata is also excluded; only curated attributed code appears in pages.
