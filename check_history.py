import sqlite3

conn = sqlite3.connect("database/youtube.db")
cursor = conn.cursor()

cursor.execute("""
SELECT
    video_id,
    COUNT(DISTINCT video_name)
FROM view_history
GROUP BY video_id
""")

rows = cursor.fetchall()

print("=" * 50)

for video_id, count in rows:
    print(video_id, "->", count, "titles")

conn.close()