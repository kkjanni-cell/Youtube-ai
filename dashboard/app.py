import streamlit as st

from style import load_css

from components.sidebar import show_sidebar
from components.cards import show_overview_cards

from utils.database import (
    load_data,
    get_total_videos,
    get_total_views,
    get_total_likes,
    get_total_comments,
    get_last_update,
    get_latest_data,
)


# ---------------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------------

st.set_page_config(
    page_title="YouTube Analytics",
    page_icon="📺",
    layout="wide",
)


# ---------------------------------------------------------
# LOAD
# ---------------------------------------------------------

load_css()
show_sidebar()

df = load_data()


# ---------------------------------------------------------
# HERO
# ---------------------------------------------------------

st.markdown(
    """
<div class="hero-title">
📺 YouTube Analytics Platform
</div>

<div class="hero-subtitle">
Track your YouTube videos with real-time analytics,
growth insights, and performance trends —
all in one professional dashboard.
</div>
""",
    unsafe_allow_html=True,
)


st.write("")


# ---------------------------------------------------------
# LIVE KPI
# ---------------------------------------------------------

st.subheader("📊 Live Performance")


if not df.empty:

    show_overview_cards(
        get_total_videos(df),
        get_total_views(df),
        get_total_likes(df),
        get_total_comments(df),
    )

else:

    st.info(
        "No tracking data available yet."
    )


# ---------------------------------------------------------
# TRACKER STATUS
# ---------------------------------------------------------

st.divider()

st.subheader("📈 Tracker Activity")


a, b = st.columns(2)


with a:

    if not df.empty:

        st.success(
            f"""
            Last Update

            {get_last_update(df)}
            """
        )

    else:

        st.warning(
            "No data available"
        )


with b:

    st.success(
        """
        🟢 Tracker Status

        Tracking system is active
        """
    )


# ---------------------------------------------------------
# QUICK ACCESS
# ---------------------------------------------------------

st.divider()

st.subheader("🚀 Quick Navigation")


c1, c2 = st.columns(2)


with c1:

    st.info(
        """
### 📊 Overview

View overall channel performance,
top videos, latest snapshots,
and growth statistics.
"""
    )


with c2:

    st.info(
        """
### 🎥 Video Analytics

Deep dive into a video's
views, likes, comments,
and growth trends.
"""
    )


c3, c4 = st.columns(2)


with c3:

    st.info(
        """
### 📈 Comparison

Compare multiple videos
side-by-side and identify
top performers.
"""
    )


with c4:

    st.info(
        """
### ⚙️ Settings

Configure your dashboard,
API settings,
and preferences.
"""
    )


# ---------------------------------------------------------
# RECENT ACTIVITY
# ---------------------------------------------------------

st.divider()

st.subheader("📋 Recent Activity")


if not df.empty:

    recent = get_latest_data(df).head(5)


    st.dataframe(
        recent[
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


else:

    st.info(
        "No recent activity available"
    )


# ---------------------------------------------------------
# FOOTER
# ---------------------------------------------------------

st.divider()

st.caption(
    "Built by Janni 🚀"
)