# PRE_IMPL Study Design

This document defines the empirical study process for PRE_IMPL.

It exists because PRE_IMPL is not primarily an API-design exercise. Its first
job is to determine whether the generated-factory model is credible enough,
semantically and performance-wise, to become the basis for dominant feature
work.

This document should be read alongside:

- `dev-docs/PRE_IMPL_DESIGN_REVIEW.md`
- `dev-docs/impl-docs/pre_impl_design.md`
- `dev-docs/PROCESS.md`
- `docs/YIDLDesign.md`
- `example/generated_factory_sample.py`

## 1. Study goal

The study answers this question first:

**Can a hand-crafted generated-only implementation shape, modeled on
`example/generated_factory_sample.py`, reproduce lifecycle semantics closely
enough and with acceptable performance to justify proceeding?**

Everything else in PRE_IMPL supports that question.

## 2. Core study method

The study should compare:

1. **Reference lifecycle class**
   A real `pyrolyze.lifecycle` / `@managed_context` class used only as the
   semantic reference backend.

2. **Generated strategy implementations**
   Hand-crafted generated-only implementations that attempt to reproduce the
   same semantics without using lifecycle decoration/runtime machinery as the
   actual implementation path.

The purpose is to see whether a generated-only architecture can be made to pass
the same behavioral scenarios as the reference while remaining plausible from a
performance perspective.

## 3. Study implementations

At minimum, the study should support multiple implementation strategies:

- `lifecycle`
- `generated_strategy_a`
- `generated_strategy_b`
- additional strategy variants as needed

When a new generated strategy is explored, the current generated strategy
should be copied into a new validation artifact and modified there rather than
silently replacing the previous strategy. This preserves comparability and
allows strategy trade-offs to be evaluated directly.

The generated strategies are validation artifacts, not the normative
implementation. They belong under `docs/validation/` until deliberately
promoted.

## 4. Validation layers

The study has two distinct layers:

### 4.1 Behavioral validation

Behavioral validation proves that each generated strategy reproduces the
intended semantics of the reference lifecycle class for the studied scenarios.

These checks should answer:

- does the generated strategy produce the same observable values?
- does it honor current/working/transaction semantics?
- does commit/rollback behave correctly?
- does initialization/default behavior match the reference for the covered
  cases?

### 4.2 Performance validation

Performance validation measures the cost of the same scenario matrix across the
reference lifecycle implementation and the generated strategies.

These checks should answer:

- is the generated strategy obviously slower on critical paths?
- which strategy is better for reads, writes, or transaction-heavy usage?
- are there Python-version cliffs?
- is the generated shape plausible enough to continue?

Do not mix these layers into one opaque test. Correctness and performance
should share scenarios, but they should be run and reported separately.

## 5. Scenario matrix

Start with a small but representative matrix focused on the managed/context
spine.

### 5.1 Operations

Measure and validate at least:

- object construction
- committed read
- working read inside active transaction
- managed write inside transaction
- commit
- rollback
- default/default_factory-driven initialization

### 5.2 Field shapes

Start with:

- one managed scalar field
- two managed fields
- one field whose initialization depends on an earlier field

Add more advanced shapes only when the core path is working:

- local-store / homed field
- multi-group transaction case
- representative advanced managed semantics
- binding/owned representative case when those are under study

### 5.3 Access patterns

Include:

- hot repeated reads
- hot repeated writes inside one transaction
- many short transactions
- repeated object construction
- read-heavy mixed usage with occasional writes

The point of the matrix is not completeness. It is to give repeatable evidence
about the core generated shape.

Implementation detail for the study should live in code where practical. Use
READMEs primarily to say what is here and how areas are organized; do not use
them as the primary home for matrices, runner configuration, or other
executable study facts that belong in code.

## 6. Recommended field/helper study set

The study should not choose field/helper cases ad hoc. Use a staged field/helper
set so the empirical work stays focused and comparable.

### 6.1 Stage A — core credibility cases

These cases should be studied first because they validate the generated shape
itself:

- `managed` single scalar field
- `managed` two-field case
- `managed` default / default_factory dependency case
- `managed` commit / rollback case

These are the minimum cases needed to judge whether the generated factory sample
is credible.

### 6.2 Stage B — shape-extension cases

Study these next once the core path is working:

- `const`
- `static`
- `local_store`
- `derived`

These show whether the generated shape extends cleanly beyond the core managed
overlay path.

### 6.3 Stage C — runtime-pressure cases

Study these when the generated shape begins to stress runtime ownership:

- `multi_group_tx`
- `transient`
- `binding`
- `owned`

These are especially important for deciding whether YIDL-owned runtime support,
including transaction-manager behavior, must already exist for the study to
remain credible.

### 6.4 Stage D — injection / hook / metadata cases

Study these after the earlier stages have established credibility:

- `initvar`
- `commit_order_key`
- `commit_validator`
- `on_before_commit`
- `on_after_commit`
- `on_after_rollback`
- `classvar`
- `lifecycle_field_escape` if it remains in scope

These cases matter, but they should not displace the earlier semantic and
performance questions about the core generated model.

### 6.5 Required classification per helper

For each studied helper or case, record whether the study goal is:

- semantic comparison only
- semantic comparison plus performance comparison
- representability probe only
- explicitly deferred beyond PRE_IMPL

## 7. Recommended layout under `docs/validation/`

Suggested structure:

- `docs/validation/generated_example/`
  Behavioral validation of the hand-crafted generated example and strategy
  variants.
- `docs/validation/field_representability/`
  Focused probes for helper kinds or edge cases that are unclear.
- `docs/validation/perf/`
  Performance harness, scenario definitions, implementation adapters, and
  measurement runners.

Keep strategy implementations and study harnesses out of `src/` and
`tests/baseline/` until they are deliberately promoted.

## 8. Harness design

The study should use one shared scenario contract across all implementations.

That means:

- the reference lifecycle implementation and each generated strategy should be
  exposed through a small common adapter shape
- the same scenarios should drive both correctness validation and performance
  measurement
- implementation-specific glue should stay in adapter code, not in the scenario
  definitions themselves

The scenario contract should make it easy to add:

- a new strategy
- a new field shape
- a new operation benchmark

without rewriting the whole harness.

## 9. Performance mechanism

Use a dedicated performance runner rather than ad hoc timing in ordinary tests.

Recommended approach:

- use ordinary `pytest` validation for semantic checks
- use a dedicated performance harness under `docs/validation/perf/`
- prefer a benchmark tool suitable for repeatable comparisons rather than
  hand-written one-off timing loops

The exact benchmark tool may be chosen during PRE_IMPL, but the mechanism must
support:

- repeated runs across strategies
- repeated runs across Python versions
- separation of cold import/compile cost from steady-state operation cost
- reporting by scenario rather than one aggregate number

## 10. Python version matrix

The study must choose and record a small Python version matrix exercised via
`uv`.

At minimum, the matrix should include:

- the lowest supported version
- one mainstream/current version
- one newer version likely to matter for future optimization decisions

The same scenario set should be run across that matrix so performance and
semantic surprises are visible early.

## 11. Runtime ownership implications

This study is expected to surface whether generated-only implementations can
really stand on their own.

In practice, that likely means some lifecycle runtime components will need to
be copied, re-homed, or redeveloped inside YIDL and then tested there rather
than treated as permanent imports from `pyrolyze.lifecycle`.

In particular, the transaction-manager path is likely to need YIDL-owned
runtime support during or soon after PRE_IMPL. If the generated study
implementations depend on transaction semantics beyond what can be treated as
pure reference behavior, a YIDL-owned transaction manager or equivalent runtime
layer should be introduced and covered by study tests.

`pyrolyze.lifecycle` remains read-only during this phase; study work must not
patch `pyrolyze/`.

## 12. Study outputs

PRE_IMPL study output should include:

1. A judgment on whether `example/generated_factory_sample.py` is credible.
2. One or more hand-crafted generated strategy implementations under
   `docs/validation/`.
3. Behavioral validation scenarios shared across lifecycle and generated
   strategies.
4. A performance matrix with results across the chosen Python versions.
5. A note on whether YIDL-owned transaction/runtime support is already required
   for the study to remain credible.
6. A short findings summary:
   - what works
   - what is unclear
   - what requires design change
   - which strategy direction is currently preferred

## 13. Exit condition for the study

The study is successful enough to unblock dominant feature work when:

- the generated factory sample is judged credible enough to target
- the core managed/context scenarios can be represented by at least one
  generated strategy
- the behavioral comparison against lifecycle is good enough for the covered
  cases
- the performance results do not reveal an obvious architectural dead end
- any required YIDL-owned runtime pieces are identified clearly enough that the
  next slice can proceed deliberately

If the study instead reveals serious semantic holes, performance cliffs, or
runtime-dependence problems, classify them as `design_gap` or `design_conflict`
and update the follow-on plan before dominant feature work proceeds.
