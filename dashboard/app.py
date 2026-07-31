import streamlit as st
import sqlite3
import pandas as pd
import os


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DB_PATH = os.path.join(
    BASE_DIR,
    "database",
    "youtube.db"
)


def load_data():

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



st.set_page_config(
    page_title="YouTube Tracker",
    layout="wide"
)


st.title("📺 YouTube View Tracker Dashboard")


df = load_data()


if df.empty:

    st.warning("No data available")

    st.stop()



# -----------------------------
# VIDEO FILTER
# -----------------------------

videos = df["video_name"].unique()


selected_video = st.selectbox(
    "Select Video",
    videos
)


video_df = df[
    df["video_name"] == selected_video
]



# -----------------------------
# SUMMARY CARDS
# -----------------------------
# -----------------------------
# SUMMARY CARDS
# -----------------------------

# Convert timestamp to datetime
video_df["timestamp"] = pd.to_datetime(video_df["timestamp"])

# Sort by time
video_df = video_df.sort_values("timestamp")

latest = video_df.iloc[-1]

current_time = latest["timestamp"]

# Last 1 Hour
last_1_hour = video_df[
    video_df["timestamp"] >= current_time - pd.Timedelta(hours=1)
]

last_1_hour_gain = int(last_1_hour["view_gain"].fillna(0).sum())

# Last 24 Hours
last_24_hours = video_df[
    video_df["timestamp"] >= current_time - pd.Timedelta(hours=24)
]

last_24_hour_gain = int(last_24_hours["view_gain"].fillna(0).sum())

# Average hourly growth
total_hours = (
    current_time - video_df["timestamp"].min()
).total_seconds() / 3600

if total_hours > 0:
    avg_hourly_growth = int(
        video_df["view_gain"].fillna(0).sum() / total_hours
    )
else:
    avg_hourly_growth = 0


col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Current Views",
        f"{latest['views']:,}"
    )

with col2:
    st.metric(
        "Last 1 Hour",
        f"{last_1_hour_gain:,}"
    )

with col3:
    st.metric(
        "Last 24 Hours",
        f"{last_24_hour_gain:,}"
    )

with col4:
    st.metric(
        "Avg / Hour",
        f"{avg_hourly_growth:,}"
    )
# -----------------------------
# TABLE
# -----------------------------

st.subheader("Tracking History")

st.dataframe(
    video_df.tail(20),
    width="stretch"
)



# -----------------------------
# CHARTS
# -----------------------------

st.subheader("Views Growth")


views_chart = video_df.set_index(
    "timestamp"
)["views"]


st.line_chart(
    views_chart
)



st.subheader("View Gain")


gain_chart = video_df.set_index(
    "timestamp"
)["view_gain"]


st.bar_chart(
    gain_chart
)