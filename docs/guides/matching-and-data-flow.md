# Follow properties into generated parameters

Run the tutorial with `--extended`. It generates `Point(x, y)` and `Size(x)` from
two class rows and five field rows. The same field spelling `x` belongs to two
owners. A hidden field and an orphan row make incorrect selection visible.

## Input rows

| ClassId | ClassName | ClassOrder | SlotNames |
| --- | --- | --- | --- |
| point | Point | 10 | x, y |
| size | Size | 20 | x |

| FieldId | Owner | FieldName | FieldOrder | Selected |
| --- | --- | --- | --- | --- |
| point.y | point | y | 20 | True |
| point.x | point | x | 10 | True |
| point.hidden | point | hidden | 30 | False |
| size.x | size | x | 10 | True |
| orphan.z | absent | z | 99 | True |

`Fields` uses `FieldId` as collection identity. The semantic property `FieldName`
is populated with the generated constructor keyword `field_name`. Neither is the
runtime field value, which is supplied later to `Point(3, 4)`.

## Selection, projection and destination

`InitProduction(cls: Classes)` retains the current class as context. Each `from
field: Fields` enumerates candidates and `where Owner == ClassId and Selected ==
True` relates them to that class. This is explicit filtering, not an implicit
keyed join. For Point, `point.y` and `point.x` survive; for Size, only `size.x`
survives. No class can match `orphan.z`.

`Params(cls: Classes, field: Fields)` chooses `Param`. Its `ident field_name =
FieldName` turns the chosen name into a Python parameter identifier.
`Assignment` binds the same property as `ident value` and `external slot` for the
outer parameter read and direct attribute target. Target `params` or `stores`
resolves against `/InitMethod` within the nested production's mapped root.

Build index `(ClassOrder, FieldOrder)` identifies an insertion independently of
its collection identity. `order FieldOrder` determines parameter/store sequence.
The facts are deliberately inserted y before x, but output is x before y:

{{source:tests/data/goldens/materialized/documentation_classes/extended_model.py|python}}

## M01–M10 contract map

| Case | Contract and executable evidence |
| --- | --- |
| M01 subset/properties | Tutorial selects FieldName while identity/owner/order have separate roles |
| M02 inputs/combinations | Tutorial contextual class + field filtering; standalone `yidl_update_a_multi_source_from.py` enumerates two sources; empty collection contributes nothing |
| M03 view/lookup | `dds_composite_identity_lookup.py`: tuple key `(TxKey, Phase)`, explicit projection; a computed view filters existing records |
| M04 ownership/ambiguity | DDS Python API `input.prop(property)` is explicit; contribution syntax exposes visible semantic names and rejects duplicates; do not invent `field.FieldName` there |
| M05 selection | `test_matcher.py`: broad/narrow, weight, default, no-match, overlap; contribution rules are separately checked |
| M06 evaluated fields | `matcher.evaluated_field(..., inputs=(left,right), value=callable, value_type=...)` derives tuple entries; emitted evaluators require an importable/generated name |
| M07 projection | `dds_matcher_productions.py`: `match.record("field").prop(name)` versus `match.value(0)`; invalid tuple index/name diagnostics are tested |
| M08 context | Tutorial retains `cls`; unavailable/duplicate visible properties reject rather than guessed qualification |
| M09 bindings/parameters | Tutorial maps one property to parameter identifier, outer read and attribute path; captures/defaults remain consumer policy |
| M10 identity/order | Tutorial numeric composite index avoids two-owner collisions; ClassId/FieldId, owner, name, index, order and target remain distinct |

## Original records versus extracted values

Generic matcher-result productions offer three different expressions:

```python
match.resource()                       # selected generated value
match.record("field").prop(name)       # original input record's property
match.value(0)                         # positional extracted/evaluated tuple entry
```

The tuple schema includes fields demanded by conditions/evaluators, not every
property of every input record. Inspect `matcher.tuple_schema`; never assume
index zero means the first record's first declared property. This complete
canonical example demonstrates the projection and generated operation snapshot:

{{source:tests/data/gold_src/dds_matcher_productions.py|python}}

For multi-input derived values, the evaluator receives inputs in its declared
`inputs` order. Source emission cannot serialize an arbitrary closure. Conditions
on the derived field can select a generated value; original records remain
available separately. [Matchers](../reference/matchers.md) gives selection rules;
[consumer excerpts](../examples/consumers.md) show real constructor/accessor uses.

## A derived value from two original inputs

This exact existing test is the minimal in-memory Python-API recipe. Four
combinations yield one selected result; original records remain ordered field,
facade, while the extracted tuple contains only the derived boolean.

{{source:tests/generation/test_matcher.py@245:305|python}}

For emitted runtime source, use `emit_matcher_runtime_source` with explicit
`evaluator_names=((callable, "generated_name"),)` and provide that callable under
the declared name in the runtime namespace (or an import at the owning boundary).
The canonical `matcher_runtime.py` fixture exercises this emission contract. A
lambda in the in-memory example is not by itself an emitted evaluator.
