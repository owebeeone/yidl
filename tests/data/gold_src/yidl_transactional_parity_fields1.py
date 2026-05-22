from __future__ import annotations

from collections.abc import Mapping
from pathlib import Path

import black

from support.golden_case import run_multi_source_case
from yidl.runtime.lifecycle import _generate_lifecycle_source
from yidl.runtime.lifecycle import const
from yidl.runtime.lifecycle import harvest_lifecycle_definition
from yidl.runtime.lifecycle import initvar
from yidl.runtime.lifecycle import lifecycle
from yidl.runtime.lifecycle import static

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
    assert "ConstField" in decorator_namespace
    assert "StaticField" in decorator_namespace
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
    calls: list[None] = []

    def make_items() -> list[int]:
        calls.append(None)
        return [1, 2]

    class Config:
        seed: int = initvar(default=3)
        slot_id: int = const(default=7)
        derived_id: int = const(default_factory=lambda seed, slot_id: seed + slot_id)
        declared: tuple[str, ...] = static()
        lazy_number: int = static(default=42)
        items: list[int] = static(default_factory=make_items)
        seeded_static: int = static(default_factory=lambda slot_id: slot_id + 5)

    Config._test_factory_calls = calls
    return Config


def _assert_generated_class(namespace: Mapping[str, object]) -> None:
    config_cls = _fixture_class()
    harvested = harvest_lifecycle_definition(config_cls)
    generated = namespace["build_lifecycle_class"](
        config_cls,
        **dict(harvested.build_kwargs),
    )
    _assert_config_class(generated)


def _assert_decorator_frontend() -> None:
    generated = lifecycle(_fixture_class())
    _assert_config_class(generated)


def _assert_config_class(generated: type[object]) -> None:
    item = generated()

    assert item.slot_id == 7
    assert item.current.slot_id == 7
    assert item.working.slot_id == 7
    assert item.derived_id == 10
    _assert_raises(
        AttributeError,
        "const field 'slot_id' is read-only",
        lambda: setattr(item, "slot_id", 8),
    )
    _assert_raises(
        AttributeError,
        "const field 'slot_id' is read-only",
        lambda: setattr(item.current, "slot_id", 8),
    )

    _assert_raises(
        AttributeError,
        "static field 'declared' is not initialized",
        lambda: getattr(item, "declared"),
    )
    item.declared = ("a", "b")
    assert item.declared == ("a", "b")
    assert item.current.declared == ("a", "b")
    assert item.working.declared == ("a", "b")
    _assert_raises(
        AttributeError,
        "static field 'declared' is already initialized",
        lambda: setattr(item, "declared", ("x",)),
    )

    override = generated(lazy_number=7)
    assert override.lazy_number == 7
    assign_first = generated()
    assign_first.lazy_number = 9
    assert assign_first.lazy_number == 9
    read_default = generated()
    assert read_default.lazy_number == 42

    calls = getattr(generated.__yidl_lifecycle_user_class__, "_test_factory_calls")
    assert calls == []
    assert item.items == [1, 2]
    assert calls == [None]
    assert item.items is item.items
    assert item.seeded_static == 12


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
        assert "const field {'slot_id'!r} is read-only" in generated
        assert "static field {'declared'!r} is not initialized" in generated
        assert "static field {'declared'!r} is already initialized" in generated
        assert "_y_declared_value = VOID" in generated
        assert "_Config_items_default_factory()" in generated
        assert (
            "_Config_seeded_static_default_factory(slot_id=self.slot_id)" in generated
        )


def _prettier_source(source: str) -> str:
    return black.format_str(source, mode=black.FileMode())


if __name__ == "__main__":
    raise SystemExit(
        run_multi_source_case(
            "yidl_transactional_parity_fields1.py",
            render_case,
            validate_case,
        )
    )
