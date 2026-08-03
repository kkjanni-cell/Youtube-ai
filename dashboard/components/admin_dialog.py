import streamlit as st

from operations.login import login_to_operations


@st.dialog("🔒 Admin Access", width="small")
def show_admin_dialog():
    """
    Native Streamlit Operations Login Dialog.
    """

    st.markdown(
        """
Welcome to the YouTube Analytics Platform.

Please sign in with your administrator credentials.
"""
    )

    username = st.text_input(
        "Username",
        key="dialog_username",
    )

    password = st.text_input(
        "Password",
        type="password",
        key="dialog_password",
    )

    col1, col2 = st.columns(2)

    with col1:
        if st.button(
            "Login",
            use_container_width=True,
        ):
            user = login_to_operations(
                username,
                password,
            )

            if user:
                st.session_state.command_palette_open = True
                st.success("Login successful.")
                st.rerun()
            else:
                st.error("Invalid username or password.")

    with col2:
        st.button(
            "Cancel",
            use_container_width=True,
        )