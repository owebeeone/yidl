"""Source emitter for YIDL assembly runtimes."""

from __future__ import annotations

import ast
from collections.abc import Mapping

from yidl.generation.assembly_plan import AndConditionSpec
from yidl.generation.assembly_plan import AssemblySpec
from yidl.generation.assembly_plan import EdgeApplySpec
from yidl.generation.assembly_plan import EqConditionSpec
from yidl.generation.assembly_plan import InlineApplySpec
from yidl.generation.assembly_plan import LiteralValueRef
from yidl.generation.assembly_plan import TupleValueRef
from yidl.generation.assembly_plan import ValueRef
from yidl.generation.container_runtime_source import emit_container_runtime_source
from yidl.generation.matcher_values import GeneratedValue
from yidl.generation.matcher_values import constructor_expr_for


def emit_concept_runtime_source(
    system: object,
    *,
    resources: Mapping[str, GeneratedValue],
    assembly_plan: object,
) -> str:
    """Emit DDS runtime source plus YIDL assembly metadata and helpers."""

    lines = [
        emit_container_runtime_source(system),
        "",
        "from types import SimpleNamespace as _YidlSimpleNamespace",
        "from yidl.generation.assembly_plan import AndConditionSpec, "
        "AssemblyEdgeSpec, AssemblyInputSpec, AssemblySpec, BindingSpec, "
        "ComposableProductionSpec, ContributionMatcherSpec, ContributionRuleSpec, "
        "ContributionSpec, EdgeApplySpec, EqConditionSpec, InlineApplySpec, "
        "LiteralValueRef, PathSegmentSpec, PathSpec, RootSpec, TargetPathSpec, "
        "TargetSpec, TupleValueRef, ValueRef",
        "from yidl.generation.assembly_runtime import run_assembly",
        "from yidl.generation.matcher_values import astichi_template, "
        "from_astichi_code, from_import",
        "",
        f"ASSEMBLY_PROPERTIES = {_properties_expr(system)}",
        f"ASSEMBLY_RESOURCES = {_resources_expr(resources)}",
        f"ASSEMBLY_CONTRIBUTIONS = {_mapping_expr(assembly_plan.contributions, _contribution_expr)}",
        f"ASSEMBLY_MATCHERS = {_mapping_expr(assembly_plan.contribution_matchers, _matcher_expr)}",
        f"ASSEMBLY_EDGES = {_mapping_expr(assembly_plan.assembly_edges, _edge_expr)}",
        f"ASSEMBLY_PRODUCTIONS = {_mapping_expr(assembly_plan.composable_productions, _production_expr)}",
        f"ASSEMBLY_ASSEMBLIES = {_mapping_expr(assembly_plan.assemblies, _assembly_expr)}",
        "",
        "ASSEMBLY_CONCEPT = _YidlSimpleNamespace(",
        "    properties=ASSEMBLY_PROPERTIES,",
        "    resources=ASSEMBLY_RESOURCES,",
        "    contributions=ASSEMBLY_CONTRIBUTIONS,",
        "    contribution_matchers=ASSEMBLY_MATCHERS,",
        "    assembly_edges=ASSEMBLY_EDGES,",
        "    composable_productions=ASSEMBLY_PRODUCTIONS,",
        "    assemblies=ASSEMBLY_ASSEMBLIES,",
        ")",
        "",
        "_YIDL_BASE_BUILD_CONTAINER = globals().get('build_container')",
        "",
        "def build_container(builder):",
        "    if _YIDL_BASE_BUILD_CONTAINER is not None:",
        "        return _YIDL_BASE_BUILD_CONTAINER(builder)",
        "    return builder.freeze()",
        "",
        "def build_assembly(entrypoint, container, *, unroll='auto'):",
        "    return run_assembly(ASSEMBLY_CONCEPT, entrypoint, container, unroll=unroll)",
    ]
    for name in assembly_plan.assemblies:
        lines.extend(
            [
                "",
                f"def build_{name}(container, *, unroll='auto'):",
                f"    return build_assembly({name!r}, container, unroll=unroll)",
            ]
        )
    return "\n".join(lines) + "\n"


def _properties_expr(system: object) -> str:
    items = []
    for prop in system.properties:
        items.append(
            f"{prop.name!r}: _YidlSimpleNamespace("
            f"name={prop.name!r}, storage_name={prop.storage_name!r})"
        )
    return "{" + ", ".join(items) + "}"


def _resources_expr(resources: Mapping[str, GeneratedValue]) -> str:
    items = []
    for name, resource in resources.items():
        items.append(f"{name!r}: {ast.unparse(constructor_expr_for(resource))}")
    return "{" + ", ".join(items) + "}"


def _mapping_expr(values: Mapping[str, object], renderer: object) -> str:
    items = [f"{name!r}: {renderer(value)}" for name, value in values.items()]
    return "{" + ", ".join(items) + "}"


def _input_expr(input_spec: object) -> str:
    return (
        "AssemblyInputSpec("
        f"name={input_spec.name!r}, "
        f"collection_name={input_spec.collection_name!r}, "
        "collection=None)"
    )


def _value_expr(value: object) -> str:
    if value is None:
        return "None"
    if isinstance(value, ValueRef):
        return f"ValueRef({value.name!r})"
    if isinstance(value, LiteralValueRef):
        return f"LiteralValueRef({value.value!r})"
    if isinstance(value, TupleValueRef):
        return f"TupleValueRef({_tuple_expr(_value_expr(item) for item in value.items)})"
    raise TypeError(f"unsupported assembly value: {type(value).__name__}")


def _condition_expr(condition: object) -> str:
    if condition is None:
        return "None"
    if isinstance(condition, EqConditionSpec):
        return (
            "EqConditionSpec("
            f"left={_value_expr(condition.left)}, "
            f"right={_value_expr(condition.right)})"
        )
    if isinstance(condition, AndConditionSpec):
        return (
            "AndConditionSpec("
            f"items={_tuple_expr(_condition_expr(item) for item in condition.items)})"
        )
    raise TypeError(f"unsupported condition: {type(condition).__name__}")


def _path_expr(path: object) -> str:
    return (
        "PathSpec("
        f"segments={_tuple_expr(_path_segment_expr(segment) for segment in path.segments)})"
    )


def _path_segment_expr(segment: object) -> str:
    return (
        "PathSegmentSpec("
        f"kind={segment.kind!r}, "
        f"name={segment.name!r}, "
        f"indexes={_tuple_expr(_value_expr(index) for index in segment.indexes)})"
    )


def _target_path_expr(target_path: object) -> str:
    return (
        "TargetPathSpec("
        f"kind={target_path.kind!r}, "
        f"path={_path_expr(target_path.path)})"
    )


def _target_expr(target: object) -> str:
    if target is None:
        return "None"
    return (
        "TargetSpec("
        f"name={target.name!r}, "
        f"paths={_tuple_expr(_target_path_expr(path) for path in target.paths)})"
    )


def _binding_expr(binding: object) -> str:
    return (
        "BindingSpec("
        f"kind={binding.kind!r}, "
        f"name={binding.name!r}, "
        f"value={_value_expr(binding.value)})"
    )


def _contribution_expr(contribution: object) -> str:
    parts = [
        f"name={contribution.name!r}",
        f"source_name={contribution.source_name!r}",
        f"source_kind={contribution.source_kind!r}",
        f"build_name={contribution.build_name!r}",
        f"index={_value_expr(contribution.index)}",
        f"order={_value_expr(contribution.order)}",
        f"target={_target_expr(contribution.target)}",
        f"bindings={_tuple_expr(_binding_expr(binding) for binding in contribution.bindings)}",
    ]
    if contribution.diagnostic:
        parts.append("diagnostic=True")
    return "ContributionSpec(" + ", ".join(parts) + ")"


def _rule_expr(rule: object) -> str:
    return (
        "ContributionRuleSpec("
        f"name={rule.name!r}, "
        f"condition={_condition_expr(rule.condition)}, "
        f"contribution_name={rule.contribution_name!r}, "
        f"weight={rule.weight!r})"
    )


def _matcher_expr(matcher: object) -> str:
    return (
        "ContributionMatcherSpec("
        f"name={matcher.name!r}, "
        f"inputs={_tuple_expr(_input_expr(input_spec) for input_spec in matcher.inputs)}, "
        f"default_contribution_name={matcher.default_contribution_name!r}, "
        f"rules={_tuple_expr(_rule_expr(rule) for rule in matcher.rules)})"
    )


def _edge_expr(edge: object) -> str:
    return (
        "AssemblyEdgeSpec("
        f"name={edge.name!r}, "
        f"context_inputs={_tuple_expr(_input_expr(input_spec) for input_spec in edge.context_inputs)}, "
        f"from_inputs={_tuple_expr(_input_expr(input_spec) for input_spec in edge.from_inputs)}, "
        f"condition={_condition_expr(edge.condition)}, "
        f"matcher_name={edge.matcher_name!r})"
    )


def _root_expr(root: object) -> str:
    return (
        "RootSpec("
        f"build_name={root.build_name!r}, "
        f"resource_name={root.resource_name!r}, "
        f"bindings={_tuple_expr(_binding_expr(binding) for binding in root.bindings)})"
    )


def _apply_expr(apply: object) -> str:
    if isinstance(apply, InlineApplySpec):
        return f"InlineApplySpec(edge={_edge_expr(apply.edge)})"
    if isinstance(apply, EdgeApplySpec):
        return f"EdgeApplySpec(edge_name={apply.edge_name!r})"
    raise TypeError(f"unsupported apply: {type(apply).__name__}")


def _production_expr(production: object) -> str:
    return (
        "ComposableProductionSpec("
        f"name={production.name!r}, "
        f"inputs={_tuple_expr(_input_expr(input_spec) for input_spec in production.inputs)}, "
        f"root={_root_expr(production.root)}, "
        f"applies={_tuple_expr(_apply_expr(apply) for apply in production.applies)})"
    )


def _assembly_expr(assembly: AssemblySpec) -> str:
    return (
        "AssemblySpec("
        f"name={assembly.name!r}, "
        f"production_name={assembly.production_name!r})"
    )


def _tuple_expr(items: object) -> str:
    values = tuple(items)
    if not values:
        return "()"
    if len(values) == 1:
        return f"({values[0]},)"
    return "(" + ", ".join(values) + ")"
