# Release Process

## Python 3.15 patch

The next patch adds CPython 3.15 to the source, Gearu and publication matrices,
retaining 3.12–3.14. See `dev-docs/Python315Release.md` for current evidence.
This does not authorize unrelated compiler or runtime changes. Astichi stays
at the already-published 1.1.3 pin.

## 0.1.1 documentation patch

The package README now links to the published documentation using absolute
URLs, so its links work when rendered on PyPI as well as GitHub. This patch
does not change compiler or runtime behavior, or dependency constraints.
Lifecycle 0.1.0 continues to use its tested, exact YIDL 0.1.0 pin.

## Initial 0.1.0 alpha

YIDL supplies the current braced concept compiler through its Python API. The existing yidl-compile entry point remains the legacy transducer route.

The supported first-use route selects the Python backend. Astichi 1.1.3 is installed automatically. Native and other platform evidence is separately bounded.

The operator selected **LGPL-2.1-only** for this package. `LICENSE` contains the
license text and both distribution types carry the license and README metadata.

## Publication order and gates

1. Prepare and publish **yidl-cache 0.1.0**.
2. Prepare and publish **yidl 0.1.0**.
3. Prepare and publish **yidl-lifecycle 0.1.0**.

Astichi 1.1.3 is already on PyPI. The three new pending publishers identify their
own `publish.yml` with no environment requirement. Astichi's existing publisher
uses its separate `pypi` environment and remains unchanged.

Commit and review the setup before planning the release from a clean checkout.
Use the manual workflow trigger to verify without uploading. For each package,
wait for its PyPI publication and verify a fresh registry-only installation before
starting the next package. A published GitHub release triggers the upload job;
creating that release is a publication action, not a build-only check.

`gearu.toml` runs source tests on Python 3.12–3.15, builds the wheel from the
sdist and requires strict Twine validation. GEARU checks ignore local sibling
source overrides; Lifecycle's checks therefore require the released upstream
packages. CI additionally verifies fresh wheel/sdist installations before upload.
Release lock refresh uses `uv lock --no-sources` so a temporary worktree never
requires neighboring development checkouts.

The automated CI matrix runs on Ubuntu with the explicit Python backend where
applicable. This does not certify native backends, every filesystem or every
platform. Existing platform evidence keeps its original revision and limits.
See the repository's publishing record in `dev-docs/` for local verification and
remaining dispositions. No release is authorized merely by adding this setup.

## Downstream integration coverage

`tests/test_yidl_lifecycle_external_smoke.py` imports the downstream Lifecycle
package. It is run separately against the combined local candidates during
preparation; the YIDL-only GEARU/CI gate explicitly excludes it so publishing
YIDL does not require publishing Lifecycle first. All other YIDL tests remain in
the gate. The consumer test is retained unchanged, not represented as passing
when Lifecycle is absent.

<!-- gearu:release:start -->
## Gearu Release Process

Gearu prepares and verifies the repository, creates an immutable tag, and can
create the GitHub Release that starts this repository's publication workflow.
It does not publish directly to package registries.

Full documentation: <https://owebeeone.github.io/gearu/>

### Install

Install the released tool with:

```sh
uv tool install gearu
```

Upgrade an existing installation with:

```sh
uv tool upgrade gearu
```

To test the unreleased `main` branch, install it directly from its repository:

```sh
uv tool install git+https://github.com/owebeeone/gearu.git
```

Verify the installation with `gearu --version`.

### Preconditions

- Read `gearu.toml` and this repository's release workflow.
- Choose an explicit release version or an explicit major, minor, or patch bump.
  Gearu does not infer release intent from commits.
- Use a clean checkout on the branch configured by `project.branch`.
- Synchronize configured release and source branches with their remote.
- Release required cross-repository dependencies first.
- Install and authenticate `gh` before requesting GitHub Release creation.

### Plan

Always inspect the read-only plan first:

```sh
gearu plan VERSION
```

Or ask Gearu to select the next version:

```sh
gearu plan --bump patch
gearu plan --bump minor
gearu plan --bump major
```

Gearu compares configured package versions with valid local and remote release
tags, then bumps the highest version. It reads remote tags directly and does not
fetch or create local tags while planning.

For a release candidate, use a numbered version such as `1.2.3-rc.1`.

Override a configured dependency tag only when the release intentionally uses a
different version:

```sh
gearu plan VERSION --dependency-tag DEPENDENCY=TAG
```

### Prepare the Local Release

After reviewing the plan:

```sh
gearu release VERSION
```

The release command can select the version itself:

```sh
gearu release --bump minor
```

This recalculates the next version at release time. To lock the version reviewed
in a prior bump plan, pass that plan's reported `VERSION` explicitly.

Gearu builds and tests in a temporary worktree. Only a successful candidate is
applied to the local release branch and tagged. This step does not change a
remote repository.

### Push and Create the GitHub Release

Push the exact release commit and tag atomically:

```sh
gearu release VERSION --push
```

Create the GitHub Release after that push:

```sh
gearu release VERSION --push --github-release
```

The final command starts workflows listening for `release.published`, including
package publication and documentation deployment where configured.

### Recovery

- If candidate checks fail, fix the problem and rerun; the normal checkout is
  left unchanged.
- If local preparation succeeds, rerun the same version with `--push`.
- If the push succeeds but GitHub Release creation fails, rerun with
  `--push --github-release`.
- If released contents must change, use a new patch or release-candidate version.
  Never move or replace the existing tag.
- If only a publication workflow fails, repair and rerun that workflow for the
  same GitHub Release.
<!-- gearu:release:end -->
