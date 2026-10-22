# Split a project and regenerate

A source map is an explicit mapping of logical filenames to source text. The
entry name is a **map key**, not the module declaration and not a search through
the filesystem. Keep logical keys stable when packaging files.

The canonical two-file example is executable on its own:

```sh
ASTICHI_LOWER_ENGINE=python build/example-env/bin/python \
  tests/data/gold_src/yidl_imported_concepts.py build/imported.py
```

{{source:tests/data/gold_src/yidl_imported_concepts.py|python}}

`export concept LifecycleCore` makes the base available to imports. The importing
file uses an alias and extends that concept. The filename spelling in the import
is resolved relative to the logical importer key. For three files, supply all
three texts in the map; imports do not fetch omitted resources from the current
working directory. Relative keys such as `shared/base.yidl` and `app/model.yidl`
allow `../shared/base.yidl` without a sibling-checkout dependency.

## Packaged authority

A package can read its `.yidl` assets with `importlib.resources.files(package)`
and pass those texts under stable logical names. Include the assets in wheel and
sdist, or distribute a generated runtime base with an explicit build authority.
Runtime requirements depend on the generated module's imports: a checked-in base
still uses YIDL runtime descriptors and Astichi when it assembles models.

A consumer regeneration tool should default to comparing emitted bytes, provide
an explicit write mode, and record source digests. YIDL's concept API does not
provide a universal `--write` CLI. Existing consumer tools implement their own
check/write contract; do not invent a compiler flag.

After editing authority, regenerate the base, inspect the diff, run behavior
checks, then refresh canonical output. Start a new process to discard previously
imported generated modules or cached wrappers. [Shared resources](../guides/shared-resources.md)
explains provenance and missing-authority handling.

A missing source-map key is an import/setup error; a concept not exported by its
source is a symbol error. Do not patch imports into generated Python as a remedy.
