from __future__ import annotations

from collections import UserList
from collections.abc import Iterable
from dataclasses import dataclass
from dataclasses import field


@dataclass(eq=False, slots=True)
class BindingBase:
    _ref_count: int = field(default=1, init=False, repr=False)
    _accepted: bool = field(default=False, init=False, repr=False)
    _closed: bool = field(default=False, init=False, repr=False)

    @property
    def is_accepted(self) -> bool:
        return self._accepted

    @property
    def is_closed(self) -> bool:
        return self._closed

    def accepted(self) -> None:
        if self._closed:
            raise RuntimeError("cannot accept a closed binding")
        self._accepted = True

    def inc_ref(self) -> None:
        if self._closed:
            raise RuntimeError("cannot retain a closed binding")
        self._ref_count += 1

    def dec_ref(self) -> None:
        if self._ref_count <= 0:
            raise AssertionError("dec_ref called without a matching ref")
        self._ref_count -= 1
        if self._ref_count == 0:
            self._closed = True
            self._close()

    def _close(self) -> None:
        pass


class BindingList(UserList):
    def __init__(self, initlist: Iterable[BindingBase] | None = None) -> None:
        super().__init__(list(initlist or ()))

    def clear(self) -> None:
        values = list(self.data)
        super().clear()
        for value in values:
            value.dec_ref()
