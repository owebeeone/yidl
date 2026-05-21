# YIDL Transactional Base Phase C Plan

## Scope

Phase C is only parameterized lifecycle `default_factory` support.

Phase A proved generated transactional behavior. Phase B proved the decorator
frontend, inheritance harvesting, generated-base peeling, and decorator-path
goldens. Phase C should stabilize constructor value evaluation before adding
more field kinds or transaction hook behavior.

## Goals

1. Support lifecycle field factories whose callable parameters name other
   constructor-visible values.
2. Generate direct keyword calls, not `locals()`-based binding.
3. Compute dependency order before source generation.
4. Reject unknown providers and dependency cycles at decorator time.
5. Preserve the Phase B unpacked generated boundary.

## Design Note: Future Feature YIDL

Phase C is not itself a feature-YIDL split. It should still be authored so the
default-factory dependency feature can move into a later
`lifecycle_default_factories.yidl` layer without changing semantics. Keep the
new schema rows, computed operation, matchers, contributions, and diagnostics
bounded to default-factory dependency evaluation. Phase D owns physically
splitting the YIDL files and proving merge behavior.

## Non-Goals

1. Do not add new field kinds.
2. Do not split lifecycle into feature YIDL files in this phase.
3. Do not add validator, hook, owned, binding, or transient semantics.
4. Do not introduce `__post_init__` or user `__init__` chaining.
5. Do not solve general dependency language features beyond factory parameter
   names.

## User Surface

```python
@lifecycle
class Example:
    SCALE: int = classvar(default=10)
    v1: int
    seed: int = initvar(init=False, default=4)
    temp: int = initvar(init=False, default_factory=lambda seed, v1: seed + v1)
    v2: int = managed(default_factory=lambda v1: v1 + 2)
    v3: int = managed(default_factory=lambda v2, v1: v1 + v2 + 2)
    v4: int = managed(init=False, default_factory=lambda v3: v3 * 2)
    v5: int = managed(init=False, default_factory=lambda SCALE, v4: SCALE + v4)
```

The generated constructor should evaluate `v2` before `v3` even though the
field declaration order is `v1`, `v2`, `v3` only accidentally compatible here.
It should then evaluate `v4` after `v3`.

Generated source should first assign every non-`default_factory` value into the
backing state. It should also assign caller-provided values for
`default_factory` fields into state before any later factory can read them.
After that, factory providers that are stored fields or classvars should be
read uniformly through `self.<name>`. Initvars remain locals because they are
not stored on `self` in Phase C.

`initvar(init=False)` has no constructor parameter. In Phase C it is still
allowed to be a provider if it has a `default` or `default_factory`; it lowers
to a local value before dependent factories run:

```python
seed = _Example_seed_default
temp = _Example_temp_default_factory(seed=seed, v1=self.v1)
```

`initvar(init=False)` with no `default` and no `default_factory` is rejected
because it has no value source. Phase C does not store initvars in state. If
the transient phase needs reusable temporary provider state, that storage
policy belongs to Phase G.

Init fields keep the sentinel guard because the caller can provide a value.
When the caller omits the value, the factory call uses `self.<name>` for stored
providers:

```python
state._y_v1_current = v1

if v2 is _HAS_DEFAULT_FACTORY:
    v2 = _Example_v2_default_factory(v1=self.v1)
state._y_v2_current = v2

if v3 is _HAS_DEFAULT_FACTORY:
    v3 = _Example_v3_default_factory(v2=self.v2, v1=self.v1)
state._y_v3_current = v3
```

For an `init=False` field, the constructor has no `v4` parameter, so there is
no sentinel to test. The generated source should assign the computed value
unconditionally at the correct dependency point:

```python
v4 = _Example_v4_default_factory(v3=self.v3)
state._y_v4_current = v4
```

No generated code should use `locals()` for factory argument binding.

Classvars follow the same stored-provider lowering: the provider parameter name
stays identical to the classvar name and the value is read through `self`.

```python
v5 = _Example_v5_default_factory(SCALE=self.SCALE)
state._y_v5_current = v5
```

Do not rename classvar provider parameters to lowercase aliases.

Initvars are the exception. Both `init=True` and `init=False` initvars remain
local constructor values and are passed directly by local name:

```python
v6 = _Example_v6_default_factory(seed=seed, v3=self.v3)
```

Expected runtime values for `Example(v1=1)`:

```text
seed = 4
temp = 5
v2 = 3
v3 = 6
v4 = 12
v5 = 22
```

Factory `self.<name>` reads use the generated lifecycle property. During
construction, this is the first user-visible access and no transaction is in
flight, so the property reads the initialized current value. No
transaction-staleness path is triggered during construction.

## Fact Model

Phase C should add computed facts rather than pushing dependency logic into
templates:

```text
DefaultFactoryDependency
DefaultFactoryEvaluationStep
DefaultFactoryDiagnostic
```

Candidate properties:

```text
DependencyOwner
ConsumerFieldId
ConsumerFieldName
ProviderName
ProviderFieldId
ParamName
ParamOrder
EvalOrder
```

The harvester can collect primitive facts:

- whether a field has `default_factory`
- the callable object
- the callable parameter names

The YIDL-generated computed operation should derive dependency rows and
evaluation steps.

The dependency graph and topological sort operate on the merged field set after
Phase B inheritance remapping. Evaluation steps are emitted across the local
and inherited union.

## Provider Rules

Allowed providers:

- stored plain, managed, and classvar values readable as `self.<name>` after
  assignment into state/class-visible storage
- caller-provided values for default-factory fields after they have been
  assigned into state
- inherited fields after Phase B remapping, if they are visible in the merged
  field set
- initvars with `init=True`, passed as local variables rather than `self.<name>`
- initvars with `init=False` when they have a `default` or `default_factory`;
  they lower to local provider values and are not stored in state in Phase C

Rejected providers:

- unknown names
- fields whose value cannot exist before the factory call
- `initvar(init=False)` with no `default` and no `default_factory`
- dependency cycles

Validation runs while materializing the generated lifecycle source for the
decorated class. Failures surface as `LifecycleDefinitionError` from the
decorator with the offending class, field, and provider when available.

Diagnostic examples:

```text
Example: default_factory dependency cycle: v2 -> v3 -> v2
Example.v2: default_factory references unknown name 'vX'
Example.v2: default_factory cannot reference 'temp' (initvar has no default or default_factory)
```

## Generated Boundary

The build function continues to receive unpacked keyword-only values:

```python
_Example_v2_default_factory=<callable>
_Example_v3_default_factory=<callable>
```

`_HAS_DEFAULT_FACTORY` is a generated-source-private sentinel imported from the
YIDL runtime sentinel surface. It must be a single shared object for all
generated lifecycle classes so `is` checks are stable across inheritance
chains. The generated source should import it rather than create a per-class
`object()` sentinel. It is analogous to the existing generated `VOID`
identity-sentinel usage but belongs in runtime because constructor defaults may
cross generated-class boundaries.

Do not introduce generic `defaults` or `default_factories` dictionaries.

## Implementation Slices

### C1: Harvester Parameter Discovery

Deliverables:

- inspect factory callable signatures
- store parameter names as primitive harvested facts
- preserve existing zero-argument factories
- refine the Phase B `initvar(init=False)` skip: carry through initvars with a
  `default` or `default_factory` as local providers, and reject initvars with
  neither using a targeted diagnostic

Verification:

- focused harvester tests for zero-arg and parameterized factories
- focused harvester tests for `initvar(init=False, default=...)` and
  `initvar(init=False, default_factory=...)`
- unsupported callable signature diagnostics: reject positional-only
  parameters, `*args`, and `**kwargs` because provider binding is by name
- callable parameter defaults do not create optional dependencies; every named
  parameter is still resolved as a provider. Optional positional-only
  parameters are ignored only to preserve zero-argument builtin factories such
  as `list`; required positional-only parameters still reject.

### C2: Computed Dependency Operation

Deliverables:

- dependency and evaluation-step collections
- computed operation for provider resolution and topological sort
- diagnostics for unknown provider and cycle

Verification:

- operation-level tests for graph order, unknown provider, and cycle

### C3: Generated Constructor Rewire

Deliverables:

- YIDL contributions that emit direct factory calls with named arguments
- constructor assignments ordered by computed evaluation steps
- inherited provider support

Verification:

- decorator-path golden with `v1`, `v2`, `v3` dependency chain
- generated source assertions: direct keyword calls, no `locals()`

## Golden Shape

Suggested fixture:

```text
tests/data/gold_src/yidl_transactional_phase_c_default_factories.py
```

Suggested materialized outputs:

```text
tests/data/goldens/materialized/yidl_transactional_phase_c_default_factories/decorator.py
tests/data/goldens/materialized/yidl_transactional_phase_c_default_factories/decorator_prettier.py
tests/data/goldens/materialized/yidl_transactional_phase_c_default_factories/generated_output.py
tests/data/goldens/materialized/yidl_transactional_phase_c_default_factories/generated_output_prettier.py
```

## Roll-Build

Phase C is a roll-build candidate after the source shape is reviewed.

Suggested tag prefix:

```text
txphaseC-factories/
```

Recommended slices:

1. `start`
   - clean-tree tag before work begins
2. `C1-harvester-factory-params`
   - discover callable parameter names
   - reject positional-only, `*args`, and `**kwargs`
   - add `_HAS_DEFAULT_FACTORY` runtime sentinel
   - refine `initvar(init=False)` handling so default/factory initvars become
     local providers and no-source initvars reject
   - focused harvester/marker tests
3. `C2-factory-fact-schema`
   - add dependency, evaluation-step, and diagnostic fact schema
   - add primitive harvested fields needed by generated runtime
   - verify parser/compiler/golden source still materializes without behavior
     change
4. `C3-dependency-operation`
   - implement provider resolution and topological sort operation
   - emit diagnostics for unknown providers and cycles
   - focused operation-level tests
5. `C4-constructor-rewire`
   - assign non-factory values into state before factory reads
   - sentinel-gate `init=True` factory fields
   - always compute `init=False` factory fields
   - pass stored providers as `self.<name>`
   - pass initvars as locals
   - verify direct keyword calls and no `locals()`
6. `C5-decorator-golden`
   - add end-to-end decorator-path golden for the canonical fixture
   - assert runtime values for `v1`, `seed`, `temp`, `v2`, `v3`, `v4`, and
     `v5`
   - cover classvar provider lowering as `SCALE=self.SCALE`
   - cover inherited provider behavior if it was not already proven in C4
7. `C6-boundary-cleanup`
   - update docs for implementation drift
   - full regression
   - confirm no generic `defaults` / `default_factories` dictionaries
   - confirm `_HAS_DEFAULT_FACTORY` is runtime-imported and shared

Stop if the computed-operation model needs new YIDL grammar.

## Follow-On Phases

The former umbrella Phase C has been split:

- Phase D: lifecycle feature-YIDL layering
- Phase E: diagnostics and attribute discipline
- Phase F: transaction validators, order keys, hooks, and current setter policy
- Phase G: transient fields
- Phase H: owned fields
- Phase I: binding fields
- Phase J: productionization and replacement readiness
