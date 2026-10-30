"""PUT <tabla> (<campo> = <valor>, ...) [WHERE]

  sin WHERE -> INSERT      con WHERE -> UPDATE
"""

from ..formatting import comma_list, statement


class PutMixin:
    def assignment(self, items):
        return (items[0], items[1])

    def put_stmt(self, items):
        table, *assignments, where = items
        if where is None:
            return self._insert(table, assignments)
        return self._update(table, assignments, where)

    @staticmethod
    def _insert(table, assignments):
        cols = comma_list(c for c, _ in assignments)
        vals = comma_list(v for _, v in assignments)
        return statement(f"INSERT INTO {table} ({cols})", f"VALUES ({vals})")

    @staticmethod
    def _update(table, assignments, where):
        sets = comma_list(f"{c} = {v}" for c, v in assignments)
        return statement(f"UPDATE {table}", f"SET {sets}", where)
