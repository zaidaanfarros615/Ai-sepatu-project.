import streamlit as st
import pandas as pd

# Konfigurasi Halaman Professional
st.set_page_config(page_title="NORYZE AI - Footwear Engineering", layout="wide")

# --- STYLE CSS (Agar Tampilan Mewah) ---
st.markdown("""
    <style>
    .reportview-container { background: #f0f2f6; }
    .stButton>button { width: 100%; border-radius: 10px; background-color: #007BFF; color: white; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

st.title("👟 NORYZE PRO v4.0")
st.subheader("Sistem Pengembangan Produk & Grading (Standar ATK Yogyakarta)")
st.markdown("---")

# --- SIDEBAR: INPUT TEKNIS ---
with st.sidebar:
    st.header("📋 Data Antropometri")
    kategori = st.selectbox("Target Pengguna", ["Pria Dewasa", "Wanita Dewasa", "Anak-anak"])
    
    # Standar Allowance (Ruang Gerak) dari Dokumen Hal 27
    allowance = 1.58 if "Dewasa" in kategori else 2.54 
    
    st.info(f"Standar Ruang Jari ({kategori}): {allowance} cm")
    
    p_kaki = st.number_input("Panjang Kaki Asli (cm)", value=25.0, help="Ukur dari tumit ke ujung jari terpanjang")
    l_kaki = st.number_input("Lebar Kaki Asli (cm)", value=9.5)
    size_master = st.number_input("Nomor Master (EUR)", value=40)

# --- LOGIKA MIX (GRADING + BIOMEKANIKA) ---
def proses_produk(p_kaki, l_kaki, allowance, s_master):
    # Rumus Pola Nyaman: Panjang Kaki + Ruang Gerak (Fitting)
    p_pola_master = p_kaki + allowance
    
    hasil = []
    # Membuat rentang 5 ukuran ke bawah dan 5 ke atas
    for s in range(int(s_master)-5, int(s_master)+6):
        selisih = s - s_master
        # Pitch standar internasional: 0.66 cm per nomor
        p_baru = p_pola_master + (selisih * 0.66)
        # Pitch lebar standar: 0.2 cm
        l_baru = l_kaki + (selisih * 0.2)
        
        # Estimasi Luas Bahan (Upper) - Logika Industri
        luas_bahan = (p_baru * l_baru * 2.5) 
        
        hasil.append({
            "Nomor (Size)": s,
            "Pola Panjang (cm)": round(p_baru, 2),
            "Pola Lebar (cm)": round(l_baru, 2),
            "Est. Bahan (cm²)": round(luas_bahan, 1),
            "Tipe": "⭐⭐ MASTER" if s == s_master else "Hasil Grading"
        })
    return pd.DataFrame(hasil)

# --- HALAMAN UTAMA ---
if st.button("🚀 MULAI ANALISIS TEKNIS"):
    df = proses_produk(p_kaki, l_kaki, allowance, size_master)
    
    # Dashboard Singkat
    c1, c2, c3 = st.columns(3)
    c1.metric("Panjang Pola Master", f"{p_kaki + allowance} cm")
    c2.metric("Rasio Beban (U:Q)", "3:1 (Tumit:Bal)")
    c3.metric("Status", "Standar Industri")

    # Tabel Data
    st.subheader("📊 Tabel Hasil Analisis Ukuran & Material")
    st.dataframe(df.style.highlight_max(subset=['Pola Panjang (cm)'], color='#ff4b4b'), use_container_width=True)

    # Visualisasi Sederhana (Dokumen Hal 30)
    st.markdown("---")
    st.subheader("🧪 Rekomendasi Teknis Produksi")
    
    col_a, col_b = st.columns(2)
    with col_a:
        st.success("**Pemilihan Material Outsole:**")
        st.write("- Gunakan Karet (Rubber) dengan kekerasan 55-65 Shore A.")
        st.write("- Area tumit harus lebih tebal (Beban 75% ada di tumit).")
    with col_b:
        st.warning("**Instruksi Cutting:**")
        st.write(f"- Pastikan ada toleransi potong 2-3mm.")
        st.write(f"- Luas bahan per pasang (Size {size_master}): {df[df['Nomor (Size)'] == size_master]['Est. Bahan (cm²)'].values[0]} cm²")

    # Download
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button("📥 Download Laporan Produksi (CSV)", csv, "laporan_noryze.csv", "text/csv")

st.markdown("---")
st.caption("NORYZE PRO v4.0 | Integrated with Politeknik ATK Standards")
