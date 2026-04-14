# Semantic Source Design Rules

## Purpose

These rules apply specifically to YIDL source design and the relationship
between:

- author-facing YIDL source
- helper or registration/spec surfaces
- generated/runtime support

This is the YIDL-generalized counterpart to semantic-library rules in other
projects.

## Rules

### No compiler internals in hand-written source

Never write compiler-emitted names or internal lowered implementation details
in:

- hand-written YIDL source
- hand-written `_yidl.py` bootstrap containers
- examples
- author-facing design examples

If an example requires lowered or generated names to make sense, the example is
showing the wrong layer.

### One semantic concept, one public source form

Do not introduce multiple public source forms for the same semantic concept
unless there is a strong explicit reason.

The default should be one clear author-facing form per concept, with other
representations treated as generated or internal.

### Keep authoring, spec metadata, and runtime helpers separate

For every YIDL feature proposal, identify:

1. the author-facing source form
2. the registration/spec or harvested metadata form
3. the generated/runtime-only helper surface

If one proposal mixes those layers, rewrite it before presenting it.

### Keep semantic identity separate from backend/runtime identity

Do not make a semantic YIDL construct depend directly on one backend singleton,
temporary bootstrap mechanism, or one runtime implementation detail.

Keep separate:

- semantic/source identity
- generator/spec identity
- runtime compatibility or execution identity

### Use explicit source/spec flow

YIDL may use:

- source files
- embedded bootstrap containers
- helper calls
- generated manifests/spec objects

But generator/runtime support should consume explicit source/spec data rather
than depend on fragile implicit reflection or hidden runtime context.

## Review Checklist

Before accepting a source-surface proposal, check:

1. What is the one public source form for the semantic concept?
2. What identifies the semantic construct at the source/spec layer?
3. What explicit source/spec object does generation/runtime consume?
4. Is runtime compatibility kept separate from source identity?
