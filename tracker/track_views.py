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
# GET VIDEOS FROM DATABASE
# -----------------------------

def get_database_videos():

    conn = sqlite3.connect(DB_PATH)

    cursor = conn.cursor()

    cursor.execute("""
        SELECT video_id, video_name
        FROM videos
    """)

    videos = cursor.fetchall()

    conn.close()

    return videos



# -----------------------------
# SAVE HISTORY
# -----------------------------

def save_history(data, video_name):

    conn = sqlite3.connect(DB_PATH)

    cursor = conn.cursor()


    # Previous views

    cursor.execute("""
        SELECT views
        FROM view_history
        WHERE video_id = ?
        ORDER BY timestamp DESC
        LIMIT 1
    """,
    (data["video_id"],))


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
        video_name,
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


    for video_id, video_name in videos:


        print(f"Checking: {video_name}")


        data = get_video_details(video_id)


        if data:

            save_history(data, video_name)

            print("✅ Saved")

            print("----------------")