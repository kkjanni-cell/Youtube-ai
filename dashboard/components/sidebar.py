import streamlit as st
from datetime import datetime


def show_sidebar():

    with st.sidebar:

        st.markdown(
            """
            <h2 style="margin-bottom:0;">
                📺 YouTube Analytics
            </h2>

            <p style="color:#888;margin-top:0;">
                Professional Dashboard
            </p>
            """,
            unsafe_allow_html=True,
        )

        st.divider()

        st.markdown("### 🧭 Navigation")

        st.page_link("app.py", label="Home", icon="🏠")
        st.page_link("pages/1_Overview.py", label="Overview", icon="📈")
        st.page_link("pages/2_Video_Analytics.py", label="Video Analytics", icon="🎥")
        st.page_link("pages/3_Comparison.py", label="Comparison", icon="📊")
        st.page_link("pages/4_Settings.py", label="Settings", icon="⚙️")

        st.divider()

        st.markdown("### 📡 Tracker Status")

        st.success("🟢 Running")

        st.caption(
            f"Last Opened\n\n{datetime.now().strftime('%d %b %Y, %I:%M %p')}"
        )

        st.divider()

        st.markdown("### 📊 Dashboard")

        c1, c2 = st.columns(2)

        with c1:
            st.metric("Pages", "4")

        with c2:
            st.metric("Version", "1.0")

        st.divider()

        st.markdown(
            """
            <div style="text-align:center;color:#888;font-size:13px;">
            Built with ❤️ using Streamlit
            <br><br>
            <b>By Janni 🚀</b>
            </div>
            """,
            unsafe_allow_html=True,
        )