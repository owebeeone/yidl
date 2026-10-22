# End-user documentation — remediation 1 patch and evidence

Date: 2026-10-23. Author response to the two initial NO-GO reviews.
**Independent acceptance remains pending.** This document proposes the responses
below; it does not close findings or change the reviewers' verdicts.

## Object, scope and provenance

Starting/ending YIDL HEAD: `e98a22cc987342e1326384ee77cac6198b8bc647`.
The controlling brief is `EndUserDocs-RemPlan-1.md`. Both full filed reports and
the checkpoint were read before editing. This is one patch for five merged
roots: reader foundation, external paths, excerpts, help/defaults and cleanup.

Changes are confined to the named public prose/navigation, CLI help text,
excerpt selections/hashes and separately identified evidence. No compiler/runtime,
metadata, dependency, generated product base, consumer, workspace, archival or
release changes were made. The CPython 3.12+ minimum remains distinct from exact
CPython 3.12.12 execution evidence. There is no new platform qualification.

## Response map for every original finding

| Original ID | Root and patch response | Checks supplied for independent review |
| --- | --- | --- |
| Consistency P2-1 | Reader foundation: README and home recommend How YIDL works → Generation stages → Installation → First generator. Existing model/pipeline pages now explain purpose/capabilities, author inputs, two generated products, facts versus instance values, responsibilities and vocabulary in ordinary Python terms. Start Here/footer follow that sequence. | Followed the rendered home button/model/stages/install/tutorial route. Direct tutorial entry also provides the three-stage explanation before its short excerpts and full source. Full concept is the sixth code block, after the field walkthrough/stage table. A simple extension-authority decision distinguishes facts/slot input/checks, resource rules and instance values. Experienced readers retain the direct run anchor. |
| Safety P2-1 | Same reader-foundation correction; no separate architecture or framework introduced. DDS is expanded, and composable/AST/materialization/hygiene are translated before the pipeline uses them. | README links and rendered main/sidebar/footer route inspected; the author/input/YIDL/Astichi/application roles appear before reliance on the complete files. These observations support reviewer reassessment, not self-certification of end-user fitness. |
| Consistency P2-2 | External path correction: capture interpreter location and original directory before changing into a temporary tutorial copy, run its actual `generate.py`, and give an explicit local output destination. | Literal public build, first-use, external-copy and cleanup blocks were extracted unchanged from Markdown and executed in a disposable checkout copy, followed by an external copy outside that tree/workspace. Installed origins, observations and confined output verified. See LiteralWalkthrough.json. |
| Safety P3-1 | Same external-directory correction; merged severity remains P2 as specified by the lane owner. | The interpreter stays usable after `cd`; the command clears PYTHONPATH/PYTHONHOME and uses copied script-relative authority. Both generated/runtime.py and generated/model.py were observed in the external copy. |
| Consistency P3-1 | Excerpts: Lifecycle matcher selection now includes exactly pinned lines 1268–1270, through its default and closing brace; its excerpt hash/link were refreshed without changing revision or whole-source hash. Evaluated-field test includes lines 245–305, through both original-record and extracted-value assertions. | All 14 fixed-revision provenance checks pass. Served code blocks contain `default -> ManagedDefaultFacadeProperty`, both record observations and `values == (True,)`. |
| Safety P3-2 | Help/defaults: meaningful argparse descriptions/default display; tutorial option table gives default Point scenario, false switches, output filename/directory and current-directory behavior. | Public `--help` command executed in the disposable installed environment; output/defaults/effects checked without reading main(). The existing scenarios and option parsing/actions remain unchanged. |
| Safety P3-3 | Cleanup: install and first-use/inspection pages distinguish created outputs, environment/wheels and authored sources. Cleanup is optional after experimentation and targets only directories created for the walkthrough. | Literal cleanup blocks removed generated/, build/first, build/example-env and build/wheels in disposable trees. Original and copied classes.yidl/generate.py remained; all original tutorial-source hashes stayed unchanged. No new cleanup CLI. |

## Exact changed source paths

- `README.md`
- `docs/index.md`
- `docs/concepts/model.md`
- `docs/concepts/generation-pipeline.md`
- `docs/start/install.md`
- `docs/start/first-generator.md`
- `docs/start/inspect-output.md`
- `docs/guides/matching-and-data-flow.md`
- `docs/_snippets/consumers.json`
- `example/documentation/generate.py` — descriptions/formatter/help only
- `mkdocs.yml` — ordering/labels in existing navigation only

New evidence consists of this report and
`EndUserDocs-Remediation-1/{LiteralWalkthrough.json,ExampleRuns.json,RenderedChecks.json,Help.txt}`.
Original reports, prompts, plan, checkpoint and historical evidence were preserved.
All 13 pre-existing documentation Markdown/JSON evidence/review files checked at
start were verified byte-identical afterward.

## Executed verification

All commands use the existing installed runtime/docs environments; no toolchain
or dependency changes were introduced.

| Check | Observed result |
| --- | --- |
| Literal public shell walkthrough | Exit 0; fresh wheel and explicit Astichi 1.1.3 install, CPython 3.12.12, YIDL 0.1.0, actual requested/selected Python engine with no fallback; no ambient Python-path assistance |
| First-use plus external run | Both Point observations x=3/y=4 and signature x/y; copied authority resolved beside copied script; output confined to explicit directory |
| Literal cleanup | Created outputs/environment/wheels removed; original/copied authority retained and original source hashes unchanged |
| Existing verify_examples.py with separate --out | 13 installed-package runs pass; seven new tutorial/recipe runs outside checkout, six existing fixtures with installed packages |
| Existing canonical documentation/fixture-set checks | 2 passed, 42 deselected; seven canonical outputs unchanged |
| Existing consumer provenance checker | 14 fixed committed excerpts/source hashes match |
| Help/interface check | All options described; default build/documentation and false scenario defaults/current-directory behavior visible |
| AST comparison against starting revision | `generate` function and `Output` class identical; no generation algorithm or data interface change |
| Strict MkDocs build and active-site checker | 35 HTML pages including 404, 1,909 local links/assets, 110 search entries; no bad local anchors/assets/excluded output |
| Served content checks | Seven active routes HTTP 200; primary beginner button targets the model; full source follows explanation; decisive excerpt content present |
| Browser inspection | Home → model → stages → install → first generator followed; layout/readable text inspected; search for DDS returned 12 documents including the introduction's definition |
| Formatting/diff check | Black check for the sole changed Python file and git diff --check pass |

The runtime catalogue result and exact literal commands are newly recorded in the
round-specific evidence directory. Historical ExampleEvidence.json,
ExternalLinks.json, Verification.md and earlier correction evidence were not
updated to represent these runs as old results. External links were not rechecked
or repaired in this patch.

## Review artifact and limitations

The existing served preview remains at the local `/yidl/` route. Rebuilt ignored
artifacts: `build/docs-site/`, `build/docs-site-manifest.json` and
`build/yidl-documentation-html.zip` (81 files). Archive SHA-256:
`0a841c895490edc4e6f5c82bba5840994eb6832e4dadabf826255e05d9166cda`.

No shared compiler/runtime semantics, generator interface, package boundary or
platform contract changed. The example's CLI help presentation changed, while
names/actions/defaults remained the same. The installed walkthrough qualifies
this Mac/Python tuple; its POSIX command presentation is not a Windows or native
backend acceptance claim. Existing unsupported/limited contracts remain as
recorded. No new feature, licensing choice, metadata repair or product fix was
used to satisfy an editorial finding.

The author performed no commits, pushes, tags or deployment. The lane owner must
settle the revised tuple and request the original reviewers' focused closure
reports. Acceptance remains their decision.
