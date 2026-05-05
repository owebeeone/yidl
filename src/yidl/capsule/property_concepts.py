"""Property capsule concepts selected by field kind."""

from __future__ import annotations

from collections.abc import Callable

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
from yidl.generation.data_def_sys import MatcherGeneratedValue


PLAIN_FIELD = "plain"
MANAGED_FIELD = "managed"

PLAIN_PROPERTY = from_astichi_code(
    "@property\n"
    "def field_name__astichi_arg__(self):\n"
    "    return self.astichi_ref(external=storage_path)\n"
    "\n"
    "@field_name__astichi_arg__.setter\n"
    "def field_name__astichi_arg__(self, value):\n"
    "    self.astichi_ref(external=storage_path)._ = value\n"
)
MANAGED_PROPERTY = from_astichi_code(
    "@property\n"
    "def field_name__astichi_arg__(self):\n"
    "    return self.astichi_ref(external=working_path)\n"
    "\n"
    "@field_name__astichi_arg__.setter\n"
    "def field_name__astichi_arg__(self, value):\n"
    "    self.astichi_ref(external=working_path)._ = value\n"
)

PROPERTY_TEMPLATE_VALUE_NAMES = (
    (PLAIN_PROPERTY, "PLAIN_PROPERTY"),
    (MANAGED_PROPERTY, "MANAGED_PROPERTY"),
)
PROPERTY_TEMPLATE_GLOBALS = {
    "PLAIN_PROPERTY": PLAIN_PROPERTY,
    "MANAGED_PROPERTY": MANAGED_PROPERTY,
}

PropertyTemplateBinder = Callable[[object], dict[str, object]]
_PROPERTY_TEMPLATE_BINDERS: dict[MatcherGeneratedValue, PropertyTemplateBinder] = {}


def register_property_template(
    template: MatcherGeneratedValue,
    binder: PropertyTemplateBinder,
) -> None:
    """Register edge bindings needed by a property component template."""

    existing = _PROPERTY_TEMPLATE_BINDERS.get(template)
    if existing is not None and existing is not binder:
        raise ValueError("property template is already registered differently")
    _PROPERTY_TEMPLATE_BINDERS[template] = binder


def property_order_for(result: object) -> int:
    return 100 + result.records[0].order


PROPERTY_EVALUATOR_NAMES = ((property_order_for, "property_order_for"),)
PROPERTY_EVALUATOR_GLOBALS = {"property_order_for": property_order_for}


def define_property_productions(dds: DataDefinitionSystem) -> None:
    """Define matcher-selected property class-body productions."""

    name = name_prop(dds)
    kind = kind_prop(dds)
    target_port = target_port_prop(dds)
    order = order_prop(dds)
    template = template_prop(dds)

    fields = fields_collection(dds)
    components = components_collection(dds)
    class_body = class_body_port(dds)

    property_template = dds.ensure_matcher("PropertyTemplate")
    field_input = property_template.ensure_input("field", fields)
    property_template.default(PLAIN_PROPERTY)
    property_template.rule(
        when=(field_input.prop(kind).eq(MANAGED_FIELD),),
        resource=MANAGED_PROPERTY,
        name="managed-property",
    )

    dds.ensure_production_group(
        "Properties",
        dds.production(
            "Property",
            source=property_template.results(),
            target=components,
            values={
                name: match.record("field").prop(name),
                target_port: class_body.of("runtime"),
                order: call("property-order", property_order_for),
                template: match.resource(),
            },
            policy=AddIfAbsent,
        ),
    )


def build_property_capsule_definition(
    name: str = "PropertyCapsule",
) -> CapsuleDefinition:
    """Build a capsule definition that emits property methods."""

    return capsule(
        name,
        concept("class-field-schema", define_class_field_schema),
        concept("property-productions", define_property_productions),
    )


def property_class_body_edge_plan() -> TemplateEdgePlan:
    """Return the class-body edge plan for property component templates."""

    return TemplateEdgePlan(
        "ClassBody",
        arg_names=_property_arg_names,
        bind=_property_bind,
    )


def _property_arg_names(record: object) -> dict[str, str]:
    if record.template not in _PROPERTY_TEMPLATE_BINDERS:
        return {}
    return {"field_name": record.name}


def _property_bind(record: object) -> dict[str, object]:
    binder = _PROPERTY_TEMPLATE_BINDERS.get(record.template)
    if binder is None:
        return {}
    return binder(record)


def _plain_property_bind(record: object) -> dict[str, object]:
    return {"storage_path": f"_{record.name}"}


def _managed_property_bind(record: object) -> dict[str, object]:
    return {"working_path": f"_{record.name}_working"}


register_property_template(PLAIN_PROPERTY, _plain_property_bind)
register_property_template(MANAGED_PROPERTY, _managed_property_bind)


__all__ = [
    "MANAGED_FIELD",
    "MANAGED_PROPERTY",
    "PLAIN_FIELD",
    "PLAIN_PROPERTY",
    "PROPERTY_EVALUATOR_GLOBALS",
    "PROPERTY_EVALUATOR_NAMES",
    "PROPERTY_TEMPLATE_GLOBALS",
    "PROPERTY_TEMPLATE_VALUE_NAMES",
    "build_property_capsule_definition",
    "define_property_productions",
    "property_class_body_edge_plan",
    "property_order_for",
    "register_property_template",
]
