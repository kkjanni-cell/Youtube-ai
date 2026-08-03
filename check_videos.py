import sqlite3

conn = sqlite3.connect("database/youtube.db")
cursor = conn.cursor()

cursor.execute("""
SELECT
    video_id,
    video_name,
    start_time,
    end_time,
    tracking_interval,
    status
FROM videos
""")

rows = cursor.fetchall()

print(f"\nFound {len(rows)} videos\n")

for row in rows:
    print(row)

conn.close()