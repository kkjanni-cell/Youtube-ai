import streamlit as st


def premium_kpi_card(
    title,
    value,
    icon="📊",
    change=None,
    change_type="positive",
):
    """
    Premium KPI Card
    """

    if change is None:
        change_html = ""
    else:
        color = "#22C55E" if change_type == "positive" else "#EF4444"

        arrow = "▲" if change_type == "positive" else "▼"

        change_html = f"""
        <div style="
            color:{color};
            font-size:15px;
            font-weight:600;
            margin-top:12px;
        ">
            {arrow} {change}
        </div>
        """

    st.markdown(
        f"""
        <div class="metric-card">

            <div style="
                display:flex;
                justify-content:space-between;
                align-items:center;
            ">

                <div class="metric-label">
                    {title}
                </div>

                <div style="font-size:28px;">
                    {icon}
                </div>

            </div>

            <div class="metric-value">
                {value}
            </div>

            {change_html}

        </div>
        """,
        unsafe_allow_html=True,
    )