import sqlite3
import pandas as pd
import os

# -----------------------------
# PATHS
# -----------------------------

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DB_PATH = os.path.join(BASE_DIR, "database", "youtube.db")

CSV_PATH = os.path.join(BASE_DIR, "config", "videos.csv")

# -----------------------------
# CONNECT DATABASE
# -----------------------------

conn = sqlite3.connect(DB_PATH)

cursor = conn.cursor()

# -----------------------------
# READ CSV
# -----------------------------

videos = pd.read_csv(CSV_PATH)

print(f"\nFound {len(videos)} videos.\n")

# -----------------------------
# INSERT INTO DATABASE
# -----------------------------

for _, row in videos.iterrows():

    cursor.execute("""
        INSERT OR IGNORE INTO videos
        (video_id, video_name)
        VALUES (?, ?)
    """, (
        row["Video_ID"],
        row["Video_Name"]
    ))

    if cursor.rowcount == 1:
        print(f"Added : {row['Video_Name']}")
    else:
        print(f"Already exists : {row['Video_Name']}")