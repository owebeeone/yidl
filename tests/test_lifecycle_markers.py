from __future__ import annotations

import pytest

from yidl.runtime.lifecycle import LifecycleDefinitionError
from yidl.runtime.lifecycle import MISSING
from yidl.runtime.lifecycle import _HAS_DEFAULT_FACTORY
from yidl.runtime.lifecycle import classvar
from yidl.runtime.lifecycle import field
from yidl.runtime.lifecycle import initvar
from yidl.runtime.lifecycle import managed
from yidl.runtime.lifecycle import normalize_marker
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
    assert decl.tx_group == DEFAULT_TRANSACTION
    assert decl.default == 1


def test_managed_marker_accepts_positional_transaction_group() -> None:
    decl = normalize_marker("audit_count", int, managed("audit", default=10))

    assert decl.kind == "managed"
    assert decl.tx_group == "audit"
    assert decl.default == 10


def test_managed_marker_accepts_keyword_transaction_group() -> None:
    decl = normalize_marker(
        "audit_count",
        int,
        managed(tx_group="audit", default=10),
    )

    assert decl.tx_group == "audit"


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


def test_marker_rejects_default_and_default_factory() -> None:
    with pytest.raises(LifecycleDefinitionError, match="both default and default_factory"):
        field(default=1, default_factory=int)


def test_marker_rejects_non_callable_default_factory() -> None:
    with pytest.raises(LifecycleDefinitionError, match="default_factory must be callable"):
        managed(default_factory=1)


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
