import pandas as pd

# -----------------------------
# SETTINGS
# -----------------------------
WINDOW_SIZE = 120      # Last 120 minutes
PREDICT_AFTER = 120    # Predict 120 minutes later
# -----------------------------

# Load prepared data
df = pd.read_csv("prepared_data.csv")
# Remove the first row (initial count is not a true 1-minute growth)
df = df.iloc[1:].reset_index(drop=True)

windows = []

# Start only after enough history exists
for i in range(WINDOW_SIZE, len(df) - PREDICT_AFTER):

    history = df.iloc[i-WINDOW_SIZE:i]

    # Last 120 one-minute growth values
    growth = history["Count"].tolist()

    # Current views
    current_views = history.iloc[-1]["Views"]

    # Future views
    future_views = df.iloc[i + PREDICT_AFTER]["Views"]

    target_gain = future_views - current_views

    row = growth + [current_views, target_gain]

    windows.append(row)

# Create column names
columns = []

for i in range(WINDOW_SIZE):
    columns.append(f"Growth_{i+1}")

columns.append("Current_Views")
columns.append("Target_Gain")

window_df = pd.DataFrame(windows, columns=columns)

window_df.to_csv("window_dataset.csv", index=False)

print("\n✅ Window dataset created!")

print("Rows :", len(window_df))
print("Columns :", len(window_df.columns))

print("\nFirst 5 columns:")
print(window_df.iloc[:, :5])

print("\nLast columns:")
print(window_df[["Current_Views", "Target_Gain"]].head())