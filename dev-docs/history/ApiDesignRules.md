# API Design Rules

## Purpose

These are generic API design rules for `yidl`. They apply beyond any one
frontend surface and beyond any one bootstrap or generated-code path.

## Rules

### Prefer explicit signatures

Prefer explicit named parameters over `*args` and `**kwargs` when the supported
shape is known.

Reason:

- better IDE support
- better type inference
- clearer docs
- fewer ambiguous call forms

### Keep annotations complete and precise

Public API examples and proposals should carry full type annotations when
practical.

Reason:

- IDE guidance
- easier review
- fewer hidden assumptions

If there is an expected type, annotate it precisely. Do not hide an expected
type behind `Any` unless the value is genuinely unconstrained.

### Do not optimize for neatness at the cost of semantics

A shorter or less repetitive API shape is not better if it changes the meaning,
blurs ownership, or hides important constraints.

### Keep one concept in one place

Do not duplicate the same concept across multiple public entry points unless
there is a strong explicit reason.

### Prefer explicit compile-time boundaries over ambient runtime state

When a system boundary can be expressed through explicit source, schema,
harvested metadata, IR, or generated output, prefer that over ambient runtime
state, reflection, or hidden context.

### Separate authoring surface from metadata and runtime internals

Keep distinct:

- author-facing APIs
- registration/manifest/spec metadata
- runtime-only helpers

Mixing them makes APIs harder to reason about and easier to misuse.

## Review Checklist

Before accepting an API proposal, check:

1. Is the callable or declarative surface explicit?
2. Are the types precise enough for IDEs?
3. Is the proposal cleaner without changing meaning?
4. Are compile-time and runtime boundaries explicit enough to inspect and test?
