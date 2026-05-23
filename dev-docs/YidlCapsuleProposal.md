# YIDL Capsule Proposal

Temporary design note. This replaces the current syntax-first direction with a
model-first direction.

## 1. Decision

1. Hold off on YIDL grammar.
2. Build the semantic model first.
3. Let authored fluent API and later parser/frontend both target the same core
   model.
4. Use **Capsule** as the core composable unit.

## 2. Capsule

1. A **Capsule** is a composable container of YIDL build knowledge.
2. A capsule does not represent one field, one helper, or one class by itself.
3. A capsule can carry any combination of:
   1. field-spec properties
   2. field-specifier defaults/fixed overrides
   3. facade declarations
   4. method builders
   5. variable builders
   6. code snippets
   7. facets
   8. rules
   9. runtime constant bindings
   10. derived-property functions
4. A capsule is closed under composition:
   1. compose two capsules -> get another capsule
   2. start from a null capsule
   3. refine by repeated composition

## 3. Why Capsule

1. The grammar is not the hard part. The semantic model is.
2. A fluent API can express the model now without committing to parser syntax.
3. A future parser can compile into capsules instead of inventing a second
   semantic path.
4. Astichi already gives a compositional model for code snippets. Capsule gives
   YIDL the same kind of compositional model for lifecycle generation.

## 4. Null Capsule

1. There must be a **null capsule**.
2. The null capsule contains nothing:
   1. no facades
   2. no methods
   3. no variables
   4. no properties
   5. no rules
   6. no snippets
3. It is the identity element for composition.
4. Example:

```python
capsule = YidlCapsule.null()
capsule = capsule.compose(base_capsule)
capsule = capsule.compose(managed_capsule)
capsule = capsule.compose(binding_capsule)
```

## 5. Core Contents

### 5.1 Field-Spec Properties

1. A field-spec property is a named semantic property.
2. Examples:

```python
Init = fieldspec_property("init", bool)
Default = fieldspec_property("default", object)
DefaultFactory = fieldspec_property("default_factory", object)
FieldName = fieldspec_property("name", str)
FieldAnno = fieldspec_property("annotation", object)
TxKey = fieldspec_property("tx_key", object)
```

3. Properties are the input vocabulary for rules.
4. Properties hold values, but rules often care only about the value shape:
   1. specified vs unspecified
   2. init true vs false
   3. literal default vs factory default vs no default
   4. transaction-aware vs not
5. Property definitions keep stable semantic names such as `Init`, `Default`,
   `FieldName`, and `FieldAnno`.
6. Callable/resource binding names are separate from property definition names.
7. The default binding-name rule is: derive a snake_case parameter name from the
   property definition name:
   1. `Init -> init`
   2. `Default -> default`
   3. `FieldName -> field_name`
   4. `FieldAnno -> field_anno`
8. A later capsule may override that derived binding name when needed, but the
   derived snake_case name is the default contract.

### 5.2 Field Specifier Profiles

1. A field specifier profile is the author-facing helper identity.
2. Examples: `managed`, `static`, `initvar`, `binding`, `owned`.
3. A profile does not emit code directly.
4. A profile contributes:
   1. default property values
   2. fixed property values
   3. allowed user-provided properties
   4. validation rules
5. Example direction:

```python
ctx.field_specifiers.managed.defaults.set(Init, False)
ctx.field_specifiers.commit_validator.fixed.set(Init, False)
```

### 5.3 Facades

1. A facade is a generated class surface.
2. `Main` is the default user-facing facade.
3. Users may define more facades.
4. A facade can have one or more facade classes/capabilities.
5. Methods are attached to facades.

### 5.4 Method Builders

1. A method builder defines one generated method shape.
2. A method builder can target:
   1. one facade
   2. many facades
   3. one class-level method surface
3. A method builder owns facets such as:
   1. parameters
   2. setup
   3. per-field body stages
   4. return path
4. `__init__` is just another method builder.

### 5.5 Variable Builders

1. A variable builder defines a generated variable/class attribute.
2. Examples:
   1. classvars
   2. tx-name <-> tx-id maps
   3. generated constants
   4. helper lookup tables

### 5.6 Code Snippets

1. Code snippets are Astichi composables.
2. Snippets advertise what they need through their Astichi demand ports.
3. A rule does not own handwritten string formatting logic if the snippet can
   express its needs directly.
4. The rule maps snippet needs to available properties, constants, or derived
   values.

### 5.7 Facets

1. A facet names a place where snippets can be attached.
2. Examples:
   1. constructor parameters
   2. constructor body
   3. facade getter resolve
   4. facade setter assign
   5. tx commit apply
3. Facets are grouped by builder target.
4. Facets have a policy:
   1. additive
   2. single-winner
   3. future: exclusive groups if needed

### 5.8 Rules

1. Rules decide what snippet goes into which facet.
2. A rule has:
   1. target facet
   2. condition
   3. Astichi composable snippet
   4. binding map from snippet needs to property values / constants / derived values
   5. precedence or specificity
3. Rules are grouped by facet.
4. Rules are evaluated against a context subject such as:
   1. one field spec
   2. one class model
   3. one facade + field combination

## 6. Connections Between Parts

1. Field specifier profile resolves property values.
2. Resolved properties become the subject for rule evaluation.
3. Rule evaluation selects snippets for a facet.
4. Selected snippets bind their demands from:
   1. field properties
   2. class properties
   3. runtime constants
   4. derived values
5. Method builders and variable builders collect facet results.
6. Astichi composes the snippets into final emitted methods and variables.

Flow:

```text
field specifier profile
-> resolved properties
-> facet rule evaluation
-> selected snippets + bindings
-> method/variable builders
-> Astichi composition
-> generated class
```

## 7. Composition

1. Capsule composition is left-to-right overlay/combine.
2. It is closed:
   1. `Capsule × Capsule -> Capsule`
3. It has identity:
   1. `NullCapsule.compose(X) == X`
   2. `X.compose(NullCapsule) == X`
4. It should be associative as far as practical.
5. It is not assumed to be commutative.

Reason:

1. Order matters for defaults, overrides, and precedence.
2. `base.compose(transaction)` is not necessarily the same as
   `transaction.compose(base)`.

## 8. What Composition Merges

Capsule composition merges:

1. property declarations
2. field specifier profiles
3. facade declarations
4. method builder declarations
5. variable builder declarations
6. facet declarations
7. rules
8. snippet registries
9. derived-value providers

Composition must reject:

1. same property name with incompatible type
2. same facet path with incompatible policy
3. same builder target with incompatible shape
4. ambiguous override of the same rule identity without an explicit replace

## 9. Rule Evaluation Model

1. Rule conditions are evaluated against property values.
2. The minimum useful condition model is simple:
   1. equality
   2. specified / unspecified
   3. and-composition
   4. precedence / specificity
3. For many lifecycle cases, the actual default value does not matter to rule
   selection; only the default source class matters:
   1. no default
   2. literal default
   3. default factory
4. Rules should stay concrete.
5. A rule should return a snippet contribution, not a new mini-language.

## 10. Example Direction

This is only a shape sketch:

```python
ctx = YidlCapsule.null()

ctx = ctx.with_property(Init)
ctx = ctx.with_property(Default)
ctx = ctx.with_property(DefaultFactory)
ctx = ctx.with_property(FieldName)
ctx = ctx.with_property(FieldAnno)

ctx = ctx.with_facet("constructor.params", policy="additive")
ctx = ctx.with_facet("constructor.body", policy="additive")

ctx = ctx.with_rule(
    facet="constructor.params",
    condition=Condition.all(
        Init.eq(True),
        Default.is_unspecified(),
        DefaultFactory.is_unspecified(),
    ).priority(90),
    snippet=astichi.compile(
        '''
def astichi_params(*, name__astichi_arg__: anno__astichi_arg__ = UNSPECIFIED__astichi_arg__):
    pass
'''
    ),
    binds={
        "name": FieldName,
        "anno": FieldAnno,
        "UNSPECIFIED": runtime_constant("UNSPECIFIED"),
    },
)
```

The important part is not this exact API. The important part is:

1. rules are facet-local
2. snippets are Astichi composables
3. snippet needs are bound from semantic properties
4. callable/resource parameter names are binding names such as `init`,
   `default`, `field_name`, and `field_anno`, not the property definition names
   `Init`, `Default`, `FieldName`, and `FieldAnno`

Additional selector/resource sketch:

```python
builder = build_from(BaseCapsule)
builder.property.add.FieldName(str)
builder.property.add.FieldAnno(object, default=UNSPECIFIED)
builder.spec.add.field_spec.FieldName.FieldAnno.Init.Default
builder.method.add.Main.named("__init__").on(INIT_ONLY_METHOD_SHELL)\
    .define.params.specs(lambda init: init)\
    .define.prep.any()\
    .define.field_init.specs(lambda field_name: True)\
    .define.finalize.any()\
    .done()

builder.resource.add.init_param.into.params.specs(lambda init: init)\
    .on(INIT_ONLY_PARAM_RESOURCE)\
    .define.field_name.spec.field_name()\
    .define.anno.spec.compute(
        lambda field_anno: field_anno if field_anno is not UNSPECIFIED else None
    )\
    .define.default_value.spec.compute(
        lambda default: default if default is not UNSPECIFIED else UNSPECIFIED
    )\
    .done()
```

## 11. What Replaces "Transducer"

1. The old `transducer` concept disappears as the semantic center.
2. If the word survives at all, it is only a packaging convenience.
3. The real semantic units are:
   1. field specifier profiles
   2. properties
   3. facets
   4. rules
   5. snippets
   6. builders
4. A former transducer is now just a capsule fragment that contributes some of
   those things.

## 12. Why This Is Better

1. It removes pressure to invent parser syntax too early.
2. It gives one semantic model for both fluent API and future parser input.
3. It keeps codegen lean because only selected snippets are stitched.
4. It matches Astichi's compositional style.
5. It gives a clear identity/closure story:
   1. always start from a null capsule
   2. always build another capsule
   3. evaluate a capsule into a class model

## 13. Immediate Next Steps

1. Define the minimum `YidlCapsule` object model:
   1. property registry
   2. facet registry
   3. rule registry
   4. snippet binding model
2. Define field specifier profile defaults/fixed overrides.
3. Define the first two builders:
   1. constructor method builder
   2. one facade getter/setter method builder
4. Prove the model with one narrow lifecycle slice:
   1. init/default/default_factory
   2. constructor params facet
   3. constructor body facet
