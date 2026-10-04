# YIDL Recorded Capsule Data-Driven API Proposal

## Purpose

The recorded capsule builder should support both quick fluent authoring and
data-driven authoring. Attribute syntax is good for hand-written concepts:

```python
Name = builder.props.Name(str, REQUIRED)
FieldInput = builder.records.FieldInput(Name, Kind)
ClassBody = builder.ports.Class.body(cardinality=builder.many)
```

But YIDL will also generate or assemble concepts from data. That path cannot
depend on hard-coded Python attribute names. It needs function-call equivalents
for every attribute path.

## Principle

Every attribute-chain operation must have a data-driven function form with the
same semantics and the same symbolic-handle result.

Attribute syntax is sugar. The function-call API is the canonical lower-level
surface for generated definitions, loops, and table-driven concept builders.

## Naming

Use explicit call methods named for the semantic object being declared:

```python
builder.props.define("Name", str, REQUIRED)
builder.records.define("FieldInput", Name, Kind)
builder.collections.define("Fields", FieldInput, cardinality=builder.many, identity=Name)
builder.ports.define("Class.body", cardinality=builder.many)
builder.matchers.define("PropertyTemplate")
builder.use_matcher("PropertyTemplate")
builder.productions.define("Property", ...)
```

Attribute syntax delegates to the same methods:

```python
builder.props.Name(str, REQUIRED)
# equivalent to:
builder.props.define("Name", str, REQUIRED)
```

## Properties

Attribute form:

```python
Name = builder.props.Name(str, REQUIRED)
Kind = builder.props.Kind(str, "plain")
Frozen = builder.props.Frozen(bool)
```

Data-driven form:

```python
Name = builder.props.define("Name", str, REQUIRED)
Kind = builder.props.define("Kind", str, "plain")
Frozen = builder.props.define("Frozen", bool)
```

Rules:

1. The second positional argument means `default`.
2. `default=` is also accepted.
3. `storage_name` can be passed explicitly.
4. If `storage_name` is omitted, it is derived from the property name.
5. Data-driven names must pass the same validation as attribute names.

## Records

Attribute form:

```python
FieldInput = builder.records.FieldInput(Name, Kind, Order)
```

Data-driven form:

```python
FieldInput = builder.records.define("FieldInput", Name, Kind, Order)
```

Extension attribute form:

```python
builder.extend_record.FieldInput(Frozen)
```

Extension data-driven form:

```python
builder.extend_record("FieldInput", Frozen)
```

If explicit extension points are used, they also need both forms:

```python
builder.extension_points.FieldInput()
builder.extension_points.define("FieldInput")
```

## Collections

Attribute form:

```python
Fields = builder.collections.Fields(
    FieldInput,
    cardinality=builder.many,
    identity=Name,
)
```

Data-driven form:

```python
Fields = builder.collections.define(
    "Fields",
    FieldInput,
    cardinality=builder.many,
    identity=Name,
)
```

Computed collections:

```python
InitFields = builder.computed.define(
    "InitFields",
    source=Fields,
    when=(Init.eq(True),),
)
```

## Ports

Attribute form:

```python
ClassBody = builder.ports.Class.body(cardinality=builder.many)
```

Data-driven form:

```python
ClassBody = builder.ports.define("Class.body", cardinality=builder.many)
```

The dotted path is the semantic port name. Attribute syntax is only a convenient
way to build that dotted path.

## Matchers

Attribute form:

```python
PropertyTemplate = builder.matchers.PropertyTemplate()
field = PropertyTemplate.input.field(Fields)
PropertyTemplate.rule.managed(
    when=(field.prop(Kind).eq(MANAGED_FIELD),),
    resource=from_astichi_code("... managed property ..."),
)
```

Data-driven form:

```python
PropertyTemplate = builder.matchers.define("PropertyTemplate")
field = PropertyTemplate.input.define("field", Fields)
PropertyTemplate.rule.define(
    "managed",
    when=(field.prop(Kind).eq(MANAGED_FIELD),),
    resource=from_astichi_code("... managed property ..."),
)
```

Reopening a matcher:

```python
PropertyTemplate = builder.use_matcher("PropertyTemplate")
```

This should be equivalent to:

```python
PropertyTemplate = builder.use_matcher.PropertyTemplate()
```

## Productions

Attribute form:

```python
builder.productions.Property(
    source=PropertyTemplate.results(),
    target=Components,
    values={Name: match.record("field").prop(Name)},
    policy=AddIfAbsent,
).in_group("Properties")
```

Data-driven form:

```python
builder.productions.define(
    "Property",
    source=PropertyTemplate.results(),
    target=Components,
    values={Name: match.record("field").prop(Name)},
    policy=AddIfAbsent,
).in_group("Properties")
```

Groups:

```python
builder.production_groups.define("Properties", PropertyProduction)
```

or via the production handle:

```python
PropertyProduction.in_group("Properties")
```

## Generated Values And Runtime Helpers

Generated values are passed directly where they are used:

```python
PropertyTemplate.rule.define(
    "managed",
    when=(field.prop(Kind).eq(MANAGED_FIELD),),
    resource=from_astichi_code("... managed property ..."),
)
```

The recorded concept plan discovers these values from matcher defaults, matcher
rules, productions, and other recorded operation operands. If runtime emission
chooses to hoist a value to a generated binding, that name is private and
deterministic. It is not part of the concept authoring API.

Non-generated runtime helpers, such as evaluator functions, still need a way to
enter the generated runtime environment:

```python
builder.runtime.evaluator(property_order_for)
builder.runtime.evaluator(property_order_for, name="property_order_for")
```

Inference rules for helper names:

1. Infer a helper name when reliable.
2. Require `name=` when inference is unavailable or ambiguous.
3. Explicit `name=` always wins.
4. Duplicate helper names with different values reject.
5. Duplicate helper names with the same value may coalesce.

## Example: Table-Driven Field Properties

```python
for name, value_type, default in field_property_specs:
    prop = builder.props.define(name, value_type, default)
    builder.extend_record("FieldInput", prop)
```

This is the key use case. Concept authors should not need to choose between a
nice handwritten API and a separate low-level dynamic API.

## Implementation Notes

1. Implement function-call forms first.
2. Implement attribute syntax as a thin proxy over the function-call forms.
3. Ensure every symbolic handle stores the canonical string name/path.
4. Tests should assert attribute and data-driven forms produce equivalent
   recorded plans for properties, records, ports, matchers, and productions.
5. Keep generated-code success tests in the golden harness; use bespoke tests
   only for API equivalence and validation failures.
