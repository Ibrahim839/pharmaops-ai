from numpy import average
import pandas as pd

file_path = "data/pharmaceutical-inventory-supply-chains.csv"

df = pd.read_csv(file_path)

print("Shape:", df.shape)
print("\nColumns:")
print(df.columns.tolist())

print("\nFirst 5 rows:")
print(df.head())


