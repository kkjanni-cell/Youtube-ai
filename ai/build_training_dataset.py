import pandas as pd

PREDICTION_HORIZON = 120  # minutes

# Load prepared data
df = pd.read_csv("prepared_data.csv")

# -----------------------------
# Feature Engineering
# -----------------------------

df["Growth_1m"] = df["Views"].diff()
df["Growth_5m"] = df["Growth_1m"].rolling(5).mean()
df["Growth_15m"] = df["Growth_1m"].rolling(15).mean()
df["Growth_30m"] = df["Views"] - df["Views"].shift(30)
df["Acceleration"] = df["Growth_1m"].diff()

# Remove missing values
df = df.dropna().reset_index(drop=True)


df["Target_Views"] = df["Views"].shift(-PREDICTION_HORIZON)
df["Target_Gain"] = df["Target_Views"] - df["Views"]
# Remove rows without future values
df = df.dropna().reset_index(drop=True)

# Add horizon
df["Horizon"] = PREDICTION_HORIZON

# Keep only useful columns
training_df = df[
    [
        "Minute",
        "Views",
        "Growth_1m",
        "Growth_5m",
        "Growth_15m",
        "Growth_30m",
        "Acceleration",
        "Horizon",
        "Target_Views",
        "Target_Gain"
    ]
]

training_df.to_csv("training_dataset.csv", index=False)

print("\n✅ Training dataset created!")
print("Rows:", len(training_df))
print()
print(training_df.head())