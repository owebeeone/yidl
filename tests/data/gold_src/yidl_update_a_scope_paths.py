from __future__ import annotations

from collections.abc import Mapping
from pprint import pformat

from support.golden_case import run_case
from yidl.concept_parser import compile_yidl_files
from yidl.generation.assembly_runtime import DataStack
from yidl.generation.assembly_runtime import path_selector_tuple
from yidl.generation.assembly_runtime import render_path_selector


YIDL_SOURCE = """
module scope_paths

concept ScopePaths {
    property FieldName: str
    property FieldOrder: int

    family FieldSpecs {
        variant Field {
            FieldName
            FieldOrder
        }
    }

    collection Fields: FieldSpecs identity FieldName many

    resource RootTemplate = code `astichi_hole(entries)`
    resource EntryTemplate = code `astichi_hole(value)`
    resource ValueTemplate = template `value = 1`

    contribution EntryContribution = EntryTemplate {
        as GetterEntry
        index FieldOrder
        order FieldOrder

        target entries {
            build /Root
        }
    }

    contribution ValueContribution = ValueTemplate {
        as GetterValue
        index FieldOrder
        order FieldOrder

        target value {
            build /Root/GetterEntry[FieldOrder]
        }
    }

    matcher EntrySelection(field: Fields) -> contribution {
        default -> EntryContribution
    }

    matcher ValueSelection(field: Fields) -> contribution {
        default -> ValueContribution
    }

    production RootProduction -> composable {
        root Root = RootTemplate
        apply entries from field: Fields using EntrySelection
        apply values from field: Fields using ValueSelection
    }

    assembly Module = RootProduction
}
"""


def render_case() -> str:
    result = _path_result()
    return "\n".join(
        [
            "from __future__ import annotations",
            "",
            f"PATHS = {pformat(result, sort_dicts=True, width=88)}",
            "",
        ]
    )


def validate_case(source: str) -> None:
    namespace: dict[str, object] = {}
    exec(source, namespace)
    assert namespace["PATHS"] == {
        "rendered": "Root/GetterEntry[10]",
        "selector": ("Root", "GetterEntry[10]"),
    }


def _path_result() -> Mapping[str, object]:
    module = compile_yidl_files({"scope_paths.yidl": YIDL_SOURCE}, "scope_paths.yidl")
    concept = module.concepts["ScopePaths"]
    contribution = concept.contributions["ValueContribution"]
    build_path = next(
        target_path.path
        for target_path in contribution.target.paths
        if target_path.kind == "build"
    )
    stack = DataStack(({"FieldName": "count", "FieldOrder": 10},))
    return {
        "rendered": render_path_selector(build_path, stack),
        "selector": path_selector_tuple(
            build_path,
            stack,
            context="ValueContribution build",
        ),
    }


if __name__ == "__main__":
    raise SystemExit(run_case("yidl_update_a_scope_paths.py", render_case, validate_case))
