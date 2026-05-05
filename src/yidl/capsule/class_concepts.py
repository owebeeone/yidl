"""Reusable DDS concepts for class-shaped capsule generation."""

from __future__ import annotations

from collections.abc import Sequence
from functools import cache
from weakref import WeakKeyDictionary

from yidl.generation.data_def_sys import CollectionSpec
from yidl.generation.data_def_sys import ComputedCollectionSpec
from yidl.generation.data_def_sys import DataDefinitionSystem
from yidl.generation.data_def_sys import PortSpec
from yidl.generation.data_def_sys import PropertySpec
from yidl.generation.data_def_sys import REQUIRED
from yidl.generation.data_def_sys import RecordSpec
from yidl.capsule.recorded_builder import CapsuleConceptPlan
from yidl.capsule.recorded_builder import capsule_concept

_FIELD_INPUT_EXTENSIONS: WeakKeyDictionary[
    DataDefinitionSystem,
    tuple[PropertySpec, ...],
] = WeakKeyDictionary()
def name_prop(dds: DataDefinitionSystem) -> PropertySpec:
    return dds.ensure_property("Name", str, default=REQUIRED, storage_name="name")


def init_prop(dds: DataDefinitionSystem) -> PropertySpec:
    return dds.ensure_property("Init", bool, default=True, storage_name="init")


def kind_prop(dds: DataDefinitionSystem) -> PropertySpec:
    return dds.ensure_property("Kind", str, default="plain", storage_name="kind")


def defaulted_prop(dds: DataDefinitionSystem) -> PropertySpec:
    return dds.ensure_property(
        "Defaulted",
        bool,
        default=False,
        storage_name="defaulted",
    )


def default_value_prop(dds: DataDefinitionSystem) -> PropertySpec:
    return dds.ensure_property(
        "DefaultValue",
        object,
        default=None,
        storage_name="default_value",
    )


def order_prop(dds: DataDefinitionSystem) -> PropertySpec:
    return dds.ensure_property("Order", int, default=0, storage_name="order")


def target_port_prop(dds: DataDefinitionSystem) -> PropertySpec:
    return dds.ensure_property(
        "TargetPort",
        object,
        default=REQUIRED,
        storage_name="target_port",
    )


def template_prop(dds: DataDefinitionSystem) -> PropertySpec:
    return dds.ensure_property(
        "Template",
        object,
        default=REQUIRED,
        storage_name="template",
    )


def source_name_prop(dds: DataDefinitionSystem) -> PropertySpec:
    return dds.ensure_property(
        "SourceName",
        str,
        default=REQUIRED,
        storage_name="source_name",
    )


def target_name_prop(dds: DataDefinitionSystem) -> PropertySpec:
    return dds.ensure_property(
        "TargetName",
        str,
        default=REQUIRED,
        storage_name="target_name",
    )


def runtime_value_prop(dds: DataDefinitionSystem) -> PropertySpec:
    return dds.ensure_property(
        "RuntimeValue",
        object,
        default=REQUIRED,
        storage_name="runtime_value",
    )


def extend_field_input_record(
    dds: DataDefinitionSystem,
    *properties: PropertySpec,
) -> None:
    """Allow capsule concepts to add semantic fields to ``FieldInput``."""

    extensions = _FIELD_INPUT_EXTENSIONS.get(dds, ())
    additions = _new_field_input_properties(dds, extensions, properties)
    if not additions:
        return
    _FIELD_INPUT_EXTENSIONS[dds] = (*extensions, *additions)
    existing = _record_named(dds, "FieldInput")
    if existing is not None:
        _append_record_properties(existing, additions)


def class_value_record(dds: DataDefinitionSystem) -> RecordSpec:
    return dds.ensure_record(
        "ClassValue",
        name_prop(dds),
        target_port_prop(dds),
        order_prop(dds),
        runtime_value_prop(dds),
    )


def field_input_record(dds: DataDefinitionSystem) -> RecordSpec:
    return dds.ensure_record(
        "FieldInput",
        name_prop(dds),
        init_prop(dds),
        kind_prop(dds),
        defaulted_prop(dds),
        default_value_prop(dds),
        order_prop(dds),
        *_field_input_extensions(dds),
    )


def component_record(dds: DataDefinitionSystem) -> RecordSpec:
    return dds.ensure_record(
        "Component",
        name_prop(dds),
        target_port_prop(dds),
        order_prop(dds),
        template_prop(dds),
    )


def init_param_record(dds: DataDefinitionSystem) -> RecordSpec:
    return dds.ensure_record(
        "InitParam",
        name_prop(dds),
        target_port_prop(dds),
        order_prop(dds),
        template_prop(dds),
        defaulted_prop(dds),
        default_value_prop(dds),
    )


def init_assignment_record(dds: DataDefinitionSystem) -> RecordSpec:
    return dds.ensure_record(
        "InitAssignment",
        name_prop(dds),
        target_port_prop(dds),
        order_prop(dds),
        template_prop(dds),
        source_name_prop(dds),
        target_name_prop(dds),
    )


def class_values_collection(dds: DataDefinitionSystem) -> CollectionSpec:
    return dds.ensure_collection(
        "ClassValues",
        class_value_record(dds),
        cardinality=dds.many,
        identity=name_prop(dds),
    )


def fields_collection(dds: DataDefinitionSystem) -> CollectionSpec:
    return dds.ensure_collection(
        "Fields",
        field_input_record(dds),
        cardinality=dds.many,
        identity=name_prop(dds),
    )


def components_collection(dds: DataDefinitionSystem) -> CollectionSpec:
    return dds.ensure_collection(
        "Components",
        component_record(dds),
        cardinality=dds.many,
        identity=name_prop(dds),
    )


def init_params_collection(dds: DataDefinitionSystem) -> CollectionSpec:
    return dds.ensure_collection(
        "InitParams",
        init_param_record(dds),
        cardinality=dds.many,
        identity=name_prop(dds),
    )


def init_assignments_collection(dds: DataDefinitionSystem) -> CollectionSpec:
    return dds.ensure_collection(
        "InitAssignments",
        init_assignment_record(dds),
        cardinality=dds.many,
        identity=name_prop(dds),
    )


def init_fields_collection(dds: DataDefinitionSystem) -> ComputedCollectionSpec:
    return dds.ensure_computed_collection(
        "InitFields",
        source=fields_collection(dds),
        when=(init_prop(dds).eq(True),),
    )


def class_name_port(dds: DataDefinitionSystem) -> PortSpec:
    return dds.ensure_port("Class.name", cardinality=dds.single)


def class_body_port(dds: DataDefinitionSystem) -> PortSpec:
    return dds.ensure_port("Class.body", cardinality=dds.many)


def init_params_port(dds: DataDefinitionSystem) -> PortSpec:
    return dds.ensure_port("Init.params", cardinality=dds.many)


def init_body_port(dds: DataDefinitionSystem) -> PortSpec:
    return dds.ensure_port("Init.body", cardinality=dds.many)


def define_class_field_schema(dds: DataDefinitionSystem) -> None:
    """Define the common class, field, component, and init port surfaces."""

    class_values_collection(dds)
    fields_collection(dds)
    components_collection(dds)
    init_params_collection(dds)
    init_assignments_collection(dds)
    init_fields_collection(dds)
    class_name_port(dds)
    class_body_port(dds)
    init_params_port(dds)
    init_body_port(dds)
    dds.ensure_port_index(target=target_port_prop(dds), order=order_prop(dds))


@cache
def build_class_field_schema_concept() -> CapsuleConceptPlan:
    """Build the recorded common class/field schema concept."""

    builder = capsule_concept("class-field-schema")
    name = builder.props.Name(str, REQUIRED)
    init = builder.props.Init(bool, True)
    kind = builder.props.Kind(str, "plain")
    defaulted = builder.props.Defaulted(bool)
    default_value = builder.props.DefaultValue(object, None)
    order = builder.props.Order(int)
    target_port = builder.props.TargetPort(object, REQUIRED)
    template = builder.props.Template(object, REQUIRED)
    source_name = builder.props.SourceName(str, REQUIRED)
    target_name = builder.props.TargetName(str, REQUIRED)
    runtime_value = builder.props.RuntimeValue(object, REQUIRED)

    class_value = builder.records.ClassValue(
        name,
        target_port,
        order,
        runtime_value,
    )
    field_input = builder.records.FieldInput(
        name,
        init,
        kind,
        defaulted,
        default_value,
        order,
    )
    component = builder.records.Component(name, target_port, order, template)
    init_param = builder.records.InitParam(
        name,
        target_port,
        order,
        template,
        defaulted,
        default_value,
    )
    init_assignment = builder.records.InitAssignment(
        name,
        target_port,
        order,
        template,
        source_name,
        target_name,
    )

    builder.collections.ClassValues(
        class_value,
        cardinality=builder.many,
        identity=name,
    )
    fields = builder.collections.Fields(
        field_input,
        cardinality=builder.many,
        identity=name,
    )
    builder.collections.Components(
        component,
        cardinality=builder.many,
        identity=name,
    )
    builder.collections.InitParams(
        init_param,
        cardinality=builder.many,
        identity=name,
    )
    builder.collections.InitAssignments(
        init_assignment,
        cardinality=builder.many,
        identity=name,
    )
    builder.computed.InitFields(source=fields, when=(init.eq(True),))
    builder.ports.Class.name(cardinality=builder.single)
    builder.ports.Class.body(cardinality=builder.many)
    builder.ports.Init.params(cardinality=builder.many)
    builder.ports.Init.body(cardinality=builder.many)
    builder.port_index(target=target_port, order=order)

    return builder.build()


def _field_input_extensions(dds: DataDefinitionSystem) -> tuple[PropertySpec, ...]:
    return _FIELD_INPUT_EXTENSIONS.get(dds, ())


def _new_field_input_properties(
    dds: DataDefinitionSystem,
    existing: Sequence[PropertySpec],
    properties: Sequence[PropertySpec],
) -> tuple[PropertySpec, ...]:
    additions = []
    for prop in properties:
        if getattr(prop, "system", None) is not dds:
            raise ValueError("field-input extension properties must belong to this DDS")
        if prop in existing or prop in additions:
            continue
        additions.append(prop)
    return tuple(additions)


def _record_named(dds: DataDefinitionSystem, name: str) -> RecordSpec | None:
    for record in dds.records:
        if record.name == name:
            return record
    return None


def _append_record_properties(
    record: RecordSpec,
    properties: Sequence[PropertySpec],
) -> None:
    record.extend_properties(*properties)


__all__ = [
    "class_body_port",
    "class_name_port",
    "class_value_record",
    "class_values_collection",
    "component_record",
    "components_collection",
    "build_class_field_schema_concept",
    "default_value_prop",
    "defaulted_prop",
    "define_class_field_schema",
    "extend_field_input_record",
    "field_input_record",
    "fields_collection",
    "init_assignment_record",
    "init_assignments_collection",
    "init_body_port",
    "init_fields_collection",
    "init_param_record",
    "init_params_collection",
    "init_params_port",
    "init_prop",
    "kind_prop",
    "name_prop",
    "order_prop",
    "runtime_value_prop",
    "source_name_prop",
    "target_name_prop",
    "target_port_prop",
    "template_prop",
]
