from __future__ import annotations

import pytest

from yidl.concept_parser import YidlSyntaxError
from yidl.concept_parser import YidlSymbolError
from yidl.concept_parser import compile_yidl_files
from yidl.concept_parser import parse_yidl_source


def test_yidl_syntax_error_reports_line_and_column() -> None:
    with pytest.raises(YidlSyntaxError) as exc_info:
        parse_yidl_source(
            "broken.yidl",
            "module example\nconcept Broken {\n    property Name str\n}\n",
        )

    message = str(exc_info.value)
    assert "broken.yidl" in message
    assert "line 3" in message
    assert "column" in message


def test_yidl_undefined_symbol_reports_name() -> None:
    source = """
    module example

    concept Broken {
        family FieldSpecs {
            variant Field {
                MissingProperty
            }
        }
    }
    """

    with pytest.raises(YidlSymbolError, match="MissingProperty"):
        compile_yidl_files({"broken.yidl": source}, "broken.yidl")


def test_yidl_imported_symbol_cannot_be_redefined() -> None:
    core = """
    module core
    export concept Core

    concept Core {
        property Name: str storage name
    }
    """
    child = """
    module child
    import "core.yidl" as core

    concept Child extends core.Core {
        property Name: int storage name
    }
    """

    with pytest.raises(YidlSymbolError, match="Name"):
        compile_yidl_files({"core.yidl": core, "child.yidl": child}, "child.yidl")


def test_yidl_extended_family_resolves_local_then_owner_properties() -> None:
    core = """
    module core
    export concept Core

    concept Core {
        property Name: str storage name
        property Kind: object storage kind

        family FieldSpecs {
            common Name, Kind
            variant PlainField {}
        }
    }
    """
    managed = """
    module managed
    import "core.yidl" as core
    export concept Managed

    concept Managed extends core.Core {
        property TxGroup: str = "default" storage tx_group

        family core.FieldSpecs {
            variant ManagedField {
                TxGroup
                Kind
            }
        }
    }
    """

    compiled = compile_yidl_files(
        {"core.yidl": core, "managed.yidl": managed},
        "managed.yidl",
    )
    dds = compiled.concepts["Managed"].plan.build_data_definition()

    managed_field = dds.unions[0].variants[1]
    assert managed_field.name == "ManagedField"
    assert [prop.name for prop in managed_field.properties] == [
        "Name",
        "Kind",
        "TxGroup",
    ]
