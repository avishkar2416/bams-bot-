import streamlit as st
from google import genai
import markdown
import time

# --- Page Setup ---
st.set_page_config(
    page_title="AyurVeda AI | BAMS Clinical Companion",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- High-End Premium Web UI Styling ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=Noto+Sans+Devanagari:wght@400;500;600;700&display=swap');

    /* Global Base */
    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', 'Noto Sans Devanagari', -apple-system, sans-serif;
        color: #1e293b;
    }
    .stApp {
        background: radial-gradient(circle at top right, #f0fdf4 0%, #f8fafc 40%, #ffffff 100%);
    }

    /* Premium Navigation Header */
    .premium-navbar {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 14px 28px;
        background: rgba(255, 255, 255, 0.85);
        backdrop-filter: blur(16px);
        -webkit-backdrop-filter: blur(16px);
        border: 1px solid rgba(226, 232, 240, 0.8);
        border-radius: 18px;
        margin-bottom: 30px;
        box-shadow: 0 8px 30px rgba(0, 0, 0, 0.04);
    }
    .nav-brand {
        display: flex;
        align-items: center;
        gap: 12px;
    }
    .nav-logo {
        background: linear-gradient(135deg, #059669 0%, #10b981 100%);
        color: white;
        width: 44px;
        height: 44px;
        border-radius: 12px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 22px;
        box-shadow: 0 4px 12px rgba(16, 185, 129, 0.35);
    }
    .brand-title {
        font-size: 20px;
        font-weight: 800;
        letter-spacing: -0.02em;
        background: linear-gradient(135deg, #0f172a 0%, #334155 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 0;
    }
    .brand-tag {
        font-size: 11px;
        font-weight: 700;
        text-transform: uppercase;
        color: #059669;
        letter-spacing: 0.08em;
    }

    /* Owner Badge */
    .owner-pill {
        display: flex;
        flex-direction: column;
        align-items: flex-end;
        background: #ecfdf5;
        border: 1px solid #a7f3d0;
        padding: 6px 14px;
        border-radius: 12px;
    }
    .owner-title {
        font-size: 12px;
        font-weight: 800;
        color: #065f46;
    }
    .owner-subtitle {
        font-size: 10px;
        color: #059669;
        font-weight: 600;
    }

    /* Hero Banner */
    .hero-card {
        background: linear-gradient(135deg, #064e3b 0%, #047857 60%, #059669 100%);
        padding: 40px 36px;
        border-radius: 24px;
        color: white;
        margin-bottom: 35px;
        box-shadow: 0 20px 40px -15px rgba(5, 150, 105, 0.35);
        position: relative;
        overflow: hidden;
    }
    .hero-card::after {
        content: '';
        position: absolute;
        top: -60px;
        right: -60px;
        width: 220px;
        height: 220px;
        background: radial-gradient(circle, rgba(255,255,255,0.18) 0%, transparent 70%);
        border-radius: 50%;
    }
    .hero-badge {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        background: rgba(255, 255, 255, 0.18);
        border: 1px solid rgba(255, 255, 255, 0.25);
        padding: 5px 14px;
        border-radius: 100px;
        font-size: 12px;
        font-weight: 600;
        letter-spacing: 0.03em;
        margin-bottom: 14px;
    }
    .hero-title {
        font-size: 32px;
        font-weight: 800;
        line-height: 1.25;
        margin: 0 0 10px 0;
        letter-spacing: -0.02em;
    }
    .hero-desc {
        font-size: 15px;
        line-height: 1.6;
        opacity: 0.9;
        margin: 0;
        max-width: 680px;
    }

    /* Control Panel Box */
    .control-box {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 20px;
        padding: 28px;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.03);
        margin-bottom: 35px;
    }

    /* Generated Notes Card */
    .output-card {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 24px;
        padding: 40px;
        box-shadow: 0 15px 45px rgba(0, 0, 0, 0.05);
        margin-top: 30px;
        line-height: 1.85;
    }
    .output-card h1, .output-card h2 {
        color: #064e3b;
        border-bottom: 2px solid #ecfdf5;
        padding-bottom: 8px;
        margin-top: 30px;
        font-weight: 800;
    }
    .output-card h3 {
        color: #047857;
        margin-top: 22px;
        font-weight: 700;
    }
    .output-card blockquote {
        background: #f0fdf4;
        border-left: 5px solid #10b981;
        padding: 16px 22px;
        border-radius: 0 14px 14px 0;
        font-weight: 600;
        color: #065f46;
        margin: 20px 0;
    }
    .output-card strong {
        color: #0f172a;
        font-weight: 700;
    }

    /* Footer */
    .app-footer {
        text-align: center;
        padding: 30px 10px 10px 10px;
        color: #64748b;
        font-size: 13px;
    }
    .app-footer strong {
        color: #065f46;
    }
</style>
""", unsafe_allow_html=True)

# --- API Key Configuration ---
api_key = st.secrets.get("GEMINI_API_KEY", "")

if not api_key:
    st.error("⚠️ कृपया Settings > Secrets मध्ये तुमची GEMINI_API_KEY कॉन्फिगर करा.")
    st.stop()

client = genai.Client(api_key=api_key)

# --- High Quality Export Generator ---
def create_printable_html_doc(subject_name, topic_name, raw_content):
    html_content = markdown.markdown(raw_content, extensions=['extra', 'nl2br'])

    full_html = f"""
    <!DOCTYPE html>
    <html lang="mr">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>{topic_name} - BAMS Master Notes</title>
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@500;700&family=Noto+Sans+Devanagari:wght@400;600;700&display=swap');
            body {{
                font-family: 'Noto Sans Devanagari', 'Plus Jakarta Sans', -apple-system, sans-serif;
                line-height: 1.85;
                color: #1e293b;
                padding: 40px 24px;
                max-width: 860px;
                margin: auto;
                background-color: #ffffff;
            }}
            .header-banner {{
                background: linear-gradient(135deg, #064e3b 0%, #047857 100%);
                color: white;
                border-radius: 16px;
                padding: 24px 30px;
                margin-bottom: 30px;
            }}
            .header-banner h2 {{ margin: 0 0 6px 0; color: #ffffff; font-size: 24px; }}
            .header-banner p {{ margin: 0; font-size: 14px; opacity: 0.95; }}
            h1, h2 {{ color: #064e3b; border-bottom: 2px solid #e2e8f0; padding-bottom: 8px; margin-top: 30px; }}
            h3 {{ color: #047857; margin-top: 20px; }}
            blockquote {{
                background: #f0fdf4;
                border-left: 5px solid #10b981;
                margin: 18px 0;
                padding: 14px 20px;
                border-radius: 0 10px 10px 0;
                font-weight: 600;
                color: #065f46;
            }}
            strong {{ color: #0f172a; font-weight: 700; }}
            ul, ol {{ padding-left: 22px; margin: 12px 0; }}
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
                box-shadow: 0 6px 20px rgba(5, 150, 105, 0.3);
            }}
            .doc-footer {{
                margin-top: 40px;
                border-top: 1px solid #e2e8f0;
                padding-top: 15px;
                text-align: center;
                font-size: 12px;
                color: #64748b;
            }}
            @media print {{
                .no-print {{ display: none !important; }}
                body {{ padding: 0; }}
            }}
        </style>
    </head>
    <body>
        <div class="no-print" style="text-align: center; margin-bottom: 30px;">
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
            <p><strong>Created by Avishkar Alashe</strong> | BAMS AI Study Companion | तुमच्या सेवेसाठी 🙏</p>
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

# --- Navigation Bar ---
st.markdown("""
<div class="premium-navbar">
    <div class="nav-brand">
        <div class="nav-logo">🌿</div>
        <div>
            <div class="brand-title">AyurVeda AI</div>
            <div class="brand-tag">NCISM Curriculum Engine</div>
        </div>
    </div>
    <div class="owner-pill">
        <span class="owner-title">👨‍💻 Avishkar Alashe</span>
        <span class="owner-subtitle">तुमच्या सेवेसाठी 🙏</span>
    </div>
</div>
""", unsafe_allow_html=True)

# --- Hero Banner ---
st.markdown("""
<div class="hero-card">
    <div class="hero-badge">🎓 NCISM & University Exam Standard</div>
    <h1 class="hero-title">BAMS इंटेलिजंट स्टडी असिस्टंट</h1>
    <p class="hero-desc">अस्सल संहिता संदर्भ, संस्कृत श्लोक व अन्वय, मॉडर्न मेडिकल कोरिलेशन आणि हाय-स्कोरिंग क्लिनिकल नोट्स — सर्वकाही १-क्लिकमध्ये.</p>
</div>
""", unsafe_allow_html=True)

# --- Configuration Form Card ---
st.markdown('<div class="control-box">', unsafe_allow_html=True)

col1, col2 = st.columns([1.2, 1])

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
        "🌐 माध्यम (Language):",
        ["मराठी (संस्कृत श्लोक + सोपा अर्थ + मॉडर्न टर्म्स)", "English + Sanskrit Shlokas"],
        horizontal=True
    )

topic = st.text_input(
    "🔍 अभ्यासाचा विषय / प्रश्न टाका:",
    placeholder="उदा. Pitta Dosha types and functions, Ashwagandha pharmacology, किंवा Amavata Chikitsa"
)

generate_btn = st.button("🚀 सविस्तर अभ्यास नोट्स तयार करा", type="primary", use_container_width=True)

st.markdown('</div>', unsafe_allow_html=True)

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
            
            # Notes Display Card
            st.markdown('<div class="output-card">', unsafe_allow_html=True)
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

# --- Bottom Footer Branding ---
st.markdown("""
<div class="app-footer">
    <p>🌿 <strong>BAMS AI Study Companion</strong> | विकसित केले: <strong>Avishkar Alashe</strong> (तुमच्या सेवेसाठी 🙏)</p>
</div>
""", unsafe_allow_html=True)

