from datetime import datetime

import streamlit as st

from operations.session import (
    get_session,
    is_authenticated,
    logout,
)


def initialize_command_palette():
    if "command_palette_open" not in st.session_state:
        st.session_state.command_palette_open = False

    if "show_add_video_form" not in st.session_state:
        st.session_state.show_add_video_form = False


@st.dialog("⌘ Operations Console", width="large")
def render_command_palette():
    """
    Operations Console
    """

    if not st.session_state.command_palette_open:
        return

    if not is_authenticated():
        st.warning("Please log in first.")
        return

    session = get_session()

    st.success(f"Welcome, {session['full_name']}")

    st.divider()

    # =====================================================
    # ADD VIDEO
    # =====================================================

    if st.button(
        "➕ Add YouTube Video",
        use_container_width=True,
    ):
        st.session_state.show_add_video_form = True

    if st.session_state.show_add_video_form:

        st.divider()

        st.subheader("➕ Add YouTube Video")

        url = st.text_input(
            "YouTube URL or Video ID",
            key="new_video_url",
            placeholder="https://www.youtube.com/watch?v=dQw4w9WgXcQ",
        )

        st.write("### 🗓 Tracking Schedule")

        left, right = st.columns(2)

        with left:

            start_date = st.date_input(
                "Start Date",
                value=datetime.now().date(),
                key="track_start_date",
            )

            start_time = st.time_input(
                "Start Time",
                value=datetime.now().replace(
                    second=0,
                    microsecond=0,
                ).time(),
                key="track_start_time",
            )

        with right:

            end_date = st.date_input(
                "End Date",
                value=datetime.now().date(),
                key="track_end_date",
            )

            end_time = st.time_input(
                "End Time",
                value=datetime.now().replace(
                    second=0,
                    microsecond=0,
                ).time(),
                key="track_end_time",
            )

        interval = st.radio(
            "Tracking Interval",
            options=[1, 5, 10],
            index=1,
            horizontal=True,
            format_func=lambda x: f"{x} Minute{'s' if x > 1 else ''}",
            key="tracking_interval",
        )

        start_datetime = datetime.combine(
            start_date,
            start_time,
        )

        end_datetime = datetime.combine(
            end_date,
            end_time,
        )

        if end_datetime <= start_datetime:
            st.error("End time must be after the start time.")

        col1, col2 = st.columns(2)

        with col1:

            if st.button(
                "💾 Save Video",
                use_container_width=True,
            ):

                if not url.strip():

                    st.error("Please enter a YouTube URL or Video ID.")

                elif end_datetime <= start_datetime:

                    st.error("Please correct the schedule.")

                else:

                    from services.tracking_service import add_video

                    success, message = add_video(
                        url=url,
                        start_time=start_datetime,
                        end_time=end_datetime,
                        tracking_interval=interval,
                    )

                    if success:

                        st.success(message)

                        st.session_state.show_add_video_form = False

                        st.rerun()

                    else:

                        st.error(message)

        with col2:

            if st.button(
                "Cancel",
                use_container_width=True,
            ):

                st.session_state.show_add_video_form = False

                st.rerun()

    # =====================================================
    # REMOVE TRACKING
    # =====================================================

    st.divider()

    if st.button(
        "➖ Remove Tracking",
        use_container_width=True,
    ):
        st.info("Coming in the next step.")

    # =====================================================
    # LOGOUT
    # =====================================================

    st.divider()

    if st.button(
        "🚪 Logout",
        use_container_width=True,
    ):

        logout()

        st.session_state.command_palette_open = False
        st.session_state.show_add_video_form = False

        st.rerun()