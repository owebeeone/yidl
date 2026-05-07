from __future__ import annotations

import pytest
from lark import Tree

from yidl.concept_parser import YidlSyntaxError
from yidl.concept_parser import YidlSymbolError
from yidl.concept_parser import compile_yidl_files
from yidl.concept_parser import parse_yidl_source
from yidl.generation.data_def_sys import AstichiTemplateValue
from yidl.generation.data_def_sys import MatcherGeneratedValue


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


def test_yidl_lark_resource_snippet_forms_parse() -> None:
    source = '''
    module snippets

    concept Snippets {
        resource StringSnippet = code "lambda s: s + 1"
        resource InlineBacktick = code `lambda s: s + 1`
        resource DollarParenInline = code $(lambda s: s + 1)$
        resource DollarSquareInline = code $[lambda s: s + 1]$

        resource DollarSquareBlock = code $[
            # Python comment, not a YIDL comment.
            def f():
                return 1
        ]$ {
            keep f, value
        }

        resource DollarParenBlock = code $(
            def g():
                return 2
        )$

        resource FencePlain = code ```
            def h():
                return 3
        ```

        resource FencePython = template ```python
            def i():
                return 4
        ``` {
            edge keep_names = KeepNamesResource
            edge arg_names = ArgNamesResource
            edge bind = BindResource
        }
    }
    '''

    tree = parse_yidl_source("snippets.yidl", source)

    assert len(_children(tree, "resource_code")) == 7
    assert len(_children(tree, "resource_template")) == 1
    assert len(_children(tree, "resource_keep")) == 1
    assert len(_children(tree, "resource_edge")) == 3
    assert "# Python comment, not a YIDL comment." in str(tree)


def test_yidl_lark_unterminated_snippet_reports_syntax_error() -> None:
    source = """
    module snippets

    concept Snippets {
        resource Broken = code $[
            def f():
                return 1
    }
    """

    with pytest.raises(YidlSyntaxError) as exc_info:
        parse_yidl_source("unterminated.yidl", source)

    message = str(exc_info.value)
    assert "unterminated.yidl" in message
    assert "line" in message
    assert "column" in message


def test_yidl_lark_code_resource_lowers_to_generated_value() -> None:
    source = """
    module snippets

    concept Snippets {
        resource Inc = code `lambda s: s + 1`

        resource Getter = code $[
            def get(self):
                return self.value
        ]$ {
            keep get, self
        }
    }
    """

    compiled = compile_yidl_files({"snippets.yidl": source}, "snippets.yidl")
    resources = compiled.concepts["Snippets"].resources

    inc = resources["Inc"]
    getter = resources["Getter"]

    assert isinstance(inc, MatcherGeneratedValue)
    assert inc.source == "lambda s: s + 1"
    assert inc.file_name == "snippets.yidl"
    assert inc.line_number > 0
    assert inc.offset > 0
    inc.to_generator()

    assert isinstance(getter, MatcherGeneratedValue)
    assert getter.source == "def get(self):\n    return self.value"
    assert getter.file_name == "snippets.yidl"
    assert getter.line_number > inc.line_number
    assert getter.offset == 0
    assert "get" in getter.keep_names
    assert "self" in getter.keep_names
    getter.to_generator()


def test_yidl_lark_empty_code_resource_reports_resource_name() -> None:
    source = """
    module snippets

    concept Snippets {
        resource Empty = code ``
    }
    """

    with pytest.raises(YidlSymbolError, match="Empty"):
        compile_yidl_files({"snippets.yidl": source}, "snippets.yidl")


def test_yidl_lark_template_resource_lowers_edges() -> None:
    source = """
    module snippets

    concept Snippets {
        resource ArgNames = code `{"field_name": "name"}`
        resource Bind = code `{"value": self.value}`
        resource KeepNames = code `("value",)`

        resource GetterTemplate = template $[
            def get(self):
                return value
        ]$ {
            keep get
            edge arg_names = ArgNames
            edge bind = Bind
            edge keep_names = KeepNames
        }
    }
    """

    compiled = compile_yidl_files({"snippets.yidl": source}, "snippets.yidl")
    resources = compiled.concepts["Snippets"].resources
    template = resources["GetterTemplate"]

    assert isinstance(template, AstichiTemplateValue)
    assert template.template.source == "def get(self):\n    return value"
    assert "get" in template.template.keep_names
    assert template.edge_arg_names is resources["ArgNames"]
    assert template.edge_bind is resources["Bind"]
    assert template.edge_keep_names is resources["KeepNames"]
    template.to_generator()


def test_yidl_lark_template_edge_reports_missing_resource() -> None:
    source = """
    module snippets

    concept Snippets {
        resource GetterTemplate = template `pass` {
            edge bind = Missing
        }
    }
    """

    with pytest.raises(YidlSymbolError, match="Missing"):
        compile_yidl_files({"snippets.yidl": source}, "snippets.yidl")


def _children(tree: Tree, data: str) -> tuple[Tree, ...]:
    result: list[Tree] = []
    for child in tree.iter_subtrees():
        if child.data == data:
            result.append(child)
    return tuple(result)
