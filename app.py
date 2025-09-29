# phishing site detection with Streamlit

import streamlit as st
import numpy as np
import pandas as pd
import joblib
import warnings
from feature import FeatureExtraction   # make sure feature.py is in the same folder

warnings.filterwarnings('ignore')

# Load model
@st.cache_resource
def load_model():
    return joblib.load("pickle/model.pkl")

gbc = load_model()

# Streamlit UI
st.set_page_config(page_title="Phishing Website Detector", page_icon="🛡️", layout="centered")

st.title("🛡️ Phishing Website Detection")
st.markdown(
    """
    Enter a website URL below and check if it is **Safe or Phishing**.
    """
)

# Input field
url = st.text_input("🔗 Enter Website URL:")

if st.button("Check"):
    if url.strip() == "":
        st.warning("⚠️ Please enter a valid URL.")
    else:
        try:
            obj = FeatureExtraction(url)
            x = np.array(obj.getFeaturesList()).reshape(1, 30)

            # Prediction
            y_pred = gbc.predict(x)[0]
            y_pro_phishing = gbc.predict_proba(x)[0, 0]
            y_pro_non_phishing = gbc.predict_proba(x)[0, 1]

            # Output with colors
            if y_pred == 1:
                st.success(f"✅ Safe Website! ({y_pro_non_phishing*100:.2f}% confidence)")
            else:
                st.error(f"🚨 Phishing Website Detected! ({y_pro_phishing*100:.2f}% confidence)")

        except Exception as e:
            st.error(f"❌ Error: {str(e)}")
