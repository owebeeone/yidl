from __future__ import annotations

import pytest

from yidl.capsule.recorded_builder import CapsuleConceptBuilder
from yidl.capsule.recorded_builder import capsule_concept
from yidl.generation.data_def_sys import DataDefinitionSystem
from yidl.generation.data_def_sys import REQUIRED


def test_recorded_concept_plan_replays_property_definitions() -> None:
    builder = capsule_concept("property")
    name = builder.props.Name(str, REQUIRED)
    init = builder.props.Init(bool)

    plan = builder.build()
    dds = DataDefinitionSystem()
    plan.apply(dds)

    assert isinstance(builder, CapsuleConceptBuilder)
    assert name.name == "Name"
    assert init.name == "Init"
    assert [(prop.name, prop.storage_name, prop.default) for prop in dds.properties] == [
        ("Name", "name", REQUIRED),
        ("Init", "init", False),
    ]


def test_recorded_concept_builder_cannot_be_replayed_directly() -> None:
    builder = capsule_concept("property")
    builder.props.Name(str, REQUIRED)

    with pytest.raises(TypeError, match="build"):
        builder.apply(DataDefinitionSystem())  # type: ignore[attr-defined]


def test_recorded_concept_plan_is_immutable_after_build() -> None:
    builder = capsule_concept("property")
    builder.props.Name(str, REQUIRED)

    plan = builder.build()

    with pytest.raises(RuntimeError, match="already been built"):
        builder.props.Init(bool)

    dds = DataDefinitionSystem()
    plan.apply(dds)
    assert [prop.name for prop in dds.properties] == ["Name"]


def test_dependency_reference_reuses_parent_property_without_redefinition() -> None:
    parent = capsule_concept("property")
    parent_name = parent.props.Name(str, REQUIRED)
    parent_plan = parent.build()

    child = capsule_concept("frozen", requires=(parent_plan,))
    parent_ref = child.use(parent_plan)
    referenced_name = parent_ref.props.Name
    frozen = child.props.Frozen(bool)
    child_plan = child.build()

    dds = DataDefinitionSystem()
    child_plan.apply(dds)

    assert referenced_name == parent_name
    assert [prop.name for prop in dds.properties] == ["Name", "Frozen"]
    assert frozen.name == "Frozen"


def test_dependency_diamond_replays_parent_once() -> None:
    root = capsule_concept("root")
    root.props.Name(str, REQUIRED)
    root_plan = root.build()

    left = capsule_concept("left", requires=(root_plan,))
    left.props.Left(bool)
    left_plan = left.build()

    right = capsule_concept("right", requires=(root_plan,))
    right.props.Right(bool)
    right_plan = right.build()

    child = capsule_concept("child", requires=(left_plan, right_plan))
    child.props.Child(bool)
    child_plan = child.build()

    dds = DataDefinitionSystem()
    child_plan.apply(dds)

    assert [prop.name for prop in dds.properties] == [
        "Name",
        "Left",
        "Right",
        "Child",
    ]


def test_redefining_dependency_owned_property_rejects() -> None:
    parent = capsule_concept("property")
    parent.props.Name(str, REQUIRED)
    parent_plan = parent.build()

    child = capsule_concept("frozen", requires=(parent_plan,))
    child.props.Name(str, REQUIRED)
    child_plan = child.build()

    with pytest.raises(ValueError, match="property 'Name' is already owned"):
        child_plan.apply(DataDefinitionSystem())


def test_conflicting_property_definitions_reject() -> None:
    left = capsule_concept("left")
    left.props.Name(str, REQUIRED)
    left_plan = left.build()

    right = capsule_concept("right")
    right.props.Name(int, REQUIRED)
    right_plan = right.build()

    child = capsule_concept("child", requires=(left_plan, right_plan))
    child_plan = child.build()

    with pytest.raises(ValueError, match="property 'Name' is already owned"):
        child_plan.apply(DataDefinitionSystem())
