import sqlite3
import pandas as pd

DB_PATH = "database/youtube.db"

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

# Convert timestamp
df["timestamp"] = pd.to_datetime(df["timestamp"])

# Sort
df = df.sort_values(
    ["video_name", "timestamp"]
).reset_index(drop=True)

# Minutes since first record for each video
df["minutes_from_start"] = (
    df.groupby("video_name")["timestamp"]
      .transform(lambda x: (x - x.min()).dt.total_seconds() / 60)
)

# Hours since first record
df["hours_from_start"] = (
    df["minutes_from_start"] / 60
)

print(df.head())

df.to_csv(
    "data/prepared_data.csv",
    index=False
)

print(f"\n✅ Prepared {len(df)} records")