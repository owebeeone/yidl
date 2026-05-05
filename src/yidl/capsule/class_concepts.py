"""Reusable DDS concepts for class-shaped capsule generation."""

from __future__ import annotations

from yidl.generation.data_def_sys import DataDefinitionSystem
from yidl.generation.data_def_sys import REQUIRED


def name_prop(dds: DataDefinitionSystem) -> object:
    return dds.ensure_property("Name", str, default=REQUIRED, storage_name="name")


def init_prop(dds: DataDefinitionSystem) -> object:
    return dds.ensure_property("Init", bool, default=True, storage_name="init")


def kind_prop(dds: DataDefinitionSystem) -> object:
    return dds.ensure_property("Kind", str, default="plain", storage_name="kind")


def defaulted_prop(dds: DataDefinitionSystem) -> object:
    return dds.ensure_property(
        "Defaulted",
        bool,
        default=False,
        storage_name="defaulted",
    )


def default_value_prop(dds: DataDefinitionSystem) -> object:
    return dds.ensure_property(
        "DefaultValue",
        object,
        default=None,
        storage_name="default_value",
    )


def order_prop(dds: DataDefinitionSystem) -> object:
    return dds.ensure_property("Order", int, default=0, storage_name="order")


def target_port_prop(dds: DataDefinitionSystem) -> object:
    return dds.ensure_property(
        "TargetPort",
        object,
        default=REQUIRED,
        storage_name="target_port",
    )


def template_prop(dds: DataDefinitionSystem) -> object:
    return dds.ensure_property(
        "Template",
        object,
        default=REQUIRED,
        storage_name="template",
    )


def source_name_prop(dds: DataDefinitionSystem) -> object:
    return dds.ensure_property(
        "SourceName",
        str,
        default=REQUIRED,
        storage_name="source_name",
    )


def target_name_prop(dds: DataDefinitionSystem) -> object:
    return dds.ensure_property(
        "TargetName",
        str,
        default=REQUIRED,
        storage_name="target_name",
    )


def runtime_value_prop(dds: DataDefinitionSystem) -> object:
    return dds.ensure_property(
        "RuntimeValue",
        object,
        default=REQUIRED,
        storage_name="runtime_value",
    )


def class_value_record(dds: DataDefinitionSystem) -> object:
    return dds.ensure_record(
        "ClassValue",
        name_prop(dds),
        target_port_prop(dds),
        order_prop(dds),
        runtime_value_prop(dds),
    )


def field_input_record(dds: DataDefinitionSystem) -> object:
    return dds.ensure_record(
        "FieldInput",
        name_prop(dds),
        init_prop(dds),
        kind_prop(dds),
        defaulted_prop(dds),
        default_value_prop(dds),
        order_prop(dds),
    )


def component_record(dds: DataDefinitionSystem) -> object:
    return dds.ensure_record(
        "Component",
        name_prop(dds),
        target_port_prop(dds),
        order_prop(dds),
        template_prop(dds),
    )


def init_param_record(dds: DataDefinitionSystem) -> object:
    return dds.ensure_record(
        "InitParam",
        name_prop(dds),
        target_port_prop(dds),
        order_prop(dds),
        template_prop(dds),
        defaulted_prop(dds),
        default_value_prop(dds),
    )


def init_assignment_record(dds: DataDefinitionSystem) -> object:
    return dds.ensure_record(
        "InitAssignment",
        name_prop(dds),
        target_port_prop(dds),
        order_prop(dds),
        template_prop(dds),
        source_name_prop(dds),
        target_name_prop(dds),
    )


def class_values_collection(dds: DataDefinitionSystem) -> object:
    return dds.ensure_collection(
        "ClassValues",
        class_value_record(dds),
        cardinality=dds.many,
        identity=name_prop(dds),
    )


def fields_collection(dds: DataDefinitionSystem) -> object:
    return dds.ensure_collection(
        "Fields",
        field_input_record(dds),
        cardinality=dds.many,
        identity=name_prop(dds),
    )


def components_collection(dds: DataDefinitionSystem) -> object:
    return dds.ensure_collection(
        "Components",
        component_record(dds),
        cardinality=dds.many,
        identity=name_prop(dds),
    )


def init_params_collection(dds: DataDefinitionSystem) -> object:
    return dds.ensure_collection(
        "InitParams",
        init_param_record(dds),
        cardinality=dds.many,
        identity=name_prop(dds),
    )


def init_assignments_collection(dds: DataDefinitionSystem) -> object:
    return dds.ensure_collection(
        "InitAssignments",
        init_assignment_record(dds),
        cardinality=dds.many,
        identity=name_prop(dds),
    )


def init_fields_collection(dds: DataDefinitionSystem) -> object:
    return dds.ensure_computed_collection(
        "InitFields",
        source=fields_collection(dds),
        when=(init_prop(dds).eq(True),),
    )


def class_name_port(dds: DataDefinitionSystem) -> object:
    return dds.ensure_port("Class.name", cardinality=dds.single)


def class_body_port(dds: DataDefinitionSystem) -> object:
    return dds.ensure_port("Class.body", cardinality=dds.many)


def init_params_port(dds: DataDefinitionSystem) -> object:
    return dds.ensure_port("Init.params", cardinality=dds.many)


def init_body_port(dds: DataDefinitionSystem) -> object:
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


__all__ = [
    "class_body_port",
    "class_name_port",
    "class_value_record",
    "class_values_collection",
    "component_record",
    "components_collection",
    "default_value_prop",
    "defaulted_prop",
    "define_class_field_schema",
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
