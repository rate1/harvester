import sqlite3
import pytest

from database import initialize_db


@pytest.fixture()
def db_connection():
    """Фикстура для создания временной БД в памяти."""

    conn = sqlite3.connect(":memory:")
    yield conn
    conn.close()


def test_initialize_db(db_connection, monkeypatch):
    """Функция для тестирования инициализации БД."""

    expected_tables = [
            "languages", "translators", "publication_status", "subjects",
            "categories", "topics", "platforms", "channels",
            "channels_categories", "original_texts", "videos", "translates",
            "rewrites", "publications"
            ]

    def mock_connect(db_name):
        return db_connection

    monkeypatch.setattr(sqlite3, "connect", mock_connect)

    initialize_db("test.db")

    cursor = db_connection.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    actual_tables = [table[0] for table in cursor.fetchall()]

    for table in expected_tables:
        assert table in actual_tables, f"Таблица {table} не была создана."
