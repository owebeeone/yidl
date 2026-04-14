"""Smoke for the PRE_IMPL study harness."""

from __future__ import annotations

import pytest

from study.generated_strategy_a_backend import GeneratedStrategyACounterSubject
from study.lifecycle_backend import LifecycleCounterSubject
from study.runner import run_scenario
from study.scenarios import scenario_default_tx_increment


@pytest.mark.usefixtures("require_lifecycle_importable")
def test_default_tx_increment_lifecycle():
    out = run_scenario(LifecycleCounterSubject(), scenario_default_tx_increment)
    assert out.details == {"value_after_commit": 1}


def test_default_tx_increment_generated_strategy_a():
    out = run_scenario(GeneratedStrategyACounterSubject(), scenario_default_tx_increment)
    assert out.details == {"value_after_commit": 1}
