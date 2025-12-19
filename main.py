import streamlit as st
from modules import utils, business_understanding, data_understanding, data_preparation, modeling, evaluation

# ====================== PAGE CONFIG & STYLE ======================
st.set_page_config(page_title="Income Inequality Forecast - CRISP-DM", layout="wide")
utils.load_css()

# ====================== LOAD DATA ======================
df_raw = utils.load_data()

# ====================== SIDEBAR NAVIGATION ======================
with st.sidebar:
    st.markdown("## 🧭 Navigasi CRISP-DM")
    st.markdown("---")
    
    menu = st.radio(
        "Pilih Proses:",
        [
            "💼 Business Understanding",
            "🔍 Data Understanding", 
            "🧹 Data Preparation",
            "🤖 Modeling",
            "✅ Evaluation"
        ],
        label_visibility="collapsed"
    )
    
    st.markdown("---")
    st.markdown("""
    <div style='padding: 15px; background: #1a202c; border-radius: 10px; border-left: 3px solid #00E396;'>
        <small style='color: #E5E7EB;'>
            <strong>CRISP-DM</strong><br>
            Cross-Industry Standard Process for Data Mining
        </small>
    </div>
    """, unsafe_allow_html=True)

# ====================== PAGE CONTENT ======================

if menu == "💼 Business Understanding":
    business_understanding.show(df_raw)

elif menu == "🔍 Data Understanding":
    data_understanding.show(df_raw)

elif menu == "🧹 Data Preparation":
    data_preparation.show(df_raw)

elif menu == "🤖 Modeling":
    modeling.show(df_raw)

elif menu == "✅ Evaluation":
    evaluation.show(df_raw)