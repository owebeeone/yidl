from __future__ import annotations

import ast

import pytest

from yidl.generation.data_def_sys import PYTHON_BUILTIN_KEEP_NAMES
from yidl.generation.data_def_sys import DataDefinitionSystem
from yidl.generation.data_def_sys import NOT_PROVIDED
from yidl.generation.data_def_sys import REQUIRED
from yidl.generation.data_def_sys import constructor_expr_for
from yidl.generation.data_def_sys import from_astichi_code
from yidl.generation.data_def_sys import from_literal


def test_more_specific_rule_wins_over_less_specific_rule() -> None:
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
        value=lambda record: isinstance(record, managed_field.record_class()),
        value_type=bool,
    )
    plain_resource = from_literal("plain")
    managed_resource = from_literal("managed")
    matcher.rule(
        name="plain-string-no-init",
        when=(
            field.prop(init).eq(False),
            field.prop(annotation).eq(str),
        ),
        resource=plain_resource,
    )
    matcher.rule(
        name="managed-string-no-init",
        when=(
            field.prop(init).eq(False),
            field.prop(annotation).eq(str),
            is_managed.eq(True),
        ),
        resource=managed_resource,
    )
    runtime = matcher.runtime()

    plain_result = runtime.resolve(plain_field.record(name="count", init=False, annotation=str))
    managed_result = runtime.resolve(
        managed_field.record(name="owner", init=False, annotation=str)
    )

    assert matcher.tuple_schema == (
        field.prop(init),
        field.prop(annotation),
        is_managed,
    )
    assert plain_result is not None
    assert plain_result.resource is plain_resource
    assert plain_result.rule == "plain-string-no-init"
    assert plain_result.score == 2.0
    assert managed_result is not None
    assert managed_result.resource is managed_resource
    assert managed_result.rule == "managed-string-no-init"
    assert managed_result.score == 3.0


def test_weight_breaks_same_specificity_tie() -> None:
    dds = DataDefinitionSystem()
    name = dds.property("Name", str, default=REQUIRED, storage_name="name")
    init = dds.property("Init", bool, default=True, storage_name="init")
    annotation = dds.property(
        "Annotation",
        object,
        default=REQUIRED,
        storage_name="annotation",
    )
    field_spec = dds.record("FieldSpec", name, init, annotation)
    fields = dds.collection("Fields", field_spec, cardinality=dds.many, identity=name)
    matcher = dds.matcher("Getter")
    field = matcher.input("field", fields)
    default_resource = from_literal("default")
    preferred_resource = from_literal("preferred")
    matcher.rule(
        name="init-rule",
        when=(field.prop(init).eq(False),),
        resource=default_resource,
    )
    matcher.rule(
        name="annotation-rule",
        when=(field.prop(annotation).eq(str),),
        weight=1.1,
        resource=preferred_resource,
    )

    result = matcher.runtime().resolve(field_spec.record(name="count", init=False, annotation=str))

    assert result is not None
    assert result.resource is preferred_resource
    assert result.rule == "annotation-rule"
    assert result.score == 1.1


def test_equal_score_overlapping_rules_reject_before_runtime() -> None:
    dds = DataDefinitionSystem()
    name = dds.property("Name", str, default=REQUIRED, storage_name="name")
    init = dds.property("Init", bool, default=True, storage_name="init")
    annotation = dds.property(
        "Annotation",
        object,
        default=REQUIRED,
        storage_name="annotation",
    )
    field_spec = dds.record("FieldSpec", name, init, annotation)
    fields = dds.collection("Fields", field_spec, cardinality=dds.many, identity=name)
    matcher = dds.matcher("Getter")
    field = matcher.input("field", fields)
    matcher.rule(
        name="first",
        when=(field.prop(init).eq(False),),
        resource=from_literal("first"),
    )
    matcher.rule(
        name="second",
        when=(field.prop(annotation).eq(str),),
        resource=from_literal("second"),
    )

    with pytest.raises(ValueError, match="equal-score overlapping rules"):
        matcher.runtime()


def test_equal_score_conflicting_rules_are_allowed() -> None:
    dds = DataDefinitionSystem()
    name = dds.property("Name", str, default=REQUIRED, storage_name="name")
    init = dds.property("Init", bool, default=True, storage_name="init")
    field_spec = dds.record("FieldSpec", name, init)
    fields = dds.collection("Fields", field_spec, cardinality=dds.many, identity=name)
    matcher = dds.matcher("Getter")
    field = matcher.input("field", fields)
    false_resource = from_literal("false")
    true_resource = from_literal("true")
    matcher.rule(
        name="false",
        when=(field.prop(init).eq(False),),
        resource=false_resource,
    )
    matcher.rule(
        name="true",
        when=(field.prop(init).eq(True),),
        resource=true_resource,
    )

    runtime = matcher.runtime()
    false_result = runtime.resolve(field_spec.record(name="count", init=False))
    true_result = runtime.resolve(field_spec.record(name="label", init=True))

    assert false_result is not None
    assert false_result.resource is false_resource
    assert true_result is not None
    assert true_result.resource is true_resource


def test_conflicting_conditions_inside_one_rule_reject() -> None:
    dds = DataDefinitionSystem()
    name = dds.property("Name", str, default=REQUIRED, storage_name="name")
    init = dds.property("Init", bool, default=True, storage_name="init")
    field_spec = dds.record("FieldSpec", name, init)
    fields = dds.collection("Fields", field_spec, cardinality=dds.many, identity=name)
    matcher = dds.matcher("Getter")
    field = matcher.input("field", fields)
    matcher.rule(
        name="impossible",
        when=(
            field.prop(init).eq(False),
            field.prop(init).eq(True),
        ),
        resource=from_literal("impossible"),
    )

    with pytest.raises(ValueError, match="conflicting conditions"):
        matcher.runtime()


def test_missing_variant_property_can_match_not_provided() -> None:
    dds = DataDefinitionSystem()
    name = dds.property("Name", str, default=REQUIRED, storage_name="name")
    tx_id = dds.property("TxId", int, default=REQUIRED, storage_name="tx_id")
    field_specs = dds.union("FieldSpecs")
    plain_field = field_specs.variant("PlainField", name)
    field_specs.variant("ManagedField", name, tx_id)
    fields = dds.collection("Fields", field_specs, cardinality=dds.many, identity=name)
    matcher = dds.matcher("Getter")
    field = matcher.input("field", fields)
    no_tx_resource = from_literal("no-tx")
    matcher.rule(
        name="no-tx",
        when=(field.prop(tx_id).eq(NOT_PROVIDED),),
        resource=no_tx_resource,
    )

    result = matcher.runtime().resolve(plain_field.record(name="count"))

    assert result is not None
    assert result.resource is no_tx_resource
    assert result.values == (NOT_PROVIDED,)


def test_default_resource_is_returned_when_no_rule_matches() -> None:
    dds = DataDefinitionSystem()
    name = dds.property("Name", str, default=REQUIRED, storage_name="name")
    init = dds.property("Init", bool, default=True, storage_name="init")
    field_spec = dds.record("FieldSpec", name, init)
    fields = dds.collection("Fields", field_spec, cardinality=dds.many, identity=name)
    matcher = dds.matcher("Getter")
    field = matcher.input("field", fields)
    default_resource = from_literal("default")
    matcher.default(default_resource)
    matcher.rule(
        name="not-init",
        when=(field.prop(init).eq(False),),
        resource=from_literal("not-init"),
    )

    result = matcher.runtime().resolve(field_spec.record(name="count", init=True))

    assert result is not None
    assert result.rule is None
    assert result.resource is default_resource
    assert result.score == 0.0


def test_evaluated_field_can_depend_on_multiple_inputs() -> None:
    dds = DataDefinitionSystem()
    field_name = dds.property("FieldName", str, default=REQUIRED, storage_name="field_name")
    facade_name = dds.property(
        "FacadeName",
        str,
        default=REQUIRED,
        storage_name="facade_name",
    )
    field_spec = dds.record("FieldSpec", field_name)
    facade_spec = dds.record("FacadeSpec", facade_name)
    fields = dds.collection(
        "Fields",
        field_spec,
        cardinality=dds.many,
        identity=field_name,
    )
    facades = dds.collection(
        "Facades",
        facade_spec,
        cardinality=dds.many,
        identity=facade_name,
    )
    matcher = dds.matcher("Visibility")
    field = matcher.input("field", fields)
    facade = matcher.input("facade", facades)
    visible = matcher.evaluated_field(
        "Visible",
        inputs=(field, facade),
        value=lambda field_record, facade_record: (
            field_record.field_name == "count"
            and facade_record.facade_name == "runtime"
        ),
        value_type=bool,
    )
    visible_resource = from_literal("visible")
    matcher.rule(
        name="visible",
        when=(visible.eq(True),),
        resource=visible_resource,
    )
    runtime = matcher.runtime()

    results = tuple(
        runtime.sequence(
            (
                field_spec.record(field_name="count"),
                field_spec.record(field_name="label"),
            ),
            (
                facade_spec.record(facade_name="runtime"),
                facade_spec.record(facade_name="debug"),
            ),
        )
    )

    assert len(results) == 1
    assert results[0].resource is visible_resource
    assert results[0].records[0].field_name == "count"
    assert results[0].records[1].facade_name == "runtime"
    assert results[0].values == (True,)


def test_matcher_cache_reuses_value_selection_for_equal_records() -> None:
    dds = DataDefinitionSystem()
    name = dds.property("Name", str, default=REQUIRED, storage_name="name")
    field_spec = dds.record("FieldSpec", name)
    fields = dds.collection("Fields", field_spec, cardinality=dds.many, identity=name)
    matcher = dds.matcher("Getter")
    field = matcher.input("field", fields)
    resource = from_literal("resource")
    matcher.rule(
        name="count",
        when=(field.prop(name).eq("count"),),
        resource=resource,
    )
    runtime = matcher.runtime()
    first_record = field_spec.record(name="count")
    second_record = field_spec.record(name="count")

    first = runtime.resolve(first_record)
    second = runtime.resolve(second_record)

    assert first is not None
    assert second is not None
    assert first is not second
    assert first.resource is resource
    assert second.resource is resource
    assert first.records == (first_record,)
    assert second.records == (second_record,)


def test_resources_are_returned_unchanged() -> None:
    dds = DataDefinitionSystem()
    name = dds.property("Name", str, default=REQUIRED, storage_name="name")
    field_spec = dds.record("FieldSpec", name)
    fields = dds.collection("Fields", field_spec, cardinality=dds.many, identity=name)
    matcher = dds.matcher("Getter")
    field = matcher.input("field", fields)
    resource = from_literal("resource")
    matcher.rule(
        name="count",
        when=(field.prop(name).eq("count"),),
        resource=resource,
    )

    result = matcher.runtime().resolve(field_spec.record(name="count"))

    assert result is not None
    assert result.resource is resource


def test_rule_resource_must_be_generated_value() -> None:
    dds = DataDefinitionSystem()
    name = dds.property("Name", str, default=REQUIRED, storage_name="name")
    field_spec = dds.record("FieldSpec", name)
    fields = dds.collection("Fields", field_spec, cardinality=dds.many, identity=name)
    matcher = dds.matcher("Getter")
    field = matcher.input("field", fields)

    with pytest.raises(TypeError, match="matcher rule resource"):
        matcher.rule(
            name="count",
            when=(field.prop(name).eq("count"),),
            resource=object(),
        )


def test_default_resource_must_be_generated_value() -> None:
    dds = DataDefinitionSystem()
    matcher = dds.matcher("Getter")

    with pytest.raises(TypeError, match="matcher default resource"):
        matcher.default(object())


def test_generated_value_caches_generator() -> None:
    value = from_literal("resource")

    first = value.to_generator()
    second = value.to_generator()

    assert first is second


def test_astichi_generated_values_keep_python_builtins_by_default() -> None:
    value = from_astichi_code(
        "@property\n"
        "def answer(self):\n"
        "    return len(())\n",
        keep_names=("custom_name",),
    )

    assert "property" in value.keep_names
    assert "len" in value.keep_names
    assert "custom_name" in value.keep_names
    assert set(PYTHON_BUILTIN_KEEP_NAMES) < set(value.keep_names)

    source = value.to_generator().materialize().emit(provenance=False)
    assert "@property" in source
    assert "property__astichi_scoped" not in source

    constructor_source = ast.unparse(constructor_expr_for(value))
    assert "keep_names=('custom_name',)" in constructor_source
