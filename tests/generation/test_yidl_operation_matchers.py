from __future__ import annotations

import pytest

from yidl.concept_parser import YidlSymbolError
from yidl.concept_parser import compile_yidl_files
from yidl.generation.assembly_source import emit_concept_runtime_source
from yidl.generation.data_schema import OperationMatcherDispatch


def test_operation_matcher_lowers_rules_and_default() -> None:
    concept = _compile_concept("""
        resource BuildDefault = code `pass`
        resource BuildSpecial = code `pass`

        matcher BuildFacts(field: Fields) -> operation {
            default -> BuildDefault
            rule special when Name == "special" -> BuildSpecial weight 2
        }
        """)

    matcher = concept.operation_matchers["BuildFacts"]
    assert matcher.default_resource_name == "BuildDefault"
    assert [input_spec.name for input_spec in matcher.inputs] == ["field"]
    assert [rule.name for rule in matcher.rules] == ["special"]
    assert matcher.rules[0].resource_name == "BuildSpecial"
    assert matcher.rules[0].weight == 2.0


def test_operation_matcher_merges_inherited_rules() -> None:
    module = compile_yidl_files(
        {
            "base.yidl": """
                module base

                export concept Base

                concept Base {
                    property Name: str

                    record Field {
                        Name
                    }

                    collection Fields: Field identity Name many

                    resource BuildDefault = code `pass`
                    resource BuildSpecial = code `pass`

                    matcher BuildFacts(field: Fields) -> operation {
                        default -> BuildDefault
                    }
                }
            """,
            "child.yidl": """
                module child

                import "base.yidl" as base

                concept Child extends base.Base {
                    matcher BuildFacts(field: Fields) -> operation {
                        rule special when Name == "special" -> BuildSpecial
                    }
                }
            """,
        },
        "child.yidl",
    )

    matcher = module.concepts["Child"].operation_matchers["BuildFacts"]
    assert matcher.default_resource_name == "BuildDefault"
    assert [rule.name for rule in matcher.rules] == ["special"]


def test_operation_matcher_rejects_contribution_rhs() -> None:
    with pytest.raises(YidlSymbolError, match="contribution, not a resource"):
        _compile_concept("""
            resource Root = code `astichi_hole(body)`
            resource Item = template `pass`

            contribution ItemContribution = Item {
                target body {
                    build /RootNode
                }
            }

            matcher BuildFacts(field: Fields) -> operation {
                default -> ItemContribution
            }
            """)


def test_matcher_selected_operation_lowers_dispatch() -> None:
    concept = _compile_concept("""
        resource BuildDefault = code `pass`

        matcher BuildFacts(field: Fields) -> operation {
            default -> BuildDefault
        }

        operation BuildFactsOperation
            from field: Fields
            inputs(Fields)
            outputs(Fields)
            using matcher BuildFacts
        """)

    system = concept.plan.build_data_definition()
    operation = system.operations[0]
    assert isinstance(operation.resource, OperationMatcherDispatch)
    assert operation.resource.matcher_name == "BuildFacts"
    assert operation.resource.from_input_name == "field"
    assert operation.resource.from_collection.name == "Fields"


def test_matcher_selected_operation_requires_matching_input_name() -> None:
    with pytest.raises(YidlSymbolError, match="input set"):
        _compile_concept("""
            resource BuildDefault = code `pass`

            matcher BuildFacts(source: Fields) -> operation {
                default -> BuildDefault
            }

            operation BuildFactsOperation
                from field: Fields
                inputs(Fields)
                outputs(Fields)
                using matcher BuildFacts
            """)


def test_matcher_selected_operation_generated_source_dispatches_body() -> None:
    concept = _compile_concept("""
        property Kind: str

        record Output {
            Name
            Kind
        }

        collection Outputs: Output identity Name many

        resource BuildDefault = code $[
            ctx.write(
                OutputsCollection,
                Output(name=field.name, kind="default"),
                policy=RejectDuplicate,
            )
        ]$ {
            keep ctx, field, OutputsCollection, Output, RejectDuplicate
        }

        resource BuildSpecial = code $[
            ctx.write(
                OutputsCollection,
                Output(name=field.name, kind="special"),
                policy=RejectDuplicate,
            )
        ]$ {
            keep ctx, field, OutputsCollection, Output, RejectDuplicate
        }

        matcher BuildFacts(field: Fields) -> operation {
            default -> BuildDefault
            rule special when Name == "special" -> BuildSpecial
        }

        operation BuildFactsOperation
            from field: Fields
            inputs(Fields)
            outputs(Outputs)
            using matcher BuildFacts
        """)
    system = concept.plan.build_data_definition()
    source = emit_concept_runtime_source(
        system,
        resources=concept.resources,
        assembly_plan=concept,
    )
    namespace: dict[str, object] = {}
    exec(source, namespace)

    builder = namespace["new_builder"]()
    fields_collection = namespace["FieldsCollection"]
    field_record = namespace["Field"]
    builder.add(fields_collection, field_record(name="plain"))
    builder.add(fields_collection, field_record(name="special"))

    container = namespace["build_container"](builder)
    outputs = tuple(container.Outputs.sequence())

    assert [(item.name, item.kind) for item in outputs] == [
        ("plain", "default"),
        ("special", "special"),
    ]
    assert "def _operation_0_body_0_build_default(ctx, field):" in source
    assert "def _operation_0_body_1_build_special(ctx, field):" in source
    assert "if field.name == 'special':" in source
    assert "OperationExecutionError" in source


def _compile_concept(body: str) -> object:
    module = compile_yidl_files(
        {"operation_matchers.yidl": f"""
                module operation_matchers

                concept OperationMatchers {{
                    property Name: str

                    record Field {{
                        Name
                    }}

                    collection Fields: Field identity Name many

                    {body}
                }}
            """},
        "operation_matchers.yidl",
    )
    return module.concepts["OperationMatchers"]
