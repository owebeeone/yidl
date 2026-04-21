# YIDL Multi-Facade Model Schema Design

This document defines the current schema footing for YIDL's generated
multi-facade model.

Its job is to solidify where generated semantics live, where data lives, how
facade names relate to stores, and which design holes still need focused work
before the grammar and generator can be considered stable.

This document is intentionally compared against `pyrolyze.lifecycle` because
lifecycle already demonstrates one concrete multi-facade implementation. The
important distinction is that lifecycle hard-codes several names and structural
choices, while YIDL must model those same ideas as generated/transducer-defined
semantics.

## 1. Glossary

These terms should be treated as aligned, not competing:

- facade
- proxy
- veneer

All three refer to application-facing generated surfaces.

YIDL should use `facade` as the primary term in design documents. `proxy` and
`veneer` are explanatory aliases only.

## 2. Facade Names vs Store Names

This distinction must be explicit from the start.

Lifecycle exposes user-visible facade names such as `current` and `working`.
Those names are hard-coded into the lifecycle implementation.

YIDL also needs generated facade names such as `current` and `working`, but in
YIDL those names are not magic by themselves. Their meaning comes from the
transducers and the generated mapping onto stores.

Hard rules:

- `current` and `working` are facade names as concepts in generated managed
  fields
- facades are application-facing surfaces
- stores are physically separate objects from facades
- store names are generated/declared names, not the meaning of the field by
  themselves
- `committed` is both a useful concept and a likely store-name pattern, but it
  is not a fixed required identifier in YIDL
- transducers define the semantics that map facade access onto stores

Example of the distinction:

- `working` is a facade name
- a working-facing transducer may map that facade to one or more physical
  slotted store fields
- the fact that a field is visible on `working` does not imply any fixed store
  object name

## 3. Hard Requirements

The generated class must preserve the user-class feel as much as possible.

That means:

- the emitted main facade should inherit from the user-declared class
- generated current/working facades should also inherit from the user-declared
  class
- user methods should run on main/current/working facades and route through the
  same declared field names
- generated internals must use a collision-resistant `__y_...` prefix
- the user-visible contract may include `current` and `working`
- YIDL may introduce other generated identifiers, but they must not casually
  collide with user code

The purpose is that a generated class should still feel like “the user class,
but with declared superpowers”, similar in spirit to dataclasses, pydantic, and
lifecycle.

## 4. Layer Model

YIDL currently needs at least four distinct layers.

### 4.1 Facade Layer

These are behavior-bearing application-facing objects.

Examples:

- main facade
- current facade
- working facade

These objects may expose:

- generated properties
- user methods
- routing logic
- convenience helpers tied to that facade

They must not be the home for opaque runtime bookkeeping that should be shared
uniformly across facades.

### 4.2 Store Layer

Stores are zero-behavior objects whose job is to hold data.

Stores may hold:

- committed field values
- scratch snapshots used only for commit/rollback repair
- plain slotted storage for optimized local/current/working values

Values may also be homed directly on a facade when the YIDL definition selects
that optimization. `local_store` is the obvious example where the self/main
facade may be the natural home for raw-speed read/write access.

Stores must not hold:

- transaction manager references
- field metadata
- commit ordering policy
- rollback error aggregation
- helper dispatch policy

If an object is a store, it is data first. If a helper function must exist near
store data for optimization reasons, that choice must be deliberate and called
out explicitly rather than treated as the default model.

### 4.3 YidlState Layer

`YidlState` is the shared runtime anchor visible from all facades.

It should hold:

- transaction manager
- non-const field metadata
- field runtime state records
- rollback/cleanup error aggregation
- other cross-facade runtime coordination data

Const metadata should not generally require runtime access. If metadata is truly
const, it should normally be compiled directly into generated functions.

This is where field state belongs, not in stores.

### 4.4 Field Runtime State Layer

Each field may need a runtime-state record that can express at least:

- transaction group
- whether a working value exists
- which transaction owns the working value
- prior committed value snapshot when partial commit rollback needs it
- anything else explicitly defined by the transducer

That record must be accessible from any generated facade through `YidlState`.

This should be read broadly: any facade defined in YIDL should be able to
reach the relevant field runtime state through `YidlState`, not only the common
proxy/current/working trio.

## 5. Naming Rules

Generated internals should use `__y_...` names.

Examples:

- `__y_state`
- `__y_current_store`
- `__y_commit_scratch_store`
- `__y_working_child`

This keeps collisions with user code unlikely while leaving application-facing
facade names available.

Value stores and control stores should also be treated as separate naming
namespaces. The generator should know whether an internal name is:

- a facade-facing value location
- a control-state location
- a scratch/repair location
- a transducer helper location

## 6. Store Policy

The store split should be explicit.

Minimum useful stores today:

- committed-value store
- generic commit scratch store

Possible future stores:

- dedicated working store for fields where that shape wins
- initvar/post-init parameter store
- validation snapshot store

`initvar` / post-init parameter storage is not just hypothetical. Lifecycle
already demonstrates that an initvar can be retained and referenced later by
things such as `working_default_factory`, so this should be treated as an
active design requirement rather than a speculative extension.

One open implementation question is whether a single large physical slotted
store can carry many logical store namespaces by using generated field names
rather than multiple Python objects. That is a real optimization path and
should remain on the table.

Related practical concern:

- what Python slot-count or flattening limits may exist for this strategy

Another important point is that “commit scratch store” is generic. It is not
just “previous store”; it is the namespace where prior transaction data,
partial-rollback data, validation scratch, or other repair-oriented snapshots
may live.

## 7. Field-Spec Composition

The lifecycle meanings of `binding` and `owned` should be treated as the
starting semantic model for YIDL.

Definitions:

- `binding`: resource semantics without transactional managed overlay
- `owned`: `binding` plus managed/transactional semantics

That means:

- `binding` is a resource-holding concept built around `BindingBase`
- `owned` is the transactional/managed version of that resource-holding concept

YIDL should eventually document all lifecycle field-spec behaviors explicitly,
because these meanings matter when deciding what the grammar is actually
describing.

## 8. Binding / Owned Container Shapes

Single value, list, and map forms are not a settled trivial detail.

Today, the important hard statement is:

- binding/owned may apply to single values, lists, or maps

The unresolved hole is whether those should be modeled as:

- one semantic family with generated shape selection
- or three separate transducers
- or combined transducers that can auto-select the right specialization

One hard directional requirement to preserve is that the grammar should be able
to expose container ownership semantics directly. Whether that becomes separate
surface syntax, transducer-driven shape selection, or some hybrid is still
open, but the grammar cannot treat container ownership as invisible incidental
detail.

This is a major design hole, not a minor note. It affects:

- the YIDL source model
- grammar surface area
- transducer composition
- commit/rollback generation
- specialization opportunities

This needs its own focused design work once the implementation space is better
understood.

## 9. Initialization Tracking

Initialization tracking is important and unresolved.

The system needs a reliable “is initialized” detection method. That includes
cases where YIDL wants to remove initialization overhead by doing work lazily,
similar in spirit to static/default-driven strategies.

This is currently `TBD`.

Hard requirement:

- YIDL must support explicit initialization detection semantics
- YIDL should not rely on dataclasses `MISSING` for this role

Direction to preserve:

- choose a distinct YIDL sentinel or equivalent mechanism for “not yet
  initialized”; `VOID` is a candidate name worth serious consideration

Open research item:

- which mechanism is best

Candidates worth studying:

- explicit boolean/bitmask tracking
- optimistic read followed by initialization on failure
- lazily initialized slot patterns
- other generated techniques benchmarked across Python versions

Concrete strategy sketches worth preserving for study:

- optimistic read in a `try`/fallback initialization path
- explicit bitmask/flag checks per field or per store
- generated initialization helpers that collect the required parameters from the
  current store/state layout before constructing the value

One concrete mechanism idea worth preserving explicitly:

- a generated helper such as `create_init_for_store_value(...)` that gathers
  the required parameters from the store/state layout and returns the
  initialization callable or constructed value needed for that field

Do not lock this design prematurely. It needs research first.

## 10. Transducer-to-Store Relationship

The schema must be able to express how a transducer interacts with storage.

For each field/helper kind, YIDL needs to know:

- how many stores/facades it uses
- where committed value lives
- where working value lives
- whether prior committed value must be retained during commit
- how rollback destroys or restores staged state
- how close/cleanup is triggered when ownership ends

Examples:

- plain managed scalar:
  committed value + working value
- owned scalar:
  committed value + working value + prior committed scratch during commit
- owned list/map:
  current container + working container + prior committed scratch during commit
  with best-effort rollback/cleanup semantics

The important point is that field semantics live in the transducer. Stores are
only the physical data targets the transducer maps to.

## 11. Resource Contract

YIDL-owned internal structures are invisible to the user, so YIDL must preserve
the refcounted resource contract on their behalf.

That means:

- provisional owned values replaced during the same transaction should be
  released promptly
- rollback should attempt cleanup for every staged owned field at least once
- commit should defer release of replaced committed values until the new value
  is installed
- discard of refcounted objects must happen only after the final data
  structures are in their final consistent order
- any list of objects to `dec_ref()` should live only in local generated state,
  not in durable user-visible structures

One tricky point is transaction tying. If transaction APIs later allow multiple
transaction groups to be tied or coordinated, YIDL may need an additional
transaction-manager-level release signal so deferred resource release is not
forced too early.

For container ownership, YIDL may rely on runtime helpers such as
`BindingList` / `BindingDict`, but the generator still owns the higher-level
commit/rollback ordering around those helpers.

## 12. Rollback Policy

Rollback is best-effort cleanup, not “stop on first error”.

Hard rule:

- rollback must visit every rollback-relevant field at least once
- cleanup failures must be collected
- rollback must not stop after the first cleanup failure
- rollback should raise an `ExceptionGroup`, even if only one cleanup error was
  collected

This keeps rollback traversal robust while preserving the real failure set.

## 13. Directional Design Notes

These are not vague ideas; they are meaningful implementation directions.

### 13.1 Store Allocation

While there may be multiple logical surfaces such as:

- `current.field_x`
- `working.field_x`

those may still resolve to a single physical slotted store object with multiple
generated field names.

This suggests that:

- loads/stores should be as direct as possible in generated Python
- transaction data keyed by logical concepts may be flattened into direct field
  names
- finite known keys such as transaction-group resources can be translated into
  slotted identifiers

### 13.2 Refcounted Facades

The runtime `BindingBase` model makes it possible to reason about when certain
generated structures are no longer referenced.

If YIDL ever enables a “refcounted main facade” feature, then:

- weakref topology likely becomes necessary
- cyclic references must be avoided if deterministic `__del__` timing matters
- lazily created secondary facades need a topology that preserves lifecycle
  semantics without keeping everything alive forever

Stronger consequence to keep in view:

- if deterministic refcount-driven teardown is required, facade retention rules
  may become strict enough that some seemingly convenient native/facade-homed
  placements stop being viable for that mode

This is a serious design area, not something to improvise later.

### 13.3 Transaction IDs and Flattened Control State

YIDL will likely need to flatten transaction-group-related control state into
direct generated field names.

That implies:

- store-field name generation
- transaction-group-id to identifier translation
- Python-source-visible algorithms for per-field transaction resources
- a source-to-AST path where helper/transducer code can refer to abstract store
  references and `astichi` lowers them into concrete generated field accesses

The source-hook path should be kept explicit:

- some per-field or per-transaction algorithms may live in Python source files
- those files may be imported as Python modules for ordinary development use
- their source may then be rediscovered and retranslated into AST
- abstract references such as store-ref or tx-group-ref forms can then be
  lowered by `astichi` into concrete generated field accesses

This is one of the reasons the transducer source model needs to remain explicit.

### 13.4 Lazy Facade Allocation

To optimize initialization time, it may be possible to allocate only:

- the main facade
- and the underlying state/store object

with secondary facades created lazily on first access.

This raises real topology questions:

- how are secondary facades recreated
- how are they preserved or reaped
- how is deterministic lifecycle maintained if refcounted facade features exist

More specifically:

- if the main facade becomes unreferenced, what is notified immediately
- how do secondary facades remain reconstructible or retainable without causing
  the wrong objects to stay alive indefinitely

The “lazy star-chain” idea is promising, but it needs a proper design pass.

## 14. Virtual vs Physical Layout

Hard distinction:

- multiple virtual stores may exist purely to disambiguate allocation semantics
- the physical layout may still be one large slotted object

This is a good example of why the schema must separate:

- conceptual store namespaces
- physical storage layout

Those are related, but they are not the same thing.

## 15. Open Holes That Must Be Covered

These are the main unresolved design holes that need more than a paragraph.

### 15.1 Single vs List vs Map Binding/Owned Transducers

We need a real design answer on whether YIDL should use:

- separate transducers
- combined transducers with specialization
- or an auto-selected transducer family

This is large enough to deserve its own design document.

### 15.2 Initialization Detection Mechanism

We know initialization detection must exist.

We do not yet know which mechanism is best.

This requires focused research and benchmark work before the design can be
locked.

### 15.3 Lazy Facade Topology

If facades are lazily created and some become refcount-sensitive, the retention
topology must be designed explicitly.

### 15.4 Grammar Coverage

The current grammar does not yet fully describe:

- number of stores required by a transducer
- field-local scratch/previous-commit retention
- destruction/cleanup policy
- rollback error aggregation behavior
- optimized per-kind surface placement decisions
- container-shape-specific transducer selection

This document should drive the next grammar/design pass. After that, the design
matrix should be revisited.
