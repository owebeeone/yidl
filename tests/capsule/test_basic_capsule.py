from __future__ import annotations

from dataclasses import is_dataclass
from typing import TypeVar

import yidl.capsule as capsule

T = TypeVar("T")


def test_builder_creates_base_capsule() -> None:
    builder = capsule.build()
    builder.facade.add.Main(default=True)
    builder.property.add.Init(bool, default=True)
    builder.property.add.Default(T, default=capsule.UNSPECIFIED)
    builder.spec.add.base_spec.Init.Default

    base_capsule = builder.build()

    assert isinstance(base_capsule, capsule.YidlCapsule)
    assert is_dataclass(base_capsule)
    assert base_capsule.__dataclass_params__.frozen is True

    assert [facade.name for facade in base_capsule.facades] == ["Main"]
    assert base_capsule.facades[0].default is True

    assert [prop.name for prop in base_capsule.properties] == ["Init", "Default"]
    assert base_capsule.properties[0].value_type is bool
    assert base_capsule.properties[0].default is True
    assert base_capsule.properties[1].value_type is T
    assert base_capsule.properties[1].default is capsule.UNSPECIFIED

    assert [spec.name for spec in base_capsule.specs] == ["base_spec"]
    assert base_capsule.specs[0].property_names == ("Init", "Default")
