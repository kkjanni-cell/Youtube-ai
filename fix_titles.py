import sqlite3

conn = sqlite3.connect("database/youtube.db")
cursor = conn.cursor()

print("Updating historical titles...")

cursor.execute("""
UPDATE view_history
SET video_name = (
    SELECT video_name
    FROM videos
    WHERE videos.video_id = view_history.video_id
)
""")

conn.commit()

print(f"Rows updated: {conn.total_changes}")

conn.close()

print("✅ Done!")