import streamlit as st


def hero_video_card(video):
    """
    Displays the fastest growing video in a premium hero card.
    """

    st.markdown(
        f"""
        <div style="
            background: linear-gradient(135deg,#FF0000,#FF5F6D);
            border-radius:25px;
            padding:30px;
            color:white;
            margin-bottom:20px;
            box-shadow:0 15px 35px rgba(0,0,0,.15);
        ">

            <div style="font-size:18px;opacity:.9;">
                🔥 Fastest Growing Video
            </div>

            <div style="
                font-size:30px;
                font-weight:700;
                margin-top:12px;
                margin-bottom:25px;
            ">
                {video["video_name"]}
            </div>

            <div style="
                display:flex;
                justify-content:space-between;
                flex-wrap:wrap;
                gap:25px;
            ">

                <div>
                    <div style="opacity:.8;">👀 Views</div>
                    <div style="font-size:28px;font-weight:700;">
                        {int(video["views"]):,}
                    </div>
                </div>

                <div>
                    <div style="opacity:.8;">📈 Latest Gain</div>
                    <div style="font-size:28px;font-weight:700;">
                        +{int(video["view_gain"]):,}
                    </div>
                </div>

                <div>
                    <div style="opacity:.8;">❤️ Likes</div>
                    <div style="font-size:28px;font-weight:700;">
                        {int(video["likes"]):,}
                    </div>
                </div>

                <div>
                    <div style="opacity:.8;">💬 Comments</div>
                    <div style="font-size:28px;font-weight:700;">
                        {int(video["comments"]):,}
                    </div>
                </div>

            </div>

        </div>
        """,
        unsafe_allow_html=True,
    )