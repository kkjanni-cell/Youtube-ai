import pandas as pd


# -----------------------------------
# SETTINGS
# -----------------------------------

TRACKING_INTERVAL_MINUTES = 5

# User-facing prediction times
PREDICTION_MINUTES = [
    10,
    30,
    60,
]


# Convert minutes into records
PREDICTION_HORIZONS = [
    minutes // TRACKING_INTERVAL_MINUTES
    for minutes in PREDICTION_MINUTES
]


# -----------------------------------
# LOAD PROCESSED DATA
# -----------------------------------

df = pd.read_csv(
    "data/processed_data.csv"
)


# Make sure data is ordered correctly

df = df.sort_values(
    [
        "video_name",
        "timestamp"
    ]
).reset_index(drop=True)



training_rows = []


# -----------------------------------
# CREATE MULTI HORIZON DATASET
# -----------------------------------

for video_name, video_df in df.groupby("video_name"):

    video_df = video_df.reset_index(drop=True)


    for horizon in PREDICTION_HORIZONS:

        future_views = (
            video_df["views"]
            .shift(-horizon)
        )


        temp = video_df.copy()

        temp["target_views"] = future_views

        temp["target_gain"] = (
            temp["target_views"]
            - temp["views"]
        )


        temp["prediction_horizon"] = horizon


        training_rows.append(temp)



# Combine everything

training_df = pd.concat(
    training_rows,
    ignore_index=True
)



# Remove rows where future data does not exist

training_df = (
    training_df
    .dropna()
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
    FEATURES + TARGETS
]


# -----------------------------------
# SAVE
# -----------------------------------

training_df.to_csv(
    "data/training_dataset.csv",
    index=False
)


print("\n✅ Multi Horizon Training Dataset Created")

print("-----------------------------")

print("Rows:", len(training_df))

print(
    "Horizons used:",
    PREDICTION_HORIZONS
)

print("\nSample:")

print(
    training_df.head()
)