import streamlit as st
import streamlit.components.v1 as components


def keyboard_shortcuts():

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

        // Streamlit recreates this component's iframe on every rerun
        // (including every auto-refresh cycle). When an iframe is torn
        // down, any listener it registered - even one attached to the
        // parent page - silently stops working. So instead of only
        // guarding against re-adding a listener (which left us with
        // zero working listeners after the first refresh), we
        // explicitly remove whatever the previous listener was and
        // install a fresh, currently-alive one every single time.
        // This keeps exactly one working listener at all times, never
        // stacks duplicates, and never goes silently dead.

        if (window.parent.__keyboardHandler) {
            doc.removeEventListener(
                "keydown",
                window.parent.__keyboardHandler
            );
        }

        function handleShortcutKeydown(e) {

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

        }

        window.parent.__keyboardHandler = handleShortcutKeydown;
        doc.addEventListener("keydown", handleShortcutKeydown);

        </script>
        """,
        height=0,
    )