"""PRE_IMPL empirical study harness (Phases 0c–0d)."""

from __future__ import annotations

from study.contract import ScenarioFn, ScenarioResult, StudySubject
from study.generated_strategy_a_backend import GeneratedStrategyACounterSubject
from study.lifecycle_backend import LifecycleCounterSubject
from study.runner import run_scenario
from study.scenarios import scenario_default_tx_increment

__all__ = [
    "GeneratedStrategyACounterSubject",
    "LifecycleCounterSubject",
    "ScenarioFn",
    "ScenarioResult",
    "StudySubject",
    "run_scenario",
    "scenario_default_tx_increment",
]
