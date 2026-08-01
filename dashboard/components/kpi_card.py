import streamlit as st


def kpi_card(
    title,
    value,
    icon,
    change=None,
    color="#2563EB",
):
    """
    Premium KPI Card
    """

    if change:
        change_html = f"""
        <div class="kpi-change">
            ↗ {change}
        </div>
        """
    else:
        change_html = ""

    st.markdown(
        f"""
        <div class="kpi-card">

            <div class="kpi-icon"
                style="
                    background:linear-gradient(
                        135deg,
                        {color},
                        #3B82F6
                    );
                ">
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