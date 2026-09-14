import streamlit as st
from google import genai
from google.genai import types
import json
import time
import markdown

# --- Page Setup ---
st.set_page_config(
    page_title="AyurVeda AI | गणेशोत्सव विशेष पर्व",
    page_icon="🌺",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- GANESHOTSAV ROYAL GOLDEN & FESTIVE CSS ANIMATIONS ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@500;600;700;800;900&family=Mukta:wght@400;600;700;800;900&display=swap');

    /* 1. Festive Background with Floating Aura */
    html, body, .stApp {
        background: radial-gradient(circle at 50% 0%, #fffbeb 0%, #fef3c7 25%, #fdfcf7 60%, #fff7ed 100%) !important;
        background-attachment: fixed !important;
        font-family: 'Mukta', 'Plus Jakarta Sans', sans-serif !important;
        color: #1e1b4b !important;
        overflow-x: hidden;
    }

    /* 2. Floating Festive Diya & Flower Glow Animation */
    @keyframes flowerFall {
        0% { transform: translateY(-10px) rotate(0deg); opacity: 0.8; }
        50% { transform: translateY(15px) rotate(15deg); opacity: 1; }
        100% { transform: translateY(-10px) rotate(0deg); opacity: 0.8; }
    }

    @keyframes goldPulse {
        0% { box-shadow: 0 0 0 0 rgba(245, 158, 11, 0.6); }
        70% { box-shadow: 0 0 0 18px rgba(245, 158, 11, 0); }
        100% { box-shadow: 0 0 0 0 rgba(245, 158, 11, 0); }
    }

    @keyframes divineShimmer {
        0% { background-position: -200% 0; }
        100% { background-position: 200% 0; }
    }

    label, p, span, div, h1, h2, h3 {
        color: #1e1b4b !important;
    }

    /* 3. Golden Luxury Floating Navbar */
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
    .diya-icon {
        font-size: 28px;
        animation: flowerFall 3.5s ease-in-out infinite;
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
        display: flex;
        align-items: center;
        gap: 6px;
        transition: transform 0.25s ease;
    }
    .vip-badge:hover {
        transform: scale(1.05) rotate(1deg);
    }

    /* 4. Royal Festive Hero Banner */
    .ganesha-hero {
        background: linear-gradient(135deg, #b45309 0%, #c2410c 45%, #991b1b 100%) !important;
        padding: 26px 24px;
        border-radius: 24px;
        margin-bottom: 24px;
        color: #ffffff !important;
        box-shadow: 0 18px 40px -10px rgba(180, 83, 9, 0.45);
        border: 2px solid #fef08a;
        position: relative;
        overflow: hidden;
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
        margin-bottom: 10px;
        border: 1px solid rgba(255, 255, 255, 0.35);
    }

    /* 5. Inputs with Golden Glow on Focus */
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

    /* 6. Kesari Gold Animated Button with Ripple Scale */
    div.stButton > button {
        background: linear-gradient(135deg, #ea580c 0%, #d97706 50%, #b45309 100%) !important;
        color: #ffffff !important;
        border: 2px solid #fde68a !important;
        border-radius: 18px !important;
        padding: 17px 36px !important;
        font-size: 17px !important;
        font-weight: 900 !important;
        letter-spacing: 0.4px !important;
        box-shadow: 0 12px 30px -4px rgba(234, 88, 12, 0.5) !important;
        cursor: pointer !important;
        transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1) !important;
        animation: goldPulse 2.5s infinite;
    }
    div.stButton > button:hover {
        transform: translateY(-3px) scale(1.02) !important;
        box-shadow: 0 18px 40px -4px rgba(234, 88, 12, 0.7) !important;
    }
    div.stButton > button:active {
        transform: translateY(2px) scale(0.96) !important;
        box-shadow: 0 4px 14px rgba(234, 88, 12, 0.3) !important;
    }

    /* 7. Festive Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 14px;
        margin-bottom: 24px;
    }
    .stTabs [data-baseweb="tab"] {
        background-color: rgba(255, 255, 255, 0.85) !important;
        border-radius: 16px !important;
        padding: 13px 26px !important;
        font-weight: 800 !important;
        border: 1.5px solid #fed7aa !important;
        transition: all 0.25s ease !important;
    }
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #b45309 0%, #ea580c 100%) !important;
        border-color: #ea580c !important;
        color: #ffffff !important;
        box-shadow: 0 8px 22px rgba(234, 88, 12, 0.3) !important;
        transform: scale(1.02);
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

# --- API Key Setup ---
api_key = st.secrets.get("GEMINI_API_KEY", "")
if not api_key:
    st.error("⚠️ कृपया Settings > Secrets मध्ये GEMINI_API_KEY कॉन्फिगर करा.")
    st.stop()

client = genai.Client(api_key=api_key)

# =========================================================================
# STABLE GEMINI CALLER (Auto-Fallback Models)
# =========================================================================
@st.cache_data(show_spinner=False, ttl=86400)
def cached_ask_gemini(prompt: str, as_json: bool = False):
    models = ['gemini-2.5-flash', 'gemini-3.1-pro-preview', 'gemini-3.6-flash']
    last_err = None

    for model_name in models:
        for attempt in range(2):
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
                last_err = e
                time.sleep(1.5)
                continue

    raise RuntimeError(f"तांत्रिक अडचण आली: {last_err}")

# =========================================================================
# A4 BLUE BALLPEN HANDWRITTEN SHEET GENERATOR
# =========================================================================
def create_a4_handwritten_doc(data, subject_name, topic_name, is_marathi=True):
    marks = data.get("exam_marks", "१० गुण - दीर्घोत्तरी (LAQ)" if is_marathi else "10 Marks - LAQ")
    title = data.get("main_heading", topic_name)
    has_flowchart = data.get("include_flowchart", True)
    
    t1 = data.get("entity_1", {})
    t2 = data.get("entity_2", {})
    
    # 100% Strict Dynamic Headers
    lbl_flowchart = "संप्राप्ती प्रवाह तक्ता (फ्लोचार्ट)" if is_marathi else "Pathogenesis / Samprapti Flowchart"
    lbl_exam_points = "परीक्षेसाठी महत्त्वाचे मुद्दे:" if is_marathi else "High-Yield Exam Points:"
    lbl_clinical = "लक्षणे, विकार व चिकित्सा:" if is_marathi else "Clinical / Systemic Features:"
    lbl_key_concept = "★ मुख्य संकल्पना:" if is_marathi else "★ Key Exam Concept:"
    lbl_modern = "★ आधुनिक वैद्यकीय सांगड:" if is_marathi else "★ Contemporary / Modern Link:"
    lbl_table = "★ परीक्षा तुलनात्मक तक्ता:" if is_marathi else "★ Quick Exam Comparison Table:"
    lbl_feature = "मुद्दा / लक्षण" if is_marathi else "Feature"
    lbl_punch = "✍️ परीक्षेसाठी मुख्य सूत्र:" if is_marathi else "✍️ Exam Punch Line:"
    lbl_btn_png = "📸 A4 बॉलपेन फोटो डाऊनलोड करा (.PNG)" if is_marathi else "📸 Download A4 Note (.PNG)"
    lbl_btn_pdf = "📄 थेट PDF प्रिंट करा" if is_marathi else "📄 Print / Save as PDF"
    lbl_def = "व्याख्या:" if is_marathi else "Def:"

    flow_html = ""
    if has_flowchart and data.get("flowchart_steps"):
        flow_steps = "".join([f'<div class="box-step">{s}</div><div class="arrow">↓</div>' for s in data.get("flowchart_steps")[:-1]])
        flow_steps += f'<div class="cloud-step">{data.get("flowchart_steps")[-1]}</div>'
        flow_html = f"""
        <div style="text-align:center; margin: 10px 0 16px 0;">
            <span class="capsule-tag">{lbl_flowchart}</span>
            <div class="flow-wrap">{flow_steps}</div>
        </div>
        """

    table_rows = "".join([f'<tr><td><b>{r.get("feature","")}</b></td><td>{r.get("point_1","")}</td><td>{r.get("point_2","")}</td></tr>' for r in data.get("comparison_table", [])])
    table_html = ""
    if table_rows:
        table_html = f"""
        <div style="margin-top: 14px;">
            <div class="sec-heading">{lbl_table}</div>
            <table class="hw-table">
                <thead>
                    <tr>
                        <th style="width:26%;">{lbl_feature}</th>
                        <th>{t1.get('title','Part 1')}</th>
                        <th>{t2.get('title','Part 2')}</th>
                    </tr>
                </thead>
                <tbody>{table_rows}</tbody>
            </table>
        </div>
        """

    p1_html = "".join([f'<li>{p}</li>' for p in t1.get("key_points", [])])
    p2_html = "".join([f'<li>{p}</li>' for p in t2.get("key_points", [])])

    font_family = "'Mukta', sans-serif" if is_marathi else "'Architects Daughter', sans-serif"

    full_html = f"""
    <!DOCTYPE html>
    <html lang="{'mr' if is_marathi else 'en'}">
    <head>
        <meta charset="UTF-8">
        <title>{topic_name} - A4 Handwritten Notes</title>
        <script src="https://cdnjs.cloudflare.com/ajax/libs/html2canvas/1.4.1/html2canvas.min.js"></script>
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Mukta:wght@500;600;700;800;900&family=Architects+Daughter&family=Plus+Jakarta+Sans:wght@600;700;800&display=swap');

            body {{
                background-color: #f1f5f9;
                margin: 0;
                padding: 20px 10px;
                display: flex;
                flex-direction: column;
                align-items: center;
                font-family: {font_family};
                -webkit-font-smoothing: antialiased;
            }}

            .action-bar {{
                margin-bottom: 22px;
                display: flex;
                gap: 14px;
                font-family: 'Plus Jakarta Sans', sans-serif;
            }}
            .btn-action {{
                background: linear-gradient(135deg, #0284c7 0%, #0369a1 100%);
                color: white;
                border: none;
                padding: 13px 26px;
                font-size: 15px;
                font-weight: 800;
                border-radius: 12px;
                cursor: pointer;
                box-shadow: 0 6px 18px rgba(2,132,199,0.35);
                transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
            }}
            .btn-action:hover {{
                transform: translateY(-2px);
                box-shadow: 0 10px 22px rgba(2,132,199,0.45);
            }}
            .btn-action:active {{
                transform: scale(0.95);
            }}

            /* True A4 Paper Canvas */
            .a4-paper {{
                width: 794px;
                min-height: 1123px;
                background: #ffffff;
                border: 2.5px solid #0f2b5c;
                box-shadow: 0 12px 35px rgba(0,0,0,0.15);
                padding: 30px 34px;
                box-sizing: border-box;
                color: #123060; /* Realistic Blue Ballpen */
                position: relative;
                letter-spacing: 0.1px;
            }}

            .hl-red {{
                background-color: #ffe4e6 !important;
                color: #b91c1c !important;
                padding: 1px 6px !important;
                border-radius: 4px !important;
                border: 1px solid #fecdd3 !important;
                font-weight: 700 !important;
                display: inline-block;
            }}

            .header-grid {{
                display: flex;
                justify-content: space-between;
                align-items: center;
                border-bottom: 2px solid #123060;
                padding-bottom: 10px;
                margin-bottom: 14px;
            }}
            .title-box {{
                border: 2.5px solid #123060;
                border-radius: 12px;
                padding: 10px 18px;
                font-size: 23px;
                font-weight: 900 !important;
                width: 68%;
                text-align: center;
                background: #ffffff;
                color: #0a1f42 !important;
            }}
            .title-box span {{
                border-bottom: 3px double #123060;
                padding-bottom: 2px;
                display: inline-block;
            }}

            .marks-tag-box {{
                border: 2px solid #123060;
                border-radius: 8px;
                padding: 6px 12px;
                text-align: center;
                font-size: 14px;
                font-weight: 700;
                background: #ffffff;
            }}

            .dual-grid {{
                display: flex;
                gap: 16px;
            }}
            .col-half {{
                flex: 1;
                padding: 0 8px;
            }}
            .col-half:first-child {{
                border-right: 1.5px dashed #123060;
            }}

            .capsule-badge {{
                display: inline-block;
                border: 2px solid #123060;
                border-radius: 14px;
                padding: 2px 12px;
                font-size: 17.5px;
                font-weight: 800;
                margin-bottom: 6px;
                background: #ffffff;
            }}
            .capsule-tag {{
                display: inline-block;
                border: 1.5px solid #123060;
                border-radius: 10px;
                padding: 2px 14px;
                font-size: 14px;
                font-weight: 700;
                background: #ffffff;
            }}

            .box-step {{
                border: 1.5px solid #123060;
                border-radius: 8px;
                padding: 5px 12px;
                font-size: 14px;
                font-weight: 600;
                width: 82%;
                margin: auto;
                background: #ffffff;
            }}
            .arrow {{
                font-size: 15px;
                font-weight: 800;
                margin: 2px 0;
            }}
            .cloud-step {{
                border: 2px dashed #123060;
                border-radius: 16px;
                padding: 6px 14px;
                font-size: 14px;
                font-weight: 700;
                width: 85%;
                margin: auto;
                background: #ffffff;
            }}

            ul.hw-list {{
                margin: 6px 0 10px 0;
                padding-left: 18px;
                font-size: 14.5px;
                line-height: 1.55;
            }}
            ul.hw-list li {{ margin-bottom: 5px; }}

            .key-concept-box {{
                border: 1.5px dashed #123060;
                border-radius: 10px;
                padding: 8px 12px;
                font-size: 14px;
                margin: 8px 0;
                background: #fafafa;
                line-height: 1.45;
            }}

            .sec-heading {{
                font-size: 16px;
                font-weight: 700;
                text-decoration: underline;
                margin: 10px 0 6px 0;
            }}

            .hw-table {{
                width: 100%;
                border-collapse: collapse;
                font-size: 14px;
                margin-bottom: 12px;
                background: #ffffff;
            }}
            .hw-table th, .hw-table td {{
                border: 1.5px solid #123060;
                padding: 6px 8px;
                text-align: left;
            }}

            .exam-line {{
                border-top: 2px solid #123060;
                padding-top: 8px;
                margin-top: 12px;
                font-size: 14.5px;
                font-weight: 700;
                line-height: 1.45;
            }}

            .footer-tag {{
                position: absolute;
                bottom: 10px;
                right: 25px;
                font-size: 11px;
                opacity: 0.7;
                font-family: sans-serif;
            }}

            @media print {{
                .action-bar {{ display: none !important; }}
                body {{ padding: 0; background: none; }}
                .a4-paper {{ border: none; box-shadow: none; }}
            }}
        </style>
    </head>
    <body>
        <div class="action-bar">
            <button class="btn-action" onclick="downloadA4Image()">{lbl_btn_png}</button>
            <button class="btn-action" style="background:linear-gradient(135deg, #059669 0%, #047857 100%);" onclick="window.print()">{lbl_btn_pdf}</button>
        </div>

        <div class="a4-paper" id="a4Canvas">
            <!-- Header -->
            <div class="header-grid">
                <div class="title-box">
                    <span>{title}</span>
                </div>
                <div class="marks-tag-box">
                    <b>{subject_name}</b><br>
                    <span class="hl-red">🎯 {marks}</span>
                </div>
            </div>

            <!-- Flowchart -->
            {flow_html}

            <!-- 2-Column Notes -->
            <div class="dual-grid">
                <div class="col-half">
                    <div class="capsule-badge">① {t1.get('title','Part 1')}</div>
                    <p style="margin:4px 0 6px 0; font-size:14px;"><b>{lbl_def}</b> {t1.get('definition','')}</p>
                    <div class="sec-heading">{lbl_exam_points}</div>
                    <ul class="hw-list">{p1_html}</ul>
                    <div class="key-concept-box">
                        <b>{lbl_key_concept}</b><br>{t1.get('exam_key','')}
                    </div>
                </div>

                <div class="col-half">
                    <div class="capsule-badge">② {t2.get('title','Part 2')}</div>
                    <p style="margin:4px 0 6px 0; font-size:14px;"><b>{lbl_def}</b> {t2.get('definition','')}</p>
                    <div class="sec-heading">{lbl_clinical}</div>
                    <ul class="hw-list">{p2_html}</ul>
                    <div class="key-concept-box">
                        <b>{lbl_modern}</b><br>{t2.get('exam_key','')}
                    </div>
                </div>
            </div>

            <!-- Comparison Table -->
            {table_html}

            <!-- Exam Punch Line -->
            <div class="exam-line">
                {lbl_punch} → "{data.get('exam_punch_line','')}"
            </div>

            <div class="footer-tag">
                🌿 AyurVeda AI Handwritten Notes | Avishkar Alase
            </div>
        </div>

        <script>
            function downloadA4Image() {{
                const el = document.getElementById('a4Canvas');
                html2canvas(el, {{ scale: 2.2, useCORS: true }}).then(canvas => {{
                    const a = document.createElement('a');
                    a.download = '{topic_name.replace(" ", "_")}_A4_Notes.png';
                    a.href = canvas.toDataURL('image/png');
                    a.click();
                }});
            }}
        </script>
    </body>
    </html>
    """
    return full_html

# --- Top Navigation Bar ---
st.markdown("""
<div class="ganesha-navbar">
    <div class="brand-group">
        <div class="diya-icon">🪔</div>
        <div>
            <div class="brand-title">🌿 AyurVeda AI</div>
            <small style="color:#b45309; font-weight:800; letter-spacing:0.5px;">गणेशोत्सव विशेष पर्व | BAMS HANDWRITTEN STUDIO</small>
        </div>
    </div>
    <div class="vip-badge">
        <span>Avishkar Alase</span> <span style="background:#ea580c; color:white; border-radius:50%; width:15px; height:15px; display:inline-flex; align-items:center; justify-content:center; font-size:9px;">✓</span>
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
    <div class="ganesha-hero">
        <div class="festive-tag">🌺 ॥ श्री गणेशाय नमः ॥ 🌺</div>
        <h3 style="margin:0 0 8px 0; font-weight:900; font-size:24px;">🎯 BAMS A4 बॉलपेन Handwritten नोट्स</h3>
        <p style="margin:0; font-size:14px; opacity:0.95;">बुद्धीची देवता गणपती बाप्पाच्या आशीर्वादाने परिपूर्ण परीक्षा नोट्स: ठळक हेडिंग, महत्वाच्या शब्दांना <b>Red Highlight</b> आणि अचूक फ्लोचार्ट.</p>
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
                    - Write in very simple, natural Marathi as spoken in Maharashtra.
                    - Include authentic Sanskrit concepts/shlokas with simple Marathi explanation.
                    - Add simple English terms in parentheses for important points (उदा. 'पित्त दोषाचे स्वरूप व गुणधर्म (Pitta Dosha Swaroopa & Attributes)').
                    - Marks weightage in Marathi (उदा. '१० गुण - दीर्घोत्तरी (LAQ)' किंवा '५ गुण - लघुत्तरी (SAQ)').
                    """
                else:
                    lang_rule = """
                    STRICT ZERO-MARATHI INSTRUCTION (100% PURE ENGLISH):
                    - The student has selected 'Simple Indian English + Sanskrit'.
                    - ABSOLUTELY DO NOT WRITE ANY MARATHI/DEVANAGARI WORDS OR SCRIPTS ANYWHERE IN THE JSON!
                    - Every single word in the flowchart ('Step 1:', 'Step 2:', 'Final:'), definitions, tables, points, and punch line MUST be in ENGLISH.
                    - Write Sanskrit terms purely in English Roman transliteration (e.g. 'Pitta Prakopa', 'Ushna-Tikshna Guna', 'Rakta Dhatu', 'Pachaka Pitta', 'Virechana').
                    - Marks must be written as '10 Marks - LAQ' or '5 Marks - SAQ'.
                    """

                json_prompt = f"""
                You are a senior Ayurveda Professor and BAMS University Paper Setter.
                Subject: {subject}
                Topic: {topic}
                Language Selected: {language_preference}

                {lang_rule}

                Create crisp, highly readable handwritten exam notes for a single A4 page.
                Determine if this is typically a 10-Mark LAQ or 5-Mark SAQ in university exams.
                Only include flowchart steps IF it genuinely needs pathogenesis/stages.

                RED HIGHLIGHT INSTRUCTION:
                - Wrap all crucial medical keywords, cardinal symptoms, important drugs, or main mechanisms inside `<span class="hl-red">...</span>` so they get a red background highlight!
                Example: `<span class="hl-red">{'उष्ण-तीक्ष्ण' if is_marathi else 'Ushna-Tikshna'}</span>`, `<span class="hl-red">{'रक्त धातू' if is_marathi else 'Rakta Dhatu'}</span>`.
                
                Return ONLY valid JSON matching this schema:
                {{
                    "exam_marks": "{'१० गुण - दीर्घोत्तरी (LAQ)' if is_marathi else '10 Marks - LAQ'}",
                    "main_heading": "{'मराठीत मुख्य शीर्षक' if is_marathi else 'Clean Topic Title strictly in English'}",
                    "include_flowchart": true or false,
                    "flowchart_steps": [
                        "{'पायरी १: हेतू सेवन' if is_marathi else 'Step 1: Intake of Nidana / Causes'} with <span class='hl-red'>keyword</span>",
                        "{'पायरी २: अग्नी दुष्टी व दोष प्रकोप' if is_marathi else 'Step 2: Agni Dushti & Dosha Vitiation'}",
                        "{'पायरी ३: शरीरात रक्ताची दुष्टी' if is_marathi else 'Step 3: Spread into Rakta Dhatu'}",
                        "{'अंतिम: मुख्य लक्षणे व व्याधी निर्मिती' if is_marathi else 'Final: Manifestation of Pittaja Vyadhi'}"
                    ],
                    "entity_1": {{
                        "title": "{'संकल्पना १' if is_marathi else 'Concept 1 Title in English'}",
                        "definition": "{'१-२ ओळींची साधी व्याख्या' if is_marathi else '1-2 lines clean definition in English'} with <span class='hl-red'>keyword</span>",
                        "key_points": [
                            "Point 1 with <span class='hl-red'>vital keyword</span>",
                            "Point 2",
                            "Point 3 with <span class='hl-red'>cardinal symptom</span>"
                        ],
                        "exam_key": "1 core mechanism sentence with <span class='hl-red'>high-yield concept</span>"
                    }},
                    "entity_2": {{
                        "title": "{'संकल्पना २' if is_marathi else 'Concept 2 Title in English'}",
                        "definition": "{'१-२ ओळींची साधी व्याख्या' if is_marathi else '1-2 lines clean definition in English'} with <span class='hl-red'>keyword</span>",
                        "key_points": [
                            "Point 1 with <span class='hl-red'>vital keyword</span>",
                            "Point 2",
                            "Point 3 with <span class='hl-red'>treatment / chikitsa</span>"
                        ],
                        "exam_key": "1 clinical or contemporary correlation sentence with <span class='hl-red'>modern correlation</span>"
                    }},
                    "comparison_table": [
                        {{"feature": "{'स्वरूप व गुणधर्म' if is_marathi else 'Dominant Gunas'}", "point_1": "... with <span class='hl-red'>key</span>", "point_2": "..."}},
                        {{"feature": "{'प्रधान लक्षणे' if is_marathi else 'Clinical Signs'}", "point_1": "<span class='hl-red'>...</span>", "point_2": "<span class='hl-red'>...</span>"}},
                        {{"feature": "{'चिकित्सा उपक्रम' if is_marathi else 'Line of Treatment'}", "point_1": "<span class='hl-red'>...</span>", "point_2": "<span class='hl-red'>...</span>"}}
                    ],
                    "exam_punch_line": "{'परीक्षेसाठी १ मुख्य अंतिम निष्कर्ष सूत्र' if is_marathi else '1 memorable summary sentence strictly in English'} with <span class='hl-red'>core punch</span>."
                }}
                """

                with st.spinner("✍️ AI A4 Sheet तयार करत आहे..."):
                    try:
                        raw_json = cached_ask_gemini(json_prompt, as_json=True)
                        clean_json = raw_json.strip()
                        if clean_json.startswith("```json"): clean_json = clean_json[7:]
                        if clean_json.startswith("```"): clean_json = clean_json[3:]
                        if clean_json.endswith("```"): clean_json = clean_json[:-3]

                        sheet_data = json.loads(clean_json.strip())
                        a4_html = create_a4_handwritten_doc(sheet_data, subject, topic, is_marathi=is_marathi)

                        st.balloons()
                        st.success(f"✅ A4 Sheet तयार झाली आहे! (अपेक्षित गुण: {sheet_data.get('exam_marks')})")

                        st.components.v1.html(a4_html, height=1250, scrolling=True)

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
# TAB 2: MEDICINE FORMULATION & MANUFACTURING (औषध निर्माण विधी)
# =========================================================================
with tab2:
    st.markdown("""
    <div class="ganesha-hero" style="background: linear-gradient(135deg, #0f766e 0%, #0d9488 100%) !important; border-color: #5eead4;">
        <div class="festive-tag" style="background: rgba(255,255,255,0.18);">🌿 रसौषधी विधी</div>
        <h3 style="margin:0 0 8px 0; font-weight:900; font-size:24px;">🧪 रसशास्त्र व भैषज्य कल्पना स्पेशल</h3>
        <p style="margin:0; font-size:14px; opacity:0.95;">आयुर्वेदिक औषध घटक व सविस्तर निर्माण विधी सोप्या स्टेप्समध्ये शिका.</p>
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
                    med_prompt = f"Explain manufacturing of {medicine_name} ({dosage_form}) in simple spoken {m_lang} with ingredients table, purification, and steps."
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
