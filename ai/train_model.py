import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
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

X = df[FEATURES]

# Predict future view gain
y = df["target_gain"]

# -----------------------
# TRAIN / TEST SPLIT
# -----------------------

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42
)

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
# EVALUATE
# -----------------------

predictions = model.predict(X_test)

mae = mean_absolute_error(y_test, predictions)
r2 = r2_score(y_test, predictions)

print("\n==============================")
print("MODEL RESULTS")
print("==============================")
print(f"Rows Used          : {len(df)}")
print(f"Mean Absolute Error: {mae:,.2f}")
print(f"R² Score           : {r2:.4f}")

# -----------------------
# SAVE MODEL
# -----------------------

joblib.dump(model, "models/youtube_predictor.pkl")

print("\n✅ Model saved successfully!")