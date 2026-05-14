from __future__ import annotations

import pytest

from yidl.concept_parser import YidlSymbolError
from yidl.concept_parser import compile_yidl_files


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
