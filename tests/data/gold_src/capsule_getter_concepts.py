from __future__ import annotations

from support.golden_case import run_case
from yidl.capsule.build_mapper import CapsuleClassBuildPlan
from yidl.capsule.build_mapper import RuntimePortRef
from yidl.capsule.build_mapper import build_class_source
from yidl.capsule.class_concepts import define_class_field_schema
from yidl.capsule.definition import capsule
from yidl.capsule.definition import concept
from yidl.capsule.getter_concepts import GETTER_EVALUATOR_GLOBALS
from yidl.capsule.getter_concepts import GETTER_EVALUATOR_NAMES
from yidl.capsule.getter_concepts import GETTER_TEMPLATE_GLOBALS
from yidl.capsule.getter_concepts import GETTER_TEMPLATE_VALUE_NAMES
from yidl.capsule.getter_concepts import MANAGED_FIELD
from yidl.capsule.getter_concepts import PLAIN_FIELD
from yidl.capsule.getter_concepts import define_getter_productions
from yidl.capsule.getter_concepts import getter_class_body_edge_plan


def _runtime():
    definition = capsule(
        "GetterConcepts",
        concept("class-field-schema", define_class_field_schema),
        concept("getter-productions", define_getter_productions),
    )
    return definition.load_runtime(
        evaluator_names=GETTER_EVALUATOR_NAMES,
        value_names=GETTER_TEMPLATE_VALUE_NAMES,
        runtime_globals={
            **GETTER_EVALUATOR_GLOBALS,
            **GETTER_TEMPLATE_GLOBALS,
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
    builder.add(fields, field(name="label", order=2))

    container = runtime.build_container(builder)
    return build_class_source(
        container,
        namespace,
        CapsuleClassBuildPlan(
            class_name=RuntimePortRef("ClassNamePort", "runtime"),
            class_body=RuntimePortRef("ClassBodyPort", "runtime"),
            class_body_edge=getter_class_body_edge_plan(),
        ),
    )


def validate_case(source: str) -> None:
    namespace = {}
    exec(source, namespace)
    example = namespace["Example"]()
    example._count = 7
    example._owner_working = "Ada"
    example._label = "cold"

    assert example.count == 7
    assert example.owner == "Ada"
    assert example.label == "cold"
    assert "def count(self):" in source
    assert "return self._owner_working" in source
    assert "@property" in source


if __name__ == "__main__":
    raise SystemExit(run_case("capsule_getter_concepts.py", render_case, validate_case))
