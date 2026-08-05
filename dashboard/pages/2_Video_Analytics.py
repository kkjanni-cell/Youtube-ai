import streamlit as st
import pandas as pd

from style import load_css
from components.sidebar import show_sidebar
from utils.database import load_data
from utils.analytics import calculate_metrics

from components.cards import (
    show_kpi_cards,
    show_growth_cards,
)

from components.charts import (
    views_chart,
    gain_chart,
    likes_chart,
    comments_chart,
)
from components.global_console import setup_global_console
from components.keyboard_shortcuts import keyboard_shortcuts

# ----------------------------------------------------
# PAGE CONFIG
# ----------------------------------------------------

st.set_page_config(
    page_title="Video Analytics",
    page_icon="📺",
    layout="wide",
)

load_css()
show_sidebar()
setup_global_console()
keyboard_shortcuts()

st.title("📺 Video Analytics")
st.caption("Analyze the performance of an individual YouTube video")

# ----------------------------------------------------
# LOAD DATA
# ----------------------------------------------------

df = load_data()

if df.empty:
    st.warning("No tracking data available.")
    st.stop()

# ----------------------------------------------------
# FILTERS
# ----------------------------------------------------

st.subheader("🔎 Filters")

col1, col2 = st.columns(2)

with col1:
    selected = st.selectbox(
        "Select Video",
        sorted(df["video_name"].unique())
    )

with col2:
    days = st.selectbox(
        "Time Range",
        [
            "All",
            "Last 24 Hours",
            "Last 7 Days",
            "Last 30 Days",
        ]
    )

# ----------------------------------------------------
# FILTER DATA
# ----------------------------------------------------

video_df = df[df["video_name"] == selected].copy()

video_df["timestamp"] = pd.to_datetime(video_df["timestamp"])

if days == "Last 24 Hours":
    video_df = video_df[
        video_df["timestamp"] >=
        video_df["timestamp"].max() - pd.Timedelta(days=1)
    ]

elif days == "Last 7 Days":
    video_df = video_df[
        video_df["timestamp"] >=
        video_df["timestamp"].max() - pd.Timedelta(days=7)
    ]

elif days == "Last 30 Days":
    video_df = video_df[
        video_df["timestamp"] >=
        video_df["timestamp"].max() - pd.Timedelta(days=30)
    ]

video_df = video_df.sort_values("timestamp")

if video_df.empty:
    st.warning("No data available for the selected time range.")
    st.stop()

# ----------------------------------------------------
# CALCULATE METRICS
# ----------------------------------------------------

metrics = calculate_metrics(video_df)

# ----------------------------------------------------
# KPI CARDS
# ----------------------------------------------------

show_kpi_cards(metrics)

st.divider()

show_growth_cards(metrics)

st.divider()

# ----------------------------------------------------
# MAIN CHART
# ----------------------------------------------------

views_chart(video_df)

st.divider()

# ----------------------------------------------------
# SECOND ROW OF CHARTS
# ----------------------------------------------------

col1, col2 = st.columns(2)

with col1:
    gain_chart(video_df)

with col2:
    likes_chart(video_df)

st.divider()

# ----------------------------------------------------
# COMMENTS CHART
# ----------------------------------------------------

comments_chart(video_df)

st.divider()

# ----------------------------------------------------
# TRACKING HISTORY
# ----------------------------------------------------

st.subheader("📋 Recent Tracking History")

history = video_df.sort_values(
    "timestamp",
    ascending=False
)

st.dataframe(
    history,
    hide_index=True,
    use_container_width=True,
)