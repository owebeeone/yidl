from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
import inspect
from types import MappingProxyType
import warnings

from yidl.runtime.lifecycle_markers import FieldDecl
from yidl.runtime.lifecycle_markers import LifecycleDefinitionError
from yidl.runtime.lifecycle_markers import LifecycleDefinitionWarning
from yidl.runtime.lifecycle_markers import LifecycleMarker
from yidl.runtime.lifecycle_markers import MISSING
from yidl.runtime.lifecycle_markers import field
from yidl.runtime.lifecycle_markers import normalize_marker
from yidl.runtime.transaction_yidl import DEFAULT_TRANSACTION

LIFECYCLE_METADATA_VERSION = 1
ORDER_STEP = 10
_FACADE_EXPOSURE_NAMES = frozenset({"default", "current", "working"})
_GENERATED_HELPER_NAMES = frozenset(
    {"begin", "validate", "commit_only", "commit", "rollback"}
)


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
    annotations = dict(cls.__dict__.get("__annotations__", {}))
    class_fact = _class_fact(cls)
    _reject_generated_name_collisions(cls, annotations, class_fact)
    class_id = str(class_fact["class_id"])
    class_name = str(class_fact["class_name"])

    field_facts_by_name: dict[str, Mapping[str, object]] = {}
    build_kwargs: dict[str, object] = {
        str(class_fact["lifecycle_definition_param_name"]): None,
        str(class_fact["annotations_param_name"]): MappingProxyType(dict(annotations)),
        str(class_fact["tx_groups_param_name"]): (),
    }
    tx_groups = _TxGroupBuilder()
    next_order = ORDER_STEP

    for definition in _inherited_lifecycle_definitions(cls):
        for group in _definition_tx_groups(definition):
            tx_groups.add(group)
        for inherited_fact in _definition_field_facts(definition):
            name = str(inherited_fact["field_name"])
            if name in field_facts_by_name:
                continue
            fact = _remap_inherited_field_fact(class_id, class_name, inherited_fact)
            field_facts_by_name[name] = MappingProxyType(fact)
            next_order = max(next_order, int(fact["field_order"]) + ORDER_STEP)

    for name, annotation in annotations.items():
        marker = _marker_for(cls, name)
        decl = normalize_marker(name, annotation, marker, context=class_name)
        if (
            decl.kind == "initvar"
            and decl.init is False
            and not decl.has_default
            and not decl.has_default_factory
        ):
            raise LifecycleDefinitionError(
                f"{class_name}.{decl.name}: initvar(init=False) must define "
                "default or default_factory",
            )
        existing = field_facts_by_name.get(name)
        if existing is None:
            order = next_order
            next_order += ORDER_STEP
        else:
            _validate_override(class_name, decl, existing)
            order = int(existing["field_order"])
        fact = _field_fact(class_id, class_name, decl, order)
        field_facts_by_name[name] = MappingProxyType(fact)
        if decl.kind == "managed":
            tx_groups.add(decl.tx_group)

    field_facts = tuple(
        sorted(
            field_facts_by_name.values(),
            key=lambda fact: int(fact["field_order"]),
        ),
    )
    class_fact["lifecycle_field_names"] = tuple(
        str(fact["field_name"])
        for fact in field_facts
        if fact["field_kind"] in {"field", "managed"}
    )
    for fact in field_facts:
        if fact["field_kind"] == "managed":
            tx_groups.add(fact["tx_group_key"])
        if fact["has_default"]:
            build_kwargs[str(fact["default_value_param_name"])] = fact["default_value"]
        if fact["has_default_factory"]:
            build_kwargs[str(fact["default_factory_param_name"])] = fact[
                "default_factory"
            ]

    tx_group_values = tx_groups.values()
    lifecycle_definition = MappingProxyType(
        {
            "version": LIFECYCLE_METADATA_VERSION,
            "class": MappingProxyType(dict(class_fact)),
            "fields": field_facts,
            "tx_groups": tx_group_values,
        },
    )
    build_kwargs[str(class_fact["lifecycle_definition_param_name"])] = (
        lifecycle_definition
    )
    build_kwargs[str(class_fact["tx_groups_param_name"])] = tx_group_values

    return HarvestedLifecycle(
        class_fact=MappingProxyType(dict(class_fact)),
        field_facts=field_facts,
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
        "lifecycle_field_names": (),
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
        "default_factory_param_names": _default_factory_param_names(
            class_name,
            decl,
        ),
        "default_factory_param_name": (
            f"_{class_name}_{name}_default_factory" if decl.has_default_factory else ""
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


def _remap_inherited_field_fact(
    class_id: str,
    class_name: str,
    inherited: Mapping[str, object],
) -> dict[str, object]:
    name = str(inherited["field_name"])
    kind = str(inherited["field_kind"])
    has_default = bool(inherited["has_default"])
    has_default_factory = bool(inherited["has_default_factory"])
    fact = dict(inherited)
    fact.setdefault("default_factory_param_names", ())
    fact.update(
        {
            "field_id": f"{class_id}.{name}",
            "field_owner": class_id,
            "default_value_param_name": (
                f"_{class_name}_{name}_default" if has_default else ""
            ),
            "default_factory_param_name": (
                f"_{class_name}_{name}_default_factory" if has_default_factory else ""
            ),
            "value_slot_name": "",
            "current_slot_name": "",
            "working_slot_name": "",
        },
    )
    if kind == "field":
        fact["value_slot_name"] = f"_y_{name}_value"
    elif kind == "managed":
        fact["current_slot_name"] = f"_y_{name}_current"
        fact["working_slot_name"] = f"_y_{name}_working"
    return fact


def _default_factory_param_names(
    class_name: str,
    decl: FieldDecl,
) -> tuple[str, ...]:
    if not decl.has_default_factory:
        return ()
    try:
        signature = inspect.signature(decl.default_factory)
    except (TypeError, ValueError):
        _warn_unintrospectable_default_factory(class_name, decl)
        return ()
    names: list[str] = []
    for parameter in signature.parameters.values():
        if parameter.kind in (
            inspect.Parameter.VAR_POSITIONAL,
            inspect.Parameter.VAR_KEYWORD,
        ):
            _raise_unbindable_default_factory_param(class_name, decl)
        if parameter.kind is inspect.Parameter.POSITIONAL_ONLY:
            if parameter.default is inspect.Parameter.empty:
                _raise_unbindable_default_factory_param(class_name, decl)
            continue
        names.append(parameter.name)
    return tuple(names)


def _warn_unintrospectable_default_factory(
    class_name: str,
    decl: FieldDecl,
) -> None:
    warnings.warn(
        (
            f"{class_name}.{decl.name}: default_factory signature could not be "
            "introspected; treating it as zero-argument"
        ),
        LifecycleDefinitionWarning,
        stacklevel=4,
    )


def _raise_unbindable_default_factory_param(
    class_name: str,
    decl: FieldDecl,
) -> None:
    raise LifecycleDefinitionError(
        f"{class_name}.{decl.name}: default_factory parameters must be "
        "bindable by name",
    )


def _inherited_lifecycle_definitions(
    cls: type[object],
) -> tuple[Mapping[str, object], ...]:
    definitions: list[Mapping[str, object]] = []
    for base in cls.__mro__[1:]:
        if base is object:
            continue
        if getattr(base, "__yidl_lifecycle_generated__", False) is not True:
            continue
        definition = getattr(base, "__yidl_lifecycle_definition__", None)
        if not isinstance(definition, Mapping):
            raise LifecycleDefinitionError(
                f"{cls.__name__}: inherited lifecycle metadata is invalid",
            )
        version = definition.get("version")
        if version != LIFECYCLE_METADATA_VERSION:
            raise LifecycleDefinitionError(
                f"{cls.__name__}: unsupported lifecycle metadata version {version!r}",
            )
        _validate_inherited_definition(cls, definition)
        definitions.append(definition)
    return tuple(definitions)


def _validate_override(
    class_name: str,
    decl: FieldDecl,
    inherited: Mapping[str, object],
) -> None:
    inherited_kind = inherited["field_kind"]
    if inherited_kind != "managed":
        return
    if decl.kind != "managed":
        raise LifecycleDefinitionError(
            f"{class_name}.{decl.name}: managed lifecycle field cannot be "
            f"overridden as {decl.kind}",
        )
    inherited_tx_group = inherited["tx_group_key"]
    if inherited_tx_group != decl.tx_group:
        raise LifecycleDefinitionError(
            f"{class_name}.{decl.name}: managed lifecycle field cannot change "
            "transaction group",
        )


def _validate_inherited_definition(
    cls: type[object],
    definition: Mapping[str, object],
) -> None:
    if "fields" not in definition:
        raise LifecycleDefinitionError(
            f"{cls.__name__}: inherited lifecycle metadata is missing fields",
        )
    if "tx_groups" not in definition:
        raise LifecycleDefinitionError(
            f"{cls.__name__}: inherited lifecycle metadata is missing tx_groups",
        )
    tx_groups = _definition_tx_groups(definition)
    if not tx_groups or tx_groups[0] != DEFAULT_TRANSACTION:
        raise LifecycleDefinitionError(
            f"{cls.__name__}: inherited transaction group indexes are invalid",
        )
    if len(set(tx_groups)) != len(tx_groups):
        raise LifecycleDefinitionError(
            f"{cls.__name__}: inherited transaction group indexes contain duplicates",
        )
    for field_fact in _definition_field_facts(definition):
        if field_fact["field_kind"] != "managed":
            continue
        if field_fact["tx_group_key"] not in tx_groups:
            raise LifecycleDefinitionError(
                f"{cls.__name__}: inherited managed field references an unknown "
                "transaction group",
            )


def _definition_field_facts(
    definition: Mapping[str, object],
) -> tuple[Mapping[str, object], ...]:
    fields = definition["fields"]
    if not isinstance(fields, tuple):
        raise LifecycleDefinitionError("inherited lifecycle fields must be a tuple")
    for field_fact in fields:
        if not isinstance(field_fact, Mapping):
            raise LifecycleDefinitionError(
                "inherited lifecycle field metadata is invalid",
            )
    return fields


def _definition_tx_groups(definition: Mapping[str, object]) -> tuple[object, ...]:
    tx_groups = definition.get("tx_groups", (DEFAULT_TRANSACTION,))
    if not isinstance(tx_groups, tuple):
        raise LifecycleDefinitionError(
            "inherited lifecycle transaction groups must be a tuple",
        )
    return tx_groups


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


def _reject_generated_name_collisions(
    cls: type[object],
    annotations: Mapping[str, object],
    class_fact: Mapping[str, object],
) -> None:
    for name in annotations:
        if name in _FACADE_EXPOSURE_NAMES:
            raise LifecycleDefinitionError(
                f"{cls.__name__}.{name}: field name collides with generated "
                "facade exposure",
            )
        if name in _GENERATED_HELPER_NAMES:
            raise LifecycleDefinitionError(
                f"{cls.__name__}.{name}: name collides with generated "
                "lifecycle helper",
            )
    for name in cls.__dict__:
        if name in _GENERATED_HELPER_NAMES:
            raise LifecycleDefinitionError(
                f"{cls.__name__}.{name}: name collides with generated "
                "lifecycle helper",
            )
    generated_class_names = {
        str(class_fact["state_class_name"]),
        str(class_fact["facade_base_class_name"]),
        str(class_fact["current_facade_class_name"]),
        str(class_fact["working_facade_class_name"]),
    }
    for name in cls.__dict__:
        if name in generated_class_names:
            raise LifecycleDefinitionError(
                f"{cls.__name__}.{name}: name collides with generated "
                "lifecycle class",
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
