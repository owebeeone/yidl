from __future__ import annotations

from support.golden_case import run_case
from yidl.generation.data_def_sys import AddIfAbsent
from yidl.generation.data_def_sys import DataDefinitionSystem
from yidl.generation.data_def_sys import REQUIRED
from yidl.generation.data_def_sys import ReplaceExisting
from yidl.generation.data_def_sys import emit_container_runtime_source


def _build_dds() -> DataDefinitionSystem:
    dds = DataDefinitionSystem()
    name = dds.property("Name", str, default=REQUIRED, storage_name="name")
    value = dds.property("Value", int, default=REQUIRED, storage_name="value")
    item = dds.record("Item", name, value)
    dds.collection("Items", item, cardinality=dds.many, identity=name)
    return dds


def render_case() -> str:
    return emit_container_runtime_source(_build_dds())


def validate_case(source: str) -> None:
    namespace = {}
    exec(source, namespace)

    builder = namespace["new_builder"]()
    item = namespace["Item"]
    items = namespace["ItemsCollection"]

    builder.write(items, item(name="count", value=1))
    builder.write(items, item(name="count", value=2), policy=namespace["AddIfAbsent"])
    builder.write(items, item(name="label", value=3))
    builder.write(items, item(name="label", value=4), policy=namespace["ReplaceExisting"])

    container = builder.freeze()

    assert [record.value for record in container.Items.sequence()] == [1, 4]
    assert "AddIfAbsent" in source
    assert "ReplaceExisting" in source
    assert "RejectDuplicate" in source
    assert "def write(self, *args, **kwargs):" in source
    assert "DataDefinitionSystem()" not in source


if __name__ == "__main__":
    raise SystemExit(run_case("dds_write_policy.py", render_case, validate_case))
