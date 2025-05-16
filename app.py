import streamlit as st
import pandas as pd
from PIL import Image
from googletrans import Translator
import os

# Load logo
if os.path.exists("logo.png"):
    logo = Image.open("logo.png")
else:
    logo = None

# Load data
@st.cache_data
def load_data():
    return pd.read_csv("symptom_disease_suggestions.csv")

def match_symptoms(user_symptoms, data):
    user_symptom_list = [s.strip().lower() for s in user_symptoms.split(",")]
    results = []
    for _, row in data.iterrows():
        known_symptoms = [s.strip().lower() for s in row["Symptoms"].split(";")]
        if any(symptom in known_symptoms for symptom in user_symptom_list):
            results.append(row)
    return pd.DataFrame(results)

# Translator setup
translator = Translator()

def translate(text, dest):
    try:
        return translator.translate(text, dest=dest).text
    except:
        return text

# UI config
st.set_page_config(page_title="SymptomChecker - AI-Based OTC Suggestion App", page_icon="⚕", layout="centered")
if logo:
    st.image(logo, width=100)
st.title("SymptomChecker")
st.caption("An AI-powered multilingual tool for safe OTC medicine suggestions")

# Language selector
lang = st.selectbox("Choose Language", ["English", "Hindi", "Bengali"])

# Language dictionary
translations = {
    "English": {
        "enter_symptoms": "Enter your symptoms (comma-separated):",
        "check": "Check Suggestions",
        "possible_disease": "Possible Disease:",
        "medications": "OTC Medications:",
        "advice": "Advice:",
        "no_match": "No matching condition found. Please try again with different symptoms."
    },
    "Hindi": {
        "enter_symptoms": "अपने लक्षण दर्ज करें (कॉमा से अलग करें):",
        "check": "सुझाव देखें",
        "possible_disease": "संभावित बीमारी:",
        "medications": "ओटीसी दवाएं:",
        "advice": "सलाह:",
        "no_match": "कोई मेल नहीं मिला। कृपया अलग लक्षणों के साथ पुनः प्रयास करें।"
    },
    "Bengali": {
        "enter_symptoms": "আপনার উপসর্গ লিখুন (কমা দিয়ে আলাদা করুন):",
        "check": "সুজ্ঞা দেখুন",
        "possible_disease": "সম্ভাব্য রোগ:",
        "medications": "ওটিসি ওষুধ:",
        "advice": "পরামর্শ:",
        "no_match": "মিল পাওয়া যায়নি। দয়া করে অন্য উপসর্গ দিয়ে চেষ্টা করুন।"
    }
}

# Input
user_input = st.text_input(translations[lang]["enter_symptoms"], "Fever, Cough")

if st.button(translations[lang]["check"]):
    data = load_data()
    result_df = match_symptoms(user_input, data)

    if not result_df.empty:
        for i, row in result_df.iterrows():
            st.subheader(f"{translations[lang]['possible_disease']} {translate(row['Possible Disease'], lang[:2])}")
            st.write(f"**{translations[lang]['medications']}** {translate(row['OTC Medications'], lang[:2])}")
            st.write(f"**{translations[lang]['advice']}** {translate(row['Advice'], lang[:2])}")
            st.markdown("---")
    else:
        st.warning(translations[lang]["no_match"])

st.markdown("---")
st.markdown("Made with ❤ by SymptomChecker")
