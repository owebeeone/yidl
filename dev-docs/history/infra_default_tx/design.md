# infra_default_tx

## Goal

Establish that parity tests can load **`pyrolyze.lifecycle`** without importing **`pyrolyze.api`** (Python 3.10–safe stub in `tests/baseline/_impl_switch.py`), and that the **default transaction key** commit path works end-to-end for a trivial `managed` field.

## Support code

- **`tests/baseline/_impl_switch.py`**: stub `pyrolyze` package, load `type_annotations` then `lifecycle`.
- **`TransactionManager.begin()` context manager**: validates, applies commits on normal exit (`GroupTransactionManager.commit`).

## YIDL mapping

Global **stores** / **surfaces** in `spec/lifecycle_baseline.yidl` are the shell; **managed** transducer text lands with `managed_single_group`. This slice only needs runtime + reference test.

## Hand-crafted

No handcrafted `Counter` yet — `lifecycle_sample.py` stays minimal until the handcrafted path is implemented.

## Exit criteria

- [x] Loader works when `pyrolyze` checkout is sibling to `yidl` under the monorepo root (path `parents[3]` from this test file).
- [x] `test_lifecycle_default_transaction_commit` passes with `LC_PARITY_IMPL=lifecycle` (default).
