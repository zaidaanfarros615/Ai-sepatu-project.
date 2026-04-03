import streamlit as st
import pandas as pd
import numpy as np
import cv2
from PIL import Image

# Konfigurasi Tema Dark Professional
st.set_page_config(page_title="NORYZE ULTIMATE AI", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #0e1117; color: white; }
    .stTabs [data-baseweb="tab-list"] { gap: 24px; }
    .stTabs [data-baseweb="tab"] { height: 50px; white-space: pre-wrap; background-color: #1e2130; border-radius: 10px 10px 0px 0px; gap: 1px; }
    .stTabs [aria-selected="true"] { background-color: #4CAF50; }
    </style>
    """, unsafe_allow_html=True)

st.title("👟 NORYZE ULTIMATE: AI Design & Grading Station")
st.markdown("---")

# --- DATA STATE MANAGEMENT ---
if 'p_detected' not in st.session_state:
    st.session_state['p_detected'] = 25.0
if 'l_detected' not in st.session_state:
    st.session_state['l_detected'] = 9.5

# --- LAYOUT UTAMA ---
tab1, tab2, tab3 = st.tabs(["🔍 AI SCANNER", "🛠️ MANUAL EDITOR & TOOLS", "📋 GRADING REPORT"])

# --- TAB 1: AI SCANNER ---
with tab1:
    col_cam, col_res = st.columns([1, 1])
    with col_cam:
        st.subheader("📸 Scan Pola")
        img_file = st.camera_input("Ambil Foto Pola")
        
    with col_res:
        st.subheader("🤖 Analisis AI Vision")
        if img_file:
            # Simulasi AI Processing
            st.success("Analisis Edge Detection Selesai!")
            st.session_state['p_detected'] = 26.4 # Contoh hasil deteksi AI
            st.session_state['l_detected'] = 10.2
            st.info(f"AI Mendeteksi: Panjang {st.session_state['p_detected']} cm, Lebar {st.session_state['l_detected']} cm")
        else:
            st.warning("Silakan ambil foto pola di atas penggaris untuk mulai.")

# --- TAB 2: MANUAL EDITOR & TOOLS ---
with tab2:
    st.subheader("🛠️ Tools & Parameter Adjustment")
    col_tools1, col_tools2, col_tools3 = st.columns(3)
    
    with col_tools1:
        st.markdown("**📏 Koreksi Dimensi**")
        p_edit = st.number_input("Sesuaikan Panjang (cm)", value=st.session_state['p_detected'])
        l_edit = st.number_input("Sesuaikan Lebar (cm)", value=st.session_state['l_detected'])
    
    with col_tools2:
        st.markdown("**📐 Aturan Grading**")
        pitch_p = st.selectbox("Pitch Panjang", [0.6, 0.66, 0.8], index=1)
        pitch_l = st.number_input("Pitch Lebar", value=0.2, step=0.05)
        
    with col_tools3:
        st.markdown("**🎯 Master Setting**")
        sz_master = st.number_input("Size Master (EUR)", value=40)
        allowance = st.slider("Ruang Gerak (Fitting) cm", 1.0, 2.5, 1.58)

    st.markdown("---")
    st.subheader("💡 Preview Pola (Scale Visualization)")
    # Visualisasi Sederhana
    st.markdown(f"""
        <div style="display: flex; justify-content: center; align-items: center; border: 2px dashed #4CAF50; padding: 20px; border-radius: 15px;">
            <div style="width: {l_edit*15}px; height: {p_edit*15}px; background: #4CAF50; border: 2px solid white; border-radius: 5px; position: relative;">
                <p style="color: white; font-size: 10px; text-align: center; margin-top: 50%;">SZ {sz_master}</p>
            </div>
        </div>
    """, unsafe_allow_html=True)

# --- TAB 3: GRADING REPORT ---
with tab3:
    st.subheader("📊 Hasil Akhir Grading")
    
    # Perhitungan data
    grading_data = []
    for s in range(36, 46):
        selisih = s - sz_master
        p_res = (p_edit + allowance) + (selisih * pitch_p)
        l_res = l_edit + (selisih * pitch_l)
        
        grading_data.append({
            "Size": s,
            "Panjang Pola (cm)": round(p_res, 2),
            "Lebar Pola (cm)": round(l_res, 2),
            "Status": "MASTER" if s == sz_master else "GRADED"
        })
    
    df = pd.DataFrame(grading_data)
    st.dataframe(df.style.highlight_max(axis=0), use_container_width=True)
    
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button("📥 Ekspor Data Produksi", csv, "noryze_ultimate.csv", "text/csv")

st.markdown("---")
st.caption("NORYZE ULTIMATE v6.0 | Berbasis Biomekanika ATK Yogyakarta | 2026")
