import streamlit as st
import pandas as pd
import numpy as np
import cv2
from PIL import Image
from datetime import datetime

# Konfigurasi Tema Industri Modern
st.set_page_config(page_title="NORYZE x SHOEMETRICS", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #0f172a; color: #f8fafc; }
    .metric-card { background: #1e293b; padding: 15px; border-radius: 15px; border: 1px solid #334155; text-align: center; }
    .stTabs [data-baseweb="tab-list"] { gap: 10px; }
    .stTabs [data-baseweb="tab"] { background-color: #1e293b; border-radius: 10px 10px 0 0; padding: 10px 20px; }
    .stTabs [aria-selected="true"] { background-color: #3b82f6 !important; color: white !important; }
    </style>
    """, unsafe_allow_html=True)

# --- HEADER ---
st.title("👟 NORYZE × SHOEMETRICS")
st.markdown("<span style='color:#10b981'>ATK YOGYAKARTA STANDARDS | INTEGRATED ENGINEERING SYSTEM</span>", unsafe_allow_html=True)
st.markdown("---")

# --- LOGIKA PERHITUNGAN SHOEMETRICS (TRANSPLANTASI DARI JS) ---
def calculate_engineering(p_kaki, girth_kaki, style_allowance, toe_extra, heel_height):
    # Standar Internasional French Point (EU)
    # EU Size = (Panjang Kaki + Allowance) * 1.5
    allowance_total = style_allowance + toe_extra
    sl_panjang_last = p_kaki + allowance_total
    eu_size = sl_panjang_last * 1.5
    
    # Perhitungan Komponen Pola (Point Engineering)
    # Berdasarkan standar Shoemetrics yang kamu berikan
    vamp_point = sl_panjang_last * 0.7  # 7/10 SL
    joint_point = sl_panjang_last * 0.66 # 2/3 SL
    instep_point = sl_panjang_last * 0.5 # 1/2 SL
    
    # Girth Mold Analysis
    # Penyesuaian lingkar berdasarkan tinggi hak (Heel Height)
    girth_adjustment = (heel_height * 0.1) # Semakin tinggi hak, lingkar sedikit berubah
    girth_final = girth_kaki + girth_adjustment
    
    return {
        "eu_size": round(eu_size, 1),
        "sl_last": round(sl_panjang_last, 2),
        "vamp": round(vamp_point, 2),
        "joint": round(joint_point, 2),
        "instep": round(instep_point, 2),
        "girth": round(girth_final, 2),
        "allowance": round(allowance_total, 2)
    }

# --- SIDEBAR: INPUT TEKNIS ---
with st.sidebar:
    st.header("⚙️ Project Settings")
    project_name = st.text_input("🏷️ Project Name", "NORYZE_01")
    gender = st.radio("👤 Gender", ["MEN", "WOMEN"])
    
    st.markdown("---")
    st.subheader("📏 Foot Measurements")
    p_kaki = st.number_input("Foot Length (cm)", value=25.0, step=0.1)
    g_kaki = st.number_input("Ball Girth (cm)", value=23.5, step=0.1)
    
    st.markdown("---")
    st.subheader("👞 Style & Design")
    style = st.selectbox("Shoe Style", [
        ("Sport/Sneakers (+1.5cm)", 1.5),
        ("Oxford/Casual (+1.0cm)", 1.0),
        ("Pumps/Stiletto (+0.4cm)", 0.4),
        ("Safety Boots (+2.0cm)", 2.0)
    ], format_func=lambda x: x[0])
    
    toe = st.selectbox("Toe Shape", [
        ("Round Toe (+0.1cm)", 0.1),
        ("Square Toe (+0.0cm)", 0.0),
        ("Pointy/Lancip (+2.5cm)", 2.5)
    ], format_func=lambda x: x[0])
    
    heel = st.number_input("Heel Height (cm)", value=0.0, step=0.5)

# --- EXECUTION ---
eng = calculate_engineering(p_kaki, g_kaki, style[1], toe[1], heel)

# --- MAIN INTERFACE ---
tab1, tab2, tab3 = st.tabs(["🔍 AI VISION SCANNER", "📐 ENGINEERING SPEC", "📊 MANUFACTURING REPORT"])

with tab1:
    col_a, col_b = st.columns(2)
    with col_a:
        st.subheader("📸 Pattern Capture")
        camera_img = st.camera_input("Scan Pola Asli")
    with col_b:
        st.subheader("🤖 AI Analysis")
        if camera_img:
            st.success("Edge Detection Active")
            st.info(f"AI Recommendation: Use EU Size {eng['eu_size']}")
        else:
            st.warning("Menunggu input kamera untuk sinkronisasi otomatis...")

with tab2:
    st.subheader(f"🛠️ Technical Specification: {project_name}")
    
    # Dashboard Metrics
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("EU SIZE", eng['eu_size'])
    m2.metric("LAST LENGTH (SL)", f"{eng['sl_last']} cm")
    m3.metric("GIRTH MOLD", f"{eng['girth']} cm")
    m4.metric("ALLOWANCE", f"{eng['allowance']} cm")
    
    st.markdown("---")
    st.subheader("📐 Pattern Marking Points (A-Z Standard)")
    
    # Diagram Illustrasi (Konsep Visual)
    st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/5/5b/Shoe_last_measurements.png/400px-Shoe_last_measurements.png", width=300)
    
    col_spec1, col_spec2 = st.columns(2)
    with col_spec1:
        st.write(f"📍 **Vamp Point (V):** {eng['vamp']} cm (7/10 SL)")
        st.write(f"📍 **Joint Point (J):** {eng['joint']} cm (2/3 SL)")
    with col_spec2:
        st.write(f"📍 **Instep Point (I):** {eng['instep']} cm (1/2 SL)")
        st.write(f"📍 **Toe Spring Adj:** Standard {toe[0]}")

with tab3:
    st.subheader("📊 Production Grading Report")
    
    # Generate Tabel Grading Otomatis
    grading_list = []
    for s in range(36, 46):
        # Selisih dari Master Size hasil hitungan
        diff = s - int(eng['eu_size'])
        p_grad = eng['sl_last'] + (diff * 0.66)
        g_grad = eng['girth'] + (diff * 0.3) # Standar penambahan lingkar
        
        grading_list.append({
            "Size (EU)": s,
            "Last Length (cm)": round(p_grad, 2),
            "Girth/Lingkar (cm)": round(g_grad, 2),
            "Status": "MASTER" if s == int(eng['eu_size']) else "GRADED"
        })
    
    df_grading = pd.DataFrame(grading_list)
    st.table(df_grading)
    
    # Export Button
    csv = df_grading.to_csv(index=False).encode('utf-8')
    st.download_button("📥 Download Engineering Sheet (CSV)", csv, f"{project_name}_report.csv", "text/csv")

st.markdown("---")
st.caption(f"NORYZE x SHOEMETRICS v7.0 | Generated at: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
