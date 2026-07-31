import streamlit as st

st.set_page_config(
    page_title="YouTube Analytics",
    page_icon="📺",
    layout="wide"
)

st.title("📺 YouTube Analytics Platform")

st.markdown(
    """
Welcome to your YouTube Analytics Dashboard.

Use the navigation menu on the left to explore:

- 🏠 Overview
- 📺 Video Analytics
- 📊 Compare Videos
- ⚙️ Settings
"""
)

st.info("Select a page from the sidebar to begin.")