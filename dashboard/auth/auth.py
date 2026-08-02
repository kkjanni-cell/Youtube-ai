import sqlite3
import bcrypt
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DB_PATH = os.path.join(BASE_DIR, "database", "youtube.db")


def authenticate(username, password):

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            username,
            password_hash,
            full_name,
            role,
            active
        FROM users
        WHERE username = ?
    """, (username,))

    user = cursor.fetchone()

    conn.close()

    if not user:
        return None

    username, password_hash, full_name, role, active = user

    if active != 1:
        return None

    if bcrypt.checkpw(password.encode(), password_hash.encode()):

        return {
            "username": username,
            "full_name": full_name,
            "role": role
        }

    return None