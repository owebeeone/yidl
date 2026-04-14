# PRE_IMPL study harness contract (Phase 0c)

## Purpose

One **scenario** API drives every **study subject** (reference lifecycle vs
generated strategies) so behavioral checks and future perf runs stay
comparable.

## Layout

- **`contract.py`** — `StudySubject` ABC plus shared scenario result types.
- **`lifecycle_access.py`** — load `pyrolyze.lifecycle` without `pyrolyze.api`
  (monorepo: sibling `pyrolyze/src`).
- **`lifecycle_backend.py`** — lifecycle reference subject.
- **`generated_strategy_a_backend.py`** — first generated strategy subject.
- **`scenarios.py`** — concrete scenario functions.
- **`runner.py`** — `run_scenario(subject, scenario)`.

## Rules

- Scenarios must not embed implementation-specific types; they operate only on
  the shared `StudySubject` surface.
- Subjects own how classes and runtime pieces are built.
- Executable matrix: `docs/validation/perf/version_matrix.py` (`VERSION_MATRIX`).
- Do not edit `pyrolyze/` from this tree.

## Running smoke tests

From the **yidl** repo root (with **yidl** and sibling **pyrolyze** checkout as
used by `tests/baseline/_impl_switch.py`):

```bash
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 uv run --with pytest pytest docs/validation/study -q
```

Use `PYTEST_DISABLE_PLUGIN_AUTOLOAD=1` when a globally installed pytest plugin
(e.g. pyrolyze) breaks collection before tests run.

Lifecycle-backed tests skip if `pyrolyze` cannot be loaded (layout / deps).
