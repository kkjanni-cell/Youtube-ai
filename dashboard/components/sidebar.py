import streamlit as st

from utils.database import (
    load_data,
    get_last_update,
    get_total_videos,
)

from operations.permissions import can
from operations.session import get_session


def show_sidebar():

    with st.sidebar:

        # --------------------------------------------------
        # LOAD DATA
        # --------------------------------------------------

        df = load_data()

        if df.empty:
            status = "🔴 Offline"
            status_class = "offline"
            last_update = "N/A"
            total_videos = 0

        else:
            status = "🟢 Online"
            status_class = "online"
            last_update = get_last_update(df)
            total_videos = get_total_videos(df)


        # --------------------------------------------------
        # OPERATIONS SESSION
        # --------------------------------------------------

        session = get_session()


        # --------------------------------------------------
        # LOGO
        # --------------------------------------------------

        st.markdown(
            """
            <div class="sidebar-logo">
                🎬 <span>YouTube Analytics</span>
            </div>

            <div class="sidebar-subtitle">
                Professional Dashboard
            </div>
            """,
            unsafe_allow_html=True,
        )


        st.markdown("<hr>", unsafe_allow_html=True)


        # --------------------------------------------------
        # USER STATUS
        # --------------------------------------------------

        if session["authenticated"]:

            st.markdown(
                f"""
                <div class="nav-title">
                    👤 {session["full_name"]}
                </div>

                <div class="sidebar-subtitle">
                    Role: {session["role"]}
                </div>
                """,
                unsafe_allow_html=True,
            )

        else:

            st.markdown(
                """
                <div class="sidebar-subtitle">
                    Public Dashboard
                </div>
                """,
                unsafe_allow_html=True,
            )


        st.markdown("<hr>", unsafe_allow_html=True)


        # --------------------------------------------------
        # NAVIGATION
        # --------------------------------------------------

        st.markdown(
            """
            <div class="nav-title">
                Navigation
            </div>
            """,
            unsafe_allow_html=True,
        )


        st.page_link(
            "app.py",
            label="Home",
            icon="🏠",
        )


        st.page_link(
            "pages/1_Overview.py",
            label="Overview",
            icon="📊",
        )


        st.page_link(
            "pages/2_Video_Analytics.py",
            label="Video Analytics",
            icon="🎥",
        )

        st.page_link(
        "pages/8_AI_Prediction.py",
        label="AI Prediction",
        icon="🤖",
        )

        st.page_link(
            "pages/3_Comparison.py",
            label="Comparison",
            icon="📈",
        )


        st.page_link(
            "pages/4_Settings.py",
            label="Settings",
            icon="⚙️",
        )


        # --------------------------------------------------
        # OPERATIONS MENU
        # --------------------------------------------------

        if session["authenticated"]:

            st.markdown("<hr>", unsafe_allow_html=True)

            st.markdown(
                """
                <div class="nav-title">
                    ⚙️ Operations
                </div>
                """,
                unsafe_allow_html=True,
            )


            if can("tracking.create"):

                st.page_link(
                    "pages/5_Tracking_Request.py",
                    label="Tracking Requests",
                    icon="➕",
                )


            if can("users.manage"):

                st.page_link(
                    "pages/6_User_Management.py",
                    label="User Management",
                    icon="👥",
                )


            if can("settings.manage"):

                st.page_link(
                    "pages/7_System_Settings.py",
                    label="System Settings",
                    icon="🔧",
                )


        st.markdown("<hr>", unsafe_allow_html=True)


        # --------------------------------------------------
        # TRACKER STATUS
        # --------------------------------------------------

        st.markdown(
            """
            <div class="nav-title">
                📡 Tracker Status
            </div>
            """,
            unsafe_allow_html=True,
        )


        st.markdown(
f"""
<div class="tracker-card">

<div class="tracker-status {status_class}">
{status}
</div>

<div class="tracker-item">

<div class="tracker-label">
Last Update
</div>

<div class="tracker-value">
{last_update}
</div>

</div>


<div class="tracker-item">

<div class="tracker-label">
Tracked Videos
</div>

<div class="tracker-value">
{total_videos}
</div>

</div>

</div>
""",
unsafe_allow_html=True,
)


        # --------------------------------------------------
        # FOOTER
        # --------------------------------------------------

        st.markdown(
            """
            <div class="sidebar-footer">
                Version 1.0
                <br><br>
                Built by <b>Janni</b> 🚀
            </div>
            """,
            unsafe_allow_html=True,
        )