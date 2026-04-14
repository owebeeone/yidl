"""Pytest fixtures for PRE_IMPL study harness tests."""

from __future__ import annotations

import pytest

from study.lifecycle_access import lifecycle_importable


@pytest.fixture
def require_lifecycle_importable():
    if not lifecycle_importable():
        pytest.skip(
            "pyrolyze.lifecycle cannot be loaded (need monorepo sibling pyrolyze/src); "
            "see study/lifecycle_access.py",
        )
