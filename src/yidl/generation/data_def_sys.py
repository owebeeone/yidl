"""Compatibility facade for YIDL data-definition schema primitives."""

from __future__ import annotations

from yidl.generation import data_schema as _data_schema
from yidl.generation import data_container as _data_container
from yidl.generation import matcher_values as _matcher_values
from yidl.generation import container_runtime_source as _container_runtime_source
from yidl.generation.assembly_source import emit_concept_runtime_source
from yidl.generation.container_runtime_source import *  # noqa: F403
from yidl.generation.container_runtime_source import SourceNameMap
from yidl.generation.container_runtime_source import emit_container_runtime_source
from yidl.generation.data_container import *  # noqa: F403
from yidl.generation.data_schema import *  # noqa: F403
from yidl.generation.data_schema import _emit_record_class_source
from yidl.generation.data_schema import (
    DataDefinitionSystem as _SchemaDataDefinitionSystem,
)
from yidl.generation.matcher_values import *  # noqa: F403
from yidl.generation.matcher import *  # noqa: F403
from yidl.generation.matcher import MatcherSpec
from yidl.generation import matcher as _matcher
from yidl.generation.assembly_runtime import AssemblyDiagnosticError
from yidl.generation.assembly_runtime import OperationExecutionError


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

    def ensure_matcher(self, name: str) -> MatcherSpec:
        existing = self._matchers.get(name)
        if existing is not None:
            return existing
        return self.matcher(name)

    def emit_container_runtime_source(
        self,
        *,
        evaluator_names: SourceNameMap = (),
        value_names: SourceNameMap = (),
    ) -> str:
        return emit_container_runtime_source(
            self,
            evaluator_names=evaluator_names,
            value_names=value_names,
        )


__all__ = [
    *_container_runtime_source.__all__,
    *_data_container.__all__,
    *_data_schema.__all__,
    *_matcher.__all__,
    *_matcher_values.__all__,
    "AssemblyDiagnosticError",
    "DataDefinitionSystem",
    "OperationExecutionError",
    "emit_concept_runtime_source",
    "_emit_record_class_source",
]
