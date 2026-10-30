"""Fase 3a: análisis semántico.

Recorre el AST y valida reglas que la gramática no puede expresar.
No genera código: si termina sin errores, el árbol es válido para el generador.
"""

from lark import Tree, Visitor

from ..errors import CompileError
from .type_system import FieldType, valid_types_hint


class SemanticAnalyzer(Visitor):
    def field(self, tree: Tree):
        _, type_tok = tree.children
        field_type = FieldType.parse(type_tok)
        if not field_type.is_known:
            raise CompileError.at(
                type_tok, f"tipo desconocido '{field_type.raw}' ({valid_types_hint()})"
            )

    def make_stmt(self, tree: Tree):
        table, *fields = tree.children
        seen = set()
        for field in fields:
            name = field.children[0]
            if name in seen:
                raise CompileError.at(
                    name, f"el campo '{name}' está duplicado en la tabla '{table}'"
                )
            seen.add(name)


def analyze(tree: Tree) -> Tree:
    """Valida el árbol; lanza CompileError ante la primera violación."""
    SemanticAnalyzer().visit(tree)
    return tree
