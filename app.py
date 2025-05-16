import streamlit as st
import pandas as pd
from PIL import Image
import os

# Load logo if exists
if os.path.exists("logo.png"):
    logo = Image.open("logo.png")
else:
    logo = None

# Load data
@st.cache_data
def load_data():
    return pd.read_csv("symptom_disease_suggestions.csv")

def match_symptoms(user_symptoms, data):
    user_symptom_list = [s.strip().lower() for s in user_symptoms if s.strip()]
    results = []
    for _, row in data.iterrows():
        known_symptoms = [s.strip().lower() for s in row["Symptoms"].split(";")]
        if any(symptom in known_symptoms for symptom in user_symptom_list):
            results.append(row)
    return pd.DataFrame(results)

# UI config
st.set_page_config(page_title="SymptomChecker - AI-Based OTC Suggestion App", page_icon="⚕", layout="centered")

if logo:
    st.image(logo, width=100)
st.title("SymptomChecker")
st.caption("An AI-powered multilingual tool for safe OTC medicine suggestions")

data = load_data()

# Extract all unique symptoms for multiselect
all_symptoms = set()
for s in data["Symptoms"]:
    all_symptoms.update([sym.strip() for sym in s.split(";")])
all_symptoms = sorted(all_symptoms)

# Language selection
lang = st.selectbox("Choose Language / भाषा चुनें / ভাষা নির্বাচন করুন", ["English", "Hindi", "Bengali"])

# Translation dictionary
translations = {
    "English": {
        "select_symptoms": "Select your symptoms (multiple):",
        "or_type": "Or type your symptoms (comma-separated):",
        "check": "Check Suggestions",
        "possible_disease": "Possible Disease:",
        "medications": "OTC Medications:",
        "advice": "Advice:",
        "no_match": "No matching condition found. Please try different symptoms."
    },
    "Hindi": {
        "select_symptoms": "अपने लक्षण चुनें (एक से अधिक):",
        "or_type": "या अपने लक्षण टाइप करें (कॉमा से अलग करें):",
        "check": "सुझाव देखें",
        "possible_disease": "संभावित बीमारी:",
        "medications": "ओटीसी दवाएं:",
        "advice": "सलाह:",
        "no_match": "कोई मेल नहीं मिला। कृपया अलग लक्षणों से पुनः प्रयास करें।"
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

# Inputs
selected_symptoms = st.multiselect(translations[lang]["select_symptoms"], all_symptoms)
typed_symptoms = st.text_input(translations[lang]["or_type"])

# Combine symptoms
typed_symptoms_list = [s.strip() for s in typed_symptoms.split(",") if s.strip()]
combined_symptoms = list(set(selected_symptoms + typed_symptoms_list))  # remove duplicates

if st.button(translations[lang]["check"]):
    if combined_symptoms:
        results = match_symptoms(combined_symptoms, data)
        if not results.empty:
            for _, row in results.iterrows():
                disease_col = f"Possible Disease ({lang})"
                med_col = f"OTC Medications ({lang})"
                advice_col = f"Advice ({lang})"
                
                st.subheader(f"{translations[lang]['possible_disease']} {row[disease_col]}")
                st.write(f"**{translations[lang]['medications']}** {row[med_col]}")
                st.write(f"**{translations[lang]['advice']}** {row[advice_col]}")
                st.markdown("---")
        else:
            st.warning(translations[lang]["no_match"])
    else:
        st.warning(translations[lang]["no_match"])

st.markdown("---")
st.markdown("Made with ❤ by SymptomChecker")
