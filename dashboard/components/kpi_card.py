import streamlit as st


def kpi_card(
    title,
    value,
    icon,
    change=None,
    color="#2563EB",
):

    change_html = ""

    if change:
        change_html = f"""
<div class="kpi-change">
↗ {change}
</div>
"""

    st.markdown(
f"""
<div class="kpi-card">

<div class="kpi-icon" style="background:{color};">
{icon}
</div>

<div class="kpi-title">
{title}
</div>

<div class="kpi-value">
{value}
</div>

{change_html}

</div>
""",
        unsafe_allow_html=True,
    )