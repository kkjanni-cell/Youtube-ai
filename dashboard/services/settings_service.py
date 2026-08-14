import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DB_PATH = os.path.join(BASE_DIR, "database", "youtube.db")


def get_connection():
    return sqlite3.connect(DB_PATH)


def _ensure_table():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS app_settings (
            key TEXT PRIMARY KEY,
            value TEXT
        )
        """
    )
    conn.commit()
    conn.close()


def get_setting(key: str, default=None):
    _ensure_table()

    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT value FROM app_settings WHERE key = ?", (key,))
    row = cur.fetchone()
    conn.close()

    return row[0] if row else default


def set_setting(key: str, value: str):
    _ensure_table()

    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        """
        INSERT INTO app_settings (key, value)
        VALUES (?, ?)
        ON CONFLICT(key) DO UPDATE SET value = excluded.value
        """,
        (key, str(value)),
    )
    conn.commit()
    conn.close()


def get_default_tracking_interval() -> int:
    return int(get_setting("default_tracking_interval", 5))


def set_default_tracking_interval(minutes: int):
    set_setting("default_tracking_interval", minutes)