import sqlite3
import bcrypt
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, "database", "youtube.db")

USERNAME = "janni"
PASSWORD = "jannikk@65!"
FULL_NAME = "Janni"
ROLE = "Admin"

password_hash = bcrypt.hashpw(
    PASSWORD.encode(),
    bcrypt.gensalt()
).decode()

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# Check if user already exists
cursor.execute(
    "SELECT id FROM users WHERE username = ?",
    (USERNAME,)
)

existing_user = cursor.fetchone()

if existing_user:
    print(f"⚠️ User '{USERNAME}' already exists.")
else:
    cursor.execute("""
        INSERT INTO users
        (username, password_hash, full_name, role)
        VALUES (?, ?, ?, ?)
    """, (
        USERNAME,
        password_hash,
        FULL_NAME,
        ROLE
    ))

    conn.commit()
    print("✅ Admin created successfully.")

conn.close()