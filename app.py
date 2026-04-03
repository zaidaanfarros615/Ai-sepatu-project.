import streamlit as st
import pandas as pd
import numpy as np
import cv2
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from PIL import Image

# --- KONFIGURASI CAD DARK MODE ---
st.set_page_config(page_title="NORYZE CAD PRO", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #0b0e14; color: #00ff41; }
    .sidebar .sidebar-content { background-color: #161b22; border-right: 1px solid #30363d; }
    .stMetric { background: #161b22; border: 1px solid #30363d; padding: 10px; border-radius: 8px; }
    .cad-header { color: #ffffff; font-family: 'Courier New', Courier, monospace; border-bottom: 2px solid #00ff41; }
    </style>
    """, unsafe_allow_html=True)

# --- FUNGSI ENGINE CAD ---
def draw_cad_workspace(p, l, v_point, j_point, margin, size_name):
    fig, ax = plt.subplots(figsize=(12, 7), facecolor='#0b0e14')
    ax.set_facecolor('#0b0e14')
    
    # Grid Utama (Major & Minor)
    ax.grid(which='major', color='#1f242c', linestyle='-', linewidth=0.8)
    ax.grid(which='minor', color='#161b22', linestyle=':', linewidth=0.5)
    ax.minorticks_on()

    # Drawing Pola (Main Object)
    main_pola = patches.Rectangle((0, 0), p, l, linewidth=2, edgecolor='#00ff41', facecolor='none')
    ax.add_patch(main_pola)

    # Drawing Seam Allowance / Cutting Margin (Layer 2)
    margin_pola = patches.Rectangle((-margin, -margin), p+(2*margin), l+(2*margin), 
                                    linewidth=1, edgecolor='#ff3e3e', linestyle='--', facecolor='none', label='Cutting Margin')
    ax.add_patch(margin_pola)

    # Drafting Lines (Titik Ukur ATK Yogyakarta)
    ax.axvline(x=v_point, color='#3b82f6', alpha=0.6, label='Vamp Line')
    ax.axvline(x=j_point, color='#f59e0b', alpha=0.6, label='Joint Line')
    ax.scatter([v_point, j_point], [l/2, l/2], color='white', zorder=5)

    # Label Dimensi ala AutoCAD
    ax.annotate('', xy=(0, -2), xytext=(p, -2), arrowprops=dict(arrowstyle='<->', color='white'))
    ax.text(p/2, -3.5, f"{p} cm", color='white', ha='center', fontsize=10)
    
    ax.set_xlim(-5, p + 10)
    ax.set_ylim(-5, l + 10)
    ax.set_title(f"CAD VIEWER - LAYER: SIZE {size_name}", color='white', loc='left', fontsize=14)
    ax.legend(facecolor='#0b0e14', labelcolor='white', loc='upper right')
    return fig

# --- TOOLBAR UTAMA (SIDEBAR) ---
with st.sidebar:
    st.markdown("<h2 class='cad-header'>CAD TOOLBAR</h2>", unsafe_allow_html=True)
    
    # FITUR REQUEST: INPUT DARI ALBUM JANGAN HILANG
    st.subheader("📁 Input Data")
    input_type = st.radio("Source:", ["📷 Camera", "🖼️ Gallery/Album"])
    file_pola = None
    if input_type == "📷 Camera":
        file_pola = st.camera_input("Scan Pola")
    else:
        file_pola = st.file_uploader("Upload Pola dari Album", type=['png', 'jpg', 'jpeg'])

    st.markdown("---")
    st.subheader("🛠️ Drafting Tools")
    tool = st.selectbox("Active Command:", ["SELECT", "MEASURE", "OFFSET (Margin)", "GRADING"])
    
    st.subheader("📐 Property Editor")
    p_master = st.number_input("Length (cm)", value=25.5)
    l_master = st.number_input("Width (cm)", value=10.0)
    c_margin = st.slider("Cutting Margin (mm)", 0, 10, 5) / 10 # Convert to CM
    
    st.subheader("🧪 Nesting & Cutting")
    material_w = st.number_input("Lebar Bahan (cm)", value=100)
    gap = st.slider("Gap antar Pola (cm)", 0.1, 2.0, 0.5)

# --- WORKSPACE AREA ---
col_main, col_stats = st.columns([3, 1])

with col_main:
    # Logic ATK Engineering
    v_p = p_master * 0.7
    j_p = p_master * 0.66
    
    # Render Drawing
    st.pyplot(draw_cad_workspace(p_master, l_master, v_p, j_p, c_margin, "MASTER"))
    
    # Fitur "P-Cutting" (Prompt Permintaan)
    st.chat_input("Ketik perintah CAD (Contoh: 'Buat grading size 38-44' atau 'Hitung efisiensi bahan')")

with col_stats:
    st.markdown("<h3 style='color:white'>Object Info</h3>", unsafe_allow_html=True)
    st.metric("Total Perimeter", f"{round(2*(p_master+l_master), 2)} cm")
    st.metric("Cutting Area", f"{round(p_master * l_master, 2)} cm²")
    
    st.markdown("---")
    st.subheader("📦 Nesting Calc")
    # Hitung berapa banyak pola muat dalam 1 baris bahan
    per_row = int(material_w / (l_master + gap))
    st.write(f"Estimasi per Baris: **{per_row} pcs**")
    st.write(f"Efisiensi Ruang: **{round(((l_master*per_row)/material_w)*100, 1)}%**")

# --- GRADING AUTO-GENERATION ---
st.markdown("---")
st.header("📐 Automated Grading Engine")
col_grad = st.columns(5)

sizes = [38, 39, 40, 41, 42]
for i, s in enumerate(sizes):
    diff = s - 40 # Master 40
    p_s = p_master + (diff * 0.66)
    l_s = l_master + (diff * 0.2)
    
    with col_grad[i]:
        st.metric(f"Size {s}", f"{round(p_s, 2)} cm")
        # Mini Drawing
        f_m, a_m = plt.subplots(figsize=(2, 2), facecolor='#0b0e14')
        a_m.set_facecolor('#0b0e14')
        a_m.add_patch(patches.Rectangle((0,0), p_s, l_s, edgecolor='#00ff41', facecolor='none'))
        a_m.axis('off')
        a_m.set_xlim(-2, 35)
        a_m.set_ylim(-2, 15)
        st.pyplot(f_m)

st.caption("NORYZE CAD PRO v10.0 | High-Precision Footwear Engineering")
