import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

def show(df_raw):
    # safii, data preparation
    st.markdown("# 🧹 Data Preparation")
    st.markdown("*Data Cleaning, Transformation, dan Exploration untuk Income Inequality South Africa*")
    st.markdown("---")
    
    # Load data original untuk perbandingan
    df_original = df_raw.copy()
    
    # ========== STEP 1: Data Loading & Initial Exploration ==========
    st.markdown("## 📥 STEP 1: Data Loading & Initial Exploration")
    
    st.markdown("""
    <div class='highlight-box'>
        <strong>📌 Penjelasan Step 1:</strong><br>
        ✓ Membaca file Excel yang berisi data Income Inequality South Africa<br>
        ✓ Menyimpan copy original untuk perbandingan sebelum vs sesudah preprocessing
    </div>
    """, unsafe_allow_html=True)
    
    # Display data info metrics
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f"""
        <div class='metric-card'>
            <h3>{df_original.shape[0]}</h3>
            <p>Total Rows</p>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
        <div class='metric-card'>
            <h3>{df_original.shape[1]}</h3>
            <p>Total Columns</p>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown(f"""
        <div class='metric-card'>
            <h3>{df_original.isnull().sum().sum()}</h3>
            <p>Missing Values</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Preview data
    st.subheader("Data Preview (First 5 Rows)")
    st.dataframe(df_original.head(), use_container_width=True)
    
    # Data Info dengan Tabs
    st.subheader("Data Information")
    tabs1 = st.tabs(["📊 Data Types", "📈 Summary Statistics", "❓ Missing Values"])
    
    with tabs1[0]:
        st.write("**Column Data Types:**")
        info_df = pd.DataFrame({
            "Column": df_original.columns,
            "Data Type": df_original.dtypes.astype(str),
            # "Non-Null Count": df_original.count(),
            # "Null Count": df_original.isnull().sum()
        })
        st.dataframe(info_df, use_container_width=True, hide_index=True)
    
    with tabs1[1]:
        st.write("**Summary Statistics (Descriptive):**")
        st.dataframe(df_original.describe(), use_container_width=True)
    
    with tabs1[2]:
        st.write("**Missing Values per Column:**")
        missing_df = pd.DataFrame({
            "Column": df_original.columns,
            "Missing Count": df_original.isnull().sum(),
            "Missing %": (df_original.isnull().sum() / len(df_original) * 100).round(2)
        })
        missing_with_values = missing_df[missing_df["Missing Count"] > 0]
        if len(missing_with_values) > 0:
            st.dataframe(missing_with_values, use_container_width=True, hide_index=True)
        else:
            st.success("✅ Tidak ada missing values!")
    
    # View Full Dataset
    with st.expander("📊 View Full Dataset"):
        st.dataframe(df_original, use_container_width=True, hide_index=True)
    
    st.markdown("---")
    
    # ========== STEP 2: Data Sorting & Interpolation ==========
    st.markdown("## 🔧 STEP 2: Data Sorting & Interpolation")
    
    st.markdown("""
    <div class='highlight-box'>
        <strong>📌 Penjelasan Step 2:</strong><br>
        ✓ Mengurutkan data berdasarkan Year (wajib untuk time series interpolation)<br>
        ✓ Mengidentifikasi kolom numerik (menghilangkan Year dari daftar interpolasi)<br>
        ✓ Melakukan Linear Interpolation untuk mengisi missing values dengan nilai yang proporsional antara dua data terdekat<br>
        ✓ Linear Interpolation cocok karena trend data yang smooth dan consistent
    </div>
    """, unsafe_allow_html=True)
    
    # Sort dan Interpolasi
    df_clean = df_original.sort_values(by='Year').reset_index(drop=True)
    
    # Ambil kolom numerik selain Year
    numeric_cols = df_clean.select_dtypes(include='number').columns.tolist()
    if 'Year' in numeric_cols:
        numeric_cols.remove('Year')
    
    # Lakukan interpolasi
    for col in numeric_cols:
        df_clean[col] = df_clean[col].interpolate(method='linear')
    
    st.success("✅ Data telah disort berdasarkan Year dan dilakukan interpolasi linear")
    
    # Tampilkan hasil interpolasi
    st.subheader("Data Setelah Interpolasi")
    col1, col2 = st.columns(2)
    with col1:
        st.write("**Missing Values Sebelum Interpolasi:**")
        st.dataframe(df_original.isnull().sum(), use_container_width=True)
    with col2:
        st.write("**Missing Values Sesudah Interpolasi:**")
        st.dataframe(df_clean.isnull().sum(), use_container_width=True)
    
    st.markdown("---")
    
    # ========== STEP 3: Visualisasi Interpolasi ==========
    st.markdown("## 📈 STEP 3: Visualisasi Interpolasi - Before vs After")
    
    st.markdown("""
    <div class='highlight-box'>
        <strong>📌 Penjelasan Step 3:</strong><br>
        ✓ Membandingkan visualisasi data SEBELUM interpolasi (dengan missing values) vs SESUDAH<br>
        ✓ Garis merah (before) menunjukkan data asli dengan gaps pada missing values<br>
        ✓ Garis hijau (after) menunjukkan hasil interpolasi yang smooth dan continuous<br>
        ✓ Membantu kita mengidentifikasi apakah interpolasi dilakukan dengan tepat
    </div>
    """, unsafe_allow_html=True)
    
    # Pilih kolom untuk visualisasi interpolasi
    selected_col_interp = st.selectbox("Pilih Kolom untuk Visualisasi Interpolasi:", numeric_cols)
    
    fig, ax = plt.subplots(figsize=(12, 5))
    
    # Plot sebelum interpolasi (original dengan missing values)
    ax.plot(df_original['Year'], df_original[selected_col_interp],
            'o-', color='#EF4444', label='Before (Raw Data)', alpha=0.7, linewidth=2, markersize=8)
    
    # Plot sesudah interpolasi
    ax.plot(df_clean['Year'], df_clean[selected_col_interp],
            '-', color='#00E396', label='After Interpolation', linewidth=2.5)
    
    ax.set_title(f"Perbandingan Interpolasi: {selected_col_interp}", fontsize=14, fontweight='bold', color='white')
    ax.set_xlabel("Year", fontsize=12, color='white')
    ax.set_ylabel(selected_col_interp, fontsize=12, color='white')
    ax.set_facecolor('#0E1117')
    fig.patch.set_facecolor('#0E1117')
    ax.tick_params(colors='white')
    ax.grid(True, alpha=0.3)
    ax.legend(facecolor='#1a202c', edgecolor='#334155', labelcolor='white')
    plt.tight_layout()
    
    st.pyplot(fig)
    
    st.markdown("---")

    # ========== STEP: Stationarity Test (ADF) - Added from Reference ==========

    # ========== STEP 4: Boxplot Visualisasi Kolom Numerik ========== 
    st.markdown("## 📊 STEP 4: Boxplot Kolom Numerik")
    st.markdown("""
    <div class='highlight-box'>
        <strong>📌 Penjelasan Step 4:</strong><br>
        ✓ Visualisasi distribusi dan deteksi outlier pada setiap kolom numerik (kecuali 'Year') menggunakan boxplot.<br>
        ✓ Membantu memahami sebaran data dan potensi nilai ekstrim/outlier.<br>
    </div>
    """, unsafe_allow_html=True)

    # Pilih kolom numerik kecuali 'Year'
    numeric_cols = df_clean.select_dtypes(include='number').columns
    numeric_cols = [col for col in numeric_cols if col.lower() != "year"]

    # Loop kolom dan buat boxplot satu-satu
    for col in numeric_cols:
        fig, ax = plt.subplots(figsize=(10, 7))
        ax.boxplot(df_clean[col].dropna())
        ax.set_title(f"Boxplot {col}")
        ax.set_ylabel(col)
        ax.set_xticks([1])
        ax.set_xticklabels([col])
        ax.grid(True)
        st.pyplot(fig)

    st.markdown("---")
    
    # ========== STEP 4: Column Selection & Filtering ==========
    st.markdown("## 🎯 STEP 4: Column Selection & Filtering")
    
    st.markdown("""
    <div class='highlight-box'>
        <strong>📌 Penjelasan Step 4:</strong><br>
        ✓ Memilih kolom yang relevan untuk analisis forecasting dan machine learning<br>
        ✓ Menghilangkan kolom yang tidak diperlukan (noise reduction)<br>
        ✓ Fokus pada variabel yang berkaitan dengan income inequality dan faktor-faktor ekonomi<br>
        ✓ Kolom yang dipilih harus memiliki data berkualitas dan tidak terlalu banyak missing values
    </div>
    """, unsafe_allow_html=True)
    
    # Define selected columns - hanya kolom yang tersedia di dataset
    available_cols = df_clean.columns.tolist()
    selected_cols = ['Year', 'gini_disp']
    
    # Tambahkan kolom lain jika ada
    optional_cols = ['gini_mkt', 'Inflation rate', 'GDP', 'GOVEDU', 'GOVEXP', 'FINDEV 1', 'DEMOCRACY', 'FLABOUR']
    for col in optional_cols:
        if col in available_cols:
            selected_cols.append(col)
    
    # Filter dataframe
    df_filtered = df_clean[selected_cols].copy()
    
    st.subheader("Kolom yang Dipilih untuk Analisis")
    col_descriptions = {
        'Year': 'Tahun pengamatan',
        'gini_disp': 'Gini Coefficient (Disposable Income) - TARGET VARIABLE',
        'gini_mkt': 'Gini Coefficient (Market Income)',
        'Inflation rate': 'Inflation rate (%)',
        'GDP': 'Gross Domestic Product',
        'GOVEDU': 'Government Education Spending',
        'GOVEXP': 'Government Expenditure',
        'FINDEV 1': 'Financial Development Index',
        'DEMOCRACY': 'Democracy Index',
        'FLABOUR': 'Labour Force Participation'
    }
    
    col_info = pd.DataFrame({
        "No": range(1, len(selected_cols) + 1),
        "Kolom": selected_cols,
        "Deskripsi": [col_descriptions.get(col, col) for col in selected_cols]
    })
    st.dataframe(col_info, use_container_width=True, hide_index=True)
    
    st.subheader("Data Hasil Filtering")
    st.dataframe(df_filtered, use_container_width=True, hide_index=True)
    
    # Summary Statistics
    st.subheader("📊 Summary Statistik Filtered Data")
    st.dataframe(df_filtered.describe(), use_container_width=True)
    
    st.markdown("---")
    
    # ========== Summary ==========
    st.markdown("## ✅ Data Preparation Complete!")
    
    st.markdown(f"""
    <div class='highlight-box'>
        <strong>📊 Ringkasan Proses:</strong><br><br>
        ✓ Dari <strong>{df_original.shape[0]}</strong> baris, <strong>{df_original.shape[1]}</strong> kolom awal<br>
        ✓ Setelah filtering: <strong>{df_filtered.shape[0]}</strong> baris, <strong>{df_filtered.shape[1]}</strong> kolom<br>
        ✓ Missing values telah diatasi dengan interpolasi linear<br>
        ✓ Data siap untuk Modeling dan Evaluation
    </div>
    """, unsafe_allow_html=True)

