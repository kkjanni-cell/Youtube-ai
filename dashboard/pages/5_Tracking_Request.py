from datetime import datetime

import streamlit as st
from streamlit_autorefresh import st_autorefresh
st_autorefresh(interval=5000, key="datarefresh")

from style import load_css
from components.sidebar import show_sidebar
from components.global_console import setup_global_console
from components.keyboard_shortcuts import keyboard_shortcuts
from operations.session import get_session
from services.tracking_service import add_video, get_all_videos, stop_tracking
from services.settings_service import get_default_tracking_interval
default_interval = get_default_tracking_interval()

st.set_page_config(
    page_title="Tracking Requests",
    page_icon="➕",
    layout="wide",
)

load_css()
show_sidebar()
setup_global_console()
keyboard_shortcuts()

# =====================================================
# ADMIN GATE
# =====================================================

session = get_session()

if not session.get("authenticated") or session.get("role") != "Admin":
    st.warning("You need Admin access to view this page.")
    st.stop()

st.title("➕ Tracking Requests")
st.caption("Add new videos to track, or stop tracking existing ones.")

st.divider()

# =====================================================
# ADD VIDEO
# =====================================================

st.subheader("➕ Add a Video")

with st.form("add_video_form"):

    url = st.text_input(
        "YouTube URL or Video ID",
        placeholder="https://www.youtube.com/watch?v=dQw4w9WgXcQ",
    )

    st.write("**🗓 Tracking Schedule**")

    left, right = st.columns(2)

    with left:
        start_date = st.date_input(
            "Start Date", value=datetime.now().date()
        )
        start_time_input = st.time_input(
            "Start Time",
            value=datetime.now().replace(second=0, microsecond=0).time(),
        )

    with right:
        end_date = st.date_input(
            "End Date", value=datetime.now().date()
        )
        end_time_input = st.time_input(
            "End Time",
            value=datetime.now().replace(second=0, microsecond=0).time(),
        )

    interval = st.radio(
        "Tracking Interval",
        options=[1, 5, 10],
        index=[1, 5, 10].index(default_interval),
        horizontal=True,
        format_func=lambda x: f"{x} Minute{'s' if x > 1 else ''}",
    )

    submitted = st.form_submit_button("💾 Save Video", width="stretch")

    if submitted:

        start_datetime = datetime.combine(start_date, start_time_input)
        end_datetime = datetime.combine(end_date, end_time_input)

        if not url.strip():
            st.error("Please enter a YouTube URL or Video ID.")

        elif end_datetime <= start_datetime:
            st.error("End time must be after the start time.")

        else:
            success, message = add_video(
                url=url,
                start_time=start_datetime,
                end_time=end_datetime,
                tracking_interval=interval,
            )

            if success:
                st.success(message)
                st.rerun()
            else:
                st.error(message)

st.divider()

# =====================================================
# CURRENT TRACKING REQUESTS
# =====================================================

st.subheader("📋 All Tracking Requests")

videos = get_all_videos()

if not videos:
    st.info("No videos have been added yet.")
    st.stop()

status_icons = {
    "scheduled": "🟡 Scheduled",
    "tracking": "🟢 Tracking",
    "completed": "⚪ Completed",
    "stopped": "🔴 Stopped",
}

filter_options = ["All"] + sorted(
    set(v["status"] for v in videos)
)

status_filter = st.selectbox("Filter by status", filter_options)

for video in videos:

    if status_filter != "All" and video["status"] != status_filter:
        continue

    with st.container(border=True):

        col1, col2, col3, col4 = st.columns([3, 2, 2, 1])

        with col1:
            st.markdown(f"**{video['video_name'] or video['video_id']}**")
            st.caption(video["video_id"])

        with col2:
            st.write(
                status_icons.get(video["status"], video["status"])
            )
            st.caption(f"Every {video['tracking_interval']} min")

        with col3:
            st.caption(f"Start: {video['start_time']}")
            st.caption(f"End: {video['end_time']}")

        with col4:
            if video["status"] in ("scheduled", "tracking"):
                if st.button(
                    "Stop",
                    key=f"stop_{video['video_id']}",
                    width="stretch",
                ):
                    success, message = stop_tracking(video["video_id"])
                    if success:
                        st.success(message)
                    else:
                        st.error(message)
                    st.rerun()