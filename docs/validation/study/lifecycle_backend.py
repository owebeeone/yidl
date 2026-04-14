"""Lifecycle reference subject for the PRE_IMPL study harness."""

from __future__ import annotations

from study.contract import StudySubject
from study.lifecycle_access import load_lifecycle_module


class LifecycleCounterSubject(StudySubject):
    """Minimal ``@managed_context`` + ``TransactionManager`` path for study scenarios."""

    def __init__(self) -> None:
        super().__init__(name="lifecycle", lcm=load_lifecycle_module())

    def build_class(self) -> type:
        @self.lcm.managed_context
        class Counter:
            value: int = self.lcm.managed(default=0)

        return Counter
