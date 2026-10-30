"""GET <campos> FROM <tabla> [WHERE] [SORT] [TOP]  ->  SELECT"""

from ..formatting import comma_list, statement


class GetMixin:
    def all_columns(self, _):
        return "*"

    def column_list(self, names):
        return comma_list(names)

    def sort_clause(self, items):
        column, direction = items
        if direction is None:
            return f"ORDER BY {column}"
        return f"ORDER BY {column} {direction.upper()}"

    def top_clause(self, items):
        return f"LIMIT {items[0]}"

    def get_stmt(self, items):
        columns, table, where, sort, top = items
        return statement(f"SELECT {columns}", f"FROM {table}", where, sort, top)
