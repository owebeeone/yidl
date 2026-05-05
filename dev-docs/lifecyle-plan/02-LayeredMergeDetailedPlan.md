# Layered Merge Detailed Plan

## Goal

Support MRO-like inherited declaration merging using generic DDS productions and
write policies.

Critical review status: `dds.layered_merge(...)` is not a V1 DDS-core API. This
document describes the lifecycle-layer convenience semantics. The initial
implementation should lower layered merge to `dds.operation(...)` with ordered
inputs, declared outputs, and a generated merge resource.

This feature lets lifecycle concepts merge field specs from base classes and the
current class without embedding MRO-specific logic in DDS core.

## Problem

The lifecycle backend needs to combine declarations from multiple ordered
layers:

1. oldest base class layer
2. later base class layers
3. current class layer

Same-name declarations may replace base declarations only when an override
policy allows it. Override validation may inspect annotation, kind, declaration
space, and helper-specific facts.

Existing `write(...)` policies decide what to do with duplicates inside one
builder. They do not describe ordered source layers or provide source context
for override diagnostics.

## Operation-First API

Represent layered merge as an aggregate generated operation. A lifecycle fluent
helper may wrap this later, but the initial DDS surface is `dds.operation(...)`.

```python
ClassLayer = dds.record(
    "ClassLayer",
    LayerIndex,
    LayerName,
    LayerFields,
)

MergedFields = dds.collection(
    "MergedFields",
    FieldSpecs,
    identity=Name,
)

dds.operation(
    "MergeFieldSpecs",
    inputs=(LayerFields,),
    outputs=(MergedFields,),
    order_by=(LayerIndex, SourceOrder),
    resource=MergeFieldSpecsOperation,
)
```

The operation resource owns the merge loop and writes `MergedFields` through the
configured write policy.

### Optional Fluent Helper

```python
concept.operations.layered_merge(
    "MergeFieldSpecs",
    source=LayerFields,
    target=MergedFields,
    order_by=(LayerIndex, SourceOrder),
    policy=field_override_policy,
)
```

This helper is fluent/concept sugar. It lowers to `dds.operation(...)` and must
not introduce a second runner.

## Layer Record Shape

The lifecycle generator should not ask DDS to inspect Python MRO. It should
feed DDS layer records.

```python
ClassLayer = dds.record(
    "ClassLayer",
    LayerIndex,
    LayerName,
    FieldRecords,
)
```

Generated decorator code harvests base class metadata and current class
metadata, then writes:

```python
builder.add(
    ClassLayer(
        layer_index=0,
        layer_name="Base",
        field_records=(Base_count_field, Base_label_field),
    )
)

builder.add(
    ClassLayer(
        layer_index=1,
        layer_name="Example",
        field_records=(Example_count_field, Example_owner_field),
    )
)
```

If storing `field_records` as a tuple of record objects is awkward in current
DDS, use a flat layer-field record instead:

```python
LayerField = dds.record(
    "LayerField",
    LayerIndex,
    LayerName,
    FieldRecord,
)
```

The flat record is preferred for source emission because generated code can
iterate one collection without nested tuple handling.

## Override Policy API

Layered merge uses a semantic policy object, not a string tag.

```python
class FieldOverridePolicy:
    def merge(self, existing, incoming, *, layer, diagnostics):
        ...
```

V1 can use a function-like policy resource:

```python
field_override_policy = OverridePolicy.from_astichi_code(
    """
    astichi_pyimport(module="yidl.generation.lifecycle_merge", names=("merge_field_override",))
    merge_field_override
    """
)
```

However, if policy resources are not ready yet, the generated runtime may call a
named helper passed through a source-name map:

```python
concept.operations.layered_merge(..., policy=merge_field_override)
```

The policy returns one of:

- keep existing
- replace with incoming
- raise diagnostic/error

Do not encode these as strings in user-facing APIs. If an internal enum-like
implementation is needed, keep it private.

## Override Semantics For V1

Use this precise behavior for the first implementation:

- Layers are processed by ascending `LayerIndex`.
- Within a layer, source records keep their declaration order.
- Target identity is `Name` unless explicitly configured otherwise.
- If target identity is new, incoming is written.
- If target identity exists, call policy with existing and incoming.
- If policy returns replacement, new record replaces old record.
- If policy rejects, the merge writes a diagnostic or raises immediately.
- If two records with the same identity appear in the same layer, policy still
  handles it. The diagnostic should mention same-layer duplicate.

## Expected Use Case

```python
concept.operations.layered_merge(
    "MergeLifecycleFields",
    source=FieldRecord,
    target=MergedFields,
    order_by=(LayerIndex, SourceOrder),
    policy=LifecycleFieldOverride,
)

dds.production_group("Merge", MergeLifecycleFields)
```

Input:

```python
builder.add(LayerField(layer_index=0, layer_name="Base", field=Base_count))
builder.add(LayerField(layer_index=1, layer_name="Example", field=Example_count))
builder.add(LayerField(layer_index=1, layer_name="Example", field=Example_owner))
```

Output:

```python
container.MergedFields.sequence()
# count from Example
# owner from Example
```

## Expected Generated Source Golden

Expected excerpt for `tests/data/goldens/materialized/dds_lifecycle_layered_merge.py`:

```python
def merge_lifecycle_fields(ctx):
    records = sorted(
        ctx.records(LayerFieldsCollection),
        key=lambda record: (record.layer_index, record.source_order),
    )
    for layer_field in records:
        incoming = layer_field.field
        existing = ctx.matching(MergedFieldsCollection, incoming.name)
        if existing is NOT_PROVIDED:
            ctx.write(MergedFieldsCollection, incoming, policy=RejectDuplicate)
            continue
        replacement = merge_field_override(
            existing,
            incoming,
            layer_name=layer_field.layer_name,
        )
        if replacement is existing:
            continue
        ctx.write(MergedFieldsCollection, replacement, policy=ReplaceExisting)


def run_operations(ctx):
    merge_lifecycle_fields(ctx)
    return ctx.freeze()
```

The exact `matching(...)` API can follow current container naming. The golden
must show:

- stable sorting by layer and source order
- policy call with existing/incoming records
- replace through `ReplaceExisting`
- no direct MRO inspection
- no dependency on `pyrolyze`

## Diagnostics

Required diagnostic cases:

- missing layer order property
- missing field record
- target collection without identity
- policy rejects override
- policy returns an invalid object
- incompatible field variant replacement

Example error:

```text
MergeLifecycleFields rejected override for field 'count' in layer 'Example':
ManagedField cannot override InitVarField
```

## Implementation Notes

Implement layered merge as an aggregate generated operation. That allows source
emission to reuse the generated operation machinery.

Potential internal types:

```python
LayeredMergeSpec
```

Avoid exposing a public `dds.layered_merge(...)` unless repeated concept usage
proves the fluent helper belongs in the public API.

## Test Plan

Bespoke:

- `test_layered_merge_processes_layers_in_order`
- `test_layered_merge_calls_policy_for_duplicate_identity`
- `test_layered_merge_rejects_policy_invalid_return`
- `test_layered_merge_reports_layer_name_in_diagnostic`
- `test_layered_merge_rejects_target_without_identity`

Goldens:

- `tests/data/gold_src/dds_lifecycle_layered_merge.py`
- `tests/data/goldens/materialized/dds_lifecycle_layered_merge.py`

The golden should include:

- base `count` field
- derived `count` field with narrower annotation or changed default
- derived `owner` field
- a printed merged sequence showing derived `count` wins
