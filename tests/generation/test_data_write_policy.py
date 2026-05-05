from __future__ import annotations

import pytest

from yidl.generation.data_def_sys import AddIfAbsent
from yidl.generation.data_def_sys import DataDefinitionSystem
from yidl.generation.data_def_sys import REQUIRED
from yidl.generation.data_def_sys import RejectDuplicate
from yidl.generation.data_def_sys import ReplaceExisting


def _items_shape() -> tuple[DataDefinitionSystem, object, object]:
    dds = DataDefinitionSystem()
    name = dds.property("Name", str, default=REQUIRED, storage_name="name")
    value = dds.property("Value", int, default=REQUIRED, storage_name="value")
    item = dds.record("Item", name, value)
    keyed_items = dds.collection("Items", item, cardinality=dds.many, identity=name)
    unkeyed_items = dds.collection("LogItems", item, cardinality=dds.many)
    return dds, keyed_items, unkeyed_items


def test_write_add_if_absent_keeps_first_identity() -> None:
    dds, items, _ = _items_shape()
    first = items.record(name="count", value=1)
    second = items.record(name="count", value=2)
    builder = dds.container_builder()

    builder.write(items, first, policy=AddIfAbsent)
    builder.write(items, second, policy=AddIfAbsent)

    assert builder.records(items) == (first,)
    assert builder.by_identity(items, "count") is first


def test_write_replace_existing_replaces_same_identity() -> None:
    dds, items, _ = _items_shape()
    first = items.record(name="count", value=1)
    second = items.record(name="count", value=2)
    builder = dds.container_builder()

    builder.write(items, first)
    builder.write(items, second, policy=ReplaceExisting)

    assert builder.records(items) == (second,)
    assert builder.by_identity(items, "count") is second


def test_write_reject_duplicate_matches_add_semantics() -> None:
    dds, items, _ = _items_shape()
    first = items.record(name="count", value=1)
    duplicate = items.record(name="count", value=2)
    builder = dds.container_builder()

    builder.write(items, first, policy=RejectDuplicate)
    builder.write(items, first, policy=RejectDuplicate)

    with pytest.raises(ValueError, match="duplicate identity"):
        builder.write(items, duplicate, policy=RejectDuplicate)

    assert builder.records(items) == (first,)


def test_write_rejects_duplicate_composite_identity() -> None:
    dds = DataDefinitionSystem()
    kind = dds.property("Kind", str, default=REQUIRED, storage_name="kind")
    name = dds.property("Name", str, default=REQUIRED, storage_name="name")
    value = dds.property("Value", int, default=REQUIRED, storage_name="value")
    item = dds.record("Item", kind, name, value)
    items = dds.collection(
        "Items",
        item,
        cardinality=dds.many,
        identity=(kind, name),
    )
    first = items.record(kind="field", name="count", value=1)
    duplicate = items.record(kind="field", name="count", value=2)
    builder = dds.container_builder()

    builder.write(items, first, policy=RejectDuplicate)

    with pytest.raises(ValueError, match=r"duplicate identity \('field', 'count'\)"):
        builder.write(items, duplicate, policy=RejectDuplicate)


def test_write_policies_on_unkeyed_collection() -> None:
    dds, _, log_items = _items_shape()
    first = log_items.record(name="first", value=1)
    second = log_items.record(name="first", value=2)
    builder = dds.container_builder()

    builder.write(log_items, first, policy=RejectDuplicate)
    builder.write(log_items, first, policy=RejectDuplicate)
    builder.write(log_items, second, policy=RejectDuplicate)

    assert builder.records(log_items) == (first, second)
    with pytest.raises(ValueError, match="requires an identity"):
        builder.write(log_items, second, policy=AddIfAbsent)
    with pytest.raises(ValueError, match="requires an identity"):
        builder.write(log_items, second, policy=ReplaceExisting)


def test_write_after_freeze_rejects() -> None:
    dds, items, _ = _items_shape()
    item = items.record(name="count", value=1)
    builder = dds.container_builder()
    builder.freeze()

    with pytest.raises(RuntimeError, match="frozen"):
        builder.write(items, item)
