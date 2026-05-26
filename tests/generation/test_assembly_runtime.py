from __future__ import annotations

from types import SimpleNamespace

import astichi
from astichi.perf_counters import collect_perf_counters

from yidl.generation.assembly_plan import AssemblyEdgeSpec
from yidl.generation.assembly_plan import AssemblySpec
from yidl.generation.assembly_plan import BindingSpec
from yidl.generation.assembly_plan import ComposableProductionSpec
from yidl.generation.assembly_plan import ContributionMatcherSpec
from yidl.generation.assembly_plan import ContributionSpec
from yidl.generation.assembly_plan import InlineApplySpec
from yidl.generation.assembly_plan import LiteralValueRef
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


def test_nested_production_contribution_uses_lower_astichi_build(monkeypatch) -> None:
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
    assert counts["build_merge"] == 0


def test_run_assembly_uses_astichi_batch_scope(monkeypatch) -> None:
    monkeypatch.setenv("ASTICHI_LOWER_ENGINE", "python")
    concept = SimpleNamespace(
        properties={},
        resources={
            "ModuleRoot": from_astichi_code(
                "class class_name__astichi_arg__:\n"
                "    astichi_hole(body)\n"
            ),
            "Body": from_astichi_code(
                "def run(self):\n"
                "    return astichi_bind_external(result)\n"
            ),
        },
        contributions={
            "BodyContribution": ContributionSpec(
                name="BodyContribution",
                source_name="Body",
                source_kind="resource",
                build_name="Body",
                index=None,
                order=None,
                target=_target("body", "Root"),
                bindings=(
                    BindingSpec(
                        kind="external",
                        name="result",
                        value=LiteralValueRef("ok"),
                    ),
                ),
            ),
        },
        contribution_matchers={
            "BodyMatcher": ContributionMatcherSpec(
                name="BodyMatcher",
                inputs=(),
                default_contribution_name="BodyContribution",
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
                    bindings=(
                        BindingSpec(
                            kind="ident",
                            name="class_name",
                            value=LiteralValueRef("Generated"),
                        ),
                    ),
                ),
                applies=(_edge("module.body", "BodyMatcher"),),
            ),
        },
        assemblies={
            "Module": AssemblySpec(
                name="Module",
                production_name="ModuleProduction",
            ),
        },
    )

    with collect_perf_counters() as counters:
        result = run_assembly(concept, "Module", SimpleNamespace()).materialize()

    source = result.emit(provenance=False)
    namespace: dict[str, object] = {}
    exec(source, namespace)
    counts = counters.snapshot()["counts"]

    assert namespace["Generated"]().run() == "ok"  # type: ignore[operator]
    assert counts["scope_batch"] == 3
    assert counts["scope_batch_apply_count"] == 3
    assert counts["scope_batch_candidate_count"] == 3
    assert counts.get("candidate_lookup_lower", 0) == 0
    assert counts.get("assembly_scope_apply", 0) == 0
