from __future__ import annotations

from support.golden_case import run_case
from yidl.concept_parser import compile_yidl_files
from yidl.generation.assembly_runtime import run_assembly
from yidl.generation.data_def_sys import emit_container_runtime_source


YIDL_SOURCE = """
module apply_namespaces

concept ApplyNamespaces {
    property Name: str

    family ItemSpecs {
        variant Item {
            Name
        }
    }

    collection Items: ItemSpecs identity Name many

    resource RootTemplate = code $[
        EVENTS = []
        astichi_hole(inline)
        astichi_hole(top)
    ]$ {
        keep EVENTS
    }

    resource InlineTemplate = template `EVENTS.append("inline")` {
        keep EVENTS
    }

    resource TopTemplate = template `EVENTS.append("top")` {
        keep EVENTS
    }

    contribution InlineContribution = InlineTemplate {
        target inline {
            build /Root
        }
    }

    contribution TopContribution = TopTemplate {
        target top {
            build /Root
        }
    }

    matcher InlineSelection(item: Items) -> contribution {
        default -> InlineContribution
    }

    matcher TopSelection(item: Items) -> contribution {
        default -> TopContribution
    }

    assemble emit
        from item: Items
        using TopSelection

    production RootProduction -> composable {
        root Root = RootTemplate
        apply emit from item: Items using InlineSelection
        apply emit
    }

    assembly Module = RootProduction
}
"""


def render_case() -> str:
    output = _output_source()
    return "\n".join(
        [
            "from __future__ import annotations",
            "",
            f"OUTPUT = {output!r}",
            "",
        ]
    )


def validate_case(source: str) -> None:
    namespace: dict[str, object] = {}
    exec(source, namespace)
    output = namespace["OUTPUT"]
    assert "EVENTS.append('inline')" in output
    assert "EVENTS.append('top')" in output
    assert output.index("EVENTS.append('inline')") < output.index("EVENTS.append('top')")


def _output_source() -> str:
    module = compile_yidl_files({"apply_namespaces.yidl": YIDL_SOURCE}, "apply_namespaces.yidl")
    concept = module.concepts["ApplyNamespaces"]
    return run_assembly(concept, "Module", _container(concept)).emit_commented()


def _container(concept: object) -> object:
    namespace: dict[str, object] = {}
    exec(emit_container_runtime_source(concept.plan.build_data_definition()), namespace)
    builder = namespace["new_builder"]()
    item = namespace["Item"]
    items = namespace["ItemsCollection"]
    builder.add(items, item(name="one"))
    return builder.freeze()


if __name__ == "__main__":
    raise SystemExit(run_case("yidl_update_a_apply_namespaces.py", render_case, validate_case))
