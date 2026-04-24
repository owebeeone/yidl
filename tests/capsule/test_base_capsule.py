from __future__ import annotations

from yidl.capsule.base_capsule import BaseCapsule, build_base_capsule


def test_base_capsule_matches_minimal_bootstrap_shape() -> None:
    built = build_base_capsule()

    assert built == BaseCapsule
    assert [facade.name for facade in built.facades] == ["Main"]
    assert built.facades[0].default is True

    assert [prop.name for prop in built.properties] == ["Init", "Default"]
    assert built.properties[0].default is True
    assert built.specs[0].name == "base_spec"
    assert built.specs[0].property_names == ("Init", "Default")
