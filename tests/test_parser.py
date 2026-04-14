"""Tests for yidl.parser."""

from pathlib import Path

from yidl.lexer import lex_yidl
from yidl.parser import (
    BehaviorNode,
    InputNode,
    StoreNode,
    SurfaceNode,
    TransducerNode,
    YIDLParser,
)

_DATA_YIDL = Path(__file__).resolve().parent / "data" / "yidl"


def _parse(src: str):
    return YIDLParser(list(lex_yidl(src))).parse()


def test_parse_store_and_surface():
    src = """
store PublishedStore : type=Slotted, location="self._p"
surface Current : phase=execution
"""
    ast = _parse(src)
    assert len(ast.stores) == 1
    assert ast.stores[0] == StoreNode(
        "PublishedStore", {"type": "Slotted", "location": "self._p"}
    )
    assert len(ast.surfaces) == 1
    assert ast.surfaces[0] == SurfaceNode("Current", {"phase": "execution"})


def test_parse_transducer_inputs_and_behavior():
    src = """
transducer ManagedField: fieldhelper=managed
    inputs:
        name: @id
        annotation: @type
        default: ?@object(Any) = None
    behavior Init:
        store = PublishedStore
        get: native
"""
    ast = _parse(src)
    assert len(ast.transducers) == 1
    t: TransducerNode = ast.transducers[0]
    assert t.name == "ManagedField"
    assert t.options["fieldhelper"] == "managed"
    assert t.inputs[0] == InputNode("name", "@id", None)
    assert t.inputs[2].name == "default"
    assert t.inputs[2].default_expr == "None"
    assert len(t.behaviors) == 1
    b: BehaviorNode = t.behaviors[0]
    assert b.names == ["Init"]
    assert b.properties["store"] == "PublishedStore"


def test_parse_minimal_round_trip_counts():
    src = """
store S : a=1
surface X : p=q
transducer T: h=1
    inputs:
        n: @id
    behavior B:
        get: %% pass
"""
    ast = _parse(src)
    assert len(ast.stores) == 1
    assert len(ast.surfaces) == 1
    assert len(ast.transducers) == 1
    assert ast.transducers[0].inputs[0].name == "n"


def test_parse_example_yidl_fixture():
    path = _DATA_YIDL / "example.yidl"
    source = path.read_text(encoding="utf-8")
    ast = _parse(source)
    assert len(ast.stores) == 4
    assert [s.name for s in ast.stores] == [
        "PublishedStore",
        "WorkingStore",
        "InstanceStore",
        "HiddenStore",
    ]
    assert len(ast.surfaces) == 7
    assert len(ast.transducers) == 10
    names = [t.name for t in ast.transducers]
    assert names[0] == "ManagedField"
    assert names[-1] == "CommitOrderKeyMeta"
    managed = ast.transducers[0]
    assert isinstance(managed, TransducerNode)
    assert len(managed.behaviors) >= 1
    assert any("Init" in b.names for b in managed.behaviors)
