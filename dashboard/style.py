import streamlit as st
from pathlib import Path


def load_css():
    css_folder = Path(__file__).parent / "assets" / "css"

    css = ""

    for file in [
        "base.css",
        "sidebar.css",
        "cards.css",
        "dashboard.css",
        "activity.css",
    ]:
        css += (css_folder / file).read_text(encoding="utf-8")

    st.markdown(
        f"<style>{css}</style>",
        unsafe_allow_html=True,
    )