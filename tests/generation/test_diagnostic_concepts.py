from __future__ import annotations

import pytest

from yidl.capsule.recorded_builder import capsule_concept
from yidl.generation.data_def_sys import REQUIRED
from yidl.generation.data_def_sys import from_astichi_code


RaiseScenarioDiagnostics = from_astichi_code(
    """
    for scenario in ctx.records(ScenariosCollection):
        if not scenario.is_error:
            continue
        ctx.write(
            DiagnosticsCollection,
            Diagnostic(
                severity="error",
                category="user_input_error",
                message=f"{scenario.kind}: {scenario.name}",
                source_label=scenario.source_label,
                field_name=scenario.name,
                concept_name="ScenarioDiagnostics",
            ),
            policy=RejectDuplicate,
        )
    errors = [
        diagnostic
        for diagnostic in ctx.records(DiagnosticsCollection)
        if diagnostic.severity == "error"
    ]
    if errors:
        raise TypeError("\\n".join(diagnostic.message for diagnostic in errors))
    """,
    keep_names=(
        "Diagnostic",
        "DiagnosticsCollection",
        "RejectDuplicate",
        "ScenariosCollection",
        "TypeError",
        "ctx",
    ),
)


def _runtime():
    builder = capsule_concept("ScenarioDiagnostics")
    name = builder.props.Name(str, REQUIRED)
    kind = builder.props.Kind(str, REQUIRED)
    is_error = builder.props.IsError(bool, False)
    source_label = builder.props.SourceLabel(str, "")
    severity = builder.props.Severity(str, REQUIRED)
    category = builder.props.Category(str, REQUIRED)
    message = builder.props.Message(str, REQUIRED)
    field_name = builder.props.FieldName(str, "")
    concept_name = builder.props.ConceptName(str, "")

    scenario = builder.records.Scenario(name, kind, is_error, source_label)
    diagnostic = builder.records.Diagnostic(
        severity,
        category,
        message,
        source_label,
        field_name,
        concept_name,
    )
    scenarios = builder.collections.Scenarios(scenario, cardinality=builder.many)
    diagnostics = builder.collections.Diagnostics(diagnostic, cardinality=builder.many)
    builder.operations.RaiseScenarioDiagnostics(
        inputs=(scenarios, diagnostics),
        outputs=(diagnostics,),
        resource=RaiseScenarioDiagnostics,
    ).in_group("Validation")
    return builder.build().runtime().load()


@pytest.mark.parametrize(
    ("kind", "message"),
    (
        ("duplicate field", "duplicate field: count"),
        ("invalid override", "invalid override: owner"),
        ("missing template binding", "missing template binding: label"),
    ),
)
def test_diagnostic_gate_reports_user_model_errors(kind: str, message: str) -> None:
    runtime = _runtime()
    namespace = runtime.namespace
    builder = runtime.new_builder()
    builder.add(
        namespace["ScenariosCollection"],
        namespace["Scenario"](
            name=message.rsplit(": ", 1)[1],
            kind=kind,
            is_error=True,
            source_label="Example",
        ),
    )

    with pytest.raises(TypeError, match=message):
        runtime.build_container(builder)
