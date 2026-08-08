import streamlit as st
from streamlit_autorefresh import st_autorefresh
st_autorefresh(interval=5000, key="datarefresh")

from utils.formatter import format_number
from components.sidebar import show_sidebar

from utils.database import (
    load_data,
    get_total_videos,
    get_total_views,
    get_total_likes,
    get_total_comments,
    get_total_view_gain,
    get_last_update,
    get_top_growing_video,
    get_latest_data,
    get_top_videos,
)

from components.video_card import video_card

from style import load_css
from components.cards import show_overview_cards
from components.section import section_header
from components.charts import overview_growth_chart
from components.global_console import setup_global_console
from components.keyboard_shortcuts import keyboard_shortcuts


st.set_page_config(
    page_title="Overview",
    page_icon="📊",
    layout="wide",
)


load_css()
show_sidebar()
setup_global_console()
keyboard_shortcuts()

# =====================================================
# LOAD DATA
# =====================================================

df = load_data()


if df.empty:
    st.warning("No tracking data available.")
    st.stop()



# =====================================================
# VIDEO FILTER
# =====================================================

video_list = [
    "All Videos"
] + sorted(
    df["video_name"].unique().tolist()
)


header_col, filter_col = st.columns(
    [3,1]
)


with header_col:

    section_header(
        "📊 Overview Dashboard",
        "Real-time performance of tracked YouTube videos.",
    )


with filter_col:

    st.markdown(
        """
        <div class="filter-label">
        🎥 Video Filter
        </div>
        """,
        unsafe_allow_html=True
    )


    selected_video = st.selectbox(
        "Video Filter",
        video_list,
        label_visibility="collapsed"
    )



# Apply filter

if selected_video == "All Videos":

    filtered_df = df

else:

    filtered_df = df[
        df["video_name"] == selected_video
    ]



# =====================================================
# LATEST DATA
# =====================================================

latest = get_latest_data(filtered_df)



# =====================================================
# KPI CARDS
# =====================================================

show_overview_cards(
    get_total_videos(filtered_df),
    get_total_views(filtered_df),
    get_total_likes(filtered_df),
    get_total_comments(filtered_df),
)



st.divider()



# =====================================================
# PERFORMANCE CHART
# =====================================================

section_header(
    "📈 Performance Overview",
    "Track views growth and performance trends.",
)


fig = overview_growth_chart(filtered_df)


st.plotly_chart(
    fig,
    use_container_width=True,
)



st.divider()



# =====================================================
# DASHBOARD INFO
# =====================================================

left, right = st.columns([2,1])


with left:


    if selected_video == "All Videos":

        st.subheader(
            "🔥 Fastest Growing Video"
        )

        top = get_top_growing_video(filtered_df)


        st.success(
            f"""
**{top['video_name']}**

📈 Latest Gain : **+{int(top['view_gain']):,} Views**

👀 Total Views : **{int(top['views']):,}**

❤️ Likes : **{int(top['likes']):,}**

💬 Comments : **{int(top['comments']):,}**
"""
        )


    else:

        latest_video = latest.iloc[0]


        st.subheader(
            "🎥 Selected Video Performance"
        )


        st.success(
            f"""
**{latest_video['video_name']}**

📈 Latest Gain : **+{int(latest_video['view_gain']):,} Views**

👀 Total Views : **{int(latest_video['views']):,}**

❤️ Likes : **{int(latest_video['likes']):,}**

💬 Comments : **{int(latest_video['comments']):,}**
"""
        )



with right:


    st.subheader(
        "📌 Dashboard Summary"
    )


    st.metric(
        "📈 Total View Gain",
        f"{get_total_view_gain(filtered_df):,}",
    )


    st.metric(
        "🕒 Last Updated",
        str(get_last_update(filtered_df)),
    )



st.divider()



# =====================================================
# TOP VIDEOS
# =====================================================

st.subheader(
    "🏆 Top Performing Videos"
)


top_videos = get_top_videos(
    filtered_df
).copy()



top_videos["Views"] = (
    top_videos["views"]
    .apply(format_number)
)


top_videos["Likes"] = (
    top_videos["likes"]
    .apply(format_number)
)


top_videos["Comments"] = (
    top_videos["comments"]
    .apply(format_number)
)



top_videos["Growth"] = (
    top_videos["view_gain"]
    .apply(
        lambda x:
        f"🟢 +{format_number(x)}"
        if x >= 0
        else f"🔴 {format_number(x)}"
    )
)



def trending_badge(gain):

    if gain >= 10000:
        return "🔥 Viral"

    elif gain >= 5000:
        return "🚀 Trending"

    elif gain >= 1000:
        return "📈 Growing"

    return "➖ Stable"



top_videos["Status"] = (
    top_videos["view_gain"]
    .apply(trending_badge)
)



score = (
    top_videos["views"] * 0.6
    + top_videos["likes"] * 2
    + top_videos["comments"] * 5
    + top_videos["view_gain"] * 3
)


top_videos["Performance Score"] = (
    score / score.max() * 100
).round().astype(int)


top_videos["Performance Score"] = (
    top_videos["Performance Score"]
    .astype(str)
    + " ⭐"
)



search = st.text_input(
    "🔍 Search Video",
    placeholder="Search by video name...",
)



if search:

    top_videos = top_videos[
        top_videos["video_name"]
        .str.contains(
            search,
            case=False,
            na=False
        )
    ]



sort_column = st.selectbox(
    "Sort By",
    [
        "views",
        "view_gain",
        "likes",
        "comments",
    ],
)



top_videos = top_videos.sort_values(
    sort_column,
    ascending=False,
)



for _, row in top_videos.iterrows():

    video_card(row)



st.divider()



# =====================================================
# LATEST SNAPSHOT
# =====================================================

st.subheader(
    "📋 Latest Snapshot"
)


st.dataframe(
    latest[
        [
            "video_name",
            "views",
            "view_gain",
            "likes",
            "comments",
            "timestamp",
        ]
    ],
    hide_index=True,
    use_container_width=True,
)