import pandas as pd

# Read the tracker
df = pd.read_csv("Tracker.csv")

# Clean numeric columns
df["Views"] = df["Views"].astype(str).str.replace(",", "", regex=False).astype(int)
df["Count"] = df["Count"].astype(str).str.replace(",", "", regex=False).astype(int)

# Convert Time
df["Time"] = pd.to_datetime(df["Time"], format="%H:%M:%S")

# Sort from oldest to newest
df = df.sort_values("Time").reset_index(drop=True)

# ---------- Features ----------

df["Growth_1min"] = df["Views"].diff()

df["Growth_5min"] = df["Growth_1min"].rolling(5).mean()

df["Growth_15min"] = df["Growth_1min"].rolling(15).mean()

df["Acceleration"] = df["Growth_1min"].diff()

df["Minutes"] = range(len(df))

# Remove rows with missing values
df = df.dropna()

# Save
df.to_csv("processed_data.csv", index=False)

print("✅ processed_data.csv created")
print("Rows:", len(df))