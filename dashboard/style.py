import streamlit as st


def load_css():

    st.markdown("""
    <style>

    .main {
        background-color:#f5f7fb;
    }

    .block-container{
        padding-top:2rem;
        padding-bottom:2rem;
        padding-left:3rem;
        padding-right:3rem;
    }

    h1{
        font-weight:700;
    }

    div[data-testid="metric-container"]{
        background:white;
        border-radius:15px;
        padding:18px;
        box-shadow:0px 2px 8px rgba(0,0,0,0.08);
    }

    div[data-testid="stDataFrame"]{
        border-radius:15px;
    }

    </style>
    """, unsafe_allow_html=True)