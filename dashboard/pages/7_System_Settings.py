import os
import sqlite3
from pathlib import Path

import streamlit as st
from streamlit_autorefresh import st_autorefresh
st_autorefresh(interval=5000, key="datarefresh")

from style import load_css
from components.sidebar import show_sidebar
from components.global_console import setup_global_console
from components.keyboard_shortcuts import keyboard_shortcuts
from operations.session import get_session
from services.settings_service import (
    get_default_tracking_interval,
    set_default_tracking_interval,
)

st.set_page_config(
    page_title="System Settings",
    page_icon="🛠️",
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

st.title("🛠️ System Settings")
st.caption("App-wide configuration and system health.")

BASE_DIR = Path(__file__).resolve().parent.parent.parent
DB_PATH = BASE_DIR / "database" / "youtube.db"
TRACKER_LOG_PATH = BASE_DIR / "tracker" / "tracker_log.txt"

st.divider()

# =====================================================
# DEFAULT TRACKING INTERVAL
# =====================================================

st.subheader("⏱️ Default Tracking Interval")

current_default = get_default_tracking_interval()

new_default = st.radio(
    "Used to pre-fill the interval when adding a new video",
    options=[1, 5, 10],
    index=[1, 5, 10].index(current_default) if current_default in [1, 5, 10] else 1,
    horizontal=True,
    format_func=lambda x: f"{x} Minute{'s' if x > 1 else ''}",
)

if new_default != current_default:
    if st.button("Save Default Interval"):
        set_default_tracking_interval(new_default)
        st.success(f"Default tracking interval set to {new_default} minutes.")
        st.rerun()

st.divider()

# =====================================================
# API KEY STATUS
# =====================================================

st.subheader("🔑 YouTube API Key")

api_key = os.getenv("YOUTUBE_API_KEY")

if api_key:
    st.success(f"✅ Configured (ends in ...{api_key[-4:]})")
else:
    st.error("❌ Not configured - tracking will fail without this.")

st.divider()

# =====================================================
# TRACKER HEALTH
# =====================================================

st.subheader("📡 Tracker Health")

if TRACKER_LOG_PATH.exists():

    mtime = TRACKER_LOG_PATH.stat().st_mtime
    import datetime as dt
    last_modified = dt.datetime.fromtimestamp(mtime)
    minutes_ago = (dt.datetime.now() - last_modified).total_seconds() / 60

    if minutes_ago < 15:
        st.success(f"🟢 Log last updated {int(minutes_ago)} min ago - tracker appears active")
    else:
        st.warning(f"🟡 Log last updated {int(minutes_ago)} min ago - tracker may be stalled")

    with open(TRACKER_LOG_PATH, "r", errors="replace") as f:
        lines = f.readlines()

    recent_lines = lines[-60:]
    recent_text = "".join(recent_lines)

    has_error = "Traceback" in recent_text or "Error" in recent_text

    if has_error:
        st.error("⚠️ Errors found in recent log output - check details below.")

    with st.expander("View recent log output", expanded=has_error):
        st.code(recent_text or "(log is empty)", language="text")

else:
    st.info("No tracker log file found yet.")

st.divider()

# =====================================================
# DATABASE STATS
# =====================================================

st.subheader("🗄️ Database")

if DB_PATH.exists():

    size_mb = DB_PATH.stat().st_size / (1024 * 1024)

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute("SELECT COUNT(*) FROM videos")
    total_videos = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM view_history")
    total_snapshots = cur.fetchone()[0]

    cur.execute("SELECT MIN(timestamp), MAX(timestamp) FROM view_history")
    oldest, newest = cur.fetchone()

    conn.close()

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Database Size", f"{size_mb:.2f} MB")

    with col2:
        st.metric("Total Videos", total_videos)

    with col3:
        st.metric("Total Snapshots", total_snapshots)

    st.caption(f"Data range: {oldest} → {newest}")

    st.write("")

    with st.expander("⚠️ Danger Zone - Clear All Tracking Data"):

        st.error(
            "This permanently deletes ALL videos and ALL tracking history. "
            "This cannot be undone. Your AI model and comparisons will lose "
            "all training data."
        )

        confirm_text = st.text_input(
            "Type DELETE to confirm",
            key="confirm_clear_data",
        )

        if st.button("🗑️ Permanently Clear All Data", disabled=(confirm_text != "DELETE")):

            conn = sqlite3.connect(DB_PATH)
            cur = conn.cursor()
            cur.execute("DELETE FROM view_history")
            cur.execute("DELETE FROM videos")
            conn.commit()
            conn.close()

            st.success("All tracking data cleared.")
            st.rerun()

else:
    st.warning("Database file not found.")