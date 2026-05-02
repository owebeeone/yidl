# YIDL Matcher Proposal

## Purpose

YIDL needs a generic rule matcher that can be defined during the YIDL
definition/specification phase, emitted as normal Python source, and evaluated
during decoration.

The matcher is not Astichi-specific. Its output is an opaque resource. A
resource may wrap an Astichi composable, but the matcher core only selects and
returns resources.

The matcher exists to let capsules and facades contribute default behavior and
selective overrides without hard-coding every generated shape.

## Scope

This proposal covers the matcher in isolation:

- matcher definitions
- matcher rules
- scoped property conditions
- evaluated matcher fields
- specificity scoring
- weighted tie breaking
- runtime generated matcher behavior
- cached evaluation
- resource output

It does not define the Astichi build mapper. The build mapper consumes selected
resources later.

## Definition-Time Shape

A matcher is a named decision surface:

```python
Getter = dds.matcher("Getter")
```

It declares one or more input slots. Each input slot reads from a concrete or
computed DDS collection view:

```python
field = Getter.input("field", Fields)
facade = Getter.input("facade", Facades)
```

It may declare evaluated fields. Evaluated fields are matcher-local tuple values
computed from input records:

```python
IsManaged = Getter.evaluated_field(
    "IsManaged",
    inputs=(field,),
    value=is_managed_field,
)
```

The evaluator must be source-emittable. The first implementation can require an
importable generated-module binding or helper function. Later implementations
may add a structured expression API for inline generated code.

Rules attach resources:

```python
Getter.rule(
    when=(
        field.prop(Init).eq(False),
        field.prop(Annotation).eq(str),
    ),
    resource=StringNoInitGetter,
)

Getter.rule(
    when=(
        field.prop(Init).eq(False),
        field.prop(Annotation).eq(str),
        IsManaged.eq(True),
    ),
    resource=ManagedStringNoInitGetter,
)
```

The second rule wins for managed string non-init fields because it has three
matching terms, while the first has two.

## Conditions

Matcher rules use Eq-only conditions. The basic condition is a scoped property
equality:

```python
field.prop(Init).eq(False)
facade.prop(FacadeRole).eq(Working)
```

Input scoping is required because multiple input records may expose properties
with the same semantic name.

A scoped condition contains:

- input slot
- property specifier
- expected value

The condition matches when the input record provides the property and its value
equals the expected value.

Conditions can also target evaluated fields:

```python
IsManaged.eq(True)
```

Evaluated fields are local to one matcher. They should be used for cheap
matcher-specific facts. If many matchers need the same fact, prefer a DDS
derived property or computed collection so the value has one shared definition.

If an input record does not provide a property, the tuple value is
`NOT_PROVIDED`. Ordinary equality conditions do not match `NOT_PROVIDED` unless
the rule explicitly asks for it:

```python
field.prop(TxId).eq(NOT_PROVIDED)
```

`NOT_PROVIDED` is distinct from DDS `REQUIRED`. `REQUIRED` is a record
construction sentinel. `NOT_PROVIDED` is a matcher tuple fact.

## Match Tuples

At generation time, each matcher computes a fixed tuple schema from the union of
scoped properties and evaluated fields required by all of its rules. The schema
order is part of the generated matcher contract.

The specification model can describe tuple entries as scoped property refs and
evaluated field refs:

```python
Getter.tuple_schema == (
    field.prop(Init),
    field.prop(Annotation),
    IsManaged,
    facade.prop(FacadeRole),
)
```

The generated runtime code should not use a dictionary for tuple values. It
should extract a simple positional tuple with straight-line code derived from
the schema:

```python
values = (
    getattr(field_record, "init", NOT_PROVIDED),
    getattr(field_record, "annotation", NOT_PROVIDED),
    is_managed_field(field_record),
    getattr(facade_record, "facade_role", NOT_PROVIDED),
)
```

The runtime match tuple carries:

- concrete input records
- positional values for all scoped properties and evaluated fields used by
  matcher rules
- `NOT_PROVIDED` for missing property values

Conceptually:

```python
MatcherTuple(
    records=(field_record, facade_record),
    values=(False, str, True, Working),
)
```

Generated rule checks are ordered by descending score. Because equal-score
overlap is rejected during definition/code generation, the first matching rule
is the winner and later lower-score rules do not need to be checked.

```python
if values[0:3] == (False, str, True):
    return self._finish(cache_key, (ManagedStringNoInitGetter, "managed", 3.0), records, values)

if values[0:2] == (False, str):
    return self._finish(cache_key, (StringNoInitGetter, "string", 2.0), records, values)
```

The resolved match result must preserve this tuple so the later build mapper can
bind selected resources using the concrete records and values that matched.

The tuple schema may be exposed for diagnostics, but generated runtime matching
should assume fixed positional indexes.

## Evaluated Fields

An evaluated field is a matcher-local computed tuple value.

Definition shape:

```python
IsManaged = Getter.evaluated_field(
    "IsManaged",
    inputs=(field,),
    value=is_managed_field,
)
```

Required properties:

- name
- input dependencies
- source-emittable evaluator
- optional value type for validation and diagnostics

Generated extraction shape:

```python
is_managed_value = is_managed_field(field_record)
```

An evaluated field may depend on more than one input:

```python
IsFacadeVisible = Getter.evaluated_field(
    "IsFacadeVisible",
    inputs=(field, facade),
    value=is_facade_visible,
)
```

Generated extraction:

```python
is_facade_visible_value = is_facade_visible(field_record, facade_record)
```

The matcher core treats the resulting value like any other positional tuple
entry. Rule checks still use Eq-only conditions:

```python
IsManaged.eq(True)
```

The first implementation should reject non-emittable evaluators during code
generation. The in-memory runtime may accept any callable evaluator; source
emission is stricter and requires every evaluator to have an explicit generated
module binding name.

## Scoring

Matcher specificity is determined by the number of matching terms.

Base score:

```python
base_score = number_of_conditions
```

Each rule may declare a small weight multiplier:

```python
Getter.rule(..., weight=1.1, resource=PreferredGetter)
Getter.rule(..., weight=0.9, resource=DeprioritizedGetter)
```

Final score:

```python
score = base_score * weight
```

The expected weight range is near `1.0`. Weights are not intended to be large
priority numbers. They are a tie-break and selective override tool.

Examples:

- 3 terms at weight `1.0` scores `3.0`
- 2 terms at weight `1.1` scores `2.2`, so the 3-term rule still wins
- 3 terms at weight `0.9` scores `2.7`
- 2 terms at weight `1.5` would score `3.0`; this should be legal only if the
  defining code intentionally wants that override, but docs should discourage
  large weights

## Winning Rule

For one match tuple, generated runtime code should:

1. Extract the positional match tuple.
2. Evaluate rule checks in descending score order.
3. Return immediately on the first matching rule.
4. If no rule matches, return the matcher default if one exists.
5. If no rule matches and no default exists, return no match.

Generated runtime code should not build a list of matching rules and then scan
it a second time. It also should not maintain mutable score/resource state while
walking lower-score rules; sorted checks plus early return are the matcher.

Equal winning scores are handled before runtime. During definition/code
generation, rules with equal score must be checked for compatible conditions.
If two same-score rules can both match the same tuple, generation rejects and
the user must adjust rule conditions or weights.

Two same-score rules are compatible when all shared tuple positions have equal
expected values and neither rule has a conflicting expected value on a shared
position. Rules with a conflicting expected value on at least one shared tuple
position cannot match the same tuple and are allowed.

This avoids hidden declaration-order behavior. Capsule override should be
visible in either more specific conditions or an explicit weight adjustment.

## Defaults

A matcher may define a default resource:

```python
Getter.default(DefaultGetter)
```

The default is used only when no rule matches. It does not participate in
specificity scoring. The implementation should use a private "no default"
sentinel; `NOT_PROVIDED` remains only a matcher tuple value.

Open decision: whether a default should be modelled as a rule with zero
conditions and weight `1.0`. The preferred first design is to keep it explicit
as `default(...)` because diagnostics are clearer.

## Runtime Generated Matcher

The definition/specification phase should emit normal Python source for runtime
matchers.

Runtime matcher responsibilities:

- generate candidate tuples from named container views
- extract positional values required by the matcher rules using straight-line
  generated code
- evaluate rules lazily
- cache results by tuple identity/value key
- return selected resources and match tuples

Example runtime use:

```python
container = builder.build()

result = container.matchers.Getter.resolve(field, facade)
if result is not None:
    resource = result.resource
    match_tuple = result.match_tuple
```

For matchers that naturally enumerate all candidates:

```python
for result in container.matchers.Getter.sequence():
    ...
```

The exact container attachment shape is an implementation detail. The important
contract is that generated matchers operate over the frozen container and do not
mutate it.

## Implementation Contract

The first implementation should follow these invariants.

Definition objects:

- `MatcherSpec` owns name, inputs, rules, default resource, evaluated fields,
  and tuple schema.
- `MatcherInputSpec` owns input name and source collection/computed collection.
- `ScopedPropertyRef` is `(input, property)`.
- `MatcherEvaluatedFieldSpec` owns name, input dependencies, evaluator, and
  optional value type.
- `MatcherRuleSpec` owns conditions, weight, resource, and diagnostic name.
- `MatcherResult` owns selected resource, selected rule, score, records tuple,
  and values tuple.
- `MatcherResult.rule` is a diagnostic rule-name string or `None`, not a
  definition-time `MatcherRuleSpec` object. Generated and in-memory runtimes
  must return the same shape.

Tuple schema order:

- Tuple schema is computed deterministically by first occurrence while walking
  rules in declaration order and each rule's conditions in condition order.
- Duplicate scoped property refs or evaluated field refs are included once.
- The resulting order is fixed in generated code.
- Explicit user-declared tuple schemas can be added later if needed.

Candidate generation:

- V1 uses the Cartesian product of each input view's `.sequence()`.
- One input means one simple loop.
- Multiple inputs mean nested loops in input declaration order.
- Correlated/dependent inputs are not part of V1.

Runtime extraction:

- Generated code extracts tuple values with straight-line code in tuple-schema
  order.
- Scoped property refs use `getattr(record, storage_name, NOT_PROVIDED)` so
  missing variant properties are represented directly.
- Missing property values become `NOT_PROVIDED`.
- Evaluated fields call their generated/imported evaluator with the declared
  input records.
- No dictionary is used for tuple values.
- Specializing extraction by concrete variant class is a later optimization, not
  part of V1.

Runtime evaluation:

- Definition/code generation validates that same-score rules cannot collide.
- Generated code emits rule checks in descending score order. Declaration order
  is retained only as the stable order among same-score rules that cannot
  overlap.
- Rule checks use positional tuple indexes and tuple slices where useful.
- Non-contiguous rule checks should combine contiguous tuple slices, for
  example `values[0:2] + values[4:6] + values[8:10]`.
- Score is `len(rule.conditions) * rule.weight`.
- The first matching rule returns immediately.
- No match returns default if defined, else `None`.

Caching:

- `resolve(*records)` extracts `values` first and caches the winning
  selection by the positional values tuple.
- Cached entries store only the selected resource/rule/score. `resolve(...)`
  still returns a fresh `MatcherResult` with the concrete records passed to
  that call.
- If the values tuple is unhashable, runtime skips caching for that tuple and
  evaluates normally.
- `sequence()` can reuse `resolve(...)` for each candidate tuple.
- Cache is per matcher instance attached to one frozen container.

Resource protocol:

- Matcher core treats resources as opaque.
- For code generation, every resource must be source-emittable.
- V1 can require resources to be emitted as generated module binding names.
- Astichi resources are wrappers outside matcher core.

Generated runtime shape:

```python
resolve(*records) -> MatcherResult | None
sequence() -> Iterator[MatcherResult]
```

- The generated matcher is initialized with the frozen container.
- It does not mutate the container.

Diagnostics:

- Equal-score overlap errors include matcher name, score, candidate
  rules/resources, and the compatible condition positions.
- Invalid scoped property or evaluated field references fail during definition
  or code generation.
- Non-emittable resources or evaluators fail during code generation.

## Caching

The first implementation should use lazy cached evaluation, not a full
precomputed index.

Rationale:

- decorator runs are bounded by class decoration, not hot request loops
- rule sets should be small to moderate
- direct generated tuple loops are simple and inspectable
- caching avoids repeated rule scans for the same tuple
- an indexed implementation can be added later without changing matcher
  semantics

Cache key should include:

- matcher identity
- extracted tuple values

The cache must not be keyed by `id(record)` alone. The matcher decision is a
function of the extracted tuple values, not object identity. Equivalent records
should reuse the same selected resource/rule/score while preserving the concrete
records in each returned result.

## Resources

Matcher resources are opaque to the matcher core.

A resource may be:

- an Astichi composable wrapper
- a generated operation function
- a value object
- another matcher-selected resource

The only matcher requirement is that resources can be emitted into the generated
spec module and returned by runtime matcher evaluation.

Astichi-specific resources should be wrapped outside matcher core. The wrapper
can carry:

- the Astichi composable or importable recipe
- static metadata
- binding strategy
- diagnostics name

The matcher result returns the wrapper as an opaque resource.

## Dependency Between Matchers

Some resources selected by one matcher may depend on resources selected by
another matcher. The matcher core should allow resources to be opaque enough to
perform that lookup later.

Do not predefine a fixed set of matcher targets such as
`PropertyGetterMatcher`. Matchers are user/developer-declared surfaces. A
capsule can introduce a new matcher if it introduces a new decision point.

Cycles between matchers are a later diagnostic problem. The first matcher core
should keep evaluation lazy and explicit so dependency cycles are visible when a
resource asks for another matcher result.

## Relationship To DDSContainer

`DDSContainer` supplies frozen records and generated named collection views.

Matchers consume those views:

```python
for field in container.InitSignatureFields.sequence():
    ...
```

The container does not decide which resource wins. The matcher does.

The matcher does not own records. It reads from the frozen container and caches
its own results.

## Initial Tests

Use focused unit tests for matcher mechanics.

Initial coverage:

- more-specific rule wins over less-specific rule
- small weight multiplier breaks a same-specificity tie
- equal-score compatible rules reject at definition/codegen
- equal-score incompatible rules are allowed
- missing property yields `NOT_PROVIDED`
- explicit `NOT_PROVIDED` condition can match
- evaluated field condition can match
- evaluated field can depend on multiple inputs
- default resource is returned when no rule matches
- matcher cache returns stable result for repeated tuple evaluation
- resources are opaque objects and are returned unchanged
