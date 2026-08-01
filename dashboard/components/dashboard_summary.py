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

### 📡 Tracker Status

**{tracker_status}**

**Last Update**

{last_update}

**Total Snapshots**

{total_snapshots:,}

</div>
""",
            unsafe_allow_html=True,
        )

    with right:
        st.markdown(
            f"""
<div class="summary-card">

### 🔥 Top Growing Video

**{top_video['video_name']}**

👀 {int(top_video['views']):,} Views

📈 +{int(top_video['view_gain']):,}

❤️ {int(top_video['likes']):,}

</div>
""",
            unsafe_allow_html=True,
        )