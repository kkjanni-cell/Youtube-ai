import streamlit as st


def action_card(icon, title, description, page):

    st.markdown(
f"""
<div class="action-card">

<div class="action-icon">
{icon}
</div>

<div class="action-title">
{title}
</div>

<div class="action-description">
{description}
</div>

</div>
""",
        unsafe_allow_html=True,
    )

    st.page_link(
        page,
        label=f"Open {title}",
        icon="➡️",
    )