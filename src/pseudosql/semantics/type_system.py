"""Tabla de tipos del pseudolenguaje y su traducción a PostgreSQL.

Es la única fuente de verdad sobre tipos: la usan tanto el analizador
semántico (para validar) como el generador de código (para traducir).
"""

from dataclasses import dataclass

NOT_NULL_SUFFIX = "!"

TYPE_MAP = {
    "id": "BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY",
    "num": "NUMERIC",
    "text": "TEXT",
    "bool": "BOOLEAN DEFAULT FALSE",
    "time": "TIMESTAMPTZ DEFAULT NOW()",
}


@dataclass(frozen=True)
class FieldType:
    raw: str
    base: str
    not_null: bool

    @classmethod
    def parse(cls, raw: str) -> "FieldType":
        raw = str(raw)
        return cls(
            raw=raw,
            base=raw.rstrip(NOT_NULL_SUFFIX),
            not_null=raw.endswith(NOT_NULL_SUFFIX),
        )

    @property
    def is_known(self) -> bool:
        return self.base in TYPE_MAP

    def to_sql(self) -> str:
        return TYPE_MAP[self.base] + (" NOT NULL" if self.not_null else "")


def valid_types_hint() -> str:
    return f"tipos válidos: {', '.join(TYPE_MAP)}; agregue '{NOT_NULL_SUFFIX}' para NOT NULL"
