"""DDS-native capsule definition primitives.

This module is the first replacement layer for the original experimental
capsule builder.  A capsule is a named set of contributors that extend a
``DataDefinitionSystem``.  Code generation remains downstream: this layer only
owns definition composition and generated DDS runtime loading.
"""

from __future__ import annotations

from collections.abc import Callable, Mapping, Sequence
from dataclasses import dataclass
from types import MappingProxyType
from typing import Any

from yidl.generation.data_def_sys import DataDefinitionSystem
from yidl.generation.data_def_sys import SourceNameMap


CapsuleContributor = Callable[[DataDefinitionSystem], object]


@dataclass(frozen=True, slots=True)
class CapsuleConcept:
    """A named contributor that introduces or extends DDS concepts."""

    name: str
    contributor: CapsuleContributor

    def __post_init__(self) -> None:
        if not self.name:
            raise ValueError("capsule concept name must not be empty")
        if not callable(self.contributor):
            raise TypeError("capsule concept contributor must be callable")

    def apply(self, dds: DataDefinitionSystem) -> None:
        self.contributor(dds)


@dataclass(frozen=True, slots=True)
class CapsuleDefinition:
    """A composable DDS-backed capsule definition."""

    name: str
    concepts: tuple[CapsuleConcept, ...] = ()

    def __post_init__(self) -> None:
        if not self.name:
            raise ValueError("capsule definition name must not be empty")

    @classmethod
    def define(
        cls,
        name: str,
        *concepts: CapsuleConcept | CapsuleContributor,
    ) -> CapsuleDefinition:
        return cls(name=name).extend(*concepts)

    def extend(
        self,
        *concepts: CapsuleConcept | CapsuleContributor,
    ) -> CapsuleDefinition:
        return CapsuleDefinition(
            name=self.name,
            concepts=(
                *self.concepts,
                *(_coerce_concept(concept) for concept in concepts),
            ),
        )

    @property
    def concept_names(self) -> tuple[str, ...]:
        return tuple(concept.name for concept in self.concepts)

    def build_data_definition(self) -> DataDefinitionSystem:
        dds = DataDefinitionSystem()
        for concept in self.concepts:
            concept.apply(dds)
        return dds

    def emit_runtime_source(
        self,
        *,
        evaluator_names: SourceNameMap = (),
        value_names: SourceNameMap = (),
    ) -> str:
        return self.build_data_definition().emit_container_runtime_source(
            evaluator_names=evaluator_names,
            value_names=value_names,
        )

    def load_runtime(
        self,
        *,
        evaluator_names: SourceNameMap = (),
        value_names: SourceNameMap = (),
        runtime_globals: Mapping[str, object] | None = None,
    ) -> CapsuleRuntime:
        source = self.emit_runtime_source(
            evaluator_names=evaluator_names,
            value_names=value_names,
        )
        namespace: dict[str, object] = dict(runtime_globals or {})
        exec(compile(source, f"<yidl.capsule.{self.name}>", "exec"), namespace)
        return CapsuleRuntime(
            definition=self,
            source=source,
            namespace=MappingProxyType(namespace),
        )


@dataclass(frozen=True, slots=True)
class CapsuleRuntime:
    """Loaded generated DDS runtime for a capsule definition."""

    definition: CapsuleDefinition
    source: str
    namespace: Mapping[str, object]

    def __getitem__(self, name: str) -> object:
        return self.namespace[name]

    def get(self, name: str, default: Any = None) -> object:
        return self.namespace.get(name, default)

    def new_builder(self) -> object:
        builder_factory = self.namespace["new_builder"]
        if not callable(builder_factory):
            raise TypeError("generated runtime new_builder is not callable")
        return builder_factory()

    def build_container(self, builder: object) -> object:
        build_container = self.namespace["build_container"]
        if not callable(build_container):
            raise TypeError("generated runtime build_container is not callable")
        return build_container(builder)


def concept(name: str, contributor: CapsuleContributor) -> CapsuleConcept:
    """Name a DDS contributor for use in capsule definitions."""

    return CapsuleConcept(name=name, contributor=contributor)


def capsule(
    name: str,
    *concepts: CapsuleConcept | CapsuleContributor,
) -> CapsuleDefinition:
    """Create a DDS-backed capsule definition."""

    return CapsuleDefinition.define(name, *concepts)


def _coerce_concept(
    concept_or_contributor: CapsuleConcept | CapsuleContributor,
) -> CapsuleConcept:
    if isinstance(concept_or_contributor, CapsuleConcept):
        return concept_or_contributor
    if not callable(concept_or_contributor):
        raise TypeError(
            "capsule concepts must be CapsuleConcept or callable contributors"
        )
    return CapsuleConcept(
        name=getattr(
            concept_or_contributor,
            "__name__",
            type(concept_or_contributor).__name__,
        ),
        contributor=concept_or_contributor,
    )


__all__ = [
    "CapsuleConcept",
    "CapsuleContributor",
    "CapsuleDefinition",
    "CapsuleRuntime",
    "capsule",
    "concept",
]
