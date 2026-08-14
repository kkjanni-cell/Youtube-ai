import json
import sqlite3
from pathlib import Path

import joblib
import pandas as pd


# --------------------------------------------------
# PATHS
# --------------------------------------------------

ROOT = Path(__file__).resolve().parent.parent

DB_PATH = ROOT / "database" / "youtube.db"
MODEL_PATH = ROOT / "models" / "youtube_predictor.pkl"
MAE_PATH = ROOT / "models" / "mae_by_horizon.json"


# --------------------------------------------------
# MODEL SETTINGS
# --------------------------------------------------

MODEL = joblib.load(MODEL_PATH)

with open(MAE_PATH) as f:
    MAE_BY_HORIZON = {int(k): v for k, v in json.load(f).items()}

# Fallback if a requested horizon has no exact match in the trained
# set (shouldn't normally happen since the dashboard dropdown only
# offers trained horizons, but this avoids a crash if it ever does)
DEFAULT_MAE = sum(MAE_BY_HORIZON.values()) / len(MAE_BY_HORIZON)


def mae_for_horizon(minutes_ahead: int) -> float:
    if minutes_ahead in MAE_BY_HORIZON:
        return MAE_BY_HORIZON[minutes_ahead]

    # Pick the closest trained horizon instead of defaulting blindly
    closest = min(MAE_BY_HORIZON.keys(), key=lambda h: abs(h - minutes_ahead))
    return MAE_BY_HORIZON.get(closest, DEFAULT_MAE)


# --------------------------------------------------
# FEATURE LIST
# --------------------------------------------------

FEATURE_COLUMNS = [
    "hours_from_start",
    "views",
    "growth_1_record",
    "growth_5_records",
    "growth_15_records",
    "acceleration",
    "like_ratio",
    "comment_ratio",
    "prediction_horizon",
]


# --------------------------------------------------
# LOAD VIDEO HISTORY
# --------------------------------------------------

def load_video_history(video_id: str) -> pd.DataFrame:

    conn = sqlite3.connect(DB_PATH)

    query = """
        SELECT
            video_id,
            video_name,
            timestamp,
            views,
            likes,
            comments
        FROM view_history
        WHERE video_id = ?
        ORDER BY timestamp
    """

    df = pd.read_sql_query(
        query,
        conn,
        params=(video_id,)
    )

    conn.close()

    if df.empty:
        raise ValueError(
            "No history found for this video."
        )

    df["timestamp"] = pd.to_datetime(
        df["timestamp"]
    )

    return df



# --------------------------------------------------
# FEATURE ENGINEERING
# --------------------------------------------------

def build_features(df: pd.DataFrame) -> pd.DataFrame:

    df = df.copy()


    df["growth_1_record"] = (
        df["views"]
        .diff()
    )


    df["growth_5_records"] = (
        df["growth_1_record"]
        .rolling(
            5,
            min_periods=1
        )
        .mean()
    )


    df["growth_15_records"] = (
        df["growth_1_record"]
        .rolling(
            15,
            min_periods=1
        )
        .mean()
    )


    df["acceleration"] = (
        df["growth_1_record"]
        .diff()
    )


    df["like_ratio"] = (
        df["likes"]
        /
        df["views"]
    ).fillna(0)


    df["comment_ratio"] = (
        df["comments"]
        /
        df["views"]
    ).fillna(0)


    df["hours_from_start"] = (
        (
            df["timestamp"]
            -
            df["timestamp"].min()
        )
        .dt.total_seconds()
        /
        3600
    )


    df = df.fillna(0)


    return df



# --------------------------------------------------
# PREDICTION FUNCTION
# --------------------------------------------------

def predict_views(
    video_id: str,
    minutes_ahead: int
):

    history = load_video_history(
        video_id
    )


    history = build_features(
        history
    )


    latest = history.iloc[-1]


    row = latest.to_dict()


    # prediction_horizon is now in MINUTES directly, matching how
    # the model was trained - no more row-count conversion that
    # assumed a fixed 5-minute tracking interval.
    row["prediction_horizon"] = minutes_ahead


    X = pd.DataFrame(
        [
            [
                row[column]
                for column in FEATURE_COLUMNS
            ]
        ],
        columns=FEATURE_COLUMNS
    )


    predicted_gain = float(
        MODEL.predict(X)[0]
    )


    current_views = int(
        latest["views"]
    )


    predicted_views = int(
        current_views
        +
        predicted_gain
    )


    # --------------------------------------------------
    # CONFIDENCE + RANGE
    # Uses the MAE trained specifically for this horizon, not a
    # single blanket number for every prediction distance.
    # --------------------------------------------------

    error_margin = mae_for_horizon(minutes_ahead)


    lower_bound = max(
        0,
        predicted_views - error_margin
    )


    upper_bound = (
        predicted_views
        +
        error_margin
    )


    confidence = (
        100
        -
        (
            error_margin
            /
            max(predicted_views, 1)
            *
            100
        )
    )


    confidence = max(
        50,
        min(
            95,
            confidence
        )
    )


    # --------------------------------------------------
    # RETURN RESULT
    # --------------------------------------------------

    return {

        "video_id": video_id,

        "current_views": current_views,

        "predicted_gain": int(
            predicted_gain
        ),

        "predicted_views": predicted_views,

        "prediction_horizon": minutes_ahead,

        "prediction_minutes": minutes_ahead,

        "confidence": round(
            confidence,
            1
        ),

        "prediction_range": {

            "lower": int(
                lower_bound
            ),

            "upper": int(
                upper_bound
            )

        }

    }



# --------------------------------------------------
# TEST RUN
# --------------------------------------------------

if __name__ == "__main__":


    VIDEO_ID = input(
        "Video ID: "
    ).strip()


    result = predict_views(
        VIDEO_ID,
        60
    )


    print()


    print("============================")
    print("AI VIEW PREDICTION")
    print("============================")


    for key, value in result.items():

        print(
            f"{key:20}: {value}"
        )