import pandas as pd

df = pd.read_csv("tracker.csv")

print("=" * 40)
print("DATASET INFORMATION")
print("=" * 40)

print("Total Rows:", len(df))
print()

print("First 5 rows:")
print(df.head())

print()

print("Last 5 rows:")
print(df.tail())

print()

print("First Time:", df.iloc[0]["Time"])
print("Last Time :", df.iloc[-1]["Time"])