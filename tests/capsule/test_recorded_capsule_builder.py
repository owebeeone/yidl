from __future__ import annotations

import ast

import pytest

from yidl.capsule.recorded_builder import CapsuleConceptBuilder
from yidl.capsule.recorded_builder import capsule_concept
from yidl.capsule.recorded_builder import match
from yidl.generation.data_def_sys import AddIfAbsent
from yidl.generation.data_def_sys import call
from yidl.generation.data_def_sys import DataDefinitionSystem
from yidl.generation.data_def_sys import REQUIRED
from yidl.generation.data_def_sys import from_literal


def test_recorded_concept_plan_replays_property_definitions() -> None:
    builder = capsule_concept("property")
    name = builder.props.Name(str, REQUIRED)
    init = builder.props.Init(bool)

    plan = builder.build()
    dds = DataDefinitionSystem()
    plan.apply(dds)

    assert isinstance(builder, CapsuleConceptBuilder)
    assert name.name == "Name"
    assert init.name == "Init"
    assert [(prop.name, prop.storage_name, prop.default) for prop in dds.properties] == [
        ("Name", "name", REQUIRED),
        ("Init", "init", False),
    ]


def test_recorded_concept_builder_cannot_be_replayed_directly() -> None:
    builder = capsule_concept("property")
    builder.props.Name(str, REQUIRED)

    with pytest.raises(TypeError, match="build"):
        builder.apply(DataDefinitionSystem())  # type: ignore[attr-defined]


def test_recorded_concept_plan_is_immutable_after_build() -> None:
    builder = capsule_concept("property")
    builder.props.Name(str, REQUIRED)

    plan = builder.build()

    with pytest.raises(RuntimeError, match="already been built"):
        builder.props.Init(bool)

    dds = DataDefinitionSystem()
    plan.apply(dds)
    assert [prop.name for prop in dds.properties] == ["Name"]


def test_extension_reference_reuses_parent_property_without_redefinition() -> None:
    parent = capsule_concept("property")
    parent_name = parent.props.Name(str, REQUIRED)
    parent_plan = parent.build()

    child = capsule_concept("frozen", extends=(parent_plan,))
    parent_ref = child.use(parent_plan)
    referenced_name = parent_ref.props.Name
    frozen = child.props.Frozen(bool)
    child_plan = child.build()

    dds = DataDefinitionSystem()
    child_plan.apply(dds)

    assert referenced_name == parent_name
    assert [prop.name for prop in dds.properties] == ["Name", "Frozen"]
    assert frozen.name == "Frozen"


def test_extension_diamond_replays_parent_once() -> None:
    root = capsule_concept("root")
    root.props.Name(str, REQUIRED)
    root_plan = root.build()

    left = capsule_concept("left", extends=(root_plan,))
    left.props.Left(bool)
    left_plan = left.build()

    right = capsule_concept("right", extends=(root_plan,))
    right.props.Right(bool)
    right_plan = right.build()

    child = capsule_concept("child", extends=(left_plan, right_plan))
    child.props.Child(bool)
    child_plan = child.build()

    dds = DataDefinitionSystem()
    child_plan.apply(dds)

    assert [prop.name for prop in dds.properties] == [
        "Name",
        "Left",
        "Right",
        "Child",
    ]


def test_redefining_extension_owned_property_rejects() -> None:
    parent = capsule_concept("property")
    parent.props.Name(str, REQUIRED)
    parent_plan = parent.build()

    child = capsule_concept("frozen", extends=(parent_plan,))
    child.props.Name(str, REQUIRED)
    child_plan = child.build()

    with pytest.raises(ValueError, match="property 'Name' is already owned"):
        child_plan.apply(DataDefinitionSystem())


def test_conflicting_property_definitions_reject() -> None:
    left = capsule_concept("left")
    left.props.Name(str, REQUIRED)
    left_plan = left.build()

    right = capsule_concept("right")
    right.props.Name(int, REQUIRED)
    right_plan = right.build()

    child = capsule_concept("child", extends=(left_plan, right_plan))
    child_plan = child.build()

    with pytest.raises(ValueError, match="property 'Name' is already owned"):
        child_plan.apply(DataDefinitionSystem())


def test_recorded_concept_plan_replays_records_collections_and_ports() -> None:
    builder = capsule_concept("class")
    name = builder.props.Name(str, REQUIRED)
    init = builder.props.Init(bool)
    target = builder.props.Target(object, REQUIRED)
    order = builder.props.Order(int)
    field_input = builder.records.FieldInput(name, init)
    fields = builder.collections.Fields(
        field_input,
        cardinality=builder.many,
        identity=name,
    )
    builder.computed.InitFields(source=fields, when=(init.eq(True),))
    class_body = builder.ports.Class.body(cardinality=builder.many)
    builder.port_index(target=target, order=order)

    plan = builder.build()
    assert plan.ports.Class.body == class_body

    dds = DataDefinitionSystem()
    plan.apply(dds)

    assert [record.name for record in dds.records] == ["FieldInput"]
    assert [prop.name for prop in dds.records[0].properties] == ["Name", "Init"]
    assert [collection.name for collection in dds.collections] == ["Fields"]
    assert [collection.name for collection in dds.computed_collections] == [
        "InitFields"
    ]
    assert [port.name for port in dds.ports] == ["Class.body"]
    assert dds.port_index_spec is not None
    assert dds.port_index_spec.target.name == "Target"
    assert dds.port_index_spec.order.name == "Order"


def test_extension_record_extension_uses_parent_record_handle() -> None:
    parent = capsule_concept("property")
    name = parent.props.Name(str, REQUIRED)
    field_input = parent.records.FieldInput(name)
    fields = parent.collections.Fields(
        field_input,
        cardinality=parent.many,
        identity=name,
    )
    parent_plan = parent.build()

    child = capsule_concept("frozen", extends=(parent_plan,))
    parent_ref = child.use(parent_plan)
    frozen = child.props.Frozen(bool)
    child.extend_record(parent_ref.records.FieldInput, frozen)
    child.computed.FrozenFields(
        source=parent_ref.collections.Fields,
        when=(frozen.eq(True),),
    )

    dds = DataDefinitionSystem()
    child.build().apply(dds)

    assert fields.name == "Fields"
    assert [prop.name for prop in dds.records[0].properties] == [
        "Name",
        "Frozen",
    ]
    assert [collection.name for collection in dds.computed_collections] == [
        "FrozenFields"
    ]


def test_child_redefining_extension_record_rejects() -> None:
    parent = capsule_concept("property")
    name = parent.props.Name(str, REQUIRED)
    parent.records.FieldInput(name)
    parent_plan = parent.build()

    child = capsule_concept("frozen", extends=(parent_plan,))
    parent_ref = child.use(parent_plan)
    frozen = child.props.Frozen(bool)
    assert parent_ref.records.FieldInput.name == "FieldInput"
    child.records.FieldInput(frozen)

    with pytest.raises(ValueError, match="record 'FieldInput' is already owned"):
        child.build().apply(DataDefinitionSystem())


def test_unknown_extension_reference_rejects() -> None:
    parent = capsule_concept("property")
    parent_plan = parent.build()
    other = capsule_concept("other")
    other_plan = other.build()

    child = capsule_concept("frozen", extends=(parent_plan,))

    with pytest.raises(ValueError, match="not in the extension closure"):
        child.use(other_plan)


def test_recorded_matcher_production_replays_to_generated_runtime() -> None:
    builder = capsule_concept("property")
    name = builder.props.Name(str, REQUIRED)
    kind = builder.props.Kind(str, "plain")
    template = builder.props.Template(object, REQUIRED)
    field_input = builder.records.FieldInput(name, kind)
    fields = builder.collections.Fields(
        field_input,
        cardinality=builder.many,
        identity=name,
    )
    component = builder.records.Component(name, template)
    components = builder.collections.Components(
        component,
        cardinality=builder.many,
        identity=name,
    )

    property_template = builder.matchers.PropertyTemplate()
    field = property_template.input.field(fields)
    property_template.default(from_literal("plain-property"))
    property_template.rule.managed(
        when=(field.prop(kind).eq("managed"),),
        resource=from_literal("managed-property"),
    )
    builder.productions.Property(
        source=property_template.results(),
        target=components,
        values={
            name: match.record("field").prop(name),
            template: match.resource(),
        },
        policy=AddIfAbsent,
    ).in_group("Properties")

    dds = DataDefinitionSystem()
    builder.build().apply(dds)
    source = dds.emit_container_runtime_source()
    namespace: dict[str, object] = {}
    exec(compile(source, "<recorded-property-runtime>", "exec"), namespace)

    runtime_builder = namespace["new_builder"]()
    field_class = namespace["FieldInput"]
    fields_collection = namespace["FieldsCollection"]
    runtime_builder.add(
        fields_collection,
        field_class(name="count", kind="plain"),
    )
    runtime_builder.add(
        fields_collection,
        field_class(name="owner", kind="managed"),
    )
    container = namespace["build_container"](runtime_builder)

    components_collection = namespace["ComponentsCollection"]
    rendered = [
        (
            record.name,
            ast.literal_eval(
                record.template.to_generator()
                .materialize()
                .emit(provenance=False)
                .strip()
            ),
        )
        for record in container.Components.sequence()
    ]
    assert components_collection.name == "Components"
    assert rendered == [
        ("count", "plain-property"),
        ("owner", "managed-property"),
    ]


def test_recorded_production_group_accumulates_same_name_memberships() -> None:
    builder = capsule_concept("grouped")
    name = builder.props.Name(str, REQUIRED)
    value = builder.props.Value(str, REQUIRED)
    source_record = builder.records.Source(name)
    sources = builder.collections.Sources(
        source_record,
        cardinality=builder.many,
        identity=name,
    )
    target_record = builder.records.Target(name, value)
    targets = builder.collections.Targets(
        target_record,
        cardinality=builder.many,
        identity=name,
    )
    builder.productions.First(
        source=sources,
        target=targets,
        values={name: name.read(), value: "first"},
        policy=AddIfAbsent,
    ).in_group("Targets")
    builder.productions.Second(
        source=sources,
        target=targets,
        values={name: name.read(), value: "second"},
        policy=AddIfAbsent,
    ).in_group("Targets")

    plan = builder.build()
    assert [
        (group.name, [production.name for production in group.productions])
        for group in plan.production_groups
    ] == [("Targets", ["First", "Second"])]

    dds = DataDefinitionSystem()
    plan.apply(dds)
    assert [
        (group.name, [production.name for production in group.productions])
        for group in dds.production_groups
    ] == [("Targets", ["First", "Second"])]


def test_child_concept_adds_rule_to_extension_owned_matcher() -> None:
    parent = capsule_concept("property")
    name = parent.props.Name(str, REQUIRED)
    kind = parent.props.Kind(str, "plain")
    field_input = parent.records.FieldInput(name, kind)
    fields = parent.collections.Fields(
        field_input,
        cardinality=parent.many,
        identity=name,
    )
    parent_template = parent.matchers.PropertyTemplate()
    parent_field = parent_template.input.field(fields)
    assert parent_field.name == "field"
    parent_template.default(from_literal("plain-property"))
    parent_plan = parent.build()

    child = capsule_concept("frozen", extends=(parent_plan,))
    parent_ref = child.use(parent_plan)
    frozen = child.props.Frozen(bool)
    child.extend_record(parent_ref.records.FieldInput, frozen)
    child_template = child.use_matcher(parent_ref.matchers.PropertyTemplate)
    child_field = child_template.input.field(parent_ref.collections.Fields)
    child_template.rule.readonly(
        when=(child_field.prop(frozen).eq(True),),
        resource=from_literal("readonly-property"),
    )

    dds = DataDefinitionSystem()
    child.build().apply(dds)
    matcher = dds.matchers[0]

    assert matcher.name == "PropertyTemplate"
    assert [input_spec.name for input_spec in matcher.inputs] == ["field"]
    assert matcher.rules[0].name == "readonly"


def test_recorded_concept_runtime_loads_registered_evaluators() -> None:
    def value_for(source: object) -> int:
        return len(source.name)

    builder = capsule_concept("values")
    name = builder.props.Name(str, REQUIRED)
    value = builder.props.Value(int, REQUIRED)
    source_record = builder.records.Source(name)
    sources = builder.collections.Sources(
        source_record,
        cardinality=builder.many,
        identity=name,
    )
    target_record = builder.records.Target(name, value)
    targets = builder.collections.Targets(
        target_record,
        cardinality=builder.many,
        identity=name,
    )
    builder.productions.TargetValue(
        source=sources,
        target=targets,
        values={name: name.read(), value: call("value-for", value_for)},
        policy=AddIfAbsent,
    ).in_group("Targets")
    builder.runtime.evaluator(value_for, name="value_for")

    runtime = builder.build().runtime().load()
    namespace = runtime.namespace
    runtime_builder = runtime.new_builder()
    runtime_builder.add(
        namespace["SourcesCollection"],
        namespace["Source"](name="count"),
    )
    container = runtime.build_container(runtime_builder)

    assert [(record.name, record.value) for record in container.Targets.sequence()] == [
        ("count", 5)
    ]


def test_recorded_concept_runtime_rejects_conflicting_helper_names() -> None:
    def left_helper(source: object) -> int:
        del source
        return 1

    def right_helper(source: object) -> int:
        del source
        return 2

    left = capsule_concept("left")
    left.runtime.evaluator(left_helper, name="value_for")
    left_plan = left.build()

    right = capsule_concept("right")
    right.runtime.evaluator(right_helper, name="value_for")
    right_plan = right.build()

    child = capsule_concept("child", extends=(left_plan, right_plan))

    with pytest.raises(ValueError, match="runtime helper 'value_for'"):
        child.build().runtime().load()
