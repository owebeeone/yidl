# Preview and release publication

The documentation site is published to
[owebeeone.github.io/yidl](https://owebeeone.github.io/yidl/) when a YIDL GitHub
release is published. The release workflow builds the exact tag's sources;
package upload and documentation deployment are separate jobs/workflows and
must both be checked. Configuring this route does not mean the first site or
package release has already been published.

## Preview before release

Follow the [documentation build instructions](documentation.md), then preview:

```sh
build/docs-env/bin/python -m mkdocs serve --dev-addr 127.0.0.1:8000
```

Check the reading order, search for `FieldName`, follow guide/reference links,
inspect code blocks and narrow-screen navigation. Pull requests and manual
workflow runs execute installed examples, strict MkDocs and HTML/search checks,
then retain a preview artifact. They do not deploy the production site.

## Release route

The operator selected GEARU for release preparation; see
[the repository release process](https://github.com/owebeeone/yidl/blob/main/RELEASE.md).
The release event must use a tag matching the package version and its public
version mirror. The documentation build checks out that tag, installs the
pinned site toolchain and a freshly built package, executes the public examples
and canonical tutorial checks, and validates the built site.

Only a published release in the owning repository uploads the Pages artifact
and starts deployment. The deployment job has scoped Pages/OIDC write
permissions and uses the `github-pages` environment. Its repository policy
allows release tags matching `v*`; preview runs carry no deployment permission.
GitHub Pages is configured to use Actions, with HTTPS and the project-site base
path. The workflow does not create a release or publish a package by itself.

After release, inspect both the PyPI workflow and documentation workflow. Verify
the live homepage, navigation, search and installation instructions against the
released candidate. If deployment fails, repair and rerun the release workflow
for that immutable tag; do not move or reuse a release tag. If released source
content is wrong, prepare a corrected release. Earlier artifact/evidence records
retain their original build-only scope.
