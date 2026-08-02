import streamlit as st


DEFAULT_SESSION = {
    "authenticated": False,
    "username": None,
    "full_name": None,
    "role": "Viewer",
}


def initialize_session():
    """
    Initialize the Operations Session.
    Safe to call multiple times.
    """

    if "operations" not in st.session_state:
        st.session_state.operations = DEFAULT_SESSION.copy()


def get_session():
    """
    Return the current Operations Session.
    """

    initialize_session()
    return st.session_state.operations


def login(user: dict):
    """
    Populate the Operations Session after authentication.
    """

    st.session_state.operations = {
        "authenticated": True,
        "username": user["username"],
        "full_name": user["full_name"],
        "role": user["role"],
    }


def logout():
    """
    Reset the Operations Session.
    """

    st.session_state.operations = DEFAULT_SESSION.copy()


def is_authenticated() -> bool:
    """
    Return True if the user is authenticated.
    """

    return get_session()["authenticated"]