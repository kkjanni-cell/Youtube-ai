import pandas as pd
import joblib

PREDICTION_HORIZON = 120

# Load model
model = joblib.load("youtube_predictor.pkl")

# Load latest tracker
df = pd.read_csv("prepared_data.csv")

# -------------------------
# Feature Engineering
# -------------------------

df["Growth_1m"] = df["Views"].diff()
df["Growth_5m"] = df["Growth_1m"].rolling(5).mean()
df["Growth_15m"] = df["Growth_1m"].rolling(15).mean()
df["Growth_30m"] = df["Views"] - df["Views"].shift(30)
df["Acceleration"] = df["Growth_1m"].diff()

df = df.dropna().reset_index(drop=True)

# Use the latest available row
latest = df.iloc[-1]

features = [[
    latest["Minute"],
    latest["Views"],
    latest["Growth_1m"],
    latest["Growth_5m"],
    latest["Growth_15m"],
    latest["Growth_30m"],
    latest["Acceleration"],
    PREDICTION_HORIZON
]]

predicted_gain = model.predict(features)[0]

predicted_views = latest["Views"] + predicted_gain

print("\n============================")
print("YOUTUBE VIEW PREDICTION")
print("============================")

print(f"Current Minute : {int(latest['Minute'])}")
print(f"Current Views  : {int(latest['Views']):,}")

print(f"\nPrediction after {PREDICTION_HORIZON} minutes")

print(f"Expected Gain  : {int(predicted_gain):,}")
print(f"Expected Views : {int(predicted_views):,}")