import streamlit as st

from auth.auth import authenticate
from auth.session import login_user

from operations.session import login as operations_login


def login_page():

    st.title("📺 YouTube Analytics")

    st.subheader("Login")

    username = st.text_input("Username")

    password = st.text_input(
        "Password",
        type="password"
    )

    if st.button("Login"):

        user = authenticate(
            username,
            password
        )

        if user:

            login_user(user)

            operations_login(user)

            st.success(
                f"Welcome {user['full_name']}!"
            )

            st.rerun()

        else:

            st.error(
                "Invalid username or password."
            )