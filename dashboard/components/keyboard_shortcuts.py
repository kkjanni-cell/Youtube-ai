import streamlit as st
import streamlit.components.v1 as components


def keyboard_shortcuts():

    # Hide trigger button but keep it available for JS click
    st.markdown(
        """
        <style>
        div[data-testid="stButton"] button {
            opacity: 0;
            position: fixed;
            width: 1px;
            height: 1px;
            overflow: hidden;
            pointer-events: none;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    trigger = st.button(
        "⌨️ Keyboard Trigger",
        key="keyboard_shortcut_trigger",
    )

    if trigger:
        st.session_state.command_palette_open = True
        st.rerun()


    components.html(
        """
        <script>

        const doc = window.parent.document;

        if (!window.keyboardListenerInstalled) {

            window.keyboardListenerInstalled = true;

            doc.addEventListener("keydown", function(e){

                const isMac = navigator.platform
                    .toUpperCase()
                    .includes("MAC");

                const modifier = isMac
                    ? e.metaKey
                    : e.ctrlKey;

                if (
                    modifier &&
                    e.shiftKey &&
                    e.key.toLowerCase() === "k"
                ) {

                    e.preventDefault();

                    const buttons = Array.from(
                        doc.querySelectorAll("button")
                    );

                    const target = buttons.find(
                        b => b.innerText.includes("Keyboard Trigger")
                    );

                    if (target) {

                        console.log("⌘ + Shift + K detected");

                        target.click();

                    }

                }

            });

        }

        </script>
        """,
        height=0,
    )