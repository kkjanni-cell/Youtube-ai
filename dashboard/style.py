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

/* ========================================
Hide Streamlit Default Multipage Navigation
======================================== */

section[data-testid="stSidebarNav"]{
    display:none;
}
/* ======================================================
SIDEBAR
====================================================== */

.sidebar-logo{

    font-size:30px;

    font-weight:800;

    margin-top:5px;

    color:#111827;

}

.sidebar-logo span{

    vertical-align:middle;

}

.sidebar-subtitle{

    color:#6B7280;

    font-size:14px;

    margin-top:6px;

    margin-bottom:15px;

}



/* Tracker Card */

.tracker-card{

    background:white;

    border-radius:18px;

    padding:18px;

    border:1px solid #E5E7EB;

    box-shadow:0 8px 20px rgba(0,0,0,.05);

}


.tracker-status{

    font-weight:700;

    margin-bottom:18px;

}


.online{

    color:#16A34A;

}


.offline{

    color:#DC2626;

}


.tracker-item{

    margin-top:12px;

}


.tracker-label{

    color:#6B7280;

    font-size:13px;

}


.tracker-value{

    font-size:18px;

    font-weight:700;

    color:#111827;

}



/* Navigation */

.nav-title{

    font-size:14px;

    font-weight:700;

    letter-spacing:1px;

    text-transform:uppercase;

    color:#6B7280;

    margin-bottom:10px;

}



/* Footer */

.sidebar-footer{

    text-align:center;

    color:#9CA3AF;

    font-size:12px;

}
/* =====================================================
PREMIUM KPI CARD
=====================================================*/

.kpi-card{

    background:#FFFFFF;

    border-radius:22px;

    padding:24px;

    min-height:190px;

    border:1px solid #E5E7EB;

    box-shadow:
        0 10px 25px rgba(0,0,0,.05);

    transition:.3s;

}


.kpi-card:hover{

    transform:translateY(-6px);

    box-shadow:
        0 20px 40px rgba(0,0,0,.12);

}


.kpi-icon{

    width:56px;

    height:56px;

    border-radius:16px;

    display:flex;

    align-items:center;

    justify-content:center;

    color:white;

    font-size:28px;

    margin-bottom:18px;

}


.kpi-title{

    color:#6B7280;

    font-size:15px;

    font-weight:600;

}


.kpi-value{

    margin-top:12px;

    font-size:36px;

    font-weight:800;

    color:#111827;

}


.kpi-change{

    margin-top:18px;

    display:inline-block;

    background:#ECFDF5;

    color:#16A34A;

    padding:6px 12px;

    border-radius:999px;

    font-size:13px;

    font-weight:700;

}

/* ===========================================
Dashboard Summary Cards
===========================================*/

.summary-card{

    background:white;

    border-radius:20px;

    padding:22px;

    border:1px solid #E5E7EB;

    box-shadow:0 10px 25px rgba(0,0,0,.05);

    min-height:220px;

}
/* ======================================================
ACTION CARDS
======================================================*/

.action-card{

    background:white;

    border-radius:20px;

    padding:22px;

    border:1px solid #E5E7EB;

    box-shadow:
        0 10px 25px rgba(0,0,0,.05);

    transition:.30s;

    min-height:180px;

    margin-bottom:10px;

}

.action-card:hover{

    transform:translateY(-6px);

    box-shadow:
        0 20px 40px rgba(0,0,0,.10);

}

.action-icon{

    font-size:34px;

}

.action-title{

    margin-top:15px;

    font-size:22px;

    font-weight:700;

    color:#111827;

}

.action-description{

    margin-top:10px;

    color:#6B7280;

    line-height:1.7;

    min-height:55px;

}
/* =====================================================
ACTIVITY CARDS
=====================================================*/

.activity-card{

    background:#FFFFFF;

    border-radius:22px;

    padding:22px;

    border:1px solid #E5E7EB;

    box-shadow:
        0 10px 25px rgba(0,0,0,.05);

    margin-bottom:20px;

    transition:.30s;

}

.activity-card:hover{

    transform:translateY(-4px);

    box-shadow:
        0 18px 35px rgba(0,0,0,.08);

}

.video-title{

    font-size:24px;

    font-weight:700;

    color:#111827;

    margin-bottom:16px;

    line-height:1.4;

}

.growth-pill{

    display:inline-block;

    background:#ECFDF5;

    color:#15803D;

    padding:8px 16px;

    border-radius:999px;

    font-size:14px;

    font-weight:700;

    margin-top:12px;

    margin-bottom:10px;

}

/* Rounded images */

[data-testid="stImage"] img{

    border-radius:18px;

}
/* ======================================================
VIDEO METRICS
======================================================*/

.video-metrics{

    display:flex;

    gap:18px;

    margin-top:18px;

    margin-bottom:18px;

    flex-wrap:wrap;

}


.video-metric{

    display:flex;

    align-items:center;

    gap:12px;

    background:#F8FAFC;

    border:1px solid #E5E7EB;

    border-radius:14px;

    padding:12px 18px;

    min-width:170px;

    transition:.25s;

}


.video-metric:hover{

    background:#FFFFFF;

    transform:translateY(-2px);

    box-shadow:0 8px 18px rgba(0,0,0,.05);

}


.metric-icon{

    font-size:24px;

}


.metric-number{

    font-size:20px;

    font-weight:700;

    color:#111827;

}


.metric-text{

    font-size:13px;

    color:#6B7280;

}

/* =====================================================
STATUS PILL
=====================================================*/

.status-pill{

    display:inline-block;

    color:white;

    padding:8px 18px;

    border-radius:999px;

    font-size:13px;

    font-weight:700;

    margin-top:10px;

    margin-bottom:10px;

    letter-spacing:.3px;

}

</style>
""",
        unsafe_allow_html=True,
    )