import streamlit as st
import plotly.express as px
import plotly.graph_objects as go


# ==========================================================
# OVERVIEW DASHBOARD CHART
# ==========================================================

def overview_growth_chart(df):
    """
    Multi-video views trend over time.
    """

    fig = px.line(
        df,
        x="timestamp",
        y="views",
        color="video_name",
        markers=True,
        title="📈 Views Growth Timeline",
    )

    fig.update_traces(
        line=dict(width=3),
        marker=dict(size=6),
    )

    fig.update_layout(
        template="plotly_white",
        height=550,
        hovermode="x unified",
        legend_title="Videos",
        margin=dict(
            l=20,
            r=20,
            t=60,
            b=20,
        ),
        xaxis_title="Time",
        yaxis_title="Views",
    )

    return fig


# ==========================================================
# VIDEO ANALYTICS CHARTS
# ==========================================================

def views_chart(video_df):

    fig = px.line(
        video_df,
        x="timestamp",
        y="views",
        markers=True,
        title="Views Over Time",
    )

    fig.update_traces(
        line=dict(width=3),
        marker=dict(size=6),
    )

    fig.update_layout(
        height=400,
        template="plotly_white",
        hovermode="x unified",
        margin=dict(
            l=20,
            r=20,
            t=60,
            b=20,
        ),
    )

    st.plotly_chart(fig, use_container_width=True)


def gain_chart(video_df):

    fig = px.bar(
        video_df,
        x="timestamp",
        y="view_gain",
        title="View Gain Over Time",
    )

    fig.update_layout(
        height=350,
        template="plotly_white",
        hovermode="x unified",
        margin=dict(
            l=20,
            r=20,
            t=60,
            b=20,
        ),
    )

    st.plotly_chart(fig, use_container_width=True)


def likes_chart(video_df):

    fig = px.line(
        video_df,
        x="timestamp",
        y="likes",
        markers=True,
        title="Likes Over Time",
    )

    fig.update_traces(
        line=dict(width=3),
        marker=dict(size=6),
    )

    fig.update_layout(
        height=350,
        template="plotly_white",
        hovermode="x unified",
        margin=dict(
            l=20,
            r=20,
            t=60,
            b=20,
        ),
    )

    st.plotly_chart(fig, use_container_width=True)


def comments_chart(video_df):

    fig = px.line(
        video_df,
        x="timestamp",
        y="comments",
        markers=True,
        title="Comments Over Time",
    )

    fig.update_traces(
        line=dict(width=3),
        marker=dict(size=6),
    )

    fig.update_layout(
        height=350,
        template="plotly_white",
        hovermode="x unified",
        margin=dict(
            l=20,
            r=20,
            t=60,
            b=20,
        ),
    )

    st.plotly_chart(fig, use_container_width=True)