import pandas as pd


def calculate_metrics(video_df):
    """
    Calculate dashboard metrics for a selected video.
    """

    video_df = video_df.copy()

    video_df["timestamp"] = pd.to_datetime(video_df["timestamp"])

    video_df = video_df.sort_values("timestamp")

    latest = video_df.iloc[-1]

    current_time = latest["timestamp"]

    # -------------------------------------------------
    # Last 1 Hour
    # -------------------------------------------------

    last_1_hour = video_df[
        video_df["timestamp"] >= current_time - pd.Timedelta(hours=1)
    ]

    last_1_hour_gain = int(
        last_1_hour["view_gain"].fillna(0).sum()
    )

    # -------------------------------------------------
    # Last 24 Hours
    # -------------------------------------------------

    last_24_hours = video_df[
        video_df["timestamp"] >= current_time - pd.Timedelta(hours=24)
    ]

    last_24_hour_gain = int(
        last_24_hours["view_gain"].fillna(0).sum()
    )

    # -------------------------------------------------
    # Average Hourly Growth
    # -------------------------------------------------

    total_hours = (
        current_time - video_df["timestamp"].min()
    ).total_seconds() / 3600

    if total_hours > 0:
        avg_hourly_growth = int(
            video_df["view_gain"].fillna(0).sum() / total_hours
        )
    else:
        avg_hourly_growth = 0

    # -------------------------------------------------
    # Peak Growth
    # -------------------------------------------------

    peak_growth = int(
        video_df["view_gain"].fillna(0).max()
    )

    # -------------------------------------------------
    # Total Growth
    # -------------------------------------------------

    total_growth = int(
        video_df["view_gain"].fillna(0).sum()
    )

    # -------------------------------------------------
    # Views Per Minute
    # -------------------------------------------------

    total_minutes = (
        current_time - video_df["timestamp"].min()
    ).total_seconds() / 60

    if total_minutes > 0:
        views_per_minute = round(
            total_growth / total_minutes,
            2
        )
    else:
        views_per_minute = 0

    return {
        "latest": latest,
        "last_1_hour_gain": last_1_hour_gain,
        "last_24_hour_gain": last_24_hour_gain,
        "avg_hourly_growth": avg_hourly_growth,
        "peak_growth": peak_growth,
        "total_growth": total_growth,
        "views_per_minute": views_per_minute,
    }