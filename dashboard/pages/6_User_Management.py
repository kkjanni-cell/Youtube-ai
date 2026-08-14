import streamlit as st
from streamlit_autorefresh import st_autorefresh
st_autorefresh(interval=5000, key="datarefresh")

from style import load_css
from components.sidebar import show_sidebar
from components.global_console import setup_global_console
from components.keyboard_shortcuts import keyboard_shortcuts
from operations.session import get_session
from services.user_service import (
    get_all_users,
    create_user,
    set_user_active,
    update_user_role,
    admin_reset_password,
)

st.set_page_config(
    page_title="User Management",
    page_icon="👥",
    layout="wide",
)

load_css()
show_sidebar()
setup_global_console()
keyboard_shortcuts()

# =====================================================
# ADMIN GATE
# =====================================================

session = get_session()

if not session.get("authenticated") or session.get("role") != "Admin":
    st.warning("You need Admin access to view this page.")
    st.stop()

current_username = session["username"]

st.title("👥 User Management")
st.caption("Manage who has access to this dashboard.")

st.divider()

# =====================================================
# ADD USER
# =====================================================

st.subheader("➕ Add User")

with st.form("add_user_form"):

    col1, col2 = st.columns(2)

    with col1:
        new_username = st.text_input("Username")
        new_full_name = st.text_input("Full Name")

    with col2:
        new_password = st.text_input("Password", type="password")
        new_role = st.selectbox("Role", ["Viewer", "Admin"])

    submitted = st.form_submit_button("💾 Create User", width="stretch")

    if submitted:
        success, message = create_user(
            new_username, new_password, new_full_name, new_role
        )
        if success:
            st.success(message)
            st.rerun()
        else:
            st.error(message)

st.divider()

# =====================================================
# ALL USERS
# =====================================================

st.subheader("📋 All Users")

users = get_all_users()

for user in users:

    is_self = user["username"] == current_username

    with st.container(border=True):

        col1, col2, col3, col4 = st.columns([2, 2, 2, 2])

        with col1:
            label = user["full_name"] or user["username"]
            if is_self:
                label += " (you)"
            st.markdown(f"**{label}**")
            st.caption(f"@{user['username']}")

        with col2:
            status = "🟢 Active" if user["active"] else "⚪ Inactive"
            st.write(status)
            st.caption(f"Joined: {user['created_at']}")

        with col3:
            new_role_value = st.selectbox(
                "Role",
                ["Viewer", "Admin"],
                index=0 if user["role"] == "Viewer" else 1,
                key=f"role_{user['username']}",
                label_visibility="collapsed",
                disabled=is_self,
            )

            if new_role_value != user["role"] and not is_self:
                if st.button(
                    "Save Role",
                    key=f"save_role_{user['username']}",
                    width="stretch",
                ):
                    success, message = update_user_role(
                        user["username"], new_role_value
                    )
                    if success:
                        st.success(message)
                    else:
                        st.error(message)
                    st.rerun()

        with col4:

            btn_col1, btn_col2 = st.columns(2)

            with btn_col1:
                toggle_label = "Deactivate" if user["active"] else "Activate"
                if st.button(
                    toggle_label,
                    key=f"toggle_{user['username']}",
                    width="stretch",
                    disabled=is_self,
                ):
                    success, message = set_user_active(
                        user["username"], not user["active"]
                    )
                    if success:
                        st.success(message)
                    else:
                        st.error(message)
                    st.rerun()

            with btn_col2:
                if st.button(
                    "Reset PW",
                    key=f"reset_pw_btn_{user['username']}",
                    width="stretch",
                ):
                    st.session_state[f"show_reset_{user['username']}"] = True

        if st.session_state.get(f"show_reset_{user['username']}"):

            with st.form(f"reset_form_{user['username']}"):

                st.write(f"Reset password for **{user['username']}**")

                new_pw = st.text_input(
                    "New Password",
                    type="password",
                    key=f"new_pw_{user['username']}",
                )

                reset_submitted = st.form_submit_button("Confirm Reset")

                if reset_submitted:
                    success, message = admin_reset_password(
                        user["username"], new_pw
                    )
                    if success:
                        st.success(message)
                        st.session_state[f"show_reset_{user['username']}"] = False
                        st.rerun()
                    else:
                        st.error(message)

        if is_self:
            st.caption(
                "⚠️ You can't change your own role or deactivate your own account, "
                "to avoid accidentally locking yourself out."
            )