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

    # Decide what to show.
    if is_authenticated():
        render_command_palette()
    else:
        show_login_dialog()