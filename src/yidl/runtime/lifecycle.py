from __future__ import annotations

from types import ModuleType

from yidl.runtime.lifecycle_markers import FieldDecl
from yidl.runtime.lifecycle_markers import LifecycleDefinitionError
from yidl.runtime.lifecycle_markers import LifecycleMarker
from yidl.runtime.lifecycle_markers import MISSING
from yidl.runtime.lifecycle_markers import classvar
from yidl.runtime.lifecycle_markers import field
from yidl.runtime.lifecycle_markers import initvar
from yidl.runtime.lifecycle_markers import managed
from yidl.runtime.lifecycle_markers import normalize_marker
from yidl.runtime.lifecycle_harvester import HarvestedLifecycle
from yidl.runtime.lifecycle_harvester import harvest_lifecycle_definition


def lifecycle(cls: type[object]) -> type[object]:
    """Decorate ``cls`` with the generated lifecycle implementation."""

    if not isinstance(cls, type):
        raise TypeError("@lifecycle can only decorate classes")
    harvested = harvest_lifecycle_definition(cls)
    source = _generate_lifecycle_source(harvested)
    namespace: dict[str, object] = {"__name__": cls.__module__}
    exec(source, namespace)
    generated = namespace["build_lifecycle_class"](
        cls,
        **dict(harvested.build_kwargs),
    )
    if not isinstance(generated, type):
        raise TypeError("generated lifecycle builder did not return a class")
    return generated


def _generate_lifecycle_source(harvested: HarvestedLifecycle) -> str:
    generated = _generated_lifecycle_base_module()
    return generated.build_LifecycleModule(
        _build_lifecycle_container(generated, harvested),
    ).emit_commented()


def _build_lifecycle_container(
    generated: ModuleType,
    harvested: HarvestedLifecycle,
) -> object:
    builder = generated.new_builder()
    builder.add(
        generated.ClassesCollection,
        generated.LifecycleClass(**dict(harvested.class_fact)),
    )
    for fact in harvested.field_facts:
        builder.add(
            generated.FieldsCollection,
            _field_record_type(generated, str(fact["field_kind"]))(**dict(fact)),
        )
    return generated.build_container(builder)


def _field_record_type(generated: ModuleType, kind: str) -> type[object]:
    if kind == "field":
        return generated.PlainField
    if kind == "initvar":
        return generated.InitVarField
    if kind == "classvar":
        return generated.ClassVarField
    if kind == "managed":
        return generated.ManagedField
    raise LifecycleDefinitionError(f"unsupported lifecycle field kind: {kind!r}")


def _generated_lifecycle_base_module() -> ModuleType:
    from yidl.runtime import _generated_lifecycle_base

    return _generated_lifecycle_base


__all__ = [
    "FieldDecl",
    "LifecycleDefinitionError",
    "LifecycleMarker",
    "MISSING",
    "classvar",
    "field",
    "HarvestedLifecycle",
    "harvest_lifecycle_definition",
    "initvar",
    "lifecycle",
    "managed",
    "normalize_marker",
]
