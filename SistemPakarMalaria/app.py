import streamlit as st
import pandas as pd
import datetime

# ================= SETTING ==================
st.set_page_config(
    page_title="Sistem Pakar Malaria",
    page_icon="🦟",
    layout="wide"
)

# ================= SESSION STATE ==================
if "riwayat" not in st.session_state:
    st.session_state.riwayat = []

# ================= SIDEBAR ==================
with st.sidebar:
    st.image("assets/logo.png", width=150)
    st.title("🦟 Sistem Pakar")

    menu = st.selectbox(
        "Menu",
        ["🏠 Dashboard", "🩺 Diagnosa", "📊 Grafik", "📄 Riwayat", "ℹ️ Tentang"]
    )

# ================= DASHBOARD ==================
if menu == "🏠 Dashboard":
    st.title("🦟 Sistem Pakar Diagnosis Malaria")
    st.success("Selamat Datang 👋")
    st.write("""
Aplikasi ini digunakan untuk membantu mendiagnosis kemungkinan penyakit malaria
berdasarkan gejala pasien.
""")

# ================= DIAGNOSA ==================
elif menu == "🩺 Diagnosa":
    st.title("🩺 Form Diagnosa Malaria")

    nama = st.text_input("Nama Pasien")
    umur = st.number_input("Umur", min_value=1, max_value=120)

    st.subheader("Masukkan Gejala")

    demam = st.selectbox("Demam tinggi?", ["Tidak", "Ringan", "Tinggi"])
    menggigil = st.selectbox("Menggigil?", ["Ya", "Tidak"])
    sakit_kepala = st.selectbox("Sakit kepala?", ["Ya", "Tidak"])
    mual = st.selectbox("Mual/Muntah?", ["Ya", "Tidak"])
    lemas = st.selectbox("Lemas?", ["Ya", "Tidak"])
    berkeringat = st.selectbox("Berkeringat dingin?", ["Ya", "Tidak"])

    if st.button("🔍 Diagnosa Sekarang"):

        skor = 0

        if demam == "Tinggi":
            skor += 3
        elif demam == "Ringan":
            skor += 1

        if menggigil == "Ya":
            skor += 2
        if sakit_kepala == "Ya":
            skor += 1
        if mual == "Ya":
            skor += 1
        if lemas == "Ya":
            skor += 1
        if berkeringat == "Ya":
            skor += 2

        if skor >= 7:
            hasil = "⚠️ POSITIF MALARIA (TINGGI)"
        elif skor >= 4:
            hasil = "⚠️ KEMUNGKINAN MALARIA (SEDANG)"
        else:
            hasil = "✅ TIDAK TERINDIKASI MALARIA"

        data = {
            "Waktu": datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
            "Nama": nama,
            "Umur": umur,
            "Skor": skor,
            "Hasil": hasil
        }

        st.session_state.riwayat.append(data)

        st.success("Hasil Diagnosa")
        st.info(hasil)
        st.write("Skor:", skor)

# ================= RIWAYAT ==================
elif menu == "📄 Riwayat":
    st.title("📄 Riwayat Diagnosa")

    if len(st.session_state.riwayat) == 0:
        st.warning("Belum ada data diagnosa")
    else:
        df = pd.DataFrame(st.session_state.riwayat)
        st.dataframe(df, use_container_width=True)

        csv = df.to_csv(index=False).encode("utf-8")
        st.download_button(
            "⬇️ Download Data",
            csv,
            "riwayat_malaria.csv",
            "text/csv"
        )

# ================= GRAFIK ==================
elif menu == "📊 Grafik":
    st.title("📊 Grafik Hasil Diagnosa")

    if len(st.session_state.riwayat) == 0:
        st.warning("Belum ada data untuk ditampilkan")
    else:
        df = pd.DataFrame(st.session_state.riwayat)

        grafik = df["Hasil"].value_counts()
        st.bar_chart(grafik)

# ================= TENTANG ==================
elif menu == "ℹ️ Tentang":
    st.title("ℹ️ Tentang Aplikasi")

    st.write("""
Aplikasi Sistem Pakar Malaria ini dibuat untuk membantu:
- Diagnosa awal malaria
- Menyimpan riwayat pasien
- Menampilkan grafik hasil diagnosa

Dibuat menggunakan:
- Python
- Streamlit
""")