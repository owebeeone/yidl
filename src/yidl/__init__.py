"""YIDL — declarative specification language for AOT lifecycle / transducer codegen."""

__version__ = "0.1.0"

from yidl.lexer import Token, lex_yidl
from yidl.parser import AST, YIDLParser
from yidl.runtime import DEFAULT_TRANSACTION
from yidl.runtime import TransactionManager

__all__ = [
    "__version__",
    "AST",
    "DEFAULT_TRANSACTION",
    "Token",
    "TransactionManager",
    "YIDLParser",
    "lex_yidl",
]
