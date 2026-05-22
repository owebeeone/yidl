from __future__ import annotations

from collections.abc import Mapping
from pathlib import Path

import black

from support.golden_case import run_multi_source_case
from yidl.runtime.lifecycle import _generate_lifecycle_source
from yidl.runtime.lifecycle import harvest_lifecycle_definition
from yidl.runtime.lifecycle import initvar
from yidl.runtime.lifecycle import lifecycle
from yidl.runtime.lifecycle import transient
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
    assert "TransientField" in decorator_namespace
    assert "IndexedTransientField" in decorator_namespace
    assert "build_LifecycleModule" in decorator_namespace

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
        seed: int = initvar(default=4)
        label: str = transient(default="ready")
        marker: str = transient(default="base")
        items: list[int] = transient(default_factory=lambda seed: [seed])
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

    return Scratch


def _assert_generated_class(namespace: Mapping[str, object]) -> None:
    scratch_cls = _fixture_class()
    harvested = harvest_lifecycle_definition(scratch_cls)
    generated = namespace["build_lifecycle_class"](
        scratch_cls,
        **dict(harvested.build_kwargs),
    )
    _assert_scratch_class(generated)


def _assert_decorator_frontend() -> None:
    generated = lifecycle(_fixture_class())
    _assert_scratch_class(generated)


def _assert_scratch_class(generated: type[object]) -> None:
    item = generated()
    assert generated.__name__ == "Scratch"
    assert generated.__yidl_tx_index_to_key__ == (DEFAULT_TRANSACTION, "audit")

    assert item._y_state._y_seed_initvar == 4
    assert item.label == "ready"
    assert item.current.label == "ready"
    assert item.marker == "base"
    assert item.current.marker == "base"
    assert item.items == [4]
    assert item.current.items == [4]
    assert item.buffer is None
    assert item.current.buffer is None
    assert item.audit_buffer is None

    _assert_raises(RuntimeError, "writes require", lambda: setattr(item, "buffer", [9]))
    _assert_raises(
        AttributeError,
        "no setter",
        lambda: setattr(item.current, "buffer", [9]),
    )

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
        assert item.audit_buffer is None

    assert item.buffer is None
    assert item.current.buffer is None

    _assert_raises(RuntimeError, "abort", lambda: _abort_default_tx(item))
    assert item.buffer is None
    assert item.current.buffer is None

    with item.begin("audit"):
        assert item.buffer is None
        assert item.audit_buffer == []
        item.audit_buffer.append(3)
        assert item.audit_buffer == [3]
        assert item.current.audit_buffer is None

    assert item.audit_buffer is None
    assert item.current.audit_buffer is None


def _abort_default_tx(item: object) -> None:
    with item.begin(DEFAULT_TRANSACTION):
        item.buffer = [2]
        raise RuntimeError("abort")


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


def _assert_source_shape(sources: Mapping[str, str]) -> None:
    source = sources["generated_output.py"]
    prettier_source = sources["generated_output_prettier.py"]
    for generated in (source, prettier_source):
        assert "_Scratch_items_default_factory(seed=seed)" in generated
        assert "_Scratch_buffer_working_default_factory(" in generated
        assert "self=state._y_get_default_facade()" in generated
        assert "current=state._y_get_current_facade()" in generated
        assert "working=state._y_get_working_facade()" in generated
        assert "seed=state._y_seed_initvar" in generated
        assert "_Scratch_audit_buffer_working_default_factory()" in generated
        assert "state._y_ensure_working_transaction(0)" in generated
        assert "state._y_ensure_working_transaction(1)" in generated
        assert "state._y_marker_working = state._y_marker_current" in generated
        assert "tx_index = self.__yidl_tx_key_to_index__[tx_key]" in generated
        assert 'if tx_key == "audit":' not in generated
        assert 'if tx_key == "default_transaction":' not in generated
        assert "_y_buffer_working = VOID" in generated
        assert "_y_audit_buffer_working = VOID" in generated


def _prettier_source(source: str) -> str:
    return black.format_str(source, mode=black.FileMode())


if __name__ == "__main__":
    raise SystemExit(
        run_multi_source_case(
            "yidl_transactional_phase_g_transient.py",
            render_case,
            validate_case,
        )
    )
