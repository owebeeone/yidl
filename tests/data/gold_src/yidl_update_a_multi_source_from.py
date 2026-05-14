from __future__ import annotations

from collections.abc import Mapping
from itertools import product
from pprint import pformat

from support.golden_case import run_case
from yidl.concept_parser import compile_yidl_files
from yidl.generation.assembly_runtime import DataStack
from yidl.generation.assembly_runtime import evaluate_condition
from yidl.generation.assembly_runtime import evaluate_external
from yidl.generation.assembly_runtime import evaluate_order
from yidl.generation.data_def_sys import emit_concept_runtime_source


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

    resource RootTemplate = code $[
        RESULTS = []
        astichi_hole(entries)
    ]$ {
        keep RESULTS
    }
    resource EntryTemplate = template `RESULTS.append(astichi_bind_external(owner))` {
        keep RESULTS
    }

    contribution EntryContribution = EntryTemplate {
        index Order
        order Order

        target entries {
            build /Root
        }

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
    results, output = _selected_entries_and_output()
    return "\n".join(
        [
            "from __future__ import annotations",
            "",
            f"RESULTS = {pformat(results, sort_dicts=True, width=88)}",
            "",
            f"OUTPUT = {output!r}",
            "",
        ]
    )


def validate_case(source: str) -> None:
    namespace: dict[str, object] = {}
    exec(source, namespace)
    assert namespace["RESULTS"] == [
        {"order": 20, "owner": "owner_a"},
        {"order": 10, "owner": "owner_b"},
    ]
    assert "RESULTS.append('owner_a')" in namespace["OUTPUT"]
    assert "RESULTS.append('owner_b')" in namespace["OUTPUT"]


def _selected_entries_and_output() -> tuple[list[Mapping[str, object]], str]:
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
            if binding.kind == "external":
                values[binding.name] = evaluate_external(binding.value, stack)
        results.append(values)
    compiler_source = emit_concept_runtime_source(
        concept.plan.build_data_definition(),
        resources=concept.resources,
        assembly_plan=concept,
    )
    namespace: dict[str, object] = {}
    exec(compiler_source, namespace)
    output = namespace["build_Module"](_container(namespace)).emit_commented()
    return results, output


def _container(namespace: Mapping[str, object]) -> object:
    builder = namespace["new_builder"]()
    facade = namespace["Facade"]
    field = namespace["Field"]
    facades = namespace["FacadesCollection"]
    fields = namespace["FieldsCollection"]
    for values in FACADES:
        builder.add(facades, facade(id=values["Id"]))
    for values in FIELDS:
        builder.add(
            fields,
            field(
                field_name=values["FieldName"],
                kind=values["Kind"],
                order=values["Order"],
                owner=values["Owner"],
            ),
        )
    return builder.freeze()


if __name__ == "__main__":
    raise SystemExit(run_case("yidl_update_a_multi_source_from.py", render_case, validate_case))
