import streamlit as st
import cv2
import numpy as np
from PIL import Image
import io

# --- 1. KONFIGURASI HALAMAN ---
st.set_page_config(page_title="Smart Shoe-Dev Hub", layout="wide")

# --- 2. CUSTOM CSS (Smart & Modern) ---
st.markdown("""
    <style>
    .stApp { background-color: #0c0c0c; color: white; }
    section[data-testid="stSidebar"] { background-color: #111111 !important; border-right: 1px solid #262626; }
    .stat-card {
        background: linear-gradient(145deg, #161616, #1e1e1e);
        padding: 20px; border-radius: 15px; border: 1px solid #262626;
        text-align: center; margin-bottom: 15px;
    }
    .purple-text { color: #a855f7; font-weight: bold; }
    .component-box { border-left: 4px solid #a855f7; padding-left: 15px; margin: 10px 0; background: #1a1a1a; padding: 10px; border-radius: 5px; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. SIDEBAR NAVIGATION ---
with st.sidebar:
    st.markdown("## 👟 <span class='purple-text'>Smart</span>Shoe AI", unsafe_allow_html=True)
    st.write("---")
    menu = st.radio("Navigasi Modul:", ["📊 Dashboard", "🦴 Anatomi & Komponen", "📐 Kalkulator Size & Rumus", "🎨 AI Vision Tool (1000 DPI)"])
    st.write("---")
    [span_0](start_span)[span_1](start_span)st.caption("Data Source: Modul Praktik TPP - Politeknik ATK Yogyakarta[span_0](end_span)[span_1](end_span)")

# --- 4. DASHBOARD ---
if menu == "📊 Dashboard":
    st.title("Digital <span class='purple-text'>Learning</span> System", unsafe_allow_html=True)
    c1, c2, c3, c4 = st.columns(4)
    with c1: st.markdown('<div class="stat-card"><h3>26</h3><p>Tulang Kaki</p></div>', unsafe_allow_html=True)
    with c2: st.markdown('<div class="stat-card"><h3>4</h3><p>Kelompok Otot</p></div>', unsafe_allow_html=True)
    with c3: st.markdown('<div class="stat-card"><h3>5</h3><p>Sendi Utama</p></div>', unsafe_allow_html=True)
    with c4: st.markdown('<div class="stat-card"><h3>5/8"</h3><p>Allowance</p></div>', unsafe_allow_html=True)

    st.subheader("Titik Penting Penahan Berat (Weight Bearing)")
    [span_2](start_span)st.write("Menurut dokumen ATK, terdapat **3 titik utama** penahan berat pada telapak kaki untuk stabilitas berjalan[span_2](end_span):")
    [span_3](start_span)st.markdown("- **Tumit (Os-calcis)**\n- **Kepala Metatarsal (Ujung Depan)**\n- **Outer Longitudinal Arch**[span_3](end_span)")

# --- 5. ANATOMI & KOMPONEN ---
elif menu == "🦴 Anatomi & Komponen":
    st.title("Anatomi & Komponen <span class='purple-text'>Alas Kaki</span>", unsafe_allow_html=True)
    
    col_a, col_b = st.columns(2)
    with col_a:
        st.subheader("Nama Komponen Penting")
        komponen = {
            [span_4](start_span)"Upper": "Bagian atas pelindung kaki[span_4](end_span).",
            [span_5](start_span)"Insole": "Alas pijakan kaki di dalam sepatu untuk kenyamanan[span_5](end_span).",
            [span_6](start_span)"Midsole": "Peredam kejut (shock absorbing) di antara insole & outsole[span_6](end_span).",
            [span_7](start_span)"Outsole": "Bagian bawah yang kontak langsung dengan tanah[span_7](end_span).",
            [span_8](start_span)"Lining": "Lapisan dalam sepatu[span_8](end_span).",
            [span_9](start_span)[span_10](start_span)"Toe Box": "Ruang untuk jari-jari kaki[span_9](end_span)[span_10](end_span)."
        }
        for k, v in komponen.items():
            st.markdown(f"<div class='component-box'><b>{k}</b>: {v}</div>", unsafe_allow_html=True)

    with col_b:
        st.subheader("Fungsi Mekanis Kaki")
        [span_11](start_span)st.info("**Propulsion**: Kaki sebagai pendorong maju[span_11](end_span).")
        [span_12](start_span)st.info("**Shock Absorbing**: Peredam tumbukan antar tulang[span_12](end_span).")
        [span_13](start_span)st.info("**Weight Bearing**: Penahan berat tubuh[span_13](end_span).")

# --- 6. KALKULATOR SIZE & RUMUS ---
elif menu == "📐 Kalkulator Size & Rumus":
    st.title("Smart <span class='purple-text'>Fitting</span> Calculator", unsafe_allow_html=True)
    
    st.write("### Rumus Allowance (Kelonggaran)")
    st.latex(r"Ukuran\ Sepatu = Panjang\ Kaki + Allowance")
    
    panjang_kaki = st.number_input("Masukkan Panjang Kaki (mm):", min_value=100, max_value=400, value=250)
    
    # [span_14](start_span)[span_15](start_span)Logika Allowance berdasarkan file[span_14](end_span)[span_15](end_span)
    allowance_inch = 5/8 # 0.625 inch
    allowance_mm = allowance_inch * 25.4 # Konversi ke mm
    
    total_length = panjang_kaki + allowance_mm
    
    st.success(f"Rekomendasi Panjang Dalam Sepatu: **{total_length:.2f} mm**")
    [span_16](start_span)st.write(f"*Berdasarkan standar Politeknik ATK, ruang depan minimal **5/8 inch** (±15.8mm) untuk dewasa agar jari bergerak bebas[span_16](end_span).*")

# --- 7. AI VISION TOOL (SKALA 1000) ---
elif menu == "🎨 AI Vision Tool (1000 DPI)":
    st.title("AI <span class='purple-text'>Edge</span> Scaler 1000", unsafe_allow_html=True)
    st.write("Gunakan skala sensitivitas hingga 1000 untuk deteksi garis super halus.")
    
    up = st.file_uploader("Upload Sketch Sepatu", type=['jpg', 'png'])
    if up:
        img = Image.open(up)
        # Slider dengan angka sampai 1000
        sens = st.slider("Level Sensitivitas AI (0 - 1000)", 0, 1000, 300)
        
        # Konversi slider ke skala OpenCV (0-255)
        cv_sens = int((sens / 1000) * 255)
        
        img_np = np.array(img)
        gray = cv2.cvtColor(img_np, cv2.COLOR_RGB2GRAY)
        edges = cv2.Canny(gray, cv_sens, cv_sens * 2)
        
        c1, c2 = st.columns(2)
        c1.image(img, caption="Original")
        c2.image(edges, caption=f"AI Result (Sens: {sens})", clamp=True)
