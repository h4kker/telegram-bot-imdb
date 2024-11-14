import sqlite3
from contextlib import closing

# Имя файла базы данных
DB_NAME = "bot_history.db"


def create_tables():
    with closing(sqlite3.connect(DB_NAME)) as conn, conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                command TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
    print("Таблица истории создана (если её не было).")


def add_to_history(user_id: int, command: str):
    with closing(sqlite3.connect(DB_NAME)) as conn, conn:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO history (user_id, command)
            VALUES (?, ?)
        ''', (user_id, command))


def get_user_history(user_id: int):
    with closing(sqlite3.connect(DB_NAME)) as conn, conn:
        cursor = conn.cursor()
        cursor.execute('''
            SELECT command, timestamp FROM history
            WHERE user_id = ?
            ORDER BY timestamp DESC
            LIMIT 10
        ''', (user_id,))
        return cursor.fetchall()
