"""PRE_IMPL study harness — minimal subject contract."""

from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import Callable
from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class ScenarioResult:
    value: Any
    details: dict[str, Any]


class StudySubject(ABC):
    """Minimal study contract for one implementation under test."""

    def __init__(self, *, name: str, lcm: Any | None = None) -> None:
        self.name = name
        self.lcm = lcm

    @abstractmethod
    def build_class(self) -> type:
        """Return the post-decoration or fully generated class under study."""

    def build_transaction_manager(self) -> Any:
        if self.lcm is None:
            raise NotImplementedError(
                "subject must provide build_transaction_manager() when no lifecycle module is attached",
            )
        return self.lcm.TransactionManager()

    def make_instance(self, cls: type, txm: Any) -> Any:
        return cls(transaction_manager=txm)


ScenarioFn = Callable[[StudySubject], ScenarioResult]
