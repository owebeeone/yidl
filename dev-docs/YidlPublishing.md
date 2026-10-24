# YIDL release preparation and publication

## Scope and publisher identity

The operator authorized release setup in YIDL, Cache and Lifecycle, including
YIDL's missing Astichi dependency, and selected LGPL-2.1 for all three packages.
This work changes packaging metadata, release configuration, release guidance
and the public installation instructions. Astichi, other consumers, GEARU's
implementation and GWZ configuration remain reference-only. Compiler semantics
and the legacy CLI are unchanged. No commit, push, tag, GitHub release, package
upload or site deployment is performed by this setup task.

The pending publisher identifies `owebeeone/yidl`, workflow `publish.yml`, with
no required environment. The publish job uses the official PyPA action and
job-local `id-token: write`, without a token secret or environment requirement.
Astichi's existing `pypi` environment is separate and unchanged. See
[PyPI's trusted-publishing guide](https://docs.pypi.org/trusted-publishers/using-a-publisher/).

## Resolved preparation gaps

- YIDL declares `astichi==1.1.3`, the published SDK tested here. Installing either
  artifact now obtains Astichi automatically; the smoke gate injects no SDK.
- Metadata points to the README and source/issue URLs. `LICENSE` and SPDX
  `LGPL-2.1-only` metadata record the owner's license decision. Hatchling's
  minimum supports these metadata fields; both artifacts carry the license.
- `gearu.toml`, `.release.env` and `RELEASE.md` configure the selected preparation
  route. A small owned script synchronizes or verifies `yidl.__version__` against
  metadata; GEARU declares that file among its managed release files.
- Release checks install the candidate itself so generated-output subprocesses
  can import it on every interpreter. They ignore sibling source overrides.
  Lock refresh also uses `--no-sources`.

The earlier fresh-install `ModuleNotFoundError: astichi`, missing GEARU config,
missing license and absent README metadata were confirmed before these changes.
They are resolved here under the operator's expanded release-setup authorization.

## Workflow and publication sequence

Manual **Run workflow** builds and verifies without publishing. Publishing a
GitHub release checks out its exact tag and uploads only after all gates pass.
Tags must be `v` plus the metadata version, which must match `yidl.__version__`.

The build job builds the wheel from the sdist, runs strict Twine validation,
then installs wheel and sdist independently outside the checkout using only
registry dependencies. Each executes compiler imports and the documentation's
first-generator recipe. A separate Ubuntu matrix runs repository tests with the
explicit Python backend on CPython 3.12, 3.13 and 3.14.

The downstream `tests/test_yidl_lifecycle_external_smoke.py` is excluded from the
YIDL-only gate: importing Lifecycle before YIDL is published would reverse the
required publication order. The test remains unchanged and is verified
separately against the combined candidates. All other YIDL tests stay in the
gate. No test is represented as passing merely because it was excluded.

Only release events in `owebeeone/yidl` can upload. The upload job downloads the
verified artifacts without rebuilding; all actions use pinned upstream commits.
Concurrency does not cancel an active upload, and existing versions are not
silently skipped. See `RELEASE.md` for the GEARU route. Commit and review this
setup before a clean-checkout `gearu plan 0.1.0`; a full plan has not been run
against this uncommitted tree.

Publish Cache 0.1.0, then YIDL 0.1.0, then Lifecycle 0.1.0. Confirm each registry
publication and fresh registry-only installation before starting the next.
Creating a published GitHub release starts an upload; use the manual trigger
for the prior build-only verification.

## Local evidence and limits

Preparation date: 2026-10-25. Source baseline:
`4550f690f0b325a6d425e4ed5f0ae1051cdfd2d1` plus this uncommitted setup.
Local matrix: macOS arm64, CPython 3.12.12, 3.13.12 and 3.14.3,
`ASTICHI_LOWER_ENGINE=python`, published Astichi 1.1.3, Black 26.3.1,
pytest 8.4.2. Local candidate versions are 0.1.0.

- Wheel and sdist build and pass strict Twine checks; metadata and license
  contents are inspected. Fresh installations use only declared dependencies,
  and compiler imports plus the first-generator recipe pass outside the checkout.
- Each interpreter passes 299 source tests with 2 skips; results are recorded in
  ignored `build/release-tests-<python>.log` files. The two existing skipped
  baseline cases explicitly defer handcrafted/generated Lifecycle samples.
- The separate downstream consumer smoke passes on all three interpreters using
  the local Lifecycle and Cache wheels plus published Astichi. This is candidate
  integration evidence, not registry-only availability of those new packages.
- Version synchronization has positive and negative fixture checks. Workflow
  syntax, version/tag rejection, GEARU config loading and strict documentation
  build/link checks are verified locally.

This does not claim native-backend qualification, new cross-platform evidence,
a hosted Actions run, a successful OIDC exchange, or independent release review.
Existing evidence keeps its original scope and revision. The publication gate
still requires a committed/reviewed candidate and the ordered hosted checks.

## Release documentation and review follow-up

The operator subsequently authorized the Cache/Lifecycle user-guide corrections,
release-triggered YIDL Pages publication, and a correctness/readability review.
This adds current installation/first-use routes, task-oriented reference links,
cache troubleshooting and Lifecycle public docs in its sdist. It does not change
compiler semantics or deploy a release during preparation. Pyrolyze's separately
authorized sentinel migration remains owned by that repository.

The Pages configuration uses Actions and the project's HTTPS URL. Deployment
uses the exact published release tag, requires matching version metadata, and
is scoped to the owning repository's release events. The environment permits
`v*` tags. Manual/PR runs remain build-only. The deployment downloads the built
Pages artifact; it does not rebuild or use a moving main-branch checkout. The
PyPI and Pages workflows are separate: inspect both after a release.

The local review has two passes: correctness against source/dependency metadata
and executed examples, then a human reading-path pass from installation through
first result and task reference. Findings corrected in this cycle include the
missing Lifecycle docs in the sdist, stale Cache status text, an unlinked mixed
Lifecycle draft/proposal, old completion-failure wording and a hard-coded wheel
version in docs CI. Proposed APIs are now separate and clearly unavailable.
This is a self-review with executable checks, not an independent reviewer GO.

Local checks include strict MkDocs, HTML/assets/search validation, consumer
Markdown targets/anchors, installed tutorial and cold/warm consumer examples,
workflow syntax, release-tag rejection and preview/deployment separation. The
first hosted deployment/OIDC exchange remains a release-time check; repository
settings alone do not prove live content was published.
