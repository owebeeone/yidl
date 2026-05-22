from __future__ import annotations

from pathlib import Path
from types import SimpleNamespace

import pytest

from yidl.concept_parser import compile_yidl_files
from yidl.generation.data_def_sys import emit_concept_runtime_source
from yidl.runtime.lifecycle import _build_lifecycle_container
from yidl.runtime.lifecycle import LifecycleDefinitionError
from yidl.runtime.lifecycle import harvest_lifecycle_definition
from yidl.runtime.lifecycle import managed
from yidl.runtime.lifecycle import transient


_YIDL_DIR = Path("tests/data/yidl/yidl_transactional_lifecycle")


def test_core_layer_rejects_managed_field_with_missing_layer_diagnostic() -> None:
    generated = _compiled_namespace(
        paths=(_YIDL_DIR / "lifecycle_core.yidl",),
        entry_path=_YIDL_DIR / "lifecycle_core.yidl",
        concept_name="LifecycleCore",
    )

    class Counter:
        value: int = managed(default=1)

    harvested = harvest_lifecycle_definition(Counter)

    with pytest.raises(
        LifecycleDefinitionError,
        match="managed lifecycle field requires generated record ManagedField",
    ):
        _build_lifecycle_container(generated, harvested)


def test_default_factory_layer_rejects_transient_field_with_missing_layer_diagnostic() -> None:
    generated = _compiled_namespace(
        paths=(
            _YIDL_DIR / "lifecycle_core.yidl",
            _YIDL_DIR / "lifecycle_managed.yidl",
            _YIDL_DIR / "lifecycle_default_factories.yidl",
        ),
        entry_path=_YIDL_DIR / "lifecycle_default_factories.yidl",
        concept_name="LifecycleDefaultFactories",
    )

    class Counter:
        scratch: list[int] = transient(default_factory=list)

    harvested = harvest_lifecycle_definition(Counter)

    with pytest.raises(
        LifecycleDefinitionError,
        match="transient lifecycle field requires generated record TransientField",
    ):
        _build_lifecycle_container(generated, harvested)


def test_lifecycle_layers_have_distinct_surfaces() -> None:
    core = _compiled_namespace(
        paths=(_YIDL_DIR / "lifecycle_core.yidl",),
        entry_path=_YIDL_DIR / "lifecycle_core.yidl",
        concept_name="LifecycleCore",
    )
    assert hasattr(core, "build_LifecycleCoreModule")
    assert not hasattr(core, "build_LifecycleModule")
    assert not hasattr(core, "ManagedField")
    assert not hasattr(core, "ManagedFieldsCollection")
    assert not hasattr(core, "TxGroup")
    assert not hasattr(core, "DefaultFactoryDependency")

    managed = _compiled_namespace(
        paths=(
            _YIDL_DIR / "lifecycle_core.yidl",
            _YIDL_DIR / "lifecycle_managed.yidl",
        ),
        entry_path=_YIDL_DIR / "lifecycle_managed.yidl",
        concept_name="LifecycleManaged",
    )
    assert hasattr(managed, "ManagedField")
    assert hasattr(managed, "ManagedFieldsCollection")
    assert hasattr(managed, "TxGroup")
    assert not hasattr(managed, "DefaultFactoryDependency")
    assert not hasattr(managed, "build_LifecycleModule")

    default_factories = _compiled_namespace(
        paths=(
            _YIDL_DIR / "lifecycle_core.yidl",
            _YIDL_DIR / "lifecycle_managed.yidl",
            _YIDL_DIR / "lifecycle_default_factories.yidl",
        ),
        entry_path=_YIDL_DIR / "lifecycle_default_factories.yidl",
        concept_name="LifecycleDefaultFactories",
    )
    assert hasattr(default_factories, "ManagedField")
    assert hasattr(default_factories, "DefaultFactoryDependency")
    assert not hasattr(default_factories, "TransientField")
    assert not hasattr(default_factories, "build_LifecycleModule")

    transient_layer = _compiled_namespace(
        paths=(
            _YIDL_DIR / "lifecycle_core.yidl",
            _YIDL_DIR / "lifecycle_managed.yidl",
            _YIDL_DIR / "lifecycle_default_factories.yidl",
            _YIDL_DIR / "lifecycle_transient.yidl",
        ),
        entry_path=_YIDL_DIR / "lifecycle_transient.yidl",
        concept_name="LifecycleTransient",
    )
    assert hasattr(transient_layer, "ManagedField")
    assert hasattr(transient_layer, "DefaultFactoryDependency")
    assert hasattr(transient_layer, "TransientField")
    assert hasattr(transient_layer, "TransientFieldsCollection")
    assert not hasattr(transient_layer, "build_LifecycleModule")


def test_combined_layer_exposes_managed_field_record() -> None:
    generated = _compiled_namespace(
        paths=tuple(sorted(_YIDL_DIR.glob("*.yidl"))),
        entry_path=_YIDL_DIR / "lifecycle_base.yidl",
        concept_name="LifecycleBase",
    )

    assert hasattr(generated, "ManagedField")
    assert hasattr(generated, "DefaultFactoryDependency")
    assert hasattr(generated, "TransientField")
    assert hasattr(generated, "build_LifecycleModule")


def _compiled_namespace(
    *,
    paths: tuple[Path, ...],
    entry_path: Path,
    concept_name: str,
) -> SimpleNamespace:
    concept = compile_yidl_files(
        {path.as_posix(): path.read_text(encoding="utf-8") for path in paths},
        entry_path.as_posix(),
    ).concepts[concept_name]
    source = emit_concept_runtime_source(
        concept.plan.build_data_definition(),
        resources=concept.resources,
        assembly_plan=concept,
    )
    namespace: dict[str, object] = {}
    exec(source, namespace)
    return SimpleNamespace(**namespace)
