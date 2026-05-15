"""Lark-backed parser for standalone ``.yidl`` concept modules.

This parser is definition-stage only.  It lowers checked modules into recorded
capsule concept plans and is intentionally not imported by generated decorator
or field-spec runtime paths.
"""

from __future__ import annotations

import ast
from collections.abc import Mapping
from dataclasses import dataclass
from importlib import resources
import posixpath
from typing import Any

from lark import Lark
from lark import Token
from lark import Tree
from lark.exceptions import UnexpectedInput

from yidl.capsule.recorded_builder import CapsuleConceptPlan
from yidl.capsule.recorded_builder import CollectionHandle
from yidl.capsule.recorded_builder import MatcherHandle
from yidl.capsule.recorded_builder import MatcherInputHandle
from yidl.capsule.recorded_builder import MatcherResultSourceHandle
from yidl.capsule.recorded_builder import OperationHandle
from yidl.capsule.recorded_builder import PropertyHandle
from yidl.capsule.recorded_builder import ProductionHandle
from yidl.capsule.recorded_builder import RecordHandle
from yidl.capsule.recorded_builder import SchemaFamilyHandle
from yidl.capsule.recorded_builder import capsule_concept
from yidl.capsule.recorded_builder import match as recorded_match
from yidl.generation.assembly_plan import AndConditionSpec
from yidl.generation.assembly_plan import ApplySpec
from yidl.generation.assembly_plan import AssemblyConditionSpec
from yidl.generation.assembly_plan import AssemblyEdgeSpec
from yidl.generation.assembly_plan import AssemblyInputSpec
from yidl.generation.assembly_plan import AssemblySpec
from yidl.generation.assembly_plan import AssemblyValueRef
from yidl.generation.assembly_plan import BindingSpec
from yidl.generation.assembly_plan import ComposableProductionSpec
from yidl.generation.assembly_plan import ContributionMatcherSpec
from yidl.generation.assembly_plan import ContributionRuleSpec
from yidl.generation.assembly_plan import ContributionSpec
from yidl.generation.assembly_plan import EdgeApplySpec
from yidl.generation.assembly_plan import EqConditionSpec
from yidl.generation.assembly_plan import InlineApplySpec
from yidl.generation.assembly_plan import LiteralValueRef
from yidl.generation.assembly_plan import PathSegmentSpec
from yidl.generation.assembly_plan import PathSpec
from yidl.generation.assembly_plan import RootSpec
from yidl.generation.assembly_plan import TargetPathSpec
from yidl.generation.assembly_plan import TargetSpec
from yidl.generation.assembly_plan import TupleValueRef
from yidl.generation.assembly_plan import ValueRef
from yidl.generation.data_def_sys import AddIfAbsent
from yidl.generation.data_def_sys import GeneratedValue
from yidl.generation.data_def_sys import MatcherGeneratedValue
from yidl.generation.data_def_sys import REQUIRED
from yidl.generation.data_def_sys import RejectDuplicate
from yidl.generation.data_def_sys import ReplaceExisting
from yidl.generation.data_def_sys import astichi_template
from yidl.generation.data_def_sys import from_astichi_code
from yidl.generation.data_def_sys import from_import
from yidl.generation.data_def_sys import from_literal


class YidlSyntaxError(ValueError):
    """Raised when Lark cannot parse a ``.yidl`` source file."""


class YidlSymbolError(ValueError):
    """Raised when parsed YIDL references cannot be resolved."""


@dataclass(frozen=True, slots=True)
class YidlCompiledConcept:
    """Compiled concept plus exported handles used by later imports."""

    name: str
    plan: CapsuleConceptPlan
    properties: Mapping[str, PropertyHandle]
    families: Mapping[str, SchemaFamilyHandle]
    records: Mapping[str, RecordHandle]
    collections: Mapping[str, CollectionHandle]
    resources: Mapping[str, GeneratedValue]
    matchers: Mapping[str, MatcherHandle]
    productions: Mapping[str, ProductionHandle]
    operations: Mapping[str, OperationHandle]
    contributions: Mapping[str, ContributionSpec]
    contribution_matchers: Mapping[str, ContributionMatcherSpec]
    composable_productions: Mapping[str, ComposableProductionSpec]
    assembly_edges: Mapping[str, AssemblyEdgeSpec]
    assemblies: Mapping[str, AssemblySpec]


@dataclass(frozen=True, slots=True)
class YidlCompiledModule:
    """Compiled YIDL module."""

    path: str
    module_name: str | None
    concepts: Mapping[str, YidlCompiledConcept]
    exports: frozenset[tuple[str, str]]


@dataclass(frozen=True, slots=True)
class _SnippetSource:
    source: str
    line_number: int
    offset: int


@dataclass(frozen=True, slots=True)
class _ResourceOptions:
    keep_names: tuple[str, ...] = ()
    edge_options: tuple[Tree, ...] = ()


_POLICIES: Mapping[str, object] = {
    "AddIfAbsent": AddIfAbsent,
    "RejectDuplicate": RejectDuplicate,
    "ReplaceExisting": ReplaceExisting,
}
_PARSER: Lark | None = None
_TYPE_NAMES: dict[str, type[object]] = {
    "object": object,
    "str": str,
    "int": int,
    "bool": bool,
    "float": float,
}
_VALUE_CONSTANTS: dict[str, object] = {
    **_TYPE_NAMES,
    "dict": dict,
    "list": list,
    "set": set,
    "tuple": tuple,
}


def parse_yidl_source(path: str, source: str) -> Tree:
    """Parse one YIDL source string into a Lark tree."""

    parser = _parser()
    try:
        return parser.parse(source)
    except UnexpectedInput as exc:
        raise YidlSyntaxError(
            f"{path}: syntax error at line {exc.line}, column {exc.column}"
        ) from exc


def compile_yidl_files(
    sources: Mapping[str, str],
    entry_path: str,
) -> YidlCompiledModule:
    """Compile an entry source and its imports into recorded concept plans."""

    compiler = _YidlCompiler(sources)
    return compiler.compile(entry_path)


class _YidlCompiler:
    def __init__(self, sources: Mapping[str, str]) -> None:
        self._sources = dict(sources)
        self._cache: dict[str, YidlCompiledModule] = {}
        self._active: set[str] = set()

    def compile(self, path: str) -> YidlCompiledModule:
        resolved_path = posixpath.normpath(path)
        cached = self._cache.get(resolved_path)
        if cached is not None:
            return cached
        if resolved_path in self._active:
            raise YidlSymbolError(f"import cycle involving {resolved_path!r}")
        try:
            source = self._sources[resolved_path]
        except KeyError as exc:
            raise YidlSymbolError(f"missing imported YIDL source {resolved_path!r}") from exc

        self._active.add(resolved_path)
        tree = _file_tree(parse_yidl_source(resolved_path, source))
        imports = self._compile_imports(resolved_path, tree)
        exports = frozenset(self._exports(tree))
        concepts: dict[str, YidlCompiledConcept] = {}
        module_name = self._module_name(tree)
        module = YidlCompiledModule(
            path=resolved_path,
            module_name=module_name,
            concepts=concepts,
            exports=exports,
        )
        for concept_tree in _children(tree, "concept_decl"):
            compiled = _ConceptCompiler(
                module=module,
                imports=imports,
                prior_concepts=concepts,
            ).compile(concept_tree)
            concepts[compiled.name] = compiled
        self._active.remove(resolved_path)
        self._cache[resolved_path] = module
        return module

    def _compile_imports(
        self,
        path: str,
        tree: Tree,
    ) -> dict[str, YidlCompiledModule]:
        imports: dict[str, YidlCompiledModule] = {}
        for import_tree in _children(tree, "import_alias"):
            imported_path = _resolve_import_path(path, _string_value(import_tree.children[0]))
            alias = _token_text(import_tree.children[1])
            imports[alias] = self.compile(imported_path)
        return imports

    def _exports(self, tree: Tree) -> tuple[tuple[str, str], ...]:
        exports: list[tuple[str, str]] = []
        for export_tree in _children(tree, "export_decl"):
            kind = _symbol_kind(export_tree.children[0])
            exports.append((kind, _token_text(export_tree.children[1])))
        return tuple(exports)

    def _module_name(self, tree: Tree) -> str | None:
        module = _first_child(tree, "module_decl")
        if module is None:
            return None
        return _qname(module.children[0])


class _ConceptCompiler:
    def __init__(
        self,
        *,
        module: YidlCompiledModule,
        imports: Mapping[str, YidlCompiledModule],
        prior_concepts: Mapping[str, YidlCompiledConcept],
    ) -> None:
        self._module = module
        self._imports = imports
        self._prior_concepts = prior_concepts
        self._local_properties: dict[str, PropertyHandle] = {}
        self._local_families: dict[str, SchemaFamilyHandle] = {}
        self._local_records: dict[str, RecordHandle] = {}
        self._local_collections: dict[str, CollectionHandle] = {}
        self._local_resources: dict[str, GeneratedValue] = {}
        self._local_matchers: dict[str, MatcherHandle] = {}
        self._local_matcher_inputs: dict[str, frozenset[str]] = {}
        self._local_productions: dict[str, ProductionHandle] = {}
        self._local_operations: dict[str, OperationHandle] = {}
        self._local_contributions: dict[str, ContributionSpec] = {}
        self._local_contribution_matchers: dict[str, ContributionMatcherSpec] = {}
        self._local_composable_productions: dict[str, ComposableProductionSpec] = {}
        self._local_assembly_edges: dict[str, AssemblyEdgeSpec] = {}
        self._local_assemblies: dict[str, AssemblySpec] = {}
        self._declared_contributions: set[str] = set()
        self._declared_composable_productions: set[str] = set()
        self._declared_assembly_edges: set[str] = set()
        self._declared_assemblies: set[str] = set()
        self._extensions: tuple[YidlCompiledConcept, ...] = ()

    def compile(self, tree: Tree) -> YidlCompiledConcept:
        name = _token_text(tree.children[0])
        extends_tree = _first_child(tree, "extends_clause")
        self._extensions = (
            tuple(self._resolve_concept(_qname(child)) for child in extends_tree.children)
            if extends_tree is not None
            else ()
        )
        builder = capsule_concept(
            name,
            extends=tuple(extension.plan for extension in self._extensions),
        )
        members = _concept_members(tree)
        for member in members:
            self._compile_base_member(builder, member)
        self._declare_update_a_members(members)
        for member in members:
            if member.data == "matcher_decl" and _matcher_kind(member) == "resource":
                matcher = self._compile_matcher(builder, member)
                self._local_matchers[matcher.name] = matcher
        for member in members:
            if member.data == "matcher_decl" and _matcher_kind(member) == "contribution":
                matcher = self._compile_contribution_matcher(member)
                self._local_contribution_matchers[matcher.name] = matcher
        for member in members:
            if member.data == "production_decl":
                production = self._compile_production(builder, member)
                self._local_productions[production.name] = production
        for member in members:
            if member.data == "composable_production_decl":
                production = self._compile_composable_production(member)
                self._local_composable_productions[production.name] = production
        for member in members:
            if member.data == "contribution_decl":
                contribution = self._compile_contribution(member)
                self._local_contributions[contribution.name] = contribution
        for member in members:
            if member.data == "assemble_decl":
                edge = self._compile_assembly_edge(member)
                self._local_assembly_edges[edge.name] = edge
        for member in members:
            if member.data == "assembly_decl":
                assembly = self._compile_assembly(member)
                self._local_assemblies[assembly.name] = assembly
        for member in members:
            if member.data == "operation_decl":
                operation = self._compile_operation(builder, member)
                self._local_operations[operation.name] = operation
            elif member.data in {
                "use_decl",
                "union_decl",
                "computed_collection_decl",
                "port_decl",
                "diagnostics_decl",
            }:
                raise YidlSymbolError(f"{member.data} lowering is not implemented yet")
        plan = builder.build()
        self._validate_assembly_value_contexts(plan)
        self._validate_static_assembly_scopes()
        return YidlCompiledConcept(
            name=name,
            plan=plan,
            properties=dict(self._local_properties),
            families=dict(self._local_families),
            records=dict(self._local_records),
            collections=dict(self._local_collections),
            resources=dict(self._local_resources),
            matchers=dict(self._local_matchers),
            productions=dict(self._local_productions),
            operations=dict(self._local_operations),
            contributions=dict(self._local_contributions),
            contribution_matchers=dict(self._local_contribution_matchers),
            composable_productions=dict(self._local_composable_productions),
            assembly_edges=dict(self._local_assembly_edges),
            assemblies=dict(self._local_assemblies),
        )

    def _compile_base_member(self, builder: Any, member: Tree) -> None:
        data = member.data
        if data == "property_decl":
            prop = self._compile_property(builder, member)
            self._local_properties[prop.name] = prop
            return
        if data == "family_decl":
            self._compile_family(builder, member)
            return
        if data == "record_decl":
            record = self._compile_record(builder, member)
            self._local_records[record.name] = record
            return
        if data == "collection_decl":
            collection = self._compile_collection(builder, member)
            self._local_collections[collection.name] = collection
            return
        if data == "resource_decl":
            name, resource = self._compile_resource(member)
            self._local_resources[name] = resource
            return
        if data in {
            "matcher_decl",
            "production_decl",
            "composable_production_decl",
            "contribution_decl",
            "assemble_decl",
            "assembly_decl",
            "operation_decl",
        }:
            return
        if data in {
            "use_decl",
            "union_decl",
            "computed_collection_decl",
            "port_decl",
            "diagnostics_decl",
        }:
            return
        raise YidlSymbolError(f"unsupported concept member {data!r}")

    def _declare_update_a_members(self, members: tuple[Tree, ...]) -> None:
        for member in members:
            if member.data == "contribution_decl":
                name = _token_text(member.children[0])
                if name in self._declared_contributions:
                    raise YidlSymbolError(f"contribution {name!r} is already defined")
                self._declared_contributions.add(name)
            elif member.data == "composable_production_decl":
                name = _token_text(member.children[0])
                if name in self._declared_composable_productions:
                    raise YidlSymbolError(
                        f"composable production {name!r} is already defined"
                    )
                self._declared_composable_productions.add(name)
            elif member.data == "assemble_decl":
                name = _token_text(member.children[0])
                if name in self._declared_assembly_edges:
                    raise YidlSymbolError(f"assembly edge {name!r} is already defined")
                self._declared_assembly_edges.add(name)
            elif member.data == "assembly_decl":
                name = _token_text(member.children[0])
                if name in self._declared_assemblies:
                    raise YidlSymbolError(f"assembly {name!r} is already defined")
                self._declared_assemblies.add(name)

    def _compile_resource(self, tree: Tree) -> tuple[str, GeneratedValue]:
        name = _token_text(tree.children[0])
        if name in self._local_resources:
            raise YidlSymbolError(f"resource {name!r} is already defined")
        expr = tree.children[1]
        if not isinstance(expr, Tree):
            raise YidlSymbolError(f"resource {name!r} has invalid expression")

        try:
            if expr.data == "resource_literal":
                return name, from_literal(self._value(expr.children[0]))
            if expr.data == "resource_import":
                module = _string_value(expr.children[0])
                imported_name = _token_text(expr.children[1])
                return name, from_import(module, imported_name)
            if expr.data in {"resource_code", "resource_astichi_code"}:
                options = self._resource_options(expr, name)
                if options.edge_options:
                    raise YidlSymbolError(
                        f"resource {name!r} code resources do not support edge options"
                    )
                snippet = _snippet_source(expr.children[0])
                return name, from_astichi_code(
                    snippet.source,
                    file_name=self._module.path,
                    line_number=snippet.line_number,
                    offset=snippet.offset,
                    keep_names=options.keep_names,
                )
            if expr.data in {"resource_template", "resource_astichi_template"}:
                options = self._resource_options(expr, name)
                snippet = _snippet_source(expr.children[0])
                template = from_astichi_code(
                    snippet.source,
                    file_name=self._module.path,
                    line_number=snippet.line_number,
                    offset=snippet.offset,
                    keep_names=options.keep_names,
                )
                return name, astichi_template(
                    template,
                    **self._template_edge_options(options, name),
                )
        except YidlSymbolError:
            raise
        except ValueError as exc:
            raise YidlSymbolError(f"resource {name!r}: {exc}") from exc

        raise YidlSymbolError(f"resource {name!r} uses unsupported expression {expr.data!r}")

    def _resource_options(self, tree: Tree, resource_name: str) -> _ResourceOptions:
        options_tree = _first_child(tree, "resource_options")
        if options_tree is None:
            return _ResourceOptions()

        keep_names: list[str] = []
        edge_options: list[Tree] = []
        for option in _children(options_tree, "resource_keep"):
            keep_list = option.children[0]
            if not isinstance(keep_list, Tree):
                raise YidlSymbolError(f"resource {resource_name!r} has invalid keep list")
            keep_names.extend(_token_text(child) for child in keep_list.children)
        edge_options.extend(_children(options_tree, "resource_edge"))
        return _ResourceOptions(
            keep_names=tuple(dict.fromkeys(keep_names)),
            edge_options=tuple(edge_options),
        )

    def _template_edge_options(
        self,
        options: _ResourceOptions,
        resource_name: str,
    ) -> dict[str, MatcherGeneratedValue]:
        result: dict[str, MatcherGeneratedValue] = {}
        for edge in options.edge_options:
            edge_kind = edge.children[0]
            edge_ref = edge.children[1]
            if not isinstance(edge_kind, Tree) or not isinstance(edge_ref, Tree):
                raise YidlSymbolError(f"resource {resource_name!r} has invalid edge")
            key = edge_kind.data.removeprefix("edge_")
            if key in result:
                raise YidlSymbolError(
                    f"resource {resource_name!r} repeats template edge {key!r}"
                )
            target = self._lower_resource_expr(
                edge_ref,
                context=f"resource {resource_name!r} template edge {key!r}",
            )
            if not isinstance(target, MatcherGeneratedValue):
                target_name = _resource_expr_name(edge_ref)
                raise YidlSymbolError(
                    f"resource {resource_name!r} edge {key!r} target "
                    f"{target_name!r} must be a code resource"
                )
            result[key] = target
        return result

    def _lower_resource_expr(
        self,
        tree: Tree,
        *,
        context: str,
        allow_match_resource: bool = False,
    ) -> GeneratedValue:
        if tree.data in {"resource_ref", "resource_name_ref"}:
            return self._resolve_resource(_qname(tree))
        if tree.data == "resource_match_ref":
            if allow_match_resource:
                raise YidlSymbolError(
                    f"{context} match.resource() resource flow is not lowered yet"
                )
            raise YidlSymbolError(
                f"{context} cannot use match.resource() without a matcher-result context"
            )
        raise YidlSymbolError(
            f"{context} uses unsupported resource expression {tree.data!r}"
        )

    def _compile_property(self, builder: Any, tree: Tree) -> PropertyHandle:
        name = _token_text(tree.children[0])
        self._reject_imported_property_redefinition(name)
        value_type = self._type_value(tree.children[1])
        default = REQUIRED
        storage_name: str | None = None
        for child in tree.children[2:]:
            if not isinstance(child, Tree):
                continue
            if child.data == "default_clause":
                default = self._value(child.children[0])
            elif child.data == "storage_clause":
                storage_name = _token_text(child.children[0])
        return getattr(builder.props, name)(
            value_type,
            default,
            storage_name=storage_name,
        )

    def _compile_family(self, builder: Any, tree: Tree) -> None:
        family_name = _qname(tree.children[0])
        if "." in family_name:
            family, owner = self._resolve_family(family_name)
            editor = builder.extend_schema_family(family)
        else:
            editor = builder.schema_family(family_name)
            self._local_families[family_name] = editor.handle
            owner = None
        for raw_member in tree.children[1:]:
            member = (
                raw_member.children[0]
                if isinstance(raw_member, Tree) and raw_member.data == "family_member"
                else raw_member
            )
            if member.data == "family_common":
                editor.common(
                    *(self._resolve_property(_qname(child)) for child in member.children)
                )
                continue
            if member.data != "variant_decl":
                continue
            variant_name = _token_text(member.children[0])
            variant = editor.variant(
                variant_name,
                *(
                    self._resolve_property_for_family_variant(_qname(child), owner)
                    for child in member.children[1:]
                ),
            )
            self._local_records[variant.name] = variant

    def _compile_record(self, builder: Any, tree: Tree) -> RecordHandle:
        name = _token_text(tree.children[0])
        try:
            return getattr(builder.records, name)(
                *(self._resolve_property(_qname(child)) for child in tree.children[1:])
            )
        except ValueError as exc:
            raise YidlSymbolError(str(exc)) from exc

    def _compile_collection(self, builder: Any, tree: Tree) -> CollectionHandle:
        name = _token_text(tree.children[0])
        record_shape = self._resolve_record_shape(_qname(tree.children[1].children[0]))
        identity: PropertyHandle | None = None
        cardinality = builder.many
        for child in tree.children[2:]:
            if child.data == "identity_clause":
                identity = self._resolve_property(_first_qname(child))
            elif child.data == "cardinality_single":
                cardinality = builder.single
            elif child.data == "cardinality_many":
                cardinality = builder.many
        return getattr(builder.collections, name)(
            record_shape,
            cardinality=cardinality,
            identity=identity,
        )

    def _compile_matcher(self, builder: Any, tree: Tree) -> MatcherHandle:
        name = _token_text(tree.children[0])
        if name in self._local_matchers or name in self._local_contribution_matchers:
            raise YidlSymbolError(f"matcher {name!r} is already defined")
        editor = getattr(builder.matchers, name)()
        inputs: dict[str, MatcherInputHandle] = {}

        input_list = _first_child(tree, "matcher_input_list")
        if input_list is not None:
            for input_tree in input_list.children:
                if not isinstance(input_tree, Tree) or input_tree.data != "matcher_input":
                    continue
                input_name = _token_text(input_tree.children[0])
                source = self._resolve_collection(_qname(input_tree.children[1]))
                inputs[input_name] = getattr(editor.input, input_name)(source)
        self._local_matcher_inputs[name] = frozenset(inputs)

        for child in tree.children[1:]:
            if not isinstance(child, Tree):
                continue
            if child.data == "matcher_default":
                editor.default(
                    self._lower_resource_expr(
                        child.children[0],
                        context=f"matcher {name!r} default",
                    )
                )
                continue
            if child.data == "matcher_rule":
                rule_name = _token_text(child.children[0])
                conditions = self._matcher_conditions(child.children[1], inputs)
                resource = self._lower_resource_expr(
                    child.children[2],
                    context=f"matcher {name!r} rule {rule_name!r}",
                )
                weight = 1.0
                weight_tree = _first_child(child, "weight_clause")
                if weight_tree is not None:
                    weight = float(str(weight_tree.children[0]))
                getattr(editor.rule, rule_name)(
                    when=conditions,
                    resource=resource,
                    weight=weight,
                )
        return editor.handle

    def _compile_contribution_matcher(self, tree: Tree) -> ContributionMatcherSpec:
        name = _token_text(tree.children[0])
        if name in self._local_matchers or name in self._local_contribution_matchers:
            raise YidlSymbolError(f"matcher {name!r} is already defined")

        inputs = self._assembly_inputs(_first_child(tree, "matcher_input_list"))
        default_name: str | None = None
        rules: list[ContributionRuleSpec] = []
        for child in tree.children[1:]:
            if not isinstance(child, Tree):
                continue
            if child.data == "matcher_default":
                default_name = self._resolve_contribution_ref(
                    child.children[0],
                    context=f"matcher {name!r} default",
                )
                continue
            if child.data == "matcher_rule":
                rule_name = _token_text(child.children[0])
                condition = self._assembly_condition(child.children[1])
                contribution_name = self._resolve_contribution_ref(
                    child.children[2],
                    context=f"matcher {name!r} rule {rule_name!r}",
                )
                weight = 1.0
                weight_tree = _first_child(child, "weight_clause")
                if weight_tree is not None:
                    weight = float(str(weight_tree.children[0]))
                rules.append(
                    ContributionRuleSpec(
                        name=rule_name,
                        condition=condition,
                        contribution_name=contribution_name,
                        weight=weight,
                    )
                )
        return ContributionMatcherSpec(
            name=name,
            inputs=inputs,
            default_contribution_name=default_name,
            rules=tuple(rules),
        )

    def _matcher_conditions(
        self,
        tree: Tree,
        inputs: Mapping[str, MatcherInputHandle],
    ) -> tuple[Any, ...]:
        if tree.data == "condition_and":
            return (
                *self._matcher_conditions(tree.children[0], inputs),
                *self._matcher_conditions(tree.children[1], inputs),
            )
        if tree.data == "condition_term":
            left = tree.children[0]
            right = tree.children[1]
            left_ref = self._matcher_property_ref(left, inputs)
            right_ref = self._matcher_property_ref(right, inputs)
            if left_ref is not None and right_ref is None:
                return (left_ref.eq(self._value(right)),)
            if right_ref is not None and left_ref is None:
                return (right_ref.eq(self._value(left)),)
            raise YidlSymbolError("matcher conditions must compare one input property")
        raise YidlSymbolError(f"unsupported matcher condition {tree.data!r}")

    def _matcher_property_ref(
        self,
        node: object,
        inputs: Mapping[str, MatcherInputHandle],
    ) -> Any | None:
        if not isinstance(node, Tree) or node.data != "qname" or len(node.children) != 2:
            return None
        input_name = _token_text(node.children[0])
        input_handle = inputs.get(input_name)
        if input_handle is None:
            raise YidlSymbolError(f"undefined matcher input {input_name!r}")
        property_name = _token_text(node.children[1])
        return input_handle.prop(self._resolve_property(property_name))

    def _compile_production(self, builder: Any, tree: Tree) -> ProductionHandle:
        name = _token_text(tree.children[0])
        if name in self._local_productions:
            raise YidlSymbolError(f"production {name!r} is already defined")
        source, matcher_inputs = self._production_source(tree.children[1])
        target = self._resolve_collection(_qname(tree.children[2]))
        identity: Any | None = None
        values: dict[PropertyHandle, Any] = {}
        policy = RejectDuplicate

        for member in tree.children[3:]:
            if not isinstance(member, Tree) or member.data != "production_member":
                continue
            if len(member.children) == 1:
                child = member.children[0]
                if isinstance(child, Tree) and child.data == "qname":
                    policy = self._policy(_qname(child))
                else:
                    identity = self._production_value(child, matcher_inputs)
                continue
            if len(member.children) == 2:
                prop = self._resolve_property(_qname(member.children[0]))
                values[prop] = self._production_value(member.children[1], matcher_inputs)
                continue
            raise YidlSymbolError(f"production {name!r} has invalid member")

        return getattr(builder.productions, name)(
            source=source,
            target=target,
            values=values,
            policy=policy,
            identity=identity,
        ).handle

    def _production_source(
        self,
        tree: object,
    ) -> tuple[CollectionHandle | MatcherResultSourceHandle, frozenset[str] | None]:
        if not isinstance(tree, Tree):
            raise YidlSymbolError("production source is invalid")
        if tree.data == "matcher_results_source":
            matcher_name = _token_text(tree.children[0])
            matcher = self._resolve_matcher(matcher_name)
            return (
                MatcherResultSourceHandle(matcher),
                self._local_matcher_inputs.get(matcher_name, frozenset()),
            )
        if tree.data == "collection_source":
            return self._resolve_collection(_qname(tree.children[0])), None
        raise YidlSymbolError(f"unsupported production source {tree.data!r}")

    def _production_value(
        self,
        node: object,
        matcher_inputs: frozenset[str] | None,
    ) -> Any:
        if isinstance(node, Token | Tree):
            if isinstance(node, Tree):
                if node.data == "literal_expr":
                    return self._value(node)
                if node.data == "qname":
                    return self._value(node)
                if node.data == "match_resource":
                    if matcher_inputs is None:
                        raise YidlSymbolError(
                            "match.resource() requires a matcher-result production source"
                        )
                    return recorded_match.resource()
                if node.data == "match_record":
                    if matcher_inputs is None:
                        raise YidlSymbolError(
                            "match.record(...) requires a matcher-result production source"
                        )
                    input_name = _string_value(node.children[0])
                    if input_name not in matcher_inputs:
                        raise YidlSymbolError(f"undefined matcher input {input_name!r}")
                    return recorded_match.record(input_name).prop(
                        self._resolve_property(_qname(node.children[1]))
                    )
            return self._value(node)
        raise YidlSymbolError("unsupported production value expression")

    def _compile_contribution(self, tree: Tree) -> ContributionSpec:
        name = _token_text(tree.children[0])
        if name in self._local_contributions:
            raise YidlSymbolError(f"contribution {name!r} is already defined")

        source_name: str | None = None
        source_kind: str | None = None
        source_tree = _first_child(tree, "contribution_source")
        if source_tree is not None:
            source_name, source_kind = self._contribution_source(
                source_tree.children[0],
                context=f"contribution {name!r} source",
            )
        build_name = name
        index: AssemblyValueRef | None = None
        order: AssemblyValueRef | None = None
        target: TargetSpec | None = None
        bindings: list[BindingSpec] = []
        seen_bindings: set[tuple[str, str]] = set()
        seen_as = False
        diagnostic_message: str | None = None

        for member in _wrapped_children(tree, "contribution_member"):
            if member.data == "contribution_as":
                if seen_as:
                    raise YidlSymbolError(f"contribution {name!r} repeats as")
                seen_as = True
                build_name = _token_text(member.children[0])
                continue
            if member.data == "contribution_index":
                if index is not None:
                    raise YidlSymbolError(f"contribution {name!r} repeats index")
                index = self._assembly_value(member.children[0])
                continue
            if member.data == "contribution_order":
                if order is not None:
                    raise YidlSymbolError(f"contribution {name!r} repeats order")
                order = self._assembly_value(member.children[0])
                continue
            if member.data == "target_decl":
                if target is not None:
                    raise YidlSymbolError(f"contribution {name!r} repeats target")
                target = self._target_spec(member, context=f"contribution {name!r}")
                continue
            if member.data == "bind_decl":
                binding = self._binding_spec(
                    member,
                    context=f"contribution {name!r}",
                )
                binding_key = (binding.kind, binding.name)
                if binding_key in seen_bindings:
                    raise YidlSymbolError(
                        f"contribution {name!r} repeats {binding.kind} "
                        f"binding {binding.name!r}"
                    )
                seen_bindings.add(binding_key)
                bindings.append(binding)
                continue
            if member.data == "contribution_diagnostic":
                if diagnostic_message is not None:
                    raise YidlSymbolError(f"contribution {name!r} repeats diagnostic")
                diagnostic_message = _string_value(member.children[0])
                continue
            raise YidlSymbolError(
                f"contribution {name!r} has invalid member {member.data!r}"
            )

        if diagnostic_message is not None:
            if source_name is not None:
                raise YidlSymbolError(
                    f"diagnostic contribution {name!r} must not declare a source"
                )
            if target is not None:
                raise YidlSymbolError(
                    f"diagnostic contribution {name!r} must not declare a target"
                )
            source_name = ""
            source_kind = "diagnostic"
        else:
            if source_name is None or source_kind is None:
                raise YidlSymbolError(f"contribution {name!r} must declare a source")
            if target is None:
                raise YidlSymbolError(
                    f"contribution {name!r} must declare exactly one target"
                )

        return ContributionSpec(
            name=name,
            source_name=source_name,
            source_kind=source_kind,  # type: ignore[arg-type]
            build_name=build_name,
            index=index,
            order=order,
            target=target,
            bindings=tuple(bindings),
            diagnostic_message=diagnostic_message,
        )

    def _compile_composable_production(
        self,
        tree: Tree,
    ) -> ComposableProductionSpec:
        name = _token_text(tree.children[0])
        if name in self._local_composable_productions or name in self._local_productions:
            raise YidlSymbolError(f"production {name!r} is already defined")

        inputs_tree = _first_child(tree, "composable_production_inputs")
        inputs = self._assembly_inputs(
            _first_child(inputs_tree, "matcher_input_list")
            if inputs_tree is not None
            else None
        )
        root: RootSpec | None = None
        applies: list[ApplySpec] = []
        for member in _wrapped_children(tree, "composable_production_member"):
            if member.data == "root_decl":
                if root is not None:
                    raise YidlSymbolError(f"production {name!r} repeats root")
                root = self._root_spec(member, context=f"production {name!r}")
                continue
            if member.data == "apply_decl":
                apply_spec = self._apply_spec(name, inputs, member)
                if isinstance(apply_spec, InlineApplySpec):
                    if apply_spec.edge.name in self._local_assembly_edges:
                        raise YidlSymbolError(
                            f"assembly edge {apply_spec.edge.name!r} is already defined"
                        )
                    self._local_assembly_edges[apply_spec.edge.name] = apply_spec.edge
                applies.append(apply_spec)
                continue
            raise YidlSymbolError(
                f"production {name!r} has invalid member {member.data!r}"
            )

        if root is None:
            raise YidlSymbolError(f"production {name!r} must declare a root")

        return ComposableProductionSpec(
            name=name,
            inputs=inputs,
            root=root,
            applies=tuple(applies),
        )

    def _compile_assembly_edge(self, tree: Tree) -> AssemblyEdgeSpec:
        name = _token_text(tree.children[0])
        if name in self._local_assembly_edges:
            raise YidlSymbolError(f"assembly edge {name!r} is already defined")
        context_tree = _first_child(tree, "assemble_context")
        context_inputs = self._assembly_inputs(
            _first_child(context_tree, "matcher_input_list")
            if context_tree is not None
            else None
        )
        return self._edge_spec(
            name,
            context_inputs=context_inputs,
            tail_children=tree.children[1:],
            context=f"assemble {name!r}",
        )

    def _compile_assembly(self, tree: Tree) -> AssemblySpec:
        name = _token_text(tree.children[0])
        if name in self._local_assemblies:
            raise YidlSymbolError(f"assembly {name!r} is already defined")
        production_name = _qname(tree.children[1])
        production = self._local_composable_productions.get(production_name)
        if production is None:
            if production_name in self._local_productions:
                raise YidlSymbolError(
                    f"assembly {name!r} target {production_name!r} is a data "
                    "production, not a composable production"
                )
            raise YidlSymbolError(
                f"assembly {name!r} references undefined composable production "
                f"{production_name!r}"
            )
        if production.inputs:
            raise YidlSymbolError(
                f"assembly {name!r} root production {production_name!r} "
                "must not declare inputs"
            )
        return AssemblySpec(name=name, production_name=production_name)

    def _contribution_source(
        self,
        node: object,
        *,
        context: str,
    ) -> tuple[str, str]:
        if not isinstance(node, Tree):
            raise YidlSymbolError(f"{context} is invalid")
        if node.data == "resource_match_ref":
            raise YidlSymbolError(f"{context} cannot use match.resource()")
        if node.data not in {"resource_ref", "resource_name_ref"}:
            raise YidlSymbolError(f"{context} has unsupported source {node.data!r}")
        name = _qname(node)
        has_resource = self._resource_exists(name)
        has_production = self._composable_production_exists(name)
        if has_resource and has_production:
            raise YidlSymbolError(f"{context} {name!r} is ambiguous")
        if has_resource:
            return name, "resource"
        if has_production:
            return name, "production"
        raise YidlSymbolError(f"{context} references undefined source {name!r}")

    def _target_spec(self, tree: Tree, *, context: str) -> TargetSpec:
        paths: list[TargetPathSpec] = []
        for child in tree.children[1:]:
            if not isinstance(child, Tree):
                continue
            if child.data == "target_build":
                paths.append(TargetPathSpec(kind="build", path=self._path_spec(child.children[0])))
                continue
            if child.data == "target_owner":
                paths.append(TargetPathSpec(kind="owner", path=self._path_spec(child.children[0])))
                continue
            raise YidlSymbolError(f"{context} has invalid target option {child.data!r}")
        return TargetSpec(name=_token_text(tree.children[0]), paths=tuple(paths))

    def _path_spec(self, tree: Tree) -> PathSpec:
        segments: list[PathSegmentSpec] = []
        for child in tree.children:
            if not isinstance(child, Tree):
                continue
            if child.data == "path_segment":
                indexes = tuple(
                    self._assembly_value(index_child)
                    for index in _children(child, "path_index")
                    for index_child in index.children
                )
                segments.append(
                    PathSegmentSpec(
                        kind="name",
                        name=_token_text(child.children[0]),
                        indexes=indexes,
                    )
                )
                continue
            operator_kind = {
                "path_current": "current",
                "path_optional": "optional",
                "path_any": "any",
                "path_many": "many",
            }.get(child.data)
            if operator_kind is None:
                raise YidlSymbolError(f"invalid path segment {child.data!r}")
            segments.append(PathSegmentSpec(kind=operator_kind))
        return PathSpec(segments=tuple(segments))

    def _root_spec(self, tree: Tree, *, context: str) -> RootSpec:
        resource_expr = tree.children[1]
        if not isinstance(resource_expr, Tree):
            raise YidlSymbolError(f"{context} root has invalid resource")
        self._lower_resource_expr(resource_expr, context=f"{context} root")
        bindings: list[BindingSpec] = []
        options = _first_child(tree, "root_options")
        if options is not None:
            for bind in _children(options, "bind_decl"):
                bindings.append(self._binding_spec(bind, context=f"{context} root"))
        return RootSpec(
            build_name=_token_text(tree.children[0]),
            resource_name=_resource_expr_name(resource_expr),
            bindings=tuple(bindings),
        )

    def _apply_spec(
        self,
        production_name: str,
        context_inputs: tuple[AssemblyInputSpec, ...],
        tree: Tree,
    ) -> ApplySpec:
        apply_name = _token_text(tree.children[0])
        tail = _first_child(tree, "apply_tail")
        if tail is None:
            return EdgeApplySpec(edge_name=apply_name)
        edge = self._edge_spec(
            f"{production_name}.{apply_name}",
            context_inputs=context_inputs,
            tail_children=tail.children,
            context=f"apply {apply_name!r}",
        )
        return InlineApplySpec(edge=edge)

    def _edge_spec(
        self,
        name: str,
        *,
        context_inputs: tuple[AssemblyInputSpec, ...],
        tail_children: list[object],
        context: str,
    ) -> AssemblyEdgeSpec:
        from_inputs: tuple[AssemblyInputSpec, ...] = ()
        condition: AssemblyConditionSpec | None = None
        matcher_name: str | None = None
        for child in tail_children:
            if isinstance(child, Tree) and child.data == "assemble_from":
                from_inputs = self._assembly_inputs(_first_child(child, "matcher_input_list"))
                continue
            if isinstance(child, Tree) and child.data == "where_clause":
                condition = self._assembly_condition(child.children[0])
                continue
            if isinstance(child, Token):
                matcher_name = str(child)
        if matcher_name is None:
            raise YidlSymbolError(f"{context} must name a matcher")
        self._resolve_contribution_matcher_name(matcher_name, context=context)
        return AssemblyEdgeSpec(
            name=name,
            context_inputs=context_inputs,
            from_inputs=from_inputs,
            condition=condition,
            matcher_name=matcher_name,
        )

    def _binding_spec(self, tree: Tree, *, context: str) -> BindingSpec:
        kind_tree = tree.children[0]
        if not isinstance(kind_tree, Tree):
            raise YidlSymbolError(f"{context} has invalid binding")
        kind = kind_tree.data.removeprefix("bind_")
        if kind not in {"ident", "external"}:
            raise YidlSymbolError(f"{context} has invalid binding kind {kind!r}")
        return BindingSpec(
            kind=kind,  # type: ignore[arg-type]
            name=_token_text(tree.children[1]),
            value=self._assembly_value(tree.children[2]),
        )

    def _assembly_inputs(self, input_list: Tree | None) -> tuple[AssemblyInputSpec, ...]:
        if input_list is None:
            return ()
        inputs: list[AssemblyInputSpec] = []
        for input_tree in input_list.children:
            if not isinstance(input_tree, Tree) or input_tree.data != "matcher_input":
                continue
            collection_name = _qname(input_tree.children[1])
            inputs.append(
                AssemblyInputSpec(
                    name=_token_text(input_tree.children[0]),
                    collection_name=collection_name,
                    collection=self._resolve_collection(collection_name),
                )
            )
        return tuple(inputs)

    def _assembly_condition(self, tree: Tree) -> AssemblyConditionSpec:
        if tree.data == "condition_and":
            left = self._assembly_condition(tree.children[0])
            right = self._assembly_condition(tree.children[1])
            items: list[AssemblyConditionSpec] = []
            for condition in (left, right):
                if isinstance(condition, AndConditionSpec):
                    items.extend(condition.items)
                else:
                    items.append(condition)
            return AndConditionSpec(items=tuple(items))
        if tree.data == "condition_term":
            return EqConditionSpec(
                left=self._assembly_value(tree.children[0]),
                right=self._assembly_value(tree.children[1]),
            )
        raise YidlSymbolError(f"unsupported assembly condition {tree.data!r}")

    def _assembly_value(self, node: object) -> AssemblyValueRef:
        if isinstance(node, Token) and node.type == "CNAME":
            return ValueRef(str(node))
        if not isinstance(node, Tree):
            raise YidlSymbolError("unsupported assembly value expression")
        if node.data in {"literal_expr", "true", "false", "none"}:
            return LiteralValueRef(self._value(node))
        if node.data == "contribution_value_name":
            return ValueRef(_token_text(node.children[0]))
        if node.data == "qname":
            name = _qname(node)
            if len(node.children) != 1:
                raise YidlSymbolError(
                    f"qualified value reference {name!r} is not supported "
                    "in assembly values"
                )
            return ValueRef(name)
        if node.data in {
            "contribution_tuple_expr",
            "tuple_empty",
            "tuple_single",
            "tuple_multi",
        }:
            return TupleValueRef(
                items=tuple(self._assembly_value(child) for child in node.children)
            )
        raise YidlSymbolError(
            f"unsupported assembly value expression {node.data!r}"
        )

    def _resolve_contribution_ref(self, tree: Tree, *, context: str) -> str:
        if tree.data == "resource_match_ref":
            raise YidlSymbolError(f"{context} cannot use match.resource()")
        if tree.data not in {"resource_ref", "resource_name_ref"}:
            raise YidlSymbolError(
                f"{context} has unsupported contribution expression {tree.data!r}"
            )
        name = _qname(tree)
        return self._resolve_contribution_name(name, context=context)

    def _resolve_contribution_name(self, name: str, *, context: str) -> str:
        if self._contribution_exists(name):
            return name
        if self._resource_exists(name):
            raise YidlSymbolError(f"{context} {name!r} is a resource, not a contribution")
        raise YidlSymbolError(f"{context} references undefined contribution {name!r}")

    def _resolve_contribution_matcher_name(self, name: str, *, context: str) -> str:
        if name in self._local_contribution_matchers:
            return name
        if name in self._local_matchers:
            raise YidlSymbolError(f"{context} {name!r} is a resource matcher")
        raise YidlSymbolError(f"{context} references undefined contribution matcher {name!r}")

    def _resource_exists(self, name: str) -> bool:
        try:
            self._resolve_resource(name)
        except YidlSymbolError:
            return False
        return True

    def _contribution_exists(self, name: str) -> bool:
        parts = name.split(".")
        if len(parts) == 1:
            if parts[0] in self._declared_contributions:
                return True
            return any(parts[0] in extension.contributions for extension in self._extensions)
        if len(parts) == 2:
            module = self._import_module(parts[0])
            return any(parts[1] in concept.contributions for concept in module.concepts.values())
        return False

    def _composable_production_exists(self, name: str) -> bool:
        parts = name.split(".")
        if len(parts) == 1:
            if parts[0] in self._declared_composable_productions:
                return True
            return any(
                parts[0] in extension.composable_productions
                for extension in self._extensions
            )
        if len(parts) == 2:
            module = self._import_module(parts[0])
            return any(
                parts[1] in concept.composable_productions
                for concept in module.concepts.values()
            )
        return False

    def _validate_assembly_value_contexts(self, plan: CapsuleConceptPlan) -> None:
        for matcher in self._local_contribution_matchers.values():
            names = self._value_names_for_inputs(
                plan,
                matcher.inputs,
                context=f"matcher {matcher.name!r}",
            )
            for rule in matcher.rules:
                self._validate_condition_names(
                    rule.condition,
                    names,
                    context=f"matcher {matcher.name!r} rule {rule.name!r}",
                )

        for production in self._local_composable_productions.values():
            production_names = self._value_names_for_inputs(
                plan,
                production.inputs,
                context=f"production {production.name!r}",
            )
            for binding in production.root.bindings:
                self._validate_value_names(
                    binding.value,
                    production_names,
                    context=f"production {production.name!r} root",
                )
            for apply in production.applies:
                if isinstance(apply, EdgeApplySpec):
                    if apply.edge_name not in self._local_assembly_edges:
                        raise YidlSymbolError(
                            f"production {production.name!r} apply references "
                            f"undefined assembly edge {apply.edge_name!r}"
                        )

        for edge in self._local_assembly_edges.values():
            names = self._value_names_for_inputs(
                plan,
                (*edge.context_inputs, *edge.from_inputs),
                context=f"assembly edge {edge.name!r}",
            )
            if edge.condition is not None:
                self._validate_condition_names(
                    edge.condition,
                    names,
                    context=f"assembly edge {edge.name!r}",
                )
            matcher = self._local_contribution_matchers[edge.matcher_name]
            for contribution_name in _matcher_contribution_names(matcher):
                contribution = self._resolve_contribution_spec(contribution_name)
                self._validate_contribution_names(
                    contribution,
                    names,
                    context=(
                        f"contribution {contribution.name!r} selected by "
                        f"assembly edge {edge.name!r}"
                    ),
                )

    def _validate_contribution_names(
        self,
        contribution: ContributionSpec,
        names: frozenset[str],
        *,
        context: str,
    ) -> None:
        if contribution.index is not None:
            self._validate_value_names(contribution.index, names, context=context)
        if contribution.order is not None:
            self._validate_value_names(contribution.order, names, context=context)
        if contribution.target is not None:
            for target_path in contribution.target.paths:
                for segment in target_path.path.segments:
                    for index in segment.indexes:
                        self._validate_value_names(index, names, context=context)
        for binding in contribution.bindings:
            self._validate_value_names(binding.value, names, context=context)

    def _validate_condition_names(
        self,
        condition: AssemblyConditionSpec,
        names: frozenset[str],
        *,
        context: str,
    ) -> None:
        if isinstance(condition, AndConditionSpec):
            for item in condition.items:
                self._validate_condition_names(item, names, context=context)
            return
        if isinstance(condition, EqConditionSpec):
            self._validate_value_names(condition.left, names, context=context)
            self._validate_value_names(condition.right, names, context=context)
            return
        raise YidlSymbolError(f"{context} has unsupported condition")

    def _validate_value_names(
        self,
        value: AssemblyValueRef,
        names: frozenset[str],
        *,
        context: str,
    ) -> None:
        if isinstance(value, ValueRef):
            if value.name not in names:
                raise YidlSymbolError(
                    f"{context} references undefined value {value.name!r}"
                )
            return
        if isinstance(value, LiteralValueRef):
            return
        if isinstance(value, TupleValueRef):
            for item in value.items:
                self._validate_value_names(item, names, context=context)
            return
        raise YidlSymbolError(f"{context} has unsupported value")

    def _value_names_for_inputs(
        self,
        plan: CapsuleConceptPlan,
        inputs: tuple[AssemblyInputSpec, ...],
        *,
        context: str,
    ) -> frozenset[str]:
        names: dict[str, str] = {}
        for input_spec in inputs:
            for prop_name in self._collection_property_names(plan, input_spec.collection):
                owner = names.get(prop_name)
                if owner is not None:
                    raise YidlSymbolError(
                        f"{context} has duplicate visible value {prop_name!r} "
                        f"from inputs {owner!r} and {input_spec.name!r}"
                    )
                names[prop_name] = input_spec.name
        return frozenset(names)

    def _collection_property_names(
        self,
        plan: CapsuleConceptPlan,
        collection: object,
    ) -> tuple[str, ...]:
        if not isinstance(collection, CollectionHandle):
            raise YidlSymbolError("assembly inputs must reference collections")
        record = collection.record
        if isinstance(record, RecordHandle):
            return tuple(prop.name for prop in record.properties)
        if isinstance(record, SchemaFamilyHandle):
            family_plan = _plan_for_owner(plan, record.owner_id)
            properties: dict[str, None] = {}
            for operation in family_plan.schema_family_common:
                if operation.family == record:
                    for prop in operation.properties:
                        properties.setdefault(prop.name, None)
            for operation in family_plan.schema_family_variants:
                if operation.family == record:
                    for prop in operation.record.properties:
                        properties.setdefault(prop.name, None)
            return tuple(properties)
        raise YidlSymbolError("unsupported assembly input record shape")

    def _resolve_contribution_spec(self, name: str) -> ContributionSpec:
        contribution = self._local_contributions.get(name)
        if contribution is not None:
            return contribution
        for extension in self._extensions:
            contribution = extension.contributions.get(name)
            if contribution is not None:
                return contribution
        raise YidlSymbolError(f"undefined contribution {name!r}")

    def _validate_static_assembly_scopes(self) -> None:
        validated: set[str] = set()
        for production in self._local_composable_productions.values():
            self._validate_static_scope(production, visiting=set(), validated=validated)

    def _validate_static_scope(
        self,
        production: ComposableProductionSpec,
        *,
        visiting: set[str],
        validated: set[str],
    ) -> None:
        if production.name in validated:
            return
        if production.name in visiting:
            raise YidlSymbolError(
                f"composable production cycle involving {production.name!r}"
            )
        visiting.add(production.name)

        root_holes = self._resource_hole_names(
            production.root.resource_name,
            context=f"production {production.name!r} root",
        )
        path_holes: dict[tuple[str, ...], frozenset[str]] = {
            (production.root.build_name,): root_holes,
        }

        for apply in production.applies:
            edge = (
                apply.edge
                if isinstance(apply, InlineApplySpec)
                else self._local_assembly_edges[apply.edge_name]
            )
            matcher = self._local_contribution_matchers[edge.matcher_name]
            for contribution_name in _matcher_contribution_names(matcher):
                contribution = self._resolve_contribution_spec(contribution_name)
                if contribution.source_kind == "production":
                    source = self._local_composable_productions.get(
                        contribution.source_name
                    )
                    if source is not None:
                        self._validate_static_scope(
                            source,
                            visiting=visiting,
                            validated=validated,
                        )
                self._validate_static_contribution(
                    contribution,
                    path_holes,
                    context=(
                        f"contribution {contribution.name!r} selected by "
                        f"apply {edge.name!r}"
                    ),
                )

        visiting.remove(production.name)
        validated.add(production.name)

    def _validate_static_contribution(
        self,
        contribution: ContributionSpec,
        path_holes: dict[tuple[str, ...], frozenset[str]],
        *,
        context: str,
    ) -> None:
        concrete_build_paths: list[tuple[str, ...]] = []
        if contribution.target is None:
            return
        for target_path in contribution.target.paths:
            parts, dynamic = _static_path_parts(target_path.path)
            if dynamic:
                if parts and parts not in path_holes:
                    raise YidlSymbolError(
                        f"{context} references unreachable path /{'/'.join(parts)}"
                    )
                continue
            if parts not in path_holes:
                raise YidlSymbolError(
                    f"{context} references unreachable path /{'/'.join(parts)}"
                )
            if target_path.kind == "build":
                if contribution.target.name not in path_holes[parts]:
                    raise YidlSymbolError(
                        f"{context} target {contribution.target.name!r} is not "
                        f"available at /{'/'.join(parts)}"
                    )
                concrete_build_paths.append(parts)

        source_holes = self._contribution_source_hole_names(contribution)
        for build_path in concrete_build_paths:
            path_holes[build_path + (contribution.build_name,)] = source_holes

    def _contribution_source_hole_names(
        self,
        contribution: ContributionSpec,
    ) -> frozenset[str]:
        if contribution.source_kind == "resource":
            return self._resource_hole_names(
                contribution.source_name,
                context=f"contribution {contribution.name!r} source",
            )
        production = self._local_composable_productions.get(contribution.source_name)
        if production is None:
            return frozenset()
        return self._resource_hole_names(
            production.root.resource_name,
            context=f"production {production.name!r} root",
        )

    def _resource_hole_names(self, name: str, *, context: str) -> frozenset[str]:
        resource = self._resolve_resource(name)
        try:
            description = resource.to_generator().describe()
        except Exception as exc:
            raise YidlSymbolError(f"{context} cannot be described: {exc}") from exc
        return frozenset(hole.name for hole in description.holes)

    def _policy(self, name: str) -> object:
        try:
            return _POLICIES[name]
        except KeyError as exc:
            raise YidlSymbolError(f"unsupported production policy {name!r}") from exc

    def _compile_operation(self, builder: Any, tree: Tree) -> OperationHandle:
        name = _token_text(tree.children[0])
        if name in self._local_operations:
            raise YidlSymbolError(f"operation {name!r} is already defined")
        io_tree = tree.children[1]
        if not isinstance(io_tree, Tree) or io_tree.data != "operation_io":
            raise YidlSymbolError(f"operation {name!r} has invalid inputs/outputs")
        qname_lists = [
            child
            for child in io_tree.children
            if isinstance(child, Tree) and child.data == "qname_list"
        ]
        if len(qname_lists) != 2:
            raise YidlSymbolError(
                f"operation {name!r} must declare input and output lists"
            )
        inputs = tuple(
            self._resolve_collection(_qname(child))
            for child in qname_lists[0].children
            if isinstance(child, Tree)
        )
        outputs = tuple(
            self._resolve_collection(_qname(child))
            for child in qname_lists[1].children
            if isinstance(child, Tree)
        )
        resource_expr = tree.children[2]
        if not isinstance(resource_expr, Tree):
            raise YidlSymbolError(f"operation {name!r} has invalid resource")
        resource = self._lower_resource_expr(
            resource_expr,
            context=f"operation {name!r} resource",
        )
        order_by: list[PropertyHandle] = []
        options = _first_child(tree, "operation_options")
        if options is not None:
            for option in options.children:
                if not isinstance(option, Tree) or option.data != "operation_option":
                    continue
                option_value = option.children[0]
                if isinstance(option_value, Tree) and option_value.data == "property_ref":
                    order_by.append(self._resolve_property(_qname(option_value)))
                    continue
                if isinstance(option_value, Tree) and option_value.data == "qname":
                    raise YidlSymbolError(
                        f"operation {name!r} diagnostics option is not implemented yet"
                    )
                raise YidlSymbolError(f"operation {name!r} has invalid option")

        return getattr(builder.operations, name)(
            inputs=inputs,
            outputs=outputs,
            resource=resource,
            order_by=tuple(order_by),
        ).handle

    def _resolve_concept(self, name: str) -> YidlCompiledConcept:
        parts = name.split(".")
        if len(parts) == 1:
            try:
                return self._prior_concepts[parts[0]]
            except KeyError as exc:
                raise YidlSymbolError(f"undefined concept {name!r}") from exc
        if len(parts) == 2:
            module = self._import_module(parts[0])
            try:
                return module.concepts[parts[1]]
            except KeyError as exc:
                raise YidlSymbolError(f"undefined concept {name!r}") from exc
        raise YidlSymbolError(f"unsupported concept reference {name!r}")

    def _resolve_family(
        self,
        name: str,
    ) -> tuple[SchemaFamilyHandle, YidlCompiledConcept | None]:
        parts = name.split(".")
        if len(parts) == 1:
            family = self._local_families.get(parts[0])
            if family is not None:
                return family, None
            for extension in self._extensions:
                family = extension.families.get(parts[0])
                if family is not None:
                    return family, extension
            raise YidlSymbolError(f"undefined schema family {name!r}")
        if len(parts) == 2:
            module = self._import_module(parts[0])
            for concept in module.concepts.values():
                family = concept.families.get(parts[1])
                if family is not None:
                    return family, concept
            raise YidlSymbolError(f"undefined schema family {name!r}")
        raise YidlSymbolError(f"unsupported schema family reference {name!r}")

    def _resolve_record_shape(self, name: str) -> RecordHandle | SchemaFamilyHandle:
        family, _ = self._resolve_family_or_none(name)
        if family is not None:
            return family
        record = self._local_records.get(name)
        if record is not None:
            return record
        for extension in self._extensions:
            record = extension.records.get(name)
            if record is not None:
                return record
        raise YidlSymbolError(f"undefined record or schema family {name!r}")

    def _resolve_collection(self, name: str) -> CollectionHandle:
        parts = name.split(".")
        if len(parts) == 1:
            collection = self._local_collections.get(parts[0])
            if collection is not None:
                return collection
            for extension in self._extensions:
                collection = extension.collections.get(parts[0])
                if collection is not None:
                    return collection
            raise YidlSymbolError(f"undefined collection {name!r}")
        if len(parts) == 2:
            module = self._import_module(parts[0])
            for concept in module.concepts.values():
                collection = concept.collections.get(parts[1])
                if collection is not None:
                    return collection
            raise YidlSymbolError(f"undefined collection {name!r}")
        raise YidlSymbolError(f"unsupported collection reference {name!r}")

    def _resolve_matcher(self, name: str) -> MatcherHandle:
        parts = name.split(".")
        if len(parts) == 1:
            matcher = self._local_matchers.get(parts[0])
            if matcher is not None:
                return matcher
            for extension in self._extensions:
                matcher = extension.matchers.get(parts[0])
                if matcher is not None:
                    return matcher
            raise YidlSymbolError(f"undefined matcher {name!r}")
        if len(parts) == 2:
            module = self._import_module(parts[0])
            for concept in module.concepts.values():
                matcher = concept.matchers.get(parts[1])
                if matcher is not None:
                    return matcher
            raise YidlSymbolError(f"undefined matcher {name!r}")
        raise YidlSymbolError(f"unsupported matcher reference {name!r}")

    def _resolve_family_or_none(
        self,
        name: str,
    ) -> tuple[SchemaFamilyHandle | None, YidlCompiledConcept | None]:
        try:
            return self._resolve_family(name)
        except YidlSymbolError:
            return None, None

    def _resolve_property_for_family_variant(
        self,
        name: str,
        owner: YidlCompiledConcept | None,
    ) -> PropertyHandle:
        if "." in name:
            return self._resolve_property(name)
        local = self._local_properties.get(name)
        if local is not None:
            return local
        if owner is not None:
            prop = owner.properties.get(name)
            if prop is not None:
                return prop
        return self._resolve_property(name)

    def _resolve_property(self, name: str) -> PropertyHandle:
        parts = name.split(".")
        if len(parts) == 1:
            prop = self._local_properties.get(parts[0])
            if prop is not None:
                return prop
            for extension in self._extensions:
                prop = extension.properties.get(parts[0])
                if prop is not None:
                    return prop
            raise YidlSymbolError(f"undefined property {name!r}")
        if len(parts) == 2:
            module = self._import_module(parts[0])
            for concept in module.concepts.values():
                prop = concept.properties.get(parts[1])
                if prop is not None:
                    return prop
            raise YidlSymbolError(f"undefined property {name!r}")
        raise YidlSymbolError(f"unsupported property reference {name!r}")

    def _resolve_resource(self, name: str) -> GeneratedValue:
        parts = name.split(".")
        if len(parts) == 1:
            resource = self._local_resources.get(parts[0])
            if resource is not None:
                return resource
            for extension in self._extensions:
                resource = extension.resources.get(parts[0])
                if resource is not None:
                    return resource
            kind = self._known_local_non_resource_kind(parts[0])
            if kind is not None:
                raise YidlSymbolError(f"{name!r} is a {kind}, not a resource")
            raise YidlSymbolError(f"undefined resource {name!r}")
        if len(parts) == 2:
            module = self._import_module(parts[0])
            for concept in module.concepts.values():
                resource = concept.resources.get(parts[1])
                if resource is not None:
                    return resource
            kind = self._known_imported_non_resource_kind(module, parts[1])
            if kind is not None:
                raise YidlSymbolError(f"{name!r} is a {kind}, not a resource")
            raise YidlSymbolError(f"undefined resource {name!r}")
        raise YidlSymbolError(f"unsupported resource reference {name!r}")

    def _known_local_non_resource_kind(self, name: str) -> str | None:
        if name in self._local_properties:
            return "property"
        if name in self._local_families:
            return "schema family"
        if name in self._local_records:
            return "record"
        if name in self._local_collections:
            return "collection"
        if name in self._declared_contributions:
            return "contribution"
        if name in self._declared_composable_productions:
            return "composable production"
        for extension in self._extensions:
            if name in extension.properties:
                return "property"
            if name in extension.families:
                return "schema family"
            if name in extension.records:
                return "record"
            if name in extension.collections:
                return "collection"
            if name in extension.contributions:
                return "contribution"
            if name in extension.composable_productions:
                return "composable production"
        return None

    def _known_imported_non_resource_kind(
        self,
        module: YidlCompiledModule,
        name: str,
    ) -> str | None:
        for concept in module.concepts.values():
            if name in concept.properties:
                return "property"
            if name in concept.families:
                return "schema family"
            if name in concept.records:
                return "record"
            if name in concept.collections:
                return "collection"
            if name in concept.contributions:
                return "contribution"
            if name in concept.composable_productions:
                return "composable production"
        return None

    def _reject_imported_property_redefinition(self, name: str) -> None:
        for extension in self._extensions:
            if name in extension.properties:
                raise YidlSymbolError(
                    f"property {name!r} is imported from extended concept "
                    f"{extension.name!r}; redefine is not allowed"
                )

    def _import_module(self, alias: str) -> YidlCompiledModule:
        try:
            return self._imports[alias]
        except KeyError as exc:
            raise YidlSymbolError(f"unknown import alias {alias!r}") from exc

    def _type_value(self, tree: Tree) -> type[object]:
        if len(tree.children) == 1 and isinstance(tree.children[0], Tree):
            name = _qname(tree.children[0])
        else:
            name = tree.data.removeprefix("type_")
        try:
            return _TYPE_NAMES[name]
        except KeyError as exc:
            raise YidlSymbolError(f"unsupported property type {name!r}") from exc

    def _value(self, node: Tree | Token) -> object:
        if isinstance(node, Token):
            if node.type == "STRING":
                return _string_value(node)
            if node.type == "INT":
                return int(str(node))
            if node.type == "NUMBER":
                text = str(node)
                return float(text) if "." in text else int(text)
        if isinstance(node, Tree):
            if node.data == "literal_expr":
                return self._value(node.children[0])
            if node.data == "true":
                return True
            if node.data == "false":
                return False
            if node.data == "none":
                return None
            if node.data == "qname":
                name = _qname(node)
                if name == "REQUIRED":
                    return REQUIRED
                if name in _VALUE_CONSTANTS:
                    return _VALUE_CONSTANTS[name]
            if node.data in {"tuple_empty", "tuple_single", "tuple_multi"}:
                return tuple(self._value(child) for child in node.children)
        raise YidlSymbolError("unsupported value expression in this parser slice")


def _parser() -> Lark:
    global _PARSER
    if _PARSER is None:
        grammar = resources.files("yidl").joinpath("concept_grammar.lark").read_text()
        _PARSER = Lark(grammar, parser="lalr", propagate_positions=True)
    return _PARSER


def _file_tree(tree: Tree) -> Tree:
    if tree.data == "start":
        return tree.children[0]
    return tree


def _children(tree: Tree, data: str) -> tuple[Tree, ...]:
    result: list[Tree] = []
    for child in tree.children:
        if isinstance(child, Tree) and child.data == data:
            result.append(child)
        elif isinstance(child, Tree) and child.data in {"top_level_decl", "concept_member"}:
            result.extend(_children(child, data))
    return tuple(result)


def _first_child(tree: Tree, data: str) -> Tree | None:
    for child in tree.children:
        if isinstance(child, Tree) and child.data == data:
            return child
    return None


def _concept_members(tree: Tree) -> tuple[Tree, ...]:
    members: list[Tree] = []
    for child in tree.children[1:]:
        if isinstance(child, Tree) and child.data == "concept_member":
            members.append(child.children[0])
    return tuple(members)


def _wrapped_children(tree: Tree, wrapper_data: str) -> tuple[Tree, ...]:
    members: list[Tree] = []
    for child in tree.children:
        if (
            isinstance(child, Tree)
            and child.data == wrapper_data
            and child.children
            and isinstance(child.children[0], Tree)
        ):
            members.append(child.children[0])
    return tuple(members)


def _matcher_kind(tree: Tree) -> str:
    if _first_child(tree, "matcher_kind_contribution") is not None:
        return "contribution"
    return "resource"


def _matcher_contribution_names(
    matcher: ContributionMatcherSpec,
) -> tuple[str, ...]:
    names: list[str] = []
    if matcher.default_contribution_name is not None:
        names.append(matcher.default_contribution_name)
    names.extend(rule.contribution_name for rule in matcher.rules)
    return tuple(dict.fromkeys(names))


def _static_path_parts(path: PathSpec) -> tuple[tuple[str, ...], bool]:
    parts: list[str] = []
    dynamic = False
    for segment in path.segments:
        if segment.kind == "name":
            if not dynamic and segment.name is not None:
                parts.append(segment.name)
            continue
        dynamic = True
    return tuple(parts), dynamic


def _plan_for_owner(plan: CapsuleConceptPlan, owner_id: int) -> CapsuleConceptPlan:
    if plan.owner_id == owner_id:
        return plan
    for extension in plan.extensions:
        try:
            return _plan_for_owner(extension, owner_id)
        except YidlSymbolError:
            continue
    raise YidlSymbolError(f"undefined concept plan owner {owner_id!r}")


def _qname(tree: Tree) -> str:
    if tree.data in {"property_ref", "type_ref", "resource_ref", "resource_name_ref"}:
        return _qname(tree.children[0])
    return ".".join(_token_text(child) for child in tree.children)


def _resource_expr_name(tree: Tree) -> str:
    if tree.data == "resource_match_ref":
        return "match.resource()"
    if tree.data in {"resource_ref", "resource_name_ref"}:
        return _qname(tree)
    return tree.data


def _first_qname(tree: Tree) -> str:
    for child in tree.children:
        if isinstance(child, Tree):
            if child.data in {"qname", "property_ref", "identity_expr"}:
                return _first_qname(child) if child.data == "identity_expr" else _qname(child)
    raise YidlSymbolError("expected property reference")


def _token_text(value: object) -> str:
    if not isinstance(value, Token):
        raise TypeError(f"expected token, got {type(value).__name__}")
    return str(value)


def _string_value(value: object) -> str:
    if not isinstance(value, Token):
        raise TypeError(f"expected string token, got {type(value).__name__}")
    return ast.literal_eval(str(value))


def _snippet_source(tree: object) -> _SnippetSource:
    if not isinstance(tree, Tree) or len(tree.children) != 1:
        raise YidlSymbolError("expected snippet source")
    token = tree.children[0]
    if not isinstance(token, Token):
        raise YidlSymbolError("expected snippet token")
    text = str(token)
    line_number = token.line or 1
    column = token.column or 1

    if tree.data == "snippet_string":
        return _SnippetSource(
            source=_string_value(token),
            line_number=line_number,
            offset=column,
        )
    if tree.data == "snippet_backtick_inline":
        return _SnippetSource(
            source=text[1:-1],
            line_number=line_number,
            offset=column,
        )
    if tree.data == "snippet_dollar_paren_inline":
        return _SnippetSource(
            source=text[2:-2],
            line_number=line_number,
            offset=column + 1,
        )
    if tree.data == "snippet_dollar_square_inline":
        return _SnippetSource(
            source=text[2:-2],
            line_number=line_number,
            offset=column + 1,
        )
    if tree.data in {
        "snippet_backtick_block",
        "snippet_dollar_paren_block",
        "snippet_dollar_square_block",
    }:
        lines = text.splitlines()
        body = "\n".join(lines[1:-1])
        return _SnippetSource(
            source=body,
            line_number=line_number + 1,
            offset=0,
        )
    raise YidlSymbolError(f"unsupported snippet form {tree.data!r}")


def _symbol_kind(tree: Tree) -> str:
    return tree.data.removeprefix("symbol_")


def _resolve_import_path(current_path: str, imported: str) -> str:
    if imported.startswith("/"):
        raise YidlSymbolError("absolute YIDL import paths are not allowed")
    return posixpath.normpath(posixpath.join(posixpath.dirname(current_path), imported))


__all__ = [
    "YidlCompiledConcept",
    "YidlCompiledModule",
    "YidlSymbolError",
    "YidlSyntaxError",
    "compile_yidl_files",
    "parse_yidl_source",
]
