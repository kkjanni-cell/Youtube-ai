import streamlit as st

from services.tracking_service import add_video


@st.dialog("➕ Add YouTube Video", width="large")
def show_add_video_dialog():
    """
    Dialog for adding a new YouTube video to tracking.
    """

    st.write(
        "Paste a YouTube URL or an 11-character Video ID."
    )

    url = st.text_input(
        "YouTube URL or Video ID",
        placeholder="https://www.youtube.com/watch?v=dQw4w9WgXcQ",
    )

    col1, col2 = st.columns(2)

    with col1:
        if st.button("Add Video", use_container_width=True):

            if not url.strip():
                st.warning("Please enter a YouTube URL or Video ID.")
                return

            with st.spinner("Fetching video details..."):
                success, message = add_video(url)

            if success:
                st.success(message)

                st.balloons()

                # Refresh app so new video appears
                st.rerun()

            else:
                st.error(message)

    with col2:
        if st.button("Cancel", use_container_width=True):
            st.rerun()