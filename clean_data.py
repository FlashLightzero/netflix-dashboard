import pandas as pd

# 1. Baca data mentah
df = pd.read_csv("data/netflix_titles.csv")
print("Baris awal:", len(df))

# 2. Rapikan spasi berlebih di semua kolom teks
for col in df.select_dtypes(include="str").columns:
    df[col] = df[col].str.strip()

# 3. Hapus duplikat
df = df.drop_duplicates()

# 4. Perbaiki rating yang salah tempat (isinya "xx min")
mask = df["rating"].str.contains("min", na=False)
df.loc[mask, "duration"] = df.loc[mask, "rating"]
df.loc[mask, "rating"] = None

# 5. Isi data kosong pada kolom teks
for col in ["director", "cast", "country", "rating"]:
    df[col] = df[col].fillna("Unknown")

# 6. Tanggal: ubah ke format tanggal, buang yang kosong
df["date_added"] = pd.to_datetime(df["date_added"], format="%B %d, %Y", errors="coerce")
df = df.dropna(subset=["date_added"]).copy()
df["year_added"] = df["date_added"].dt.year.astype(int)
df["month_added"] = df["date_added"].dt.month.astype(int)

# 7. Duration: pisahkan angka untuk film (menit) dan serial (season)
angka = pd.to_numeric(df["duration"].str.extract(r"(\d+)")[0], errors="coerce")
df["duration_min"] = angka.where(df["type"] == "Movie")
df["seasons"] = angka.where(df["type"] == "TV Show")

# 8. Kolom utama untuk grafik
def nilai_pertama(teks):
    bagian = [b.strip() for b in str(teks).split(",") if b.strip()]
    return bagian[0] if bagian else "Unknown"

df["country_main"] = df["country"].apply(nilai_pertama)
df["genre_main"] = df["listed_in"].apply(nilai_pertama)

# 9. Simpan data bersih
df.to_csv("data/netflix_clean.csv", index=False)

print("Baris akhir:", len(df))
print("\nData kosong tersisa:")
print(df.isnull().sum())
print("\nJumlah per type:")
print(df["type"].value_counts())
print("\nRentang tahun ditambahkan:", df["year_added"].min(), "-", df["year_added"].max())
print("\nContoh kolom baru:")
print(df[["title", "year_added", "duration_min", "seasons", "country_main", "genre_main"]].head())