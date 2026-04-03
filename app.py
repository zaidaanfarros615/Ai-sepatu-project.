import streamlit as st
import cv2
import numpy as np
from PIL import Image
import io

# --- KONFIGURASI HALAMAN ---
st.set_page_config(page_title="AI Design Assistant", layout="wide")

# --- CUSTOM CSS (Sangat Mirip dengan Gambar Referensi) ---
st.markdown("""
    <style>
    .stApp { background-color: #0c0c0c; color: white; }
    h1, h2, h3 { font-family: 'Inter', sans-serif; color: white !important; }
    .purple-text { color: #a855f7; font-weight: bold; }
    .card {
        background-color: #161616;
        border: 1px solid #262626;
        padding: 2rem;
        border-radius: 20px;
    }
    .stButton>button {
        background: linear-gradient(135deg, #a855f7 0%, #6d28d9 100%);
        color: white; border: none; border-radius: 10px; width: 100%;
    }
    .upload-box {
        border: 2px dashed #a855f7;
        padding: 20px;
        border-radius: 15px;
        text-align: center;
    }
    </style>
    """, unsafe_allow_html=True)

# --- HERO SECTION ---
st.markdown('<h1 style="text-align: center;">AI <span class="purple-text">Vision</span> Assistant</h1>', unsafe_allow_html=True)
st.markdown('<p style="text-align: center; color: #888;">Transform your images with AI Edge Detection technology based on your Python script.</p>', unsafe_allow_html=True)
st.write("---")

# --- MAIN CONTENT (Kemampuan dari File Anda) ---
col1, col2 = st.columns([1, 1], gap="large")

with col1:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<h3><span class="purple-text">1.</span> Upload Image</h3>', unsafe_allow_html=True)
    uploaded_file = st.file_uploader("Pilih gambar (JPG/PNG)", type=['jpg', 'jpeg', 'png'])
    
    # Slider untuk parameter Canny (Logika dari script Anda)
    st.markdown('<h3><span class="purple-text">2.</span> AI Parameters</h3>', unsafe_allow_html=True)
    low_threshold = st.slider("Low Threshold", 0, 255, 100)
    high_threshold = st.slider("High Threshold", 0, 255, 200)
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    if uploaded_file is not None:
        # Load Gambar
        image = Image.open(uploaded_file)
        img_array = np.array(image)
        
        # Logika Pemrosesan (Sesuai salinan_dari_untitled3.py)
        # Mengonversi ke Grayscale lalu Edge Detection
        gray = cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY)
        edges = cv2.Canny(gray, low_threshold, high_threshold)
        
        st.markdown('<h3>Processing <span class="purple-text">Result</span></h3>', unsafe_allow_html=True)
        st.image(edges, caption="AI Generated Edge Detection", use_column_width=True, clamp=True)
        
        # Tombol Download
        result_img = Image.fromarray(edges)
        buf = io.BytesIO()
        result_img.save(buf, format="PNG")
        st.download_button("Download Result", buf.getvalue(), "ai_design_result.png", "image/png")
    else:
        st.markdown('<div style="height: 300px; display: flex; align-items: center; justify-content: center; background: #161616; border-radius: 20px; border: 1px solid #262626;">', unsafe_allow_html=True)
        st.write("Awaiting image upload...")
        st.markdown('</div>', unsafe_allow_html=True)

# --- PRICING SECTION (Visual Only) ---
st.write("---")
st.markdown('<h2 style="text-align:center">Affordable <span class="purple-text">Plans</span></h2>', unsafe_allow_html=True)
p1, p2, p3 = st.columns(3)

plans = [
    {"name": "Free", "price": "$0", "features": ["Basic Detection", "5 Daily Exports"]},
    {"name": "Pro", "price": "$15", "features": ["Advanced AI", "Unlimited Exports", "Priority Support"]},
    {"name": "Enterprise", "price": "$49", "features": ["Custom API", "Batch Processing", "Dedicated Server"]}
]

for i, p in enumerate(plans):
    with [p1, p2, p3][i]:
        # Memberikan efek warna ungu pada kartu tengah (Pro)
        style = 'style="background: linear-gradient(135deg, #a855f7 0%, #6d28d9 100%);"' if p['name'] == "Pro" else 'class="card"'
        st.markdown(f"""
            <div {style if p['name'] == "Pro" else 'class="card"'}>
                <small>{p['name'].upper()}</small>
                <h2>{p['price']}<span style="font-size: 15px;">/mo</span></h2>
                <ul style="color: {'white' if p['name'] == 'Pro' else '#888'}; font-size: 14px;">
                    {"".join([f"<li>✓ {f}</li>" for f in p['features']])}
                </ul>
            </div>
        """, unsafe_allow_html=True)
