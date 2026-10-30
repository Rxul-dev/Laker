"""Fase 3b: generación de código SQL.

SqlGenerator compone un mixin por instrucción más el de expresiones.
Para agregar una instrucción nueva: crear su mixin en statements/ y sumarlo aquí.
"""

from lark import Transformer, Tree
from lark.exceptions import VisitError

from ..errors import CompileError
from .expressions import ExpressionsMixin
from .formatting import program
from .statements import DropMixin, GetMixin, MakeMixin, PutMixin


class SqlGenerator(MakeMixin, GetMixin, PutMixin, DropMixin, ExpressionsMixin, Transformer):
    """Cada método recibe los hijos ya transformados y devuelve una cadena SQL."""

    def start(self, statements):
        return program(statements)


def generate(tree: Tree) -> str:
    """Traduce un AST (ya validado semánticamente) a SQL."""
    try:
        return SqlGenerator().transform(tree)
    except VisitError as e:
        if isinstance(e.orig_exc, CompileError):
            raise e.orig_exc from None
        raise
