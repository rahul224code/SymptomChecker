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
st.image(logo, width=150)
st.markdown("<h2 style='text-align: center; color: #4B8BBE; font-weight: bold;'>SymptomChecker</h2>", unsafe_allow_html=True)
st.caption("An AI-powered multilingual tool for safe OTC medicine suggestions")

# Language selector
lang = st.selectbox("Choose Language / भाषा चुनें / ভাষা বেছে নিন", ["English", "Hindi", "Bengali"])
lang_code = {"English": "English", "Hindi": "Hindi", "Bengali": "Bengali"}[lang]

# UI Text in multiple languages
ui_text = {
    "select_symptoms": {
        "English": "Select symptoms:",
        "Hindi": "लक्षण चुनें:",
        "Bengali": "উপসর্গ নির্বাচন করুন:"
    },
    "type_symptoms": {
        "English": "Or type your symptoms (comma-separated):",
        "Hindi": "या अपने लक्षण टाइप करें (कॉमा से अलग करें):",
        "Bengali": "অথবা আপনার উপসর্গ টাইপ করুন (কমা দিয়ে আলাদা করে):"
    },
    "check_button": {
        "English": "Check Suggestions",
        "Hindi": "सुझाव देखें",
        "Bengali": "সুপারিশ দেখুন"
    },
    "no_match": {
        "English": "No matching condition found. Try different symptoms.",
        "Hindi": "कोई मेल खाने वाली स्थिति नहीं मिली। कृपया अन्य लक्षण आज़माएं।",
        "Bengali": "কোনো মেলানো অবস্থা পাওয়া যায়নি। অনুগ্রহ করে ভিন্ন উপসর্গ চেষ্টা করুন।"
    },
    "declaration": {
        "English": "**Declaration:** This tool provides general guidance based on common symptoms. For emergencies or serious conditions, consult a licensed medical professional.",
        "Hindi": "**घोषणा:** यह टूल सामान्य लक्षणों के आधार पर सामान्य मार्गदर्शन प्रदान करता है। आपात स्थिति या गंभीर बीमारी में कृपया किसी प्रमाणित चिकित्सक से संपर्क करें।",
        "Bengali": "**ঘোষণা:** এই টুলটি সাধারণ উপসর্গের উপর ভিত্তি করে সাধারণ পরামর্শ প্রদান করে। জরুরি বা গুরুতর অবস্থার জন্য একজন লাইসেন্সপ্রাপ্ত চিকিৎসকের পরামর্শ নিন।"
    }
}

# Load data
data = load_data()

# Extract all symptoms in selected language
symptom_col = f"Symptoms ({lang_code})"
all_symptoms = set()
for symptoms in data[symptom_col]:
    all_symptoms.update([s.strip() for s in symptoms.split(";")])

# Show multiselect options and custom input
selected_symptoms = st.multiselect(ui_text["select_symptoms"][lang], sorted(all_symptoms))
custom_input = st.text_input(ui_text["type_symptoms"][lang])

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
if st.button(ui_text["check_button"][lang]):
    result_df = match_symptoms(final_symptoms, data, lang_code)

    if not result_df.empty:
        for _, row in result_df.iterrows():
            st.subheader(f"🩺 Possible Disease: {row[f'Possible Disease ({lang_code})']}")
            st.markdown(f"**💊 OTC Medications:** {row[f'OTC Medications ({lang_code})']}")
            st.markdown(f"**📋 Advice:** {row[f'Advice ({lang_code})']}")

    else:
        st.warning(ui_text["no_match"][lang])

st.markdown("---")
st.markdown(ui_text["declaration"][lang])
st.markdown("Made with ❤ by SymptomChecker")
