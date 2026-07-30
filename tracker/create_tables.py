import sqlite3
import os


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DB_PATH = os.path.join(BASE_DIR, "database", "youtube.db")


conn = sqlite3.connect(DB_PATH)

cursor = conn.cursor()


cursor.execute("""
CREATE TABLE IF NOT EXISTS view_history (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    video_id TEXT,

    views INTEGER,

    likes INTEGER,

    comments INTEGER,

    recorded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

)
""")


conn.commit()

conn.close()


print("✅ view_history table created")