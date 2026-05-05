# YIDL Recorded Capsule Resource Model

## Purpose

Matcher resources and template resources must be value based. A resource should
be the value used by the rule, not a separately registered named object with
parallel side tables.

The bad shape is:

```python
READONLY_PROPERTY = from_astichi_code("...")
FROZEN_PROPERTY_TEMPLATE_VALUE_NAMES = ((READONLY_PROPERTY, "READONLY_PROPERTY"),)
FROZEN_PROPERTY_TEMPLATE_GLOBALS = {"READONLY_PROPERTY": READONLY_PROPERTY}
```

That splits one semantic value into multiple bookkeeping declarations. The
recorded capsule builder should instead capture generated values directly where
they are used.

## Core Model

`from_astichi_code(...)` is the resource value:

```python
PropertyTemplate = builder.matchers.PropertyTemplate()
field = PropertyTemplate.input.field(Fields)
PropertyTemplate.rule.managed(
    when=(field.prop(Kind).eq(MANAGED_FIELD),),
    resource=from_astichi_code(
        "@property\n"
        "def field_name__astichi_arg__(self):\n"
        "    return self.astichi_ref(external=working_path)\n"
        "\n"
        "@field_name__astichi_arg__.setter\n"
        "def field_name__astichi_arg__(self, value):\n"
        "    self.astichi_ref(external=working_path)._ = value\n"
    ),
)
```

The concept recorder sees that value in the matcher rule and records it as part
of the concept plan. A caller should not have to separately register a resource,
value name, or global.

## Generated Value Requirements

A generated value must provide:

1. Value semantics: equivalent generated values compare by content, not object
   identity alone.
2. The underlying runtime value needed by existing matcher/build-mapper code.
   For Astichi snippets, this remains compatible with `MatcherGeneratedValue`.
3. A source expression that can reconstruct the value in generated runtime
   source, such as a `from_astichi_code(...)` call.
4. Optional diagnostic metadata, such as source location.

A generated value does not need a public symbolic name. The emitter may decide
to inline it or hoist it to a generated private binding.

## Authoring Rule

Concept authors should write resources inline unless reuse improves readability:

```python
PropertyTemplate.default(from_astichi_code("... plain property ..."))
PropertyTemplate.rule.managed(
    when=(field.prop(Kind).eq(MANAGED_FIELD),),
    resource=from_astichi_code("... managed property ..."),
)
```

Named local variables are fine for readability, but they are ordinary Python
locals, not mandatory runtime bindings:

```python
managed_property = from_astichi_code("... managed property ...")
PropertyTemplate.rule.managed(..., resource=managed_property)
```

No `*_VALUE_NAMES`. No `*_GLOBALS`.

## Runtime Emission

During replay/source emission, the concept runtime builder derives all generated
values by scanning the recorded concept plan:

- matcher defaults
- matcher rules
- production values
- other recorded operation operands that contain generated values

For each generated value the emitter can choose one of two strategies:

1. Inline reconstruction at use site:

   ```python
   resource=from_astichi_code("...")
   ```

2. Hoist to a generated binding and reference it:

   ```python
   _y_resource_0 = from_astichi_code("...")
   resource=_y_resource_0
   ```

The choice is an implementation detail. Hoisting is useful for deduplication and
readability, but it must not leak into the authoring API.

## Deduplication

Generated values should be deduplicated by value when hoisted. The dedupe key
should include the fields that affect runtime behavior:

- source text
- file name
- line number
- offset
- arg names
- keep names, after builtin defaults are normalized
- source kind

Diagnostic-only metadata can be excluded if it does not alter runtime behavior.

## Literals

Literal resources should also be values used directly:

```python
PropertyTemplate.rule.example(
    when=(field.prop(Kind).eq("example"),),
    resource=from_literal({"kind": "example"}),
)
```

The emitter can inline or hoist the literal-generated value just like an Astichi
snippet value.

## Imported Values

Imported symbols are a different category. If a matcher resource needs to refer
to an imported object, the value should still be represented as a reconstructible
value expression, not a side table. A future helper may look like:

```python
from_import("yidl.runtime.transaction", "TransactionManager")
```

That helper would be a value object with source-emission behavior. Import
consolidation should use Astichi import support where practical.

## Matcher Integration

Matchers already accept generated values as resources. The recorded builder's
job is to preserve those values in the concept plan and make runtime source
emission reconstruct them without manual maps.

Existing low-level matcher APIs may continue to accept `MatcherGeneratedValue`
for compatibility. The recorded concept layer should not expose or require
manual value-name/global maps.

## Build Mapper Integration

The class build mapper currently expects produced `template` records to contain
`MatcherGeneratedValue`. V1 can keep that internal shape. Inline
`from_astichi_code(...)` values already produce that kind of value.

Longer term, the generated value type can be generalized if matcher resources
need to represent imported values or non-Astichi generated resources. That should
not change the concept authoring shape.

## Example: Frozen Property Without Side Tables

```python
FrozenBuilder = capsule_concept("frozen", requires=(PropertyConcept,))

Frozen = FrozenBuilder.props.Frozen(bool)
FrozenBuilder.extend_record.FieldInput(Frozen)

PropertyTemplate = FrozenBuilder.use_matcher.PropertyTemplate()
field = PropertyTemplate.input.field(Fields)
PropertyTemplate.rule.readonly_plain(
    when=(field.prop(Frozen).eq(True), field.prop(Kind).eq(PLAIN_FIELD)),
    resource=from_astichi_code(
        "@property\n"
        "def field_name__astichi_arg__(self):\n"
        "    return self.astichi_ref(external=storage_path)\n"
    ),
)
PropertyTemplate.rule.readonly_managed(
    when=(field.prop(Frozen).eq(True), field.prop(Kind).eq(MANAGED_FIELD)),
    resource=from_astichi_code(
        "@property\n"
        "def field_name__astichi_arg__(self):\n"
        "    return self.astichi_ref(external=working_path)\n"
    ),
)
```

No value-name tuple. No globals dict. The concept plan records the values from
the rule definitions.

## Implementation Slices

1. Ensure generated values have stable equality/hash semantics by runtime
   content.
2. Teach recorded concept plans to collect generated values from matcher and
   production operations automatically.
3. Teach runtime source emission to reconstruct collected values inline or as
   generated private bindings.
4. Replace manual `*_VALUE_NAMES` / `*_GLOBALS` in property/frozen concepts with
   inline generated values.
5. Add bespoke tests for generated-value dedupe and source reconstruction. Keep
   success behavior under goldens.

## Open Questions

1. Should hoisted generated bindings be deterministic private names based on
   declaration order or content hash?
2. Should source location fields participate in dedupe when they do not affect
   runtime behavior but do affect diagnostics?
3. Should generated values remain `MatcherGeneratedValue`, or should that class
   be renamed/generalized once non-matcher consumers use it directly?
