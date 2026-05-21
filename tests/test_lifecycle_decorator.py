from __future__ import annotations

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
    assert child.v1 == 1
    assert child.v2 == 2
    assert child.v3 == 5


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
