"""Concrete study scenarios."""

from __future__ import annotations

from study.contract import ScenarioResult, StudySubject


def scenario_default_tx_increment(subject: StudySubject) -> ScenarioResult:
    """One field written under a default transaction then committed."""

    cls = subject.build_class()
    txm = subject.build_transaction_manager()
    ctx = subject.make_instance(cls, txm)

    with txm.begin():
        ctx.value = 1

    value = int(ctx.value)
    return ScenarioResult(
        value=value,
        details={"value_after_commit": value},
    )
