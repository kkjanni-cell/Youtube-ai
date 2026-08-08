from __future__ import annotations

import subprocess
import threading
import time
from pathlib import Path

import streamlit as st

# Root of the project
ROOT = Path(__file__).resolve().parents[2]

TRACKER_SCRIPT = ROOT / "tracker" / "track_views.py"

# 5 minutes
INTERVAL_SECONDS = 300


def _tracker_loop():
    """
    Runs forever in a background thread.
    """

    while True:

        try:

            print("📡 Running tracker...")

            subprocess.run(
                ["python", str(TRACKER_SCRIPT)],
                cwd=ROOT,
                check=False,
            )

            print("✅ Tracker finished.")

        except Exception as e:

            print("Tracker Error:", e)

        time.sleep(INTERVAL_SECONDS)


def start_scheduler():
    """
    Start only ONE scheduler thread.
    """

    if "tracker_scheduler_started" not in st.session_state:

        thread = threading.Thread(
            target=_tracker_loop,
            daemon=True,
        )

        thread.start()

        st.session_state.tracker_scheduler_started = True

        print("🚀 Local tracker scheduler started.")