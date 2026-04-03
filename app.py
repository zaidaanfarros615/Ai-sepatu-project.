import streamlit as st
import pandas as pd
import numpy as np
import cv2
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from PIL import Image

# --- CONFIGURASI UI ---
st.set_page_config(page_title="NORYZE AI CAD ULTIMATE", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #0b0e14; color: #00ff41; }
    .sidebar .sidebar-content { background-color: #161b22; border-right: 1px solid #30363d; }
    .stMetric { background: #1c2128; border: 1px solid #00ff41; padding: 10px; border-radius: 5px; }
    .cad-label { color: #8b949e; font-size: 12px; font-weight: bold; text-transform: uppercase; }
    </style>
    """, unsafe_allow_html=True)

# --- ENGINE AI: DETEKSI DIMENSI OTOMATIS ---
def ai_dimension_detector(uploaded_file):
    if uploaded_file is None:
        return 25.0, 10.0, None
    
    # Konversi ke format OpenCV
    file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
    img = cv2.imdecode(file_bytes, 1)
    
    # Image Processing (Canny Edge Detection)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    edged = cv2.Canny(blur, 50, 150)
    
    # Cari Kontur Terbesar (Pola)
    contours, _ = cv2.findContours(edged, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    if contours:
        c = max(contours, key=cv2.contourArea)
        x, y, w, h = cv2.boundingRect(c)
        
        # Kalibrasi dasar (asumsi standard 1px = sekian cm)
        # User bisa memperbaiki ini di editor
        p_detected = h / 37.8 
        l_detected = w / 37.8
        return round(p_detected, 2), round(l_detected, 2), edged
    
    return 25.0, 10.0, edged

# --- ENGINE CAD DRAWING ---
def render_cad_canvas(p, l, margin, size):
    fig, ax = plt.subplots(figsize=(10, 6), facecolor='#0b0e14')
    ax.set_facecolor('#0b0e14')
    
    # Drawing Grid
    ax.grid(color='#1f242c', linestyle='-', linewidth=0.5)
    
    # Layer 1: Pola Utama (Green Neon)
    rect = patches.Rectangle((0, 0), p, l, linewidth=2, edgecolor='#00ff41', facecolor='none', label='Main Pattern')
    ax.add_patch(rect)
    
    # Layer 2: Cutting Margin (Red Dash)
    if margin > 0:
        cut_rect = patches.Rectangle((-margin, -margin), p+(2*margin), l+(2*margin), 
                                     linewidth=1, edgecolor='#ff3e3e', linestyle='--', facecolor='none', label='Seam Allowance')
        ax.add_patch(cut_rect)
    
    # Dimensi Dinamis
    ax.annotate(f'{p} cm', xy=(p/2, l+1), color='white', ha='center', fontsize=9)
    ax.annotate(f'{l} cm', xy=(p+1, l/2), color='white', rotation=-90, va='center', fontsize=9)
    
    ax.set_xlim(-5, p+10)
    ax.set_ylim(-5, l+10)
    ax.axis('off')
    ax.set_title(f"CAD WORKSPACE [MODE: EDITING SIZE {size}]", color='#00ff41', fontsize=10)
    return fig

# --- SIDEBAR TOOLBAR ---
with st.sidebar:
    st.title("🛠️ CAD TOOLBAR")
    
    # INPUT SOURCE (Album / Camera)
    st.subheader("📁 Input Source")
    src = st.radio("Ambil Data Dari:", ["Galeri Album", "Kamera Langsung"])
    if src == "Galeri Album":
        uploaded = st.file_uploader("Upload Foto Pola", type=['jpg','png','jpeg'])
    else:
        uploaded = st.camera_input("Scan Pola")
    
    # AI SCAN BUTTON
    st.markdown("---")
    ai_p, ai_l, ai_view = ai_dimension_detector(uploaded)
    
    if uploaded:
        st.success(f"AI Detected: {ai_p}x{ai_l} cm")
        if st.checkbox("Lihat Jalur AI Scan"):
            st.image(ai_view, use_container_width=True)

    # PROPERTY EDITOR
    st.subheader("📐 Property Editor")
    edit_p = st.number_input("Length (L)", value=ai_p)
    edit_l = st.number_input("Width (W)", value=ai_l)
    edit_m = st.slider("Cutting Margin (mm)", 0, 10, 5) / 10
    edit_sz = st.number_input("Master Size", value=40)

# --- MAIN WORKSPACE ---
col_canvas, col_tools = st.columns([3, 1])

with col_canvas:
    # Render Utama
    st.pyplot(render_cad_canvas(edit_p, edit_l, edit_m, edit_sz))
    
    # P-CUTTING COMMAND (Prompt Editing)
    cmd = st.chat_input("P-Cutting: Ketik perintah (Contoh: 'Ubah panjang ke 27' atau 'Tambah margin 1cm')")
    if cmd:
        st.info(f"Command '{cmd}' diterima. Memproses modifikasi...")

with col_tools:
    st.markdown("<p class='cad-label'>Engineering Data</p>", unsafe_allow_html=True)
    st.metric("VAMP POINT", f"{round(edit_p * 0.7, 2)} cm")
    st.metric("JOINT LINE", f"{round(edit_p * 0.66, 2)} cm")
    
    st.markdown("---")
    st.markdown("<p class='cad-label'>Nesting / Efficiency</p>", unsafe_allow_html=True)
    eff = (edit_p * edit_l) / ((edit_p+1) * (edit_l+1)) * 100
    st.write(f"Efisiensi Bahan: **{round(eff, 1)}%**")
    
# --- GRADING SECTION ---
st.markdown("---")
st.subheader("📊 Automated Multi-Size Grading")
sizes = [37, 38, 39, 40, 41, 42, 43]
cols = st.columns(len(sizes))

for i, s in enumerate(sizes):
    diff = s - edit_sz
    grad_p = edit_p + (diff * 0.66)
    grad_l = edit_l + (diff * 0.2)
    with cols[i]:
        st.metric(f"SZ {s}", f"{round(grad_p, 1)}")
        # Mini Preview
        fig_m, ax_m = plt.subplots(figsize=(1.5, 1.5), facecolor='#0b0e14')
        ax_m.set_facecolor('#0b0e14')
        ax_m.add_patch(patches.Rectangle((0,0), grad_p, grad_l, edgecolor='#00ff41', facecolor='none'))
        ax_m.axis('off')
        ax_m.set_xlim(-2, 35)
        ax_m.set_ylim(-2, 15)
        st.pyplot(fig_m)

st.caption("NORYZE CAD ULTIMATE v11.0 | 2026 Integrated AI System")
