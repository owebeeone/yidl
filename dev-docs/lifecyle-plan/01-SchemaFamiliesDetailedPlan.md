# Schema Families Detailed Plan

## Goal

Make lifecycle declarations expressible as one coherent DDS union family instead
of scattered helper-specific collections.

Critical review status: schema families are fluent/concept-layer ergonomics in
V1. They lower to existing `UnionSpec.variant(...)` calls. Do not add
`UnionSpec.common(...)` to DDS core unless the fluent helper proves insufficient
in more than one concept builder.

This feature addresses:

- stored fields
- initvars
- classvars
- hook declarations
- validators
- order keys
- future resource field kinds

The feature is a DDS ergonomics improvement over existing `UnionSpec`. It is
not a new YIDL `FieldSpec` runtime.

## Problem

Lifecycle declarations share common facts:

- name
- source order
- source label
- annotation
- helper/kind identity
- declaration space

They also have variant facts:

- managed fields have transaction group, compare mode, defaults, freeze/thaw
- initvars have constructor-only defaults/factories
- classvars have class materialization behavior
- hooks have phase and callable
- validators/order keys have transaction group and callable
- binding/owned fields have resource-policy facts

Today DDS can define a union and variants, but common property repetition is
boilerplate-heavy. That encourages helper-specific record shapes and later
normalization code. The lifecycle generator needs the opposite: one data family
with coherent views.

## Proposed Fluent API

The preferred API is a concept-builder schema-family helper. It records common
properties and variant declarations, then lowers to ordinary
`UnionSpec.variant(...)` calls when the concept is replayed.

```python
concept = CapsuleConceptBuilder("LifecycleFieldFamily")

Name = concept.props.Name(str, REQUIRED)
Annotation = concept.props.Annotation(object, REQUIRED)
SourceOrder = concept.props.SourceOrder(int, REQUIRED, storage_name="source_order")
SourceLabel = concept.props.SourceLabel(str, "")
Kind = concept.props.Kind(object, REQUIRED)
DeclarationSpace = concept.props.DeclarationSpace(object, REQUIRED)

TxGroup = concept.props.TxGroup(object, "default_transaction")
Default = concept.props.Default(object, REQUIRED)
DefaultFactory = concept.props.DefaultFactory(object, None)
InitialWorking = concept.props.InitialWorking(object, None)
Freeze = concept.props.Freeze(object, None)
Thaw = concept.props.Thaw(object, None)
HookPhase = concept.props.HookPhase(object, REQUIRED)

FieldSpecs = concept.schema_family("FieldSpecs")
FieldSpecs.common(Name, Annotation, SourceOrder, SourceLabel, Kind, DeclarationSpace)

ManagedField = FieldSpecs.variant(
    "ManagedField",
    TxGroup,
    Default,
    DefaultFactory,
    InitialWorking,
    Freeze,
    Thaw,
)

ConstField = FieldSpecs.variant(
    "ConstField",
    Default,
    DefaultFactory,
)

InitVarField = FieldSpecs.variant(
    "InitVarField",
    Default,
    DefaultFactory,
)

ClassVarField = FieldSpecs.variant(
    "ClassVarField",
    Default,
    DefaultFactory,
)

HookField = FieldSpecs.variant(
    "HookField",
    TxGroup,
    HookPhase,
    Default,
)
```

The lowered DDS shape is still:

```python
FieldSpecs = dds.union("FieldSpecs")
ManagedField = FieldSpecs.variant(
    "ManagedField",
    Name,
    Annotation,
    SourceOrder,
    SourceLabel,
    Kind,
    DeclarationSpace,
    TxGroup,
    Default,
    DefaultFactory,
    InitialWorking,
    Freeze,
    Thaw,
)
```

`UnionSpec.common(...)` is only a possible later promotion if more than one
fluent/concept builder needs the same helper and replay lowering becomes
duplicated.

### Semantics

`concept.schema_family(...).common(...)` records common properties to include in every later
variant. It does not create a base record class and it does not create
inheritance at runtime. It is definition-time sugar.

This:

```python
FieldSpecs.common(Name, SourceOrder)
ManagedField = FieldSpecs.variant("ManagedField", TxGroup)
```

is equivalent to:

```python
ManagedField = FieldSpecs.variant("ManagedField", Name, SourceOrder, TxGroup)
```

but the common list is checked consistently.

### Duplicate Handling

- A property repeated in `common(...)` and a variant is accepted only if it is
  the same `PropertySpec` object.
- A property with the same name but incompatible type/default/storage rejects.
- Calling `common(...)` after variants exist is allowed only if the new common
  properties can be appended to every existing variant without conflict.
- Variant property order is: common properties in common declaration order,
  then variant-specific properties in variant declaration order.

This ordering matters because generated record constructors and golden output
must be stable.

## Data-Driven Access

The recorded concept builder should expose properties by semantic name after
definition.

```python
ClassFields = builder.extends(ClassFieldSchemaConcept)

Name = ClassFields.props.Name
SourceOrder = ClassFields.props.SourceOrder
ManagedField = ClassFields.records.ManagedField
FieldSpecs = ClassFields.unions.FieldSpecs
```

Only one concept should define `Name`. Other concepts should reference it
through the concept they extend. If a concept tries to redefine `Name`
incompatibly, replay rejects.

## Expected Use Case

The initial lifecycle field family should support this data:

```python
builder = dds.container_builder()

builder.add(
    ManagedField(
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
)

builder.add(
    InitVarField(
        name="seed",
        annotation=int,
        source_order=1,
        source_label="Example.seed",
        kind=INITVAR_KIND,
        declaration_space=INITVAR_SPACE,
        default=REQUIRED,
        default_factory=None,
    )
)
```

Computed views then classify the records:

```python
StoredFields = dds.computed_collection(
    "StoredFields",
    source=FieldSpecs,
    when=(DeclarationSpace.eq(INSTANCE_FIELD),),
)

InitVars = dds.computed_collection(
    "InitVars",
    source=FieldSpecs,
    when=(DeclarationSpace.eq(INITVAR_SPACE),),
)
```

## Expected Generated Source Golden

The generated container source should not rebuild the schema with
`DataDefinitionSystem()` calls. It should contain direct runtime record classes
and collection helpers.

Expected excerpt for `tests/data/goldens/materialized/dds_lifecycle_field_family.py`:

```python
REQUIRED = _RequiredSentinel()

class ManagedField:
    __slots__ = (
        "name",
        "annotation",
        "source_order",
        "source_label",
        "kind",
        "declaration_space",
        "tx_group",
        "default",
        "default_factory",
        "initial_working",
        "freeze",
        "thaw",
    )

    __annotations__ = {
        "name": str,
        "annotation": object,
        "source_order": int,
        "source_label": str,
        "kind": object,
        "declaration_space": object,
        "tx_group": object,
        "default": object,
        "default_factory": object,
        "initial_working": object,
        "freeze": object,
        "thaw": object,
    }

    def __init__(
        self,
        *,
        name: str,
        annotation: object,
        source_order: int,
        source_label: str = "",
        kind: object,
        declaration_space: object,
        tx_group: object = "default_transaction",
        default: object = REQUIRED,
        default_factory: object = None,
        initial_working: object = None,
        freeze: object = None,
        thaw: object = None,
    ):
        object.__setattr__(self, "name", name)
        object.__setattr__(self, "annotation", annotation)
        object.__setattr__(self, "source_order", source_order)
        object.__setattr__(self, "source_label", source_label)
        object.__setattr__(self, "kind", kind)
        object.__setattr__(self, "declaration_space", declaration_space)
        object.__setattr__(self, "tx_group", tx_group)
        object.__setattr__(self, "default", default)
        object.__setattr__(self, "default_factory", default_factory)
        object.__setattr__(self, "initial_working", initial_working)
        object.__setattr__(self, "freeze", freeze)
        object.__setattr__(self, "thaw", thaw)

    def __setattr__(self, name, value):
        raise AttributeError("ManagedField records are immutable")


class InitVarField:
    __slots__ = (
        "name",
        "annotation",
        "source_order",
        "source_label",
        "kind",
        "declaration_space",
        "default",
        "default_factory",
    )
    ...


class Container:
    def StoredFields(self):
        return (
            record
            for record in self.FieldSpecs
            if getattr(record, "declaration_space", NOT_PROVIDED) is INSTANCE_FIELD
        )

    def InitVars(self):
        return (
            record
            for record in self.FieldSpecs
            if getattr(record, "declaration_space", NOT_PROVIDED) is INITVAR_SPACE
        )
```

The exact class names can follow current generated-container naming, but the
golden must prove:

- common properties are present in every variant
- variant-specific properties are not present in other variants
- computed views use `getattr(..., NOT_PROVIDED)` for union-safe access
- no source-time DDS construction appears in the generated runtime module

## Diagnostics

Required errors:

- duplicate common property with incompatible definition
- common property added after variant conflicts with existing variant property
- variant with no common properties is allowed
- variant names are unique within a union
- property storage names are unique within a final variant record

Example error:

```text
FieldSpecs variant ManagedField cannot add property Name: storage name 'name'
already belongs to incompatible property OtherName
```

## Implementation Notes

The smallest implementation is likely:

- add concept-builder recording for `schema_family(...)`
- store common properties in the recorded concept plan
- lower each family variant to an ordinary `UnionSpec.variant(...)` replay call
  with common properties prepended
- keep generated runtime emission unchanged because the lowered variant records
  already include common properties

Do not add `UnionSpec.common(...)` as the first implementation. Promote it only
if multiple independent concept builders duplicate the family-lowering helper.

If the current `UnionSpec.variant(...)` already validates property conflicts,
reuse that path. Do not add a separate validation path for common properties.

## Test Plan

Bespoke:

- `test_union_common_properties_are_added_to_variants`
- `test_union_common_rejects_incompatible_duplicate_storage`
- `test_union_common_after_variant_replays_to_existing_variants`
- `test_union_variant_specific_property_absent_from_other_variant`

Goldens:

- `tests/data/gold_src/dds_lifecycle_field_family.py`
- `tests/data/goldens/materialized/dds_lifecycle_field_family.py`

The golden should construct at least:

- one managed field
- one initvar
- one classvar
- one hook declaration

and print or assert the computed view membership.
