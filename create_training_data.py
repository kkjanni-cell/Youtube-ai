import pandas as pd

PREDICT_AFTER = 120  # 2 hours

df = pd.read_csv("processed_data.csv")

df["Future_Views"] = df["Views"].shift(-PREDICT_AFTER)

df = df.dropna()

df.to_csv("training_data.csv", index=False)

print("✅ training_data.csv created")
print("Rows available for training:", len(df))