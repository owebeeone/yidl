from __future__ import annotations

from collections.abc import Mapping
from itertools import product
from pprint import pformat

from support.golden_case import run_case
from yidl.concept_parser import compile_yidl_files
from yidl.generation.assembly_runtime import DataStack
from yidl.generation.assembly_runtime import evaluate_condition
from yidl.generation.assembly_runtime import evaluate_external
from yidl.generation.assembly_runtime import evaluate_identifier
from yidl.generation.assembly_runtime import evaluate_order


YIDL_SOURCE = """
module multi_source

concept MultiSource {
    property Id: str
    property Owner: str
    property Kind: str
    property FieldName: str
    property Order: int

    family FacadeSpecs {
        variant Facade {
            Id
        }
    }

    family FieldSpecs {
        variant Field {
            Owner
            Kind
            FieldName
            Order
        }
    }

    collection Facades: FacadeSpecs identity Id many
    collection Fields: FieldSpecs identity FieldName many

    resource RootTemplate = code `astichi_hole(entries)`
    resource EntryTemplate = template `field_name__astichi_arg__`

    contribution EntryContribution = EntryTemplate {
        index Order
        order Order

        target entries {
            build /Root
        }

        ident field_name = FieldName
        external owner = Id
    }

    matcher EntrySelection(facade: Facades, field: Fields) -> contribution {
        rule selected when Owner == Id and Kind == "selected" -> EntryContribution
    }

    assemble Entries
        from facade: Facades, field: Fields
        where Owner == Id and Kind == "selected"
        using EntrySelection

    production RootProduction -> composable {
        root Root = RootTemplate
        apply Entries
    }

    assembly Module = RootProduction
}
"""


FACADES = (
    {"Id": "owner_a"},
    {"Id": "owner_b"},
)
FIELDS = (
    {"FieldName": "count", "Kind": "selected", "Order": 20, "Owner": "owner_a"},
    {"FieldName": "hidden", "Kind": "ignored", "Order": 30, "Owner": "owner_a"},
    {"FieldName": "total", "Kind": "selected", "Order": 10, "Owner": "owner_b"},
)


def render_case() -> str:
    results = _selected_entries()
    return "\n".join(
        [
            "from __future__ import annotations",
            "",
            f"RESULTS = {pformat(results, sort_dicts=True, width=88)}",
            "",
        ]
    )


def validate_case(source: str) -> None:
    namespace: dict[str, object] = {}
    exec(source, namespace)
    assert namespace["RESULTS"] == [
        {"field_name": "count", "order": 20, "owner": "owner_a"},
        {"field_name": "total", "order": 10, "owner": "owner_b"},
    ]


def _selected_entries() -> list[Mapping[str, object]]:
    module = compile_yidl_files({"multi_source.yidl": YIDL_SOURCE}, "multi_source.yidl")
    concept = module.concepts["MultiSource"]
    edge = concept.assembly_edges["Entries"]
    contribution = concept.contributions["EntryContribution"]

    results: list[Mapping[str, object]] = []
    for facade, field in product(FACADES, FIELDS):
        stack = DataStack((facade, field))
        if edge.condition is None or not evaluate_condition(edge.condition, stack):
            continue
        values: dict[str, object] = {"order": evaluate_order(contribution.order, stack)}
        for binding in contribution.bindings:
            if binding.kind == "ident":
                values[binding.name] = evaluate_identifier(binding.value, stack)
            else:
                values[binding.name] = evaluate_external(binding.value, stack)
        results.append(values)
    return results


if __name__ == "__main__":
    raise SystemExit(run_case("yidl_update_a_multi_source_from.py", render_case, validate_case))
