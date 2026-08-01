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


/* Hide Streamlit Header */

header{
    visibility:hidden;
}

footer{
    visibility:hidden;
}


/* -----------------------------
Titles
------------------------------*/

.main-title{

    font-size:40px;

    font-weight:800;

    color:#111827;

    margin-bottom:5px;

}

.sub-title{

    color:#6B7280;

    font-size:16px;

    margin-bottom:30px;

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

    box-shadow:0 8px 18px rgba(0,0,0,.05);

    margin-bottom:20px;

}

</style>
""",
        unsafe_allow_html=True,
    )