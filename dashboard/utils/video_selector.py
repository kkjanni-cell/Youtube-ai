import pandas as pd
import streamlit as st

# Shared key so Video Analytics and AI Prediction stay in sync
# when you navigate between them.
SELECTED_VIDEO_KEY = "global_selected_video"


def _default_video_name(df: pd.DataFrame) -> str:
    """
    The video that started being tracked most recently
    (i.e. the video whose earliest snapshot is the newest
    among all tracked videos).
    """
    timestamps = pd.to_datetime(df["timestamp"])
    starts = timestamps.groupby(df["video_name"]).min()
    return starts.idxmax()


def select_video(df: pd.DataFrame, label: str = "🎥 Select Video") -> str:
    """
    Renders a video selectbox that:
    - defaults to the most recently added tracked video (not
      alphabetically first)
    - stays in sync across every page that calls this same
      function, instead of resetting on navigation
    """

    video_names = sorted(df["video_name"].unique().tolist())

    # Initialize once, or recover if the previously selected video
    # is no longer in the list (e.g. deleted from tracking)
    if (
        SELECTED_VIDEO_KEY not in st.session_state
        or st.session_state[SELECTED_VIDEO_KEY] not in video_names
    ):
        st.session_state[SELECTED_VIDEO_KEY] = _default_video_name(df)

    selected = st.selectbox(
        label,
        video_names,
        key=SELECTED_VIDEO_KEY,
    )

    return selected