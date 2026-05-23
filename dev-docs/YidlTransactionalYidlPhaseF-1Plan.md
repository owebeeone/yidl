# YIDL Transactional Base Phase F-1 Plan

## Purpose

Phase F proved the marker and hook surface, but the generated transaction
lowering is still too rough. This plan tightens the lowered shape and adds
managed-field conversion functions before moving on to richer rollback behavior
or more transaction protocol features.

The immediate issues are:

1. Generated transaction-method branches compare against concrete transaction
   key literals such as `"default_transaction"`. That is wrong. The default
   transaction symbol is `DEFAULT_TRANSACTION`, and in general transaction
   keys can be any hashable object.
2. The generated state protocol takes both a transaction instance id and a
   transaction key:

   ```python
   def _commit_transaction(self, tx_instance_id, tx_key=DEFAULT_TRANSACTION): ...
   ```

   This mixes an instance-token check with a key/index dispatch concern. It is
   too easy to generate or call a mismatched pair.
3. The generated commit body is a single function containing repeated
   `if tx_index == N` branches. Field commit/rollback blocks become more
   complex once managed-field conversion functions and conversion failures are
   included. They need separate generated functions per transaction key.
4. Managed fields need the same conversion property names as
   `pyrolyze.lifecycle`: `freeze` and `thaw`.

## Terminology

Phase F-1 should use this vocabulary:

| Term | Meaning |
| --- | --- |
| `tx_key` | The user-facing transaction identity. Examples: `DEFAULT_TRANSACTION`, `"audit"`, or a custom hashable object. |
| `tx_index` | A generated class-local integer index for one `tx_key`. This exists so hot generated code can use slots/list indexes and `match` branches. |
| `tx_instance_id` | A runtime token for one active begin/commit/rollback cycle for one key. The current runtime calls this `tx_id`; that name is misleading. |
| `tx_token` | The generated-source and runtime-state shorthand for `tx_instance_id`. This is the preferred name in new generated code because it emphasizes ownership rather than key selection. |

`tx_key` and `tx_index` are a 1:1 pair for one generated lifecycle class. The
keys are build-time/runtime values passed to `build_lifecycle_class`; generated
source must not inline or stringify them:

```python
def build_lifecycle_class(
    decorated_cls,
    *,
    _Counter_tx_keys,
    ...
):
    class Counter:
        __yidl_tx_index_to_key__ = _Counter_tx_keys
        __yidl_tx_key_to_index__ = {
            key: index for index, key in enumerate(_Counter_tx_keys)
        }
```

`tx_key` should not be a YIDL lifecycle model term. It is the old runtime
name for what this plan calls `tx_key`. A "multi-group" scope in the current
runtime is more precisely a multi-key transaction scope.

## Current Runtime Facts

`TransactionManager` already supports multiple transaction keys active at the
same time.

- `TransactionManager.begin(key_a, key_b)` starts one `LifecycleTransaction`
  per key and returns a multi-key scope.
- Each key is currently managed by its own `GroupTransactionManager`.
- Each key has its own `begin_count`, active transaction, and transaction
  instance id sequence.
- `tests/test_transaction_yidl.py` already verifies independent begin counts
  and multi-key context-manager commit.

Because transaction instance ids are per key, the current `tx_id` alone is not
a unique address. Two active keys can both have instance id `1`. Therefore a
pure `_commit_tx_by_id(tx_id)` entrypoint is not valid unless a later runtime
slice makes transaction instance ids globally unique or adds an id-to-key map.

For Phase F-1, key/index dispatch is the right state boundary.

## Lowering Rule

Generated state code should dispatch by transaction index, not by transaction
key literal.

The reason this must be key/index based, rather than instance-id based, is that
two active transaction keys can both have the same transaction instance id.
`tx_token` is only an ownership guard after the key has selected the lane.

The generated class should carry key/index maps built from the builder
parameter:

```python
__yidl_tx_index_to_key__ = _Counter_tx_keys
__yidl_tx_key_to_index__ = {
    key: index for index, key in enumerate(_Counter_tx_keys)
}
```

All generated transaction-method dispatch should first derive `tx_index`:

```python
tx_index = self.__yidl_tx_key_to_index__[tx_key]
```

Then generated code should match on integer indexes:

```python
match tx_index:
    case 0:
        ...
    case 1:
        ...
```

This avoids rendering transaction key objects into generated Python source.
It also avoids special-casing the default transaction. The generated source can
still use `DEFAULT_TRANSACTION` in function defaults and as the first value in
the builder-provided key tuple, but branch predicates should never compare
against key literals or stringified key values.

The decorator/harvester owns key collection and ordering. Its build kwargs
should provide a tuple such as:

```python
_Counter_tx_keys = (DEFAULT_TRANSACTION, audit_key)
```

where `audit_key` can be any hashable runtime object. This tuple is passed into
the generated builder call; it is not synthesized as a literal inside generated
source. The YIDL-generated class then derives indexes from that tuple.

`_Counter_tx_keys` must be an ordered tuple, never a set. `tx_index` stability
depends on tuple order. The decorator/harvester should build the tuple with this
order:

1. `DEFAULT_TRANSACTION` at index `0`
2. inherited transaction keys in inherited metadata order, preserving parent
   indexes
3. new local transaction keys in first-seen class-body field declaration order

Transaction method markers may reference known keys, but they should not create
new keys by themselves in Phase F-1. A key is known when it is introduced by
inherited lifecycle metadata or by a local lifecycle field declaration before
method-marker validation runs. A marker-only key is not known. A marker that
references a key not present in the tuple remains a decorator-time diagnostic.

Generated code targets the same minimum Python version as the YIDL runtime,
currently Python 3.12 or newer. The `match` statement is therefore
unconditionally available.

## Proposed Context Protocol

Replace the generated context protocol entrypoints:

```python
_commit_transaction(tx_instance_id, tx_key=DEFAULT_TRANSACTION)
_rollback_transaction(tx_instance_id, tx_key=DEFAULT_TRANSACTION)
```

with key-addressed staged commit methods:

```python
_prepare_commit_tx_by_key(tx_key=DEFAULT_TRANSACTION, tx_token=None)
_apply_prepared_commit_tx_by_key(tx_key=DEFAULT_TRANSACTION, tx_token=None)
_after_commit_tx_by_key(tx_key=DEFAULT_TRANSACTION, tx_token=None)
_rollback_tx_by_key(tx_key=DEFAULT_TRANSACTION, tx_token=None)
```

`LifecycleTransaction.prepare_commits()` would call:

```python
context._prepare_commit_tx_by_key(self.tx_key, self.tx_token)
```

`LifecycleTransaction.apply_prepared_commits()` would call:

```python
context._apply_prepared_commit_tx_by_key(self.tx_key, self.tx_token)
```

`LifecycleTransaction.after_commits()` would call:

```python
context._after_commit_tx_by_key(self.tx_key, self.tx_token)
```

`LifecycleTransaction.rollback_dirty()` would call:

```python
context._rollback_tx_by_key(self.tx_key, self.tx_token)
```

The transaction manager is already processing one active transaction for one
key at that point. The key selects the generated lane; the token is only an
ownership/recovery guard for the lane. The state object derives `tx_index` from
the key and inspects `_y_working_tx_tokens[tx_index]` to decide whether it has
work for that key.

`_commit_tx_by_id(tx_id)` and `_rollback_tx_by_id(tx_id)` should not be part of
Phase F-1 unless the runtime also makes transaction instance ids globally
unique. If a future debugging or low-level API needs instance-id addressing, it
should reject ambiguous ids explicitly.

## Target Generated Shape

For a class with default transaction fields and an audit transaction key, the
generated shape should be closer to this. The audit key value is present only
in the builder-provided `_Counter_tx_keys` tuple, not in dispatch branches:

```python
def commit_order_key_for(self, tx_key=DEFAULT_TRANSACTION):
    tx_index = self.__yidl_tx_key_to_index__[tx_key]
    match tx_index:
        case 0:
            return self._commit_order_key_tx_0()
        case 1:
            return self._commit_order_key_tx_1()
    raise AssertionError("unreachable transaction index")


def requires_validation_for(self, tx_key=DEFAULT_TRANSACTION):
    tx_index = self.__yidl_tx_key_to_index__[tx_key]
    match tx_index:
        case 0:
            return self._requires_validation_tx_0()
        case 1:
            return self._requires_validation_tx_1()
    raise AssertionError("unreachable transaction index")


def validate_commit_for(self, tx_key=DEFAULT_TRANSACTION):
    tx_index = self.__yidl_tx_key_to_index__[tx_key]
    match tx_index:
        case 0:
            return self._validate_commit_tx_0()
        case 1:
            return self._validate_commit_tx_1()
    raise AssertionError("unreachable transaction index")


def _prepare_commit_tx_by_key(self, tx_key=DEFAULT_TRANSACTION, tx_token=None):
    tx_index = self.__yidl_tx_key_to_index__[tx_key]
    match tx_index:
        case 0:
            return self._prepare_commit_tx_0(tx_token)
        case 1:
            return self._prepare_commit_tx_1(tx_token)
    raise AssertionError("unreachable transaction index")


def _apply_prepared_commit_tx_by_key(self, tx_key=DEFAULT_TRANSACTION, tx_token=None):
    tx_index = self.__yidl_tx_key_to_index__[tx_key]
    match tx_index:
        case 0:
            return self._apply_prepared_commit_tx_0(tx_token)
        case 1:
            return self._apply_prepared_commit_tx_1(tx_token)
    raise AssertionError("unreachable transaction index")


def _after_commit_tx_by_key(self, tx_key=DEFAULT_TRANSACTION, tx_token=None):
    tx_index = self.__yidl_tx_key_to_index__[tx_key]
    match tx_index:
        case 0:
            return self._after_commit_tx_0(tx_token)
        case 1:
            return self._after_commit_tx_1(tx_token)
    raise AssertionError("unreachable transaction index")


def _rollback_tx_by_key(self, tx_key=DEFAULT_TRANSACTION, tx_token=None):
    tx_index = self.__yidl_tx_key_to_index__[tx_key]
    match tx_index:
        case 0:
            return self._rollback_tx_0(tx_token)
        case 1:
            return self._rollback_tx_1(tx_token)
    raise AssertionError("unreachable transaction index")
```

Unknown transaction keys raise `KeyError` from the map lookup. The manager
should only call lifecycle participants for transaction keys they are enlisted
in. The final assertion is only a malformed-metadata guard for a map whose
indexes do not match the generated branches; it is not the unknown-key policy.

Key-specific methods are then flat and specialized:

```python
def _prepare_commit_tx_0(self, tx_token):
    if self._y_working_tx_tokens[0] is not tx_token:
        raise StaleLifecycleTransactionToken()
    self._before_commit_tx_0()
    self._validate_commit_tx_0()
    self._prepare_commit_tx_0_fields()
    return self._y_get_default_facade()


def _apply_prepared_commit_tx_0(self, tx_token):
    if self._y_working_tx_tokens[0] is not tx_token:
        raise StaleLifecycleTransactionToken()
    self._apply_prepared_commit_tx_0_fields()
    self._y_working_tx_tokens[0] = None
    return self._y_get_default_facade()


def _rollback_tx_0(self, tx_token):
    self._rollback_tx_0_fields()
    self._y_working_tx_tokens[0] = None
    return self._y_get_default_facade()
```

Hook methods are also key-specific:

```python
def _before_commit_tx_0(self):
    self._y_get_default_facade()._before_default()


def _after_commit_tx_0(self, tx_token):
    self._y_get_default_facade()._after_default()


def _after_rollback_tx_1(self, tx_token):
    self._y_get_default_facade()._after_audit_rollback()
```

Empty hook keys should lower to a small `pass` function, not a missing hole.
The Phase C redundant-pass cleanup preserves a single-statement `pass` function
body, so an intentionally empty generated hook remains valid source.

## Field Commit Functions

Field commit and rollback logic should move out of the dispatcher and into
per-key functions:

Phase F-1 changes the managed-field state layout from two value slots to three
value slots per managed field:

```text
_y_<field>_current  # committed value visible through the current facade
_y_<field>_working  # uncommitted transaction overlay
_y_<field>_staged   # prepared commit value, not visible to facade reads
```

`VOID` marks absence for both `working` and `staged`. Facade reads continue to
look only at `working` and `current`; staged values are an internal
two-phase-commit buffer. Preparation writes staged values, apply moves staged
values to current, and rollback clears both working and staged values.
Generated `__init__` initializes each `_y_<field>_staged` slot to `VOID`
alongside `_y_<field>_working`.

Three-slot storage applies only to managed fields. Plain field storage,
initvar locals, and classvar class-level attributes are unchanged from Phase
A/B.

F-1 also adds managed-field conversion functions using the same authored names
as `pyrolyze.lifecycle`:

```python
count: int = managed(
    default=1,
    freeze=freeze_count,
    thaw=thaw_count,
)
```

`freeze` converts a working value into the prepared/staged value during
`_prepare_commit_tx_N_fields()`. It is the generated equivalent of the old
`pyrolyze.lifecycle` `spec.freeze(next_value)` commit path. If `freeze` raises,
the prepare phase fails, no current value is mutated, and the transaction
manager rolls back working/staged state for every dirty participant.

`thaw` converts a current value into a working overlay when the managed working
facade explicitly asks for a transaction-local value. It is the generated
equivalent of the old `spec.thaw(state.resolve_default_field(name))` getter
path, but F-1 should avoid making the default facade pay an active-transaction
check on every read. Default-facade reads remain cheap resolved-view reads:
working value if present, otherwise current value. Current-facade reads never
thaw. Working-facade reads may thaw and enlist. If `thaw` raises, the read
fails and the field must not publish a working value or staged value.

This means in-place mutation through a thawed managed value should work through
the working facade during an active transaction:

```python
mfoo: tuple[int, ...] = managed(default=(0, 0, 0), thaw=list, freeze=tuple)

with obj.begin():
    obj.working.mfoo[2] = 1
```

The working getter thaws the current tuple to a working list, stores that list
in the working slot, enlists the state object, and returns the same list. The
item assignment mutates the working list. Commit then freezes the list back to
a tuple in the prepare phase. Outside an active transaction, or through the
current facade, the read returns the current tuple and item assignment fails in
normal Python fashion. The default facade also does not auto-thaw; `obj.mfoo`
is a cheap resolved-view read unless a working value already exists.

Nullable conversion should be a matcher-selected lowering shape, not a
user-authored wrapper-function requirement. For example:

```python
mfoo: tuple[int, ...] | None = managed(thaw=list, freeze=tuple, default=None)
```

should lower differently from the non-nullable tuple/list example when the
harvester supplies `HasOptionalNone == True`. The generated code still calls
the authored `thaw` and `freeze` callables directly for non-`None` values, but
it guards the `None` case with a ternary expression in the selected Astichi
resource:

```python
self._y_mfoo_staged = (
    None
    if self._y_mfoo_working is None
    else _Counter_mfoo_freeze(self._y_mfoo_working)
)
```

and:

```python
_mfoo_next = (
    None
    if state._y_mfoo_current is None
    else _Counter_mfoo_thaw(state._y_mfoo_current)
)
```

This keeps authoring simple, avoids synthesizing `{thaw,freeze}_<field>`
wrapper functions, and keeps the conditional as a single expression in the
matcher-selected resource only when the field's facts say the value domain
accepts `None`.

The generated code must stay specialized. YIDL matchers choose the resource
shape from `HasFreeze` and `HasThaw`; generated Python should not contain
runtime `if freeze is not None` or `if thaw is not None` branches.

For a field with `freeze`, the prepare contribution lowers to:

```python
def _prepare_commit_tx_0_fields(self):
    _count_is_set = self._y_count_working is not VOID

    if _count_is_set:
        _count_next = _Counter_count_freeze(self._y_count_working)
        self._y_count_staged = _count_next
```

For a field without `freeze`, the matcher selects the plain prepare
contribution instead:

```python
def _prepare_commit_tx_0_fields(self):
    _count_is_set = self._y_count_working is not VOID

    if _count_is_set:
        self._y_count_staged = self._y_count_working
```

The apply and rollback contributions are the same for both cases:

```python
def _apply_prepared_commit_tx_0_fields(self):
    if self._y_count_staged is not VOID:
        self._y_count_current = self._y_count_staged
        self._y_count_staged = VOID
        self._y_count_working = VOID


def _rollback_tx_0_fields(self):
    self._y_count_staged = VOID
    self._y_count_working = VOID
```

The two-phase local shape is deliberate:

1. compute all next values first
2. mutate current values only after all preparation succeeds

If conversion raises, no current value has been changed. The transaction
manager's failure path can then call rollback and clear working/staged values
without needing to undo a partial current commit.

If a later feature truly needs mutation during commit preparation, that feature
must add an explicit generated undo log or generated old-value locals. Phase
F-1 should avoid that by keeping conversion/preparation side-effect-free.

## Conversion Fact Shape

The marker, harvester, and generated-builder boundary should use the same
property names as the old lifecycle surface: `freeze` and `thaw`.

At the Python marker layer, `managed(...)` accepts:

```python
freeze: Callable[[object], object] | None = None
thaw: Callable[[object], object] | None = None
```

F-1 keeps these call signatures simple: each callable receives exactly one
value. `freeze(working_value)` returns the staged/current value.
`thaw(current_value)` returns the initial working-overlay value. Parameter
injection for conversion functions is out of scope until there is a concrete
need.

At the harvested fact/YIDL data layer, managed field facts should include
conversion presence and builder parameter names. The exact storage casing can
follow the existing YIDL conventions, but the semantic names remain `freeze`
and `thaw`:

```text
HasFreeze
Freeze
FreezeParamName
HasThaw
Thaw
ThawParamName
HasOptionalNone
```

The generated decorator boundary passes callables as unpacked keyword
parameters, matching existing default/default_factory handling:

```python
_Counter_count_freeze=freeze_count
_Counter_count_thaw=thaw_count
```

Generated lifecycle source calls those parameters directly. It should not use a
generic conversion table or `getattr`.

Default facade reads stay cheap even when `thaw` exists:

```python
def _y_get_count_default(self):
    state = self._y_state
    if state._y_count_working is not VOID:
        return state._y_count_working
    return state._y_count_current
```

For a field with `thaw`, the working getter contribution computes the thawed
value before publishing it to the working slot:

```python
def _y_get_count_working(self):
    state = self._y_state
    if state._y_count_working is not VOID:
        return state._y_count_working
    state._y_ensure_enlisted_tx(0)
    _count_next = _Counter_count_thaw(state._y_count_current)
    state._y_count_working = _count_next
    return _count_next
```

For a field without `thaw`, the matcher selects the plain working getter
contribution:

```python
def _y_get_count_working(self):
    state = self._y_state
    if state._y_count_working is not VOID:
        return state._y_count_working
    state._y_ensure_enlisted_tx(0)
    state._y_count_working = state._y_count_current
    return state._y_count_working
```

If `thaw` raises, `_y_count_working` and `_y_count_staged` remain `VOID` and
the current value remains unchanged. The implementation can choose the exact
helper names, but it must preserve that visibility rule.

## Facade Cache Shape

Phase F-1 should also make secondary facade access cheap. The default facade
should maintain hard references to its non-default facades:

```python
class Counter:
    __slots__ = (
        "_y_state",
        "_y_current_facade",
        "_y_working_facade",
        "__weakref__",
    )

    @property
    def current(self):
        current = self._y_current_facade
        if current is None:
            current = Counter_Current._y_new(self._y_state)
            self._y_current_facade = current
            self._y_state._y_current_ref = weakref.ref(current)
        return current

    @property
    def working(self):
        working = self._y_working_facade
        if working is None:
            working = Counter_Working._y_new(self._y_state)
            self._y_working_facade = working
            self._y_state._y_working_ref = weakref.ref(working)
        return working
```

This keeps `obj.working.mfoo[1] = 1` from creating a working facade on every
access. The state object can still hold weakrefs for secondary-to-default and
internal lookup paths, but the default facade owns the hot strong cache.

The secondary-first case must also keep references coherent. If code reaches a
secondary facade before the default facade exists, state lookup may create that
secondary and keep only a weakref. When the default facade is later created,
its `_y_current_facade` and `_y_working_facade` slots should be populated from
any live state weakrefs. Conversely, when the default facade creates a
secondary facade, it must update both its hard reference and the state's weakref
for that secondary.

The ownership rule is:

- default facade has strong cached links to current and working facades
- secondary facades have only `_y_state`
- state has weakrefs for all facade lookup/fallback paths
- state does not become the lifetime owner of secondary facades

## Manager Commit Pipeline

Phase F-1 is allowed to change `yidl.runtime.transaction_yidl`. The generated
state protocol and the transaction manager should move together; do not force
the new two-phase generated shape through the old one-phase
`_commit_transaction(...)` API.

The transaction manager should not fail fast when a participant unexpectedly
raises. It should drain the current phase for all relevant participants, collect
exceptions, run the required cleanup/recovery phase, and then report failures
through a manager-level handler or grouped exception.

The manager-side surface should be concrete, not ad hoc free functions:

```python
manager.commit_order(tx_key) -> list[object]
manager.dirty_contexts(tx_key) -> list[object]
manager.commit_failure(tx_key, tx_token, prepare_failures, rollback_failures)
manager.unexpected_commit_failure(tx_key, tx_token, apply_failures, after_failures)
manager.rollback_failure(tx_key, tx_token, rollback_failures, after_failures)
```

`commit_order(tx_key)` returns participants enlisted with the manager for the
active transaction token, sorted by each participant's
`commit_order_key_for(tx_key)` with registration order as the stable tie-breaker.
`dirty_contexts(tx_key)` returns the participants that the manager believes are
dirty/enlisted for the active transaction key. It should not filter by the
state object's stored token; rollback is deliberately cleanup-oriented and must
be allowed to clear stale local token state. The failure methods raise the
public manager failure for the phase; subclasses can override them to produce
custom diagnostics, logging, or recovery policy.

The phase policy is **drain first, report after**:

- prepare failures prevent current-value mutation, but every participant still
  gets a prepare attempt so the manager can report all broken participants.
- rollback failures do not stop rollback for later participants.
- apply failures are unexpected because apply is generated to be assignment and
  sentinel clearing only; if one still happens, the manager continues applying
  prepared commits for the remaining participants before invoking its
  unexpected-commit handler.
- after hooks are contractually no-raise hooks; if they do raise, the manager
  runs all after hooks and then raises a grouped failure.

The intended commit pipeline is:

```python
def collect_failures(label, contexts, call):
    failures = []
    for context in contexts:
        try:
            call(context)
        except BaseException as exc:
            failures.append((label, context, exc))
    return failures

commit_order = manager.commit_order(tx_key)
dirty_contexts = manager.dirty_contexts(tx_key)

prepare_failures = []
for context in commit_order:
    try:
        context._prepare_commit_tx_by_key(tx_key, tx_token)
    except BaseException as exc:
        prepare_failures.append(exc)

if prepare_failures:
    rollback_failures = collect_failures(
        "rollback",
        dirty_contexts,
        lambda context: context._rollback_tx_by_key(tx_key, tx_token),
    )
    manager.commit_failure(tx_key, tx_token, prepare_failures, rollback_failures)

apply_failures = collect_failures(
    "apply",
    commit_order,
    lambda context: context._apply_prepared_commit_tx_by_key(tx_key, tx_token),
)

after_failures = collect_failures(
    "after_commit",
    commit_order,
    lambda context: context._after_commit_tx_by_key(tx_key, tx_token),
)

if apply_failures or after_failures:
    manager.unexpected_commit_failure(
        tx_key,
        tx_token,
        apply_failures,
        after_failures,
    )
```

The design goal is that `apply_prepared_commit` is generated as ordinary
assignment and sentinel clearing only. It should be exception-free in normal
operation. If it still raises because of a bug or an unexpected runtime
condition, the manager should keep applying prepared commits to the remaining
participants and report the collected failure after the phase drains. This is
not a normal validation path; it is a manager-specific unexpected-commit path
for a broken participant or broken generated code.

After-commit and after-rollback hooks are user extension points. Their contract
should say they must not raise. The runtime still has to be resilient when they
do raise: run every after hook for every relevant participant, collect
exceptions, and raise a grouped or manager-specific failure after all
hooks have been attempted. After-commit hook failures do not undo the commit.
After-rollback hook failures do not undo the rollback cleanup.

Rollback uses the same drain-first policy:

```python
rollback_failures = collect_failures(
    "rollback",
    dirty_contexts,
    lambda context: context._rollback_tx_by_key(tx_key, tx_token),
)
after_rollback_failures = collect_failures(
    "after_rollback",
    dirty_contexts,
    lambda context: context._after_rollback_tx_by_key(tx_key, tx_token),
)
if rollback_failures or after_rollback_failures:
    manager.rollback_failure(
        tx_key,
        tx_token,
        rollback_failures,
        after_rollback_failures,
    )
```

The concrete manager API should have one place to translate collected
unexpected exceptions into the public failure shape. The default implementation
should raise a `BaseExceptionGroup`, or `ExceptionGroup` when every collected
exception is an `Exception` subclass. The important contract is that one broken
participant does not prevent the manager from attempting cleanup, commit apply,
or after hooks for the remaining participants.

## Runtime Rename

Phase F-1 should rename public/generated lifecycle metadata and generated
state internals toward the new vocabulary:

```text
__yidl_tx_index_to_group__ -> __yidl_tx_index_to_key__
__yidl_tx_key_to_index__ -> __yidl_tx_key_to_index__
TxKeysParamName          -> TxKeysParamName
_y_working_tx_ids          -> _y_working_tx_tokens
```

The low-level runtime can keep transitional aliases if needed, but new YIDL
lowering should not introduce new `tx_key` names.

Phase F-1 introduces the new names as canonical and keeps the old generated
metadata aliases in emitted classes:

```python
__yidl_tx_index_to_group__ = __yidl_tx_index_to_key__
__yidl_tx_key_to_index__ = __yidl_tx_key_to_index__
```

The aliases are silent compatibility aliases, not new authored vocabulary.
Tests should be refreshed to prefer the `tx_key` names while still asserting
the old aliases resolve to the same objects. Removing the aliases is outside
Phase F-1 and should be handled by a later explicit deprecation/removal plan if
this surface becomes public enough to matter.

The current `LifecycleTransaction.tx_id` should be treated as a transaction
instance token. A later runtime cleanup can rename it to `tx_token` or
`tx_instance_id`, but that rename is not required before the generated state
protocol switches to key-addressed commit/rollback calls.

## YIDL Fact Changes

The current Phase F method facts contain `TxKeyKey`. Under the new vocabulary
this should become `TxKey`. That is enough for harvest diagnostics but not for
robust generated branching. The lowering layer needs indexed method facts.

Add an indexed method record, either in the managed layer or in a small
transaction-method operation layer that has access to `TxKeys`:

```text
record IndexedTransactionMethod {
    MethodId
    MethodOwner
    MethodName
    MethodKind
    TxKey
    TxIndex
    DeclarationOrder
}

collection IndexedTransactionMethods:
    IndexedTransactionMethod identity MethodId many
```

The operation that builds transaction key/index facts should also join
`TransactionMethods` to `TxKeys` by `(ClassId, TxKey)` and emit
`IndexedTransactionMethods`. This operation may compare runtime key objects
while building facts; generated branch code must only receive the resulting
`TxIndex`.

If a transaction method references a key that is not present in `TxKeys`, the
operation must surface a decorator-time lifecycle diagnostic naming the owning
class, method, and unknown key. It should not silently drop the method or
create a key from the marker alone.

Then the method-kind computed collections should be based on indexed records:

```text
CommitOrderKeyProviders from IndexedTransactionMethods
CommitValidators from IndexedTransactionMethods
BeforeCommitHooks from IndexedTransactionMethods
AfterCommitHooks from IndexedTransactionMethods
AfterRollbackHooks from IndexedTransactionMethods
```

Contributions should bind `TxIndex`, not `TxKey`:

```text
external tx_index_value = TxIndex
```

Generated branch resources then compare integer indexes, not transaction key
objects.

## YIDL Production Shape

Phase F-1 needs more structure than the current single
`commit_transaction_body` and `rollback_transaction_body` holes.

Suggested generated production surfaces:

```text
commit_dispatch_body
rollback_dispatch_body
commit_order_key_dispatch_body
requires_validation_dispatch_body
validate_commit_dispatch_body

before_commit_tx_body
prepare_commit_tx_fields_body
apply_prepared_commit_tx_fields_body
after_commit_tx_body
rollback_tx_fields_body
after_rollback_tx_body
```

The class production should create one indexed key component per `TxKeys`
row:

```text
CommitTxKey[TxIndex]
RollbackTxKey[TxIndex]
CommitOrderKeyTxKey[TxIndex]
ValidationTxKey[TxIndex]
```

Field contributions then target:

```text
/ClassDef/CommitTxKey[TxIndex]/prepare_commit_tx_fields_body
/ClassDef/CommitTxKey[TxIndex]/apply_prepared_commit_tx_fields_body
/ClassDef/RollbackTxKey[TxIndex]/rollback_tx_fields_body
```

Managed conversion contributions are matcher-selected field contributions:

- managed field without `freeze` -> plain prepare contribution
- managed field with `freeze` -> freeze prepare contribution
- managed field with `freeze` and `HasOptionalNone` -> null-aware freeze
  prepare contribution
- default getter -> cheap resolved-view contribution, independent of `thaw`
- working getter without `thaw` -> plain working materialization contribution
- working getter with `thaw` -> thawing working materialization contribution
- working getter with `thaw` and `HasOptionalNone` -> null-aware thawing
  working materialization contribution

This keeps conversion behavior in YIDL matcher space rather than hard-coding it
as a runtime table lookup.

The matcher shape should be explicit:

```text
ManagedPrepareContributions:
  rule with_optional_freeze when HasFreeze == True and HasOptionalNone == True
      -> ManagedOptionalFreezePrepareContribution
  rule with_freeze when HasFreeze == True
      -> ManagedFreezePrepareContribution
  default -> ManagedPlainPrepareContribution

ManagedDefaultGetterContributions:
  default -> ManagedResolvedDefaultGetterContribution

ManagedWorkingGetterContributions:
  rule with_optional_thaw when HasThaw == True and HasOptionalNone == True
      -> ManagedOptionalThawWorkingGetterContribution
  rule with_thaw when HasThaw == True
      -> ManagedThawWorkingGetterContribution
  default -> ManagedPlainWorkingGetterContribution
```

The exact matcher names can follow the implementation's local naming, but the
selection rule is fixed: the presence facts select different Astichi resources;
the emitted Python stays branch-free with respect to conversion availability.

Hook contributions target:

```text
/ClassDef/CommitTxKey[TxIndex]/before_commit_tx_body
/ClassDef/CommitTxKey[TxIndex]/after_commit_tx_body
/ClassDef/RollbackTxKey[TxIndex]/after_rollback_tx_body
```

This keeps field, hook, validator, and dispatch logic independently
overridable by matchers.

## Failure Semantics

The intended failure behavior remains:

| Site | Behavior |
| --- | --- |
| validator raises or returns `False` | manager rolls back working/staged values and re-raises |
| before-commit hook raises | no current values are changed; manager rolls back working/staged values and re-raises |
| conversion/preparation raises | no current values are changed; manager rolls back working/staged values and re-raises |
| field apply raises after preparation | should be structurally impossible in Phase F-1; if it happens, the manager drains apply for remaining participants and reports the collected failure |
| after-commit hook raises | commit remains committed; working values stay cleared; all after-commit hooks are attempted and collected failures are reported |
| after-rollback hook raises | rollback remains complete; working values stay cleared; all after-rollback hooks are attempted and collected failures are reported |
| transaction manager callback raises unexpectedly | manager drains the active phase for remaining participants, invokes the manager-specific unexpected-exception handler, and reports the collected failures |

The important design rule is: all fallible field conversion work happens before
current-value mutation.

Rollback is the recovery path and must be cleanup-oriented. The transaction
manager has at most one active transaction token for a key. Therefore, if a
rollback callback reaches a state object whose stored token does not match the
manager's token, that state object is stale for that transaction index. It
should clear the working data, staged data, and stored token for that index
anyway. Rollback should not preserve working or staged data to protect a
hypothetical newer same-key transaction; the runtime does not allow concurrent
active transactions for one key.

Commit is different. A commit/preparation token mismatch is dangerous because
it could apply stale values to current state. Token mismatch should be detected
in the prepare phase, reported as a prepare failure, and cause the manager to
roll back all dirty participants for the transaction key. The apply phase
should only run after every participant has prepared successfully.

Phase F-1 must leave room for Phase G transient semantics. If transient values
are excluded from staged commit, they participate in working/rollback only. If
transient values later become commit participants, they need either their own
staged slot or a documented exemption from the three-slot managed-field rule.

## Verification

Refresh the Phase F hook goldens and update any affected lifecycle/decorator
goldens so the generated prettier output proves:

- the golden YIDL fixture includes at least two managed fields in the same
  generated class: one with `freeze`/`thaw` and one without either conversion
  function
- no generated branch compares `tx_key` or `tx_key` to `"default_transaction"`
- no generated branch compares against `"audit"` or any other concrete key
  literal
- generated source accepts transaction keys through an unpacked builder
  parameter such as `_Counter_tx_keys`
- generated source accepts managed conversion callables through unpacked
  builder parameters such as `_Counter_count_freeze` and `_Counter_count_thaw`
- default facade slots include hard references for secondary facades, such as
  `_y_current_facade` and `_y_working_facade`
- default facade `.current` and `.working` accessors use the hard-reference
  cache and update state weakrefs when they create a secondary facade
- class metadata maps are derived from the builder-provided key tuple
- concrete generated code uses `DEFAULT_TRANSACTION` only as a symbol/default
  or through metadata maps, not as a string branch predicate
- generated transaction dispatch uses `match tx_index`
- generated managed field state has current, working, and staged value slots
- generated prepare code calls `freeze` directly for fields that define it and
  emits no freeze branch for fields that do not
- generated nullable prepare/getter code is present only for fields where
  `HasOptionalNone` is true
- generated default getter code remains a cheap resolved-view read and does not
  check the transaction manager to auto-thaw
- generated working getter code calls `thaw` directly for fields that define it
  and emits no thaw branch for fields that do not
- generated field commit code is split into `_prepare_commit_tx_N_fields()`
  and `_apply_prepared_commit_tx_N_fields()`
- generated rollback code is split into `_rollback_tx_N_fields()`
- generated hooks are split into `_before_commit_tx_N()`,
  `_after_commit_tx_N()`, and `_after_rollback_tx_N()`
- multi-key begin/commit/rollback behavior remains unchanged

Focused runtime tests should cover:

- `begin(key_a, key_b)` still commits both keys independently
- committing a transaction with no working changes is a no-op
- nested begin counts remain independent per key
- before-commit failure does not mutate current values and rolls back every
  dirty participant
- `freeze` failure does not mutate current values, does not run apply, and
  rolls back working/staged values for every dirty participant
- successful `freeze` stores the converted value in staged state and publishes
  that value on apply
- `.working` access on the default facade reuses the same secondary facade
  instance across repeated reads
- if a secondary facade exists before the default facade is created, default
  facade creation adopts any live secondary facade weakrefs into its hard cache
- `thaw` on a working-facade read during an active transaction materializes a
  working value and enlists the state object
- in-place mutation of a thawed managed value mutates the working overlay and
  commits through `freeze`, for example tuple current -> list working -> tuple
  current
- `thaw` failure does not mutate current, working, or staged values
- nullable conversion behavior is matcher-selected: `HasOptionalNone` lowers
  `thaw=list, freeze=tuple, default=None` to ternary `None` pass-through
  expressions without generating `{thaw,freeze}_<field>` wrapper functions
- default-facade managed reads do not create a working value or enlist the state
  object
- unexpected apply failure drains apply for remaining prepared participants and
  reports a manager-level failure
- after-commit failure leaves current values committed, attempts all after
  hooks, and reports collected failures
- after-rollback failure leaves working values cleared, attempts all after
  rollback hooks, and reports collected failures
- lifecycle materialization time for the Phase F hook fixture is not materially
  worse than the current Phase F baseline

## Roll-Build Candidate

This is a roll-build candidate because each slice can be made green
independently:

1. Add indexed transaction method facts and switch hook/validator predicates
   from `TxKey` literals to `TxIndex`.
2. Add managed `freeze`/`thaw` marker, harvester, and YIDL facts while keeping
   generated behavior unchanged.
3. Change the transaction context protocol from `tx_instance_id + tx_key`
   commit calls to key-addressed commit/rollback calls.
4. Split generated commit/rollback field bodies into per-key helper
   functions.
5. Add default-facade hard-reference caches for secondary facades and keep them
   coherent with state weakrefs.
6. Add staged managed slots and `freeze` prepare/apply lowering.
7. Add `thaw` working getter lowering while keeping default getter reads cheap.
8. Split hook/validator/key generation into per-key helper functions.
9. Refresh Phase F goldens and run the full lifecycle/golden regression scope.

Stop if Phase F-1 requires new YIDL grammar. The intended implementation should
use existing code operations, computed collections, matchers, productions, and
contributions. If `IndexedTransactionMethods` or any other Phase F-1 fact needs
new authored syntax, pause and write a grammar plan before continuing.
