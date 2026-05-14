from __future__ import annotations

from collections.abc import Mapping
from pprint import pformat

from support.golden_case import run_case
from yidl.concept_parser import compile_yidl_files
from yidl.generation.assembly_plan import AndConditionSpec
from yidl.generation.assembly_plan import EdgeApplySpec
from yidl.generation.assembly_plan import EqConditionSpec
from yidl.generation.assembly_plan import InlineApplySpec
from yidl.generation.assembly_plan import LiteralValueRef
from yidl.generation.assembly_plan import TupleValueRef
from yidl.generation.assembly_plan import ValueRef
from yidl.generation.assembly_runtime import DataStack
from yidl.generation.assembly_runtime import evaluate_condition
from yidl.generation.assembly_runtime import evaluate_value


YIDL_SOURCE = """
module update_a

concept UpdateA {
    property ClassId: str
    property FieldOwner: str
    property FieldOrder: int
    property FieldName: str

    family FacadeSpecs {
        variant Facade {
            ClassId
        }
    }

    family FieldSpecs {
        variant Field {
            FieldOwner
            FieldOrder
            FieldName
        }
    }

    collection Facades: FacadeSpecs identity ClassId many
    collection Fields: FieldSpecs identity FieldName many

    resource RootTemplate = code `astichi_hole(body)`
    resource ChildTemplate = template `field_name__astichi_arg__`

    production ChildProduction(facade: Facades) -> composable {
        root ChildRoot = ChildTemplate
    }

    contribution ChildContribution = ChildTemplate {
        as ChildNode
        index FieldOrder
        order (FieldOrder,)

        target body {
            build /Root/ChildNode[FieldOrder]
            owner /Root/*
            owner /Root/./?/+
        }

        ident field_name = FieldName
        external field_name = FieldName
    }

    contribution ProductionContribution = ChildProduction {
        target body {
            build /Root
        }
    }

    matcher ChildSelection(field: Fields, facade: Facades) -> contribution {
        default -> ChildContribution
        rule selected when FieldOwner == ClassId -> ProductionContribution weight 5
    }

    assemble ChildEdge(facade: Facades)
        from field: Fields
        where FieldOwner == ClassId
        using ChildSelection

    production RootProduction -> composable {
        root Root = RootTemplate

        apply child_items
            from facade: Facades, field: Fields
            where FieldOwner == ClassId
            using ChildSelection

        apply ChildEdge
    }

    assembly Module = RootProduction
}
"""


def render_case() -> str:
    summary = _summary()
    return "\n".join(
        [
            "from __future__ import annotations",
            "",
            f"SUMMARY = {pformat(summary, sort_dicts=True, width=88)}",
            "",
        ]
    )


def validate_case(source: str) -> None:
    namespace: dict[str, object] = {}
    exec(source, namespace)
    summary = namespace["SUMMARY"]
    assert summary == _summary()

    assert summary["contributions"]["ChildContribution"]["source_kind"] == "resource"
    assert summary["contributions"]["ProductionContribution"]["source_kind"] == "production"
    assert summary["matchers"]["ChildSelection"]["rules"][0]["contribution"] == (
        "ProductionContribution"
    )
    assert summary["productions"]["RootProduction"]["applies"] == [
        {"edge": "RootProduction.child_items", "kind": "inline"},
        {"edge": "ChildEdge", "kind": "edge"},
    ]
    assert summary["assemblies"] == {"Module": "RootProduction"}


def _summary() -> Mapping[str, object]:
    module = compile_yidl_files({"update_a.yidl": YIDL_SOURCE}, "update_a.yidl")
    concept = module.concepts["UpdateA"]
    child = concept.contributions["ChildContribution"]
    child_edge = concept.assembly_edges["ChildEdge"]
    stack = DataStack(
        (
            {
                "ClassId": "Owner",
                "FieldName": "count",
                "FieldOrder": 7,
                "FieldOwner": "Owner",
            },
        )
    )
    return {
        "assemblies": {
            name: assembly.production_name
            for name, assembly in sorted(concept.assemblies.items())
        },
        "edges": {
            name: {
                "condition": _condition_summary(edge.condition),
                "context": _inputs_summary(edge.context_inputs),
                "from": _inputs_summary(edge.from_inputs),
                "matcher": edge.matcher_name,
            }
            for name, edge in sorted(concept.assembly_edges.items())
        },
        "contributions": {
            name: {
                "bindings": [
                    {
                        "kind": binding.kind,
                        "name": binding.name,
                        "value": _value_summary(binding.value),
                    }
                    for binding in contribution.bindings
                ],
                "build_name": contribution.build_name,
                "index": _value_summary(contribution.index),
                "order": _value_summary(contribution.order),
                "source_kind": contribution.source_kind,
                "source_name": contribution.source_name,
                "target": {
                    "name": contribution.target.name,
                    "paths": [
                        {
                            "kind": target_path.kind,
                            "path": _path_summary(target_path.path),
                        }
                        for target_path in contribution.target.paths
                    ],
                },
            }
            for name, contribution in sorted(concept.contributions.items())
        },
        "matchers": {
            name: {
                "default": matcher.default_contribution_name,
                "inputs": _inputs_summary(matcher.inputs),
                "rules": [
                    {
                        "condition": _condition_summary(rule.condition),
                        "contribution": rule.contribution_name,
                        "name": rule.name,
                        "weight": rule.weight,
                    }
                    for rule in matcher.rules
                ],
            }
            for name, matcher in sorted(concept.contribution_matchers.items())
        },
        "productions": {
            name: {
                "applies": [_apply_summary(apply) for apply in production.applies],
                "inputs": _inputs_summary(production.inputs),
                "root": {
                    "bindings": [
                        {
                            "kind": binding.kind,
                            "name": binding.name,
                            "value": _value_summary(binding.value),
                        }
                        for binding in production.root.bindings
                    ],
                    "build_name": production.root.build_name,
                    "resource": production.root.resource_name,
                },
            }
            for name, production in sorted(concept.composable_productions.items())
        },
        "runtime": {
            "child_edge_condition": evaluate_condition(child_edge.condition, stack),
            "child_index": evaluate_value(child.index, stack),
            "child_order": evaluate_value(child.order, stack),
        },
    }


def _apply_summary(apply: object) -> Mapping[str, object]:
    if isinstance(apply, InlineApplySpec):
        return {"edge": apply.edge.name, "kind": "inline"}
    if isinstance(apply, EdgeApplySpec):
        return {"edge": apply.edge_name, "kind": "edge"}
    raise TypeError(f"unsupported apply spec: {type(apply).__name__}")


def _inputs_summary(inputs: object) -> list[Mapping[str, str]]:
    return [
        {"collection": input_spec.collection_name, "name": input_spec.name}
        for input_spec in inputs
    ]


def _path_summary(path: object) -> list[Mapping[str, object]]:
    return [
        {
            "indexes": [_value_summary(index) for index in segment.indexes],
            "kind": segment.kind,
            "name": segment.name,
        }
        for segment in path.segments
    ]


def _condition_summary(condition: object) -> object:
    if condition is None:
        return None
    if isinstance(condition, EqConditionSpec):
        return {
            "eq": [
                _value_summary(condition.left),
                _value_summary(condition.right),
            ]
        }
    if isinstance(condition, AndConditionSpec):
        return {"and": [_condition_summary(item) for item in condition.items]}
    raise TypeError(f"unsupported condition spec: {type(condition).__name__}")


def _value_summary(value: object) -> object:
    if value is None:
        return None
    if isinstance(value, ValueRef):
        return {"ref": value.name}
    if isinstance(value, LiteralValueRef):
        return {"literal": value.value}
    if isinstance(value, TupleValueRef):
        return {"tuple": [_value_summary(item) for item in value.items]}
    raise TypeError(f"unsupported value spec: {type(value).__name__}")


if __name__ == "__main__":
    raise SystemExit(run_case("yidl_update_a_parse_surface.py", render_case, validate_case))
