import streamlit as st
from style import load_css
from components.sidebar import show_sidebar
from components.global_console import setup_global_console
from components.keyboard_shortcuts import keyboard_shortcuts

st.set_page_config(
    page_title="Settings",
    page_icon="⚙️",
    layout="wide"
)

load_css()
show_sidebar()
setup_global_console()
keyboard_shortcuts()