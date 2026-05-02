"""Compatibility facade for YIDL data-definition schema primitives."""

from __future__ import annotations

from yidl.generation import data_schema as _data_schema
from yidl.generation.data_schema import *  # noqa: F403
from yidl.generation.data_schema import _emit_record_class_source
from yidl.generation.data_schema import DataDefinitionSystem as _SchemaDataDefinitionSystem
from yidl.generation.matcher import *  # noqa: F403
from yidl.generation.matcher import MatcherSpec
from yidl.generation import matcher as _matcher


class DataDefinitionSystem(_SchemaDataDefinitionSystem):
    """Full generation data-definition facade."""

    __slots__ = ("_matchers",)

    def __init__(self) -> None:
        super().__init__()
        self._matchers: dict[str, MatcherSpec] = {}

    @property
    def matchers(self) -> tuple[MatcherSpec, ...]:
        return tuple(self._matchers.values())

    def matcher(self, name: str) -> MatcherSpec:
        if name in self._matchers:
            raise ValueError(f"matcher {name!r} is already defined")
        spec = MatcherSpec(name, system=self)
        self._matchers[name] = spec
        return spec


__all__ = [
    *_data_schema.__all__,
    *_matcher.__all__,
    "DataDefinitionSystem",
    "_emit_record_class_source",
]
