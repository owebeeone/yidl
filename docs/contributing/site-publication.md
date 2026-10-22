# Preview and prepare publication

The current deliverable is a **built artifact**, with build-only CI. It does not
deploy a site, upload a package or change repository Pages settings.

Follow [documentation build instructions](documentation.md). Preview locally:

```sh
build/docs-env/bin/python -m mkdocs serve --dev-addr 127.0.0.1:8000
```

Open the displayed URL and try search for `FieldName`, follow a guide/reference
link, inspect code blocks and check narrow-screen navigation. The production base
URL is configured for `https://owebeeone.github.io/yidl/`; this is the intended
project-site path, not a claim that a live deployment exists.

## Build-only CI

The documentation workflow installs the pinned site dependencies, builds strictly,
runs active HTML/search/output checks, and retains an artifact. It has no Pages
deployment job or write permission. Runtime examples have their separate qualified
installation instructions and canonical test command; a site build alone does
not establish their semantics.

## Future publication gate

Before a separately authorized deployment, verify repository ownership/visibility,
Pages eligibility, Actions/environment controls, exact source revision, artifact
hash and base URL. Review the completed HTML first. Use a dedicated Pages job
with minimal scoped permissions and retain the prior artifact for rollback.
Do not enable automatic production deployment as an incidental docs update.

The project owner selected **GEARU** for eventual release tooling. Release
configuration/operations are outside this documentation task. Tagging, commits,
pushes, registry upload, releases and site deployment each need applicable
authorization. A planning GO is not implementation or release acceptance.

After an authorized deployment, verify homepage/navigation/search and the public
install route against the approved revision. If bad, redeploy the prior approved
artifact rather than moving a published release tag. Keep development docs labeled
as such until they match a qualified supported release.
