import sqlite3
import pandas as pd
import os

from youtube_api import get_video_details

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
# IMPORT VIDEOS
# -----------------------------

for _, row in videos.iterrows():

    video_id = row["video_id"]

    details = get_video_details(video_id)

    if details is None:
        print(f"❌ Could not fetch {video_id}")
        continue

    cursor.execute(
        """
        INSERT INTO videos (video_id, video_name)
        VALUES (?, ?)
        ON CONFLICT(video_id)
        DO UPDATE SET
            video_name = excluded.video_name
        """,
        (
            video_id,
            details["title"],
        ),
    )

    print(f"✅ {details['title']}")

conn.commit()
conn.close()

print("\nImport Complete.")