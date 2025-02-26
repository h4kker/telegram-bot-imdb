import sqlite3
import logging
from contextlib import closing
from typing import List, Tuple

DB_NAME = "bot_history.db"
logging.basicConfig(level=logging.INFO)


def create_tables():
    with closing(sqlite3.connect(DB_NAME)) as conn, conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                command TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_user_id ON history (user_id);")
    print("Таблица истории создана (если её не было).")


def add_to_history(user_id: int, command: str):
    with closing(sqlite3.connect(DB_NAME)) as conn, conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO history (user_id, command)
            VALUES (?, ?)
        """,
            (user_id, command))
        logging.info(f"Запись добавлена в историю: user_id={user_id}, command={command}")


def get_user_history(user_id: int) -> List[Tuple[str, str]]:
    with closing(sqlite3.connect(DB_NAME)) as conn, conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT command, timestamp FROM history
            WHERE user_id = ?
            ORDER BY timestamp DESC
            LIMIT 10
        """,
            (user_id,),
        )
        history = cursor.fetchall()
        logging.info(f"Получена история для user_id={user_id}: {history}")
        return history
