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


def test_combined_layer_exposes_managed_field_record() -> None:
    generated = _compiled_namespace(
        paths=tuple(sorted(_YIDL_DIR.glob("*.yidl"))),
        entry_path=_YIDL_DIR / "lifecycle_base.yidl",
        concept_name="LifecycleBase",
    )

    assert hasattr(generated, "ManagedField")


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
