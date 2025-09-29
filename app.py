# app.py
import streamlit as st
import numpy as np
import pandas as pd
import pickle
import warnings
from feature import FeatureExtraction

warnings.filterwarnings("ignore")

# Load the trained model
with open("pickle/model.pkl", "rb") as file:
    gbc = pickle.load(file)

# Streamlit app
st.set_page_config(page_title="Phishing URL Detector", page_icon="🔐", layout="centered")

st.markdown(
    "<h1 style='text-align: center; color: #FF4B4B;'>🔐 Phishing URL Detection</h1>",
    unsafe_allow_html=True,
)

# Input box
url = st.text_input("Enter the URL to check:")

if st.button("Check URL"):
    if url:
        # Extract features
        obj = FeatureExtraction(url)
        x = np.array(obj.getFeaturesList()).reshape(1, 30)

        # Prediction
        y_pred = gbc.predict(x)[0]
        y_pro_phishing = gbc.predict_proba(x)[0, 0]
        y_pro_non_phishing = gbc.predict_proba(x)[0, 1]

        # Show results with colors
        if y_pred == 1:
            st.success(f"✅ This URL looks SAFE with {y_pro_non_phishing*100:.2f}% confidence.")
        else:
            st.error(f"⚠️ This URL looks PHISHING with {y_pro_phishing*100:.2f}% confidence.")
    else:
        st.warning("⚠️ Please enter a valid URL.")
