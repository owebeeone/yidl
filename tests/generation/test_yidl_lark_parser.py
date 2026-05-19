from __future__ import annotations

from pathlib import Path

import pytest
from lark import Tree

from yidl.concept_parser import YidlSyntaxError
from yidl.concept_parser import YidlSymbolError
from yidl.concept_parser import compile_yidl_files
from yidl.concept_parser import parse_yidl_source
from yidl.generation.data_def_sys import AstichiTemplateValue
from yidl.generation.data_def_sys import MatcherGeneratedValue

_DATA_YIDL = Path(__file__).resolve().parents[1] / "data" / "yidl"


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


def test_yidl_lark_record_decl_and_default_values_lower() -> None:
    source = """
    module records

    concept Records {
        property Name: str
        property Bases: object = ()
        property Tags: object = ("primary",)
        property Annotation: object = object

        record Field {
            Name
            Bases
            Tags
            Annotation
        }

        collection Fields: Field identity Name many
    }
    """

    compiled = compile_yidl_files({"records.yidl": source}, "records.yidl")
    concept = compiled.concepts["Records"]
    record = concept.records["Field"]

    assert concept.properties["Bases"].default == ()
    assert concept.properties["Tags"].default == ("primary",)
    assert concept.properties["Annotation"].default is object
    assert [prop.name for prop in record.properties] == [
        "Name",
        "Bases",
        "Tags",
        "Annotation",
    ]
    assert concept.collections["Fields"].record is record

    dds = concept.plan.build_data_definition()
    assert [(prop.name, prop.default) for prop in dds.properties] == [
        ("Name", concept.properties["Name"].default),
        ("Bases", ()),
        ("Tags", ("primary",)),
        ("Annotation", object),
    ]


def test_yidl_lark_dataclasses_source_fixture_compiles() -> None:
    entry_path = "tests/data/yidl/dataclasses_example.yidl"
    source = (_DATA_YIDL / "dataclasses_example.yidl").read_text(encoding="utf-8")

    compiled = compile_yidl_files({entry_path: source}, entry_path)
    concept = compiled.concepts["DataclassSubstitute"]

    assert sorted(concept.records) == ["DataclassFacade", "DataclassField"]
    assert sorted(concept.collections) == ["Facades", "Fields"]
    assert sorted(concept.assemblies) == ["DataclassModule"]


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


def test_yidl_lark_update_a_assembly_surface_parses() -> None:
    source = """
    module update_a

    concept UpdateA {
        property ClassId: str
        property FieldOwner: str
        property FieldOrder: int
        property FieldName: str

        family FacadeSpecs {
            variant Facade {
                ClassId
            }
        }

        family FieldSpecs {
            variant Field {
                FieldOwner
                FieldOrder
                FieldName
            }
        }

        collection Facades: FacadeSpecs identity ClassId many
        collection Fields: FieldSpecs identity FieldName many

        resource RootTemplate = code `astichi_hole(body)`
        resource ChildTemplate = template `field_name__astichi_arg__`

        contribution ChildContribution = ChildTemplate {
            as ChildNode
            index FieldOrder
            order (FieldOrder,)

            target body {
                build /Root/ChildNode[FieldOrder]
                owner /Root/*
            }

            ident field_name = FieldName
            external field_name = FieldName
        }

        matcher ChildSelection(field: Fields, facade: Facades) -> contribution {
            default -> ChildContribution
            rule selected when FieldOwner == ClassId -> ChildContribution weight 5
        }

        assemble ChildEdge(facade: Facades)
            from field: Fields
            where FieldOwner == ClassId
            using ChildSelection

        production RootProduction(facade: Facades) -> composable {
            root Root = RootTemplate {
                external module_name = ClassId
            }

            apply child_items
                from field: Fields
                where FieldOwner == ClassId
                using ChildSelection

            apply ChildEdge
        }

        assembly Module = RootProduction
    }
    """

    tree = parse_yidl_source("update_a.yidl", source)

    assert len(_children(tree, "contribution_decl")) == 1
    assert len(_children(tree, "target_decl")) == 1
    assert len(_children(tree, "target_build")) == 1
    assert len(_children(tree, "target_owner")) == 1
    assert len(_children(tree, "path_index")) == 1
    assert len(_children(tree, "matcher_kind_contribution")) == 1
    assert len(_children(tree, "assemble_decl")) == 1
    assert len(_children(tree, "composable_production_decl")) == 1
    assert len(_children(tree, "apply_decl")) == 2
    assert len(_children(tree, "assembly_decl")) == 1


def test_yidl_lark_matcher_default_requires_arrow() -> None:
    source = """
    module matcher_example

    concept MatcherExample {
        resource Plain = code `{"getter": "plain"}`

        matcher Getter() {
            default Plain
        }
    }
    """

    with pytest.raises(YidlSyntaxError):
        parse_yidl_source("matcher.yidl", source)


def test_yidl_lark_apply_where_requires_using() -> None:
    source = """
    module update_a

    concept UpdateA {
        property FieldOwner: str
        property ClassId: str
        resource RootTemplate = code `astichi_hole(body)`

        production RootProduction -> composable {
            root Root = RootTemplate
            apply child_items where FieldOwner == ClassId
        }
    }
    """

    with pytest.raises(YidlSyntaxError):
        parse_yidl_source("apply.yidl", source)


def test_yidl_lark_path_segments_reject_decorated_names() -> None:
    source = """
    module update_a

    concept UpdateA {
        resource ChildTemplate = template `pass`

        contribution ChildContribution = ChildTemplate {
            target body {
                build /Root.Child
            }
        }
    }
    """

    with pytest.raises(YidlSyntaxError):
        parse_yidl_source("path.yidl", source)


def test_yidl_lark_path_interpolation_rejected_by_parser() -> None:
    source = """
    module update_a

    concept UpdateA {
        resource ChildTemplate = template `pass`

        contribution ChildContribution = ChildTemplate {
            target body {
                build /Root/{ClassId}
            }
        }
    }
    """

    with pytest.raises(YidlSyntaxError):
        parse_yidl_source("path.yidl", source)


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


def test_yidl_lark_template_edge_resolves_imported_resource() -> None:
    core = """
    module core
    export concept Core

    concept Core {
        resource Bind = code `{"value": self.value}`
    }
    """
    child = """
    module child
    import "core.yidl" as core

    concept Child {
        resource GetterTemplate = template `pass` {
            edge bind = core.Bind
        }
    }
    """

    compiled = compile_yidl_files(
        {"core.yidl": core, "child.yidl": child},
        "child.yidl",
    )

    template = compiled.concepts["Child"].resources["GetterTemplate"]

    assert isinstance(template, AstichiTemplateValue)
    assert isinstance(template.edge_bind, MatcherGeneratedValue)
    assert template.edge_bind.source == '{"value": self.value}'


def test_yidl_lark_from_import_concept_extends() -> None:
    core = """
    module core

    concept Core {
        property Name: str
    }
    """
    child = """
    module child
    from "core.yidl" import concept Core

    concept Child extends Core {
        property Count: int
    }
    """

    compiled = compile_yidl_files(
        {"core.yidl": core, "child.yidl": child},
        "child.yidl",
    )

    dds = compiled.concepts["Child"].plan.build_data_definition()

    assert [prop.name for prop in dds.properties] == ["Name", "Count"]


def test_yidl_lark_from_import_resource_alias_resolves_template_edge() -> None:
    core = """
    module core

    concept Core {
        resource Bind = code `{"value": self.value}`
    }
    """
    child = """
    module child
    from "core.yidl" import resource Bind as BaseBind

    concept Child {
        resource GetterTemplate = template `pass` {
            edge bind = BaseBind
        }
    }
    """

    compiled = compile_yidl_files(
        {"core.yidl": core, "child.yidl": child},
        "child.yidl",
    )

    template = compiled.concepts["Child"].resources["GetterTemplate"]

    assert isinstance(template, AstichiTemplateValue)
    assert isinstance(template.edge_bind, MatcherGeneratedValue)
    assert template.edge_bind.source == '{"value": self.value}'


def test_yidl_lark_from_import_missing_symbol_reports_kind_path_and_name() -> None:
    core = """
    module core

    concept Core {
        resource Bind = code `{}`
    }
    """
    child = """
    module child
    from "core.yidl" import resource Missing

    concept Child {
    }
    """

    with pytest.raises(YidlSymbolError) as exc_info:
        compile_yidl_files(
            {"core.yidl": core, "child.yidl": child},
            "child.yidl",
        )

    message = str(exc_info.value)
    assert "core.yidl" in message
    assert "resource" in message
    assert "Missing" in message
    assert "missing" in message


def test_yidl_lark_from_import_duplicate_alias_rejects() -> None:
    left = """
    module left

    concept Left {
        resource Root = code `1`
    }
    """
    right = """
    module right

    concept Right {
        resource Other = code `2`
    }
    """
    child = """
    module child
    from "left.yidl" import resource Root
    from "right.yidl" import resource Other as Root

    concept Child {
    }
    """

    with pytest.raises(YidlSymbolError, match="import.*Root.*already"):
        compile_yidl_files(
            {"left.yidl": left, "right.yidl": right, "child.yidl": child},
            "child.yidl",
        )


def test_yidl_lark_from_import_alias_collides_with_import_alias() -> None:
    left = """
    module left

    concept Left {
    }
    """
    right = """
    module right

    concept Right {
        resource Root = code `2`
    }
    """
    child = """
    module child
    import "left.yidl" as core
    from "right.yidl" import resource Root as core

    concept Child {
    }
    """

    with pytest.raises(YidlSymbolError, match="import.*core.*already"):
        compile_yidl_files(
            {"left.yidl": left, "right.yidl": right, "child.yidl": child},
            "child.yidl",
        )


def test_yidl_lark_from_import_local_shadow_rejects() -> None:
    core = """
    module core

    concept Core {
        resource Root = code `1`
    }
    """
    child = """
    module child
    from "core.yidl" import resource Root

    concept Child {
        resource Root = code `2`
    }
    """

    with pytest.raises(YidlSymbolError, match="Root.*import.*already|already.*import.*Root"):
        compile_yidl_files(
            {"core.yidl": core, "child.yidl": child},
            "child.yidl",
        )


def test_yidl_lark_from_import_unsupported_kind_rejects() -> None:
    core = """
    module core

    concept Core {
    }
    """
    child = """
    module child
    from "core.yidl" import port FieldPort

    concept Child {
    }
    """

    with pytest.raises(YidlSymbolError) as exc_info:
        compile_yidl_files(
            {"core.yidl": core, "child.yidl": child},
            "child.yidl",
        )

    message = str(exc_info.value)
    assert "from-import" in message
    assert "port" in message
    assert "not implemented" in message


def test_yidl_lark_resource_expression_reports_wrong_kind() -> None:
    source = """
    module snippets

    concept Snippets {
        property Bind: str

        resource GetterTemplate = template `pass` {
            edge bind = Bind
        }
    }
    """

    with pytest.raises(YidlSymbolError, match="property"):
        compile_yidl_files({"snippets.yidl": source}, "snippets.yidl")


def test_yidl_lark_match_resource_rejected_without_match_context() -> None:
    source = """
    module snippets

    concept Snippets {
        resource GetterTemplate = template `pass` {
            edge bind = match.resource()
        }
    }
    """

    with pytest.raises(YidlSymbolError, match=r"match\.resource"):
        compile_yidl_files({"snippets.yidl": source}, "snippets.yidl")


def test_yidl_lark_matcher_lowers_default_rule_and_weight() -> None:
    source = """
    module matcher_example

    concept MatcherExample {
        property Name: str
        property Kind: str

        family FieldSpecs {
            common Name, Kind
            variant Field {}
        }

        collection Fields: FieldSpecs identity Name many

        resource Plain = code `{"getter": "plain"}`
        resource Managed = code `{"getter": "managed"}`

        matcher Getter(field: Fields) {
            default -> Plain
            rule managed when field.Kind == "managed" -> Managed weight 10
        }
    }
    """

    compiled = compile_yidl_files({"matcher.yidl": source}, "matcher.yidl")
    concept = compiled.concepts["MatcherExample"]
    dds = concept.plan.build_data_definition()
    matcher = dds.matchers[0]
    rule = matcher.rules[0]
    condition = rule.conditions[0]

    assert concept.matchers["Getter"].name == "Getter"
    assert matcher.name == "Getter"
    assert matcher.inputs[0].name == "field"
    assert matcher.inputs[0].source.name == "Fields"
    assert matcher.default_resource is concept.resources["Plain"]
    assert rule.name == "managed"
    assert rule.resource is concept.resources["Managed"]
    assert rule.weight == 10.0
    assert condition.ref.input.name == "field"
    assert condition.ref.property.name == "Kind"
    assert condition.value == "managed"


def test_yidl_lark_matcher_reports_missing_input_property() -> None:
    source = """
    module matcher_example

    concept MatcherExample {
        property Name: str
        family FieldSpecs {
            common Name
            variant Field {}
        }
        collection Fields: FieldSpecs identity Name many
        resource Plain = code `{"getter": "plain"}`

        matcher Getter(field: Fields) {
            rule broken when field.Missing == "managed" -> Plain
        }
    }
    """

    with pytest.raises(YidlSymbolError, match="Missing"):
        compile_yidl_files({"matcher.yidl": source}, "matcher.yidl")


def test_yidl_lark_matcher_rejects_match_resource_target() -> None:
    source = """
    module matcher_example

    concept MatcherExample {
        property Name: str
        family FieldSpecs {
            common Name
            variant Field {}
        }
        collection Fields: FieldSpecs identity Name many

        matcher Getter(field: Fields) {
            rule broken when field.Name == "count" -> match.resource()
        }
    }
    """

    with pytest.raises(YidlSymbolError, match=r"match\.resource"):
        compile_yidl_files({"matcher.yidl": source}, "matcher.yidl")


def test_yidl_lark_matcher_result_production_lowers_resource_flow() -> None:
    source = """
    module production_example

    concept ProductionExample {
        property Name: str
        property Kind: str
        property Template: object

        family FieldSpecs {
            common Name, Kind
            variant Field {}
        }

        family ComponentSpecs {
            variant Component {
                Name
                Template
            }
        }

        collection Fields: FieldSpecs identity Name many
        collection Components: Component identity Name many

        resource Plain = code `{"getter": "plain"}`
        resource Managed = code `{"getter": "managed"}`

        matcher Getter(field: Fields) {
            default -> Plain
            rule managed when field.Kind == "managed" -> Managed
        }

        production ToComponents from Getter.results() to Components {
            identity match.record("field").Name
            policy AddIfAbsent
            set Name = match.record("field").Name
            set Template = match.resource()
        }
    }
    """

    compiled = compile_yidl_files({"production.yidl": source}, "production.yidl")
    dds = compiled.concepts["ProductionExample"].plan.build_data_definition()
    production = dds.productions[0]
    values = {item.property.name: item.expression for item in production.values}

    assert production.name == "ToComponents"
    assert production.source.matcher.name == "Getter"
    assert production.target.name == "Components"
    assert production.policy.name == "AddIfAbsent"
    assert production.identity.__class__.__name__ == "MatchRecordProperty"
    assert production.identity.input_index == 0
    assert values["Name"].__class__.__name__ == "MatchRecordProperty"
    assert values["Name"].input_index == 0
    assert values["Template"].__class__.__name__ == "MatchResource"


def test_yidl_lark_matcher_result_production_reports_bad_input_name() -> None:
    source = """
    module production_example

    concept ProductionExample {
        property Name: str
        property Kind: str
        property Template: object

        family FieldSpecs {
            common Name, Kind
            variant Field {}
        }
        family ComponentSpecs {
            variant Component {
                Name
                Template
            }
        }
        collection Fields: FieldSpecs identity Name many
        collection Components: Component identity Name many
        resource Plain = code `{"getter": "plain"}`
        matcher Getter(field: Fields) {
            default -> Plain
            rule plain when field.Kind == "plain" -> Plain
        }

        production ToComponents from Getter.results() to Components {
            set Name = match.record("missing").Name
            set Template = match.resource()
        }
    }
    """

    with pytest.raises(YidlSymbolError, match="missing"):
        compile_yidl_files({"production.yidl": source}, "production.yidl")


def test_yidl_lark_operation_lowers_direct_resource_and_ordering() -> None:
    source = """
    module operation_example

    concept OperationExample {
        property Name: str
        property Order: int

        family ItemSpecs {
            variant Item {
                Name
                Order
            }
        }

        collection Items: Item identity Name many
        resource BuildItemsBody = code `pass`

        operation BuildItems inputs(Items) outputs(Items) using BuildItemsBody {
            ordered(Order)
        }
    }
    """

    compiled = compile_yidl_files({"operation.yidl": source}, "operation.yidl")
    concept = compiled.concepts["OperationExample"]
    dds = concept.plan.build_data_definition()
    operation = dds.operations[0]

    assert concept.operations["BuildItems"].name == "BuildItems"
    assert operation.name == "BuildItems"
    assert operation.inputs[0].name == "Items"
    assert operation.outputs[0].name == "Items"
    assert operation.resource is concept.resources["BuildItemsBody"]
    assert operation.order_by[0].name == "Order"


def test_yidl_lark_operation_rejects_match_resource_body() -> None:
    source = """
    module operation_example

    concept OperationExample {
        property Name: str
        family ItemSpecs {
            variant Item {
                Name
            }
        }
        collection Items: Item identity Name many

        operation BuildItems inputs(Items) outputs(Items) using match.resource()
    }
    """

    with pytest.raises(YidlSymbolError, match=r"match\.resource"):
        compile_yidl_files({"operation.yidl": source}, "operation.yidl")


def test_yidl_lark_operation_reports_unsupported_diagnostics_option() -> None:
    source = """
    module operation_example

    concept OperationExample {
        property Name: str
        family ItemSpecs {
            variant Item {
                Name
            }
        }
        collection Items: Item identity Name many
        resource BuildItemsBody = code `pass`

        operation BuildItems inputs(Items) outputs(Items) using BuildItemsBody {
            diagnostics BuildDiagnostics
        }
    }
    """

    with pytest.raises(YidlSymbolError, match="diagnostics"):
        compile_yidl_files({"operation.yidl": source}, "operation.yidl")


def _children(tree: Tree, data: str) -> tuple[Tree, ...]:
    result: list[Tree] = []
    for child in tree.iter_subtrees():
        if child.data == data:
            result.append(child)
    return tuple(result)
