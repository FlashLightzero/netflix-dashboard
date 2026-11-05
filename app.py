import pandas as pd
import plotly.express as px
import streamlit as st

# Palet warna konsisten di seluruh dashboard
WARNA = {"Movie": "#E50914", "TV Show": "#B3B3B3"}
# ---------- Pengaturan halaman ----------
st.set_page_config(page_title="Netflix Dashboard", page_icon="🎬", layout="wide")


# ---------- Load data (di-cache supaya cepat) ----------
@st.cache_data
def load_data():
    data = pd.read_csv("data/netflix_clean.csv", parse_dates=["date_added"])
    data["country_main"] = data["country_main"].fillna("Unknown")
    data["genre_main"] = data["genre_main"].fillna("Unknown")
    return data

df = load_data()

# ---------- Sidebar: filter ----------
st.sidebar.header("🎛️ Filter")

tahun_min, tahun_max = int(df["year_added"].min()), int(df["year_added"].max())
rentang_tahun = st.sidebar.slider(
    "Tahun ditambahkan ke Netflix", tahun_min, tahun_max, (tahun_min, tahun_max)
)

semua_tipe = sorted(df["type"].unique())
tipe = st.sidebar.multiselect("Tipe konten", semua_tipe, default=semua_tipe)

daftar_negara = sorted(df["country_main"].unique())
negara = st.sidebar.multiselect(
    "Negara (kosongkan = semua)",
    daftar_negara,
    default=[],
    placeholder="Semua negara",
)

# ---------- Terapkan filter ----------
filtered = df[df["year_added"].between(*rentang_tahun) & df["type"].isin(tipe)]
if negara:
    filtered = filtered[filtered["country_main"].isin(negara)]

# ---------- Judul ----------
st.title("🎬 Dashboard Konten Netflix")
st.caption(
    f"Menampilkan {len(filtered):,} dari {len(df):,} judul".replace(",", ".")
    + " | Sumber: Kaggle - Netflix Movies and TV Shows"
)

# Jika filter menghasilkan data kosong, hentikan agar tidak error
if filtered.empty:
    st.warning("Tidak ada data untuk kombinasi filter ini. Coba ubah filter.")
    st.stop()

# ---------- KPI Cards ----------
total_judul = len(filtered)
persen_film = (filtered["type"] == "Movie").mean() * 100
rata_durasi = filtered["duration_min"].mean()
jumlah_negara = filtered.loc[filtered["country_main"] != "Unknown", "country_main"].nunique()

k1, k2, k3, k4 = st.columns(4)
k1.metric("Total Judul", f"{total_judul:,}".replace(",", "."))
k2.metric("Persentase Film", f"{persen_film:.1f}%")
k3.metric(
    "Rata-rata Durasi Film",
    "-" if pd.isna(rata_durasi) else f"{rata_durasi:.0f} menit",
)
k4.metric("Jumlah Negara", jumlah_negara)

st.divider()

# ---------- Area chart (akan diisi di langkah 5B dan 5C) ----------
# ---------- Baris 1: Tren (line) + Proporsi (donut) ----------
kolom_kiri, kolom_kanan = st.columns([2, 1])

with kolom_kiri:
    st.subheader("Tren Judul Ditambahkan per Tahun")
    tren = filtered.groupby(["year_added", "type"]).size().reset_index(name="jumlah")
    fig_tren = px.line(
        tren,
        x="year_added",
        y="jumlah",
        color="type",
        markers=True,
        color_discrete_map=WARNA,
        labels={"year_added": "Tahun ditambahkan", "jumlah": "Jumlah judul", "type": "Tipe"},
    )
    fig_tren.update_layout(xaxis=dict(dtick=1), legend_title_text="")
    st.plotly_chart(fig_tren, width="stretch")

with kolom_kanan:
    st.subheader("Proporsi Film vs Serial")
    proporsi = filtered["type"].value_counts().reset_index()
    proporsi.columns = ["type", "jumlah"]
    fig_donut = px.pie(
        proporsi,
        names="type",
        values="jumlah",
        hole=0.55,
        color="type",
        color_discrete_map=WARNA,
    )
    fig_donut.update_layout(legend_title_text="")
    st.plotly_chart(fig_donut, width="stretch")

# ---------- Baris 2: Top 10 negara (bar horizontal) ----------
st.subheader("10 Negara dengan Konten Terbanyak")
top_negara = (
    filtered[filtered["country_main"] != "Unknown"]
    .groupby(["country_main", "type"])
    .size()
    .reset_index(name="jumlah")
)
urutan = (
    top_negara.groupby("country_main")["jumlah"].sum().nlargest(10).index
)
top_negara = top_negara[top_negara["country_main"].isin(urutan)]
fig_negara = px.bar(
    top_negara,
    x="jumlah",
    y="country_main",
    color="type",
    orientation="h",
    color_discrete_map=WARNA,
    labels={"jumlah": "Jumlah judul", "country_main": "Negara", "type": "Tipe"},
)
fig_negara.update_yaxes(categoryorder="total ascending")
fig_negara.update_layout(legend_title_text="")
st.plotly_chart(fig_negara, width="stretch")

# ---------- Area chart 4 dan 5 + insight (akan diisi di langkah 5C) ----------
# ---------- Baris 3: Heatmap + Histogram ----------
NAMA_BULAN = ["Jan", "Feb", "Mar", "Apr", "Mei", "Jun",
              "Jul", "Agu", "Sep", "Okt", "Nov", "Des"]

kiri, kanan = st.columns(2)

with kiri:
    st.subheader("Kapan Netflix Paling Aktif Menambah Judul?")
    pivot = (
        filtered.groupby(["year_added", "month_added"])
        .size()
        .unstack(fill_value=0)
        .reindex(columns=range(1, 13), fill_value=0)
    )
    fig_heat = px.imshow(
        pivot,
        x=NAMA_BULAN,
        y=[str(t) for t in pivot.index],
        color_continuous_scale=["#1a1a1a", "#E50914"],
        labels=dict(x="Bulan", y="Tahun", color="Jumlah judul"),
        aspect="auto",
    )
    fig_heat.update_yaxes(type="category")
    st.plotly_chart(fig_heat, width="stretch")

with kanan:
    st.subheader("Distribusi Durasi Film")
    film = filtered[filtered["type"] == "Movie"]
    if film.empty:
        st.info("Tidak ada film pada filter ini, jadi histogram durasi tidak ditampilkan.")
    else:
        fig_hist = px.histogram(
            film,
            x="duration_min",
            nbins=30,
            color_discrete_sequence=["#E50914"],
            labels={"duration_min": "Durasi (menit)"},
        )
        fig_hist.update_layout(yaxis_title="Jumlah film", bargap=0.05)
        st.plotly_chart(fig_hist, width="stretch")

# ---------- Kotak Insight (berubah mengikuti filter) ----------
st.divider()
st.subheader("💡 Insight Utama")

per_tahun = filtered.groupby("year_added").size()
tahun_puncak = int(per_tahun.idxmax())
jumlah_puncak = int(per_tahun.max())

per_bulan = filtered.groupby("month_added").size()
bulan_puncak = NAMA_BULAN[int(per_bulan.idxmax()) - 1]

negara_valid = filtered.loc[filtered["country_main"] != "Unknown", "country_main"]

def fmt(n):
    return f"{n:,}".replace(",", ".")


poin = [
    f"**Puncak penambahan konten** terjadi pada tahun **{tahun_puncak}**, "
    f"dengan **{fmt(jumlah_puncak)}** judul.",
    f"**Bulan tersibuk** untuk penambahan judul adalah **{bulan_puncak}**.",
]

if not negara_valid.empty:
    negara_top = negara_valid.value_counts().idxmax()
    jumlah_top = int(negara_valid.value_counts().max())
    poin.append(
        f"**{negara_top}** menjadi negara asal konten terbanyak "
        f"({fmt(jumlah_top)} judul)."
    )

if not film.empty:
    poin.append(
        f"**Durasi film** paling umum berada di sekitar **{film['duration_min'].median():.0f} menit** "
        f"(nilai tengah dari {fmt(len(film))} film)."
    )
    
for p in poin:
    st.markdown(f"- {p}")

st.caption(
    "Catatan data: data tahun 2021 belum mencakup satu tahun penuh, sehingga "
    "penurunan di akhir grafik tren tidak berarti Netflix berhenti menambah konten. "
    "Judul tanpa informasi negara tidak dihitung pada KPI dan grafik negara."
)
