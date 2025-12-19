import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def show(df_raw):
    st.markdown("# ✅ Evaluation")
    st.markdown("*Evaluasi performa model forecasting*")
    st.markdown("---")
    
    st.markdown("""
    <div class='process-header'>
        <h3>📊 Metrik Evaluasi Model</h3>
        <p>Menggunakan berbagai metrik error untuk mengukur akurasi model forecasting.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Parameter
    with st.sidebar:
        st.markdown("---")
        st.markdown("### 📊 Parameter Evaluasi")
        alpha = st.slider("Alpha (α)", min_value=0.01, max_value=0.99, value=0.80, step=0.01, key="eval_alpha")
        periods_ahead = st.number_input("Periode Prediksi", min_value=1, max_value=20, value=5, key="eval_periods")
        
    # Display Data Info (To The Point)
    col1, col2 = st.columns(2)
    with col1:
        st.info("Data yang digunakan: **Income Inequality in South Africa** (Gini Disposible)")
    with col2:
        st.info(f"Model: **Double Exponential Smoothing (Brown)** | Alpha (α): **{alpha}**")

    # Perhitungan (Auto Run)
    # 1. Load & Clean Data (Konsisten dengan Data Understanding)
    df_clean = df_raw[['Year', 'gini_disp']].sort_values('Year').reset_index(drop=True)
    # Interpolasi untuk menangani missing values agar evaluasi bisa berjalan
    df_clean['gini_disp'] = df_clean['gini_disp'].interpolate(method='linear')
    df_clean = df_clean.dropna()

    Y = df_clean['gini_disp'].values.astype(float)
    years = df_clean['Year'].values.astype(int)
    n = len(Y)
    
    # Validasi Data (dari referensi)
    if n < 4:
        st.error("❌ Data tidak cukup untuk melakukan evaluasi. Minimal diperlukan 4 data points.")
        return

    # 2. DES Calculation (Brown) - Loop Manual sesuai referensi
    S1 = [Y[0]]
    S2 = [Y[0]]
    for t in range(1, n):
        S1.append(alpha * Y[t] + (1 - alpha) * S1[t-1])
        S2.append(alpha * S1[t] + (1 - alpha) * S2[t-1])
    
    a = [2 * S1[i] - S2[i] for i in range(n)]
    b = [((alpha / (1 - alpha)) * (S1[i] - S2[i])) if (1 - alpha) != 0 else 0.0 for i in range(n)]
    
    # 3. Forecast In-Sample
    forecast = [None]
    for i in range(1, n):
        forecast.append(a[i-1] + b[i-1])
    
    # 4. Error Calculation (Residual)
    error = [None]
    abs_error = [None]
    error2 = [None]
    
    for i in range(1, n):
        f = forecast[i]
        if f is not None:
            e = Y[i] - f
            error.append(e)
            abs_error.append(abs(e))
            error2.append(e**2)
    
    # 5. Evaluation Metrics
    valid_errors = [e for e in error if e is not None]
    valid_abs_errors = [e for e in abs_error if e is not None]
    valid_error2 = [e for e in error2 if e is not None]
    
    if not valid_errors: # Safety check
        st.error("Tidak ada data valid untuk menghitung error.")
        return

    MAE = np.mean(valid_abs_errors)
    MSE = np.mean(valid_error2)
    RMSE = np.sqrt(MSE)
    
    # MAPE Calculation (avoid zero division)
    valid_y_mape = [Y[i] for i in range(1, n) if Y[i] != 0 and abs_error[i] is not None]
    valid_abs_err_mape = [abs_error[i] for i in range(1, n) if Y[i] != 0 and abs_error[i] is not None]
    
    if len(valid_y_mape) > 0:
        MAPE = (np.mean(np.array(valid_abs_err_mape) / np.array(valid_y_mape)) * 100)
    else:
        MAPE = 0.0
    
    # Display Metrics (Result Focus)
    st.subheader("📊 Evaluation Result")
    
    cols = st.columns(4)
    with cols[0]:
        st.markdown(f"""
        <div class='metric-card'>
            <h3>{MAE:.4f}</h3>
            <p>MAE</p>
        </div>
        """, unsafe_allow_html=True)
    with cols[1]:
        st.markdown(f"""
        <div class='metric-card'>
            <h3>{MSE:.4f}</h3>
            <p>MSE</p>
        </div>
        """, unsafe_allow_html=True)
    with cols[2]:
        st.markdown(f"""
        <div class='metric-card'>
            <h3>{RMSE:.4f}</h3>
            <p>RMSE</p>
        </div>
        """, unsafe_allow_html=True)
    with cols[3]:
        mape_color = "🟢" if MAPE < 5 else "🟡" if MAPE < 10 else "🟠" if MAPE < 20 else "🔴"
        st.markdown(f"""
        <div class='metric-card'>
            <h3>{mape_color} {MAPE:.2f}%</h3>
            <p>MAPE</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    

    
    # Conclusion text similar to script output summary if needed
    st.markdown("---")
    st.code(f"""=== Summary Evaluation ===
Model  : Double Exponential Smoothing (Brown)
Alpha  : {alpha}
MAE    : {MAE:.4f}
MSE    : {MSE:.4f}
RMSE   : {RMSE:.4f}
MAPE   : {MAPE:.2f}%
    """, language="text")
