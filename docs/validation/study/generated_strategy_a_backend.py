"""Hand-crafted generated strategy A subject for PRE_IMPL study work."""

from __future__ import annotations

from typing import Any

from study.contract import StudySubject


class _GeneratedTransaction:
    def __enter__(self) -> "_GeneratedTransaction":
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc: BaseException | None,
        tb: Any,
    ) -> bool:
        del exc_type, exc, tb
        return False


class _GeneratedTransactionManager:
    def begin(self) -> _GeneratedTransaction:
        return _GeneratedTransaction()


class GeneratedStrategyACounterSubject(StudySubject):
    def __init__(self) -> None:
        super().__init__(name="generated_strategy_a")

    def build_class(self) -> type:
        # THIS IS ONLY A PLACEHOLDER FOR THE ACTUAL IMPLEMENTATION.
        # DO NOT CONSIDER THIS AS AN EXAMPLE OF HOW TO IMPLEMENT THIS
        # GENERATED STRATEGY.
        class Counter:
            __slots__ = ("transaction_manager", "_value")

            def __init__(self, *, transaction_manager: Any) -> None:
                self.transaction_manager = transaction_manager
                self._value = 0

            @property
            def value(self) -> int:
                return self._value

            @value.setter
            def value(self, value: int) -> None:
                self._value = value

        return Counter

    def build_transaction_manager(self) -> Any:
        return _GeneratedTransactionManager()
