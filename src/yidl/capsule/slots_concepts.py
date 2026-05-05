"""``__slots__`` capsule concepts built from DDS and Astichi templates."""

from __future__ import annotations

from yidl.capsule.build_mapper import CapsuleClassBuildPlan
from yidl.capsule.build_mapper import ChildPortPlan
from yidl.capsule.build_mapper import RuntimePortRef
from yidl.capsule.build_mapper import TemplateEdgePlan
from yidl.capsule.class_concepts import class_body_port
from yidl.capsule.class_concepts import class_values_collection
from yidl.capsule.class_concepts import components_collection
from yidl.capsule.class_concepts import define_class_field_schema
from yidl.capsule.class_concepts import fields_collection
from yidl.capsule.class_concepts import name_prop
from yidl.capsule.class_concepts import order_prop
from yidl.capsule.class_concepts import target_port_prop
from yidl.capsule.class_concepts import template_prop
from yidl.capsule.definition import CapsuleDefinition
from yidl.capsule.definition import capsule
from yidl.capsule.definition import concept
from yidl.generation.data_def_sys import AddIfAbsent
from yidl.generation.data_def_sys import CollectionSpec
from yidl.generation.data_def_sys import DataDefinitionSystem
from yidl.generation.data_def_sys import PortSpec
from yidl.generation.data_def_sys import PropertySpec
from yidl.generation.data_def_sys import REQUIRED
from yidl.generation.data_def_sys import RecordSpec
from yidl.generation.data_def_sys import from_astichi_code
from yidl.generation.data_def_sys import read


SLOTS_CLASSVAR = from_astichi_code(
    "__slots__ = (*astichi_hole(items),)\n"
)
SLOT_ITEM = from_astichi_code(
    "astichi_bind_external(slot_name)\n"
    "slot_name\n"
)

SLOTS_TEMPLATE_VALUE_NAMES = (
    (SLOTS_CLASSVAR, "SLOTS_CLASSVAR"),
    (SLOT_ITEM, "SLOT_ITEM"),
)
SLOTS_TEMPLATE_GLOBALS = {
    "SLOTS_CLASSVAR": SLOTS_CLASSVAR,
    "SLOT_ITEM": SLOT_ITEM,
}


def slot_name_prop(dds: DataDefinitionSystem) -> PropertySpec:
    return dds.ensure_property(
        "SlotName",
        str,
        default=REQUIRED,
        storage_name="slot_name",
    )


def slot_item_record(dds: DataDefinitionSystem) -> RecordSpec:
    return dds.ensure_record(
        "SlotItem",
        name_prop(dds),
        target_port_prop(dds),
        order_prop(dds),
        template_prop(dds),
        slot_name_prop(dds),
    )


def slot_items_collection(dds: DataDefinitionSystem) -> CollectionSpec:
    return dds.ensure_collection(
        "SlotItems",
        slot_item_record(dds),
        cardinality=dds.many,
        identity=name_prop(dds),
    )


def slots_items_port(dds: DataDefinitionSystem) -> PortSpec:
    return dds.ensure_port("Slots.items", cardinality=dds.many)


def define_slots_productions(dds: DataDefinitionSystem) -> None:
    """Define ``__slots__`` class-body and item productions."""

    name = name_prop(dds)
    order = order_prop(dds)
    target_port = target_port_prop(dds)
    template = template_prop(dds)
    slot_name = slot_name_prop(dds)

    class_values = class_values_collection(dds)
    fields = fields_collection(dds)
    components = components_collection(dds)
    slot_items = slot_items_collection(dds)
    class_body = class_body_port(dds)
    slots_items = slots_items_port(dds)

    dds.ensure_production_group(
        "Slots",
        dds.production(
            "SlotsClassVar",
            source=class_values,
            target=components,
            values={
                name: "__slots__",
                target_port: class_body.of("runtime"),
                order: -10,
                template: SLOTS_CLASSVAR,
            },
            policy=AddIfAbsent,
        ),
        dds.production(
            "SlotItem",
            source=fields,
            target=slot_items,
            values={
                name: read(name),
                target_port: slots_items.of(("runtime", "__slots__")),
                order: read(order),
                template: SLOT_ITEM,
                slot_name: read(name),
            },
            policy=AddIfAbsent,
        ),
    )


def build_slots_capsule_definition(
    name: str = "SlotsCapsule",
) -> CapsuleDefinition:
    """Build a capsule definition that emits a slotted class shell."""

    return capsule(
        name,
        concept("class-field-schema", define_class_field_schema),
        concept("slots-productions", define_slots_productions),
    )


def slots_child_port_plan() -> ChildPortPlan:
    """Return the mapper child-port plan for ``Slots.items``."""

    return ChildPortPlan(
        parent_name="__slots__",
        port_name="SlotsItemsPort",
        target_hole="items",
        edge=TemplateEdgePlan(
            "SlotItem",
            bind=lambda record: {"slot_name": record.slot_name},
        ),
    )


def slots_class_build_plan() -> CapsuleClassBuildPlan:
    """Return the mapper plan for class + ``__slots__`` source emission."""

    return CapsuleClassBuildPlan(
        class_name=RuntimePortRef("ClassNamePort", "runtime"),
        class_body=RuntimePortRef("ClassBodyPort", "runtime"),
        child_ports=(slots_child_port_plan(),),
    )


__all__ = [
    "SLOTS_CLASSVAR",
    "SLOTS_TEMPLATE_GLOBALS",
    "SLOTS_TEMPLATE_VALUE_NAMES",
    "SLOT_ITEM",
    "build_slots_capsule_definition",
    "define_slots_productions",
    "slot_item_record",
    "slot_items_collection",
    "slot_name_prop",
    "slots_child_port_plan",
    "slots_class_build_plan",
    "slots_items_port",
]
