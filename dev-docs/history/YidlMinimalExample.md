# YIDL Minimal Example

This note fixes one stable picture for the first useful YIDL example.

The goal is not full YIDL. The goal is one capsule that can emit one simple
class with one generated `__init__` method and straightforward field
initialization.

## 1. Target Example

The user should be able to write something conceptually like:

```python
init_only = compile_capsule(InitOnlyCapsule, globals())


@init_only
class Example:
    field1: int = field_spec(init=True, default=1)
    field2: str = field_spec(init=False, default="this is it")
```

and get behavior equivalent to:

```python
class Example:
    def __init__(self, *, field1: int = 1):
        self.field1 = field1
        self.field2 = "this is it"
```

This is the minimal end-to-end slice.

## 2. Capsule Stack

The current intended capsule stack is:

1. `YidlCapsule.null()`
   Identity capsule. Knows nothing.
2. `BaseCapsule`
   Defines the minimum shared field-spec vocabulary:
   1. facade `Main`
   2. property `Init`
   3. property `Default`
   4. spec `base_spec = {Init, Default}`
3. `InitOnlyCapsule`
   Extends `BaseCapsule` with what is needed for simple constructor emission:
   1. property `FieldName`
   2. property `FieldAnno`
   3. spec `field_spec = {FieldName, FieldAnno, Init, Default}`
   4. one method composer for `Main.__init__`

This is composition, not inheritance in the Python object-model sense. Every
result is still just another `YidlCapsule`.

## 3. Intended Minimal Builder Picture

The stable intended picture for the first emitting capsule is:

```python
ParameterSnippet = """
def astichi_params(
    *,
    field_name__astichi_arg__: astichi_hole(anno) = astichi_hole(default_value),
):
    pass
"""


MethodSnippet = """
def method_name__astichi_arg__(self, method_params__astichi_param_hole__):
    astichi_hole(method_preparation)
    astichi_hole(method_body)
    astichi_hole(method_cleanup)
"""


FieldInitSnippet = """
self.field_name__astichi_arg__ = field_value__astichi_arg__
"""


def build_init_only_capsule() -> YidlCapsule:
    builder = build_from(BaseCapsule)
    builder.property.add.FieldName(str)
    builder.property.add.FieldAnno(object, default=UNSPECIFIED)

    # field_spec contains the field-level values consumed by this capsule.
    builder.spec.add.field_spec.FieldName.FieldAnno.Init.Default

    init_method = builder.method.add.Main.InitMethod(
        "__init__",
        method_snippet=MethodSnippet,
        parameter_snippet=ParameterSnippet,
    )

    init_method.params.over.spec.filter(lambda init: init)
    init_method.body.over.spec.on(FieldInitSnippet)

    return builder.build()
```

This is not fully implemented today. It is the stable picture we are aiming to
make real.

## 4. Meaning Of The Parts

### 4.1 Properties

The relevant field-spec properties for the minimal example are:

1. `FieldName`
2. `FieldAnno`
3. `Init`
4. `Default`

These are semantic property definition names.

Their stored/binding names default to:

1. `field_name`
2. `field_anno`
3. `init`
4. `default`

Actual field-spec instance values are stored by these stored names.

### 4.2 `field_spec`

```python
builder.spec.add.field_spec.FieldName.FieldAnno.Init.Default
```

means:

`field_spec` is a spec schema whose allowed semantic properties are:

1. `FieldName`
2. `FieldAnno`
3. `Init`
4. `Default`

It defines the shape of one field declaration. It does not assign values by
itself.

### 4.3 `Main`

`Main` is the default facade. It is defined by `BaseCapsule`.

For the minimal example, the generated class surface is just the `Main`
facade.

### 4.4 `InitMethod`

`InitMethod` is the first real method composer.

It is responsible for building the generated `Main.__init__` method from:

1. one method shell
2. one parameter snippet shape
3. rules/selectors over field specs
4. field/resource snippets inserted into named method surfaces

### 4.5 Method Surfaces

The stable intended method surfaces for the minimal example are:

1. `method_params`
2. `method_preparation`
3. `method_body`
4. `method_cleanup`

For `InitOnlyCapsule`, the important ones are:

1. `method_params`
   Constructor parameter contributions.
2. `method_body`
   Per-field assignment/default contributions.

The other two surfaces exist so the method shape does not need to be reinvented
when default factories, initvars, validation, or transactions are added later.

## 5. Runtime Input Model

The generated code should not assume every runtime value is emitted directly
into Python source.

For the minimal example, the stable runtime input model is:

1. the authored class object
2. one `class_definition` object

The `class_definition` object is the runtime structure produced by scanning the
decorated class. It owns the resolved field-spec values for that class.

Conceptually:

```python
class_definition = ClassDefinition(
    class_name="Example",
    fields=[
        FieldDefinition(
            field_name="field1",
            field_anno=int,
            init=True,
            default=1,
        ),
        FieldDefinition(
            field_name="field2",
            field_anno=str,
            init=False,
            default="this is it",
        ),
    ],
)
```

So the generated factory should receive:

```python
make_wrapper_class(wrapped_class, class_definition)
```

not:

```python
make_wrapper_class(wrapped_class, f1_default, f2_default, ...)
```

This keeps the runtime interface small and gives the generated code one stable
place to pull values from.

## 6. Codegen Flow

The intended minimal flow is:

1. `compile_capsule(InitOnlyCapsule, globals())` returns a decorator.
2. The decorator receives the user-authored class.
3. YIDL scans the class body for `field_spec(...)` declarations.
4. Each field declaration becomes a `field_spec` instance with stored property
   values.
5. YIDL builds one `class_definition` object from those field specs.
6. The method composer selects which fields contribute to `method_params`.
   For the minimal example:
   1. `lambda init: init`
7. The method composer selects which fields contribute to `method_body`.
   For the minimal example:
   1. all fields
8. YIDL lowers the method shell and per-field snippets through Astichi.
9. YIDL lowers a class wrapper shell through Astichi.
10. YIDL materializes Python source for a class factory and executes it.
11. YIDL calls the factory with:
    1. `wrapped_class`
    2. `class_definition`
12. The decorator returns the generated wrapper class.

## 7. Class Composer Shape

The intended minimal class-level shell is:

```python
"""
def make_wrapper_class(wrapped_class, class_definition):
    class class_name__astichi_arg__(wrapped_class):
        astichi_hole(class_defs)
        astichi_hole(class_methods)
    return class_name__astichi_arg__
"""
```

Then the decorator flow is:

```python
source = emit_capsule(...)
exec(source, local_dict, local_dict)
wrapped = local_dict["make_wrapper_class"](decorated_class, class_definition)
return wrapped
```

This keeps:

1. class-level composition in one place
2. method composers contributing into `class_methods`
3. future generated class vars and helpers contributing into `class_defs`

The important consequence is:

1. defaults
2. annotations
3. factories
4. validators
5. later transaction metadata

do not all need to become separate factory parameters. They can be read from the
runtime `class_definition` object.

## 8. What Already Works

These pieces already exist in some form:

1. `YidlCapsule`
2. `BaseCapsule`
3. `InitOnlyCapsule`
4. fluent builder for facades, properties, specs, and simple method names/surfaces
5. stored `property_name` mapping
6. `CapsuleSpecInstance`
7. a hard-coded `render_init_only_class(...)` proof of behavior
8. generic Astichi-backed callable wrapper generation in `yidl.codegen.wrapper`

So the model pieces are not zero. They are just not fully connected yet.

## 9. Holes

These are the intentional holes in the current picture:

1. `builder.method.add.Main.InitMethod(...)` is not implemented yet.
2. Method composers are not implemented yet.
3. Resource/snippet registration is not implemented yet.
4. `.over.spec.filter(...)` is not implemented yet.
5. `.on(FieldInitSnippet)` style resource binding is not implemented yet.
6. The class composer/decorator shell is not implemented yet.
7. `field_spec(...)` as a user-facing runtime marker is not implemented yet.
8. Capsule compilation to a decorator is not implemented yet.
9. Capsule emission to Astichi-driven class source is not implemented yet.
10. The current `render_init_only_class(...)` path is still hard-coded AST and
    must be replaced by the Astichi/composer path.

## 10. Next Order Of Work

Work the holes in this order:

1. implement the class composer shell
2. implement one real method composer: `InitMethod`
3. implement the `class_definition` runtime structure
4. implement method surfaces and snippet registration
5. connect method surfaces to `yidl.codegen.wrapper`
6. implement `field_spec(...)` scanning on the decorated class
7. replace hard-coded `render_init_only_class(...)` with the capsule/composer path

This order keeps one stable mental model while moving one layer at a time.

## 11. Stability Rule

Do not keep changing the picture while implementing it.

For this minimal example, the stable picture is:

1. capsule stack: `Null -> Base -> InitOnly`
2. one `class_definition` runtime object
3. one class composer
4. one method composer: `InitMethod`
5. one field-spec schema: `field_spec`
6. Astichi method shell + parameter snippet + body snippet composition
7. decorator compilation as the public entrypoint

If an implementation bug appears, fix the bug. Do not replace the planned
surface with a workaround unless the model itself is being intentionally
changed.
