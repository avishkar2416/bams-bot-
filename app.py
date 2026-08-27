import streamlit as st
from google import genai
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

# --- Printable HTML Document Generator ---
def create_printable_html(subject_name, topic_name, content_markdown):
    # Markdown चे साध्या व सुंदर HTML मध्ये रूपांतर
    content_html = html.escape(content_markdown)
    
    # Bold
    content_html = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', content_html)
    # Italic
    content_html = re.sub(r'\*(.*?)\*', r'<em>\1</em>', content_html)
    # Headings
    content_html = re.sub(r'^### (.*?)$', r'<h3>\1</h3>', content_html, flags=re.MULTILINE)
    content_html = re.sub(r'^## (.*?)$', r'<h2>\1</h2>', content_html, flags=re.MULTILINE)
    content_html = re.sub(r'^# (.*?)$', r'<h1>\1</h1>', content_html, flags=re.MULTILINE)
    # Bullet points
    content_html = re.sub(r'^\* (.*?)$', r'<li>\1</li>', content_html, flags=re.MULTILINE)
    content_html = re.sub(r'^- (.*?)$', r'<li>\1</li>', content_html, flags=re.MULTILINE)
    # Line breaks
    content_html = content_html.replace('\n', '<br>')

    html_doc = f"""
    <!DOCTYPE html>
    <html lang="mr">
    <head>
        <meta charset="UTF-8">
        <title>{topic_name} - BAMS Notes</title>
        <style>
            body {{
                font-family: 'Segoe UI', Arial, 'Noto Sans Devanagari', sans-serif;
                line-height: 1.8;
                color: #1a1a1a;
                padding: 30px;
                max-width: 800px;
                margin: auto;
            }}
            h1, h2, h3 {{
                color: #1b4d3e;
                margin-top: 20px;
                border-bottom: 1px solid #ddd;
                padding-bottom: 5px;
            }}
            strong {{
                color: #000;
                font-weight: 700;
            }}
            .header-box {{
                background-color: #f0f7f4;
                padding: 15px;
                border-radius: 8px;
                margin-bottom: 25px;
                border-left: 5px solid #2e7d32;
            }}
            li {{
                margin-bottom: 8px;
            }}
            @media print {{
                body {{ padding: 0; }}
                button {{ display: none; }}
            }}
        </style>
    </head>
    <body>
        <div class="header-box">
            <h2 style="margin:0; border:none; color:#2e7d32;">🌿 BAMS AI अभ्यास मार्गदर्शक</h2>
            <p style="margin:5px 0 0 0;"><strong>विषय:</strong> {subject_name} | <strong>संकल्पना:</strong> {topic_name}</p>
        </div>
        <div>
            {content_html}
        </div>
    </body>
    </html>
    """
    return html_doc

# --- User Interface ---
st.title("🌿 BAMS AI अभ्यास मार्गदर्शक")
st.caption("आयुर्वेद संकल्पना, श्लोक अर्थ, मॉडर्न कोरिलेशन आणि परीक्षेसाठी परिपूर्ण नोट्स.")

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
                1. Use clean bullet points and numbered points. Do NOT use complex markdown tables.
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
                
                # Printable HTML download (Perfect Marathi fonts without distortion)
                html_doc = create_printable_html(subject, topic, notes_text)
                st.download_button(
                    label="📥 PDF / प्रिंट स्वरूपात नोट्स डाऊनलोड करा (HTML)",
                    data=html_doc.encode('utf-8'),
                    file_name=f"{topic.replace(' ', '_')}_notes.html",
                    mime="text/html"
                )
                st.info("💡 टीप: डाऊनलोड केलेली फाईल ओपन करून थेट मोबाईल/ब्राऊझरमधून 'Print to PDF' करू शकता. यात अक्षरे अजिबात फुटणार नाहीत.")
            except Exception as e:
                st.error(f"त्रुटी आली: {e}")
