import streamlit as st
import pandas as pd
import numpy as np
import cv2
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from io import BytesIO

# Konfigurasi Tema CAD (Dark Charcoal)
st.set_page_config(page_title="NORYZE CAD ENGINE", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #121212; color: #00FF00; } /* Neon Green typical of CAD */
    .sidebar .sidebar-content { background-color: #1e1e1e; }
    h1, h2, h3 { color: #FFFFFF !important; font-family: 'Segoe UI', sans-serif; }
    .stMetric { background: #252525; border: 1px solid #3b82f6; border-radius: 5px; }
    </style>
    """, unsafe_allow_html=True)

# --- ENGINE: LOGIKA KOORDINAT CAD ---
def generate_cad_preview(p, l, vamp_p, joint_p, size):
    fig, ax = plt.subplots(figsize=(10, 6), facecolor='#1e1e1e')
    ax.set_facecolor('#1e1e1e')
    
    # Grid ala AutoCAD
    ax.grid(color='#333333', linestyle='--', linewidth=0.5)
    
    # Gambar Pola Utama (Rectangle as Base)
    pattern = patches.Rectangle((0, 0), p, l, linewidth=2, edgecolor='#00FF00', facecolor='none', label=f'Size {size}')
    ax.add_patch(pattern)
    
    # Garis Sumbu (X-Y Axis)
    ax.axhline(0, color='white', linewidth=1)
    ax.axvline(0, color='white', linewidth=1)
    
    # Penanda Titik Engineering (ShoeMetrics Standards)
    ax.scatter([vamp_p], [l/2], color='red', s=50, label='Vamp Point (V)')
    ax.axvline(x=joint_p, color='#3b82f6', linestyle=':', label='Joint Line (J)')
    
    # Anotasi Dimensi ala Corel
    ax.annotate(f'{p} cm', xy=(p/2, l+0.5), color='white', ha='center')
    ax.annotate(f'{l} cm', xy=(p+0.5, l/2), color='white', rotation=-90, va='center')
    
    ax.set_xlim(-2, p + 5)
    ax.set_ylim(-2, l + 5)
    ax.set_title(f"CAD WORKSPACE - SIZE {size}", color='white', loc='left')
    ax.legend(facecolor='#1e1e1e', labelcolor='white')
    
    return fig

# --- SIDEBAR: TOOLBAR KIRI (Ala Photoshop/Corel) ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/1055/1055666.png", width=50) # Icon Tools
    st.title("CAD TOOLBAR")
    
    tool_mode = st.radio("Active Tool:", ["📐 Dimension Tool", "✂️ Cutting Edit", "🖊️ Mark Point"])
    
    st.markdown("---")
    st.subheader("Property Editor")
    sz_master = st.number_input("Nomor Master (EUR)", value=40)
    p_base = st.number_input("Base Length (cm)", value=25.5, step=0.1)
    l_base = st.number_input("Base Width (cm)", value=10.0, step=0.1)
    
    st.subheader("Layer Settings")
    show_grid = st.checkbox("Show Grid Lines", value=True)
    line_color = st.color_picker("Line Color", "#00FF00")

# --- MAIN WORKSPACE ---
col_canvas, col_props = st.columns([2.5, 1])

with col_canvas:
    st.subheader("🖥️ Design Canvas")
    
    # Kalkulasi Engineering
    v_point = p_base * 0.7
    j_point = p_base * 0.66
    
    # Tampilkan Preview CAD
    cad_fig = generate_cad_preview(p_base, l_base, v_point, j_point, sz_master)
    st.pyplot(cad_fig)
    
    st.info("💡 Mode AutoCAD Aktif: Gunakan Toolbar kiri untuk merubah dimensi Master.")

with col_props:
    st.subheader("📑 Object Properties")
    with st.expander("Anatomi & Fitting", expanded=True):
        st.write(f"Vamp Position: `{round(v_point,2)} cm`")
        st.write(f"Joint Line: `{round(j_point,2)} cm`")
        st.write(f"Toe Spring: `Standard 1.5cm` (Auto)")
    
    with st.expander("AI Scan Calibration"):
        cam_file = st.camera_input("Sync AI Vision")
        if cam_file:
            st.success("Visual Sync Complete")

# --- BOTTOM SECTION: GRADING AUTOMATION (DIBUAT SEPERTI TIMELINE CORE) ---
st.markdown("---")
st.header("🎞️ Grading Multi-Scale View")
sizes = st.multiselect("Pilih Layer Ukuran yang ingin di-Grading:", 
                      [36, 37, 38, 39, 40, 41, 42, 43, 44, 45], default=[38, 40, 42])

c_grad = st.columns(len(sizes))
for i, s in enumerate(sizes):
    diff = s - sz_master
    p_grad = p_base + (diff * 0.66)
    l_grad = l_base + (diff * 0.2)
    
    with c_grad[i]:
        st.metric(f"Size {s}", f"{round(p_grad, 2)} cm")
        # Mini Preview per ukuran
        mini_fig, mini_ax = plt.subplots(figsize=(2, 2), facecolor='#121212')
        mini_ax.set_facecolor('#1e1e1e')
        rect = patches.Rectangle((0, 0), p_grad, l_grad, color=line_color, alpha=0.5)
        mini_ax.add_patch(rect)
        mini_ax.axis('off')
        mini_ax.set_xlim(0, 35)
        mini_ax.set_ylim(0, 15)
        st.pyplot(mini_fig)

st.caption("NORYZE CAD ENGINE v9.0 | Integrated Engineering Design")
