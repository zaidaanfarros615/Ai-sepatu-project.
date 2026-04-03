import streamlit as st
import pandas as pd

# Konfigurasi Standar Industri ATK Yogyakarta
st.set_page_config(page_title="NORYZE PRO v3.0 - AI Footwear Engineering", layout="wide")

st.title("👟 NORYZE PRO: Advanced Product Development System")
st.markdown("_Sistem Berbasis Standar Politeknik ATK Yogyakarta_")

# --- SIDEBAR: PARAMETER ANTROPOMETRI ---
with st.sidebar:
    st.header("📐 Parameter Antropometri")
    kategori = st.radio("Kategori Pengguna", ["Dewasa", "Anak-anak"])
    
    # Standar Ruang Gerak (Foot Fitting) [Source: Hal 27-28]
    if kategori == "Dewasa":
        allowance = 1.58  # Standar 5/8 inch untuk jari
    else:
        allowance = 2.54  # Standar up to 1 inch untuk pertumbuhan

    st.subheader("📏 Data Kaki Pasien/User")
    p_kaki = st.number_input("Panjang Kaki Asli (cm)", value=25.0)
    l_kaki = st.number_input("Lebar Kaki Asli (cm)", value=9.5)
    size_master = st.number_input("Ukuran Master (EUR)", value=40)

# --- LOGIKA BIOMEKANIKA & GRADING ---
def analisis_produk(p_kaki, l_kaki, allowance, size_master):
    # Hitung Panjang Pola Minimum agar Nyaman (Foot Fitting)
    p_pola_min = p_kaki + allowance
    
    data = []
    for s in range(size_master - 3, size_master + 4):
        selisih = s - size_master
        # Standar Grading Pitch: 0.66 cm
        p_baru = p_pola_min + (selisih * 0.66)
        l_baru = l_kaki + (selisih * 0.2)
        
        # Analisis Beban Biomekanika (Standar Hal 30-31)
        # Pada posisi berdiri, beban Tumit (U) = 3x Beban Bal Kaki (Q)
        beban_tumit = "75%" # Distribusi 3:1
        beban_depan = "25%"
        
        data.append({
            "Size": s,
            "Pola Panjang (cm)": round(p_baru, 2),
            "Pola Lebar (cm)": round(l_baru, 2),
            "Distribusi Beban (U:Q)": f"{beban_tumit} : {beban_depan}",
            "Catatan": "MASTER" if s == size_master else "GRADED"
        })
    return pd.DataFrame(data)

# --- TAMPILAN UTAMA ---
if st.button("🚀 JALANKAN ANALISIS PENGEMBANGAN PRODUK"):
    df = analisis_produk(p_kaki, l_kaki, allowance, size_master)
    
    # Dashboard Metrik
    col1, col2, col3 = st.columns(3)
    col1.metric("Panjang Pola Master", f"{df.iloc[3]['Pola Panjang (cm)']} cm")
    col2.metric("Allowance (Ruang Jari)", f"{allowance} cm")
    col3.metric("Rasio Beban (U:Q)", "3 : 1")

    st.subheader("📊 Tabel Hasil Grading & Biomekanika")
    st.table(df)

    # --- FITUR VISUALISASI BEBAN ---
    st.markdown("---")
    st.subheader("💡 Rekomendasi Material (Berdasarkan Evaluasi Performa)")
    
    # Logika pemilihan material dari Bab 1 & 2
    st.info(f"""
    **Rekomendasi Teknik untuk {kategori}:**
    * **Insole:** Gunakan **PU Foam** untuk peredam kejut (Shock Absorbing).
    * **Outsole:** Gunakan **Karet (Rubber)** untuk ketahanan abrasi (Martindale Test).
    * **Upper:** Perlu ruang gerak minimal **{allowance} cm** di depan jari agar tidak terjadi cacat 'Mata Ikan'.
    """)

st.caption("NORYZE PRO v3.0 | Berdasarkan Buku Materi Praktik Teknik Pengembangan Produk 2025")
