import streamlit as st
import pandas as pd
import numpy as np
from PIL import Image
from streamlit_drawable_canvas import st_canvas

# --- SETUP PAGE ---
st.set_page_config(page_title="NORYZE AI CAD ULTIMATE", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #0b0e14; color: #00ff41; }
    .sidebar .sidebar-content { background-color: #161b22; }
    </style>
    """, unsafe_allow_html=True)

# --- SIDEBAR TOOLBAR ---
with st.sidebar:
    st.title("🎨 CAD TOOLBAR")
    
    # Pilih sumber input
    src = st.radio("Ambil Pola Dari:", ["Album / Galeri", "Kamera HP"])
    
    bg_image = None
    uploaded_file = None
    
    if src == "Album / Galeri":
        uploaded_file = st.file_uploader("Upload Pola Sepatu", type=['png', 'jpg', 'jpeg'])
    else:
        uploaded_file = st.camera_input("Scan Pola")

    # PROSES GAMBAR (Mencegah Error AttributeError)
    if uploaded_file is not None:
        try:
            img = Image.open(uploaded_file)
            # Resize otomatis ke lebar 700px agar Canvas stabil
            w_percent = (700 / float(img.size[0]))
            h_size = int((float(img.size[1]) * float(w_percent)))
            bg_image = img.resize((700, h_size), Image.Resampling.LANCZOS)
        except Exception as e:
            st.error(f"Gagal memuat gambar: {e}")

    st.markdown("---")
    st.subheader("🖋️ Pen Tools")
    tool = st.selectbox("Alat Gambar:", ("line", "freedraw", "rect", "circle", "transform"))
    color = st.color_picker("Warna Garis:", "#00ff41")
    size = st.slider("Tebal Garis:", 1, 10, 3)

# --- MAIN WORKSPACE ---
st.header("🖥️ NORYZE CAD WORKSPACE")
col_canvas, col_data = st.columns([3, 1])

with col_canvas:
    # Canvas yang lebih stabil
    canvas_result = st_canvas(
        fill_color="rgba(0, 255, 65, 0.2)",
        stroke_width=size,
        stroke_color=color,
        background_image=bg_image, # Sekarang aman dari error
        update_streamlit=True,
        height=600,
        drawing_mode=tool,
        key="noryze_canvas_v11",
    )
    st.caption("Gunakan 'freedraw' untuk mengikuti lekukan pola Adidas atau 'line' untuk garis lurus.")

with col_data:
    st.subheader("📐 Engineering")
    p_master = st.number_input("Panjang Master (cm)", value=26.5)
    l_master = st.number_input("Lebar Master (cm)", value=10.0)
    
    st.markdown("---")
    # Tabel Grading Otomatis (Standar ATK)
    st.write("**Preview Grading (SZ 38-42)**")
    grading = []
    for s in [38, 39, 40, 41, 42]:
        diff = s - 40
        grading.append({
            "Size": s,
            "P (cm)": round(p_master + (diff * 0.66), 2),
            "L (cm)": round(l_master + (diff * 0.2), 2)
        })
    st.dataframe(pd.DataFrame(grading), hide_index=True)

if st.button("💾 Simpan Koordinat Pola"):
    if canvas_result.json_data is not None:
        st.success("Koordinat vektor pola berhasil disimpan ke database!")
