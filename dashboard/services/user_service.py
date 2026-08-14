import sqlite3
import os
from datetime import datetime

import bcrypt

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DB_PATH = os.path.join(BASE_DIR, "database", "youtube.db")


def get_connection():
    return sqlite3.connect(DB_PATH)


def get_all_users():
    """
    Return every user account, most recently created first.
    """

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        SELECT username, full_name, role, active, created_at
        FROM users
        ORDER BY created_at DESC
        """
    )

    rows = cur.fetchall()
    conn.close()

    columns = ["username", "full_name", "role", "active", "created_at"]

    return [dict(zip(columns, row)) for row in rows]


def user_exists(username: str) -> bool:

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        "SELECT 1 FROM users WHERE username = ?", (username,)
    )

    exists = cur.fetchone() is not None
    conn.close()

    return exists


def create_user(username: str, password: str, full_name: str, role: str):
    """
    Create a new user account.

    Returns:
        (success: bool, message: str)
    """

    username = username.strip()
    full_name = full_name.strip()

    if not username or not password or not full_name:
        return False, "Username, password, and full name are required."

    if len(password) < 8:
        return False, "Password must be at least 8 characters."

    if user_exists(username):
        return False, "That username already exists."

    if role not in ("Admin", "Viewer"):
        return False, "Role must be Admin or Viewer."

    password_hash = bcrypt.hashpw(
        password.encode(), bcrypt.gensalt()
    ).decode()

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        INSERT INTO users
        (username, password_hash, full_name, role, active)
        VALUES (?, ?, ?, ?, 1)
        """,
        (username, password_hash, full_name, role),
    )

    conn.commit()
    conn.close()

    return True, f"User '{username}' created successfully."


def set_user_active(username: str, active: bool):
    """
    Activate or deactivate a user account (soft, reversible -
    does not delete anything).
    """

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        "UPDATE users SET active = ? WHERE username = ?",
        (1 if active else 0, username),
    )

    conn.commit()
    conn.close()

    state = "activated" if active else "deactivated"
    return True, f"User '{username}' {state}."


def update_user_role(username: str, role: str):

    if role not in ("Admin", "Viewer"):
        return False, "Role must be Admin or Viewer."

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        "UPDATE users SET role = ? WHERE username = ?",
        (role, username),
    )

    conn.commit()
    conn.close()

    return True, f"Role for '{username}' updated to {role}."


def admin_reset_password(username: str, new_password: str):
    """
    Admin-initiated password reset - does NOT require the
    user's current password (unlike the self-service change
    on the Settings page).
    """

    if len(new_password) < 8:
        return False, "New password must be at least 8 characters."

    new_hash = bcrypt.hashpw(
        new_password.encode(), bcrypt.gensalt()
    ).decode()

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        "UPDATE users SET password_hash = ? WHERE username = ?",
        (new_hash, username),
    )

    conn.commit()
    conn.close()

    return True, f"Password reset for '{username}'."