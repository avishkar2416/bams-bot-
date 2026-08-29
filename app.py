import streamlit as st
from google import genai
import markdown
import time

# --- Page Setup ---
st.set_page_config(
    page_title="AyurVeda AI | BAMS Companion",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- Universal Mobile-Friendly CSS ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@500;600;700;800&family=Noto+Sans+Devanagari:wght@400;600;700;800&display=swap');

    /* Global Text Visibility Fix for Mobile & Dark Mode */
    * {
        font-family: 'Noto Sans Devanagari', 'Plus Jakarta Sans', sans-serif !important;
    }
    
    .stApp {
        background-color: #f8faf9 !important;
    }

    /* Force Label & Text Visibility */
    label, p, span, div {
        color: #0f172a !important;
    }

    /* Top Navbar */
    .premium-navbar {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 14px 20px;
        background: #ffffff !important;
        border: 1px solid #e2e8f0;
        border-radius: 16px;
        margin-bottom: 20px;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.04);
    }
    .nav-brand {
        display: flex;
        align-items: center;
        gap: 10px;
    }
    .nav-logo {
        background: #059669;
        color: #ffffff !important;
        width: 40px;
        height: 40px;
        border-radius: 10px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 20px;
    }
    .brand-title {
        font-size: 18px;
        font-weight: 800;
        color: #064e3b !important;
        margin: 0;
    }
    .brand-tag {
        font-size: 10px;
        font-weight: 700;
        color: #059669 !important;
        text-transform: uppercase;
    }

    /* Owner Badge */
    .owner-badge {
        background: #ecfdf5 !important;
        border: 1px solid #a7f3d0;
        padding: 6px 12px;
        border-radius: 10px;
        text-align: right;
    }
    .owner-name {
        font-size: 12px;
        font-weight: 800;
        color: #065f46 !important;
    }
    .owner-service {
        font-size: 10px;
        color: #059669 !important;
        font-weight: 600;
    }

    /* Main Hero Banner */
    .hero-banner {
        background: linear-gradient(135deg, #064e3b 0%, #047857 100%) !important;
        padding: 28px 24px;
        border-radius: 20px;
        margin-bottom: 25px;
        box-shadow: 0 10px 25px rgba(5, 150, 105, 0.25);
    }
    .hero-banner * {
        color: #ffffff !important;
    }
    .hero-tag {
        display: inline-block;
        background: rgba(255, 255, 255, 0.2);
        padding: 4px 12px;
        border-radius: 50px;
        font-size: 11px;
        font-weight: 700;
        margin-bottom: 10px;
    }
    .hero-title {
        font-size: 26px;
        font-weight: 800;
        margin: 0 0 8px 0;
    }
    .hero-desc {
        font-size: 14px;
        line-height: 1.6;
        opacity: 0.95;
        margin: 0;
    }

    /* Streamlit Selectbox & Inputs styling */
    div[data-baseweb="select"] > div,
    div[data-baseweb="input"] > div {
        background-color: #ffffff !important;
        border: 1.5px solid #cbd5e1 !important;
        border-radius: 12px !important;
    }
    div[data-baseweb="select"] span,
    div[data-baseweb="input"] input {
        color: #0f172a !important;
    }

    /* Main Button */
    div.stButton > button {
        background: linear-gradient(135deg, #059669 0%, #047857 100%) !important;
        color: #ffffff !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 14px 20px !important;
        font-size: 16px !important;
        font-weight: 700 !important;
        box-shadow: 0 4px 15px rgba(5, 150, 105, 0.35) !important;
    }

    /* Notes Display Box */
    .notes-box {
        background: #ffffff !important;
        border: 1px solid #e2e8f0;
        border-radius: 20px;
        padding: 30px 24px;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.04);
        margin-top: 25px;
    }
    .notes-box h1, .notes-box h2 {
        color: #064e3b !important;
        border-bottom: 2px solid #ecfdf5;
        padding-bottom: 6px;
    }
    .notes-box h3 {
        color: #047857 !important;
    }
    .notes-box blockquote {
        background: #f0fdf4 !important;
        border-left: 4px solid #10b981;
        padding: 12px 18px;
        border-radius: 0 12px 12px 0;
        margin: 16px 0;
    }
    .notes-box blockquote * {
        color: #065f46 !important;
        font-weight: 600;
    }

    /* Footer */
    .app-footer {
        text-align: center;
        padding: 35px 10px 10px 10px;
        font-size: 13px;
        color: #64748b !important;
    }
</style>
""", unsafe_allow_html=True)

# --- API Key Configuration ---
api_key = st.secrets.get("GEMINI_API_KEY", "")

if not api_key:
    st.error("⚠️ कृपया Settings > Secrets मध्ये तुमची GEMINI_API_KEY कॉन्फिगर करा.")
    st.stop()

client = genai.Client(api_key=api_key)

# --- Printable HTML Document Generator ---
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
            @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+Devanagari:wght@400;600;700;800&display=swap');
            body {{
                font-family: 'Noto Sans Devanagari', Arial, sans-serif;
                line-height: 1.85;
                color: #1e293b;
                padding: 35px 20px;
                max-width: 850px;
                margin: auto;
                background-color: #ffffff;
            }}
            .header-banner {{
                background: linear-gradient(135deg, #064e3b 0%, #047857 100%);
                color: white;
                border-radius: 16px;
                padding: 22px 28px;
                margin-bottom: 30px;
            }}
            .header-banner h2 {{ margin: 0 0 6px 0; color: #ffffff; font-size: 22px; font-weight: 800; }}
            .header-banner p {{ margin: 0; font-size: 14px; opacity: 0.95; color: #ffffff; }}
            h1 {{ color: #064e3b; border-bottom: 2px solid #e2e8f0; padding-bottom: 8px; margin-top: 25px; }}
            h2 {{ color: #047857; margin-top: 26px; font-size: 20px; }}
            h3 {{ color: #059669; margin-top: 18px; }}
            blockquote {{
                background: #f0fdf4;
                border-left: 5px solid #10b981;
                margin: 18px 0;
                padding: 14px 20px;
                border-radius: 0 12px 12px 0;
                font-weight: 600;
                color: #065f46;
            }}
            strong {{ color: #0f172a; font-weight: 700; }}
            ul, ol {{ padding-left: 22px; margin: 10px 0; }}
            li {{ margin-bottom: 8px; }}
            .print-btn {{
                background: linear-gradient(135deg, #059669 0%, #047857 100%);
                color: white;
                padding: 14px 30px;
                font-size: 15px;
                font-weight: 700;
                border: none;
                border-radius: 12px;
                cursor: pointer;
            }}
            .doc-footer {{
                margin-top: 45px;
                border-top: 1px solid #e2e8f0;
                padding-top: 18px;
                text-align: center;
                font-size: 13px;
                color: #64748b;
            }}
            @media print {{
                .no-print {{ display: none !important; }}
                body {{ padding: 0; }}
            }}
        </style>
    </head>
    <body>
        <div class="no-print" style="text-align: center; margin-bottom: 28px;">
            <button class="print-btn" onclick="window.print()">📥 थेट PDF सेव्ह करा / प्रिंट करा</button>
            <p style="color: #64748b; font-size: 13px; margin-top: 8px;">(मोबाईलमध्ये 'Save as PDF' निवडून डाऊनलोड करा)</p>
        </div>

        <div class="header-banner">
            <h2>🌿 BAMS AI Clinical & Exam Guide</h2>
            <p><strong>विषय:</strong> {subject_name} &nbsp;|&nbsp; <strong>संकल्पना:</strong> {topic_name}</p>
        </div>

        <div>
            {html_content}
        </div>

        <div class="doc-footer">
            <p>🌿 <strong>BAMS AI Study Companion</strong> | विकसित केले: <strong>Avishkar Alashe</strong> (तुमच्या सेवेसाठी 🙏)</p>
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

# --- Top Navigation Bar ---
st.markdown("""
<div class="premium-navbar">
    <div class="nav-brand">
        <div class="nav-logo">🌿</div>
        <div>
            <div class="brand-title">AyurVeda AI</div>
            <div class="brand-tag">NCISM Curriculum Engine</div>
        </div>
    </div>
    <div class="owner-badge">
        <div class="owner-name">Avishkar Alashe</div>
        <div class="owner-service">तुमच्या सेवेसाठी 🙏</div>
    </div>
</div>
""", unsafe_allow_html=True)

# --- Hero Banner ---
st.markdown("""
<div class="hero-banner">
    <div class="hero-tag">✨ NCISM Standard Study Matrix</div>
    <div class="hero-title">BAMS इंटेलिजंट स्टडी असिस्टंट</div>
    <div class="hero-desc">अस्सल संहिता संदर्भ, अचूक संस्कृत श्लोक व अन्वय, मॉडर्न मेडिकल कोरिलेशन आणि हाय-स्कोरिंग क्लिनिकल नोट्स — सर्वकाही १-क्लिकमध्ये.</div>
</div>
""", unsafe_allow_html=True)

# --- Inputs ---
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

language_preference = st.radio(
    "🌐 माध्यम (Language):",
    ["मराठी (संस्कृत श्लोक + सोपा अर्थ + मॉडर्न टर्म्स)", "English + Sanskrit Shlokas"],
    horizontal=True
)

topic = st.text_input(
    "🔍 अभ्यासाचा विषय / प्रश्न टाका:",
    placeholder="उदा. Pitta Dosha types and functions किंवा Ashwagandha pharmacology"
)

generate_btn = st.button("🚀 सविस्तर अभ्यास नोट्स तयार करा", type="primary", use_container_width=True)

# --- Generation Logic ---
if generate_btn:
    if not topic.strip():
        st.warning("⚠️ कृपया अभ्यासाचा विषय किंवा प्रश्न प्रविष्ट करा.")
    else:
        system_instruction = f"""
        You are a senior Ayurveda Acharya and BAMS Exam Paper Evaluator according to NCISM standards.
        Subject: {subject}
        Topic: {topic}
        Language: {language_preference}

        Generate detailed, high-yield, structured revision notes:
        1. NEVER create ASCII diagrams or text tree boxes (avoid '|---' and box drawings).
        2. Format Sanskrit Shlokas strictly inside blockquotes (> "Shloka").
        3. Highlight key terms, anatomical words, and keywords in **Bold**.
        4. Structure strictly into:
           - # 🌿 {topic} - परिपूर्ण अभ्यास नोट्स
           - ## १. निरुक्ती, व्याख्या आणि मूळ संदर्भ श्लोक (अचूक पदच्छेद, अन्वय व अर्थ)
           - ## २. सविस्तर वर्गीकरण, गुण, कर्म व प्रकार (स्थान व कार्यासह सुटसुटीत बुलेट पॉईंट्स)
           - ## ३. आधुनिक वैद्यकशास्त्राशी तुलना (Modern Medical Correlation)
           - ## ४. चिकित्सा सूत्र व उपयुक्त औषधी कल्प
           - ## ५. परीक्षेसाठी महत्त्वाचे मुद्दे आणि ३-४ हमखास व्हायव्हा (Viva) प्रश्न व उत्तरे
        """

        notes_text = ""
        success_flag = False

        models_to_try = [
            'gemini-2.5-flash',
            'models/gemini-3.6-flash',
            'models/gemini-2.5-pro'
        ]

        with st.spinner("⚡ AI आयुर्वेद तज्ज्ञ तुमच्यासाठी संपूर्ण नोट्स एकत्र तयार करत आहे..."):
            for model_name in models_to_try:
                try:
                    response = client.models.generate_content(
                        model=model_name,
                        contents=system_instruction
                    )
                    if response and response.text:
                        notes_text = response.text
                        success_flag = True
                        break
                except Exception:
                    time.sleep(1)
                    continue

        if success_flag:
            st.success("✅ सर्व श्लोक आणि मुद्द्यांसह संपूर्ण नोट्स तयार झाल्या आहेत!")
            
            st.markdown('<div class="notes-box">', unsafe_allow_html=True)
            st.markdown(notes_text)
            st.markdown('</div>', unsafe_allow_html=True)
            
            st.markdown("<br>", unsafe_allow_html=True)
            doc_html = create_printable_html_doc(subject, topic, notes_text)
            st.download_button(
                label="📥 सुंदर PDF / प्रिंट फॉरमॅट डाऊनलोड करा (.pdf)",
                data=doc_html.encode('utf-8'),
                file_name=f"{topic.replace(' ', '_')}_BAMS_Notes.html",
                mime="text/html",
                use_container_width=True
            )
        else:
            st.error("गुगल सर्व्हरवर सध्या भार आहे. कृपया ५ सेकंद थांबा आणि पुन्हा बटण दाबा.")

# --- Footer ---
st.markdown("""
<div class="app-footer">
    🌿 <strong>BAMS AI Study Companion</strong> | विकसित केले: <strong>Avishkar Alashe</strong> (तुमच्या सेवेसाठी 🙏)
</div>
""", unsafe_allow_html=True)
