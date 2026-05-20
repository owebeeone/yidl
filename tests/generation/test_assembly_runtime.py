from __future__ import annotations

from types import SimpleNamespace

import astichi

from yidl.generation.assembly_plan import AssemblyEdgeSpec
from yidl.generation.assembly_plan import AssemblySpec
from yidl.generation.assembly_plan import ComposableProductionSpec
from yidl.generation.assembly_plan import ContributionMatcherSpec
from yidl.generation.assembly_plan import ContributionSpec
from yidl.generation.assembly_plan import InlineApplySpec
from yidl.generation.assembly_plan import PathSegmentSpec
from yidl.generation.assembly_plan import PathSpec
from yidl.generation.assembly_plan import RootSpec
from yidl.generation.assembly_plan import TargetPathSpec
from yidl.generation.assembly_plan import TargetSpec
from yidl.generation.assembly_runtime import run_assembly
from yidl.generation.matcher_values import from_astichi_code


def _path(*names: str) -> PathSpec:
    return PathSpec(
        tuple(PathSegmentSpec(kind="name", name=name) for name in names)
    )


def _target(name: str, *build_path: str) -> TargetSpec:
    return TargetSpec(
        name=name,
        paths=(
            TargetPathSpec(
                kind="build",
                path=_path(*build_path),
            ),
        ),
    )


def _edge(name: str, matcher_name: str) -> InlineApplySpec:
    return InlineApplySpec(
        AssemblyEdgeSpec(
            name=name,
            context_inputs=(),
            from_inputs=(),
            condition=None,
            matcher_name=matcher_name,
        )
    )


def test_nested_production_contribution_runs_in_one_astichi_build(monkeypatch) -> None:
    concept = SimpleNamespace(
        properties={},
        resources={
            "ModuleRoot": from_astichi_code("astichi_hole(body)"),
            "ChildRoot": from_astichi_code("astichi_hole(items)"),
            "Item": from_astichi_code("item = 1"),
        },
        contributions={
            "ChildContribution": ContributionSpec(
                name="ChildContribution",
                source_name="ChildProduction",
                source_kind="production",
                build_name="Child",
                index=None,
                order=None,
                target=_target("body", "Root"),
                bindings=(),
            ),
            "ItemContribution": ContributionSpec(
                name="ItemContribution",
                source_name="Item",
                source_kind="resource",
                build_name="Item",
                index=None,
                order=None,
                target=_target("items", "Child"),
                bindings=(),
            ),
        },
        contribution_matchers={
            "ChildMatcher": ContributionMatcherSpec(
                name="ChildMatcher",
                inputs=(),
                default_contribution_name="ChildContribution",
                rules=(),
            ),
            "ItemMatcher": ContributionMatcherSpec(
                name="ItemMatcher",
                inputs=(),
                default_contribution_name="ItemContribution",
                rules=(),
            ),
        },
        assembly_edges={},
        composable_productions={
            "ModuleProduction": ComposableProductionSpec(
                name="ModuleProduction",
                inputs=(),
                root=RootSpec(
                    build_name="Root",
                    resource_name="ModuleRoot",
                    bindings=(),
                ),
                applies=(_edge("module.child", "ChildMatcher"),),
            ),
            "ChildProduction": ComposableProductionSpec(
                name="ChildProduction",
                inputs=(),
                root=RootSpec(
                    build_name="Child",
                    resource_name="ChildRoot",
                    bindings=(),
                ),
                applies=(_edge("child.item", "ItemMatcher"),),
            ),
        },
        assemblies={
            "Module": AssemblySpec(
                name="Module",
                production_name="ModuleProduction",
            ),
        },
    )
    counts = {"build_merge": 0}
    import astichi.materialize as materialize_module

    original_build_merge = materialize_module.build_merge

    def counted_build_merge(*args, **kwargs):
        counts["build_merge"] += 1
        return original_build_merge(*args, **kwargs)

    monkeypatch.setattr(materialize_module, "build_merge", counted_build_merge)

    result = run_assembly(concept, "Module", SimpleNamespace()).materialize()

    assert result.emit(provenance=False) == "item = 1\n"
    assert counts["build_merge"] == 1
