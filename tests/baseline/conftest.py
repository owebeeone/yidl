"""Baseline parity fixtures."""

from __future__ import annotations

import pytest

from tests.baseline._impl_switch import get_backend, lifecycle_importable


@pytest.fixture
def lc_parity_backend():
    return get_backend()


@pytest.fixture
def require_lifecycle_importable():
    if not lifecycle_importable():
        pytest.skip(
            "pyrolyze.lifecycle cannot be loaded (need pyrolyze/src on path and "
            "compatible deps); see tests/baseline/_impl_switch.py",
        )
