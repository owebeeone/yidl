# Produce facts before assembly

DDS starts with schema. A builder owns mutable records for one generation;
operations and data productions can write derived facts before freezing.
Assembly consumes those facts to produce composables.

A data production declares a source, target record values and write policy.
Sources can be concrete collections, computed views or generic matcher results.
A computed collection is a filtered view of existing records; it does not store
another set or derive records during a query. Keyed lookup reads an identity;
it is different from enumerating two collections' combinations.

Generic matcher-result production evaluates a stable builder snapshot. Reads
from that snapshot do not see writes made later in the same step. Sequence
operations/groups deliberately when one phase needs another's output.

## Aggregate operations

An operation resource receives `DDSOperationContext`. Its declared input/output
collections bound the operation. Supported context reads include `records(...)`,
`by_identity(...)`, `children_at(...)`, and `write_order(...)`; `write(...)`
applies an explicit policy. Unknown providers and signature analysis are
consumer responsibilities, expressed as ordinary operations and records.

The canonical callable-fact example is executable and records analysis output:

```sh
ASTICHI_LOWER_ENGINE=python build/example-env/bin/python \
  tests/data/gold_src/dds_lifecycle_callable_facts.py build/callable_facts.py
```

Its Lifecycle analyzer understands a particular injection registry. It is not a
generic DDS callable resolver. Likewise initvar dependency closure is a
Lifecycle-specific operation, not a public DDS `reachable_collection` helper.

Use strict insertion for accidental duplicates. `AddIfAbsent` and replacement
are deliberate alternatives for identity-bearing collections; they do not make
all writes safe to reorder. After freeze, query without mutation. See
[data model](../reference/data-model.md) for cardinality and
[matching/data flow](matching-and-data-flow.md) for result projection.
