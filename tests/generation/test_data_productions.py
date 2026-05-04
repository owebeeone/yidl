from __future__ import annotations

import pytest

from yidl.generation.data_def_sys import AddIfAbsent
from yidl.generation.data_def_sys import DataDefinitionSystem
from yidl.generation.data_def_sys import REQUIRED
from yidl.generation.data_def_sys import call
from yidl.generation.data_def_sys import read


def test_production_rejects_union_target() -> None:
    dds = DataDefinitionSystem()
    name = dds.property("Name", str, default=REQUIRED, storage_name="name")
    source_record = dds.record("Source", name)
    source = dds.collection("Sources", source_record, cardinality=dds.many)
    target_union = dds.union("Targets")
    target_union.variant("Target", name)
    target = dds.collection("Targets", target_union, cardinality=dds.many, identity=name)

    with pytest.raises(ValueError, match="concrete record"):
        dds.production(
            "BadTarget",
            source=source,
            target=target,
            values={name: read(name)},
        )


def test_production_rejects_missing_required_target_value() -> None:
    dds = DataDefinitionSystem()
    name = dds.property("Name", str, default=REQUIRED, storage_name="name")
    value = dds.property("Value", int, default=REQUIRED, storage_name="value")
    source_record = dds.record("Source", name)
    target_record = dds.record("Target", name, value)
    source = dds.collection("Sources", source_record, cardinality=dds.many)
    target = dds.collection("Targets", target_record, cardinality=dds.many, identity=name)

    with pytest.raises(ValueError, match="missing required target value"):
        dds.production(
            "MissingValue",
            source=source,
            target=target,
            values={name: read(name)},
        )


def test_production_rejects_cross_system_source_target() -> None:
    left = DataDefinitionSystem()
    right = DataDefinitionSystem()
    left_name = left.property("Name", str, default=REQUIRED, storage_name="name")
    right_name = right.property("Name", str, default=REQUIRED, storage_name="name")
    source_record = left.record("Source", left_name)
    target_record = right.record("Target", right_name)
    source = left.collection("Sources", source_record, cardinality=left.many)
    target = right.collection("Targets", target_record, cardinality=right.many)

    with pytest.raises(ValueError, match="same data-definition system"):
        left.production(
            "CrossSystem",
            source=source,
            target=target,
            values={right_name: read(left_name)},
        )


def test_production_group_rejects_foreign_production() -> None:
    left = DataDefinitionSystem()
    right = DataDefinitionSystem()
    left_name = left.property("Name", str, default=REQUIRED, storage_name="name")
    right_name = right.property("Name", str, default=REQUIRED, storage_name="name")
    left_record = left.record("Source", left_name)
    right_record = right.record("Source", right_name)
    left_source = left.collection("Sources", left_record, cardinality=left.many)
    right_source = right.collection("Sources", right_record, cardinality=right.many)
    production = right.production(
        "RightProduction",
        source=right_source,
        target=right_source,
        values={right_name: read(right_name)},
        policy=AddIfAbsent,
    )

    with pytest.raises(ValueError, match="same data-definition system"):
        left.production_group("Group", production)


def test_production_rejects_unemittable_call_without_source_name() -> None:
    dds = DataDefinitionSystem()
    name = dds.property("Name", str, default=REQUIRED, storage_name="name")
    value = dds.property("Value", int, default=REQUIRED, storage_name="value")
    source_record = dds.record("Source", name)
    target_record = dds.record("Target", name, value)
    source = dds.collection("Sources", source_record, cardinality=dds.many)
    target = dds.collection("Targets", target_record, cardinality=dds.many, identity=name)

    def value_for(source_record: object) -> int:
        del source_record
        return 1

    dds.production(
        "NeedsCallName",
        source=source,
        target=target,
        values={name: read(name), value: call("value-for", value_for)},
    )

    with pytest.raises(ValueError, match="computed value"):
        dds.emit_container_runtime_source()

