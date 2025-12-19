import streamlit as st
import pandas as pd
import os

def load_css():
    st.markdown("""
    <style>
        .main {background-color: #0E1117; color: #E5E7EB;}
        .stApp {background-color: #0E1117;}
        h1, h2, h3, h4, h5, h6 {color: #00E396; font-weight: bold;}
        .stTextArea label, .stNumberInput label, .stSelectbox label, .stSlider label {color: #E5E7EB !important;}
        
        .metric-card {
            background: linear-gradient(135deg, #1e242f, #2a3244);
            padding: 20px;
            border-radius: 16px;
            box-shadow: 0 8px 25px rgba(0,0,0,0.6);
            text-align: center;
            border: 1px solid #334155;
        }
        
        .info-card {
            background: #1a202c;
            padding: 20px;
            border-radius: 12px;
            border-left: 5px solid #00E396;
            height: 100%;
        }
        
        .process-header {
            background: linear-gradient(135deg, #1e242f, #2a3244);
            padding: 25px;
            border-radius: 16px;
            border-left: 5px solid #00E396;
            margin-bottom: 20px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.4);
        }
        
        .process-step {
            background: #1a202c;
            padding: 20px;
            border-radius: 12px;
            border: 1px solid #334155;
            margin: 10px 0;
        }
        
        .highlight-box {
            background: rgba(0, 227, 150, 0.1);
            padding: 15px;
            border-radius: 10px;
            border: 1px solid #00E396;
            margin: 10px 0;
        }
        
        .step-number {
            background: #00E396;
            color: #0E1117;
            width: 30px;
            height: 30px;
            border-radius: 50%;
            display: inline-flex;
            align-items: center;
            justify-content: center;
            font-weight: bold;
            margin-right: 10px;
        }
        
        .stButton > button {
            background: #00E396 !important;
            color: black !important;
            font-weight: bold;
        }
        .stButton > button:hover {
            background: #00ffb8 !important;
        }
        .info-box {
            background: #1a202c;
            padding: 15px;
            border-radius: 10px;
            border-left: 4px solid #00E396;
            margin: 10px 0;
        }
    </style>
    """, unsafe_allow_html=True)

@st.cache_data
def load_data():
    # Construct absolute path to the dataset file relative to this utility script
    # Assuming main.py is in the parent directory and dataset is in the same directory as main.py
    # We need to go up one level from modules/utils.py to find the dataset
    script_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    file_path = os.path.join(script_dir, "Income Inequality in South Africa_Dataset.xlsx")
    
    if not os.path.exists(file_path):
        st.error(f"Dataset not found at: {file_path}")
        return pd.DataFrame() # Return empty DF to avoid crash

    df = pd.read_excel(file_path)
    df = df.sort_values(by='Year')
    return df
