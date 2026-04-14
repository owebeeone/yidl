"""Run scenarios against study subjects."""

from __future__ import annotations

from study.contract import ScenarioFn, ScenarioResult, StudySubject


def run_scenario(subject: StudySubject, scenario: ScenarioFn) -> ScenarioResult:
    return scenario(subject)
