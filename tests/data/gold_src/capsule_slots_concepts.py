from __future__ import annotations

from support.golden_case import run_case
from yidl.capsule.build_mapper import CapsuleClassBuildPlan
from yidl.capsule.build_mapper import RuntimePortRef
from yidl.capsule.build_mapper import build_class_source
from yidl.capsule.class_concepts import define_class_field_schema
from yidl.capsule.definition import capsule
from yidl.capsule.definition import concept
from yidl.capsule.init_concepts import INIT_TEMPLATE_GLOBALS
from yidl.capsule.init_concepts import INIT_TEMPLATE_VALUE_NAMES
from yidl.capsule.init_concepts import define_init_productions
from yidl.capsule.init_concepts import init_class_build_plan
from yidl.capsule.slots_concepts import SLOTS_TEMPLATE_GLOBALS
from yidl.capsule.slots_concepts import SLOTS_TEMPLATE_VALUE_NAMES
from yidl.capsule.slots_concepts import define_slots_productions
from yidl.capsule.slots_concepts import slots_child_port_plan


def _runtime():
    definition = capsule(
        "SlotsAndInit",
        concept("class-field-schema", define_class_field_schema),
        concept("slots-productions", define_slots_productions),
        concept("init-productions", define_init_productions),
    )
    return definition.load_runtime(
        value_names=(
            *SLOTS_TEMPLATE_VALUE_NAMES,
            *INIT_TEMPLATE_VALUE_NAMES,
        ),
        runtime_globals={
            **SLOTS_TEMPLATE_GLOBALS,
            **INIT_TEMPLATE_GLOBALS,
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
    builder.add(fields, field(name="count", init=True, defaulted=False, order=0))
    builder.add(
        fields,
        field(name="label", init=True, defaulted=True, default_value="cold", order=1),
    )
    builder.add(fields, field(name="cache", init=False, defaulted=False, order=2))
    builder.add(
        fields,
        field(name="retries", init=True, defaulted=True, default_value=3, order=3),
    )

    init_plan = init_class_build_plan()
    build_plan = CapsuleClassBuildPlan(
        class_name=RuntimePortRef("ClassNamePort", "runtime"),
        class_body=RuntimePortRef("ClassBodyPort", "runtime"),
        child_ports=(
            slots_child_port_plan(),
            *init_plan.child_ports,
        ),
    )
    container = runtime.build_container(builder)
    return build_class_source(container, namespace, build_plan)


def validate_case(source: str) -> None:
    namespace = {}
    exec(source, namespace)
    example_type = namespace["Example"]
    example = example_type(count=7)

    assert not hasattr(example, "__dict__")
    assert example.count == 7
    assert example.label == "cold"
    assert example.retries == 3
    assert not hasattr(example, "cache")
    assert "__slots__ = ('count', 'label', 'cache', 'retries')" in source
    assert "def __init__(self, *, count, label='cold', retries=3):" in source


if __name__ == "__main__":
    raise SystemExit(run_case("capsule_slots_concepts.py", render_case, validate_case))
