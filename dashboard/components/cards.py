import streamlit as st

from components.premium_cards import premium_kpi_card


# ---------------------------------------------------------
# OVERVIEW KPI CARDS
# ---------------------------------------------------------

def show_overview_cards(
    total_videos,
    total_views,
    total_likes,
    total_comments,
):

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        premium_kpi_card(
            title="Videos",
            value=f"{total_videos:,}",
            icon="🎥",
        )

    with c2:
        premium_kpi_card(
            title="Total Views",
            value=f"{total_views:,}",
            icon="👀",
        )

    with c3:
        premium_kpi_card(
            title="Likes",
            value=f"{total_likes:,}",
            icon="❤️",
        )

    with c4:
        premium_kpi_card(
            title="Comments",
            value=f"{total_comments:,}",
            icon="💬",
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