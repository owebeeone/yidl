from __future__ import annotations

from support.golden_case import run_case
from yidl.concept_parser import compile_yidl_files


CORE_YIDL = """
module yidl.lifecycle.core
export concept LifecycleCore

concept LifecycleCore {
    property Name: str storage name
    property Kind: object storage kind
    property SourceOrder: int = 0 storage source_order

    family FieldSpecs {
        common Name, Kind, SourceOrder
        variant PlainField {}
    }

    collection Fields: FieldSpecs identity Name
}
"""


MANAGED_YIDL = """
module yidl.lifecycle.managed
import "core.yidl" as core
export concept ManagedFields

concept ManagedFields extends core.LifecycleCore {
    property TxGroup: str = "default" storage tx_group

    family core.FieldSpecs {
        variant ManagedField {
            TxGroup
            Kind
        }
    }
}
"""


def _compiled():
    return compile_yidl_files(
        {
            "core.yidl": CORE_YIDL,
            "managed.yidl": MANAGED_YIDL,
        },
        "managed.yidl",
    )


def render_case() -> str:
    return _compiled().concepts["ManagedFields"].plan.emit_runtime_source()


def validate_case(source: str) -> None:
    namespace: dict[str, object] = {}
    exec(source, namespace)

    builder = namespace["new_builder"]()
    fields = namespace["FieldsCollection"]
    builder.add(
        fields,
        namespace["PlainField"](
            name="count",
            kind="plain",
            source_order=0,
        ),
    )
    builder.add(
        fields,
        namespace["ManagedField"](
            name="owner",
            kind="managed",
            source_order=1,
            tx_group="tx",
        ),
    )
    container = builder.freeze()

    assert [record.name for record in container.Fields.sequence()] == [
        "count",
        "owner",
    ]
    assert "FieldSpecsUnion = RuntimeUnion" in source
    assert "PlainField" in source
    assert "ManagedField" in source
    assert source.count("RuntimeProperty('Name'") == 1
    assert source.count("RuntimeUnion('FieldSpecs'") == 1


if __name__ == "__main__":
    raise SystemExit(run_case("yidl_imported_concepts.py", render_case, validate_case))
