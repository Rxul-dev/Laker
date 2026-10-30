"""
Compilador del Pseudolenguaje PostgreSQL  ->  SQL (PostgreSQL)
===============================================================

Fases del compilador (un subpaquete por fase):
  1-2. parsing/   : análisis léxico + sintáctico con Lark (LALR(1)) -> AST
  3a.  semantics/ : análisis semántico (tipos, campos duplicados)
  3b.  codegen/   : generación de SQL (un mixin por instrucción)

Uso como librería:
    from pseudosql import compile_source
    sql = compile_source("GET * FROM users TOP 10")
"""

from .compiler import compile_source
from .errors import CompileError
from .parsing import parse

__all__ = ["compile_source", "parse", "CompileError"]
__version__ = "1.0.0"
