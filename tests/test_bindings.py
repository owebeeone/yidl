from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass, field
import gc

import pytest

from yidl.runtime.bindings import BindingBase
from yidl.runtime.bindings import BindingDict
from yidl.runtime.bindings import BindingList
from yidl.runtime.bindings import FrozenBindingDict
from yidl.runtime.bindings import FrozenBindingList


@dataclass(eq=False, slots=True)
class SpyBinding(BindingBase):
    name: str = ""
    closed: bool = field(default=False, init=False)

    def _close(self) -> None:
        self.closed = True


def test_binding_base_inc_ref_rejects_closed() -> None:
    b = SpyBinding("x")
    b.dec_ref()
    assert b.is_closed is True
    with pytest.raises(RuntimeError, match="cannot retain a closed binding"):
        b.inc_ref()


def test_binding_base_dec_ref_without_inc_raises() -> None:
    b = SpyBinding("x")
    b.dec_ref()
    with pytest.raises(AssertionError, match="dec_ref called without a matching inc_ref"):
        b.dec_ref()


def test_binding_dict_adopts_plain_mapping_without_changing_refcount() -> None:
    a = SpyBinding("a")
    assert a.ref_count == 1
    d = BindingDict({"k": a})
    assert a.ref_count == 1
    assert d["k"] is a


def test_binding_dict_setitem_new_key_increments_refcount() -> None:
    a = SpyBinding("a")
    d = BindingDict()
    d["k"] = a
    assert a.ref_count == 2


def test_binding_dict_setitem_same_object_is_noop_for_refcount() -> None:
    a = SpyBinding("a")
    d = BindingDict()
    d["k"] = a
    assert a.ref_count == 2
    d["k"] = a
    assert a.ref_count == 2


def test_binding_dict_second_key_same_binding_increments_refcount() -> None:
    a = SpyBinding("a")
    d = BindingDict()
    d["q"] = a
    d["k"] = a
    assert a.ref_count == 3


def test_binding_dict_replace_key_transfers_retention() -> None:
    a = SpyBinding("a")
    b = SpyBinding("b")
    d = BindingDict()
    d["k"] = a
    d["k"] = b
    assert a.ref_count == 1
    assert b.ref_count == 2


def test_binding_dict_delitem_decrements_refcount() -> None:
    a = SpyBinding("a")
    d = BindingDict()
    d["k"] = a
    assert a.ref_count == 2
    del d["k"]
    assert a.ref_count == 1


def test_binding_dict_pop_decrements_refcount() -> None:
    a = SpyBinding("a")
    d = BindingDict()
    d["k"] = a
    assert a.ref_count == 2
    assert d.pop("k") is a
    assert a.ref_count == 1


def test_binding_dict_clear_releases_all_slots() -> None:
    a = SpyBinding("a")
    b = SpyBinding("b")
    d = BindingDict()
    d["x"] = a
    d["y"] = b
    assert a.ref_count == 2 and b.ref_count == 2
    d.clear()
    assert a.ref_count == 1 and b.ref_count == 1
    assert d == {}


def test_binding_dict_clear_on_adopted_only_holder_closes() -> None:
    a = SpyBinding("a")
    d = BindingDict({"k": a})
    assert a.ref_count == 1
    d.clear()
    assert a.ref_count == 0
    assert a.closed is True


def test_binding_dict_update_uses_setitem_semantics() -> None:
    a = SpyBinding("a")
    d = BindingDict()
    d.update({"k": a})
    assert a.ref_count == 2


def test_binding_dict_init_from_binding_dict_shares_with_inc_ref() -> None:
    a = SpyBinding("a")
    inner = BindingDict()
    inner["k"] = a
    assert a.ref_count == 2
    outer = BindingDict(inner)
    assert a.ref_count == 3
    assert outer["k"] is a


def test_binding_dict_init_from_binding_list_uses_index_keys() -> None:
    a = SpyBinding("a")
    bl = BindingList([a])
    assert a.ref_count == 1
    bd = BindingDict(bl)
    assert bd[0] is a
    assert a.ref_count == 2


def test_binding_list_adopts_plain_iterable_without_changing_refcount() -> None:
    a = SpyBinding("a")
    lst = BindingList([a])
    assert a.ref_count == 1
    assert lst[0] is a


def test_binding_list_append_increments_refcount() -> None:
    a = SpyBinding("a")
    lst = BindingList()
    lst.append(a)
    assert a.ref_count == 2


def test_binding_list_pop_decrements_refcount() -> None:
    a = SpyBinding("a")
    lst = BindingList()
    lst.append(a)
    assert a.ref_count == 2
    assert lst.pop() is a
    assert a.ref_count == 1
    assert lst == []


def test_binding_list_extend_increments_each_item() -> None:
    a = SpyBinding("a")
    b = SpyBinding("b")
    lst = BindingList()
    lst.extend([a, b])
    assert a.ref_count == 2 and b.ref_count == 2


def test_binding_list_extend_binding_dict_uses_values_not_keys() -> None:
    a = SpyBinding("a")
    bd = BindingDict({"k": a})
    assert a.ref_count == 1
    lst = BindingList()
    lst.extend(bd)
    assert lst[0] is a
    assert a.ref_count == 2


def test_binding_list_init_from_binding_dict_extends_values() -> None:
    a = SpyBinding("a")
    bd = BindingDict()
    bd["x"] = a
    assert a.ref_count == 2
    lst = BindingList(bd)
    assert lst[0] is a
    assert a.ref_count == 3


def test_binding_list_setitem_replaces_with_ref_transfer() -> None:
    a = SpyBinding("a")
    b = SpyBinding("b")
    lst = BindingList()
    lst.append(a)
    lst[0] = b
    assert a.ref_count == 1
    assert b.ref_count == 2


def test_binding_list_setitem_same_index_same_object_noop() -> None:
    a = SpyBinding("a")
    lst = BindingList()
    lst.append(a)
    assert a.ref_count == 2
    lst[0] = a
    assert a.ref_count == 2


def test_binding_list_slice_assignment_updates_refs() -> None:
    a = SpyBinding("a")
    b = SpyBinding("b")
    c = SpyBinding("c")
    lst = BindingList([a, b])
    assert a.ref_count == 1 and b.ref_count == 1 and c.ref_count == 1
    lst[0:2] = [c]
    assert a.is_closed and b.is_closed
    assert c.ref_count == 2
    assert list(lst) == [c]


def test_binding_list_delitem_decrements() -> None:
    a = SpyBinding("a")
    lst = BindingList()
    lst.append(a)
    del lst[0]
    assert a.ref_count == 1


def test_binding_list_remove_decrements() -> None:
    a = SpyBinding("a")
    lst = BindingList()
    lst.append(a)
    lst.remove(a)
    assert a.ref_count == 1


def test_binding_list_clear_releases_slots() -> None:
    a = SpyBinding("a")
    lst = BindingList()
    lst.append(a)
    lst.clear()
    assert a.ref_count == 1


def test_frozen_binding_dict_registers_as_mapping() -> None:
    a = SpyBinding("a")
    frozen = FrozenBindingDict({"k": a})
    assert isinstance(frozen, Mapping)


def test_freeze_dict_transfers_backing_and_empties_mutable() -> None:
    a = SpyBinding("a")
    d = BindingDict()
    d["k"] = a
    assert a.ref_count == 2
    frozen = d.freeze()
    assert d == {}
    assert frozen["k"] is a
    assert a.ref_count == 2


def test_frozen_dict_close_releases_snapshot_values() -> None:
    a = SpyBinding("a")
    d = BindingDict({"k": a})
    assert a.ref_count == 1
    frozen = d.freeze()
    assert a.ref_count == 1
    frozen.dec_ref()
    assert a.ref_count == 0
    assert a.closed is True


def test_cow_dict_proxies_reads_until_mutation() -> None:
    a = SpyBinding("a")
    d = BindingDict({"k": a})
    frozen = d.freeze()
    cow = BindingDict.cow_from_frozen(frozen)
    assert cow._cow_parent is not None
    assert len(cow) == 1
    assert cow["k"] is a
    assert list(cow.keys()) == ["k"]
    assert frozen.ref_count == 2


def test_cow_dict_mutation_moves_entries_off_frozen_snapshot() -> None:
    a = SpyBinding("a")
    d = BindingDict({"k": a})
    frozen = d.freeze()
    cow = BindingDict(frozen=frozen)
    assert frozen.ref_count == 2
    b = SpyBinding("b")
    cow["x"] = b
    assert cow._cow_parent is None
    assert len(frozen) == 0
    assert cow["k"] is a and cow["x"] is b
    assert a.ref_count == 1
    assert b.ref_count == 2


def test_cow_dict_clear_detaches_without_copying_snapshot() -> None:
    a = SpyBinding("a")
    frozen = FrozenBindingDict({"k": a})
    assert a.ref_count == 1
    cow = BindingDict(frozen=frozen)
    assert frozen.ref_count == 2
    cow.clear()
    assert cow._cow_parent is None
    assert frozen.ref_count == 1
    assert len(frozen) == 1
    assert cow == {}


def test_cow_dict_setdefault_hit_does_not_materialize() -> None:
    a = SpyBinding("a")
    frozen = FrozenBindingDict({"k": a})
    cow = BindingDict(frozen=frozen)
    assert cow.setdefault("k", a) is a
    assert cow._cow_parent is not None
    assert len(cow.data) == 0


def test_cow_dict_gc_drops_retained_frozen_ref() -> None:
    frozen_holder: list[FrozenBindingDict] = []

    def make_cow() -> BindingDict:
        d = BindingDict({"k": SpyBinding("k")})
        f = d.freeze()
        frozen_holder.append(f)
        return BindingDict(frozen=f)

    cow = make_cow()
    assert frozen_holder[0].ref_count == 2
    del cow
    gc.collect()
    assert frozen_holder[0].ref_count == 1


def test_binding_dict_rejects_frozen_with_initial_mapping() -> None:
    empty = FrozenBindingDict({})
    with pytest.raises(TypeError, match="cannot combine frozen="):
        BindingDict({"a": SpyBinding("a")}, frozen=empty)


def test_freeze_list_transfers_backing() -> None:
    a = SpyBinding("a")
    lst = BindingList()
    lst.append(a)
    assert a.ref_count == 2
    frozen = lst.freeze()
    assert lst.data == []
    assert frozen[0] is a
    assert a.ref_count == 2


def test_cow_list_mutation_moves_off_frozen() -> None:
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
    assert frozen.ref_count == 2
    cow.clear()
    assert frozen.ref_count == 1
    assert len(frozen) == 1
    assert cow.data == []


def test_cow_list_add_uses_frozen_view_without_materializing() -> None:
    a = SpyBinding("a")
    frozen = FrozenBindingList([a])
    cow = BindingList(frozen=frozen)
    other = BindingList([SpyBinding("b")])
    combined = cow + other
    assert cow._cow_parent is not None
    assert len(combined) == 2
