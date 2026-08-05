import streamlit as st

from operations.login import login_to_operations


@st.dialog("🔐 Operations Login", width="small")
def show_login_dialog():
    """
    Operations login dialog.
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
            use_container_width=True,
        ):

            user = login_to_operations(
                username,
                password,
            )

            if user:

                st.success("Login successful.")

                # Open the console after login
                st.session_state.command_palette_open = True

                st.rerun()

            else:

                st.error(
                    "Invalid username or password."
                )

    with right:

        if st.button(
            "Cancel",
            use_container_width=True,
        ):

            st.session_state.command_palette_open = False

            st.rerun()