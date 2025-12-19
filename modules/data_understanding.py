import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

def show(df_raw):
    st.markdown("# 🔍 Data Understanding")
    st.markdown("*Eksplorasi dan pemahaman karakteristik data*")
    st.markdown("---")
    
    # andi, data under - Redesigned UI based on dataunder_ineq.py
    
    # 1. Tampilkan 5 Data Teratas
    st.subheader("1. Sampel Data (Head)")
    st.dataframe(df_raw.head(5), use_container_width=True)
    
    # 2. Informasi Awal Data (df.info)
    st.subheader("2. Informasi Dataset")
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**Tipe Data & Null Count:**")
        info_df = pd.DataFrame({
            "Column": df_raw.columns,
            "Non-Null Count": df_raw.count(),
            "Dtype": df_raw.dtypes.astype(str)
        })
        st.dataframe(info_df, use_container_width=True)
        
    with col2:
         st.write("**Dimensi Data:**")
         st.info(f"Jumlah Baris: {df_raw.shape[0]}\n\nJumlah Kolom: {df_raw.shape[1]}")

    # 3. Statistik Deskriptif (df.describe)
    st.subheader("3. Statistik Deskriptif")
    st.dataframe(df_raw.describe(), use_container_width=True)
    
    st.markdown("---")
    
    # 4. Visualisasi Tren Time Series (EDA Utama)
    st.subheader("4. Visualisasi Tren Gini Disposible")
    
    # Dataset untuk forecasting (sesuai script)
    df_forecast = df_raw[['Year', 'gini_disp']].copy()
    
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.plot(df_forecast['Year'], df_forecast['gini_disp'], marker='o', color='#00E396', linewidth=2)
    ax.set_title("Trend Gini Disposable Income (South Africa)", color='white')
    ax.set_xlabel("Year", color='white')
    ax.set_ylabel("Gini Disposable Income", color='white')
    
    # Styling plot agar sesuai tema gelap
    ax.set_facecolor('#0E1117')
    fig.patch.set_facecolor('#0E1117')
    ax.tick_params(colors='white')
    ax.grid(True, alpha=0.3)
    st.pyplot(fig)
    
    st.markdown("---")
    
    # 5. Kualitas Data (Missing, Duplikasi, Outlier)
    st.subheader("5. Pengecekan Kualitas Data")
    
    # Fokus pada variabel utama
    df_q = df_raw[['Year', 'gini_disp']].copy()
    
    # Missing value
    missing_value = df_q['gini_disp'].isnull().sum()
    
    # Duplikasi data
    duplikasi = df_q.duplicated().sum()
    
    # Outlier (metode IQR sederhana)
    Q1 = df_q['gini_disp'].quantile(0.25)
    Q3 = df_q['gini_disp'].quantile(0.75)
    IQR = Q3 - Q1
    
    lower = Q1 - 1.5 * IQR
    upper = Q3 + 1.5 * IQR
    
    outlier = df_q[
        (df_q['gini_disp'] < lower) | (df_q['gini_disp'] > upper)
    ].shape[0]
    
    # Tabel ringkasan kualitas data
    quality_summary = pd.DataFrame({
        "Aspek Kualitas Data": ["Missing Value", "Duplikasi Data", "Outlier (IQR Method)"],
        "Jumlah": [missing_value, duplikasi, outlier]
    })
    
    st.write("**Rangkuman Kualitas Data:**")
    st.table(quality_summary) # Sesuai script yang pakai display() tabel sederhana
