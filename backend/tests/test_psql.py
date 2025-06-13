import pytest

from core.engines.PostgresEngine import PostgresEngine
from core.engines.exceptions import DBNotExists, DBExists


dump_1 = \
"""
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    name VARCHAR(30) NOT NULL,
    age INTEGER NOT NULL
);
INSERT INTO users (name, age) VALUES ('vasya', 19);
"""


def test_1():
    engine = PostgresEngine(
        root_db="dbpg",
        user="dbpg",
        password="dbpg_pwd",
        host="127.0.0.1",
        port=5432,
    )

    with pytest.raises(DBNotExists):
        engine.get_db("test_2_db")

    engine.create_db("test_2_db", dump_1)

    with pytest.raises(DBExists):
        engine.create_db("test_2_db", "")

    db = engine.get_db("test_2_db")
    engine.drop_db("test_2_db")

    assert db is not None
    assert db.name == "test_2_db"
    assert any(table.name == "users" for table in db.tables)
    assert any(any((c.name, c.type) == ('age', 'integer') for c in t.columns) for t in db.tables)
    assert any(any((c.name, c.type) == ('name', 'character varying') for c in t.columns) for t in db.tables)
