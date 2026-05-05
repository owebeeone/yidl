"""Recorded class-shaped capsule concept."""

from __future__ import annotations

from yidl.capsule.recorded_builder import CapsuleConceptPlan
from yidl.capsule.recorded_builder import capsule_concept
from yidl.generation.data_def_sys import REQUIRED


def _build_class_concept() -> CapsuleConceptPlan:
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


ClassConcept: CapsuleConceptPlan = _build_class_concept()


__all__ = ["ClassConcept"]
