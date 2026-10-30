from pseudosql import compile_source


def test_make_creates_table_with_mapped_types():
    sql = compile_source("MAKE users (id id, name text!, active bool)")
    assert sql == (
        "CREATE TABLE users (\n"
        "  id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,\n"
        "  name TEXT NOT NULL,\n"
        "  active BOOLEAN DEFAULT FALSE\n"
        ");\n"
    )


def test_get_with_all_clauses():
    sql = compile_source("GET name, email FROM users WHERE age >= 18 SORT name TOP 5")
    assert sql == "SELECT name, email\nFROM users\nWHERE age >= 18\nORDER BY name\nLIMIT 5;\n"


def test_get_star():
    assert compile_source("GET * FROM users") == "SELECT *\nFROM users;\n"


def test_put_without_where_is_insert():
    sql = compile_source("PUT users (name = 'O''Brien', age = 30)")
    assert sql == "INSERT INTO users (name, age)\nVALUES ('O''Brien', 30);\n"


def test_put_with_where_is_update():
    sql = compile_source("PUT users (active = FALSE) WHERE id = 1")
    assert sql == "UPDATE users\nSET active = FALSE\nWHERE id = 1;\n"


def test_drop_without_where_is_drop_table():
    assert compile_source("DROP users") == "DROP TABLE users;\n"


def test_drop_with_where_is_delete():
    assert compile_source("DROP users WHERE email IS NULL") == "DELETE FROM users WHERE email IS NULL;\n"


def test_conditions_keep_grouping_and_precedence():
    sql = compile_source("GET * FROM t WHERE a = 1 AND (b LIKE 'x%' OR c IS NOT NULL)")
    assert "WHERE a = 1 AND (b LIKE 'x%' OR c IS NOT NULL)" in sql


def test_multiple_statements_comments_and_blank_lines():
    src = "\n-- comentario\nGET * FROM a\n\n\nDROP b\n"
    assert compile_source(src) == "SELECT *\nFROM a;\n\nDROP TABLE b;\n"


def test_comment_lines_between_statements():
    src = "GET * FROM a  -- fin de línea\n  -- solo comentario\n\n-- otro\nDROP b"
    assert compile_source(src) == "SELECT *\nFROM a;\n\nDROP TABLE b;\n"


def test_empty_program():
    assert compile_source("") == ""


def test_keywords_are_case_insensitive():
    sql = compile_source("get name from users where active = true sort name top 5")
    assert sql == "SELECT name\nFROM users\nWHERE active = TRUE\nORDER BY name\nLIMIT 5;\n"


def test_lowercase_booleans_in_put():
    sql = compile_source("PUT users (active = false, note = null)")
    assert sql == "INSERT INTO users (active, note)\nVALUES (FALSE, NULL);\n"


def test_get_all_is_star():
    assert compile_source("GET ALL FROM users") == "SELECT *\nFROM users;\n"


def test_double_quoted_string_becomes_single_quoted():
    sql = compile_source('GET * FROM t WHERE a = "it\'s ""ok"""')
    assert "WHERE a = 'it''s \"ok\"'" in sql


def test_sort_direction():
    assert "ORDER BY price DESC;" in compile_source("GET * FROM t SORT price DESC")
    assert "ORDER BY price ASC;" in compile_source("GET * FROM t sort price asc")
