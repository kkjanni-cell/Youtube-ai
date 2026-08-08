import streamlit as st
from streamlit_autorefresh import st_autorefresh
st_autorefresh(interval=5000, key="datarefresh")

st.title("🔧 System Settings")

st.info(
    "System settings will be added here."
)