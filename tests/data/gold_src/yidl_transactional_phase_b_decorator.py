from __future__ import annotations

from collections.abc import Mapping
from pathlib import Path

import black

from support.golden_case import run_multi_source_case
from yidl.runtime.lifecycle import _generate_lifecycle_source
from yidl.runtime.lifecycle import classvar
from yidl.runtime.lifecycle import field
from yidl.runtime.lifecycle import harvest_lifecycle_definition
from yidl.runtime.lifecycle import initvar
from yidl.runtime.lifecycle import lifecycle
from yidl.runtime.lifecycle import managed
from yidl.runtime.transaction_yidl import DEFAULT_TRANSACTION


DECORATOR_PATH = Path("src/yidl/runtime/_generated_lifecycle_base.py")


def render_case() -> Mapping[str, str]:
    decorator_source = DECORATOR_PATH.read_text(encoding="utf-8")
    output_source = _generate_lifecycle_source(
        harvest_lifecycle_definition(_fixture_class()),
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
    assert "build_LifecycleModule" in decorator_namespace

    output_namespace: dict[str, object] = {}
    exec(sources["generated_output.py"], output_namespace)
    output_prettier_namespace: dict[str, object] = {}
    exec(sources["generated_output_prettier.py"], output_prettier_namespace)

    _assert_generated_class(output_namespace)
    _assert_generated_class(output_prettier_namespace)
    _assert_decorator_frontend()


def _fixture_class() -> type[object]:
    class Counter:
        plain: int = field(default=3)
        seed: int = initvar(default=2)
        KIND: str = classvar(default="counter")
        count: int = managed(default=1)
        audit_count: int = managed("audit", default=10)

        def user_method(self) -> str:
            return "user"

    return Counter


def _assert_generated_class(namespace: Mapping[str, object]) -> None:
    counter_cls = _fixture_class()
    harvested = harvest_lifecycle_definition(counter_cls)
    generated = namespace["build_lifecycle_class"](
        counter_cls,
        **dict(harvested.build_kwargs),
    )
    _assert_counter_class(generated, counter_cls)


def _assert_decorator_frontend() -> None:
    counter_cls = _fixture_class()
    generated = lifecycle(counter_cls)
    _assert_counter_class(generated, counter_cls)


def _assert_counter_class(
    generated: type[object],
    counter_cls: type[object],
) -> None:
    assert generated.__name__ == "Counter"
    assert generated.__qualname__ == counter_cls.__qualname__
    assert generated.__module__ == counter_cls.__module__
    assert generated.__yidl_lifecycle_generated__ is True
    assert generated.__yidl_lifecycle_user_class__ is counter_cls
    assert generated.__yidl_tx_index_to_group__ == (DEFAULT_TRANSACTION, "audit")
    assert generated.__yidl_tx_group_to_index__ == {
        DEFAULT_TRANSACTION: 0,
        "audit": 1,
    }

    counter = generated()
    assert isinstance(counter, counter_cls)
    assert counter.user_method() == "user"
    assert counter.default is counter
    assert counter.current is counter.current
    assert counter.working is counter.working

    assert generated.KIND == "counter"
    assert counter.current.KIND == "counter"
    assert counter.working.KIND == "counter"
    assert counter.plain == 3
    assert counter.current.plain == 3
    assert counter.working.plain == 3

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


def _prettier_source(source: str) -> str:
    return black.format_str(source, mode=black.FileMode())


if __name__ == "__main__":
    raise SystemExit(
        run_multi_source_case(
            "yidl_transactional_phase_b_decorator.py",
            render_case,
            validate_case,
        )
    )
