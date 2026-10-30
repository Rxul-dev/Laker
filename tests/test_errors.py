import pytest

from pseudosql import CompileError, compile_source


def compile_error(src) -> CompileError:
    with pytest.raises(CompileError) as exc:
        compile_source(src)
    return exc.value


def test_unknown_type_reports_position():
    err = compile_error("MAKE t (a texto)")
    assert "tipo desconocido 'texto'" in err.message
    assert (err.line, err.column) == (1, 11)


def test_duplicate_field():
    err = compile_error("MAKE t (a text, a num)")
    assert "el campo 'a' está duplicado en la tabla 't'" in err.message
    assert (err.line, err.column) == (1, 17)


def test_unexpected_character():
    err = compile_error("GET * FROM t WHERE a = 1 ; ")
    assert "carácter inesperado ';'" in err.message


def test_unexpected_token_lists_expected():
    err = compile_error("GET * users")
    assert "se encontró 'users' y se esperaba: FROM" in err.message


def test_error_on_second_line():
    err = compile_error("GET * FROM t\nMAKE x (a nope)")
    assert err.line == 2
