from __future__ import annotations

import pytest

from yidl.concept_parser import YidlSymbolError
from yidl.concept_parser import compile_yidl_files


def test_operation_matcher_lowers_rules_and_default() -> None:
    concept = _compile_concept(
        """
        resource BuildDefault = code `pass`
        resource BuildSpecial = code `pass`

        matcher BuildFacts(field: Fields) -> operation {
            default -> BuildDefault
            rule special when Name == "special" -> BuildSpecial weight 2
        }
        """
    )

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
        _compile_concept(
            """
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
            """
        )


def _compile_concept(body: str) -> object:
    module = compile_yidl_files(
        {
            "operation_matchers.yidl": f"""
                module operation_matchers

                concept OperationMatchers {{
                    property Name: str

                    record Field {{
                        Name
                    }}

                    collection Fields: Field identity Name many

                    {body}
                }}
            """
        },
        "operation_matchers.yidl",
    )
    return module.concepts["OperationMatchers"]
