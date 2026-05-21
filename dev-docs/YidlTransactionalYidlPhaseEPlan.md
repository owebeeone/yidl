# YIDL Transactional Base Phase E Plan

## Scope

Phase E tightens diagnostics and facade attribute discipline.

Phase B added reserved-prefix rejection and contextual decorator errors. Phase E
locks the generated facade write policy and broadens decorator-time diagnostics
for generated-name collisions that would otherwise become confusing runtime
shadowing.

## Goals

1. Define and implement facade write/delete policy for classes with a user
   `__dict__`.
2. Detect generated helper, facade exposure, and facade class-name collisions.
3. Keep diagnostics class- and field-specific.
4. Avoid changing transaction semantics.

## Non-Goals

1. Do not add new lifecycle field kinds.
2. Do not add validators or hooks.
3. Do not attempt full dataclass annotation compatibility. Annotation-only
   `ClassVar[...]` / `InitVar[...]` detection remains out of scope unless
   explicitly reintroduced.
4. Do not support user-defined `__slots__`.
5. Do not add a per-class attribute-policy opt-out in Phase E. If permissive
   facades become necessary, add an explicit decorator option in a later phase.

## Attribute Policy

Use the hybrid policy:

- Lifecycle field names are strict. Writes must flow through the generated
  lifecycle property descriptor, so managed fields keep transaction checks and
  plain fields keep the generated storage path.
- Lifecycle field deletion is rejected with an `AttributeError`; Phase E does
  not define "unset" semantics.
- Generated/reserved names remain protected. Assignments or deletions for
  `_y_*` and `__yidl_*__` names are rejected.
- Unrelated user attributes remain normal Python attributes. If the decorated
  user class supplies a `__dict__`, unrelated writes continue to work through
  `object.__setattr__`; if the generated MRO has no `__dict__`, Python raises
  the normal `AttributeError`.

Strict-all facades are rejected for Phase E because they can break legitimate
non-lifecycle attributes added by user methods, descriptors such as
`cached_property`, or framework code. Diagnostic-only facades are too weak
because they leave lifecycle field-name writes vulnerable to bypass if a user
`__dict__` is present.

The generated `__setattr__` shape should be:

```python
def __setattr__(self, name, value):
    if name in _Counter_lifecycle_field_names:
        descriptor = getattr(type(self), name, None)
        if descriptor is None or not hasattr(descriptor, "__set__"):
            raise AttributeError(f"lifecycle field {name!r} is not assignable")
        descriptor.__set__(self, value)
        return
    if name.startswith("_y_") or name.startswith("__yidl_"):
        raise AttributeError(f"{name!r} is reserved for generated lifecycle state")
    object.__setattr__(self, name, value)
```

The generated `__delattr__` shape should reject lifecycle and reserved names,
then delegate unrelated names to `object.__delattr__`.

## Diagnostics

Already enforced by Phase B or earlier:

- reserved prefix `_y_*` / `__yidl_*__`
- malformed inherited lifecycle metadata
- generated state slot collision through the reserved-prefix rule

New in Phase E:

- Field name collides with facade exposure names: `default`, `current`,
  `working`.
- Field name collides with generated helper method names: `begin`, `validate`,
  `commit_only`, `commit`, `rollback`.
- User class body collides with generated facade class names:
  `<ClassName>_State`, `<ClassName>_FacadeBase`, `<ClassName>_Current`,
  `<ClassName>_Working`.

Diagnostics should name the decorated class, the offending member, and the
generated name being protected. Future hook/validator diagnostics in Phase F
should follow the same class- and field-specific shape.

## Verification

Use focused bespoke tests for diagnostics and attribute policy. Add golden
coverage only if generated source shape changes enough that the lifecycle
golden fixture should pin it.

Required tests:

1. A lifecycle field named `default`, `current`, or `working` is rejected with a
   class- and field-specific diagnostic.
2. A lifecycle field named `begin`, `commit`, or another generated helper is
   rejected with a class- and field-specific diagnostic.
3. A user class body member named `<ClassName>_State` or another generated
   facade class name is rejected.
4. Assigning an unrelated attribute on a decorated class that has a user
   `__dict__` still works.
5. Assigning a managed lifecycle field still uses transaction checks; assigning
   without an active transaction raises the existing transaction error.
6. Assigning a reserved `_y_*` or `__yidl_*__` attribute on a generated facade
   raises `AttributeError`.
7. Deleting a lifecycle field raises `AttributeError`.

## Roll-Build

Suggested tag prefix:

```text
txphaseE-diagnostics/
```

Suggested slices:

1. E1: add diagnostic tests for facade exposure/helper/class-name collisions.
2. E2: implement and verify hybrid generated `__setattr__` / `__delattr__`
   policy.
3. E3: refresh generated runtime/goldens if source shape changes and run the
   lifecycle decorator test target.
