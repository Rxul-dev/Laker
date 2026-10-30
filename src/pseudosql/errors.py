"""Errores compartidos por todas las fases del compilador."""

from lark import Token


class CompileError(Exception):
    """Error de compilación con posición (línea/columna) cuando se conoce."""

    def __init__(self, message, line=None, column=None):
        self.message = message
        self.line = line
        self.column = column
        where = f"línea {line}" if line else ""
        if line and column:
            where += f", columna {column}"
        super().__init__(f"{where}: {message}" if where else message)

    @classmethod
    def at(cls, token: Token, message: str) -> "CompileError":
        """Crea el error usando la posición de un token del árbol."""
        return cls(message, getattr(token, "line", None), getattr(token, "column", None))
