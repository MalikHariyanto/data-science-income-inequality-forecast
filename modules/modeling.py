import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def show(df_raw):
    st.markdown("# Modeling")
    st.markdown("Tahap ini membahas pemodelan menggunakan Double Exponential Smoothing (Holt's Method) untuk memprediksi koefisien GINI berdasarkan data historis.")

    st.markdown("""
    <div class='process-header'>
        <h3>Double Exponential Smoothing</h3>
        <p>Metode peramalan untuk data deret waktu dengan tren linier.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # # Method Explanation
    # col1, col2 = st.columns(2)
    
    # with col1:
    #     st.markdown("""
    #     <div class='info-card'>
    #         <h4>Proses Perhitungan</h4>
    #         <p>Proses Double Exponential Smoothing (DES) terdiri dari dua tahap smoothing untuk menangkap komponen level dan tren pada data deret waktu. Setiap tahap perhitungan melibatkan pembaruan nilai level dan tren, yang kemudian digunakan untuk menghasilkan prediksi pada periode berikutnya.</p>
    #         <ul>
    #             <li><strong>Level (a):</strong> Nilai rata-rata yang dihaluskan</li>
    #             <li><strong>Trend (b):</strong> Arah perubahan data</li>
    #         </ul>
    #     </div>
    #     """, unsafe_allow_html=True)
    
    # with col2:
    #     st.markdown("""
    #     <div class='info-card'>
    #         <h4>Parameter Model</h4>
    #         <p><strong>Alpha (α):</strong> Faktor smoothing (0 < α < 1)</p>
    #         <ul>
    #             <li>α mendekati 0: smoothing lambat, hasil lebih stabil</li>
    #             <li>α mendekati 1: lebih responsif terhadap data terbaru</li>
    #         </ul>
    #         <p><strong>Rekomendasi:</strong> α = 0.1 - 0.3 untuk data yang relatif stabil</p>
    #     </div>
    #     """, unsafe_allow_html=True)
    
    # st.markdown("<br>", unsafe_allow_html=True)
    
    # Formulas
    st.subheader("Formula Double Exponential Smoothing")
    
    st.markdown("""
    <div class='highlight-box'>
        <strong>Single Exponential Smoothing (S'):</strong><br>
        <code>S't = α × Yt + (1 - α) × S't-1</code><br><br>
        <strong>Double Exponential Smoothing (S''):</strong><br>
        <code>S''t = α × S't + (1 - α) × S''t-1</code><br><br>
        <strong>Komponen Level (a):</strong><br>
        <code>at = 2 × S't - S''t</code><br><br>
        <strong>Komponen Trend (b):</strong><br>
        <code>bt = (α / (1 - α)) × (S't - S''t)</code><br><br>
        <strong>Forecast m periode ke depan:</strong><br>
        <code>Ft+m = at + bt × m</code>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Interactive Demo
    st.markdown("### Demo Perhitungan")
    
    with st.sidebar:
        st.markdown("---")
        st.markdown("### Parameter Model")
        alpha = st.slider("Alpha (α)", min_value=0.01, max_value=0.99, value=0.80, step=0.01)
        periods_ahead = st.number_input("Periode Prediksi", min_value=1, max_value=20, value=5)
        
        if st.button("Hitung Forecast", type="primary", use_container_width=True):
            st.session_state.calculate = True
    
    if st.session_state.get("calculate", False):
        # Perhitungan
        # Lakukan interpolasi agar time series tidak bolong
        df_clean = df_raw[['Year', 'gini_disp']].sort_values('Year').reset_index(drop=True)
        df_clean['gini_disp'] = df_clean['gini_disp'].interpolate(method='linear')
        df_clean = df_clean.dropna() # Drop rows yang masih NaN (misal di awal/akhir)

        Y = df_clean['gini_disp'].values.astype(float)
        years = df_clean['Year'].values.astype(int)
        n = len(Y)
        
        S1 = [Y[0]]
        S2 = [Y[0]]
        for t in range(1, n):
            S1.append(alpha * Y[t] + (1 - alpha) * S1[t-1])
            S2.append(alpha * S1[t] + (1 - alpha) * S2[t-1])

        a = [2 * S1[i] - S2[i] for i in range(n)]
        b = [(alpha / (1 - alpha)) * (S1[i] - S2[i]) for i in range(n)]

        # Forecast in-sample: forecast[0]=np.nan, forecast[i]=a[i-1]+b[i-1]
        forecast = [np.nan]
        for i in range(1, n):
            forecast.append(a[i-1] + b[i-1])

        # Extend forecast for future periods
        for m in range(1, periods_ahead + 1):
            future_forecast = a[-1] + b[-1] * m
            forecast.append(future_forecast)
        
        # Tabel Hasil

        st.markdown("#### Tabel Perhitungan")
        table_data = []
        for i in range(n):
            y_true = Y[i]
            y_pred = forecast[i]
            if i == 0 or np.isnan(y_pred):
                err = np.nan
                abs_err = np.nan
                sq_err = np.nan
                abs_pct_err = np.nan
            else:
                err = y_true - y_pred
                abs_err = abs(err)
                sq_err = err ** 2
                abs_pct_err = abs_err / y_true if y_true != 0 else np.nan
            table_data.append({
                "No": i + 1,
                "Tahun": int(years[i]),
                "Gini (Yt)": f"{y_true:.6f}",
                "S1": f"{S1[i]:.6f}",
                "S2": f"{S2[i]:.6f}",
                "a": f"{a[i]:.6f}",
                "b": f"{b[i]:.6f}",
                "Forecast": f"{y_pred:.6f}" if not np.isnan(y_pred) else "-",
                "Error": f"{err:.6f}" if not np.isnan(err) else "-",
                "Abs Error": f"{abs_err:.6f}" if not np.isnan(abs_err) else "-",
                "Error^2": f"{sq_err:.6f}" if not np.isnan(sq_err) else "-",
                "Abs Error/Actual": f"{abs_pct_err:.6f}" if not np.isnan(abs_pct_err) else "-",
            })
        st.dataframe(pd.DataFrame(table_data), use_container_width=True, hide_index=True)
        
        # Prediksi
        # surya, modeling grafik dan forecast periode tertentu
        future_years = [years[-1] + k + 1 for k in range(periods_ahead)]
        future_forecasts = [a[-1] + b[-1] * m for m in range(1, periods_ahead + 1)]
        
        st.markdown(f"#### Prediksi {periods_ahead} Tahun ke Depan")
        pred_df = pd.DataFrame({
            "Tahun": future_years,
            "Prediksi Gini": [f"{v:.4f}" for v in future_forecasts]
        })
        st.dataframe(pred_df, use_container_width=True, hide_index=True)
        
        # ========== GRAFIK VISUALISASI ==========
        st.markdown("<br>", unsafe_allow_html=True)
        st.subheader("Visualisasi: Aktual vs Forecast")
        
        fig, ax = plt.subplots(figsize=(12, 6))
        
        # Plot data aktual

        # Debug: Print lengths to diagnose error
        print(f"Length of years: {len(years)}")
        print(f"Length of forecast_clean: {len([f if f is not None else np.nan for f in forecast])}")

        ax.plot(years, Y, marker='o', label='Actual GINI', color='#00E396', linewidth=2, markersize=6)

        # Plot forecast in-sample
        forecast_clean = [f if f is not None else np.nan for f in forecast]
        # Ensure forecast_clean matches years length
        forecast_clean_plot = forecast_clean[:len(years)]
        ax.plot(years, forecast_clean_plot, marker='x', linestyle='--', label='Forecast (In-sample)', color='#00D1FF', linewidth=2)
        
        # Plot forecast future
        ax.plot(future_years, future_forecasts, marker='s', linestyle='--', label='Forecast (Future)', color='#FEB019', linewidth=2, markersize=8)
        
        # Garis pemisah
        ax.axvline(x=years[-1], color='#EF4444', linestyle=':', alpha=0.7, label='Cutoff')
        
        # Styling
        ax.set_xlabel('Year', fontsize=12, color='white')
        ax.set_ylabel('GINI Coefficient', fontsize=12, color='white')
        ax.set_title(f'Forecasting Gini Coefficient (α = {alpha})', fontsize=14, fontweight='bold', color='white')
        ax.set_facecolor('#0E1117')
        fig.patch.set_facecolor('#0E1117')
        ax.tick_params(colors='white')
        ax.legend(facecolor='#1a202c', edgecolor='#334155', labelcolor='white')
        ax.grid(True, alpha=0.3)
        
        st.pyplot(fig)
    else:
        st.info("Silakan atur parameter di sidebar dan klik 'Hitung Forecast' untuk melihat hasil perhitungan.")
