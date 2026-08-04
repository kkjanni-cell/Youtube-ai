import streamlit as st
import streamlit.components.v1 as components


def global_keyboard():

    event = components.html(
        """
        <script>

        const sendShortcut = () => {

            window.parent.postMessage(
                {
                    type: "streamlit:setComponentValue",
                    value: {
                        action: "operations"
                    }
                },
                "*"
            );

        };


        window.parent.document.addEventListener(
            "keydown",
            function(e){

                if(
                    (e.metaKey || e.ctrlKey)
                    &&
                    e.shiftKey
                    &&
                    e.key.toLowerCase() === "k"
                ){

                    e.preventDefault();

                    sendShortcut();

                }

            }

        );

        </script>
        """,
        height=0,
    )

    return event