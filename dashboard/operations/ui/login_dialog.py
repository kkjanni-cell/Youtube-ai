import streamlit as st

from operations.login import login_to_operations


@st.dialog("🔐 Operations Login", width="small")
def show_login_dialog():
    """
    Operations login dialog.
    Responsible only for authentication.
    """

    st.write(
        "Please log in to access the Operations Console."
    )

    username = st.text_input(
        "Username",
        key="operations_username",
    )

    password = st.text_input(
        "Password",
        type="password",
        key="operations_password",
    )

    left, right = st.columns(2)

    with left:

        if st.button(
            "🔐 Login",
            key="operations_login_button",
            width="stretch",
        ):

            user = login_to_operations(
                username,
                password,
            )

            if user:

                st.success(
                    "Login successful."
                )

                # Don't change command_palette_open here.
                # global_console.py will automatically
                # render the Operations Console because
                # it is still True.
                st.rerun()

            else:

                st.error(
                    "Invalid username or password."
                )

    with right:

        if st.button(
            "Cancel",
            key="operations_cancel_button",
            width="stretch",
        ):

            st.session_state.command_palette_open = False

            st.rerun()