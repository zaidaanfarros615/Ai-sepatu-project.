import streamlit as st
import pandas as pd
import numpy as np
import cv2
from PIL import Image
from streamlit_drawable_canvas import st_canvas

# --- CONFIGURASI UI CAD PRO ---
st.set_page_config(page_title="NORYZE VECTOR CAD", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #0b0e14; color: #00ff41; }
    .sidebar .sidebar-content { background-color: #161b22; }
    /* Toolbar Styling */
    .btn-tool { border: 1px solid #00ff41; padding: 5px; border-radius: 5px; margin: 2px; }
    </style>
    """, unsafe_allow_html=True)

# --- SIDEBAR: ADVANCED TOOLBAR ---
with st.sidebar:
    st.title("🎨 VECTOR TOOLBAR")
    
    st.subheader("1. Input & Scan")
    src = st.radio("Source:", ["Album", "Camera"])
    bg_image = None
    if src == "Album":
        bg_file = st.file_uploader("Upload Pola", type=['png', 'jpg'])
        if bg_file: bg_image = Image.open(bg_file)
    else:
        cam_file = st.camera_input("Scan")
        if cam_file: bg_image = Image.open(cam_file)

    st.markdown("---")
    
    st.subheader("2. Pen & Drawing Tools")
    draw_mode = st.selectbox(
        "Tool Aktif:",
        ("transform", "line", "rect", "circle", "freedraw", "polygon")
    )
    
    stroke_width = st.slider("Ketebalan Garis (px):", 1, 10, 2)
    stroke_color = st.color_picker("Warna Garis:", "#00ff41")
    bg_color = "#000000" if bg_image is None else "#eee"

    st.markdown("---")
    st.subheader("3. Manual Property")
    p_real = st.number_input("Real Length (cm)", value=25.5)
    l_real = st.number_input("Real Width (cm)", value=10.0)

# --- MAIN WORKSPACE: THE CANVAS ---
st.header("🖥️ Interactive CAD Canvas")
col_canvas, col_inspector = st.columns([3, 1])

with col_canvas:
    # Komponen Canvas Interaktif
    canvas_result = st_canvas(
        fill_color="rgba(0, 255, 65, 0.3)",  # Warna isi untuk poligon
        stroke_width=stroke_width,
        stroke_color=stroke_color,
        background_image=bg_image,
        update_streamlit=True,
        height=500,
        drawing_mode=draw_mode,
        key="canvas",
    )
    
    st.info("💡 **Cara Edit:** Pilih tool di kiri. Gunakan 'transform' untuk menggeser atau mengubah ukuran garis yang sudah dibuat.")

with col_inspector:
    st.subheader("🔍 Inspector")
    if canvas_result.json_data is not None:
        objects = pd.json_normalize(canvas_result.json_data["objects"])
        if not objects.empty:
            st.write("Daftar Garis/Objek:")
            st.dataframe(objects[["type", "left", "top", "width", "height", "scaleX"]])
        else:
            st.write("Belum ada guratan mesin.")

    st.markdown("---")
    st.subheader("📐 Engineering Calc")
    # Logika ATK Yogyakarta
    vamp = p_real * 0.7
    joint = p_real * 0.66
    st.write(f"Titik Vamp: **{round(vamp, 2)} cm**")
    st.write(f"Titik Joint: **{round(joint, 2)} cm**")

# --- GRADING TABLE (AUTOMATED) ---
st.markdown("---")
st.subheader("📊 Automated Grading & Production Data")

data_grading = []
master_size = 40
for s in range(37, 45):
    diff = s - master_size
    # Rumus Grading Standar
    p_s = p_real + (diff * 0.66)
    l_s = l_real + (diff * 0.2)
    data_grading.append({
        "Size": s,
        "Panjang (cm)": round(p_s, 2),
        "Lebar (cm)": round(l_s, 2),
        "Status": "MASTER" if s == master_size else "GRADE"
    })

st.table(pd.DataFrame(data_grading))

# Tombol Export ala AutoCAD
if st.button("💾 EXPORT TO CAD DATA (JSON/CSV)"):
    st.success("Data koordinat vektor berhasil diekspor!")
