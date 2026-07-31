import streamlit as st


# ---------------------------------------------------------
# OVERVIEW KPI CARDS
# ---------------------------------------------------------

def show_overview_cards(
    total_videos,
    total_views,
    total_likes,
    total_comments,
):
    """
    Dashboard overview KPI cards.
    """

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "🎥 Videos",
            total_videos
        )

    with col2:
        st.metric(
            "👀 Total Views",
            f"{total_views:,}"
        )

    with col3:
        st.metric(
            "❤️ Total Likes",
            f"{total_likes:,}"
        )

    with col4:
        st.metric(
            "💬 Total Comments",
            f"{total_comments:,}"
        )


# ---------------------------------------------------------
# VIDEO KPI CARDS
# ---------------------------------------------------------

def show_kpi_cards(metrics):
    """
    Individual video KPI cards.
    """

    latest = metrics["latest"]

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "👀 Current Views",
            f"{latest['views']:,}"
        )

    with col2:
        st.metric(
            "❤️ Likes",
            f"{latest['likes']:,}"
        )

    with col3:
        st.metric(
            "💬 Comments",
            f"{latest['comments']:,}"
        )

    with col4:
        st.metric(
            "📈 Latest Gain",
            f"{latest['view_gain']:,}"
        )


# ---------------------------------------------------------
# GROWTH CARDS
# ---------------------------------------------------------

def show_growth_cards(metrics):
    """
    Growth statistics.
    """

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "⚡ Last 1 Hour",
            f"{metrics['last_1_hour_gain']:,}"
        )

    with col2:
        st.metric(
            "📅 Last 24 Hours",
            f"{metrics['last_24_hour_gain']:,}"
        )

    with col3:
        st.metric(
            "🚀 Avg / Hour",
            f"{metrics['avg_hourly_growth']:,}"
        )