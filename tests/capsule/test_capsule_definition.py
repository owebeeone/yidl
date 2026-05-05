from __future__ import annotations

import pytest

from yidl.capsule.definition import CapsuleDefinition
from yidl.capsule.definition import capsule
from yidl.capsule.definition import concept
from yidl.generation.data_def_sys import DataDefinitionSystem
from yidl.generation.data_def_sys import REQUIRED


def define_class_input(dds: DataDefinitionSystem) -> None:
    name = dds.ensure_property("Name", str, default=REQUIRED, storage_name="name")
    runtime_value = dds.ensure_property(
        "RuntimeValue",
        object,
        default=REQUIRED,
        storage_name="runtime_value",
    )
    record = dds.ensure_record("ClassInput", name, runtime_value)
    dds.ensure_collection(
        "ClassInputs",
        record,
        cardinality=dds.single,
        identity=name,
    )


def define_field_input(dds: DataDefinitionSystem) -> None:
    name = dds.ensure_property("Name", str, default=REQUIRED, storage_name="name")
    init = dds.ensure_property("Init", bool, default=True, storage_name="init")
    record = dds.ensure_record("FieldInput", name, init)
    dds.ensure_collection(
        "Fields",
        record,
        cardinality=dds.many,
        identity=name,
    )


def test_capsule_definition_composes_named_dds_concepts() -> None:
    definition = capsule(
        "ExampleCapsule",
        concept("class-input", define_class_input),
    ).extend(concept("field-input", define_field_input))

    dds = definition.build_data_definition()

    assert isinstance(definition, CapsuleDefinition)
    assert definition.concept_names == ("class-input", "field-input")
    assert [record.name for record in dds.records] == ["ClassInput", "FieldInput"]
    assert [collection.name for collection in dds.collections] == [
        "ClassInputs",
        "Fields",
    ]


def test_capsule_definition_rejects_incompatible_concept_extensions() -> None:
    def define_name_as_int(dds: DataDefinitionSystem) -> None:
        dds.ensure_property("Name", int, default=REQUIRED, storage_name="name")

    definition = capsule(
        "BrokenCapsule",
        define_class_input,
        define_name_as_int,
    )

    with pytest.raises(
        ValueError,
        match="property 'Name' is already defined differently",
    ):
        definition.build_data_definition()
