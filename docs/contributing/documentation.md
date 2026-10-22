# Maintain executable documentation

Public content lives in `docs/`. Existing design and validation originals remain
preserved but excluded from the built site. Internal plans, reviews, evidence and
inventory dispositions belong in `dev-docs/documentation/`, outside public output.
Do not repair references to archived/history material as incidental cleanup.

## Build and check

```sh
uv venv build/docs-env --python 3.12
uv pip install --python build/docs-env/bin/python -r docs-requirements.txt
build/docs-env/bin/python -m mkdocs build --strict
build/docs-env/bin/python dev-docs/documentation/check_site.py build/docs-site
```

The dependency file pins the resolved documentation toolchain independently of
runtime dependencies. Material 9.7.7 / MkDocs 1.6.1 is the qualified build tuple.
The [upstream installation guidance](https://squidfunk.github.io/mkdocs-material/getting-started/)
recommends isolated pip installation; Material is maintained through 2027-05-05.
A future migration is a maintenance decision, not required for this artifact.

## Add a recipe

Keep executable authority under `example/` or the existing canonical fixture
harness. First assert intended behavior, then snapshot readable generated output.
Use the site's `source` inclusion token for examples/outputs rather than copying
them into prose. The build hook validates repository-relative paths and includes
the exact bytes. New fixture successes belong in the canonical golden harness;
bespoke tests are for narrow diagnostics/edge recognition.

```sh
ASTICHI_LOWER_ENGINE=python build/example-env/bin/python \
  tests/data/gold_src/documentation_classes.py build/proposed-goldens
ASTICHI_LOWER_ENGINE=python build/example-env/bin/python -m pytest \
  tests/test_yidl_goldens.py -q -k documentation_classes
```

Review proposed source against independent assertions before copying intentional
changes into canonical goldens. Record package versions, import origins, actual
backend, Python patch and command exit. A selected native request alone is not
native-dispatch evidence. Do not mark an inventory ID closed by adding a heading;
link evidence or preserve an explicit limited/deferred disposition.

The site check validates active local HTML links/anchors/assets, search entries,
base-path-safe links and excluded output. External URL availability is separately
checked; network failures must not silently alter contract claims.
