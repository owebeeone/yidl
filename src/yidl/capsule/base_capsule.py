"""Prebuilt baseline YIDL capsule."""

from __future__ import annotations

from typing import TypeVar

from .core import UNSPECIFIED, YidlCapsule, build

T = TypeVar("T")


def build_base_capsule() -> YidlCapsule:
    builder = build()
    builder.facade.add.Main(default=True)
    builder.property.add.Init(bool, default=True)
    builder.property.add.Default(T, default=UNSPECIFIED)
    builder.spec.add.base_spec.Init.Default
    return builder.build()


BaseCapsule = build_base_capsule()


__all__ = [
    "BaseCapsule",
    "build_base_capsule",
]
