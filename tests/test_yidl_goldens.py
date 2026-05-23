from __future__ import annotations

import ast
from pathlib import Path
import shutil
import sys

import pytest

from yidl.testing.versioned_test_harness import (
    actual_results_dir,
    data_golden_dir,
    data_gold_src_dir,
    discover_golden_cases,
    materialized_output_name,
    run_golden_case,
)


_PROJECT_ROOT = Path(__file__).resolve().parents[1]
_GOLD_SRC_DIR = data_gold_src_dir(_PROJECT_ROOT)
_MATERIALIZED_GOLDENS_DIR = data_golden_dir(_PROJECT_ROOT)
_ACTUAL_GOLDENS_ROOT = actual_results_dir(
    _PROJECT_ROOT,
    runtime_version=(sys.version_info.major, sys.version_info.minor),
) / "goldens"

_CASES = discover_golden_cases(_PROJECT_ROOT)


def _materialized_name(case_name: str) -> str:
    return materialized_output_name(_GOLD_SRC_DIR / case_name)


def test_golden_fixture_sets_match() -> None:
    source_names = {path.name for path in _GOLD_SRC_DIR.glob("*.py")}
    expected_materialized_names = {_materialized_name(name) for name in source_names}
    materialized_names = {path.name for path in _MATERIALIZED_GOLDENS_DIR.iterdir()}

    assert source_names
    assert materialized_names == expected_materialized_names


@pytest.mark.parametrize("case_name", _CASES)
def test_fixture_outputs_match_goldens(case_name: str) -> None:
    materialized_name = _materialized_name(case_name)
    actual_materialized = _ACTUAL_GOLDENS_ROOT / "materialized" / materialized_name
    actual_materialized.parent.mkdir(parents=True, exist_ok=True)
    if actual_materialized.exists():
        if actual_materialized.is_dir():
            shutil.rmtree(actual_materialized)
        else:
            actual_materialized.unlink()

    completed = run_golden_case(
        _GOLD_SRC_DIR / case_name,
        actual_materialized,
        cwd=_PROJECT_ROOT,
        check=False,
    )
    assert completed.returncode == 0, (
        f"{case_name} failed with exit code {completed.returncode}\n"
        f"stdout:\n{completed.stdout}\n"
        f"stderr:\n{completed.stderr}"
    )
    assert actual_materialized.exists()

    expected_materialized = _MATERIALIZED_GOLDENS_DIR / materialized_name
    _assert_materialized_matches(actual_materialized, expected_materialized, case_name)


def _assert_materialized_matches(
    actual_path: Path,
    expected_path: Path,
    case_name: str,
) -> None:
    if expected_path.is_dir():
        assert actual_path.is_dir()
        actual_files = _relative_files(actual_path)
        expected_files = _relative_files(expected_path)
        assert actual_files == expected_files
        for relative_path in expected_files:
            _assert_source_file_matches(
                actual_path / relative_path,
                expected_path / relative_path,
                f"{case_name}/{relative_path.as_posix()}",
            )
        return

    assert actual_path.is_file()
    _assert_source_file_matches(actual_path, expected_path, case_name)


def _relative_files(root: Path) -> tuple[Path, ...]:
    return tuple(
        sorted(
            path.relative_to(root)
            for path in root.rglob("*")
            if path.is_file()
        )
    )


def _assert_source_file_matches(
    actual_path: Path,
    expected_path: Path,
    case_name: str,
) -> None:
    materialized_source = actual_path.read_text(encoding="utf-8")
    expected_materialized_source = expected_path.read_text(encoding="utf-8")

    ast.parse(materialized_source, filename=f"goldens/materialized/{case_name}")
    compile(materialized_source, f"goldens/materialized/{case_name}", "exec")
    assert materialized_source == expected_materialized_source
