# 🎬 Dashboard Konten Netflix

**Nama:** MUHAMMAD ADRIAN OKTAV AL FATTAH 
**NPM:** 241051009  
**Mata Kuliah:** Visualisasi Data (UTS Ganjil TA 2026/2027) | Universitas Dirgantara Marsekal Suryadarma

## 🔗 Tautan

- **Live Dashboard:** https://netflix-dashboard-241051009utsvd.streamlit.app
- **Dataset (Kaggle):** https://www.kaggle.com/datasets/shivamb/netflix-shows

## 📌 Latar Belakang

Netflix menambah ribuan film dan serial ke katalognya setiap tahun. Dashboard interaktif ini
membantu menjawab pertanyaan: bagaimana komposisi kontennya, kapan pertumbuhannya terjadi,
dan dari negara mana konten berasal. Data yang dipakai adalah dataset *Netflix Movies and TV Shows*
dari Kaggle (8.807 baris, 12 kolom) yang dibersihkan menjadi 8.797 baris.

## 🧹 Pengolahan Data

Skrip `clean_data.py` melakukan: merapikan spasi, menghapus duplikat, memperbaiki nilai
`rating` yang tertukar dengan `duration`, mengisi data kosong dengan "Unknown", mengubah
`date_added` menjadi tanggal (10 baris tanpa tanggal dibuang), memisahkan durasi film (menit)
dan jumlah season serial, serta mengambil negara dan genre utama.

## 📊 Fitur Dashboard

- **4 KPI:** Total Judul, Persentase Film, Rata-rata Durasi Film, Jumlah Negara
- **5 jenis chart:** line (tren per tahun), donut (proporsi), bar horizontal (top 10 negara), heatmap (bulan x tahun), histogram (durasi film)
- **3 filter interaktif:** rentang tahun ditambahkan, tipe konten, negara
- **Insight dinamis** yang berubah mengikuti filter

## 💡 Key Insights

1. **Film mendominasi katalog.** Sekitar 69,7% judul adalah film dan 30,3% serial TV.
2. **Pertumbuhan melonjak sejak 2016.** Penambahan judul per tahun naik tajam setelah 2015 dan memuncak pada 2019, dengan film menembus sekitar 1.400 judul pada tahun itu.
3. **Penurunan 2020-2021 perlu dibaca hati-hati.** Data 2021 belum mencakup satu tahun penuh, jadi penurunan di ujung grafik tidak berarti Netflix berhenti menambah konten.
4. **Durasi film rata-rata sekitar 100 menit**, dengan sebaran yang terkonsentrasi di kisaran durasi film pada umumnya (lihat histogram).
5. **[ISI: negara dengan konten terbanyak, mis. "Amerika Serikat menjadi negara asal konten terbanyak (... judul)"]**
6. **[ISI: bulan tersibuk menambah judul, dari heatmap]**

(Pilih 3 sampai 5 insight yang paling kuat, hapus sisanya.)

## 🚀 Menjalankan Secara Lokal

```bash
git clone https://github.com/FlashLightzero/netflix-dashboard.git
cd netflix-dashboard
pip install -r requirements.txt
streamlit run app.py
```

Dashboard terbuka di `http://localhost:8501`.

## 📁 Struktur Repositori

```
netflix-dashboard/
├── app.py              # aplikasi dashboard Streamlit
├── clean_data.py       # skrip pembersihan data
├── requirements.txt    # dependensi
├── .streamlit/config.toml
└── data/
    ├── netflix_titles.csv   # data mentah
    └── netflix_clean.csv    # data bersih
```

## 🛠️ Teknologi

Python, Streamlit, Pandas, Plotly. Di-deploy di Streamlit Community Cloud.
