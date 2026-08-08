#!/bin/bash
PROJECT_DIR="/Users/kk/youtube-ai/Youtube-ai/tracker"
VENV_DIR="/Users/kk/youtube-ai/Youtube-ai/.venv"

cd "$PROJECT_DIR" || exit 1
source "$VENV_DIR/bin/activate"

{
  echo ""
  echo "---- Run started: $(date) ----"
  python3 track_views.py
  echo "---- Run finished: $(date) ----"
} >> "$PROJECT_DIR/tracker_log.txt" 2>&1
