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
    get_top_videos,
)

from style import load_css
from components.cards import show_overview_cards 
from components.hero import hero_video_card 

st.set_page_config(
    page_title="Overview",
    page_icon="📊",
    layout="wide",
)

load_css()

st.title("📊 YouTube Analytics Dashboard")
st.caption("Real-time performance of all tracked YouTube videos")

# -------------------------------------------------
# LOAD DATA
# -------------------------------------------------

df = load_data()

if df.empty:
    st.warning("No tracking data available.")
    st.stop()

latest = get_latest_data(df)

# -------------------------------------------------
# KPI CARDS
# -------------------------------------------------
show_overview_cards(
    get_total_videos(df),
    get_total_views(df),
    get_total_likes(df),
    get_total_comments(df),
)


st.divider()

# -------------------------------------------------
# DASHBOARD INFO
# -------------------------------------------------

left, right = st.columns([2, 1])

with left:

  st.subheader("🔥 Featured Video")

  top = get_top_growing_video(df)

  hero_video_card(top) 
(
   
        f"""
**{top['video_name']}**

📈 Latest Gain : **+{int(top['view_gain']):,} Views**

👀 Total Views : **{int(top['views']):,}**

❤️ Likes : **{int(top['likes']):,}**

💬 Comments : **{int(top['comments']):,}**
"""
    )

with right:

    st.subheader("📌 Dashboard Summary")

    st.metric(
        "📈 Total View Gain",
        f"{get_total_view_gain(df):,}"
    )

    st.metric(
        "🕒 Last Updated",
        str(get_last_update(df))
    )

st.divider()

# -------------------------------------------------
# TOP VIDEOS
# -------------------------------------------------

st.subheader("🏆 Top Videos")

top_videos = get_top_videos(df)

st.dataframe(
    top_videos[
        [
            "video_name",
            "views",
            "view_gain",
            "likes",
            "comments",
        ]
    ],
    hide_index=True,
    use_container_width=True,
)

st.divider()

# -------------------------------------------------
# LATEST SNAPSHOT
# -------------------------------------------------

st.subheader("📋 Latest Snapshot")

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
    hide_index=True,
    use_container_width=True,
)