import streamlit as st
import pandas as pd
import numpy as np
import cv2
from PIL import Image

st.set_page_config(page_title="NORYZE AI ULTIMATE", layout="wide")

# --- CSS MEWAH ---
st.markdown("""
    <style>
    .stApp { background-color: #0f172a; }
    .st-emotion-cache-1kyxreq { justify-content: center; }
    .reportview-container .main { color: white; }
    .sidebar .sidebar-content { background: #1e293b; }
    div[data-testid="stMetricValue"] { color: #10b981; font-family: 'Courier New'; }
    </style>
    """, unsafe_allow_html=True)

# --- FUNGSI AI CERDAS (Object Detection & Scaling) ---
def advanced_ai_scan(image_file, ref_width_cm):
    file_bytes = np.asarray(bytearray(image_file.read()), dtype=np.uint8)
    img = cv2.imdecode(file_bytes, 1)
    
    # Pre-processing untuk deteksi kontur
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (7, 7), 0)
    edged = cv2.Canny(blur, 40, 150)
    
    cnts, _ = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    if len(cnts) < 1:
        return 25.0, 10.0, edged
    
    # Ambil kontur terbesar (Pola Sepatu)
    cnts = sorted(cnts, key=cv2.contourArea, reverse=True)
    c_pola = cnts[0]
    
    # Hitung Bounding Box
    x, y, w, h = cv2.boundingRect(c_pola)
    
    # Logika Kalibrasi: 
    # Jika ada koin, gunakan koin. Jika tidak, gunakan nilai referensi standar (Pixel per CM)
    px_per_cm = w / ref_width_cm # Kalibrasi berdasarkan input manual 'Prom Edit'
    
    calc_h = h / px_per_cm
    calc_w = w / px_per_cm
    
    return round(calc_h, 2), round(calc_w, 2), edged

# --- UI INTERFACE ---
st.title("👟 NORYZE AI ULTIMATE v8.0")
st.markdown("---")

# --- STEP 1: AI SCANNING ---
st.header("📸 1. Advanced AI Scanner")
c_scan, c_preview = st.columns([1, 1])

with c_scan:
    mode = st.radio("Input Source:", ["Live Camera", "Upload Gallery"])
    if mode == "Live Camera":
        foto = st.camera_input("Scan Pola")
    else:
        foto = st.file_uploader("Upload Pola", type=['jpg','png','jpeg'])
    
    ref_val = st.slider("📐 Calibration (Jika hasil melesat, geser ini)", 20.0, 30.0, 25.4)

p_ai, l_ai = 25.0, 9.5
if foto:
    p_ai, l_ai, process_view = advanced_ai_scan(foto, ref_val)
    with c_preview:
        st.image(process_view, caption="AI Vision: Edge Contours Detected", use_container_width=True)
        st.success(f"AI Suggestion: {p_ai} cm x {l_ai} cm")

st.markdown("---")

# --- STEP 2: PROFESSIONAL EDITING TOOLS ---
st.header("🛠️ 2. Production Editing Tools (Prom)")
col_tool1, col_tool2, col_tool3 = st.columns(3)

with col_tool1:
    st.subheader("📏 Master Adjustment")
    # Fitur EDIT Canggih: Menggabungkan hasil AI ke slider manual
    final_p = st.number_input("Final Length (cm)", value=p_ai)
    final_l = st.number_input("Final Width (cm)", value=l_ai)
    sz_master = st.number_input("Master Size", value=40)

with col_tool2:
    st.subheader("📐 Engineering Param")
    # Standar ATK Yogyakarta Hal 27
    allowance = st.selectbox("Foot Fitting (Allowance)", [1.58, 1.0, 2.54], format_func=lambda x: f"{x} cm (Standard)")
    pitch_p = st.slider("Grading Pitch Length", 0.60, 0.80, 0.66)
    pitch_l = st.slider("Grading Pitch Width", 0.15, 0.30, 0.20)

with col_tool3:
    st.subheader("🧵 Material Analysis")
    wastage = st.slider("Wastage Margin (%)", 5, 25, 15)
    material = st.selectbox("Upper Material", ["Cow Leather", "Synthetic", "Canvas", "Mesh"])

# --- STEP 3: AUTOMATED PRODUCTION REPORT ---
st.markdown("---")
st.header("📊 3. Automated Manufacturing Report")

# Live Metrics
sl_last = final_p + allowance
m1, m2, m3 = st.columns(3)
m1.metric("Last Length (SL)", f"{round(sl_last, 2)} cm")
m2.metric("Vamp Point (7/10)", f"{round(sl_last * 0.7, 2)} cm")
m3.metric("Joint Girth Est.", f"{round(final_l * 2.4, 1)} cm")

# Tabel Grading
grading_data = []
for s in range(36, 46):
    selisih = s - sz_master
    p_grad = sl_last + (selisih * pitch_p)
    l_grad = final_l + (selisih * pitch_l)
    
    # Rumus Luas (Standard Industrial)
    area = (p_grad * l_grad * 2.2) * (1 + wastage/100)
    
    grading_data.append({
        "Size": s,
        "Length (cm)": round(p_grad, 2),
        "Width (cm)": round(l_grad, 2),
        "Material Req (cm²)": round(area, 1),
        "Status": "MASTER" if s == sz_master else "GRADED"
    })

df = pd.DataFrame(grading_data)
st.dataframe(df.style.highlight_max(subset=['Length (cm)'], color='#3b82f6'), use_container_width=True)

# Download Section
csv = df.to_csv(index=False).encode('utf-8')
st.download_button("📥 Export Production Sheet", csv, "noryze_production.csv", "text/csv")
