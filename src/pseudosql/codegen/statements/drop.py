"""DROP <tabla> [WHERE]

  sin WHERE -> DROP TABLE  con WHERE -> DELETE
"""

from ..formatting import statement


class DropMixin:
    def drop_stmt(self, items):
        table, where = items
        if where is None:
            return statement(f"DROP TABLE {table}")
        return statement(f"DELETE FROM {table}", where, sep=" ")
