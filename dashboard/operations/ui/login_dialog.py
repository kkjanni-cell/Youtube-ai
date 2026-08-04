import streamlit as st

from operations.login import login_to_operations


@st.dialog("🔐 Operations Access", width="small")
def show_login_dialog():
    """
    Operations login dialog.
    """

    st.write("Enter your credentials to access the Operations Console.")

    username = st.text_input(
        "Username",
        key="operations_username",
    )

    password = st.text_input(
        "Password",
        type="password",
        key="operations_password",
    )

    col1, col2 = st.columns(2)

    with col1:

        if st.button(
            "Login",
            use_container_width=True,
        ):

            user = login_to_operations(username, password)

            if user:

                st.success("Login successful.")

                st.session_state.command_palette_open = True

                st.rerun()

            else:

                st.error("Invalid username or password.")

    with col2:

        if st.button(
            "Cancel",
            use_container_width=True,
        ):

            st.rerun()