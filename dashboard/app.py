import streamlit as st
from style import load_css

st.set_page_config(
    page_title="YouTube Analytics",
    page_icon="📺",
    layout="wide"
)

load_css()

st.markdown(
    """
<div class="main-title">
📺 YouTube Analytics Platform
</div>

<div class="sub-title">
Professional YouTube analytics with real-time tracking, insights, and growth monitoring.
</div>
""",
    unsafe_allow_html=True,
)

st.markdown("### Welcome 👋")

st.markdown(
    """
Use the navigation menu on the left to explore:

- 🏠 **Overview**
- 📺 **Video Analytics**
- 📊 **Compare Videos**
- ⚙️ **Settings**
"""
)

st.info("👈 Select a page from the sidebar to begin.")