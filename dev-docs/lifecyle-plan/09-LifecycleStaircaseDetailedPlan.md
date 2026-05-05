# Lifecycle Staircase Detailed Plan

## Goal

Define the first generated lifecycle subset and its roll-build path.

This is the concrete use case that proves the DDS features are sufficient. It
should be small enough to build, but broad enough to force the important
architecture:

- schema family
- layered merge
- transaction index
- generated resources
- diagnostics
- operation contributions
- state/facade split
- generated class source

## First Supported Subset

The first staircase supports:

- `managed` fields
- `const` fields
- constructor defaults
- one or more transaction groups
- state class
- direct main facade class
- current and working value slots
- property getter/setter
- simple commit
- simple rollback
- close hook placeholder

The first staircase does not support:

- binding/owned resources
- transient fields
- local/derived stores
- initvar retention
- hooks/validators/order keys
- multiple facades
- MRO merge beyond one base plus one derived layer

Those come after the architecture is proven.

## Roll-Build Slices

### Slice A: Field Family Input

Define records:

```python
ManagedField
ConstField
FieldSpecs
MergedFields
```

Input:

```python
count = ManagedField(
    name="count",
    annotation=int,
    source_order=0,
    source_label="Example.count",
    kind=MANAGED_KIND,
    declaration_space=INSTANCE_FIELD,
    tx_group="default_transaction",
    default=0,
    default_factory=None,
    initial_working=None,
    freeze=None,
    thaw=None,
)

label = ConstField(
    name="label",
    annotation=str,
    source_order=1,
    source_label="Example.label",
    kind=CONST_KIND,
    declaration_space=INSTANCE_FIELD,
    default="x",
    default_factory=None,
)
```

Golden checks computed views:

```text
StoredFields: count, label
TransactionalFields: count
ConstFields: label
```

### Slice B: Transaction Index

Add:

```python
TxGroups
IndexedFields
```

Expected result:

```text
TxGroups: default_transaction=0
IndexedFields: count(tx_index=0)
```

### Slice C: State Slots

Produce state slot records:

```python
StateSlot(
    name="_count_current",
    field_name="count",
    role=CURRENT_VALUE,
    order=0,
)

StateSlot(
    name="_count_working",
    field_name="count",
    role=WORKING_VALUE,
    order=1,
)

StateSlot(
    name="_label_value",
    field_name="label",
    role=PUBLISHED_VALUE,
    order=2,
)
```

Expected class slot golden:

```python
class ExampleState:
    __slots__ = (
        "_count_current",
        "_count_working",
        "_label_value",
    )
```

### Slice D: Init Parameters And Body

Produce:

```python
InitParam(name="count", annotation=int, default=0)
InitParam(name="label", annotation=str, default="x")
InitStatement(template=AssignCurrentValue, bindings={...})
```

Expected golden:

```python
class ExampleState:
    def __init__(self, *, count: int = 0, label: str = "x"):
        self._count_current = count
        self._count_working = _NO_WORKING_VALUE
        self._label_value = label
```

If annotation/default values are not source-emittable as literals, bind them as
generated resources or module constants.

### Slice E: Facade Init

Produce main facade class:

```python
class Example:
    __slots__ = ("_state",)

    def __init__(self, *, count: int = 0, label: str = "x"):
        self._state = ExampleState(count=count, label=label)
```

The facade init can share parameter records with the state init but has a
different body template.

### Slice F: Properties

Managed getter/setter:

```python
@property
def count(self):
    state = self._state
    if state._count_working is not _NO_WORKING_VALUE:
        return state._count_working
    return state._count_current

@count.setter
def count(self, value):
    self._state._count_working = value
```

Const getter:

```python
@property
def label(self):
    return self._state._label_value
```

No setter for const.

### Slice G: Commit And Rollback

Simple transaction behavior:

```python
def commit(self):
    state = self._state
    if state._count_working is not _NO_WORKING_VALUE:
        state._count_current = state._count_working
        state._count_working = _NO_WORKING_VALUE

def rollback(self):
    self._state._count_working = _NO_WORKING_VALUE
```

This does not yet implement transaction manager integration. It proves operation
contribution assembly.

## Proposed DDS Records

### Core Input Records

```python
FieldSpecs
MergedFields
IndexedFields
TxGroups
```

### Generated Class Records

```python
GeneratedClass(
    class_role=STATE_CLASS,
    class_name="ExampleState",
    storage_root=None,
)

GeneratedClass(
    class_role=MAIN_FACADE,
    class_name="Example",
    storage_root=StateRoot("_state"),
)
```

### Contribution Records

```python
StateSlot
InitParam
InitStatement
ClassComponent
PropertyComponent
OperationContribution
```

## Fluent Concept Sketch

```python
builder = CapsuleConceptBuilder("LifecycleManagedConst")

Core = builder.extends(LifecycleCoreConcept)
Fields = builder.extends(FieldFamilyConcept)
Tx = builder.extends(TransactionIndexConcept)
State = builder.extends(StateClassConcept)
Facade = builder.extends(MainFacadeConcept)

PropertyTemplate = builder.matchers.PropertyTemplate()
field = PropertyTemplate.input.field(Fields.collections.IndexedFields)

PropertyTemplate.rule.managed(
    when=(field.prop(Fields.props.Kind).eq(MANAGED_KIND),),
    resource=from_astichi_template(
        """
        astichi_comment("property template: managed value")

        @property
        def field_name__astichi_arg__(self):
            state = self._state
            if state.astichi_ref(external=working_slot) is not _NO_WORKING_VALUE:
                return state.astichi_ref(external=working_slot)
            return state.astichi_ref(external=current_slot)

        @field_name__astichi_arg__.setter
        def field_name__astichi_arg__(self, value):
            self._state.astichi_ref(external=working_slot)._ = value
        """
    ),
)

PropertyTemplate.rule.const(
    when=(field.prop(Fields.props.Kind).eq(CONST_KIND),),
    resource=from_astichi_template(
        """
        astichi_comment("property template: const value")

        @property
        def field_name__astichi_arg__(self):
            return self._state.astichi_ref(external=published_slot)
        """
    ),
)
```

`state.astichi_ref(...)` and assignment through `astichi_ref(...)._` are proven
Astichi surfaces in `astichi/tests/data/gold_src/lifecycle_template_surfaces.py`.
Do not replace them with fragile string concatenation.

## Expected Full Generated Source Golden

Expected excerpt for
`tests/data/goldens/materialized/dds_lifecycle_managed_const_staircase.py`:

```python
_NO_WORKING_VALUE = object()


class ExampleState:
    __slots__ = (
        "_count_current",
        "_count_working",
        "_label_value",
    )

    def __init__(self, *, count: int = 0, label: str = "x"):
        self._count_current = count
        self._count_working = _NO_WORKING_VALUE
        self._label_value = label


class Example:
    __slots__ = ("_state",)

    def __init__(self, *, count: int = 0, label: str = "x"):
        self._state = ExampleState(count=count, label=label)

    @property
    def count(self):
        state = self._state
        if state._count_working is not _NO_WORKING_VALUE:
            return state._count_working
        return state._count_current

    @count.setter
    def count(self, value):
        self._state._count_working = value

    @property
    def label(self):
        return self._state._label_value

    def commit(self):
        state = self._state
        if state._count_working is not _NO_WORKING_VALUE:
            state._count_current = state._count_working
            state._count_working = _NO_WORKING_VALUE

    def rollback(self):
        self._state._count_working = _NO_WORKING_VALUE
```

This golden is intentionally small and direct. Later slices can replace
`commit()` and `rollback()` with transaction-manager-aware methods.

## Runtime Behavior Test

The runtime test should execute the generated class:

```python
obj = Example(count=1, label="a")
assert obj.count == 1
assert obj.label == "a"

obj.count = 2
assert obj.count == 2

obj.rollback()
assert obj.count == 1

obj.count = 3
obj.commit()
assert obj.count == 3

try:
    obj.label = "b"
except AttributeError:
    pass
else:
    raise AssertionError("const label should be read-only")
```

## Golden Source Driver

Suggested `tests/data/gold_src/dds_lifecycle_managed_const_staircase.py` shape:

```python
from yidl.generation import DataDefinitionSystem
from yidl.capsule.lifecycle_concepts import build_lifecycle_managed_const_concept


def build():
    concept = build_lifecycle_managed_const_concept()
    runtime = concept.build_runtime()
    builder = runtime.new_builder()

    builder.add_managed_field(
        name="count",
        annotation=int,
        default=0,
        tx_group="default_transaction",
    )
    builder.add_const_field(
        name="label",
        annotation=str,
        default="x",
    )

    container = runtime.run(builder)
    return runtime.render_module(container, class_name="Example")
```

The exact helper names may differ. The key rule is that the source uses
concept/runtime APIs, not ad hoc class string generation.

## Diagnostics For First Staircase

Required failure modes:

- duplicate field name in one layer
- const field with setter contribution
- managed field without transaction group
- missing state slot for property template binding
- template binding missing required slot path
- unsupported annotation/default source value

These should be bespoke failure tests unless a diagnostic success source is
useful as a golden.

## Implementation Notes

The staircase should be implemented after enough generic features exist. It
should not add new DDS features unless the feature is truly generic.

If the implementation needs to manually do:

```python
for field in fields:
    source += f"...{field.name}..."
```

stop and replace that with:

- a field record
- a matcher-selected generated resource
- a production into a contribution collection
- a renderer that consumes contribution records

## Test Plan

Goldens:

- `tests/data/gold_src/dds_lifecycle_managed_const_staircase.py`
- `tests/data/goldens/materialized/dds_lifecycle_managed_const_staircase.py`

Runtime:

- generated class init/get/set/commit/rollback
- const read-only property
- working value rolls back
- working value commits

Bespoke:

- duplicate field diagnostic
- missing slot binding diagnostic
- invalid template resource diagnostic

## Exit Criteria

The staircase is complete when:

- generated source matches the golden
- runtime behavior passes
- no generated runtime path imports `pyrolyze`
- no generated decorator/runtime path calls the Python parser
- state owns storage and facade owns behavior
- managed/const behavior is produced through records, matchers, productions,
  ports, and generated resources
