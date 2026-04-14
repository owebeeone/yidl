"""Tests for yidl.ast_tx."""

import ast

from yidl.ast_tx import YIDLTransformer


def test_transformer_read_call_becomes_attribute_load():
    tree = ast.parse("store.read()")
    tx = YIDLTransformer("myfield", {"store": "self._working"})
    out = tx.visit(tree)
    assert isinstance(out, ast.Module)
    expr = out.body[0]
    assert isinstance(expr, ast.Expr)
    # read() -> self._working.myfield (Load)
    val = expr.value
    assert isinstance(val, ast.Attribute)
    assert val.attr == "myfield"
    assert isinstance(val.value, ast.Attribute)
    assert val.value.attr == "_working"


def test_transformer_has_call_becomes_is_not_missing():
    tree = ast.parse("store.has()")
    tx = YIDLTransformer("f", {"store": "self._pub"})
    out = tx.visit(tree)
    expr = out.body[0]
    cmp = expr.value
    assert isinstance(cmp, ast.Compare)
    assert isinstance(cmp.ops[0], ast.IsNot)
    assert isinstance(cmp.comparators[0], ast.Name)
    assert cmp.comparators[0].id == "MISSING"


def test_transformer_write_in_expr_to_assign():
    tree = ast.parse("store.write(42)")
    tx = YIDLTransformer("x", {"store": "self._w"})
    out = tx.visit(tree)
    stmt = out.body[0]
    assert isinstance(stmt, ast.Assign)
    assert isinstance(stmt.targets[0], ast.Attribute)
    assert stmt.targets[0].attr == "x"
