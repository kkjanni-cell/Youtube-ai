import os
import sqlite3
from datetime import datetime
from zoneinfo import ZoneInfo

from youtube_api import get_video_details

# --------------------------------------------------
# PATHS
# --------------------------------------------------

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, "database", "youtube.db")

IST = ZoneInfo("Asia/Kolkata")


# --------------------------------------------------
# DATABASE
# --------------------------------------------------

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


# --------------------------------------------------
# GET TRACKABLE VIDEOS
# --------------------------------------------------

def get_database_videos():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM videos
        WHERE status IN ('scheduled', 'tracking')
    """)

    videos = cursor.fetchall()

    conn.close()

    return videos


# --------------------------------------------------
# UPDATE VIDEO TITLE
# --------------------------------------------------

def update_video_details(data):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE videos
        SET
            video_name = ?,
            updated_at = ?
        WHERE video_id = ?
    """, (
        data["title"],
        datetime.now(IST).isoformat(timespec="seconds"),
        data["video_id"],
    ))

    conn.commit()
    conn.close()


# --------------------------------------------------
# UPDATE STATUS
# --------------------------------------------------

def update_video_status(video_id, status):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE videos
        SET
            status = ?,
            updated_at = ?
        WHERE video_id = ?
    """, (
        status,
        datetime.now(IST).isoformat(timespec="seconds"),
        video_id,
    ))

    conn.commit()
    conn.close()


# --------------------------------------------------
# SHOULD TRACK?
# --------------------------------------------------

def should_track(video):
    """
    Returns:
        scheduled
        tracking
        completed

    Old videos (without schedule) continue tracking forever.
    """

    start_time = video["start_time"]
    end_time = video["end_time"]

    # -----------------------------
    # Backward compatibility
    # -----------------------------

    if not start_time or not end_time:
        return "tracking"

    now = datetime.now(IST)

    start = datetime.fromisoformat(start_time)
    end = datetime.fromisoformat(end_time)

    if start.tzinfo is None:
        start = start.replace(tzinfo=IST)

    if end.tzinfo is None:
        end = end.replace(tzinfo=IST)

    if now < start:
        return "scheduled"

    if now > end:
        return "completed"

    return "tracking"


# --------------------------------------------------
# SAVE HISTORY
# --------------------------------------------------

def save_history(data):

    conn = get_connection()
    cursor = conn.cursor()

    now = datetime.now(IST)

    rounded_minute = (now.minute // 5) * 5

    rounded_time = now.replace(
        minute=rounded_minute,
        second=0,
        microsecond=0,
    )

    timestamp = rounded_time.strftime("%Y-%m-%d %H:%M:%S")

    cursor.execute("""
        SELECT views
        FROM view_history
        WHERE video_id = ?
        ORDER BY timestamp DESC
        LIMIT 1
    """, (data["video_id"],))

    previous = cursor.fetchone()

    if previous:
        view_gain = data["views"] - previous["views"]
    else:
        view_gain = 0

    cursor.execute("""
        SELECT id
        FROM view_history
        WHERE video_id = ?
        AND timestamp = ?
    """, (
        data["video_id"],
        timestamp,
    ))

    existing = cursor.fetchone()

    if existing:

        cursor.execute("""
            UPDATE view_history
            SET
                video_name = ?,
                views = ?,
                view_gain = ?,
                likes = ?,
                comments = ?
            WHERE id = ?
        """, (
            data["title"],
            data["views"],
            view_gain,
            data["likes"],
            data["comments"],
            existing["id"],
        ))

        print(f"🔄 Updated {timestamp}")

    else:

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
        """, (
            data["video_id"],
            data["title"],
            timestamp,
            data["views"],
            view_gain,
            data["likes"],
            data["comments"],
        ))

        print(f"➕ Added {timestamp}")

    conn.commit()
    conn.close()

    print(f"View Gain: {view_gain}")


# --------------------------------------------------
# MAIN
# --------------------------------------------------

if __name__ == "__main__":

    videos = get_database_videos()

    print(f"\nFound {len(videos)} scheduled/tracking videos\n")

    for video in videos:

        video_id = video["video_id"]

        state = should_track(video)

        if state == "scheduled":

            print(f"⏳ Waiting : {video_id}")

            continue

        if state == "completed":

            update_video_status(video_id, "completed")

            print(f"✅ Completed : {video_id}")

            continue

        update_video_status(video_id, "tracking")

        print(f"📡 Tracking : {video_id}")

        data = get_video_details(video_id)

        if not data:
            print("❌ Unable to fetch video")
            continue

        update_video_details(data)

        save_history(data)

        print(f"✅ {data['title']}")
        print("----------------------------------")