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
        for member in _concept_members(tree):
            self._compile_member(builder, member)
        plan = builder.build()
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
        )

    def _compile_member(self, builder: Any, member: Tree) -> None:
        data = member.data
        if data == "property_decl":
            prop = self._compile_property(builder, member)
            self._local_properties[prop.name] = prop
            return
        if data == "family_decl":
            self._compile_family(builder, member)
            return
        if data == "collection_decl":
            collection = self._compile_collection(builder, member)
            self._local_collections[collection.name] = collection
            return
        if data == "resource_decl":
            name, resource = self._compile_resource(member)
            self._local_resources[name] = resource
            return
        if data == "matcher_decl":
            matcher = self._compile_matcher(builder, member)
            self._local_matchers[matcher.name] = matcher
            return
        if data == "production_decl":
            production = self._compile_production(builder, member)
            self._local_productions[production.name] = production
            return
        if data == "operation_decl":
            operation = self._compile_operation(builder, member)
            self._local_operations[operation.name] = operation
            return
        if data in {
            "use_decl",
            "record_decl",
            "union_decl",
            "computed_collection_decl",
            "port_decl",
            "diagnostics_decl",
        }:
            raise YidlSymbolError(f"{data} lowering is not implemented yet")
        raise YidlSymbolError(f"unsupported concept member {data!r}")

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
        if name in self._local_matchers:
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
        for extension in self._extensions:
            if name in extension.properties:
                return "property"
            if name in extension.families:
                return "schema family"
            if name in extension.records:
                return "record"
            if name in extension.collections:
                return "collection"
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
