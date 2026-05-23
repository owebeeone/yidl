from __future__ import annotations

from yidl_lifecycle.lifecycle import lifecycle
from yidl_lifecycle.lifecycle import managed
from yidl_lifecycle.transaction_yidl import DEFAULT_TRANSACTION


def test_yidl_lifecycle_external_consumer_smoke() -> None:
    class Counter:
        count: int = managed(default=1)

    generated = lifecycle(Counter)
    counter = generated()

    assert counter.count == 1
    with counter.begin(DEFAULT_TRANSACTION):
        counter.count = 2
        assert counter.current.count == 1
        assert counter.working.count == 2

    assert counter.count == 2
    assert counter.current.count == 2
