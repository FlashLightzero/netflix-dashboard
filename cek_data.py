import pandas as pd

df = pd.read_csv("data/netflix_titles.csv")

print("Jumlah baris & kolom:", df.shape)
print("\nTipe data:")
print(df.dtypes)
print("\nData kosong per kolom:")
print(df.isnull().sum())
print("\n5 baris pertama:")
print(df.head())