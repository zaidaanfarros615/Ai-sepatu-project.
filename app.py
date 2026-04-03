import streamlit as st
import pandas as pd

# Judul Utama Website
st.set_page_config(page_title="NORYZE SISTEM ALAS KAKI", layout="wide")
st.title("👟 NORYZE Sistem Alas Kaki")
st.markdown("---")

# Bagian Input di Samping (Sidebar)
st.sidebar.header("🛠️ Pengaturan Grading")
jenis = st.sidebar.selectbox("Jenis Sepatu", ["SNEAKER", "BOOTS", "OXFORD"])
panjang_ref = st.sidebar.number_input("Panjang Pola Asli (cm)", value=25.0)
lebar_ref = st.sidebar.number_input("Lebar Pola Asli (cm)", value=10.0)
size_master = st.sidebar.number_input("Ukuran Master", value=38)

st.sidebar.subheader("Rentang Ukuran")
size_min = st.sidebar.number_input("Terkecil", value=36)
size_max = st.sidebar.number_input("Terbesar", value=42)

# Tombol Eksekusi
if st.button("🚀 PROSES GRADING SEKARANG"):
    with st.spinner('Menghitung...'):
        data_grading = []
        for size in range(int(size_min), int(size_max) + 1):
            selisih = size - size_master
            # Rumus standar grading (0.66 cm per nomor)
            p_baru = panjang_ref + (selisih * 0.66)
            l_baru = lebar_ref + (selisih * (0.66 * 0.4))
            
            data_grading.append({
                "Nomor": size,
                "Panjang (cm)": round(p_baru, 2),
                "Lebar (cm)": round(l_baru, 2),
                "Status": "MASTER" if size == size_master else "HASIL"
            })
            
        st.success("✅ Berhasil Dihitung!")
        
        # Kolom Tampilan: Kiri untuk Tabel, Kanan untuk Visual
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.subheader("📊 Tabel Ukuran")
            df = pd.DataFrame(data_grading)
            st.table(df)
            
            # Tombol Download
            csv = df.to_csv(index=False).encode('utf-8')
            st.download_button("⬇️ Download Data CSV", data=csv, file_name='noryze_grading.csv')

        with col2:
            st.subheader("📐 Visual Perbandingan")
            # Membuat kotak sederhana untuk visualisasi skala
            for d in data_grading:
                label = f"Size {d['Nomor']}"
                # Skala diperkecil agar pas di layar
                width = d['Lebar (cm)'] * 5
                height = d['Panjang (cm)'] * 5
                color = "#4CAF50" if d['Status'] == "MASTER" else "#2196F3"
                
                st.write(f"{label}: {d['Panjang (cm)']} x {d['Lebar (cm)']} cm")
                st.markdown(
                    f'<div style="width:{width}px; height:{height}px; background-color:{color}; border:1px solid white; margin-bottom:10px; border-radius:5px;"></div>', 
                    unsafe_allow_html=True
                )

st.markdown("---")
st.info("💡 Warna hijau adalah Ukuran Master, warna biru adalah hasil Grading.")
st.write("Dibuat untuk Noryze Sistem Alas Kaki")
