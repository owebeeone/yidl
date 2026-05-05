from __future__ import annotations

from support.golden_case import run_case
from yidl.capsule.recorded_builder import capsule_concept
from yidl.generation.data_def_sys import REQUIRED
from yidl.generation.data_def_sys import from_astichi_code


ValidateDuplicateFields = from_astichi_code(
    """
    seen = set()
    for field in ctx.records(FieldsCollection):
        if field.name not in seen:
            seen.add(field.name)
            continue
        ctx.write(
            DiagnosticsCollection,
            Diagnostic(
                severity="error",
                category="design_conflict",
                message=f"duplicate field {field.name!r}",
                source_label=field.source_label,
                field_name=field.name,
                concept_name="FieldValidation",
            ),
            policy=RejectDuplicate,
        )
    """,
    keep_names=(
        "Diagnostic",
        "DiagnosticsCollection",
        "FieldsCollection",
        "RejectDuplicate",
        "ctx",
    ),
)


RaiseDiagnostics = from_astichi_code(
    """
    errors = [
        diagnostic
        for diagnostic in ctx.records(DiagnosticsCollection)
        if diagnostic.severity == "error"
    ]
    if errors:
        raise TypeError("\\n".join(diagnostic.message for diagnostic in errors))
    """,
    keep_names=("DiagnosticsCollection", "TypeError", "ctx"),
)


def _build_concept():
    builder = capsule_concept("LifecycleDiagnostics")
    name = builder.props.Name(str, REQUIRED)
    source_label = builder.props.SourceLabel(str, "")
    severity = builder.props.Severity(str, REQUIRED)
    category = builder.props.Category(str, REQUIRED)
    message = builder.props.Message(str, REQUIRED)
    field_name = builder.props.FieldName(str, "")
    concept_name = builder.props.ConceptName(str, "")

    field = builder.records.Field(name, source_label)
    diagnostic = builder.records.Diagnostic(
        severity,
        category,
        message,
        source_label,
        field_name,
        concept_name,
    )
    fields = builder.collections.Fields(
        field,
        cardinality=builder.many,
    )
    diagnostics = builder.collections.Diagnostics(
        diagnostic,
        cardinality=builder.many,
    )
    builder.operations.ValidateDuplicateFields(
        inputs=(fields,),
        outputs=(diagnostics,),
        resource=ValidateDuplicateFields,
    ).in_group("Validation")
    builder.operations.RaiseDiagnostics(
        inputs=(diagnostics,),
        outputs=(),
        resource=RaiseDiagnostics,
    ).in_group("Validation")
    return builder.build()


def render_case() -> str:
    return _build_concept().emit_runtime_source()


def validate_case(source: str) -> None:
    namespace: dict[str, object] = {}
    exec(source, namespace)

    clean_builder = namespace["new_builder"]()
    field = namespace["Field"]
    fields = namespace["FieldsCollection"]
    clean_builder.add(fields, field(name="count", source_label="Example.count"))
    clean_builder.add(fields, field(name="label", source_label="Example.label"))
    clean_container = namespace["build_container"](clean_builder)
    assert tuple(clean_container.Diagnostics.sequence()) == ()

    duplicate_builder = namespace["new_builder"]()
    duplicate_builder.add(fields, field(name="count", source_label="Example.count"))
    duplicate_builder.add(fields, field(name="count", source_label="Mixin.count"))
    try:
        namespace["build_container"](duplicate_builder)
    except TypeError as exc:
        assert "duplicate field 'count'" in str(exc)
    else:
        raise AssertionError("expected duplicate field diagnostic to raise")

    assert "def run_validate_duplicate_fields(builder):" in source
    assert "def run_raise_diagnostics(builder):" in source
    assert "ctx.records(DiagnosticsCollection)" in source
    assert "Diagnostic(" in source
    assert "duplicate field" in source


if __name__ == "__main__":
    raise SystemExit(
        run_case("dds_lifecycle_validation_operation.py", render_case, validate_case)
    )
