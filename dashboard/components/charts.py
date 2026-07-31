import plotly.express as px
import streamlit as st


def plot_views(video_df):
    """
    View growth over time.
    """

    fig = px.line(
        video_df,
        x="timestamp",
        y="views",
        markers=True,
        title="Views Over Time",
    )

    fig.update_layout(
        xaxis_title="Time",
        yaxis_title="Views",
        height=450,
    )

    st.plotly_chart(fig, use_container_width=True)


def plot_view_gain(video_df):
    """
    View gain per tracking interval.
    """

    fig = px.bar(
        video_df,
        x="timestamp",
        y="view_gain",
        title="View Gain",
    )

    fig.update_layout(
        xaxis_title="Time",
        yaxis_title="Views Gained",
        height=450,
    )

    st.plotly_chart(fig, use_container_width=True)


def plot_likes(video_df):
    """
    Likes over time.
    """

    fig = px.line(
        video_df,
        x="timestamp",
        y="likes",
        markers=True,
        title="Likes Over Time",
    )

    fig.update_layout(height=450)

    st.plotly_chart(fig, use_container_width=True)


def plot_comments(video_df):
    """
    Comments over time.
    """

    fig = px.line(
        video_df,
        x="timestamp",
        y="comments",
        markers=True,
        title="Comments Over Time",
    )

    fig.update_layout(height=450)

    st.plotly_chart(fig, use_container_width=True)