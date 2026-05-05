"""Recorded init-method capsule concept."""

from __future__ import annotations

from yidl.capsule.build_mapper import CapsuleClassBuildPlan
from yidl.capsule.build_mapper import ChildPortPlan
from yidl.capsule.build_mapper import RuntimePortRef
from yidl.capsule.build_mapper import TemplateEdgePlan
from yidl.capsule.class_concepts import ClassConcept
from yidl.capsule.recorded_builder import CapsuleConceptPlan
from yidl.capsule.recorded_builder import capsule_concept
from yidl.capsule.recorded_builder import match
from yidl.generation.data_def_sys import AddIfAbsent
from yidl.generation.data_def_sys import from_astichi_code


def _build_init_concept() -> CapsuleConceptPlan:
    builder = capsule_concept("init-productions", extends=(ClassConcept,))
    Class = builder.use(ClassConcept)
    name = Class.props.Name
    order = Class.props.Order
    defaulted = Class.props.Defaulted
    default_value = Class.props.DefaultValue
    target_port = Class.props.TargetPort
    template = Class.props.Template
    source_name = Class.props.SourceName
    target_name = Class.props.TargetName
    init_fields = Class.computed.InitFields
    class_values = Class.collections.ClassValues
    components = Class.collections.Components
    params = Class.collections.InitParams
    assignments = Class.collections.InitAssignments
    class_body = Class.ports.Class.body
    init_params = Class.ports.Init.params
    init_body = Class.ports.Init.body

    param_template = builder.matchers.InitParamTemplate()
    field = param_template.input.field(init_fields)
    param_template.default(
        from_astichi_code(
            """
            def astichi_params(*, field_name__astichi_arg__):
                pass
            """
        )
    )
    param_template.rule.defaulted_param(
        when=(field.prop(defaulted).eq(True),),
        resource=from_astichi_code(
            """
            def astichi_params(
                *,
                field_name__astichi_arg__=astichi_bind_external(default_value),
            ):
                pass
            """
        ),
    )

    builder.productions.InitMethod(
        source=class_values,
        target=components,
        values={
            name: "__init__",
            target_port: class_body.of("runtime"),
            order: 0,
            template: from_astichi_code(
                """
                def __init__(self, params__astichi_param_hole__):
                    astichi_hole(body)
                """
            ),
        },
        policy=AddIfAbsent,
    ).in_group("Class")
    builder.productions.InitParam(
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
    ).in_group("Class")
    builder.productions.InitAssignment(
        source=init_fields,
        target=assignments,
        values={
            name: name.read(),
            target_port: init_body.of(("runtime", "__init__")),
            order: order.read(),
            template: from_astichi_code(
                """
                astichi_import(self)
                self.astichi_ref(external=target_path)._ = astichi_pass(
                    source_name,
                    outer_bind=True,
                )
                """
            ),
            source_name: name.read(),
            target_name: name.read(),
        },
        policy=AddIfAbsent,
    ).in_group("Class")

    return builder.build()


InitConcept: CapsuleConceptPlan = _build_init_concept()


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


__all__ = ["InitConcept", "init_class_build_plan"]
