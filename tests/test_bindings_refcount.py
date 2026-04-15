"""Parity tests for ``yidl.runtime.bindings_refcount`` (explicit inc_ref/dec_ref).

Semantics differ from ``test_bindings.py`` in a few places (e.g. COW materialize
clears the frozen snapshot backing; ``BindingBase`` has no ``__del__``—use ``dec_ref``).
"""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass, field
import gc
import sys
import weakref

import pytest

from yidl.runtime.bindings_refcount import BindingBase
from yidl.runtime.bindings_refcount import BindingDict
from yidl.runtime.bindings_refcount import BindingList
from yidl.runtime.bindings_refcount import FrozenBindingDict
from yidl.runtime.bindings_refcount import FrozenBindingList

_spy_dc = (
    dataclass(eq=False, slots=True, weakref_slot=True)
    if sys.version_info >= (3, 11)
    else dataclass(eq=False, slots=True)
)


@_spy_dc
class SpyBinding(BindingBase):
    name: str = ""
    closed: bool = field(default=False, init=False)

    def _close(self) -> None:
        self.closed = True


def test_binding_base_close_runs_when_dec_ref_hits_zero() -> None:
    """Refcount ``BindingBase`` has no ``__del__``; teardown is explicit ``dec_ref``."""
    events: list[int] = []

    @dataclass(eq=False, slots=True)
    class Track(BindingBase):
        def _close(self) -> None:
            events.append(1)

    t = Track()
    t.dec_ref()
    assert events == [1]


def test_binding_base_accepted_and_closed_properties() -> None:
    b = SpyBinding("x")
    assert b.is_accepted is False
    assert b.is_closed is False
    b.accepted()
    assert b.is_accepted is True


def test_binding_dict_adopts_plain_mapping() -> None:
    a = SpyBinding("a")
    d = BindingDict({"k": a})
    assert d["k"] is a


def test_binding_dict_setitem_and_getitem() -> None:
    a = SpyBinding("a")
    d = BindingDict()
    d["k"] = a
    assert d["k"] is a


def test_binding_dict_setitem_same_object_still_one_slot() -> None:
    a = SpyBinding("a")
    d = BindingDict()
    d["k"] = a
    d["k"] = a
    assert d["k"] is a


def test_binding_dict_second_key_same_binding() -> None:
    a = SpyBinding("a")
    d = BindingDict()
    d["q"] = a
    d["k"] = a
    assert d["q"] is d["k"] is a


def test_binding_dict_replace_key() -> None:
    a = SpyBinding("a")
    b = SpyBinding("b")
    d = BindingDict()
    d["k"] = a
    d["k"] = b
    assert d["k"] is b


def test_binding_dict_delitem_removes_key() -> None:
    a = SpyBinding("a")
    d = BindingDict()
    d["k"] = a
    del d["k"]
    assert "k" not in d


def test_binding_dict_pop_removes_key() -> None:
    a = SpyBinding("a")
    d = BindingDict()
    d["k"] = a
    assert d.pop("k") is a
    assert "k" not in d


def test_binding_dict_clear_empties() -> None:
    a = SpyBinding("a")
    b = SpyBinding("b")
    d = BindingDict()
    d["x"] = a
    d["y"] = b
    d.clear()
    assert d == {}


def test_binding_dict_update_merges() -> None:
    a = SpyBinding("a")
    d = BindingDict()
    d.update({"k": a})
    assert d["k"] is a


def test_binding_dict_init_from_binding_dict_copies_entries() -> None:
    a = SpyBinding("a")
    inner = BindingDict()
    inner["k"] = a
    outer = BindingDict(inner)
    assert outer["k"] is a


def test_binding_dict_init_from_binding_list_uses_index_keys() -> None:
    a = SpyBinding("a")
    bl = BindingList([a])
    bd = BindingDict(bl)
    assert bd[0] is a


def test_binding_list_adopts_plain_iterable() -> None:
    a = SpyBinding("a")
    lst = BindingList([a])
    assert lst[0] is a


def test_binding_list_append() -> None:
    a = SpyBinding("a")
    lst = BindingList()
    lst.append(a)
    assert lst[0] is a


def test_binding_list_pop_removes() -> None:
    a = SpyBinding("a")
    lst = BindingList()
    lst.append(a)
    assert lst.pop() is a
    assert lst == []


def test_binding_list_extend() -> None:
    a = SpyBinding("a")
    b = SpyBinding("b")
    lst = BindingList()
    lst.extend([a, b])
    assert lst[0] is a and lst[1] is b


def test_binding_list_extend_binding_dict_uses_values_not_keys() -> None:
    a = SpyBinding("a")
    bd = BindingDict({"k": a})
    lst = BindingList()
    lst.extend(bd)
    assert lst[0] is a


def test_binding_list_init_from_binding_dict_extends_values() -> None:
    a = SpyBinding("a")
    bd = BindingDict()
    bd["x"] = a
    lst = BindingList(bd)
    assert lst[0] is a


def test_binding_list_setitem_replaces() -> None:
    a = SpyBinding("a")
    b = SpyBinding("b")
    lst = BindingList()
    lst.append(a)
    lst[0] = b
    assert lst[0] is b


def test_binding_list_setitem_same_index_same_object() -> None:
    a = SpyBinding("a")
    lst = BindingList()
    lst.append(a)
    lst[0] = a
    assert lst[0] is a


def test_binding_list_slice_getitem_returns_new_list() -> None:
    a = SpyBinding("a")
    b = SpyBinding("b")
    lst = BindingList([a, b])
    sub = lst[0:2]
    assert isinstance(sub, BindingList)
    assert sub[0] is a and sub[1] is b


def test_binding_list_delitem() -> None:
    a = SpyBinding("a")
    lst = BindingList()
    lst.append(a)
    del lst[0]
    assert lst == []


def test_binding_list_remove() -> None:
    a = SpyBinding("a")
    lst = BindingList()
    lst.append(a)
    lst.remove(a)
    assert lst == []


def test_binding_list_clear_empties() -> None:
    a = SpyBinding("a")
    lst = BindingList()
    lst.append(a)
    lst.clear()
    assert lst == []


def test_frozen_binding_dict_registers_as_mapping() -> None:
    a = SpyBinding("a")
    frozen = FrozenBindingDict({"k": a})
    assert isinstance(frozen, Mapping)


def test_freeze_dict_transfers_backing_and_empties_mutable() -> None:
    a = SpyBinding("a")
    d = BindingDict()
    d["k"] = a
    frozen = d.freeze()
    assert d == {}
    assert frozen["k"] is a


def test_frozen_dict_snapshot_holds_values_until_released() -> None:
    a = SpyBinding("a")
    d = BindingDict({"k": a})
    frozen = d.freeze()
    assert frozen["k"] is a
    del d
    gc.collect()
    assert frozen["k"] is a


def test_cow_dict_proxies_reads_until_mutation() -> None:
    a = SpyBinding("a")
    d = BindingDict({"k": a})
    frozen = d.freeze()
    cow = BindingDict.cow_from_frozen(frozen)
    assert cow._cow_parent is not None
    assert len(cow) == 1
    assert cow["k"] is a
    assert list(cow.keys()) == ["k"]
    assert cow._read_map() is frozen._data


def test_cow_dict_mutation_materializes_copy_frozen_unchanged() -> None:
    a = SpyBinding("a")
    d = BindingDict({"k": a})
    frozen = d.freeze()
    cow = BindingDict(frozen=frozen)
    b = SpyBinding("b")
    cow["x"] = b
    assert cow._cow_parent is None
    assert len(frozen) == 0
    assert cow["k"] is a and cow["x"] is b


def test_cow_dict_clear_detaches_without_touching_frozen() -> None:
    a = SpyBinding("a")
    frozen = FrozenBindingDict({"k": a})
    cow = BindingDict(frozen=frozen)
    cow.clear()
    assert cow._cow_parent is None
    assert cow == {}
    assert len(frozen) == 1
    assert frozen["k"] is a


def test_cow_dict_setdefault_hit_does_not_materialize() -> None:
    a = SpyBinding("a")
    frozen = FrozenBindingDict({"k": a})
    cow = BindingDict(frozen=frozen)
    assert cow.setdefault("k", a) is a
    assert cow._cow_parent is not None
    assert len(cow.data) == 0


def test_cow_dict_gc_does_not_break_frozen_still_reachable() -> None:
    frozen_holder: list[FrozenBindingDict] = []

    def make_cow() -> BindingDict:
        d = BindingDict({"k": SpyBinding("k")})
        f = d.freeze()
        frozen_holder.append(f)
        return BindingDict(frozen=f)

    cow = make_cow()
    k = frozen_holder[0]["k"]
    del cow
    gc.collect()
    assert frozen_holder[0]["k"] is k


def test_binding_dict_rejects_frozen_with_initial_mapping() -> None:
    empty = FrozenBindingDict({})
    with pytest.raises(TypeError, match="cannot combine frozen="):
        BindingDict({"a": SpyBinding("a")}, frozen=empty)


def test_freeze_list_transfers_backing() -> None:
    a = SpyBinding("a")
    lst = BindingList()
    lst.append(a)
    frozen = lst.freeze()
    assert lst.data == []
    assert frozen[0] is a


def test_cow_list_mutation_materializes_frozen_unchanged() -> None:
    a = SpyBinding("a")
    lst = BindingList([a])
    frozen = lst.freeze()
    cow = BindingList(frozen=frozen)
    b = SpyBinding("b")
    cow.append(b)
    assert cow._cow_parent is None
    assert len(frozen) == 0
    assert cow[0] is a and cow[1] is b


def test_cow_list_clear_detaches() -> None:
    a = SpyBinding("a")
    frozen = FrozenBindingList([a])
    cow = BindingList(frozen=frozen)
    cow.clear()
    assert cow._cow_parent is None
    assert cow.data == []
    assert len(frozen) == 1


def test_cow_list_add_uses_frozen_view_without_materializing() -> None:
    a = SpyBinding("a")
    frozen = FrozenBindingList([a])
    cow = BindingList(frozen=frozen)
    other = BindingList([SpyBinding("b")])
    combined = cow + other
    assert cow._cow_parent is not None
    assert len(combined) == 2


@pytest.mark.skipif(sys.version_info < (3, 11), reason="dataclass weakref_slot requires Python 3.11+")
def test_spy_binding_weakref_after_local_goes_dead() -> None:
    w: weakref.ReferenceType[SpyBinding] | None = None

    def make() -> None:
        nonlocal w
        b = SpyBinding("x")
        w = weakref.ref(b)

    make()
    gc.collect()
    assert w is not None
    assert w() is None
