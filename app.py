import streamlit as st
from google import genai
import markdown
import time

# --- Page Setup ---
st.set_page_config(
    page_title="BAMS AI Study Companion | आयुर्वेद अभ्यास",
    page_icon="🌿",
    layout="wide"
)

# --- Custom Styling ---
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
    .stSelectbox, .stTextInput, .stRadio {
        font-family: 'Segoe UI', Arial, sans-serif;
    }
</style>
""", unsafe_allow_html=True)

# --- API Key Configuration ---
api_key = st.secrets.get("GEMINI_API_KEY", "")

if not api_key:
    st.warning("⚠️ कृपया सुरू ठेवण्यासाठी तुमची Gemini API Key जोडा (Settings > Secrets).")
    st.stop()

client = genai.Client(api_key=api_key)

# --- Clean Printable Document Generator (Zero Distorted Characters) ---
def create_printable_html_doc(subject_name, topic_name, raw_content):
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
            .header-banner h2 {{ margin: 0 0 6px 0; color: #ffffff; font-size: 22px; }}
            .header-banner p {{ margin: 0; font-size: 14px; opacity: 0.95; }}
            h1, h2 {{ color: #1b4d3e; border-bottom: 2px solid #e2e8f0; padding-bottom: 6px; margin-top: 26px; }}
            h3 {{ color: #2e7d32; margin-top: 18px; }}
            blockquote {{
                background: #f0fdf4;
                border-left: 4px solid #22c55e;
                margin: 15px 0;
                padding: 12px 18px;
                border-radius: 0 8px 8px 0;
                font-weight: 600;
                color: #14532d;
            }}
            strong {{ color: #0f172a; font-weight: 700; }}
            ul, ol {{ padding-left: 22px; margin: 10px 0; }}
            li {{ margin-bottom: 8px; }}
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
                .no-print {{ display: none !important; }}
                body {{ padding: 0; }}
            }}
        </style>
    </head>
    <body>
        <div class="no-print" style="text-align: center; margin-bottom: 25px;">
            <button class="print-btn" onclick="window.print()">📥 PDF सेव्ह करा / प्रिंट करा</button>
            <p style="color: #64748b; font-size: 13px; margin-top: 6px;">(मोबाईलमध्ये 'Save as PDF' निवडून डाऊनलोड करा)</p>
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

# --- UI Header ---
st.markdown("""
<div class="hero-box">
    <h2 style="margin:0; font-size:24px;">🌿 BAMS AI अभ्यास मार्गदर्शक</h2>
    <p style="margin:6px 0 0 0; opacity:0.9;">NCISM अभ्यासक्रमानुसार अस्सल श्लोक, अन्वय, मॉडर्न कोरिलेशन आणि परीक्षा-उपयोगी सविस्तर नोट्स.</p>
</div>
""", unsafe_allow_html=True)

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
    placeholder="उदा. Pitta Dosha Prakar & Karya किंवा Ashwagandha Dravyaguna"
)

if st.button("📝 सविस्तर अभ्यास नोट्स तयार करा", type="primary"):
    if not topic.strip():
        st.error("कृपया अभ्यासाचा विषय प्रविष्ट करा.")
    else:
        system_instruction = f"""
        You are a senior Ayurveda Professor and BAMS Exam Expert according to NCISM curriculum.
        Subject: {subject}
        Topic: {topic}
        Language: {language_preference}

        Generate detailed, high-yield, structured revision notes:
        1. NEVER create ASCII diagrams or text tree boxes (avoid '|---' and box drawings).
        2. Format Sanskrit Shlokas strictly inside blockquotes (> "Shloka").
        3. Highlight key terms, anatomical words, and keywords in **Bold**.
        4. Structure strictly into:
           - १. निरुक्ती, व्याख्या आणि मूळ संदर्भ श्लोक (अचूक पदच्छेद, अन्वय व अर्थ)
           - २. सविस्तर वर्गीकरण, गुण, कर्म व प्रकार (स्थान व कार्यासह सुटसुटीत बुलेट पॉईंट्स)
           - ३. आधुनिक वैद्यकशास्त्राशी तुलना (Modern Medical Correlation)
           - ४. चिकित्सा सूत्र व उपयुक्त औषधी कल्प
           - ५. परीक्षेसाठी महत्त्वाचे मुद्दे आणि ३-४ हमखास व्हायव्हा (Viva) प्रश्न व उत्तरे
        """

        output_area = st.empty()
        notes_text = ""
        success_flag = False

        # फास्ट एक्झिक्युशन आणि 503 लोड एररसाठी ऑटोमॅटिक बॅकअप मॉडेल्स लिस्ट
        models_to_try = [
            'models/gemini-3.6-flash',
            'models/gemini-2.5-pro',
            'gemini-2.5-flash'
        ]

        with st.spinner("⚡ AI तज्ज्ञ जलद गतीने नोट्स तयार करत आहे..."):
            for model_name in models_to_try:
                try:
                    stream = client.models.generate_content_stream(
                        model=model_name,
                        contents=system_instruction
                    )
                    
                    for chunk in stream:
                        if chunk.text:
                            notes_text += chunk.text
                            output_area.markdown(notes_text)

                    if notes_text.strip():
                        success_flag = True
                        break
                except Exception:
                    time.sleep(1)
                    continue

        if success_flag:
            st.success("✅ सर्व श्लोक आणि मुद्द्यांसह नोट्स तयार झाल्या आहेत!")
            
            doc_html = create_printable_html_doc(subject, topic, notes_text)
            st.download_button(
                label="📥 PDF नोट्स डाऊनलोड करा (.pdf / .html)",
                data=doc_html.encode('utf-8'),
                file_name=f"{topic.replace(' ', '_')}_BAMS_Notes.html",
                mime="text/html"
            )
        else:
            st.error("गुगल सर्व्हरवर सध्या प्रचंड भार आहे. कृपया ५ सेकंद थांबा आणि पुन्हा बटण दाबा.")
