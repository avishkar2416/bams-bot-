import streamlit as st
from google import genai
import html
import re

# --- Page Setup ---
st.set_page_config(
    page_title="BAMS AI Study Companion | आयुर्वेद अभ्यास",
    page_icon="🌿",
    layout="wide"
)

# --- Custom UI Styling ---
st.markdown("""
<style>
    .main {
        background-color: #fcfdfd;
    }
    .stSelectbox, .stTextInput {
        font-family: 'Segoe UI', Arial, sans-serif;
    }
    .hero-box {
        background: linear-gradient(135deg, #1b4d3e 0%, #2e7d32 100%);
        padding: 24px;
        border-radius: 12px;
        color: white;
        margin-bottom: 25px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.08);
    }
</style>
""", unsafe_allow_html=True)

# --- API Key Configuration ---
api_key = st.secrets.get("GEMINI_API_KEY", "")

if not api_key:
    st.warning("⚠️ कृपया सुरू ठेवण्यासाठी तुमची Gemini API Key टाका (Settings > Secrets मध्ये जोडा).")
    st.stop()

client = genai.Client(api_key=api_key)

def format_notes_as_printable_doc(subject_name, topic_name, raw_content):
    formatted_body = html.escape(raw_content)
    
    # Text Formatting
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
        <title>{topic_name} - BAMS Study Companion</title>
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+Devanagari:wght@400;500;600;700&display=swap');
            body {{
                font-family: 'Noto Sans Devanagari', Arial, sans-serif;
                line-height: 1.8;
                color: #222;
                padding: 30px;
                max-width: 900px;
                margin: auto;
                background-color: #fff;
            }}
            .header-banner {{
                background: linear-gradient(135deg, #1b4d3e 0%, #2e7d32 100%);
                color: white;
                border-radius: 10px;
                padding: 20px 25px;
                margin-bottom: 25px;
            }}
            .header-banner h2 {{
                margin: 0 0 8px 0;
                color: #ffffff;
                font-size: 24px;
            }}
            .header-banner p {{
                margin: 0;
                font-size: 14px;
                opacity: 0.95;
            }}
            h1, h2 {{
                color: #1b4d3e;
                border-bottom: 2px solid #e0e0e0;
                padding-bottom: 6px;
                margin-top: 24px;
            }}
            h3 {{
                color: #2e7d32;
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
                background-color: #1b4d3e;
                color: white;
                padding: 12px 26px;
                font-size: 15px;
                font-weight: 600;
                border: none;
                border-radius: 6px;
                cursor: pointer;
                transition: background 0.3s;
            }}
            .print-btn:hover {{
                background-color: #14382d;
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
            <button class="print-btn" onclick="window.print()">📥 थेट PDF सेव्ह करा / प्रिंट करा</button>
            <p style="color: #666; font-size: 13px; margin-top: 6px;">(मोबाईलमध्ये 'Save as PDF' निवडून डाऊनलोड करा)</p>
        </div>

        <div class="header-banner">
            <h2>🌿 BAMS AI अभ्यास मार्गदर्शक</h2>
            <p><strong>विषय:</strong> {subject_name} &nbsp;|&nbsp; <strong>संकल्पना:</strong> {topic_name}</p>
        </div>

        <div>
            {formatted_body}
        </div>

        <script>
            window.onload = function() {{
                setTimeout(function() {{ window.print(); }}, 600);
            }};
        </script>
    </body>
    </html>
    """
    return html_template

# --- Header Section ---
st.markdown("""
<div class="hero-box">
    <h2 style="margin:0; font-size:26px;">🌿 BAMS AI अभ्यास मार्गदर्शक</h2>
    <p style="margin:6px 0 0 0; opacity:0.9;">NCISM अभ्यासक्रमानुसार अस्सल श्लोक, अन्वय, मॉडर्न कोरिलेशन, चिकित्सा सूत्र आणि परीक्षा-उपयोगी सविस्तर नोट्स.</p>
</div>
""", unsafe_allow_html=True)

# Layout Inputs
col1, col2 = st.columns([1, 1])

with col1:
    subject = st.selectbox(
        "📚 विषय निवडा (Select Subject):",
        [
            "Kriya Sharir (क्रिया शारीर)",
            "Rachana Sharir (रचना शारीर)",
            "Dravyaguna Vijnana (द्रव्यगुण विज्ञान)",
            "Rasashastra & Bhaishajya Kalpana (रसशास्त्र व भैषज्य कल्पना)",
            "Roga Nidan & Vikriti Vigyan (रोगनिदान)",
            "Samhita Siddhant & Charak Samhita (संहिता सिद्धांत)",
            "Kayachikitsa (कायचिकित्सा)",
            "Panchakarma (पंचकर्म)",
            "Shalya Tantra (शल्य तंत्र)",
            "Shalakya Tantra (शालाक्य तंत्र)",
            "Prasuti Tantra & Stri Roga (प्रसूति तंत्र व स्त्रीरोग)",
            "Kaumarbhritya (कौमारभृत्य)",
            "Agada Tantra & Vyavahara Ayurveda (अगद तंत्र)"
        ]
    )

with col2:
    language_preference = st.radio(
        "🌐 नोट्सचे माध्यम (Language):",
        ["मराठी (संस्कृत श्लोक + सोपा अर्थ + इंग्रजी टर्म्स)", "English + Sanskrit Shlokas"],
        horizontal=True
    )

topic = st.text_input(
    "🔍 अभ्यासाचा विषय / प्रश्न टाका:",
    placeholder="उदा. Pitta Dosha Prakar & Karya, Ashwagandha Dravyaguna, किंवा Amavata Nidan & Chikitsa"
)

if st.button("📝 सविस्तर अभ्यास नोट्स तयार करा", type="primary"):
    if not topic.strip():
        st.error("कृपया अभ्यासाचा विषय किंवा प्रश्न प्रविष्ट करा.")
    else:
        with st.spinner("AI आयुर्वेद तज्ज्ञ तुमच्यासाठी परिपूर्ण श्लोक व सविस्तर नोट्स तयार करत आहे..."):
            try:
                system_instruction = f"""
                You are a senior Ayurveda Acharya and BAMS Exam Paper Evaluator according to NCISM curriculum standards.
                Subject: {subject}
                Topic: {topic}
                Language: {language_preference}

                Generate extremely detailed, comprehensive, high-scoring BAMS study notes formatted with utmost clarity.
                Follow this exact structure:

                # 🌿 {topic} - परिपूर्ण अभ्यास नोट्स

                ## १. निरुक्ती, व्याख्या आणि मूळ संदर्भ श्लोक (Etymology, Definition & Shlokas)
                * मूळ संस्कृत श्लोक अचूक देवनागरीमध्ये लिहा (संहिता संदर्भ नमूद करा - चरक/सुश्रुत/अष्टांग हृदय).
                * श्लोकाचा पदच्छेद आणि शब्दशः अन्वय.
                * अत्यंत सोप्या व ओघवत्या भाषेत संपूर्ण श्लोकार्थ.

                ## २. सविस्तर वर्गीकरण, गुण, कर्म व प्रकार (Classification, Guna-Karma & Functions)
                * घटक, गुण, स्थान आणि प्रकार यांची स्पष्ट बुलेट पॉईंट्समध्ये विभागणी (• वापरून).
                * प्रत्येक प्रकाराचे विशिष्ट स्थान (Seat) आणि नेमके कार्य (Function).
                * वृद्धी आणि क्षय लक्षणे (Symptoms of increase/decrease, if applicable).

                ## ३. आधुनिक वैद्यकशास्त्राशी तुलना (Modern Medical Correlation)
                * ॲनाटॉमी (Anatomy), फिजिओलॉजी (Physiology) किंवा पॅथॉलॉजी (Pathology) नुसार आधुनिक संकल्पनांशी अचूक तुलना.
                * संबंधित हार्मोन्स, एन्झाईम्स किंवा ऑर्गन्सचे संदर्भ (Clear bullet points).

                ## ४. चिकित्सा सूत्र व उपयुक्त कल्प / औषधी (Chikitsa Sutra & Formulations - if applicable)
                * प्रधान चिकित्सा सिद्धांत / पंचकर्म उपाय.
                * प्रमुख क्लासिकल योग व औषधी द्रव्ये.

                ## ५. परीक्षेसाठी महत्त्वाचे मुद्दे आणि व्हायव्हा प्रश्न (High-Yield Exam Points & Viva Voce)
                * Long Answer Questions (LAQ) आणि Short Answer Questions (SAQ) साठी महत्त्वाचे की-वर्ड्स.
                * तोंडी परीक्षेसाठी (Viva Voce) ३-४ हमखास विचारले जाणारे प्रश्न व त्यांची उत्तरे.

                Keep the entire content deeply informative, crystal-clear, structured with bullet points, and highlight critical keywords in **Bold**.
                """
                
                response = client.models.generate_content(
                    model='models/gemini-3.6-flash',
                    contents=system_instruction
                )
                
                notes_text = response.text
                st.success("✅ सर्व श्लोक आणि मुद्द्यांसह सविस्तर नोट्स तयार झाल्या आहेत!")
                st.markdown(notes_text)
                
                doc_html = format_notes_as_printable_doc(subject, topic, notes_text)
                st.download_button(
                    label="📥 थेट PDF डाऊनलोड करा (.pdf)",
                    data=doc_html.encode('utf-8'),
                    file_name=f"{topic.replace(' ', '_')}_BAMS_Notes.html",
                    mime="text/html"
                )
            except Exception as e:
                st.error(f"त्रुटी आली: {e}")
