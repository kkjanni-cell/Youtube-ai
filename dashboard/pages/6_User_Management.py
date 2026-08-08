import streamlit as st
from streamlit_autorefresh import st_autorefresh
st_autorefresh(interval=5000, key="datarefresh")

st.title("👥 User Management")

st.info(
    "User management will be added here."
)