import streamlit as st

from utils.database import (
    load_data,
    get_total_videos,
    get_total_views,
    get_total_likes,
    get_total_comments,
    get_total_view_gain,
    get_last_update,
    get_top_growing_video,
    get_latest_data,
)

from style import load_css

st.set_page_config(
    page_title="Overview",
    page_icon="📊",
    layout="wide"
)

load_css()

st.title("📊 YouTube Analytics Platform")
st.caption("Overall performance of all tracked videos")

# ---------------------------------
# LOAD DATA
# ---------------------------------

df = load_data()

if df.empty:
    st.warning("No tracking data available.")
    st.stop()

# ---------------------------------
# SUMMARY METRICS
# ---------------------------------

total_videos = get_total_videos(df)
total_views = get_total_views(df)
total_likes = get_total_likes(df)
total_comments = get_total_comments(df)

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("🎥 Videos Tracked", total_videos)

with col2:
    st.metric("👀 Total Views", f"{total_views:,}")

with col3:
    st.metric("❤️ Total Likes", f"{total_likes:,}")

with col4:
    st.metric("💬 Total Comments", f"{total_comments:,}")

st.divider()

# ---------------------------------
# SECOND ROW
# ---------------------------------

col1, col2 = st.columns([2, 1])

with col1:

    latest = get_latest_data(df)

    st.subheader("📋 Latest Video Statistics")

    st.dataframe(
        latest[
            [
                "video_name",
                "views",
                "view_gain",
                "likes",
                "comments",
                "timestamp",
            ]
        ],
        use_container_width=True,
        hide_index=True,
    )

with col2:

    st.subheader("📌 Dashboard Summary")

    st.metric(
        "📈 Total View Gain",
        f"{get_total_view_gain(df):,}"
    )

    top = get_top_growing_video(df)

    st.metric(
        "🚀 Top Growing Video",
        top["video_name"],
        delta=f'+{int(top["view_gain"]):,}'
    )

    st.metric(
        "🕒 Last Updated",
        str(get_last_update(df))
    )