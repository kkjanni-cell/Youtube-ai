import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parents[1] / "database" / "youtube.db"

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

cursor.execute("DELETE FROM view_history")
cursor.execute("DELETE FROM videos")

conn.commit()
conn.close()

print("✅ All tracked videos removed.")
print("✅ All tracking history removed.")
print("🚀 Database is ready for scheduled tracking.")