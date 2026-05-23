# YIDL State Field Proposal

Temporary proposal for a richer field-lowering model. This document is a
working design note, not yet the canonical P1 plan.

## 1. Problem

1. The current `StateRef` plan is too narrow if it only names individual field
   value homes.
2. A field can require a related state object, not just one value slot.
3. Examples:
   1. A `managed` field needs current value, working value, and field
      transaction state.
   2. A `transient` field needs active working state and transaction-window
      cleanup behavior.
   3. An `owned` field needs value homes plus ownership cleanup state.
   4. A `derived` field needs cache state and invalidation behavior.
4. Initialization is not a minor detail. The generator needs explicit rules for
   slot allocation, sentinel initialization, default resolution, callable
   wrappers, class constants, and per-event behavior.
5. YIDL should let behavior be written against semantic state objects, then
   lower those objects into flat state/store slots and Astichi-compatible ASTs.

## 2. Core Direction

1. Define field behavior through restricted Python control sources.
2. Control sources describe:
   1. Value homes.
   2. Associated per-field state objects.
   3. Class-level generated constants.
   4. Initialization rules.
   5. Event handlers such as read, write, begin, commit, rollback, and cleanup.
3. YIDL parses the control source with `ast.parse()`.
4. YIDL does not execute the control source during schema discovery.
5. YIDL harvests annotated fields, event methods, and marker metadata.
6. YIDL lowers semantic references inside event methods into Astichi-compatible
   AST fragments.
7. Astichi stitches and materializes the lowered fragments, but YIDL owns the
   lifecycle semantics.

## 3. Terminology

1. **Control source**. Restricted Python module-like fragment that defines a
   helper kind such as `managed`, `transient`, or `owned`. It is not wrapped in
   a required outer behavior class.
2. **State class**. Restricted Python class in the control source that
   declares slots needed by a field, transaction key, record, facade cache,
   or class surface.
3. **State field**. Annotated member of a state class. It becomes a generated
   flat slot unless explicitly marked as class-level metadata.
4. **Event method**. Restricted Python method marked as running at a lifecycle
   event.
5. **Semantic ref**. Reference in control-source code to a logical state object
   or member.
6. **Lowered ref**. Direct generated attribute name on the single state/store
   object.
7. **State layout**. Complete discovered set of generated slots and class
   constants for a target generated class.

## 4. Restricted Python Subset

1. Allowed at control-source top level:
   1. Class definitions.
   2. Annotated assignments.
   3. Simple literal defaults.
   4. Event methods.
   5. Marker decorators and marker calls that YIDL recognizes by name.
   6. Docstrings.
2. Allowed in state classes:
   1. Annotated fields.
   2. Literal defaults.
   3. Sentinel defaults such as `VOID` and `UNSPECIFIED`.
   4. `ClassVar[...]` annotations for generated class constants.
3. Initially disallowed:
   1. Runtime imports.
   2. Inheritance.
   3. Properties and descriptors.
   4. Metaclasses.
   5. Dynamic attribute creation.
   6. Arbitrary decorators.
   7. Top-level executable behavior.
4. Event method bodies use a Python subset compatible with Astichi lowering.
   Any unsupported Python construct must fail before code emission.

## 5. State Surfaces

1. P1 should model these semantic surfaces:

| Surface | Scope | Purpose |
|---|---|---|
| `record` | one per generated instance | shared store/control state |
| `field` | one per logical field | field value and sidecar state |
| `field_tx` | one per transaction-aware field | transaction-window state for that field |
| `tx` | one per transaction key | group control state |
| `facade` | one per generated facade kind | facade cache and view-specific helpers |
| `cls` | one per generated class | generated constants and metadata |
| `compile` | one per field/helper expansion | compile-time constants used during lowering |

2. A field has one identity: its declared field name.
3. A transaction-aware field can carry one `tx_index`, but the `tx_index` is
   field metadata, not part of the field identity.
4. Lowering may include `tx_index` in physical slot names when the state member
   belongs to transaction-routed state.

## 6. Field Spec And Transducer Parameters

1. A transducer must declare every parameter it reads. Selection predicates
   must not imply hidden field-spec vocabulary such as `has_default`.
2. A field helper is an API artifact that assembles transducers and supplies
   concrete parameter objects for each transducer expansion.
3. Parameters are semantic objects, not passive tags. They own validation,
   type rules, callable signature rules, selector helpers, and lowering hooks.
4. Initial P1 parameter object families:
   1. `FieldNameParameter` for the user-visible field name.
   2. `TypeParameter[T]` for `T`, `T | None`, and other accepted type
      expressions.
   3. `InitParameter[T]` for generated constructor exposure and constructor
      argument binding.
   4. `ValueParameter[T]` for a literal/object default value.
   5. `CallableRunner[T]` for lowered callables such as default factories,
      freeze/thaw functions, validators, and hooks.
   6. `TxNameParameter` for user transaction key names.
   7. `InitialValuePlan[T]` for normalized construction behavior derived from
      init exposure, default value, and default factory parameters.
5. `None` is a legal value when the field type permits it. `UNSPECIFIED` is
   the sentinel for omitted spec parameters or omitted optional constructor
   arguments.
6. Constructor exposure and construction behavior are separate:
   1. `init=True` means the generated constructor accepts a user argument for
      the field.
   2. `@on.construct...` means a generated code contribution runs in a
      construction stage.
   3. A literal `default` on an exposed constructor parameter becomes the
      Python signature default. The construct body then only assigns the
      parameter value.
   4. A `default_factory` cannot live in a Python signature. The constructor
      parameter defaults to `UNSPECIFIED`, then the selected construct snippet
      either assigns the supplied value or calls the factory runner.
   5. If there is no default source, an exposed constructor parameter defaults
      to `UNSPECIFIED` and emits the direct required-value check for that field.
   6. If no constructor argument, default value, or default factory can produce
      a required initial value, construction emits no generic decision ladder;
      the resolved plan either allows `VOID` or fails generation / emits one
      direct error.
7. Callable parameters lower to named runners before behavior snippets run.
   Behavior code calls the runner symbol. The Astichi-facing lowering later
   rewrites that symbol through `astichi_pass(...)` or the equivalent scoped
   bind reference.
8. Transducer composition unifies compatible parameters by name and rejects
   incompatible declarations. Example: two transducers can share
   `field_name`; they cannot silently disagree on whether `default_factory`
   accepts initvars, facade refs, or no arguments.
9. `InitialValuePlan` is a family of concrete contribution plans. Each variant
   emits only the parameter payload and construct snippet it needs:

| Variant | Constructor payload | Construct snippet |
|---|---|---|
| `InitDefaultValue` | `*, field: T = default_value` | `store.field = field` |
| `InitRequired` | `*, field: T = UNSPECIFIED` | `if field is UNSPECIFIED: raise ...; store.field = field` |
| `InitFactoryFallback` | `*, field: T = UNSPECIFIED` | `store.field = factory() if field is UNSPECIFIED else field` |
| `HiddenDefaultValue` | no parameter | `store.field = default_value` |
| `HiddenFactoryDefault` | no parameter | `store.field = factory()` |
| `HiddenUninitializedAllowed` | no parameter | no construct assignment; slot remains `VOID` |
| `MissingInitialValueError` | no parameter | generation error or one direct construction error, depending on helper policy |

10. Constructor parameter emission uses Astichi parameter holes, not a custom
   YIDL signature emitter:
   1. The generated constructor template exposes a parameter target such as
      `_y_init_params__astichi_param_hole__`.
   2. Each constructor-participating field contributes a payload carrier named
      `astichi_params`.
   3. Only the payload signature is inserted; the payload body is `pass`.
   4. YIDL should emit lifecycle field parameters as keyword-only constructor
      parameters. This avoids Python's non-default-after-default restriction
      for ordinary parameters while preserving declared field order.
   5. Defaults and annotations in the payload are ordinary Astichi expression
      surfaces: annotations may use annotation holes and defaults may use
      expression holes or bound external references.

Example constructor target:

```python
def __init__(self, _y_init_params__astichi_param_hole__):
    ...
```

Example payloads:

```python
# Required constructor value.
def astichi_params(*, amount: astichi_hole(amount_type)):
    pass

# Literal/default value lives directly in the keyword-only parameter. No
# runtime default selection code is needed for this field.
def astichi_params(*, limit: astichi_hole(limit_type) = astichi_hole(limit_default)):
    pass

# Factory fallback uses UNSPECIFIED in the signature because the factory must
# run during this field's initialization point when the user omitted the arg.
def astichi_params(*, token: astichi_hole(token_type) = UNSPECIFIED):
    pass
```

## 7. Example Field Control Shape

This is illustrative syntax, not yet locked.

```python
T = type_param("T")
default_factory_runner = callable_runner("default_factory", signature=DefaultFactory[T])
initial_value = initial_value_plan(init_value, default_value, default_factory_runner)

kind_name: str = class_constant("managed")
tx_index: int = compile_constant()


class CurrentValue:
    value: T = lazy_state(init=True)


class WorkingValue:
    value: T = lazy_state(init=False)


@on.construct_slots
def construct_slots():
    current.value = VOID
    working.value = VOID


@on.get_current
def get_current():
    return current.value


@on.set_working
def set_working(value):
    ensure_transaction()
    working.value = thaw_runner(value)
    mutated()


@on.commit_apply
def commit_apply():
    if working.value is not VOID:
        current.value = freeze_runner(working.value)
        working.value = VOID


@on.rollback
def rollback():
    if working.value is not VOID:
        working.value = VOID
```

Notes:

1. `current` and `working` are separate value surfaces. They are not two
   members on one shared field-value class.
2. `tx_index` is compile-time state. It belongs to field/helper expansion and
   physical-name lowering; it is not a runtime field transaction slot.
3. Presence of working state can be derived from `working.value is not VOID`
   unless a specific helper proves it needs a separate runtime bit.
4. `ever_committed` is intentionally omitted from the demo. If
   `initial_working` or another rule needs it, it should be introduced as a
   named semantic requirement, not as default field state.
5. Event markers use attribute syntax such as `@on.commit_apply`. They are
   behavior-owning marker objects, not strings, integers, enum values, or other
   passive tags.

## 8. Event Model

1. Events are generator-owned marker objects, not public runtime methods.
2. Event markers use attribute syntax such as `@on.rollback`.
3. Initial proposed event marker objects:

| Event | Meaning |
|---|---|
| `declare_slots` | discover slots and generated class constants |
| `construct_slots` | initialize state/store slots during instance construction |
| `wire_facades` | initialize facade references and weakref cache |
| `post_init` | run after constructor parameters/defaults have been assigned |
| `get_default` | resolve a default/current value |
| `get_current` | generate current-facade read behavior |
| `get_working` | generate working-facade read behavior |
| `set_current` | generate direct current assignment when allowed |
| `set_working` | generate working-facade assignment behavior |
| `join_tx` | enlist or ensure transaction participation |
| `validate_commit` | run per-field or per-group validation |
| `commit_prepare` | stage commit data before mutation |
| `commit_apply` | write committed state |
| `commit_cleanup` | release staged previous values after successful update |
| `rollback` | discard transaction-window mutations |
| `node_release` | release binding/owned nodes when lifetime ends |
| `invalidate` | clear derived/cache state |

4. Event handlers can be absent. Absence means the helper kind has no behavior
   for that event.
5. Multiple control sources can contribute to the same event. Ordering must be
   explicit in the transducer or derived from the field operation matrix.
6. Event handlers should be written once and unrolled for every matching field.
7. A rollback event only runs for fields mutated during the active transaction
   window for that group.

## 9. Marker Functions Inside Event Methods

Marker functions are parsed, not executed during schema discovery.

| Marker | Purpose |
|---|---|
| `@on.<event>` | marks an event method with a behavior-owning event marker object |
| `slot(surface.member)` | declares or references generated state |
| `lazy_state(...)` | declares runtime state initialized on instances |
| `compile_constant(...)` | declares compile-time state used during lowering |
| `class_constant(...)` | declares generated class-level metadata |
| `default_factory_runner(...)` | injected callable runner for the lowered default factory |
| `working_default_runner(...)` | injected callable runner for transient working defaults |
| `freeze_runner(value)` | injected callable runner for freeze behavior |
| `thaw_runner(value)` | injected callable runner for thaw behavior |
| `ensure_transaction()` | inserts transaction-join behavior |
| `mutated()` | marks the current field as rollback-relevant |
| `release_node(value)` | inserts binding/owned node release behavior |

The exact marker names are open. The important rules are that event markers are
not strings, integers, enums, or passive tags, and marker calls lower to
explicit Astichi snippets before final materialization.

## 10. Enum And Passive Tag Rule

1. No enums without explicit project-owner approval.
2. Do not get around that rule with magic strings, magic integers, sentinel
   strings, or other passive tags.
3. If a concept has semantics, it must be represented by an object or class
   that can own those semantics.
4. Event markers, state surfaces, state refs, transducers, callable injectors,
   lowering policies, and validation policies are semantic concepts.
5. Passive labels are acceptable only when the project owner explicitly agrees
   that they are truly inert and local.

## 11. Lowering Model

1. Parse the control source into a Python AST.
2. Harvest state classes and build a semantic state schema.
3. Harvest event methods and attach them to lifecycle event names.
4. Build a target class field layout from author fields and transaction keys.
5. For each field/helper pair:
   1. Instantiate semantic refs for every required state member.
   2. Allocate physical slot names through `StateNaming`.
   3. Rewrite event method ASTs so semantic refs become direct state/store
      attributes.
   4. Bind callable wrappers such as defaults, freeze/thaw, validators, and
      hooks.
   5. Unroll the event snippet into the target generated method.
6. Astichi receives already-semantic-lowered refs and performs AST composition,
   scope hygiene, marker stripping, and materialization.
7. Astichi must not know what `managed`, `field_tx`, or `commit` means.

## 12. Identifier Insertion

1. Control-source code should be written against stable semantic identifiers:
   `current`, `working`, `field_tx`, `tx`, `record`, `facade`, `cls`, and
   `compile`.
2. The lowering pass replaces those identifiers with Astichi references or
   direct state/store names.
3. For virtual execution tests, those identifiers may map to real lightweight
   objects.
4. For generated code, those identifiers lower to flat attributes on the
   single state/store object or to generated class attributes.
5. Physical names are never written by control-source authors.

Example lowering:

```python
working.value = thaw_runner(value)
```

May lower to:

```python
state._y_wv_t0_balance = _y_thaw_balance(value)
```

The exact slot spelling is owned by `StateNaming`, not by the control source.

## 13. Initialization

1. Initialization is generated in phases:
   1. Allocate main facade.
   2. Allocate the single state/store object.
   3. Initialize class constants if not already materialized.
   4. Initialize all generated state/store slots.
   5. Wire facade cache and transaction manager references.
   6. Consume constructor parameters and initvars.
   7. Run field initialization in declared order.
   8. Run post-init hooks.
2. State classes define the required slots and default initializers.
3. Event handlers define behavior that cannot be expressed as static defaults.
4. `VOID` means runtime not-yet-initialized value.
5. `UNSPECIFIED` means a spec parameter or optional constructor argument was
   omitted.
6. Generated initialization must be sequential unless a transducer explicitly
   provides a safe dependency ordering rule.

## 14. Class Fields

1. Control sources may define generated class constants.
2. Class constants are used for:
   1. Helper kind names.
   2. Transaction group metadata.
   3. Field descriptor metadata useful for diagnostics.
   4. Callable registries.
   5. Static lookup tables needed by dynamic fallback helpers.
3. Class constants are not per-instance state.
4. Class constants must use generated-internal names unless intentionally
   exposed as public API.
5. Public class-level lifecycle surfaces must be explicit in the field helper
   spec, not accidental byproducts of lowering.

## 15. Automatic Field Discovery

1. The generator can discover required physical slots from:
   1. State class annotated fields.
   2. Event method semantic refs.
   3. Marker calls.
   4. Field descriptors and transaction metadata.
2. Discovery should be deterministic and complete before code emission.
3. Unknown semantic refs fail during discovery.
4. Ambiguous refs fail during discovery.
5. A state member referenced in behavior but not declared can either:
   1. Fail strictly by default.
   2. Be allowed only if a marker explicitly declares it.
6. Strict declaration is the safer P1 default.

## 16. TDD Shape

Initial tests should target the proposal without requiring full lifecycle
generation.

1. Parse a restricted control source and discover state classes.
2. Reject unsupported class syntax.
3. Discover state fields and class constants.
4. Discover event methods and their event names.
5. Lower semantic refs for one field into deterministic physical names.
6. Lower the same control source for two fields and verify both field-specific
   slot sets are generated.
7. Verify `tx_index` is resolved from field metadata, not from the ref itself.
8. Verify event snippets lower to valid Python AST.
9. Verify virtual-object execution and flattened execution produce equivalent
   results for a minimal managed field.
10. Verify rollback snippets only run for fields marked mutated in the active
    transaction window.

## 17. Candidate Module Layout

```text
src/yidl/codegen/state_schema.py
src/yidl/codegen/state_refs.py
src/yidl/codegen/state_naming.py
src/yidl/codegen/control_parser.py
src/yidl/codegen/control_events.py
src/yidl/codegen/field_lowering.py
src/yidl/codegen/astichi_lowering.py
```

1. `state_schema.py` owns parsed state class data structures.
2. `state_refs.py` owns semantic references to surfaces and members.
3. `state_naming.py` owns physical slot/class-name generation.
4. `control_parser.py` parses restricted Python control sources.
5. `control_events.py` validates event names and event method signatures.
6. `field_lowering.py` binds control sources to concrete field descriptors.
7. `astichi_lowering.py` is the only layer that imports Astichi.
8. Runtime modules must not import these codegen modules.

## 18. Open Questions

1. Whether event markers should be decorators, class attributes, or explicit
   function calls.
2. Whether state members must always be declared before reference.
3. Whether control sources can compose through inheritance later.
4. How much Python expression syntax event methods should allow before Astichi
   lowering.
5. How virtual execution tests should represent `field`, `field_tx`, `tx`,
   `record`, `facade`, and `cls`.
6. Which callable runner signatures are accepted for each field helper and
   lifecycle event.
7. Whether control-source text belongs in `.yidl` grammar, fenced Python, or
   generated Python libraries.
8. How much of the current `StateRefNamingPlan.md` survives after this richer
   state-field model lands.

## 19. Working Conclusion

This model turns `StateRef` into one piece of a broader state-field lowering
system. The immediate next useful implementation slice is no longer just
`PublishedValueRef` / `WorkingValueRef`; it is a restricted control-source
parser plus state-schema discovery, followed by deterministic lowering for one
minimal `managed` control source.
