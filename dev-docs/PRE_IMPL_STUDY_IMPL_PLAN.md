# PRE_IMPL Study Implementation Plan

This document is the execution plan for the PRE_IMPL empirical study.

It turns `dev-docs/PRE_IMPL_STUDY_DESIGN.md` into an ordered sequence of phases
and sub-phases with concrete outputs and gates.

Use this document to monitor fine-grained progress. Use the study design doc to
understand *why* the work exists.

This document should be read alongside:

- `dev-docs/PRE_IMPL_STUDY_DESIGN.md`
- `dev-docs/PRE_IMPL_DESIGN_REVIEW.md`
- `dev-docs/impl-docs/pre_impl_design.md`
- `dev-docs/PROCESS.md`

## Monitoring model

- A **phase** is a major study checkpoint with an exit gate.
- A **sub-phase** is a bounded work item inside a phase.
- Do not advance to the next phase until the current phase gate is satisfied or
  an explicit design deferral is recorded.
- If a sub-phase reveals a `design_gap` or `design_conflict`, stop and record
  that before continuing.

## Phase 0 — Study harness bootstrap

Goal: create the minimum study infrastructure needed to run the empirical work.

### 0a. Validation scaffold

Work:

- establish the `docs/validation/` study directories needed for generated
  example validation, representability probes, and performance work

Artifacts:

- `docs/validation/generated_example/`
- `docs/validation/field_representability/`
- `docs/validation/perf/`
- `docs/validation/generated_example/README.md`
- `docs/validation/field_representability/README.md`
- `docs/validation/perf/README.md`

Verification:

- directories exist
- each subtree has a short README describing purpose, allowed contents, and
  validation-only status
- the validation scaffold is documented enough to guide contributors without
  guessing where new study artifacts belong

Failure means:

- PRE_IMPL structure is still too vague to run consistently

### 0b. Python version matrix

Work:

- choose the initial Python versions to exercise with `uv`

Artifacts:

- recorded version matrix in the study docs or validation README

Verification:

- the chosen versions are concrete enough to run without further design debate

Failure means:

- performance review cannot be compared consistently

### 0c. Scenario contract

Work:

- define the common scenario/adapter contract shared by lifecycle and generated
  strategies

Artifacts:

- written scenario contract
- initial harness skeleton under `docs/validation/`

Verification:

- one lifecycle reference scenario and one generated-strategy placeholder can be
  expressed through the same contract

Failure means:

- the harness is too ad hoc to support comparable study results

### 0d. Backend adapter skeletons

Work:

- add the initial lifecycle adapter and generated-strategy adapter skeletons

Artifacts:

- lifecycle adapter
- `generated_strategy_a` adapter placeholder

Verification:

- harness can select and invoke both adapter families, even if generated is
  still skeletal

Failure means:

- the study cannot compare implementations cleanly

### Phase 0 exit gate

Phase 0 is complete when:

- the validation scaffold exists
- the Python version matrix is chosen
- the scenario contract exists
- lifecycle and generated adapter skeletons can both be targeted by the study
  harness

## Phase 1 — Generated factory sample credibility

Goal: determine whether `example/generated_factory_sample.py` is credible as
the first serious generated target.

### 1a. Audit the sample

Work:

- audit `example/generated_factory_sample.py` against `docs/YIDLDesign.md`

Artifacts:

- mismatch list
- notes on illustrative-only vs must-be-real portions

Verification:

- every meaningful mismatch is recorded explicitly

Failure means:

- the sample and design are not aligned closely enough to study honestly

### 1b. Reconcile target shape

Work:

- decide whether mismatches should be fixed in the sample or in `YIDLDesign.md`

Artifacts:

- explicit target-shape decision record

Verification:

- no silent disagreement remains about the intended first generated shape

Failure means:

- PRE_IMPL is studying an undefined target

### 1c. Define Stage A managed scenarios

Work:

- define the core managed/context scenarios used to judge the sample

Artifacts:

- Stage A scenario list
- expected semantic results

Verification:

- the lifecycle reference can express those scenarios

Failure means:

- the study is not targeting the core generated model clearly enough

### Phase 1 exit gate

Phase 1 is complete when:

- the generated factory sample has been audited
- a reconciled target-shape decision exists
- the Stage A core scenarios are defined clearly enough to implement

## Phase 2 — Reference lifecycle baseline

Goal: establish the lifecycle reference behavior for the core study scenarios.

### 2a. Build lifecycle reference class(es)

Work:

- implement the real `pyrolyze.lifecycle` reference classes for the Stage A
  scenarios

Artifacts:

- lifecycle reference study artifacts under `docs/validation/`

Verification:

- scenarios instantiate and run against lifecycle

Failure means:

- the reference contract is not stable enough to compare against

### 2b. Record reference behavior

Work:

- record expected observable results for the Stage A scenarios

Artifacts:

- baseline results / assertions

Verification:

- lifecycle results are captured explicitly rather than implicitly assumed

Failure means:

- generated strategies cannot be compared honestly

### Phase 2 exit gate

Phase 2 is complete when lifecycle provides a stable, runnable semantic
reference for the Stage A scenarios.

## Phase 3 — Generated strategy A

Goal: build the first generated-only strategy and compare it against lifecycle.

### 3a. Implement `generated_strategy_a`

Work:

- create the first hand-crafted generated-only strategy shaped by
  `example/generated_factory_sample.py`

Artifacts:

- generated strategy A validation artifact

Verification:

- the strategy can be instantiated through the study harness

Failure means:

- the generated sample is not yet concrete enough to implement

### 3b. Run Stage A semantic comparison

Work:

- compare lifecycle and strategy A on the Stage A scenarios

Artifacts:

- semantic comparison results

Verification:

- core managed/context semantics either match or produce explicit design issues

Failure means:

- generated-only semantics are not credible for the core path

### 3c. Record strategy A findings

Work:

- summarize where strategy A succeeds, fails, or remains unclear

Artifacts:

- strategy A findings note

Verification:

- failures are classified as implementation issues vs design issues

Failure means:

- the study cannot make a trustworthy go/no-go judgment

### Phase 3 exit gate

Phase 3 is complete when at least one generated-only strategy can either:

- reproduce the core managed scenarios well enough to continue

or

- produce a clearly documented design issue that blocks continuation.

## Phase 4 — Core performance review

Goal: measure whether the generated shape is plausible on the core path.

### 4a. Implement performance runners

Work:

- add the dedicated performance harness for the Stage A scenarios

Artifacts:

- performance runners under `docs/validation/perf/`

Verification:

- lifecycle and strategy A can both be measured through the same harness

Failure means:

- performance conclusions would be ad hoc and untrustworthy

### 4b. Run Stage A performance matrix

Work:

- run the Stage A matrix across the chosen Python versions

Artifacts:

- comparative results for reads, writes, construction, commit, rollback, and
  initialization-related cases as defined for Stage A

Verification:

- results exist for all required implementations and Python versions

Failure means:

- PRE_IMPL cannot judge whether the generated shape is plausibly performant

### 4c. Assess performance risks

Work:

- record whether the generated strategy shows obvious architectural weakness

Artifacts:

- performance findings note

Verification:

- major regressions, cliffs, or unknowns are explicit

Failure means:

- the study continues without understanding obvious performance risks

### Phase 4 exit gate

Phase 4 is complete when there is enough evidence to say whether the generated
core path is performance-plausible or whether it reveals an architectural dead
end.

## Phase 5 — Shape-extension study

Goal: test whether the model extends cleanly beyond the minimal managed core.

### 5a. Study Stage B helper set

Work:

- run the Stage B helper set:
  - `const`
  - `static`
  - `local_store`
  - `derived`

Artifacts:

- representability and behavioral notes for each Stage B helper

Verification:

- each helper is classified as workable, unclear, deferred, or design-changing

Failure means:

- the model may only work for trivial managed cases

### 5b. Add targeted probes where needed

Work:

- add focused validation probes for unclear Stage B cases

Artifacts:

- Stage B probes under `docs/validation/field_representability/`

Verification:

- every unclear Stage B case either has a probe or an explicit deferral

Failure means:

- extension conclusions are based on guesswork rather than evidence

### Phase 5 exit gate

Phase 5 is complete when there is enough evidence to say whether the generated
model extends credibly beyond the trivial managed core.

## Phase 6 — Runtime-pressure study

Goal: determine whether YIDL-owned runtime support is already required for the
study to remain credible.

### 6a. Study Stage C helper set

Work:

- run the Stage C helper set:
  - `multi_group_tx`
  - `transient`
  - `binding`
  - `owned`

Artifacts:

- runtime-pressure findings per helper

Verification:

- each helper is classified as workable with current study machinery, requiring
  YIDL-owned runtime support, or design-changing

Failure means:

- the study cannot say whether runtime ownership is still optional

### 6b. Transaction-manager decision

Work:

- determine whether the transaction-manager path must be copied/re-homed into
  YIDL now for the study to stay honest

Artifacts:

- explicit decision note on YIDL-owned transaction manager or equivalent

Verification:

- the study no longer relies on an implicit assumption that lifecycle runtime
  can remain external indefinitely

Failure means:

- core runtime dependence remains ambiguous

### Phase 6 exit gate

Phase 6 is complete when the study has an explicit position on whether YIDL
runtime ownership, especially the transaction-manager path, must already begin.

## Phase 7 — Injection, hooks, and metadata viability

Goal: determine whether later-pressure cases appear viable enough to avoid
surprises immediately after PRE_IMPL.

### 7a. Study Stage D helper set

Work:

- review and selectively probe:
  - `initvar`
  - `commit_order_key`
  - `commit_validator`
  - `on_before_commit`
  - `on_after_commit`
  - `on_after_rollback`
  - `classvar`
  - `lifecycle_field_escape` if still in scope

Artifacts:

- viability notes and deferral decisions

Verification:

- each Stage D item is classified as viable, deferred, unclear, or requiring
  design change

Failure means:

- the first post-PRE_IMPL slice begins without enough visibility into later
  pressure cases

### Phase 7 exit gate

Phase 7 is complete when the later-pressure cases are classified clearly enough
that the first implementation slices are not walking blind.

## Phase 8 — Findings and recommendation

Goal: close the study with a decision-quality summary.

### 8a. Consolidate findings

Work:

- summarize what works, what is unclear, what requires design change, and which
  generated strategy direction is preferred

Artifacts:

- PRE_IMPL findings summary

Verification:

- all important open questions are visible in one place

Failure means:

- PRE_IMPL ends without decision-quality guidance

### 8b. Recommend next action

Work:

- recommend whether to:
  - proceed to dominant feature work
  - proceed with explicit deferrals
  - pause for design revision

Artifacts:

- study conclusion / recommendation note

Verification:

- the go / adjust / stop decision is explicit

Failure means:

- the PRE_IMPL gate is not actionable

### Phase 8 exit gate

Phase 8 is complete when PRE_IMPL ends with a clear recommendation and explicit
remaining risks.
