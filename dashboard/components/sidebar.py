import streamlit as st


def show_sidebar():
    with st.sidebar:
        st.markdown("# 📺 YouTube Analytics")
        st.caption("Professional Dashboard")

        st.divider()

        st.markdown("### 📊 Navigation")
        st.page_link("app.py", label="Home", icon="🏠")
        st.page_link("pages/1_Overview.py", label="Overview", icon="📈")
        st.page_link("pages/2_Video_Analytics.py", label="Video Analytics", icon="🎥")
        st.page_link("pages/3_Comparison.py", label="Comparison", icon="📊")
        st.page_link("pages/4_Settings.py", label="Settings", icon="⚙️")

        st.divider()

        st.markdown("### 📌 Project")
        st.write("Version **1.0**")
        st.caption("Built by Janni 🚀")