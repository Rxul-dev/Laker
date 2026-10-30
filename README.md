# pseudosql

Compilador del Pseudolenguaje PostgreSQL → SQL (PostgreSQL), implementado con [Lark](https://github.com/lark-parser/lark).

## Estructura

```
src/pseudosql/
├── __init__.py            API pública: compile_source, parse, CompileError
├── __main__.py            permite `python -m pseudosql`
├── cli.py                 interfaz de línea de comandos (argparse)
├── compiler.py            pipeline: parse -> analyze -> generate
├── errors.py              CompileError (compartido por todas las fases)
├── parsing/               FASE 1-2: léxico + sintáctico -> AST
│   ├── pseudo.lark        gramática EBNF
│   ├── parser.py          construye el parser LALR(1) (una sola vez)
│   └── diagnostics.py     traduce errores de Lark a mensajes en español
├── semantics/             FASE 3a: análisis semántico
│   ├── type_system.py     tabla de tipos (fuente única de verdad)
│   └── analyzer.py        valida tipos y campos duplicados
└── codegen/               FASE 3b: generación de SQL
    ├── generator.py       SqlGenerator = suma de mixins
    ├── formatting.py      helpers de formato reutilizables
    ├── expressions.py     WHERE / AND / OR / LIKE / valores
    └── statements/        un archivo por instrucción
        ├── make.py        MAKE  -> CREATE TABLE
        ├── get.py         GET   -> SELECT
        ├── put.py         PUT   -> INSERT / UPDATE
        └── drop.py        DROP  -> DROP TABLE / DELETE
```

## Instalación

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
```

## Uso

```bash
pseudosql examples/demo.pseudo              # escribe examples/demo.sql
pseudosql examples/demo.pseudo -o out.sql
pseudosql examples/demo.pseudo --ast        # muestra además el árbol
python -m pseudosql examples/demo.pseudo    # equivalente
```

Como librería:

```python
from pseudosql import compile_source
print(compile_source("GET * FROM users TOP 10"))
```

## Tipos

| Pseudo | PostgreSQL |
|--------|------------|
| `id`   | `BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY` |
| `num`  | `NUMERIC` |
| `text` | `TEXT` |
| `bool` | `BOOLEAN DEFAULT FALSE` |
| `time` | `TIMESTAMPTZ DEFAULT NOW()` |

Agregar `!` al tipo (`text!`) añade `NOT NULL`.

## Sintaxis

- Las palabras clave no distinguen mayúsculas (`GET`, `get`, `Get`; también `true`/`TRUE`, `null`/`NULL`).
- `GET ALL` equivale a `GET *`.
- `SORT campo [ASC|DESC]`.
- Las cadenas aceptan comillas simples (`'texto'`) o dobles (`"texto"`); ambas se generan como literal `'texto'`.

## Extender el lenguaje

- **Nuevo tipo:** una línea en `semantics/type_system.py`.
- **Nueva instrucción:** regla en `parsing/pseudo.lark`, un mixin en `codegen/statements/`, y sumarlo a `SqlGenerator` en `codegen/generator.py`. Si tiene reglas semánticas, agregar el método en `semantics/analyzer.py`.

## Tests

```bash
pytest
```
