import streamlit as st
from google import genai
import markdown
import time

# --- Page Setup ---
st.set_page_config(
    page_title="AyurVeda AI | BAMS Enterprise Companion",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- Ultra-Premium CSS Design System ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=Noto+Sans+Devanagari:wght@400;500;600;700;800&display=swap');

    /* Global Base */
    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', 'Noto Sans Devanagari', -apple-system, sans-serif;
        color: #0f172a;
    }
    
    .stApp {
        background: radial-gradient(1200px 800px at 80% -10%, #ecfdf5 0%, #f8fafc 50%, #f0fdf4 100%);
        min-height: 100vh;
    }

    /* Main Container Padding */
    .block-container {
        padding-top: 2rem;
        padding-bottom: 4rem;
        max-width: 1100px;
    }

    /* Floating Ultra-Glass Navbar */
    .premium-navbar {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 16px 28px;
        background: rgba(255, 255, 255, 0.75);
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 255, 255, 0.9);
        border-radius: 20px;
        margin-bottom: 28px;
        box-shadow: 0 10px 30px -10px rgba(16, 185, 129, 0.12), 0 1px 3px rgba(0,0,0,0.05);
    }
    
    .nav-brand {
        display: flex;
        align-items: center;
        gap: 14px;
    }
    
    .nav-logo {
        background: linear-gradient(135deg, #059669 0%, #10b981 100%);
        color: white;
        width: 46px;
        height: 46px;
        border-radius: 14px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 24px;
        box-shadow: 0 8px 16px -4px rgba(16, 185, 129, 0.4);
        transition: transform 0.3s ease;
    }
    .nav-logo:hover {
        transform: rotate(10deg) scale(1.05);
    }
    
    .brand-title {
        font-size: 22px;
        font-weight: 800;
        letter-spacing: -0.03em;
        background: linear-gradient(135deg, #064e3b 0%, #047857 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 0;
        line-height: 1.1;
    }
    
    .brand-tag {
        font-size: 11px;
        font-weight: 700;
        text-transform: uppercase;
        color: #059669;
        letter-spacing: 0.08em;
    }

    /* Creator Signature Badge */
    .owner-pill {
        display: flex;
        align-items: center;
        gap: 12px;
        background: rgba(236, 253, 245, 0.8);
        border: 1px solid rgba(167, 243, 208, 0.8);
        padding: 8px 16px;
        border-radius: 14px;
        box-shadow: 0 2px 8px rgba(5, 150, 105, 0.06);
    }
    .owner-avatar {
        width: 32px;
        height: 32px;
        border-radius: 50%;
        background: linear-gradient(135deg, #047857, #10b981);
        color: white;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 14px;
        font-weight: bold;
    }
    .owner-meta {
        display: flex;
        flex-direction: column;
    }
    .owner-title {
        font-size: 13px;
        font-weight: 800;
        color: #064e3b;
    }
    .owner-subtitle {
        font-size: 10px;
        color: #059669;
        font-weight: 600;
    }

    /* Dynamic Hero Banner */
    .hero-card {
        background: linear-gradient(135deg, #064e3b 0%, #065f46 50%, #047857 100%);
        padding: 42px 40px;
        border-radius: 26px;
        color: white;
        margin-bottom: 30px;
        box-shadow: 0 20px 45px -15px rgba(4, 120, 87, 0.4);
        position: relative;
        overflow: hidden;
        border: 1px solid rgba(255, 255, 255, 0.15);
    }
    
    .hero-card::before {
        content: '';
        position: absolute;
        width: 300px;
        height: 300px;
        background: radial-gradient(circle, rgba(16, 185, 129, 0.3) 0%, transparent 70%);
        top: -100px;
        right: -80px;
        border-radius: 50%;
    }

    .hero-badge {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        background: rgba(255, 255, 255, 0.15);
        backdrop-filter: blur(8px);
        border: 1px solid rgba(255, 255, 255, 0.25);
        padding: 6px 14px;
        border-radius: 100px;
        font-size: 12px;
        font-weight: 700;
        letter-spacing: 0.04em;
        margin-bottom: 16px;
        color: #ecfdf5;
    }
    
    .hero-title {
        font-size: 34px;
        font-weight: 800;
        line-height: 1.25;
        margin: 0 0 12px 0;
        letter-spacing: -0.03em;
        color: #ffffff;
    }
    
    .hero-desc {
        font-size: 15px;
        line-height: 1.65;
        color: #e6f4ea;
        margin: 0;
        max-width: 720px;
        font-weight: 400;
    }

    /* Control Panel Card */
    .control-box {
        background: rgba(255, 255, 255, 0.9);
        backdrop-filter: blur(12px);
        border: 1px solid #e2e8f0;
        border-radius: 22px;
        padding: 30px;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.03);
        margin-bottom: 30px;
    }

    /* Streamlit Widget Enhancements */
    div[data-baseweb="select"] > div,
    div[data-baseweb="input"] > div {
        background-color: #f8fafc !important;
        border-radius: 14px !important;
        border: 1.5px solid #e2e8f0 !important;
        transition: all 0.2s ease-in-out !important;
    }
    div[data-baseweb="select"] > div:focus-within,
    div[data-baseweb="input"] > div:focus-within {
        border-color: #059669 !important;
        background-color: #ffffff !important;
        box-shadow: 0 0 0 4px rgba(5, 150, 105, 0.12) !important;
    }

    /* Primary CTA Button */
    div.stButton > button {
        background: linear-gradient(135deg, #059669 0%, #047857 100%) !important;
        color: #ffffff !important;
        border: none !important;
        border-radius: 14px !important;
        padding: 14px 28px !important;
        font-size: 16px !important;
        font-weight: 700 !important;
        letter-spacing: -0.01em !important;
        box-shadow: 0 8px 24px -4px rgba(5, 150, 105, 0.4) !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
    }
    div.stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 12px 30px -4px rgba(5, 150, 105, 0.5) !important;
    }

    /* High-End Output Notes Canvas */
    .output-card {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 24px;
        padding: 42px 45px;
        box-shadow: 0 20px 50px rgba(0, 0, 0, 0.05);
        margin-top: 35px;
        line-height: 1.9;
    }
    
    .output-card h1 {
        color: #064e3b;
        font-size: 26px;
        font-weight: 800;
        border-bottom: 2px solid #ecfdf5;
        padding-bottom: 12px;
        margin-top: 20px;
    }
    .output-card h2 {
        color: #047857;
        font-size: 20px;
        font-weight: 700;
        border-left: 4px solid #10b981;
        padding-left: 12px;
        margin-top: 30px;
    }
    .output-card h3 {
        color: #059669;
        font-size: 17px;
        font-weight: 700;
        margin-top: 22px;
    }
    
    .output-card blockquote {
        background: #f0fdf4;
        border-left: 4px solid #10b981;
        padding: 16px 24px;
        border-radius: 0 16px 16px 0;
        font-weight: 600;
        color: #065f46;
        margin: 22px 0;
        font-size: 15px;
        box-shadow: inset 0 2px 4px rgba(0,0,0,0.01);
    }
    
    .output-card strong {
        color: #0f172a;
        font-weight: 700;
    }

    /* Footer Branding */
    .app-footer {
        text-align: center;
        padding: 40px 10px 15px 10px;
        color: #64748b;
        font-size: 13px;
        font-weight: 500;
    }
    .app-footer strong {
        color: #064e3b;
    }
</style>
""", unsafe_allow_html=True)

# --- API Key Configuration ---
api_key = st.secrets.get("GEMINI_API_KEY", "")

if not api_key:
    st.error("⚠️ कृपया Settings > Secrets मध्ये तुमची GEMINI_API_KEY कॉन्फिगर करा.")
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
        <title>{topic_name} - BAMS Master Notes</title>
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@500;700;800&family=Noto+Sans+Devanagari:wght@400;600;700;800&display=swap');
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
                border-radius: 18px;
                padding: 26px 32px;
                margin-bottom: 35px;
            }}
            .header-banner h2 {{ margin: 0 0 6px 0; color: #ffffff; font-size: 24px; font-weight: 800; }}
            .header-banner p {{ margin: 0; font-size: 14px; opacity: 0.95; }}
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
                box-shadow: 0 6px 20px rgba(5, 150, 105, 0.3);
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
        <div class="owner-avatar">A</div>
        <div class="owner-meta">
            <span class="owner-title">Avishkar Alashe</span>
            <span class="owner-subtitle">तुमच्या सेवेसाठी 🙏</span>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# --- Hero Banner ---
st.markdown("""
<div class="hero-card">
    <div class="hero-badge">✨ NCISM Standard Study Matrix</div>
    <h1 class="hero-title">BAMS इंटेलिजंट स्टडी असिस्टंट</h1>
    <p class="hero-desc">अस्सल संहिता संदर्भ, अचूक संस्कृत श्लोक व अन्वय, मॉडर्न मेडिकल कोरिलेशन आणि हाय-स्कोरिंग क्लिनिकल नोट्स — सर्वकाही १-क्लिकमध्ये.</p>
</div>
""", unsafe_allow_html=True)

# --- Control Panel Card ---
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
