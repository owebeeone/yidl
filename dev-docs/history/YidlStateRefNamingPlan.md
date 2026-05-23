# YIDL StateRef Naming Plan

This note defines the proposed `StateRef` interface and the lowering model used
to translate logical state references into flattened generated field names.

The goal is to keep:

- generated code fast and direct
- external/helper code decoupled from the flattened slot naming scheme
- Astichi composition working with explicit semantic handles rather than
  string-building at every template site

## 1. Role

`StateRef` is a small immutable semantic reference object.

It identifies:

- what kind of state is being referenced
- which field it belongs to, when field-scoped
- which transaction it belongs to, when tx-scoped

It should not be treated as a rich runtime state object.

Its primary jobs are:

- carry semantic identity through harvesting/codegen
- lower into a concrete flattened slot name
- provide a fallback dynamic accessor for helper/external code

## 2. Proposed Interface

Minimal shape:

```python
class StateRef(ABC):
    @property
    @abstractmethod
    def field_name(self) -> str | None: ...

    @property
    @abstractmethod
    def tx_index(self) -> int | None: ...

    @property
    @abstractmethod
    def tx_name(self) -> str | None: ...

    @abstractmethod
    def slot_name(self, naming: StateNaming) -> str: ...

    @abstractmethod
    def get(self, yidl_state: Any) -> Any: ...

    @abstractmethod
    def set(self, yidl_state: Any, value: Any) -> None: ...

    @abstractmethod
    def exists(self, yidl_state: Any) -> bool: ...


@dataclass(frozen=True)
class PublishedValueRef(StateRef):
    field_name: str
    tx_index: int | None = None
    tx_name: str | None = None


@dataclass(frozen=True)
class WorkingValueRef(StateRef):
    field_name: str
    tx_index: int
    tx_name: str | None = None


@dataclass(frozen=True)
class CurrentFieldStateRef(StateRef):
    field_name: str
    tx_index: int | None = None
    tx_name: str | None = None


@dataclass(frozen=True)
class WorkingFieldStateRef(StateRef):
    field_name: str
    tx_index: int
    tx_name: str | None = None


@dataclass(frozen=True)
class WorkingPresentRef(StateRef):
    field_name: str | None = None
    tx_index: int
    tx_name: str | None = None


@dataclass(frozen=True)
class WorkingTxIdRef(StateRef):
    field_name: str | None = None
    tx_index: int
    tx_name: str | None = None


@dataclass(frozen=True)
class InitvarConstructionRef(StateRef):
    field_name: str
    tx_index: int | None = None
    tx_name: str | None = None


@dataclass(frozen=True)
class InitvarRetainedRef(StateRef):
    field_name: str
    tx_index: int | None = None
    tx_name: str | None = None
```

Rules:

- field-scoped refs expose `field_name`
- tx-scoped refs expose `tx_index`
- `tx_name` is optional metadata for diagnostics/docs
- the semantic target is represented by the concrete `StateRef` subtype, not by
  an enum discriminator or a free-form `property` string

## 3. Preferred Construction API

Callers should not instantiate arbitrary `StateRef(...)` combinations directly.

Preferred constructors:

```python
PublishedValueRef("foo")
WorkingValueRef("foo", tx_index=2, tx_name="publish")
CurrentFieldStateRef("foo")
WorkingFieldStateRef("foo", tx_index=2, tx_name="publish")
WorkingPresentRef(tx_index=2, tx_name="publish")
WorkingTxIdRef(tx_index=2, tx_name="publish")
InitvarConstructionRef("seed")
InitvarRetainedRef("seed")
```

This prevents invalid combinations and keeps template/harvester code explicit.

## 4. Canonical StateRef Types

| Type | Field-scoped | Tx-scoped | Meaning |
|---|---|---|---|
| `PublishedValueRef` | Yes | No | Authoritative committed value home for a field |
| `WorkingValueRef` | Yes | Yes | Working overlay value home for a field in a tx key |
| `CurrentFieldStateRef` | Yes | No | Current runtime sidecar state for a field |
| `WorkingFieldStateRef` | Yes | Yes | Working copied runtime sidecar state for a field |
| `WorkingPresentRef` | No | Yes | Whether a working overlay currently exists for that tx |
| `WorkingTxIdRef` | No | Yes | The active tx id that owns the working overlay |
| `InitvarConstructionRef` | Yes | No | Constructor-phase initvar home |
| `InitvarRetainedRef` | Yes | No | Retained initvar home for late consumers |

Later additions are possible, but these should be treated as the stable base
surface.

## 5. Lowering Model

Concrete `StateRef` types should lower through one naming object rather than ad hoc f-strings
spread throughout templates.

Suggested interface:

```python
class StateNaming(Protocol):
    def slot_name(self, ref: StateRef) -> str: ...
```

Suggested default flattened templates:

| StateRef type | Required data | Flat slot template |
|---|---|---|
| `PublishedValueRef` | `field_name` | `__y_pv__{field_name}` |
| `WorkingValueRef` | `field_name`, `tx_index` | `__y_wv__t{tx_index}__{field_name}` |
| `CurrentFieldStateRef` | `field_name` | `__y_cfs__{field_name}` |
| `WorkingFieldStateRef` | `field_name`, `tx_index` | `__y_wfs__t{tx_index}__{field_name}` |
| `WorkingPresentRef` | `tx_index` | `__y_wp__t{tx_index}` |
| `WorkingTxIdRef` | `tx_index` | `__y_wtx__t{tx_index}` |
| `InitvarConstructionRef` | `field_name` | `__y_ivc__{field_name}` |
| `InitvarRetainedRef` | `field_name` | `__y_ivr__{field_name}` |

The exact prefixes can still change, but the lowering table should be
centralized and deterministic.

## 6. Dynamic Accessor Fallback

The primary target is still direct lowered field access in generated code.

But `StateRef` should also support a fallback dynamic accessor surface for
helpers, external libraries, debugging, and glue code:

```python
value = state_ref.get(yidl_state)
state_ref.set(yidl_state, value)
present = state_ref.exists(yidl_state)
```

This is useful in cases where:

- code is not generated all the way down
- a helper is shared across multiple generated classes
- an external integration should not know flattened field names
- Astichi templates need a safe fallback before a fully direct lowering exists

This fallback should be treated as a convenience/compatibility layer, not the
hot-path model for generated code.

## 7. Relationship To Field Descriptors

Each harvested/generated field descriptor should carry `StateRef`s for the
locations it owns.

Example:

```python
FieldLayout(
    field_name="total",
    tx_name="publish",
    tx_index=2,
    published_value_ref=PublishedValueRef("total"),
    working_value_ref=WorkingValueRef("total", tx_index=2, tx_name="publish"),
    current_field_state_ref=None,
    working_field_state_ref=None,
)
```

That lets later phases use either:

- the semantic `StateRef`
- or the already-lowered slot name derived from it

without recomputing naming rules at every emission site.

## 8. Astichi Integration Direction

For Astichi-backed emission, the useful pattern is:

- field descriptors carry `StateRef`s
- codegen lowers those refs into final slot names before or during composition
- Astichi templates consume the lowered names as bound values

That keeps templates simple:

- no repeated string-building in template code
- no template-local tx-name/tx-id logic
- no need for templates to understand the whole naming table

If necessary, the temporary fallback is acceptable:

- bind a `StateRef`
- call `state_ref.get(yidl_state)` / `state_ref.set(...)`

But the preferred mature path remains direct slot-name lowering.

## 9. Design Position

The intended split is:

- semantic identity lives in concrete `StateRef` types
- flattened storage identity lives in `StateNaming`
- field descriptors carry precomputed refs and may also cache final slot names
- generated code should usually use the final slot names directly
- non-generated utilities may go through the `StateRef` dynamic accessor layer

This gives YIDL a stable logical model without forcing every consumer to know
the physical flattened names.
