"""Traducción de los errores de Lark a mensajes legibles en español."""

from lark.exceptions import UnexpectedCharacters, UnexpectedEOF, UnexpectedInput, UnexpectedToken

from ..errors import CompileError

MAX_EXPECTED = 6

TERMINAL_NAMES = {
    "NAME": "un identificador",
    "TYPE_NAME": "un tipo",
    "STRING": "una cadena",
    "NUMBER": "un número",
    "INT": "un entero",
    "OP": "un operador",
    "STAR": "'*'",
    "LPAR": "'('",
    "RPAR": "')'",
    "COMMA": "','",
    "EQUAL": "'='",
    "_NL": "fin de línea",
    "$END": "fin del archivo",
}


def friendly(terminal: str) -> str:
    return TERMINAL_NAMES.get(terminal, terminal)


def describe_found(token) -> str:
    if token.type == "$END":
        return "el fin del archivo"
    if token.type == "_NL":
        return "un fin de línea"
    return repr(str(token))


def to_compile_error(error: UnexpectedInput) -> CompileError:
    """Convierte una excepción de Lark en un CompileError con posición."""
    if isinstance(error, UnexpectedCharacters):
        return CompileError(f"carácter inesperado {error.char!r}", error.line, error.column)
    if isinstance(error, UnexpectedToken):
        expected = ", ".join(sorted(friendly(t) for t in error.expected)[:MAX_EXPECTED])
        return CompileError(
            f"se encontró {describe_found(error.token)} y se esperaba: {expected}",
            error.line, error.column,
        )
    if isinstance(error, UnexpectedEOF):
        return CompileError("la instrucción termina inesperadamente")
    return CompileError(str(error))
