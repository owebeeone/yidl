# Validation

This directory holds empirical validation material for YIDL design and
implementation work.

## Layout (PRE_IMPL Phase 0a)

Subdirectories are fixed up front so contributors know where new artifacts go:

| Directory | Purpose |
|-----------|---------|
| `generated_example/` | Behavioral validation: reference lifecycle vs hand-crafted generated strategies; shared scenario harness entry points live alongside this tree as the study grows. |
| `field_representability/` | Focused probes for unclear helper kinds or edge cases. |
| `perf/` | Dedicated performance runners and measurement helpers (same scenarios as behavior, separate execution layer). |

Normative study intent: `dev-docs/PRE_IMPL_STUDY_DESIGN.md`.  
Ordered execution: `dev-docs/PRE_IMPL_STUDY_IMPL_PLAN.md`.

Typical contents also include:

- Python-version comparison work driven by the study matrix
- other bounded experiments that help validate the design

This directory is intentionally separate from:

- `src/` product/source code
- `tests/` parity and main regression suites

Artifacts here are for validation and de-risking. They should not be treated as
supported product code unless they are deliberately promoted.
