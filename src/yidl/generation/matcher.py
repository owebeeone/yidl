"""Rule matcher primitives for YIDL generation data."""

from __future__ import annotations

import ast
from collections.abc import Callable, Iterable, Iterator, Mapping, Sequence
from dataclasses import dataclass
from itertools import product
import textwrap

import astichi
from astichi.model import BasicComposable
from astichi.model import CompileOrigin
from astichi.model import value_to_ast

from yidl.generation.data_schema import CollectionSpec
from yidl.generation.data_schema import ComputedCollectionSpec
from yidl.generation.data_schema import MatcherResultSource
from yidl.generation.data_schema import PropertySpec
from yidl.generation.matcher_values import MatcherGeneratedValue
from yidl.generation.matcher_values import constructor_expr_for


class NotProvidedValue:
    """Matcher tuple sentinel for values absent from a record variant."""

    __slots__ = ()

    def __repr__(self) -> str:
        return "NOT_PROVIDED"


NOT_PROVIDED = NotProvidedValue()
_MISSING_CONDITION = object()
_NO_DEFAULT = object()


@dataclass(frozen=True)
class MatcherInputSpec:
    matcher: MatcherSpec
    name: str
    source: CollectionSpec | ComputedCollectionSpec
    index: int

    def prop(self, property: PropertySpec) -> ScopedPropertyRef:
        if property.system is not self.source.system:
            raise ValueError(
                f"property {property.name!r} belongs to another data-definition system"
            )
        self.source.record_shape.require_property(property)
        return ScopedPropertyRef(self, property)

    def __repr__(self) -> str:
        return f"{self.matcher.name}.{self.name}"


@dataclass(frozen=True)
class ScopedPropertyRef:
    input: MatcherInputSpec
    property: PropertySpec

    def eq(self, value: object) -> MatcherCondition:
        if value is not NOT_PROVIDED:
            self.property.validate(value)
        return MatcherCondition(self, value)

    def __repr__(self) -> str:
        return f"{self.input}.{self.property}"


@dataclass(frozen=True)
class MatcherEvaluatedFieldSpec:
    matcher: MatcherSpec
    name: str
    inputs: tuple[MatcherInputSpec, ...]
    evaluator: Callable[..., object]
    value_type: type[object] | tuple[type[object], ...] | None = None

    def eq(self, value: object) -> MatcherCondition:
        if value is not NOT_PROVIDED and self.value_type is not None:
            if not isinstance(value, self.value_type):
                raise TypeError(
                    f"{self.name} must be {_type_name(self.value_type)}, "
                    f"got {type(value).__name__}"
                )
        return MatcherCondition(self, value)

    def __repr__(self) -> str:
        return f"{self.matcher.name}.{self.name}"


MatcherTupleRef = ScopedPropertyRef | MatcherEvaluatedFieldSpec


@dataclass(frozen=True)
class MatcherCondition:
    ref: MatcherTupleRef
    value: object

    def __repr__(self) -> str:
        return f"{self.ref} == {self.value!r}"


@dataclass(frozen=True)
class MatcherRuleSpec:
    matcher: MatcherSpec
    name: str
    conditions: tuple[MatcherCondition, ...]
    weight: float
    resource: MatcherGeneratedValue

    @property
    def score(self) -> float:
        return len(self.conditions) * self.weight

    def __repr__(self) -> str:
        return self.name


@dataclass(frozen=True)
class MatcherResult:
    resource: MatcherGeneratedValue
    rule: str | None
    score: float
    records: tuple[object, ...]
    values: tuple[object, ...]


SourceNameMap = Mapping[object, str] | Sequence[tuple[object, str]]


class MatcherSpec:
    """Definition-time matcher with a lazy in-memory runtime evaluator."""

    __slots__ = (
        "_default_resource",
        "_evaluated_fields",
        "_inputs",
        "_rules",
        "_system",
        "name",
    )

    def __init__(self, name: str, *, system: object | None = None) -> None:
        _require_name(name, "matcher name")
        self.name = name
        self._system = system
        self._inputs: list[MatcherInputSpec] = []
        self._evaluated_fields: list[MatcherEvaluatedFieldSpec] = []
        self._rules: list[MatcherRuleSpec] = []
        self._default_resource: object = _NO_DEFAULT

    @property
    def system(self) -> object | None:
        return self._system

    @property
    def inputs(self) -> tuple[MatcherInputSpec, ...]:
        return tuple(self._inputs)

    @property
    def evaluated_fields(self) -> tuple[MatcherEvaluatedFieldSpec, ...]:
        return tuple(self._evaluated_fields)

    @property
    def rules(self) -> tuple[MatcherRuleSpec, ...]:
        return tuple(self._rules)

    @property
    def default_resource(self) -> MatcherGeneratedValue | object:
        return self._default_resource

    @property
    def has_default_resource(self) -> bool:
        return self._default_resource is not _NO_DEFAULT

    @property
    def tuple_schema(self) -> tuple[MatcherTupleRef, ...]:
        resolved: list[MatcherTupleRef] = []
        for rule in self._rules:
            for condition in rule.conditions:
                if condition.ref not in resolved:
                    resolved.append(condition.ref)
        return tuple(resolved)

    def input(
        self,
        name: str,
        source: CollectionSpec | ComputedCollectionSpec,
    ) -> MatcherInputSpec:
        _require_name(name, "matcher input name")
        if self._system is not None and source.system is not self._system:
            raise ValueError(
                f"matcher input {name!r} belongs to another data-definition system"
            )
        if any(existing.name == name for existing in self._inputs):
            raise ValueError(f"matcher {self.name!r} already has input {name!r}")
        spec = MatcherInputSpec(self, name, source, len(self._inputs))
        self._inputs.append(spec)
        return spec

    def ensure_input(
        self,
        name: str,
        source: CollectionSpec | ComputedCollectionSpec,
    ) -> MatcherInputSpec:
        for existing in self._inputs:
            if existing.name == name:
                if existing.source is not source:
                    raise ValueError(
                        f"matcher {self.name!r} input {name!r} is already "
                        "defined differently"
                    )
                return existing
        return self.input(name, source)

    def evaluated_field(
        self,
        name: str,
        *,
        inputs: Sequence[MatcherInputSpec],
        value: Callable[..., object],
        value_type: type[object] | tuple[type[object], ...] | None = None,
    ) -> MatcherEvaluatedFieldSpec:
        _require_name(name, "evaluated field name")
        if any(existing.name == name for existing in self._evaluated_fields):
            raise ValueError(f"matcher {self.name!r} already has evaluated field {name!r}")
        resolved_inputs = tuple(inputs)
        if not resolved_inputs:
            raise ValueError("evaluated fields must depend on at least one matcher input")
        for input_spec in resolved_inputs:
            if input_spec.matcher is not self:
                raise ValueError(
                    f"evaluated field {name!r} references input from another matcher"
                )
        spec = MatcherEvaluatedFieldSpec(
            self,
            name,
            resolved_inputs,
            value,
            value_type,
        )
        self._evaluated_fields.append(spec)
        return spec

    def rule(
        self,
        *,
        when: Sequence[MatcherCondition],
        resource: MatcherGeneratedValue,
        weight: float = 1.0,
        name: str | None = None,
    ) -> MatcherRuleSpec:
        _require_generated_value(resource, "matcher rule resource")
        if weight <= 0:
            raise ValueError("matcher rule weight must be greater than zero")
        resolved_conditions = tuple(when)
        if not resolved_conditions:
            raise ValueError("matcher rules must have at least one condition; use default()")
        for condition in resolved_conditions:
            self._require_own_condition(condition)
        rule_name = name or f"{self.name}_rule_{len(self._rules)}"
        _require_label(rule_name, "matcher rule name")
        spec = MatcherRuleSpec(
            self,
            rule_name,
            resolved_conditions,
            float(weight),
            resource,
        )
        self._rules.append(spec)
        return spec

    def default(self, resource: MatcherGeneratedValue) -> MatcherGeneratedValue:
        _require_generated_value(resource, "matcher default resource")
        self._default_resource = resource
        return resource

    def results(self) -> MatcherResultSource:
        return MatcherResultSource(self)

    def runtime(self) -> MatcherRuntime:
        self.validate()
        return MatcherRuntime(self)

    def emit_runtime_source(
        self,
        *,
        class_name: str | None = None,
        evaluator_names: SourceNameMap = (),
        value_names: SourceNameMap = (),
    ) -> str:
        return emit_matcher_runtime_source(
            self,
            class_name=class_name,
            evaluator_names=evaluator_names,
            value_names=value_names,
        )

    def validate(self) -> None:
        _validate_no_equal_score_overlaps(self)

    def _require_own_condition(self, condition: MatcherCondition) -> None:
        ref = condition.ref
        if isinstance(ref, ScopedPropertyRef):
            if ref.input.matcher is not self:
                raise ValueError("matcher rule condition references another matcher")
            return
        if ref.matcher is not self:
            raise ValueError("matcher rule condition references another matcher")

    def __repr__(self) -> str:
        return self.name


class MatcherRuntime:
    """Lazy cached evaluator for one matcher attached to one resolved context."""

    __slots__ = ("_cache", "_index_by_ref", "_matcher", "_rules", "_tuple_schema")

    def __init__(self, matcher: MatcherSpec) -> None:
        self._matcher = matcher
        self._tuple_schema = matcher.tuple_schema
        self._index_by_ref = {
            ref: index
            for index, ref in enumerate(self._tuple_schema)
        }
        self._rules = _rules_by_descending_score(matcher)
        self._cache: dict[
            tuple[object, ...],
            tuple[object, str | None, float] | None,
        ] = {}

    @property
    def matcher(self) -> MatcherSpec:
        return self._matcher

    def resolve(self, *records: object) -> MatcherResult | None:
        if len(records) != len(self._matcher.inputs):
            raise ValueError(
                f"matcher {self._matcher.name!r} expects {len(self._matcher.inputs)} "
                f"records, got {len(records)}"
            )
        self._validate_records(records)
        values = self._extract_values(records)
        try:
            cached = self._cache.get(values, NOT_PROVIDED)
        except TypeError:
            return self._result_from_selection(
                self._select(values),
                records,
                values,
            )
        if cached is NOT_PROVIDED:
            cached = self._select(values)
            self._cache[values] = cached
        return self._result_from_selection(cached, records, values)

    def sequence(self, *record_sequences: Iterable[object]) -> Iterator[MatcherResult]:
        if len(record_sequences) != len(self._matcher.inputs):
            raise ValueError(
                f"matcher {self._matcher.name!r} expects {len(self._matcher.inputs)} "
                f"record sequences, got {len(record_sequences)}"
            )
        for records in product(*record_sequences):
            result = self.resolve(*records)
            if result is not None:
                yield result

    def _validate_records(self, records: tuple[object, ...]) -> None:
        for input_spec, record in zip(self._matcher.inputs, records, strict=True):
            input_spec.source.record_shape.validate_record(record)

    def _select(
        self,
        values: tuple[object, ...],
    ) -> tuple[object, str | None, float] | None:
        for rule in self._rules:
            if all(
                values[self._index_by_ref[condition.ref]] == condition.value
                for condition in rule.conditions
            ):
                return (rule.resource, rule.name, rule.score)
        if self._matcher.default_resource is _NO_DEFAULT:
            return None
        return (self._matcher.default_resource, None, 0.0)

    def _result_from_selection(
        self,
        selection: tuple[object, str | None, float] | None,
        records: tuple[object, ...],
        values: tuple[object, ...],
    ) -> MatcherResult | None:
        if selection is None:
            return None
        resource, rule, score = selection
        return MatcherResult(
            resource=resource,
            rule=rule,
            score=score,
            records=records,
            values=values,
        )

    def _extract_values(self, records: tuple[object, ...]) -> tuple[object, ...]:
        values: list[object] = []
        for ref in self._tuple_schema:
            if isinstance(ref, ScopedPropertyRef):
                record = records[ref.input.index]
                values.append(getattr(record, ref.property.storage_name, NOT_PROVIDED))
                continue
            args = tuple(records[input_spec.index] for input_spec in ref.inputs)
            values.append(ref.evaluator(*args))
        return tuple(values)


def emit_matcher_runtime_source(
    matcher: MatcherSpec,
    *,
    class_name: str | None = None,
    evaluator_names: SourceNameMap = (),
    value_names: SourceNameMap = (),
) -> str:
    """Emit a source module containing a runtime matcher class."""

    return build_matcher_runtime_composable(
        matcher,
        class_name=class_name or f"{matcher.name}Matcher",
        evaluator_names=evaluator_names,
        value_names=value_names,
    ).materialize().emit(provenance=False)


def build_matcher_runtime_composable(
    matcher: MatcherSpec,
    *,
    class_name: str,
    evaluator_names: SourceNameMap,
    value_names: SourceNameMap,
) -> astichi.Composable:
    matcher.validate()
    _require_name(class_name, "matcher runtime class name")
    builder = astichi.build()
    builder.add.Root(
        _MATCHER_CLASS.bind(
            input_count=len(matcher.inputs),
        ),
        arg_names={"matcher_class_name": class_name},
        keep_names=[
            class_name,
            "MatcherResult",
            "NOT_PROVIDED",
            "TypeError",
            "ValueError",
            "from_astichi_code",
            "getattr",
            "len",
            "product",
        ],
    )
    for order, input_spec in enumerate(matcher.inputs):
        record_name = _record_var_name(input_spec)
        builder.add.Param[order](
            _PARAM,
            arg_names={"record": record_name},
            keep_names=[record_name],
        )
        builder.Root.params.add.Param[order](order=order)
        builder.add.RecordEntry[order](
            _RECORD_ENTRY,
            arg_names={"record": record_name},
        )
        builder.Root.record_entries.add.RecordEntry[order](order=order)
    for order, ref in enumerate(matcher.tuple_schema):
        builder.add.ValueEntry[order](
            _value_entry_piece(ref, evaluator_names),
        )
        builder.Root.value_entries.add.ValueEntry[order](order=order)
    for order, rule in enumerate(_rules_by_descending_score(matcher)):
        builder.add.RuleCheck[order](
            _rule_check_piece(rule, matcher, value_names),
        )
        builder.Root.rule_checks.add.RuleCheck[order](order=order)
    builder.add.DefaultResult(
        _default_result_piece(matcher),
    )
    builder.Root.default_result.add.DefaultResult()
    return builder.build()


def _rule_check_piece(
    rule: MatcherRuleSpec,
    matcher: MatcherSpec,
    value_names: SourceNameMap,
) -> astichi.Composable:
    builder = astichi.build()
    index_by_ref = {
        ref: index
        for index, ref in enumerate(matcher.tuple_schema)
    }
    indexes = tuple(index_by_ref[condition.ref] for condition in rule.conditions)
    bind_values: dict[str, object] = {
        "rule_score": rule.score,
        "rule_name": rule.name,
    }
    builder.add.Root(
        _RULE_CHECK.bind(bind_values),
    )
    builder.add.Actual(_actual_values_piece(indexes))
    builder.Root.actual_values.add.Actual()
    builder.add.Resource(_generated_value_piece(rule.resource))
    builder.Root.resource.add.Resource()
    for order, condition in enumerate(rule.conditions):
        builder.add.Expected[order](
            _expected_value_piece(condition.value, value_names),
        )
        builder.Root.expected_values.add.Expected[order](order=order)
    return builder.build()


def _value_entry_piece(
    ref: MatcherTupleRef,
    evaluator_names: SourceNameMap,
) -> astichi.Composable:
    if isinstance(ref, ScopedPropertyRef):
        return _VALUE_PROPERTY.bind(
            storage_name=ref.property.storage_name,
        ).bind_identifier(
            record=_record_var_name(ref.input),
        ).with_keep_names(["getattr", "NOT_PROVIDED"])
    builder = astichi.build()
    builder.add.Root(
        _VALUE_EVALUATED.bind(
            evaluator_path=_source_path_for(ref.evaluator, evaluator_names, "evaluator"),
        )
    )
    for order, input_spec in enumerate(ref.inputs):
        builder.add.Arg[order](
            _FUNCARG_RECORD,
            arg_names={"record": _record_var_name(input_spec)},
        )
        builder.Root.args.add.Arg[order](order=order)
    return builder.build()


def _expected_value_piece(value: object, value_names: SourceNameMap) -> astichi.Composable:
    if value is NOT_PROVIDED:
        return _source_ref_piece("NOT_PROVIDED")
    if isinstance(value, type) and value.__module__ == "builtins":
        return _source_ref_piece(value.__qualname__)
    if value is None or isinstance(value, (bool, int, float, str)):
        return _literal_piece(value)
    return _source_ref_piece(
        _source_path_for(value, value_names, "condition value")
    )


def _default_result_piece(
    matcher: MatcherSpec,
) -> astichi.Composable:
    if matcher.default_resource is _NO_DEFAULT:
        return _DEFAULT_NONE
    builder = astichi.build()
    builder.add.Root(_DEFAULT_RESOURCE)
    builder.add.Resource(_generated_value_piece(matcher.default_resource))
    builder.Root.resource.add.Resource()
    return builder.build()


def _rules_by_descending_score(matcher: MatcherSpec) -> tuple[MatcherRuleSpec, ...]:
    return tuple(
        sorted(
            matcher.rules,
            key=lambda rule: rule.score,
            reverse=True,
        )
    )


def _record_var_name(input_spec: MatcherInputSpec) -> str:
    return f"{input_spec.name}_record"


def _actual_values_piece(indexes: tuple[int, ...]) -> astichi.Composable:
    runs = _contiguous_index_runs(indexes)
    if len(runs) == 1:
        start, stop = runs[0]
        return _VALUE_SLICE.bind(start=start, stop=stop)
    pieces = [
        _VALUE_SLICE.bind(start=start, stop=stop)
        for start, stop in runs
    ]
    result = pieces[0]
    for order, piece in enumerate(pieces[1:], start=1):
        builder = astichi.build()
        builder.add.Root(_VALUE_ADD)
        builder.add.Left(result)
        builder.add.Right(piece)
        builder.Root.left.add.Left(order=0)
        builder.Root.right.add.Right(order=order)
        result = builder.build()
    return result


def _contiguous_index_runs(indexes: tuple[int, ...]) -> tuple[tuple[int, int], ...]:
    if not indexes:
        raise ValueError("matcher rules must have at least one condition")
    runs: list[tuple[int, int]] = []
    start = indexes[0]
    previous = indexes[0]
    for index in indexes[1:]:
        if index == previous + 1:
            previous = index
            continue
        runs.append((start, previous + 1))
        start = index
        previous = index
    runs.append((start, previous + 1))
    return tuple(runs)


def _literal_piece(value: object) -> BasicComposable:
    return _expr_piece(value_to_ast(value))


def _generated_value_piece(value: MatcherGeneratedValue) -> BasicComposable:
    return _expr_piece(
        constructor_expr_for(value),
        keep_names=["from_astichi_code"],
    )


def _source_ref_piece(path: str) -> BasicComposable:
    _require_ref_path(path, "source reference")
    parts = path.split(".")
    expr: ast.expr = ast.Name(id=parts[0], ctx=ast.Load())
    for part in parts[1:]:
        expr = ast.Attribute(value=expr, attr=part, ctx=ast.Load())
    return _expr_piece(expr, keep_names=[parts[0]])


def _expr_piece(
    expr: ast.expr,
    *,
    keep_names: Iterable[str] = (),
) -> BasicComposable:
    tree = ast.Module(body=[ast.Expr(value=expr)], type_ignores=[])
    ast.fix_missing_locations(tree)
    return BasicComposable(
        tree=tree,
        origin=CompileOrigin("<yidl.matcher>", 1, 0),
        keep_names=frozenset(keep_names),
    )


def _source_path_for(value: object, source_names: SourceNameMap, label: str) -> str:
    for candidate, path in _iter_source_names(source_names):
        if candidate is value:
            _require_ref_path(path, label)
            return path
    raise ValueError(f"no source name registered for {label} {value!r}")


def _iter_source_names(source_names: SourceNameMap) -> Iterator[tuple[object, str]]:
    if isinstance(source_names, Mapping):
        yield from source_names.items()
        return
    yield from source_names


def _validate_no_equal_score_overlaps(matcher: MatcherSpec) -> None:
    rules = matcher.rules
    values_by_rule = {
        rule: _condition_values_by_ref(rule)
        for rule in rules
    }
    for left_index, left in enumerate(rules):
        for right in rules[left_index + 1:]:
            if left.score != right.score:
                continue
            if _rule_values_can_overlap(values_by_rule[left], values_by_rule[right]):
                raise ValueError(
                    f"matcher {matcher.name!r} has equal-score overlapping rules "
                    f"at score {left.score}: {left.name}, {right.name}"
                )


def _rule_values_can_overlap(
    left_values: Mapping[MatcherTupleRef, object],
    right_values: Mapping[MatcherTupleRef, object],
) -> bool:
    """Return whether two condition maps can match the same tuple.

    Same-score rules are allowed only when at least one shared tuple position
    requires different values. No shared positions means they can overlap.
    """

    for ref in left_values.keys() & right_values.keys():
        if left_values[ref] != right_values[ref]:
            return False
    return True


def _condition_values_by_ref(rule: MatcherRuleSpec) -> dict[MatcherTupleRef, object]:
    resolved: dict[MatcherTupleRef, object] = {}
    for condition in rule.conditions:
        existing = resolved.get(condition.ref, _MISSING_CONDITION)
        if existing is not _MISSING_CONDITION and existing != condition.value:
            raise ValueError(
                f"matcher rule {rule.name!r} has conflicting conditions for {condition.ref}"
            )
        resolved[condition.ref] = condition.value
    return resolved


def _require_name(value: str, label: str) -> None:
    if not isinstance(value, str) or not value.isidentifier():
        raise ValueError(f"{label} must be a valid identifier: {value!r}")


def _require_label(value: str, label: str) -> None:
    if not isinstance(value, str) or not value:
        raise ValueError(f"{label} must be a non-empty string")


def _require_ref_path(value: str, label: str) -> None:
    if not isinstance(value, str) or not value:
        raise ValueError(f"{label} source path must be a non-empty string")
    for part in value.split("."):
        _require_name(part, f"{label} source path component")


def _require_generated_value(value: object, label: str) -> None:
    if not isinstance(value, MatcherGeneratedValue):
        raise TypeError(f"{label} must be a MatcherGeneratedValue")


def _type_name(value_type: type[object] | tuple[type[object], ...]) -> str:
    if isinstance(value_type, tuple):
        return " or ".join(item.__name__ for item in value_type)
    return value_type.__name__


def _compile_template(source: str) -> astichi.Composable:
    return astichi.compile(textwrap.dedent(source).strip() + "\n")


_MATCHER_CLASS = _compile_template(
    """
astichi_pyimport(module=itertools, names=(product,))
astichi_pyimport(
    module=yidl.generation.data_def_sys,
    names=(MatcherResult, NOT_PROVIDED, from_astichi_code),
)


class matcher_class_name__astichi_arg__:
    def __init__(self):
        self._cache = {}

    def resolve(self, params__astichi_param_hole__):
        records = (*astichi_hole(record_entries),)
        values = (*astichi_hole(value_entries),)
        try:
            cached = self._cache.get(values, NOT_PROVIDED)
        except TypeError:
            cached = NOT_PROVIDED
            cache_key = None
        else:
            cache_key = values
        if cached is not NOT_PROVIDED:
            return self._finish(None, cached, records, values)
        astichi_hole(rule_checks)
        return self._finish(cache_key, astichi_hole(default_result), records, values)

    def _finish(self, cache_key, selection, records, values):
        if cache_key is not None:
            self._cache[cache_key] = selection
        if selection is None:
            return None
        resource, rule, score = selection
        return MatcherResult(
            resource=resource,
            rule=rule,
            score=score,
            records=records,
            values=values,
        )

    def sequence(self, *record_sequences):
        if len(record_sequences) != astichi_bind_external(input_count):
            raise ValueError("wrong number of record sequences")
        for records in product(*record_sequences):
            result = self.resolve(*records)
            if result is not None:
                yield result
"""
)

_PARAM = _compile_template(
    """
def astichi_params(record__astichi_arg__):
    pass
"""
)

# Expands into one record reference inside the generated `records = (...)` tuple.
_RECORD_ENTRY = _compile_template(
    """
astichi_import(record__astichi_arg__)
record__astichi_arg__
"""
)

_VALUE_PROPERTY = _compile_template(
    """
getattr(
    astichi_pass(record__astichi_arg__, outer_bind=True),
    astichi_bind_external(storage_name),
    NOT_PROVIDED,
)
"""
)

_VALUE_EVALUATED = _compile_template(
    """
astichi_ref(external=evaluator_path)(astichi_hole(args))
"""
)

_FUNCARG_RECORD = _compile_template(
    """
astichi_funcargs(astichi_pass(record__astichi_arg__, outer_bind=True))
"""
)

_VALUE_SLICE = _compile_template(
    """
astichi_pass(values, outer_bind=True)[
    astichi_bind_external(start):astichi_bind_external(stop)
]
"""
)

_VALUE_ADD = _compile_template(
    """
astichi_hole(left) + astichi_hole(right)
"""
)

_RULE_CHECK = _compile_template(
    """
if astichi_hole(actual_values) == (*astichi_hole(expected_values),):
    return astichi_pass(self, outer_bind=True)._finish(
        astichi_pass(cache_key, outer_bind=True),
        (
            astichi_hole(resource),
            astichi_bind_external(rule_name),
            astichi_bind_external(rule_score),
        ),
        astichi_pass(records, outer_bind=True),
        astichi_pass(values, outer_bind=True),
    )
"""
)

_DEFAULT_NONE = _compile_template(
    """
None
"""
)

_DEFAULT_RESOURCE = _compile_template(
    """
(
    astichi_hole(resource),
    None,
    0.0,
)
"""
)


__all__ = [
    "MatcherCondition",
    "MatcherEvaluatedFieldSpec",
    "MatcherInputSpec",
    "MatcherResult",
    "MatcherRuleSpec",
    "MatcherRuntime",
    "MatcherSpec",
    "NOT_PROVIDED",
    "NotProvidedValue",
    "ScopedPropertyRef",
    "build_matcher_runtime_composable",
    "emit_matcher_runtime_source",
]
