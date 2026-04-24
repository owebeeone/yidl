# YIDL Lifecycle Data Model Requirements

Temporary design note. This intentionally avoids YIDL syntax and transducer
syntax. The goal is to define the semantic data model the compiler needs before
choosing how authors spell it.

## 1. Purpose

1. Describe lifecycle behavior as data first.
2. Make code generation a consequence of resolved semantic objects, not a
   consequence of ad hoc syntax flags.
3. Support composition of small behavior pieces without emitting generic
   runtime decision ladders.
4. Preserve lifecycle semantics while allowing optimized, flattened generated
   code.
5. Keep Astichi as the AST stitching/materialization layer; YIDL owns lifecycle
   meaning.

## 2. Model Requirements

1. The data model must represent author-visible declarations:
   1. Target class.
   2. Facades.
   3. Field declarations.
   4. Helper names such as `managed`, `transient`, and `initvar`.
   5. Constructor parameters.
   6. Callable parameters such as factories, hooks, validators, freeze, and
      thaw.
2. The data model must represent generated-only structures:
   1. Physical store slots.
   2. Class constants.
   3. Callable runner functions.
   4. Constructor signature contributions.
   5. Constructor body contributions.
   6. Facade getter/setter contributions.
   7. Transaction callback contributions.
   8. Cleanup/refcount contributions.
3. The data model must produce concrete plan objects before code emission.
4. A concrete plan emits exactly the snippets needed for its case.
5. The generator must not emit a generic `if/elif` ladder when the case is
   known at generation time.
6. Variants with semantics must be classes/objects that own behavior. Do not
   use enums, magic strings, or passive integer tags.

## 3. Core Entities

| Entity | Owns | Notes |
|---|---|---|
| `TargetClassModel` | class name, base-class policy, facade models, fields, tx groups | One per generated user class. |
| `FacadeModel` | facade name and facade capability objects | A facade can have multiple capabilities. |
| `FieldModel` | field name, annotation, helper assembly, parameters, declaration order | Field name is the stable identity. |
| `HelperModel` | author-facing helper API and composed behavior components | Example: `managed` assembles init/default/storage/tx/freeze-thaw pieces. |
| `ParameterModel` | typed parameter object and validation/lowering rules | Examples: init exposure, default source, tx name, callable runner. |
| `StoreSlotModel` | semantic store owner and physical slot name | Generated from value homes and sidecar state requirements. |
| `CallableRunnerModel` | callable source, accepted injected names, emitted runner | Factories/hooks/validators/freeze/thaw use this. |
| `OperationPlan` | ordered concrete contributions for one generated operation | Constructor, getter, setter, commit, rollback, etc. |
| `ContributionPlan` | one exact AST/source contribution | No contribution means no generated code. |

## 4. Relationship Rules

1. `TargetClassModel` contains `FieldModel` objects in declaration order.
2. A `FieldModel` has exactly one field name.
3. A transaction-aware `FieldModel` may belong to at most one transaction
   group.
4. Transaction-aware field behavior includes `managed`, `owned`, and
   `transient`.
5. `binding` is refcount/lifetime-aware but not transaction-aware.
6. `owned` is both transaction-aware and ownership/lifetime-aware.
7. `HelperModel` does not inherit behavior from another helper by default.
   Helpers assemble behavior components.
8. Behavior components can contribute to the same operation stage only through
   explicit order.
9. If a behavior component does not contribute to a stage, no code is emitted
   for that component at that stage.
10. Conflicting exclusive contributions must fail during model resolution, not
    during code emission.

## 5. Parameter Model Requirements

1. Every helper parameter must be represented by a semantic object.
2. Parameter objects must own:
   1. Validation.
   2. Type compatibility.
   3. Default/omitted handling.
   4. Callable signature validation where applicable.
   5. Lowering into constructor params, runner params, or generated constants.
3. `None` is a real value.
4. `UNSPECIFIED` means omitted by the user or omitted by generated constructor
   call site.
5. The database-reserved absent-value terminology must not be used for YIDL
   sentinels.
6. `default` and `default_factory` are both default sources.
7. `default_factory` differs from `default` because it executes user code at
   the field's initialization point.
8. `default` and `default_factory` are mutually exclusive for one default
   source.
9. `init` controls constructor participation only. It does not decide storage.
10. Callable parameters lower to named runner functions before lifecycle body
    snippets are emitted.

## 6. Initial Value Model

Initial value behavior is the product of:

1. `InitExposure`.
2. `DefaultSource`.
3. `StorageRequirement`.

`DefaultSource` concrete variants:

| Variant | Meaning |
|---|---|
| `NoDefaultSource` | No literal default or factory exists. |
| `LiteralDefaultSource` | A default value exists, including `None`. |
| `FactoryDefaultSource` | A default factory runner exists. |

`InitialValuePlan` concrete variants:

| Variant | Constructor payload | Construct body contribution |
|---|---|---|
| `InitDefaultValue` | `def astichi_params(*, field: T = default_value): pass` | `store.field = field` |
| `InitRequired` | `def astichi_params(*, field: T = UNSPECIFIED): pass` | error if `field is UNSPECIFIED`, then assign |
| `InitFactoryFallback` | `def astichi_params(*, field: T = UNSPECIFIED): pass` | assign supplied value, otherwise call factory runner |
| `HiddenDefaultValue` | no constructor payload | assign literal default |
| `HiddenFactoryDefault` | no constructor payload | call factory runner |
| `HiddenUninitializedAllowed` | no constructor payload | no assignment; slot remains `VOID` |
| `MissingInitialValueError` | no constructor payload | generation error or one direct construction error, depending on helper policy |

Rules:

1. A literal default on an exposed init parameter lives in the Python signature.
2. A factory default never lives in the Python signature.
3. A required exposed init parameter uses `UNSPECIFIED` in the Python signature.
4. The generated construction body is specialized to the resolved variant.
5. There is no general default-selection ladder in emitted code.
6. Initialization runs in declared field order.
7. Factory defaults run at their field's initialization point.
8. There is no dataclass-style `__post_init__` lifecycle concept.

## 7. Initvar Model

1. `initvar` is a constructor/input value, not a normal stored field.
2. `initvar(init=True)` participates in the constructor parameter surface.
3. `initvar(init=False)` must be resolved from its default source.
4. An initvar value can be consumed by callable runners by name.
5. Constructor-only initvars exist only during construction unless a later
   callable requires retention.
6. Retained initvar storage is generated only when required by a post-
   construction consumer such as a hook or validator.
7. Every initvar must be consumed by at least one callable runner, otherwise
   generation fails.

## 8. Constructor Surface Requirements

1. Constructor parameters are generated through Astichi parameter holes.
2. The constructor template owns a parameter target such as
   `_y_init_params__astichi_param_hole__`.
3. Each constructor-participating field contributes an `astichi_params`
   payload.
4. Payload bodies are empty; only signatures are inserted.
5. Field constructor parameters should be keyword-only unless a later design
   explicitly requires positional compatibility.
6. Duplicate final parameter names are errors.
7. Constructor parameter defaults and annotations are Astichi expression
   surfaces.
8. Requiredness is expressed by generated construction code, not by relying on
   Python missing-argument behavior.

## 9. Operation Surfaces

The model must be able to emit contributions for these surfaces:

| Surface | Examples |
|---|---|
| constructor signature | init params, initvars, transaction manager input |
| constructor body | slot init, default assignment, factory calls, initvar capture |
| facade get | current/default/working reads, derived cache resolution |
| facade set | write rejection, working promotion, thaw, assignment, mutation marking |
| tx begin | group begin depth, tx iteration id setup |
| tx validate | validators and commit-order inputs |
| tx commit | before hooks, field commit writes, freeze, ownership cleanup, after hooks |
| tx rollback | rollback-relevant field cleanup and after-rollback hooks |
| node lifetime release | binding/owned refcount close/release |
| class materialization | classvars, tx name maps, helper metadata |

## 10. Composition Requirements

1. Composition is assemble/combine, not inherit/override.
2. A helper is an assembly of behavior components.
3. A behavior component can declare:
   1. Required parameters.
   2. Provided semantic values.
   3. Store slots.
   4. Callable runners.
   5. Operation contributions.
   6. Invariants.
4. Behavior components may be abstract/non-instantiable.
5. A non-instantiable component can be reused by helpers but cannot produce an
   author-facing helper by itself.
6. Parameter conflicts are resolved before any AST is emitted.
7. Stage ordering is explicit and stable.

## 11. Minimum Testable Slices

1. Resolve `InitialValuePlan` truth table into concrete plan classes.
2. Emit Astichi parameter payloads for init fields.
3. Emit specialized constructor body snippets for each `InitialValuePlan`
   variant.
4. Verify no irrelevant branches are emitted.
5. Verify declaration-order factory execution.
6. Verify `None` as a literal default differs from `UNSPECIFIED`.
7. Verify initvar capture and factory injection by name.
8. Verify duplicate constructor parameter names fail before materialization.
9. Verify transaction-aware fields carry one tx group without changing field
   identity.
10. Verify binding is lifetime-aware but not transaction-aware.

## 12. Open Questions

1. For each helper, which plan owns `init=False` plus no default source:
   `HiddenUninitializedAllowed`, `MissingInitialValueError`, or helper-specific
   behavior?
2. Whether generated constructor parameters are permanently keyword-only.
3. Whether construction errors for missing values should be generation-time or
   runtime for each helper.
4. How MRO/override rules feed into `FieldModel` before plan resolution.
5. How retained initvars are discovered without over-retaining construction
   values.
6. How callable runner objects should represent injected facade refs without
   reintroducing generic runtime dispatch.
7. How much of the component assembly model should be visible in author-facing
   YIDL syntax.
