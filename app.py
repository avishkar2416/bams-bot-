import streamlit as st
from google import genai
from google.genai import types
import json
import time
import markdown

# --- Page Setup ---
st.set_page_config(
    page_title="AyurVeda AI | Avishkar Alase",
    page_icon="🌺",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- GANESHOTSAV ROYAL GOLDEN & FESTIVE CSS ANIMATIONS ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@500;600;700;800;900&family=Mukta:wght@400;600;700;800;900&display=swap');

    html, body, .stApp {
        background: radial-gradient(circle at 50% 0%, #fffbeb 0%, #fef3c7 25%, #fdfcf7 60%, #fff7ed 100%) !important;
        background-attachment: fixed !important;
        font-family: 'Mukta', 'Plus Jakarta Sans', sans-serif !important;
        color: #1e1b4b !important;
        overflow-x: hidden;
    }

    @keyframes goldPulse {
        0% { box-shadow: 0 0 0 0 rgba(245, 158, 11, 0.6); }
        70% { box-shadow: 0 0 0 18px rgba(245, 158, 11, 0); }
        100% { box-shadow: 0 0 0 0 rgba(245, 158, 11, 0); }
    }

    label, p, span, div, h1, h2, h3 {
        color: #1e1b4b !important;
    }

    /* Golden Navbar */
    .ganesha-navbar {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 14px 22px;
        background: rgba(255, 255, 255, 0.9) !important;
        backdrop-filter: blur(18px);
        -webkit-backdrop-filter: blur(18px);
        border: 2px solid #fde68a !important;
        border-radius: 24px;
        margin-bottom: 22px;
        box-shadow: 0 12px 35px -8px rgba(217, 119, 6, 0.2);
    }
    .brand-group {
        display: flex;
        align-items: center;
        gap: 12px;
    }
    .brand-title {
        font-size: 21px;
        font-weight: 900;
        background: linear-gradient(135deg, #b45309 0%, #ea580c 50%, #d97706 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 0;
        letter-spacing: -0.5px;
    }
    .vip-badge {
        background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%) !important;
        border: 1.5px solid #f59e0b;
        padding: 8px 18px;
        border-radius: 14px;
        font-size: 13.5px;
        font-weight: 800;
        color: #92400e !important;
        box-shadow: 0 4px 15px rgba(245, 158, 11, 0.25);
    }

    /* Royal Festive Hero Banner */
    .ganesha-hero {
        background: linear-gradient(135deg, #b45309 0%, #c2410c 45%, #991b1b 100%) !important;
        padding: 24px 22px;
        border-radius: 22px;
        margin-bottom: 24px;
        color: #ffffff !important;
        box-shadow: 0 16px 36px -10px rgba(180, 83, 9, 0.45);
        border: 2px solid #fef08a;
    }
    .ganesha-hero * { color: #ffffff !important; }
    .festive-tag {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        background: rgba(255, 255, 255, 0.22);
        padding: 5px 14px;
        border-radius: 30px;
        font-size: 12px;
        font-weight: 800;
        letter-spacing: 0.5px;
        margin-bottom: 8px;
        border: 1px solid rgba(255, 255, 255, 0.35);
    }

    /* Floating Inputs */
    div[data-baseweb="select"] > div,
    div[data-baseweb="input"] > div {
        background-color: rgba(255, 255, 255, 0.95) !important;
        border: 2px solid #fed7aa !important;
        border-radius: 16px !important;
        box-shadow: 0 4px 12px rgba(245, 158, 11, 0.04) !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
    }
    div[data-baseweb="select"] > div:hover,
    div[data-baseweb="input"] > div:hover {
        border-color: #f59e0b !important;
        box-shadow: 0 6px 20px rgba(245, 158, 11, 0.25) !important;
        transform: translateY(-2px);
    }

    /* Animated Button with Scale */
    div.stButton > button {
        background: linear-gradient(135deg, #ea580c 0%, #d97706 50%, #b45309 100%) !important;
        color: #ffffff !important;
        border: 2px solid #fde68a !important;
        border-radius: 18px !important;
        padding: 16px 34px !important;
        font-size: 17px !important;
        font-weight: 900 !important;
        box-shadow: 0 12px 30px -4px rgba(234, 88, 12, 0.5) !important;
        cursor: pointer !important;
        transition: all 0.25s ease !important;
        animation: goldPulse 2.5s infinite;
    }
    div.stButton > button:hover {
        transform: translateY(-2px) scale(1.015) !important;
        box-shadow: 0 18px 40px -4px rgba(234, 88, 12, 0.7) !important;
    }
    div.stButton > button:active {
        transform: translateY(1px) scale(0.97) !important;
    }

    /* Festive Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 14px;
        margin-bottom: 22px;
    }
    .stTabs [data-baseweb="tab"] {
        background-color: rgba(255, 255, 255, 0.85) !important;
        border-radius: 16px !important;
        padding: 12px 24px !important;
        font-weight: 800 !important;
        border: 1.5px solid #fed7aa !important;
        transition: all 0.25s ease !important;
    }
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #b45309 0%, #ea580c 100%) !important;
        border-color: #ea580c !important;
        color: #ffffff !important;
        box-shadow: 0 8px 22px rgba(234, 88, 12, 0.3) !important;
    }
    .stTabs [aria-selected="true"] * {
        color: #ffffff !important;
    }

    .app-footer {
        text-align: center;
        padding: 40px 10px 15px 10px;
        font-size: 13.5px;
        color: #92400e !important;
        font-weight: 700;
    }
</style>
""", unsafe_allow_html=True)

# --- API Setup ---
api_key = st.secrets.get("GEMINI_API_KEY", "")
if not api_key:
    st.error("⚠️ कृपया Settings > Secrets मध्ये GEMINI_API_KEY कॉन्फिगर करा.")
    st.stop()

client = genai.Client(api_key=api_key)

@st.cache_data(show_spinner=False, ttl=86400)
def cached_ask_gemini(prompt: str, as_json: bool = False):
    model_name = 'gemini-3.6-flash'
    for attempt in range(3):
        try:
            config = types.GenerateContentConfig(response_mime_type="application/json") if as_json else None
            res = client.models.generate_content(
                model=model_name,
                contents=prompt,
                config=config
            )
            if res and res.text:
                return res.text
        except Exception as e:
            if "429" in str(e) or "RESOURCE_EXHAUSTED" in str(e):
                time.sleep(16)
            else:
                time.sleep(2)
            continue
    raise RuntimeError("गुगल सर्व्हर व्यस्त आहे. कृपया पुन्हा प्रयत्न करा.")

# =========================================================================
# अस्सल फोटोसारखी A4 HANDWRITTEN NOTE GENERATOR
# =========================================================================
def render_photo_identical_sheet(data, subject_name, topic_name, is_marathi=True):
    title = data.get("title", topic_name)
    marks = data.get("marks", "10 Marks (LAQ)")
    
    definition = data.get("definition", "")
    def_sub = data.get("definition_sub", "")
    
    sthana_main = data.get("sthana_main", "")
    sthana_sub = data.get("sthana_sub", "")
    
    gunadharma = data.get("gunadharma", "")
    gunadharma_en = data.get("gunadharma_en", "")
    
    karya_list = "".join([f"<li>{k}</li>" for k in data.get("karya", [])])
    types_list = "".join([f"<li><b>{t.get('name','')}</b> - {t.get('desc','')}</li>" for t in data.get("types", [])])
    nidana_list = "".join([f"<li>{n}</li>" for n in data.get("nidana", [])])
    lakshana_list = "".join([f"<li>{l}</li>" for l in data.get("lakshana", [])])
    
    sidebar_box_title = data.get("sidebar_box_title", "Key Correlation")
    sidebar_box_points = "".join([f"<div>✓ {p}</div>" for p in data.get("sidebar_box_points", [])])
    
    flow_steps = data.get("samprapti_steps", [])
    flow_html = ""
    if flow_steps:
        steps_inner = "".join([f'<div class="hw-box">{s}</div><div class="hw-arrow">↓</div>' for s in flow_steps[:-1]])
        steps_inner += f'<div class="hw-box-final">{flow_steps[-1]}</div>'
        flow_title = "७. <u>संप्राप्ती (Pathogenesis)</u> :-" if is_marathi else "7. <u>Pathogenesis (Samprapti)</u> :-"
        flow_html = f"""
        <div class="sec-title">{flow_title}</div>
        <div style="text-align:center; margin: 6px 0 12px 0;">
            {steps_inner}
        </div>
        """
        
    chikitsa_list = "".join([f"<li>{c}</li>" for c in data.get("chikitsa", [])])
    aushadha_list = "".join([f"<li>{a}</li>" for a in data.get("aushadha", [])])
    punch_line = data.get("punch_line", "")

    # Labels based on Language
    lbl_def = "व्याख्या (Definition)" if is_marathi else "Definition"
    lbl_sthana = "स्थान (Location)" if is_marathi else "Location (Sthana)"
    lbl_sthana_main = "मुख्य स्थान" if is_marathi else "Primary Seat"
    lbl_sthana_sub = "उपस्थान" if is_marathi else "Secondary Seats"
    lbl_guna = "गुणधर्म (Properties)" if is_marathi else "Properties (Guna)"
    lbl_karya = "कार्ये (Functions)" if is_marathi else "Functions (Karma)"
    lbl_types = "प्रकार (Types / Sub-types)" if is_marathi else "Classification / Types"
    lbl_nidana = "प्रकोपांची कारणे (Nidana)" if is_marathi else "Etiology (Nidana)"
    lbl_lakshana = "प्रकोपांची लक्षणे (Lakshana)" if is_marathi else "Symptoms (Lakshana)"
    lbl_chikitsa = "चिकित्सा (Management)" if is_marathi else "Management (Chikitsa)"
    lbl_aushadha = "महत्त्वाची औषधे :-" if is_marathi else "Important Formulations :-"
    lbl_punch = "परीक्षेसाठी मुख्य सूत्र (Exam Punch Line)" if is_marathi else "Exam Punch Line"

    html_code = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <script src="https://cdnjs.cloudflare.com/ajax/libs/html2canvas/1.4.1/html2canvas.min.js"></script>
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Mukta:wght@500;600;700;800;900&family=Patrick+Hand&display=swap');

            body {{
                background-color: #cbd5e1;
                margin: 0;
                padding: 15px 5px;
                display: flex;
                flex-direction: column;
                align-items: center;
                font-family: {'"Mukta", sans-serif' if is_marathi else '"Patrick Hand", "Mukta", sans-serif'};
            }}

            .action-bar {{
                margin-bottom: 16px;
                display: flex;
                gap: 12px;
                font-family: sans-serif;
            }}
            .btn-action {{
                background: linear-gradient(135deg, #0284c7 0%, #0369a1 100%);
                color: white;
                border: none;
                padding: 12px 24px;
                font-size: 15px;
                font-weight: 800;
                border-radius: 12px;
                cursor: pointer;
                box-shadow: 0 4px 14px rgba(2,132,199,0.35);
            }}

            .a4-container {{
                width: 820px;
                min-height: 1160px;
                background-color: #fcfbf7;
                border: 2px solid #0f2b5c;
                box-shadow: 0 12px 35px rgba(0,0,0,0.18);
                padding: 24px 28px;
                box-sizing: border-box;
                color: #0b2559;
                position: relative;
                font-size: 15.5px;
                line-height: 1.45;
            }}

            .hl-red {{
                background-color: #ffe4e6;
                color: #991b1b;
                padding: 0 4px;
                border-radius: 3px;
                font-weight: 700;
            }}
            .u-red {{
                text-decoration: underline;
                text-decoration-color: #ef4444;
                text-decoration-thickness: 1.8px;
            }}

            .header-top {{
                display: flex;
                justify-content: space-between;
                align-items: center;
                border-bottom: 2px solid #0f2b5c;
                padding-bottom: 10px;
                margin-bottom: 12px;
            }}
            .ganesha-namah {{
                font-size: 16px;
                font-weight: 700;
                color: #0b2559;
                width: 20%;
            }}
            .main-title-box {{
                border: 2px solid #0f2b5c;
                border-radius: 8px;
                padding: 4px 22px;
                font-size: 26px;
                font-weight: 900;
                background: #ffffff;
                letter-spacing: 0.5px;
            }}
            .marks-box {{
                border: 1.8px solid #0f2b5c;
                border-radius: 6px;
                padding: 4px 10px;
                text-align: center;
                font-size: 13.5px;
                background: #ffffff;
            }}

            .sheet-grid {{
                display: flex;
                gap: 16px;
            }}
            .left-col {{
                flex: 1.25;
                padding-right: 12px;
                border-right: 1.5px solid #0f2b5c;
            }}
            .right-col {{
                flex: 1;
                padding-left: 6px;
            }}

            .sec-title {{
                font-weight: 800;
                font-size: 16px;
                margin: 8px 0 3px 0;
            }}
            ul.hw-list {{
                margin: 3px 0 8px 0;
                padding-left: 18px;
                line-height: 1.45;
            }}
            ul.hw-list li {{ margin-bottom: 3px; }}

            .side-card {{
                border: 1.8px solid #0f2b5c;
                border-radius: 8px;
                padding: 8px 12px;
                background: #ffffff;
                margin-bottom: 12px;
                font-size: 14.5px;
            }}
            .side-card-title {{
                font-weight: 800;
                border-bottom: 1.5px solid #0f2b5c;
                padding-bottom: 2px;
                margin-bottom: 5px;
                text-align: center;
            }}

            .hw-box {{
                border: 1.8px solid #0f2b5c;
                border-radius: 6px;
                padding: 4px 8px;
                font-size: 14px;
                background: #ffffff;
                margin: auto;
                width: 90%;
            }}
            .hw-arrow {{
                font-size: 15px;
                font-weight: 900;
                margin: 2px 0;
            }}
            .hw-box-final {{
                border: 1.8px solid #0f2b5c;
                border-radius: 6px;
                padding: 5px 8px;
                font-size: 14px;
                font-weight: 800;
                background: #ffe4e6;
                color: #991b1b;
                margin: auto;
                width: 90%;
            }}

            .punch-box {{
                border-top: 2px solid #0f2b5c;
                margin-top: 12px;
                padding-top: 6px;
                font-size: 15px;
                font-weight: 800;
            }}

            .footer-sign {{
                position: absolute;
                bottom: 8px;
                right: 20px;
                font-size: 12px;
                font-family: 'Patrick Hand', sans-serif;
                color: #047857;
                font-weight: 800;
            }}

            @media print {{
                .action-bar {{ display: none !important; }}
                body {{ padding: 0; background: none; }}
                .a4-container {{ border: none; box-shadow: none; }}
            }}
        </style>
    </head>
    <body>
        <div class="action-bar">
            <button class="btn-action" onclick="downloadSheet()">📸 फोटो डाऊनलोड करा (.PNG)</button>
            <button class="btn-action" style="background:#059669;" onclick="window.print()">📄 प्रिंट करा / PDF सेव्ह करा</button>
        </div>

        <div class="a4-container" id="captureCanvas">
            <!-- Header -->
            <div class="header-top">
                <div class="ganesha-namah">॥ श्री गणेशाय नमः ॥</div>
                <div class="main-title-box">{title}</div>
                <div class="marks-box">
                    <span style="color:#0369a1; font-weight:700;">{subject_name}</span><br>
                    <span style="color:#b91c1c; font-weight:800; border-bottom: 1.5px solid #ef4444;">{marks}</span>
                </div>
            </div>

            <!-- 2-Column Exact Layout -->
            <div class="sheet-grid">
                <!-- Left Column -->
                <div class="left-col">
                    <div class="sec-title">* <span class="u-red">{lbl_def}</span> :-</div>
                    <div style="margin-bottom:8px;">{definition} <span style="font-size:13.5px; opacity:0.9;">({def_sub})</span></div>

                    <div class="sec-title">१. <span class="u-red">{lbl_sthana}</span> :-</div>
                    <ul class="hw-list">
                        <li><b>{lbl_sthana_main}</b> - {sthana_main}</li>
                        <li><b>{lbl_sthana_sub}</b> - {sthana_sub}</li>
                    </ul>

                    <div class="sec-title">२. <span class="u-red">{lbl_guna}</span> :-</div>
                    <ul class="hw-list">
                        <li>{gunadharma}</li>
                        <div style="font-size:13.5px; opacity:0.9; margin-top:2px;">({gunadharma_en})</div>
                    </ul>

                    <div class="sec-title">३. <span class="u-red">{lbl_karya}</span> :-</div>
                    <ul class="hw-list">{karya_list}</ul>

                    <div class="sec-title">४. <span class="u-red">{lbl_types}</span> :-</div>
                    <ul class="hw-list">{types_list}</ul>

                    <div class="sec-title">५. <span class="u-red">{lbl_nidana}</span> :-</div>
                    <ul class="hw-list">{nidana_list}</ul>

                    <div class="sec-title">६. <span class="u-red">{lbl_lakshana}</span> :-</div>
                    <ul class="hw-list">{lakshana_list}</ul>
                </div>

                <!-- Right Column -->
                <div class="right-col">
                    <div class="side-card">
                        <div class="side-card-title">{sidebar_box_title}</div>
                        {sidebar_box_points}
                    </div>

                    {flow_html}

                    <div class="sec-title">८. <span class="u-red">{lbl_chikitsa}</span> :-</div>
                    <ul class="hw-list">{chikitsa_list}</ul>

                    <div class="side-card" style="margin-top:10px;">
                        <div class="side-card-title" style="color:#991b1b;">{lbl_aushadha}</div>
                        <ul class="hw-list" style="margin-bottom:2px;">{aushadha_list}</ul>
                    </div>
                </div>
            </div>

            <!-- Bottom Punchline -->
            <div class="punch-box">
                ✍️ <span class="u-red">{lbl_punch}</span> :-<br>
                <div style="text-align:center; margin-top:4px; font-size:16px;">
                    "{punch_line}"
                </div>
            </div>

            <!-- Watermark Sign -->
            <div class="footer-sign">
                🌿 AyurVeda AI | By Avishkar Alase
            </div>
        </div>

        <script>
            function downloadSheet() {{
                const el = document.getElementById('captureCanvas');
                html2canvas(el, {{ scale: 2.2, useCORS: true }}).then(canvas => {{
                    const a = document.createElement('a');
                    a.download = '{topic_name.replace(" ", "_")}_Handwritten.png';
                    a.href = canvas.toDataURL('image/png');
                    a.click();
                }});
            }}
        </script>
    </body>
    </html>
    """
    return html_code

# --- Top Navigation Bar ---
st.markdown("""
<div class="ganesha-navbar">
    <div class="brand-group">
        <div style="font-size:26px;">🪔</div>
        <div>
            <div class="brand-title">🌿 AyurVeda AI</div>
            <small style="color:#b45309; font-weight:800; letter-spacing:0.5px;">गणेशोत्सव विशेष पर्व | BAMS HANDWRITTEN STUDIO</small>
        </div>
    </div>
    <div class="vip-badge">
        <span>Avishkar Alase</span> ✓
    </div>
</div>
""", unsafe_allow_html=True)

# --- 2 Main Tabs (दोन्ही मुख्य टॅब्स परत आणले) ---
tab1, tab2 = st.tabs([
    "📖 BAMS स्टडी नोट्स (Syllabus Notes)",
    "🧪 औषध घटक व निर्माण विधी (Medicine & Manufacturing)"
])

# =========================================================================
# TAB 1: SYLLABUS STUDY NOTES (सर्व ऑप्शन्स पूर्ववत)
# =========================================================================
with tab1:
    st.markdown("""
    <div class="ganesha-hero">
        <div class="festive-tag">🌺 ॥ श्री गणेशाय नमः ॥ 🌺</div>
        <h3 style="margin:0 0 6px 0; font-weight:900;">🎯 BAMS A4 बॉलपेन Handwritten नोट्स</h3>
        <p style="margin:0; font-size:13.5px; opacity:0.95;">ठळक मुख्य हेडिंग, सुवाच्य अक्षरे, महत्वाच्या शब्दांना <b>Red Highlight</b>, फ्लोचार्ट आणि गुण (Marks Weightage).</p>
    </div>
    """, unsafe_allow_html=True)

    r1_col1, r1_col2 = st.columns([1, 1.2])
    with r1_col1:
        bams_year = st.selectbox(
            "🎓 BAMS वर्ष निवडा (Academic Year):",
            [
                "BAMS 1st Professional (प्रथम वर्ष)",
                "BAMS 2nd Professional (द्वितीय वर्ष)",
                "BAMS 3rd Professional (तृतीय वर्ष)",
                "BAMS Final Professional (अंतिम वर्ष)"
            ]
        )

    with r1_col2:
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

    r2_col1, r2_col2 = st.columns([1.2, 1])
    with r2_col1:
        study_mode = st.selectbox(
            "🎯 अभ्यासाचा प्रकार निवडा (Study Mode):",
            [
                "📋 A4 Blue Ballpen Handwritten Sheet (अस्सल A4 पेन नोट्स)",
                "📖 Comprehensive Notes (संपूर्ण सविस्तर अभ्यास नोट्स)",
                "📜 Only Shlokas & Meanings (फक्त मूळ श्लोक, अन्वय व अर्थ)",
                "📝 10-Mark LAQ Answer Format (दीर्घोत्तरी प्रश्न-उत्तर फॉरमॅट)",
                "⚡ Quick Revision / Viva Voce Points (तोंडी परीक्षेसाठी महत्त्वाचे मुद्दे)"
            ]
        )

    with r2_col2:
        language_preference = st.radio(
            "🌐 माध्यम (Language):",
            [
                "मराठी (संस्कृत श्लोक + सोपा अर्थ + मॉडर्न टर्म्स)",
                "Simple Indian English + Sanskrit"
            ],
            horizontal=True
        )

    topic = st.text_input(
        "🔍 अभ्यासाचा विषय / प्रश्न टाका:",
        placeholder="उदा. Pitta Dosha, Garavisha vs Dooshivisha, किंवा Ashwagandha"
    )

    generate_notes_btn = st.button("🚀 सविस्तर अभ्यास नोट्स तयार करा", key="btn_notes", use_container_width=True)

    if generate_notes_btn:
        if not topic.strip():
            st.warning("⚠️ कृपया अभ्यासाचा विषय प्रविष्ट करा.")
        else:
            is_marathi = "मराठी" in language_preference

            if "A4 Blue Ballpen" in study_mode:
                if is_marathi:
                    lang_rule = """
                    LANGUAGE INSTRUCTION (MARATHI):
                    - Generate notes in natural, simple spoken Marathi with Sanskrit terms.
                    - Add simple English terms in parentheses for important points (e.g. 'लहान आंत्र (Small intestine)', 'दाह (Burning sensation)').
                    - Marks weightage in Marathi (e.g. '10 Marks (LAQ)' or '5 Marks (SAQ)').
                    """
                else:
                    lang_rule = """
                    STRICT ZERO-MARATHI INSTRUCTION (100% PURE ENGLISH):
                    - The user chose 'Simple Indian English + Sanskrit'.
                    - ABSOLUTELY DO NOT WRITE ANY MARATHI/DEVANAGARI SCRIPT ANYWHERE!
                    - Every single section, definition, flow step, and word must be in English with English-transliterated Sanskrit terms.
                    """

                json_prompt = f"""
                You are a senior Ayurveda Professor and BAMS University Paper Setter.
                Subject: {subject}
                Topic: {topic}
                Language Selected: {language_preference}

                {lang_rule}

                Generate crisp exam notes matching this JSON schema:
                {{
                    "title": "{topic}",
                    "marks": "{'10 Marks (LAQ)' if is_marathi else '10 Marks (LAQ)'}",
                    "definition": "{'जे द्रव्य शरीरामध्ये <span class=\\'hl-red\\'>पाचन, दहन, रूपांतरण व उष्णता</span> निर्माण करते त्याला पित्त दोष म्हणतात.' if is_marathi else 'The bio-principle responsible for digestion, heat and metabolic transformations.'}",
                    "definition_sub": "It is the bio-transformative principle in the body",
                    "sthana_main": "{'आमाशय, ग्रहणी, लहान आंत्र (Small intestine)' if is_marathi else 'Grahani, Amashaya, Small intestine'}",
                    "sthana_sub": "{'रक्त, यकृत, प्लीहा, स्वेद, नेत्र' if is_marathi else 'Rakta, Yakrit, Pleeha, Sweda, Netra'}",
                    "gunadharma": "<span class='hl-red'>{'उष्ण, तीक्ष्ण, लघु, द्रव, सार, अम्ल, कटु' if is_marathi else 'Ushna, Tikshna, Laghu, Drava, Sara, Amla, Katu'}</span>",
                    "gunadharma_en": "Hot, Sharp, Light, Liquid, Spreading, Sour, Pungent",
                    "karya": [
                        "{'अन्न पचन व धातूंचे रूपांतरण' if is_marathi else 'Digestion of food & tissue transformation'}",
                        "{'देहाला उष्णता व तापमान प्रदान करणे' if is_marathi else 'Maintaining normal body temperature'}",
                        "{'वर्ण, प्रभा, बुद्धी, दृष्टी प्रदान करणे' if is_marathi else 'Providing vision, complexion, and intellect'}",
                        "{'मूत्र, पुरीष, स्वेद यांचे नियमन' if is_marathi else 'Excretion and regulation of body wastes'}"
                    ],
                    "types": [
                        {{"name": "{'पाचक पित्त' if is_marathi else 'Pachaka Pitta'}", "desc": "{'आमाशय व ग्रहणी स्थित' if is_marathi else 'Located in Grahani / Stomach'}"}},
                        {{"name": "{'रंजक पित्त' if is_marathi else 'Ranjaka Pitta'}", "desc": "{'यकृत व प्लीहा स्थित' if is_marathi else 'Located in Liver & Spleen'}"}},
                        {{"name": "{'साधक पित्त' if is_marathi else 'Sadhaka Pitta'}", "desc": "{'हृदय व मन स्थित' if is_marathi else 'Located in Heart & Mind'}"}},
                        {{"name": "{'आलोचक पित्त' if is_marathi else 'Alochaka Pitta'}", "desc": "{'नेत्र स्थित' if is_marathi else 'Located in Eyes / Vision'}"}},
                        {{"name": "{'भ्राजक पित्त' if is_marathi else 'Bhrajaka Pitta'}", "desc": "{'त्वचा स्थित' if is_marathi else 'Located in Skin'}"}}
                    ],
                    "nidana": [
                        "<span class='hl-red'>{'अतिउष्ण, अम्ल, लवण आहार' if is_marathi else 'Intake of Ushna, Amla, Lavana diet'}</span>",
                        "{'क्रोध, अतिताप, उपवास' if is_marathi else 'Excessive anger, sun exposure, irregular fasting'}"
                    ],
                    "lakshana": [
                        "{'दाह (Burning sensation)' if is_marathi else 'Burning sensation (Daha)'}",
                        "{'तृष्णा, पीत-नेत्र-मूत्र' if is_marathi else 'Excess thirst, yellowish stool & urine'}",
                        "{'अम्लपित्त, रक्तपित्त लक्षणे' if is_marathi else 'Hyperacidity and bleeding tendencies'}"
                    ],
                    "sidebar_box_title": "{'Pitta = Agni' if is_marathi else 'Core Concept'}",
                    "sidebar_box_points": ["Transformation", "Metabolism", "Heat Regulation", "Intelligence"],
                    "samprapti_steps": [
                        "{'निदान सेवन' if is_marathi else 'Intake of Etiology (Nidana)'}",
                        "{'दोष संचय व प्रकोप' if is_marathi else 'Dosha Aggravation (Prakopa)'}",
                        "{'रक्त धातू दुष्टी' if is_marathi else 'Vitiation of Rakta Dhatu'}",
                        "{'व्याधी निर्मिती' if is_marathi else 'Disease Manifestation'}"
                    ],
                    "chikitsa": [
                        "{'शीत, मधुर, तिक्त आहार' if is_marathi else 'Sheetal, Madhura and Tikta Ahara'}",
                        "<span class='hl-red'>{'विरेचन' if is_marathi else 'Virechana'}</span> {'हे श्रेष्ठ शोधन' if is_marathi else 'is the prime purificatory treatment'}",
                        "{'तिक्तघृत व शतधौत घृत वापर' if is_marathi else 'Use of Tikta Ghrita and Sheeta Upachara'}"
                    ],
                    "aushadha": [
                        "{'आवळा (Amalaki)' if is_marathi else 'Amalaki (Emblica officinalis)'}",
                        "{'गुडुची (Guduchi)' if is_marathi else 'Guduchi (Tinospora cordifolia)'}",
                        "{'शतधौत घृत' if is_marathi else 'Shatadhouta Ghrita'}",
                        "{'सारिवा, उशीर' if is_marathi else 'Sariva and Ushira'}"
                    ],
                    "punch_line": "{'पित्त हे दहन, पाचन व रूपांतरण करणारे उष्ण द्रव्य आहे.' if is_marathi else 'Pitta represents the metabolic fire; Virechana is its supreme treatment.'}"
                }}
                """

                with st.spinner("✍️ AI अस्सल वहीच्या पानावर फोटोसारख्या नोट्स तयार करत आहे..."):
                    try:
                        raw_json = cached_ask_gemini(json_prompt, as_json=True)
                        clean_json = raw_json.strip()
                        if clean_json.startswith("```json"): clean_json = clean_json[7:]
                        if clean_json.startswith("```"): clean_json = clean_json[3:]
                        if clean_json.endswith("```"): clean_json = clean_json[:-3]

                        sheet_data = json.loads(clean_json.strip())
                        a4_html = render_photo_identical_sheet(sheet_data, subject, topic, is_marathi=is_marathi)

                        st.balloons()
                        st.success(f"✅ अस्सल वही-फोटो शीट तयार झाली आहे! (अपेक्षित गुण: {sheet_data.get('marks')})")
                        st.components.v1.html(a4_html, height=1300, scrolling=True)

                    except Exception as e:
                        st.error(f"त्रुटी: {e}")

            else:
                system_instruction = f"""
                You are a senior Ayurveda Acharya according to NCISM standards.
                Academic Level: {bams_year}, Subject: {subject}, Study Mode: {study_mode}, Topic: {topic}, Language: {language_preference}.
                Generate tailored, high-yield study material strictly aligned with '{study_mode}'.
                - If English is chosen, write purely in English with transliterated Sanskrit terms.
                - Format Sanskrit Shlokas inside blockquotes (> "Shloka").
                - Bold all key terms.
                """
                with st.spinner(f"⚡ AI आयुर्वेद तज्ज्ञ '{study_mode}' नुसार नोट्स तयार करत आहे..."):
                    try:
                        notes_text = cached_ask_gemini(system_instruction, as_json=False)
                        st.balloons()
                        st.success("✅ नोट्स तयार झाल्या आहेत!")
                        st.markdown(notes_text)
                    except Exception as e:
                        st.error(f"त्रुटी: {e}")

# =========================================================================
# TAB 2: MEDICINE FORMULATION & MANUFACTURING (औषध निर्माण विधी पूर्ववत)
# =========================================================================
with tab2:
    st.markdown("""
    <div class="ganesha-hero" style="background: linear-gradient(135deg, #0f766e 0%, #0d9488 100%) !important; border-color: #5eead4;">
        <div class="festive-tag" style="background: rgba(255,255,255,0.18);">🌿 रसौषधी विधी</div>
        <h3 style="margin:0 0 6px 0; font-weight:900;">🧪 रसशास्त्र व भैषज्य कल्पना स्पेशल</h3>
        <p style="margin:0; font-size:13.5px; opacity:0.95;">आयुर्वेदिक औषध घटक व सविस्तर निर्माण विधी सोप्या स्टेप्समध्ये शिका.</p>
    </div>
    """, unsafe_allow_html=True)

    m_col1, m_col2 = st.columns([1.2, 1])
    with m_col1:
        dosage_form = st.selectbox(
            "🏺 औषधाचा प्रकार (Dosage Form):",
            ["Vati / Gutika (गोळी / वटी)", "Churna (चूर्ण)", "Asava & Arishta (आसव व अरिष्ट)", "Taila / Ghrita (सिद्ध तेल व घृत)", "Bhasma & Pishti (भस्म व पिष्टी)"]
        )
    with m_col2:
        m_lang = st.radio("🌐 भाषा:", ["Simple Indian English", "मराठी"], horizontal=True, key="m_lang")

    medicine_name = st.text_input("💊 गोळी किंवा औषधाचे नाव टाका:", placeholder="उदा. आरोग्यवर्धिनी वटी किंवा चंद्रप्रभावटी")

    if st.button("🔬 औषध घटक व बनवण्याची कृती शिका", key="btn_med", use_container_width=True):
        if not medicine_name.strip():
            st.warning("⚠️ कृपया औषधाचे नाव टाका.")
        else:
            with st.spinner(f"🔬 AI तज्ज्ञ '{medicine_name}' ची निर्माण पद्धत तयार करत आहे..."):
                try:
                    med_prompt = f"Explain manufacturing of {medicine_name} ({dosage_form}) in {m_lang} with ingredients table, purification, and steps."
                    res_text = cached_ask_gemini(med_prompt, as_json=False)
                    st.success("✅ माहिती तयार झाली आहे!")
                    st.markdown(res_text)
                except Exception as e:
                    st.error(f"त्रुटी: {e}")

# --- Footer ---
st.markdown("""
<div class="app-footer">
    🌺 ॥ गणपती बाप्पा मोरया ॥ 🌿 <strong>AyurVeda AI</strong> | Developed by <strong>Avishkar Alase</strong>
</div>
""", unsafe_allow_html=True)
