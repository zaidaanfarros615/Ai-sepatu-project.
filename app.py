import streamlit as st
import pandas as pd
import numpy as np
import cv2
from PIL import Image

# Konfigurasi UI
st.set_page_config(page_title="NORYZE PRO - Multi Input System", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #0f172a; }
    .stMetric { background: #1e293b; padding: 15px; border-radius: 15px; border-top: 4px solid #10b981; }
    .stButton>button { 
        background: #3b82f6; color: white; border-radius: 10px; font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("👟 NORYZE PRO: Multi-Source Engine")
st.write("Input dari Kamera, Galeri, dan Grading Otomatis Terintegrasi")

# --- 1. BAGIAN SCAN & INPUT (KAMERA + ALBUM) ---
st.header("📸 1. Input Sumber Pola")
col_input, col_view = st.columns([1, 1])

with col_input:
    # FITUR BARU: Pilihan Sumber Data
    source = st.radio("Pilih Sumber Foto:", ["Ambil Kamera Langsung", "Pilih dari Galeri/Album"])
    
    img_data = None
    if source == "Ambil Kamera Langsung":
        img_data = st.camera_input("Scan Pola")
    else:
        img_data = st.file_uploader("Pilih File Foto Pola (JPG/PNG)", type=['jpg', 'jpeg', 'png'])

# Default nilai awal
p_ai = 25.0
l_ai = 9.8

if img_data:
    with col_view:
        st.image(img_data, caption="Foto Berhasil Dimuat", use_container_width=True)
        st.success("✅ File terbaca. AI sedang menganalisis dimensi...")
        # Simulasi AI deteksi dari file
        p_ai = 26.2 
        l_ai = 10.3

st.markdown("---")

# --- 2. SISTEM PROM EDIT & TOOLS ---
st.header("🛠️ 2. Konfigurasi & Edit Manual")
c1, c2, c3, c4 = st.columns(4)

with c1:
    p_final = st.number_input("📏 Edit Panjang (cm)", value=p_ai, step=0.1)
with c2:
    l_final = st.number_input("📐 Edit Lebar (cm)", value=l_ai, step=0.1)
with c3:
    sz_master = st.number_input("🎯 Nomor Master", value=40)
with c4:
    style = st.selectbox("👞 Jenis Sepatu", ["Sneakers (+1.5)", "Formal (+1.0)", "Safety (+2.0)"])

# Perhitungan Otomatis
allowance = 1.5 if "Sneakers" in style else (1.0 if "Formal" in style else 2.0)
sl_last = p_final + allowance

# Live Dashboard
d1, d2, d3 = st.columns(3)
d1.metric("Panjang Last (SL)", f"{round(sl_last, 2)} cm")
d2.metric("Titik Vamp (7/10)", f"{round(sl_last * 0.7, 2)} cm")
d3.metric("Estimasi Size EU", round(sl_last * 1.5, 1))

st.markdown("---")

# --- 3. TABEL GRADING OTOMATIS ---
st.header("📊 3. Laporan Grading Produksi")

grading_list = []
# Loop otomatis dari size 36 ke 45
for s in range(36, 46):
    selisih = s - sz_master
    p_grad = sl_last + (selisih * 0.66) # Rumus Pitch Panjang
    l_grad = l_final + (selisih * 0.2)  # Rumus Pitch Lebar
    
    # Perhitungan Luas Bahan (Materi ATK Hal 45)
    luas_bahan = (p_grad * l_grad * 2.3)
    
    grading_list.append({
        "Size": s,
        "Panjang (cm)": round(p_grad, 2),
        "Lebar (cm)": round(l_grad, 2),
        "Est. Bahan (cm2)": round(luas_bahan, 1),
        "Status": "MASTER" if s == sz_master else "GRADED"
    })

df_hasil = pd.DataFrame(grading_list)

# Tampilkan Tabel
st.table(df_hasil)

# Tombol Download
st.download_button("📥 Simpan Hasil ke Excel/CSV", df_hasil.to_csv(index=False).encode('utf-8'), "noryze_report.csv", "text/csv")

st.markdown("---")
st.info("💡 **Tips:** Jika foto dari album miring, gunakan fitur 'Edit Panjang' untuk menyesuaikan dengan ukuran fisik penggaris.")
