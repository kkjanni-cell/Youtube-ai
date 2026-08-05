from datetime import datetime

import streamlit as st

from operations.session import (
    get_session,
    is_authenticated,
    logout,
)


def initialize_command_palette():
    """
    Initialize Operations Console state.
    Safe to call multiple times.
    """

    defaults = {
        "command_palette_open": False,
        "show_add_video_form": False,
    }

    for key, value in defaults.items():

        if key not in st.session_state:
            st.session_state[key] = value


@st.dialog("⌘ Operations Console", width="large")
def render_command_palette():
    """
    Operations Console
    """

    if not is_authenticated():

        st.error("Not authenticated.")
        return

    session = get_session()

    st.success(
        f"Welcome, {session['full_name']}"
    )

    st.divider()

    # =====================================================
    # ADD VIDEO
    # =====================================================

    if not st.session_state.show_add_video_form:

        if st.button(
            "➕ Add YouTube Video",
            key="show_add_video",
            width="stretch",
        ):

            st.session_state.show_add_video_form = True
            st.rerun()

    else:

        st.subheader(
            "➕ Add YouTube Video"
        )

        url = st.text_input(
            "YouTube URL or Video ID",
            key="video_url",
            placeholder="https://www.youtube.com/watch?v=dQw4w9WgXcQ",
        )

        st.write(
            "### 🗓 Tracking Schedule"
        )

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
            format_func=lambda x: (
                f"{x} Minute{'s' if x > 1 else ''}"
            ),
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

            st.error(
                "End time must be after the start time."
            )

        save_col, cancel_col = st.columns(2)

        with save_col:

            if st.button(
                "💾 Save Video",
                key="save_video",
                width="stretch",
            ):

                if not url.strip():

                    st.error(
                        "Please enter a YouTube URL or Video ID."
                    )

                elif end_datetime <= start_datetime:

                    st.error(
                        "Please correct the tracking schedule."
                    )

                else:

                    from services.tracking_service import (
                        add_video,
                    )

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

        with cancel_col:

            if st.button(
                "Cancel",
                key="cancel_add_video",
                width="stretch",
            ):

                st.session_state.show_add_video_form = False

                st.rerun()

    # =====================================================
    # REMOVE TRACKING
    # =====================================================

    st.divider()

    if st.button(
        "➖ Remove Tracking",
        key="remove_tracking",
        width="stretch",
    ):

        st.info(
            "Remove Tracking will be implemented in the next step."
        )

    # =====================================================
    # FOOTER
    # =====================================================

    st.divider()

    left, right = st.columns(2)

    with left:

        if st.button(
            "🚪 Logout",
            key="operations_logout",
            width="stretch",
        ):

            logout()

            st.session_state.command_palette_open = False
            st.session_state.show_add_video_form = False

            st.rerun()

    with right:

        if st.button(
            "Close",
            key="close_console",
            width="stretch",
        ):

            st.session_state.command_palette_open = False
            st.session_state.show_add_video_form = False

            st.rerun()