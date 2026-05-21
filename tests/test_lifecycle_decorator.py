from __future__ import annotations

import dataclasses
import os
from pathlib import Path
import runpy
from time import perf_counter

import pytest

from yidl.runtime.lifecycle import _generate_lifecycle_source
from yidl.runtime.lifecycle import LifecycleDefinitionError
from yidl.runtime.lifecycle import classvar
from yidl.runtime.lifecycle import field
from yidl.runtime.lifecycle import harvest_lifecycle_definition
from yidl.runtime.lifecycle import initvar
from yidl.runtime.lifecycle import lifecycle
from yidl.runtime.lifecycle import managed
from yidl.runtime.transaction_yidl import DEFAULT_TRANSACTION

_PERF_CONSTRUCTION_TIME_LIMIT = 5.0
_PERF_FIELD_GROUP_SIZES = (10, 50, 100)
_PERF_TOTAL_OBJECTS = 10_000
_PERF_BATCH_SIZE = 100
_LIFECYCLE_PERF_FIXTURE = (
    Path(__file__).parent / "data" / "perf" / "lifecycle_constructor_perf_generated.py"
)


def test_lifecycle_decorator_builds_phase_a_generated_class() -> None:
    class Counter:
        plain: int = field(default=3)
        seed: int = initvar(default=2)
        KIND: str = classvar(default="counter")
        count: int = managed(default=1)
        audit_count: int = managed("audit", default=10)

        def user_method(self) -> str:
            return "user"

    generated = lifecycle(Counter)

    assert generated is not Counter
    assert generated.__name__ == "Counter"
    assert generated.__qualname__ == Counter.__qualname__
    assert generated.__module__ == __name__
    assert generated.__yidl_lifecycle_generated__ is True
    assert generated.__yidl_lifecycle_user_class__ is Counter
    assert generated.__yidl_tx_index_to_group__ == (DEFAULT_TRANSACTION, "audit")
    assert generated.__yidl_tx_group_to_index__ == {
        DEFAULT_TRANSACTION: 0,
        "audit": 1,
    }

    counter = generated()
    assert isinstance(counter, Counter)
    assert counter.user_method() == "user"
    assert counter.default is counter
    assert counter.current is counter.current
    assert counter.working is counter.working

    assert generated.KIND == "counter"
    assert counter.KIND == "counter"
    assert counter.current.KIND == "counter"
    assert counter.working.KIND == "counter"

    assert counter.plain == 3
    assert counter.current.plain == 3
    counter.working.plain = 4
    assert counter.plain == 4
    assert counter.current.plain == 4

    assert counter.count == 1
    assert counter.current.count == 1
    assert counter.working.count == 1
    with pytest.raises(RuntimeError, match="writes require"):
        counter.count = 2
    with counter.begin(DEFAULT_TRANSACTION):
        counter.count = 11
        assert counter.count == 11
        assert counter.current.count == 1
        assert counter.working.count == 11
    assert counter.current.count == 11

    with counter.begin("audit"):
        counter.audit_count = 20
        assert counter.audit_count == 20
        assert counter.current.audit_count == 10
    assert counter.current.audit_count == 20


def test_lifecycle_source_uses_unpacked_builder_parameters() -> None:
    class Counter:
        plain: int = field(default=3)
        seed: int = initvar(default=2)
        KIND: str = classvar(default="counter")
        count: int = managed(default=1)

    source = _generate_lifecycle_source(harvest_lifecycle_definition(Counter))

    assert "_Counter_plain_default" in source
    assert "default_factories" not in source
    assert "defaults" not in source
    assert "\n        pass\n" not in source


def test_lifecycle_decorator_evaluates_parameterized_default_factories() -> None:
    class Example:
        SCALE: int = classvar(default=10)
        v1: int
        seed: int = initvar(init=False, default=4)
        temp: int = initvar(
            init=False,
            default_factory=lambda seed, v1: seed + v1,
        )
        v2: int = managed(default_factory=lambda v1: v1 + 2)
        v3: int = managed(default_factory=lambda v2, v1: v1 + v2 + 2)
        v4: int = managed(init=False, default_factory=lambda v3: v3 * 2)
        v5: int = managed(
            init=False,
            default_factory=lambda SCALE, v4: SCALE + v4,
        )

    generated = lifecycle(Example)
    item = generated(v1=1)

    assert item.v1 == 1
    assert item.v2 == 3
    assert item.v3 == 6
    assert item.v4 == 12
    assert item.v5 == 22
    assert not hasattr(item._y_state, "_y_seed_value")
    assert not hasattr(item._y_state, "_y_temp_value")

    explicit = generated(v1=1, v2=20, v3=30)
    assert explicit.v2 == 20
    assert explicit.v3 == 30
    assert explicit.v4 == 60
    assert explicit.v5 == 70


def test_lifecycle_source_uses_direct_default_factory_calls() -> None:
    class Example:
        SCALE: int = classvar(default=10)
        v1: int
        v2: int = managed(default_factory=lambda v1: v1 + 2)
        v3: int = managed(default_factory=lambda v2, v1: v1 + v2 + 2)
        v4: int = managed(init=False, default_factory=lambda v3: v3 * 2)
        v5: int = managed(
            init=False,
            default_factory=lambda SCALE, v4: SCALE + v4,
        )

    source = _generate_lifecycle_source(harvest_lifecycle_definition(Example))

    assert "locals()" not in source
    assert "_Example_v2_default_factory(v1=self.v1)" in source
    assert "_Example_v3_default_factory(v2=self.v2, v1=self.v1)" in source
    assert "_Example_v4_default_factory(v3=self.v3)" in source
    assert "_Example_v5_default_factory(SCALE=self.SCALE, v4=self.v4)" in source


def test_lifecycle_decorator_rejects_unknown_default_factory_provider() -> None:
    class Example:
        v1: int = managed(default_factory=lambda missing: missing)

    with pytest.raises(
        LifecycleDefinitionError,
        match=r"Example\.v1: default_factory references unknown name 'missing'",
    ):
        lifecycle(Example)


def test_lifecycle_decorator_rejects_default_factory_dependency_cycle() -> None:
    class Example:
        v1: int = managed(default_factory=lambda v2: v2)
        v2: int = managed(default_factory=lambda v1: v1)

    with pytest.raises(
        LifecycleDefinitionError,
        match="Example: default_factory dependency cycle: v1 -> v2 -> v1",
    ):
        lifecycle(Example)


def test_lifecycle_decorator_merges_generated_base_facts() -> None:
    @lifecycle
    class A:
        plain: int = field(default=1)
        seed: int = initvar(default=2)
        KIND: str = classvar(default="A")
        v1: int = managed(default=1)

    @lifecycle
    class B(A):
        plain: int = managed(default=3)
        seed: int = initvar(default=4)
        KIND: str = classvar(default="B")
        v2: int = managed(default=2)

    item = B()

    assert isinstance(item, A)
    assert B.KIND == "B"
    assert item.current.KIND == "B"
    assert item.plain == 3
    assert item.v1 == 1
    assert item.v2 == 2

    with pytest.raises(RuntimeError, match="writes require"):
        item.plain = 4

    with item.begin(DEFAULT_TRANSACTION):
        item.plain = 4
        item.v1 = 11
        item.v2 = 22
        assert item.current.plain == 3
        assert item.working.plain == 4
    assert item.current.plain == 4
    assert item.current.v1 == 11
    assert item.current.v2 == 22

    @lifecycle
    class C(B):
        v3: int = managed(default=5)

    child = C()
    assert isinstance(child, A)
    assert isinstance(child, B)
    assert child.v1 == 1
    assert child.v2 == 2
    assert child.v3 == 5


@pytest.mark.skipif(
    os.environ.get("YIDL_PERF_TESTS") != "1",
    reason="set YIDL_PERF_TESTS=1 to run constructor throughput comparison",
)
def test_lifecycle_generated_class_constructor_throughput_comparison() -> None:
    deadline = perf_counter() + _PERF_CONSTRUCTION_TIME_LIMIT
    lifecycle_classes = _load_lifecycle_perf_classes()
    completed_sizes = 0

    for field_group_size in _PERF_FIELD_GROUP_SIZES:
        if perf_counter() >= deadline:
            break

        lifecycle_type = lifecycle_classes[field_group_size]
        dataclass_type = _make_dataclass_perf_class(field_group_size)

        lifecycle_sample = lifecycle_type()
        dataclass_sample = dataclass_type()
        assert getattr(lifecycle_sample, "derived_0") == (
            getattr(lifecycle_sample, "count_0") + 1
        )
        assert getattr(dataclass_sample, "derived_0") == (
            getattr(dataclass_sample, "count_0") + 1
        )
        assert getattr(lifecycle_sample, f"derived_{field_group_size - 1}") == (
            getattr(lifecycle_sample, f"count_{field_group_size - 1}") + 1
        )
        assert getattr(dataclass_sample, f"derived_{field_group_size - 1}") == (
            getattr(dataclass_sample, f"count_{field_group_size - 1}") + 1
        )

        lifecycle_result = _measure_constructor_throughput(
            lifecycle_type,
            deadline=deadline,
        )
        dataclass_result = _measure_constructor_throughput(
            dataclass_type,
            deadline=deadline,
        )
        print(
            "constructor throughput comparison: "
            f"{field_group_size} plain + {field_group_size} count + "
            f"{field_group_size} derived fields; "
            f"lifecycle {lifecycle_result[0]} in {lifecycle_result[1]:.6f}s "
            f"({lifecycle_result[2]:,.0f}/s); "
            f"dataclass {dataclass_result[0]} in {dataclass_result[1]:.6f}s "
            f"({dataclass_result[2]:,.0f}/s)"
        )
        completed_sizes += 1

    assert completed_sizes > 0


def _load_lifecycle_perf_classes() -> dict[int, type[object]]:
    namespace = runpy.run_path(_LIFECYCLE_PERF_FIXTURE)
    return namespace["LIFECYCLE_PERF_CLASSES"]


def _make_dataclass_perf_class(field_group_size: int) -> type[object]:
    def __post_init__(self: object) -> None:
        for index in range(field_group_size):
            setattr(
                self,
                f"derived_{index}",
                getattr(self, f"count_{index}") + 1,
            )

    fields: list[tuple[str, type[object], object]] = []
    for index in range(field_group_size):
        fields.append((f"plain_{index}", int, dataclasses.field(default=index)))
    for index in range(field_group_size):
        fields.append((f"count_{index}", int, dataclasses.field(default=index)))
    for index in range(field_group_size):
        fields.append((f"derived_{index}", int, dataclasses.field(init=False)))
    return dataclasses.make_dataclass(
        f"PerfDataclass{field_group_size}",
        fields,
        namespace={"__post_init__": __post_init__, "__module__": __name__},
        slots=True,
    )


def _measure_constructor_throughput(
    cls: type[object],
    *,
    deadline: float,
) -> tuple[int, float, float]:
    total_created = 0
    live_batch: list[object] = []

    # Keep the last batch alive while constructing the next one, then drop it.
    # This keeps roughly 100-200 generated objects live during the timed loop.
    start = perf_counter()
    while total_created < _PERF_TOTAL_OBJECTS and perf_counter() < deadline:
        next_count = min(_PERF_BATCH_SIZE, _PERF_TOTAL_OBJECTS - total_created)
        next_batch = [cls() for _ in range(next_count)]
        total_created += len(next_batch)
        live_batch = next_batch
    live_batch = []
    elapsed = perf_counter() - start
    objects_per_second = total_created / elapsed if elapsed else float("inf")
    return total_created, elapsed, objects_per_second


def test_lifecycle_wraps_generation_failure_with_class_context(monkeypatch) -> None:
    class Counter:
        value: int = field(default=1)

    def fail_generate(_harvested: object) -> str:
        raise ValueError("boom")

    monkeypatch.setattr(
        "yidl.runtime.lifecycle._generate_lifecycle_source", fail_generate
    )

    with pytest.raises(
        LifecycleDefinitionError,
        match="Counter: lifecycle source generation failed: boom",
    ):
        lifecycle(Counter)


def test_lifecycle_wraps_exec_failure_with_class_context(monkeypatch) -> None:
    class Counter:
        value: int = field(default=1)

    monkeypatch.setattr(
        "yidl.runtime.lifecycle._generate_lifecycle_source",
        lambda _harvested: "not valid python",
    )

    with pytest.raises(
        LifecycleDefinitionError,
        match="Counter: lifecycle source execution failed:",
    ):
        lifecycle(Counter)


def test_lifecycle_wraps_build_failure_with_class_context(monkeypatch) -> None:
    class Counter:
        value: int = field(default=1)

    monkeypatch.setattr(
        "yidl.runtime.lifecycle._generate_lifecycle_source",
        lambda _harvested: (
            "def build_lifecycle_class(decorated_cls, **kwargs):\n"
            "    raise RuntimeError('boom')\n"
        ),
    )

    with pytest.raises(
        LifecycleDefinitionError,
        match="Counter: lifecycle class build failed: boom",
    ):
        lifecycle(Counter)
