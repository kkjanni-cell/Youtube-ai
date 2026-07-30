import pandas as pd
import joblib

from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, r2_score

# Load window dataset
df = pd.read_csv("window_dataset.csv")

# Features
X = df.drop(columns=["Target_Gain"])

# Target
y = df["Target_Gain"]

# -----------------------------
# TIME-BASED TRAIN / TEST SPLIT
# -----------------------------
split = int(len(df) * 0.8)

X_train = X.iloc[:split]
X_test = X.iloc[split:]

y_train = y.iloc[:split]
y_test = y.iloc[split:]

print(f"Training rows : {len(X_train)}")
print(f"Testing rows  : {len(X_test)}")

# Train model
model = RandomForestRegressor(
    n_estimators=300,
    random_state=42,
    n_jobs=-1
)

model.fit(X_train, y_train)

# Predict
pred = model.predict(X_test)

# Metrics
mae = mean_absolute_error(y_test, pred)
r2 = r2_score(y_test, pred)

print("\n========================")
print("WINDOW MODEL RESULTS")
print("========================")
print(f"MAE : {mae:,.0f} views")
print(f"R²  : {r2:.4f}")

# Save model
joblib.dump(model, "window_model.pkl")

print("\n✅ Model saved as window_model.pkl")