import os
import streamlit.components.v1 as components

_RELEASE = False

if not _RELEASE:
    _component = components.declare_component(
        "keyboard",
        url="http://localhost:5173",
    )
else:
    build_dir = os.path.join(
        os.path.dirname(__file__),
        "frontend",
        "dist",
    )

    _component = components.declare_component(
        "keyboard",
        path=build_dir,
    )


def keyboard():
    return _component(default=None)