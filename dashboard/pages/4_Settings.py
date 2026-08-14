import sqlite3
import os

import bcrypt
import streamlit as st
from streamlit_autorefresh import st_autorefresh
st_autorefresh(interval=5000, key="datarefresh")

from style import load_css
from components.sidebar import show_sidebar
from components.global_console import setup_global_console
from components.keyboard_shortcuts import keyboard_shortcuts
from operations.session import get_session
from auth.auth import authenticate

st.set_page_config(
    page_title="Settings",
    page_icon="⚙️",
    layout="wide"
)

load_css()
show_sidebar()
setup_global_console()
keyboard_shortcuts()

st.title("⚙️ Settings")
st.caption("Manage your account and personal dashboard preferences.")

# =====================================================
# DB PATH (matches the rest of the app's convention)
# =====================================================

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DB_PATH = os.path.join(BASE_DIR, "database", "youtube.db")


def get_connection():
    return sqlite3.connect(DB_PATH)


# =====================================================
# CURRENT USER
# =====================================================

session = get_session()

if not session.get("authenticated"):
    st.warning("You need to be logged in to view settings.")
    st.stop()

username = session["username"]

st.divider()

# =====================================================
# ACCOUNT SETTINGS
# =====================================================

st.subheader("👤 Account")

col1, col2 = st.columns(2)

with col1:
    st.text_input("Username", value=username, disabled=True)

with col2:
    st.text_input("Role", value=session["role"], disabled=True)

with st.form("update_profile_form"):

    new_full_name = st.text_input(
        "Full Name",
        value=session.get("full_name", ""),
    )

    profile_submitted = st.form_submit_button("Save Profile")

    if profile_submitted:

        if not new_full_name.strip():
            st.error("Full name cannot be empty.")
        else:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE users SET full_name = ? WHERE username = ?",
                (new_full_name.strip(), username),
            )
            conn.commit()
            conn.close()

            session["full_name"] = new_full_name.strip()

            st.success("Profile updated.")
            st.rerun()

st.divider()

# =====================================================
# CHANGE PASSWORD
# =====================================================

st.subheader("🔒 Change Password")

with st.form("change_password_form"):

    current_password = st.text_input(
        "Current Password", type="password"
    )
    new_password = st.text_input(
        "New Password", type="password"
    )
    confirm_password = st.text_input(
        "Confirm New Password", type="password"
    )

    password_submitted = st.form_submit_button("Update Password")

    if password_submitted:

        if not current_password or not new_password or not confirm_password:
            st.error("Please fill in all password fields.")

        elif not authenticate(username, current_password):
            st.error("Current password is incorrect.")

        elif len(new_password) < 8:
            st.error("New password must be at least 8 characters.")

        elif new_password != confirm_password:
            st.error("New password and confirmation do not match.")

        else:
            new_hash = bcrypt.hashpw(
                new_password.encode(), bcrypt.gensalt()
            ).decode()

            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE users SET password_hash = ? WHERE username = ?",
                (new_hash, username),
            )
            conn.commit()
            conn.close()

            st.success("Password updated successfully.")

st.divider()

# =====================================================
# DASHBOARD PREFERENCES
# =====================================================

st.subheader("🖥️ Dashboard Preferences")

refresh_options = {
    "3 seconds": 3000,
    "5 seconds (default)": 5000,
    "10 seconds": 10000,
    "30 seconds": 30000,
}

current_interval = st.session_state.get("refresh_interval_ms", 5000)
current_label = next(
    (label for label, ms in refresh_options.items() if ms == current_interval),
    "5 seconds (default)",
)

selected_label = st.selectbox(
    "Auto-Refresh Rate",
    list(refresh_options.keys()),
    index=list(refresh_options.keys()).index(current_label),
)

st.session_state["refresh_interval_ms"] = refresh_options[selected_label]

st.caption(
    "⚠️ Not yet active: this preference is saved but not yet applied to "
    "page refresh timing. All pages still refresh every 5 seconds regardless "
    "of this setting, until this is wired in."
)