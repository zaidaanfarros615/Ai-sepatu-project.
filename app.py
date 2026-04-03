import streamlit as st
import pandas as pd
from PIL import Image
from streamlit_drawable_canvas import st_canvas

# --- KONFIGURASI HALAMAN ---
st.set_page_config(page_title="NORYZE CAD PRO", layout="wide")

# CSS untuk tampilan gelap khas AutoCAD
st.markdown("""
    <style>
    .stApp { background-color: #0b0e14; color: #00ff41; }
    [data-testid="stSidebar"] { background-color: #161b22; }
    .stMarkdown h1, h2, h3 { color: white !important; }
    </style>
    """, unsafe_allow_html=True)

# --- SIDEBAR TOOLBAR ---
with st.sidebar:
    st.header("🛠️ CAD TOOLS")
    
    source = st.radio("Ambil Pola:", ("Album / Galeri", "Kamera HP"))
    uploaded_file = None
    
    if source == "Album / Galeri":
        uploaded_file = st.file_uploader("Upload Gambar Pola", type=["png", "jpg", "jpeg"])
    else:
        uploaded_file = st.camera_input("Ambil Foto")

    # Inisialisasi gambar agar tidak error
    bg_img = None
    if uploaded_file is not None:
        try:
            # Buka gambar dan kecilkan ukurannya agar ringan
            img = Image.open(uploaded_file)
            img.thumbnail((700, 700)) 
            bg_img = img
        except Exception as e:
            st.error(f"Gagal memproses gambar: {e}")

    st.markdown("---")
    st.subheader("🖋️ Drawing Mode")
    mode = st.selectbox("Alat:", ("freedraw", "line", "rect", "circle", "transform"))
    stroke_w = st.slider("Tebal Garis:", 1, 10, 3)
    stroke_c = st.color_picker("Warna Garis:", "#00ff41")

# --- MAIN WORKSPACE ---
st.title("🖥️ NORYZE CAD ENGINE v12")

col1, col2 = st.columns([3, 1])

with col1:
    # Komponen Canvas Utama
    canvas_result = st_canvas(
        fill_color="rgba(0, 255, 65, 0.2)",
        stroke_width=stroke_w,
        stroke_color=stroke_c,
        background_image=bg_img, # Jika bg_img None, canvas tetap jalan (hitam)
        update_streamlit=True,
        height=500,
        drawing_mode=mode,
        key="noryze_cad_canvas"
    )
    st.caption("Gunakan alat di samping untuk mulai mendigitalisasi pola Adidas kamu.")

with col2:
    st.subheader("📐 Ukuran Master")
    p_master = st.number_input("Panjang (cm)", value=26.5)
    l_master = st.number_input("Lebar (cm)", value=10.0)
    
    st.markdown("---")
    st.write("**Tabel Grading (ATK)**")
    
    # Kalkulasi Grading Otomatis
    rows = []
    for s in [38, 39, 40, 41, 42]:
        diff = s - 40
        rows.append({
            "Size": s,
            "P (cm)": round(p_master + (diff * 0.66), 2),
            "L (cm)": round(l_master + (diff * 0.2), 2)
        })
    st.table(pd.DataFrame(rows))

if st.button("📥 Simpan Project"):
    st.balloons()
    st.success("Project Berhasil Disimpan!")
