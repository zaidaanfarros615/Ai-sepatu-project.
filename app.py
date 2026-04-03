import streamlit as st
import cv2
import numpy as np
from PIL import Image
import io

# --- 1. KONFIGURASI HALAMAN ---
st.set_page_config(page_title="Footwear Dev Learning", layout="wide")

# --- 2. CUSTOM CSS (Agar Mirip Gambar Referensi) ---
st.markdown("""
    <style>
    /* Background utama */
    .stApp { background-color: #0c0c0c; color: white; }
    
    /* Sidebar styling */
    section[data-testid="stSidebar"] {
        background-color: #111111 !important;
        border-right: 1px solid #262626;
    }
    
    /* Card Material styling */
    .learning-card {
        background-color: #161616;
        border: 1px solid #262626;
        padding: 20px;
        border-radius: 15px;
        transition: 0.3s;
        height: 250px;
    }
    .learning-card:hover {
        border-color: #a855f7;
        background-color: #1a1a1a;
    }
    
    /* Text colors */
    .purple-text { color: #a855f7; font-weight: bold; }
    h1, h2, h3 { color: white !important; }
    
    /* Button styling */
    .stButton>button {
        background: linear-gradient(135deg, #a855f7 0%, #6d28d9 100%);
        color: white; border: none; border-radius: 8px;
        font-weight: 600;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. SIDEBAR NAVIGATION ---
with st.sidebar:
    st.markdown("## 👟 <span class='purple-text'>Shoe</span>Lab", unsafe_allow_html=True)
    st.write("---")
    menu = st.radio(
        "Pilih Modul Pembelajaran:",
        ["🏠 Dashboard", "🦴 Anatomi Kaki", "🧪 Pengetahuan Material", "📐 Teknik Fitting", "🎨 AI Design Tool"]
    )
    st.write("---")
    st.info("Log: Materi berdasarkan Kurikulum Politeknik ATK Yogyakarta.")

# --- 4. KONTEN BERDASARKAN MENU ---

if menu == "🏠 Dashboard":
    # Header Section
    st.markdown('<h1>Welcome to <span class="purple-text">Footwear Learning</span> Hub</h1>', unsafe_allow_html=True)
    st.write("Eksplorasi teknik pengembangan produk alas kaki secara digital dan interaktif.")
    
    # Grid Layout (Mirip Dashboard Gambar Referensi)
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f"""
            <div class="learning-card">
                <h3 class="purple-text">01</h3>
                <h4>Anatomi Kaki</h4>
                <p style="color: #888; font-size: 14px;">Mempelajari 26 tulang manusia dan cara kerja biomekanika saat berjalan.</p>
            </div>
        """, unsafe_allow_html=True)
        if st.button("Buka Anatomi"):
            st.info("Pindah ke tab Anatomi di Sidebar")

    with col2:
        st.markdown(f"""
            <div class="learning-card">
                <h3 class="purple-text">02</h3>
                <h4>Material Kulit</h4>
                <p style="color: #888; font-size: 14px;">Memahami perbedaan Leather, Sintetik, dan Outsole Rubber/EVA.</p>
            </div>
        """, unsafe_allow_html=True)
        st.button("Cek Material")

    with col3:
        st.markdown(f"""
            <div class="learning-card">
                <h3 class="purple-text">03</h3>
                <h4>AI Edge Detection</h4>
                <p style="color: #888; font-size: 14px;">Gunakan teknologi Vision untuk memperjelas pola desain sepatu Anda.</p>
            </div>
        """, unsafe_allow_html=True)
        st.button("Coba AI")

elif menu == "🦴 Anatomi Kaki":
    st.header("Anatomi Kaki (Foot Anatomy)")
    st.markdown("""
    - **Tarsal & Metatarsal**: Struktur utama penyangga berat badan.
    - **Arch (Lengkungan)**: Berfungsi sebagai pegas alami tubuh.
    """)
    st.image("https://via.placeholder.com/800x400.png?text=Diagram+Anatomi+Kaki", use_column_width=True)

elif menu == "🎨 AI Design Tool":
    st.header("AI <span class='purple-text'>Vision</span> Sketch Assistant", unsafe_allow_html=True)
    uploaded_file = st.file_uploader("Upload sketsa desain sepatu Anda", type=['jpg', 'jpeg', 'png'])
    
    if uploaded_file:
        img = Image.open(uploaded_file)
        img_array = np.array(img)
        
        # Slider UI
        low = st.slider("Sensitivity Low", 0, 255, 100)
        high = st.slider("Sensitivity High", 0, 255, 200)
        
        # Processing
        gray = cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY)
        edges = cv2.Canny(gray, low, high)
        
        c1, c2 = st.columns(2)
        c1.image(img, caption="Sketsa Asli")
        c2.image(edges, caption="Hasil AI Edge Detection", clamp=True)
