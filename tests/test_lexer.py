"""Tests for yidl.lexer."""

from yidl.lexer import Token, lex_yidl


def test_lex_yidl_skips_blank_and_comment_only_lines():
    src = """
# full-line comment

store Foo : a=1
"""
    tokens = list(lex_yidl(src))
    assert len(tokens) == 1
    assert tokens[0] == Token("STATEMENT", "store Foo : a=1", 0, 4)


def test_lex_yidl_code_snippet_fence():
    src = """
transducer T: fieldhelper=t
    behavior B:
        get: %%
            x = 1
            y = 2
    behavior Next:
        get: native
"""
    tokens = list(lex_yidl(src))
    kinds = [t.type for t in tokens]
    assert "CODE_SNIPPET" in kinds
    snippet = next(t for t in tokens if t.type == "CODE_SNIPPET")
    assert "x = 1" in snippet.value
    assert "y = 2" in snippet.value


def test_lex_yidl_inline_after_fence():
    src = "behavior X:\n    get: %% return 1\n"
    tokens = list(lex_yidl(src))
    code = [t for t in tokens if t.type == "CODE_SNIPPET"]
    assert len(code) == 1
    assert code[0].value == "return 1"
