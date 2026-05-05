"""Recorded frozen-property concept extension."""

from __future__ import annotations

from yidl.capsule.class_concepts import ClassConcept
from yidl.capsule.property_concepts import MANAGED_FIELD
from yidl.capsule.property_concepts import PLAIN_FIELD
from yidl.capsule.property_concepts import PropertyConcept
from yidl.capsule.property_concepts import register_property_template
from yidl.capsule.recorded_builder import CapsuleConceptPlan
from yidl.capsule.recorded_builder import capsule_concept
from yidl.generation.data_def_sys import from_astichi_code


def _readonly_property_bind(record: object) -> dict[str, object]:
    return {"storage_path": f"_{record.name}"}


def _readonly_managed_property_bind(record: object) -> dict[str, object]:
    return {"working_path": f"_{record.name}_working"}


def _build_frozen_property_concept() -> CapsuleConceptPlan:
    builder = capsule_concept(
        "frozen-property-overrides",
        extends=(PropertyConcept,),
    )
    Class = builder.use(ClassConcept)
    Property = builder.use(PropertyConcept)
    frozen = builder.props.Frozen(bool)
    builder.extend_record(Class.records.FieldInput, frozen)

    kind = Class.props.Kind
    fields = Class.collections.Fields
    property_template = builder.use_matcher(Property.matchers.PropertyTemplate)
    field = property_template.input.field(fields)
    property_template.rule.readonly_property(
        when=(
            field.prop(frozen).eq(True),
            field.prop(kind).eq(PLAIN_FIELD),
        ),
        resource=register_property_template(
            from_astichi_code(
                """
                @property
                def field_name__astichi_arg__(self):
                    return self.astichi_ref(external=storage_path)
                """
            ),
            _readonly_property_bind,
        ),
    )
    property_template.rule.readonly_managed_property(
        when=(
            field.prop(frozen).eq(True),
            field.prop(kind).eq(MANAGED_FIELD),
        ),
        resource=register_property_template(
            from_astichi_code(
                """
                @property
                def field_name__astichi_arg__(self):
                    return self.astichi_ref(external=working_path)
                """
            ),
            _readonly_managed_property_bind,
        ),
    )

    return builder.build()


FrozenPropertyConcept: CapsuleConceptPlan = _build_frozen_property_concept()


__all__ = ["FrozenPropertyConcept"]
