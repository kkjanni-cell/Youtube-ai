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

    conn = sqlite3.connect(DB_PATH)

    query = """
    SELECT
        video_id,
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
# TOTAL SNAPSHOTS
# -------------------------------------------------------

def get_total_snapshots(df):
    return len(df)

# -------------------------------------------------------
# METRICS
# -------------------------------------------------------

def get_total_videos(df):
    return df["video_id"].nunique()


def _latest(df):
    return (
        df.sort_values("timestamp")
          .groupby("video_id")
          .tail(1)
    )


def get_total_views(df):
    return int(_latest(df)["views"].sum())


def get_total_likes(df):
    return int(_latest(df)["likes"].sum())


def get_total_comments(df):
    return int(_latest(df)["comments"].sum())


def get_latest_data(df):

    return (
        _latest(df)
        .sort_values("views", ascending=False)
        .reset_index(drop=True)
    )

def get_total_snapshots(df):
    return len(df)

def get_last_update(df):
    return df["timestamp"].max()


def get_top_growing_video(df):
    return (
        get_latest_data(df)
        .sort_values("view_gain", ascending=False)
        .iloc[0]
    )


def get_total_view_gain(df):
    return int(
        get_latest_data(df)["view_gain"]
        .fillna(0)
        .sum()
    )


def get_top_videos(df, limit=5):

    return (
        get_latest_data(df)
        .sort_values("views", ascending=False)
        .head(limit)
    )


def get_video_history(df, video_id):

    return (
        df[df["video_id"] == video_id]
        .sort_values("timestamp")
        .reset_index(drop=True)
    )