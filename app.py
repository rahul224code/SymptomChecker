import streamlit as st
import pandas as pd
from PIL import Image

# Load logo
logo = Image.open("logo.png")

# Load data
@st.cache_data

def load_data():
    return pd.read_csv("symptom_disease_suggestions_extended_v2.csv")

# Language dictionary
translations = {
    "English": {
        "enter_symptoms": "Enter your symptoms (comma-separated or select from below):",
        "select_symptoms": "Or select symptoms:",
        "check": "Check Suggestions",
        "possible_disease": "Possible Disease:",
        "medications": "OTC Medications:",
        "advice": "Advice:",
        "no_match": "No matching condition found. Please try again with different symptoms."
    },
    "Hindi": {
        "enter_symptoms": "अपने लक्षण दर्ज करें (कॉमा से अलग करें या नीचे से चुनें):",
        "select_symptoms": "या लक्षण चुनें:",
        "check": "सुझाव देखें",
        "possible_disease": "संभावित बीमारी:",
        "medications": "ओटीसी दवाएं:",
        "advice": "सलाह:",
        "no_match": "कोई मेल नहीं मिला। कृपया अलग लक्षणों के साथ पुनः प्रयास करें।"
    },
    "Bengali": {
        "enter_symptoms": "আপনার উপসর্গ লিখুন (কমা দিয়ে আলাদা করুন বা নিচে থেকে বেছে নিন):",
        "select_symptoms": "অথবা উপসর্গ বেছে নিন:",
        "check": "সুজ্ঞা দেখুন",
        "possible_disease": "সম্ভাব্য রোগ:",
        "medications": "ওটিসি ওষুধ:",
        "advice": "পরামর্শ:",
        "no_match": "মিল পাওয়া যায়নি। দয়া করে অন্য উপসর্গ দিয়ে চেষ্টা করুন।"
    }
}

# UI config
st.set_page_config(page_title="SymptomChecker - AI-Based OTC Suggestion App", page_icon="⚕", layout="centered")
st.image(logo, width=100)
st.title("SymptomChecker")
st.caption("An AI-powered multilingual tool for safe OTC medicine suggestions")

# Language selector
lang = st.selectbox("Choose Language", ["English", "Hindi", "Bengali"])

# Load data
data = load_data()

# Extract unique symptoms for multi-select
unique_symptoms = set()
for s in data["Symptoms"]:
    unique_symptoms.update([i.strip().capitalize() for i in s.split(";")])
sorted_symptoms = sorted(unique_symptoms)

# Input method
st.markdown(f"**{translations[lang]['enter_symptoms']}**")
text_input = st.text_input("", placeholder="e.g., Fever, Headache")
selected_symptoms = st.multiselect(translations[lang]['select_symptoms'], sorted_symptoms)

# Combine inputs
def get_combined_symptoms():
    combined = []
    if text_input:
        combined += [s.strip().lower() for s in text_input.split(",") if s.strip()]
    if selected_symptoms:
        combined += [s.strip().lower() for s in selected_symptoms if s.strip()]
    return list(set(combined))

# Match logic
def match_symptoms(user_symptoms, data):
    results = []
    for _, row in data.iterrows():
        known_symptoms = [s.strip().lower() for s in row["Symptoms"].split(";")]
        if any(symptom in known_symptoms for symptom in user_symptoms):
            results.append(row)
    return pd.DataFrame(results)

if st.button(translations[lang]["check"]):
    symptoms_list = get_combined_symptoms()
    result_df = match_symptoms(symptoms_list, data)

    if not result_df.empty:
        for _, row in result_df.iterrows():
            st.subheader(f"{translations[lang]['possible_disease']} {row[f'Possible Disease ({lang})']}")
            st.write(f"**{translations[lang]['medications']}** {row[f'OTC Medications ({lang})']}")
            st.write(f"**{translations[lang]['advice']}** {row[f'Advice ({lang})']}")
            st.markdown("---")
    else:
        st.warning(translations[lang]["no_match"])

st.markdown("---")
st.markdown("Made with ❤ by SymptomChecker")
