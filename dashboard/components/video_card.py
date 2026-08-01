import streamlit as st


def video_card(row):

    with st.container(border=True):

        col1, col2 = st.columns([4, 1])

        with col1:

            st.subheader(f"🎥 {row['video_name']}")

            c1, c2, c3 = st.columns(3)

            c1.metric(
                "Views",
                row["Views"],
            )

            c2.metric(
                "Likes",
                row["Likes"],
            )

            c3.metric(
                "Comments",
                row["Comments"],
            )

        with col2:

            st.markdown("### " + row["Status"])

            st.metric(
                "Growth",
                row["Growth"],
            )

            st.metric(
                "Score",
                row["Performance Score"],
            )