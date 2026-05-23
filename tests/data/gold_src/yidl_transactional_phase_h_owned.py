from __future__ import annotations

from collections.abc import Mapping
from pathlib import Path

import black

from support.golden_case import run_multi_source_case
from yidl.runtime.bindings import BindingBase
from yidl.runtime.bindings import BindingDict
from yidl.runtime.lifecycle import _generate_lifecycle_source
from yidl.runtime.lifecycle import binding
from yidl.runtime.lifecycle import harvest_lifecycle_definition
from yidl.runtime.lifecycle import lifecycle
from yidl.runtime.lifecycle import managed
from yidl.runtime.lifecycle import owned
from yidl.runtime.transaction_yidl import DEFAULT_TRANSACTION

DECORATOR_PATH = Path("src/yidl/runtime/_generated_lifecycle_base.py")


class SpyBinding(BindingBase):
    def __init__(self, name: str):
        super().__init__()
        self.name = name

    def __eq__(self, other: object) -> bool:
        return isinstance(other, SpyBinding) and self.name == other.name


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
    assert "BindingField" in decorator_namespace
    assert "OwnedField" in decorator_namespace
    assert "IndexedOwnedField" in decorator_namespace
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
    class Owner:
        value_state: list[int] = managed(default_factory=lambda: [1])
        identity_state: list[int] = managed(compare="identity", default_factory=lambda: [1])
        child: BindingBase | None = owned(default=None)
        identity_child: BindingBase | None = owned(compare="identity", default=None)
        children: dict[str, BindingBase] = owned(default_factory=lambda: {})
        handle: BindingBase | None = binding(default=None)
        handles: dict[str, BindingBase] = binding(default_factory=lambda: {})

    return Owner


def _assert_generated_class(namespace: Mapping[str, object]) -> None:
    owner_cls = _fixture_class()
    harvested = harvest_lifecycle_definition(owner_cls)
    generated = namespace["build_lifecycle_class"](
        owner_cls,
        **dict(harvested.build_kwargs),
    )
    _assert_owner_class(generated)


def _assert_decorator_frontend() -> None:
    generated = lifecycle(_fixture_class())
    _assert_owner_class(generated)


def _assert_owner_class(generated: type[object]) -> None:
    owner = generated()
    assert generated.__name__ == "Owner"
    assert generated.__yidl_tx_index_to_key__ == (DEFAULT_TRANSACTION,)

    assert owner.value_state == [1]
    assert owner.identity_state == [1]
    assert owner.child is None
    assert owner.identity_child is None
    assert isinstance(owner.children, BindingDict)
    assert owner.handle is None
    assert isinstance(owner.handles, BindingDict)

    current_value_state = owner.value_state
    with owner.begin(DEFAULT_TRANSACTION):
        owner.value_state = [1]
        assert owner.value_state is current_value_state

    identity_replacement = [1]
    with owner.begin(DEFAULT_TRANSACTION):
        owner.identity_state = identity_replacement
        assert owner.identity_state is identity_replacement
        assert owner.current.identity_state is not identity_replacement

    assert owner.identity_state is identity_replacement

    handle = SpyBinding("handle")
    owner.handle = handle
    assert owner.handle is handle
    _assert_raises(TypeError, "binding field 'handle' expects", lambda: setattr(owner, "handle", object()))

    mapped_handle = SpyBinding("mapped-handle")
    owner.handles = {"mapped": mapped_handle}
    assert isinstance(owner.handles, BindingDict)
    assert owner.handles["mapped"] is mapped_handle
    _assert_raises(
        TypeError,
        "binding map field 'handles' expects",
        lambda: setattr(owner, "handles", object()),
    )
    _assert_raises(
        TypeError,
        "expects BindingBase values",
        lambda: setattr(owner, "handles", {"bad": object()}),
    )

    child = SpyBinding("child")
    _assert_raises(RuntimeError, "writes require", lambda: setattr(owner, "child", child))
    _assert_raises(
        AttributeError,
        "current facade is read-only",
        lambda: setattr(owner.current, "child", child),
    )

    with owner.begin(DEFAULT_TRANSACTION):
        owner.child = child
        assert owner.child is child
        assert owner.current.child is None
        assert child.is_accepted is False

    assert owner.child is child
    assert owner.current.child is child
    assert child.is_accepted is True

    equal_child = SpyBinding("child")
    with owner.begin(DEFAULT_TRANSACTION):
        owner.child = equal_child
        assert owner.child is child

    identity_child = SpyBinding("identity-child")
    with owner.begin(DEFAULT_TRANSACTION):
        owner.identity_child = identity_child

    equal_identity_child = SpyBinding("identity-child")
    with owner.begin(DEFAULT_TRANSACTION):
        owner.identity_child = equal_identity_child
        assert owner.identity_child is equal_identity_child
        assert owner.current.identity_child is identity_child

    assert owner.identity_child is equal_identity_child

    first = SpyBinding("first")
    second = SpyBinding("second")
    with owner.begin(DEFAULT_TRANSACTION):
        owner.children = {"first": first, "second": second}
        assert owner.children["first"] is first
        assert owner.current.children == {}
        assert first.is_accepted is False
        assert second.is_accepted is False

    assert owner.children["first"] is first
    assert owner.children["second"] is second
    assert first.is_accepted is True
    assert second.is_accepted is True

    replacement = SpyBinding("replacement")
    _assert_raises(RuntimeError, "abort", lambda: _abort_owned_map(owner, replacement))
    assert "replacement" not in owner.children
    assert owner.children["first"] is first
    assert replacement.is_accepted is False

    with owner.begin(DEFAULT_TRANSACTION):
        owner.child = None
        assert owner.child is None
        assert owner.current.child is child

    assert owner.child is None
    assert owner.current.child is None


def _abort_owned_map(owner: object, replacement: SpyBinding) -> None:
    with owner.begin(DEFAULT_TRANSACTION):
        owner.children = {"replacement": replacement}
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
    for source in sources.values():
        assert "inc_ref(" not in source
        assert "dec_ref(" not in source

    source = sources["generated_output.py"]
    prettier_source = sources["generated_output_prettier.py"]
    for generated in (source, prettier_source):
        assert "_y_validate_binding_value" in generated
        assert "_y_validate_binding_map_value" in generated
        assert "if current == next_value:" in generated
        assert "if current is next_value:" in generated
        assert ".accepted()" in generated
        assert "BindingDict" in generated
        assert "state._y_ensure_working_transaction(0)" in generated
        assert "_y_child_staged = VOID" in generated
        assert "_y_children_staged = VOID" in generated


def _prettier_source(source: str) -> str:
    return black.format_str(source, mode=black.FileMode())


if __name__ == "__main__":
    raise SystemExit(
        run_multi_source_case(
            "yidl_transactional_phase_h_owned.py",
            render_case,
            validate_case,
        )
    )
