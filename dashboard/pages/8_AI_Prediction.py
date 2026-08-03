import sys
from pathlib import Path

import streamlit as st
import pandas as pd
import plotly.graph_objects as go


ROOT = Path(__file__).resolve().parent.parent.parent

sys.path.append(str(ROOT))


from style import load_css

from components.sidebar import show_sidebar

from utils.database import load_data

from ai.predict import predict_views


# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(
    page_title="AI Prediction",
    page_icon="🤖",
    layout="wide",
)


# =====================================================
# LOAD STYLE + SIDEBAR
# =====================================================

load_css()

show_sidebar()


# =====================================================
# HEADER
# =====================================================

st.title("🤖 Prediction Engine")

st.caption(
    "Forecast video views by using historical data"
)



# =====================================================
# LOAD VIDEOS
# =====================================================

df = load_data()


if df.empty:

    st.warning(
        "No tracking data available."
    )

    st.stop()



videos = (
    df[
        [
            "video_id",
            "video_name"
        ]
    ]
    .drop_duplicates()
)



# =====================================================
# CONTROLS
# =====================================================

col1, col2 = st.columns(2)


with col1:

    selected_video = st.selectbox(
        "🎥 Select Video",
        videos["video_name"].tolist()
    )



selected_video_id = (
    videos[
        videos["video_name"]
        ==
        selected_video
    ]
    ["video_id"]
    .iloc[0]
)



with col2:

    prediction_options = {

        "10 Minutes": 10,

        "30 Minutes": 30,

        "1 Hour": 60,

    }


    selected_time = st.selectbox(
        "⏳ Predict After",
        list(
            prediction_options.keys()
        )
    )


    minutes = prediction_options[
        selected_time
    ]



st.divider()



# =====================================================
# RUN PREDICTION
# =====================================================

try:

    result = predict_views(
        selected_video_id,
        minutes
    )


except Exception as e:

    st.error(
        str(e)
    )

    st.stop()



# =====================================================
# KPI CARDS
# =====================================================

c1, c2, c3 = st.columns(3)



with c1:

    st.metric(
        "📈 Predicted Views",
        f"{result['predicted_views']:,}"
    )



with c2:

    st.metric(
        "🎯 Confidence",
        f"{result['confidence']}%"
    )



with c3:

    lower = result[
        "prediction_range"
    ]["lower"]

    upper = result[
        "prediction_range"
    ]["upper"]


    st.metric(
        "📉 Prediction Range",
        f"{lower:,} - {upper:,}"
    )



st.divider()



# =====================================================
# FORECAST GRAPH
# =====================================================


current_views = result[
    "current_views"
]


predicted_views = result[
    "predicted_views"
]



chart_data = pd.DataFrame(
    {
        "Stage": [
            "Current",
            f"After {minutes} min"
        ],

        "Views": [
            current_views,
            predicted_views
        ]
    }
)



fig = go.Figure()



fig.add_trace(
    go.Scatter(
        x=chart_data["Stage"],
        y=chart_data["Views"],
        mode="lines+markers",
        name="Forecast"
    )
)



fig.update_layout(

    title="📈 AI Forecast",

    xaxis_title="",

    yaxis_title="Views",

    height=400,

    template="plotly_white"

)



st.plotly_chart(
    fig,
    use_container_width=True
)



# =====================================================
# DETAILS
# =====================================================

st.subheader(
    "Prediction Details"
)


details = {

    "Current Views":
        f"{result['current_views']:,}",

    "Expected Gain":
        f"+{result['predicted_gain']:,}",

    "Prediction Time":
        f"{result['prediction_minutes']} minutes",

    "Model Horizon":
        f"{result['prediction_horizon']} records"

}



st.table(
    pd.DataFrame(
        details.items(),
        columns=[
            "Metric",
            "Value"
        ]
    )
)