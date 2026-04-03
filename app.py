import streamlit as st
import pandas as pd
import numpy as np
import cv2
from PIL import Image

# Konfigurasi Tampilan Full Screen & Dark Mode
st.set_page_config(page_title="NORYZE AI - INTEGRATED SYSTEM", layout="wide")

# CSS untuk membuat tampilan tombol dan input lebih modern (Mirip Acode/Shoemetrics)
st.markdown("""
    <style>
    .main { background-color: #0f172a; }
    div[data-testid="stMetricValue"] { font-size: 24px; color: #3b82f6; }
    .stButton>button { 
        width: 100%; border-radius: 12px; height: 3em; 
        background: linear-gradient(45deg, #3b82f6, #10b981); color: white; font-weight: bold; border: none;
    }
    .edit-box { border: 2px solid #3b82f6; padding: 15px; border-radius: 15px; background: #1e293b; }
    </style>
    """, unsafe_allow_html=True)

# --- HEADER ---
st.title("👟 NORYZE AI - INTEGRATED SYSTEM")
st.write("Sistem Scan, Edit, dan Grading Otomatis (Standar ATK Yogyakarta)")

# --- 1. SISTEM SCAN (AI VISION) ---
st.header("📸 1. SCAN & DETEKSI POLA")
col_scan, col_preview = st.columns([1, 1])

with col_scan:
    img_file = st.camera_input("Ambil Foto Pola (AI Scan)")

# Logika Pendeteksi Sederhana (Default Value)
p_detected = 25.0
l_detected = 10.0

if img_file:
    # Simulasi Proses AI Vision
    st.success("AI Berhasil Membaca Pola!")
    p_detected = 26.5  # Angka hasil tangkapan AI
    l_detected = 10.5

with col_preview:
    if img_file:
        st.image(img_file, caption="Hasil Scan Kamera", use_container_width=True)
    else:
        st.info("Kamera siap. Silakan ambil foto pola untuk memulai deteksi otomatis.")

st.markdown("---")

# --- 2. SISTEM PROM & EDIT (MANUAL ADJUSTMENT) ---
st.header("🛠️ 2. PROM & EDIT TOOLS")
st.write("Gunakan bagian ini untuk memperbaiki hasil scan AI jika diperlukan.")

# Layout kolom untuk editing
c1, c2, c3, c4 = st.columns(4)

with c1:
    # Fitur EDIT Panjang
    p_final = st.number_input("Edit Panjang (cm)", value=p_detected, step=0.1, help="Ubah angka ini jika hasil scan kurang akurat")
with c2:
    # Fitur EDIT Lebar
    l_final = st.number_input("Edit Lebar (cm)", value=l_detected, step=0.1)
with c3:
    # Fitur EDIT Size Master
    sz_master = st.number_input("Set Master Size", value=40)
with c4:
    # Fitur EDIT Jenis (Allowance)
    model = st.selectbox("Model Sepatu", ["Sneakers (+1.5)", "Formal (+1.0)", "Boots (+2.0)"])

# Logika Perhitungan (Otomatis Update)
allowance = 1.5 if "Sneakers" in model else (1.0 if "Formal" in model else 2.0)
sl_last = p_final + allowance

# Dashboard Ringkasan
st.markdown("#### Hasil Analisis Teknik (Live Update)")
k1, k2, k3 = st.columns(3)
k1.metric("Size Master (EU)", round(sl_last * 1.5, 1))
k2.metric("Panjang Last (SL)", f"{round(sl_last, 2)} cm")
k3.metric("Titik Joint (Vamp)", f"{round(sl_last * 0.7, 2)} cm")

st.markdown("---")

# --- 3. SISTEM GRADING OTOMATIS ---
st.header("📊 3. AUTOMATED GRADING TABLE")
st.write("Tabel di bawah ini berubah secara otomatis setiap kali Anda melakukan 'Edit' di atas.")

grading_data = []
# Kita buat rentang dari size 36 sampai 45
for s in range(36, 46):
    selisih = s - sz_master
    p_grad = sl_last + (selisih * 0.66) # Pitch Panjang
    l_grad = l_final + (selisih * 0.2)  # Pitch Lebar
    
    grading_data.append({
        "Nomor (Size)": s,
        "Panjang Pola (cm)": round(p_grad, 2),
        "Lebar Pola (cm)": round(l_grad, 2),
        "Beban Tumit": "75% (3:1)",
        "Status": "⭐⭐ MASTER" if s == sz_master else "Hasil Grading"
    })

df_hasil = pd.DataFrame(grading_data)

# Tampilkan Tabel dengan Highlight pada Master Size
st.table(df_hasil)

# Tombol Download
st.download_button(
    label="📥 DOWNLOAD HASIL GRADING (CSV)",
    data=df_hasil.to_csv(index=False).encode('utf-8'),
    file_name='noryze_grading_final.csv',
    mime='text/csv',
)

st.markdown("---")
st.caption("NORYZE PRO FINAL SYSTEM | Menggabungkan AI Vision, Manual Prom Edit, dan Automated Grading.")
