"""Recorded property-method capsule concept."""

from __future__ import annotations

from collections.abc import Callable

from yidl.capsule.build_mapper import TemplateEdgePlan
from yidl.capsule.class_concepts import ClassConcept
from yidl.capsule.recorded_builder import CapsuleConceptPlan
from yidl.capsule.recorded_builder import capsule_concept
from yidl.capsule.recorded_builder import match
from yidl.generation.data_def_sys import AddIfAbsent
from yidl.generation.data_def_sys import call
from yidl.generation.data_def_sys import from_astichi_code
from yidl.generation.data_def_sys import MatcherGeneratedValue


PLAIN_FIELD = "plain"
MANAGED_FIELD = "managed"

PropertyTemplateBinder = Callable[[object], dict[str, object]]
_PROPERTY_TEMPLATE_BINDERS: dict[MatcherGeneratedValue, PropertyTemplateBinder] = {}


def register_property_template(
    template: MatcherGeneratedValue,
    binder: PropertyTemplateBinder,
) -> MatcherGeneratedValue:
    """Register edge bindings needed by a property component template."""

    existing = _PROPERTY_TEMPLATE_BINDERS.get(template)
    if existing is not None and existing is not binder:
        raise ValueError("property template is already registered differently")
    _PROPERTY_TEMPLATE_BINDERS[template] = binder
    return template


def property_order_for(result: object) -> int:
    return 100 + result.records[0].order


def _plain_property_bind(record: object) -> dict[str, object]:
    return {"storage_path": f"_{record.name}"}


def _managed_property_bind(record: object) -> dict[str, object]:
    return {"working_path": f"_{record.name}_working"}


def _build_property_concept() -> CapsuleConceptPlan:
    builder = capsule_concept("property-productions", extends=(ClassConcept,))
    Class = builder.use(ClassConcept)
    name = Class.props.Name
    kind = Class.props.Kind
    target_port = Class.props.TargetPort
    order = Class.props.Order
    template = Class.props.Template
    fields = Class.collections.Fields
    components = Class.collections.Components
    class_body = Class.ports.Class.body

    property_template = builder.matchers.PropertyTemplate()
    field = property_template.input.field(fields)
    property_template.default(
        register_property_template(
            from_astichi_code(
                """
                @property
                def field_name__astichi_arg__(self):
                    return self.astichi_ref(external=storage_path)

                @field_name__astichi_arg__.setter
                def field_name__astichi_arg__(self, value):
                    self.astichi_ref(external=storage_path)._ = value
                """
            ),
            _plain_property_bind,
        )
    )
    property_template.rule.managed_property(
        when=(field.prop(kind).eq(MANAGED_FIELD),),
        resource=register_property_template(
            from_astichi_code(
                """
                @property
                def field_name__astichi_arg__(self):
                    return self.astichi_ref(external=working_path)

                @field_name__astichi_arg__.setter
                def field_name__astichi_arg__(self, value):
                    self.astichi_ref(external=working_path)._ = value
                """
            ),
            _managed_property_bind,
        ),
    )

    builder.productions.Property(
        source=property_template.results(),
        target=components,
        values={
            name: match.record("field").prop(name),
            target_port: class_body.of("runtime"),
            order: call("property-order", property_order_for),
            template: match.resource(),
        },
        policy=AddIfAbsent,
    ).in_group("Properties")
    builder.runtime.evaluator(property_order_for, name="property_order_for")

    return builder.build()


PropertyConcept: CapsuleConceptPlan = _build_property_concept()


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


__all__ = [
    "MANAGED_FIELD",
    "PLAIN_FIELD",
    "PropertyConcept",
    "property_class_body_edge_plan",
    "property_order_for",
    "register_property_template",
]
