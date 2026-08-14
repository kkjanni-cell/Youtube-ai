import json

import pandas as pd
import joblib

from sklearn.metrics import mean_absolute_error, r2_score

from xgboost import XGBRegressor

# -----------------------
# LOAD TRAINING DATA
# -----------------------

df = pd.read_csv("data/training_dataset.csv")

# -----------------------
# FEATURES
# -----------------------

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

# -----------------------
# TIME-BASED TRAIN / TEST SPLIT
# Uses the 'split' column already assigned per-video in
# build_training_dataset.py - never randomly shuffled, since this
# is time-series data and a random split would leak future
# information into training.
# -----------------------

train_df = df[df["split"] == "train"]
test_df = df[df["split"] == "test"]

X_train = train_df[FEATURES]
y_train = train_df["target_gain"]

X_test = test_df[FEATURES]
y_test = test_df["target_gain"]

# -----------------------
# MODEL
# -----------------------

model = XGBRegressor(
    n_estimators=500,
    learning_rate=0.05,
    max_depth=6,
    subsample=0.8,
    colsample_bytree=0.8,
    random_state=42
)

# -----------------------
# TRAIN
# -----------------------

model.fit(X_train, y_train)

# -----------------------
# EVALUATE (overall)
# -----------------------

predictions = model.predict(X_test)

mae = mean_absolute_error(y_test, predictions)
r2 = r2_score(y_test, predictions)

print("\n==============================")
print("MODEL RESULTS (overall)")
print("==============================")
print(f"Rows Used          : {len(df)}")
print(f"Mean Absolute Error: {mae:,.2f}")
print(f"R² Score           : {r2:.4f}")

# -----------------------
# EVALUATE PER HORIZON
# A 10-minute prediction and a 2-hour prediction should NOT share
# the same confidence range - this computes a separate MAE for
# each horizon so predict.py can report honest uncertainty.
# -----------------------

test_eval = test_df.copy()
test_eval["predicted_gain"] = predictions

mae_by_horizon = {}

print("\n==============================")
print("MODEL RESULTS (per horizon)")
print("==============================")

for horizon, group in test_eval.groupby("prediction_horizon"):
    horizon_mae = mean_absolute_error(
        group["target_gain"], group["predicted_gain"]
    )
    mae_by_horizon[int(horizon)] = round(float(horizon_mae), 2)
    print(f"Horizon {int(horizon):>4} min | rows: {len(group):>6} | MAE: {horizon_mae:,.2f}")

# -----------------------
# SAVE MODEL + PER-HORIZON MAE
# -----------------------

joblib.dump(model, "models/youtube_predictor.pkl")

with open("models/mae_by_horizon.json", "w") as f:
    json.dump(mae_by_horizon, f, indent=2)

print("\n✅ Model saved to models/youtube_predictor.pkl")
print("✅ Per-horizon MAE saved to models/mae_by_horizon.json")