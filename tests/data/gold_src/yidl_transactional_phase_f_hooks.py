from __future__ import annotations

from collections.abc import Mapping
from pathlib import Path

import black

from support.golden_case import run_multi_source_case
from yidl.runtime.lifecycle import _generate_lifecycle_source
from yidl.runtime.lifecycle import after_commit
from yidl.runtime.lifecycle import after_rollback
from yidl.runtime.lifecycle import before_commit
from yidl.runtime.lifecycle import commit_order_key
from yidl.runtime.lifecycle import field
from yidl.runtime.lifecycle import harvest_lifecycle_definition
from yidl.runtime.lifecycle import lifecycle
from yidl.runtime.lifecycle import managed
from yidl.runtime.lifecycle import validate_commit
from yidl.runtime.transaction_yidl import DEFAULT_TRANSACTION

DECORATOR_PATH = Path("src/yidl/runtime/_generated_lifecycle_base.py")


def render_case() -> Mapping[str, str]:
    decorator_source = DECORATOR_PATH.read_text(encoding="utf-8")
    output_source = _generate_lifecycle_source(
        harvest_lifecycle_definition(_fixture_class([])),
    )
    return {
        "decorator.py": decorator_source,
        "decorator_prettier.py": _prettier_source(decorator_source),
        "generated_output.py": output_source,
        "generated_output_prettier.py": _prettier_source(output_source),
    }


def validate_case(sources: Mapping[str, str]) -> None:
    decorator_namespace: dict[str, object] = {}
    exec(sources["decorator.py"], decorator_namespace)
    assert "LifecycleClass" in decorator_namespace
    assert "TransactionMethod" in decorator_namespace
    assert "build_LifecycleModule" in decorator_namespace

    output_namespace: dict[str, object] = {}
    exec(sources["generated_output.py"], output_namespace)
    output_prettier_namespace: dict[str, object] = {}
    exec(sources["generated_output_prettier.py"], output_prettier_namespace)

    _assert_generated_class(output_namespace)
    _assert_generated_class(output_prettier_namespace)
    _assert_decorator_frontend()
    _assert_source_shape(sources)


def _fixture_class(events: list[tuple[str, str, int]]) -> type[object]:
    def thaw_items(value: tuple[int, ...]) -> list[int]:
        return list(value)

    def freeze_items(value: list[int]) -> tuple[int, ...]:
        return tuple(value)

    class Counter:
        rank: int = field(default=5)
        count: int = managed(default=1)
        items: tuple[int, ...] = managed(
            default=(1, 2),
            thaw=thaw_items,
            freeze=freeze_items,
        )
        optional_items: tuple[int, ...] | None = managed(
            default=None,
            thaw=thaw_items,
            freeze=freeze_items,
        )
        audit_count: int = managed("audit", default=10)

        @commit_order_key(DEFAULT_TRANSACTION)
        def _commit_key(self) -> tuple[int]:
            return (self.rank,)

        @validate_commit(DEFAULT_TRANSACTION)
        def _validate_count(self) -> bool:
            return self.count >= 0

        @before_commit(DEFAULT_TRANSACTION)
        def _before_default(self) -> None:
            events.append(("before", "default", self.count))

        @after_commit(DEFAULT_TRANSACTION)
        def _after_default(self) -> None:
            events.append(("after", "default", self.count))

        @after_rollback("audit")
        def _after_audit_rollback(self) -> None:
            events.append(("rollback", "audit", self.audit_count))

    return Counter


def _assert_generated_class(namespace: Mapping[str, object]) -> None:
    events: list[tuple[str, str, int]] = []
    counter_cls = _fixture_class(events)
    harvested = harvest_lifecycle_definition(counter_cls)
    generated = namespace["build_lifecycle_class"](
        counter_cls,
        **dict(harvested.build_kwargs),
    )
    _assert_counter_class(generated, counter_cls, events)


def _assert_decorator_frontend() -> None:
    events: list[tuple[str, str, int]] = []
    counter_cls = _fixture_class(events)
    generated = lifecycle(counter_cls)
    _assert_counter_class(generated, counter_cls, events)


def _assert_counter_class(
    generated: type[object],
    counter_cls: type[object],
    events: list[tuple[str, str, int]],
) -> None:
    assert generated.__name__ == "Counter"
    assert generated.__qualname__ == counter_cls.__qualname__
    assert generated.__module__ == counter_cls.__module__
    assert generated.__yidl_lifecycle_generated__ is True
    assert generated.__yidl_lifecycle_user_class__ is counter_cls
    assert generated.__yidl_tx_index_to_key__ == (DEFAULT_TRANSACTION, "audit")

    item = generated()
    assert item._y_state.commit_order_key_for(DEFAULT_TRANSACTION) == (5,)
    assert item._y_state.requires_validation_for(DEFAULT_TRANSACTION) is True
    assert item._y_state.requires_validation_for("audit") is False

    with item.begin(DEFAULT_TRANSACTION):
        item.count = 2
        item.working.items[1] = 9

    assert item.count == 2
    assert item.items == (1, 9)
    assert item.optional_items is None
    assert events == [
        ("before", "default", 2),
        ("after", "default", 2),
    ]

    events.clear()
    _assert_raises_exception_group(
        "yidl commit validation failed",
        lambda: _attempt_invalid_commit(item),
    )
    assert item.count == 2
    assert item.current.count == 2
    assert item.working.count == 2
    assert events == []

    _assert_raises(
        RuntimeError, "rollback audit", lambda: _attempt_audit_rollback(item)
    )
    assert item.audit_count == 10
    assert events == [("rollback", "audit", 10)]


def _attempt_invalid_commit(item: object) -> None:
    with item.begin(DEFAULT_TRANSACTION):
        item.count = -1


def _attempt_audit_rollback(item: object) -> None:
    with item.begin("audit"):
        item.audit_count = 20
        raise RuntimeError("rollback audit")


def _assert_raises(
    exception_type: type[BaseException],
    message: str,
    func: object,
) -> None:
    try:
        func()
    except exception_type as exc:
        assert message in str(exc)
        return
    raise AssertionError(f"expected {exception_type.__name__}")


def _assert_raises_exception_group(message: str, func: object) -> None:
    try:
        func()
    except ExceptionGroup as exc:
        assert message in str(exc)
        return
    raise AssertionError("expected ExceptionGroup")


def _assert_source_shape(sources: Mapping[str, str]) -> None:
    source = sources["generated_output.py"]
    prettier_source = sources["generated_output_prettier.py"]
    for generated in (source, prettier_source):
        assert "return self._y_get_default_facade()._commit_key()" in generated
        assert "result = self._y_get_default_facade()._validate_count()" in generated
        assert "self._y_get_default_facade()._before_default()" in generated
        assert "self._y_get_default_facade()._after_default()" in generated
        assert "self._y_get_default_facade()._after_audit_rollback()" in generated
        assert "if result is False:" not in generated
        assert "return self._y_get_default_facade()._commit_key()\n            return ()" not in generated
        assert "return True\n            return False" not in generated
        assert "__weakref__" in generated
        assert 'if tx_key == "default_transaction":' not in generated
        assert 'if tx_key == "audit":' not in generated
        assert "tx_index = self.__yidl_tx_key_to_index__[tx_key]" in generated
        assert "match tx_index:" in generated
        assert "case _ if tx_index == 0:" in generated
        assert "case _ if tx_index == 1:" in generated
        assert "def _prepare_commit_tx_by_key(" in generated
        assert "def _apply_prepared_commit_tx_by_key(" in generated
        assert "def _after_commit_tx_by_key(" in generated
        assert "def _rollback_tx_by_key(" in generated
        assert "def _after_rollback_tx_by_key(" in generated
        assert "def _commit_order_key_tx_0(self):" in generated
        assert "def _requires_validation_tx_0(self):" in generated
        assert "def _validate_commit_tx_0(self):" in generated
        assert "def _before_commit_tx_0(self):" in generated
        assert "def _after_commit_tx_0(self):" in generated
        assert "def _after_rollback_tx_1(self):" in generated
        assert "def _apply_prepared_commit_tx_0_fields(self):" in generated
        assert "def _apply_prepared_commit_tx_1_fields(self):" in generated
        assert "def _rollback_tx_0_fields(self):" in generated
        assert "def _rollback_tx_1_fields(self):" in generated
        assert "_Counter_items_freeze" in generated
        assert "_Counter_items_thaw" in generated
        assert "_y_items_staged" in generated
        assert "self._y_items_staged = _Counter_items_freeze(" in generated
        assert "next_value = _Counter_items_thaw(" in generated
        assert "_y_optional_items_staged" in generated
        assert "if self._y_optional_items_working is None" in generated
        assert "_Counter_optional_items_freeze" in generated
        assert "_Counter_optional_items_thaw" in generated
        assert "if current_value is None" in generated
        assert "def _commit_transaction(" not in generated
        assert "def _rollback_transaction(" not in generated
        assert "getattr(\n            self._y_get_default_facade()" not in generated


def _prettier_source(source: str) -> str:
    return black.format_str(source, mode=black.FileMode())


if __name__ == "__main__":
    raise SystemExit(
        run_multi_source_case(
            "yidl_transactional_phase_f_hooks.py",
            render_case,
            validate_case,
        )
    )
