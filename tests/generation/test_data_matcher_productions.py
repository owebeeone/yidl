from __future__ import annotations

import pytest

from yidl.generation.data_def_sys import DataDefinitionSystem
from yidl.generation.data_def_sys import REQUIRED
from yidl.generation.data_def_sys import from_literal
from yidl.generation.data_def_sys import match
from yidl.generation.data_def_sys import read


def test_match_expression_requires_matcher_result_source() -> None:
    dds = DataDefinitionSystem()
    name = dds.property("Name", str, default=REQUIRED, storage_name="name")
    source_record = dds.record("Source", name)
    target_record = dds.record("Target", name)
    source = dds.collection("Sources", source_record, cardinality=dds.many)
    target = dds.collection("Targets", target_record, cardinality=dds.many)

    with pytest.raises(ValueError, match="source=matcher.results"):
        dds.production(
            "BadSource",
            source=source,
            target=target,
            values={name: match.resource()},
        )


def test_matcher_result_source_rejects_read_property_shortcut() -> None:
    dds = DataDefinitionSystem()
    name = dds.property("Name", str, default=REQUIRED, storage_name="name")
    field = dds.record("Field", name)
    fields = dds.collection("Fields", field, cardinality=dds.many)
    target = dds.collection("Targets", field, cardinality=dds.many)
    matcher = dds.matcher("FieldMatcher")
    matcher.input("field", fields)
    matcher.default(from_literal("field"))

    with pytest.raises(ValueError, match="match.record"):
        dds.production(
            "BadRead",
            source=matcher.results(),
            target=target,
            values={name: read(name)},
        )


def test_matcher_result_source_rejects_unknown_input_name() -> None:
    dds = DataDefinitionSystem()
    name = dds.property("Name", str, default=REQUIRED, storage_name="name")
    field = dds.record("Field", name)
    fields = dds.collection("Fields", field, cardinality=dds.many)
    target = dds.collection("Targets", field, cardinality=dds.many)
    matcher = dds.matcher("FieldMatcher")
    matcher.input("field", fields)
    matcher.default(from_literal("field"))

    with pytest.raises(ValueError, match="has no input"):
        dds.production(
            "BadInput",
            source=matcher.results(),
            target=target,
            values={name: match.record("missing").prop(name)},
        )


def test_matcher_result_source_rejects_out_of_range_tuple_value() -> None:
    dds = DataDefinitionSystem()
    name = dds.property("Name", str, default=REQUIRED, storage_name="name")
    init = dds.property("Init", bool, default=True, storage_name="init")
    field = dds.record("Field", name, init)
    target_record = dds.record("Target", name, init)
    fields = dds.collection("Fields", field, cardinality=dds.many)
    target = dds.collection("Targets", target_record, cardinality=dds.many)
    matcher = dds.matcher("FieldMatcher")
    field_input = matcher.input("field", fields)
    matcher.default(from_literal("field"))
    matcher.rule(
        when=(field_input.prop(init).eq(True),),
        resource=from_literal("init"),
    )

    with pytest.raises(ValueError, match="out of range"):
        dds.production(
            "BadTupleIndex",
            source=matcher.results(),
            target=target,
            values={name: match.record("field").prop(name), init: match.value(1)},
        )
