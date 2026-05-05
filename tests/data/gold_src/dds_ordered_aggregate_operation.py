from __future__ import annotations

from support.golden_case import run_case
from yidl.generation.data_def_sys import DataDefinitionSystem
from yidl.generation.data_def_sys import REQUIRED
from yidl.generation.data_def_sys import emit_container_runtime_source
from yidl.generation.data_def_sys import from_astichi_code


BuildTxGroupsOperation = from_astichi_code(
    """
    seen = set()
    next_index = 0
    for field in ctx.records(TransactionalFieldsCollection):
        tx_group = field.tx_group
        if tx_group in seen:
            continue
        seen.add(tx_group)
        ctx.write(
            TxGroupsCollection,
            TxGroupRecord(tx_group=tx_group, tx_index=next_index),
            policy=AddIfAbsent,
        )
        next_index += 1
    """,
    keep_names=(
        "AddIfAbsent",
        "TransactionalFieldsCollection",
        "TxGroupRecord",
        "TxGroupsCollection",
        "ctx",
    ),
)


def _build_dds() -> DataDefinitionSystem:
    dds = DataDefinitionSystem()
    name = dds.property("Name", str, default=REQUIRED, storage_name="name")
    source_order = dds.property(
        "SourceOrder",
        int,
        default=0,
        storage_name="source_order",
    )
    tx_group = dds.property("TxGroup", str, default=REQUIRED, storage_name="tx_group")
    tx_index = dds.property("TxIndex", int, default=REQUIRED, storage_name="tx_index")

    field = dds.record("TransactionalField", name, tx_group, source_order)
    tx_group_record = dds.record("TxGroupRecord", tx_group, tx_index)
    transactional_fields = dds.collection(
        "TransactionalFields",
        field,
        cardinality=dds.many,
        identity=name,
    )
    tx_groups = dds.collection(
        "TxGroups",
        tx_group_record,
        cardinality=dds.many,
        identity=tx_group,
    )
    operation = dds.operation(
        "BuildTxGroups",
        inputs=(transactional_fields,),
        outputs=(tx_groups,),
        order_by=(source_order,),
        resource=BuildTxGroupsOperation,
    )
    dds.production_group("Aggregate", operation)
    return dds


def render_case() -> str:
    return emit_container_runtime_source(_build_dds())


def validate_case(source: str) -> None:
    namespace = {}
    exec(source, namespace)

    builder = namespace["new_builder"]()
    field = namespace["TransactionalField"]
    transactional_fields = namespace["TransactionalFieldsCollection"]

    builder.add(
        transactional_fields,
        field(name="session", tx_group="session", source_order=30),
    )
    builder.add(
        transactional_fields,
        field(name="count", tx_group="default", source_order=10),
    )
    builder.add(
        transactional_fields,
        field(name="owner", tx_group="resource", source_order=20),
    )
    builder.add(
        transactional_fields,
        field(name="label", tx_group="default", source_order=40),
    )
    container = namespace["build_container"](builder)

    groups = tuple(container.TxGroups.sequence())

    assert [(group.tx_group, group.tx_index) for group in groups] == [
        ("default", 0),
        ("resource", 1),
        ("session", 2),
    ]
    assert "DDSOperationContext" in source
    assert "ctx = DDSOperationContext(" in source
    assert "ctx.records(TransactionalFieldsCollection)" in source
    assert "astichi_hole" not in source
    assert "dds.operation(" not in source


if __name__ == "__main__":
    raise SystemExit(
        run_case("dds_ordered_aggregate_operation.py", render_case, validate_case)
    )
