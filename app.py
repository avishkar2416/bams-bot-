import streamlit as st
from google import genai
import markdown
import time

# --- Page Setup ---
st.set_page_config(
    page_title="AyurVeda AI | Avishkar Alase",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- Ultra-Futuristic Design & Button/Card Animations ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=Noto+Sans+Devanagari:wght@400;600;700;800&display=swap');

    * {
        font-family: 'Noto Sans Devanagari', 'Plus Jakarta Sans', sans-serif !important;
    }

    /* Dynamic Fluid Canvas */
    .stApp {
        background: linear-gradient(-45deg, #f0fdf4, #e6fcf5, #f8fafc, #ecfdf5);
        background-size: 400% 400%;
        animation: gradientShift 14s ease infinite;
    }

    @keyframes gradientShift {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }

    @keyframes cardEntrance {
        0% { opacity: 0; transform: translateY(24px) scale(0.97); }
        100% { opacity: 1; transform: translateY(0) scale(1); }
    }

    @keyframes floatIcon {
        0% { transform: translateY(0px) rotate(0deg); }
        50% { transform: translateY(-4px) rotate(4deg); }
        100% { transform: translateY(0px) rotate(0deg); }
    }

    @keyframes shineSweep {
        0% { transform: translateX(-150%) skewX(-25deg); }
        40% { transform: translateX(150%) skewX(-25deg); }
        100% { transform: translateX(150%) skewX(-25deg); }
    }

    @keyframes pulseAura {
        0% { box-shadow: 0 0 0 0 rgba(16, 185, 129, 0.45); }
        70% { box-shadow: 0 0 0 14px rgba(16, 185, 129, 0); }
        100% { box-shadow: 0 0 0 0 rgba(16, 185, 129, 0); }
    }

    label, p, span, div {
        color: #0f172a !important;
    }

    /* Top Navbar */
    .premium-navbar {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 14px 22px;
        background: rgba(255, 255, 255, 0.88) !important;
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border: 1.5px solid rgba(255, 255, 255, 0.9);
        border-radius: 20px;
        margin-bottom: 24px;
        box-shadow: 0 10px 30px -10px rgba(5, 150, 105, 0.12);
        animation: cardEntrance 0.6s cubic-bezier(0.16, 1, 0.3, 1);
    }
    
    .nav-brand {
        display: flex;
        align-items: center;
        gap: 12px;
    }
    .nav-logo {
        background: linear-gradient(135deg, #059669 0%, #10b981 100%);
        color: white !important;
        width: 42px;
        height: 42px;
        border-radius: 12px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 22px;
        animation: floatIcon 4s ease-in-out infinite;
        box-shadow: 0 6px 18px rgba(16, 185, 129, 0.35);
    }
    .brand-title {
        font-size: 19px;
        font-weight: 800;
        background: linear-gradient(135deg, #064e3b 0%, #047857 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 0;
        line-height: 1.1;
    }
    .brand-tag {
        font-size: 9.5px;
        font-weight: 800;
        color: #059669 !important;
        letter-spacing: 0.08em;
        text-transform: uppercase;
    }

    /* Ultra-Professional Top-Right Signature Badge */
    .vip-creator-card {
        position: relative;
        overflow: hidden;
        display: flex;
        align-items: center;
        gap: 10px;
        background: linear-gradient(135deg, #ffffff 0%, #f0fdf4 100%) !important;
        border: 1.5px solid #a7f3d0;
        padding: 8px 16px;
        border-radius: 16px;
        box-shadow: 0 4px 20px rgba(16, 185, 129, 0.15);
        cursor: default;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    }
    
    .vip-creator-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 60%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.8), transparent);
        animation: shineSweep 3.8s ease-in-out infinite;
    }

    .vip-creator-card:hover {
        transform: translateY(-2px) scale(1.03);
        border-color: #34d399;
        box-shadow: 0 8px 25px rgba(5, 150, 105, 0.25);
    }

    .vip-avatar {
        width: 34px;
        height: 34px;
        border-radius: 10px;
        background: linear-gradient(135deg, #064e3b 0%, #059669 100%);
        color: white !important;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 15px;
        font-weight: 800;
        box-shadow: 0 4px 10px rgba(5, 150, 105, 0.3);
    }

    .vip-name {
        font-size: 14px;
        font-weight: 800;
        letter-spacing: -0.01em;
        background: linear-gradient(135deg, #064e3b 0%, #047857 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        display: flex;
        align-items: center;
        gap: 5px;
    }

    .verified-tick {
        background: #10b981;
        color: white !important;
        font-size: 9px;
        width: 15px;
        height: 15px;
        border-radius: 50%;
        display: inline-flex;
        align-items: center;
        justify-content: center;
        box-shadow: 0 2px 6px rgba(16, 185, 129, 0.4);
    }

    /* 3D Hero Banner */
    .hero-banner {
        background: linear-gradient(135deg, #064e3b 0%, #065f46 50%, #047857 100%) !important;
        padding: 32px 28px;
        border-radius: 22px;
        margin-bottom: 26px;
        box-shadow: 0 20px 45px -12px rgba(4, 120, 87, 0.45);
        border: 1px solid rgba(255, 255, 255, 0.2);
        animation: cardEntrance 0.7s cubic-bezier(0.16, 1, 0.3, 1);
        position: relative;
        overflow: hidden;
    }
    .hero-banner::before {
        content: '';
        position: absolute;
        width: 250px;
        height: 250px;
        background: radial-gradient(circle, rgba(16, 185, 129, 0.35) 0%, transparent 70%);
        top: -80px;
        right: -60px;
        border-radius: 50%;
    }
    .hero-banner * {
        color: #ffffff !important;
    }
    .hero-tag {
        display: inline-block;
        background: rgba(255, 255, 255, 0.18);
        backdrop-filter: blur(8px);
        padding: 5px 14px;
        border-radius: 100px;
        font-size: 11px;
        font-weight: 700;
        margin-bottom: 12px;
        border: 1px solid rgba(255, 255, 255, 0.25);
    }
    .hero-title {
        font-size: 28px;
        font-weight: 800;
        margin: 0 0 8px 0;
        letter-spacing: -0.02em;
    }
    .hero-desc {
        font-size: 14px;
        line-height: 1.65;
        opacity: 0.95;
        margin: 0;
    }

    /* Control Panel Card */
    .control-panel {
        background: rgba(255, 255, 255, 0.88) !important;
        backdrop-filter: blur(16px);
        border: 1.5px solid #ffffff;
        border-radius: 22px;
        padding: 26px;
        box-shadow: 0 12px 35px rgba(0, 0, 0, 0.04);
        margin-bottom: 26px;
        animation: cardEntrance 0.8s cubic-bezier(0.16, 1, 0.3, 1);
    }

    /* Inputs Micro-Interactions */
    div[data-baseweb="select"] > div,
    div[data-baseweb="input"] > div {
        background-color: #ffffff !important;
        border: 1.5px solid #cbd5e1 !important;
        border-radius: 14px !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
    }
    div[data-baseweb="select"] > div:hover,
    div[data-baseweb="input"] > div:hover {
        border-color: #059669 !important;
        transform: translateY(-2px);
        box-shadow: 0 6px 18px rgba(5, 150, 105, 0.1) !important;
    }

    /* ULTRA ANIMATED BUTTONS */
    div.stButton > button, div[data-testid="stDownloadButton"] > button {
        background: linear-gradient(135deg, #059669 0%, #047857 50%, #064e3b 100%) !important;
        color: #ffffff !important;
        border: none !important;
        border-radius: 16px !important;
        padding: 16px 30px !important;
        font-size: 16.5px !important;
        font-weight: 800 !important;
        letter-spacing: -0.01em !important;
        box-shadow: 0 10px 30px -4px rgba(5, 150, 105, 0.45) !important;
        transition: all 0.35s cubic-bezier(0.4, 0, 0.2, 1) !important;
        animation: pulseAura 2.5s infinite;
        position: relative !important;
        overflow: hidden !important;
        cursor: pointer !important;
    }

    div.stButton > button:hover, div[data-testid="stDownloadButton"] > button:hover {
        transform: translateY(-4px) scale(1.015) !important;
        box-shadow: 0 16px 38px -4px rgba(5, 150, 105, 0.6) !important;
    }

    div.stButton > button:active, div[data-testid="stDownloadButton"] > button:active {
        transform: translateY(2px) scale(0.96) !important;
    }

    /* Output Canvas Card */
    .notes-box {
        background: #ffffff !important;
        border: 1px solid #e2e8f0;
        border-radius: 24px;
        padding: 38px 32px;
        box-shadow: 0 20px 50px rgba(0, 0, 0, 0.05);
        margin-top: 28px;
        animation: cardEntrance 0.8s cubic-bezier(0.16, 1, 0.3, 1) forwards;
        line-height: 1.9;
    }
    .notes-box h1 {
        color: #064e3b !important;
        font-size: 25px;
        font-weight: 800;
        border-bottom: 2px solid #ecfdf5;
        padding-bottom: 10px;
        margin-top: 15px;
    }
    .notes-box h2 {
        color: #047857 !important;
        font-size: 20px;
        font-weight: 700;
        margin-top: 28px;
    }
    .notes-box h3 {
        color: #059669 !important;
        font-size: 17px;
        margin-top: 20px;
    }
    .notes-box blockquote {
        background: #f0fdf4 !important;
        border-left: 5px solid #10b981;
        padding: 16px 24px;
        border-radius: 0 16px 16px 0;
        margin: 20px 0;
        transition: transform 0.3s ease;
    }
    .notes-box blockquote:hover {
        transform: translateX(6px);
    }
    .notes-box blockquote * {
        color: #065f46 !important;
        font-weight: 600;
    }

    /* Footer */
    .app-footer {
        text-align: center;
        padding: 40px 10px 15px 10px;
        font-size: 13.5px;
        color: #64748b !important;
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)

# --- API Key Configuration ---
api_key = st.secrets.get("GEMINI_API_KEY", "")

if not api_key:
    st.error("⚠️ कृपया Settings > Secrets मध्ये तुमची GEMINI_API_KEY कॉन्फिगर करा.")
    st.stop()

client = genai.Client(api_key=api_key)

# --- Printable Clean Document ---
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
            @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+Devanagari:wght@400;600;700;800&family=Plus+Jakarta+Sans:wght@600;700;800&display=swap');
            body {{
                font-family: 'Noto Sans Devanagari', 'Plus Jakarta Sans', Arial, sans-serif;
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
                border-radius: 18px;
                padding: 26px 32px;
                margin-bottom: 35px;
            }}
            .header-banner h2 {{ margin: 0 0 6px 0; color: #ffffff; font-size: 24px; font-weight: 800; }}
            .header-banner p {{ margin: 0; font-size: 14px; opacity: 0.95; color: #ffffff; }}
            h1 {{ color: #064e3b; border-bottom: 2px solid #e2e8f0; padding-bottom: 8px; margin-top: 25px; }}
            h2 {{ color: #047857; margin-top: 30px; font-size: 20px; }}
            h3 {{ color: #059669; margin-top: 20px; }}
            blockquote {{
                background: #f0fdf4;
                border-left: 5px solid #10b981;
                margin: 20px 0;
                padding: 16px 22px;
                border-radius: 0 12px 12px 0;
                font-weight: 600;
                color: #065f46;
            }}
            strong {{ color: #0f172a; font-weight: 700; }}
            ul, ol {{ padding-left: 22px; margin: 12px 0; }}
            li {{ margin-bottom: 8px; }}
            .print-btn {{
                background: linear-gradient(135deg, #059669 0%, #047857 100%);
                color: white;
                padding: 14px 32px;
                font-size: 15px;
                font-weight: 700;
                border: none;
                border-radius: 12px;
                cursor: pointer;
            }}
            .doc-footer {{
                margin-top: 50px;
                border-top: 1px solid #e2e8f0;
                padding-top: 20px;
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
            <p>🌿 <strong>BAMS AI Study Companion</strong> | Developed by <strong>Avishkar Alase</strong></p>
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

# --- Top Navigation Bar with Ultra-Professional VIP Creator Card ---
st.markdown("""
<div class="premium-navbar">
    <div class="nav-brand">
        <div class="nav-logo">🌿</div>
        <div>
            <div class="brand-title">AyurVeda AI</div>
            <div class="brand-tag">NCISM Curriculum Engine</div>
        </div>
    </div>
    <div class="vip-creator-card">
        <div class="vip-avatar">A</div>
        <div class="vip-name">
            Avishkar Alase <span class="verified-tick">✓</span>
        </div>
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

# --- Control Panel Card ---
st.markdown('<div class="control-panel">', unsafe_allow_html=True)

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

        with st.spinner("⚡ AI आयुर्वेद तज्ज्ञ तुमच्यासाठी संपूर्ण नोट्स तयार करत आहे..."):
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
            st.balloons()
            st.success("✅ सर्व श्लोक आणि मुद्द्यांसह संपूर्ण नोट्स तयार झाल्या आहेत!")
            
            # Notes Display Card
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

# --- Bottom Footer Branding ---
st.markdown("""
<div class="app-footer">
    🌿 <strong>BAMS AI Study Companion</strong> | Developed by <strong>Avishkar Alase</strong>
</div>
""", unsafe_allow_html=True)
