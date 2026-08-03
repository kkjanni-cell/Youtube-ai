import sqlite3

conn = sqlite3.connect("database/youtube.db")
cursor = conn.cursor()

cursor.execute("SELECT COUNT(*) FROM videos")
print("Videos:", cursor.fetchone()[0])

cursor.execute("SELECT COUNT(*) FROM view_history")
print("History:", cursor.fetchone()[0])

conn.close()