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

    Handles:
    - Session state initialization
    - Login dialog
    - Operations console

    This function should be called once on every page.
    """

    initialize_command_palette()

    if not st.session_state.command_palette_open:
        return

    # Consume the trigger immediately so it behaves like
    # a one-shot event instead of a persistent flag.
    st.session_state.command_palette_open = False

    if is_authenticated():
        render_command_palette()
    else:
        show_login_dialog()