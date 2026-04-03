import streamlit as st
import cv2
import numpy as np
from PIL import Image
import io

# --- KONFIGURASI HALAMAN ---
st.set_page_config(page_title="Shoe-Edu: Footwear Learning Hub", layout="wide")

# --- CUSTOM CSS (Tema Dark & Purple) ---
st.markdown("""
    <style>
    .stApp { background-color: #0c0c0c; color: white; }
    h1, h2, h3 { font-family: 'Inter', sans-serif; color: #a855f7 !important; }
    .content-card {
        background-color: #161616;
        border: 1px solid #262626;
        padding: 25px;
        border-radius: 15px;
        margin-bottom: 20px;
    }
    .highlight { color: #a855f7; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# --- HEADER ---
st.title("👟 Shoe-Edu: Teknik Pengembangan Produk")
st.write("Modul Digital Politeknik ATK Yogyakarta - *Belajar Anatomi, Material, & Desain*")
st.write("---")

# --- NAVIGASI SLIDE (TABS) ---
tab1, tab2, tab3, tab4 = st.tabs([
    "🦴 Anatomi Kaki", 
    "🧪 Material Alas Kaki", 
    "📏 Foot Fitting", 
    "🖼️ AI Design Tool"
])

# --- TAB 1: ANATOMI KAKI ---
with tab1:
    st.header("Anatomi Kaki & Biomekanika")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        <div class="content-card">
        <h3>Struktur Kaki</h3>
        Kaki manusia adalah struktur kompleks yang terdiri dari:
        <ul>
            <li><b>26 Tulang</b> (Tarsus, Metatarsus, Phalanges)</li>
            <li><b>Sendi & Otot</b> untuk fleksibilitas</li>
            <li><b>Ligament & Tendon</b> sebagai pengikat dan penggerak</li>
        </ul>
        <br>
        <p><b>Fungsi Utama:</b></p>
        1. <i>Weight Bearing</i> (Menahan beban tubuh)<br>
        2. <i>Propulsion</i> (Pendorong saat melangkah)<br>
        3. <i>Shock Absorbing</i> (Peredam benturan)
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.info("💡 **Tips Desain:** Desainer harus memahami letak sendi agar sepatu tidak menghambat gerakan alami kaki saat menekuk (flexing).")

# --- TAB 2: MATERIAL ---
with tab2:
    st.header("Klasifikasi Material")
    m1, m2, m3 = st.columns(3)
    
    with m1:
        st.subheader("Upper")
        st.write("- Kulit Sapi/Kambing (Genuine Leather)")
        st.write("- Kulit Sintetis (PU/PVC)")
        st.write("- Tekstil (Canvas, Mesh, Flyknit)")
        
    with m2:
        st.subheader("Midsole")
        st.write("- **EVA:** Ringan & murah")
        st.write("- **Phylon:** Lebih empuk & awet")
        st.write("- **PU:** Stabil tapi bisa hidrolisis")
        
    with m3:
        st.subheader("Outsole")
        st.write("- **Rubber:** Anti-selip & kuat")
        st.write("- **TPR:** Ringan & fleksibel")
        st.write("- **PVC:** Tahan lama tapi kaku")

# --- TAB 3: FOOT FITTING ---
with tab3:
    st.header("Prinsip Kesesuaian (Fitting)")
    st.warning("Desain yang buruk dapat menyebabkan kelainan kaki seperti Flat Foot atau Hallux Valgus.")
    
    st.markdown("""
    <div class="content-card">
    <h4>Standard Allowance (Ruang Tambahan)</h4>
    Untuk kenyamanan, panjang sepatu harus menyisakan ruang dari ujung jari kaki:
    <br><br>
    <ul>
        <li><b>Dewasa:</b> Minimal 5/8 inch (± 1.5 cm)</li>
        <li><b>Anak-anak:</b> Membutuhkan ruang tumbuh yang lebih fleksibel</li>
    </ul>
    </div>
    """, unsafe_allow_html=True)

# --- TAB 4: AI DESIGN TOOL ---
with tab4:
    st.header("AI Vision Assistant")
    st.write("Gunakan fitur ini untuk memperjelas sketsa desain sepatu Anda.")
    
    up_file = st.file_uploader("Upload Sketsa Desain", type=['jpg', 'png'])
    if up_file:
        img = Image.open(up_file)
        img_np = np.array(img)
        
        # Sesuai logika coding sebelumnya
        low = st.sidebar.slider("Detail Level (Low)", 0, 255, 100)
        high = st.sidebar.slider("Detail Level (High)", 0, 255, 200)
        
        gray = cv2.cvtColor(img_np, cv2.COLOR_RGB2GRAY)
        edges = cv2.Canny(gray, low, high)
        
        c1, c2 = st.columns(2)
        c1.image(img, caption="Original Sketch")
        c2.image(edges, caption="AI Edge Detection", clamp=True)
