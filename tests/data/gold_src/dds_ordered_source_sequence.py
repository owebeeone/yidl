from __future__ import annotations

from support.golden_case import run_case
from yidl.generation.data_def_sys import AddIfAbsent
from yidl.generation.data_def_sys import DataDefinitionSystem
from yidl.generation.data_def_sys import REQUIRED
from yidl.generation.data_def_sys import emit_container_runtime_source
from yidl.generation.data_def_sys import read


def _build_dds() -> DataDefinitionSystem:
    dds = DataDefinitionSystem()
    name = dds.property("Name", str, default=REQUIRED, storage_name="name")
    layer = dds.property("Layer", int, default=0, storage_name="layer")
    order = dds.property("Order", int, default=0, storage_name="order")

    source_record = dds.record("SourceItem", name, layer, order)
    target_record = dds.record("OrderedItem", name, layer, order)
    source_items = dds.collection(
        "SourceItems",
        source_record,
        cardinality=dds.many,
        identity=name,
    )
    ordered_items = dds.collection(
        "OrderedItems",
        target_record,
        cardinality=dds.many,
        identity=name,
    )
    production = dds.production(
        "SourceProvidesOrderedItem",
        source=source_items.ordered(layer, order),
        target=ordered_items,
        values={
            name: read(name),
            layer: read(layer),
            order: read(order),
        },
        policy=AddIfAbsent,
    )
    dds.production_group("OrderedSources", production)
    return dds


def render_case() -> str:
    return emit_container_runtime_source(_build_dds())


def validate_case(source: str) -> None:
    namespace = {}
    exec(source, namespace)

    builder = namespace["new_builder"]()
    source_item = namespace["SourceItem"]
    source_items = namespace["SourceItemsCollection"]

    builder.add(source_items, source_item(name="first-tie", layer=1, order=1))
    builder.add(source_items, source_item(name="later", layer=2, order=0))
    builder.add(source_items, source_item(name="second-tie", layer=1, order=1))
    builder.add(source_items, source_item(name="earlier", layer=0, order=3))
    container = namespace["build_container"](builder)

    assert [record.name for record in container.OrderedItems.sequence()] == [
        "earlier",
        "first-tie",
        "second-tie",
        "later",
    ]
    assert "builder.ordered_records(SourceItemsCollection, _LayerProperty, _OrderProperty)" in source
    assert "builder.records(SourceItemsCollection)" not in source
    assert "dds.production(" not in source


if __name__ == "__main__":
    raise SystemExit(
        run_case("dds_ordered_source_sequence.py", render_case, validate_case)
    )
