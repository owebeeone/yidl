"""infra_default_tx — DEFAULT group transaction path (see dev-docs/history/IMPL_PROGRESS.md)."""

from __future__ import annotations

import pytest

from tests.baseline._impl_switch import get_backend, get_lifecycle_module


def test_parity_backend_env():
    b = get_backend()
    assert b in ("lifecycle", "handcrafted", "generated")


@pytest.mark.usefixtures("require_lifecycle_importable")
def test_lifecycle_default_transaction_commit():
    if get_backend() != "lifecycle":
        pytest.skip("handcrafted Counter not implemented yet")

    lc = get_lifecycle_module()
    managed = lc.managed
    managed_context = lc.managed_context
    TransactionManager = lc.TransactionManager

    @managed_context
    class Counter:
        value: int = managed(default=0)

    txm = TransactionManager()
    ctx = Counter(transaction_manager=txm)
    with txm.begin():
        ctx.value = 1
    assert ctx.value == 1


def test_handcrafted_backend_skipped_until_sample_exists():
    if get_backend() != "handcrafted":
        pytest.skip("only runs for LC_PARITY_IMPL=handcrafted")
    pytest.skip("implement Counter in yidl.handcrafted.lifecycle_sample first")


def test_generated_backend_skipped_until_generated_path_exists():
    if get_backend() != "generated":
        pytest.skip("only runs for LC_PARITY_IMPL=generated")
    pytest.skip("implement Counter in the YIDL compiler/generated path first")
