import streamlit as st
import streamlit.components.v1 as components


def keyboard_shortcuts():

    # Scope the "hide this button" CSS to ONLY the trigger button's
    # own container (st-key-keyboard_trigger_container), instead of
    # every button in the app (div[data-testid="stButton"] button).
    st.markdown(
        """
        <style>
        .st-key-keyboard_trigger_container button {
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

    # Wrap ONLY the trigger button in a uniquely-keyed container so the
    # CSS above can target it specifically, without affecting any other
    # button rendered elsewhere in the app (e.g. inside dialogs).
    with st.container(key="keyboard_trigger_container"):

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