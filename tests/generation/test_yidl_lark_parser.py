from __future__ import annotations

from pathlib import Path

import pytest
from lark import Tree

from yidl.concept_parser import YidlSyntaxError
from yidl.concept_parser import YidlSymbolError
from yidl.concept_parser import compile_yidl_files
from yidl.concept_parser import parse_yidl_source
from yidl.generation.data_def_sys import emit_concept_runtime_source
from yidl.generation.data_def_sys import AstichiTemplateValue
from yidl.generation.data_def_sys import MatcherGeneratedValue
from yidl.runtime.transaction_yidl import DEFAULT_TRANSACTION

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


def test_yidl_transactional_phase_a_schema_compiles() -> None:
    path = _DATA_YIDL / "yidl_transactional_phase_a_base" / "lifecycle_base.yidl"
    compiled = compile_yidl_files(
        {path.as_posix(): path.read_text(encoding="utf-8")},
        path.as_posix(),
    )
    concept = compiled.concepts["LifecycleBase"]

    assert set(concept.collections) >= {
        "Classes",
        "Fields",
        "FacadeClasses",
        "FacadeExposures",
        "TransactionalFields",
        "TxGroups",
        "IndexedTransactionalFields",
        "InitParameters",
        "InitAssignments",
        "ClassVarAssignments",
        "DefaultFactoryDependencies",
        "DefaultFactoryEvaluationSteps",
        "DefaultFactoryDiagnostics",
    }
    assert set(concept.records) >= {
        "LifecycleClass",
        "FacadeClass",
        "FacadeExposure",
        "TransactionalField",
        "TxGroup",
        "IndexedTransactionalField",
        "InitParameter",
        "InitAssignment",
        "ClassVarAssignment",
        "DefaultFactoryDependency",
        "DefaultFactoryEvaluationStep",
        "DefaultFactoryDiagnostic",
    }
    dds = concept.plan.build_data_definition()
    field_family = next(
        union for union in dds.unions if union.name == "LifecycleFieldSpec"
    )
    assert "DefaultFactoryParamNames" in {
        prop.name for prop in field_family.variants[0].properties
    }
    assert [variant.name for variant in field_family.variants] == [
        "PlainField",
        "InitVarField",
        "ClassVarField",
        "ManagedField",
    ]


def test_yidl_transactional_phase_a_tx_facts_are_computed() -> None:
    namespace = _lifecycle_base_namespace()

    builder = namespace["new_builder"]()
    classes = namespace["ClassesCollection"]
    fields = namespace["FieldsCollection"]
    lifecycle_class = namespace["LifecycleClass"]
    plain_field = namespace["PlainField"]
    managed_field = namespace["ManagedField"]

    builder.add(
        classes,
        lifecycle_class(
            class_id="Counter",
            class_name="Counter",
            class_order=10,
            state_class_name="Counter_State",
            facade_base_class_name="Counter_FacadeBase",
            current_facade_class_name="Counter_Current",
            working_facade_class_name="Counter_Working",
            lifecycle_definition_param_name="_Counter_lifecycle_definition",
            annotations_param_name="_Counter_annotations",
            tx_groups_param_name="_Counter_tx_groups",
        ),
    )
    builder.add(
        fields,
        plain_field(
            field_id="Counter.plain",
            field_owner="Counter",
            field_name="plain",
            field_order=10,
            field_kind="field",
        ),
    )
    builder.add(
        fields,
        managed_field(
            field_id="Counter.count",
            field_owner="Counter",
            field_name="count",
            field_order=20,
            field_kind="managed",
        ),
    )
    builder.add(
        fields,
        managed_field(
            field_id="Counter.audit_count",
            field_owner="Counter",
            field_name="audit_count",
            field_order=30,
            field_kind="managed",
            tx_group_key="audit",
        ),
    )

    container = namespace["build_container"](builder)

    assert [
        (record.class_id, record.tx_group_key, record.tx_index, record.tx_group_order)
        for record in container.TxGroups.sequence()
    ] == [
        ("Counter", DEFAULT_TRANSACTION, 0, 0),
        ("Counter", "audit", 1, 30),
    ]
    assert [
        (record.field_id, record.tx_group_key, record.tx_index)
        for record in container.IndexedTransactionalFields.sequence()
    ] == [
        ("Counter.count", DEFAULT_TRANSACTION, 0),
        ("Counter.audit_count", "audit", 1),
    ]


def test_yidl_transactional_default_factory_facts_are_computed() -> None:
    namespace = _lifecycle_base_namespace()
    builder = namespace["new_builder"]()
    classes = namespace["ClassesCollection"]
    fields = namespace["FieldsCollection"]
    lifecycle_class = namespace["LifecycleClass"]
    plain_field = namespace["PlainField"]
    initvar_field = namespace["InitVarField"]
    managed_field = namespace["ManagedField"]

    builder.add(
        classes,
        lifecycle_class(
            class_id="Example",
            class_name="Example",
            class_order=10,
            state_class_name="Example_State",
            facade_base_class_name="Example_FacadeBase",
            current_facade_class_name="Example_Current",
            working_facade_class_name="Example_Working",
            lifecycle_definition_param_name="_Example_lifecycle_definition",
            annotations_param_name="_Example_annotations",
            tx_groups_param_name="_Example_tx_groups",
        ),
    )
    builder.add(
        fields,
        plain_field(
            field_id="Example.v1",
            field_owner="Example",
            field_name="v1",
            field_order=10,
            field_kind="field",
        ),
    )
    builder.add(
        fields,
        initvar_field(
            field_id="Example.seed",
            field_owner="Example",
            field_name="seed",
            field_order=20,
            field_kind="initvar",
            init=False,
            has_default=True,
            default_value_param_name="_Example_seed_default",
        ),
    )
    builder.add(
        fields,
        initvar_field(
            field_id="Example.temp",
            field_owner="Example",
            field_name="temp",
            field_order=30,
            field_kind="initvar",
            init=False,
            has_default_factory=True,
            default_factory_param_name="_Example_temp_default_factory",
            default_factory_param_names=("seed", "v1"),
        ),
    )
    builder.add(
        fields,
        managed_field(
            field_id="Example.v2",
            field_owner="Example",
            field_name="v2",
            field_order=40,
            field_kind="managed",
            has_default_factory=True,
            default_factory_param_name="_Example_v2_default_factory",
            default_factory_param_names=("v1",),
        ),
    )
    builder.add(
        fields,
        managed_field(
            field_id="Example.v3",
            field_owner="Example",
            field_name="v3",
            field_order=50,
            field_kind="managed",
            has_default_factory=True,
            default_factory_param_name="_Example_v3_default_factory",
            default_factory_param_names=("v2", "v1"),
        ),
    )

    container = namespace["build_container"](builder)

    assert [
        (record.eval_field_name, record.eval_order)
        for record in container.DefaultFactoryEvaluationSteps.sequence()
    ] == [
        ("temp", 0),
        ("v2", 1),
        ("v3", 2),
    ]
    assert [
        (
            record.consumer_field_name,
            record.param_name,
            record.provider_name,
            record.provider_field_kind,
            record.provider_init,
            record.param_order,
        )
        for record in container.DefaultFactoryDependencies.sequence()
    ] == [
        ("temp", "seed", "seed", "initvar", False, 0),
        ("temp", "v1", "v1", "field", True, 1),
        ("v2", "v1", "v1", "field", True, 0),
        ("v3", "v2", "v2", "managed", True, 0),
        ("v3", "v1", "v1", "field", True, 1),
    ]
    assert list(container.DefaultFactoryDiagnostics.sequence()) == []


def test_yidl_transactional_default_factory_unknown_provider_diagnostic() -> None:
    container = _default_factory_diagnostic_container(("missing",), ())

    assert [
        record.diagnostic_message
        for record in container.DefaultFactoryDiagnostics.sequence()
    ] == [
        "Example.v2: default_factory references unknown name 'missing'",
    ]


def test_yidl_transactional_default_factory_cycle_diagnostic() -> None:
    container = _default_factory_diagnostic_container(("v3",), ("v2",))

    assert [
        record.diagnostic_message
        for record in container.DefaultFactoryDiagnostics.sequence()
    ] == [
        "Example: default_factory dependency cycle: v2 -> v3 -> v2",
    ]


def _lifecycle_base_namespace() -> dict[str, object]:
    path = _DATA_YIDL / "yidl_transactional_phase_a_base" / "lifecycle_base.yidl"
    compiled = compile_yidl_files(
        {path.as_posix(): path.read_text(encoding="utf-8")},
        path.as_posix(),
    )
    concept = compiled.concepts["LifecycleBase"]
    source = emit_concept_runtime_source(
        concept.plan.build_data_definition(),
        resources=concept.resources,
        assembly_plan=concept,
    )
    namespace: dict[str, object] = {}
    exec(source, namespace)
    return namespace


def _default_factory_diagnostic_container(
    v2_params: tuple[str, ...],
    v3_params: tuple[str, ...],
) -> object:
    namespace = _lifecycle_base_namespace()
    builder = namespace["new_builder"]()
    classes = namespace["ClassesCollection"]
    fields = namespace["FieldsCollection"]
    lifecycle_class = namespace["LifecycleClass"]
    managed_field = namespace["ManagedField"]

    builder.add(
        classes,
        lifecycle_class(
            class_id="Example",
            class_name="Example",
            class_order=10,
            state_class_name="Example_State",
            facade_base_class_name="Example_FacadeBase",
            current_facade_class_name="Example_Current",
            working_facade_class_name="Example_Working",
            lifecycle_definition_param_name="_Example_lifecycle_definition",
            annotations_param_name="_Example_annotations",
            tx_groups_param_name="_Example_tx_groups",
        ),
    )
    builder.add(
        fields,
        managed_field(
            field_id="Example.v2",
            field_owner="Example",
            field_name="v2",
            field_order=20,
            field_kind="managed",
            has_default_factory=True,
            default_factory_param_name="_Example_v2_default_factory",
            default_factory_param_names=v2_params,
        ),
    )
    builder.add(
        fields,
        managed_field(
            field_id="Example.v3",
            field_owner="Example",
            field_name="v3",
            field_order=30,
            field_kind="managed",
            has_default_factory=True,
            default_factory_param_name="_Example_v3_default_factory",
            default_factory_param_names=v3_params,
        ),
    )
    namespace["run_build_transaction_facts"](builder)
    namespace["run_build_default_factory_facts"](builder)
    return builder.freeze()


def test_yidl_lark_computed_collection_filter_parse() -> None:
    source = """
    module filters

    concept Filters {
        property Name: str
        property Init: bool = False
        property Kind: str = "plain"

        record Field {
            Name
            Init
            Kind
        }

        collection Fields: Field identity Name many
        computed collection InitFields: Field from Fields where Init == True
        filter InitFields where Kind == "managed"
    }
    """

    tree = parse_yidl_source("filters.yidl", source)

    assert len(tuple(tree.find_data("computed_collection_filter_decl"))) == 1


def test_yidl_lark_computed_collection_filter_refines_runtime_view() -> None:
    module = compile_yidl_files(
        {
            "base.yidl": _computed_filter_base_source(),
            "managed.yidl": """
                module managed

                import "base.yidl" as base

                concept Managed extends base.Base {
                    filter InitFields where Kind == "managed"
                }
            """,
        },
        "managed.yidl",
    )
    concept = module.concepts["Managed"]
    source = emit_concept_runtime_source(
        concept.plan.build_data_definition(),
        resources=concept.resources,
        assembly_plan=concept,
    )
    namespace: dict[str, object] = {}
    exec(source, namespace)

    builder = namespace["new_builder"]()
    fields = namespace["FieldsCollection"]
    field = namespace["Field"]
    builder.add(fields, field(name="plain_init", init=True, kind="plain"))
    builder.add(fields, field(name="managed_init", init=True, kind="managed"))
    builder.add(fields, field(name="managed_no_init", init=False, kind="managed"))

    container = namespace["build_container"](builder)

    assert [record.name for record in container.InitFields.sequence()] == [
        "managed_init"
    ]


def test_yidl_lark_computed_collection_duplicate_diamond_filters_dedupe() -> None:
    module = compile_yidl_files(
        {
            "base.yidl": _computed_filter_base_source(),
            "left.yidl": """
                module left

                import "base.yidl" as base

                concept Left extends base.Base {
                    filter InitFields where Kind == "managed"
                }
            """,
            "right.yidl": """
                module right

                import "base.yidl" as base

                concept Right extends base.Base {
                    filter InitFields where Kind == "managed"
                }
            """,
            "combined.yidl": """
                module combined

                import "left.yidl" as left
                import "right.yidl" as right

                concept Combined extends left.Left, right.Right {}
            """,
        },
        "combined.yidl",
    )

    dds = module.concepts["Combined"].plan.build_data_definition()

    assert [
        condition.property.name for condition in dds.computed_collections[0].conditions
    ] == [
        "Init",
        "Kind",
    ]


def test_yidl_lark_computed_collection_filter_rejects_wrong_target_kind() -> None:
    with pytest.raises(YidlSymbolError, match="not a computed collection"):
        compile_yidl_files(
            {"filters.yidl": """
                    module filters

                    concept Filters {
                        property Name: str
                        property Kind: str = "plain"

                        record Field {
                            Name
                            Kind
                        }

                        collection Fields: Field identity Name many
                        filter Fields where Kind == "managed"
                    }
                """},
            "filters.yidl",
        )


def test_yidl_lark_computed_collection_filter_rejects_unknown_property() -> None:
    with pytest.raises(YidlSymbolError, match="undefined property 'Missing'"):
        compile_yidl_files(
            {"filters.yidl": """
                    module filters

                    concept Filters {
                        property Name: str
                        property Init: bool = False

                        record Field {
                            Name
                            Init
                        }

                        collection Fields: Field identity Name many
                        computed collection InitFields: Field from Fields where Init == True
                        filter InitFields where Missing == True
                    }
                """},
            "filters.yidl",
        )


def test_yidl_lark_computed_collection_redefinition_rejects() -> None:
    with pytest.raises(YidlSymbolError, match="already inherited"):
        compile_yidl_files(
            {
                "base.yidl": _computed_filter_base_source(),
                "child.yidl": """
                    module child

                    import "base.yidl" as base

                    concept Child extends base.Base {
                        computed collection InitFields: Field from Fields where Kind == "managed"
                    }
                """,
            },
            "child.yidl",
        )


def test_yidl_lark_dataclasses_source_fixture_compiles() -> None:
    entry_path = "tests/data/yidl/dataclasses_example.yidl"
    source = (_DATA_YIDL / "dataclasses_example.yidl").read_text(encoding="utf-8")

    compiled = compile_yidl_files({entry_path: source}, entry_path)
    concept = compiled.concepts["DataclassSubstitute"]

    assert sorted(concept.records) == ["DataclassFacade", "DataclassField"]
    assert sorted(concept.collections) == ["Facades", "Fields"]
    assert sorted(concept.assemblies) == ["DataclassModule"]


def test_yidl_lark_resource_snippet_forms_parse() -> None:
    source = """
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
    """

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


def test_yidl_lark_empty_code_resource_lowers_to_no_output_resource() -> None:
    source = """
    module snippets

    concept Snippets {
        resource Empty = code ``
    }
    """

    compiled = compile_yidl_files({"snippets.yidl": source}, "snippets.yidl")
    empty = compiled.concepts["Snippets"].resources["Empty"]

    assert isinstance(empty, MatcherGeneratedValue)
    assert empty.source == ""
    assert empty.to_generator().tree.body == []


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

    with pytest.raises(
        YidlSymbolError, match="Root.*import.*already|already.*import.*Root"
    ):
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


def test_yidl_lark_child_exposes_inherited_assembly_runtime() -> None:
    parent = """
    module parent

    concept Parent {
        resource ModuleRoot = code $[
            VALUE = "parent"
        ]$

        production ModuleProduction -> composable {
            root Root = ModuleRoot
        }

        assembly Module = ModuleProduction
    }
    """
    child = """
    module child
    import "parent.yidl" as parent

    concept Child extends parent.Parent {
        property Extra: str = "x"
    }
    """

    compiled = compile_yidl_files(
        {"parent.yidl": parent, "child.yidl": child},
        "child.yidl",
    )
    concept = compiled.concepts["Child"]

    assert "ModuleRoot" in concept.resources
    assert "ModuleProduction" in concept.composable_productions
    assert "Module" in concept.assemblies
    assert "Extra" in concept.properties

    source = emit_concept_runtime_source(
        concept.plan.build_data_definition(),
        resources=concept.resources,
        assembly_plan=concept,
    )
    namespace: dict[str, object] = {}
    exec(source, namespace)

    assert "build_Module" in namespace
    rendered = namespace["build_Module"](
        namespace["new_builder"]().freeze(),
    ).emit_commented()
    assert "VALUE = 'parent'" in rendered


def test_yidl_lark_composable_production_phases_flatten_in_source_order() -> None:
    source = """
    module phases

    concept PhaseExample {
        resource Root = code $[
            VALUE = []
            astichi_hole(body)
        ]$
        resource AddA = code `VALUE.append("a")`
        resource AddB = code `VALUE.append("b")`
        resource AddC = code `VALUE.append("c")`

        contribution AddA = AddA {
            target body { build /Root }
        }
        contribution AddB = AddB {
            target body { build /Root }
        }
        contribution AddC = AddC {
            target body { build /Root }
        }

        matcher AddAContributions() -> contribution {
            default -> AddA
        }
        matcher AddBContributions() -> contribution {
            default -> AddB
        }
        matcher AddCContributions() -> contribution {
            default -> AddC
        }

        production ModuleProduction -> composable {
            root Root = Root
            phase first {
                apply add_a using AddAContributions
            }
            apply add_b using AddBContributions
            phase second {
                apply add_c using AddCContributions
            }
        }

        assembly Module = ModuleProduction
    }
    """

    concept = compile_yidl_files({"phases.yidl": source}, "phases.yidl").concepts[
        "PhaseExample"
    ]
    production = concept.composable_productions["ModuleProduction"]

    assert [_apply_name(apply) for apply in production.applies] == [
        "ModuleProduction.add_a",
        "ModuleProduction.add_b",
        "ModuleProduction.add_c",
    ]

    generated = emit_concept_runtime_source(
        concept.plan.build_data_definition(),
        resources=concept.resources,
        assembly_plan=concept,
    )
    namespace: dict[str, object] = {}
    exec(generated, namespace)
    rendered = namespace["build_Module"](namespace["new_builder"]().freeze())
    emitted = rendered.emit_commented()
    assert emitted.index(".append('a')") < emitted.index(".append('b')")
    assert emitted.index(".append('b')") < emitted.index(".append('c')")


def test_yidl_lark_composable_production_duplicate_phase_rejects() -> None:
    source = """
    module phases

    concept PhaseExample {
        resource Root = code `VALUE = []`

        production ModuleProduction -> composable {
            root Root = Root
            phase repeat {
            }
            phase repeat {
            }
        }
    }
    """

    with pytest.raises(YidlSymbolError, match="repeats phase"):
        compile_yidl_files({"phases.yidl": source}, "phases.yidl")


def test_yidl_lark_composable_production_phase_rejects_root_member() -> None:
    source = """
    module phases

    concept PhaseExample {
        resource Root = code `VALUE = []`

        production ModuleProduction -> composable {
            root Root = Root
            phase invalid {
                root Other = Root
            }
        }
    }
    """

    with pytest.raises(YidlSyntaxError):
        compile_yidl_files({"phases.yidl": source}, "phases.yidl")


def _apply_name(apply: object) -> str:
    edge = getattr(apply, "edge", None)
    if edge is not None:
        return str(edge.name)
    return str(apply.edge_name)


def test_yidl_lark_diamond_inheritance_dedupes_inherited_maps() -> None:
    source = """
    module diamond

    concept Base {
        property Name: str
        resource Root = code `1`
    }

    concept Left extends Base {
    }

    concept Right extends Base {
    }

    concept Combined extends Left, Right {
        property Count: int
    }
    """

    compiled = compile_yidl_files({"diamond.yidl": source}, "diamond.yidl")
    concept = compiled.concepts["Combined"]

    assert sorted(concept.properties) == ["Count", "Name"]
    assert sorted(concept.resources) == ["Root"]


def test_yidl_lark_inherited_resource_collision_rejects() -> None:
    source = """
    module collision

    concept Left {
        resource Root = code `1`
    }

    concept Right {
        resource Root = code `2`
    }

    concept Combined extends Left, Right {
    }
    """

    with pytest.raises(YidlSymbolError) as exc_info:
        compile_yidl_files({"collision.yidl": source}, "collision.yidl")

    message = str(exc_info.value)
    assert "resource" in message
    assert "Root" in message
    assert "Left" in message
    assert "Right" in message


def test_yidl_lark_local_redefinition_of_inherited_resource_rejects() -> None:
    source = """
    module redefinition

    concept Parent {
        resource Root = code `1`
    }

    concept Child extends Parent {
        resource Root = code `2`
    }
    """

    with pytest.raises(YidlSymbolError) as exc_info:
        compile_yidl_files({"redefinition.yidl": source}, "redefinition.yidl")

    message = str(exc_info.value)
    assert "resource" in message
    assert "Root" in message
    assert "Child" in message
    assert "inherited" in message


def test_yidl_lark_contribution_matcher_rules_merge_across_extends() -> None:
    parent = """
    module parent

    concept Parent {
        property Name: str
        property Kind: str

        record Field {
            Name
            Kind
        }

        collection Fields: Field identity Name many

        resource PlainTemplate = template `pass`

        contribution PlainContribution = PlainTemplate {
            as Plain
            target body { build /Root }
        }

        matcher FieldContributions(field: Fields) -> contribution {
            rule plain when Kind == "plain" -> PlainContribution
        }
    }
    """
    child = """
    module child
    import "parent.yidl" as parent

    concept Child extends parent.Parent {
        resource SpecialTemplate = template `pass`

        contribution SpecialContribution = SpecialTemplate {
            as Special
            target body { build /Root }
        }

        matcher FieldContributions(field: Fields) -> contribution {
            rule special when Kind == "special" -> SpecialContribution weight 10
        }
    }
    """

    compiled = compile_yidl_files(
        {"parent.yidl": parent, "child.yidl": child},
        "child.yidl",
    )

    matcher = compiled.concepts["Child"].contribution_matchers["FieldContributions"]

    assert [rule.name for rule in matcher.rules] == ["plain", "special"]
    assert [rule.contribution_name for rule in matcher.rules] == [
        "PlainContribution",
        "SpecialContribution",
    ]


def test_yidl_lark_resource_matcher_rules_merge_across_extends() -> None:
    parent = """
    module parent

    concept Parent {
        property Name: str
        property Kind: str

        record Field {
            Name
            Kind
        }

        collection Fields: Field identity Name many

        resource Plain = code `{"selected": "plain"}`

        matcher ResourceFor(field: Fields) {
            default -> Plain
        }
    }
    """
    child = """
    module child
    import "parent.yidl" as parent

    concept Child extends parent.Parent {
        resource Special = code `{"selected": "special"}`

        matcher ResourceFor(field: Fields) {
            rule special when field.Kind == "special" -> Special weight 10
        }
    }
    """

    compiled = compile_yidl_files(
        {"parent.yidl": parent, "child.yidl": child},
        "child.yidl",
    )
    concept = compiled.concepts["Child"]
    dds = concept.plan.build_data_definition()
    matcher = next(matcher for matcher in dds.matchers if matcher.name == "ResourceFor")

    assert concept.matchers["ResourceFor"].name == "ResourceFor"
    assert matcher.default_resource is concept.resources["Plain"]
    assert [rule.name for rule in matcher.rules] == ["special"]
    assert matcher.rules[0].resource is concept.resources["Special"]


def test_yidl_lark_resource_matcher_inherited_default_redefinition_rejects() -> None:
    parent = """
    module parent

    concept Parent {
        property Name: str
        record Field { Name }
        collection Fields: Field identity Name many

        resource Plain = code `{"selected": "plain"}`

        matcher ResourceFor(field: Fields) {
            default -> Plain
        }
    }
    """
    child = """
    module child
    import "parent.yidl" as parent

    concept Child extends parent.Parent {
        resource Special = code `{"selected": "special"}`

        matcher ResourceFor(field: Fields) {
            default -> Special
        }
    }
    """

    with pytest.raises(YidlSymbolError) as exc_info:
        compile_yidl_files(
            {"parent.yidl": parent, "child.yidl": child},
            "child.yidl",
        )

    message = str(exc_info.value)
    assert "ResourceFor" in message
    assert "default" in message
    assert "inherited" in message


def test_yidl_lark_resource_matcher_diamond_rules_merge_once() -> None:
    source = """
    module matcher_diamond

    concept Base {
        property Name: str
        property Kind: str

        record Field {
            Name
            Kind
        }

        collection Fields: Field identity Name many

        resource Plain = code `{"selected": "plain"}`

        matcher ResourceFor(field: Fields) {
            default -> Plain
        }
    }

    concept Left extends Base {
        resource LeftResource = code `{"selected": "left"}`

        matcher ResourceFor(field: Fields) {
            rule left when field.Kind == "left" -> LeftResource weight 10
        }
    }

    concept Right extends Base {
        resource RightResource = code `{"selected": "right"}`

        matcher ResourceFor(field: Fields) {
            rule right when field.Kind == "right" -> RightResource weight 10
        }
    }

    concept Combined extends Left, Right {
    }
    """

    compiled = compile_yidl_files(
        {"matcher_diamond.yidl": source}, "matcher_diamond.yidl"
    )
    concept = compiled.concepts["Combined"]
    dds = concept.plan.build_data_definition()
    matcher = next(matcher for matcher in dds.matchers if matcher.name == "ResourceFor")

    assert sorted(concept.resources) == ["LeftResource", "Plain", "RightResource"]
    assert matcher.default_resource is concept.resources["Plain"]
    assert [rule.name for rule in matcher.rules] == ["left", "right"]


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


def test_yidl_lark_collection_lowers_composite_identity() -> None:
    source = """
    module composite_identity_example

    concept CompositeIdentityExample {
        property Owner: str
        property Name: str

        record Item {
            Owner
            Name
        }

        collection Items: Item identity (Owner, Name) many
    }
    """

    compiled = compile_yidl_files({"collection.yidl": source}, "collection.yidl")
    concept = compiled.concepts["CompositeIdentityExample"]
    collection = concept.plan.build_data_definition().collections[0]

    assert [prop.name for prop in collection.identity] == ["Owner", "Name"]


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


def _computed_filter_base_source() -> str:
    return """
        module base

        export concept Base

        concept Base {
            property Name: str
            property Init: bool = False
            property Kind: str = "plain"

            record Field {
                Name
                Init
                Kind
            }

            collection Fields: Field identity Name many
            computed collection InitFields: Field from Fields where Init == True
        }
    """


def _children(tree: Tree, data: str) -> tuple[Tree, ...]:
    result: list[Tree] = []
    for child in tree.iter_subtrees():
        if child.data == data:
            result.append(child)
    return tuple(result)
