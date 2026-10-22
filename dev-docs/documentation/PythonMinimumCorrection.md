# Python minimum wording correction

2026-10-23. Base documentation revision:
`8bf33765868d9c2e50476fc7a1698c3f0b2c4f08`.

The operator requested a narrow correction: installation requires CPython 3.12
or newer (3.12+); the previously recorded 3.12.12 test patch is reproduction
evidence, not an installation restriction.

Changed only current public installation/compatibility wording and this record.
The install example selects the 3.12 series and explains selection of another
installed 3.12+ interpreter. Qualification tables and historical evidence remain
unchanged. No new Python/backend/platform qualification is claimed. Runtime
metadata already declares `requires-python >=3.12` and was not edited.

Verification: strict MkDocs build passed; the existing active-site checker passed
35 HTML pages, 1,830 local links/assets and 90 search entries. Both served pages
returned HTTP 200 at the existing local `/yidl/` route and contained the corrected
minimum; the install page no longer selects `--python 3.12.12`. Historical
`ExampleEvidence.json`, `ExternalLinks.json` and `Verification.md` were checked
byte-for-byte against the base revision. `git diff --check` passed.

Rebuilt ignored artifacts: `build/docs-site/`, `build/docs-site-manifest.json`
and `build/yidl-documentation-html.zip` (81 files). Archive SHA-256:
`945a83e0b3b1979e7eebf6221452484babe7b8c3b0c50dfcb5ddf36e2bcb9207`.

No link repair, new qualification/tooling, compiler/metadata/dependency/consumer
changes, commit, push or deployment was performed.
