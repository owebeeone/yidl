"""Property getter capsule concepts selected by field kind."""

from __future__ import annotations

from yidl.capsule.build_mapper import TemplateEdgePlan
from yidl.capsule.class_concepts import class_body_port
from yidl.capsule.class_concepts import components_collection
from yidl.capsule.class_concepts import define_class_field_schema
from yidl.capsule.class_concepts import fields_collection
from yidl.capsule.class_concepts import kind_prop
from yidl.capsule.class_concepts import name_prop
from yidl.capsule.class_concepts import order_prop
from yidl.capsule.class_concepts import target_port_prop
from yidl.capsule.class_concepts import template_prop
from yidl.capsule.definition import CapsuleDefinition
from yidl.capsule.definition import capsule
from yidl.capsule.definition import concept
from yidl.generation.data_def_sys import AddIfAbsent
from yidl.generation.data_def_sys import DataDefinitionSystem
from yidl.generation.data_def_sys import call
from yidl.generation.data_def_sys import from_astichi_code
from yidl.generation.data_def_sys import match


PLAIN_FIELD = "plain"
MANAGED_FIELD = "managed"

PLAIN_GETTER = from_astichi_code(
    "@property__astichi_keep__\n"
    "def field_name__astichi_arg__(self__astichi_keep__):\n"
    "    return self.astichi_ref(external=storage_path)\n"
)
MANAGED_GETTER = from_astichi_code(
    "@property__astichi_keep__\n"
    "def field_name__astichi_arg__(self__astichi_keep__):\n"
    "    return self.astichi_ref(external=working_path)\n"
)

GETTER_TEMPLATE_VALUE_NAMES = (
    (PLAIN_GETTER, "PLAIN_GETTER"),
    (MANAGED_GETTER, "MANAGED_GETTER"),
)
GETTER_TEMPLATE_GLOBALS = {
    "PLAIN_GETTER": PLAIN_GETTER,
    "MANAGED_GETTER": MANAGED_GETTER,
}


def getter_order_for(result: object) -> int:
    return 100 + result.records[0].order


GETTER_EVALUATOR_NAMES = ((getter_order_for, "getter_order_for"),)
GETTER_EVALUATOR_GLOBALS = {"getter_order_for": getter_order_for}


def define_getter_productions(dds: DataDefinitionSystem) -> None:
    """Define matcher-selected property getter class-body productions."""

    name = name_prop(dds)
    kind = kind_prop(dds)
    target_port = target_port_prop(dds)
    order = order_prop(dds)
    template = template_prop(dds)

    fields = fields_collection(dds)
    components = components_collection(dds)
    class_body = class_body_port(dds)

    getter_template = dds.ensure_matcher("GetterTemplate")
    field_input = getter_template.ensure_input("field", fields)
    getter_template.default(PLAIN_GETTER)
    getter_template.rule(
        when=(field_input.prop(kind).eq(MANAGED_FIELD),),
        resource=MANAGED_GETTER,
        name="managed-getter",
    )

    dds.ensure_production_group(
        "Getters",
        dds.production(
            "Getter",
            source=getter_template.results(),
            target=components,
            values={
                name: match.record("field").prop(name),
                target_port: class_body.of("runtime"),
                order: call("getter-order", getter_order_for),
                template: match.resource(),
            },
            policy=AddIfAbsent,
        ),
    )


def build_getter_capsule_definition(
    name: str = "GetterCapsule",
) -> CapsuleDefinition:
    """Build a capsule definition that emits property getter methods."""

    return capsule(
        name,
        concept("class-field-schema", define_class_field_schema),
        concept("getter-productions", define_getter_productions),
    )


def getter_class_body_edge_plan() -> TemplateEdgePlan:
    """Return the class-body edge plan for getter component templates."""

    return TemplateEdgePlan(
        "ClassBody",
        arg_names=_getter_arg_names,
        bind=_getter_bind,
    )


def _getter_arg_names(record: object) -> dict[str, str]:
    if record.template not in (PLAIN_GETTER, MANAGED_GETTER):
        return {}
    return {"field_name": record.name}


def _getter_bind(record: object) -> dict[str, object]:
    if record.template == PLAIN_GETTER:
        return {"storage_path": f"_{record.name}"}
    if record.template == MANAGED_GETTER:
        return {"working_path": f"_{record.name}_working"}
    return {}


__all__ = [
    "GETTER_EVALUATOR_GLOBALS",
    "GETTER_EVALUATOR_NAMES",
    "GETTER_TEMPLATE_GLOBALS",
    "GETTER_TEMPLATE_VALUE_NAMES",
    "MANAGED_FIELD",
    "MANAGED_GETTER",
    "PLAIN_FIELD",
    "PLAIN_GETTER",
    "build_getter_capsule_definition",
    "define_getter_productions",
    "getter_class_body_edge_plan",
    "getter_order_for",
]
