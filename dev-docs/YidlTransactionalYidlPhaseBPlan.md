# YIDL Transactional Base Phase B Plan

## Status

Draft detailed plan.

Phase A proved that YIDL can generate a transactional lifecycle-shaped class
from explicit facts. Phase B turns that proof into a credible decorator
compiler: it harvests facts from a decorated Python class, handles inherited
YIDL-generated bases, emits the same generated source boundary proven in
Phase A, and adds focused diagnostics around the frontend and inheritance
surface.

Phase B should not add new lifecycle field semantics. It should make the
Phase A semantics usable and trustworthy from a decorator-style API.

## Goals

1. Provide a real lifecycle decorator frontend over the Phase A generated
   compiler.
2. Harvest `field`, `initvar`, `classvar`, and `managed` facts from a
   decorated Python class.
3. Preserve the Phase A generated build-function boundary:
   - decorated class passed explicitly
   - static/default values passed as unpacked keyword-only parameters
   - no generic `defaults` or `default_factories` dictionary in generated
     class constructors
4. Implement semantic peeling for inherited YIDL-generated lifecycle bases.
5. Merge inherited and local lifecycle facts without re-harvesting generated
   internals.
6. Preserve normal Python type expectations:
   - returned class has the decorated class name, qualname, and module
   - returned class inherits from the decorated class
   - redecorated derived classes preserve `isinstance(B(), A)`
7. Add focused diagnostics for invalid frontend and inheritance cases.
8. Prove the decorator path through the existing YIDL golden-source harness.

## Non-Goals

1. Do not implement `transient`, `owned`, or `binding` in Phase B.
2. Do not implement commit validators, commit order keys, or commit hooks.
3. Do not add `__post_init__` or user `__init__` chaining.
4. Do not make Phase B a separate feature YIDL file over Phase A.
5. Do not implement broad unknown-attribute enforcement with generated
   `__setattr__` / `__delattr__` gates.
6. Do not add a generic descriptor-table runtime engine.
7. Do not import or patch `pyrolyze`.
8. Do not support user-defined `__slots__` on decorated classes in Phase B.
9. Do not support custom `__init_subclass__` or descriptor `__set_name__`
   lifecycle interactions in Phase B.
10. Do not support `@lifecycle(...)` options in Phase B. Only bare
    `@lifecycle` is supported; Phase C options should be keyword-only.
11. Do not support promoting an existing base instance into a generated
    derived class. Inherited unmanaged-to-managed field promotion affects new
    generated derived instances only.

## Phase B Policy Decisions

### Phase B Is Not A Feature-YIDL Split

Phase B should remain a Python decorator/frontend layer over the Phase A
`lifecycle_base.yidl` concept. It should not introduce a new feature YIDL file
on top of Phase A.

No new YIDL grammar or compiler features are expected for Phase B. If
implementation discovers that a new YIDL surface is required, stop and discuss
the YIDL change before patching the grammar or compiler.

### Decorator Frontend Owns Fact Harvesting

The frontend should convert a class object into the same fact data that the
Phase A golden currently builds by hand.

Phase B should not require users to author YIDL facts directly for normal
decorator use. Direct fact construction remains valuable as compiler-level
test coverage.

The harvester is handwritten Python frontend code, not a YIDL code snippet.
It inspects live class objects, annotations, marker instances, MRO, and
generated lifecycle metadata. YIDL should consume the harvested facts and
generate source; it should not be responsible for Python object inspection.

Recommended module ownership:

```text
src/yidl/runtime/lifecycle.py
src/yidl/runtime/lifecycle_markers.py
src/yidl/runtime/lifecycle_harvester.py
src/yidl/runtime/_generated_lifecycle_base.py
```

Responsibilities:

- `lifecycle.py`: public API: `lifecycle`, `field`, `initvar`, `classvar`,
  `managed`, `MISSING`, and public diagnostics
- `lifecycle_markers.py`: marker objects and normalization into `FieldDecl`
- `lifecycle_harvester.py`: class inspection, semantic peeling, inherited
  metadata merge, and Phase A-compatible fact generation
- `_generated_lifecycle_base.py`: build-time generated Python source compiled
  from `lifecycle_base.yidl`

`_generated_lifecycle_base.py` should be checked into the source tree as a
build-time artifact, analogous to generated parser/runtime artifacts. It should
not be generated at import time by default. Import-time generation can remain a
development/debug path if useful, but it is not the Phase B packaging model.

### Generated Source Remains The Runtime

The YIDL-compiled decorator module should be Python source and should be usable
as a library build-time artifact. A project may still generate that source at
import time, but the normal distribution shape is expected to be:

```text
lifecycle_base.yidl -> generated decorator .py -> imported by runtime package
```

The decorator invokes code generated from the decorated class facts. That code
may be executed from source or from a generated AST, but the generated code
shape remains the authoritative runtime. Do not replace generated field
properties with a shared runtime descriptor engine.

Any cache in Phase B should be private and boring. Caching the compiled YIDL
decorator module/concept is acceptable. Caching user-class-specific generated
classes is optional and not required for Phase B correctness.

The only cache in scope for Phase B is a module-level memo of the imported
generated LifecycleBase decorator module, if implementation needs one. Do not
add user-class-specific generated-class caching in Phase B.

The public decorator surface lives in `yidl.runtime.lifecycle`. Transaction
primitives such as `DEFAULT_TRANSACTION` and `TransactionManager` remain in
`yidl.runtime.transaction_yidl`; the lifecycle API should not absorb the lower
level transaction runtime.

### Semantic Peeling Is Metadata-Driven

When a decorated base class is already YIDL-generated, the frontend reads:

```python
__yidl_lifecycle_generated__
__yidl_lifecycle_user_class__
__yidl_lifecycle_definition__
```

The frontend must ignore generated state classes, generated facade classes,
generated properties, generated helper methods, and generated slots when
harvesting the derived class. The metadata is the contract.

### Parent Facts First

For inheritance merges:

1. inherited facts are loaded first in MRO order
2. local facts are applied after inherited facts
3. compatible local redeclarations override or refine inherited facts by
   field name
4. child-only transaction groups are appended after inherited groups

This preserves parent tx indexes and slot names.

## Frontend Surface

Phase B should introduce a test-facing public shape equivalent to:

```python
from yidl.runtime.lifecycle import classvar
from yidl.runtime.lifecycle import field
from yidl.runtime.lifecycle import initvar
from yidl.runtime.lifecycle import lifecycle
from yidl.runtime.lifecycle import managed
from yidl.runtime.transaction_yidl import DEFAULT_TRANSACTION


@lifecycle
class Counter:
    plain: int = field(default=3)
    optional: str | None = field(default=None)
    tags: list[str] = field(default_factory=list)
    seed: int = initvar(default=2)
    KIND: str = classvar(default="counter")
    count: int = managed(default=1)
    audit_count: int = managed(tx_group="audit", default=10)
    default_count: int = managed(DEFAULT_TRANSACTION, default=20)
```

The exact marker object API can be minimal in Phase B. It only needs to
express the fields already supported by the Phase A YIDL facts:

```text
field(default=..., default_factory=..., init=True)
initvar(default=..., default_factory=..., init=True)
classvar(default=...)
managed(tx_group=DEFAULT_TRANSACTION, default=..., init=True)
```

The intended marker forms are:

```python
field()
field(default=3)
field(default=None)
field(default_factory=list)
field(init=False, default=3)

initvar(default=2)

classvar(default="counter")

managed(default=1)
managed("audit", default=10)
managed(tx_group="audit", default=10)
managed(init=False, default=1)
```

Use `yidl.sentinel_maker.sentinels.MISSING` or an equivalent exported
`MISSING` sentinel internally so `default=None` is distinct from no default.
The sentinel helper should use Python's PEP 661 sentinel implementation when
available and otherwise fall back to a pickle-stable local sentinel.

If annotation-based `ClassVar[...]` / `InitVar[...]` recognition is cheaper
than helper functions, keep it out of Phase B anyway. Phase B requires explicit
`classvar(...)` and `initvar(...)` markers. Bare `ClassVar[...]` or
`InitVar[...]` annotations without markers are unsupported; emit a specific
diagnostic if detection is cheap, otherwise leave them as ordinary annotations
for this phase.

Normalized marker output should have this shape:

```python
FieldDecl(
    name="count",
    annotation=int,
    kind="managed",
    init=True,
    has_default=True,
    default=1,
    has_default_factory=False,
    default_factory=MISSING,
    tx_group=DEFAULT_TRANSACTION,
)
```

## Harvested Fact Model

The frontend should produce a lifecycle definition payload with enough
information to rebuild the generated class and to merge derived classes later.

`module_name` comes from `decorated_cls.__module__`. This includes `__main__`
for interactive or script execution. Classes decorated inside function bodies
still use the containing module name; their qualname carries the local nesting.

At minimum:

```python
{
    "classes": (
        {
            "class_id": "Counter",
            "class_name": "Counter",
            "module_name": "...",
            "state_class_name": "Counter_State",
            "facade_base_class_name": "Counter_FacadeBase",
            "current_facade_class_name": "Counter_Current",
            "working_facade_class_name": "Counter_Working",
            "lifecycle_definition_param_name": "_Counter_lifecycle_definition",
            "annotations_param_name": "_Counter_annotations",
            "tx_groups_param_name": "_Counter_tx_groups",
        },
    ),
    "fields": (
        {
            "field_id": "Counter.count",
            "field_owner": "Counter",
            "field_name": "count",
            "field_kind": "managed",
            "field_order": 30,
            "annotation": int,
            "init": True,
            "has_default": True,
            "default_value_param_name": "_Counter_count_default",
            "tx_group_key": DEFAULT_TRANSACTION,
            "current_slot_name": "_y_count_current",
            "working_slot_name": "_y_count_working",
        },
    ),
    "tx_groups": (DEFAULT_TRANSACTION, "audit"),
}
```

The structure may use dataclasses internally. The generated metadata payload
stored on the returned class should be plain and stable enough for later
compiler versions to read.

The top-level metadata should include a schema version:

```python
{
    "version": 1,
    "class": {...},
    "fields": (...),
    "tx_groups": (...),
}
```

In Phase B the only valid lifecycle metadata version is `1`. Reading a
generated base with any other version rejects with `LifecycleDefinitionError`.
Cross-version compatibility is deferred until a version `2` schema exists.

### Field Ordering

Field order is deterministic and based on class-body annotation order.

For a single decorated class:

```text
field_order = (annotation_index + 1) * 10
```

where `annotation_index` is zero-based order in `__annotations__`.

For inheritance:

1. inherited fields keep their parent `field_order`
2. a child override of the same field name keeps the inherited `field_order`
3. child-only fields append after the inherited maximum order, in child
   annotation order, using increments of `10`
4. no merge step renumbers inherited fields into a contiguous run

This preserves deterministic generated source and keeps inherited layout stable
while leaving gaps for later inserted computed fields if needed.

## Default And Factory Boundary

Phase B should keep the Phase A boundary style:

```python
build_lifecycle_class(
    decorated_cls,
    _Counter_lifecycle_definition=definition,
    _Counter_annotations=annotations,
    _Counter_tx_groups=tx_groups,
    _Counter_plain_default=3,
    _Counter_count_default=1,
)
```

If zero-argument default factories are included in Phase B, they should use
unpacked parameters:

```python
_Counter_tags_default_factory=list
```

Do not reintroduce a generic `default_factories` dictionary. Parameterized
default factories and dependency ordering can be Phase C unless they are
already trivial to reuse from the computed-fact work.

## Semantic Peeling Algorithm

For a class `B(A)` where `A` is generated by the lifecycle decorator:

```python
@lifecycle
class A:
    v1: int = managed(default=1)

@lifecycle
class B(A):
    v2: int = managed(default=2)
```

the frontend should:

1. identify generated lifecycle bases using `__yidl_lifecycle_generated__`
2. read inherited facts from `A.__yidl_lifecycle_definition__`
3. use `A.__yidl_lifecycle_user_class__` as the semantic user-class base when
   needed for harvesting
4. harvest only facts declared on the new class body for `B`
5. merge inherited facts and local facts
6. generate a new class whose facade base inherits from decorated `B`

The generated `B` must keep generated `A` in the Python MRO through the
decorated class:

```python
assert isinstance(B(), A)
```

Do not physically remove generated `A` from the MRO. The goal is semantic
peeling for harvesting, not MRO surgery.

The newly generated facades for `B` should re-emit and override every lifecycle
property from the merged fact set. Inherited generated descriptors must not own
`B` state.

Classvars materialize on the generated common facade base, not on only the main
facade class. The main, current, and working facades should see classvars
through normal inheritance from that common base.

## Override And Merge Rules

Field identity is by final field name within the generated class.

Allowed in Phase B:

- inherited field reused unchanged
- local field with a new name
- local field with the same name replacing default/init metadata
- inherited unmanaged field becoming a managed field

Do not enforce same-kind overrides broadly in Phase B. Field kinds may later
need a richer compatibility relation such as union/subclass behavior.

Rejected in Phase B:

- inherited `managed` field becoming unmanaged
- inherited `managed` field changing transaction group
- local field whose generated slot names would collide with another field
- local field whose constructor parameter name collides with another parameter
- inherited transaction group re-indexing

Parent transaction groups keep their indexes. Child-only groups append in
local declaration order. This should naturally fall out of reverse-MRO field
discovery, but the generated metadata should still make it explicit.

A child field that references a transaction group already present in an
inherited definition reuses the inherited group's tx index. For multiple new
transaction groups in one class body, indexes are assigned by first managed
field declaration that references each new group.

### Reserved Names

Phase B uses a reserved-prefix policy rather than a hand-maintained generated
name list.

The harvester rejects decorated class-body declarations whose names match:

```text
_y_*
__yidl_*__
```

This includes annotations, marker fields, methods, and class attributes visible
in the class body. Future generated slots and helpers should continue using
these prefixes so new Phase C generated names cannot silently collide with user
declarations.

## Diagnostics

Phase B diagnostics should be specific and early. Suggested cases:

1. duplicate field name in one decorated class body
2. constructor parameter collision
3. duplicate generated parameter name
4. reserved `_y_*` or `__yidl_*__` name declared by the decorated class
5. inherited managed field is overridden by an unmanaged field
6. inherited managed field would change tx group index
7. default and default_factory both provided
8. initvar with `init=False` is ignored in Phase B and should not be covered
   by Phase B tests
9. unsupported annotation or field marker shape
10. generated lifecycle metadata is missing required keys or has an unknown
    schema version

The error should name the decorated class and field when possible.

Use one frontend exception type for harvesting, marker, metadata, and
inheritance diagnostics:

```python
class LifecycleDefinitionError(ValueError):
    pass
```

Prefer messages like:

```text
Counter.count: managed field cannot change transaction group from 'audit' to 'default_transaction'
```

over generic failures.

## Golden Test Shape

Add a decorator-path golden separate from the explicit-fact Phase A golden.

Suggested source:

```text
tests/data/gold_src/yidl_transactional_phase_b_decorator.py
```

Suggested materialized outputs:

```text
tests/data/goldens/materialized/yidl_transactional_phase_b_decorator/decorator.py
tests/data/goldens/materialized/yidl_transactional_phase_b_decorator/decorator_prettier.py
tests/data/goldens/materialized/yidl_transactional_phase_b_decorator/generated_output.py
tests/data/goldens/materialized/yidl_transactional_phase_b_decorator/generated_output_prettier.py
tests/data/goldens/materialized/yidl_transactional_phase_b_decorator/generated_inherited_output.py
tests/data/goldens/materialized/yidl_transactional_phase_b_decorator/generated_inherited_output_prettier.py
```

The golden should prove:

1. the decorator frontend creates the same generated source shape as Phase A
   for the common fixture
2. generated class identity is preserved
3. plain fields, classvars, initvars, and managed fields work
4. two transaction groups work
5. inherited generated base works with all marker kinds in both base and
   derived classes, including colliding and non-colliding names:

```python
@lifecycle
class A:
    plain: int = field(default=1)
    seed: int = initvar(default=2)
    KIND: str = classvar(default="A")
    v1: int = managed(default=1)

@lifecycle
class B(A):
    plain: int = managed(default=3)  # unmanaged -> managed is allowed
    seed: int = initvar(default=4)
    KIND: str = classvar(default="B")
    v2: int = managed(default=2)

assert isinstance(B(), A)
```

Assert `isinstance(B(), A)`, all marker kinds work, colliding names use the
derived definition, non-colliding inherited fields still work, and transaction
behavior works.

Keep lower-level explicit-fact tests for compiler mechanics and diagnostics
that the golden harness does not express cleanly.

## Implementation Slices

### Slice B1: Frontend Marker Objects

Deliverables:

- minimal marker/helper objects for `field`, `initvar`, `classvar`, `managed`
- normalized internal field declaration dataclass
- focused tests for marker normalization

Verification:

- helper objects preserve default/default_factory/init/tx metadata
- unsupported combinations fail with clear diagnostics

### Slice B2: Class Harvester

Deliverables:

- harvest annotations and marker objects from a plain class
- produce Phase A-compatible class and field fact dictionaries
- generate deterministic class, slot, and parameter names
- ignore `initvar(init=False)` without producing constructor, state, or
  diagnostic facts

Verification:

- focused harvester tests for `field`, `initvar`, `classvar`, `managed`
- duplicate field and parameter diagnostics

### Slice B3: Decorator Wrapper

Deliverables:

- compile/build the LifecycleBase concept through the existing runtime emitter
- create the YIDL container from harvested facts
- call `build_LifecycleModule`
- execute generated output and return `build_lifecycle_class(...)`

Verification:

- decorator-path golden for a single class
- no manual explicit fact construction in the common-path fixture

### Slice B4: Semantic Peeling

Deliverables:

- detect generated lifecycle bases
- read and validate `__yidl_lifecycle_definition__`
- merge inherited and local facts
- preserve generated base in MRO

Verification:

- `isinstance(B(), A)` smoke
- `class C(B): ...` and `assert isinstance(C(), A)` smoke
- inherited managed field works in derived class
- child-only managed field works in derived class
- all marker kinds work in both base and derived fixtures
- colliding derived field names override inherited field facts
- non-colliding inherited field names remain visible
- inherited tx indexes remain stable

### Slice B5: Override Diagnostics

Deliverables:

- managed-to-unmanaged inherited overrides reject
- managed tx group changes reject
- tx group re-indexing rejects
- reserved `_y_*` and `__yidl_*__` names reject
- malformed lifecycle metadata rejects

Verification:

- focused diagnostic tests
- no duplicate success-path assertions already covered by goldens

### Slice B6: Boundary And Cache Cleanup

Deliverables:

- module-level generated LifecycleBase decorator module memo, if needed
- no generic defaults/default_factories dictionaries in generated class source
- stable lifecycle metadata schema version
- documentation update for the decorator surface

Verification:

- generated source grep/shape assertions
- decorator-path golden asserts generated output uses unpacked keyword-only
  values such as `_Counter_plain_default`, not generic `defaults` or
  `default_factories` dictionaries
- full relevant regression

## Roll-Build Candidate Assessment

Phase B is a good roll-build candidate after B1 and B2 source shapes are agreed.
Recommended checkpoints:

1. `txphaseB/B1-markers`
2. `txphaseB/B2-harvester`
3. `txphaseB/B3-decorator`
4. `txphaseB/B4-inheritance`
5. `txphaseB/B5-diagnostics`
6. `txphaseB/B6-boundary`

Stop before Phase C if inheritance semantics become ambiguous.

## Open Questions For Later Phases

1. Should parameterized default factories be included in late Phase B or kept
   as Phase C?
2. How much dataclass-compatible annotation interpretation is worth supporting?
3. Should the metadata schema be versioned with an integer or a named object?
4. Should decorator caching be keyed by class identity, field signature, or both?
5. Should transaction support split into a feature YIDL after Phase B proves
   the decorator path?
