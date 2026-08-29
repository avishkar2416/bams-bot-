import streamlit as st
from google import genai
import markdown

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
        background-color: #f8faf9;
    }
    .hero-box {
        background: linear-gradient(135deg, #1b4d3e 0%, #2e7d32 100%);
        padding: 22px 25px;
        border-radius: 12px;
        color: white;
        margin-bottom: 25px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.08);
    }
    .notes-card {
        background-color: #ffffff;
        padding: 25px;
        border-radius: 12px;
        border: 1px solid #e2e8f0;
        box-shadow: 0 2px 8px rgba(0,0,0,0.04);
        margin-top: 20px;
    }
</style>
""", unsafe_allow_html=True)

# --- API Key Configuration ---
api_key = st.secrets.get("GEMINI_API_KEY", "")

if not api_key:
    st.warning("⚠️ कृपया सुरू ठेवण्यासाठी तुमची Gemini API Key टाका (Settings > Secrets मध्ये जोडा).")
    st.stop()

client = genai.Client(api_key=api_key)

def create_printable_html_doc(subject_name, topic_name, raw_content):
    # Markdown चे अचूक HTML मध्ये रूपांतर
    html_content = markdown.markdown(raw_content, extensions=['extra', 'nl2br'])

    full_html = f"""
    <!DOCTYPE html>
    <html lang="mr">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>{topic_name} - BAMS Notes</title>
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+Devanagari:wght@400;500;600;700&display=swap');
            body {{
                font-family: 'Noto Sans Devanagari', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                line-height: 1.8;
                color: #1e293b;
                padding: 30px 20px;
                max-width: 850px;
                margin: auto;
                background-color: #ffffff;
            }}
            .header-banner {{
                background: linear-gradient(135deg, #1b4d3e 0%, #2e7d32 100%);
                color: white;
                border-radius: 10px;
                padding: 20px 24px;
                margin-bottom: 30px;
            }}
            .header-banner h2 {{
                margin: 0 0 6px 0;
                color: #ffffff;
                font-size: 22px;
            }}
            .header-banner p {{
                margin: 0;
                font-size: 14px;
                opacity: 0.95;
            }}
            h1, h2 {{
                color: #1b4d3e;
                border-bottom: 2px solid #e2e8f0;
                padding-bottom: 6px;
                margin-top: 26px;
                font-size: 20px;
            }}
            h3 {{
                color: #2e7d32;
                margin-top: 18px;
                font-size: 16px;
            }}
            blockquote {{
                background: #f0fdf4;
                border-left: 4px solid #22c55e;
                margin: 15px 0;
                padding: 12px 18px;
                border-radius: 0 8px 8px 0;
                font-weight: 600;
                color: #14532d;
            }}
            strong {{
                color: #0f172a;
                font-weight: 700;
            }}
            ul, ol {{
                padding-left: 22px;
                margin: 10px 0;
            }}
            li {{
                margin-bottom: 8px;
            }}
            .print-btn {{
                background-color: #1b4d3e;
                color: white;
                padding: 12px 24px;
                font-size: 15px;
                font-weight: bold;
                border: none;
                border-radius: 8px;
                cursor: pointer;
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
        <div class="no-print" style="text-align: center; margin-bottom: 25px;">
            <button class="print-btn" onclick="window.print()">📥 PDF डाऊनलोड करा / प्रिंट करा</button>
            <p style="color: #64748b; font-size: 13px; margin-top: 6px;">(मोबाईलमध्ये उघडल्यावर 'Save as PDF' निवडून डाऊनलोड करा)</p>
        </div>

        <div class="header-banner">
            <h2>🌿 BAMS अभ्यास मार्गदर्शक</h2>
            <p><strong>विषय:</strong> {subject_name} &nbsp;|&nbsp; <strong>संकल्पना:</strong> {topic_name}</p>
        </div>

        <div class="content-body">
            {html_content}
        </div>

        <script>
            window.onload = function() {{
                setTimeout(function() {{ window.print(); }}, 600);
            }};
        </script>
    </body>
    </html>
    """
    return full_html

# --- Header Section ---
st.markdown("""
<div class="hero-box">
    <h2 style="margin:0; font-size:24px;">🌿 BAMS AI अभ्यास मार्गदर्शक</h2>
    <p style="margin:6px 0 0 0; opacity:0.9;">NCISM अभ्यासक्रमानुसार अस्सल श्लोक, अन्वय, मॉडर्न कोरिलेशन आणि परीक्षा-उपयोगी सविस्तर नोट्स.</p>
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
        with st.spinner("AI आयुर्वेद तज्ज्ञ तुमच्यासाठी परिपूर्ण श्लोक व सुटसुटीत नोट्स तयार करत आहे..."):
            try:
                system_instruction = f"""
                You are a senior Ayurveda Professor and BAMS Exam Paper Evaluator according to NCISM curriculum standards.
                Subject: {subject}
                Topic: {topic}
                Language: {language_preference}

                Generate extremely detailed, comprehensive, high-scoring BAMS study notes.
                
                STRICT FORMATTING RULES:
                1. NEVER use ASCII or text tree diagrams (do not draw box charts or '|---' lines).
                2. Use clear hierarchical bullet points (•) and numbered lists for types and classifications.
                3. Wrap Sanskrit Shlokas in blockquotes (> "Shloka here").
                4. Highlight all critical keywords, anatomical names, and viva terms in **Bold Black text**.
                5. Use clean, natural Marathi with correct terminology.

                Follow this exact section structure:

                # 🌿 {topic} - परिपूर्ण अभ्यास नोट्स

                ## १. निरुक्ती, व्याख्या आणि मूळ संदर्भ श्लोक (Etymology, Definition & Shlokas)
                * मूळ संस्कृत श्लोक देवनागरीमध्ये व संहिता संदर्भ (चरक/सुश्रुत/अष्टांग हृदय).
                * श्लोकाचा पदच्छेद आणि शब्दशः अन्वय.
                * सोप्या भाषेत संपूर्ण श्लोकार्थ.

                ## २. सविस्तर वर्गीकरण, गुण, कर्म व प्रकार (Classification, Guna-Karma & Functions)
                * गुण आणि स्थान.
                * प्रकार (प्रत्येक प्रकाराचे नाव, स्थान आणि कार्य सुटसुटीत बुलेट पॉईंट्समध्ये).
                * वृद्धी आणि क्षय लक्षणे.

                ## ३. आधुनिक वैद्यकशास्त्राशी तुलना (Modern Medical Correlation)
                * ॲनाटॉमी (Anatomy), फिजिओलॉजी (Physiology) किंवा पॅथॉलॉजी (Pathology) नुसार आधुनिक संकल्पनांशी अचूक तुलना.
                * हार्मोन्स, एन्झाईम्स किंवा ऑर्गन्सचे संदर्भ.

                ## ४. चिकित्सा सूत्र व उपयुक्त कल्प / औषधी (Chikitsa Sutra & Formulations)
                * प्रधान चिकित्सा सिद्धांत व प्रमुख औषधी द्रव्ये.

                ## ५. परीक्षेसाठी महत्त्वाचे मुद्दे आणि व्हायव्हा प्रश्न (High-Yield Exam Points & Viva Voce)
                * Theory परीक्षेसाठी महत्त्वाचे की-वर्ड्स.
                * तोंडी परीक्षेसाठी (Viva Voce) ३-४ हमखास प्रश्न व उत्तरे.
                """
                
                response = client.models.generate_content(
                    model='models/gemini-3.6-flash',
                    contents=system_instruction
                )
                
                notes_text = response.text
                st.success("✅ सर्व श्लोक आणि मुद्द्यांसह सविस्तर नोट्स तयार झाल्या आहेत!")
                
                with st.container():
                    st.markdown(f'<div class="notes-card">', unsafe_allow_html=True)
                    st.markdown(notes_text)
                    st.markdown('</div>', unsafe_allow_html=True)
                
                doc_html = create_printable_html_doc(subject, topic, notes_text)
                st.download_button(
                    label="📥 PDF नोट्स डाऊनलोड करा (.html / .pdf)",
                    data=doc_html.encode('utf-8'),
                    file_name=f"{topic.replace(' ', '_')}_BAMS_Notes.html",
                    mime="text/html"
                )
            except Exception as e:
                st.error(f"त्रुटी आली: {e}")
