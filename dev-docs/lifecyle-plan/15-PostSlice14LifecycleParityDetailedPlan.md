# Post-Slice-14 Lifecycle Parity Detailed Plan

## Purpose

Define the lifecycle parity roll-build that follows the current
`lcb/slice-14-call-arguments` baseline.

This document exists because the initial lifecycle slicing plan proves the
generic DDS/fluent machinery and the first lifecycle staircase, while full
lifecycle parity still requires decorator/helper generation, complete callable
injection, transaction behavior, advanced field kinds, resource policies, and a
parity harness.

The objective is not to create a second lifecycle engine. Each slice must keep
using the same model:

- declarations become DDS records
- rule matchers select generated resources
- generated resources are Astichi composables or source-emittable values
- ports assemble class, method, parameter, statement, and call-argument shapes
- operation records and operation phases drive runtime methods
- goldens prove successful generated source
- bespoke tests cover diagnostics and narrow runtime behavior

## Baseline Assumptions

The post-slice-14 baseline includes:

- field-family and lifecycle concept records
- generated resource values
- state/facade contribution records
- managed/const staircase rendering
- callable fact production foundations
- resource hook foundations
- initvar closure classification
- retained initvar state storage
- method call-argument records and current-facade injection

The next slices should not add new DDS-core concepts unless the existing
record, matcher, resource, port, and aggregate-operation model cannot express
the needed behavior cleanly. If Astichi is awkward for a template, prefer
improving Astichi over writing string-generation workarounds.

## Slice 15: Generated Decorator And Helper Surface

### Objective

Emit and exercise the generated lifecycle decorator/helper surface:

- `managed_context`
- `lifecycle_field`
- kind-specific helper functions where they reduce user-facing boilerplate
- generated class metadata needed by later MRO merge and parity tests

The generated decorator and generated field-spec helper functions must not
invoke the Python parser at decoration time. They should create records and
resources directly.

### Fluent/DDS Shape

Expected concept additions:

```python
LifecycleHelpers = concept.extends(LifecycleConcept)

LifecycleHelpers.helpers.decorator(
    "managed_context",
    resource=from_astichi_code(
        """
        astichi_comment("helper: managed_context decorator")
        def managed_context(*decorator_args, **decorator_kwargs):
            ...
        """
    ),
)

LifecycleHelpers.helpers.field_spec(
    "lifecycle_field",
    output=FieldDeclarations,
    resource=from_astichi_code(
        """
        astichi_comment("helper: lifecycle_field")
        def lifecycle_field(*, name=None, kind=None, default=REQUIRED, **options):
            ...
        """
    ),
)
```

The exact helper-builder names may change, but the lowering must produce
ordinary concept records/resources. There should be no helper-specific runtime
engine.

### Expected Golden

`tests/data/gold_src/dds_lifecycle_decorator_surface.py`

Expected materialized excerpt:

```python
REQUIRED = object()

def lifecycle_field(*, name=None, kind=None, default=REQUIRED, **options):
    return FieldDeclarationInput(
        name=name,
        kind=kind,
        default=default,
        options=options,
    )

def managed_context(_cls=None, **context_options):
    def decorate(cls):
        input_records = harvest_lifecycle_inputs(cls, context_options)
        runtime = build_lifecycle_runtime(input_records)
        return runtime.decorate(cls)
    if _cls is None:
        return decorate
    return decorate(_cls)
```

### Runtime Check

Decorate a small class using generated helpers and verify:

- field declarations are harvested into DDS input records
- generated metadata is attached to the resulting class
- helper-created records match direct record construction

### Bespoke Tests

- helper rejects unknown kind
- helper rejects unsupported option for kind
- decorator-time code path does not call parser entry points

## Slice 16: Default And Factory Initialization

### Objective

Implement default and factory ordering for constructor parameters and state
initialization.

This slice covers:

- explicit default values
- `default_factory`
- `working_default_factory`
- `initial_working`
- constructor argument supplied vs omitted
- default/factory callables that require supported injections

### Fluent/DDS Shape

Represent initialization as records, not special cases:

```python
InitValuePlan = concept.records.InitValuePlan(
    field=FieldRef,
    phase=InitPhase,
    value_resource=GeneratedResource,
    call_args=CallArguments,
    target=StateRef,
)

DefaultTemplate.rule.factory(
    when=(field.prop(DefaultFactory).is_provided(),),
    resource=from_astichi_code(
        """
        astichi_comment("init default_factory")
        self.astichi_ref(external=target_path)._ = factory(
            *astichi_hole(call_args)
        )
        """
    ),
)
```

Factories should use the same callable fact and method-call-argument machinery
as hooks and validators. Do not introduce a default-only invocation model.

### Expected Golden

`tests/data/gold_src/dds_lifecycle_defaults_factories.py`

Expected materialized excerpt:

```python
class ExampleState:
    __slots__ = ("_count_current", "_label_current", "_token_current")

    def __init__(self, *, count=0, label=REQUIRED):
        if label is REQUIRED:
            label = make_label()
        self._count_current = count
        self._label_current = label
        self._token_current = make_token(self)
```

### Runtime Check

- explicit constructor argument wins over default
- default value is not recomputed per access
- factory is called exactly once per instance when argument is omitted
- factory receives requested injection values

### Bespoke Tests

- unsupported factory parameter rejects during callable analysis
- both default and default_factory reject unless the kind explicitly allows it
- required constructor parameter omitting value raises the generated diagnostic

## Slice 17: Full Callable Injection Matrix

### Objective

Complete callable injection for all callable surfaces:

- default factories
- working/default factories
- freeze/thaw/state-copy/state-factory callables
- commit order keys
- commit validators
- before/after/rollback hooks
- resource retain/release/close hooks

Supported injection names should be represented as data, not hard-coded in each
template.

### Fluent/DDS Shape

Extend callable facts and call arguments:

```python
CallableInjection.rule.current(
    when=(param.prop(Name).eq("current"),),
    resource=from_astichi_code("current_facade"),
)

CallableInjection.rule.working(
    when=(param.prop(Name).eq("working"),),
    resource=from_astichi_code("working_facade"),
)

CallableInjection.rule.retained_initvar(
    when=(param.prop(Name).matches(RetainedInitvarNames),),
    resource=from_astichi_code(
        """
        state.astichi_ref(external=retained_initvar_path)
        """
    ),
)
```

The actual matcher API should follow the current matcher/resource surfaces.
The important constraint is that every injected argument is a `MethodCallArgument`
or equivalent call-argument record consumed by a call site.

### Expected Golden

`tests/data/gold_src/dds_lifecycle_callable_injection_matrix.py`

Expected materialized excerpt:

```python
def _run_validator(self, state, tx_group):
    previous = self._previous_facade_for(tx_group)
    current = self._current_facade_for(tx_group)
    working = self._working_facade_for(tx_group)
    validate_balance(
        self,
        current,
        working,
        previous,
        tx_group,
        state._request_id_initvar,
    )
```

### Runtime Check

- each supported parameter name receives the expected runtime object
- retained initvars are available to post-init callables
- constructor-only initvars are rejected for post-init callables

### Bespoke Tests

- unknown callable parameter rejects with callable name and parameter name
- duplicate injection provider for the same parameter rejects
- callable signature facts are cached/deterministic

## Slice 18: Transaction Manager And Active Transaction Semantics

### Objective

Generate the transaction manager surface and active transaction state needed by
managed, transient, hooks, validators, and cleanup phases.

This slice proves the runtime model, not every hook phase.

### Fluent/DDS Shape

Represent transaction groups and active transaction slots as state/method
contributions:

```python
TransactionRuntime = concept.records.TransactionRuntime(
    tx_group=TxGroup,
    tx_index=TxIndex,
    active_slot=StateRef,
    current_store=StateRef,
    working_store=StateRef,
)

LifecycleMethods.method.begin_transaction(
    phase=TransactionPhase.begin,
    body=from_astichi_code(
        """
        astichi_comment("transaction begin")
        self._state.astichi_ref(external=active_slot)._ = True
        """
    ),
)
```

### Expected Golden

`tests/data/gold_src/dds_lifecycle_transaction_manager.py`

Expected materialized excerpt:

```python
class Example:
    def begin_transaction(self, tx_group="default_transaction"):
        tx_index = self.__yidl_tx_index_by_name__[tx_group]
        self._state._active_transactions[tx_index] = True

    def rollback(self, tx_group="default_transaction"):
        tx_index = self.__yidl_tx_index_by_name__[tx_group]
        self._rollback_working_values(tx_index)
        self._state._active_transactions[tx_index] = False
```

### Runtime Check

- managed writes update working state while a transaction is active
- rollback clears working state for the selected transaction group
- no-active-transaction behavior matches the selected policy
- unknown transaction group rejects

### Bespoke Tests

- nested transaction policy diagnostic
- transaction group lookup diagnostic
- active-state array length matches transaction group count

## Slice 19: Commit/Rollback Pipeline Parity

### Objective

Generate the ordered commit/rollback operation pipeline:

- commit order keys
- commit validators
- before-commit hooks
- value promotion
- after-commit hooks
- rollback hooks
- cleanup phase hooks

This slice uses contribution records and operation phases. It must not hard-code
a monolithic commit method.

### Fluent/DDS Shape

```python
OperationContribution = concept.records.OperationContribution(
    phase=OperationPhase,
    tx_group=TxGroup,
    order=Order,
    resource=GeneratedResource,
    call_args=CallArguments,
)

CommitPipeline = concept.operations.pipeline(
    "CommitPipeline",
    source=OperationContributions,
    order_by=(PhaseOrder, TxIndex, Order, SourceOrder),
)
```

If `concept.operations.pipeline(...)` is too specific, keep it as fluent sugar
over `dds.operation(...)`.

### Expected Golden

`tests/data/gold_src/dds_lifecycle_commit_pipeline.py`

Expected materialized excerpt:

```python
def commit(self, tx_group="default_transaction"):
    tx_index = self.__yidl_tx_index_by_name__[tx_group]
    ordered = sorted(
        self.__yidl_commit_items__[tx_index],
        key=lambda item: item.order_key(self),
    )
    for item in ordered:
        item.validate(self)
    for item in ordered:
        item.before_commit(self)
    self._promote_working_values(tx_index)
    for item in ordered:
        item.after_commit(self)
```

### Runtime Check

- order key determines commit order
- validator can stop commit before promotion
- before/after hooks run in deterministic order
- rollback restores working state after validation failure

### Bespoke Tests

- duplicate order-key diagnostic
- duplicate validator diagnostic
- rollback aggregation diagnostic once cleanup exceptions exist

## Slice 20: Advanced Managed Value Semantics

### Objective

Complete managed value behavior:

- `freeze`
- `thaw`
- `initial_working`
- `state_factory`
- `state_copy`
- compare mode
- ever-committed/current-state tracking if required by parity

### Fluent/DDS Shape

Model transformations as callable-backed resources selected by matchers:

```python
ManagedTransform.rule.freeze(
    when=(field.prop(Freeze).is_provided(),),
    resource=from_astichi_code(
        """
        astichi_comment("managed freeze")
        frozen_value = freeze(value, *astichi_hole(call_args))
        """
    ),
)
```

Callables use the callable injection matrix from Slice 17.

### Expected Golden

`tests/data/gold_src/dds_lifecycle_managed_advanced.py`

Expected materialized excerpt:

```python
def _set_count_working(self, value):
    value = thaw_count(value, self)
    self._state._count_working = copy_count(value)

def _promote_count(self):
    value = self._state._count_working
    if value is not _NO_WORKING_VALUE:
        self._state._count_current = freeze_count(value, self)
        self._state._count_working = _NO_WORKING_VALUE
```

### Runtime Check

- thaw is applied when accepting user input
- freeze is applied before current-state promotion
- state_copy prevents aliasing between current and working state
- initial_working is visible in working facade before explicit write

### Bespoke Tests

- unsupported transform callable parameter rejects
- compare-mode record selection is deterministic
- invalid transform result diagnostic if validation is available

## Slice 21: Field Kind Expansion

### Objective

Add parity for additional lifecycle field kinds:

- `static`
- `transient`
- `local_store`
- `derived`
- `classvar`

This slice may be split if a kind exposes a missing generic concept. The first
implementation should still express each kind through the same family,
matcher, resource, and port model.

### Fluent/DDS Shape

```python
FieldSpecs.variant.StaticField(...)
FieldSpecs.variant.TransientField(...)
FieldSpecs.variant.LocalStoreField(...)
FieldSpecs.variant.DerivedField(...)
FieldSpecs.variant.ClassVarField(...)
```

Each variant contributes storage, property, init, method, and operation records
through rules. Do not create separate renderers per kind.

### Expected Golden

`tests/data/gold_src/dds_lifecycle_field_kinds.py`

Expected materialized excerpt:

```python
class ExampleState:
    __slots__ = (
        "_static_config",
        "_scratch_by_tx",
        "_local_cache",
        "_derived_total",
    )

class Example:
    __slots__ = ("_state",)

    @property
    def total(self):
        if self._state._derived_total is _UNSET:
            self._state._derived_total = compute_total(self)
        return self._state._derived_total
```

### Runtime Check

- static field rejects second assignment when policy requires immutability
- transient field requires active transaction if that is the selected policy
- local_store reset/close contribution runs
- derived value caches and invalidates according to generated rules
- classvar materializes on the generated class, not instance state

### Bespoke Tests

- unsupported option per kind rejects
- classvar/default_factory signature diagnostic
- derived dependency cycle diagnostic only if dependency graph is implemented

## Slice 22: Binding And Owned Resource Semantics

### Objective

Implement resource lifecycle parity for `binding` and `owned` fields:

- scalar retained resources
- mapping retained resources
- retain/release/close policies
- replacement cleanup
- rollback cleanup
- evict-last behavior where required

### Fluent/DDS Shape

```python
ResourcePolicy = concept.records.ResourcePolicy(
    field=FieldRef,
    shape=ResourceShape,
    retain=GeneratedResource,
    release=GeneratedResource,
    close=GeneratedResource,
    evict_last=EvictLastPolicy,
)
```

Resource cleanup contributes to the same operation phase records used by the
commit/rollback pipeline.

### Expected Golden

`tests/data/gold_src/dds_lifecycle_binding_owned_resources.py`

Expected materialized excerpt:

```python
def _replace_owner(self, value):
    old = self._state._owner_current
    if old is not _NO_RESOURCE:
        release_owner(old)
    self._state._owner_current = retain_owner(value)

def rollback(self, tx_group="default_transaction"):
    pending = self._state._owner_working
    if pending is not _NO_WORKING_VALUE:
        close_owner(pending)
        self._state._owner_working = _NO_WORKING_VALUE
```

### Runtime Check

- retained resource receives retain on assignment
- old scalar resource receives release/close on replacement
- mapping cleanup runs for removed entries
- rollback cleans pending owned resources

### Bespoke Tests

- invalid resource policy diagnostic
- scalar vs mapping shape mismatch diagnostic
- cleanup exception aggregation policy

## Slice 23: Multi-Facade State Routing

### Objective

Complete state/facade topology:

- state owns all mutable storage
- main/current/working facades own behavior only
- facades hold only state reference and role-specific metadata
- templates are selected by facade role
- simple field templates can be shared when routing is identical
- managed templates select current vs working paths by facade role

### Fluent/DDS Shape

```python
FacadeRole = concept.properties.FacadeRole(ClassRoleValue)

PropertyTemplate.rule.managed_current_facade(
    when=(
        field.prop(Kind).eq(MANAGED_KIND),
        facade.prop(FacadeRole).eq(CURRENT_FACADE),
    ),
    resource=from_astichi_code(
        """
        astichi_comment("managed current facade getter")
        return self._state.astichi_ref(external=current_path)
        """
    ),
)
```

### Expected Golden

`tests/data/gold_src/dds_lifecycle_multi_facade_routing.py`

Expected materialized excerpt:

```python
class ExampleState:
    __slots__ = ("_count_current", "_count_working")

class Example:
    __slots__ = ("_state",)

    @property
    def current(self):
        return ExampleCurrent(self._state)

    @property
    def working(self):
        return ExampleWorking(self._state)

class ExampleCurrent:
    __slots__ = ("_state",)

    @property
    def count(self):
        return self._state._count_current

class ExampleWorking:
    __slots__ = ("_state",)

    @property
    def count(self):
        if self._state._count_working is not _NO_WORKING_VALUE:
            return self._state._count_working
        return self._state._count_current
```

### Runtime Check

- all facades share one state object
- current facade cannot mutate working state
- working facade reads working value when present, current otherwise
- direct facade behavior matches selected policy

### Bespoke Tests

- missing state route diagnostic
- facade role with no template diagnostic
- facade property collision diagnostic

## Slice 24: MRO Merge And Override Parity

### Objective

Integrate decorator/helper harvesting with inherited class metadata:

- harvest base-class lifecycle metadata
- represent each base/current layer as input records
- run layered merge operation
- apply override policies per kind
- preserve source provenance in diagnostics

### Fluent/DDS Shape

Use the layered merge pattern from the earlier detailed plan, but now feed it
from generated decorator records:

```python
LifecycleMerge = concept.operations.layered_merge(
    "MergeLifecycleFields",
    source=LifecycleFieldLayers,
    target=MergedFields,
    identity=Name,
    policy=field_override_policy,
)
```

If the fluent helper is not yet justified, lower directly to
`dds.operation(...)`.

### Expected Golden

`tests/data/gold_src/dds_lifecycle_mro_override_parity.py`

Expected materialized excerpt:

```python
def harvest_lifecycle_inputs(cls, context_options):
    layers = []
    for layer_index, base in enumerate(reversed(cls.__mro__[1:])):
        definition = getattr(base, "__yidl_lifecycle_definition__", None)
        if definition is not None:
            layers.extend(definition.field_layers(layer_index))
    layers.extend(harvest_current_class_fields(cls, len(layers)))
    return layers
```

### Runtime Check

- derived field overrides compatible base field
- incompatible override rejects with base and derived provenance
- base class generated lifecycle metadata is reused without reparsing source

### Bespoke Tests

- diamond/base order deterministic
- override policy diagnostic includes field name and layer names
- current-class declaration wins only when policy allows it

## Slice 25: Lifecycle Parity Harness

### Objective

Create the parity harness that compares selected reference lifecycle scenarios
against generated YIDL lifecycle scenarios.

This is not a replacement for source goldens. It is a runtime confidence layer
for externally visible behavior.

### Harness Shape

```python
def run_lifecycle_scenario(impl, scenario):
    cls = impl.build_class(scenario)
    instance = cls(**scenario.constructor_args)
    return scenario.exercise(instance)
```

The harness should allow selecting the implementation through an explicit test
parameter or environment variable. Do not make generated source tests depend on
the reference backend.

### Expected Coverage

`tests/lifecycle/test_yidl_lifecycle_parity.py`

Scenarios:

- managed field construction/get/set
- const/static immutability
- multiple transaction groups
- commit validator failure
- commit order key ordering
- hook order
- transient active-transaction behavior
- binding/owned scalar cleanup
- binding/owned mapping cleanup
- multi-facade routing

### Bespoke Tests

This slice is mostly runtime/integration coverage. Bespoke diagnostic tests
remain in the slices that introduce each diagnostic.

## Post-Slice Stop Conditions

Stop and revise the plan before coding if any remaining parity slice requires:

- parser calls in generated decorator/runtime paths
- per-kind bespoke renderer functions
- source string concatenation for Astichi templates
- direct dependency on `pyrolyze` from generated YIDL code
- a new matcher or operation engine
- putting lifecycle-specific semantics into DDS core

## Canonical Golden Set

Post-slice-14 parity goldens should be:

- `dds_lifecycle_decorator_surface.py`
- `dds_lifecycle_defaults_factories.py`
- `dds_lifecycle_callable_injection_matrix.py`
- `dds_lifecycle_transaction_manager.py`
- `dds_lifecycle_commit_pipeline.py`
- `dds_lifecycle_managed_advanced.py`
- `dds_lifecycle_field_kinds.py`
- `dds_lifecycle_binding_owned_resources.py`
- `dds_lifecycle_multi_facade_routing.py`
- `dds_lifecycle_mro_override_parity.py`

Runtime parity coverage belongs in `tests/lifecycle/test_yidl_lifecycle_parity.py`.

