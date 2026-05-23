from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
import inspect
from types import MappingProxyType
from types import NoneType
from types import UnionType
from typing import get_args
from typing import get_origin
import warnings

from yidl.runtime.lifecycle_markers import FieldDecl
from yidl.runtime.lifecycle_markers import LifecycleDefinitionError
from yidl.runtime.lifecycle_markers import LifecycleDefinitionWarning
from yidl.runtime.lifecycle_markers import LifecycleMarker
from yidl.runtime.lifecycle_markers import MISSING
from yidl.runtime.lifecycle_markers import field
from yidl.runtime.lifecycle_markers import normalize_marker
from yidl.runtime.lifecycle_markers import transaction_method_markers
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
    transaction_method_facts: tuple[Mapping[str, object], ...]
    lifecycle_definition: Mapping[str, object]
    annotations: Mapping[str, object]
    tx_keys: tuple[object, ...]
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
    transaction_method_facts: list[Mapping[str, object]] = []
    build_kwargs: dict[str, object] = {
        str(class_fact["lifecycle_definition_param_name"]): None,
        str(class_fact["annotations_param_name"]): MappingProxyType(dict(annotations)),
        str(class_fact["tx_keys_param_name"]): (),
    }
    tx_keys = _TxKeyBuilder()
    next_order = ORDER_STEP
    next_method_order = ORDER_STEP

    for definition in _inherited_lifecycle_definitions(cls):
        for group in _definition_tx_keys(definition):
            tx_keys.add(group)
        for inherited_fact in _definition_field_facts(definition):
            name = str(inherited_fact["field_name"])
            if name in field_facts_by_name:
                continue
            fact = _remap_inherited_field_fact(class_id, class_name, inherited_fact)
            field_facts_by_name[name] = MappingProxyType(fact)
            next_order = max(next_order, int(fact["field_order"]) + ORDER_STEP)
        for inherited_fact in _definition_transaction_method_facts(definition):
            fact = _remap_inherited_transaction_method_fact(
                class_id,
                inherited_fact,
                _definition_tx_keys(definition),
            )
            transaction_method_facts.append(MappingProxyType(fact))
            next_method_order = max(
                next_method_order,
                int(fact["declaration_order"]) + ORDER_STEP,
            )

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
        if decl.kind in {"managed", "owned", "transient"}:
            tx_keys.add(decl.tx_key)

    field_facts = tuple(
        sorted(
            field_facts_by_name.values(),
            key=lambda fact: int(fact["field_order"]),
        ),
    )
    class_fact["lifecycle_field_names"] = tuple(
        str(fact["field_name"])
        for fact in field_facts
        if fact["field_kind"]
        in {
            "binding",
            "const",
            "field",
            "local_store",
            "managed",
            "owned",
            "static",
            "transient",
        }
    )
    for fact in field_facts:
        if fact["field_kind"] in {"managed", "owned", "transient"}:
            tx_keys.add(fact["tx_key_key"])
        if (
            fact["field_kind"] == "local_store"
            and fact["default_factory_param_names"]
        ):
            raise LifecycleDefinitionError(
                f"{class_name}.{fact['field_name']}: local_store "
                "default_factory must be zero-argument",
            )
        if fact["has_default"]:
            build_kwargs[str(fact["default_value_param_name"])] = fact["default_value"]
        if fact["has_default_factory"]:
            build_kwargs[str(fact["default_factory_param_name"])] = fact[
                "default_factory"
            ]
        if fact.get("has_working_default_factory"):
            build_kwargs[str(fact["working_default_factory_param_name"])] = fact[
                "working_default_factory"
            ]
        if fact["has_freeze"]:
            build_kwargs[str(fact["freeze_param_name"])] = fact["freeze"]
        if fact["has_thaw"]:
            build_kwargs[str(fact["thaw_param_name"])] = fact["thaw"]

    tx_key_values = tx_keys.values()
    transaction_method_facts.extend(
        _local_transaction_method_facts(
            cls,
            class_id,
            tx_key_values,
            next_order=next_method_order,
        )
    )
    transaction_method_facts_tuple = tuple(transaction_method_facts)
    _validate_transaction_method_facts(
        class_name,
        transaction_method_facts_tuple,
        tx_key_values,
    )
    lifecycle_definition = MappingProxyType(
        {
            "version": LIFECYCLE_METADATA_VERSION,
            "class": MappingProxyType(dict(class_fact)),
            "fields": field_facts,
            "transaction_methods": transaction_method_facts_tuple,
            "tx_keys": tx_key_values,
        },
    )
    build_kwargs[str(class_fact["lifecycle_definition_param_name"])] = (
        lifecycle_definition
    )
    build_kwargs[str(class_fact["tx_keys_param_name"])] = tx_key_values

    return HarvestedLifecycle(
        class_fact=MappingProxyType(dict(class_fact)),
        field_facts=field_facts,
        transaction_method_facts=transaction_method_facts_tuple,
        lifecycle_definition=lifecycle_definition,
        annotations=MappingProxyType(dict(annotations)),
        tx_keys=tx_key_values,
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
        "tx_keys_param_name": f"_{class_name}_tx_keys",
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
        "binding_shape": _binding_shape(decl.annotation),
        "annotation": decl.annotation,
        "init": decl.init,
        "has_default": decl.has_default,
        "default_value": decl.default,
        "default_value_param_name": (
            f"_{class_name}_{name}_default" if decl.has_default else ""
        ),
        "has_default_factory": decl.has_default_factory,
        "default_factory": decl.default_factory,
        "allow_self_factory": decl.allow_self_factory,
        "default_factory_param_names": _default_factory_param_names(
            class_name,
            decl,
        ),
        "default_factory_param_name": (
            f"_{class_name}_{name}_default_factory" if decl.has_default_factory else ""
        ),
        "has_working_default_factory": decl.has_working_default_factory,
        "working_default_factory": decl.working_default_factory,
        "working_default_factory_param_names": _working_default_factory_param_names(
            class_name,
            decl,
        ),
        "working_default_factory_param_name": (
            f"_{class_name}_{name}_working_default_factory"
            if decl.has_working_default_factory
            else ""
        ),
        "tx_key_key": None,
        "value_slot_name": "",
        "current_slot_name": "",
        "working_slot_name": "",
        "staged_slot_name": "",
        "has_freeze": False,
        "freeze": MISSING,
        "freeze_param_name": "",
        "has_thaw": False,
        "thaw": MISSING,
        "thaw_param_name": "",
        "has_optional_none": _has_optional_none(decl.annotation),
    }
    if kind in {"binding", "const", "field", "local_store", "static"}:
        fact["value_slot_name"] = f"_y_{name}_value"
    elif kind in {"managed", "owned"}:
        fact["tx_key_key"] = decl.tx_key
        fact["current_slot_name"] = f"_y_{name}_current"
        fact["working_slot_name"] = f"_y_{name}_working"
        if kind == "owned":
            fact["staged_slot_name"] = f"_y_{name}_staged"
        if kind == "managed":
            fact["staged_slot_name"] = f"_y_{name}_staged"
            fact["has_freeze"] = decl.has_freeze
            fact["freeze"] = decl.freeze
            fact["freeze_param_name"] = (
                f"_{class_name}_{name}_freeze" if decl.has_freeze else ""
            )
            fact["has_thaw"] = decl.has_thaw
            fact["thaw"] = decl.thaw
            fact["thaw_param_name"] = (
                f"_{class_name}_{name}_thaw" if decl.has_thaw else ""
            )
    elif kind == "transient":
        fact["tx_key_key"] = decl.tx_key
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
    fact.setdefault("allow_self_factory", False)
    fact.setdefault("binding_shape", _binding_shape(fact.get("annotation")))
    fact.setdefault("has_freeze", False)
    fact.setdefault("freeze", MISSING)
    fact.setdefault("has_thaw", False)
    fact.setdefault("thaw", MISSING)
    fact.setdefault("has_optional_none", _has_optional_none(fact.get("annotation")))
    fact.setdefault("has_working_default_factory", False)
    fact.setdefault("working_default_factory", MISSING)
    fact.setdefault("working_default_factory_param_names", ())
    has_freeze = bool(fact["has_freeze"])
    has_thaw = bool(fact["has_thaw"])
    has_working_default_factory = bool(fact["has_working_default_factory"])
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
            "working_default_factory_param_name": (
                f"_{class_name}_{name}_working_default_factory"
                if has_working_default_factory
                else ""
            ),
            "value_slot_name": "",
            "current_slot_name": "",
            "working_slot_name": "",
            "staged_slot_name": "",
            "freeze_param_name": f"_{class_name}_{name}_freeze" if has_freeze else "",
            "thaw_param_name": f"_{class_name}_{name}_thaw" if has_thaw else "",
        },
    )
    if kind in {"binding", "const", "field", "local_store", "static"}:
        fact["value_slot_name"] = f"_y_{name}_value"
    elif kind in {"managed", "owned"}:
        fact["current_slot_name"] = f"_y_{name}_current"
        fact["working_slot_name"] = f"_y_{name}_working"
        if kind == "owned":
            fact["staged_slot_name"] = f"_y_{name}_staged"
        if kind == "managed":
            fact["staged_slot_name"] = f"_y_{name}_staged"
    elif kind == "transient":
        fact["current_slot_name"] = f"_y_{name}_current"
        fact["working_slot_name"] = f"_y_{name}_working"
    return fact


def _local_transaction_method_facts(
    cls: type[object],
    class_id: str,
    tx_keys: tuple[object, ...],
    *,
    next_order: int,
) -> tuple[Mapping[str, object], ...]:
    facts: list[Mapping[str, object]] = []
    for name, value in cls.__dict__.items():
        markers = transaction_method_markers(value)
        for marker in markers:
            if marker.tx_key not in tx_keys:
                raise LifecycleDefinitionError(
                    f"{cls.__name__}.{name}: transaction marker references "
                    f"unknown group {marker.tx_key!r}",
                )
            tx_index = tx_keys.index(marker.tx_key)
            facts.append(
                MappingProxyType(
                    {
                        "method_id": f"{class_id}.{name}.{marker.kind}",
                        "method_owner": class_id,
                        "method_name": name,
                        "method_kind": marker.kind,
                        "tx_key_key": marker.tx_key,
                        "tx_index": tx_index,
                        "declaration_order": next_order,
                    },
                ),
            )
            next_order += ORDER_STEP
    return tuple(facts)


def _remap_inherited_transaction_method_fact(
    class_id: str,
    inherited: Mapping[str, object],
    tx_keys: tuple[object, ...],
) -> dict[str, object]:
    fact = dict(inherited)
    name = str(fact["method_name"])
    kind = str(fact["method_kind"])
    tx_key = fact["tx_key_key"]
    if "tx_index" not in fact:
        fact["tx_index"] = tx_keys.index(tx_key)
    fact.update(
        {
            "method_id": f"{class_id}.{name}.{kind}",
            "method_owner": class_id,
        },
    )
    return fact


def _validate_transaction_method_facts(
    class_name: str,
    facts: tuple[Mapping[str, object], ...],
    tx_keys: tuple[object, ...],
) -> None:
    commit_order_groups: set[object] = set()
    for fact in facts:
        tx_key = fact["tx_key_key"]
        if tx_key not in tx_keys:
            raise LifecycleDefinitionError(
                f"{class_name}.{fact['method_name']}: transaction marker references "
                f"unknown group {tx_key!r}",
            )
        if fact["method_kind"] != "commit_order_key":
            continue
        if tx_key in commit_order_groups:
            raise LifecycleDefinitionError(
                f"{class_name}.{fact['method_name']}: multiple commit order key "
                f"providers for transaction key {tx_key!r}",
            )
        commit_order_groups.add(tx_key)


def _default_factory_param_names(
    class_name: str,
    decl: FieldDecl,
) -> tuple[str, ...]:
    return _factory_param_names(
        class_name,
        decl,
        has_factory=decl.has_default_factory,
        factory=decl.default_factory,
        role="default_factory",
    )


def _working_default_factory_param_names(
    class_name: str,
    decl: FieldDecl,
) -> tuple[str, ...]:
    return _factory_param_names(
        class_name,
        decl,
        has_factory=decl.has_working_default_factory,
        factory=decl.working_default_factory,
        role="working_default_factory",
    )


def _factory_param_names(
    class_name: str,
    decl: FieldDecl,
    *,
    has_factory: bool,
    factory: object,
    role: str,
) -> tuple[str, ...]:
    if not has_factory:
        return ()
    try:
        signature = inspect.signature(factory)
    except (TypeError, ValueError):
        _warn_unintrospectable_factory(class_name, decl, role=role)
        return ()
    names: list[str] = []
    for parameter in signature.parameters.values():
        if parameter.kind in (
            inspect.Parameter.VAR_POSITIONAL,
            inspect.Parameter.VAR_KEYWORD,
        ):
            _raise_unbindable_factory_param(class_name, decl, role=role)
        if parameter.kind is inspect.Parameter.POSITIONAL_ONLY:
            if parameter.default is inspect.Parameter.empty:
                _raise_unbindable_factory_param(class_name, decl, role=role)
            continue
        names.append(parameter.name)
    return tuple(names)


def _warn_unintrospectable_factory(
    class_name: str,
    decl: FieldDecl,
    *,
    role: str,
) -> None:
    warnings.warn(
        (
            f"{class_name}.{decl.name}: {role} signature could not be "
            "introspected; treating it as zero-argument"
        ),
        LifecycleDefinitionWarning,
        stacklevel=4,
    )


def _raise_unbindable_factory_param(
    class_name: str,
    decl: FieldDecl,
    *,
    role: str,
) -> None:
    raise LifecycleDefinitionError(
        f"{class_name}.{decl.name}: {role} parameters must be bindable by name",
    )


def _has_optional_none(annotation: object) -> bool:
    if isinstance(annotation, str):
        return "None" in annotation
    origin = get_origin(annotation)
    if origin is None:
        return False
    if origin is UnionType:
        return NoneType in get_args(annotation)
    return NoneType in get_args(annotation)


def _binding_shape(annotation: object) -> str:
    if isinstance(annotation, str):
        if "dict[" in annotation or "Mapping[" in annotation:
            return "map"
        return "scalar"
    origin = get_origin(annotation)
    if origin in {dict, Mapping}:
        return "map"
    return "scalar"


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
    inherited_tx_key = inherited["tx_key_key"]
    if inherited_tx_key != decl.tx_key:
        raise LifecycleDefinitionError(
            f"{class_name}.{decl.name}: managed lifecycle field cannot change "
            "transaction key",
        )


def _validate_inherited_definition(
    cls: type[object],
    definition: Mapping[str, object],
) -> None:
    if "fields" not in definition:
        raise LifecycleDefinitionError(
            f"{cls.__name__}: inherited lifecycle metadata is missing fields",
        )
    if "tx_keys" not in definition:
        raise LifecycleDefinitionError(
            f"{cls.__name__}: inherited lifecycle metadata is missing tx_keys",
        )
    tx_keys = _definition_tx_keys(definition)
    if not tx_keys or tx_keys[0] != DEFAULT_TRANSACTION:
        raise LifecycleDefinitionError(
            f"{cls.__name__}: inherited transaction key indexes are invalid",
        )
    if len(set(tx_keys)) != len(tx_keys):
        raise LifecycleDefinitionError(
            f"{cls.__name__}: inherited transaction key indexes contain duplicates",
        )
    for field_fact in _definition_field_facts(definition):
        if field_fact["field_kind"] not in {"managed", "owned"}:
            continue
        if field_fact["tx_key_key"] not in tx_keys:
            raise LifecycleDefinitionError(
                f"{cls.__name__}: inherited transactional field references an unknown "
                "transaction key",
            )
    for method_fact in _definition_transaction_method_facts(definition):
        if method_fact["tx_key_key"] not in tx_keys:
            raise LifecycleDefinitionError(
                f"{cls.__name__}: inherited transaction method references an "
                "unknown transaction key",
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


def _definition_transaction_method_facts(
    definition: Mapping[str, object],
) -> tuple[Mapping[str, object], ...]:
    methods = definition.get("transaction_methods", ())
    if not isinstance(methods, tuple):
        raise LifecycleDefinitionError(
            "inherited lifecycle transaction method metadata must be a tuple",
        )
    for method_fact in methods:
        if not isinstance(method_fact, Mapping):
            raise LifecycleDefinitionError(
                "inherited lifecycle transaction method metadata is invalid",
            )
    return methods


def _definition_tx_keys(definition: Mapping[str, object]) -> tuple[object, ...]:
    tx_keys = definition.get("tx_keys", (DEFAULT_TRANSACTION,))
    if not isinstance(tx_keys, tuple):
        raise LifecycleDefinitionError(
            "inherited lifecycle transaction keys must be a tuple",
        )
    return tx_keys


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
class _TxKeyBuilder:
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
            raise RuntimeError("transaction key builder is not initialized")
        return self._groups
