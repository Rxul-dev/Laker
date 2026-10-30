"""MAKE <tabla> (<campo> <tipo>, ...)  ->  CREATE TABLE"""

from ...semantics.type_system import FieldType
from ..formatting import indented, statement


class MakeMixin:
    def field(self, items):
        name, type_tok = items
        return f"{name} {FieldType.parse(type_tok).to_sql()}"

    def make_stmt(self, items):
        table, *fields = items
        return statement(f"CREATE TABLE {table} (\n{indented(fields)}\n)")
