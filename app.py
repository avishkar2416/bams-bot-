import streamlit as st
from google import genai
import html
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

def format_notes_as_printable_doc(subject_name, topic_name, raw_content):
    # Markdown ला व्यवस्थित आणि सुबक फॉरमॅट करणे
    formatted_body = html.escape(raw_content)
    formatted_body = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', formatted_body)
    formatted_body = re.sub(r'\*(.*?)\*', r'<em>\1</em>', formatted_body)
    formatted_body = re.sub(r'^### (.*?)$', r'<h3>\1</h3>', formatted_body, flags=re.MULTILINE)
    formatted_body = re.sub(r'^## (.*?)$', r'<h2>\1</h2>', formatted_body, flags=re.MULTILINE)
    formatted_body = re.sub(r'^# (.*?)$', r'<h1>\1</h1>', formatted_body, flags=re.MULTILINE)
    formatted_body = re.sub(r'^[-*]\s+(.*?)$', r'<li>\1</li>', formatted_body, flags=re.MULTILINE)
    formatted_body = formatted_body.replace('\n', '<br>')

    html_template = f"""
    <!DOCTYPE html>
    <html lang="mr">
    <head>
        <meta charset="UTF-8">
        <title>{topic_name} - BAMS Notes</title>
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+Devanagari:wght@400;600;700&display=swap');
            body {{
                font-family: 'Noto Sans Devanagari', Arial, sans-serif;
                line-height: 1.8;
                color: #111;
                padding: 25px;
                max-width: 850px;
                margin: auto;
            }}
            .header-banner {{
                background-color: #f4fbf7;
                border: 2px solid #2e7d32;
                border-radius: 8px;
                padding: 15px 20px;
                margin-bottom: 20px;
            }}
            h1, h2, h3 {{
                color: #1b4d3e;
                margin-top: 18px;
            }}
            strong {{
                color: #000;
                font-weight: 700;
            }}
            li {{
                margin-bottom: 6px;
            }}
            .print-btn {{
                background-color: #2e7d32;
                color: white;
                padding: 12px 24px;
                font-size: 16px;
                font-weight: bold;
                border: none;
                border-radius: 6px;
                cursor: pointer;
                margin-bottom: 20px;
            }}
            @media print {{
                .no-print {{
                    display: none !important;
                }}
                body {{
                    padding: 0;
                }}
            }}
        </style>
    </head>
    <body>
        <div class="no-print" style="text-align: center; margin-bottom: 20px;">
            <button class="print-btn" onclick="window.print()">🖨️ PDF स्वरूपात सेव्ह करा / प्रिंट करा</button>
            <p style="color: #666; font-size: 13px;">(मोबाईलमध्ये 'Save as PDF' निवडून डाऊनलोड करा)</p>
        </div>

        <div class="header-banner">
            <h2 style="margin:0; color:#2e7d32;">🌿 BAMS अभ्यास मार्गदर्शक</h2>
            <p style="margin: 6px 0 0 0;"><strong>विषय:</strong> {subject_name} | <strong>संकल्पना:</strong> {topic_name}</p>
        </div>

        <div>
            {formatted_body}
        </div>

        <script>
            // फाईल उघडल्याबरोबर आपोआप प्रिंट/PDF डायलॉग उघडणे
            window.onload = function() {{
                setTimeout(function() {{ window.print(); }}, 500);
            }};
        </script>
    </body>
    </html>
    """
    return html_template

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
                
                doc_html = format_notes_as_printable_doc(subject, topic, notes_text)
                st.download_button(
                    label="📥 PDF नोट्स डाऊनलोड करा",
                    data=doc_html.encode('utf-8'),
                    file_name=f"{topic.replace(' ', '_')}_Notes.html",
                    mime="text/html"
                )
            except Exception as e:
                st.error(f"त्रुटी आली: {e}")
