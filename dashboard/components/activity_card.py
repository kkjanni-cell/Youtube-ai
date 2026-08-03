import streamlit as st


# ---------------------------------------------------------
# VIDEO STATUS
# ---------------------------------------------------------

def get_status(view_gain):

    if view_gain >= 10000:
        return "🔥 Viral", "#DC2626"

    elif view_gain >= 5000:
        return "🚀 Trending", "#2563EB"

    elif view_gain >= 1000:
        return "📈 Growing", "#16A34A"

    return "➖ Stable", "#6B7280"



# ---------------------------------------------------------
# ACTIVITY CARD
# ---------------------------------------------------------

def activity_card(video):

    status, color = get_status(video["view_gain"])

    thumbnail = (
        f"https://img.youtube.com/vi/"
        f"{video['video_id']}/hqdefault.jpg"
    )


    st.markdown(
f"""
<div class="activity-card">

</div>
""",
unsafe_allow_html=True,
    )


    left, right = st.columns([1.4, 3])


    # -----------------------------------------------------
    # THUMBNAIL
    # -----------------------------------------------------

    with left:

        st.image(
            thumbnail,
            width="stretch",
        )


    # -----------------------------------------------------
    # DETAILS
    # -----------------------------------------------------

    with right:

        st.markdown(
f"""
<div class="video-title">
{video['video_name']}
</div>
""",
unsafe_allow_html=True,
        )


        st.markdown(
f"""
<div class="video-metrics">

<div class="video-metric">

<div class="metric-icon">
👀
</div>

<div>

<div class="metric-number">
{int(video['views']):,}
</div>

<div class="metric-text">
Views
</div>

</div>

</div>


<div class="video-metric">

<div class="metric-icon">
❤️
</div>

<div>

<div class="metric-number">
{int(video['likes']):,}
</div>

<div class="metric-text">
Likes
</div>

</div>

</div>


<div class="video-metric">

<div class="metric-icon">
💬
</div>

<div>

<div class="metric-number">
{int(video['comments']):,}
</div>

<div class="metric-text">
Comments
</div>

</div>

</div>


</div>
""",
unsafe_allow_html=True,
        )


        st.markdown(
f"""
<div class="status-pill" style="background:{color};">
{status}
</div>
""",
unsafe_allow_html=True,
        )


        st.markdown(
f"""
<div class="growth-pill">
📈 +{int(video['view_gain']):,} Views since last snapshot
</div>
""",
unsafe_allow_html=True,
        )


        st.caption(
            f"🕒 Updated: {video['timestamp']}"
        )


    st.divider()