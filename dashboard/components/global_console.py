import streamlit as st

from components.command_palette import (
    initialize_command_palette,
    render_command_palette,
)
from operations.session import is_authenticated
from operations.ui.login_dialog import show_login_dialog


def setup_global_console():
    """
    Global router for the Operations Console.
    Call this once on every page.
    """

    # Initialize required session-state keys
    initialize_command_palette()

    # Console closed? Nothing to render.
    if not st.session_state.command_palette_open:
        return

    # Hide Streamlit's native dialog "X" button. It closes the dialog
    # visually but has no way to tell our Python code it was clicked,
    # so command_palette_open never gets reset - meaning the dialog
    # reopens on the very next rerun (e.g. the next auto-refresh).
    # Routing everyone through our own Close/Cancel buttons instead
    # keeps the session state and the visible dialog in sync.
    st.markdown(
        """
        <style>
        div[data-testid="stDialog"] button[aria-label="Close"] {
            display: none !important;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    # Decide what to show.
    if is_authenticated():
        render_command_palette()
    else:
        show_login_dialog()