from __future__ import annotations

from support.golden_case import run_case
from yidl.capsule.build_mapper import CapsuleClassBuildPlan
from yidl.capsule.build_mapper import RuntimePortRef
from yidl.capsule.build_mapper import build_class_source
from yidl.capsule.definition import concept
from yidl.capsule.frozen_concepts import FROZEN_PROPERTY_TEMPLATE_GLOBALS
from yidl.capsule.frozen_concepts import FROZEN_PROPERTY_TEMPLATE_VALUE_NAMES
from yidl.capsule.frozen_concepts import define_frozen_property_overrides
from yidl.capsule.property_concepts import MANAGED_FIELD
from yidl.capsule.property_concepts import PLAIN_FIELD
from yidl.capsule.property_concepts import PROPERTY_EVALUATOR_GLOBALS
from yidl.capsule.property_concepts import PROPERTY_EVALUATOR_NAMES
from yidl.capsule.property_concepts import PROPERTY_TEMPLATE_GLOBALS
from yidl.capsule.property_concepts import PROPERTY_TEMPLATE_VALUE_NAMES
from yidl.capsule.property_concepts import build_property_capsule_definition
from yidl.capsule.property_concepts import property_class_body_edge_plan


def _runtime():
    definition = build_property_capsule_definition("PropertyConcepts").extend(
        concept("frozen-property-overrides", define_frozen_property_overrides),
    )
    return definition.load_runtime(
        evaluator_names=PROPERTY_EVALUATOR_NAMES,
        value_names=(
            *PROPERTY_TEMPLATE_VALUE_NAMES,
            *FROZEN_PROPERTY_TEMPLATE_VALUE_NAMES,
        ),
        runtime_globals={
            **PROPERTY_EVALUATOR_GLOBALS,
            **PROPERTY_TEMPLATE_GLOBALS,
            **FROZEN_PROPERTY_TEMPLATE_GLOBALS,
        },
    )


def render_case() -> str:
    runtime = _runtime()
    namespace = runtime.namespace
    builder = runtime.new_builder()
    builder.add(
        namespace["ClassValuesCollection"],
        namespace["ClassValue"](
            name="Example",
            target_port=namespace["ClassNamePort"].of("runtime"),
            order=0,
            runtime_value="Example",
        ),
    )
    field = namespace["FieldInput"]
    fields = namespace["FieldsCollection"]
    builder.add(fields, field(name="count", kind=PLAIN_FIELD, order=0))
    builder.add(fields, field(name="owner", kind=MANAGED_FIELD, order=1))
    builder.add(fields, field(name="label", kind=PLAIN_FIELD, frozen=True, order=2))
    builder.add(
        fields,
        field(name="session", kind=MANAGED_FIELD, frozen=True, order=3),
    )

    container = runtime.build_container(builder)
    return build_class_source(
        container,
        namespace,
        CapsuleClassBuildPlan(
            class_name=RuntimePortRef("ClassNamePort", "runtime"),
            class_body=RuntimePortRef("ClassBodyPort", "runtime"),
            class_body_edge=property_class_body_edge_plan(),
        ),
    )


def validate_case(source: str) -> None:
    namespace = {}
    exec(source, namespace)
    example = namespace["Example"]()
    example._count = 7
    example._owner_working = "Ada"
    example._label = "cold"
    example._session_working = "active"

    assert example.count == 7
    example.count = 8
    assert example._count == 8

    assert example.owner == "Ada"
    example.owner = "Grace"
    assert example._owner_working == "Grace"

    assert example.label == "cold"
    _assert_attribute_error(lambda: setattr(example, "label", "hot"))

    assert example.session == "active"
    _assert_attribute_error(lambda: setattr(example, "session", "inactive"))

    assert "@count.setter" in source
    assert "@owner.setter" in source
    assert "@label.setter" not in source
    assert "@session.setter" not in source


def _assert_attribute_error(action) -> None:
    try:
        action()
    except AttributeError:
        return
    raise AssertionError("expected AttributeError")


if __name__ == "__main__":
    raise SystemExit(run_case("capsule_property_concepts.py", render_case, validate_case))
