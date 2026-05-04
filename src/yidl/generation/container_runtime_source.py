"""Source emission for decorator-time DDS container modules."""

from __future__ import annotations

from collections.abc import Mapping, Sequence

from yidl.generation.data_schema import CollectionSpec
from yidl.generation.data_schema import ComputedCollectionSpec
from yidl.generation.data_schema import DataDefinitionSystem
from yidl.generation.data_schema import PropertySpec
from yidl.generation.data_schema import REQUIRED
from yidl.generation.data_schema import RecordSpec
from yidl.generation.data_schema import UnionSpec
from yidl.generation.matcher import MatcherSpec
from yidl.generation.matcher import NOT_PROVIDED
from yidl.generation.matcher import emit_matcher_runtime_source


SourceNameMap = Mapping[object, str] | Sequence[tuple[object, str]]


def emit_container_runtime_source(
    system: DataDefinitionSystem,
    *,
    evaluator_names: SourceNameMap = (),
    value_names: SourceNameMap = (),
) -> str:
    """Emit a Python module containing DDS records, collections, and matchers."""

    lines: list[str] = [
        "from yidl.generation.data_def_sys import AddIfAbsent, DDSContainerBuilder, NOT_PROVIDED, REQUIRED",
        "from yidl.generation.data_def_sys import RejectDuplicate, ReplaceExisting",
        "from yidl.generation.data_def_sys import RuntimeCollection, RuntimeComputedCollection, RuntimeContainerSpec",
        "from yidl.generation.data_def_sys import RuntimeProperty, RuntimeRecord, RuntimeUnion",
    ]
    prop_vars = _property_vars(system)
    record_vars: dict[RecordSpec, str] = {}
    union_vars: dict[UnionSpec, str] = {}
    collection_vars: dict[CollectionSpec | ComputedCollectionSpec, str] = {}

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
        record_expr = _record_shape_expr(collection.record_shape, record_vars, union_vars)
        identity_expr = (
            "None"
            if collection.identity is None
            else prop_vars[collection.identity]
        )
        cardinality_expr = (
            "True"
            if collection.cardinality.allows_multiple()
            else "False"
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

    lines.append(
        "_RUNTIME_SPEC = RuntimeContainerSpec("
        f"collections={_tuple_expr(collection_vars[collection] for collection in system.collections)}, "
        f"computed_collections={_tuple_expr(collection_vars[collection] for collection in system.computed_collections)}"
        ")"
    )
    lines.append("")

    matchers = _system_matchers(system)
    for matcher in matchers:
        lines.extend(
            emit_matcher_runtime_source(
                matcher,
                class_name=_matcher_runtime_class_name(matcher),
                evaluator_names=evaluator_names,
                value_names=value_names,
            ).rstrip().splitlines()
        )
        lines.append("")

    lines.extend(_emit_container_builder_lines(matchers))
    return "\n".join(lines).rstrip() + "\n"


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


def _record_shape_expr(
    shape: RecordSpec | UnionSpec,
    record_vars: Mapping[RecordSpec, str],
    union_vars: Mapping[UnionSpec, str],
) -> str:
    if isinstance(shape, UnionSpec):
        return union_vars[shape]
    return record_vars[shape]


def _property_vars(system: DataDefinitionSystem) -> dict[PropertySpec, str]:
    return {prop: f"_{prop.name}Property" for prop in system.properties}


def _record_var(record: RecordSpec) -> str:
    return f"_{record.name}Spec"


def _union_var(union: UnionSpec) -> str:
    return f"_{union.name}Union"


def _collection_var(collection: CollectionSpec | ComputedCollectionSpec) -> str:
    return f"{collection.name}Collection"


def _matcher_runtime_class_name(matcher: MatcherSpec) -> str:
    return f"{matcher.name}Matcher"


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
    if isinstance(value, type):
        return _type_expr(value)
    if value is None or isinstance(value, (bool, int, float, str)):
        return repr(value)
    return _source_path_for(value, source_names, label)


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
        raise ValueError(f"{label} source path must be a dotted identifier path: {path!r}")


def _type_name(value_type: type[object] | tuple[type[object], ...]) -> str:
    if isinstance(value_type, tuple):
        return " or ".join(item.__name__ for item in value_type)
    return value_type.__name__


def _system_matchers(system: DataDefinitionSystem) -> tuple[MatcherSpec, ...]:
    return tuple(getattr(system, "matchers", ()))


__all__ = ["SourceNameMap", "emit_container_runtime_source"]
