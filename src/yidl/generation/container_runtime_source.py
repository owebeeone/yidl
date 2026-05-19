"""Source emission for decorator-time DDS container modules."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
import textwrap

import astichi

from yidl.generation.matcher import build_matcher_runtime_composable
from yidl.generation.data_schema import CollectionSpec
from yidl.generation.data_schema import ComputedValue
from yidl.generation.data_schema import ComputedCollectionSpec
from yidl.generation.data_schema import DataDefinitionSystem
from yidl.generation.data_schema import LiteralValue
from yidl.generation.data_schema import LookupValue
from yidl.generation.data_schema import MatchRecordProperty
from yidl.generation.data_schema import MatcherResultSource
from yidl.generation.data_schema import MatchResource
from yidl.generation.data_schema import MatchTupleValue
from yidl.generation.data_schema import OrderedCollectionSource
from yidl.generation.data_schema import OperationMatcherDispatch
from yidl.generation.data_schema import OperationSpec
from yidl.generation.data_schema import PortAddress
from yidl.generation.data_schema import PropertySpec
from yidl.generation.data_schema import REQUIRED
from yidl.generation.data_schema import ReadProperty
from yidl.generation.data_schema import RecordSpec
from yidl.generation.data_schema import ProductionSpec
from yidl.generation.data_schema import UnionSpec
from yidl.generation.data_schema import _NO_LOOKUP_DEFAULT
from yidl.generation.matcher import MatcherSpec
from yidl.generation.matcher import NOT_PROVIDED
from yidl.generation.assembly_plan import AndConditionSpec
from yidl.generation.assembly_plan import AssemblyConditionSpec
from yidl.generation.assembly_plan import AssemblyValueRef
from yidl.generation.assembly_plan import EqConditionSpec
from yidl.generation.assembly_plan import LiteralValueRef
from yidl.generation.assembly_plan import OperationMatcherSpec
from yidl.generation.assembly_plan import TupleValueRef
from yidl.generation.assembly_plan import ValueRef
from yidl.generation.matcher_values import render_value_constructor
from yidl.generation.matcher_values import GeneratedValue
from yidl.generation.matcher_values import generated_value_constructor_names
from yidl.generation.matcher_values import generated_value_uses_astichi_template
from yidl.generation.matcher_values import is_generated_value

SourceNameMap = Mapping[object, str] | Sequence[tuple[object, str]]


def emit_container_runtime_source(
    system: DataDefinitionSystem,
    *,
    evaluator_names: SourceNameMap = (),
    operation_matchers: Mapping[str, OperationMatcherSpec] = (),
    resources: Mapping[str, GeneratedValue] = (),
    value_names: SourceNameMap = (),
) -> str:
    """Emit a Python module containing DDS records, collections, and matchers."""

    generated_value_import_names = _system_generated_value_import_names(system)
    uses_astichi_templates = _system_uses_astichi_templates(system)
    uses_operations = bool(system.operations)
    uses_operation_dispatch = any(
        isinstance(operation.resource, OperationMatcherDispatch)
        for operation in system.operations
    )
    lines: list[str] = [
        _pyimport_prefix(
            generated_value_import_names,
            uses_astichi_templates,
            uses_operations,
            uses_operation_dispatch,
        )
    ]
    prop_vars = _property_vars(system)
    record_vars: dict[RecordSpec, str] = {}
    union_vars: dict[UnionSpec, str] = {}
    collection_vars: dict[CollectionSpec | ComputedCollectionSpec, str] = {}
    port_vars = _port_vars(system)

    for prop in system.properties:
        lines.append(
            f"{prop_vars[prop]} = RuntimeProperty("
            f"{prop.name!r}, "
            f"{_type_expr(prop.value_type)}, "
            f"default={_value_expr(prop.default, value_names, 'property default')}, "
            f"storage_name={prop.storage_name!r}"
            ")"
        )
    if system.properties:
        lines.append("")

    for record in system.records:
        record_var = _record_var(record)
        record_vars[record] = record_var
        lines.append(
            f"{record_var} = RuntimeRecord("
            f"{record.name!r}, "
            f"{_tuple_expr(prop_vars[prop] for prop in record.properties)}"
            ")"
        )
    if system.records:
        lines.append("")

    for union in system.unions:
        union_var = _union_var(union)
        union_vars[union] = union_var
        lines.append(
            f"{union_var} = RuntimeUnion("
            f"{union.name!r}, "
            f"{_tuple_expr(record_vars[variant] for variant in union.variants)}"
            ")"
        )
    if system.unions:
        lines.append("")

    for record in system.records:
        lines.extend(_emit_record_class_lines(record, record_vars[record], value_names))
        lines.append(f"{record_vars[record]}.bind_record_class({record.name})")
        lines.append("")

    for collection in system.collections:
        collection_var = _collection_var(collection)
        collection_vars[collection] = collection_var
        record_expr = _record_shape_expr(
            collection.record_shape, record_vars, union_vars
        )
        identity_expr = (
            "None"
            if collection.identity is None
            else _identity_expr(collection.identity, prop_vars)
        )
        cardinality_expr = (
            "True" if collection.cardinality.allows_multiple() else "False"
        )
        lines.append(
            f"{collection_var} = RuntimeCollection("
            f"{collection.name!r}, "
            f"{record_expr}, "
            f"allows_multiple={cardinality_expr}, "
            f"identity={identity_expr}"
            ")"
        )
    if system.collections:
        lines.append("")

    for collection in system.computed_collections:
        collection_var = _collection_var(collection)
        collection_vars[collection] = collection_var
        lines.append(
            f"{collection_var} = RuntimeComputedCollection("
            f"{collection.name!r}, "
            f"source={collection_vars[collection.source]}, "
            f"when={_conditions_expr(collection.conditions, prop_vars, value_names)}"
            ")"
        )
    if system.computed_collections:
        lines.append("")

    for port in system.ports:
        lines.append(
            f"{port_vars[port]} = RuntimePort("
            f"{port.name!r}, "
            f"allows_multiple={port.cardinality.allows_multiple()!r}"
            ")"
        )
    if system.ports:
        lines.append("")

    port_index = system.port_index_spec
    port_index_expr = (
        "None"
        if port_index is None
        else "RuntimePortIndex("
        f"target={prop_vars[port_index.target]}, "
        f"order={prop_vars[port_index.order]}"
        ")"
    )
    lines.append(
        "_RUNTIME_SPEC = RuntimeContainerSpec("
        f"collections={_tuple_expr(collection_vars[collection] for collection in system.collections)}, "
        f"computed_collections={_tuple_expr(collection_vars[collection] for collection in system.computed_collections)}, "
        f"ports={_tuple_expr(port_vars[port] for port in system.ports)}, "
        f"port_index={port_index_expr}"
        ")"
    )
    lines.append("")

    matchers = _system_matchers(system)
    if matchers:
        lines.append("astichi_hole(matcher_definitions)")
        lines.append("")

    for production in system.productions:
        lines.extend(
            _emit_production_lines(
                production,
                collection_vars=collection_vars,
                prop_vars=prop_vars,
                port_vars=port_vars,
                evaluator_names=evaluator_names,
                value_names=value_names,
            )
        )
        lines.append("")
    for order, operation in enumerate(system.operations):
        lines.extend(
            _emit_aggregate_operation_lines(
                operation,
                operation_index=order,
                collection_vars=collection_vars,
                operation_matchers=operation_matchers,
                prop_vars=prop_vars,
                resources=resources,
            )
        )
        lines.append("")
    if system.productions or system.operations:
        lines.extend(_emit_operation_runner_lines(system))
        lines.append("")

    lines.extend(_emit_container_builder_lines(matchers))
    return _materialize_container_module(
        "\n".join(lines).rstrip() + "\n",
        system=system,
        matchers=matchers,
        evaluator_names=evaluator_names,
        value_names=value_names,
        operation_matchers=operation_matchers,
        resources=resources,
    )


def _materialize_container_module(
    source: str,
    *,
    system: DataDefinitionSystem,
    matchers: Sequence[MatcherSpec],
    evaluator_names: SourceNameMap,
    operation_matchers: Mapping[str, OperationMatcherSpec],
    resources: Mapping[str, GeneratedValue],
    value_names: SourceNameMap,
) -> str:
    root = astichi.compile(
        source,
        keep_names=_container_keep_names(
            system,
            matchers,
            evaluator_names,
            operation_matchers,
            resources,
            value_names,
        ),
    )
    if not matchers and not system.operations:
        return root.materialize().emit(provenance=False)

    builder = astichi.build()
    builder.add.Root(root)
    for order, matcher in enumerate(matchers):
        builder.add.Matcher[order](
            build_matcher_runtime_composable(
                matcher,
                class_name=_matcher_runtime_class_name(matcher),
                evaluator_names=evaluator_names,
                value_names=value_names,
            )
        )
        builder.Root.matcher_definitions.add.Matcher[order](order=order)
    body_order = 0
    for order, operation in enumerate(system.operations):
        if isinstance(operation.resource, OperationMatcherDispatch):
            for body_index, _, resource in _operation_matcher_body_resources(
                operation,
                operation_matchers=operation_matchers,
                resources=resources,
            ):
                builder.add.OperationBody[body_order](resource.to_generator())
                getattr(
                    builder.Root,
                    _operation_matcher_body_hole(order, body_index),
                ).add.OperationBody[body_order](order=body_order)
                body_order += 1
            continue
        if not is_generated_value(operation.resource):
            raise TypeError(
                f"operation {operation.name!r} resource must be a generated value"
            )
        builder.add.OperationBody[body_order](operation.resource.to_generator())
        getattr(builder.Root, _operation_body_hole(order)).add.OperationBody[
            body_order
        ](order=body_order)
        body_order += 1
    return builder.build().materialize().emit(provenance=False)


def _container_keep_names(
    system: DataDefinitionSystem,
    matchers: Sequence[MatcherSpec],
    evaluator_names: SourceNameMap,
    operation_matchers: Mapping[str, OperationMatcherSpec],
    resources: Mapping[str, GeneratedValue],
    value_names: SourceNameMap,
) -> tuple[str, ...]:
    generated_value_import_names = _system_generated_value_import_names(system)
    uses_astichi_templates = _system_uses_astichi_templates(system)
    uses_operations = bool(system.operations)
    uses_operation_dispatch = any(
        isinstance(operation.resource, OperationMatcherDispatch)
        for operation in system.operations
    )
    return tuple(
        dict.fromkeys(
            (
                *_runtime_import_names(
                    generated_value_import_names,
                    uses_astichi_templates,
                    uses_operations,
                    uses_operation_dispatch,
                ),
                *_BUILTIN_KEEP_NAMES,
                "_RUNTIME_SPEC",
                "_GeneratedMatcherNamespace",
                "_GeneratedContainerBuilder",
                "ctx",
                "new_builder",
                "run_operations",
                "build_container",
                *(_property_vars(system).values()),
                *(_record_var(record) for record in system.records),
                *(_union_var(union) for union in system.unions),
                *(_collection_var(collection) for collection in system.collections),
                *(
                    _collection_var(collection)
                    for collection in system.computed_collections
                ),
                *(_port_vars(system).values()),
                *(record.name for record in system.records),
                *(_matcher_runtime_class_name(matcher) for matcher in matchers),
                *(f"_Container{matcher.name}Matcher" for matcher in matchers),
                *(
                    _production_func_name(production)
                    for production in system.productions
                ),
                *(_operation_func_name(operation) for operation in system.operations),
                *(
                    _operation_body_func_name(
                        operation_index, body_index, resource_name
                    )
                    for operation_index, operation in enumerate(system.operations)
                    if isinstance(operation.resource, OperationMatcherDispatch)
                    for body_index, resource_name, _ in _operation_matcher_body_resources(
                        operation,
                        operation_matchers=operation_matchers,
                        resources=resources,
                    )
                ),
                *_source_name_roots(evaluator_names),
                *_source_name_roots(value_names),
            )
        )
    )


def _emit_container_builder_lines(matchers: Sequence[MatcherSpec]) -> list[str]:
    lines = [
        "class _GeneratedMatcherNamespace:",
        "    def __init__(self, container):",
    ]
    if matchers:
        lines.extend(
            f"        self.{matcher.name} = _Container{matcher.name}Matcher(container)"
            for matcher in matchers
        )
    else:
        lines.append("        pass")
    lines.append("")
    for matcher in matchers:
        lines.extend(_emit_container_matcher_lines(matcher))
        lines.append("")
    lines.extend(
        [
            "class _GeneratedContainerBuilder:",
            "    def __init__(self):",
            "        self._builder = DDSContainerBuilder(_RUNTIME_SPEC)",
            "",
            "    def add(self, *args, **kwargs):",
            "        self._builder.add(*args, **kwargs)",
            "        return self",
            "",
            "    def write(self, *args, **kwargs):",
            "        self._builder.write(*args, **kwargs)",
            "        return self",
            "",
            "    def children_at(self, port_address):",
            "        return self._builder.children_at(port_address)",
            "",
            "    def _snapshot(self):",
            "        container = self._builder._snapshot()",
            "        container.matchers = _GeneratedMatcherNamespace(container)",
            "        return container",
            "",
            "    def record(self, *args, **kwargs):",
            "        return self._builder.record(*args, **kwargs)",
            "",
            "    def freeze(self):",
            "        container = self._builder.freeze()",
            "        container.matchers = _GeneratedMatcherNamespace(container)",
            "        return container",
            "",
            "    def __getattr__(self, name):",
            "        return getattr(self._builder, name)",
            "",
            "def new_builder():",
            "    return _GeneratedContainerBuilder()",
        ]
    )
    return lines


def _emit_container_matcher_lines(matcher: MatcherSpec) -> list[str]:
    lines = [
        f"class _Container{matcher.name}Matcher:",
        "    def __init__(self, container):",
        "        self._container = container",
        f"        self._runtime = {_matcher_runtime_class_name(matcher)}()",
        "",
        "    def resolve(self, *records):",
        "        return self._runtime.resolve(*records)",
        "",
        "    def sequence(self):",
    ]
    sequence_args = ", ".join(
        f"self._container.{input_spec.source.name}.sequence()"
        for input_spec in matcher.inputs
    )
    lines.append(f"        yield from self._runtime.sequence({sequence_args})")
    return lines


def _emit_production_lines(
    production: ProductionSpec,
    *,
    collection_vars: Mapping[CollectionSpec | ComputedCollectionSpec, str],
    prop_vars: Mapping[PropertySpec, str],
    port_vars: Mapping[object, str],
    evaluator_names: SourceNameMap,
    value_names: SourceNameMap,
) -> list[str]:
    target_var = collection_vars[production.target]
    record_class = production.target.record_shape.name
    if isinstance(production.source, MatcherResultSource):
        lines = [
            f"def {_production_func_name(production)}(builder):",
            "    snapshot = builder._snapshot()",
            f"    for source in snapshot.matchers.{production.source.matcher.name}.sequence():",
        ]
    elif isinstance(production.source, OrderedCollectionSource):
        source_var = collection_vars[production.source.source]
        order_vars = ", ".join(prop_vars[prop] for prop in production.source.order_by)
        lines = [
            f"def {_production_func_name(production)}(builder):",
            f"    for source in builder.ordered_records({source_var}, {order_vars}):",
        ]
    else:
        source_var = collection_vars[production.source]
        lines = [
            f"def {_production_func_name(production)}(builder):",
            f"    for source in builder.records({source_var}):",
        ]
    if production.conditions:
        lines.extend(
            [
                f"        if not ({_condition_check_expr(production.conditions, value_names)}):",
                "            continue",
            ]
        )
    lookup_vars: dict[LookupValue, str] = {}
    for index, item in enumerate(production.values):
        if isinstance(item.expression, LookupValue):
            var_name = f"lookup_{index}"
            lookup_vars[item.expression] = var_name
            lines.extend(
                _emit_lookup_lines(
                    item.expression,
                    var_name,
                    collection_vars=collection_vars,
                    port_vars=port_vars,
                    evaluator_names=evaluator_names,
                    value_names=value_names,
                )
            )
    values = ", ".join(
        f"{item.property.storage_name}="
        f"{_value_expression_expr(item.expression, 'source', port_vars, evaluator_names, value_names, lookup_vars)}"
        for item in production.values
    )
    lines.extend(
        [
            f"        record = {record_class}({values})",
            f"        builder.write({target_var}, record, policy={production.policy.name})",
        ]
    )
    return lines


def _emit_aggregate_operation_lines(
    operation: OperationSpec,
    *,
    operation_index: int,
    collection_vars: Mapping[CollectionSpec | ComputedCollectionSpec, str],
    operation_matchers: Mapping[str, OperationMatcherSpec],
    prop_vars: Mapping[PropertySpec, str],
    resources: Mapping[str, GeneratedValue],
) -> list[str]:
    if isinstance(operation.resource, OperationMatcherDispatch):
        return _emit_matcher_operation_lines(
            operation,
            operation_index=operation_index,
            collection_vars=collection_vars,
            matcher=_operation_matcher_for(operation, operation_matchers),
            prop_vars=prop_vars,
            resources=resources,
        )
    return [
        f"def {_operation_func_name(operation)}(builder):",
        "    ctx = DDSOperationContext(",
        "        builder,",
        f"        {operation.name!r},",
        f"        ordered_inputs={_operation_ordered_inputs_expr(operation, collection_vars, prop_vars)},",
        "    )",
        f"    astichi_hole({_operation_body_hole(operation_index)})",
    ]


def _emit_matcher_operation_lines(
    operation: OperationSpec,
    *,
    operation_index: int,
    collection_vars: Mapping[CollectionSpec | ComputedCollectionSpec, str],
    matcher: OperationMatcherSpec,
    prop_vars: Mapping[PropertySpec, str],
    resources: Mapping[str, GeneratedValue],
) -> list[str]:
    dispatch = _operation_dispatch_for(operation)
    body_entries = _operation_matcher_body_resources(
        operation,
        operation_matchers={matcher.name: matcher},
        resources=resources,
    )
    body_funcs = {
        resource_name: _operation_body_func_name(
            operation_index, body_index, resource_name
        )
        for body_index, resource_name, _ in body_entries
    }
    from_var = dispatch.from_input_name
    from_collection = dispatch.from_collection
    from_collection_var = collection_vars[from_collection]
    lines: list[str] = []
    for body_index, resource_name, _ in body_entries:
        lines.extend(
            [
                f"def {_operation_body_func_name(operation_index, body_index, resource_name)}(ctx, {from_var}):",
                f"    astichi_hole({_operation_matcher_body_hole(operation_index, body_index)})",
                "",
            ]
        )

    lines.extend(
        [
            f"def {_operation_func_name(operation)}(builder):",
            "    ctx = DDSOperationContext(",
            "        builder,",
            f"        {operation.name!r},",
            f"        ordered_inputs={_operation_ordered_inputs_expr(operation, collection_vars, prop_vars)},",
            "    )",
            f"    for {from_var} in ctx.records({from_collection_var}):",
            "        try:",
        ]
    )
    sorted_rules = sorted(
        enumerate(matcher.rules),
        key=lambda item: _operation_condition_score(item[1].condition) * item[1].weight,
        reverse=True,
    )
    if not sorted_rules and matcher.default_resource_name is None:
        lines.append("            pass")
    for branch_index, (_, rule) in enumerate(sorted_rules):
        prefix = "if" if branch_index == 0 else "elif"
        lines.append(
            "            "
            f"{prefix} {_operation_condition_expr(rule.condition, from_var, from_collection)}:"
        )
        _append_operation_body_call(
            lines,
            body_funcs=body_funcs,
            from_var=from_var,
            resource_name=rule.resource_name,
        )
    if matcher.default_resource_name is not None:
        if sorted_rules:
            lines.append("            else:")
        _append_operation_body_call(
            lines,
            body_funcs=body_funcs,
            from_var=from_var,
            resource_name=matcher.default_resource_name,
        )
    elif sorted_rules:
        lines.extend(
            [
                "            else:",
                "                pass",
            ]
        )
    lines.extend(
        [
            "        except AssemblyDiagnosticError:",
            "            raise",
            "        except Exception as exc:",
            "            raise OperationExecutionError(",
            f'                "operation {operation.name!r} failed for "',
            f'                f"{from_var}={{{from_var}!r}}"',
            "            ) from exc",
        ]
    )
    return lines


def _append_operation_body_call(
    lines: list[str],
    *,
    body_funcs: Mapping[str, str],
    from_var: str,
    resource_name: str,
) -> None:
    body_func = body_funcs.get(resource_name)
    if body_func is None:
        lines.append("                pass")
        return
    lines.append(f"                {body_func}(ctx, {from_var})")


def _operation_matcher_for(
    operation: OperationSpec,
    operation_matchers: Mapping[str, OperationMatcherSpec],
) -> OperationMatcherSpec:
    dispatch = _operation_dispatch_for(operation)
    matcher = operation_matchers.get(dispatch.matcher_name)
    if matcher is None:
        raise ValueError(
            f"operation {operation.name!r} references unknown operation matcher "
            f"{dispatch.matcher_name!r}"
        )
    return matcher


def _operation_dispatch_for(operation: OperationSpec) -> OperationMatcherDispatch:
    if not isinstance(operation.resource, OperationMatcherDispatch):
        raise TypeError(f"operation {operation.name!r} is not matcher-selected")
    return operation.resource


def _operation_matcher_body_resources(
    operation: OperationSpec,
    *,
    operation_matchers: Mapping[str, OperationMatcherSpec],
    resources: Mapping[str, GeneratedValue],
) -> tuple[tuple[int, str, GeneratedValue], ...]:
    matcher = _operation_matcher_for(operation, operation_matchers)
    ordered_names: list[str] = []
    if matcher.default_resource_name is not None:
        ordered_names.append(matcher.default_resource_name)
    ordered_names.extend(rule.resource_name for rule in matcher.rules)

    entries: list[tuple[int, str, GeneratedValue]] = []
    seen: set[str] = set()
    for resource_name in ordered_names:
        if resource_name in seen:
            continue
        seen.add(resource_name)
        resource = resources.get(resource_name)
        if resource is None:
            raise ValueError(
                f"operation matcher {matcher.name!r} references unknown resource "
                f"{resource_name!r}"
            )
        if _is_empty_generated_value(resource):
            continue
        entries.append((len(entries), resource_name, resource))
    return tuple(entries)


def _is_empty_generated_value(resource: GeneratedValue) -> bool:
    source = getattr(resource, "source", None)
    if isinstance(source, str):
        return source == ""
    template = getattr(resource, "template", None)
    source = getattr(template, "source", None)
    return isinstance(source, str) and source == ""


def _operation_condition_expr(
    condition: AssemblyConditionSpec,
    from_var: str,
    from_collection: CollectionSpec | ComputedCollectionSpec,
) -> str:
    if isinstance(condition, EqConditionSpec):
        return (
            f"{_operation_value_expr(condition.left, from_var, from_collection)} == "
            f"{_operation_value_expr(condition.right, from_var, from_collection)}"
        )
    if isinstance(condition, AndConditionSpec):
        items = tuple(
            _operation_condition_expr(item, from_var, from_collection)
            for item in condition.items
        )
        if not items:
            return "True"
        return " and ".join(f"({item})" for item in items)
    raise TypeError(f"unsupported operation condition: {type(condition).__name__}")


def _operation_value_expr(
    value: AssemblyValueRef,
    from_var: str,
    from_collection: CollectionSpec | ComputedCollectionSpec,
) -> str:
    if isinstance(value, ValueRef):
        prop = _operation_property_for(from_collection, value.name)
        return f"{from_var}.{prop.storage_name}"
    if isinstance(value, LiteralValueRef):
        return repr(value.value)
    if isinstance(value, TupleValueRef):
        return _tuple_expr(
            _operation_value_expr(item, from_var, from_collection)
            for item in value.items
        )
    raise TypeError(f"unsupported operation value: {type(value).__name__}")


def _operation_property_for(
    collection: CollectionSpec | ComputedCollectionSpec,
    property_name: str,
) -> PropertySpec:
    shape = collection.record_shape
    if isinstance(shape, UnionSpec):
        for variant in shape.variants:
            for prop in variant.properties:
                if prop.name == property_name:
                    return prop
    else:
        for prop in shape.properties:
            if prop.name == property_name:
                return prop
    raise ValueError(
        f"operation matcher condition references unknown property "
        f"{property_name!r} on collection {collection.name!r}"
    )


def _operation_condition_score(condition: AssemblyConditionSpec) -> int:
    if isinstance(condition, AndConditionSpec):
        return sum(_operation_condition_score(item) for item in condition.items)
    if isinstance(condition, EqConditionSpec):
        return 1
    return 0


def _operation_ordered_inputs_expr(
    operation: OperationSpec,
    collection_vars: Mapping[CollectionSpec | ComputedCollectionSpec, str],
    prop_vars: Mapping[PropertySpec, str],
) -> str:
    if not operation.order_by:
        return "{}"
    items = [
        f"{collection_vars[collection]}: "
        f"{_tuple_expr(prop_vars[prop] for prop in operation.order_by)}"
        for collection in operation.inputs
    ]
    return "{" + ", ".join(items) + "}"


def _emit_operation_runner_lines(system: DataDefinitionSystem) -> list[str]:
    production_groups = system.production_groups
    if production_groups:
        steps = tuple(entry for group in production_groups for entry in group.entries)
    else:
        steps = (*system.productions, *system.operations)
    lines = ["def run_operations(builder):"]
    for step in steps:
        if isinstance(step, OperationSpec):
            lines.append(f"    {_operation_func_name(step)}(builder)")
        else:
            lines.append(f"    {_production_func_name(step)}(builder)")
    if not steps:
        lines.append("    pass")
    lines.extend(
        [
            "    return builder",
            "",
            "def build_container(builder):",
            "    run_operations(builder)",
            "    return builder.freeze()",
        ]
    )
    return lines


def _emit_record_class_lines(
    record: RecordSpec,
    record_var: str,
    value_names: SourceNameMap,
) -> list[str]:
    lines = [
        f"class {record.name}:",
        f"    __slots__ = {tuple(prop.storage_name for prop in record.properties)!r}",
        f"    __dds_record_spec__ = {record_var}",
    ]
    if not record.properties:
        lines.extend(
            [
                "",
                "    def __init__(self):",
                "        pass",
                "",
                "    def __repr__(self):",
                f"        return {record.name!r} + '()'",
            ]
        )
        return lines

    lines.extend(
        f"    {prop.storage_name}: {_type_expr(prop.value_type)}"
        for prop in record.properties
    )
    params = ", ".join(_param_expr(prop, value_names) for prop in record.properties)
    lines.extend(
        [
            "",
            f"    def __init__(self, *, {params}):",
        ]
    )
    for prop in record.properties:
        if prop.value_type is not object:
            lines.extend(
                [
                    f"        if not isinstance({prop.storage_name}, {_type_expr(prop.value_type)}):",
                    "            raise TypeError(",
                    f"                {prop.name + ' must be ' + _type_name(prop.value_type) + ', got '!r}",
                    f"                + type({prop.storage_name}).__name__",
                    "            )",
                ]
            )
        lines.append(
            f"        object.__setattr__(self, {prop.storage_name!r}, {prop.storage_name})"
        )
    lines.extend(
        [
            "",
            "    def __setattr__(self, name, value):",
            f"        if name in {tuple(prop.storage_name for prop in record.properties)!r}:",
            f"            raise AttributeError({record.name + ' records are immutable'!r})",
            "        object.__setattr__(self, name, value)",
            "",
            "    def __repr__(self):",
            "        pieces = []",
        ]
    )
    for prop in record.properties:
        lines.append(
            f"        pieces.append({prop.storage_name + '='!r} + repr(self.{prop.storage_name}))"
        )
    lines.append(f"        return {record.name!r} + '(' + ', '.join(pieces) + ')'")
    return lines


def _param_expr(prop: PropertySpec, value_names: SourceNameMap) -> str:
    expr = f"{prop.storage_name}: {_type_expr(prop.value_type)}"
    if prop.default is not REQUIRED:
        expr += f"={_value_expr(prop.default, value_names, 'property default')}"
    return expr


def _conditions_expr(
    conditions: Sequence[object],
    prop_vars: Mapping[PropertySpec, str],
    value_names: SourceNameMap,
) -> str:
    items = [
        f"{prop_vars[condition.property]}.eq({_value_expr(condition.value, value_names, 'condition value')})"
        for condition in conditions
    ]
    return _tuple_expr(items)


def _condition_check_expr(
    conditions: Sequence[object],
    value_names: SourceNameMap,
) -> str:
    checks = [
        f"getattr(source, {condition.property.storage_name!r}, NOT_PROVIDED) == "
        f"{_value_expr(condition.value, value_names, 'condition value')}"
        for condition in conditions
    ]
    return " and ".join(checks) if checks else "True"


def _value_expression_expr(
    expression: object,
    source_name: str,
    port_vars: Mapping[object, str],
    evaluator_names: SourceNameMap,
    value_names: SourceNameMap,
    lookup_vars: Mapping[LookupValue, str] | None = None,
) -> str:
    if isinstance(expression, LookupValue):
        if lookup_vars is None or expression not in lookup_vars:
            raise ValueError("lookup expression is not bound to a generated local")
        return f"{lookup_vars[expression]}_value"
    if isinstance(expression, ReadProperty):
        return f"{source_name}.{expression.property.storage_name}"
    if isinstance(expression, LiteralValue):
        return _literal_expr(expression.value, port_vars, value_names)
    if isinstance(expression, ComputedValue):
        helper = _source_path_for(
            expression.func,
            evaluator_names,
            f"computed value {expression.name}",
        )
        return f"{helper}({source_name})"
    if isinstance(expression, MatchResource):
        return f"{source_name}.resource"
    if isinstance(expression, MatchRecordProperty):
        if expression.input_index is None:
            raise ValueError("matcher record expression is not bound to an input")
        return (
            f"{source_name}.records[{expression.input_index}]"
            f".{expression.property.storage_name}"
        )
    if isinstance(expression, MatchTupleValue):
        return f"{source_name}.values[{expression.index}]"
    raise TypeError(f"unsupported value expression {type(expression).__name__}")


def _emit_lookup_lines(
    expression: LookupValue,
    var_name: str,
    *,
    collection_vars: Mapping[CollectionSpec | ComputedCollectionSpec, str],
    port_vars: Mapping[object, str],
    evaluator_names: SourceNameMap,
    value_names: SourceNameMap,
) -> list[str]:
    key_expr = _lookup_key_expr(
        expression.key,
        port_vars=port_vars,
        evaluator_names=evaluator_names,
        value_names=value_names,
    )
    collection_var = collection_vars[expression.collection]
    lines = [
        f"        {var_name}_key = {key_expr}",
        f"        {var_name}_record = builder.by_identity({collection_var}, {var_name}_key)",
    ]
    if expression.default is _NO_LOOKUP_DEFAULT:
        lines.extend(
            [
                f"        if {var_name}_record is None:",
                "            raise ValueError(",
                f"                'no {expression.collection.name} record for identity '",
                f"                + repr({var_name}_key)",
                "            )",
                f"        {var_name}_value = {var_name}_record.{expression.value.storage_name}",
            ]
        )
        return lines
    default_expr = _value_expression_expr(
        expression.default,
        "source",
        port_vars,
        evaluator_names,
        value_names,
    )
    lines.extend(
        [
            f"        if {var_name}_record is None:",
            f"            {var_name}_value = {default_expr}",
            "        else:",
            f"            {var_name}_value = {var_name}_record.{expression.value.storage_name}",
        ]
    )
    return lines


def _lookup_key_expr(
    key: object,
    *,
    port_vars: Mapping[object, str],
    evaluator_names: SourceNameMap,
    value_names: SourceNameMap,
) -> str:
    if isinstance(key, tuple):
        return _tuple_expr(
            _value_expression_expr(
                item,
                "source",
                port_vars,
                evaluator_names,
                value_names,
            )
            for item in key
        )
    return _value_expression_expr(
        key,
        "source",
        port_vars,
        evaluator_names,
        value_names,
    )


def _literal_expr(
    value: object,
    port_vars: Mapping[object, str],
    value_names: SourceNameMap,
) -> str:
    if isinstance(value, PortAddress):
        return (
            f"{port_vars[value.port]}.of("
            f"{_value_expr(value.owner_identity, value_names, 'port owner identity')}"
            ")"
        )
    return _value_expr(value, value_names, "literal value")


def _record_shape_expr(
    shape: RecordSpec | UnionSpec,
    record_vars: Mapping[RecordSpec, str],
    union_vars: Mapping[UnionSpec, str],
) -> str:
    if isinstance(shape, UnionSpec):
        return union_vars[shape]
    return record_vars[shape]


def _identity_expr(
    identity: PropertySpec | tuple[PropertySpec, ...],
    prop_vars: Mapping[PropertySpec, str],
) -> str:
    if isinstance(identity, tuple):
        return _tuple_expr(prop_vars[prop] for prop in identity)
    return prop_vars[identity]


def _property_vars(system: DataDefinitionSystem) -> dict[PropertySpec, str]:
    return {prop: f"_{prop.name}Property" for prop in system.properties}


def _record_var(record: RecordSpec) -> str:
    return f"_{record.name}Spec"


def _union_var(union: UnionSpec) -> str:
    return f"_{union.name}Union"


def _collection_var(collection: CollectionSpec | ComputedCollectionSpec) -> str:
    return f"{collection.name}Collection"


def _port_vars(system: DataDefinitionSystem) -> dict[object, str]:
    return {port: _port_var(port.name) for port in system.ports}


def _port_var(name: str) -> str:
    parts = [part for token in name.split(".") for part in token.split("_") if part]
    return "".join(part[:1].upper() + part[1:] for part in parts) + "Port"


def _matcher_runtime_class_name(matcher: MatcherSpec) -> str:
    return f"{matcher.name}Matcher"


def _production_func_name(production: ProductionSpec) -> str:
    return "run_" + _snake_name(production.name)


def _operation_func_name(operation: OperationSpec) -> str:
    return "run_" + _snake_name(operation.name)


def _operation_body_hole(index: int) -> str:
    return f"operation_body_{index}"


def _operation_matcher_body_hole(operation_index: int, body_index: int) -> str:
    return f"operation_body_{operation_index}_{body_index}"


def _operation_body_func_name(
    operation_index: int,
    body_index: int,
    resource_name: str,
) -> str:
    return f"_operation_{operation_index}_body_{body_index}_{_operation_resource_slug(resource_name)}"


def _operation_resource_slug(resource_name: str) -> str:
    stem = (
        resource_name[:-4]
        if resource_name.endswith("Body") and len(resource_name) > len("Body")
        else resource_name
    )
    return _snake_name(stem).strip("_") or "body"


def _snake_name(name: str) -> str:
    chars: list[str] = []
    for index, char in enumerate(name):
        if char.isupper() and index and (not name[index - 1].isupper()):
            chars.append("_")
        chars.append(char.lower() if char.isalnum() else "_")
    return "".join(chars)


def _tuple_expr(items: object) -> str:
    values = tuple(items)
    if not values:
        return "()"
    return "(" + ", ".join(values) + ("," if len(values) == 1 else "") + ")"


def _type_expr(value_type: type[object] | tuple[type[object], ...] | None) -> str:
    if value_type is None:
        return "None"
    if isinstance(value_type, tuple):
        return "(" + ", ".join(_type_expr(item) for item in value_type) + ")"
    if value_type.__module__ != "builtins":
        raise ValueError(
            f"cannot emit non-builtin value type {value_type.__module__}.{value_type.__qualname__}"
        )
    return value_type.__qualname__


def _value_expr(value: object, source_names: SourceNameMap, label: str) -> str:
    if value is REQUIRED:
        return "REQUIRED"
    if value is NOT_PROVIDED:
        return "NOT_PROVIDED"
    if is_generated_value(value):
        return render_value_constructor(value)
    if isinstance(value, type):
        return _type_expr(value)
    if isinstance(value, tuple):
        return _tuple_expr(_value_expr(item, source_names, label) for item in value)
    if value is None or isinstance(value, (bool, int, float, str)):
        return repr(value)
    return _source_path_for(value, source_names, label)


def _system_generated_value_import_names(
    system: DataDefinitionSystem,
) -> tuple[str, ...]:
    names: set[str] = set()
    for prop in system.properties:
        names.update(_generated_value_constructor_names_in(prop.default))
    for collection in system.computed_collections:
        for condition in collection.conditions:
            names.update(_generated_value_constructor_names_in(condition.value))
    for production in system.productions:
        for condition in production.conditions:
            names.update(_generated_value_constructor_names_in(condition.value))
        if production.identity is not None and _expression_uses_generated_values(
            production.identity
        ):
            names.update(
                _generated_value_constructor_names_in_expression(production.identity)
            )
        for value in production.values:
            names.update(
                _generated_value_constructor_names_in_expression(value.expression)
            )
    for matcher in _system_matchers(system):
        if matcher.has_default_resource:
            names.update(generated_value_constructor_names(matcher.default_resource))
        for rule in matcher.rules:
            names.update(generated_value_constructor_names(rule.resource))
    return tuple(sorted(names))


def _system_uses_astichi_templates(system: DataDefinitionSystem) -> bool:
    for prop in system.properties:
        if _contains_astichi_template_value(prop.default):
            return True
    for collection in system.computed_collections:
        if any(
            _contains_astichi_template_value(condition.value)
            for condition in collection.conditions
        ):
            return True
    for production in system.productions:
        if any(
            _contains_astichi_template_value(condition.value)
            for condition in production.conditions
        ):
            return True
        if production.identity is not None and _expression_uses_astichi_templates(
            production.identity
        ):
            return True
        if any(
            _expression_uses_astichi_templates(value.expression)
            for value in production.values
        ):
            return True
    return False


def _expression_uses_generated_values(expression: object) -> bool:
    if isinstance(expression, LiteralValue):
        return _contains_generated_value(expression.value)
    if isinstance(expression, LookupValue):
        return _lookup_key_uses_generated_values(
            expression.key
        ) or _expression_uses_generated_values(expression.default)
    return False


def _expression_uses_astichi_templates(expression: object) -> bool:
    if isinstance(expression, LiteralValue):
        return _contains_astichi_template_value(expression.value)
    if isinstance(expression, LookupValue):
        return _lookup_key_uses_astichi_templates(
            expression.key
        ) or _expression_uses_astichi_templates(expression.default)
    return False


def _lookup_key_uses_generated_values(key: object) -> bool:
    if isinstance(key, tuple):
        return any(_expression_uses_generated_values(item) for item in key)
    return _expression_uses_generated_values(key)


def _lookup_key_uses_astichi_templates(key: object) -> bool:
    if isinstance(key, tuple):
        return any(_expression_uses_astichi_templates(item) for item in key)
    return _expression_uses_astichi_templates(key)


def _contains_generated_value(value: object) -> bool:
    if is_generated_value(value):
        return True
    if isinstance(value, tuple | list | set):
        return any(_contains_generated_value(item) for item in value)
    if isinstance(value, dict):
        return any(
            _contains_generated_value(item) for pair in value.items() for item in pair
        )
    return False


def _generated_value_constructor_names_in(value: object) -> tuple[str, ...]:
    if is_generated_value(value):
        return generated_value_constructor_names(value)
    if isinstance(value, tuple | list | set):
        names: set[str] = set()
        for item in value:
            names.update(_generated_value_constructor_names_in(item))
        return tuple(sorted(names))
    if isinstance(value, dict):
        names: set[str] = set()
        for pair in value.items():
            for item in pair:
                names.update(_generated_value_constructor_names_in(item))
        return tuple(sorted(names))
    return ()


def _generated_value_constructor_names_in_expression(
    expression: object,
) -> tuple[str, ...]:
    if isinstance(expression, LiteralValue):
        return _generated_value_constructor_names_in(expression.value)
    if isinstance(expression, LookupValue):
        names: set[str] = set()
        names.update(_generated_value_constructor_names_in_lookup_key(expression.key))
        if expression.default is not _NO_LOOKUP_DEFAULT:
            names.update(
                _generated_value_constructor_names_in_expression(expression.default)
            )
        return tuple(sorted(names))
    return ()


def _generated_value_constructor_names_in_lookup_key(key: object) -> tuple[str, ...]:
    if isinstance(key, tuple):
        names: set[str] = set()
        for item in key:
            names.update(_generated_value_constructor_names_in_expression(item))
        return tuple(sorted(names))
    return _generated_value_constructor_names_in_expression(key)


def _contains_astichi_template_value(value: object) -> bool:
    if is_generated_value(value):
        return generated_value_uses_astichi_template(value)
    if isinstance(value, tuple | list | set):
        return any(_contains_astichi_template_value(item) for item in value)
    if isinstance(value, dict):
        return any(
            _contains_astichi_template_value(item)
            for pair in value.items()
            for item in pair
        )
    return False


def _source_path_for(value: object, source_names: SourceNameMap, label: str) -> str:
    for candidate, path in _iter_source_names(source_names):
        if candidate is value:
            _require_ref_path(path, label)
            return path
    raise ValueError(f"no source name registered for {label} {value!r}")


def _iter_source_names(
    source_names: SourceNameMap,
) -> tuple[tuple[object, str], ...]:
    if isinstance(source_names, Mapping):
        return tuple(source_names.items())
    return tuple(source_names)


def _require_ref_path(path: str, label: str) -> None:
    if not path or any(not part.isidentifier() for part in path.split(".")):
        raise ValueError(
            f"{label} source path must be a dotted identifier path: {path!r}"
        )


def _type_name(value_type: type[object] | tuple[type[object], ...]) -> str:
    if isinstance(value_type, tuple):
        return " or ".join(item.__name__ for item in value_type)
    return value_type.__name__


def _system_matchers(system: DataDefinitionSystem) -> tuple[MatcherSpec, ...]:
    return tuple(getattr(system, "matchers", ()))


def _source_name_roots(source_names: SourceNameMap) -> tuple[str, ...]:
    return tuple(path.split(".", 1)[0] for _, path in _iter_source_names(source_names))


_RUNTIME_IMPORT_NAMES = (
    "AddIfAbsent",
    "DDSContainerBuilder",
    "NOT_PROVIDED",
    "REQUIRED",
    "RejectDuplicate",
    "ReplaceExisting",
    "RuntimeCollection",
    "RuntimeComputedCollection",
    "RuntimeContainerSpec",
    "RuntimePort",
    "RuntimePortIndex",
    "RuntimeProperty",
    "RuntimeRecord",
    "RuntimeUnion",
)


def _runtime_import_names(
    generated_value_import_names: tuple[str, ...],
    uses_astichi_templates: bool,
    uses_operations: bool,
    uses_operation_dispatch: bool = False,
) -> tuple[str, ...]:
    names = [*_RUNTIME_IMPORT_NAMES]
    names.extend(generated_value_import_names)
    if uses_astichi_templates:
        names.append("astichi_template")
    if uses_operations:
        names.append("DDSOperationContext")
    if uses_operation_dispatch:
        names.append("AssemblyDiagnosticError")
        names.append("OperationExecutionError")
    return tuple(dict.fromkeys(names))


_BUILTIN_KEEP_NAMES = (
    "AttributeError",
    "TypeError",
    "bool",
    "complex",
    "float",
    "getattr",
    "int",
    "isinstance",
    "len",
    "object",
    "repr",
    "str",
    "type",
)


def _pyimport_prefix(
    generated_value_import_names: tuple[str, ...],
    uses_astichi_templates: bool,
    uses_operations: bool,
    uses_operation_dispatch: bool = False,
) -> str:
    names = "\n".join(
        f"        {name},"
        for name in _runtime_import_names(
            generated_value_import_names,
            uses_astichi_templates,
            uses_operations,
            uses_operation_dispatch,
        )
    )
    return textwrap.dedent(f"""
        astichi_pyimport(
            module=yidl.generation.data_def_sys,
            names=(
        {names}
            ),
        )
        """).strip()


__all__ = ["SourceNameMap", "emit_container_runtime_source"]
