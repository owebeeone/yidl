from __future__ import annotations

from collections.abc import Mapping
from pathlib import Path

import black

from support.golden_case import run_multi_source_case
from yidl.runtime.lifecycle import _generate_lifecycle_source
from yidl.runtime.lifecycle import harvest_lifecycle_definition
from yidl.runtime.lifecycle import lifecycle
from yidl.runtime.lifecycle import local_store
from yidl.runtime.lifecycle import managed
from yidl.runtime.transaction_yidl import DEFAULT_TRANSACTION
from yidl.runtime.transaction_yidl import TransactionManager

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
    assert "LocalStoreField" in decorator_namespace
    assert "LocalStoreFieldsCollection" in decorator_namespace

    output_namespace: dict[str, object] = {}
    exec(sources["generated_output.py"], output_namespace)
    output_prettier_namespace: dict[str, object] = {}
    exec(sources["generated_output_prettier.py"], output_prettier_namespace)

    _assert_generated_class(output_namespace)
    _assert_generated_class(output_prettier_namespace)
    _assert_decorator_frontend()
    _assert_source_shape(sources)


def _fixture_class() -> type[object]:
    class Scratch:
        cache: dict[str, int] = local_store(default_factory=dict)
        marker: list[str] = local_store(default=["ready"])
        count: int = managed(default=1)

        def manager(self) -> object:
            return self._y_get_transaction_manager()

    return Scratch


def _assert_generated_class(namespace: Mapping[str, object]) -> None:
    scratch_cls = _fixture_class()
    harvested = harvest_lifecycle_definition(scratch_cls)
    transaction_manager = TransactionManager()
    generated = namespace["build_lifecycle_class"](
        scratch_cls,
        **dict(harvested.build_kwargs),
    )
    _assert_scratch_class(generated, transaction_manager=transaction_manager)


def _assert_decorator_frontend() -> None:
    generated = lifecycle(_fixture_class())
    _assert_scratch_class(generated)


def _assert_scratch_class(
    generated: type[object],
    *,
    transaction_manager: TransactionManager | None = None,
) -> None:
    scratch = (
        generated(transaction_manager=transaction_manager)
        if transaction_manager is not None
        else generated()
    )
    expected_manager = transaction_manager or scratch._y_state._y_transaction_manager
    assert scratch._y_get_transaction_manager() is expected_manager
    assert scratch.manager() is expected_manager
    assert scratch.current.manager() is expected_manager
    assert scratch.working.manager() is expected_manager
    assert scratch.cache is scratch.current.cache
    assert scratch.cache is scratch.working.cache
    assert scratch.marker == ["ready"]

    scratch.cache["a"] = 1
    assert scratch.current.cache == {"a": 1}
    assert scratch._y_state._y_working_tx_ids[0] is None

    with scratch.begin(DEFAULT_TRANSACTION):
        scratch.cache["b"] = 2
        assert scratch._y_state._y_working_tx_ids[0] is None
        scratch.count = 5

    assert scratch.cache == {"a": 1, "b": 2}
    assert scratch.count == 5

    try:
        with scratch.begin(DEFAULT_TRANSACTION):
            scratch.cache["c"] = 3
            scratch.count = 7
            raise RuntimeError("rollback")
    except RuntimeError:
        pass

    assert scratch.cache == {"a": 1, "b": 2, "c": 3}
    assert scratch.count == 5


def _assert_source_shape(sources: Mapping[str, str]) -> None:
    source = sources["generated_output.py"]
    assert "_y_cache_value" in source
    assert "_y_cache_current" not in source
    assert "_y_cache_working" not in source
    assert "_y_cache_staged" not in source
    assert "_Scratch_cache_default_factory()" in source
    assert "def _y_get_transaction_manager(self):" in source


def _prettier_source(source: str) -> str:
    return black.format_str(source, mode=black.FileMode())


if __name__ == "__main__":
    raise SystemExit(
        run_multi_source_case(
            "yidl_transactional_lifecycle_local_store.py",
            render_case,
            validate_case,
        )
    )
