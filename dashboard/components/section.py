import streamlit as st


def section_header(title: str, subtitle: str = ""):
    st.markdown(f"## {title}")

    if subtitle:
        st.caption(subtitle)

    st.write("")