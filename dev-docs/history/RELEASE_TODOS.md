# YIDL Release TODOs

Documentation audit: 2026-10-11.

The nine Markdown documents under `docs/` were reviewed against the active
implementation. The documentation is not yet ready for release: it consists
primarily of design notes and validation studies, with substantial gaps in
user-facing guidance and outdated descriptions of the compiler.

This checklist records release preparation work, not a design override or
acceptance of changes to public semantics. The
[design summary](YidlDesignSummary.md) remains the canonical semantic/design
reference, and [coding rules](YidlCodingRules.md) remain the implementation
authority.

## 1. Correct product scope and architecture

- [ ] Describe YIDL's current generic concept/DDS/assembly compiler role and
  its relationship to `yidl-lifecycle`.
- [ ] Reconcile the “normative” labels in the split design documents with the
  canonical developer summary.
- [ ] Replace active descriptions of the old indentation/recursive-descent
  parser with the current Lark-based, braced concept syntax.
- [ ] Remove or explicitly classify the advertised `yidl.embed(...)` path,
  which the current public API does not provide.
- [ ] Assign lifecycle-specific runtime documentation to its appropriate
  owner and separate historical designs from released behavior.

Evidence: [developer index](README.md),
[frontend design](../docs/YIDLFrontendDesign.md),
[codegen design](../docs/YIDLCodegenDesign.md), and
[runtime class model](../docs/YIDLRuntimeClassModel.md).

## 2. Fix packaging and document installation

- [ ] Declare the active compiler's Astichi dependency and establish its
  supported version requirements.
- [ ] Add installation instructions and supported Python/dependency versions.
- [ ] Verify installation and compiler imports in an isolated environment
  outside the GWZ workspace.

Release blocker: [package metadata](../pyproject.toml) declares only Lark, but
the active compiler imports Astichi. During the audit, importing
`yidl.concept_parser` in the existing YIDL environment failed with
`ModuleNotFoundError: astichi`. This requires a packaging fix alongside the
documentation.

## 3. Add a runnable quickstart for the current compiler

- [ ] Provide a minimal standalone `.yidl` concept example.
- [ ] Walk through compilation, runtime source emission, record creation,
  and generated output.
- [ ] State the expected output and how to run the example with installed
  release dependencies.
- [ ] Verify the example end to end outside GWZ.

Existing examples and [codegen guidance](../docs/YIDLCodegenDesign.md)
concentrate on lifecycle factories and hand-crafted target shapes rather than
providing an introduction to the current compiler.

## 4. Write a language reference

- [ ] Document modules, imports/exports, concept composition, and symbol
  resolution.
- [ ] Document properties, records/families, collections, and resources.
- [ ] Document embedded Python snippet syntax and its handling.
- [ ] Document matchers, operations, contributions, productions/phases, and
  assemblies.
- [ ] Document bindings, paths, and diagnostics.
- [ ] Explain ordering, conflicts, restrictions, and failure behavior for
  each surface, alongside syntax and examples.

The implemented [grammar](../src/yidl/concept_grammar.lark) contains
substantial functionality without a corresponding user reference.

## 5. Define and document the supported Python API

- [ ] Establish the supported import paths and public API boundary.
- [ ] Document `compile_yidl_files` and compiled modules/concepts.
- [ ] Document recorded builders, DDS containers, source emission, and
  assembly execution.
- [ ] Distinguish supported APIs from compatibility and experimental surfaces.
- [ ] Resolve the status of the old parser symbols still exposed by the
  top-level package.

Evidence: [top-level exports](../src/yidl/__init__.py),
[concept compiler](../src/yidl/concept_parser.py), and
[existing design gap notes](YidlDesignSummary-gaps2.md).

## 6. Resolve the CLI story

- [ ] Decide whether to replace, retire, or explicitly label the old
  `yidl-compile` prototype.
- [ ] Publish an authoritative compilation command or Python workflow.
- [ ] Document arguments, output behavior, diagnostics, and failure behavior
  for the supported workflow.

The installed command still runs the old transducer-to-`LCKind` API-generation
prototype in [cli.py](../src/yidl/cli.py), rather than the active concept
compiler.

## 7. Document generated-code requirements and limitations

- [ ] Explain the dependencies required by emitted modules.
- [ ] Document generation, regeneration, and artifact verification workflows.
- [ ] Establish compatibility promises for source syntax, Python APIs, and
  generated artifacts.
- [ ] Identify released, experimental, deferred, and historical features.
- [ ] Add troubleshooting for syntax, symbol, matcher, operation, and assembly
  failures.
- [ ] Identify the release status and owner of unresolved semantic questions.

The [runtime class model](../docs/YIDLRuntimeClassModel.md) leaves semantic
questions open without explaining their release status or owner. Generated
assembly runtime behavior is implemented in
[assembly_source.py](../src/yidl/generation/assembly_source.py).

## 8. Add navigation and release material

- [ ] Add a `docs/README.md` landing page with a clear reading order.
- [ ] Add a root README describing the product and linking to installation,
  quickstart, and reference material.
- [ ] Add a license file and corresponding package metadata.
- [ ] Add a changelog or release notes.
- [ ] Publish a support/version policy and known limitations.
- [ ] Add a release checklist covering isolated installation, packaged grammar
  availability, and an end-to-end example outside GWZ.

At audit time, the repository had no root README, license file, changelog, or
`docs/README.md`.

## 9. Clarify validation evidence

- [ ] Update the validation index's PRE_IMPL descriptions and distinguish
  archived plans from current requirements.
- [ ] Document current validation commands and their prerequisites, including
  sibling-checkout requirements where applicable.
- [ ] Record results with Python/dependency versions and describe what each
  study proves.
- [ ] Document benchmark invocation and distinguish the exploratory Python
  matrix from supported release versions.
- [ ] Keep validation-only examples distinct from supported product examples.

Evidence: [validation index](../docs/validation/README.md),
[study contract](../docs/validation/study/CONTRACT.md), and
[performance validation](../docs/validation/perf/README.md).

## Audit verification

Focused validation passed **20 tests** across
`docs/validation/study` and `docs/validation/generated_example` on Python
**3.12.12**, using the existing environment:

```sh
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 PYTHONDONTWRITEBYTECODE=1 \
  .venv/bin/python -m pytest \
  docs/validation/study docs/validation/generated_example \
  -q -p no:cacheprovider
```

These checks exercise the older lifecycle studies and examples. They do not
verify standalone installation of the active compiler, a release build, or the
full regression suite. The initial audit made no file changes.

## Recommended order

1. Resolve product scope, public API, and CLI decisions.
2. Fix packaging and provide a verified quickstart.
3. Write the language/API references and generated-code guidance.
4. Complete navigation, release material, and validation documentation.
