# YIDL Lifecycle Store Classifications

This note classifies the lifecycle helper surface by value-home pattern and
records the additional generated control/meta structures YIDL needs when it
flattens lifecycle state.

Sources reviewed:

- `docs/YIDLRuntimeClassModel.md`
- `dev-docs/YidlMultiFacadeModelSchemaDesign.md`
- `dev-docs/RuntimeExtractionPlan.md`
- `pyrolyze/src/pyrolyze/lifecycle.py`

Conventions used here:

- "home" means a runtime location that actually stores a field value
- class runner tables are not counted as value homes
- names below are normalized design labels, not fixed emitted identifiers
- `tx_index` means the integer in `0..num_tx_groups-1`
- each field participates in exactly one `tx_index`
- transaction groups remain independent; YIDL does not combine their state

## 1. Field Helper Classification

| Helper | Facade pattern | Value homes | Normalized YIDL homes | Lifecycle backing | Multi-home? | Notes |
|---|---|---:|---|---|---|---|
| `managed` | overlay | 2 | `PublishedStore.<field>`, `WorkingStore[tx_index].<field>` | `current_record.values`, `working_record.values` | Yes | Canonical current/working split. Optional state sidecars also exist when `state_factory` / `state_copy` are used. |
| `const` | shared current-backed | 1 | `PublishedStore.<field>` | `current_record.values` | No | Read-only after construction/default resolution. |
| `static` | shared current-backed | 1 | `PublishedStore.<field>` | `current_record.values` | No | Single-write semantics; still one home. |
| `binding` | overlay | 2 | `PublishedStore.<field>`, `WorkingStore[tx_index].<field>` | `current_record.values`, `working_record.values` | Yes | Same physical homes as `managed`; commit/rollback semantics differ. |
| `owned` | overlay | 2 | `PublishedStore.<field>`, `WorkingStore[tx_index].<field>` | `current_record.values`, `working_record.values` | Yes | Same physical homes as `binding`; ownership policy differs. |
| `transient` | overlay | 2 | `PublishedStore.<field>`, `WorkingStore[tx_index].<field>` | `current_record.values`, `working_record.values` | Yes | Working value is tx-scoped; current home remains the base/default side. |
| `local_store` | native instance home | 1 | `InstanceStore.<field>` | `local_store_values` | No | Non-transactional, proxy-native storage. |
| `derived` | cached instance home | 1 | `DerivedCache.<field>` | `derived_values` | No | Reset on commit, rollback, and close. Likely emitted on instance-owned storage. |
| `initvar` | hidden constructor-only | 1-2 | `HiddenStore.construction.<name>`, optional `HiddenStore.retained.<name>` | `_construction_initvars`, optional `_retained_initvars` | Conditional | Needs the retained home only if late consumers still need the value after `__init__`. |
| `classvar` | class-only | 1 | class attribute | managed class attribute | No | Materialized on the managed/generated class, not on instances. |
| `commit_order_key` | shared current-backed metadata | 1 | `PublishedStore.<field>` | `current_record.values` | No | Per-instance value, plus class metadata mapping `tx_group -> field`. |
| `commit_validator` | shared current-backed metadata | 1 | `PublishedStore.<field>` | `current_record.values` | No | Per-instance callable value, plus class metadata mapping `tx_group -> field`. |
| `on_before_commit` | declaration-only | 0 | class runner metadata only | class runner tables | No | No instance value home. |
| `on_after_commit` | declaration-only | 0 | class runner metadata only | class runner tables | No | No instance value home. |
| `on_after_rollback` | declaration-only | 0 | class runner metadata only | class runner tables | No | No instance value home. |

Helpers that actually require more than one value home:

- `managed`
- `binding`
- `owned`
- `transient`
- `initvar` conditionally

## 2. Additional Generated Control / Metadata Structures

This table captures the non-value structures that still need to exist even if
YIDL flattens stores rather than emitting generic `Record` objects.

| Scope | Normalized structure | Cardinality | Purpose | Notes |
|---|---|---:|---|---|
| per instance | `transaction_manager` | 1 | Runtime tx manager reference passed at construction | The injected init parameter / backing field name is generator-selected. |
| per instance, on main facade | `facade_strong_refs[facade_kind]` | 0..N strong refs | Main-facade star cache of currently materialized facades | Main is the only facade that holds strong refs to other facades. |
| per instance, on `YidlState` | `facade_weakrefs[facade_kind]` | 0..N weak refs | Weak cache used to resolve or recreate facades on demand | The state never owns facades strongly. |
| per instance | `closed` | 1 flag | Close-state guard | Matches lifecycle close semantics. |
| per instance | `ever_committed` | 1 flag | Tracks whether a commit has succeeded | Useful for lifecycle parity and hook behavior. |
| per class | `tx_index_to_group` | 1 tuple | Stable tx-id to tx-name mapping | Defines the `0..N-1` index space. Best emitted as immutable class metadata. |
| per class | `tx_group_to_index` | 1 map | Stable tx-name to tx-id mapping | Intended for utilities, reflection, and external helpers. Best emitted as immutable class metadata such as a frozen mapping. |
| per field | `field_tx_index[<field>]` | 1 per field | Declares the one tx group/index that owns the field | YIDL should keep the one-field-one-tx-index rule explicit. |
| per tx index | `working_present[tx_index]` or equivalent | 1 per tx | Whether this record currently participates in that transaction | This may be an explicit bit or derived from working-store allocation. |
| per tx index | `working_tx_id[tx_index]` | 1 per tx | The active tx id that owns the working overlay | Required for stale-working detection and commit/rollback routing. |
| per tx index | `WorkingStore[tx_index]` or flattened working slots | 1 namespace per tx | Holds speculative values for fields in that tx group | This is the main replacement for lifecycle's `working_record`. |
| per field, per tx index | `WorkingFieldState[tx_index].<field>` | optional | Holds copied runtime field state for fields that use `state_factory` / `state_copy` | Only exists for stateful fields. |
| per field | `CurrentFieldState.<field>` | optional | Holds current runtime field state | Only exists for stateful fields. |
| per instance | `HiddenStore.construction` | optional | Constructor-phase initvar storage | Cleared after construction completes. |
| per instance | `HiddenStore.retained` | optional | Retained initvar storage for late consumers | Needed only when post-init consumers still reference initvars. |
| per class | `commit_order_key_field_by_group` | 0-1 per tx group | Locate the field that provides commit ordering | Mirrors lifecycle's per-group special-field table. |
| per class | `commit_validator_field_by_group` | 0-1 per tx group | Locate the field that provides the validator callable | Mirrors lifecycle's per-group special-field table. |
| per class | `before_commit_runners[group]`, `after_commit_runners[group]`, `after_rollback_runners[group]` | 0..N per tx group | Hook dispatch metadata or generated function lists | If fully unrolled, these may become direct generated call sites instead of generic tables. |
| per field | `default_factory_runner[<field>]` | optional | Default-factory dispatch metadata | Can disappear if YIDL fully unrolls factory calls. |
| per field | `working_default_factory_runner[<field>]` | optional | Working-default-factory dispatch metadata | Same: can disappear if YIDL fully unrolls factory calls. |

## 3. Facade Weakref Strategy

Preferred topology:

- every facade holds a strong ref to `YidlState`
- `YidlState` holds only weak refs to facades
- the main facade holds strong refs to every currently materialized secondary
  facade
- secondary facades do not hold strong refs to each other

This gives a star topology rooted at the main facade rather than a secondary
chain or semi-circular back-ref model.

Operational rule:

- facade access goes through a state-owned accessor
- if the weakref for that facade kind is live, return it
- if the weakref is dead or absent, create a new facade, store a new weakref in
  `YidlState`, and ensure the main facade's strong-ref cache is refreshed
- when recreating the main facade, the rebuild step should also repopulate its
  strong links to any other still-live facades discoverable through the state's
  weak cache

Why this matters:

- `YidlState` can outlive any one facade without pinning the whole facade graph
- secondary facades can be reaped promptly when the main facade no longer keeps
  them alive
- facade re-creation remains deterministic because the state owns the canonical
  runtime stores and metadata
- there are no strong facade-to-facade cycles except through the main-facade
  star cache, which is intentional and centrally controlled

This strategy is the right place to hang lazy `current` / `working` allocation:

- facades are created only when first requested
- later requests resolve through the weak cache
- if a facade was collected, the accessor rebuilds it from `YidlState`

## 4. Flattening Rule

If YIDL flattens runtime storage, the minimum tx-aware control model is:

- one `tx_index` per field
- one class-level tx-name `<->` tx-id mapping
- one working-value namespace per `tx_index`
- one `working_tx_id[tx_index]`
- one participation indicator per `tx_index` or an equivalent derived rule

YIDL does not need one combined cross-group transaction state object.

Generated field-specific code should normally carry its own tx identity
directly:

- a field already knows its `tx_group` / `tx_index`
- direct generated code should not need to consult the class mapping for normal
  field reads/writes
- the class-level tx-name `<->` tx-id mapping exists primarily for non-generated
  utilities, reflection, and external-library integration

## 5. Need To Consider These Too

The structural model above is enough to move into the next stage, but a few
runtime scratch/control structures still need to be accounted for:

- deferred commit-cleanup queue for `binding` / `owned` evict-last sequencing
- factory-resolution stack or sentinel for default-factory cycle detection
- rollback / cleanup error aggregation list if YIDL preserves aggregated-close
  behavior
- transaction-manager-side active transaction state per tx group, including
  dirty-context tracking and validator-context tracking

These are important for full lifecycle parity, but they do not change the core
shape defined above:

- field value homes
- hidden initvar homes
- per-field `tx_index`
- class-level tx-name `<->` tx-id metadata
- per-tx working state
- field-state sidecars
- facade weakref/star topology
- thin tx-state accessors

The implementation choices are:

1. emit fully unrolled field-specific commit / rollback / close code over
   flattened fields
2. emit a thin accessor layer over flattened fields

The preferred direction is the first one. The second is acceptable if it stays
as a codegen convenience layer rather than becoming the primary semantic model.
