from __future__ import annotations

import pickle

import pytest

from yidl.sentinel_maker import SentinelNamespace
from yidl.sentinel_maker import make_sentinel
from yidl.sentinel_maker import sentinels


def test_attribute_namespace_returns_stable_sentinel() -> None:
    assert sentinels.MISSING is sentinels.MISSING
    assert repr(sentinels.MISSING) == "MISSING"


def test_different_names_create_different_sentinels() -> None:
    assert sentinels.MISSING is not sentinels.DELETED


def test_pickle_roundtrip_preserves_identity() -> None:
    missing = sentinels.MISSING

    assert pickle.loads(pickle.dumps(missing)) is missing


def test_make_sentinel_uses_module_name_in_identity() -> None:
    left = make_sentinel("MISSING", module_name="left")
    right = make_sentinel("MISSING", module_name="right")

    assert left is make_sentinel("MISSING", module_name="left")
    assert left is not right


def test_custom_namespace_uses_its_module_name() -> None:
    namespace = SentinelNamespace("custom.module")

    assert namespace.MISSING is make_sentinel(
        "MISSING",
        module_name="custom.module",
    )


def test_rejects_invalid_names() -> None:
    with pytest.raises(ValueError, match="must not be empty"):
        make_sentinel("")
