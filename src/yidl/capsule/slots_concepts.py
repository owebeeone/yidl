"""Recorded ``__slots__`` capsule concept."""

from __future__ import annotations

from yidl.capsule.build_mapper import CapsuleClassBuildPlan
from yidl.capsule.build_mapper import ChildPortPlan
from yidl.capsule.build_mapper import RuntimePortRef
from yidl.capsule.build_mapper import TemplateEdgePlan
from yidl.capsule.class_concepts import ClassConcept
from yidl.capsule.recorded_builder import CapsuleConceptPlan
from yidl.capsule.recorded_builder import capsule_concept
from yidl.generation.data_def_sys import AddIfAbsent
from yidl.generation.data_def_sys import REQUIRED
from yidl.generation.data_def_sys import from_astichi_code


def _build_slots_concept() -> CapsuleConceptPlan:
    builder = capsule_concept("slots-productions", extends=(ClassConcept,))
    Class = builder.use(ClassConcept)
    name = Class.props.Name
    order = Class.props.Order
    target_port = Class.props.TargetPort
    template = Class.props.Template
    class_values = Class.collections.ClassValues
    fields = Class.collections.Fields
    components = Class.collections.Components
    class_body = Class.ports.Class.body

    slot_name = builder.props.SlotName(str, REQUIRED)
    slot_item = builder.records.SlotItem(
        name,
        target_port,
        order,
        template,
        slot_name,
    )
    slot_items = builder.collections.SlotItems(
        slot_item,
        cardinality=builder.many,
        identity=name,
    )
    slots_items = builder.ports.Slots.items(cardinality=builder.many)

    builder.productions.SlotsClassVar(
        source=class_values,
        target=components,
        values={
            name: "__slots__",
            target_port: class_body.of("runtime"),
            order: -10,
            template: from_astichi_code(
                """
                __slots__ = (*astichi_hole(items),)
                """
            ),
        },
        policy=AddIfAbsent,
    ).in_group("Slots")
    builder.productions.SlotItem(
        source=fields,
        target=slot_items,
        values={
            name: name.read(),
            target_port: slots_items.of(("runtime", "__slots__")),
            order: order.read(),
            template: from_astichi_code(
                """
                astichi_bind_external(slot_name)
                slot_name
                """
            ),
            slot_name: name.read(),
        },
        policy=AddIfAbsent,
    ).in_group("Slots")

    return builder.build()


SlotsConcept: CapsuleConceptPlan = _build_slots_concept()


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


__all__ = ["SlotsConcept", "slots_child_port_plan", "slots_class_build_plan"]
