import streamlit as st
from google import genai
from fpdf import FPDF
import requests
import os
import re

# --- Page Setup ---
st.set_page_config(
    page_title="BAMS AI Study Companion",
    page_icon="🌿",
    layout="centered"
)

# --- API Key Configuration ---
api_key = st.secrets.get("GEMINI_API_KEY", "")

if not api_key:
    st.warning("⚠️ कृपया सुरू ठेवण्यासाठी तुमची Gemini API Key टाका (Settings > Secrets मध्ये जोडा).")
    st.stop()

client = genai.Client(api_key=api_key)

# --- Noto Sans Devanagari Font Setup ---
FONT_URL = "https://github.com/googlefonts/noto-fonts/raw/main/hinted/ttf/NotoSansDevanagari/NotoSansDevanagari-Regular.ttf"
FONT_PATH = "NotoSansDevanagari-Regular.ttf"

def ensure_font_downloaded():
    if not os.path.exists(FONT_PATH):
        response = requests.get(FONT_URL)
        with open(FONT_PATH, "wb") as f:
            f.write(response.content)

def clean_markdown_text(text):
    # Markdown चे साध्या स्वच्छ टेक्स्टमध्ये रूपांतर
    text = re.sub(r'\*\*(.*?)\*\*', r'\1', text)
    text = re.sub(r'\*(.*?)\*', r'\1', text)
    text = re.sub(r'^#+\s*', '', text, flags=re.MULTILINE)
    text = re.sub(r'^[-*]\s+', '• ', text, flags=re.MULTILINE)
    return text

def create_perfect_pdf(subject_name, topic_name, raw_content):
    ensure_font_downloaded()
    
    # FPDF क्लास इनिशिअलाइझ करतानाच text_shaping चालू करणे
    pdf = FPDF(text_shaping=True)
    pdf.add_font('Devanagari', '', FONT_PATH)
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    
    # Title Header
    pdf.set_font('Devanagari', size=14)
    pdf.cell(0, 10, '🌿 BAMS अभ्यास मार्गदर्शक', ln=True, align='C')
    pdf.set_font('Devanagari', size=10)
    pdf.cell(0, 8, f"विषय: {subject_name} | संकल्पना: {topic_name}", ln=True, align='C')
    pdf.line(10, 30, 200, 30)
    pdf.ln(5)
    
    # Body Content
    cleaned_body = clean_markdown_text(raw_content)
    pdf.set_font('Devanagari', size=10)
    pdf.multi_cell(0, 7, cleaned_body)
    
    return bytes(pdf.output())

# --- User Interface ---
st.title("🌿 BAMS AI अभ्यास मार्गदर्शक")
st.caption("आयुर्वेद संकल्पना, श्लोक अर्थ, मॉडर्न कोरिलेशन आणि परीक्षेसाठी परिपूर्ण नोट्स.")

subject = st.selectbox(
    "विषय निवडा (Subject):",
    [
        "Kriya Sharir (क्रिया शारीर)",
        "Rachana Sharir (रचना शारीर)",
        "Dravyaguna Vijnana (द्रव्यगुण विज्ञान)",
        "Roga Nidan & Vikriti Vigyan (रोगनिदान)",
        "Samhita Siddhant & Charak Samhita (संहिता सिद्धांत)",
        "Kayachikitsa (कायचिकित्सा)",
        "Shalya Tantra (शल्य तंत्र)",
        "Agada Tantra & Vyavahara Ayurveda (अगद तंत्र)"
    ]
)

topic = st.text_input(
    "अभ्यासाचा विषय / प्रश्न टाका:",
    placeholder="उदा. Pitta Dosha types and functions किंवा Ashwagandha properties"
)

language_preference = st.radio(
    "नोट्सचे माध्यम:",
    ["मराठी (सोपी आणि सुटसुटीत)", "English + Sanskrit terms"],
    horizontal=True
)

if st.button("📝 अभ्यास नोट्स तयार करा", type="primary"):
    if not topic.strip():
        st.error("कृपया विषयाचे नाव प्रविष्ट करा.")
    else:
        with st.spinner("AI शिक्षक तुमच्यासाठी सुटसुटीत पॉईंट वाईज नोट्स तयार करत आहे..."):
            try:
                system_instruction = f"""
                You are a senior Ayurveda Professor and BAMS Exam Expert.
                Subject: {subject}
                Topic: {topic}
                Language: {language_preference}

                Create clean, high-yield, exam-oriented revision notes following these strict rules:
                1. Write in clear, natural Marathi with correct Sanskrit terminology.
                2. Use clean bullet points (•) and numbered steps. Do NOT use markdown tables or weird symbols.
                3. Structure the notes strictly into:
                   १. व्याख्या आणि संदर्भ श्लोक (Definition & Reference Shloka with simple line meaning)
                   २. गुण, कर्म आणि प्रकार (Guna, Karma & Types in clear bullet points)
                   ३. आधुनिक वैद्यकशास्त्राशी तुलना (Modern Medical Correlation)
                   ४. परीक्षेसाठी महत्त्वाचे मुद्दे (High-Yield Exam Points & Viva Tips)
                """
                
                response = client.models.generate_content(
                    model='models/gemini-3.6-flash',
                    contents=system_instruction
                )
                
                notes_text = response.text
                st.success("✅ सुटसुटीत नोट्स तयार झाल्या आहेत!")
                st.markdown(notes_text)
                
                pdf_bytes = create_perfect_pdf(subject, topic, notes_text)
                st.download_button(
                    label="📥 थेट PDF डाऊनलोड करा (.pdf)",
                    data=pdf_bytes,
                    file_name=f"{topic.replace(' ', '_')}_BAMS_Notes.pdf",
                    mime="application/pdf"
                )
            except Exception as e:
                st.error(f"त्रुटी आली: {e}")
