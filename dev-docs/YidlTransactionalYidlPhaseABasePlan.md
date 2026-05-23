# YIDL Transactional Base Phase A Plan

## Status

Draft detailed plan.

This document defines the first YIDL-generated transactional lifecycle base
slice. It intentionally favors a direct base decorator proof over a fully
layered feature-YIDL split. The goal is to prove the generated object model,
transaction key indexing, managed field read/write semantics, facade weakref
management, and generated decorator/source shape before expanding into the
full lifecycle helper surface.

Phase A is not the full `pyrolyze.lifecycle` replacement. It is the first
transactional vertical that should make the later replacement credible.

## Goals

1. Generate a lifecycle-style replacement class from a decorated Python class.
2. Preserve public class identity for the main facade:
   - returned class has the decorated class name, qualname, and module
   - returned class inherits from the decorated class
   - generated current and working facades also inherit from the decorated
     class through the generated facade base
3. Generate one mutable state/store class per decorated class.
4. Generate three concrete facade surfaces over that state:
   - default/main facade
   - current facade
   - working facade
5. Generate explicit facade exposure fields:
   - `.default`
   - `.current`
   - `.working`
6. Use weak references from state to facades and strong references from
   facades to state.
7. Use the YIDL-owned transaction runtime:
   - `yidl.runtime.transaction_yidl.TransactionManager`
   - `yidl.runtime.transaction_yidl.DEFAULT_TRANSACTION`
8. Support at least these field kinds:
   - `field`
   - `initvar`
   - `classvar`
   - `managed`
9. Support multi-transaction-group metadata from the first transaction slice.
10. Prove generated code through the existing YIDL golden-source harness.

## Non-Goals

1. Do not implement `transient`, `owned`, or `binding` in Phase A.
2. Do not implement commit validators, commit order keys, or commit hooks in
   Phase A beyond protocol stubs required by `TransactionManager`.
3. Do not implement `__post_init__` or chained user `__init__` calls.
4. Do not make transaction support a separate feature YIDL file yet.
5. Do not solve arbitrary user-class `__dict__` attribute writes in Phase A.
   If this needs enforcement later, it can be handled by generated
   `__setattr__` / `__delattr__` gates or a diagnostic.
6. Do not import or patch `pyrolyze`.
7. Do not generate a generic runtime descriptor table or generic lifecycle
   engine.

## Phase A Policy Decisions

### Direct Base Decorator First

Phase A should build `lifecycle_base.yidl` as the direct generated decorator
concept. The base concept may be internally factored, but the first proof does
not need to demonstrate transaction support as a separate feature YIDL layer.

The implementation should still use records, computed fact operations,
matchers, contributions, and productions in a way that can later be split into
feature files.

### No User `__init__` Chaining

The generated main facade owns construction. It does not call the decorated
class `__init__`.

This matches the current dataclass-like direction: construction is generated
from harvested facts, defaults, and default factories. Phase A also has no
`post_init` chaining. Later work can extend the default-factory-with-parameters
model before considering any post-init style hook.

### Multi-Group From Day One

Do not implement a special single-transaction-group model.

The Phase A fixture should contain at least two transaction keys:

```text
DEFAULT_TRANSACTION -> tx_index 0
"audit"             -> tx_index 1
```

One-group behavior is just the degenerate case of the same generated metadata
and state layout.

### Current Setter Policy

Phase A should raise when assigning a transactional field through the current
facade:

```python
obj.current.count = 5  # raises for managed fields
```

The alternate behavior, where current assignment stages a working value, can
be a later class-wide option:

```text
current_setter_policy = "raise" | "stage_working"
```

The Phase A default is `"raise"` because `current` means committed/current
state, not transaction staging.

## Runtime Class Shape

For a decorated class, using `@lifecycle` here as the illustrative eventual
decorator name:

```python
@lifecycle
class Counter:
    plain: int = field(default=3)
    count: int = managed(tx_key=DEFAULT_TRANSACTION, default=1)
    audit_count: int = managed(tx_key="audit", default=10)
```

the generated source should have this broad shape:

```python
def build_lifecycle_class(
    decorated_cls,
    *,
    _Counter_lifecycle_definition,
    _Counter_annotations,
    _Counter_tx_keys,
    _Counter_plain_default,
    _Counter_count_default,
    _Counter_audit_count_default,
):
    class Counter_State:
        __slots__ = (
            "_y_transaction_manager",
            "_y_default_ref",
            "_y_current_ref",
            "_y_working_ref",
            "_y_plain_value",
            "_y_count_current",
            "_y_count_working",
            "_y_audit_count_current",
            "_y_audit_count_working",
            "_y_working_tx_ids",
        )

    class Counter_FacadeBase(decorated_cls):
        __slots__ = ("_y_state", "__weakref__")

        @property
        def default(self):
            return self._y_state._y_get_default_facade()

        @property
        def current(self):
            return self._y_state._y_get_current_facade()

        @property
        def working(self):
            return self._y_state._y_get_working_facade()

        def begin(self, *tx_keys):
            return self._y_state._y_transaction_manager.begin(*tx_keys)

        def validate(self, *tx_keys):
            return self._y_state._y_transaction_manager.validate(*tx_keys)

        def commit_only(self, *tx_keys):
            return self._y_state._y_transaction_manager.commit_only(*tx_keys)

        def commit(self, *tx_keys):
            return self._y_state._y_transaction_manager.commit(*tx_keys)

        def rollback(self, *tx_keys):
            return self._y_state._y_transaction_manager.rollback(*tx_keys)

    class Counter(Counter_FacadeBase):
        __slots__ = ()

        def __init__(
            self,
            *,
            transaction_manager=None,
            plain=_Counter_plain_default,
            count=_Counter_count_default,
            audit_count=_Counter_audit_count_default,
        ):
            state = object.__new__(Counter_State)
            object.__setattr__(self, "_y_state", state)
            state._y_transaction_manager = transaction_manager or TransactionManager(
                tx_keys=("audit",)
            )
            state._y_default_ref = weakref.ref(self)
            state._y_current_ref = None
            state._y_working_ref = None
            state._y_plain_value = plain
            state._y_count_current = count
            state._y_count_working = VOID
            state._y_audit_count_current = audit_count
            state._y_audit_count_working = VOID
            state._y_working_tx_ids = [None, None]

    class Counter_Current(Counter_FacadeBase):
        __slots__ = ()

    class Counter_Working(Counter_FacadeBase):
        __slots__ = ()

    Counter.__name__ = decorated_cls.__name__
    Counter.__qualname__ = decorated_cls.__qualname__
    Counter.__module__ = decorated_cls.__module__
    return Counter
```

The `build_lifecycle_class` boundary is intentionally unpacked. It should not
accept generic `defaults` or `default_factories` dictionaries.

The exact slot names should come from the generated naming layer. The important
shape is:

- a generated state/store class
- a generated facade base inheriting from the decorated class
- main/current/working facade classes inheriting from the facade base
- no call to the decorated class `__init__`
- direct state slot assignment during construction
- facade creation through state helper methods
- `_y_state` is the generated facade-to-state pointer name

Class-level generated metadata uses `__yidl_*__` names. Instance slots and
private generated helper methods use `_y_*` names.

## State And Facade Ownership

### Ownership Rules

1. Every facade holds a strong reference to the state object through `_y_state`.
2. The state object holds weak references to facades.
3. Facades do not need to hold strong references to other facades.
4. The state object owns all physical lifecycle data.
5. The state object is not a public facade.

### Weakref Cache Slots

The state should have one weakref slot per facade exposure:

```python
_y_default_ref: weakref.ReferenceType[Counter] | None
_y_current_ref: weakref.ReferenceType[Counter_Current] | None
_y_working_ref: weakref.ReferenceType[Counter_Working] | None
```

Phase A can use unannotated generated Python, but the semantics should be this
shape.

### Main Facade Construction

Normal user construction calls generated `Counter.__init__`, which:

1. allocates the state with `object.__new__(Counter_State)`
2. attaches the state to the main facade with `object.__setattr__`
3. initializes all state slots directly
4. creates the transaction manager if needed
5. stores a weak reference to the main facade

The state class does not need a normal public constructor.

The `_y_working_tx_ids` slot is a mutable list with length equal to the number
of transaction keys. It is indexed by `tx_index`.

### Secondary Facade Construction

The state get-or-create helpers construct facades without calling facade
`__init__`:

```python
def _y_get_current_facade(self):
    ref = self._y_current_ref
    facade = None if ref is None else ref()
    if facade is None:
        facade = object.__new__(Counter_Current)
        object.__setattr__(facade, "_y_state", self)
        self._y_current_ref = weakref.ref(facade)
    return facade
```

Equivalent generated helpers are needed for:

- `_y_get_default_facade`
- `_y_get_current_facade`
- `_y_get_working_facade`

When the main facade is requested from a secondary facade and the previous main
facade is gone, `_y_get_default_facade` recreates it with `object.__new__` and
sets `_y_state`. It must not run `Counter.__init__`.

### `default` Facade Exposure

All facades should expose:

```python
obj.default
obj.current
obj.working
```

On the main facade, `obj.default` returns `obj` when the weakref still points
to the same object. On secondary facades, `.default` returns the current main
facade object for the same state, creating it if necessary.

## Facade Exposure Facts

Facade identity, facade mode, and field exposure names should be separate
facts.

Suggested records:

```yidl
record FacadeClass {
    FacadeId
    FacadeKind
    FacadeMode
    FacadeClassName
    FacadeOrder
}

record FacadeExposure {
    OwnerFacadeId
    FieldName
    TargetFacadeId
    ExposureOrder
}
```

Seeded Phase A records:

```text
FacadeClass(base,    kind=base,    mode=base)
FacadeClass(default, kind=main,    mode=default)
FacadeClass(current, kind=current, mode=current)
FacadeClass(working, kind=working, mode=working)

FacadeExposure(default, "default", default)
FacadeExposure(default, "current", current)
FacadeExposure(default, "working", working)
FacadeExposure(current, "default", default)
FacadeExposure(current, "current", current)
FacadeExposure(current, "working", working)
FacadeExposure(working, "default", default)
FacadeExposure(working, "current", current)
FacadeExposure(working, "working", working)
```

The actual names can be refined, but the lowering should not hard-code
`.current` and `.working` as special strings outside the fact layer.

## Field Semantics

### `field`

Plain `field` is non-transactional instance state.

Phase A behavior:

- stored in one state slot
- visible from default, current, and working facades
- assignment from any facade writes the same state slot
- participates in constructor if `init=True`
- supports literal `default`
- zero-argument and parameterized `default_factory` can reuse the existing
  computed-default model if available in the fixture

### `managed`

`managed` is transactional value state.

Phase A behavior:

- each managed field belongs to exactly one transaction key
- each managed field receives a resolved `tx_index`
- state stores a current value
- state stores a working value
- a staged working value is present when the working value slot is not `VOID`
- default/main read:
  - working value if the working slot is not `VOID` for the field's tx index
  - otherwise current value
- current read:
  - current value only
- working read:
  - working value if the working slot is not `VOID`
  - otherwise current value
- default/main write:
  - requires an active transaction for the field's tx key
  - promotes/marks the state as dirty for that tx key
  - writes the working value
- current write:
  - raises for managed fields in Phase A
- working write:
  - same as default/main write

The current value should not be mutated until commit.

`managed(init=False, default=X)` does not create a constructor parameter; the
current slot is initialized to `X` during construction. Literal defaults are in
scope for Phase A. `managed(init=False, default_factory=...)` can follow once
default-factory initialization is added to the transaction fixture.

### `initvar`

Phase A supports initvars as constructor-only values.

Minimum behavior:

- `initvar(init=True)` appears in generated `__init__`
- `initvar(init=False)` rejects in Phase A unless a consumer use site exists
- initvars are available to default-factory parameter resolution if the
  existing computed-default model is used
- no post-init hook exists in Phase A
- retained initvars are out of scope unless required by a Phase A default
  factory test

### `classvar`

Phase A supports classvars as class-level materialized values.

Minimum behavior:

- no instance state slot
- no facade property
- materialized on the generated main class if needed
- inherited by current and working facades through normal class inheritance
- inherited/override behavior can be limited to simple own-class facts in the
  first fixture

## Transaction Fact Model

### Input Facts

Phase A field facts need at least:

```text
ClassId
FieldId
FieldOwner
FieldName
FieldKind
FieldOrder
Init
Annotation
HasDefault
Default
HasDefaultFactory
DefaultFactory
TxKeyKey
```

For non-transactional fields, `TxKeyKey` is absent or `None`.

For managed fields, omitted `TxKeyKey` resolves to `DEFAULT_TRANSACTION`.

### Derived Collections

Use a computed fact operation to derive transaction metadata:

```text
TransactionalFields
TxKeys
IndexedTransactionalFields
TxRuntimeSlots
```

Suggested records:

```yidl
record TransactionalField {
    FieldId
    FieldOwner
    FieldName
    TxKeyKey
    FieldOrder
}

record TxKey {
    ClassId
    TxKeyKey
    TxIndex
    TxKeyOrder
}

record IndexedTransactionalField {
    FieldId
    FieldOwner
    FieldName
    TxKeyKey
    TxIndex
    FieldOrder
}
```

`TxKeys` should always include `DEFAULT_TRANSACTION` at index `0`.
Additional groups are assigned stable indexes by first field declaration order.
For inheritance, parent groups keep their existing indexes and child-only groups
are appended in child declaration order.

Slot names for field storage are deterministic functions of final `FieldName`.
An inherited field and a compatible local redeclaration of the same field name
resolve to the same generated slot names.

### Generated Metadata

Generated state or facade classes should expose immutable class metadata:

```python
__yidl_tx_index_to_group__ = (DEFAULT_TRANSACTION, "audit")
__yidl_tx_key_to_index__ = {DEFAULT_TRANSACTION: 0, "audit": 1}
```

The `TransactionManager` constructor expects non-default groups in
`tx_keys`. Therefore generated construction should pass:

```python
TransactionManager(tx_keys=("audit",))
```

when it auto-creates a manager. For more non-default groups, the generated
constructor passes the deduplicated non-default groups in `tx_index` order. If
a caller supplies a manager, Phase A should use it directly and let the runtime
diagnose unknown transaction keys.

## Transaction Runtime Protocol

The generated state object should be the object enlisted into the transaction
manager.

The state must implement:

```python
def commit_order_key_for(self, tx_key=DEFAULT_TRANSACTION):
    return ()

def requires_validation_for(self, tx_key=DEFAULT_TRANSACTION):
    return False

def validate_commit_for(self, tx_key=DEFAULT_TRANSACTION):
    return True

def _commit_transaction(self, tx_id, tx_key=DEFAULT_TRANSACTION):
    ...

def _rollback_transaction(self, tx_id, tx_key=DEFAULT_TRANSACTION):
    ...
```

Phase A has no validators or ordering fields, so the first three methods are
fixed stubs.

### Enlistment

On the first working write for a tx index:

1. find the active transaction for the field's tx key
2. reject if no active transaction exists
3. reject if the state already has a working record for that tx index owned by
   a different tx id
4. enlist the state object in the manager for the group
5. store the returned tx id for the tx index
6. write the working value

The generated state should not enlist the public facade.

### Commit

`_commit_transaction(tx_id, tx_key)` should:

1. resolve `tx_index`
2. no-op if the stored working tx id for that index differs from `tx_id`
3. for every managed field in that tx index:
   - if the working slot is not `VOID`, copy working value to current value
   - clear working value to `VOID`
4. clear the tx id for that index
5. return the default facade

### Rollback

`_rollback_transaction(tx_id, tx_key)` should:

1. resolve `tx_index`
2. no-op if the stored working tx id for that index differs from `tx_id`
3. for every managed field in that tx index:
   - clear working value to `VOID`
4. clear the tx id for that index
5. return the default facade

## Inheritance And Re-Decoration

Phase A should record enough metadata to avoid confusing generated lifecycle
classes with user-authored declarations.

When decorating:

```python
@lifecycle
class A:
    v1: int = managed("tx1", default=1)

@lifecycle
class B(A):
    v2: int = managed("tx1", default=2)
```

the expected Python property remains:

```python
assert isinstance(B(), A)
```

This means generated `B` must keep generated `A` in its inheritance chain. We
should not physically remove generated `A` from the Python MRO in Phase A.

Instead, use semantic peeling:

1. Generated classes carry metadata:
   - `__yidl_lifecycle_generated__ = True`
   - `__yidl_lifecycle_user_class__ = <original decorated class>`
   - `__yidl_lifecycle_definition__ = <resolved definition/fact summary>`
2. The harvester reads current-class declarations from the class being
   decorated, preferably from `cls.__dict__`.
3. The harvester reads inherited lifecycle declarations from base
   `__yidl_lifecycle_definition__` metadata.
4. The harvester ignores inherited generated descriptors, state classes,
   facade classes, and lifecycle internals as new declarations.
5. The generated `B` gets a fresh state class and fresh facade classes.
6. Generated `B` explicitly shadows generated lifecycle properties for all
   merged fields, so inherited generated `A` machinery does not own `B` state.

The generated derived class must also re-emit all lifecycle facade-base
properties and methods (`default`, `current`, `working`, `begin`, `validate`,
`commit_only`, `commit`, and `rollback`) and all generated state helper
methods. Inheritance through the user MRO is preserved for user behavior and
`isinstance` semantics, not for reusing generated lifecycle internals.

For Phase A, `__yidl_lifecycle_definition__` should at least contain:

- resolved field facts needed to rebuild inherited fields:
  - field name
  - field kind
  - annotation
  - declaration order
  - init flag
  - literal default state
  - default-factory state
  - transaction key key for managed fields
- resolved transaction keys as `(tx_key, tx_index)` pairs
- facade exposure facts if they have been customized

The main generated facade class is the canonical home for this metadata.

Phase A does not need full override semantics. It should at least establish
metadata and avoid double-harvesting generated internals. A later slice can
add full MRO override diagnostics and compatibility rules.

## Generated Function Boundary

The generated function is decorator-private. It is not a user-facing API, so
its signature should be optimized for generated code size and decorator
runtime speed rather than generality.

The generated function should receive the decorated class plus materialized
static metadata and defaults as unpacked keyword-only parameters:

```python
def build_lifecycle_class(
    decorated_cls,
    *,
    _Counter_lifecycle_definition,
    _Counter_annotations,
    _Counter_tx_keys,
    _Counter_plain_default,
    _Counter_count_default,
    _Counter_audit_count_default,
):
    ...
    return Counter
```

The function may be generated for one resolved class/fact container, so it can
emit a literal class name such as `Counter`. The decorated class is still
passed in so the generated facades inherit user methods and attributes.

### Decorator Runtime Performance Notes

The current dataclass-like performance work showed that placing static
structure construction inside the generator function makes the decorator
runtime unnecessarily large and slow. Examples of static structure include:

- lifecycle definition metadata
- field/facade/transaction fact tables
- annotations and match/class metadata
- transaction key indexes
- pre-resolved property/resource names
- literal defaults and default factories

Phase A should push this work into the generated decorator module wherever
possible. The decorator can build static values once from harvested facts and
then call the generated function with explicit keyword arguments. The generated
function should avoid rebuilding static dictionaries, repeatedly calling helper
constructors for metadata rows, or indexing generic dictionaries such as
`defaults["Counter.count"]` in generated method signatures and bodies.

Prefer generated code shaped like:

```python
Counter = build_lifecycle_class(
    decorated_cls,
    _Counter_lifecycle_definition=Counter_lifecycle_definition,
    _Counter_annotations=Counter_annotations,
    _Counter_tx_keys=Counter_tx_keys,
    _Counter_plain_default=plain_default,
    _Counter_count_default=count_default,
    _Counter_audit_count_default=audit_count_default,
)
```

over a generic dictionary boundary. In particular, do not restore parameters
such as `defaults=...` or `default_factories=...`; default-factory support
should add explicit class/field-scoped keyword-only parameters such as
`_Counter_count_default_factory`.

This matters because YIDL will generate substantially more lifecycle code than
the current dataclass fixtures. Every static lookup or metadata construction
left inside `build_lifecycle_class` increases emitted AST size, source size,
compile time, and decorator runtime. The decorator boundary should therefore
move stable computation out of the runtime generator and pass already-resolved
objects directly.

Later decorator runtime can:

1. harvest facts from the decorated class
2. run the YIDL-generated builder for that class
3. build static metadata/default values in the decorator module
4. call `build_lifecycle_class(decorated_cls, _Counter_...=...)`
5. return the generated main facade class

Phase A should not require a fully general decorator cache or JIT story, but
the generated boundary should not preclude later caching of the generated AST
or decorator module.

## YIDL Source Shape

Suggested fixture path:

```text
tests/data/yidl/yidl_transactional_phase_a_base/lifecycle_base.yidl
```

The file should define one concept, tentatively:

```yidl
concept LifecycleBase {
    # field/facade/transaction schema
    # computed operations for facade exposure and tx indexing
    # resources for generated state, facade base, facades, properties,
    # transaction protocol, commit/rollback, and constructor
    # productions and assembly for one generated module/class
}
```

This can be split later. Phase A should prefer a working direct proof over
premature file layering.

## Required Computed Operations

### BuildFacadeFacts

Inputs:

```text
Facades
```

Outputs:

```text
FacadeClasses
FacadeExposures
```

Responsibilities:

- seed base/default/current/working facade classes
- seed `.default`, `.current`, `.working` exposures for all concrete facades
- preserve explicit user overrides later, but Phase A may use deterministic
  generated defaults

### BuildTransactionFacts

Inputs:

```text
Facades
Fields
```

Outputs:

```text
TransactionalFields
TxKeys
IndexedTransactionalFields
```

Responsibilities:

- select managed fields as transactional
- resolve omitted managed `TxKeyKey` to `DEFAULT_TRANSACTION`
- assign stable tx indexes
- write per-field tx indexes
- diagnose invalid transaction metadata

### BuildInitFacts

Inputs:

```text
Facades
Fields
InitVars
ClassVars
```

Outputs:

```text
InitParameters
InitAssignments
ClassVarAssignments
```

Responsibilities:

- generate constructor parameter facts
- generate direct state assignment facts
- preserve field declaration order
- integrate literal defaults
- optionally reuse existing default-factory dependency facts if available

If Phase A would become too large with parameterized default factories, keep
the first transactional golden on literal defaults and add factory support as
the next slice. Factory support should add explicit unpacked parameters such as
`_Counter_<field>_default_factory`; it should not reintroduce a generic
`default_factories` dictionary boundary.

## Generated Productions

At minimum, Phase A needs productions for:

1. Module root.
2. State class.
3. Facade base class.
4. Main facade class.
5. Current facade class.
6. Working facade class.
7. State get-or-create facade helpers.
8. Facade exposure properties.
9. Field properties per facade mode.
10. Main constructor.
11. Transaction control methods on the facade base.
12. Transaction protocol methods on state.
13. Commit and rollback bodies.
14. Build function wrapper.

The productions should be narrow enough that later features can add matcher
rules and contributions without replacing the whole class body.

## Golden Test Shape

Suggested golden source:

```text
tests/data/gold_src/yidl_transactional_phase_a_base.py
```

Suggested materialized outputs:

```text
tests/data/goldens/materialized/yidl_transactional_phase_a_base/decorator.py
tests/data/goldens/materialized/yidl_transactional_phase_a_base/decorator_prettier.py
tests/data/goldens/materialized/yidl_transactional_phase_a_base/generated_output.py
tests/data/goldens/materialized/yidl_transactional_phase_a_base/generated_output_prettier.py
```

The golden source should compile the YIDL file, emit the decorator/runtime
source, run it, generate the class output for a small fixture, and then execute
that generated output.

### Fixture Class

Use at least:

```python
class Counter:
    def user_method(self):
        return "user"
```

Fact data should represent:

```text
field plain: int = 3
managed count: int = 1, tx_key=DEFAULT_TRANSACTION
managed audit_count: int = 10, tx_key="audit"
initvar seed: int = 2
classvar KIND = "counter"
```

If initvar consumption is not ready, the Phase A fixture can include an
initvar-only schema/assertion but delay runtime use. Prefer using it in a
literal default computation only if that keeps the slice small.

### Runtime Assertions

The golden validation should assert:

1. `GeneratedCounter.__name__ == "Counter"`.
2. `GeneratedCounter.__qualname__` matches the decorated class qualname.
3. `GeneratedCounter.__module__` matches the decorated class module.
4. `isinstance(counter, DecoratedCounter)` is true.
5. `counter.user_method()` works.
6. `counter.default is counter`.
7. `counter.current.default is counter`.
8. `counter.working.default is counter`.
9. `counter.current is counter.current` is not required because weakref cache
   may recreate unreferenced secondary facades, but a held secondary facade is
   reused while strongly referenced.
10. Plain field reads/writes are visible across all facades.
11. Managed default/current/working reads start at the current value.
12. Managed write without active transaction raises.
13. During `DEFAULT_TRANSACTION`, writing `count` changes default/working
    view but not current view.
14. Rolling back `DEFAULT_TRANSACTION` restores default/working view to
    current value.
15. Committing `DEFAULT_TRANSACTION` publishes the working `count`.
16. During `"audit"`, writing `audit_count` does not affect `count`.
17. Committing `"audit"` publishes only `"audit"` group changes.
18. `counter.current.count = 99` raises for managed fields.
19. Generated tx metadata contains both default and audit groups.
20. Classvar materializes on the generated class and does not create an
    instance state slot.

### Inheritance Smoke Assertion

If small enough, include a second generated class fact set:

```python
class A:
    pass

GeneratedA = build_lifecycle_class(A, ...)

class B(GeneratedA):
    pass

GeneratedB = build_lifecycle_class(B, ...)

assert isinstance(GeneratedB(), GeneratedA)
```

This is a smoke check for the semantic-peeling direction, not full MRO merge
parity. If it makes the first golden too large, keep it as the immediate next
test after Phase A lands.

## Diagnostics

Phase A diagnostics should cover only the narrow invalid cases needed by the
base slice:

1. duplicate facade exposure name on one owner facade
2. unknown target facade in a facade exposure
3. managed field with invalid/missing transaction key metadata after
   defaulting
4. duplicate field name within one class
5. constructor parameter name collision
6. decorated class declares the reserved `_y_state` facade-state attribute
7. current setter policy rejects transactional current assignment at runtime

Do not add broad reserved-name diagnostics in Phase A. Those belong with the
later attribute/method collision slice.

## Expected Generated Shape For A3-A5

This section pins the generated Python shape for the first transactional
`Counter` fixture. The exact formatting can be controlled by the existing
golden/prettier pipeline, but the semantic source shape should match this
section closely.

### Imports And Sentinels

The generated output should import the YIDL-owned transaction runtime and
`weakref`:

```python
from __future__ import annotations

import weakref

from yidl.runtime.transaction_yidl import DEFAULT_TRANSACTION
from yidl.runtime.transaction_yidl import TransactionManager

VOID = object()
```

`VOID` is the only staged-working sentinel in Phase A. A managed field's
working value is absent when its working slot is `VOID`.

### State Class

For the fixture with `plain`, `count`, and `audit_count`, generated state slots
should be equivalent to:

```python
class Counter_State:
    __slots__ = (
        "_y_transaction_manager",
        "_y_default_ref",
        "_y_current_ref",
        "_y_working_ref",
        "_y_plain_value",
        "_y_count_current",
        "_y_count_working",
        "_y_audit_count_current",
        "_y_audit_count_working",
        "_y_working_tx_ids",
    )

    __yidl_tx_index_to_group__ = (DEFAULT_TRANSACTION, "audit")
    __yidl_tx_key_to_index__ = {DEFAULT_TRANSACTION: 0, "audit": 1}
```

State construction is performed by the main facade `__init__`, not by a public
state constructor:

```python
def __init__(
    self,
    *,
    transaction_manager=None,
    plain=_Counter_plain_default,
    count=_Counter_count_default,
    audit_count=_Counter_audit_count_default,
):
    state = object.__new__(Counter_State)
    object.__setattr__(self, "_y_state", state)
    state._y_transaction_manager = transaction_manager or TransactionManager(
        tx_keys=("audit",)
    )
    state._y_default_ref = weakref.ref(self)
    state._y_current_ref = None
    state._y_working_ref = None
    state._y_plain_value = plain
    state._y_count_current = count
    state._y_count_working = VOID
    state._y_audit_count_current = audit_count
    state._y_audit_count_working = VOID
    state._y_working_tx_ids = [None, None]
```

`_y_working_tx_ids` is a mutable list indexed by `tx_index`. Slot names are
derived from final field names, not owner class names.

### Facade Get-Or-Create Helpers

The state class should own one get-or-create helper for each facade exposure:

```python
def _y_get_default_facade(self):
    ref = self._y_default_ref
    facade = None if ref is None else ref()
    if facade is None:
        facade = object.__new__(Counter)
        object.__setattr__(facade, "_y_state", self)
        self._y_default_ref = weakref.ref(facade)
    return facade


def _y_get_current_facade(self):
    ref = self._y_current_ref
    facade = None if ref is None else ref()
    if facade is None:
        facade = object.__new__(Counter_Current)
        object.__setattr__(facade, "_y_state", self)
        self._y_current_ref = weakref.ref(facade)
    return facade


def _y_get_working_facade(self):
    ref = self._y_working_ref
    facade = None if ref is None else ref()
    if facade is None:
        facade = object.__new__(Counter_Working)
        object.__setattr__(facade, "_y_state", self)
        self._y_working_ref = weakref.ref(facade)
    return facade
```

These helpers must never call facade `__init__`.

### Facade Base

The shared facade base should inherit from the decorated class and expose the
facade fields and transaction controls:

```python
class Counter_FacadeBase(decorated_cls):
    __slots__ = ("_y_state", "__weakref__")

    @property
    def default(self):
        return self._y_state._y_get_default_facade()

    @property
    def current(self):
        return self._y_state._y_get_current_facade()

    @property
    def working(self):
        return self._y_state._y_get_working_facade()

    def begin(self, *tx_keys):
        return self._y_state._y_transaction_manager.begin(*tx_keys)

    def validate(self, *tx_keys):
        return self._y_state._y_transaction_manager.validate(*tx_keys)

    def commit_only(self, *tx_keys):
        return self._y_state._y_transaction_manager.commit_only(*tx_keys)

    def commit(self, *tx_keys):
        return self._y_state._y_transaction_manager.commit(*tx_keys)

    def rollback(self, *tx_keys):
        return self._y_state._y_transaction_manager.rollback(*tx_keys)
```

### Plain Field Properties

Plain fields are not transaction-aware. The same state slot is read and written
from all facades:

```python
def _y_get_plain(self):
    return self._y_state._y_plain_value


def _y_set_plain(self, value):
    self._y_state._y_plain_value = value
```

The generated property should be installed on default/current/working facade
classes. If Phase A emits duplicate getter/setter functions per facade for
simplicity, the behavior must still be identical.

### Managed Field Helpers

Phase A should generate direct helper methods on the state class rather than a
descriptor table. Helper names may vary, but the generated source should be
equivalent to:

```python
def _y_require_active_transaction(self, tx_index):
    tx_key = self.__yidl_tx_index_to_group__[tx_index]
    transaction = self._y_transaction_manager.active_transaction_for(tx_key)
    if transaction is None:
        if self._y_working_tx_ids[tx_index] is not None:
            raise RuntimeError(
                "stale yidl working value without an active transaction"
            )
        raise RuntimeError("writes require an active yidl transaction")
    existing_tx_id = self._y_working_tx_ids[tx_index]
    if existing_tx_id is not None and existing_tx_id != transaction.tx_id:
        raise RuntimeError("working value belongs to a different yidl transaction")
    return transaction


def _y_ensure_working_transaction(self, tx_index):
    transaction = self._y_require_active_transaction(tx_index)
    if self._y_working_tx_ids[tx_index] is None:
        tx_key = self.__yidl_tx_index_to_group__[tx_index]
        self._y_working_tx_ids[tx_index] = self._y_transaction_manager.enlist(
            self, tx_key
        )
    return transaction
```

Use these runtime error strings in Phase A tests unless implementation exposes
a better already-existing YIDL runtime diagnostic.

### Managed Field Properties

For a default-transaction managed field `count`, generated properties should be
equivalent to:

```python
def _y_get_count_default(self):
    state = self._y_state
    if state._y_count_working is not VOID:
        return state._y_count_working
    return state._y_count_current


def _y_set_count_default(self, value):
    state = self._y_state
    state._y_ensure_working_transaction(0)
    state._y_count_working = value


def _y_get_count_current(self):
    return self._y_state._y_count_current


def _y_set_count_current(self, value):
    del value
    raise AttributeError("current facade is read-only for transactional field count")


def _y_get_count_working(self):
    state = self._y_state
    if state._y_count_working is not VOID:
        return state._y_count_working
    return state._y_count_current


def _y_set_count_working(self, value):
    state = self._y_state
    state._y_ensure_working_transaction(0)
    state._y_count_working = value
```

For `audit_count`, the same shape is emitted with `tx_index == 1` and the
`_y_audit_count_*` slots.

### Transaction Protocol Methods

With no validators or commit-order fields, the state protocol methods should
be direct stubs plus generated commit/rollback logic:

```python
def commit_order_key_for(self, tx_key=DEFAULT_TRANSACTION):
    del tx_key
    return ()


def requires_validation_for(self, tx_key=DEFAULT_TRANSACTION):
    del tx_key
    return False


def validate_commit_for(self, tx_key=DEFAULT_TRANSACTION):
    del tx_key
    return True


def _commit_transaction(self, tx_id, tx_key=DEFAULT_TRANSACTION):
    tx_index = self.__yidl_tx_key_to_index__[tx_key]
    if self._y_working_tx_ids[tx_index] != tx_id:
        return self._y_get_default_facade()
    if tx_index == 0:
        if self._y_count_working is not VOID:
            self._y_count_current = self._y_count_working
            self._y_count_working = VOID
    elif tx_index == 1:
        if self._y_audit_count_working is not VOID:
            self._y_audit_count_current = self._y_audit_count_working
            self._y_audit_count_working = VOID
    self._y_working_tx_ids[tx_index] = None
    return self._y_get_default_facade()


def _rollback_transaction(self, tx_id, tx_key=DEFAULT_TRANSACTION):
    tx_index = self.__yidl_tx_key_to_index__[tx_key]
    if self._y_working_tx_ids[tx_index] != tx_id:
        return self._y_get_default_facade()
    if tx_index == 0:
        self._y_count_working = VOID
    elif tx_index == 1:
        self._y_audit_count_working = VOID
    self._y_working_tx_ids[tx_index] = None
    return self._y_get_default_facade()
```

The implementation may emit per-group helper functions instead of `if/elif`
inside the protocol methods if that is cleaner for Astichi composition. The
observable source must still be specialized to known `tx_index` values and
must not use generic descriptor tables.

## Implementation Slices

### Slice A1: Source And Schema Skeleton

Deliverables:

- `lifecycle_base.yidl` with field, facade, transaction, and init records
- direct-resource operations for the Phase A computed facts
- no matcher-selected operation dispatch in Phase A
- no new YIDL grammar is expected; if implementation discovers a grammar need,
  stop and propose the grammar change before continuing
- no generated runtime behavior yet

Verification:

- YIDL source parses
- compiled concept exposes expected schema objects

### Slice A2: Transaction Index Computed Facts

Deliverables:

- `BuildTransactionFacts` operation
- `TxKeys` and `IndexedTransactionalFields`
- diagnostics for invalid tx metadata

Verification:

- golden or focused fixture shows:
  - `DEFAULT_TRANSACTION` index `0`
  - `"audit"` index `1`
  - managed fields carry the expected tx indexes

### Slice A3: Generated Class Skeleton And Facade Cache

Deliverables:

- generated build function
- generated state class
- generated facade base
- generated default/current/working classes
- weakref get-or-create methods
- `.default`, `.current`, `.working` properties

Verification:

- generated code executes
- facades inherit decorated class behavior
- facade identity and weakref cache behavior pass runtime assertions

### Slice A4: Plain Field, Initvar, Classvar

Deliverables:

- plain field state slot and properties
- constructor parameter/assignment for plain fields
- classvar materialization
- initvar schema and minimal constructor participation

Verification:

- non-transactional field reads/writes through all facades
- classvar exists on generated class
- initvar facts do not create facade field properties

### Slice A5: Managed Field Transaction Semantics

Deliverables:

- managed field current/working slots
- managed property resources for default/current/working modes
- active transaction checks
- state enlistment
- commit/rollback protocol methods
- transaction control methods on facade base

Verification:

- begin/write/rollback
- begin/write/commit
- independent two-group behavior
- current setter rejection for managed fields

### Slice A6: Generated Decorator Boundary And Metadata

Deliverables:

- generated class metadata:
  - `__yidl_lifecycle_generated__`
  - `__yidl_lifecycle_user_class__`
  - `__yidl_lifecycle_definition__`
- decorator-private build-function shape that accepts decorated class and
  unpacked static/default values
- static lifecycle metadata assembled in the decorator module, not rebuilt in
  the generated class builder
- initial semantic-peeling helper or documented stub

Verification:

- generated class preserves public identity
- generated builder source avoids generic default dictionary lookups in method
  signatures and bodies
- inherited generated base smoke check if included
- no generated class depends on `pyrolyze`

## Roll-Build Candidate Assessment

This plan is a roll-build candidate only after the YIDL source shape is stable
enough to keep each slice independently verifiable.

Recommended roll-build checkpoints:

1. `txbase/A1-schema`
2. `txbase/A2-tx-facts`
3. `txbase/A3-facades`
4. `txbase/A4-plain-init-class`
5. `txbase/A5-managed-tx`
6. `txbase/A6-decorator-metadata`

Do not roll directly into `transient`, `owned`, `binding`, validators, hooks,
or full MRO override parity until Phase A generated transaction behavior is
green.

## Open Questions For Later Phases

These are intentionally not blockers for Phase A:

1. Should current-facade assignment to transactional fields support a
   `"stage_working"` class option?
2. How strict should reserved-name diagnostics be for decorated classes?
3. Should the generated decorator auto-create a transaction manager by
   default, or should explicit shared-manager injection remain the primary
   public shape?
4. How much parameterized `default_factory` inheritance should be supported
   before introducing any post-init-like hook?
5. How should full MRO field override compatibility diagnostics report base
   and derived provenance?
6. Should transaction support later split from `lifecycle_base.yidl` into a
   feature concept once Phase A is proven?
