import pandas as pd


# -----------------------------------
# SETTINGS
# -----------------------------------

# User-facing prediction times (minutes)
PREDICTION_MINUTES = [
    10,
    30,
    60,
    120,
]

# How close (in minutes) an actual future record must be to our
# target time to count as a valid match. Tighter for short horizons,
# looser for long ones, since tracking isn't always perfectly on-grid
# (sleep gaps, delayed runs, etc).
def tolerance_for(horizon_minutes):
    return max(2.5, horizon_minutes * 0.15)


# -----------------------------------
# LOAD PROCESSED DATA
# -----------------------------------

df = pd.read_csv(
    "data/processed_data.csv"
)

df["timestamp"] = pd.to_datetime(df["timestamp"])

# Group by video_id (the real unique key) - not video_name
df = df.sort_values(
    [
        "video_id",
        "timestamp"
    ]
).reset_index(drop=True)


training_rows = []


# -----------------------------------
# CREATE MULTI HORIZON DATASET
# (matched by actual elapsed time, not row count)
# -----------------------------------

for video_id, video_df in df.groupby("video_id"):

    video_df = video_df.sort_values("timestamp").reset_index(drop=True)

    # Lookup table of this video's own (timestamp -> views) pairs,
    # used to find the actual future snapshot closest to our target time.
    lookup = video_df[["timestamp", "views"]].rename(
        columns={"timestamp": "target_time", "views": "target_views"}
    )

    for horizon_minutes in PREDICTION_MINUTES:

        query = video_df.copy()
        query["target_time"] = query["timestamp"] + pd.Timedelta(minutes=horizon_minutes)

        tol = pd.Timedelta(minutes=tolerance_for(horizon_minutes))

        query = query.sort_values("target_time")
        lookup_sorted = lookup.sort_values("target_time")

        merged = pd.merge_asof(
            query,
            lookup_sorted,
            on="target_time",
            direction="nearest",
            tolerance=tol,
        )

        merged["target_gain"] = merged["target_views"] - merged["views"]

        # prediction_horizon is now in MINUTES directly - matches
        # exactly what the user picks in the dashboard dropdown.
        merged["prediction_horizon"] = horizon_minutes

        training_rows.append(merged)


# Combine everything

training_df = pd.concat(
    training_rows,
    ignore_index=True
)


# Remove rows where no valid future match was found within tolerance
# (this naturally drops rows around tracking gaps, instead of
# silently mislabeling them)

training_df = (
    training_df
    .dropna(subset=["target_views", "target_gain"])
    .reset_index(drop=True)
)


# -----------------------------------
# TIME-BASED TRAIN/TEST SPLIT (per video_id)
# Avoids the leakage you'd get from a random shuffled split
# on time-series data - each video's own last 20% (by time)
# becomes test, never mixed into train.
# -----------------------------------

def assign_split(group):
    group = group.sort_values("timestamp")
    cutoff = int(len(group) * 0.8)
    labels = ["train"] * cutoff + ["test"] * (len(group) - cutoff)
    group = group.copy()
    group["split"] = labels
    return group

training_df = (
    training_df
    .groupby("video_id", group_keys=False)
    .apply(assign_split)
    .reset_index(drop=True)
)


# -----------------------------------
# FEATURES
# -----------------------------------

FEATURES = [
    "hours_from_start",
    "views",
    "growth_1_record",
    "growth_5_records",
    "growth_15_records",
    "acceleration",
    "like_ratio",
    "comment_ratio",
    "prediction_horizon"
]


TARGETS = [
    "target_views",
    "target_gain"
]


training_df = training_df[
    FEATURES + TARGETS + ["split"]
]


# -----------------------------------
# SAVE
# -----------------------------------

training_df.to_csv(
    "data/training_dataset.csv",
    index=False
)


print("\n✅ Multi Horizon Training Dataset Created (time-matched)")

print("-----------------------------")

print("Rows:", len(training_df))

print(
    "Horizons used (minutes):",
    PREDICTION_MINUTES
)

print(
    "Train rows:", (training_df["split"] == "train").sum(),
    "| Test rows:", (training_df["split"] == "test").sum()
)

print("\nSample:")

print(
    training_df.head()
)