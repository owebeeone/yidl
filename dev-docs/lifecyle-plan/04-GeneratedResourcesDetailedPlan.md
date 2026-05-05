# Generated Resources Detailed Plan

## Goal

Provide one consistent source-emittable resource model for templates, imports,
state references, callable wrappers, resource policies, and support values.

This feature must extend the current matcher/generated-value mechanism. It must
not create separate "matcher resources", "production resources", and
"lifecycle resources".

## Problem

Lifecycle generation needs selected resources to move through multiple layers:

1. A matcher chooses a property template.
2. A production stores that template in a contribution record.
3. A class renderer consumes the contribution.
4. Astichi materializes the final class/module source.

The selected resource may be:

- an Astichi code snippet
- an Astichi template snippet that still has binds/holes
- Astichi comment markers that render as real `#` comments in inspectable
  output
- a Python literal that can be written directly to generated source
- an imported symbol
- a state reference expression
- a resource policy object
- a callable wrapper template

Current matcher generated values are close, but they must be usable anywhere a
source-emittable value appears, not only as `MatcherResult.resource`.

## Proposed Fluent API

### Resource Constructors

Use module-level helpers backed by one generated-resource implementation.

```python
from yidl.generation import (
    from_astichi_code,
    from_astichi_template,
    from_import,
    from_literal,
)
```

The helper names are intentionally small:

```python
REQUIRED_PARAM_TEMPLATE = from_astichi_template(
    """
    def astichi_params(
        *,
        field_name__astichi_arg__: astichi_ref(external=annotation_path),
    ):
        pass
    """
)

OBJECT_SETATTR = from_import("builtins", "object")

DEFAULT_SENTINEL = from_literal("REQUIRED")
```

Keep `from_astichi_code(...)` and `from_astichi_template(...)` as separate
public factories. They may share one implementation internally, but callers
should not use a `template=True` flag.

Module-level sentinels used by generated code, such as `_NO_WORKING_VALUE`,
should also enter the renderer through generated resources or renderer-owned
module constants. Do not smuggle arbitrary Python objects through record fields
unless they are source-emittable by one of the resource factories.

### Resource Consumption In Matchers

```python
PropertyTemplate = dds.matcher("PropertyTemplate")
field = PropertyTemplate.input.field(Fields)

PropertyTemplate.default(
    from_astichi_template(
        """
        astichi_comment("property template: plain getter for {__file__}:{__line__}")

        @property
        def field_name__astichi_arg__(self):
            return self.astichi_ref(external=storage_path)
        """
    )
)

PropertyTemplate.rule.managed(
    when=(field.prop(Kind).eq(MANAGED_KIND),),
    resource=from_astichi_template(
        """
        astichi_comment("property template: managed getter for {__file__}:{__line__}")

        @property
        def field_name__astichi_arg__(self):
            return self.astichi_ref(external=working_path)
        """
    ),
)
```

### Resource Consumption In Productions

```python
dds.production(
    "PropertyTemplateToClassBody",
    source=PropertyTemplate.results(),
    target=ClassComponents,
    identity=match.record("field").prop(Name),
    values={
        Name: match.record("field").prop(Name),
        TargetPort: literal(ClassBody.of("Example")),
        Order: match.record("field").prop(SourceOrder),
        Template: match.resource(),
    },
    policy=ReplaceExisting,
)
```

The `Template` property stores the generated resource itself. It is not lowered
until the class renderer consumes it.

### Resource Consumption In Final Renderer

```python
for component in container.children_at(ClassBody.of("Example")):
    builder.Root.body.add.Component[component.order](
        component.template.to_generator().bind(...),
    )
```

The exact builder call may differ, but the final renderer consumes a composable
resource rather than reconstructing source strings.

## Generated Resource Protocol

The implementation can keep concrete dataclasses, but the semantic contract is:

```python
class GeneratedResource:
    def to_source_expr(self, context) -> str:
        ...

    def to_generator(self):
        ...
```

`to_source_expr(...)` is for generated DDS runtime modules. It emits a Python
expression that reconstructs the resource at decorator time.

`to_generator()` is for the code generation phase that needs an Astichi
composable.

The object should cache its compiled composable because it is deterministic.

## Import Semantics

Use `astichi_pyimport(...)` at the point of use inside Astichi templates:

```python
from_astichi_template(
    """
    astichi_pyimport(module="copy", names=("copy",))
    value = copy(astichi_pass(source, outer_bind=True))
    """
)
```

Astichi consolidates imports. The generated resource model should not have an
`extra_imports` side channel unless a real non-Astichi consumer requires it.

For generated DDS runtime source, imported-symbol resources may lower to:

```python
from_import("copy", "copy")
```

Expected generated source:

```python
COPY_RESOURCE = from_import("copy", "copy")
```

The final Astichi materialization later produces:

```python
from copy import copy
```

## Debug Comment Semantics

Astichi templates should use `astichi_comment(...)` for useful generated-source
debugging comments. Comments should explain generated structure rather than
restating the Python syntax.

Recommended comment sites:

- production boundary: which production emitted this block
- matcher choice: which matcher rule selected this template
- state slot group: current/working/published storage for a field
- operation phase: init/get/set/commit/rollback contribution
- diagnostic gate: generated validation block

Example:

```python
from_astichi_template(
    """
    astichi_comment("production PropertyTemplateToClassBody: managed property")

    @property
    def field_name__astichi_arg__(self):
        return self.astichi_ref(external=working_path)
    """
)
```

Executable `materialize()` strips these markers. Inspectable/commented output
uses `emit_commented()` and renders real comments:

```python
# production PropertyTemplateToClassBody: managed property
@property
def count(self):
    return self._state._count_working
```

Use only literal strings. Dynamic values should be represented by stable
template text, source file/line placeholders, or by surrounding generated
structure. `astichi_comment(...)` intentionally does not evaluate arbitrary
Python expressions.

## Semantic StateRef Resources

State references are lifecycle resources, not DDS core.

```python
PublishedValue = lifecycle_resources.state_ref("PublishedValue")
WorkingValue = lifecycle_resources.state_ref("WorkingValue")

working_count = WorkingValue.of(field="count", tx_index=0)
```

Templates receive refs:

```python
from_astichi_template(
    """
    @property
    def field_name__astichi_arg__(self):
        return astichi_ref(external=value_ref.path)
    """
)
```

If object property access inside `external=` is awkward, generate a computed
resource first:

```python
WorkingPath = call("working-path", working_path_for)
```

The first implementation may use explicit path records while preserving the
semantic resource boundary.

## Expected Use Case

For managed property generation:

```python
ManagedGetterTemplate = from_astichi_template(
    """
    @property
    def field_name__astichi_arg__(self):
        return self.astichi_ref(external=working_path)
    """
)

PropertyTemplate.rule.managed(
    when=(field.prop(Kind).eq(MANAGED_KIND),),
    resource=ManagedGetterTemplate,
)
```

Then production:

```python
values={
    Name: field.prop(Name),
    Template: match.resource(),
    Bindings: literal({"field_name": field.prop(Name), "working_path": WorkingPath}),
}
```

## Expected Generated Source Golden

Expected excerpt for
`tests/data/goldens/materialized/dds_lifecycle_generated_resources.py`:

```python
from yidl.generation import from_astichi_template

PLAIN_PROPERTY_TEMPLATE = from_astichi_template(
    '\n'
    'astichi_comment("matcher PropertyTemplate: plain property")\n'
    '\n'
    '@property\n'
    'def field_name__astichi_arg__(self):\n'
    '    return self.astichi_ref(external=storage_path)\n'
)

MANAGED_PROPERTY_TEMPLATE = from_astichi_template(
    '\n'
    'astichi_comment("matcher PropertyTemplate: managed property")\n'
    '\n'
    '@property\n'
    'def field_name__astichi_arg__(self):\n'
    '    return self.astichi_ref(external=working_path)\n'
)


class PropertyTemplateMatcherRuntime:
    def resolve(self, field_record):
        values = (getattr(field_record, "kind", NOT_PROVIDED),)
        cache_key = values
        cached = self._cache.get(cache_key, NOT_PROVIDED)
        if cached is not NOT_PROVIDED:
            return cached
        if values[0:1] == (MANAGED_KIND,):
            return self._finish(
                cache_key,
                (MANAGED_PROPERTY_TEMPLATE, "managed_property", 1.0),
                (field_record,),
                values,
            )
        return self._finish(
            cache_key,
            (PLAIN_PROPERTY_TEMPLATE, None, 0.0),
            (field_record,),
            values,
        )


def property_templates_to_class_body(ctx):
    container = ctx.snapshot()
    for result in container.matchers.PropertyTemplate.sequence():
        field = result.records[0]
        ctx.write(
            ClassComponentsCollection,
            ClassComponent(
                name=field.name,
                target=ClassBody.of("Example"),
                order=field.source_order,
                template=result.resource,
            ),
            policy=ReplaceExisting,
        )
```

The golden must prove:

- resources are module-level constants
- matcher returns resource constants, not raw source strings
- productions store resource objects
- `emit_commented()` renders `astichi_comment(...)` markers as real comments
- executable materialized output strips `astichi_comment(...)`
- no generated source imports `pyrolyze`

## Diagnostics

Required errors:

- generated resource cannot emit source expression
- generated resource cannot produce a composable for a context that needs one
- Astichi code resource compile failure includes resource name/source label
- non-cacheable resource rejects or explicitly opts out
- imported symbol resource has invalid module/name

## Implementation Notes

Current `MatcherGeneratedValue` may already hold most fields needed for
`from_astichi_code(...)`. Prefer:

1. Move the implementation to a neutral module if needed.
2. Keep compatibility exports.
3. Make matcher and production code accept the same generated resource type.
4. Add resource source emission to value-expression lowering.

Do not add `if isinstance(value, MatcherGeneratedValue)` branches in many
places. Normalize resources at definition time.

## Test Plan

Bespoke:

- `test_generated_resource_to_generator_caches_composable`
- `test_generated_resource_source_expr_round_trips`
- `test_generated_resource_invalid_astichi_source_reports_label`
- `test_generated_resource_stored_in_record_emits_by_binding`

Goldens:

- `tests/data/gold_src/dds_lifecycle_generated_resources.py`
- `tests/data/goldens/materialized/dds_lifecycle_generated_resources.py`

The golden should select at least two property templates and one init parameter
template through matchers, store them in contribution records, and render them
through a final Astichi class snippet. It should include at least one
`astichi_comment(...)` marker in each template family.
