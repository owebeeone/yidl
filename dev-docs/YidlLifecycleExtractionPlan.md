# YIDL Lifecycle Extraction Plan

## Goal

Split the transactional lifecycle decorator into a new `yidl-lifecycle`
project while keeping `yidl` focused on the generic compiler substrate:
grammar, concept compilation, matcher/assembly lowering, generated-runtime
support, and golden-test tooling.

This should be a staged extraction. The lifecycle implementation is still a
strong consumer of YIDL features, so the first split should prioritize a clean
package boundary and compatibility, not independent release cadence.

## Why Now

The lifecycle implementation is no longer just internal test coverage. It now
has:

- a user-facing decorator and marker API
- a generated lifecycle module checked into runtime code
- transaction manager and binding runtime support
- split lifecycle YIDL layers
- Pyro lifecycle parity tests and representability probes
- generated-source goldens and constructor performance fixtures

Keeping this inside `yidl` makes core YIDL look lifecycle-specific and makes it
harder to test YIDL as a generic compiler framework for other domains such as
FastAPI, protobuf, or cross-language Astichi targets.

## Target Package Boundary

### Stays In `yidl`

Core YIDL owns generic compiler functionality:

- `src/yidl/concept_grammar.lark`
- `src/yidl/concept_parser.py`
- `src/yidl/generation/*`
- `src/yidl/cli.py`
- `src/yidl/testing/versioned_test_harness.py`
- generic golden harness support
- generic non-lifecycle YIDL fixtures and goldens
- core docs for concepts, resources, matchers, productions, assemblies,
  operations, phases, and import/merge behavior

YIDL may keep a small external-consumer smoke test that imports
`yidl_lifecycle`, compiles one lifecycle fixture, and proves the public YIDL API
still supports a real downstream concept. That smoke test should not duplicate
the lifecycle project's full success coverage.

### Moves To `yidl-lifecycle`

Lifecycle owns:

- `src/yidl/runtime/lifecycle.py`
- `src/yidl/runtime/lifecycle_markers.py`
- `src/yidl/runtime/lifecycle_harvester.py`
- `src/yidl/runtime/_generated_lifecycle_base.py`
- `src/yidl/runtime/transaction_yidl.py`
- `src/yidl/runtime/bindings.py`
- `src/yidl/runtime/bindings_refcount.py`
- `tests/data/yidl/yidl_transactional_lifecycle/*`
- `tests/data/yidl/yidl_transactional_phase_a_base/*`
- lifecycle materialized goldens:
  - `yidl_transactional_lifecycle_core`
  - `yidl_transactional_lifecycle_local_store`
  - `yidl_transactional_parity_fields1`
  - `yidl_transactional_phase_a_base`
  - `yidl_transactional_phase_b_decorator`
  - `yidl_transactional_phase_c_default_factories`
  - `yidl_transactional_phase_f_hooks`
  - `yidl_transactional_phase_g_transient`
  - `yidl_transactional_phase_h_owned`
- lifecycle golden source fixtures with `yidl_transactional_*` names
- `tests/test_lifecycle_decorator.py`
- `tests/test_lifecycle_harvester.py`
- `tests/test_lifecycle_markers.py`
- `tests/test_lifecycle_pyro_lcm_representability.py`
- `tests/test_lifecycle_yidl_layering.py`
- `tests/test_transaction_yidl.py`
- `tests/test_bindings.py`
- `tests/test_bindings_refcount.py`
- `tests/lifecycle/*`
- `tests/data/perf/*lifecycle*`
- lifecycle-specific docs, including phase plans, field-kind matrix, parity
  plans, and Pyro gap discussions

### Stays Temporarily As A Compatibility Shim

For one transition window, `yidl` should keep import compatibility by
re-exporting from `yidl_lifecycle`.

Examples:

```python
# yidl.runtime.lifecycle
from yidl_lifecycle.lifecycle import *  # noqa: F401,F403
```

```python
# yidl.runtime.transaction_yidl
from yidl_lifecycle.transaction_yidl import *  # noqa: F401,F403
```

```python
# yidl.runtime.bindings
from yidl_lifecycle.bindings import *  # noqa: F401,F403
```

The shim should emit no warnings initially. Warnings can be added after the
first migrated consumer has landed and CI has a clean import path.

## Proposed `yidl-lifecycle` Layout

```text
yidl-lifecycle/
  pyproject.toml
  src/
    yidl_lifecycle/
      __init__.py
      lifecycle.py
      lifecycle_markers.py
      lifecycle_harvester.py
      _generated_lifecycle_base.py
      transaction_yidl.py
      bindings.py
      bindings_refcount.py
      yidl/
        lifecycle_base.yidl
        lifecycle_core.yidl
        lifecycle_managed.yidl
        lifecycle_default_factories.yidl
        lifecycle_transient.yidl
        lifecycle_owned.yidl
        lifecycle_const_static.yidl
        lifecycle_local_store.yidl
  tests/
    data/
      gold_src/
      goldens/
      yidl/
      perf/
    lifecycle/
    test_lifecycle_decorator.py
    test_lifecycle_harvester.py
    test_lifecycle_markers.py
    test_lifecycle_pyro_lcm_representability.py
    test_lifecycle_yidl_layering.py
    test_transaction_yidl.py
    test_bindings.py
    test_bindings_refcount.py
  dev-docs/
    ...
```

The package should depend on `yidl` and `astichi`. It should not import from
private `yidl.tests` modules; any needed test harness support should either be
copied as test code or exposed as a generic public helper from `yidl`.

## Generated Import Policy

Generated lifecycle source currently imports runtime helpers from
`yidl.runtime.*`.

After extraction, lifecycle YIDL should emit imports from `yidl_lifecycle.*`:

```python
from yidl_lifecycle.lifecycle import _HAS_DEFAULT_FACTORY
from yidl_lifecycle.transaction_yidl import DEFAULT_TRANSACTION
from yidl_lifecycle.transaction_yidl import TransactionManager
from yidl_lifecycle.bindings import BindingBase, BindingDict
```

During the compatibility window, old generated goldens may still import
`yidl.runtime.*` through shims. New `yidl-lifecycle` goldens should pin the new
imports.

## Compatibility Policy

The initial extraction keeps `yidl.runtime.lifecycle`,
`yidl.runtime.transaction_yidl`, `yidl.runtime.bindings`, and
`yidl.runtime.bindings_refcount` as warning-free compatibility shims.

Do not add deprecation warnings in this roll-build. Warning-free shims keep
existing local consumers stable while `yidl-lifecycle` proves the new import
surface and while downstream projects move at their own pace.

Future cleanup should be a separate compatibility decision after at least one
real downstream consumer has moved to `yidl_lifecycle.*` imports. That later
decision can choose one of:

- keep the shims indefinitely
- add deprecation warnings
- remove the shims in a major-version boundary

## Slice Plan

### Slice 1: Create The Package Skeleton

Create a new local project or submodule `yidl-lifecycle` with:

- `pyproject.toml`
- `src/yidl_lifecycle/__init__.py`
- empty test tree
- editable dependency on local `yidl`
- test dependency on `black` and `pytest`

Verification:

```bash
cd yidl-lifecycle
PYTHONPATH=../astichi/src uv run pytest -q
```

Expected result: package imports and empty/basic tests pass.

### Slice 2: Move Runtime Modules

Move lifecycle runtime modules into `yidl-lifecycle`:

- `lifecycle.py`
- `lifecycle_markers.py`
- `lifecycle_harvester.py`
- `_generated_lifecycle_base.py`
- `transaction_yidl.py`
- `bindings.py`
- `bindings_refcount.py`

Update internal imports to `yidl_lifecycle.*`.

Add temporary shims in `yidl/src/yidl/runtime/*` that re-export from the new
package.

Verification:

- `yidl-lifecycle` runtime tests pass.
- `yidl` tests that import old paths still pass through shims.

### Slice 3: Move Lifecycle YIDL Sources

Move lifecycle YIDL files into `yidl-lifecycle/src/yidl_lifecycle/yidl`.

Update runtime build/generation code so the generated lifecycle module can be
rebuilt from package-relative YIDL paths, not from `tests/data/yidl`.

Update Astichi/YIDL source snippets to import from `yidl_lifecycle.*`.

Verification:

- regenerate `_generated_lifecycle_base.py` in `yidl-lifecycle`
- run lifecycle decorator tests
- run lifecycle YIDL layering tests

### Slice 4: Move Lifecycle Goldens And Perf Fixtures

Move lifecycle golden source fixtures and materialized outputs into
`yidl-lifecycle/tests/data`.

Keep generic YIDL goldens in `yidl`.

Move constructor performance fixtures into `yidl-lifecycle/tests/data/perf`.

Update `tests/data/goldens/readme.md` or copy an adapted version into
`yidl-lifecycle/tests/data/goldens/readme.md`.

Verification:

```bash
cd yidl-lifecycle
PYTHONPATH=../astichi/src uv run pytest tests/test_yidl_goldens.py -q
PYTHONPATH=../astichi/src uv run python -m yidl.testing.versioned_test_harness regen-goldens
PYTHONPATH=../astichi/src uv run pytest tests/test_yidl_goldens.py -q
```

If the generic harness cannot discover goldens outside the `yidl` repo root,
promote the needed path options into `yidl.testing.versioned_test_harness`
before this slice.

### Slice 5: Move Lifecycle Docs

Move lifecycle-specific docs into `yidl-lifecycle/dev-docs`.

Suggested moves:

- `YidlLifecycleFieldKindMatrix.md`
- `YidlPyrolyzeLifecycleParityPlan.md`
- `YidlPyroCloseTheGapPlan.md`
- `YidlTransactionalYidlPhase*.md`
- lifecycle-specific phase and parity notes

Keep core YIDL/lifecycle interface notes in `yidl` only if they describe a
generic YIDL capability, not lifecycle product behavior.

Verification:

- no committed absolute paths
- docs links point to the new repository-relative locations

### Slice 6: Add YIDL External Consumer Smoke Test

In `yidl`, replace full lifecycle tests with a small smoke test that depends on
the local `yidl-lifecycle` checkout:

- import `yidl_lifecycle.lifecycle`
- compile or use one minimal lifecycle class
- assert the generated class constructs and can stage/commit one managed field

Do not keep full lifecycle parity coverage in `yidl`; that belongs in
`yidl-lifecycle`.

Verification:

- `yidl` full tests pass
- `yidl-lifecycle` full tests pass

### Slice 7: Compatibility Cleanup Decision

After at least one downstream consumer has moved to `yidl_lifecycle.*` imports,
decide whether to:

- keep `yidl.runtime.lifecycle` shims indefinitely
- add deprecation warnings
- remove shims in a later major version

Do not make this decision in the initial extraction. The first extraction should
avoid unnecessary user-facing churn.

## Roll-Build Candidate Slices

This extraction is roll-buildable, but not as one huge commit. Suggested tag
prefix:

```text
lifecycle-extract/
```

Slices:

1. `lifecycle-extract/01-package-skeleton`
2. `lifecycle-extract/02-runtime-move`
3. `lifecycle-extract/03-yidl-sources`
4. `lifecycle-extract/04-goldens-perf`
5. `lifecycle-extract/05-docs`
6. `lifecycle-extract/06-yidl-smoke`
7. `lifecycle-extract/07-compat-policy`

Each slice should leave both repositories testable.

## Dependency And Packaging Notes

`yidl-lifecycle` should depend on released or editable `yidl`.

During local development:

```bash
cd yidl-lifecycle
uv pip install -e ../yidl
uv pip install -e .
```

For CI, prefer explicit editable installs for both projects until release
versioning is settled.

The generated lifecycle module should be checked in as a build artifact in
`yidl-lifecycle`, as it is today in `yidl`. Do not regenerate it at import time
for the normal package path.

## Open Decisions

1. Repository form: submodule under this workspace vs separate top-level
   checkout.
2. Compatibility window length for `yidl.runtime.*` shims.
3. Whether transaction and binding runtimes are permanently lifecycle-owned or
   should eventually become a small generic `yidl-runtime` package.
4. Whether the versioned golden harness needs a `--project-root` option before
   lifecycle goldens move.
5. Whether lifecycle docs should keep historical phase plans or collapse into a
   product-level design/reference after extraction.

## Non-Goals

- No semantic lifecycle changes during extraction.
- No Pyro parity changes during extraction.
- No lifecycle API rename beyond the package import path.
- No attempt to make `yidl-lifecycle` independently releasable in the first
  slice.
- No removal of compatibility shims during the first extraction.
