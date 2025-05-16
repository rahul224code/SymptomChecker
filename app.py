import streamlit as st
import pandas as pd
from PIL import Image
from googletrans import Translator
import os

# Load logo if exists
if os.path.exists("logo.png"):
    logo = Image.open("logo.png")
else:
    logo = None

# Load dataset
@st.cache_data
def load_data():
    return pd.read_csv("symptom_disease_suggestions.csv")

# Function to match symptoms
def match_symptoms(user_symptoms, data):
    user_symptom_list = [s.strip().lower() for s in user_symptoms if s.strip()]
    results = []
    for _, row in data.iterrows():
        known_symptoms = [s.strip().lower() for s in row["Symptoms"].split(";")]
        # Check if any user symptom is in known symptoms
        if any(symptom in known_symptoms for symptom in user_symptom_list):
            results.append(row)
    return pd.DataFrame(results)

# Setup translator
translator = Translator()

def translate(text, dest):
    try:
        return translator.translate(text, dest=dest).text
    except:
        return text

# Page config and header
st.set_page_config(page_title="SymptomChecker - AI-Based OTC Suggestion App", page_icon="⚕", layout="centered")
if logo:
    st.image(logo, width=100)
st.title("SymptomChecker")
st.caption("An AI-powered multilingual tool for safe OTC medicine suggestions")

# Load data
data = load_data()

# Extract all unique symptoms from dataset for multiselect
all_symptoms = set()
for s in data["Symptoms"]:
    parts = [sym.strip() for sym in s.split(";")]
    all_symptoms.update(parts)
all_symptoms = sorted(all_symptoms)

# Language selection
lang = st.selectbox("Choose Language", ["English", "Hindi", "Bengali"])

# Translations dictionary
translations = {
    "English": {
        "select_symptoms": "Select your symptoms (multiple):",
        "or_type": "Or type your symptoms (comma-separated):",
        "check": "Check Suggestions",
        "possible_disease": "Possible Disease:",
        "medications": "OTC Medications:",
        "advice": "Advice:",
        "no_match": "No matching condition found. Please try again with different symptoms."
    },
    "Hindi": {
        "select_symptoms": "अपने लक्षण चुनें (एक से अधिक):",
        "or_type": "या अपने लक्षण टाइप करें (कॉमा से अलग करें):",
        "check": "सुझाव देखें",
        "possible_disease": "संभावित बीमारी:",
        "medications": "ओटीसी दवाएं:",
        "advice": "सलाह:",
        "no_match": "कोई मेल नहीं मिला। कृपया अलग लक्षणों के साथ पुनः प्रयास करें।"
    },
    "Bengali": {
        "select_symptoms": "আপনার উপসর্গ নির্বাচন করুন (একাধিক):",
        "or_type": "অথবা আপনার উপসর্গ লিখুন (কমা দিয়ে আলাদা করুন):",
        "check": "সুজ্ঞা দেখুন",
        "possible_disease": "সম্ভাব্য রোগ:",
        "medications": "ওটিসি ওষুধ:",
        "advice": "পরামর্শ:",
        "no_match": "মিল পাওয়া যায়নি। দয়া করে অন্য উপসর্গ দিয়ে চেষ্টা করুন।"
    }
}

# User input: multiselect and text input
selected_symptoms = st.multiselect(translations[lang]["select_symptoms"], all_symptoms)
typed_symptoms = st.text_input(translations[lang]["or_type"])

# Combine symptoms list
typed_symptoms_list = [s.strip() for s in typed_symptoms.split(",") if s.strip()]
combined_symptoms = list(set(selected_symptoms + typed_symptoms_list))  # Remove duplicates

if st.button(translations[lang]["check"]):
    if combined_symptoms:
        result_df = match_symptoms(combined_symptoms, data)
        if not result_df.empty:
            for i, row in result_df.iterrows():
                st.subheader(f"{translations[lang]['possible_disease']} {translate(row['Possible Disease'], lang[:2])}")
                st.write(f"**{translations[lang]['medications']}** {translate(row['OTC Medications'], lang[:2])}")
                st.write(f"**{translations[lang]['advice']}** {translate(row['Advice'], lang[:2])}")
                st.markdown("---")
        else:
            st.warning(translations[lang]["no_match"])
    else:
        st.warning(translations[lang]["no_match"])

st.markdown("---")
st.markdown("Made with ❤ by SymptomChecker")
