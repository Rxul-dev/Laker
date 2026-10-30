"""Orquestador del pipeline: parse -> analyze -> generate."""

from .codegen import generate
from .parsing import parse
from .semantics import analyze


def compile_source(source: str) -> str:
    """Compila texto en pseudolenguaje a SQL de PostgreSQL."""
    tree = parse(source)
    analyze(tree)
    return generate(tree)
