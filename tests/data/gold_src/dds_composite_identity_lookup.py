from __future__ import annotations

from support.golden_case import run_case
from yidl.generation.data_def_sys import AddIfAbsent
from yidl.generation.data_def_sys import DataDefinitionSystem
from yidl.generation.data_def_sys import REQUIRED
from yidl.generation.data_def_sys import emit_container_runtime_source
from yidl.generation.data_def_sys import lookup
from yidl.generation.data_def_sys import read


def _build_dds() -> DataDefinitionSystem:
    dds = DataDefinitionSystem()
    name = dds.property("Name", str, default=REQUIRED, storage_name="name")
    tx_group = dds.property("TxGroup", str, default=REQUIRED, storage_name="tx_group")
    phase = dds.property("Phase", str, default=REQUIRED, storage_name="phase")
    tx_index = dds.property("TxIndex", int, default=REQUIRED, storage_name="tx_index")
    order = dds.property("Order", int, default=0, storage_name="order")

    tx_group_record = dds.record("TxGroupRecord", tx_group, phase, tx_index)
    field = dds.record("Field", name, tx_group, phase, order)
    contribution = dds.record("Contribution", tx_index, name, order)

    tx_groups = dds.collection(
        "TxGroups",
        tx_group_record,
        cardinality=dds.many,
        identity=(tx_group, phase),
    )
    fields = dds.collection("Fields", field, cardinality=dds.many, identity=name)
    contributions = dds.collection(
        "Contributions",
        contribution,
        cardinality=dds.many,
        identity=(tx_index, name),
    )
    production = dds.production(
        "FieldProvidesContribution",
        source=fields,
        target=contributions,
        values={
            tx_index: lookup(
                tx_groups,
                key=(read(tx_group), read(phase)),
                value=tx_index,
            ),
            name: read(name),
            order: read(order),
        },
        policy=AddIfAbsent,
    )
    dds.production_group("FieldChildren", production)
    return dds


def render_case() -> str:
    return emit_container_runtime_source(_build_dds())


def validate_case(source: str) -> None:
    namespace = {}
    exec(source, namespace)

    builder = namespace["new_builder"]()
    tx_group_record = namespace["TxGroupRecord"]
    field = namespace["Field"]
    tx_groups = namespace["TxGroupsCollection"]
    fields = namespace["FieldsCollection"]
    contributions = namespace["ContributionsCollection"]

    builder.add(tx_groups, tx_group_record(tx_group="main", phase="commit", tx_index=0))
    builder.add(tx_groups, tx_group_record(tx_group="aux", phase="commit", tx_index=1))
    builder.add(fields, field(name="owner", tx_group="main", phase="commit", order=2))
    builder.add(fields, field(name="memo", tx_group="aux", phase="commit", order=1))
    container = namespace["build_container"](builder)

    assert container.TxGroups.by_identity(("main", "commit")).tx_index == 0
    assert container.TxGroups.by_identity(("aux", "commit")).tx_index == 1
    assert container.Contributions.by_identity((0, "owner")).order == 2
    assert container.Contributions.by_identity((1, "memo")).order == 1
    assert [record.name for record in container.Contributions.sequence()] == [
        "owner",
        "memo",
    ]
    assert "identity=(_TxGroupProperty, _PhaseProperty)" in source
    assert "identity=(_TxIndexProperty, _NameProperty)" in source
    assert "lookup_0_key = (source.tx_group, source.phase)" in source
    assert "builder.by_identity(TxGroupsCollection, lookup_0_key)" in source
    assert "dds.collection(" not in source
    assert "dds.production(" not in source


if __name__ == "__main__":
    raise SystemExit(
        run_case("dds_composite_identity_lookup.py", render_case, validate_case)
    )
