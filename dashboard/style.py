import streamlit as st


def load_css():

    st.markdown(
        """
<style>

/* -----------------------------
General
------------------------------*/

html, body, [class*="css"]{
    font-family: Inter, sans-serif;
}


/* Background */

.stApp{
    background:#F6F8FC;
}


/* Hide Streamlit Footer */

footer{
    visibility:hidden;
}


/* -----------------------------------
Hero
------------------------------------*/

.hero-title{

    font-size:48px;

    font-weight:800;

    color:#111827;

    margin-top:10px;

    margin-bottom:10px;

}


.hero-subtitle{

    font-size:18px;

    color:#6B7280;

    max-width:850px;

    line-height:1.7;

    margin-bottom:40px;

}



/* -----------------------------
Glass KPI Card
------------------------------*/

.metric-card{

    background:white;

    border-radius:20px;

    padding:22px;

    box-shadow:
        0 10px 25px rgba(0,0,0,.06);

    border:1px solid rgba(0,0,0,.04);

    transition:.25s;

}


.metric-card:hover{

    transform:translateY(-4px);

    box-shadow:
        0 20px 40px rgba(0,0,0,.08);

}



/* KPI Title */

.metric-label{

    color:#6B7280;

    font-size:14px;

    font-weight:600;

}


/* KPI Value */

.metric-value{

    font-size:34px;

    font-weight:800;

    color:#111827;

}


/* KPI Change */

.metric-change{

    font-size:15px;

    font-weight:700;

}



/* -----------------------------
Section Title
------------------------------*/

.section-title{

    font-size:26px;

    font-weight:700;

    margin-top:20px;

    margin-bottom:15px;

}



/* -----------------------------
Chart Container
------------------------------*/

.chart-card{

    background:white;

    padding:20px;

    border-radius:20px;

    box-shadow:
        0 8px 18px rgba(0,0,0,.05);

    margin-bottom:20px;

}



/* -----------------------------
Dashboard Filter
------------------------------*/


.filter-label{

    font-size:14px;

    font-weight:700;

    color:#374151;

    margin-bottom:8px;

}


/* Selectbox wrapper */

div[data-baseweb="select"]{

    border-radius:12px;

}



/* Selectbox input */

div[data-baseweb="select"] > div{

    background:white;

    border-radius:12px;

    border:1px solid #E5E7EB;

    min-height:42px;

}



/* -----------------------------
Sidebar
------------------------------*/

section[data-testid="stSidebar"]{

    background:#FFFFFF;

    border-right:1px solid #E5E7EB;

}


section[data-testid="stSidebar"] .block-container{

    padding-top:1.5rem;

    padding-left:1rem;

    padding-right:1rem;

}



/* -----------------------------
Divider spacing
------------------------------*/

hr{

    margin-top:35px;

    margin-bottom:35px;

}


</style>
""",
        unsafe_allow_html=True,
    )