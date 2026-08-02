import streamlit as st


def login_user(user):

    st.session_state.logged_in = True
    st.session_state.user = user


def logout():

    st.session_state.clear()


def is_logged_in():

    return st.session_state.get("logged_in", False)


def current_user():

    return st.session_state.get("user")