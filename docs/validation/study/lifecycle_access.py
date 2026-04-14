"""Load ``pyrolyze.lifecycle`` without importing ``pyrolyze.api`` (Py3.10-safe).

Layout: ``yidl`` repo root is ``parents[3]`` of this file; the monorepo parent
(containing sibling ``pyrolyze/``) is ``parents[4]``. Same layout as
``tests/baseline/_impl_switch.py`` but one level deeper, so the index differs.
"""

from __future__ import annotations

import importlib
import sys
import types
from pathlib import Path
from typing import Any


def _monorepo_parent() -> Path:
    return Path(__file__).resolve().parents[4]


def load_lifecycle_module() -> Any:
    root = _monorepo_parent() / "pyrolyze" / "src"
    pyrolyze_pkg = types.ModuleType("pyrolyze")
    pyrolyze_pkg.__path__ = [str(root / "pyrolyze")]
    sys.modules["pyrolyze"] = pyrolyze_pkg
    importlib.import_module("pyrolyze.type_annotations")
    return importlib.import_module("pyrolyze.lifecycle")


def lifecycle_importable() -> bool:
    try:
        load_lifecycle_module()
        return True
    except Exception:
        return False
