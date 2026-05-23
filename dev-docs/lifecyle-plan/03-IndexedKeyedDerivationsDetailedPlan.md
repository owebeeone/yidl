# Indexed And Keyed Derivations Detailed Plan

## Goal

Provide stable derived keys for transaction keys, special per-transaction
declarations, and other lifecycle grouping needs without introducing a general
query engine.

Critical review status: composite identity and keyed lookup are DDS-core
features. `distinct_indexed_collection(...)` is not a V1 DDS-core API; distinct
indexing lowers to `dds.operation(...)` with ordered inputs and generated output
records.

This feature covers:

- distinct ordered transaction keys
- dense transaction indices
- lookup of derived indices by field transaction key
- tuple identity for uniqueness checks
- keyed lookup value expressions

## Problem

Lifecycle runtime code should not repeatedly use hashable transaction key
names in hot paths. It should map transaction key names to stable integer
indices during generation/decorator time and bind those indices into generated
methods.

The reference backend also requires uniqueness constraints such as:

- at most one commit validator per transaction key
- at most one commit order key per transaction key
- many hooks per transaction key and phase

Current DDS supports collections and identities, but it does not provide a
direct distinct-index derivation or tuple identity model.

## Operation-First API

### Distinct Indexed Collection

```python
dds.operation(
    "BuildTxKeys",
    inputs=(TransactionalFields,),
    outputs=(TxKeys,),
    order_by=(SourceOrder,),
    resource=BuildTxKeysOperation,
)
```

This creates a computed/generated collection with records:

```python
TxKeyRecord(
    tx_key_name="default_transaction",
    tx_index=0,
)
```

Optional concept-layer sugar can wrap that operation shape:

```python
concept.operations.distinct_index(
    "TxKeys",
    source=TransactionalFields,
    value=TxKey,
    order_by=(SourceOrder,),
    value_property=TxKeyName,
    index_property=TxIndex,
)
```

The helper must lower to the aggregate generated operation above.

### Field-To-Index Production

```python
dds.production(
    "BindFieldTxIndex",
    source=TransactionalFields,
    target=IndexedFields,
    identity=source.prop(Name),
    values={
        Name: source.prop(Name),
        TxKey: source.prop(TxKey),
        TxIndex: lookup(TxKeys, key=source.prop(TxKey), value=TxIndex),
    },
    policy=ReplaceExisting,
)
```

### Tuple Identity

```python
SpecialDeclarations = dds.collection(
    "SpecialDeclarations",
    SpecialDeclaration,
    identity=(SpecialKind, TxKey),
)
```

The identity expression for a record is:

```python
(record.special_kind, record.tx_key)
```

Tuple identity should work anywhere a single-property identity works:

- `matching(...)`
- `write(...)`
- `AddIfAbsent`
- `ReplaceExisting`
- `RejectDuplicate`
- generated source emission

### Keyed Lookup

```python
lookup(TxKeys, key=source.prop(TxKey), value=TxIndex)
```

V1 lookup rules:

- source collection must have an identity
- key expression must evaluate to that identity shape
- missing key rejects unless `default=` is provided
- duplicate key cannot occur if collection identity is valid

Optional default:

```python
lookup(TxKeys, key=source.prop(TxKey), value=TxIndex, default=0)
```

Defaults should be rare. Missing transaction key is usually a design error.

## Exact Index Semantics

V1 distinct-index rules:

- scan source records sorted by `order`
- if `order` ties, preserve source collection write order
- skip records where `value` is `NOT_PROVIDED`
- first occurrence of each distinct value wins its index
- indices are dense starting at zero
- output records are ordered by assigned index

This means if fields are declared:

```text
count: tx_key="default"
owner: tx_key="resource"
label: tx_key="default"
session: tx_key="session"
```

the generated transaction keys are:

```text
default -> 0
resource -> 1
session -> 2
```

## Expected Use Case

```python
TransactionalFields = dds.computed_collection(
    "TransactionalFields",
    source=MergedFields,
    when=(HasTransaction.eq(True),),
)

dds.operation(
    "BuildTxKeys",
    inputs=(TransactionalFields,),
    outputs=(TxKeys,),
    order_by=(SourceOrder,),
    resource=BuildTxKeysOperation,
)

IndexedFields = dds.collection(
    "IndexedFields",
    IndexedField,
    identity=Name,
)

dds.production(
    "AddTxIndexToFields",
    source=TransactionalFields,
    target=IndexedFields,
    identity=source.prop(Name),
    values={
        Name: source.prop(Name),
        TxKey: source.prop(TxKey),
        TxIndex: lookup(TxKeys, key=source.prop(TxKey), value=TxIndex),
    },
    policy=ReplaceExisting,
)
```

## Expected Generated Source Golden

Expected excerpt for `tests/data/goldens/materialized/dds_lifecycle_tx_index.py`:

```python
def build_tx_keys(ctx):
    seen = {}
    ordered = sorted(
        ctx.records(TransactionalFieldsCollection),
        key=lambda record: (record.source_order, ctx.write_order(record)),
    )
    for field in ordered:
        tx_key = getattr(field, "tx_key", NOT_PROVIDED)
        if tx_key is NOT_PROVIDED:
            continue
        if tx_key in seen:
            continue
        tx_index = len(seen)
        seen[tx_key] = tx_index
        ctx.write(
            TxKeysCollection,
            TxKeyRecord(tx_key_name=tx_key, tx_index=tx_index),
            policy=RejectDuplicate,
        )


def add_tx_index_to_fields(ctx):
    tx_keys_by_name = {
        record.tx_key_name: record
        for record in ctx.records(TxKeysCollection)
    }
    for field in ctx.records(TransactionalFieldsCollection):
        tx_key_record = tx_keys_by_name[field.tx_key]
        ctx.write(
            IndexedFieldsCollection,
            IndexedField(
                name=field.name,
                tx_key=field.tx_key,
                tx_index=tx_key_record.tx_index,
            ),
            policy=ReplaceExisting,
        )


def run_operations(ctx):
    build_tx_keys(ctx)
    add_tx_index_to_fields(ctx)
    return ctx.freeze()
```

Expected runtime result:

```text
TxKeys: default_transaction=0, audit=1, resources=2
IndexedFields: count:0, label:0, owner:2, updated_at:1
```

## Special Declarations Golden

Expected excerpt for tuple identity:

```python
ctx.write(
    SpecialDeclarationsCollection,
    SpecialDeclaration(
        special_kind=COMMIT_VALIDATOR,
        tx_key="default_transaction",
        field_name="validate_default",
    ),
    policy=RejectDuplicate,
)
```

Generated duplicate check should use tuple key:

```python
key = (record.special_kind, record.tx_key)
```

Expected duplicate diagnostic:

```text
duplicate SpecialDeclarations identity ('commit_validator', 'default_transaction')
```

## Diagnostics

Required errors:

- distinct index source is not a collection or computed collection
- value property is missing on a source record and no skip rule exists
- lookup target collection has no identity
- lookup key shape does not match identity shape
- lookup missing key without default
- tuple identity contains a non-source-emittable component in generated source
- tuple identity references a property absent from a variant record

## Implementation Notes

Distinct indexed collection can be implemented as a generated production group
instead of a new container view. Prefer the generated production approach if it
uses less runtime magic.

Potential internal objects:

```python
DistinctIndexedCollectionSpec
LookupValueExpression
TupleIdentitySpec
```

Do not expose all three if the public API can be smaller.

## Test Plan

Bespoke:

- `test_distinct_index_assigns_dense_indices`
- `test_distinct_index_preserves_first_order`
- `test_lookup_value_expression_reads_index`
- `test_lookup_missing_key_rejects`
- `test_tuple_identity_matching_and_duplicate_rejection`

Goldens:

- `tests/data/gold_src/dds_lifecycle_tx_index.py`
- `tests/data/goldens/materialized/dds_lifecycle_tx_index.py`

The golden should include:

- at least four fields
- at least three transaction keys
- repeated transaction key
- validator/order-key uniqueness using tuple identity
- hook many-record declaration for the same transaction key
