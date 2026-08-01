import sqlite3

conn = sqlite3.connect("database/youtube.db")
cursor = conn.cursor()

cursor.execute("""
SELECT video_id, video_name
FROM videos
ORDER BY video_name
""")

rows = cursor.fetchall()

print("=" * 60)
print(f"TOTAL VIDEOS : {len(rows)}")
print("=" * 60)

for i, row in enumerate(rows, start=1):
    print(f"{i}. {row[1]}")
    print(f"   {row[0]}")
    print()

conn.close()