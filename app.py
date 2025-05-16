import streamlit as st
import pandas as pd
from PIL import Image
from googletrans import Translator

# Load logo
logo = Image.open("logo.png")

# Load data
@st.cache_data
def load_data():
    return pd.read_csv("symptom_disease_multilingual_30symptoms.csv")

# Translator setup
translator = Translator()

def translate(text, dest):
    try:
        return translator.translate(text, dest=dest).text
    except:
        return text

# UI config
st.set_page_config(page_title="SymptomChecker - AI-Based OTC Suggestion App", page_icon="⚕", layout="centered")
st.image(logo, width=100)
st.title("SymptomChecker")
st.caption("An AI-powered multilingual tool for safe OTC medicine suggestions")

# Language selector
lang = st.selectbox("Choose Language", ["English", "Hindi", "Bengali"])
lang_code = {"English": "English", "Hindi": "Hindi", "Bengali": "Bengali"}[lang]

# Load data
data = load_data()

# Extract all symptoms in selected language
symptom_col = f"Symptoms ({lang_code})"
all_symptoms = set()
for symptoms in data[symptom_col]:
    all_symptoms.update([s.strip() for s in symptoms.split(";")])

# Show multiselect options and custom input
selected_symptoms = st.multiselect(f"Select symptoms ({lang}):", sorted(all_symptoms))
custom_input = st.text_input("Or type your symptoms (comma-separated):")

# Merge selections
final_symptoms = set(selected_symptoms)
if custom_input:
    final_symptoms.update([s.strip() for s in custom_input.split(",")])

# Match logic
def match_symptoms(user_symptoms, df, lang_code):
    results = []
    for _, row in df.iterrows():
        known_symptoms = [s.strip().lower() for s in row[f"Symptoms ({lang_code})"].split(";")]
        if any(symptom.lower() in known_symptoms for symptom in user_symptoms):
            results.append(row)
    return pd.DataFrame(results)

# Show results
if st.button("Check Suggestions"):
    result_df = match_symptoms(final_symptoms, data, lang_code)

    if not result_df.empty:
        for _, row in result_df.iterrows():
            st.subheader(f"Possible Disease: {row[f'Possible Disease ({lang_code})']}")
            st.write(f"**OTC Medications:** {row[f'OTC Medications ({lang_code})']}")
            st.write(f"**Advice:** {row[f'Advice ({lang_code})']}")
            st.markdown("---")
    else:
        st.warning("No matching condition found. Try different symptoms.")

st.markdown("---")
st.markdown("**Declaration:** This tool provides general guidance based on common symptoms. For emergencies or serious conditions, consult a licensed medical professional.")
st.markdown("Made with ❤ by SymptomChecker")
