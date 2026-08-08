import streamlit as st
from streamlit_autorefresh import st_autorefresh
st_autorefresh(interval=5000, key="datarefresh")

st.title("➕ Tracking Requests")

st.info(
    "Tracking Request management will be added here."
)