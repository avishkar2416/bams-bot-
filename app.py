import streamlit as st
from google import genai
import requests
import os
import io

from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import re
import html

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

def generate_direct_pdf(subject_name, topic_name, raw_markdown):
    ensure_font_downloaded()
    pdfmetrics.registerFont(TTFont('Devanagari', FONT_PATH))
    
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=letter,
        rightMargin=40,
        leftMargin=40,
        topMargin=40,
        bottomMargin=40
    )
    
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'MainTitle',
        fontName='Devanagari',
        fontSize=15,
        leading=20,
        textColor='#1b4d3e',
        spaceAfter=10
    )
    h2_style = ParagraphStyle(
        'H2Style',
        fontName='Devanagari',
        fontSize=12,
        leading=16,
        textColor='#2e7d32',
        spaceBefore=10,
        spaceAfter=5
    )
    body_style = ParagraphStyle(
        'BodyStyle',
        fontName='Devanagari',
        fontSize=10,
        leading=15,
        textColor='#111111',
        spaceAfter=6
    )
    
    story = []
    story.append(Paragraph(f"<b>🌿 BAMS अभ्यास मार्गदर्शक</b>", title_style))
    story.append(Paragraph(f"<b>विषय:</b> {subject_name} | <b>संकल्पना:</b> {topic_name}", body_style))
    story.append(Spacer(1, 10))
    
    lines = raw_markdown.split('\n')
    for line in lines:
        line = line.strip()
        if not line:
            continue
            
        line_escaped = html.escape(line)
        line_escaped = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', line_escaped)
        line_escaped = re.sub(r'\*(.*?)\*', r'<i>\1</i>', line_escaped)
        
        if line_escaped.startswith('# ') or line_escaped.startswith('## '):
            clean_h = re.sub(r'^#+\s*', '', line_escaped)
            story.append(Paragraph(f"<b>{clean_h}</b>", h2_style))
        elif line_escaped.startswith('### '):
            clean_h = re.sub(r'^#+\s*', '', line_escaped)
            story.append(Paragraph(f"<b>{clean_h}</b>", h2_style))
        elif line_escaped.startswith('* ') or line_escaped.startswith('- '):
            clean_bullet = line_escaped[2:]
            story.append(Paragraph(f"• {clean_bullet}", body_style))
        else:
            story.append(Paragraph(line_escaped, body_style))
            
    doc.build(story)
    buffer.seek(0)
    return buffer.getvalue()

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

                Create clean, well-structured, exam-oriented notes following these strict rules:
                1. Use clean bullet points and numbered points. Do NOT use markdown tables.
                2. Highlight all key terms, Sanskrit words, and important facts in **Bold Black text**.
                3. Language must be natural, fluent Marathi with clear Ayurvedic terminology.
                4. Structure the response strictly in these 4 sections:
                   - **१. व्याख्या आणि संदर्भ श्लोक (Definition & Reference Shloka)** (Include shloka and simple line-by-line meaning)
                   - **२. गुण, कर्म आणि प्रकार (Guna, Karma & Types)** (Point-by-point breakdown)
                   - **३. आधुनिक वैद्यकशास्त्राशी तुलना (Modern Medical Correlation)** (System/organ level comparison)
                   - **४. परीक्षेसाठी महत्त्वाचे मुद्दे (High-Yield Exam Points & Viva Tips)**
                """
                
                response = client.models.generate_content(
                    model='models/gemini-3.6-flash',
                    contents=system_instruction
                )
                
                notes_text = response.text
                st.success("✅ सुटसुटीत नोट्स तयार झाल्या आहेत!")
                st.markdown(notes_text)
                
                pdf_data = generate_direct_pdf(subject, topic, notes_text)
                st.download_button(
                    label="📥 थेट PDF डाऊनलोड करा (.pdf)",
                    data=pdf_data,
                    file_name=f"{topic.replace(' ', '_')}_BAMS_Notes.pdf",
                    mime="application/pdf"
                )
            except Exception as e:
                st.error(f"त्रुटी आली: {e}")
