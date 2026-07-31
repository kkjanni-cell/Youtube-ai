import streamlit as st

from style import load_css

from utils.database import load_data
from utils.analytics import calculate_metrics

from components.cards import (
    show_kpi_cards,
    show_growth_cards,
)

from components.charts import (
    plot_views,
    plot_view_gain,
    plot_likes,
    plot_comments,
)

st.set_page_config(
    page_title="Video Analytics",
    page_icon="📺",
    layout="wide"
)

load_css()

st.title("📺 Video Analytics")

# ------------------------------------------------
# LOAD DATA
# ------------------------------------------------

df = load_data()

if df.empty:
    st.warning("No tracking data available.")
    st.stop()

# ------------------------------------------------
# VIDEO SELECTOR
# ------------------------------------------------

videos = sorted(df["video_name"].unique())

selected_video = st.selectbox(
    "Select Video",
    videos
)

video_df = (
    df[df["video_name"] == selected_video]
    .copy()
)

metrics = calculate_metrics(video_df)

# ------------------------------------------------
# KPI CARDS
# ------------------------------------------------

show_kpi_cards(metrics)

st.divider()

# ------------------------------------------------
# GROWTH CARDS
# ------------------------------------------------

show_growth_cards(metrics)

st.divider()

# ------------------------------------------------
# CHARTS
# ------------------------------------------------

tab1, tab2, tab3, tab4 = st.tabs(
    [
        "📈 Views",
        "📊 View Gain",
        "❤️ Likes",
        "💬 Comments",
    ]
)

with tab1:
    plot_views(video_df)

with tab2:
    plot_view_gain(video_df)

with tab3:
    plot_likes(video_df)

with tab4:
    plot_comments(video_df)

st.divider()

# ------------------------------------------------
# DATA TABLE
# ------------------------------------------------

st.subheader("Tracking History")

st.dataframe(
    video_df.sort_values(
        "timestamp",
        ascending=False
    ),
    use_container_width=True,
    hide_index=True,
)