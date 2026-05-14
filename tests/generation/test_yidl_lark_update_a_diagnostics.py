from __future__ import annotations

import pytest

from yidl.concept_parser import YidlSymbolError
from yidl.concept_parser import compile_yidl_files
from yidl.generation.assembly_plan import ValueRef
from yidl.generation.assembly_runtime import DataStack
from yidl.generation.assembly_runtime import evaluate_identifier
from yidl.generation.assembly_runtime import evaluate_index
from yidl.generation.assembly_runtime import evaluate_order


def test_update_a_reports_unknown_contribution_rhs() -> None:
    with pytest.raises(YidlSymbolError, match="Missing"):
        _compile(
            """
            matcher Select(field: Fields) -> contribution {
                default -> Missing
            }
            """
        )


def test_update_a_reports_ambiguous_contribution_source() -> None:
    with pytest.raises(YidlSymbolError, match="ambiguous"):
        _compile(
            """
            resource Both = code `pass`

            production Both -> composable {
                root RootNode = Root
            }

            contribution UseBoth = Both {
                target body {
                    build /RootNode
                }
            }
            """
        )


def test_update_a_contribution_matcher_rejects_resource_rhs() -> None:
    with pytest.raises(YidlSymbolError, match="resource, not a contribution"):
        _compile(
            """
            matcher Select(field: Fields) -> contribution {
                default -> Item
            }
            """
        )


def test_update_a_resource_matcher_rejects_contribution_rhs() -> None:
    with pytest.raises(YidlSymbolError, match="contribution, not a resource"):
        _compile(
            """
            contribution ItemContribution = Item {
                target body {
                    build /RootNode
                }
            }

            matcher Select(field: Fields) {
                default -> ItemContribution
            }
            """
        )


def test_update_a_reports_duplicate_target() -> None:
    with pytest.raises(YidlSymbolError, match="repeats target"):
        _compile(
            """
            contribution ItemContribution = Item {
                target body {
                    build /RootNode
                }
                target other {
                    build /RootNode
                }
            }
            """
        )


def test_update_a_reports_duplicate_binding_pair() -> None:
    with pytest.raises(YidlSymbolError, match="repeats ident binding"):
        _compile(
            """
            contribution ItemContribution = Item {
                target body {
                    build /RootNode
                }
                ident field_name = Name
                ident field_name = FieldOrder
            }
            """
        )


def test_update_a_rejects_qualified_value_refs() -> None:
    with pytest.raises(YidlSymbolError, match="qualified value reference"):
        _compile(
            """
            contribution ItemContribution = Item {
                target body {
                    build /RootNode
                }
                ident field_name = field.Name
            }
            """
        )


def test_update_a_reports_duplicate_visible_value_names() -> None:
    with pytest.raises(YidlSymbolError, match="duplicate visible value"):
        _compile(
            """
            contribution ItemContribution = Item {
                target body {
                    build /RootNode
                }
            }

            matcher Select(field: Fields, other: Fields) -> contribution {
                default -> ItemContribution
            }
            """
        )


def test_update_a_reports_unknown_contribution_value_name() -> None:
    with pytest.raises(YidlSymbolError, match="Missing"):
        _compile(
            """
            contribution ItemContribution = Item {
                target body {
                    build /RootNode
                }
                ident field_name = Missing
            }

            matcher Select(field: Fields) -> contribution {
                default -> ItemContribution
            }

            assemble Edge
                from field: Fields
                using Select
            """
        )


def test_update_a_reports_unknown_where_value_name() -> None:
    with pytest.raises(YidlSymbolError, match="Missing"):
        _compile(
            """
            contribution ItemContribution = Item {
                target body {
                    build /RootNode
                }
            }

            matcher Select(field: Fields) -> contribution {
                default -> ItemContribution
            }

            assemble Edge
                from field: Fields
                where Missing == Name
                using Select
            """
        )


def test_update_a_reports_unknown_matcher_rule_value_name() -> None:
    with pytest.raises(YidlSymbolError, match="Missing"):
        _compile(
            """
            contribution ItemContribution = Item {
                target body {
                    build /RootNode
                }
            }

            matcher Select(field: Fields) -> contribution {
                rule selected when Missing == Name -> ItemContribution
            }
            """
        )


def test_update_a_runtime_rejects_non_int_index() -> None:
    with pytest.raises(TypeError, match="index"):
        evaluate_index(ValueRef("name"), DataStack(({"name": "not_int"},)))


def test_update_a_runtime_rejects_non_int_order() -> None:
    with pytest.raises(TypeError, match="order"):
        evaluate_order(ValueRef("name"), DataStack(({"name": "not_int"},)))


def test_update_a_runtime_rejects_invalid_identifier_binding() -> None:
    with pytest.raises(TypeError, match="identifier"):
        evaluate_identifier(ValueRef("name"), DataStack(({"name": "not valid"},)))


def _compile(body: str) -> object:
    source = f"""
    module diagnostics

    concept Diagnostics {{
        property Name: str
        property FieldOrder: int

        family FieldSpecs {{
            variant Field {{
                Name
                FieldOrder
            }}
        }}

        collection Fields: FieldSpecs identity Name many

        resource Root = code `astichi_hole(body)`
        resource Item = template `pass`

        {body}
    }}
    """
    return compile_yidl_files({"diagnostics.yidl": source}, "diagnostics.yidl")
