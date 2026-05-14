from __future__ import annotations

from support.golden_case import run_case
from yidl.concept_parser import compile_yidl_files
from yidl.generation.assembly_runtime import run_assembly
from yidl.generation.data_def_sys import emit_container_runtime_source


YIDL_SOURCE = """
module nested

concept Nested {
    property ClassName: str
    property Owner: str
    property FieldName: str

    family FacadeSpecs {
        variant Facade {
            ClassName
        }
    }

    family FieldSpecs {
        variant Field {
            Owner
            FieldName
        }
    }

    collection Facades: FacadeSpecs identity ClassName many
    collection Fields: FieldSpecs identity FieldName many

    resource ModuleTemplate = code $[
        HELPER = "ok"
        astichi_hole(classes)
    ]$ {
        keep HELPER
    }

    resource ClassTemplate = code $[
        class class_name__astichi_arg__:
            astichi_hole(body)
    ]$ {
        keep class_name
    }

    resource MethodTemplate = template $[
        def method_name__astichi_arg__(self):
            return HELPER
    ]$ {
        keep HELPER
    }

    contribution ClassContribution = ClassProduction {
        as ClassDef

        target classes {
            build /Module
        }
    }

    contribution MethodContribution = MethodTemplate {
        as MethodDef
        target body {
            build /ClassDef
        }
        ident method_name = FieldName
    }

    matcher ClassSelection(facade: Facades) -> contribution {
        default -> ClassContribution
    }

    matcher MethodSelection(facade: Facades, field: Fields) -> contribution {
        rule owned when Owner == ClassName -> MethodContribution
    }

    production ClassProduction(facade: Facades) -> composable {
        root ClassDef = ClassTemplate {
            ident class_name = ClassName
        }
        apply methods
            from field: Fields
            where Owner == ClassName
            using MethodSelection
    }

    production ModuleProduction -> composable {
        root Module = ModuleTemplate
        apply classes
            from facade: Facades
            using ClassSelection
    }

    assembly Module = ModuleProduction
}
"""


def render_case() -> str:
    source = _output_source()
    return "\n".join(
        [
            "from __future__ import annotations",
            "",
            f"OUTPUT = {source!r}",
            "",
        ]
    )


def validate_case(source: str) -> None:
    namespace: dict[str, object] = {}
    exec(source, namespace)
    output = namespace["OUTPUT"]
    output_namespace: dict[str, object] = {}
    exec(output, output_namespace)
    assert output_namespace["Widget"]().count() == "ok"


def _output_source() -> str:
    module = compile_yidl_files({"nested.yidl": YIDL_SOURCE}, "nested.yidl")
    concept = module.concepts["Nested"]
    return run_assembly(concept, "Module", _container(concept)).emit_commented()


def _container(concept: object) -> object:
    namespace: dict[str, object] = {}
    exec(emit_container_runtime_source(concept.plan.build_data_definition()), namespace)
    builder = namespace["new_builder"]()
    facade = namespace["Facade"]
    field = namespace["Field"]
    facades = namespace["FacadesCollection"]
    fields = namespace["FieldsCollection"]
    builder.add(facades, facade(class_name="Widget"))
    builder.add(fields, field(owner="Widget", field_name="count"))
    return builder.freeze()


if __name__ == "__main__":
    raise SystemExit(run_case("yidl_update_a_nested_productions.py", render_case, validate_case))
