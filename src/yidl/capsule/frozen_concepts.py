"""Frozen-field capsule concept extensions."""

from __future__ import annotations

from yidl.capsule.class_concepts import extend_field_input_record
from yidl.capsule.class_concepts import fields_collection
from yidl.capsule.class_concepts import kind_prop
from yidl.capsule.class_concepts import build_class_field_schema_concept
from yidl.capsule.property_concepts import build_property_capsule_concept
from yidl.capsule.property_concepts import MANAGED_FIELD
from yidl.capsule.property_concepts import PLAIN_FIELD
from yidl.capsule.property_concepts import register_property_template
from yidl.capsule.recorded_builder import CapsuleConceptPlan
from yidl.capsule.recorded_builder import capsule_concept
from yidl.generation.data_def_sys import DataDefinitionSystem
from yidl.generation.data_def_sys import from_astichi_code
from yidl.generation.data_def_sys import PropertySpec


READONLY_PROPERTY = from_astichi_code(
    "@property\n"
    "def field_name__astichi_arg__(self):\n"
    "    return self.astichi_ref(external=storage_path)\n"
)
READONLY_MANAGED_PROPERTY = from_astichi_code(
    "@property\n"
    "def field_name__astichi_arg__(self):\n"
    "    return self.astichi_ref(external=working_path)\n"
)

FROZEN_PROPERTY_TEMPLATE_VALUE_NAMES = (
    (READONLY_PROPERTY, "READONLY_PROPERTY"),
    (READONLY_MANAGED_PROPERTY, "READONLY_MANAGED_PROPERTY"),
)
FROZEN_PROPERTY_TEMPLATE_GLOBALS = {
    "READONLY_PROPERTY": READONLY_PROPERTY,
    "READONLY_MANAGED_PROPERTY": READONLY_MANAGED_PROPERTY,
}
_FROZEN_PROPERTY_CONCEPT: CapsuleConceptPlan | None = None


def frozen_prop(dds: DataDefinitionSystem) -> PropertySpec:
    return dds.ensure_property(
        "Frozen",
        bool,
        default=False,
        storage_name="frozen",
    )


def define_frozen_field_schema(dds: DataDefinitionSystem) -> None:
    """Extend field input records with a frozen marker property."""

    extend_field_input_record(dds, frozen_prop(dds))


def define_frozen_property_overrides(dds: DataDefinitionSystem) -> None:
    """Add frozen-aware override rules to the property matcher."""

    define_frozen_field_schema(dds)

    kind = kind_prop(dds)
    frozen = frozen_prop(dds)
    fields = fields_collection(dds)

    property_template = dds.ensure_matcher("PropertyTemplate")
    field_input = property_template.ensure_input("field", fields)
    property_template.rule(
        when=(
            field_input.prop(frozen).eq(True),
            field_input.prop(kind).eq(PLAIN_FIELD),
        ),
        resource=READONLY_PROPERTY,
        name="readonly-property",
    )
    property_template.rule(
        when=(
            field_input.prop(frozen).eq(True),
            field_input.prop(kind).eq(MANAGED_FIELD),
        ),
        resource=READONLY_MANAGED_PROPERTY,
        name="readonly-managed-property",
    )


def build_frozen_property_concept() -> CapsuleConceptPlan:
    """Build the recorded frozen-property override concept."""

    global _FROZEN_PROPERTY_CONCEPT
    if _FROZEN_PROPERTY_CONCEPT is not None:
        return _FROZEN_PROPERTY_CONCEPT

    class_schema = build_class_field_schema_concept()
    property_concept = build_property_capsule_concept()
    builder = capsule_concept(
        "frozen-property-overrides",
        requires=(property_concept,),
    )
    Class = builder.use(class_schema)
    Property = builder.use(property_concept)
    frozen = builder.props.Frozen(bool)
    builder.extend_record(Class.records.FieldInput, frozen)

    kind = Class.props.Kind
    fields = Class.collections.Fields
    property_template = builder.use_matcher(Property.matchers.PropertyTemplate)
    field_input = property_template.input.field(fields)
    property_template.rule.readonly_property(
        when=(
            field_input.prop(frozen).eq(True),
            field_input.prop(kind).eq(PLAIN_FIELD),
        ),
        resource=READONLY_PROPERTY,
    )
    property_template.rule.readonly_managed_property(
        when=(
            field_input.prop(frozen).eq(True),
            field_input.prop(kind).eq(MANAGED_FIELD),
        ),
        resource=READONLY_MANAGED_PROPERTY,
    )

    _FROZEN_PROPERTY_CONCEPT = builder.build()
    return _FROZEN_PROPERTY_CONCEPT


def _readonly_property_bind(record: object) -> dict[str, object]:
    return {"storage_path": f"_{record.name}"}


def _readonly_managed_property_bind(record: object) -> dict[str, object]:
    return {"working_path": f"_{record.name}_working"}


register_property_template(READONLY_PROPERTY, _readonly_property_bind)
register_property_template(
    READONLY_MANAGED_PROPERTY,
    _readonly_managed_property_bind,
)


__all__ = [
    "FROZEN_PROPERTY_TEMPLATE_GLOBALS",
    "FROZEN_PROPERTY_TEMPLATE_VALUE_NAMES",
    "READONLY_MANAGED_PROPERTY",
    "READONLY_PROPERTY",
    "build_frozen_property_concept",
    "define_frozen_field_schema",
    "define_frozen_property_overrides",
    "frozen_prop",
]
