"""Parsed YIDL assembly plan structures.

This module is intentionally declarative.  The Lark compiler lowers Update A
syntax into these immutable specs before any Astichi builder execution exists.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal


ValueBindKind = Literal["ident", "external"]
TargetPathKind = Literal["build", "owner"]
PathSegmentKind = Literal["name", "current", "optional", "any", "many"]


@dataclass(frozen=True, slots=True)
class ValueRef:
    name: str


@dataclass(frozen=True, slots=True)
class LiteralValueRef:
    value: object


@dataclass(frozen=True, slots=True)
class TupleValueRef:
    items: tuple[AssemblyValueRef, ...]


AssemblyValueRef = ValueRef | LiteralValueRef | TupleValueRef


@dataclass(frozen=True, slots=True)
class EqConditionSpec:
    left: AssemblyValueRef
    right: AssemblyValueRef


@dataclass(frozen=True, slots=True)
class AndConditionSpec:
    items: tuple[AssemblyConditionSpec, ...]


AssemblyConditionSpec = EqConditionSpec | AndConditionSpec


@dataclass(frozen=True, slots=True)
class AssemblyInputSpec:
    name: str
    collection_name: str
    collection: object


@dataclass(frozen=True, slots=True)
class PathSegmentSpec:
    kind: PathSegmentKind
    name: str | None = None
    indexes: tuple[AssemblyValueRef, ...] = ()


@dataclass(frozen=True, slots=True)
class PathSpec:
    segments: tuple[PathSegmentSpec, ...]


@dataclass(frozen=True, slots=True)
class TargetPathSpec:
    kind: TargetPathKind
    path: PathSpec


@dataclass(frozen=True, slots=True)
class TargetSpec:
    name: str
    paths: tuple[TargetPathSpec, ...]


@dataclass(frozen=True, slots=True)
class BindingSpec:
    kind: ValueBindKind
    name: str
    value: AssemblyValueRef


@dataclass(frozen=True, slots=True)
class ContributionSpec:
    name: str
    source_name: str
    source_kind: Literal["resource", "production"]
    build_name: str
    index: AssemblyValueRef | None
    order: AssemblyValueRef | None
    target: TargetSpec | None
    bindings: tuple[BindingSpec, ...]
    diagnostic: bool = False


@dataclass(frozen=True, slots=True)
class ContributionRuleSpec:
    name: str
    condition: AssemblyConditionSpec
    contribution_name: str
    weight: float


@dataclass(frozen=True, slots=True)
class ContributionMatcherSpec:
    name: str
    inputs: tuple[AssemblyInputSpec, ...]
    default_contribution_name: str | None
    rules: tuple[ContributionRuleSpec, ...]


@dataclass(frozen=True, slots=True)
class OperationRuleSpec:
    name: str
    condition: AssemblyConditionSpec
    resource_name: str
    weight: float


@dataclass(frozen=True, slots=True)
class OperationMatcherSpec:
    name: str
    inputs: tuple[AssemblyInputSpec, ...]
    default_resource_name: str | None
    rules: tuple[OperationRuleSpec, ...]


@dataclass(frozen=True, slots=True)
class AssemblyEdgeSpec:
    name: str
    context_inputs: tuple[AssemblyInputSpec, ...]
    from_inputs: tuple[AssemblyInputSpec, ...]
    condition: AssemblyConditionSpec | None
    matcher_name: str


@dataclass(frozen=True, slots=True)
class RootSpec:
    build_name: str
    resource_name: str
    bindings: tuple[BindingSpec, ...]


@dataclass(frozen=True, slots=True)
class InlineApplySpec:
    edge: AssemblyEdgeSpec


@dataclass(frozen=True, slots=True)
class EdgeApplySpec:
    edge_name: str


ApplySpec = InlineApplySpec | EdgeApplySpec


@dataclass(frozen=True, slots=True)
class ComposableProductionSpec:
    name: str
    inputs: tuple[AssemblyInputSpec, ...]
    root: RootSpec
    applies: tuple[ApplySpec, ...]


@dataclass(frozen=True, slots=True)
class AssemblySpec:
    name: str
    production_name: str
