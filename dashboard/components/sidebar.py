import streamlit as st

from utils.database import (
    load_data,
    get_last_update,
    get_total_videos,
)


def show_sidebar():

    with st.sidebar:

        st.markdown("# 📺 YouTube Analytics")
        st.caption("Professional Dashboard")

        st.divider()

        # -----------------------------
        # Tracker Status
        # -----------------------------

        df = load_data()


        if df.empty:
            st.error("🔴 Tracker Offline")
            last_update = "N/A"
            total_videos = 0
        else:
            st.success("🟢 Tracker Online")
            last_update = get_last_update(df)
            total_videos = get_total_videos(df)

        st.caption("Last Update")
        st.write(last_update)

        st.caption("Tracked Videos")
        st.write(f"**{total_videos}**")

        st.divider()

        # -----------------------------
        # Navigation
        # -----------------------------

        st.markdown("### Navigation")

        st.page_link(
            "app.py",
            label="Home",
            icon="🏠",
        )

        st.page_link(
            "pages/1_Overview.py",
            label="Overview",
            icon="📈",
        )

        st.page_link(
            "pages/2_Video_Analytics.py",
            label="Video Analytics",
            icon="🎥",
        )

        st.page_link(
            "pages/3_Comparison.py",
            label="Comparison",
            icon="📊",
        )

        st.page_link(
            "pages/4_Settings.py",
            label="Settings",
            icon="⚙️",
        )

        st.divider()

        st.caption("Version 1.0")
        st.caption("Built by Janni 🚀")