from __future__ import annotations

from support.golden_case import run_case
from yidl.capsule.build_mapper import build_class_source
from yidl.capsule.init_concepts import build_init_capsule_concept
from yidl.capsule.init_concepts import init_class_build_plan


def _runtime():
    return build_init_capsule_concept().runtime().load()


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

    container = runtime.build_container(builder)
    return build_class_source(container, namespace, init_class_build_plan())


def validate_case(source: str) -> None:
    namespace = {}
    exec(source, namespace)
    example = namespace["Example"]

    assert tuple(example(count=7).__dict__.items()) == (
        ("count", 7),
        ("label", "cold"),
        ("retries", 3),
    )
    assert "cache" not in source
    assert "def __init__(self, *, count, label='cold', retries=3):" in source
    assert "self.retries = retries" in source


if __name__ == "__main__":
    raise SystemExit(run_case("capsule_init_concepts.py", render_case, validate_case))
