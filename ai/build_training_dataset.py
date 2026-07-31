import pandas as pd

# -----------------------------------
# SETTINGS
# -----------------------------------

PREDICTION_HORIZON = 2  # Number of future records

# -----------------------------------
# LOAD PROCESSED DATA
# -----------------------------------

df = pd.read_csv("data/processed_data.csv")

# -----------------------------------
# TARGET
# -----------------------------------

df["target_views"] = (
    df.groupby("video_name")["views"]
      .shift(-PREDICTION_HORIZON)
)

df["target_gain"] = (
    df["target_views"] - df["views"]
)

# Remove rows without future values
df = df.dropna().reset_index(drop=True)

# Horizon feature
df["prediction_horizon"] = PREDICTION_HORIZON

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

training_df = df[
    FEATURES + TARGETS
]

# -----------------------------------
# SAVE
# -----------------------------------

training_df.to_csv(
    "data/training_dataset.csv",
    index=False
)

print("✅ Training dataset created")

print(f"Rows: {len(training_df)}")

print(training_df.head())