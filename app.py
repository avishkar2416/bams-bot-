import streamlit as st
from google import genai
from fpdf import FPDF
import requests
import os

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

# --- Noto Sans Devanagari Font Download for Marathi PDF ---
FONT_URL = "https://github.com/googlefonts/noto-fonts/raw/main/hinted/ttf/NotoSansDevanagari/NotoSansDevanagari-Regular.ttf"
FONT_PATH = "NotoSansDevanagari-Regular.ttf"

def ensure_font_downloaded():
    if not os.path.exists(FONT_PATH):
        response = requests.get(FONT_URL)
        with open(FONT_PATH, "wb") as f:
            f.write(response.content)

# --- PDF Generation Class ---
class BAMSNotesPDF(FPDF):
    def header(self):
        self.set_font('Devanagari', size=14)
        self.cell(0, 10, 'BAMS Study Notes | अभ्यास मार्गदर्शक', border=False, ln=True, align='C')
        self.line(10, 20, 200, 20)
        self.ln(6)

    def footer(self):
        self.set_y(-15)
        self.set_font('Devanagari', size=8)
        self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')

def create_pdf(subject_name, topic_name, content):
    ensure_font_downloaded()
    pdf = BAMSNotesPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_font('Devanagari', '', FONT_PATH, uni=True)
    
    # Header Details
    pdf.set_font('Devanagari', size=11)
    pdf.cell(0, 8, f"विषय (Subject): {subject_name}", ln=True)
    pdf.cell(0, 8, f"संकल्पना (Topic): {topic_name}", ln=True)
    pdf.ln(3)
    
    # Body
    pdf.set_font('Devanagari', size=10)
    pdf.multi_cell(0, 7, content)
    return bytes(pdf.output())

# --- User Interface ---
st.title("🌿 BAMS AI अभ्यास मार्गदर्शक")
st.caption("आयुर्वेद संकल्पना, श्लोक अर्थ, मॉडर्न कोरिलेशन आणि परीक्षेसाठी नोट्स.")

# विषय निवड
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
    ["मराठी + Sanskrit/English terms", "English + Sanskrit terms"],
    horizontal=True
)

if st.button("📝 अभ्यास नोट्स तयार करा", type="primary"):
    if not topic.strip():
        st.error("कृपया विषयाचे नाव प्रविष्ट करा.")
    else:
        with st.spinner("AI शिक्षक तुमच्यासाठी सविस्तर नोट्स तयार करत आहे..."):
            try:
                system_instruction = f"""
                You are a senior Ayurveda Professor and BAMS Exam Expert.
                Subject: {subject}
                Topic: {topic}
                Language: {language_preference}

                Create comprehensive, high-yield revision notes covering:
                1. Concept Definition & Shloka reference (with simple breakdown)
                2. Classifications / Guna-Karma / Properties / Types
                3. Modern Medical Correlation & Clinical Relevance
                4. Exam-oriented High-Yield Summary (Important for Viva/Theory)
                Keep formatting neat and easy to read.
                """
                
                response = client.models.generate_content(
                    model='gemini-2.0-flash',
                    contents=system_instruction
                )
                
                notes_text = response.text
                st.success("✅ नोट्स तयार झाल्या आहेत!")
                st.markdown(notes_text)
                
                pdf_bytes = create_pdf(subject, topic, notes_text)
                st.download_button(
                    label="📥 PDF डाउनलोड करा",
                    data=pdf_bytes,
                    file_name=f"{topic.replace(' ', '_')}_notes.pdf",
                    mime="application/pdf"
                )
            except Exception as e:
                st.error(f"त्रुटी आली: {e}")
