from pseudosql.cli import main


def test_writes_sql_next_to_input(tmp_path):
    src = tmp_path / "x.pseudo"
    src.write_text("DROP users\n", encoding="utf-8")
    assert main([str(src)]) == 0
    assert (tmp_path / "x.sql").read_text(encoding="utf-8") == "DROP TABLE users;\n"


def test_custom_output_path(tmp_path):
    src = tmp_path / "x.pseudo"
    src.write_text("DROP users\n", encoding="utf-8")
    out = tmp_path / "out" / "y.sql"
    assert main([str(src), "-o", str(out)]) == 0
    assert out.exists()


def test_compile_error_exit_code(tmp_path, capsys):
    src = tmp_path / "bad.pseudo"
    src.write_text("MAKE t (a foo)\n", encoding="utf-8")
    assert main([str(src)]) == 1
    assert "error de compilación" in capsys.readouterr().err


def test_missing_file_exit_code(tmp_path):
    assert main([str(tmp_path / "nope.pseudo")]) == 2
