"""YIDL — declarative specification language for AOT lifecycle / transducer codegen."""

__version__ = "0.1.0"

from yidl.lexer import Token, lex_yidl
from yidl.parser import AST, YIDLParser

__all__ = [
    "__version__",
    "AST",
    "Token",
    "YIDLParser",
    "lex_yidl",
]
