# FieldSpec helpers × YIDL design gaps — answers

This document is the compact companion to
`dev-docs/FieldSpecYIDLDesignMatrixGaps.md`.

Use it for quick review and decision-making. Use the full gaps document for the
long-form reasoning.

Format:

- **Gap title**
- **Summary:** one short statement of the shortcoming
- **Options:** mnemonic-tagged recommendation pairs
- **Direction:** preferred direction, prefilled where confidence is high
- **Details:** link back to the full gap entry

## GAP-TG — transaction-group semantics still need completion details

**Summary:** `tx_key` is now explicitly owned in the split design, but
visibility and cross-group interaction rules still need completion.

**Options**

- `RUNTIME+FRONTEND:` add a transaction-groups section to the runtime/class
  model and a small frontend/spec note for harvested `tx_key`
- `SCATTER:` leave `tx_key` implicit across commit-related sections

**Direction:** `RUNTIME+FRONTEND`

**Details:** [GAP-TG](./FieldSpecYIDLDesignMatrixGaps.md#gap-tg)

## GAP-STATIC-CLASS-SURFACE — static/class-like helpers are weakly owned

**Summary:** `static` and `classvar` do not fit cleanly into the current
instance-centric model and remain under-specified.

**Options**

- `CLASS-SURFACE:` add an explicit class-surface subsection plus harvested/spec
  mapping notes
- `DEFER:` leave them vague and treat them as later exceptions

**Direction:** `CLASS-SURFACE`

**Details:** [GAP-STATIC-CLASS-SURFACE](./FieldSpecYIDLDesignMatrixGaps.md#gap-static-class-surface)

## GAP-INJECTABLE-REGISTRY — injectable factory/hook names are not centrally specified

**Summary:** the lifecycle reference has concrete injectable names, but YIDL has
no single source of truth for them.

**Options**

- `REGISTRY:` add one injectable-name registry in frontend design and
  cross-reference it from codegen
- `IMPLICIT:` infer names ad hoc during codegen

**Direction:** `REGISTRY`

**Details:** [GAP-INJECTABLE-REGISTRY](./FieldSpecYIDLDesignMatrixGaps.md#gap-injectable-registry)

## GAP-INIT-ORDERING — init ordering across field kinds is still too generic

**Summary:** the 3-phase init rule exists, but cross-kind ordering is still too
generic for lifecycle parity.

**Options**

- `PHASE-TABLE:` add a phases-by-field-kind table, with frontend notes only
  where source expression is required
- `BEST-EFFORT:` leave ordering informal inside codegen

**Direction:** `PHASE-TABLE`

**Details:** [GAP-INIT-ORDERING](./FieldSpecYIDLDesignMatrixGaps.md#gap-init-ordering)

## GAP-COMMIT-PIPELINE — validators, order keys, hooks, and writes need one explicit pipeline

**Summary:** commit-sensitive features are individually visible, but the design
still lacks one explicit deterministic pipeline.

**Options**

- `PIPELINE:` add one runtime pipeline section plus codegen emission note
- `FRAGMENTS:` keep helper-specific notes and rely on convention

**Direction:** `PIPELINE`

**Details:** [GAP-COMMIT-PIPELINE](./FieldSpecYIDLDesignMatrixGaps.md#gap-commit-pipeline)

## GAP-BINDING-OWNED-MERGE — binding and owned semantics are too compressed

**Summary:** binding and owned currently map to similar areas, but their
semantic distinction is still too compressed to count as covered.

**Options**

- `SEPARATE-SEMANTICS:` add explicit runtime semantics and codegen lowering
  notes for both
- `ALIAS:` temporarily treat owned as binding-like and defer the difference

**Direction:** `SEPARATE-SEMANTICS`

**Details:** [GAP-BINDING-OWNED-MERGE](./FieldSpecYIDLDesignMatrixGaps.md#gap-binding-owned-merge)

## GAP-ANNOTATION-DRIVEN-BEHAVIOR — annotation-driven compare and related ambient rules are under-specified

**Summary:** some lifecycle behavior comes from harvested ambient annotation
rules, not only helper params, and the YIDL design does not state that clearly
enough.

**Options**

- `AMBIENT-HARVEST:` add a frontend ambient-semantics note plus codegen
  cross-reference
- `PARAMS-ONLY:` ignore annotation-driven behavior until later

**Direction:** `AMBIENT-HARVEST`

**Details:** [GAP-ANNOTATION-DRIVEN-BEHAVIOR](./FieldSpecYIDLDesignMatrixGaps.md#gap-annotation-driven-behavior)

## GAP-MRO-MERGE — field-spec MRO merge rules are too lightly documented

**Summary:** MRO merge behavior exists in lifecycle but remains too lightly
documented in YIDL.

**Options**

- `FRONTEND-MRO:` add explicit frontend MRO-composition rules
- `IMPLEMENTATION-ONLY:` leave merge behavior as harvester code detail

**Direction:** `FRONTEND-MRO`

**Details:** [GAP-MRO-MERGE](./FieldSpecYIDLDesignMatrixGaps.md#gap-mro-merge)

## GAP-COMBINATORIAL-PRECEDENCE — cross-helper interactions are not yet first-class

**Summary:** many risks come from helper interactions, but precedence and
combined semantics are still mostly implicit.

**Options**

- `PRECEDENCE-FIRST:` add explicit precedence/ordering rules in runtime/class
  model, extending frontend only where source must express intent
- `IMPLEMENTATION-DRIFT:` let combinations remain implementation-defined

**Direction:** `PRECEDENCE-FIRST`

**Details:** [GAP-COMBINATORIAL-PRECEDENCE](./FieldSpecYIDLDesignMatrixGaps.md#gap-combinatorial-precedence)
