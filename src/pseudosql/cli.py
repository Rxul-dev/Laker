"""Interfaz de línea de comandos."""

import argparse
import sys
from pathlib import Path

from .compiler import compile_source
from .errors import CompileError
from .parsing import parse


def build_arg_parser() -> argparse.ArgumentParser:
    ap = argparse.ArgumentParser(
        prog="pseudosql", description="Compilador Pseudolenguaje -> PostgreSQL (Lark)"
    )
    ap.add_argument("input", help="archivo de entrada (.pseudo)")
    ap.add_argument("-o", "--output", help="archivo .sql de salida (por defecto: mismo nombre con .sql)")
    ap.add_argument("--ast", action="store_true", help="mostrar el árbol de sintaxis")
    return ap


def main(argv=None) -> int:
    args = build_arg_parser().parse_args(argv)

    src_path = Path(args.input)
    try:
        source = src_path.read_text(encoding="utf-8")
        if args.ast:
            print(parse(source).pretty())
        sql = compile_source(source)
    except FileNotFoundError:
        print(f"error: no existe el archivo '{src_path}'", file=sys.stderr)
        return 2
    except CompileError as e:
        print(f"{src_path.name}: error de compilación en {e}", file=sys.stderr)
        return 1

    out_path = Path(args.output) if args.output else src_path.with_suffix(".sql")
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(sql, encoding="utf-8")
    print(f"OK  {src_path.name} -> {out_path}")
    return 0
