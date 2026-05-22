from __future__ import annotations

import ast
from collections.abc import Iterable
from collections.abc import Mapping
from types import ModuleType

from yidl.runtime.lifecycle_markers import FieldDecl
from yidl.runtime.lifecycle_markers import LifecycleDefinitionError
from yidl.runtime.lifecycle_markers import LifecycleDefinitionWarning
from yidl.runtime.lifecycle_markers import LifecycleMarker
from yidl.runtime.lifecycle_markers import MISSING
from yidl.runtime.lifecycle_markers import _HAS_DEFAULT_FACTORY
from yidl.runtime.lifecycle_markers import after_commit
from yidl.runtime.lifecycle_markers import after_rollback
from yidl.runtime.lifecycle_markers import before_commit
from yidl.runtime.lifecycle_markers import classvar
from yidl.runtime.lifecycle_markers import commit_order_key
from yidl.runtime.lifecycle_markers import field
from yidl.runtime.lifecycle_markers import initvar
from yidl.runtime.lifecycle_markers import managed
from yidl.runtime.lifecycle_markers import normalize_marker
from yidl.runtime.lifecycle_markers import transient
from yidl.runtime.lifecycle_markers import validate_commit
from yidl.runtime.lifecycle_harvester import HarvestedLifecycle
from yidl.runtime.lifecycle_harvester import harvest_lifecycle_definition


def lifecycle(cls: type[object]) -> type[object]:
    """Decorate ``cls`` with the generated lifecycle implementation."""

    if not isinstance(cls, type):
        raise TypeError("@lifecycle can only decorate classes")
    harvested = harvest_lifecycle_definition(cls)
    try:
        source = _generate_lifecycle_source(harvested)
    except Exception as exc:
        _raise_lifecycle_step_error(cls, "source generation", exc)
    namespace: dict[str, object] = {"__name__": cls.__module__}
    try:
        exec(source, namespace)
    except Exception as exc:
        _raise_lifecycle_step_error(cls, "source execution", exc)
    try:
        generated = namespace["build_lifecycle_class"](
            cls,
            **dict(harvested.build_kwargs),
        )
        if not isinstance(generated, type):
            raise TypeError("generated lifecycle builder did not return a class")
    except Exception as exc:
        _raise_lifecycle_step_error(cls, "class build", exc)
    return generated


def _generate_lifecycle_source(harvested: HarvestedLifecycle) -> str:
    generated = _generated_lifecycle_base_module()
    source = generated.build_LifecycleModule(
        _build_lifecycle_container(generated, harvested),
    ).emit_commented()
    # TODO: Emit/import the generated lifecycle class as a Python module instead
    # of executing generated source directly at decorator time.
    return _strip_redundant_pass_statements(source)


def _build_lifecycle_container(
    generated: ModuleType,
    harvested: HarvestedLifecycle,
) -> object:
    builder = generated.new_builder()
    builder.add(
        generated.ClassesCollection,
        generated.LifecycleClass(**dict(harvested.class_fact)),
    )
    for fact in harvested.field_facts:
        record_type = _field_record_type(generated, str(fact["field_kind"]))
        builder.add(
            generated.FieldsCollection,
            record_type(**_filter_record_kwargs(record_type, fact)),
        )
    transaction_method_collection = getattr(
        generated,
        "TransactionMethodsCollection",
        None,
    )
    transaction_method_record = getattr(generated, "TransactionMethod", None)
    if (
        transaction_method_collection is not None
        and transaction_method_record is not None
    ):
        for fact in harvested.transaction_method_facts:
            builder.add(
                transaction_method_collection,
                transaction_method_record(
                    **_filter_record_kwargs(transaction_method_record, fact),
                ),
            )
    return generated.build_container(builder)


def _filter_record_kwargs(
    record_type: type[object],
    fact: Mapping[str, object],
) -> dict[str, object]:
    slots = getattr(record_type, "__slots__", ())
    if not isinstance(slots, tuple):
        return dict(fact)
    return {name: fact[name] for name in slots if name in fact}


def _field_record_type(generated: ModuleType, kind: str) -> type[object]:
    if kind == "field":
        return _required_record_type(generated, "PlainField", kind)
    if kind == "initvar":
        return _required_record_type(generated, "InitVarField", kind)
    if kind == "classvar":
        return _required_record_type(generated, "ClassVarField", kind)
    if kind == "managed":
        return _required_record_type(generated, "ManagedField", kind)
    raise LifecycleDefinitionError(f"unsupported lifecycle field kind: {kind!r}")


def _required_record_type(
    generated: ModuleType,
    name: str,
    kind: str,
) -> type[object]:
    try:
        return getattr(generated, name)
    except AttributeError as exc:
        raise LifecycleDefinitionError(
            f"{kind} lifecycle field requires generated record {name}; "
            "include the matching lifecycle YIDL layer",
        ) from exc


def _generated_lifecycle_base_module() -> ModuleType:
    from yidl.runtime import _generated_lifecycle_base

    return _generated_lifecycle_base


def _raise_lifecycle_step_error(
    cls: type[object],
    step: str,
    exc: BaseException,
) -> None:
    raise LifecycleDefinitionError(
        f"{cls.__qualname__}: lifecycle {step} failed: {exc}",
    ) from exc


def _strip_redundant_pass_statements(source: str) -> str:
    """Remove generated placeholders and unreachable fallback statements."""

    tree = ast.parse(source)
    remover = _RedundantPassLineCollector()
    remover.visit(tree)
    if not remover.line_numbers:
        return source
    lines = source.splitlines(keepends=True)
    filtered = [
        line
        for index, line in enumerate(lines, start=1)
        if index not in remover.line_numbers
    ]
    return "".join(filtered)


class _RedundantPassLineCollector(ast.NodeVisitor):
    def __init__(self) -> None:
        self.line_numbers: set[int] = set()

    def visit_Module(self, node: ast.Module) -> None:
        self._visit_body(node.body)

    def visit_ClassDef(self, node: ast.ClassDef) -> None:
        self._visit_body(node.body)

    def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
        self._visit_body(node.body)

    def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef) -> None:
        self._visit_body(node.body)

    def visit_If(self, node: ast.If) -> None:
        self._visit_body(node.body)
        self._visit_body(node.orelse)

    def visit_For(self, node: ast.For) -> None:
        self._visit_body(node.body)
        self._visit_body(node.orelse)

    def visit_AsyncFor(self, node: ast.AsyncFor) -> None:
        self._visit_body(node.body)
        self._visit_body(node.orelse)

    def visit_While(self, node: ast.While) -> None:
        self._visit_body(node.body)
        self._visit_body(node.orelse)

    def visit_With(self, node: ast.With) -> None:
        self._visit_body(node.body)

    def visit_AsyncWith(self, node: ast.AsyncWith) -> None:
        self._visit_body(node.body)

    def visit_Try(self, node: ast.Try) -> None:
        self._visit_body(node.body)
        self._visit_body(node.orelse)
        self._visit_body(node.finalbody)
        for handler in node.handlers:
            self._visit_body(handler.body)

    def _visit_body(self, body: Iterable[ast.stmt]) -> None:
        statements = tuple(body)
        terminal_seen = False
        for statement in statements:
            if terminal_seen:
                self._mark_statement(statement)
                continue
            if len(statements) > 1 and isinstance(statement, ast.Pass):
                self._mark_statement(statement)
            self.visit(statement)
            if isinstance(statement, ast.Return | ast.Raise | ast.Break | ast.Continue):
                terminal_seen = True

    def _mark_statement(self, statement: ast.stmt) -> None:
        end_lineno = statement.end_lineno or statement.lineno
        self.line_numbers.update(range(statement.lineno, end_lineno + 1))


__all__ = [
    "FieldDecl",
    "LifecycleDefinitionError",
    "LifecycleDefinitionWarning",
    "LifecycleMarker",
    "MISSING",
    "_HAS_DEFAULT_FACTORY",
    "after_commit",
    "after_rollback",
    "before_commit",
    "classvar",
    "commit_order_key",
    "field",
    "HarvestedLifecycle",
    "harvest_lifecycle_definition",
    "initvar",
    "lifecycle",
    "managed",
    "normalize_marker",
    "transient",
    "validate_commit",
]
