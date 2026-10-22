# DDS, records and containers

`DataDefinitionSystem` defines schema. It has no per-class data until you create
a builder. Properties hold semantic name, Python value type, default and storage
name. Generated record constructors use the storage spelling and validate types.
Generated records are plain slotted Python classes with `__dds_record_spec__`.

```python
# Definition API: explicit semantic and storage spelling
name = dds.property("FieldName", str, storage_name="field_name")
```

The tutorial's `FieldRow(field_name="x", ...)` populates that storage spelling;
matchers and contribution declarations use `FieldName`. Unknown constructor
keywords and wrong typed values are input errors. Union/family collections accept
concrete variant records; instantiate a concrete variant, not the union itself.

## Collection and port contracts

| Surface | Contract |
| --- | --- |
| `single` | At most one record in the collection |
| `many` | Multiple records, still subject to declared identity |
| Identity | Scalar property or tuple; strict add rejects duplicates |
| Computed collection | Filtered view of existing source records; no new storage |
| `view.sequence()` | Collection/view sequence |
| `view.one()` | One record or None when empty; multiple records reject |
| `view.by_identity(key)` | Identity-based read; missing key returns None |
| `contains(...)` | Identity-key existence query, including computed-view filter |
| `ordered_records(...)` | Declared property order, then collection write order |
| Port cardinality | Number of children at **one address**, not collection size |
| `children_at(address)` | Ordered children configured by target/order properties |

The builder supports `add` and explicit `write(..., policy=...)`. `AddIfAbsent`
keeps an existing identity; replacement deliberately changes it; strict insertion
rejects accidental duplicates. Confirm exact policy class exports in your SDK
rather than using a string tag. Frozen data views cannot write or lazily derive
new records. A record may participate in several computed views without copying.

## Keyed lookup example

This canonical fixture demonstrates tuple identities and a data production that
reads one key's `TxIndex`, rather than enumerating a Cartesian product:

{{source:tests/data/gold_src/dds_composite_identity_lookup.py|python}}

Missing-key behavior can be explicitly supplied by the production `lookup`
expression's `default` argument; absent a usable key/default, preserve its lookup
diagnostic. It is not the same as an unmatched rule returning no generated value.
For operation and matcher snapshot timing see [fact production](../guides/fact-production.md).
