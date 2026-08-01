import streamlit as st
from components.kpi_card import kpi_card


def show_overview_cards(
    total_videos,
    total_views,
    total_likes,
    total_comments,
):

    c1, c2, c3, c4 = st.columns(4)

    with c1:
    kpi_card(
        "Videos",
        f"{total_videos:,}",
        "🎬",
        "Tracking",
        "#2563EB",
    )

with c2:
    kpi_card(
        "Views",
        f"{total_views:,}",
        "👀",
        "Live",
        "#7C3AED",
    )

with c3:
    kpi_card(
        "Likes",
        f"{total_likes:,}",
        "❤️",
        "Updated",
        "#EC4899",
    )

with c4:
    kpi_card(
        "Comments",
        f"{total_comments:,}",
        "💬",
        "Realtime",
        "#F59E0B",
    )


# ---------------------------------------------------------
# VIDEO KPI CARDS
# ---------------------------------------------------------

def show_kpi_cards(metrics):

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