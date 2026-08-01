import streamlit as st
from style import load_css
from components.sidebar import show_sidebar

st.set_page_config(
    page_title="Settings",
    page_icon="⚙️",
    layout="wide"
)

load_css()
show_sidebar()