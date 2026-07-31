import sqlite3
import pandas as pd
import os

# -------------------------------------------------------
# DATABASE PATH
# -------------------------------------------------------

BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.dirname(os.path.abspath(__file__))
    )
)

DB_PATH = os.path.join(
    BASE_DIR,
    "database",
    "youtube.db"
)


# -------------------------------------------------------
# LOAD ALL DATA
# -------------------------------------------------------

def load_data():
    """
    Load complete tracking history from SQLite.
    """

    conn = sqlite3.connect(DB_PATH)

    query = """
    SELECT
        video_name,
        timestamp,
        views,
        view_gain,
        likes,
        comments
    FROM view_history
    ORDER BY timestamp
    """

    df = pd.read_sql_query(query, conn)

    conn.close()

    return df


# -------------------------------------------------------
# DASHBOARD METRICS
# -------------------------------------------------------

def get_total_videos(df):
    """Return total unique videos."""
    return df["video_name"].nunique()


def get_total_views(df):
    """Return total latest views across all videos."""

    latest = (
        df.sort_values("timestamp")
        .groupby("video_name")
        .tail(1)
    )

    return int(latest["views"].sum())


def get_total_likes(df):
    """Return total latest likes."""

    latest = (
        df.sort_values("timestamp")
        .groupby("video_name")
        .tail(1)
    )

    return int(latest["likes"].sum())


def get_total_comments(df):
    """Return total latest comments."""

    latest = (
        df.sort_values("timestamp")
        .groupby("video_name")
        .tail(1)
    )

    return int(latest["comments"].sum())


# -------------------------------------------------------
# LATEST DATA
# -------------------------------------------------------

def get_latest_data(df):
    """
    Return only the latest record for each video.
    """

    latest = (
        df.sort_values("timestamp")
        .groupby("video_name")
        .tail(1)
        .sort_values("views", ascending=False)
        .reset_index(drop=True)
    )

    return latest


def get_last_update(df):
    """
    Return timestamp of the newest record.
    """

    return df["timestamp"].max()


def get_top_growing_video(df):
    """
    Return latest record of the fastest growing video.
    """

    latest = get_latest_data(df)

    return latest.sort_values(
        "view_gain",
        ascending=False
    ).iloc[0]


# -------------------------------------------------------
# TODAY'S TOTAL VIEW GAIN
# -------------------------------------------------------

def get_total_view_gain(df):
    """
    Sum of the latest view gain of all videos.
    """

    latest = get_latest_data(df)

    return int(latest["view_gain"].fillna(0).sum())


# -------------------------------------------------------
# TOP VIDEOS
# -------------------------------------------------------

def get_top_videos(df, limit=10):
    """
    Return top videos by latest views.
    """

    latest = get_latest_data(df)

    return latest.head(limit)


# -------------------------------------------------------
# SINGLE VIDEO HISTORY
# -------------------------------------------------------

def get_video_history(df, video_name):
    """
    Return full history for one video.
    """

    return (
        df[df["video_name"] == video_name]
        .sort_values("timestamp")
        .reset_index(drop=True)
    )