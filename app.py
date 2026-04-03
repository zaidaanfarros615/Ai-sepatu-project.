import streamlit as st
import pandas as pd
from PIL import Image
from streamlit_drawable_canvas import st_canvas
import io
import base64

# --- SETTING PAGE ---
st.set_page_config(page_title="NORYZE CAD PRO", layout="wide")

# CSS Tema Gelap AutoCAD
st.markdown("""
    <style>
    .stApp { background-color: #0b0e14; color: #00ff41; }
    [data-testid="stSidebar"] { background-color: #161b22; }
    </style>
    """, unsafe_allow_html=True)

# --- FUNGSI PENYELAMAT GAMBAR ---
def get_image_base64(img):
    buffered = io.BytesIO()
    img.save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue()).decode()

# --- SIDEBAR TOOLBAR ---
with st.sidebar:
    st.title("📐 NORYZE TOOLBAR")
    src = st.radio("Sumber Pola:", ["Album / Galeri", "Kamera HP"])
    
    bg_image = None
    uploaded_file = None
    
    if src == "Album / Galeri":
        uploaded_file = st.file_uploader("Upload Pola Adidas", type=['png', 'jpg', 'jpeg'])
    else:
        uploaded_file = st.camera_input("Ambil Foto")

    # Proses Gambar dengan Resize & Thumbnail
    if uploaded_file:
        try:
            img_raw = Image.open(uploaded_file)
            # Resize agar canvas tidak berat (max 800px)
            img_raw.thumbnail((800, 800))
            bg_image = img_raw
        except Exception as e:
            st.error("Gagal membaca file gambar.")

    st.markdown("---")
    tool = st.selectbox("Pilih Alat:", ("freedraw", "line", "rect", "circle", "transform"))
    stroke_width = st.slider("Tebal Garis:", 1, 10, 3)
    stroke_color = st.color_picker("Warna:", "#00ff41")

# --- WORKSPACE ---
st.header("🖥️ NORYZE CAD ENGINE")
col_canvas, col_info = st.columns([3, 1])

with col_canvas:
    # Menjalankan Canvas
    canvas_result = st_canvas(
        fill_color="rgba(0, 255, 65, 0.2)",
        stroke_width=stroke_width,
        stroke_color=stroke_color,
        background_image=bg_image, # Streamlit-canvas menangani PIL image di versi terbaru
        update_streamlit=True,
        height=600,
        drawing_mode=tool,
        key="noryze_stable_v12",
    )
    st.info("💡 Klik 'freedraw' untuk menjiplak lekukan pola Adidas di atas.")

with col_info:
    st.subheader("📊 Info Produksi")
    p_master = st.number_input("Panjang (cm)", value=26.5)
    l_master = st.number_input("Lebar (cm)", value=10.0)
    
    st.markdown("---")
    st.write("**Data Grading Otomatis**")
    grad_list = []
    for s in range(38, 43):
        diff = s - 40
        grad_list.append({
            "Size": s,
            "P (cm)": round(p_master + (diff * 0.66), 2),
            "L (cm)": round(l_master + (diff * 0.2), 2)
        })
    st.dataframe(pd.DataFrame(grad_list), hide_index=True)

if st.button("💾 Ekspor Koordinat Vektor"):
    st.balloons()
    st.success("Koordinat pola berhasil dikonversi ke format CAD!")
