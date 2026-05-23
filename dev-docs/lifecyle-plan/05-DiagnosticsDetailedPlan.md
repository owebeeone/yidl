# Diagnostics Detailed Plan

## Goal

Provide a consistent validation and diagnostics path for decoration-time
lifecycle generation failures without building a large error framework before it
is needed.

Critical review status: diagnostics are a reusable concept pattern, not a DDS
core engine. V1 diagnostics use ordinary records, generated validation
operations, and a generated final gate.

This feature supports:

- helper parameter validation
- duplicate declaration errors
- invalid overrides
- invalid callable signatures
- unused initvars
- missing transaction keys
- production/write conflicts

## Problem

Current DDS code can raise `TypeError` or `ValueError` for local API mistakes.
Lifecycle generation needs errors that mention semantic context:

- field name
- helper name
- source label
- concept name
- transaction key
- base/derived layer
- callable name/signature

If every concept raises ad hoc messages, diagnostics will be inconsistent and
hard to test.

## Proposed Fluent API

Diagnostics start as ordinary DDS records and a final gate.

```python
Severity = dds.property("Severity", object, REQUIRED, storage_name="severity")
Category = dds.property("Category", object, REQUIRED, storage_name="category")
Message = dds.property("Message", str, REQUIRED, storage_name="message")
SourceLabel = dds.property("SourceLabel", str, "", storage_name="source_label")
FieldName = dds.property("FieldName", str, "", storage_name="field_name")
ConceptName = dds.property("ConceptName", str, "", storage_name="concept_name")

Diagnostic = dds.record(
    "Diagnostic",
    Severity,
    Category,
    Message,
    SourceLabel,
    FieldName,
    ConceptName,
)

Diagnostics = dds.collection("Diagnostics", Diagnostic)
```

Validation productions can write diagnostics. Prefer ordinary productions or a
concept-layer helper that lowers to an aggregate generated operation; do not add
`dds.validation(...)` as a V1 DDS-core API.

```python
concept.operations.validate(
    "ValidateNoDuplicateValidators",
    source=CommitValidators,
    diagnostics=Diagnostics,
    rule=duplicate_validator_rule,
)
```

Equivalent ordinary production shape:

```python
dds.production(
    "DuplicateValidatorDiagnostics",
    source=DuplicateValidators,
    target=Diagnostics,
    values={
        Severity: literal(ERROR),
        Category: literal(DESIGN_CONFLICT),
        Message: call("duplicate-validator-message", duplicate_validator_message),
        FieldName: source.prop(Name),
        SourceLabel: source.prop(SourceLabel),
        ConceptName: literal("LifecycleHooks"),
    },
    policy=RejectDuplicate,
)
```

Add a validation helper only in the fluent/concept layer if ordinary production
definitions become repetitive.

## Final Gate API

Generated runners need a standard final gate:

```python
container.raise_diagnostics()
```

or:

```python
raise_if_diagnostics(ctx)
```

V1 should use generated source:

```python
def raise_if_diagnostics(ctx):
    errors = [
        diagnostic
        for diagnostic in ctx.records(DiagnosticsCollection)
        if diagnostic.severity is ERROR
    ]
    if errors:
        raise YidlGenerationError(errors)
```

If introducing `YidlGenerationError` is too much for the slice, raise
`TypeError` with a joined message. Keep the diagnostic records anyway.

## Diagnostic Categories

Use semantic objects or constants, not string enums:

```python
DESIGN_CONFLICT = DiagnosticCategory("design_conflict")
DESIGN_GAP = DiagnosticCategory("design_gap")
IMPLEMENTATION_BUG = DiagnosticCategory("implementation_bug")
USER_INPUT_ERROR = DiagnosticCategory("user_input_error")
```

If these category objects create source-emission friction, V1 may use stable
module constants. Do not pass raw strings through every API.

## Expected Use Case

Duplicate commit validator:

```python
CommitValidators = dds.collection(
    "CommitValidators",
    CommitValidator,
    identity=(SpecialKind, TxKey),
)

ctx.write(
    CommitValidators,
    CommitValidator(
        special_kind=COMMIT_VALIDATOR,
        tx_key="default_transaction",
        name="validate_a",
        source_label="Example.validate_a",
    ),
    policy=RejectDuplicate,
)
```

If the duplicate is detected during strict write, the write path can raise
directly. If duplicates are intentionally accumulated for better diagnostics,
a validation production writes:

```python
Diagnostic(
    severity=ERROR,
    category=DESIGN_CONFLICT,
    message="duplicate commit_validator for transaction key 'default_transaction'",
    source_label="Example.validate_b",
    field_name="validate_b",
    concept_name="LifecycleSpecialDeclarations",
)
```

## Expected Generated Source Golden

Expected excerpt for
`tests/data/goldens/materialized/dds_lifecycle_diagnostics.py`:

```python
class Diagnostic:
    __slots__ = (
        "severity",
        "category",
        "message",
        "source_label",
        "field_name",
        "concept_name",
    )
    ...


class YidlGenerationError(TypeError):
    def __init__(self, diagnostics):
        self.diagnostics = tuple(diagnostics)
        message = "\n".join(diagnostic.message for diagnostic in self.diagnostics)
        super().__init__(message)


def validate_unused_initvars(ctx):
    used = {edge.initvar_name for edge in ctx.records(InitvarEdgesCollection)}
    for initvar in ctx.records(InitVarsCollection):
        if initvar.name in used:
            continue
        ctx.write(
            DiagnosticsCollection,
            Diagnostic(
                severity=ERROR,
                category=USER_INPUT_ERROR,
                message=f"unused initvar {initvar.name!r}",
                source_label=initvar.source_label,
                field_name=initvar.name,
                concept_name="InitvarDependencyConcept",
            ),
            policy=RejectDuplicate,
        )


def raise_if_diagnostics(ctx):
    errors = [
        diagnostic
        for diagnostic in ctx.records(DiagnosticsCollection)
        if diagnostic.severity is ERROR
    ]
    if errors:
        raise YidlGenerationError(errors)


def run_operations(ctx):
    validate_unused_initvars(ctx)
    raise_if_diagnostics(ctx)
    return ctx.freeze()
```

The golden must prove:

- diagnostic records are ordinary generated records
- validation is an operation in the generated runner
- final gate is explicit
- source label and field name are preserved

## Immediate Raise Vs Diagnostic Record

Use direct exceptions for programmer/API misuse:

- collection belongs to the wrong DDS
- invalid production definition
- invalid property definition
- source-emission bug

Use diagnostics for user model errors:

- invalid helper combination
- duplicate lifecycle declaration
- invalid override
- unused initvar
- unsupported callable signature in user-provided hook/factory

This split keeps internal bugs from being hidden as model diagnostics.

## Diagnostics Required By Lifecycle

V1 lifecycle diagnostics should cover:

- duplicate field names in one declaration layer
- invalid override across layers
- duplicate validator/order key per transaction key
- unsupported callable parameter
- unused initvar
- helper parameter scrub/fixed mismatch
- invalid field kind for declaration space

Later diagnostics:

- binding/owned annotation shape mismatch
- invalid rollback policy combination
- invalid facade/store combination
- resource cleanup policy mismatch

## Implementation Notes

Start with ordinary records and generated validation operations. Avoid creating:

- a diagnostic DSL
- a second exception hierarchy
- a validation engine separate from productions

If validation productions become repetitive, add a small
`concept.operations.validate(...)` helper that lowers to ordinary productions.

## Test Plan

Bespoke:

- `test_diagnostic_record_source_context`
- `test_raise_if_diagnostics_raises_generation_error`
- `test_internal_api_error_raises_directly`
- `test_validation_production_writes_diagnostic`

Goldens:

- `tests/data/gold_src/dds_lifecycle_diagnostics.py`
- `tests/data/goldens/materialized/dds_lifecycle_diagnostics.py`

Failure cases should stay bespoke; success generated-source shape belongs in
goldens.
