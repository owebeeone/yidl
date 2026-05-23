from __future__ import annotations

import pytest

from yidl.runtime.lifecycle import LifecycleDefinitionError
from yidl.runtime.lifecycle import MISSING
from yidl.runtime.lifecycle import _HAS_DEFAULT_FACTORY
from yidl.runtime.lifecycle import binding
from yidl.runtime.lifecycle import classvar
from yidl.runtime.lifecycle import field
from yidl.runtime.lifecycle import harvest_lifecycle_definition
from yidl.runtime.lifecycle import initvar
from yidl.runtime.lifecycle import managed
from yidl.runtime.lifecycle import owned
from yidl.runtime.lifecycle import normalize_marker
from yidl.runtime.lifecycle import transient
from yidl.runtime.transaction_yidl import DEFAULT_TRANSACTION


def test_field_marker_preserves_default_none() -> None:
    decl = normalize_marker("optional", str | None, field(default=None))

    assert decl.name == "optional"
    assert decl.kind == "field"
    assert decl.has_default is True
    assert decl.default is None
    assert decl.has_default_factory is False
    assert decl.default_factory is MISSING


def test_field_marker_without_default_uses_missing() -> None:
    decl = normalize_marker("plain", int, field())

    assert decl.has_default is False
    assert decl.default is MISSING
    assert decl.has_default_factory is False


def test_has_default_factory_sentinel_is_shared_runtime_identity() -> None:
    from yidl.runtime import lifecycle as lifecycle_module
    from yidl.runtime import lifecycle_markers

    assert _HAS_DEFAULT_FACTORY is lifecycle_module._HAS_DEFAULT_FACTORY
    assert _HAS_DEFAULT_FACTORY is lifecycle_markers._HAS_DEFAULT_FACTORY


def test_field_marker_preserves_default_factory() -> None:
    decl = normalize_marker("tags", list[str], field(default_factory=list))

    assert decl.has_default is False
    assert decl.has_default_factory is True
    assert decl.default_factory is list


def test_initvar_marker_normalizes() -> None:
    decl = normalize_marker("seed", int, initvar(default=2))

    assert decl.kind == "initvar"
    assert decl.init is True
    assert decl.has_default is True
    assert decl.default == 2


def test_classvar_marker_normalizes_as_non_init() -> None:
    decl = normalize_marker("KIND", str, classvar(default="counter"))

    assert decl.kind == "classvar"
    assert decl.init is False
    assert decl.has_default is True
    assert decl.default == "counter"


def test_managed_marker_defaults_to_default_transaction() -> None:
    decl = normalize_marker("count", int, managed(default=1))

    assert decl.kind == "managed"
    assert decl.tx_key == DEFAULT_TRANSACTION
    assert decl.default == 1


def test_managed_marker_accepts_positional_transaction_group() -> None:
    decl = normalize_marker("audit_count", int, managed("audit", default=10))

    assert decl.kind == "managed"
    assert decl.tx_key == "audit"
    assert decl.default == 10


def test_managed_marker_accepts_keyword_transaction_group() -> None:
    decl = normalize_marker(
        "audit_count",
        int,
        managed(tx_key="audit", default=10),
    )

    assert decl.tx_key == "audit"


def test_managed_marker_preserves_freeze_and_thaw_callables() -> None:
    def freeze(value: object) -> object:
        return value

    def thaw(value: object) -> object:
        return value

    decl = normalize_marker(
        "items",
        tuple[int, ...],
        managed(default=(), freeze=freeze, thaw=thaw),
    )

    assert decl.freeze is freeze
    assert decl.thaw is thaw
    assert decl.has_freeze is True
    assert decl.has_thaw is True


def test_transient_marker_defaults_to_default_transaction_key() -> None:
    decl = normalize_marker("scratch", list[int], transient(default_factory=list))

    assert decl.kind == "transient"
    assert decl.tx_key == DEFAULT_TRANSACTION
    assert decl.has_default_factory is True
    assert decl.default_factory is list
    assert decl.has_working_default_factory is False
    assert decl.working_default_factory is MISSING


def test_transient_marker_accepts_transaction_key_and_working_factory() -> None:
    def working_factory() -> list[int]:
        return []

    decl = normalize_marker(
        "scratch",
        list[int],
        transient(
            tx_key="audit", default=None, working_default_factory=working_factory
        ),
    )

    assert decl.kind == "transient"
    assert decl.tx_key == "audit"
    assert decl.has_default is True
    assert decl.default is None
    assert decl.has_working_default_factory is True
    assert decl.working_default_factory is working_factory


def test_owned_marker_defaults_to_default_transaction_key() -> None:
    decl = normalize_marker("child", object, owned(default=None))

    assert decl.kind == "owned"
    assert decl.tx_key == DEFAULT_TRANSACTION
    assert decl.has_default is True
    assert decl.default is None


def test_owned_marker_accepts_transaction_key_and_factory() -> None:
    def factory() -> object:
        return object()

    decl = normalize_marker("child", object, owned("audit", default_factory=factory))

    assert decl.kind == "owned"
    assert decl.tx_key == "audit"
    assert decl.has_default is False
    assert decl.has_default_factory is True
    assert decl.default_factory is factory


def test_binding_marker_normalizes_as_plain_binding_resource() -> None:
    decl = normalize_marker("handle", object, binding(default=None))

    assert decl.kind == "binding"
    assert decl.tx_key is MISSING
    assert decl.has_default is True
    assert decl.default is None


def test_harvester_emits_owned_and_binding_field_facts() -> None:
    class Example:
        child: object = owned("audit", default=None)
        handle: object = binding(default=None)

    harvested = harvest_lifecycle_definition(Example)
    child = next(fact for fact in harvested.field_facts if fact["field_name"] == "child")
    handle = next(
        fact for fact in harvested.field_facts if fact["field_name"] == "handle"
    )

    assert child["field_kind"] == "owned"
    assert child["tx_key_key"] == "audit"
    assert child["current_slot_name"] == "_y_child_current"
    assert child["working_slot_name"] == "_y_child_working"
    assert handle["field_kind"] == "binding"
    assert handle["value_slot_name"] == "_y_handle_value"
    assert harvested.tx_keys == (DEFAULT_TRANSACTION, "audit")
    assert harvested.class_fact["lifecycle_field_names"] == ("child", "handle")


def test_harvester_emits_transient_field_facts() -> None:
    def working_factory(seed: int) -> list[int]:
        return [seed]

    class Example:
        seed: int = initvar(default=7)
        scratch: list[int] | None = transient(
            tx_key="audit",
            default=None,
            working_default_factory=working_factory,
        )

    harvested = harvest_lifecycle_definition(Example)
    scratch = next(
        fact for fact in harvested.field_facts if fact["field_name"] == "scratch"
    )

    assert scratch["field_kind"] == "transient"
    assert scratch["tx_key_key"] == "audit"
    assert scratch["current_slot_name"] == "_y_scratch_current"
    assert scratch["working_slot_name"] == "_y_scratch_working"
    assert scratch["has_working_default_factory"] is True
    assert scratch["working_default_factory"] is working_factory
    assert scratch["working_default_factory_param_names"] == ("seed",)
    assert (
        harvested.build_kwargs["_Example_scratch_working_default_factory"]
        is working_factory
    )
    assert harvested.tx_keys == (DEFAULT_TRANSACTION, "audit")


def test_marker_rejects_default_and_default_factory() -> None:
    with pytest.raises(
        LifecycleDefinitionError, match="both default and default_factory"
    ):
        field(default=1, default_factory=int)


def test_marker_rejects_non_callable_default_factory() -> None:
    with pytest.raises(
        LifecycleDefinitionError, match="default_factory must be callable"
    ):
        managed(default_factory=1)


def test_transient_marker_rejects_non_callable_working_default_factory() -> None:
    with pytest.raises(
        LifecycleDefinitionError,
        match="working_default_factory must be callable",
    ):
        transient(working_default_factory=1)


def test_managed_marker_rejects_non_callable_conversions() -> None:
    with pytest.raises(LifecycleDefinitionError, match="freeze must be callable"):
        managed(freeze=1)  # type: ignore[arg-type]

    with pytest.raises(LifecycleDefinitionError, match="thaw must be callable"):
        managed(thaw=1)  # type: ignore[arg-type]


def test_marker_rejects_non_bool_init() -> None:
    with pytest.raises(LifecycleDefinitionError, match="init must be a bool"):
        field(init=1)  # type: ignore[arg-type]


def test_normalize_rejects_reserved_names() -> None:
    with pytest.raises(LifecycleDefinitionError, match="Counter._y_state"):
        normalize_marker("_y_state", int, field(), context="Counter")

    with pytest.raises(LifecycleDefinitionError, match="Counter.__yidl_data__"):
        normalize_marker("__yidl_data__", int, field(), context="Counter")
