# app.py (Colorful Streamlit version)

import streamlit as st
import numpy as np
import pickle
from feature import FeatureExtraction

import os

file_path = os.path.join(os.path.dirname(__file__), "pickle", "model.pkl")
with open(file_path, "rb") as file:
    gbc = pickle.load(file)


# --- Page Config ---
st.set_page_config(page_title="Phishing URL Detector", page_icon="🔒", layout="centered")

# --- Custom CSS for Styling ---
st.markdown("""
    <style>
        body {
            background-color: #f5f7fa;
        }
        .title {
            color: #ffffff;
            text-align: center;
            padding: 15px;
            border-radius: 10px;
            background: linear-gradient(90deg, #4e54c8, #8f94fb);
            font-size: 32px;
        }
        .result-box {
            padding: 20px;
            border-radius: 12px;
            font-size: 20px;
            text-align: center;
            font-weight: bold;
        }
        .safe {
            background-color: #d4edda;
            color: #155724;
            border: 2px solid #28a745;
        }
        .phishing {
            background-color: #f8d7da;
            color: #721c24;
            border: 2px solid #dc3545;
        }
        .warning {
            background-color: #fff3cd;
            color: #856404;
            border: 2px solid #ffc107;
        }
    </style>
""", unsafe_allow_html=True)

# --- Title ---
st.markdown('<div class="title">🔒 Phishing URL Detection App</div>', unsafe_allow_html=True)
st.write("Enter a website URL below to check if it's **Safe** or **Phishing** 🚨")

# --- Input ---
url = st.text_input("🌐 Enter URL:")

if st.button("🔍 Check URL"):
    if url:
        obj = FeatureExtraction(url)
        x = np.array(obj.getFeaturesList()).reshape(1,30) 

        y_pred = gbc.predict(x)[0]
        y_pro_phishing = gbc.predict_proba(x)[0,0]
        y_pro_non_phishing = gbc.predict_proba(x)[0,1]

        if y_pred == 1:
            st.markdown(f'<div class="result-box safe">✅ Safe Website <br>Confidence: {y_pro_non_phishing*100:.2f}%</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="result-box phishing">⚠️ Phishing Website <br>Confidence: {y_pro_phishing*100:.2f}%</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="result-box warning">⚠️ Please enter a URL.</div>', unsafe_allow_html=True)
