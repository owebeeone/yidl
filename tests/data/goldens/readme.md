# YIDL Golden Tests

This directory contains checked-in golden outputs for executable fixtures in
`tests/data/gold_src`.

- `tests/data/gold_src/*.py` contains the source fixture for each golden case.
- `tests/data/goldens/materialized/*` contains the checked-in expected output.
- `tests/actual_test_results/pyX_Y/goldens/materialized/*` contains actual
  output from test runs and is useful for diffs when a test fails.

Run commands from the repository root. In this checkout, include Astichi on
`PYTHONPATH`:

```bash
PYTHONPATH=../astichi/src uv run ...
```

## Add A Golden Case

1. Add a fixture script under `tests/data/gold_src/<case_name>.py`.
2. Use `support.golden_case.run_case(...)` for a single generated source file,
   or `support.golden_case.run_multi_source_case(...)` for a generated output
   directory.
3. Keep the fixture deterministic. Put runtime assertions in the fixture's
   `validate_case` function when the golden should prove executable behavior,
   not only source shape.
4. If the fixture needs YIDL input files, put them under `tests/data/yidl`.
5. Regenerate the golden output and run the golden tests.

The harness discovers cases by filename in `tests/data/gold_src`. For a
single-source fixture, the materialized output is:

```text
tests/data/goldens/materialized/<case_name>.py
```

For a multi-source fixture using `run_multi_source_case(...)`, the materialized
output is a directory named without the `.py` suffix:

```text
tests/data/goldens/materialized/<case_name>/
```

## Run Golden Tests

Run all golden cases in the current environment:

```bash
PYTHONPATH=../astichi/src uv run pytest tests/test_yidl_goldens.py -q
```

Run one golden case by name:

```bash
PYTHONPATH=../astichi/src uv run pytest tests/test_yidl_goldens.py -q -k yidl_transactional_phase_h_owned
```

Run the full test suite in the current environment:

```bash
PYTHONPATH=../astichi/src uv run pytest -q
```

Run tests through the versioned harness for one Python version:

```bash
PYTHONPATH=../astichi/src uv run python -m yidl.testing.versioned_test_harness run-tests --python 3.13 --pytest-args tests/test_yidl_goldens.py -q
```

Run tests for every configured Python version:

```bash
PYTHONPATH=../astichi/src uv run python -m yidl.testing.versioned_test_harness run-tests-all --pytest-args tests/test_yidl_goldens.py -q
```

The configured version matrix lives in `pyproject.toml` under
`tool.yidl.test-matrix`.

## Regenerate Goldens

Regenerate all checked-in golden outputs:

```bash
PYTHONPATH=../astichi/src uv run python -m yidl.testing.versioned_test_harness regen-goldens
```

Regenerate all goldens with a specific Python version:

```bash
PYTHONPATH=../astichi/src uv run python -m yidl.testing.versioned_test_harness regen-goldens --python 3.13
```

Regenerate one single-source golden:

```bash
PYTHONPATH=../astichi/src uv run python tests/data/gold_src/yidl_transactional_phase_h_owned.py tests/data/goldens/materialized/yidl_transactional_phase_h_owned.py
```

Regenerate a single multi-source golden:

```bash
PYTHONPATH=../astichi/src uv run python tests/data/gold_src/yidl_update_a_dataclasses_split.py tests/data/goldens/materialized/yidl_update_a_dataclasses_split
```

Prefer full `regen-goldens` before committing broad compiler or runtime
changes. Single-case regeneration is useful while iterating, but it does not
remove stale outputs for deleted or renamed fixtures.

## Review Output

When a golden test fails, compare the checked-in expected output with the
actual output under `tests/actual_test_results`:

```bash
diff -ru tests/data/goldens/materialized tests/actual_test_results/py3_13/goldens/materialized
```

Use the Python version directory that matches the failing run.
