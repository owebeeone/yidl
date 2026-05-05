from __future__ import annotations

import pytest

from yidl.generation.data_def_sys import DataDefinitionSystem
from yidl.generation.data_def_sys import REQUIRED
from yidl.generation.data_def_sys import from_astichi_code


def test_operation_rejects_absent_order_property() -> None:
    dds = DataDefinitionSystem()
    name = dds.property("Name", str, default=REQUIRED, storage_name="name")
    order = dds.property("Order", int, default=0, storage_name="order")
    source_record = dds.record("Source", name)
    output_record = dds.record("Output", name)
    sources = dds.collection("Sources", source_record, cardinality=dds.many)
    outputs = dds.collection("Outputs", output_record, cardinality=dds.many)

    with pytest.raises(ValueError, match="has no property 'Order'"):
        dds.operation(
            "BadOrder",
            inputs=(sources,),
            outputs=(outputs,),
            order_by=(order,),
            resource=from_astichi_code("pass"),
        )


def test_operation_write_errors_include_operation_and_target_collection() -> None:
    dds = DataDefinitionSystem()
    name = dds.property("Name", str, default=REQUIRED, storage_name="name")
    source_record = dds.record("Source", name)
    output_record = dds.record("Output", name)
    sources = dds.collection("Sources", source_record, cardinality=dds.many)
    outputs = dds.collection("Outputs", output_record, cardinality=dds.many, identity=name)
    operation = dds.operation(
        "DuplicateOutputs",
        inputs=(sources,),
        outputs=(outputs,),
        resource=from_astichi_code(
            """
            ctx.write(OutputsCollection, Output(name="same"))
            ctx.write(OutputsCollection, Output(name="same"))
            """,
            keep_names=("ctx", "OutputsCollection", "Output"),
        ),
    )
    dds.production_group("Build", operation)

    source = dds.emit_container_runtime_source()
    namespace = {}
    exec(source, namespace)
    builder = namespace["new_builder"]()

    with pytest.raises(
        ValueError,
        match="operation 'DuplicateOutputs'.*collection 'Outputs'",
    ):
        namespace["build_container"](builder)
