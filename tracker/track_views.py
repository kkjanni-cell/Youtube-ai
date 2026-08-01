import sqlite3
import os
from datetime import datetime

from youtube_api import get_video_details

# -----------------------------
# PATHS
# -----------------------------

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, "database", "youtube.db")

# -----------------------------
# GET VIDEO IDS FROM DATABASE
# -----------------------------

def get_database_videos():

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT video_id
        FROM videos
    """)

    videos = cursor.fetchall()

    conn.close()

    return videos


# -----------------------------
# UPDATE VIDEO MASTER TABLE
# -----------------------------

def update_video_details(data):

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE videos
        SET video_name = ?
        WHERE video_id = ?
    """, (
        data["title"],
        data["video_id"]
    ))

    conn.commit()
    conn.close()


# -----------------------------
# SAVE HISTORY
# -----------------------------

def save_history(data):

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Get previous views

    cursor.execute("""
        SELECT views
        FROM view_history
        WHERE video_id = ?
        ORDER BY timestamp DESC
        LIMIT 1
    """, (data["video_id"],))

    previous = cursor.fetchone()

    if previous:
        view_gain = data["views"] - previous[0]
    else:
        view_gain = 0

    cursor.execute("""
        INSERT INTO view_history
        (
            video_id,
            video_name,
            timestamp,
            views,
            view_gain,
            likes,
            comments
        )
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """,
    (
        data["video_id"],
        data["title"],          # Always use latest YouTube title
        datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        data["views"],
        view_gain,
        data["likes"],
        data["comments"]
    ))

    conn.commit()
    conn.close()

    print(f"View Gain: {view_gain}")


# -----------------------------
# MAIN TRACKER
# -----------------------------

if __name__ == "__main__":

    videos = get_database_videos()

    print(f"\nTracking {len(videos)} videos\n")

    for (video_id,) in videos:

        print(f"Checking: {video_id}")

        data = get_video_details(video_id)

        if data:

            # Update title in master table
            update_video_details(data)

            # Save tracking history
            save_history(data)

            print(f"✅ {data['title']}")
            print("----------------")