import streamlit as st
import pandas as pd

def show(df_raw):
    st.markdown("# 💼 Business Understanding")
    st.markdown("*Memahami konteks bisnis dan tujuan proyek*")
    st.markdown("---")
    
    # david, business under - Redesigned UI
    st.markdown("""
    <div class='process-header'>
        <h3>📚 Metodologi CRISP-DM</h3>
        <p>Cross-Industry Standard Process for Data Mining</p>
    </div>
    """, unsafe_allow_html=True)

    # Definisi konten CRISP-DM (dari David)
    # Menggunakan layout 2 kolom untuk card
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class='info-card'>
            <h4>1. Business Understanding</h4>
            <p>Tahap awal yang bertujuan memahami permasalahan bisnis secara menyeluruh. Fokus utama adalah mengidentifikasi tujuan bisnis, permasalahan yang ingin diselesaikan, serta menentukan tujuan analisis data.</p>
            <p><strong>Output:</strong> Rumusan masalah yang jelas dan terukur.</p>
        </div>
        <br>
        <div class='info-card'>
            <h4>3. Data Preparation</h4>
            <p>Proses pengolahan data agar siap digunakan dalam pemodelan. Meliputi pembersihan data (cleaning), handling missing values, transformasi, dan normalisasi. Tahap ini sering memakan waktu paling lama (70-80% waktu proyek).</p>
            <p><strong>Output:</strong> Dataset akhir yang bersih dan terstruktur.</p>
        </div>
        <br>
        <div class='info-card'>
            <h4>5. Evaluation</h4>
            <p>Menilai kinerja model menggunakan metrik tertentu (MSE, MAPE, Akurasi) dan mengevaluasi apakah hasil model sudah menjawab permasalahan bisnis awal.</p>
            <p><strong>Output:</strong> Hasil evaluasi performa model dan keputusan deployment.</p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class='info-card'>
            <h4>2. Data Understanding</h4>
            <p>Memahami karakteristik data melalui pengumpulan dan eksplorasi awal. Mengidentifikasi struktur, pola, serta masalah kualitas data seperti missing values, outlier, atau inkonsistensi.</p>
            <p><strong>Output:</strong> Pemahaman mendalam tentang isi dan kualitas data.</p>
        </div>
        <br>
        <div class='info-card'>
            <h4>4. Modeling</h4>
            <p>Penerapan algoritma data science (seperti Forecasting, Klasifikasi, Regresi) pada data yang sudah disiapkan. Parameter model disesuaikan untuk mendapatkan performa terbaik.</p>
            <p><strong>Output:</strong> Model matematis yang dapat melakukan prediksi.</p>
        </div>
        <br>
        <div class='info-card'>
            <h4>6. Deployment</h4>
            <p>Penerapan model ke lingkungan nyata (produksi) agar dapat digunakan oleh pengguna akhir, misalnya dalam bentuk Dashboard atau Aplikasi Web.</p>
            <p><strong>Output:</strong> Aplikasi forecasting yang siap digunakan.</p>
        </div>
        """, unsafe_allow_html=True)
        
    st.markdown("<br>", unsafe_allow_html=True)
    st.info("Aplikasi ini mengimplementasikan keenam tahapan di atas secara berurutan, dimulai dari memahami konteks bisnis hingga deployment dalam bentuk dashboard interaktif ini.")
