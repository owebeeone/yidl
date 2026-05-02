from __future__ import annotations

from dataclasses import dataclass

from support.golden_case import run_case
from yidl.generation.data_def_sys import DataDefinitionSystem
from yidl.generation.data_def_sys import REQUIRED
from yidl.generation.data_def_sys import emit_matcher_runtime_source


@dataclass(frozen=True)
class MatcherResource:
    name: str


PlainGetter = MatcherResource("plain")
ManagedGetter = MatcherResource("managed")
DefaultGetter = MatcherResource("default")


def is_managed_field(record: object) -> bool:
    return type(record).__name__ == "ManagedField"


def _build_matcher():
    dds = DataDefinitionSystem()
    name = dds.property("Name", str, default=REQUIRED, storage_name="name")
    init = dds.property("Init", bool, default=True, storage_name="init")
    annotation = dds.property(
        "Annotation",
        object,
        default=REQUIRED,
        storage_name="annotation",
    )
    field_specs = dds.union("FieldSpecs")
    plain_field = field_specs.variant("PlainField", name, init, annotation)
    managed_field = field_specs.variant("ManagedField", name, init, annotation)
    fields = dds.collection("Fields", field_specs, cardinality=dds.many, identity=name)
    matcher = dds.matcher("Getter")
    field = matcher.input("field", fields)
    is_managed = matcher.evaluated_field(
        "IsManaged",
        inputs=(field,),
        value=is_managed_field,
        value_type=bool,
    )
    matcher.default(DefaultGetter)
    matcher.rule(
        name="plain-string-no-init",
        when=(
            field.prop(init).eq(False),
            field.prop(annotation).eq(str),
        ),
        resource=PlainGetter,
    )
    matcher.rule(
        name="managed-string-no-init",
        when=(
            field.prop(init).eq(False),
            field.prop(annotation).eq(str),
            is_managed.eq(True),
        ),
        resource=ManagedGetter,
    )
    return matcher, plain_field, managed_field


def render_case() -> str:
    matcher, _, _ = _build_matcher()
    return emit_matcher_runtime_source(
        matcher,
        class_name="GetterMatcher",
        resource_names=(
            (PlainGetter, "PlainGetter"),
            (ManagedGetter, "ManagedGetter"),
            (DefaultGetter, "DefaultGetter"),
        ),
        evaluator_names=((is_managed_field, "is_managed_field"),),
    )


def validate_case(source: str) -> None:
    _, plain_field, managed_field = _build_matcher()
    namespace = {
        "PlainGetter": PlainGetter,
        "ManagedGetter": ManagedGetter,
        "DefaultGetter": DefaultGetter,
        "is_managed_field": is_managed_field,
    }
    exec(source, namespace)
    runtime = namespace["GetterMatcher"]()
    plain_record = plain_field.record(name="count", init=False, annotation=str)
    plain_record_equivalent = plain_field.record(name="count", init=False, annotation=str)
    managed_record = managed_field.record(name="owner", init=False, annotation=str)
    default_record = plain_field.record(name="enabled", init=True, annotation=bool)

    plain_result = runtime.resolve(plain_record)
    managed_result = runtime.resolve(managed_record)
    default_result = runtime.resolve(default_record)

    assert plain_result.resource is PlainGetter
    assert plain_result.rule == "plain-string-no-init"
    assert plain_result.score == 2.0
    assert managed_result.resource is ManagedGetter
    assert managed_result.rule == "managed-string-no-init"
    assert managed_result.score == 3.0
    assert default_result.resource is DefaultGetter
    assert default_result.rule is None
    equivalent_result = runtime.resolve(plain_record_equivalent)
    assert equivalent_result is not plain_result
    assert equivalent_result.resource is PlainGetter
    assert equivalent_result.records == (plain_record_equivalent,)
    sequence_resources = [
        result.resource
        for result in runtime.sequence((plain_record, managed_record, default_record))
    ]
    assert sequence_resources == [
        PlainGetter,
        ManagedGetter,
        DefaultGetter,
    ]
    assert "matches.append" not in source
    assert "id(" not in source
    assert "cached = self._cache.get(values, NOT_PROVIDED)" in source
    assert "score = 0.0" not in source
    assert "> score" not in source
    assert source.index("values[0:3]") < source.index("values[0:2]")
    assert "astichi_" not in source


if __name__ == "__main__":
    raise SystemExit(run_case("matcher_runtime.py", render_case, validate_case))
