# Documentation delivery and verification

2026-10-23. Focused review gate: GO; see `Review.md`. Documentation implementation
is delivered as an uncommitted local change set and reviewable HTML artifact.
This does not certify package/release readiness or deploy anything.

## Delivered boundary

- 34 authored public pages, root README and explicit navigation/search.
- Installation, first use, current language grammar/API, DDS/matcher/assembly,
  ownership/caching, granular M01–M10 data flow, debugging and compatibility.
- Executable class generator with first/two-owner/empty/omitted-init variants;
  independent captures, interacting compound control flow and ordered raw-result
  comparison recipes. Existing canonical import/lookup/projection/callable/edge
  examples are reused rather than duplicated.
- One canonical fixture integrates the new examples and seven inspectable model
  snapshots. Assertions remain in their executable authorities.
- Fourteen fixed-revision Dataclass/Undoable/Lifecycle excerpts, attributed source
  links, source/excerpt hashes and an optional read-only provenance verifier.
- MkDocs 1.6.1 / Material 9.7.7 with resolved docs-only requirements, strict
  active HTML/search/manifest checks and build-only CI with read permission.
- `Inventory.md` accounts for all D01–D28/A01–A10 and M01–M10; unresolved parts
  remain limited. `Findings.md` records out-of-scope evidence/impact/disposition.

Compiler/runtime bytes and metadata, generated product bases, neighboring
repositories, workspace structure, release plan, paper and archived material are
unchanged. No commits, tags, pushes, release uploads or deployment were performed.
All new files use repository-relative paths. Existing tracked files have no diff.

## Qualified runtime route

Built current YIDL compiler/runtime revision
`ee5ded0854aa5b1fc0ddfa7213b765009b63bb95` into a temporary wheel. SHA-256:
`e65014dc851b14d5517ea7f1d802026314b578fb6bddc0301e5d62547a7fa716`.
Installed that wheel plus published Astichi 1.1.3 and Lark 1.3.1 in a fresh
CPython 3.12.12 environment. No editable/sibling imports in standalone runs.
Both package origins were checked as site-packages. Explicit requested/selected
engine: Python, no fallback. `ExampleEvidence.json` stores the portable result.

The pre-existing ignored dist wheel lacked concept_parser and the repository
venv lacked Astichi. Those failed setups were not treated as product behavior
failures. No package metadata repair or dependency-source modification followed.

## Checks actually run

Commands below use `python` to mean the appropriate installed runtime or docs
environment, as described in the public build/install pages.

| Check | Result / evidence boundary |
| --- | --- |
| `ASTICHI_LOWER_ENGINE=python python -m pytest tests/generation/test_yidl_lark_parser.py tests/generation/test_data_matcher_productions.py tests/generation/test_yidl_lark_update_a_diagnostics.py -q` | 108 passed in 8.55s; focused feasibility, repository YIDL source |
| `ASTICHI_LOWER_ENGINE=python python -m pytest tests/generation tests/test_yidl_goldens.py -q` | 239 passed in 61.25s; generation and canonical scope before final capture/control/comparison additions |
| `ASTICHI_LOWER_ENGINE=python python dev-docs/documentation/verify_examples.py` | Final 13 catalog commands passed against installed packages; seven copied tutorial/recipe runs outside checkout; six existing fixtures in repository cwd without PYTHONPATH |
| `ASTICHI_LOWER_ENGINE=python python -m pytest tests/test_yidl_goldens.py -q -k 'documentation_classes or fixture_sets'` | Final two focused checks passed, 42 deselected; seven model outputs and independent assertions current |
| `python dev-docs/documentation/check_consumer_provenance.py` | 14 excerpts match fixed committed source objects and hashes; no live-byte reliance |
| `python -m black --target-version py312 --check example/documentation tests/data/gold_src/documentation_classes.py dev-docs/documentation/*.py` | Nine files unchanged |
| `python -m mkdocs build --strict` | Passed final site; all advertised navigation pages exist |
| `python dev-docs/documentation/check_site.py build/docs-site` | 35 HTML pages including 404; 1,829 local links/assets; 90 search entries; no invalid local anchors/assets or excluded evidence/source files |
| Browser at local project path `/yidl/` | Home layout/code readable, explicit navigation, search returns results and opens data-flow guide; previous/next footer enabled |
| External HEAD checks | 17 links HTTP 200, official uv docs HTTP 403 from this client; availability restriction recorded in ExternalLinks.json, not misclassified as a bad link |
| Public artifact manifest | 81 files; no validation/history/dev-docs/snippet-storage leakage; no machine paths in HTML |

The site toolchain emits Material's upstream informational MkDocs-2 transition
notice; it does not fail the strict build. The qualified toolchain pins MkDocs
1.6.1. Material maintenance status is recorded; migration is not a prerequisite.
The GitHub workflow is authored and locally mirrored, not claimed to have run on
GitHub. Action tag revisions were checked directly against official repositories.

## HTML artifact and preview

- Main artifact: `build/yidl-documentation-html.zip` (contains `yidl/` project root).
- Entry HTML: `build/docs-site/index.html`.
- File/hash manifest: `build/docs-site-manifest.json`.
- Local review server exposes the built tree at the intended `/yidl/` base path.
- Archive SHA-256:
  `b64bc2b49050ea9d8ff9191af4054a171d7509317d0a9a689acde3075cd4e504`.

The build output is intentionally ignored/reproducible, not staged product output.
No production Pages job is configured. Future publication follows its own
approval and owner-selected GEARU release process.

## Remaining limits

Original nested indexed scalar propagation (D17), general D19 carrier/overhead,
Lifecycle live-type annotations, broad native handle/failure/copy/thread contracts,
full provider matrices and new two-consumer resource-wheel reproduction remain
explicitly unqualified/limited. Exact new compound and raw-comparison recipes
are qualified only for this installed Python tuple. No new native, Python-minor
or cross-host acceptance is inferred from separate original-candidate testing.

The standalone comparison is not asserted equivalent to every dataclass minor's
algorithm. Consumer excerpts explain related object-model uses without claiming
unrelated-domain generality. No invented licensing, CLI, compiler API removal or
product feature is used to close an inventory item.
