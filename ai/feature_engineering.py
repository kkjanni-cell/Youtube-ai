import sqlite3
import pandas as pd

DB_PATH = "database/youtube.db"

# -----------------------
# LOAD DATA
# -----------------------

conn = sqlite3.connect(DB_PATH)

query = """
SELECT
    video_id,
    video_name,
    timestamp,
    views,
    view_gain,
    likes,
    comments
FROM view_history
ORDER BY timestamp
"""

df = pd.read_sql_query(query, conn)

conn.close()

# -----------------------
# CLEAN DATA
# -----------------------

df["timestamp"] = pd.to_datetime(df["timestamp"])

df = df.sort_values(
    ["video_name", "timestamp"]
).reset_index(drop=True)

# -----------------------
# FEATURE ENGINEERING
# -----------------------

# Views gained since previous record
df["growth_1_record"] = (
    df.groupby("video_name")["views"]
      .diff()
)

# Average growth over last 5 records
df["growth_5_records"] = (
    df.groupby("video_name")["growth_1_record"]
      .transform(lambda x: x.rolling(5, min_periods=1).mean())
)

df["growth_15_records"] = (
    df.groupby("video_name")["growth_1_record"]
      .transform(lambda x: x.rolling(15, min_periods=1).mean())
)

# Growth acceleration
df["acceleration"] = (
    df.groupby("video_name")["growth_1_record"]
      .diff()
)

# Like ratio
df["like_ratio"] = (
    df["likes"] / df["views"]
)

# Comment ratio
df["comment_ratio"] = (
    df["comments"] / df["views"]
)

# Hours since tracking started
df["hours_from_start"] = (
    df.groupby("video_name")["timestamp"]
      .transform(lambda x: (x - x.min()).dt.total_seconds() / 3600)
)

# Remove rows with missing values
df = df.dropna().reset_index(drop=True)

# -----------------------
# SAVE
# -----------------------

df.to_csv(
    "data/processed_data.csv",
    index=False
)

print("✅ Feature engineering completed")
print(f"Rows: {len(df)}")

print(df.head())