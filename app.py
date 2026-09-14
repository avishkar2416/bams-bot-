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

# --- Ultra-Futuristic Design & Button Animations ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=Noto+Sans+Devanagari:wght@400;600;700;800&display=swap');

    * {
        font-family: 'Noto Sans Devanagari', 'Plus Jakarta Sans', sans-serif !important;
    }

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

    /* Top-Right VIP Signature Card */
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
    }

    /* Tabs Styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 12px;
        margin-bottom: 24px;
    }
    .stTabs [data-baseweb="tab"] {
        background-color: #ffffff !important;
        border-radius: 14px !important;
        padding: 12px 22px !important;
        font-weight: 800 !important;
        border: 1.5px solid #cbd5e1 !important;
    }
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #064e3b 0%, #059669 100%) !important;
        border-color: #059669 !important;
        color: #ffffff !important;
    }
    .stTabs [aria-selected="true"] * {
        color: #ffffff !important;
    }

    /* 3D Hero Banner */
    .hero-banner {
        background: linear-gradient(135deg, #064e3b 0%, #065f46 50%, #047857 100%) !important;
        padding: 30px 26px;
        border-radius: 22px;
        margin-bottom: 24px;
        box-shadow: 0 20px 45px -12px rgba(4, 120, 87, 0.45);
        border: 1px solid rgba(255, 255, 255, 0.2);
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
    }
    .hero-title {
        font-size: 26px;
        font-weight: 800;
        margin: 0 0 8px 0;
    }
    .hero-desc {
        font-size: 13.8px;
        line-height: 1.6;
        opacity: 0.95;
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
    }

    /* Inputs Styling */
    div[data-baseweb="select"] > div,
    div[data-baseweb="input"] > div {
        background-color: #ffffff !important;
        border: 1.5px solid #cbd5e1 !important;
        border-radius: 14px !important;
    }

    /* Buttons */
    div.stButton > button, div[data-testid="stDownloadButton"] > button {
        background: linear-gradient(135deg, #059669 0%, #047857 50%, #064e3b 100%) !important;
        color: #ffffff !important;
        border: none !important;
        border-radius: 16px !important;
        padding: 16px 30px !important;
        font-size: 16.5px !important;
        font-weight: 800 !important;
        box-shadow: 0 10px 30px -4px rgba(5, 150, 105, 0.45) !important;
        transition: all 0.35s cubic-bezier(0.4, 0, 0.2, 1) !important;
        animation: pulseAura 2.5s infinite;
        cursor: pointer !important;
    }

    /* Notes Box & Table Styling */
    .notes-box {
        background: #ffffff !important;
        border: 1px solid #e2e8f0;
        border-radius: 24px;
        padding: 38px 32px;
        box-shadow: 0 20px 50px rgba(0, 0, 0, 0.05);
        margin-top: 28px;
        line-height: 1.9;
    }
    .notes-box table {
        width: 100% !important;
        border-collapse: collapse !important;
        margin: 20px 0 !important;
        border: 2px solid #064e3b !important;
        border-radius: 10px !important;
    }
    .notes-box th {
        background-color: #ecfdf5 !important;
        color: #064e3b !important;
        font-weight: 800 !important;
        border: 1px solid #cbd5e1 !important;
        padding: 12px 14px !important;
    }
    .notes-box td {
        border: 1px solid #cbd5e1 !important;
        padding: 10px 14px !important;
        color: #0f172a !important;
    }
    .notes-box blockquote {
        background: #f0fdf4 !important;
        border-left: 5px solid #10b981;
        padding: 16px 24px;
        border-radius: 0 16px 16px 0;
        margin: 20px 0;
    }

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

# Helper function for safe model calling (Flash First)
def ask_gemini(system_prompt):
    models_to_try = [
        'gemini-2.5-flash',
        'models/gemini-3.6-flash',
        'models/gemini-2.5-pro'
    ]
    for model_name in models_to_try:
        try:
            res = client.models.generate_content(
                model=model_name,
                contents=system_prompt
            )
            if res and res.text:
                return res.text
        except Exception:
            time.sleep(1)
            continue
    raise RuntimeError("गुगल सर्व्हर व्यस्त आहे. कृपया पुन्हा प्रयत्न करा.")

# --- Document Generator (With One-Click Image Download & PDF Print) ---
def create_exportable_doc(title_tag, subtitle_info, raw_content):
    html_content = markdown.markdown(raw_content, extensions=['extra', 'tables', 'nl2br'])
    return f"""
    <!DOCTYPE html>
    <html lang="mr">
    <head>
        <meta charset="UTF-8">
        <title>{title_tag} - AyurVeda Master Doc</title>
        <script src="https://cdnjs.cloudflare.com/ajax/libs/html2canvas/1.4.1/html2canvas.min.js"></script>
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+Devanagari:wght@400;600;700;800&family=Plus+Jakarta+Sans:wght@600;700;800&display=swap');
            body {{ font-family: 'Noto Sans Devanagari', 'Plus Jakarta Sans', Arial, sans-serif; line-height: 1.85; color: #1e293b; padding: 30px 20px; max-width: 900px; margin: auto; background-color: #f8fafc; }}
            .capture-area {{ background: #ffffff; padding: 35px 30px; border-radius: 20px; border: 1.5px solid #e2e8f0; box-shadow: 0 10px 30px rgba(0,0,0,0.05); }}
            .header-banner {{ background: linear-gradient(135deg, #064e3b 0%, #047857 100%); color: white; border-radius: 16px; padding: 24px 28px; margin-bottom: 28px; }}
            .header-banner h2 {{ margin: 0 0 6px 0; color: #ffffff; font-size: 24px; font-weight: 800; }}
            .header-banner p {{ margin: 0; font-size: 13.5px; color: #ffffff; opacity: 0.95; }}
            table {{ width: 100%; border-collapse: collapse; margin: 20px 0; border: 2px solid #064e3b; border-radius: 8px; overflow: hidden; }}
            th, td {{ border: 1px solid #cbd5e1; padding: 10px 12px; text-align: left; }}
            th {{ background-color: #ecfdf5; color: #064e3b; font-weight: bold; }}
            blockquote {{ background: #f0fdf4; border-left: 5px solid #10b981; margin: 18px 0; padding: 14px 20px; color: #065f46; font-weight: bold; border-radius: 0 10px 10px 0; }}
            
            /* Action Buttons Bar */
            .action-bar {{ display: flex; justify-content: center; gap: 14px; margin-bottom: 25px; flex-wrap: wrap; }}
            .btn-img {{ background: linear-gradient(135deg, #0284c7 0%, #0369a1 100%); color: white; padding: 14px 24px; font-size: 15px; font-weight: 700; border: none; border-radius: 12px; cursor: pointer; box-shadow: 0 6px 18px rgba(2, 132, 199, 0.35); }}
            .btn-pdf {{ background: linear-gradient(135deg, #059669 0%, #047857 100%); color: white; padding: 14px 24px; font-size: 15px; font-weight: 700; border: none; border-radius: 12px; cursor: pointer; box-shadow: 0 6px 18px rgba(5, 150, 105, 0.35); }}
            
            @media print {{
                .no-print {{ display: none !important; }}
                body {{ padding: 0; background: #ffffff; }}
                .capture-area {{ box-shadow: none; border: none; padding: 0; }}
            }}
        </style>
    </head>
    <body>
        <div class="no-print action-bar">
            <button class="btn-img" onclick="downloadAsImage()">📸 फोटो (Image / PNG) म्हणून सेव्ह करा</button>
            <button class="btn-pdf" onclick="window.print()">📄 थेट PDF सेव्ह करा / प्रिंट करा</button>
        </div>

        <div class="capture-area" id="notesCapture">
            <div class="header-banner">
                <h2>🌿 {title_tag}</h2>
                <p>{subtitle_info}</p>
            </div>
            <div>{html_content}</div>
            <p style="text-align:center; margin-top:40px; font-size:13px; color:#64748b; border-top: 1px solid #e2e8f0; padding-top: 15px;">
                🌿 <strong>AyurVeda AI</strong> | Developed by <strong>Avishkar Alase</strong>
            </p>
        </div>

        <script>
            function downloadAsImage() {{
                const element = document.getElementById('notesCapture');
                html2canvas(element, {{ scale: 2, useCORS: true }}).then(canvas => {{
                    const link = document.createElement('a');
                    link.download = '{title_tag.replace(" ", "_")}_Notes.png';
                    link.href = canvas.toDataURL('image/png');
                    link.click();
                }});
            }}
        </script>
    </body>
    </html>
    """

# --- Top Navigation Bar ---
st.markdown("""
<div class="premium-navbar">
    <div class="nav-brand">
        <div class="nav-logo">🌿</div>
        <div>
            <div class="brand-title">AyurVeda AI</div>
            <div class="brand-tag">NCISM Curriculum & Pharmacy Engine</div>
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

# --- 2 Main Tabs ---
tab1, tab2 = st.tabs([
    "📖 BAMS स्टडी नोट्स (Syllabus Notes)",
    "🧪 औषध घटक व निर्माण विधी (Medicine & Manufacturing)"
])

# =========================================================================
# TAB 1: SYLLABUS STUDY NOTES
# =========================================================================
with tab1:
    st.markdown("""
    <div class="hero-banner">
        <div class="hero-tag">✨ NCISM Standard Study Matrix</div>
        <div class="hero-title">BAMS इंटेलिजंट स्टडी असिस्टंट</div>
        <div class="hero-desc">अस्सल संहिता संदर्भ, टॉपर स्टाईल फ्लोचार्ट्स, संप्राप्ती चक्र, तुलनात्मक तक्ते आणि हमखास परीक्षेतील की-पॉइंट्स.</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="control-panel">', unsafe_allow_html=True)
    row1_col1, row1_col2 = st.columns([1, 1.2])

    with row1_col1:
        bams_year = st.selectbox(
            "🎓 BAMS वर्ष निवडा (Academic Year):",
            [
                "BAMS 1st Professional (प्रथम वर्ष)",
                "BAMS 2nd Professional (द्वितीय वर्ष)",
                "BAMS 3rd Professional (तृतीय वर्ष)",
                "BAMS Final Professional (अंतिम वर्ष)"
            ]
        )

    with row1_col2:
        subject = st.selectbox(
            "📚 विषय निवडा (Select Subject):",
            [
                "Agada Tantra & Vyavahara Ayurveda (अगद तंत्र)",
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
                "Kaumarbhritya (कौमारभृत्य)"
            ]
        )

    row2_col1, row2_col2 = st.columns([1.2, 1])

    with row2_col1:
        study_mode = st.selectbox(
            "🎯 अभ्यासाचा प्रकार निवडा (Study Mode):",
            [
                "📋 Topper Hand-written Chart & Table Notes (फ्लोचार्ट + तक्ता नोट्स)",
                "📖 Comprehensive Notes (संपूर्ण सविस्तर अभ्यास नोट्स)",
                "📜 Only Shlokas & Meanings (फक्त मूळ श्लोक, अन्वय व अर्थ)",
                "📝 10-Mark LAQ Answer Format (दीर्घोत्तरी प्रश्न-उत्तर फॉरमॅट)",
                "⚡ Quick Revision / Viva Voce Points (तोंडी परीक्षेसाठी महत्त्वाचे मुद्दे)",
                "🩺 Clinical Chikitsa & Formulations (क्लिनिकल चिकित्सा व औषधी कल्प)"
            ]
        )

    with row2_col2:
        language_preference = st.radio(
            "🌐 माध्यम (Language):",
            ["English + Sanskrit (फोटोमधील टॉपर स्टाईल)", "मराठी (संस्कृत श्लोक + सोपा अर्थ + मॉडर्न टर्म्स)"],
            horizontal=True,
            key="lang_notes"
        )

    topic = st.text_input(
        "🔍 अभ्यासाचा विषय / प्रश्न टाका:",
        placeholder="उदा. Role of Garavisha and Dooshivisha in Manifestation of Diseases किंवा Pitta Dosha Prakar"
    )

    generate_notes_btn = st.button("🚀 सविस्तर अभ्यास नोट्स तयार करा", key="btn_notes", use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    if generate_notes_btn:
        if not topic.strip():
            st.warning("⚠️ कृपया अभ्यासाचा विषय किंवा प्रश्न प्रविष्ट करा.")
        else:
            if "Topper Hand-written Chart" in study_mode:
                system_instruction = f"""
                You are a university topper and professor in Ayurveda (BAMS/MD).
                Subject: {subject}
                Topic: {topic}
                Language: {language_preference}

                Create study notes EXACTLY matching the handwritten topper note layout:
                1. Main Title with Subject Tag:
                   # 🌿 {topic}
                   `{subject} | (BAMS / MD Exam Note)`
                2. Two Core Entities / Concept Definition Boxes:
                   - Clearly define entity ① and entity ②.
                3. Pathogenesis / Samprapti Step-by-Step Flowchart:
                   Present using clean text flow blocks with arrows:
                   [Step 1: Nidana / Intake]
                   ↓
                   [Step 2: Agni Dushti]
                   ↓
                   [Step 3: Ama & Dosha Vitiation]
                   ↓
                   [Step 4: Srotodushti]
                   ↓
                   [Step 5: Manifestation of Disease]
                4. Clinical Signs & Manifestations (Diseases / Lakshana):
                   - Bulleted list categorized into Agnimandya, Twak Vikara, and Systemic.
                5. Key Concept Box (> Blockquote)
                6. Contemporary / Modern Correlation Box
                7. Comparison Table (Difference in Disease Manifestation):
                   | Feature | Entity 1 | Entity 2 |
                   | :--- | :--- | :--- |
                8. Exam Line / Punch Line: One memorable final exam sentence.
                """
            else:
                system_instruction = f"""
                You are a senior Ayurveda Acharya according to NCISM standards.
                Academic Level: {bams_year}, Subject: {subject}, Study Mode: {study_mode}, Topic: {topic}, Language: {language_preference}.
                Generate tailored, high-yield study material strictly aligned with '{study_mode}'.
                - Format Sanskrit Shlokas inside blockquotes (> "Shloka").
                - Bold key terms.
                - Follow authentic NCISM syllabus structure.
                """

            with st.spinner(f"⚡ AI आयुर्वेद तज्ज्ञ '{study_mode}' नुसार नोट्स तयार करत आहे..."):
                try:
                    notes_text = ask_gemini(system_instruction)
                    st.balloons()
                    st.success("✅ नोट्स यशस्वीरीत्या तयार झाल्या आहेत!")
                    st.markdown('<div class="notes-box">', unsafe_allow_html=True)
                    st.markdown(notes_text)
                    st.markdown('</div>', unsafe_allow_html=True)

                    st.markdown("<br>", unsafe_allow_html=True)
                    doc_export = create_exportable_doc(topic, f"{bams_year} | {subject} | {study_mode}", notes_text)
                    
                    st.download_button(
                        label="📥 फोटो (Image) किंवा PDF सेव्ह करा (Download Suite)",
                        data=doc_export.encode('utf-8'),
                        file_name=f"{topic.replace(' ', '_')}_Export_Suite.html",
                        mime="text/html",
                        use_container_width=True
                    )
                except Exception as e:
                    st.error(f"त्रुटी: {e}")

# =========================================================================
# TAB 2: MEDICINE FORMULATION & MANUFACTURING (औषध निर्माण विधी)
# =========================================================================
with tab2:
    st.markdown("""
    <div class="hero-banner" style="background: linear-gradient(135deg, #0f766e 0%, #0d9488 100%) !important;">
        <div class="hero-tag">🧪 रसशास्त्र व भैषज्य कल्पना स्पेशल</div>
        <div class="hero-title">आयुर्वेदिक औषध घटक व सविस्तर निर्माण विधी</div>
        <div class="hero-desc">कोणतीही आयुर्वेदिक गोळी, वटी, चूर्ण, आसव-अरिष्ट, भस्म किंवा घृत कशापासून बनवले आहे आणि कसे तयार करायचे ते सोप्या स्टेप्समध्ये शिका.</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="control-panel">', unsafe_allow_html=True)
    m_col1, m_col2 = st.columns([1.2, 1])

    with m_col1:
        dosage_form = st.selectbox(
            "🏺 औषधाचा प्रकार (Dosage Form):",
            [
                "Vati / Gutika (गोळी / वटी)",
                "Churna (चूर्ण)",
                "Asava & Arishta (आसव व अरिष्ट)",
                "Taila / Ghrita (सिद्ध तेल व घृत)",
                "Bhasma & Pishti (भस्म व पिष्टी)",
                "Avaleha / Paka (अवलेह / पाक)",
                "Kashaya / Kwath (काढा / क्वाथ)",
                "Lepa / Malahar (लेप / मलम)"
            ]
        )

    with m_col2:
        m_lang = st.radio(
            "🌐 शिकवण्याची भाषा:",
            ["मराठी (सविस्तर मराठी कृती + प्रमाण)", "English + Sanskrit Terms"],
            horizontal=True,
            key="lang_med"
        )

    medicine_name = st.text_input(
        "💊 गोळी किंवा औषधाचे नाव टाका:",
        placeholder="उदा. आरोग्यवर्धिनी वटी, चंद्रप्रभावटी, सितोपलादी चूर्ण, किंवा त्रिभुवन कीर्ति रस"
    )

    generate_med_btn = st.button("🔬 औषध घटक व बनवण्याची पूर्ण कृती शिका", key="btn_med", use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    if generate_med_btn:
        if not medicine_name.strip():
            st.warning("⚠️ कृपया औषधाचे नाव टाका.")
        else:
            med_prompt = f"""
            You are a master Rasashastra and Bhaishajya Kalpana Acharya.
            Medicine: {medicine_name}
            Dosage Form: {dosage_form}
            Language: {m_lang}

            Provide an exhaustive, practical guide on how this medicine is formulated and manufactured:
            1. Classical Reference & Shloka (blockquote)
            2. Ingredients Table (Herb/Dhatu, Part, Ratio/Grams)
            3. Raw Material Purification (Shodhana)
            4. Step-by-Step Manufacturing (Mardan, Paka, Agni details)
            5. Siddhi Lakshana & Quality Tests
            6. Dose, Anupana & Clinical Uses
            """

            with st.spinner(f"🔬 AI तज्ज्ञ '{medicine_name}' ची निर्माण पद्धत तयार करत आहे..."):
                try:
                    med_text = ask_gemini(med_prompt)
                    st.balloons()
                    st.success(f"✅ {medicine_name} ची संपूर्ण निर्माण विधी तयार झाली आहे!")

                    st.markdown('<div class="notes-box">', unsafe_allow_html=True)
                    st.markdown(med_text)
                    st.markdown('</div>', unsafe_allow_html=True)

                    st.markdown("<br>", unsafe_allow_html=True)
                    doc_export = create_exportable_doc(f"{medicine_name} निर्माण विधी", f"{dosage_form} | Rasashastra", med_text)
                    
                    st.download_button(
                        label="📥 फोटो (Image) किंवा PDF सेव्ह करा (Download Suite)",
                        data=doc_export.encode('utf-8'),
                        file_name=f"{medicine_name.replace(' ', '_')}_Manufacturing_Suite.html",
                        mime="text/html",
                        use_container_width=True
                    )
                except Exception as e:
                    st.error(f"त्रुटी: {e}")

# --- Bottom Footer Branding ---
st.markdown("""
<div class="app-footer">
    🌿 <strong>AyurVeda AI & Bhaishajya Kalpana Studio</strong> | Developed by <strong>Avishkar Alase</strong>
</div>
""", unsafe_allow_html=True)
