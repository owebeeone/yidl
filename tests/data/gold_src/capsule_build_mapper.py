from __future__ import annotations

from support.golden_case import run_case
from yidl.capsule.build_mapper import build_class_source
from yidl.capsule.init_concepts import InitConcept
from yidl.capsule.init_concepts import init_class_build_plan


def _runtime():
    return InitConcept.runtime().load()


def _container():
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
    builder.add(
        fields,
        field(name="retries", init=True, defaulted=True, default_value=3, order=2),
    )
    return runtime.build_container(builder), namespace


def render_case() -> str:
    container, namespace = _container()
    return build_class_source(container, namespace, init_class_build_plan())


def validate_case(source: str) -> None:
    namespace = {}
    exec(source, namespace)
    example = namespace["Example"]

    assert tuple(example(count=None).__dict__.items()) == (
        ("count", None),
        ("label", "cold"),
        ("retries", 3),
    )
    overridden = example(count=5, label="hot", retries=8)
    assert overridden.count == 5
    assert overridden.label == "hot"
    assert overridden.retries == 8
    assert "class Example:" in source
    assert "def __init__(self, *, count, label='cold', retries=3):" in source
    assert "self.count = count" in source


if __name__ == "__main__":
    raise SystemExit(run_case("capsule_build_mapper.py", render_case, validate_case))
