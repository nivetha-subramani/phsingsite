import streamlit as st
import numpy as np
import joblib
import warnings
from feature import FeatureExtraction

warnings.filterwarnings("ignore")

# Load model safely with Streamlit cache
@st.cache_resource
def load_model():
    try:
        # Load joblib model (resaved from pickle)
        model = joblib.load("pickle/model_v2.pkl")
    except:
        # Fallback if still using old pickle
        import pickle
        with open("pickle/model.pkl", "rb") as f:
            model = pickle.load(f)
    return model

gbc = load_model()

# Streamlit UI
st.set_page_config(page_title="Phishing URL Detection", page_icon="🔒", layout="centered")

st.markdown(
    """
    <h1 style="text-align:center; color:#FF5733;">🔒 Phishing URL Detection</h1>
    <p style="text-align:center; color:gray;">Enter a URL to check if it's safe or phishing</p>
    """,
    unsafe_allow_html=True,
)

url_input = st.text_input("🌐 Enter URL:")

if st.button("Check Safety"):
    if url_input:
        obj = FeatureExtraction(url_input)
        x = np.array(obj.getFeaturesList()).reshape(1, 30)

        y_pred = gbc.predict(x)[0]
        y_pro_phishing = gbc.predict_proba(x)[0, 0]
        y_pro_non_phishing = gbc.predict_proba(x)[0, 1]

        if y_pred == 1:
            st.success(f"✅ Safe Website with {y_pro_non_phishing*100:.2f}% confidence")
        else:
            st.error(f"⚠️ Phishing Website detected with {y_pro_phishing*100:.2f}% confidence")
    else:
        st.warning("Please enter a URL.")
