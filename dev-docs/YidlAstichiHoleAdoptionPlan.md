# YIDL Astichi Hole Adoption Plan

## Purpose

Astichi now supports two source-level composition forms that YIDL can use
immediately:

- defaulted block holes:

  ```python
  with astichi_hole(name) as astichi_fallback:
      ...
  ```

- additive `elif` clause targets:

  ```python
  elif astichi_elif(name):
      pass
  ```

This plan is the YIDL-specific adoption layer. It is separate from the broader
production-phase merge plan. The goal here is to simplify YIDL-authored Astichi
resources and generated source before changing YIDL grammar.

This plan should not add new YIDL syntax. It updates YIDL templates/resources
to use current Astichi features.

## Current Astichi Syntax

### Defaulted block holes

Use this for a statement block that has a real fallback:

```python
def _commit_order_key_tx_0(self):
    with astichi_hole(commit_order_key_tx_body) as astichi_fallback:
        return ()
```

Semantics:

- if no contribution targets `commit_order_key_tx_body`, materialization emits
  `return ()`
- if one or more contributions target `commit_order_key_tx_body`, Astichi emits
  those contributions and discards the fallback suite
- `astichi_fallback` is a required sentinel, not a runtime variable
- `astichi_pyimport(...)` is not valid inside the fallback suite

This should replace the current pattern:

```python
def _commit_order_key_tx_0(self):
    astichi_hole(commit_order_key_tx_body)
    return ()
```

which can generate two returns when a contribution also returns.

### Additive elif targets

Use this for generated branch lists inside an existing `if` / `elif` chain:

```python
def _prepare_commit_for_index(self, tx_index):
    if False:
        pass
    elif astichi_elif(tx_branches):
        pass
    else:
        raise KeyError(tx_index)
```

Each branch contribution is an Astichi snippet rooted at exactly one
`def astichi_elif():` function:

```python
def astichi_elif():
    astichi_import(tx_index)
    astichi_import(self)

    if tx_index == astichi_bind_external(tx_index_value):
        self.astichi_ref(external=prepare_commit_fields_function_name)()
```

Materialized output becomes ordinary Python:

```python
def _prepare_commit_for_index(self, tx_index):
    if False:
        pass
    elif tx_index == 0:
        self._prepare_commit_tx_0_fields()
    elif tx_index == 1:
        self._prepare_commit_tx_1_fields()
    else:
        raise KeyError(tx_index)
```

Astichi `elif` targets are mandatory. YIDL should use them where the input facts
guarantee at least one branch, such as `TxGroups` for lifecycle classes. For
optional branch sets, use a defaulted block hole or keep an ordinary block hole
until the fact model guarantees a branch.

## Lifecycle Simplification Targets

### Function-body fallbacks

Use defaulted block holes for generated functions that currently combine a hole
with a fallback statement:

```python
resource CommitOrderKeyFunction = template $[
    def commit_order_key_function_name__astichi_arg__(self):
        with astichi_hole(commit_order_key_tx_body) as astichi_fallback:
            return ()
]$
```

```python
resource RequiresValidationFunction = template $[
    def requires_validation_function_name__astichi_arg__(self):
        with astichi_hole(requires_validation_tx_body) as astichi_fallback:
            return False
]$
```

```python
resource ValidateCommitFunction = template $[
    def validate_commit_function_name__astichi_arg__(self):
        with astichi_hole(validate_commit_tx_body) as astichi_fallback:
            return True
]$
```

```python
resource BeforeCommitFunction = template $[
    def before_commit_function_name__astichi_arg__(self):
        with astichi_hole(before_commit_tx_body) as astichi_fallback:
            pass
]$
```

The same pattern applies to after-commit, after-rollback, per-transaction field
helper bodies, and any other block whose no-contribution behavior is an explicit
fallback.

### Dispatch chains

Use `astichi_elif` for transaction-index dispatch. This replaces repeated
`match` or guarded branch snippets when the branch list is additive and ordered
from data.

Target resource:

```python
resource PrepareCommitDispatchFunction = template $[
    def _prepare_commit_for_index(self, tx_index):
        if False:
            pass
        elif astichi_elif(prepare_commit_dispatch_branches):
            pass
        else:
            raise KeyError(tx_index)
]$
```

Branch contribution resource:

```python
resource PrepareCommitDispatchBranch = template $[
    def astichi_elif():
        astichi_import(tx_index)
        astichi_import(self)

        if tx_index == astichi_bind_external(tx_index_value):
            self.astichi_ref(external=prepare_commit_fields_function_name)()
]$
```

This should be considered for:

- commit-order-key dispatch
- requires-validation dispatch
- validate-commit dispatch
- before-commit hook dispatch
- after-commit hook dispatch
- after-rollback hook dispatch
- prepare/apply/rollback field dispatch

### Placeholder pass contributions

Once defaulted block holes are used, YIDL should remove pass-only resources and
matchers that exist solely to keep Python blocks non-empty.

Do not remove semantic pass resources where the `pass` itself is selected
behavior. The target is only pass placeholders for empty block validity.

## Implementation Slices

### A1: Defaulted Function Fallbacks

Update lifecycle function resources from:

```python
astichi_hole(body)
return fallback
```

to:

```python
with astichi_hole(body) as astichi_fallback:
    return fallback
```

Deliverables:

- no generated double-return patterns such as `return helper(); return ()`
- no generated orphan fallback after a selected contribution
- goldens updated for lifecycle transactional fixtures

Focused verification:

```bash
PYTHONPATH=../astichi/src uv run --with pytest --with black pytest tests/test_yidl_goldens.py -q
```

### A2: Empty Body Fallbacks

Update resources whose empty behavior is `pass`:

```python
def _rollback_tx_0_fields(self):
    with astichi_hole(rollback_fields_body) as astichi_fallback:
        pass
```

Deliverables:

- remove pass placeholder contributions for these holes
- generated source contains `pass` only when the hole is genuinely unfilled
- filled holes do not retain pass statements

### A3: Elif Dispatch Targets

Refactor transaction dispatch helpers to use `astichi_elif` clause targets.

Deliverables:

- branch target resources use `elif astichi_elif(name): pass`
- branch contributions use `def astichi_elif(): if condition: body`
- generated output contains ordinary `elif tx_index == ...` chains
- unknown index behavior remains explicit through an `else` branch

Focused tests:

- one transaction key
- two transaction keys
- hook dispatch and field dispatch both materialize correctly
- generated prettier output has no `match tx_index` branch list where an
  `astichi_elif` target is expected

### A4: Cleanup And LOC Measurement

Remove now-unused pass resources, pass matchers, and duplicate fallback
patterns.

Deliverables:

- record LOC before and after for lifecycle YIDL
- update `YidlBetterMergeProposals.md` estimates if the measured reduction is
  materially different from the current estimate
- leave production phases untouched in this plan

## Measured Impact

Measured after applying the hole-adoption slice:

| File | Before LOC | After LOC | Delta |
| --- | ---: |
| `tests/data/yidl/yidl_transactional_lifecycle/lifecycle_core.yidl` | 1477 | 1363 | -114 |
| `tests/data/yidl/yidl_transactional_lifecycle/lifecycle_managed.yidl` | 1430 | 1313 | -117 |
| `tests/data/yidl/yidl_transactional_lifecycle/lifecycle_base.yidl` | 589 | 514 | -75 |
| Touched lifecycle YIDL subtotal | 3496 | 3190 | -306 |
| Full transactional lifecycle YIDL total | 6015 | 5709 | -306 |

This is roughly a 5.1% full transactional lifecycle YIDL reduction before
production phases. The generated source also drops placeholder pass/double
fallback noise in the lifecycle goldens.

The larger mergeability improvement still requires production phases and
`extend production`. This plan is a simplification pass that makes that later
refactor less noisy.

## Relationship To Better Merge

This plan should run before or alongside the early production-phase work:

1. Adopt Astichi defaulted block holes and `astichi_elif` targets in lifecycle
   resources.
2. Then implement YIDL production phases and production extensions.
3. Then move managed/transient/owned/binding apply edges out of
   `lifecycle_base.yidl`.

Keeping this separate avoids mixing two concerns:

- Astichi resource-source cleanup
- YIDL grammar and concept-merge changes
