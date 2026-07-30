import pandas as pd
import joblib
from sklearn.metrics import mean_absolute_error

# -------------------------
# SETTINGS
# -------------------------
HORIZON = 120      # Predict 120 minutes ahead
START_MINUTE = 30  # Need enough history
# -------------------------

# Load model
model = joblib.load("youtube_predictor.pkl")

# Load prepared data
df = pd.read_csv("prepared_data.csv")

# Feature Engineering
df["Growth_1m"] = df["Views"].diff()
df["Growth_5m"] = df["Growth_1m"].rolling(5).mean()
df["Growth_15m"] = df["Growth_1m"].rolling(15).mean()
df["Growth_30m"] = df["Views"] - df["Views"].shift(30)
df["Acceleration"] = df["Growth_1m"].diff()

df = df.dropna().reset_index(drop=True)

results = []

# Loop through every possible prediction point
for i in range(START_MINUTE, len(df) - HORIZON):

    row = df.iloc[i]

    features = [[
        row["Minute"],
        row["Views"],
        row["Growth_1m"],
        row["Growth_5m"],
        row["Growth_15m"],
        row["Growth_30m"],
        row["Acceleration"],
        HORIZON
    ]]

    predicted_gain = model.predict(features)[0]
    predicted_views = row["Views"] + predicted_gain

    actual_views = df.iloc[i + HORIZON]["Views"]

    error = predicted_views - actual_views
    abs_error = abs(error)
    pct_error = abs_error / actual_views * 100

    results.append([
        row["Minute"],
        predicted_views,
        actual_views,
        error,
        pct_error
    ])

results = pd.DataFrame(
    results,
    columns=[
        "Minute",
        "Predicted",
        "Actual",
        "Error",
        "Pct_Error"
    ]
)

results.to_csv("backtest_results.csv", index=False)

print("\n==============================")
print("BACKTEST RESULTS")
print("==============================")

print(results.head())

print("\nAverage Error (%) :",
      round(results["Pct_Error"].mean(),2))

print("Median Error (%) :",
      round(results["Pct_Error"].median(),2))

print("Maximum Error (%) :",
      round(results["Pct_Error"].max(),2))

print("\nSaved to backtest_results.csv")