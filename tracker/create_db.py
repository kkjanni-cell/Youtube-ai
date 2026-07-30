import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DB_PATH = os.path.join(BASE_DIR, "database", "youtube.db")

conn = sqlite3.connect(DB_PATH)

cursor = conn.cursor()

# -----------------------------
# VIDEOS TABLE
# -----------------------------
cursor.execute("""
CREATE TABLE IF NOT EXISTS videos (

    video_id TEXT PRIMARY KEY,

    video_name TEXT,

    channel_name TEXT,

    added_on DATETIME DEFAULT CURRENT_TIMESTAMP,

    status TEXT DEFAULT 'ACTIVE'

)
""")

# -----------------------------
# VIEW HISTORY TABLE
# -----------------------------
cursor.execute("""
CREATE TABLE IF NOT EXISTS view_history (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    video_id TEXT,

    timestamp DATETIME,

    views INTEGER,

    view_gain INTEGER,

    FOREIGN KEY(video_id)
        REFERENCES videos(video_id)

)
""")

conn.commit()

print("=================================")
print("DATABASE CREATED SUCCESSFULLY")
print("=================================")

print("\nTables Created")

print("- videos")
print("- view_history")

conn.close()