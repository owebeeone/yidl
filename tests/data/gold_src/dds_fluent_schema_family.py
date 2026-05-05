from __future__ import annotations

from support.golden_case import run_case
from yidl.capsule.recorded_builder import capsule_concept
from yidl.generation.data_def_sys import REQUIRED


def _build_concept():
    builder = capsule_concept("LifecycleFieldFamily")
    name = builder.props.Name(str, REQUIRED)
    source_order = builder.props.SourceOrder(int, 0)
    kind = builder.props.Kind(object, REQUIRED)
    default = builder.props.Default(object, REQUIRED)
    tx_group = builder.props.TxGroup(str, "default")

    field_specs = builder.schema_family("FieldSpecs")
    field_specs.common(name, source_order, kind)
    field_specs.variant("PlainField", default)
    field_specs.variant("ManagedField", tx_group, default)

    fields = builder.collections.Fields(
        field_specs.handle,
        cardinality=builder.many,
        identity=name,
    )
    builder.computed.ManagedFields(
        source=fields,
        when=(kind.eq("managed"),),
    )
    return builder.build()


def render_case() -> str:
    return _build_concept().emit_runtime_source()


def validate_case(source: str) -> None:
    namespace: dict[str, object] = {}
    exec(source, namespace)

    builder = namespace["new_builder"]()
    fields = namespace["FieldsCollection"]
    builder.add(
        fields,
        namespace["PlainField"](
            name="count",
            source_order=0,
            kind="plain",
            default=0,
        ),
    )
    builder.add(
        fields,
        namespace["ManagedField"](
            name="owner",
            source_order=1,
            kind="managed",
            tx_group="tx",
            default=None,
        ),
    )
    container = builder.freeze()

    assert [record.name for record in container.Fields.sequence()] == [
        "count",
        "owner",
    ]
    assert [record.name for record in container.ManagedFields.sequence()] == [
        "owner",
    ]
    assert "FieldSpecsUnion = RuntimeUnion" in source
    assert "RuntimeCollection('Fields', _FieldSpecsUnion" in source
    assert "PlainField" in source
    assert "ManagedField" in source


if __name__ == "__main__":
    raise SystemExit(run_case("dds_fluent_schema_family.py", render_case, validate_case))
