"""YIDL capsule package."""

from .build_mapper import (
    CapsuleClassBuildPlan,
    ChildPortPlan,
    RuntimePortRef,
    TemplateEdgePlan,
    build_class_source,
)
from .class_concepts import ClassConcept
from .frozen_concepts import FrozenPropertyConcept
from .init_concepts import InitConcept, init_class_build_plan
from .init_only_capsule import (
    InitOnlyClassDefinition,
    InitOnlyFieldSpec,
    ResolvedInitField,
    UNSPECIFIED,
    UnspecifiedType,
    class_definition_from_class,
    compile_init_only_capsule,
    emit_init_only_factory_source,
    field_spec,
    render_init_only_class,
)
from .property_concepts import (
    MANAGED_FIELD,
    PLAIN_FIELD,
    PropertyConcept,
    property_class_body_edge_plan,
    property_order_for,
)
from .recorded_builder import (
    CapsuleConceptBuilder,
    CapsuleConceptPlan,
    CapsuleRuntime,
    CollectionHandle,
    ComputedCollectionHandle,
    MatcherHandle,
    PortHandle,
    PropertyHandle,
    RecordHandle,
    capsule_concept,
    match,
)
from .slots_concepts import (
    SlotsConcept,
    slots_child_port_plan,
    slots_class_build_plan,
)

__all__ = [
    "CapsuleClassBuildPlan",
    "CapsuleConceptBuilder",
    "CapsuleConceptPlan",
    "CapsuleRuntime",
    "ChildPortPlan",
    "ClassConcept",
    "CollectionHandle",
    "ComputedCollectionHandle",
    "FrozenPropertyConcept",
    "InitConcept",
    "InitOnlyClassDefinition",
    "InitOnlyFieldSpec",
    "MANAGED_FIELD",
    "MatcherHandle",
    "PLAIN_FIELD",
    "PortHandle",
    "PropertyConcept",
    "PropertyHandle",
    "RecordHandle",
    "ResolvedInitField",
    "RuntimePortRef",
    "SlotsConcept",
    "TemplateEdgePlan",
    "UNSPECIFIED",
    "UnspecifiedType",
    "build_class_source",
    "capsule_concept",
    "class_definition_from_class",
    "compile_init_only_capsule",
    "emit_init_only_factory_source",
    "field_spec",
    "init_class_build_plan",
    "match",
    "property_class_body_edge_plan",
    "property_order_for",
    "render_init_only_class",
    "slots_child_port_plan",
    "slots_class_build_plan",
]
