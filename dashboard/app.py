import streamlit as st
import os
print("Running app.py from:", os.path.abspath(__file__))

from style import load_css
from streamlit_autorefresh import st_autorefresh
from components.sidebar import show_sidebar
from components.cards import show_overview_cards
from components.dashboard_summary import dashboard_summary
from components.action_card import action_card
from components.activity_card import activity_card
from components.global_console import setup_global_console
from operations.session import initialize_session
from components.keyboard_shortcuts import keyboard_shortcuts
from services.schedular import start_scheduler

from utils.database import (
    load_data,
    get_total_videos,
    get_total_views,
    get_total_likes,
    get_total_comments,
    get_last_update,
    get_latest_data,
    get_top_growing_video,
    get_total_snapshots,
)


# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="YouTube Analytics",
    page_icon="📺",
    layout="wide",
    initial_sidebar_state="expanded",
)
st_autorefresh(interval=5000, key="datarefresh")
# =========================================================
# LOAD
# =========================================================

load_css()
initialize_session()
# Only run the in-app background tracker when deployed on Render.
# Locally, launchd already handles tracking - running both would
# cause duplicate/conflicting writes.
if os.getenv("RUN_SCHEDULER") == "true":
    start_scheduler()
print("STEP 3")
setup_global_console()
keyboard_shortcuts()
print("STEP 4")
show_sidebar()
print("STEP 5")
df = load_data()
print("STEP 6")

# =========================================================
# HERO
# =========================================================

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

# =========================================================
# LIVE PERFORMANCE
# =========================================================

st.subheader("📊 Live Performance")


if not df.empty:

    show_overview_cards(
        total_videos=get_total_videos(df),
        total_views=get_total_views(df),
        total_likes=get_total_likes(df),
        total_comments=get_total_comments(df),
    )

else:

    st.info("No tracking data available yet.")



# =========================================================
# DASHBOARD OVERVIEW
# =========================================================

st.divider()

st.subheader("📊 Dashboard Overview")


if not df.empty:

    dashboard_summary(
        tracker_status="🟢 Online",
        last_update=get_last_update(df),
        total_snapshots=get_total_snapshots(df),
        top_video=get_top_growing_video(df),
    )


else:

    dashboard_summary(
        tracker_status="🔴 Offline",
        last_update="N/A",
        total_snapshots=0,
        top_video={
            "video_name": "No Data",
            "views": 0,
            "view_gain": 0,
            "likes": 0,
        },
    )



# =========================================================
# QUICK ACTIONS
# =========================================================

st.divider()

st.subheader("⚡ Quick Actions")


c1, c2 = st.columns(2)


with c1:

    action_card(
        "📊",
        "Overview",
        "View overall channel performance, latest statistics and growth trends.",
        "pages/1_Overview.py",
    )


with c2:

    action_card(
        "🎥",
        "Video Analytics",
        "Analyze video views, engagement and growth in detail.",
        "pages/2_Video_Analytics.py",
    )



c3, c4 = st.columns(2)


with c3:

    action_card(
        "📈",
        "Comparison",
        "Compare multiple videos and identify top performers.",
        "pages/3_Comparison.py",
    )


with c4:

    action_card(
        "⚙️",
        "Settings",
        "Manage dashboard preferences and application settings.",
        "pages/4_Settings.py",
    )



# =========================================================
# RECENT ACTIVITY
# =========================================================

st.divider()

st.subheader("🕒 Recent Activity")


if not df.empty:

    latest = (
        get_latest_data(df)
        .sort_values(
            "timestamp",
            ascending=False,
        )
        .head(5)
    )


    for _, row in latest.iterrows():

        activity_card(row)


else:

    st.info("No activity found.")


# =========================================================
# FOOTER
# =========================================================

st.divider()

st.caption("Built by Janni 🚀")