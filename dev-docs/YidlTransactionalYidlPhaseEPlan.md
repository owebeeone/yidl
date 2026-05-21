# YIDL Transactional Base Phase E Plan

## Scope

Phase E tightens diagnostics and facade attribute discipline.

Phase B added reserved-prefix rejection and contextual decorator errors. Phase E
should decide how strict generated facades are about unknown writes and broaden
compile/decorator-time diagnostics for generated-name collisions.

## Goals

1. Define facade write policy for classes with user `__dict__`.
2. Detect generated slot, helper, facade exposure, and property collisions.
3. Keep diagnostics class- and field-specific.
4. Avoid changing transaction semantics.

## Non-Goals

1. Do not add new lifecycle field kinds.
2. Do not add validators or hooks.
3. Do not attempt full dataclass annotation compatibility.
4. Do not support user-defined `__slots__` unless the policy is explicitly
   designed here.

## Policy To Decide

Options:

1. Strict generated `__setattr__` / `__delattr__` gates on all facade classes.
2. Diagnostics only when the decorated class has `__dict__`.
3. Hybrid: lifecycle field names are strict; unrelated user attrs remain normal.

The chosen policy must be reflected in generated source and tests.

## Diagnostics

Candidate diagnostics:

- field name collides with `default`, `current`, `working`
- generated state slot collision
- generated helper method collision
- generated facade class name collision
- reserved prefix `_y_*` / `__yidl_*__`
- malformed inherited lifecycle metadata

Annotation-only `ClassVar[...]` / `InitVar[...]` detection remains out of scope
unless explicitly reintroduced.

## Verification

Focused tests should cover diagnostics. Goldens should cover only successful
generated shape if the chosen attribute policy changes generated code.

## Roll-Build

Suggested tag prefix:

```text
txphaseE-diagnostics/
```
