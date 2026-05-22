# YIDL Transactional Base Phase I Plan

## Status

The original simple `binding(...)` slice is merged into
`dev-docs/YidlTransactionalYidlPhaseHPlan.md`.

The current decision is that a first `binding(...)` helper is only a plain
stored `BindingBase` field with scalar/container validation. That is a subset
of the retained-resource machinery needed for `owned(...)`, so a separate
roll-build would add process overhead without clarifying semantics.

## Reserved Future Scope

A future Phase I should only exist if `binding(...)` grows beyond plain
`BindingBase` storage into graph/relationship semantics, such as:

- source/target binding descriptors.
- cross-object or cross-facade references.
- reactive read-through or write-through behavior.
- binding dependency graph validation.
- cycle diagnostics for binding graphs.
- transaction interaction across binding boundaries.

Until then, Phase H owns the marker, validation, and simple generated code for
`binding(...)`.

## Non-Goals

1. Do not implement broad reactive dataflow as part of the Phase H merge.
2. Do not infer binding semantics from arbitrary Python descriptors.
3. Do not revive this phase unless there is a concrete graph-binding surface to
   specify and test.
