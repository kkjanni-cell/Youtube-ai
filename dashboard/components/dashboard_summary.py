import streamlit as st


def dashboard_summary(
    tracker_status,
    last_update,
    total_snapshots,
    top_video,
):

    left, right = st.columns(2)

    with left:

        st.markdown(
            f"""
<div class="summary-card">

<h3>📡 Tracker Status</h3>

<p>
<b>{tracker_status}</b>
</p>

<p>
<b>Last Update</b><br>
{last_update}
</p>

<p>
<b>Total Snapshots</b><br>
{total_snapshots:,}
</p>

</div>
""",
            unsafe_allow_html=True,
        )


    with right:

        st.markdown(
            f"""
<div class="summary-card">

<h3>🔥 Top Growing Video</h3>

<p>
<b>{top_video['video_name']}</b>
</p>

<p>
👀 {int(top_video['views']):,} Views
</p>

<p>
📈 +{int(top_video['view_gain']):,}
</p>

<p>
❤️ {int(top_video['likes']):,}
</p>

</div>
""",
            unsafe_allow_html=True,
        )