import streamlit as st
import plotly.express as px


def views_chart(video_df):

    fig = px.line(
        video_df,
        x="timestamp",
        y="views",
        markers=True,
        title="Views Over Time",
    )

    fig.update_layout(
        height=400,
        template="plotly_white",
    )

    st.plotly_chart(fig, use_container_width=True)


def gain_chart(video_df):

    fig = px.bar(
        video_df,
        x="timestamp",
        y="view_gain",
        title="View Gain",
    )

    fig.update_layout(
        height=350,
        template="plotly_white",
    )

    st.plotly_chart(fig, use_container_width=True)


def likes_chart(video_df):

    fig = px.line(
        video_df,
        x="timestamp",
        y="likes",
        markers=True,
        title="Likes",
    )

    fig.update_layout(
        height=350,
        template="plotly_white",
    )

    st.plotly_chart(fig, use_container_width=True)


def comments_chart(video_df):

    fig = px.line(
        video_df,
        x="timestamp",
        y="comments",
        markers=True,
        title="Comments",
    )

    fig.update_layout(
        height=350,
        template="plotly_white",
    )

    st.plotly_chart(fig, use_container_width=True)