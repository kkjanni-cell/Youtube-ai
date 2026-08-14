import streamlit as st

try:
    from streamlit_autorefresh import st_autorefresh
except ImportError:
    def st_autorefresh(interval=5000, key=None):
        return None

st_autorefresh(interval=5000, key="datarefresh")

import pandas as pd
import plotly.express as px

from style import load_css
from components.sidebar import show_sidebar
from components.global_console import setup_global_console
from components.keyboard_shortcuts import keyboard_shortcuts
from utils.database import load_data, get_latest_data
from utils.formatter import format_number
from components.charts import overview_growth_chart

st.set_page_config(
    page_title="Comparison",
    page_icon="📊",
    layout="wide"
)

load_css()
show_sidebar()
setup_global_console()
keyboard_shortcuts()

st.title("📊 Video Comparison")
st.caption("Compare growth and performance across multiple tracked videos.")

# =====================================================
# LOAD DATA
# =====================================================

df = load_data()

if df.empty:
    st.warning("No tracking data available.")
    st.stop()

all_videos = sorted(df["video_name"].unique().tolist())

# Default to the top 3 videos by current views, so the page
# isn't empty on first load.
latest_all = get_latest_data(df)
default_videos = (
    latest_all.sort_values("views", ascending=False)
    .head(3)["video_name"]
    .tolist()
)

# =====================================================
# VIDEO SELECTION
# =====================================================

selected_videos = st.multiselect(
    "🎥 Select videos to compare (2 or more)",
    all_videos,
    default=default_videos,
)

if len(selected_videos) < 2:
    st.info("Select at least 2 videos to see a comparison.")
    st.stop()

filtered_df = df[df["video_name"].isin(selected_videos)]

st.divider()

# =====================================================
# GROWTH TIMELINE (OVERLAY)
# =====================================================

st.subheader("📈 Growth Timeline")

fig = overview_growth_chart(filtered_df)
st.plotly_chart(fig, use_container_width=True)

st.divider()

# =====================================================
# SIDE-BY-SIDE KPI COMPARISON
# =====================================================

st.subheader("📋 Side-by-Side Comparison")

latest = get_latest_data(filtered_df)

comparison_table = latest[
    ["video_name", "views", "view_gain", "likes", "comments"]
].copy()

comparison_table.columns = [
    "Video", "Views", "Latest Gain", "Likes", "Comments"
]

comparison_table = comparison_table.sort_values(
    "Views", ascending=False
).reset_index(drop=True)

display_table = comparison_table.copy()
for col in ["Views", "Latest Gain", "Likes", "Comments"]:
    display_table[col] = display_table[col].apply(format_number)

st.dataframe(
    display_table,
    hide_index=True,
    use_container_width=True,
)

st.divider()

# =====================================================
# RANKING CHARTS
# =====================================================

st.subheader("🏆 Ranking")

rank_col1, rank_col2 = st.columns(2)

with rank_col1:
    fig_views = px.bar(
        comparison_table.sort_values("Views"),
        x="Views",
        y="Video",
        orientation="h",
        title="Total Views",
        color="Views",
        color_continuous_scale="Blues",
    )
    fig_views.update_layout(
        template="plotly_white",
        height=350,
        margin=dict(l=20, r=20, t=60, b=20),
        showlegend=False,
        coloraxis_showscale=False,
    )
    st.plotly_chart(fig_views, use_container_width=True)

with rank_col2:
    fig_gain = px.bar(
        comparison_table.sort_values("Latest Gain"),
        x="Latest Gain",
        y="Video",
        orientation="h",
        title="Latest Growth",
        color="Latest Gain",
        color_continuous_scale="Greens",
    )
    fig_gain.update_layout(
        template="plotly_white",
        height=350,
        margin=dict(l=20, r=20, t=60, b=20),
        showlegend=False,
        coloraxis_showscale=False,
    )
    st.plotly_chart(fig_gain, use_container_width=True)

# =====================================================
# TOP PERFORMER CALLOUT
# =====================================================

top_by_views = comparison_table.iloc[0]
top_by_gain = comparison_table.sort_values(
    "Latest Gain", ascending=False
).iloc[0]

callout_col1, callout_col2 = st.columns(2)

with callout_col1:
    st.success(
        f"👑 **Most Views:** {top_by_views['Video']}\n\n"
        f"{format_number(top_by_views['Views'])} views"
    )

with callout_col2:
    st.success(
        f"🚀 **Fastest Growing:** {top_by_gain['Video']}\n\n"
        f"+{format_number(top_by_gain['Latest Gain'])} views (latest)"
    )