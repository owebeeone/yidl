from __future__ import annotations

import dataclasses
import os
from pathlib import Path
import runpy
from time import perf_counter
import weakref

import pytest

from yidl.runtime.bindings import BindingBase
from yidl.runtime.bindings import BindingDict
from yidl.runtime.lifecycle import _generate_lifecycle_source
from yidl.runtime.lifecycle import LifecycleDefinitionError
from yidl.runtime.lifecycle import after_commit
from yidl.runtime.lifecycle import after_rollback
from yidl.runtime.lifecycle import before_commit
from yidl.runtime.lifecycle import binding
from yidl.runtime.lifecycle import commit_order_key
from yidl.runtime.lifecycle import classvar
from yidl.runtime.lifecycle import field
from yidl.runtime.lifecycle import const
from yidl.runtime.lifecycle import harvest_lifecycle_definition
from yidl.runtime.lifecycle import initvar
from yidl.runtime.lifecycle import lifecycle
from yidl.runtime.lifecycle import local_store
from yidl.runtime.lifecycle import managed
from yidl.runtime.lifecycle import owned
from yidl.runtime.lifecycle import static
from yidl.runtime.lifecycle import transient
from yidl.runtime.lifecycle import validate_commit
from yidl.runtime.transaction_yidl import DEFAULT_TRANSACTION

_PERF_CONSTRUCTION_TIME_LIMIT = 5.0
_PERF_FIELD_GROUP_SIZES = (5, 10, 15)
_PERF_TOTAL_OBJECTS = 10_000
_PERF_BATCH_SIZE = 100
_LIFECYCLE_PERF_FIXTURE = (
    Path(__file__).parent / "data" / "perf" / "lifecycle_constructor_perf_generated.py"
)


class _TestBinding(BindingBase):
    pass


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
    assert generated.__yidl_tx_index_to_key__ == (DEFAULT_TRANSACTION, "audit")
    assert generated.__yidl_tx_key_to_index__ == {
        DEFAULT_TRANSACTION: 0,
        "audit": 1,
    }

    counter = generated()
    assert isinstance(counter, Counter)
    assert counter.user_method() == "user"
    assert counter.default is counter
    assert counter.current is counter.current
    assert counter.working is counter.working
    assert counter._y_current_facade is counter.current
    assert counter._y_working_facade is counter.working

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


def test_lifecycle_decorator_facades_are_weakrefable_with_slotted_user_class() -> None:
    class Counter:
        __slots__ = ()

        count: int = managed(default=1)

    generated = lifecycle(Counter)
    counter = generated()
    current = counter.current
    working = counter.working

    assert weakref.ref(counter)() is counter
    assert weakref.ref(current)() is current
    assert weakref.ref(working)() is working


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
        owner: str = const(default="owner")
        owner_tag: str = const(
            default_factory=lambda self: self.owner + "-tag",
            allow_self_factory=True,
        )
        seed: int = initvar(init=False, default=4)
        class_name_size: int = initvar(
            init=False,
            default_factory=lambda cls: len(cls.__name__),
        )
        self_tag_size: int = initvar(
            init=False,
            default_factory=lambda self: len(self.owner),
            allow_self_factory=True,
        )
        temp: int = initvar(
            init=False,
            default_factory=lambda seed, v1: seed + v1,
        )
        v2: int = managed(default_factory=lambda v1: v1 + 2)
        v3: int = managed(default_factory=lambda v2, v1: v1 + v2 + 2)
        v4: int = managed(init=False, default_factory=lambda v3: v3 * 2)
        v5: int = managed(
            init=False,
            default_factory=lambda class_name_size, self_tag_size, SCALE, v4: (
                class_name_size + self_tag_size + SCALE + v4
            ),
        )

    generated = lifecycle(Example)
    item = generated(v1=1)

    assert item.owner == "owner"
    assert item.owner_tag == "owner-tag"
    assert item.v1 == 1
    assert item.v2 == 3
    assert item.v3 == 6
    assert item.v4 == 12
    assert item.v5 == 34
    assert not hasattr(item._y_state, "_y_seed_value")
    assert not hasattr(item._y_state, "_y_class_name_size_value")
    assert not hasattr(item._y_state, "_y_self_tag_size_value")
    assert not hasattr(item._y_state, "_y_temp_value")

    explicit = generated(v1=1, v2=20, v3=30)
    assert explicit.v2 == 20
    assert explicit.v3 == 30
    assert explicit.v4 == 60
    assert explicit.v5 == 82


def test_lifecycle_decorator_initializes_transient_current_defaults() -> None:
    class Scratch:
        seed: int = initvar(default=3)
        label: str = transient(default="ready")
        items: list[int] = transient(default_factory=lambda seed: [seed])

    generated = lifecycle(Scratch)
    item = generated()

    assert item.current.label == "ready"
    assert item.current.items == [3]
    with pytest.raises(AttributeError):
        item.current.label = "changed"


def test_lifecycle_decorator_transient_working_overlay_materializes_in_transaction() -> (
    None
):
    class Scratch:
        seed: int = initvar(init=False, default=4)
        label: str = transient(default="ready")
        marker: str = transient(default="base")
        buffer: list[int] | None = transient(
            default=None,
            working_default_factory=lambda self, current, working, seed: [
                seed,
                self.label,
                current.label,
                working.label,
            ],
        )
        audit_buffer: list[int] | None = transient(
            "audit",
            default=None,
            working_default_factory=list,
        )

    generated = lifecycle(Scratch)
    item = generated()

    assert item._y_state._y_seed_initvar == 4
    assert item.label == "ready"
    assert item.marker == "base"
    assert item.buffer is None
    assert item.current.buffer is None
    with pytest.raises(RuntimeError, match="writes require"):
        item.buffer = [9]

    assert item._y_state._y_working_tx_ids[0] is None
    with item.begin(DEFAULT_TRANSACTION):
        assert item._y_state._y_working_tx_ids[0] is None
        assert item.marker == "base"
        assert item._y_state._y_marker_working == "base"
        assert item._y_state._y_working_tx_ids[0] is not None
        assert item.current.marker == "base"
    assert item._y_state._y_working_tx_ids[0] is None

    with item.begin(DEFAULT_TRANSACTION):
        assert item.current.buffer is None
        assert item.buffer == [4, "ready", "ready", "ready"]
        item.buffer.append(1)
        assert item.buffer == [4, "ready", "ready", "ready", 1]
        assert item.working.buffer == [4, "ready", "ready", "ready", 1]
        assert item.current.buffer is None

    assert item.buffer is None
    assert item.current.buffer is None

    with pytest.raises(RuntimeError, match="abort"):
        with item.begin(DEFAULT_TRANSACTION):
            item.buffer = [2]
            raise RuntimeError("abort")

    assert item.buffer is None
    assert item.current.buffer is None

    with item.begin("audit"):
        assert item.buffer is None
        assert item.audit_buffer == []
        item.audit_buffer.append(3)
        assert item.current.audit_buffer is None

    assert item.audit_buffer is None
    assert item.current.audit_buffer is None


def test_lifecycle_decorator_local_store_is_shared_non_transactional() -> None:
    class Scratch:
        cache: dict[str, int] = local_store(default_factory=dict)
        count: int = managed(default=1)

    generated = lifecycle(Scratch)
    item = generated()

    assert item.cache is item.current.cache
    assert item.cache is item.working.cache
    item.cache["a"] = 1
    assert item.current.cache == {"a": 1}
    assert item._y_state._y_working_tx_ids[0] is None

    with item.begin(DEFAULT_TRANSACTION):
        item.cache["b"] = 2
        assert item._y_state._y_working_tx_ids[0] is None
        item.count = 5

    assert item.cache == {"a": 1, "b": 2}
    assert item.count == 5

    with pytest.raises(RuntimeError):
        with item.begin(DEFAULT_TRANSACTION):
            item.cache["c"] = 3
            item.count = 7
            raise RuntimeError("rollback")

    assert item.cache == {"a": 1, "b": 2, "c": 3}
    assert item.count == 5


def test_lifecycle_decorator_const_fields_are_read_only_everywhere() -> None:
    class Config:
        seed: int = initvar(default=3)
        slot_id: int = const(default=7)
        derived_id: int = const(default_factory=lambda seed, slot_id: seed + slot_id)

    item = lifecycle(Config)()

    assert item.slot_id == 7
    assert item.current.slot_id == 7
    assert item.working.slot_id == 7
    assert item.derived_id == 10
    assert item.current.derived_id == 10
    assert item.working.derived_id == 10

    with pytest.raises(AttributeError, match="const field 'slot_id' is read-only"):
        item.slot_id = 8
    with pytest.raises(AttributeError, match="const field 'slot_id' is read-only"):
        item.current.slot_id = 8
    with pytest.raises(AttributeError, match="const field 'slot_id' is read-only"):
        item.working.slot_id = 8


def test_lifecycle_decorator_static_fields_are_lazy_and_write_once() -> None:
    factory_calls: list[None] = []

    def make_items() -> list[int]:
        factory_calls.append(None)
        return [1, 2]

    class Config:
        declared: tuple[str, ...] = static()
        n: int = static(default=42)
        items: list[int] = static(default_factory=make_items)

    generated = lifecycle(Config)
    item = generated()

    with pytest.raises(
        AttributeError, match="static field 'declared' is not initialized"
    ):
        _ = item.declared

    item.declared = ("a", "b")
    assert item.declared == ("a", "b")
    assert item.current.declared == ("a", "b")
    assert item.working.declared == ("a", "b")
    with pytest.raises(
        AttributeError, match="static field 'declared' is already initialized"
    ):
        item.declared = ("x",)

    override = generated(n=7)
    assert override.n == 7
    with pytest.raises(AttributeError, match="static field 'n' is already initialized"):
        override.n = 8

    assign_first = generated()
    assign_first.n = 9
    assert assign_first.n == 9
    with pytest.raises(AttributeError, match="static field 'n' is already initialized"):
        assign_first.n = 10

    read_default = generated()
    assert read_default.n == 42
    with pytest.raises(AttributeError, match="static field 'n' is already initialized"):
        read_default.n = 43

    assert factory_calls == []
    assert item.items == [1, 2]
    assert factory_calls == [None]
    assert item.items is item.items
    with pytest.raises(
        AttributeError, match="static field 'items' is already initialized"
    ):
        item.items = []


def test_lifecycle_decorator_binding_fields_are_stored_and_validated() -> None:
    initial = _TestBinding()

    class Holder:
        handle: object = binding(default=initial)
        derived: object = binding(default_factory=lambda handle: _TestBinding())

    generated = lifecycle(Holder)
    item = generated()

    assert item.handle is initial
    assert isinstance(item.derived, _TestBinding)

    replacement = _TestBinding()
    item.handle = replacement
    assert item.handle is replacement
    assert item.current.handle is replacement
    assert item.working.handle is replacement

    with pytest.raises(TypeError, match="binding field 'handle' expects"):
        item.handle = object()
    assert item.handle is replacement

    with pytest.raises(TypeError, match="binding field 'handle' expects"):
        generated(handle=object())


def test_lifecycle_decorator_binding_map_fields_normalize_and_validate() -> None:
    class Holder:
        handles: dict[str, BindingBase] = binding(default_factory=lambda: {})

    item = lifecycle(Holder)()
    first = _TestBinding()

    assert isinstance(item.handles, BindingDict)
    item.handles = {"first": first}
    assert isinstance(item.handles, BindingDict)
    assert item.handles["first"] is first

    with pytest.raises(TypeError, match="binding map field 'handles' expects"):
        item.handles = object()
    with pytest.raises(TypeError, match="expects BindingBase values"):
        item.handles = {"bad": object()}


def test_lifecycle_decorator_rejects_invalid_binding_default_factory_result() -> None:
    class Holder:
        handle: object = binding(default_factory=object)

    generated = lifecycle(Holder)

    with pytest.raises(TypeError, match="binding field 'handle' expects"):
        generated()


def test_lifecycle_decorator_owned_scalar_commits_and_rolls_back() -> None:
    class Owner:
        child: object = owned(default=None)

    generated = lifecycle(Owner)
    item = generated()
    child = _TestBinding()

    assert item.child is None
    with pytest.raises(RuntimeError, match="writes require"):
        item.child = child
    with pytest.raises(AttributeError, match="current facade is read-only"):
        item.current.child = child

    with item.begin(DEFAULT_TRANSACTION):
        item.child = child
        assert item.child is child
        assert item.current.child is None
        assert child.is_accepted is False

    assert item.child is child
    assert item.current.child is child
    assert item.working.child is child
    assert child.is_accepted is True

    replacement = _TestBinding()
    with pytest.raises(RuntimeError, match="abort owned"):
        with item.begin(DEFAULT_TRANSACTION):
            item.child = replacement
            assert item.child is replacement
            assert item.current.child is child
            raise RuntimeError("abort owned")

    assert item.child is child
    assert item.current.child is child
    assert item.working.child is child
    assert replacement.is_accepted is False

    with item.begin(DEFAULT_TRANSACTION):
        item.child = None
        assert item.child is None
        assert item.current.child is child

    assert item.child is None
    assert item.current.child is None


def test_lifecycle_decorator_owned_scalar_rejects_invalid_values() -> None:
    class Owner:
        child: object = owned(default=None)

    item = lifecycle(Owner)()

    with item.begin(DEFAULT_TRANSACTION):
        with pytest.raises(TypeError, match="binding field 'child' expects"):
            item.child = object()


def test_lifecycle_decorator_owned_map_commits_and_rolls_back() -> None:
    class Owner:
        children: dict[str, BindingBase] = owned(default_factory=lambda: {})

    item = lifecycle(Owner)()
    first = _TestBinding()

    assert isinstance(item.children, BindingDict)
    with item.begin(DEFAULT_TRANSACTION):
        item.children = {"first": first}
        assert item.children["first"] is first
        assert item.current.children == {}
        assert first.is_accepted is False

    assert item.children["first"] is first
    assert item.current.children["first"] is first
    assert first.is_accepted is True

    replacement = _TestBinding()
    with pytest.raises(RuntimeError, match="abort owned map"):
        with item.begin(DEFAULT_TRANSACTION):
            item.children = {"replacement": replacement}
            assert "replacement" in item.children
            assert "replacement" not in item.current.children
            raise RuntimeError("abort owned map")

    assert "replacement" not in item.children
    assert item.children["first"] is first
    assert replacement.is_accepted is False

    with item.begin(DEFAULT_TRANSACTION):
        with pytest.raises(TypeError, match="expects BindingBase values"):
            item.children = {"bad": object()}


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


def test_lifecycle_decorator_rejects_facade_exposure_field_collision() -> None:
    class Counter:
        default: int = field(default=1)

    with pytest.raises(
        LifecycleDefinitionError,
        match="Counter.default: field name collides with generated facade exposure",
    ):
        lifecycle(Counter)


def test_lifecycle_decorator_rejects_generated_helper_collision() -> None:
    class Counter:
        begin: int = managed(default=1)

    with pytest.raises(
        LifecycleDefinitionError,
        match="Counter.begin: name collides with generated lifecycle helper",
    ):
        lifecycle(Counter)


def test_lifecycle_decorator_rejects_generated_facade_class_collision() -> None:
    class Counter:
        Counter_State = object()
        value: int = field(default=1)

    with pytest.raises(
        LifecycleDefinitionError,
        match="Counter.Counter_State: name collides with generated lifecycle class",
    ):
        lifecycle(Counter)


def test_lifecycle_facade_allows_unrelated_user_attributes() -> None:
    class Counter:
        value: int = field(default=1)

    item = lifecycle(Counter)()

    item.note = "kept"

    assert item.note == "kept"
    assert item.value == 1


def test_lifecycle_facade_rejects_reserved_generated_attributes() -> None:
    class Counter:
        value: int = field(default=1)

    item = lifecycle(Counter)()

    with pytest.raises(AttributeError, match="reserved for generated lifecycle state"):
        item._y_shadow = 1
    with pytest.raises(AttributeError, match="reserved for generated lifecycle state"):
        item.__yidl_shadow__ = 1


def test_lifecycle_facade_rejects_lifecycle_field_deletion() -> None:
    class Counter:
        plain: int = field(default=1)
        count: int = managed(default=2)

    item = lifecycle(Counter)()

    with pytest.raises(
        AttributeError, match="lifecycle field 'plain' cannot be deleted"
    ):
        del item.plain
    with pytest.raises(
        AttributeError, match="lifecycle field 'count' cannot be deleted"
    ):
        del item.count


def test_lifecycle_decorator_uses_commit_order_key_provider() -> None:
    class Counter:
        rank: int = field(default=5)
        count: int = managed(default=1)

        @commit_order_key(DEFAULT_TRANSACTION)
        def _commit_key(self) -> tuple[int]:
            return (self.rank,)

    item = lifecycle(Counter)()

    assert item._y_state.commit_order_key_for(DEFAULT_TRANSACTION) == (5,)


def test_lifecycle_decorator_validation_failure_rolls_back_working_value() -> None:
    class Counter:
        count: int = managed(default=1)

        @validate_commit(DEFAULT_TRANSACTION)
        def _validate_count(self) -> bool:
            return self.count >= 0

    item = lifecycle(Counter)()

    with pytest.raises(ExceptionGroup, match="yidl commit validation failed"):
        with item.begin(DEFAULT_TRANSACTION):
            item.count = -1

    assert item.count == 1
    assert item.current.count == 1
    assert item.working.count == 1


def test_lifecycle_decorator_runs_transaction_hooks_by_group() -> None:
    events: list[tuple[str, str, int]] = []

    class Counter:
        count: int = managed(default=1)
        audit_count: int = managed("audit", default=10)

        @before_commit(DEFAULT_TRANSACTION)
        def _before_default_first(self) -> None:
            events.append(("before-1", "default", self.count))

        @before_commit(DEFAULT_TRANSACTION)
        def _before_default_second(self) -> None:
            events.append(("before-2", "default", self.count))

        @after_commit(DEFAULT_TRANSACTION)
        def _after_default(self) -> None:
            events.append(("after", "default", self.count))

        @after_rollback("audit")
        def _after_audit_rollback(self) -> None:
            events.append(("rollback", "audit", self.audit_count))

    item = lifecycle(Counter)()

    with item.begin(DEFAULT_TRANSACTION):
        item.count = 2

    assert events == [
        ("before-1", "default", 2),
        ("before-2", "default", 2),
        ("after", "default", 2),
    ]

    events.clear()
    with pytest.raises(RuntimeError, match="abort audit"):
        with item.begin("audit"):
            item.audit_count = 20
            raise RuntimeError("abort audit")

    assert item.audit_count == 10
    assert events == [("rollback", "audit", 10)]


def test_lifecycle_decorator_before_commit_failure_rolls_back() -> None:
    events: list[tuple[str, int]] = []

    class Counter:
        count: int = managed(default=1)

        @before_commit(DEFAULT_TRANSACTION)
        def _before_default(self) -> None:
            events.append(("before", self.count))
            raise ValueError("before failed")

        @after_commit(DEFAULT_TRANSACTION)
        def _after_default(self) -> None:
            events.append(("after", self.count))

    item = lifecycle(Counter)()

    with pytest.raises(ValueError, match="before failed"):
        with item.begin(DEFAULT_TRANSACTION):
            item.count = 2

    assert item.count == 1
    assert item.current.count == 1
    assert item.working.count == 1
    assert events == [("before", 2)]


def test_lifecycle_decorator_after_commit_failure_keeps_commit() -> None:
    events: list[tuple[str, int]] = []

    class Counter:
        count: int = managed(default=1)

        @after_commit(DEFAULT_TRANSACTION)
        def _after_default(self) -> None:
            events.append(("after", self.count))
            raise ValueError("after failed")

    item = lifecycle(Counter)()

    with pytest.raises(ValueError, match="after failed"):
        with item.begin(DEFAULT_TRANSACTION):
            item.count = 2

    assert item.count == 2
    assert item.current.count == 2
    assert item.working.count == 2
    assert events == [("after", 2)]


def test_lifecycle_decorator_freezes_working_value_during_prepare() -> None:
    events: list[tuple[str, int]] = []

    def freeze_count(value: int) -> int:
        events.append(("freeze", value))
        return value * 10

    class Counter:
        count: int = managed(default=1, freeze=freeze_count)

    item = lifecycle(Counter)()

    with item.begin(DEFAULT_TRANSACTION):
        item.count = 2
        assert item.current.count == 1
        assert item.working.count == 2

    assert item.count == 20
    assert item.current.count == 20
    assert item.working.count == 20
    assert events == [("freeze", 2)]


def test_lifecycle_decorator_freeze_failure_rolls_back_working_value() -> None:
    events: list[tuple[str, int]] = []

    def freeze_count(value: int) -> int:
        events.append(("freeze", value))
        raise ValueError("freeze failed")

    class Counter:
        count: int = managed(default=1, freeze=freeze_count)

    item = lifecycle(Counter)()

    with pytest.raises(ValueError, match="freeze failed"):
        with item.begin(DEFAULT_TRANSACTION):
            item.count = 2

    assert item.count == 1
    assert item.current.count == 1
    assert item.working.count == 1
    assert events == [("freeze", 2)]


def test_lifecycle_decorator_thaws_working_value_for_in_place_mutation() -> None:
    thaw_calls: list[tuple[int, ...]] = []
    freeze_calls: list[list[int]] = []

    def thaw_items(value: tuple[int, ...]) -> list[int]:
        thaw_calls.append(value)
        return list(value)

    def freeze_items(value: list[int]) -> tuple[int, ...]:
        freeze_calls.append(list(value))
        return tuple(value)

    class Counter:
        items: tuple[int, ...] = managed(
            default=(0, 0, 0),
            thaw=thaw_items,
            freeze=freeze_items,
        )

    item = lifecycle(Counter)()

    assert item.items == (0, 0, 0)
    assert item.working.items == (0, 0, 0)
    assert thaw_calls == []

    with item.begin(DEFAULT_TRANSACTION):
        working_items = item.working.items
        assert working_items == [0, 0, 0]
        working_items[2] = 7
        assert item.current.items == (0, 0, 0)

    assert item.items == (0, 0, 7)
    assert item.current.items == (0, 0, 7)
    assert item.working.items == (0, 0, 7)
    assert thaw_calls == [(0, 0, 0)]
    assert freeze_calls == [[0, 0, 7]]


def test_lifecycle_decorator_thaw_failure_does_not_publish_working_value() -> None:
    calls: list[tuple[int, ...]] = []

    def thaw_items(value: tuple[int, ...]) -> list[int]:
        calls.append(value)
        raise ValueError("thaw failed")

    class Counter:
        items: tuple[int, ...] = managed(default=(0, 0), thaw=thaw_items)

    item = lifecycle(Counter)()

    with item.begin(DEFAULT_TRANSACTION):
        with pytest.raises(ValueError, match="thaw failed"):
            item.working.items
        assert item.current.items == (0, 0)

    assert item.items == (0, 0)
    assert item.current.items == (0, 0)
    assert item.working.items == (0, 0)
    assert calls == [(0, 0)]


def test_lifecycle_decorator_optional_none_skips_thaw_and_freeze() -> None:
    calls: list[str] = []

    def thaw_items(value: tuple[int, ...]) -> list[int]:
        calls.append("thaw")
        return list(value)

    def freeze_items(value: list[int]) -> tuple[int, ...]:
        calls.append("freeze")
        return tuple(value)

    class Counter:
        items: tuple[int, ...] | None = managed(
            default=None,
            thaw=thaw_items,
            freeze=freeze_items,
        )

    item = lifecycle(Counter)()

    with item.begin(DEFAULT_TRANSACTION):
        assert item.working.items is None

    assert item.items is None
    assert item.current.items is None
    assert item.working.items is None
    assert calls == []


def test_lifecycle_decorator_after_rollback_failure_keeps_rollback() -> None:
    events: list[tuple[str, int]] = []

    class Counter:
        count: int = managed(default=1)

        @after_rollback(DEFAULT_TRANSACTION)
        def _after_default_rollback(self) -> None:
            events.append(("rollback", self.count))
            raise ValueError("rollback failed")

    item = lifecycle(Counter)()

    item.begin(DEFAULT_TRANSACTION)
    item.count = 2
    with pytest.raises(ValueError, match="rollback failed"):
        item.rollback(DEFAULT_TRANSACTION)

    assert item.count == 1
    assert item.current.count == 1
    assert item.working.count == 1
    assert events == [("rollback", 1)]


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
