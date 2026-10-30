"""Utilidades de formato SQL reutilizadas por todos los generadores."""

from typing import Iterable, Optional


def comma_list(items: Iterable) -> str:
    return ", ".join(str(item) for item in items)


def indented(lines: Iterable[str], prefix: str = "  ", sep: str = ",\n") -> str:
    return sep.join(f"{prefix}{line}" for line in lines)


def statement(*parts: Optional[str], sep: str = "\n") -> str:
    """Une las partes no nulas de una sentencia y la termina con ';'."""
    return sep.join(p for p in parts if p is not None) + ";"


def program(statements: list) -> str:
    return "\n\n".join(statements) + ("\n" if statements else "")
