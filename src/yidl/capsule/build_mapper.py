"""Map DDS capsule runtime records into Astichi-built source."""

from __future__ import annotations

from collections.abc import Callable, Iterable, Mapping, Sequence
from dataclasses import dataclass
from typing import Any

import astichi

from yidl.generation.data_def_sys import MatcherGeneratedValue
from yidl.generation.data_def_sys import from_astichi_code


EdgeArgNames = Callable[[object], Mapping[str, str]]
EdgeBindValues = Callable[[object], Mapping[str, object]]
EdgeKeepNames = Callable[[object], Iterable[str]]
OwnerSelector = Callable[[object], object]


@dataclass(frozen=True, slots=True)
class RuntimePortRef:
    """Reference to a generated runtime port and one owner identity."""

    namespace_name: str
    owner: object

    def address(self, namespace: Mapping[str, object]) -> object:
        port = namespace[self.namespace_name]
        return port.of(self.owner)


@dataclass(frozen=True, slots=True)
class TemplateEdgePlan:
    """How to turn one produced record into one Astichi insertion edge."""

    family_name: str
    template_attr: str = "template"
    order_attr: str = "order"
    arg_names: EdgeArgNames | None = None
    bind: EdgeBindValues | None = None
    keep_names: EdgeKeepNames | None = None

    def template_for(self, record: object) -> MatcherGeneratedValue:
        value = getattr(record, self.template_attr)
        if not isinstance(value, MatcherGeneratedValue):
            raise TypeError(
                f"{self.template_attr} must be MatcherGeneratedValue, "
                f"got {type(value).__name__}"
            )
        return value

    def order_for(self, record: object) -> int:
        return int(getattr(record, self.order_attr, 0))

    def arg_names_for(self, record: object) -> Mapping[str, str] | None:
        if self.arg_names is None:
            return None
        values = dict(self.arg_names(record))
        return values or None

    def bind_for(self, record: object) -> Mapping[str, object] | None:
        if self.bind is None:
            return None
        values = dict(self.bind(record))
        return values or None

    def keep_names_for(self, record: object) -> tuple[str, ...] | None:
        if self.keep_names is None:
            return None
        values = tuple(self.keep_names(record))
        return values or None


@dataclass(frozen=True, slots=True)
class ChildPortPlan:
    """A child port that fills a hole on a parent body component."""

    parent_name: str
    port_name: str
    target_hole: str
    edge: TemplateEdgePlan
    owner: OwnerSelector | None = None

    def owner_for(self, parent_record: object) -> object:
        if self.owner is not None:
            return self.owner(parent_record)
        return ("runtime", parent_record.name)


@dataclass(frozen=True, slots=True)
class CapsuleClassBuildPlan:
    """Config for the first DDS-to-Astichi class mapper."""

    class_name: RuntimePortRef
    class_body: RuntimePortRef
    class_template: MatcherGeneratedValue = from_astichi_code(
        "class class_name__astichi_arg__:\n"
        "    astichi_hole(class_body)\n"
    )
    class_name_attr: str = "runtime_value"
    class_name_arg: str = "class_name"
    class_body_hole: str = "class_body"
    class_body_edge: TemplateEdgePlan = TemplateEdgePlan("ClassBody")
    child_ports: tuple[ChildPortPlan, ...] = ()


def build_class_source(
    container: object,
    namespace: Mapping[str, object],
    plan: CapsuleClassBuildPlan,
) -> str:
    """Build a class source module from generated capsule runtime records."""

    class_name_record = _single_record(
        container.children_at(plan.class_name.address(namespace))
    )
    class_name = getattr(class_name_record, plan.class_name_attr)
    _require_identifier(class_name, "generated class name")

    builder = astichi.build()
    builder.add(
        "Root",
        plan.class_template.to_generator(),
        arg_names={plan.class_name_arg: class_name},
        keep_names=[class_name],
    )

    body_records = container.children_at(plan.class_body.address(namespace))
    _insert_template_records(
        builder,
        target_instance="Root",
        target_hole=plan.class_body_hole,
        records=body_records,
        edge_plan=plan.class_body_edge,
    )

    for index, body_record in enumerate(body_records):
        body_instance = _instance_name(plan.class_body_edge.family_name, index)
        for child_plan in plan.child_ports:
            if body_record.name != child_plan.parent_name:
                continue
            port = namespace[child_plan.port_name]
            child_records = container.children_at(
                port.of(child_plan.owner_for(body_record))
            )
            _insert_template_records(
                builder,
                target_instance=body_instance,
                target_hole=child_plan.target_hole,
                records=child_records,
                edge_plan=child_plan.edge,
            )

    return builder.build().materialize().emit(provenance=False)


def _insert_template_records(
    builder: object,
    *,
    target_instance: str,
    target_hole: str,
    records: Sequence[object],
    edge_plan: TemplateEdgePlan,
) -> None:
    target = builder.instance(target_instance).target(target_hole)
    for index, record in enumerate(records):
        instance_name = _instance_name(edge_plan.family_name, index)
        builder.add(instance_name, edge_plan.template_for(record).to_generator())
        target.add(
            instance_name,
            order=edge_plan.order_for(record),
            arg_names=edge_plan.arg_names_for(record),
            bind=edge_plan.bind_for(record),
            keep_names=edge_plan.keep_names_for(record),
        )


def _single_record(records: Sequence[object]) -> object:
    if len(records) != 1:
        raise ValueError(f"expected exactly one record, found {len(records)}")
    return records[0]


def _instance_name(family_name: str, index: int) -> str:
    _require_identifier(family_name, "template family name")
    return f"{family_name}_{index}"


def _require_identifier(value: Any, label: str) -> None:
    if not isinstance(value, str) or not value.isidentifier():
        raise ValueError(f"{label} must be a Python identifier, got {value!r}")


__all__ = [
    "CapsuleClassBuildPlan",
    "ChildPortPlan",
    "RuntimePortRef",
    "TemplateEdgePlan",
    "build_class_source",
]
