"""Generación de condiciones (WHERE) y valores literales.

Es un mixin: lo comparten GET, PUT y DROP a través de SqlGenerator.
"""


class ExpressionsMixin:
    # ---- condiciones ----
    def where_clause(self, items):
        return f"WHERE {items[0]}"

    def or_expr(self, items):
        return " OR ".join(items)

    def and_expr(self, items):
        return " AND ".join(items)

    def compare(self, items):
        left, op, right = items
        return f"{left} {op} {right}"

    def like(self, items):
        return f"{items[0]} LIKE {items[1]}"

    def is_null(self, items):
        return f"{items[0]} IS NULL"

    def is_not_null(self, items):
        return f"{items[0]} IS NOT NULL"

    def group(self, items):
        return f"({items[0]})"

    # ---- valores ----
    def ident(self, items):
        return str(items[0])

    def string(self, items):
        raw = str(items[0])
        if raw.startswith("'"):
            return raw  # ya viene con comillas simples (y '' escapado)
        # "texto": en PostgreSQL las comillas dobles son identificadores,
        # así que se convierte a literal con comillas simples
        text = raw[1:-1].replace('""', '"').replace("'", "''")
        return f"'{text}'"

    def number(self, items):
        return str(items[0])

    def true(self, _):
        return "TRUE"

    def false(self, _):
        return "FALSE"

    def null(self, _):
        return "NULL"
