import pandas as pd

# Load processed data
df = pd.read_csv("processed_data.csv")

# How far into the future to predict
PREDICT_AFTER = 120of 

# Create target column
df["Future_Views"] = df["Views"].shift(-PREDICT_AFTER)

# Remove rows that don't have a future value
df = df.dropna()

# Save the training data
df.to_csv("training_data.csv", index=False)

print(df.head())

print("\n✅ training_data.csv created!")
print(f"Total training rows: {len(df)}")