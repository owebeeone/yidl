# YIDL Transactional Base Phase H Plan

## Scope

Phase H defines and implements retained `BindingBase` field support.

The main marker is `owned()`, which is a transactional retained resource field:
effectively a managed value with `BindingBase` validation, identity comparison,
current/working transactional visibility, and `accepted()` on commit.

Phase H should also absorb the first simple `binding()` slice. In this narrow
form, `binding()` is just a plain stored field whose value is a `BindingBase`
or a supported `BindingBase` container. It is not graph binding, reactive
binding, cross-object dataflow, or lifecycle-child ownership.

YIDL already has the lifetime substrate in `src/yidl/runtime/bindings.py`.
That default binding implementation relies on Python's intrinsic references and
`BindingBase.__del__` cleanup rather than the explicit `inc_ref` / `dec_ref`
model in `pyrolyze.lifecycle`. The explicit fallback remains available in
`src/yidl/runtime/bindings_refcount.py` if circular-reference pressure or
alternate Python runtimes require it later.

## Parity Decision

YIDL does not need exact `pyrolyze.lifecycle.BindingBase` parity in Phase H.
The default implementation should not manually retain/release values.

Consequences:

- generated code does not call `inc_ref()` or `dec_ref()`.
- owner cleanup only means dropping YIDL-held references.
- if user code still holds a resource reference, `BindingBase.__del__` will not
  run yet.
- tests must not assert the pyrolyze behavior where `owner.close()` closes a
  child that is still strongly referenced by a local variable.
- if this becomes a practical problem, a later slice can select
  `bindings_refcount` or add an explicit close protocol deliberately.

## Goals

1. Add `owned(...)` and simple `binding(...)` markers.
2. Treat owned fields as transaction-aware retained resource fields.
3. Treat binding fields as plain stored `BindingBase` fields.
4. Support scalar values of type `BindingBase | None`.
5. Support mapping values whose values are `BindingBase`.
6. Reuse Phase C default/default_factory parameter discovery.
7. Generate owned commit/rollback behavior using the default intrinsic
   reference model.
8. Add focused tests that prove ownership acceptance, rollback reference
   dropping, and binding type validation.

## Non-Goals

1. Do not implement lifecycle-generated child ownership in Phase H.
2. Do not propagate parent transactions into child lifecycle objects.
3. Do not implement graph/reactive binding relationships in Phase H.
4. Do not add a weak-ownership marker or option.
5. Do not switch the lifecycle generator to `bindings_refcount` unless the
   intrinsic-reference implementation cannot avoid reference cycles.
6. Do not solve distributed ownership or cross-process lifetimes.
7. Do not add deterministic `BindingBase` close parity with pyrolyze.

## Semantics

### Owned Scalar

An owned scalar field stores either `None` or a `BindingBase` instance.

```python
@lifecycle
class Owner:
    child: BindingBase | None = owned(default=None)
```

Lowered behavior:

- default and working facade writes require an active transaction for the
  field's `tx_key`.
- current facade writes are rejected.
- reads follow the normal managed overlay shape: working value when present,
  otherwise current value.
- commit calls `accepted()` on a new non-`None` working value before publishing
  it to current.
- rollback drops the working reference; under the default intrinsic-reference
  implementation this lets uncommitted resources close when no other references
  remain.
- if lifecycle `close()` is added or already available in a later slice, owned
  fields should contribute a reference-dropping close snippet. That close does
  not guarantee `BindingBase._close()` while external references remain.

The generated code should not call `inc_ref()` or `dec_ref()` in the default
implementation. Those methods belong to the fallback explicit-refcount module.

### Owned Mapping

An owned mapping field stores a mapping whose values are `BindingBase`
instances.

```python
@lifecycle
class Owner:
    children: dict[str, BindingBase] = owned(default_factory=dict)
```

The first YIDL slice can normalize mappings to `BindingDict` so freeze/COW
behavior is provided by `src/yidl/runtime/bindings.py`. Commit accepts each new
binding value that becomes current. Rollback releases provisional values by
dropping the working container reference.

The mapping form should mirror the existing `BindingDict` tests rather than
reimplement explicit occurrence counting in generated code.

### Simple `binding(...)`

Phase H should merge the simple Phase I `binding(...)` case.

The first `binding(...)` implementation is deliberately small:

- it is a plain stored field, not a transaction-aware owned value.
- it validates scalar or mapping `BindingBase` values.
- it reuses the same default/default_factory and annotation harvesting surfaces.
- it does not add graph binding, source/target resolution, cycles, or
  cross-object dataflow.

Future graph binding can still get a later plan if it proves to be a different
feature. The previous Phase I plan is therefore merged into Phase H for this
simple stored-resource subset.

## Initial Proof

Use a golden source for a narrow retained-resource case:

```python
from yidl.runtime.bindings import BindingBase
from yidl.runtime.lifecycle import binding
from yidl.runtime.lifecycle import lifecycle
from yidl.runtime.lifecycle import owned


class SpyBinding(BindingBase):
    def __init__(self, name: str):
        self.name = name
        self.closed: list[bool] = []
        super().__init__()

    def _close(self) -> None:
        self.closed.append(self.is_accepted)


@lifecycle
class Owner:
    child: BindingBase | None = owned(default=None)
    children: dict[str, BindingBase] = owned(default_factory=dict)
    handle: BindingBase | None = binding(default=None)
```

Expected runtime checks:

```python
owner = Owner()
child = SpyBinding("child")

with owner.begin():
    owner.child = child

assert owner.current.child is child
assert child.is_accepted is True

with owner.begin():
    owner.child = None

assert owner.current.child is None
```

Rollback checks should prove provisional owned values are no longer referenced
by the owner after rollback. If a test wants to observe `BindingBase.__del__`,
it must not keep an external strong reference and may need to force collection.

## Diagnostics

- `owned` scalar assignment rejects values that are neither `None` nor
  `BindingBase`.
- `owned` mapping assignment rejects non-mapping values.
- `owned` mapping assignment rejects mapping values that are not `BindingBase`.
- `binding` uses the same scalar and mapping value checks.
- `owned(default_factory=...)` uses normal Phase C callable parameter
  discovery; unsupported callable signatures get the same diagnostics as
  managed/transient factories.
- `owned` with a transaction key not present in the resolved class tx-key map
  is rejected by the same tx-key validation as managed/transient fields.

Lifecycle-child diagnostics are explicitly out of scope for Phase H.

## Implementation Shape

Phase H should be a feature YIDL layer over the Phase G lifecycle base:

```text
tests/data/yidl/yidl_transactional_lifecycle/lifecycle_owned.yidl
```

The base lifecycle YIDL should import and apply the owned layer after managed
and transient layers.

Likely YIDL facts:

- `OwnedFields`
- `IndexedOwnedFields`
- `OwnedMapFields`
- `OwnedScalarFields`
- `BindingFields`
- `BindingMapFields`
- `BindingScalarFields`

Likely generated resources:

- state current slot initialization
- state working slot initialization
- default/working facade getters and setters
- current facade getter
- commit branch for scalar owned fields
- commit branch for map owned fields
- rollback branch
- optional close branch if the lifecycle close surface lands in this slice
- plain binding property and assignment resources

The resources should use the default `yidl.runtime.bindings` API. Do not emit
manual `inc_ref()` / `dec_ref()` calls unless a later fallback slice explicitly
selects `bindings_refcount`.

## Verification

Goldens:

```text
tests/data/gold_src/yidl_transactional_phase_h_owned.py
tests/data/goldens/materialized/yidl_transactional_phase_h_owned/
```

Focused tests:

- marker harvesting recognizes `owned(...)`.
- marker harvesting recognizes simple `binding(...)`.
- scalar owned commit calls `accepted()` before the value becomes current.
- scalar owned rollback drops the provisional owner reference.
- owned replacement drops the replaced owner reference.
- owned map commit accepts all new values.
- owned map rollback drops provisional owner references.
- simple binding fields reject non-`BindingBase` values.
- invalid scalar and map values raise targeted diagnostics.
- generated source does not contain `inc_ref(` or `dec_ref(` for the default
  intrinsic-reference implementation.

## Circular Reference Watchpoint

The default implementation depends on Python object lifetime. That is fast and
should be enough if owned resources do not form cycles with their owner.

Phase H should add one documented stress test or inspection note for owner-child
cycles. If a practical owned-resource cycle cannot be avoided, do not patch
around it locally in generated code. Instead, add a later fallback slice that
selects `yidl.runtime.bindings_refcount` for lifecycle owned resources and emits
the explicit retain/release hooks deliberately.

## Roll-Build

Suggested tag prefix:

```text
txphaseH-owned/
```

### Slice H1: Markers And Harvested Facts

Add the frontend marker surface and harvested facts only.

Deliverables:

- `owned(...)` marker beside `managed`, `transient`, and `field`.
- simple `binding(...)` marker beside `owned`.
- `FieldKind == "owned"` and `FieldKind == "binding"` facts.
- default/default_factory/init/tx-key parameters follow the existing marker
  conventions.
- factory parameter discovery works for owned and binding default factories.
- no generated source changes beyond facts being visible to the existing
  compiler pipeline.

Verification:

- focused marker/harvester tests pass.
- invalid default/default_factory combinations reuse existing diagnostics.
- inherited field merge allows unmanaged-to-owned or unmanaged-to-binding only
  if the existing override policy already allows that transition; do not add
  new override semantics in this slice.

Tag:

```text
txphaseH-owned/H1
```

### Slice H2: Simple Binding Stored Fields

Implement the merged simple `binding(...)` subset.

Deliverables:

- `BindingFields`, `BindingScalarFields`, and `BindingMapFields` computed
  collections.
- scalar binding current/default property lowering as a plain stored field.
- mapping binding normalization/validation using `BindingDict` where needed.
- assignment diagnostics for invalid scalar and map values.
- no transaction commit/rollback hooks for simple binding fields.

Verification:

- focused tests prove scalar `binding` accepts `None` and `BindingBase`.
- focused tests prove scalar `binding` rejects non-`BindingBase` values.
- focused tests prove mapping `binding` rejects non-mapping values and mapping
  entries that are not `BindingBase`.
- generated source for this slice contains no `accepted(`, `inc_ref(`, or
  `dec_ref(` for simple binding fields.

Tag:

```text
txphaseH-owned/H2
```

### Slice H3: Scalar Owned Overlay

Implement scalar `owned(...)` as transaction-aware retained resource storage.

Deliverables:

- `OwnedFields`, `IndexedOwnedFields`, and `OwnedScalarFields` computed
  collections.
- scalar owned current/default/working property lowering.
- default and working setters require an active transaction.
- current setter rejects.
- commit branch calls `accepted()` on the new non-`None` value before
  publishing it to current.
- rollback branch drops the provisional owner reference by clearing the working
  slot.
- no manual `inc_ref()` / `dec_ref()` in generated source.

Verification:

- focused tests prove commit publishes the owned value and marks it accepted.
- focused tests prove rollback leaves current unchanged and drops the working
  owner reference.
- focused tests prove replacement with `None` happens transactionally.
- focused tests prove invalid assigned values raise a targeted diagnostic.

Tag:

```text
txphaseH-owned/H3
```

### Slice H4: Owned Mapping

Implement owned mapping fields.

Deliverables:

- `OwnedMapFields` lowering.
- map assignment validates mapping shape and `BindingBase` values.
- commit accepts each newly committed binding value.
- rollback drops the provisional map owner reference.
- mapping storage uses the default `yidl.runtime.bindings` substrate and does
  not reimplement explicit refcount occurrence accounting in generated code.

Verification:

- focused tests prove map commit accepts all new values.
- focused tests prove map rollback does not publish provisional values.
- focused tests prove invalid map assignments raise targeted diagnostics.
- generated source contains no `inc_ref(` or `dec_ref(`.

Tag:

```text
txphaseH-owned/H4
```

### Slice H5: Golden And Regression

Complete the end-to-end retained-resource fixture.

Deliverables:

- `tests/data/gold_src/yidl_transactional_phase_h_owned.py`
- `tests/data/goldens/materialized/yidl_transactional_phase_h_owned/`
- materialized decorator and generated-output goldens.
- source-shape assertions covering `accepted()`, lack of manual refcount calls,
  scalar binding validation, scalar owned commit, and owned map commit.

Verification:

- focused lifecycle retained-resource tests pass.
- Phase H golden matches.
- full regression suite passes.

Tag:

```text
txphaseH-owned/H5
```
