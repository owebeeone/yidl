"""Select lifecycle, handcrafted, or generated implementation for parity tests."""

from __future__ import annotations

import importlib
import os
import sys
import types
from pathlib import Path
from typing import Any, Literal

Backend = Literal["lifecycle", "handcrafted", "generated"]

_ENV_VAR = "LC_PARITY_IMPL"
_DEFAULT: Backend = "lifecycle"


def _pyrolyze_src_root() -> Path:
    # yidl/tests/baseline -> yidl -> grip-pyrolyze-dev (parent of pyrolyze + yidl)
    return Path(__file__).resolve().parents[3]


def _load_lifecycle_module() -> Any:
    """Load ``pyrolyze.lifecycle`` without importing ``pyrolyze.api`` (Py3.10-safe)."""
    root = _pyrolyze_src_root() / "pyrolyze" / "src"
    pyrolyze_pkg = types.ModuleType("pyrolyze")
    pyrolyze_pkg.__path__ = [str(root / "pyrolyze")]
    sys.modules["pyrolyze"] = pyrolyze_pkg
    importlib.import_module("pyrolyze.type_annotations")
    return importlib.import_module("pyrolyze.lifecycle")


def get_backend() -> Backend:
    v = os.environ.get(_ENV_VAR, _DEFAULT).strip().lower()
    if v in ("lifecycle", "lc", "pyrolyze"):
        return "lifecycle"
    if v in ("handcrafted", "hand"):
        return "handcrafted"
    if v in ("generated", "gen"):
        return "generated"
    raise ValueError(
        f"{_ENV_VAR} must be 'lifecycle', 'handcrafted', or 'generated', not {v!r}",
    )


def lifecycle_importable() -> bool:
    try:
        _load_lifecycle_module()
        return True
    except Exception:
        return False


def get_lifecycle_module() -> Any:
    """Return loaded ``pyrolyze.lifecycle`` (raises if unavailable)."""
    return _load_lifecycle_module()
