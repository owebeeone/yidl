from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from types import MappingProxyType

from yidl.runtime.lifecycle_markers import FieldDecl
from yidl.runtime.lifecycle_markers import LifecycleDefinitionError
from yidl.runtime.lifecycle_markers import LifecycleMarker
from yidl.runtime.lifecycle_markers import MISSING
from yidl.runtime.lifecycle_markers import field
from yidl.runtime.lifecycle_markers import normalize_marker
from yidl.runtime.transaction_yidl import DEFAULT_TRANSACTION


LIFECYCLE_METADATA_VERSION = 1
ORDER_STEP = 10


@dataclass(frozen=True, slots=True)
class HarvestedLifecycle:
    """Lifecycle facts harvested from one decorated class."""

    class_fact: Mapping[str, object]
    field_facts: tuple[Mapping[str, object], ...]
    lifecycle_definition: Mapping[str, object]
    annotations: Mapping[str, object]
    tx_groups: tuple[object, ...]
    build_kwargs: Mapping[str, object]


def harvest_lifecycle_definition(cls: type[object]) -> HarvestedLifecycle:
    """Harvest Phase A-compatible lifecycle facts from ``cls``."""

    _reject_reserved_class_body_names(cls)
    annotations = dict(getattr(cls, "__annotations__", {}))
    class_fact = _class_fact(cls)
    class_id = str(class_fact["class_id"])
    class_name = str(class_fact["class_name"])

    field_facts: list[Mapping[str, object]] = []
    build_kwargs: dict[str, object] = {
        str(class_fact["lifecycle_definition_param_name"]): None,
        str(class_fact["annotations_param_name"]): MappingProxyType(dict(annotations)),
        str(class_fact["tx_groups_param_name"]): (),
    }
    tx_groups = _TxGroupBuilder()

    for field_index, (name, annotation) in enumerate(annotations.items()):
        marker = _marker_for(cls, name)
        decl = normalize_marker(name, annotation, marker, context=class_name)
        if decl.kind == "initvar" and decl.init is False:
            continue
        order = (field_index + 1) * ORDER_STEP
        fact = _field_fact(class_id, class_name, decl, order)
        field_facts.append(MappingProxyType(fact))
        if decl.kind == "managed":
            tx_groups.add(decl.tx_group)
        if decl.has_default:
            build_kwargs[str(fact["default_value_param_name"])] = decl.default
        if decl.has_default_factory:
            build_kwargs[str(fact["default_factory_param_name"])] = decl.default_factory

    tx_group_values = tx_groups.values()
    lifecycle_definition = MappingProxyType(
        {
            "version": LIFECYCLE_METADATA_VERSION,
            "class": MappingProxyType(dict(class_fact)),
            "fields": tuple(field_facts),
            "tx_groups": tx_group_values,
        },
    )
    build_kwargs[str(class_fact["lifecycle_definition_param_name"])] = (
        lifecycle_definition
    )
    build_kwargs[str(class_fact["tx_groups_param_name"])] = tx_group_values

    return HarvestedLifecycle(
        class_fact=MappingProxyType(dict(class_fact)),
        field_facts=tuple(field_facts),
        lifecycle_definition=lifecycle_definition,
        annotations=MappingProxyType(dict(annotations)),
        tx_groups=tx_group_values,
        build_kwargs=MappingProxyType(build_kwargs),
    )


def _class_fact(cls: type[object]) -> dict[str, object]:
    class_name = cls.__name__
    class_id = cls.__qualname__
    return {
        "class_id": class_id,
        "class_name": class_name,
        "class_order": ORDER_STEP,
        "module_name": cls.__module__,
        "state_class_name": f"{class_name}_State",
        "facade_base_class_name": f"{class_name}_FacadeBase",
        "current_facade_class_name": f"{class_name}_Current",
        "working_facade_class_name": f"{class_name}_Working",
        "lifecycle_definition_param_name": f"_{class_name}_lifecycle_definition",
        "annotations_param_name": f"_{class_name}_annotations",
        "tx_groups_param_name": f"_{class_name}_tx_groups",
    }


def _field_fact(
    class_id: str,
    class_name: str,
    decl: FieldDecl,
    order: int,
) -> dict[str, object]:
    name = decl.name
    kind = decl.kind
    fact: dict[str, object] = {
        "field_id": f"{class_id}.{name}",
        "field_owner": class_id,
        "field_name": name,
        "field_order": order,
        "field_kind": kind,
        "annotation": decl.annotation,
        "init": decl.init,
        "has_default": decl.has_default,
        "default_value": decl.default,
        "default_value_param_name": (
            f"_{class_name}_{name}_default" if decl.has_default else ""
        ),
        "has_default_factory": decl.has_default_factory,
        "default_factory": decl.default_factory,
        "default_factory_param_name": (
            f"_{class_name}_{name}_default_factory"
            if decl.has_default_factory
            else ""
        ),
        "tx_group_key": None,
        "value_slot_name": "",
        "current_slot_name": "",
        "working_slot_name": "",
    }
    if kind == "field":
        fact["value_slot_name"] = f"_y_{name}_value"
    elif kind == "managed":
        fact["tx_group_key"] = decl.tx_group
        fact["current_slot_name"] = f"_y_{name}_current"
        fact["working_slot_name"] = f"_y_{name}_working"
    return fact


def _marker_for(cls: type[object], name: str) -> LifecycleMarker:
    value = cls.__dict__.get(name, MISSING)
    if isinstance(value, LifecycleMarker):
        return value
    if value is MISSING:
        return field()
    return field(default=value)


def _reject_reserved_class_body_names(cls: type[object]) -> None:
    for name in cls.__dict__:
        if name.startswith("_y_") or (
            name.startswith("__yidl_") and name.endswith("__")
        ):
            raise LifecycleDefinitionError(
                f"{cls.__name__}.{name}: reserved lifecycle name",
            )


@dataclass(slots=True)
class _TxGroupBuilder:
    _groups: list[object] | None = None

    def __post_init__(self) -> None:
        if self._groups is None:
            self._groups = [DEFAULT_TRANSACTION]

    def add(self, group: object) -> None:
        groups = self._require_groups()
        if group not in groups:
            groups.append(group)

    def values(self) -> tuple[object, ...]:
        return tuple(self._require_groups())

    def _require_groups(self) -> list[object]:
        if self._groups is None:
            raise RuntimeError("transaction group builder is not initialized")
        return self._groups
