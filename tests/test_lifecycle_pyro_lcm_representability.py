from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from yidl.runtime.lifecycle import const
from yidl.runtime.lifecycle import initvar
from yidl.runtime.lifecycle import lifecycle
from yidl.runtime.lifecycle import local_store
from yidl.runtime.lifecycle import managed
from yidl.runtime.lifecycle import transient
from yidl.runtime.transaction_yidl import TransactionManager

PASS_TX_KEY = "context_pass"


@dataclass(frozen=True, slots=True)
class DummyOwner:
    context_kind: str = "slot"


@dataclass(frozen=True, slots=True)
class FrozenComponentCallInvocationState:
    runtime_func: object | None = None


class CallSiteContextManager:
    def __init__(self) -> None:
        self.current: dict[object, object] = {}


def _resolve_render_context_state_mgr_initvar(
    cls: type[object],
    render_context_state_mgr: object | None,
    render_context: object | None,
) -> object | None:
    del cls
    if render_context_state_mgr is not None:
        return render_context_state_mgr
    if render_context is not None and hasattr(render_context, "_state_mgr"):
        return render_context._state_mgr
    return None


def _default_generation_tracker_key(self: object) -> str:
    return f"{type(self.owner).__name__}:generation"


def _default_context_kind(self: object) -> str:
    return getattr(self.owner, "context_kind", "slot")


def _bootstrap_transaction_manager(self: object) -> object:
    return self._y_get_transaction_manager()


@lifecycle
class LcmStateMgrBase:
    owner: object = const()


@lifecycle
class LcmContextBaseStateMgr(LcmStateMgrBase):
    render_context_state_mgr: object | None = initvar(default=None)
    render_context: object | None = initvar(default=None)
    _resolved_render_context_state_mgr: object | None = initvar(
        init=False,
        default_factory=_resolve_render_context_state_mgr_initvar,
    )
    _generation_tracker_key: str = const(
        default_factory=_default_generation_tracker_key,
        allow_self_factory=True,
    )
    _context_kind: str = const(
        default_factory=_default_context_kind,
        allow_self_factory=True,
    )
    _transaction_manager_bootstrap: object = const(
        default_factory=_bootstrap_transaction_manager,
        allow_self_factory=True,
    )
    children_state: dict[object, object] = managed(
        default_factory=dict,
        compare="identity",
        tx_key=PASS_TX_KEY,
    )
    ui_state: tuple[object, ...] = managed(default_factory=tuple, tx_key=PASS_TX_KEY)


@lifecycle
class LcmSlotExprSlotContextStateMgr(LcmContextBaseStateMgr):
    _call_site_context_manager: CallSiteContextManager = local_store(
        default_factory=CallSiteContextManager,
    )
    _runtime_locals_by_slot_id: dict[object, dict[str, object]] = local_store(
        default_factory=dict,
    )
    _staged_call_site_ids: tuple[object, ...] = transient(
        default_factory=tuple,
        tx_key=PASS_TX_KEY,
    )
    _staged_post_commit_callbacks: tuple[object, ...] = transient(
        default_factory=tuple,
        tx_key=PASS_TX_KEY,
    )


@lifecycle
class LcmComponentCallSlotContextStateMgr(LcmContextBaseStateMgr):
    _call_state: FrozenComponentCallInvocationState = managed(
        default_factory=FrozenComponentCallInvocationState,
        init=False,
        tx_key=PASS_TX_KEY,
    )


def test_pyro_lcm_field_shapes_are_representable() -> None:
    owner = DummyOwner(context_kind="component")
    manager = TransactionManager(tx_keys={PASS_TX_KEY})

    context = LcmContextBaseStateMgr(owner=owner, transaction_manager=manager)

    assert context.owner is owner
    assert context._generation_tracker_key == "DummyOwner:generation"
    assert context._context_kind == "component"
    assert context._transaction_manager_bootstrap is manager
    assert PASS_TX_KEY in context.__yidl_tx_key_to_index__

    child = object()
    with context.begin(PASS_TX_KEY):
        context.children_state = {"slot": child}
    assert context.current.children_state == {"slot": child}

    slot_expr = LcmSlotExprSlotContextStateMgr(
        owner=owner,
        transaction_manager=TransactionManager(tx_keys={PASS_TX_KEY}),
    )
    slot_expr._runtime_locals_by_slot_id["slot"] = {"value": 1}
    try:
        with slot_expr.begin(PASS_TX_KEY):
            slot_expr._runtime_locals_by_slot_id["slot"]["value"] = 2
            assert slot_expr._staged_call_site_ids == ()
            slot_expr._staged_call_site_ids = ("slot",)
            raise RuntimeError("rollback")
    except RuntimeError:
        pass
    assert slot_expr._runtime_locals_by_slot_id["slot"] == {"value": 2}

    component = LcmComponentCallSlotContextStateMgr(
        owner=owner,
        transaction_manager=TransactionManager(tx_keys={PASS_TX_KEY}),
    )
    assert component.current._call_state == FrozenComponentCallInvocationState()
    next_state = FrozenComponentCallInvocationState(runtime_func=object())
    with component.begin(PASS_TX_KEY):
        component._call_state = next_state
    assert component.current._call_state is next_state
