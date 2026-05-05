"""Init-method capsule concepts built from DDS and Astichi templates."""

from __future__ import annotations

from yidl.capsule.build_mapper import CapsuleClassBuildPlan
from yidl.capsule.build_mapper import ChildPortPlan
from yidl.capsule.build_mapper import RuntimePortRef
from yidl.capsule.build_mapper import TemplateEdgePlan
from yidl.capsule.class_concepts import class_body_port
from yidl.capsule.class_concepts import class_values_collection
from yidl.capsule.class_concepts import components_collection
from yidl.capsule.class_concepts import default_value_prop
from yidl.capsule.class_concepts import defaulted_prop
from yidl.capsule.class_concepts import define_class_field_schema
from yidl.capsule.class_concepts import init_assignments_collection
from yidl.capsule.class_concepts import init_body_port
from yidl.capsule.class_concepts import init_fields_collection
from yidl.capsule.class_concepts import init_params_collection
from yidl.capsule.class_concepts import init_params_port
from yidl.capsule.class_concepts import name_prop
from yidl.capsule.class_concepts import order_prop
from yidl.capsule.class_concepts import source_name_prop
from yidl.capsule.class_concepts import target_name_prop
from yidl.capsule.class_concepts import target_port_prop
from yidl.capsule.class_concepts import template_prop
from yidl.capsule.definition import CapsuleDefinition
from yidl.capsule.definition import capsule
from yidl.capsule.definition import concept
from yidl.generation.data_def_sys import AddIfAbsent
from yidl.generation.data_def_sys import DataDefinitionSystem
from yidl.generation.data_def_sys import from_astichi_code
from yidl.generation.data_def_sys import match
from yidl.generation.data_def_sys import read


INIT_METHOD = from_astichi_code(
    "def __init__(self, params__astichi_param_hole__):\n"
    "    astichi_hole(body)\n"
)
REQUIRED_PARAM = from_astichi_code(
    "def astichi_params(*, field_name__astichi_arg__):\n"
    "    pass\n"
)
DEFAULTED_PARAM = from_astichi_code(
    "def astichi_params(\n"
    "    *,\n"
    "    field_name__astichi_arg__=astichi_bind_external(default_value),\n"
    "):\n"
    "    pass\n"
)
ASSIGNMENT = from_astichi_code(
    "astichi_import(self)\n"
    "self.astichi_ref(external=target_path)._ = astichi_pass(\n"
    "    source_name,\n"
    "    outer_bind=True,\n"
    ")\n"
)

INIT_TEMPLATE_VALUE_NAMES = (
    (INIT_METHOD, "INIT_METHOD"),
    (ASSIGNMENT, "ASSIGNMENT"),
)
INIT_TEMPLATE_GLOBALS = {
    "INIT_METHOD": INIT_METHOD,
    "ASSIGNMENT": ASSIGNMENT,
}


def define_init_productions(dds: DataDefinitionSystem) -> None:
    """Define the first init-method production graph."""

    name = name_prop(dds)
    order = order_prop(dds)
    defaulted = defaulted_prop(dds)
    default_value = default_value_prop(dds)
    target_port = target_port_prop(dds)
    template = template_prop(dds)
    source_name = source_name_prop(dds)
    target_name = target_name_prop(dds)

    init_fields = init_fields_collection(dds)
    class_values = class_values_collection(dds)
    components = components_collection(dds)
    params = init_params_collection(dds)
    assignments = init_assignments_collection(dds)
    class_body = class_body_port(dds)
    init_params = init_params_port(dds)
    init_body = init_body_port(dds)

    param_template = dds.ensure_matcher("InitParamTemplate")
    field_input = param_template.ensure_input("field", init_fields)
    param_template.default(REQUIRED_PARAM)
    param_template.rule(
        when=(field_input.prop(defaulted).eq(True),),
        resource=DEFAULTED_PARAM,
        name="defaulted-param",
    )

    dds.ensure_production_group(
        "Class",
        dds.production(
            "InitMethod",
            source=class_values,
            target=components,
            values={
                name: "__init__",
                target_port: class_body.of("runtime"),
                order: 0,
                template: INIT_METHOD,
            },
            policy=AddIfAbsent,
        ),
        dds.production(
            "InitParam",
            source=param_template.results(),
            target=params,
            values={
                name: match.record("field").prop(name),
                target_port: init_params.of(("runtime", "__init__")),
                order: match.record("field").prop(order),
                template: match.resource(),
                defaulted: match.value(0),
                default_value: match.record("field").prop(default_value),
            },
            policy=AddIfAbsent,
        ),
        dds.production(
            "InitAssignment",
            source=init_fields,
            target=assignments,
            values={
                name: read(name),
                target_port: init_body.of(("runtime", "__init__")),
                order: read(order),
                template: ASSIGNMENT,
                source_name: read(name),
                target_name: read(name),
            },
            policy=AddIfAbsent,
        ),
    )


def build_init_capsule_definition(
    name: str = "InitCapsule",
) -> CapsuleDefinition:
    """Build the DDS capsule definition for the current init-method slice."""

    return capsule(
        name,
        concept("class-field-schema", define_class_field_schema),
        concept("init-productions", define_init_productions),
    )


def init_class_build_plan() -> CapsuleClassBuildPlan:
    """Return the mapper plan for class + init-method source emission."""

    return CapsuleClassBuildPlan(
        class_name=RuntimePortRef("ClassNamePort", "runtime"),
        class_body=RuntimePortRef("ClassBodyPort", "runtime"),
        child_ports=(
            ChildPortPlan(
                parent_name="__init__",
                port_name="InitParamsPort",
                target_hole="params",
                edge=TemplateEdgePlan(
                    "InitParam",
                    arg_names=lambda record: {"field_name": record.name},
                    bind=lambda record: (
                        {"default_value": record.default_value}
                        if record.defaulted
                        else {}
                    ),
                ),
            ),
            ChildPortPlan(
                parent_name="__init__",
                port_name="InitBodyPort",
                target_hole="body",
                edge=TemplateEdgePlan(
                    "InitBody",
                    arg_names=lambda record: {"source_name": record.source_name},
                    bind=lambda record: {"target_path": record.target_name},
                ),
            ),
        ),
    )


__all__ = [
    "ASSIGNMENT",
    "DEFAULTED_PARAM",
    "INIT_METHOD",
    "INIT_TEMPLATE_GLOBALS",
    "INIT_TEMPLATE_VALUE_NAMES",
    "REQUIRED_PARAM",
    "build_init_capsule_definition",
    "define_init_productions",
    "init_class_build_plan",
]
