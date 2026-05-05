# YIDL P1 Design Summary

Canonical, self-contained design summary for YIDL P1 (first lifecycle-generation
phase). Every current decision, API-relevant rule, and locked directional choice
lives here in enumerated form. Drill-down documents expand — they do not
override — anything below. History under `dev-docs/history/` is source material
only; the history documents do not require it to be read. Implementation and
process rules live in `dev-docs/YidlCodingRules.md`.

## 1. Purpose And Scope

1. Generate lifecycle-style Python classes from YIDL specs.
2. Preserve the user-class facade feel while emitting optimized direct
   storage.
3. Use the lifecycle behavior currently represented by
   `pyrolyze/src/pyrolyze/lifecycle.py` as the behavioral reference for P1,
   but do not import `pyrolyze` from YIDL code or tests.
4. Keep the dependency direction one-way: future `pyrolyze` may import YIDL
   resources; YIDL must not import `pyrolyze` resources.
5. Generated lifecycle classes are plain Python classes, not dataclasses.
6. Use Astichi for AST stitching/lowering where composition beats string
   templating; keep a clean YIDL-vs-Astichi boundary (section 26).
7. Author-facing YIDL source stays at lifecycle-concept level. Flattened slot
   names must never appear in user source, examples, or `_yidl.py` containers.

## 2. Terminology

1. **Facade** (primary term). Application-facing generated surface. Aliases
   `proxy` and `veneer` mean the same thing and appear only as explanatory
   synonyms in legacy material.
2. **Main facade**. Public instantiated class. Inherits from the user-declared
   class. Only facade that holds strong references to other facades.
3. **Secondary facade**. Lazily allocated view class (at least `current` and
   `working`). Inherits from the user-declared class. Holds a strong
   reference to the internal state/store object; never to another facade
   directly.
4. **State/store object**. Single internal generated physical object, not a
   public API. It combines flattened lifecycle value slots, virtual-store
   namespaces, transaction manager reference, per-tx control state, weak
   facade cache, runtime scratch, cleanup aggregation, and private `_y_*()`
   helpers such as `_y_fetch_or_create_facade_current()`. The generated path
   does not allocate a separate runtime state object.
5. **Virtual store**. Logical store namespace (`PublishedStore`,
   `WorkingStore`, `InstanceStore`, `HiddenStore`, `DerivedCache`). These are
   semantic namespaces; the generator lowers them into slots on the
   state/store object. Reference docs may materialize them as separate Python
   objects for readability. `WorkingStore` is singular: each field has
   exactly one owning `tx_index`, but the store itself is not indexed by
   transaction.
6. **Physical store**. Actual state/store object whose slots carry one or more
   virtual stores plus private lifecycle control state. P1 documentation may
   use explicit reference layouts for readability, but the generator target is
   one mixed internal object per main facade instance.
7. **Transaction group**. Named subset of fields/hooks/validators that share
   begin/commit/rollback. Groups are independent by default; no implicit
   cross-group coupling.
8. **`tx_index`**. Stable integer id in `0..num_tx_groups-1` assigned to every
   transaction group at class generation time. Transaction-aware value fields
   may belong to at most one `tx_index`; non-transactional fields do not carry
   one.
9. **Sentinel types**. Each public sentinel has its own concrete type. There
   is no shared sentinel base class. Concrete sentinels are immutable
   singleton objects and slotted with no instance slots.
10. **`VOID`**. Public runtime sentinel object used by slotted stores to
    denote "not yet initialized". Normal generated access should resolve it
    before user code sees it, but it is not private.
11. **`UNSPECIFIED`**. Public decoration/spec-time sentinel for omitted field
    parameters. Distinct from `VOID`, which is runtime slot state. YIDL
    generated code and docs must not use the database-reserved absent-value
    terminology for this role.
12. **Transducer**. Unit of YIDL grammar that describes a field/helper kind's
    storage, read/write, commit, and rollback semantics. Field helpers
    (`managed`, `binding`, ...) are the author-facing realisations of
    transducers.
13. **Behavior snippet**. YIDL code fragment (usually fenced Python) that
    expresses part of a transducer, lowered contextually into the final
    emitted class during codegen.
14. **Generator-internal prefix**. `_y_*` is the reserved collision domain for
    all generated internals: slots, helper closures, scratch state, and
    private helper methods on stores, facades, and state anchors. No
    user-facing surface uses this prefix. P1 does not reserve additional
    generated-prefix namespaces unless a concrete implementation need appears.

## 3. Reference Model

1. The lifecycle helper surface in `pyrolyze/src/pyrolyze/lifecycle.py`
   defines the P1 behavioral reference. The 15 concrete helpers are
   enumerated in section 4.
2. YIDL must not import `pyrolyze` directly or indirectly. This includes
   product code, generated code, tests, validation probes, and parity
   backends.
3. If parity needs reference code, copy the required reference files
   (`lifecycle.py`, `freezable.py`, and their minimal support files) into a
   YIDL-controlled `test-deps/` tree or rewrite the behavior in YIDL-owned
   test helpers. Those copies are test dependencies, not runtime
   dependencies.
   1. `test-deps/` code is only importable by tests and validation helpers.
   2. `src/yidl/`, generated code, the public YIDL API, and YIDL runtime
      modules must not import `test-deps/`.
   3. `test-deps/` is excluded from pip-installed packages and runtime
      distributions.
4. Current reference code uses generic records, descriptor tables, and
   runtime dispatch. YIDL preserves observable behavior but generates
   explicit structures and unrolled code.
5. `docs/validation/study/lifeycle_examples.py::MultiTxMultiCounter` exercises
   the full 15-helper surface plus `managed_context` inheritance and is the
   broad parity target. It is not the first implementation slice.
6. The first implementation slice is a minimum helper set (section 28.2).
7. Known reference-side issues are documented but not patched during P1.
8. YIDL-owned runtime compatibility surfaces:
   1. Transaction orchestration names already exist in YIDL runtime code:
      `TransactionManager`, `GroupTransactionManager`, and
      `LifecycleTransaction`.
   2. Shared runtime protocols/data that already exist or are being retained
      in YIDL include `BindingBase`, `DEFAULT_TRANSACTION`, validator
      exceptions, and sparse-record semantics.
   3. Existing YIDL tests already use several of these names. Preserve the
      public names and observable semantics where practical so generated code,
      validation examples, and tests do not churn without a concrete design
      reason.
   4. Any missing piece is added as YIDL-owned runtime code or replaced by a
      generated equivalent; it is not imported from `pyrolyze`.
9. Remaining extraction direction:
   1. Shrink the context state machine into a thin runtime plus generated
      commit/rollback/get/set methods.
   2. Replace decoration-time machinery (`managed_context`, `LCKind`,
      descriptor tables, class-table builders) with the YIDL harvester and
      generator.
   3. Turn injection/compiler helpers into generator rules or small YIDL-owned
      runtime helpers.
10. Per-feature rule: any runtime behavior required by a slice must be
   YIDL-owned or explicitly deferred in that slice's design note. Generated
   code and tests must not depend on any `pyrolyze` interface, private or
   public.

## 4. Field Helpers As Transducer Artifacts

These helpers are YIDL compile artifacts, not hand-authored runtime helper
classes in the long-term design. A transducer defines behavior and emits the
field-helper functions/decorators that authors use. Compiling a YIDL file
produces a Python library that contains functions which generate the target
class; that generated library can expose helper factories with the names below
while keeping the behavior source in the transducer.

The 15 concrete helper surfaces YIDL must reproduce, each with semantic
one-liners:

1. `managed` — overlay-stored transactional value; current/working split.
2. `const` — per-instance immutable configuration; set at construction or by
   default/default_factory once.
3. `static` — per-instance write-once; either single assignment, or lazy
   materialization from default/default_factory on first read.
4. `binding` — identity-compared retained resource; refcount/retain-release
   cleanup on overwrite and node teardown. It is not transaction-aware.
5. `owned` — transaction-aware owned resource; current/working split plus
   release/dec_ref on discard.
6. `transient` — tx-scoped scratch; working value exists only while the
   group is open; optional `working_default_factory` materializes on first
   working access during an active transaction.
7. `local_store` — non-transactional instance-homed value; cleared on close.
8. `derived` — cached computed value; reset on commit, rollback, and close.
9. `initvar` — constructor-only declaration; optionally retained for post-init
   consumers; consumed by factories/hooks/validators by name. Every `initvar`
   must be consumed by at least one such callable or decoration fails.
10. `classvar` — class-level attribute materialized at decoration; no instance
    storage.
11. `commit_order_key` — sortable key controlling commit ordering within a tx
    group. At most one per tx group.
12. `commit_validator` — callable validating committability; raises or returns
    False to reject. At most one per tx group.
13. `on_before_commit` — hook fired before a tx group commits; multiple per
    group allowed.
14. `on_after_commit` — hook fired after a tx group commits; multiple per
    group allowed.
15. `on_after_rollback` — hook fired after a tx group rolls back; multiple per
    group allowed.

Plus the two primitive surfaces, also generated from or backed by transducer
metadata rather than treated as final hand-written lifecycle machinery:

16. `lifecycle_field` — low-level primitive every helper lowers to. Exposes
    every knob the helpers selectively expose or fix.
17. `managed_context` — class decorator that harvests fields, validates
    overrides, and produces the generated class.

## 5. Helper Parameter Rules

1. All helper calls are keyword-only. Positional args are invalid.
2. Per-helper parameter exposure is defined by the transducer and emitted into
   the generated helper factories. The existing `LCKind.helper_params` shape is
   a compatibility/reference input, not the final authority.
3. `compare` allowed values are `"value"` and `"identity"`.
   1. `managed` / `transient` / `local_store` / `derived` / `const` /
      `static` / `classvar` / `commit_order_key`: `compare` fixed to `"value"`.
   2. `binding` / `owned` / `commit_validator` / `on_*commit` /
      `on_after_rollback`: `compare` fixed to `"identity"`.
4. `init` exposure:
   1. `managed`: `init` fixed to `False` (construction goes through explicit
      kwargs, not dataclass-style positional).
   2. `initvar`: `init` exposed (`True` takes value from constructor kwargs;
      `False` requires `default`/`default_factory`).
   3. `classvar`: `init` scrubbed (not applicable).
   4. `commit_validator`, hook helpers: `init` fixed to `False`.
5. `tx_group` exposure:
   1. Exposed on `managed`, `owned`, `transient`,
      `commit_order_key`, `commit_validator`, `on_*`.
   2. Scrubbed on `initvar`, `classvar` (no tx semantics).
   3. Absent on `local_store`, `derived` (non-transactional).
6. Mutable-default rejection: `default=list()` / `dict()` / `set()` raises at
   decoration time. Mutables must use `default_factory`.
7. At-most-one rule: per tx group, at most one `commit_order_key` field and
   at most one `commit_validator` field. Hooks are unrestricted.
8. Override rules on inheritance (`managed_context` subclasses):
   1. `kind` must match (no changing helper kind in a subclass override).
   2. `compare`, `tx_group`, `initial_working`, `freeze`, `thaw`,
      `state_factory`, `state_copy` must match the base unless the derived
      value is the neutral/default.
   3. `init` must match when both base and derived specify it.
9. Initvar consumption requirement: every `initvar` must be consumed by at
   least one factory / hook / validator by parameter name. Unused initvars
   fail the decoration with `TypeError: unused lifecycle initvar
   declarations`.

## 6. Callable Injection Registry

Allowed parameter names per callable kind (in addition to declared initvar
names by name match):

| Callable kind | Allowed names |
|---|---|
| `default_factory`; transient `working_default_factory` | `self`, `current`, `working` |
| `on_before_commit` | `self`, `current`, `working`, `tx_group` |
| `on_after_commit` | `self`, `previous`, `current`, `tx_group` |
| `on_after_rollback` | `self`, `current`, `tx_group` |
| `commit_validator` | `self` |
| `commit_order_key` (`default_factory`) | `self`, `current`, `working` |

Rules:

1. Parameters must be named only; `*args` / `**kwargs` / positional-only
   parameters fail at decoration.
2. Unknown parameter names fail at decoration with
   `TypeError: unsupported parameter <name>`.
3. Parameter types are advisory; they do not constrain codegen wiring.
4. `self` refers to the facade instance appropriate to the call site.
5. `current` / `working` / `previous` are facade views onto the corresponding
   state snapshots.
6. `tx_group` is the literal group identifier passed through from the
   transaction manager.
7. Initvar names bind to their declared values: construction-phase values are
   always available; retained storage is materialized only if at least one
   post-init consumer names the initvar.

## 7. Value Homes By Field Type

| Helper | Value homes | Normalized homes | Notes |
|---|---:|---|---|
| `managed` | 2 | `PublishedStore.<field>`, `WorkingStore.<field>` | transactional current/working overlay; field carries at most one `tx_index` |
| `const` | 1 | `PublishedStore.<field>` | read-only after construction/default resolution |
| `static` | 1 | `PublishedStore.<field>` | single-write semantics |
| `binding` | 1 | `PublishedStore.<field>` | non-transactional retained resource; retain/accept/release on replacement and node teardown |
| `owned` | 2 | `PublishedStore.<field>`, `WorkingStore.<field>` | transaction-aware ownership storage plus node release/dec_ref policy; field carries at most one `tx_index` |
| `transient` | 2 | `PublishedStore.<field>`, `WorkingStore.<field>` | transactional working value exists only during active tx; field carries at most one `tx_index` |
| `local_store` | 1 | `InstanceStore.<field>` | native/proxy-owned, non-transactional |
| `derived` | 1 | `DerivedCache.<field>` | cached; reset on commit/rollback invalidation |
| `initvar` | 1-2 | `HiddenStore.construction.<name>`, optional `HiddenStore.retained.<name>` | retained only when a post-init consumer names it |
| `classvar` | 1 | class attribute | no instance state |
| `commit_order_key` | 1 | `PublishedStore.<field>` | per-instance value plus class metadata |
| `commit_validator` | 1 | `PublishedStore.<field>` | per-instance callable plus class metadata |
| `on_before_commit` | 0 | class runner metadata only | declaration-only |
| `on_after_commit` | 0 | class runner metadata only | declaration-only |
| `on_after_rollback` | 0 | class runner metadata only | declaration-only |

Additional per-field sidecars (exist only for fields that need them):

1. `CurrentFieldState.<field>` — runtime state built by `state_factory`.
2. `WorkingFieldState.<field>` — working-side copy built by `state_copy`;
   the field's `tx_index` controls transaction routing.
3. Class-backed helpers (`classvar`, hook declarations, validator/order-key
   metadata) do not allocate instance value slots unless the helper also has a
   per-instance value home in the table.
4. Instance-backed helpers (`static`, `const`, `managed`, `binding`, `owned`,
   `transient`, `local_store`, `derived`, `initvar`) resolve through facade /
   state routing even when their physical slots are flattened.

## 8. Generated Class Layout

1. Main facade:
   1. Public instantiated class.
   2. Inherits from the user-declared class.
   3. Holds a strong reference to the state/store object.
   4. Holds strong references to every currently materialized secondary facade.
2. Secondary facades (at least `current`, `working`):
   1. Lazily allocated on first attribute access.
   2. Inherit from the user-declared class.
   3. Hold a strong reference to the state/store object.
   4. Route field access according to facade semantics (read-only current;
      copy-on-read working; per-kind routing for others).
3. State/store object:
   1. Single internal physical object allocated with the main facade.
   2. Holds flattened lifecycle values and virtual-store namespaces.
   3. Holds transaction manager reference and per-tx control state.
   4. Owns the weak facade cache.
   5. Owns runtime scratch: factory-resolution sentinel stack, deferred
      commit-cleanup queue, rollback error aggregation list.
   6. Owns the `ever_committed` flag used by managed `initial_working`
      semantics.
   7. May define private generated helpers such as
      `_y_fetch_or_create_facade_current()`.
   8. Does not expose direct client behavior or public lifecycle APIs.
4. Constructor object budget:
   1. Generated construction allocates the main facade and one state/store
      object.
   2. User code may allocate whatever its own `__init__` requires.
   3. Secondary facades are created on demand, not during construction.
5. Generator-emitted internals use the reserved prefixes from section 2.14.
6. Per-class immutable metadata:
   1. `tx_index_to_group`: tuple indexed by `tx_index`.
   2. `tx_group_to_index`: frozen mapping.
   3. `commit_order_key_field_by_group`: 0-or-1 entry per group.
   4. `commit_validator_field_by_group`: 0-or-1 entry per group.
   5. `before_commit_runners[group]`, `after_commit_runners[group]`,
      `after_rollback_runners[group]`: unrolled call lists where possible;
      generic runner tables otherwise.

## 9. Facade Ref Topology

1. Every facade holds a strong ref to the state/store object.
2. The state/store object holds only weak refs to facades.
3. The main facade holds strong refs to every currently materialized
   secondary facade.
4. Secondary facades never hold strong refs to each other.
5. Facade access goes through a state/store-owned accessor: return live
   weakref target, or recreate the facade from the state/store object on miss.
6. On main-facade recreation, strong links to other still-live secondary
   facades are repopulated from the state weak cache.
7. Purpose: avoid strong cycles, allow prompt secondary reaping, keep lazy
   allocation correct, and make reconstruction deterministic.

## 10. Virtual Vs Physical Stores

1. Multiple virtual store namespaces may collapse into one physical slotted
   object via generated field names.
2. The hand-crafted reference may model separate virtual-store objects for
   `PublishedStore`, `WorkingStore`, `HiddenStore`, `DerivedCache`, and
   facade-native `InstanceStore` fields because that layout is readable and
   validates the object model. Generated P1 output does not allocate those as
   separate physical objects.
3. The P1 generator target is one mixed state/store object per generated
   instance, not one object per virtual store.
4. The P1 generator should use the virtual field mapper plus Astichi lowering
   so semantic virtual refs can lower into optimized flat physical names.
5. `docs/validation/perf/init_detection_mvp.py` remains a layout probe input,
   not a rule that blocks generator-side virtual-to-physical collapse.
6. Slotted classes use `__slots__` and direct attribute access in generated
   code; no `__dict__` fallback on stores.

## 11. Transaction Model

1. Transaction groups are independent. YIDL does not combine transaction
   state across groups.
2. Transaction-aware value fields may participate in at most one `tx_index`.
   P1 transactional value helpers are `managed`, `owned`, and `transient`.
3. Every lifecycle class has an implicit `DEFAULT_TRANSACTION` group. Non-
   default groups are declared explicitly and mapped to additional
   `tx_index` values.
4. Class metadata carries `tx_index_to_group` (tuple) and
   `tx_group_to_index` (frozen mapping).
5. Generated code for transaction-aware value fields carries the field's
   `tx_index` directly; the hot path does not consult class metadata.
6. Class tx metadata exists for external utilities, reflection, diagnostics,
   and non-generated helpers.
7. Per-tx state:
   1. Working participation flag (or equivalent derived rule).
   2. Working tx id (`working_tx_id[tx_index]`).
   3. Working value namespace (`WorkingStore` or flattened slots). The
      namespace is singular; individual field descriptors carry the
      `tx_index` used for transaction participation and stale checks.
8. Transaction manager responsibilities (modeled from the reference behavior,
   implemented in YIDL-owned runtime code):
   1. Active transaction per group.
   2. Dirty-context tracking.
   3. Validator-context tracking.
   4. Commit, rollback, drop, commit-only behavior.
   5. Enlistment API for contexts that acquire a working overlay.
9. `TransactionManager` construction requires an explicit `tx_groups`
   iterable for non-default groups; begin on unknown group raises.
10. Nested transaction begins are counted per group. Inner `commit()` /
    `commit_only()` decrements the begin count and returns without validating
    or applying writes; the outermost call performs the actual operation.
11. `commit()` validates first, then delegates to `commit_only()` for the
    actual apply path.
12. `commit_only()` applies commits without validation. It is a runtime escape
    surface and must not be used accidentally by generated normal commit code.
13. `drop(context, tx_id, tx_group)` removes a stale context from dirty and
    validator tracking for the active transaction. Generated code calls this
    when it discards an enlisted working overlay out of band.
14. Cross-group read visibility is explicitly open and must not be relied on
   until defined (section 27.2).
15. Runtime API compatibility rule: preserve existing YIDL runtime names and
    semantics for `TransactionManager`, `GroupTransactionManager`,
    `LifecycleTransaction`, and `DEFAULT_TRANSACTION` where practical.
    Generated code should target those YIDL-owned names unless a feature
    design explicitly replaces the surface.

## 12. Init-Detection (Locked)

1. Mechanism: `VOID` sentinel in slotted storage. Identity comparison
   (`value is VOID`) gates lazy default materialization.
2. Rationale (from `init_detection_mvp.py` + `InitStudyResults.md`):
   1. Warm-path differences are small in absolute terms for generated field
      access. `try/except` wins the synthetic warm path, but the spread is
      measured in tens of ns/field rather than architectural impact.
   2. `try/except` pays a large cold-path `AttributeError` cost and only
      amortizes after roughly 15-60 additional warm reads per instance in the
      measured shapes. Short-lived stores may never reach break-even.
   3. `VOID` is the simplest primitive to emit: one sentinel compare, no
      bitmask/generation bookkeeping, and no exception handler.
   4. `VOID` remains competitive enough on cold and warm paths, and the
      detection site is a localized code-generation template if real workload
      data later justifies a different mechanism.
3. Revisit triggers:
   1. Real init-payload cost is materially larger than the detection branch.
   2. Measured instance lifetimes are strongly long-lived (favoring
      `try/except`) or construct-and-read-once / allocation-dominated
      (favoring fresh-store swap).
   3. Hot-path miss rate is nonzero enough to invalidate `try/except` math.
   4. Bulk-clear operations become frequent and a mechanism with O(1) clear
      (bitmask / generation counter / fresh-store swap) wins measurably.
4. `VOID` and `UNSPECIFIED` live in the YIDL runtime constants library,
   exported from `yidl.runtime.constants`.
5. Sentinel implementation contract:
   1. Each concrete sentinel type owns its own singleton behavior directly.
      There is no shared sentinel base class.
   2. Sentinel instances are singletons per concrete type, so
      `UnspecifiedType() is UnspecifiedType()` is true.
   3. Sentinel instances are slotted with no instance attributes and are
      effectively frozen.
   4. Generated code checks sentinel state with `is` / `is not`.
   5. Because construction returns the singleton,
      `type(VOID)() is VOID` and therefore `type(VOID)() == VOID` under
      normal object equality.
   6. Reference implementation shape:

      ```python
      class VoidType:
          __slots__ = ()
          _instance = None

          def __new__(cls):
              if cls._instance is None:
                  cls._instance = super().__new__(cls)
              return cls._instance

      class UnspecifiedType:
          __slots__ = ()
          _instance = None

          def __new__(cls):
              if cls._instance is None:
                  cls._instance = super().__new__(cls)
              return cls._instance

      VOID = VoidType()
      UNSPECIFIED = UnspecifiedType()
      ```
6. Each `VOID`-backed slot must have a distinct default-resolution path that
   writes the real value before any consumer sees it.

## 13. 3-Phase Initialization Rule

Generated `__init__` runs exactly three phases, in order, without interleaving:

1. **State/store allocation.** Instantiate the one internal state/store
   object. Its slots include the collapsed `PublishedStore`, `WorkingStore`,
   `HiddenStore`, `DerivedCache`, per-field sidecars, tx control state, weak
   facade cache, and runtime scratch. All value slots hold `VOID` (or the
   appropriate sentinel for non-value slots).
2. **View wiring.** Cache the state/store reference on the main facade.
   Secondary facades are not eagerly allocated; the weak cache and strong-ref
   slots are prepared so lazy access is deterministic.
3. **Sequential field unroll.** Iterate declared fields in their harvested
   order. For each field:
   1. Resolve `default` / `default_factory` with the injectable registry.
   2. Write the resolved value into the correct virtual store.
   3. Materialize any `state_factory` sidecar.
   4. Consume and clear the constructor-phase initvar home for fields whose
      initvars are construction-only.

Rules:

1. Phase 3 may read already-initialized fields via `self.current.<name>` or
   by virtue of declaration order. It may not read uninitialized fields.
2. Factory cycle detection runs via a sentinel stack during phase 3; a
   factory entering itself raises immediately.
3. Phase-3 dependency ordering is declaration-order, not topological auto-
   sort. Factories that need dependency-inversion must declare an explicit
   order by placing the dependency earlier in the class body.
4. Retained initvar storage is materialized in phase 1 only if section 6
   detects a post-init consumer.
5. The factory-resolution stack lives on the state/store object for the
   duration of the call chain. It detects re-entry into an already-running
   `(kind, field)` factory and unwinds on `finally`.
6. P1 cycle detection covers `default_factory` and transient
   `working_default_factory`. If `state_factory` / `state_copy` become
   injectable or lazy, they must opt into the same stack deliberately.

## 14. Commit Pipeline Order

Commit needs one per-group pipeline. The copied/reference lifecycle behavior
validates before commit-order collection (`validate_commit()` before
`apply_commits()` / `commit_order()`). P1 defaults to that validate-first
shape unless an explicit YIDL divergence is agreed. The current proposed
generated ordering is:

1. Validate. Run the group's `commit_validator`, if any. If it returns False
   or raises, commit aborts and the group falls through to rollback.
2. Commit-order-key resolution. Evaluate the group's `commit_order_key` for
   every enlisted context. Sort participating fields/contexts by the key.
3. `on_before_commit` hooks, in declaration order within the group.
4. Store writes per field, in the order determined by step 2:
   1. Freeze (if configured).
   2. Write `WorkingStore.<field>` into `PublishedStore.<field>`.
   3. Reset `WorkingStore.<field>` to `VOID`.
   4. For `owned`: schedule the prior published value onto the deferred
      evict-last queue (section 18).
5. `on_after_commit` hooks, in declaration order within the group.
6. Evict-last drain: release prior values on the deferred queue
   after all structural writes have settled.
7. Reset per-tx control (`working_tx_id`, participation flag) for the group.

Open items:

1. Resolve exact ordering interaction when a hook inside a group mutates a
   field of a different group.
2. Define how order-key evaluation failures report: aggregate with validation
   failures or propagate directly.
3. Do not treat anything beyond validate-first as a locked pipeline until
   those items are resolved.

## 15. Binding / Owned Node Cleanup

1. Facades, state/store objects, and transactions do not have a public
   `close()` lifecycle API. A transaction commits or rolls back; a facade is
   only a call surface.
2. The close-like operation is the internal `BindingBase._close()` hook on a
   binding/owned node. A `BindingBase`-derived node performs cleanup through
   that hook when the node is no longer referenced.
3. The default CPython-oriented binding runtime relies on strong-reference
   lifetime: `BindingBase.__del__` marks the node closed and calls `_close()`.
4. The explicit-refcount variant releases nodes through `dec_ref()`; when the
   count reaches zero it marks the node closed and calls `_close()`.
5. Generated YIDL code must not expose or call a public facade/state `close()`.
   It only updates references, commits, rolls back, and releases binding/owned
   nodes according to the ownership policy.

## 16. Rollback Policy

Reference note: the copied/reference lifecycle behavior currently stops
rollback on the first per-field rollback error inside a context. The policy
below is an intentional YIDL-owned divergence from that reference behavior.

1. Rollback is best-effort over the fields mutated during the active
   transaction window for that group. A rollback-relevant field is a
   transaction-aware field whose working value, ownership state, or transient
   state was created or changed in that window.
2. Cleanup failures are collected into a per-group error list on the
   state/store object; they must not abort rollback traversal.
3. `on_after_rollback` hooks run after field-level rollback cleanup
   completes.
4. If any cleanup error is collected, the group's rollback raises an
   `ExceptionGroup` containing the collected exceptions, even when there is
   exactly one.
5. Rollback mechanics per field (managed / owned / transient):
   1. Discard `WorkingStore.<field>` (reset to `VOID`).
   2. For `owned`: attempt cleanup on the staged working value; on failure,
      append to the error list and continue.
6. `derived` caches and `transient` fields are reset on rollback.
7. `local_store` is unaffected by rollback (non-transactional).

## 17. Ever-Committed / Initial-Working Semantics

1. Each generated context/state tracks whether it has successfully committed at
   least once.
2. `managed(initial_working=...)` does not share a rule with
   `working_default_factory`; that parameter belongs to `transient`.
3. For managed fields with `initial_working`, while a transaction is active
   and the context has never committed, working/default overlay reads return
   `initial_working` until an explicit working value exists.
4. After the first successful commit, managed working reads resolve from the
   current/default value and normal thaw-on-write behavior.
5. Transient `working_default_factory`, when present, materializes the
   tx-scoped working value on first working access during an active
   transaction; otherwise the transient current/default value is used.

## 18. Evict-Last Sequence (Binding / Owned)

Required ordering for any binding or owned mutation that replaces an existing
resource. `binding` applies this immediately on replacement or node lifetime
release.
`owned` applies it through transactional working/commit/rollback paths.

1. **Stage.** Retain/accept/ref the new inbound value.
2. **Update structures.** Write the new value into the correct store slot. For
   `owned` commit, set `VOID` on the working overlay once the write is
   committed. The data tree is now consistent.
3. **Evict last.** Release/dec_ref the orphaned prior value. If that drops the
   final reference, the node's internal `_close()` runs.

Rules:

1. The basic stage → update → evict ordering is required.
2. The copied/reference lifecycle behavior drains deferred commit cleanup per
   context inside each context commit.
3. Global evict-last across an entire commit step is the current YIDL design
   direction for `owned`, not yet a ratified lock: when multiple fields share
   a resource graph, evictions may need one combined traversal rather than
   per-field release.
4. Rollback best-effort cleanup for `owned` (section 16) uses the same stage
   → release ordering, skipping the update step because the new value is not
   promoted.
5. The deferred evict queue lives on the state/store object and is drained by
   generated commit/rollback for transaction-aware ownership, never by user
   code.

## 19. Resource / Refcount Contract

1. Binding replacements retain/accept the new value, update the published
   slot, then release the old value; they do not join a transaction.
2. Provisional owned values replaced during the same transaction are
   released promptly on overwrite, before commit.
3. On commit, release of replaced committed values is deferred until after
   the new value is installed (section 18).
4. Discard of refcounted objects happens only after structures are in their
   final consistent order.
5. Any list of values to release lives in local generated state / the
   state/store scratch queue, never in durable user-visible structures.
6. If YIDL later supports transaction-group tying, YIDL needs a manager-
   level release signal so deferred release is not forced too early. This
   is open until tying is specified.

## 20. StateRef And Field Mapping

1. Field locations use semantic refs, not string-built slot names.
2. Concrete `StateRef` ABC subtypes:
   1. `PublishedValueRef`
   2. `WorkingValueRef`
   3. `CurrentFieldStateRef`
   4. `WorkingFieldStateRef`
   5. `WorkingPresentRef`
   6. `WorkingTxIdRef`
   7. `InitvarConstructionRef`
   8. `InitvarRetainedRef`
3. `StateRef` responsibilities:
   1. Identify semantic target.
   2. Expose field/tx coordinates when applicable (`field_name`, `tx_index`,
      optional `tx_name`).
   3. Lower to a concrete slot name via `StateNaming.slot_name(ref)`.
   4. Provide dynamic `get(state)` / `set(state, value)` / `exists(state)`
      accessors as a fallback.
4. `StateNaming` is a single object that owns all physical flattened naming.
   Templates do not hand-roll names.
5. Field descriptors carry `StateRef`s and may cache lowered slot names.
6. Virtual field mapper declares how virtual semantic surfaces map to
   flattened storage and drives Astichi lowering.
7. Generated hot paths use the lowered slot names directly. Dynamic
   accessors are reserved for external helpers, non-generated compatibility
   code, and transitional scaffolding.
8. `WorkingValueRef` and `WorkingFieldStateRef` use `tx_index` as the
   owning transaction-group coordinate for the field. It is not an index into
   multiple working stores.

## 21. Flattened Naming

Default physical-name templates. Prefixes may evolve but the table stays
centralized.

| Ref type | Flat slot template |
|---|---|
| `PublishedValueRef` | `_y_pv_{field}` |
| `WorkingValueRef` | `_y_wv_t{tx_index}_{field}` |
| `CurrentFieldStateRef` | `_y_cfs_{field}` |
| `WorkingFieldStateRef` | `_y_wfs_t{tx_index}_{field}` |
| `WorkingPresentRef` | `_y_wp_t{tx_index}` |
| `WorkingTxIdRef` | `_y_wtx_t{tx_index}` |
| `InitvarConstructionRef` | `_y_ivc_{field}` |
| `InitvarRetainedRef` | `_y_ivr_{field}` |

Rules:

1. Templates consume precomputed names or semantic refs; no hand-rolled
   f-strings at emission sites.
2. The naming table is deterministic and reproducible.
3. Physical naming is compiler-internal; never surfaced in user source or
   examples.
4. `tx_index` in slot names is the `0..N-1` stable integer, not the tx
   group name.
5. For transaction-aware field refs, `tx_index` names the field's transaction
   group; it does not imply multiple indexed working stores.

## 22. FieldSpec Runtime Properties

| Property | Callable? | Requires wrapper? | Notes |
|---|---|---|---|
| `annotation` | No | No | harvested type; used for override/narrowing checks; annotation-driven behavior is out of P1 |
| `default` | No | No | literal/static value |
| `default_factory` | Yes | Yes | injectable parameters per section 6 |
| `working_default_factory` | Yes | Yes | transient-only working-scope inputs |
| `initial_working` | No | No | initial working value where exposed by the helper |
| `freeze` / to-frozen | Yes | Usually | converts working value before publish |
| `thaw` / to-mutable | Yes | Usually | converts published value before working mutation |
| `state_factory` | Yes | Yes/direct | creates runtime sidecar state |
| `state_copy` | Yes | Yes/direct | copies current sidecar state into working sidecar |
| `compare` | No | No | `"value"` / `"identity"` per section 5.3 |
| `tx_group` | No | No | maps to field `tx_index` |
| `init` | No | No | constructor participation; per section 5.4 |
| hook defaults | Yes | Yes | commit hook runner or direct call |
| validator default | Yes | Yes | commit validation runner or direct call |

## 23. Callable Injection / Wrapper Model

1. YIDL owns one callable wrapper/lowerer component.
2. Inputs:
   1. Callable object / reference / source.
   2. Allowed injectable names for this callable kind (section 6).
   3. Field descriptor.
   4. Tx descriptor.
   5. Initvar refs.
3. Outputs:
   1. Generated wrapper function / source / AST.
   2. Call-site lowering (direct call when possible; runner-table when not).
   3. Signature validation errors raised at generation time.
4. Unsupported or ambiguous parameters fail at generation, not runtime.
5. Factory cycle detection uses a sentinel stack on the state/store object during
   phase 3 initialization.
6. Prefer generated direct call sites over generic runner maps whenever
   the generator has enough information.

## 24. Field Operation Matrix

Core operation columns every helper implements (or explicitly opts out of):

1. default / proxy get
2. current get
3. working get
4. working set
5. tx join / ensure working
6. default resolution
7. working-default resolution (transient-only)
8. commit
9. rollback
10. close
11. validator / order-key / hook participation
12. binding / ownership cleanup

Helper-family shape:

| Helper | Key operations |
|---|---|
| `managed` | resolve default, read current/working, ensure working on set, thaw on working promotion, freeze on commit, rollback discards working |
| `const` | resolve once, read current, reject mutation |
| `static` | resolve once, enforce single-write |
| `binding` | non-transactional retained resource; retain/accept/release and evict-last on replacement or node lifetime release |
| `owned` | transaction-aware ownership semantics plus release/dec_ref ownership policy |
| `transient` | tx-scoped working/default behavior, rollback/commit cleanup |
| `local_store` | direct instance/native get/set |
| `derived` | cached compute, reset on commit/rollback invalidation |
| `initvar` | constructor capture, optional retained storage, injectable into factories/hooks |
| `classvar` | class materialization, no instance store |
| `commit_order_key` | current value read during commit ordering |
| `commit_validator` | callable invoked during validation |
| `on_before_commit` | hook call before field commits |
| `on_after_commit` | hook call after successful commit |
| `on_after_rollback` | hook call after rollback |

## 25. Combinatorial Field Interactions

These interactions define correctness; the generator must not emit N
independent snippets without respecting the pipeline they imply.

1. **`derived` reads `managed` / `transient` / `local_store`** — dependencies
   must be initialized earlier in declaration order. No topological auto-
   sort; authors order explicitly.
2. **`binding` + `owned` overlap** — both need stage → update → evict.
   `binding` applies that sequence immediately because it is not
   transaction-aware. `owned` applies it through the transaction pipeline.
   Global per-commit-step traversal is an `owned` design direction and must
   be ratified before being treated as a hard rule.
3. **`commit_order_key` + `commit_validator` + `on_*commit`** — single
   commit pipeline per group. Exact order is proposed in section 14 and
   still needs ratification.
4. **Multi-group `tx_group`** — cross-group reads while another group has
   an active tx have no defined visibility yet (section 27.2). Generator
   must not emit code that assumes a barrier.
5. **`local_store` + `derived` peer read** — routing must compose: both
   resolve via the main facade instance without view interception.
6. **`initvar` + `default_factory` referencing it** — phase 3 materialization
   order must resolve the referenced initvar before the consuming factory
   runs. Retained storage is allocated in phase 1 when the factory is
   detected as a consumer.
7. **`managed.initial_working`** — visible only for managed fields before the
   first successful commit while a transaction is active and no explicit
   working value exists (section 17).
8. **`transient.working_default_factory`** — visible only for transient
   fields; it materializes the tx-scoped working value during an active
   transaction (section 17).
9. **Field spec MRO merge** — subclass overrides must honor section 5.8;
   incompatible overrides raise at decoration.
10. **Annotation-driven compare** is out of scope for P1; compare is
   declared explicitly via helper kwargs.

## 26. Astichi Boundary

1. Astichi owns:
   1. AST fragment composition mechanics.
   2. Splice/stitch APIs and hygiene.
   3. Free-load resolution, single-evaluation lowering, dead-path elision.
   4. Python `ast` compatibility shims across versions.
2. Astichi does not know lifecycle semantics by name. It never knows what
   `managed` means, what `PublishedStore` is, or what a tx group is.
3. YIDL owns:
   1. Semantic meaning of field kinds, stores, views, phases.
   2. Which fragments are supplied for each helper.
   3. Precedence, ordering, and the pipeline (section 14).
   4. Harvested spec and final class/factory structure.
4. YIDL provides Astichi with:
   1. Fragments (Composables) declared as Python snippets.
   2. Wiring: which fragment fills which hole, with what `add_kwargs`.
   3. Literal values / paths for `astichi_ref`.
5. Astichi returns:
   1. Stitched AST, emitted Python source, or both (with optional
      `provenance` for diagnostics).
6. Astichi marker cheat-sheet (current surface):
   1. `astichi_hole(<name>)` — parent-body insertion point; filled by a
      named contribution.
   2. `@astichi_insert(<target>, order=..., ref=...)` — authored block-shell
      insertion marker for block contributions.
   3. `astichi_funcargs(...)` — authored call-argument payload surface for
      positional / keyword / variadic argument stitching.
   4. `astichi_ref(<path>)` / `astichi_ref(external=<name>)` —
      expression-only path lowered to a `Name`/`Attribute` chain. Accepts
      string or f-string literal with compile-time formatted parts only, or
      an external bind site for the path value.
   5. `astichi_ref(<path>).astichi_v = …` (or `._`) — sentinel wrapper
      accepted in Store / AugStore / Delete target positions.
   6. `astichi_for(<iterable>)` — compile-time unroll loop; supports
      tuple-target decomposition so `for (a, b, c) in astichi_for([...])`
      binds each element to its own loop variable as a literal.
   7. `astichi_import(<name>)` — declaration-form boundary marker that
      imports a parent-scope binding into the current Astichi scope.
   8. `astichi_pass(<name>)` — value-only cross-scope reference form. It
      aliases a scoped binding into an expression or assignment; bare
      statement-form `astichi_pass(...)` is invalid.
   9. `astichi_export(<name>)` — boundary declaration that publishes a local
      binding for builder assignment / wiring.
   10. `astichi_keep(<name>)` — prevents the hygiene pass from renaming a
      given identifier; used when a contribution must resolve to a specific
      outer binding.
   11. `identifier__astichi_keep__` — suffix-form identifier keep. It pins
      the stripped identifier name through hygiene without leaving the suffix
      in materialized output.
   12. `identifier__astichi_arg__` — suffix-form identifier demand. It is
      resolved through `arg_names`, `bind_identifier`, or builder assignment;
      unresolved slots fail materialization.
   13. `astichi_bind_external(<name>)` — names the wiring point for an
      external argument payload supplied at composition time.
   14. `astichi_bind_once` / `astichi_bind_shared` are recognized marker names
      but not P1 YIDL dependencies unless their lowering semantics are
      explicitly revalidated.
   15. Historical shorthand for `astichi_import(<name>)` as simply surfacing
      a free `Load` is incomplete; import is a declaration surface, while
      pass is the value surface.
7. YIDL uses Astichi for: per-field getter/setter, managed setter
   composition, freeze/thaw insertion, binding refcount bodies, owned
   evict-last bodies, commit/rollback body synthesis, 3-phase init field
   unroll.
8. Generator architecture rule: YIDL features should declare reusable Astichi
   composable resources plus construct surfaces, spec properties,
   filters/selectors, and rules. The compiler connects those ports by
   evaluating rules over resolved specs. New features should not add bespoke
   per-feature emitter loops once their construct shape is understood. For
   common class/function constructs, prefer canonical Astichi component recipes
   and standardized hole names over parallel YIDL-only interface metadata.
9. Astichi improvement rule: YIDL should prefer fixing or extending Astichi
   over working around Astichi gaps in the generator. If YIDL needs a missing
   Python construct surface, add that surface to Astichi rather than hiding the
   gap behind feature-specific source formatting or AST surgery. Temporary
   workarounds must be documented and kept out of the long-term generator path.
10. Data-driven builder rule: fluent Astichi builder paths are useful
    human-facing notation, but YIDL's mapper must call Astichi through explicit
    named/data-driven builder APIs. The mapper must not synthesize Python
    attribute chains to reach `builder.add.<Name>`, `builder.Root.slot`, or
    similar fluent-only surfaces.

### 26.1 Data Definition, Container, And Matcher System

This is the current implemented generation-data substrate. It is a schema and
resolved-data layer, not the whole capsule/codegen engine.

1. `DataDefinitionSystem` is schema-only. It defines properties, record
   shapes, unions, concrete collections, computed collections, transforms, and
   matchers. It does not store decoration-time data.
2. `PropertySpec` objects own semantic name, Python value type, default, and
   generated storage name. Property names are semantic; generated record
   constructor keywords are storage names.
3. `RecordSpec` emits plain slotted Python record classes with
   `__dds_record_spec__`. Generated YIDL record classes are not dataclasses.
   Record constructors validate declared types and defaults.
4. `UnionSpec` groups concrete record variants into one logical collection
   shape. A union collection accepts variant records, but records are created
   through concrete variants.
5. `CollectionSpec` defines a concrete stored collection. Cardinality is an
   object behavior (`single` or `many`), not an enum. Collections may declare
   one identity property or a tuple of identity properties. Ordinary insertion
   uses strict duplicate rejection; explicit `builder.write(..., policy=...)`
   supports add-if-absent and replacement where the collection has an
   identity.
6. `ComputedCollectionSpec` is a named filtered view over another collection or
   computed collection. It returns existing source records and is not stored as
   its own record set.
7. `PortSpec` / `PortAddress` define semantic build destinations. A DDS can
   configure one port index from ordinary target/order properties. Port
   cardinality constrains children at one port address, not the size of the
   backing collection.
8. `DDSContainerBuilder` is the mutable decoration-time holder. It accepts
   records for concrete collections, enforces cardinality, identity, and
   port-index constraints, supports explicit write policies, and freezes to
   a `DDSContainer`. Ordered source reads use `ordered_records(...)`, sorting
   by declared properties and then collection write order.
9. `DDSContainer` is the immutable resolved-data object. It exposes named
   collection views with `sequence()`, `one()`, `by_identity(...)`, and
   `contains(...)`, plus `children_at(port_address)` for ordered port
   children. Querying a view must not mutate or lazily derive data.
10. Runtime container source emission produces normal Python modules containing
   runtime property/record/union/collection descriptors, generated record
   classes, computed views, ports, matchers, generated production operations,
   `run_operations(...)`, `build_container(...)`, and `new_builder()`. It must
   not rebuild a source-time `DataDefinitionSystem` with `dds.property(...)`
   calls.
11. `TransformSpec` remains a compatibility/in-memory helper. The emitted
    production runner is `ProductionSpec` / `ProductionGroupSpec`; it reads
    collection, computed-collection, or matcher-result sources, builds target
    records through source-emittable value expressions, supports keyed
    `lookup(...)` reads against collection identities, supports ordered
    production sources through `collection.ordered(...)`, and writes with
    explicit policy.
12. `OperationSpec` defines aggregate generated operations over declared
    collection inputs and outputs. Generated operation functions receive a
    `DDSOperationContext`, which exposes ordered `records(...)`, `write(...)`,
    `by_identity(...)`, `children_at(...)`, and `write_order(...)`. Production
    groups are execution groups and may contain ordinary productions and
    aggregate operations.
13. External Python-object fact extraction is operation-backed, not DDS-core
    behavior. `LifecycleCallableFactsConcept` records callable declarations and
    lowers signature analysis through an ordinary generated operation that calls
    `yidl.generation.lifecycle_facts.analyze_callable(...)` and writes normal
    DDS records.
14. Resource-field cleanup and lifecycle hooks are lifecycle concept records and
    generated method-body contributions. `LifecycleResourceHooksConcept` extends
    the current staircase with owned/binding variants, hook/validator/order-key
    declarations, callable-fact production, hook method statements, and close
    cleanup statements without adding hook or resource policy behavior to DDS
    core.
15. Initvar dependency closure is lifecycle-specific generated operation code,
    not a DDS graph API. `LifecycleInitvarClosureConcept` extends the current
    resource-hook concept with an `InitVarField` variant, generated edge
    production from callable injection facts, retained/constructor-only
    classification, and unused/unknown initvar rejection. No public
    `reachable_collection(...)` helper exists yet.
16. `MatcherSpec` defines Eq-only rule matchers over concrete/computed
    collection views. Match tuples are fixed positional tuples, not dicts.
    Rules run in descending score order; equal-score overlapping rules reject
    before runtime.
17. Matcher evaluated fields are explicit callable-derived tuple entries.
    In-memory runtime may use any callable; source emission requires an
    explicit generated/importable evaluator name.
18. `MatcherResult` contains the selected generated value, rule name or
    `None`, score, concrete input records, and extracted tuple values.
19. Matcher/generated resources are produced through factory functions.
    `from_literal(...)` stores source-renderable Python literals,
    `from_astichi_code(...)` and `from_astichi_template(...)` store Astichi
    compile inputs, and `from_import(...)` references imported symbols for
    consumers outside Astichi templates. The backing generated value compiles
    lazily and caches the resulting `astichi.Composable` when a composable is
    requested.
20. Matcher-result productions use `matcher.results()` as a production source
    and `match.resource()`, `match.record("input").prop(Property)`, and
    `match.value(index)` as value expressions. Generated operation code reads
    matcher results through a stable builder snapshot.
21. The remaining DDS production work is builder-phase matcher views, only if
    snapshot semantics prove insufficient, and fragment/capsule merge, only if
    real reuse pressure requires it. That design lives in
    `dev-docs/YidlDataProductionDesign.md`.
22. Definition composition is currently handled with direct DDS extension:
    contributors call `ensure_*` helpers to share semantic definitions and are
    sequenced with `DataDefinitionSystem.extend(...)`. This covers the first
    capsule-composition pressure case without adding a parallel fragment graph.
    A separate fragment object remains deferred until direct extension becomes
    awkward.

## 27. Grammar And Source Containers

### 27.1 Grammar boundary

1. YIDL grammar expresses lifecycle semantics.
2. YIDL grammar never exposes flattened slot names or `_y_*` identifiers.
3. Field helper syntax maps to transducer artifacts that produce field
   descriptors / FieldSpec objects and helper factories.
4. Callable syntax maps to callable-wrapper / lowerer inputs.
5. Transaction group syntax maps to immutable class tx metadata.
6. Grammar follows the class/layout/operation matrices in this summary.
   Do not invent behavior that is not already motivated by the layout
   model.
7. A compiled YIDL file is a generated Python library: it contains the
   functions/decorators that generate the target class, rather than directly
   being the final target class source.

### 27.2 Known grammar coverage gaps

1. Virtual value homes required by a transducer — not yet fully expressible.
2. Field-local scratch / previous-commit retention policy.
3. Destruction / cleanup policy declaration.
4. Rollback error aggregation behavior.
5. Optimized per-kind surface placement decisions.
6. Container-shape-specific resource transducer selection (single vs list vs
   map) for `binding` and `owned`, while preserving their transaction split.
7. Cross-group visibility rules.
8. Annotation-driven compare behavior (if any).

### 27.3 Parsers

1. The older embedded `_yidl.py` development surface used an
   indentation-aware recursive-descent parser with `%% … %%` raw Python
   fences.
2. The standalone `.yidl` concept/DDS definition surface uses a Lark parser.
   It is brace-blocked, uses Python-compatible single/double/triple-quoted
   strings for resources, and lowers parsed modules into recorded
   concept/DDS builder calls.
3. Lark is definition-stage only. Generated decorators, generated field-spec
   functions, and decorator-time runtime paths must not invoke a parser.
4. Parser output is a strictly typed module AST suitable for symbol resolution
   and downstream contextual lowering.

### 27.4 `_yidl.py` bootstrap container (development-only)

1. Canonical wrapper form:
   ```python
   import yidl
   yidl.embed("""
       ... YIDL source ...
   """, yidl.global_args, globals())
   ```
2. File naming: development containers use the `_yidl.py` suffix.
3. `yidl.embed(source, args, module_globals)` contract:
   1. `source` is the authoritative YIDL source string.
   2. `args` is the dev/test args object; currently `yidl.global_args`.
   3. `module_globals` is the caller's `globals()`; the generator
      populates it in place.
   4. Returns `None`.
   5. Repeated imports of the same module are idempotent under normal
      Python import semantics; no import-order tricks required.
   6. Compilation failure raises a compiler exception with best available
      line/message.
4. `.py`-container source-preservation behavior (when detected):
   1. `yidl.global_args.pass_source_only = True`.
   2. The generator sets module attributes:
      1. `YIDL = "<original source string>"`
      2. `YIDL_PY_LINE = <1-based line number of the first YIDL source
         line inside the Python file>`.
5. Bootstrap path is slow and unsupported. Each `_yidl.py` container
   carries a prominent warning comment. This container is never the
   long-term delivery shape.
6. Bootstrap is an enabling deliverable, not a gate for empirical validation.
   PRE_IMPL probes may proceed before bootstrap exists unless they specifically
   need source-in-Python containers.
7. Accepted bootstrap risks: `globals()` as exec namespace, mutable
   `yidl.global_args`, import-time compile/exec cost, non-final wrapper
   format.

## 28. Testing Strategy

### 28.1 Test layers

1. Keep reference-behavior parity tests for observable lifecycle behavior.
   They must run against YIDL-owned or vendored `test-deps/` reference code,
   not imports from `pyrolyze`.
2. Virtual-field-mapper tests:
   1. Virtual ref declaration.
   2. Flat-name lowering.
   3. Invalid ref rejection.
3. Astichi lowering tests:
   1. Virtual source runs before lowering.
   2. Lowered source uses direct flat names.
   3. Semantics match between virtual and lowered forms.
4. Callable wrapper tests:
   1. Accepted signatures (per section 6).
   2. Rejected signatures (unknown names, `*args`, `**kwargs`,
      positional-only).
   3. Initvar injection (by name).
   4. Per-hook param availability.
5. Generated skeleton tests:
   1. Facade construction (main + lazy secondary).
   2. Weakref reconstruction after secondary is GC'd.
   3. Tx metadata correctness.
   4. `VOID` sentinel default detection.
6. Performance probes for layout choices under `docs/validation/perf/`
   (not parity tests).
7. Do not patch or import `pyrolyze/` during P1; document reference-side bugs
   separately.
8. Baseline parity tests run under `LC_PARITY_IMPL`:
   1. `lifecycle` — YIDL-owned reference backend, using copied test deps or
      rewritten reference helpers.
   2. `handcrafted` — YIDL-owned comprehensive hand-crafted/generated-shape
      baseline.
   3. `generated` — compiler output for the currently supported subset.
9. Every parity test in `tests/baseline/` must pass for all three backends
   unless a documented lifecycle-only reference bug is skipped through a
   shared helper.
10. Maintain two hand-crafted tracks while the generator grows:
   1. Comprehensive baseline: `src/yidl/handcrafted/lifecycle_sample.py`.
   2. Focused slice shape: `src/yidl/handcrafted/slices/<feature_slug>.py`.
11. The generator must keep emitting runnable output for the supported subset
    on every feature slice. Unsupported features fail explicitly and locally.
12. `tests/baseline/_impl_switch.py` owns backend selection. Its
    `lifecycle` backend must load only YIDL-owned code or `test-deps/`
    copies; it must not import any `pyrolyze` package module.
    1. The `lifecycle` backend is test-only.
    2. Public YIDL API/runtime modules must not import it.
    3. Packaging must exclude copied lifecycle/freezable reference files.
13. Python-version validation uses `uv run --python <version> ...` and covers
    the active support sweep from 3.12 through the forward-looking 3.15 line
    where available.
14. PRE_IMPL is empirical scaffolding, not product surface. Its current
    decision outputs are folded into this summary; historical matrices remain
    background unless a new design question reopens them.
15. Classify significant failures before coding around them:
    1. `implementation_bug` — design is coherent; implementation missed it.
    2. `design_gap` — behavior is under-specified.
    3. `design_conflict` — current design conflicts with required behavior or
       emitted shape.
16. Do not mark a feature complete while an unresolved `design_gap` or
    `design_conflict` affects that feature.

### 28.2 Field staircase (test order)

Each step must pass before the next begins:

1. `managed` default-tx (single field, commit / rollback).
2. `managed` advanced (`freeze`/`thaw`, `initial_working`).
3. `const` / `static`.
4. `local_store` / `derived`.
5. Multi-group tx (two groups, independent commit/rollback).
6. `transient` (including `working_default_factory`).
7. `binding` refcount cleanup and `owned` evict-last + rollback cleanup.
8. `initvar` injection (init=True and init=False, factory consumption,
   hook/validator consumption).
9. `commit_order_key`, `commit_validator`, `on_*` hooks.

### 28.3 Minimum Reference Helper Set

The first `optimal_reference.py` covers exactly these five fields, which
between them force every non-trivial layout decision:

1. `managed_scalar` — plain managed int.
2. `managed_with_thaw` — `freeze` / `thaw` callables.
3. `managed_depends_on_other` — `default_factory(self)` referencing an
   earlier-initialized field.
4. `binding_scalar` — `BindingBase`-derived resource.
5. `local_store_scalar` — native-homed on the main facade.

Deferred for the reference: validators, hooks, initvars, classvars,
multi-group tx, virtual-to-physical store collapse.

## 29. Package Structure

1. `src/yidl/`: compiler, parser/frontend, generator, YIDL-owned runtime,
   public API, test support.
   1. `src/yidl/runtime/constants.py`: public sentinel constants
      `VOID` and `UNSPECIFIED`, plus their singleton sentinel types.
2. `test-deps/`: copied reference-only dependencies used by parity tests when
   direct import would otherwise cross into `pyrolyze`. These files are not
   product runtime dependencies, are never imported by `src/yidl/`, and are
   excluded from pip packages.
3. `example/`: concise working-documentation examples. Multi-file only when
   the technique genuinely requires it.
4. `docs/validation/`: empirical probes, generated-example validation,
   representability experiments, performance checks, Python-version
   investigations. Not shipped product.
5. `docs/`: normative split design documents (`YIDLFrontendDesign.md`,
   `YIDLCodegenDesign.md`, `YIDLRuntimeClassModel.md`). `YIDLDesign.md` is a
   header/split pointer, not the current normative source by itself.
6. `dev-docs/p1-design/`: active design pack (this summary + drill-downs).
7. `dev-docs/history/`: archived exploratory material; read-only, never
   cited as current.
8. Large application integrations do not live in the core repo; they move
   to sibling repos.
9. Validation artifacts never silently promote into `src/` or the parity
   test tree.

## 30. API Design Rules

1. Helpers and public APIs use keyword-only parameters when the shape is
   known. Avoid `*args` / `**kwargs` in public signatures.
2. Public types carry full annotations; avoid `Any` where a precise type
   exists.
3. One concept lives in one place; avoid duplicating the same semantic
   across multiple public entry points.
4. Prefer explicit compile-time / generation-time boundaries over ambient
   runtime reflection.
5. Keep distinct: authoring surface, registration/manifest/spec metadata,
   runtime-only helpers.
6. Source / spec flow is explicit: source files, embedded containers,
   helper calls, or generated spec objects. No implicit discovery.
7. No compiler internals, `_y_*` names, or lowered slot names appear in
   hand-written YIDL source, examples, or `_yidl.py` containers.
8. No enums without explicit project-owner approval. Do not replace enums with
   magic strings, integers, or other passive tags when the concept has
   semantics. Semantic concepts must be represented by objects or classes that
   can own validation, lowering, behavior, and documentation.

## 31. Optimizations

1. Use flat slotted storage in generated hot paths.
2. Direct generated reads/writes; avoid generic record dicts.
3. `VOID` sentinel for unset detection in slotted storage (section 12).
4. Allocate secondary facades lazily.
5. Weakref facade cache on the state/store object.
6. Unrolled commit / rollback / resource cleanup logic per field where
   practical.
7. Thin accessors over tx state for external helpers.
8. `StateRef` dynamic accessors are fallback only, not hot path.
9. Avoid generic field-table dispatch when direct generated code is
   available.

## 32. P1 Build Order

Minimum P1 delivery surface:

1. A generated plain Python lifecycle class skeleton with main/current/working
   facades, one internal state/store object, tx metadata, `VOID` slot init,
   and lazy facade access.
2. A working virtual field mapper that lowers semantic state refs into flat
   physical names through Astichi.
3. A callable wrapper/lowerer that validates the section 6 injection registry
   and emits direct calls where possible.
4. Runtime-owned default transaction begin/commit/rollback path for the first
   managed slice.
5. Three-way parity for the supported subset under `LC_PARITY_IMPL`.

Implementation order:

1. Virtual field mapper.
2. Astichi lowering from virtual refs to flat physical names.
3. Callable injection / wrapper lowerer.
4. Minimal generated class skeleton: main facade, one internal state/store
   object, lazy current/working secondaries, `VOID` sentinel storage, tx
   metadata.
5. One generated lifecycle slice over the skeleton (start with
   `managed_scalar`).
6. Advance the comprehensive handcrafted baseline and focused slice shape in
   parallel with generator work. They are reviewable target shapes, not a
   substitute for generation.
7. Expand operation matrix one helper family at a time, following the
   staircase in section 28.2.
8. Fit grammar to the semantic matrices after layout, refs, callables,
   and operations are stable.
9. Consolidate drill-down documents as each subsystem lands; retire
   historical notes in `dev-docs/history/` as they are superseded.

## 33. Open Design Holes

1. Single vs list vs map resource transducer shapes for `binding` and
   `owned`. They share retain/release mechanics but differ on transaction
   participation, so the split must stay explicit.
2. Cross-group transaction visibility and barrier rules.
3. Lazy-facade retention topology under refcounted-facade mode (if that
   mode is ever enabled).
4. Grammar coverage items in section 27.2.
5. Transaction-group tying / coordinated commits (and the release signal
   this would require per section 19.5).
6. Final migration path off the `_yidl.py` bootstrap container.

## 34. Decision Ledger

1. The lifecycle behavior represented by the copied/reference lifecycle files
   is the P1 behavioral reference.
2. YIDL owns its generated runtime/lifecycle semantics long-term.
3. Generated lifecycle classes are plain Python classes, not dataclasses.
4. User-facing YIDL syntax expresses lifecycle semantics, not flattened
   storage.
5. Main / current / working facades inherit from the user class.
6. The generated path uses one internal state/store object as both physical
   storage and runtime state anchor.
7. The state/store object may define private `_y_*()` helpers, but exposes no
   public client behavior or orchestration policy.
8. Facade topology is main-facade star + state weak cache.
9. Facades hold strong refs to the state/store object.
10. The state/store object holds weak refs to facades.
11. Main facade is the only facade with strong refs to other facades.
12. Transaction groups are independent by default.
13. Transaction-aware value fields may belong to at most one `tx_index`;
    non-transactional fields carry no tx coordinate.
14. Class tx metadata includes immutable `tx_name <-> tx_index` mappings.
15. Generated code for transaction-aware value fields carries the field's
    `tx_index` directly.
16. Field mapping is a compiler layer, not a naming helper.
17. Do not use enums for semantic concepts. Use concrete objects/classes such
    as `StateRef` ABC subtypes, event marker objects, transducer objects, and
    callable-lowering objects. Any enum-like representation requires explicit
    project-owner approval.
18. Centralize physical slot naming in `StateNaming`.
19. Field descriptors carry semantic refs and may cache physical names.
20. Astichi lowers virtual refs into collapsed physical names.
21. Thin dynamic accessors remain for external / helper compatibility.
22. **Init detection is the `VOID` sentinel, locked.** Alternatives
    (bitmask, generation counter, try/except, fresh-store swap) are
    rejected for P1; revisit only under the conditions in section 12.3.
23. **3-phase init is mandatory**: allocate → wire → sequential unroll
    in declaration order.
24. Commit pipeline is one per transaction group. P1 defaults to the
    reference's validate-first shape; remaining hook/write/cleanup ordering is
    proposed, not fully ratified.
25. Nested transactions are counted per group. Inner commits decrement only;
    outermost commit validates/applies.
26. `commit_only()` applies without validation and is not the normal generated
    commit path.
27. `drop()` removes stale contexts from dirty/validator tracking when a
    working overlay is discarded out of band.
28. No public facade/state `close()` exists. Binding/owned node cleanup is
    reached through reference release or explicit `dec_ref()`, which may call
    the internal `BindingBase._close()` hook.
29. Managed `initial_working` and transient `working_default_factory` are
    separate helper surfaces and cannot be treated as one precedence chain.
30. Factory cycle detection is state/store-owned and covers
    `default_factory` plus transient `working_default_factory` in P1.
31. **Rollback is best-effort** across every field mutated during the active
    transaction window and raises `ExceptionGroup` when any cleanup fails,
    even for a single error. This is an intentional YIDL divergence from the
    current reference rollback path.
32. Evict-last stage → update → evict ordering is required. Global
    per-commit-step traversal is a design direction that still needs
    ratification; the current reference drains cleanup per context.
33. Prefer unrolled generated commit/rollback/resource cleanup over generic
    runner tables.
34. Keep callable injection/wrapper lowering as its own component.
35. Grammar mapping comes after layout, refs, callables, and operation
    matrices.
36. Astichi owns AST mechanics only; YIDL owns all lifecycle semantics.
37. `_yidl.py` bootstrap container is development-only; slow and
    unsupported; deliberately temporary.
38. `_yidl.py` bootstrap is not a PRE_IMPL gate; it lands when probes need
    source-in-Python containers.
39. `_y_*` is the reserved identifier prefix for generator-emitted internals;
    never surfaced in user source.
40. Mutable-instance defaults (`list`/`dict`/`set`) are rejected at
    decoration; mutables require `default_factory`.
41. `commit_order_key` and `commit_validator` are at-most-one per tx
    group.
42. Every `initvar` must be consumed by a factory / hook / validator by
    parameter name; unused initvars fail decoration.
43. P1 starts with strict internal subsystems. Field mapping and callable
    lowering are intentionally separable, and extraction into a subproject
    remains an explicit option if the seam proves valuable.
44. Runtime behavior needed by a feature slice must be YIDL-owned or
    explicitly deferred; generated code and tests must not import or depend
    on any `pyrolyze` interface.
45. Parity is three-way via `LC_PARITY_IMPL`: `lifecycle`, `handcrafted`, and
    `generated`.
46. `tests/baseline/_impl_switch.py` owns parity backend selection and the
    `lifecycle` backend loads only YIDL-owned code or `test-deps/` copies.
47. Copied lifecycle/freezable reference files are tests-only. They must not
    be imported by the public YIDL API/runtime and must not be included in
    pip-installed distributions.
48. Python-version validation uses `uv run --python <version>` across the
    active support sweep.
49. Handcrafted comprehensive and focused-slice baselines advance in parallel
    with generator work.
50. `UNSPECIFIED` is spec/decorator state; `VOID` is runtime slot state.
    Avoid database-reserved absent-value terminology in YIDL generated code
    and active design docs.
51. DDS is the schema and resolved-data substrate. It stores no
    decoration-time data until a `DDSContainerBuilder` is created for one
    decorated class.
52. `DDSContainer` is immutable after freeze. Derived data must be produced
    before freeze by generated operations, not lazily during query.
53. Matcher resources are `MatcherGeneratedValue` objects; raw arbitrary
    Python objects are not matcher resources.
54. The current transform API is not the final production runner.
    `ProductionSpec` / `ProductionGroupSpec` now cover collection,
    computed-collection, and matcher-result production, merge policies, and
    target ports. Builder-phase matcher views and fragment merge remain future
    DDS/codegen work only if reuse pressure requires them.
55. DDS capsule composition starts with direct contributors, not a new
    fragment model. Use `ensure_property`, `ensure_record`,
    `ensure_collection`, `ensure_computed_collection`, `ensure_port`,
    `ensure_port_index`, `ensure_production_group`, `ensure_matcher`, and
    `MatcherSpec.ensure_input` when multiple contributors share the same
    semantic surface. Identical definitions reuse; incompatible definitions
    reject.
56. Generated DDS runtime modules are assembled as one Astichi module.
    Runtime imports are expressed with `astichi_pyimport(...)` in the root
    module and inserted matcher runtimes, then final materialization
    consolidates those imports at module top. Do not splice emitted matcher
    source strings into the generated container module.
57. The capsule replacement path uses recorded concept plans.
    `CapsuleConceptBuilder` records schema, matcher, production, port, and
    aggregate-operation runtime-helper operations. `CapsuleConceptPlan` is the
    immutable replay object and composes other concepts with `extends=(...)`.
    Concept plans replay into the existing DDS/container/matcher implementation
    and load generated runtimes through `ConceptPlan.runtime().load()`. The
    older callback-based capsule-definition and fluent prototype modules are no
    longer authoritative.
    Recorded schema families use `concept.schema_family(...)` as definition-time
    sugar and lower to ordinary DDS unions and union variant records.
    Diagnostics are also ordinary concept records plus generated validation/gate
    operations; there is no separate DDS diagnostics engine.
    The first lifecycle concept assembly (`lifecycle_concepts.py`) uses this
    same recorded layer for field-family, transaction-index, class-structure,
    property-template, operation-contribution, and transaction-method records.
58. The first build-mapper seam is `CapsuleClassBuildPlan` /
    `build_class_source(...)`. It consumes generated runtime port records,
    turns `MatcherGeneratedValue` resources into Astichi composables, and wires
    configured child ports into configured Astichi holes. This is intentionally
    a narrow mapper seam, not a hard-coded field/init capsule model.
    Lifecycle module rendering uses the same principle: `render_lifecycle_module`
    consumes contribution records and recursively fills Astichi ports for module
    body, classes, class body, `__slots__`, `__init__`, and nested call-argument
    holes. The first staircase concept extends the contribution assembly with
    annotated/defaulted init parameters plus generated `commit()` / `rollback()`
    methods for managed fields.
