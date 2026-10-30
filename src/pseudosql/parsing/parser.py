"""Fase 1-2: análisis léxico + sintáctico -> árbol de sintaxis (AST)."""

from functools import lru_cache

from lark import Lark, Tree
from lark.exceptions import UnexpectedInput

from .diagnostics import to_compile_error

GRAMMAR_FILE = "pseudo.lark"


@lru_cache(maxsize=1)
def get_parser() -> Lark:
    """Construye el parser LALR(1) una sola vez (lexer contextual)."""
    return Lark.open(
        GRAMMAR_FILE,
        rel_to=__file__,
        parser="lalr",
        lexer="contextual",
        propagate_positions=True,
    )


def parse(source: str) -> Tree:
    """Devuelve el árbol de sintaxis (AST) o lanza CompileError."""
    try:
        return get_parser().parse(source)
    except UnexpectedInput as e:
        raise to_compile_error(e) from None
