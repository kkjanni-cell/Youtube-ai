import pandas as pd

# Read tracker
df = pd.read_csv("Tracker.csv")

# Clean numbers
df["Views"] = (
    df["Views"]
    .astype(str)
    .str.replace(",", "", regex=False)
    .astype(int)
)

df["Count"] = (
    df["Count"]
    .astype(str)
    .str.replace(",", "", regex=False)
    .astype(int)
)

df["Time"] = df["Time"].astype(str)

# Oldest first
df = df.sort_values("Time").reset_index(drop=True)

# Minute since upload
df["Minute"] = range(len(df))

print(df.head())

# Save
df.to_csv("prepared_data.csv", index=False)

print(f"\n✅ Prepared {len(df)} rows")