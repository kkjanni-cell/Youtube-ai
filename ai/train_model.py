import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, r2_score

from xgboost import XGBRegressor

# Load training data
df = pd.read_csv("training_dataset.csv")

# Features
FEATURES = [
    "Minute",
    "Views",
    "Growth_1m",
    "Growth_5m",
    "Growth_15m",
    "Growth_30m",
    "Acceleration",
    "Horizon"
]

X = df[FEATURES]

# Predict future gain
y = df["Target_Gain"]

# Train/Test Split
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42
)

# Model
model = XGBRegressor(
    n_estimators=300,
    learning_rate=0.05,
    max_depth=5,
    subsample=0.8,
    colsample_bytree=0.8,
    random_state=42
)

# Train
model.fit(X_train, y_train)

# Predict
predictions = model.predict(X_test)

# Metrics
mae = mean_absolute_error(y_test, predictions)
r2 = r2_score(y_test, predictions)

print("\n============================")
print("MODEL RESULTS")
print("============================")
print(f"Mean Absolute Error : {mae:,.0f} views")
print(f"R² Score            : {r2:.4f}")

# Save model
joblib.dump(model, "youtube_predictor.pkl")

print("\n✅ Model saved as youtube_predictor.pkl")