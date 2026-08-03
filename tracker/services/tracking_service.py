import sqlite3
from pathlib import Path

from tracker.youtube_api import get_video_details


BASE_DIR = Path(__file__).resolve().parents[2]
DB_PATH = BASE_DIR / "database" / "youtube.db"


def get_connection():
    return sqlite3.connect(DB_PATH)


def video_exists(video_id: str) -> bool:
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT 1
        FROM videos
        WHERE video_id = ?
        """,
        (video_id,),
    )

    exists = cursor.fetchone() is not None

    conn.close()

    return exists


def add_video(video_id: str):
    """
    Add a video to tracking.
    """

    details = get_video_details(video_id)

    if details is None:
        return False, "Unable to fetch video."

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO videos(video_id, video_name)
        VALUES(?, ?)
        ON CONFLICT(video_id)
        DO UPDATE SET
            video_name = excluded.video_name
        """,
        (
            video_id,
            details["title"],
        ),
    )

    conn.commit()
    conn.close()

    return True, details