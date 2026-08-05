from __future__ import annotations

import re
import sqlite3
import sys
from datetime import datetime
from pathlib import Path

# ---------------------------------------------------------
# Make the project root importable so that we can import
# modules from the top-level tracker package.
# ---------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[2]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from tracker.youtube_api import get_video_details

DB_PATH = PROJECT_ROOT / "database" / "youtube.db"


def get_connection():
    return sqlite3.connect(DB_PATH)


def extract_video_id(value: str) -> str | None:
    """
    Accepts either:
      - YouTube URL
      - youtu.be URL
      - Raw 11-character video id
    """

    value = value.strip()

    if re.fullmatch(r"[A-Za-z0-9_-]{11}", value):
        return value

    patterns = [
        r"v=([A-Za-z0-9_-]{11})",
        r"youtu\.be/([A-Za-z0-9_-]{11})",
        r"youtube\.com/embed/([A-Za-z0-9_-]{11})",
    ]

    for pattern in patterns:
        match = re.search(pattern, value)

        if match:
            return match.group(1)

    return None


def video_exists(video_id: str) -> bool:

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        "SELECT 1 FROM videos WHERE video_id=?",
        (video_id,),
    )

    exists = cur.fetchone() is not None

    conn.close()

    return exists


def add_video(
    url: str,
    start_time: datetime,
    end_time: datetime,
    tracking_interval: int,
):
    """
    Add a scheduled video to the tracking database.

    Returns:
        (success: bool, message: str)
    """

    video_id = extract_video_id(url)

    if not video_id:
        return False, "Invalid YouTube URL or Video ID."

    if video_exists(video_id):
        return False, "This video is already being tracked."

    if end_time <= start_time:
        return False, "End time must be after start time."

    details = get_video_details(video_id)

    if not details:
        return False, "Unable to fetch video details."

    now = datetime.now().isoformat(timespec="seconds")

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        INSERT INTO videos (
            video_id,
            video_name,
            start_time,
            end_time,
            tracking_interval,
            status,
            created_at,
            updated_at
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            video_id,
            details["title"],
            start_time.isoformat(timespec="seconds"),
            end_time.isoformat(timespec="seconds"),
            tracking_interval,
            "scheduled",
            now,
            now,
        ),
    )

    conn.commit()
    conn.close()

    return (
        True,
        f"'{details['title']}' scheduled successfully.",
    )