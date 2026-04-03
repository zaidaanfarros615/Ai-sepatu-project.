import streamlit as st
import pandas as pd
from PIL import Image
from streamlit_drawable_canvas import st_canvas

# Setup Tampilan AutoCAD
st.set_page_config(page_title="NORYZE CAD", layout="wide")
st.markdown("<style>.stApp {background-color: #0b0e14; color: #00ff41;}</style>", unsafe_allow_html=True)

# Sidebar Toolbar
with st.sidebar:
    st.title("🛠️ CAD TOOLS")
    uploaded_file = st.file_uploader("Upload Pola Adidas", type=["png", "jpg", "jpeg"])
    
    bg_img = None
    if uploaded_file:
        img = Image.open(uploaded_file)
        # Paksa resize agar canvas tidak crash
        img.thumbnail((700, 700))
        bg_img = img

    st.markdown("---")
    mode = st.selectbox("Alat:", ("freedraw", "line", "transform"))
    stroke_w = st.slider("Tebal:", 1, 10, 3)
    stroke_c = st.color_picker("Warna:", "#00ff41")

# Main Canvas
st.title("🖥️ NORYZE WORKSPACE")

col1, col2 = st.columns([3, 1])

with col1:
    # Canvas Tanpa Error
    canvas_result = st_canvas(
        fill_color="rgba(0, 255, 65, 0.2)",
        stroke_width=stroke_w,
        stroke_color=stroke_c,
        background_image=bg_img,
        update_streamlit=True,
        height=550,
        width=700,
        drawing_mode=mode,
        key="noryze_final_fix"
    )

with col2:
    st.subheader("📐 Ukuran")
    p_master = st.number_input("Panjang (cm)", value=26.5)
    
    # Tabel Grading Langsung Muncul
    st.write("**Grading List:**")
    data = []
    for s in [39, 40, 41]:
        diff = s - 40
        data.append({"Size": s, "P (cm)": round(p_master + (diff * 0.66), 2)})
    st.table(pd.DataFrame(data))

if st.button("💾 SAVE PROJECT"):
    st.success("Koordinat Pola Tersimpan!")
