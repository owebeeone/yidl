"""Runtime helpers for evaluating YIDL assembly values."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from itertools import product
import keyword
from typing import cast

import astichi
from astichi.assembler.scope import AssemblyScope
from astichi.assembler.scope import as_composable
from astichi.assembler.scope import as_external_value
from astichi.assembler.scope import as_identifier
from astichi.assembler.scope import find_candidates
from astichi.assembler.scope import require_one
from astichi.pathmatch import parse_path_selector

from yidl.generation.assembly_plan import AndConditionSpec
from yidl.generation.assembly_plan import AssemblyConditionSpec
from yidl.generation.assembly_plan import AssemblyEdgeSpec
from yidl.generation.assembly_plan import AssemblyValueRef
from yidl.generation.assembly_plan import BindingSpec
from yidl.generation.assembly_plan import ComposableProductionSpec
from yidl.generation.assembly_plan import ContributionMatcherSpec
from yidl.generation.assembly_plan import ContributionSpec
from yidl.generation.assembly_plan import EdgeApplySpec
from yidl.generation.assembly_plan import EqConditionSpec
from yidl.generation.assembly_plan import InlineApplySpec
from yidl.generation.assembly_plan import LiteralValueRef
from yidl.generation.assembly_plan import PathSpec
from yidl.generation.assembly_plan import TargetPathSpec
from yidl.generation.assembly_plan import TupleValueRef
from yidl.generation.assembly_plan import ValueRef


_MISSING = object()
_PATH_OPERATOR_TEXT = {
    "current": ".",
    "optional": "?",
    "any": "*",
    "many": "+",
}


class Undefined(NameError):
    """Raised when an assembly value is not visible in the current stack."""


class AssemblyPathError(ValueError):
    """Raised when an assembly path selector cannot be rendered or parsed."""


@dataclass(frozen=True, slots=True)
class DataStack:
    """Stack of record values visible to one assembly scope."""

    value_dicts: tuple[Mapping[str, object], ...] = ()
    parent: DataStack | None = None

    def push(self, *value_dicts: Mapping[str, object]) -> DataStack:
        """Return a child stack that searches ``value_dicts`` before this stack."""

        return DataStack(value_dicts=tuple(value_dicts), parent=self)

    def get(self, name: str) -> object:
        """Return the first visible value named ``name``."""

        for values in self.value_dicts:
            value = values.get(name, _MISSING)
            if value is not _MISSING:
                return value
        if self.parent is not None:
            return self.parent.get(name)
        raise Undefined(name)

    def get_mapping(self, name: str) -> Mapping[str, object]:
        value = self.get(name)
        if not isinstance(value, Mapping):
            raise TypeError(f"{name} must be a mapping")
        return cast(Mapping[str, object], value)

    def get_string(self, name: str) -> str:
        value = self.get(name)
        if not isinstance(value, str):
            raise TypeError(f"{name} must be a string")
        return value

    def get_integer(self, name: str) -> int:
        value = self.get(name)
        if not isinstance(value, int):
            raise TypeError(f"{name} must be an integer")
        return value


def evaluate_value(value: AssemblyValueRef, stack: DataStack) -> object:
    """Evaluate an assembly value reference against ``stack``."""

    if isinstance(value, ValueRef):
        return stack.get(value.name)
    if isinstance(value, LiteralValueRef):
        return value.value
    if isinstance(value, TupleValueRef):
        return tuple(evaluate_value(item, stack) for item in value.items)
    raise TypeError(f"unsupported assembly value: {type(value).__name__}")


def evaluate_index(
    value: AssemblyValueRef | None,
    stack: DataStack,
) -> int | tuple[int, ...] | None:
    """Evaluate a contribution build index."""

    if value is None:
        return None
    result = evaluate_value(value, stack)
    if isinstance(result, int):
        return result
    if isinstance(result, tuple) and all(isinstance(item, int) for item in result):
        return result
    raise TypeError("index must evaluate to int, tuple[int, ...], or None")


def evaluate_order(value: AssemblyValueRef, stack: DataStack) -> int:
    """Evaluate a contribution insertion order."""

    result = evaluate_value(value, stack)
    if not isinstance(result, int):
        raise TypeError("order must evaluate to int")
    return result


def evaluate_path_index(value: AssemblyValueRef, stack: DataStack) -> int:
    """Evaluate one path-index element."""

    result = evaluate_value(value, stack)
    if not isinstance(result, int):
        raise TypeError("path index must evaluate to int")
    return result


def evaluate_identifier(value: AssemblyValueRef, stack: DataStack) -> str:
    """Evaluate an identifier binding value."""

    result = evaluate_value(value, stack)
    if not isinstance(result, str) or not result.isidentifier() or keyword.iskeyword(result):
        raise TypeError("identifier binding must evaluate to a valid Python identifier")
    return result


def evaluate_external(value: AssemblyValueRef, stack: DataStack) -> object:
    """Evaluate an external Astichi binding value."""

    return evaluate_value(value, stack)


def evaluate_condition(condition: AssemblyConditionSpec, stack: DataStack) -> bool:
    """Evaluate an assembly condition against ``stack``."""

    if isinstance(condition, EqConditionSpec):
        return evaluate_value(condition.left, stack) == evaluate_value(
            condition.right,
            stack,
        )
    if isinstance(condition, AndConditionSpec):
        return all(evaluate_condition(item, stack) for item in condition.items)
    raise TypeError(f"unsupported assembly condition: {type(condition).__name__}")


def render_path_selector(path: PathSpec, stack: DataStack) -> str:
    """Render a structural YIDL path without its authored leading slash."""

    parts: list[str] = []
    for segment in path.segments:
        if segment.kind == "name":
            if segment.name is None:
                raise AssemblyPathError("named path segment is missing its name")
            if not segment.indexes:
                parts.append(segment.name)
                continue
            indexes = tuple(
                evaluate_path_index(index, stack)
                for index in segment.indexes
            )
            parts.append(f"{segment.name}[{','.join(str(index) for index in indexes)}]")
            continue
        operator = _PATH_OPERATOR_TEXT.get(segment.kind)
        if operator is None:
            raise AssemblyPathError(f"unsupported path segment kind {segment.kind!r}")
        parts.append(operator)
    return "/".join(parts)


def path_selector_tuple(
    path: PathSpec,
    stack: DataStack,
    *,
    context: str,
) -> tuple[str, ...]:
    """Render and parse a path selector, wrapping parser errors with context."""

    rendered = render_path_selector(path, stack)
    try:
        return parse_path_selector(rendered)
    except ValueError as exc:
        raise AssemblyPathError(f"{context}: invalid path selector {rendered!r}") from exc


def run_assembly(
    concept: object,
    entrypoint: str,
    container: object,
    *,
    unroll: bool | str = "auto",
) -> object:
    """Execute one compiled YIDL assembly entrypoint in memory."""

    assembly = concept.assemblies[entrypoint]
    production = concept.composable_productions[assembly.production_name]
    return _run_production(
        concept,
        production,
        container,
        context_records={},
        unroll=unroll,
    )


def _run_production(
    concept: object,
    production: ComposableProductionSpec,
    container: object,
    *,
    context_records: Mapping[str, object],
    unroll: bool | str,
) -> object:
    active_context_records: dict[str, object] = {}
    for input_spec in production.inputs:
        try:
            active_context_records[input_spec.name] = context_records[input_spec.name]
        except KeyError as exc:
            raise ValueError(
                f"production {production.name!r} requires input {input_spec.name!r}"
            ) from exc

    scope = AssemblyScope(astichi.build())
    root_resource = concept.resources[production.root.resource_name].to_generator()
    scope.add(production.root.build_name, root_resource)
    root_stack = DataStack(
        tuple(
            _record_mapping(concept, record)
            for record in active_context_records.values()
        )
    )
    _apply_bindings(
        scope,
        production.root.bindings,
        root_stack,
        build_match=(production.root.build_name,),
        context=f"production {production.name!r} root",
    )

    for apply in production.applies:
        edge = apply.edge if isinstance(apply, InlineApplySpec) else concept.assembly_edges[apply.edge_name]
        _run_edge(
            concept,
            edge,
            container,
            scope,
            context_records=active_context_records,
            unroll=unroll,
        )
    return scope.build(unroll=unroll)


def _run_edge(
    concept: object,
    edge: AssemblyEdgeSpec,
    container: object,
    scope: AssemblyScope,
    *,
    context_records: Mapping[str, object],
    unroll: bool | str,
) -> None:
    context_values: list[Mapping[str, object]] = []
    edge_context_records: dict[str, object] = {}
    for input_spec in edge.context_inputs:
        try:
            record = context_records[input_spec.name]
        except KeyError as exc:
            raise ValueError(
                f"assembly edge {edge.name!r} requires context input "
                f"{input_spec.name!r}"
            ) from exc
        context_values.append(_record_mapping(concept, record))
        edge_context_records[input_spec.name] = record

    from_sequences = [
        tuple(getattr(container, input_spec.collection_name).sequence())
        for input_spec in edge.from_inputs
    ]
    record_products = product(*from_sequences) if from_sequences else ((),)
    for records in record_products:
        from_records = {
            input_spec.name: record
            for input_spec, record in zip(edge.from_inputs, records, strict=True)
        }
        stack = DataStack(
            (
                *context_values,
                *(
                    _record_mapping(concept, record)
                    for record in from_records.values()
                ),
            )
        )
        if edge.condition is not None and not evaluate_condition(edge.condition, stack):
            continue
        matcher = concept.contribution_matchers[edge.matcher_name]
        contribution = _select_contribution(concept, matcher, stack)
        if contribution is None:
            continue
        _apply_contribution(
            concept,
            contribution,
            container,
            scope,
            stack,
            context_records={**edge_context_records, **from_records},
            unroll=unroll,
        )


def _select_contribution(
    concept: object,
    matcher: ContributionMatcherSpec,
    stack: DataStack,
) -> ContributionSpec | None:
    for rule in sorted(
        matcher.rules,
        key=lambda candidate: _condition_score(candidate.condition) * candidate.weight,
        reverse=True,
    ):
        if evaluate_condition(rule.condition, stack):
            return concept.contributions[rule.contribution_name]
    if matcher.default_contribution_name is None:
        return None
    return concept.contributions[matcher.default_contribution_name]


def _apply_contribution(
    concept: object,
    contribution: ContributionSpec,
    container: object,
    scope: AssemblyScope,
    stack: DataStack,
    *,
    context_records: Mapping[str, object],
    unroll: bool | str,
) -> None:
    if contribution.source_kind == "resource":
        composable = concept.resources[contribution.source_name].to_generator()
    else:
        composable = _run_production(
            concept,
            concept.composable_productions[contribution.source_name],
            container,
            context_records=context_records,
            unroll=unroll,
        )

    build_index = evaluate_index(contribution.index, stack)
    order = (
        evaluate_order(contribution.order, stack)
        if contribution.order is not None
        else 0
    )
    resource = as_composable(
        composable,
        build_name=contribution.build_name,
        build_index=build_index,
        order=order,
    )
    build_selectors = _target_selectors(
        contribution.target.paths,
        "build",
        stack,
        context=f"contribution {contribution.name!r} build",
    )
    owner_selectors = _target_selectors(
        contribution.target.paths,
        "owner",
        stack,
        context=f"contribution {contribution.name!r} owner",
    )

    concrete_build_paths: list[tuple[str, ...]] = []
    for build_match in build_selectors:
        for owner_match in owner_selectors:
            candidate = require_one(
                find_candidates(
                    scope.inventory,
                    resource,
                    name=contribution.target.name,
                    build_match=build_match,
                    owner_match=owner_match,
                )
            )
            scope.apply(candidate)
            if build_match is not None and not _selector_is_dynamic(build_match):
                concrete_build_paths.append(build_match + (resource.instance_name,))

    for build_path in concrete_build_paths:
        _apply_bindings(
            scope,
            contribution.bindings,
            stack,
            build_match=build_path,
            context=f"contribution {contribution.name!r}",
        )


def _apply_bindings(
    scope: AssemblyScope,
    bindings: tuple[BindingSpec, ...],
    stack: DataStack,
    *,
    build_match: tuple[str, ...],
    context: str,
) -> None:
    for binding in bindings:
        if binding.kind == "ident":
            resource = as_identifier(evaluate_identifier(binding.value, stack))
        else:
            resource = as_external_value(evaluate_external(binding.value, stack))
        candidate = require_one(
            find_candidates(
                scope.inventory,
                resource,
                name=binding.name,
                build_match=build_match,
            )
        )
        try:
            scope.apply(candidate)
        except ValueError as exc:
            raise ValueError(f"{context}: failed to bind {binding.name!r}") from exc


def _target_selectors(
    paths: tuple[TargetPathSpec, ...],
    kind: str,
    stack: DataStack,
    *,
    context: str,
) -> tuple[tuple[str, ...] | None, ...]:
    selectors = tuple(
        path_selector_tuple(target_path.path, stack, context=context)
        for target_path in paths
        if target_path.kind == kind
    )
    return selectors or (None,)


def _record_mapping(concept: object, record: object) -> Mapping[str, object]:
    result: dict[str, object] = {}
    for prop in concept.properties.values():
        if hasattr(record, prop.storage_name):
            result[prop.name] = getattr(record, prop.storage_name)
    return result


def _condition_score(condition: AssemblyConditionSpec) -> int:
    if isinstance(condition, AndConditionSpec):
        return sum(_condition_score(item) for item in condition.items)
    if isinstance(condition, EqConditionSpec):
        return 1
    return 0


def _selector_is_dynamic(selector: tuple[str, ...]) -> bool:
    return any(part in {".", "?", "*", "+"} for part in selector)
