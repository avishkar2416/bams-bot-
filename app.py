import streamlit as st
from google import genai
from google.genai import types
import json
import time
import urllib.parse
from datetime import datetime

# --- Page Setup (CENTERED ADVANCED LAYOUT) ---
st.set_page_config(
    page_title="AyurVeda AI | Avishkar Alase",
    page_icon="🌿",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# =========================================================================
# 🎯 AUTOMATIC DYNAMIC FESTIVAL THEME ENGINE
# =========================================================================
def get_current_festival_theme():
    now = datetime.now()
    month, day = now.month, now.day

    if month == 9 and 12 <= day <= 26:
        return {
            "name": "ganeshotsav",
            "tag": "🌺 ॥ श्री गणेशाय नमः ॥ 🌺",
            "icon": "🪔",
            "title_sub": "गणेशोत्सव विशेष पर्व | BAMS HANDWRITTEN STUDIO",
            "bg": "radial-gradient(circle at 50% 0%, #fffbeb 0%, #fef3c7 25%, #fdfcf7 60%, #fff7ed 100%)",
            "hero_grad": "linear-gradient(135deg, #b45309 0%, #c2410c 45%, #991b1b 100%)",
            "hero_border": "#fef08a",
            "btn_grad": "linear-gradient(135deg, #ea580c 0%, #d97706 50%, #b45309 100%)",
            "border_color": "#fed7aa",
            "focus_color": "#f59e0b",
            "active_tab": "linear-gradient(135deg, #b45309 0%, #ea580c 100%)",
            "footer_text": "🌺 ॥ गणपती बाप्पा मोरया ॥ 🌿",
            "font_accent": "#92400e"
        }
    elif month == 10 and 10 <= day <= 24:
        return {
            "name": "navratri",
            "tag": "🌸 ॥ जय जगदंब - शुभ नवरात्री व विजयादशमी ॥ 🌸",
            "icon": "🔱",
            "title_sub": "शक्ती व विद्या पर्व विशेष | BAMS HANDWRITTEN STUDIO",
            "bg": "radial-gradient(circle at 50% 0%, #fff1f2 0%, #ffe4e6 30%, #fffdf9 70%, #fdf4ff 100%)",
            "hero_grad": "linear-gradient(135deg, #9f1239 0%, #be123c 45%, #881337 100%)",
            "hero_border": "#fda4af",
            "btn_grad": "linear-gradient(135deg, #e11d48 0%, #be123c 50%, #9f1239 100%)",
            "border_color": "#fecdd3",
            "focus_color": "#e11d48",
            "active_tab": "linear-gradient(135deg, #9f1239 0%, #e11d48 100%)",
            "footer_text": "🌸 ॥ सर्वमंगल मांगल्ये शिवे सर्वार्थ साधिके ॥ 🌿",
            "font_accent": "#881337"
        }
    elif month == 11 and 4 <= day <= 14:
        return {
            "name": "diwali",
            "tag": "🪔 ॥ ॐ महालक्ष्म्यै नमः - शुभ दीपावली ॥ 🪔",
            "icon": "✨",
            "title_sub": "दीपोत्सव महाविशेष पर्व | BAMS HANDWRITTEN STUDIO",
            "bg": "radial-gradient(circle at 50% 0%, #172554 0%, #1e1b4b 40%, #0f172a 100%)",
            "hero_grad": "linear-gradient(135deg, #d97706 0%, #b45309 40%, #78350f 100%)",
            "hero_border": "#fde047",
            "btn_grad": "linear-gradient(135deg, #eab308 0%, #ca8a04 50%, #a16207 100%)",
            "border_color": "#fde047",
            "focus_color": "#facc15",
            "active_tab": "linear-gradient(135deg, #ca8a04 0%, #eab308 100%)",
            "footer_text": "🪔 ॥ शुभ दीपावली - सुख समृद्धी लाभो ॥ 🌿",
            "font_accent": "#facc15"
        }
    else:
        return {
            "name": "ayurveda_classic",
            "tag": "🌿 ॥ नमामि धन्वंतरिमादिदेवम् - BAMS अकॅडेमिक स्टुडिओ ॥ 🌿",
            "icon": "🌱",
            "title_sub": "NCISM BAMS A4 HANDWRITTEN STUDIO",
            "bg": "radial-gradient(circle at 50% 0%, #ecfdf5 0%, #f0fdf4 35%, #f8fafc 70%, #e6fcf5 100%)",
            "hero_grad": "linear-gradient(135deg, #064e3b 0%, #047857 50%, #065f46 100%)",
            "hero_border": "#a7f3d0",
            "btn_grad": "linear-gradient(135deg, #059669 0%, #047857 50%, #064e3b 100%)",
            "border_color": "#cbd5e1",
            "focus_color": "#059669",
            "active_tab": "linear-gradient(135deg, #064e3b 0%, #059669 100%)",
            "footer_text": "🌿 ॥ आरोग्यं परमं भाग्यम् ॥ 🌿",
            "font_accent": "#064e3b"
        }

th = get_current_festival_theme()

# --- CSS STYLES WITH PRINT OPTIMIZATION ---
st.markdown(f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@500;600;700;800;900&family=Mukta:wght@400;600;700;800;900&display=swap');

    html, body, .stApp {{
        background: {th['bg']} !important;
        background-attachment: fixed !important;
        font-family: 'Mukta', 'Plus Jakarta Sans', sans-serif !important;
        color: #0f172a !important;
    }}

    .main .block-container {{
        max-width: 820px !important;
        padding-top: 1.5rem !important;
        padding-bottom: 2.5rem !important;
        margin: auto !important;
    }}

    @keyframes themePulse {{
        0% {{ box-shadow: 0 0 0 0 rgba(234, 88, 12, 0.5); }}
        70% {{ box-shadow: 0 0 0 16px rgba(234, 88, 12, 0); }}
        100% {{ box-shadow: 0 0 0 0 rgba(234, 88, 12, 0); }}
    }}

    .dynamic-navbar {{
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 14px 22px;
        background: rgba(255, 255, 255, 0.92) !important;
        backdrop-filter: blur(18px);
        border: 2px solid {th['border_color']} !important;
        border-radius: 24px;
        margin-bottom: 14px;
        box-shadow: 0 12px 35px -8px rgba(0, 0, 0, 0.08);
    }}
    .brand-title {{
        font-size: 21px;
        font-weight: 900;
        background: {th['btn_grad']};
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 0;
    }}
    .vip-badge {{
        background: #ffffff !important;
        border: 1.5px solid {th['focus_color']};
        padding: 8px 18px;
        border-radius: 14px;
        font-size: 13.5px;
        font-weight: 800;
        color: {th['font_accent']} !important;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.06);
    }}

    .dynamic-hero {{
        background: {th['hero_grad']} !important;
        padding: 24px 22px;
        border-radius: 22px;
        margin-bottom: 24px;
        color: #ffffff !important;
        box-shadow: 0 16px 36px -10px rgba(0, 0, 0, 0.25);
        border: 2px solid {th['hero_border']};
    }}
    .dynamic-hero * {{ color: #ffffff !important; }}
    .festive-tag {{
        display: inline-flex;
        align-items: center;
        gap: 6px;
        background: rgba(255, 255, 255, 0.22);
        padding: 5px 14px;
        border-radius: 30px;
        font-size: 12.5px;
        font-weight: 800;
        margin-bottom: 8px;
        border: 1px solid rgba(255, 255, 255, 0.35);
    }}

    div[data-baseweb="select"] > div,
    div[data-baseweb="input"] > div {{
        background-color: rgba(255, 255, 255, 0.95) !important;
        border: 2px solid {th['border_color']} !important;
        border-radius: 16px !important;
        transition: all 0.3s ease !important;
    }}
    div[data-baseweb="select"] > div:hover,
    div[data-baseweb="input"] > div:hover {{
        border-color: {th['focus_color']} !important;
        transform: translateY(-2px);
    }}

    div.stButton > button {{
        background: {th['btn_grad']} !important;
        color: #ffffff !important;
        border: 2px solid {th['hero_border']} !important;
        border-radius: 18px !important;
        padding: 16px 34px !important;
        font-size: 17px !important;
        font-weight: 900 !important;
        cursor: pointer !important;
        transition: all 0.25s ease !important;
        animation: themePulse 2.5s infinite;
    }}
    div.stButton > button:hover {{
        transform: translateY(-2px) scale(1.015) !important;
    }}

    .stTabs [data-baseweb="tab-list"] {{
        gap: 10px;
        margin-bottom: 20px;
    }}
    .stTabs [data-baseweb="tab"] {{
        background-color: rgba(255, 255, 255, 0.85) !important;
        border-radius: 16px !important;
        padding: 10px 18px !important;
        font-weight: 800 !important;
        border: 1.5px solid {th['border_color']} !important;
    }}
    .stTabs [aria-selected="true"] {{
        background: {th['active_tab']} !important;
        border-color: {th['focus_color']} !important;
        color: #ffffff !important;
    }}
    .stTabs [aria-selected="true"] * {{ color: #ffffff !important; }}

    div[data-testid="stRadio"] > div[role="radiogroup"] {{
        display: flex !important;
        gap: 12px !important;
        background: rgba(255, 255, 255, 0.75) !important;
        padding: 6px !important;
        border-radius: 18px !important;
        border: 1.5px solid {th['border_color']} !important;
    }}
    div[data-testid="stRadio"] label {{
        background: #ffffff !important;
        border: 2px solid {th['border_color']} !important;
        border-radius: 14px !important;
        padding: 10px 16px !important;
        cursor: pointer !important;
        display: flex !important;
        align-items: center !important;
        flex: 1 !important;
    }}
    div[data-testid="stRadio"] label:has(input:checked) {{
        background: linear-gradient(135deg, #ffffff 0%, #fffbeb 100%) !important;
        border-color: {th['focus_color']} !important;
        transform: scale(1.02) !important;
    }}
    div[data-testid="stRadio"] label div[data-testid="stMarkdownContainer"] p {{
        font-weight: 800 !important;
        color: {th['font_accent']} !important;
        font-size: 14.5px !important;
    }}

    .notes-card-container {{
        background: #ffffff;
        border: 2px solid {th['border_color']};
        border-radius: 20px;
        padding: 24px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.06);
        margin-top: 15px;
    }}

    .wa-share-btn {{
        display: inline-flex;
        align-items: center;
        gap: 8px;
        background: #25d366;
        color: white !important;
        text-decoration: none;
        padding: 11px 20px;
        border-radius: 12px;
        font-weight: 800;
        font-size: 14px;
        box-shadow: 0 4px 12px rgba(37,211,102,0.3);
    }}

    .app-footer {{
        text-align: center;
        padding: 40px 10px 15px 10px;
        font-size: 13.5px;
        color: {th['font_accent']} !important;
        font-weight: 700;
    }}

    /* Clean Native Print Optimization for PDF Saving */
    @media print {{
        header, footer, .stButton, div[data-baseweb="select"], div[data-baseweb="input"], .stTabs [data-baseweb="tab-list"], .dynamic-navbar, .dynamic-hero, .no-print {{
            display: none !important;
        }}
        .main .block-container {{
            max-width: 100% !important;
            padding: 0 !important;
            margin: 0 !important;
        }}
        .notes-card-container {{
            border: none !important;
            box-shadow: none !important;
            padding: 0 !important;
        }}
        body {{
            background: #ffffff !important;
            color: #000000 !important;
        }}
    }}
</style>
""", unsafe_allow_html=True)

# --- API Setup ---
api_key = st.secrets.get("GEMINI_API_KEY", "")
if not api_key:
    st.error("⚠️ कृपया Settings > Secrets मध्ये GEMINI_API_KEY कॉन्फिगर करा.")
    st.stop()

# Use Google GenAI official client with direct fallback routing
client = genai.Client(api_key=api_key)

# =========================================================================
# 🎯 DYNAMIC MODEL DISCOVERY ENGINE (Auto-Selects Active Model)
# =========================================================================
@st.cache_data(show_spinner=False, ttl=86400)
def get_working_models():
    found = []
    try:
        for m in client.models.list():
            name = m.name.replace("models/", "")
            actions = getattr(m, 'supported_generation_methods', []) or getattr(m, 'supported_actions', [])
            if any("generateContent" in a for a in actions):
                if "flash" in name:
                    found.insert(0, name)
                else:
                    found.append(name)
    except Exception:
        pass

    # Reliable active fallbacks
    fallbacks = [
        "gemini-2.5-flash",
        "gemini-2.0-flash",
        "gemini-1.5-flash"
    ]
    for fb in fallbacks:
        if fb not in found:
            found.append(fb)
    return found

@st.cache_data(show_spinner=False, ttl=86400)
def cached_ask_gemini(prompt: str, as_json: bool = False):
    models_to_try = get_working_models()
    last_error = ""

    for model_name in models_to_try:
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
            last_error = str(e)
            if "429" in last_error or "RESOURCE_EXHAUSTED" in last_error:
                time.sleep(3)
            continue

    raise RuntimeError(f"API त्रुटी: {last_error[:120]}")

# =========================================================================
# अस्सल फोटोसारखी A4 HANDWRITTEN NOTE RENDERER
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
        <div style="text-align:center; margin: 6px 0 12px 0;">{steps_inner}</div>
        """
        
    chikitsa_list = "".join([f"<li>{c}</li>" for c in data.get("chikitsa", [])])
    aushadha_list = "".join([f"<li>{a}</li>" for a in data.get("aushadha", [])])
    punch_line = data.get("punch_line", "")

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
                margin: 0; padding: 15px 5px;
                display: flex; flex-direction: column; align-items: center;
                font-family: {'"Mukta", sans-serif' if is_marathi else '"Patrick Hand", "Mukta", sans-serif'};
            }}
            .action-bar {{ margin-bottom: 16px; display: flex; gap: 12px; font-family: sans-serif; }}
            .btn-action {{
                background: linear-gradient(135deg, #0284c7 0%, #0369a1 100%);
                color: white; border: none; padding: 12px 24px; font-size: 15px; font-weight: 800;
                border-radius: 12px; cursor: pointer; box-shadow: 0 4px 14px rgba(2,132,199,0.35);
            }}
            .a4-container {{
                width: 780px; min-height: 1160px; background-color: #fcfbf7;
                border: 2px solid #0f2b5c; box-shadow: 0 12px 35px rgba(0,0,0,0.18);
                padding: 24px 28px; box-sizing: border-box; color: #0b2559; position: relative;
                font-size: 15.5px; line-height: 1.45;
            }}
            .hl-red {{ background-color: #ffe4e6; color: #991b1b; padding: 0 4px; border-radius: 3px; font-weight: 700; }}
            .u-red {{ text-decoration: underline; text-decoration-color: #ef4444; text-decoration-thickness: 1.8px; }}
            .header-top {{ display: flex; justify-content: space-between; align-items: center; border-bottom: 2px solid #0f2b5c; padding-bottom: 10px; margin-bottom: 12px; }}
            .ganesha-namah {{ font-size: 16px; font-weight: 700; color: #0b2559; width: 25%; }}
            .main-title-box {{ border: 2px solid #0f2b5c; border-radius: 8px; padding: 4px 22px; font-size: 26px; font-weight: 900; background: #ffffff; }}
            .marks-box {{ border: 1.8px solid #0f2b5c; border-radius: 6px; padding: 4px 10px; text-align: center; font-size: 13.5px; background: #ffffff; }}
            .sheet-grid {{ display: flex; gap: 16px; }}
            .left-col {{ flex: 1.25; padding-right: 12px; border-right: 1.5px solid #0f2b5c; }}
            .right-col {{ flex: 1; padding-left: 6px; }}
            .sec-title {{ font-weight: 800; font-size: 16px; margin: 8px 0 3px 0; }}
            ul.hw-list {{ margin: 3px 0 8px 0; padding-left: 18px; line-height: 1.45; }}
            ul.hw-list li {{ margin-bottom: 3px; }}
            .side-card {{ border: 1.8px solid #0f2b5c; border-radius: 8px; padding: 8px 12px; background: #ffffff; margin-bottom: 12px; font-size: 14.5px; }}
            .side-card-title {{ font-weight: 800; border-bottom: 1.5px solid #0f2b5c; padding-bottom: 2px; margin-bottom: 5px; text-align: center; }}
            .hw-box {{ border: 1.8px solid #0f2b5c; border-radius: 6px; padding: 4px 8px; font-size: 14px; background: #ffffff; margin: auto; width: 90%; }}
            .hw-arrow {{ font-size: 15px; font-weight: 900; margin: 2px 0; }}
            .hw-box-final {{ border: 1.8px solid #0f2b5c; border-radius: 6px; padding: 5px 8px; font-size: 14px; font-weight: 800; background: #ffe4e6; color: #991b1b; margin: auto; width: 90%; }}
            .punch-box {{ border-top: 2px solid #0f2b5c; margin-top: 12px; padding-top: 6px; font-size: 15px; font-weight: 800; }}
            .footer-sign {{ position: absolute; bottom: 8px; right: 20px; font-size: 12px; font-family: 'Patrick Hand', sans-serif; color: #047857; font-weight: 800; }}
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
            <div class="header-top">
                <div class="ganesha-namah">॥ श्री गणेशाय नमः ॥</div>
                <div class="main-title-box">{title}</div>
                <div class="marks-box">
                    <span style="color:#0369a1; font-weight:700;">{subject_name}</span><br>
                    <span style="color:#b91c1c; font-weight:800; border-bottom: 1.5px solid #ef4444;">{marks}</span>
                </div>
            </div>

            <div class="sheet-grid">
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

            <div class="punch-box">
                ✍️ <span class="u-red">{lbl_punch}</span> :-<br>
                <div style="text-align:center; margin-top:4px; font-size:16px;">
                    "{punch_line}"
                </div>
            </div>

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
st.markdown(f"""
<div class="dynamic-navbar">
    <div style="display:flex; align-items:center; gap:10px;">
        <div style="font-size:26px;">{th['icon']}</div>
        <div>
            <div class="brand-title">🌿 AyurVeda AI</div>
            <small style="color:{th['font_accent']}; font-weight:800; letter-spacing:0.5px;">{th['title_sub']}</small>
        </div>
    </div>
    <div class="vip-badge">
        <span>Avishkar Alase</span> ✓
    </div>
</div>
""", unsafe_allow_html=True)

# --- 5 Main Tabs ---
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📖 BAMS स्टडी नोट्स व प्रश्नसंच (Syllabus & PYQ)",
    "🧪 औषध घटक व निर्माण विधी (Medicine & Manufacturing)",
    "🎯 AI BAMS Viva-Voce Simulator (तोंडी परीक्षा)",
    "🩺 Clinical Case Study (केस प्रेझेंटेशन)",
    "🔬 Research & Evidence (वैज्ञानिक संशोधन)"
])

# =========================================================================
# TAB 1: SYLLABUS STUDY NOTES & UNIVERSITY PYQ SOLVER
# =========================================================================
with tab1:
    st.markdown(f"""
    <div class="dynamic-hero">
        <div class="festive-tag">{th['tag']}</div>
        <h3 style="margin:0 0 6px 0; font-weight:900;">🎯 BAMS A4 बॉलपेन Handwritten नोट्स व PYQ Solver</h3>
        <p style="margin:0; font-size:13.5px; opacity:0.95;">ठळक मुख्य हेडिंग, सुवाच्य अक्षरे, महत्वाच्या शब्दांना <b>Red Highlight</b>, फ्लोचार्ट आणि मागील ५ वर्षांचे विद्यापीठ प्रश्नोत्तर.</p>
    </div>
    """, unsafe_allow_html=True)

    bams_year = st.selectbox(
        "🎓 BAMS वर्ष निवडा (Academic Year):",
        [
            "BAMS 1st Professional (प्रथम वर्ष)",
            "BAMS 2nd Professional (द्वितीय वर्ष)",
            "BAMS 3rd Professional (तृतीय वर्ष)",
            "BAMS Final Professional (अंतिम वर्ष)"
        ]
    )

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

    study_mode = st.selectbox(
        "🎯 अभ्यासाचा प्रकार निवडा (Study Mode):",
        [
            "📋 A4 Blue Ballpen Handwritten Sheet (अस्सल A4 पेन नोट्स)",
            "🎯 MUHS / NCISM Past 5 Years Questions & Model Answer Key",
            "📖 Comprehensive Notes (संपूर्ण सविस्तर अभ्यास नोट्स)",
            "📜 Only Shlokas & Meanings (फक्त मूळ श्लोक, अन्वय व अर्थ)",
            "📝 10-Mark LAQ Answer Format (दीर्घोत्तरी प्रश्न-उत्तर फॉरमॅट)",
            "⚡ Quick Revision / Viva Voce Points (तोंडी परीक्षेसाठी महत्त्वाचे मुद्दे)"
        ]
    )

    language_preference = st.radio(
        "🌐 माध्यम निवडा (Select Study Medium):",
        [
            "🚩 मराठी (संस्कृत + अर्थ)",
            "🌿 Simple English + Sanskrit"
        ],
        horizontal=True
    )

    topic = st.text_input(
        "🔍 अभ्यासाचा विषय / प्रश्न टाका:",
        placeholder="उदा. Pitta Dosha, Garavisha vs Dooshivisha, किंवा Virya"
    )

    generate_notes_btn = st.button("🚀 सविस्तर अभ्यास नोट्स तयार करा", key="btn_notes", use_container_width=True)

    if generate_notes_btn:
        if not topic.strip():
            st.warning("⚠️ कृपया अभ्यासाचा विषय प्रविष्ट करा.")
        else:
            is_marathi = "मराठी" in language_preference

            # Case A: A4 Blue Ballpen Handwritten Sheet
            if "A4 Blue Ballpen" in study_mode:
                if is_marathi:
                    lang_rule = "Write in natural, simple spoken Marathi with Sanskrit terms and simple English in parentheses."
                else:
                    lang_rule = "STRICT INSTRUCTION: The user selected 'Simple English + Sanskrit'. Write 100% in pure English Roman script. All titles and terms in English."

                json_prompt = f"""
                You are a senior Ayurveda Professor and BAMS University Paper Setter.
                Subject: {subject}
                Topic: {topic}
                Language Selected: {language_preference}

                {lang_rule}

                Generate crisp exam notes strictly matching this JSON schema:
                {{
                    "title": "{topic}",
                    "marks": "10 Marks (LAQ)",
                    "definition": "{'पाचन, दहन व उष्णता निर्माण करणारे द्रव्य.' if is_marathi else 'The bio-principle responsible for transformation and potency.'}",
                    "definition_sub": "{'शरीरातील परिवर्तनाचे मुख्य तत्त्व' if is_marathi else 'Core principle in the body'}",
                    "sthana_main": "{'आमाशय, ग्रहणी, लहान आंत्र' if is_marathi else 'Grahani, Amashaya, Small intestine'}",
                    "sthana_sub": "{'रक्त, यकृत, प्लीहा, स्वेद, नेत्र' if is_marathi else 'Rakta, Yakrit, Pleeha, Sweda'}",
                    "gunadharma": "<span class='hl-red'>{'उष्ण, तीक्ष्ण, लघु' if is_marathi else 'Ushna, Tikshna, Laghu'}</span>",
                    "gunadharma_en": "Hot, Sharp, Light",
                    "karya": [
                        "{'अन्न पचन व रूपांतरण' if is_marathi else 'Digestion & tissue metabolism'}",
                        "{'देहाला उष्णता प्रदान करणे' if is_marathi else 'Action potential'}"
                    ],
                    "types": [
                        {{"name": "{'शीत वीर्य' if is_marathi else 'Sheeta Virya'}", "desc": "{'सोम प्रधान' if is_marathi else 'Soma / Cooling dominant'}"}},
                        {{"name": "{'उष्ण वीर्य' if is_marathi else 'Ushna Virya'}", "desc": "{'अग्नी प्रधान' if is_marathi else 'Agni / Heating dominant'}"}}
                    ],
                    "nidana": [
                        "{'अतिउष्ण, अम्ल, लवण आहार' if is_marathi else 'Excessive intake of antagonistic diet'}"
                    ],
                    "lakshana": [
                        "{'दाह, तृष्णा' if is_marathi else 'Excessive heat, burning sensation'}"
                    ],
                    "sidebar_box_title": "{'Core Correlation' if is_marathi else 'Core Concept'}",
                    "sidebar_box_points": ["Potency", "Action Capability", "Metabolism"],
                    "samprapti_steps": [
                        "{'निदान सेवन' if is_marathi else 'Step 1: Intake of Nidana'}",
                        "{'दोष प्रकोप' if is_marathi else 'Step 2: Dosha Prakopa'}",
                        "{'धातु शैथिल्य' if is_marathi else 'Step 3: Dhatu Vitiation'}",
                        "{'व्याधी निर्मिती' if is_marathi else 'Final: Manifestation of Disease'}"
                    ],
                    "chikitsa": [
                        "{'दोषानुकूल चिकित्सा व शमन' if is_marathi else 'Dosha specific Pacification'}",
                        "<span class='hl-red'>{'शोधन' if is_marathi else 'Purification'}</span> {'हे श्रेष्ठ' if is_marathi else 'is the prime therapy'}"
                    ],
                    "aushadha": [
                        "{'गुग्गुळू / आवळा' if is_marathi else 'Amalaki / Guggulu'}",
                        "{'गुडुची (Guduchi)' if is_marathi else 'Guduchi'}"
                    ],
                    "punch_line": "{'द्रव्याचे कर्म सामर्थ्य म्हणजेच वीर्य होय.' if is_marathi else 'Virya is the quintessential potency through which action is achieved.'}"
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
                        st.success(f"✅ A4 Sheet तयार झाली आहे! (अपेक्षित गुण: {sheet_data.get('marks')})")
                        
                        share_text = f"🌿 *AyurVeda AI BAMS Notes*\n📚 *Subject:* {subject}\n🎯 *Topic:* {topic}\n✍️ *Punch Line:* {sheet_data.get('punch_line')}\n\nStudy Bot द्वारे तयार केलेली A4 Note!"
                        encoded_wa = urllib.parse.quote(share_text)
                        wa_url = f"[https://api.whatsapp.com/send?text=](https://api.whatsapp.com/send?text=){encoded_wa}"
                        
                        st.markdown(f"""
                        <div style="margin-bottom: 15px;">
                            <a href="{wa_url}" target="_blank" class="wa-share-btn">
                                📲 WhatsApp Study Group वर Share करा
                            </a>
                        </div>
                        """, unsafe_allow_html=True)

                        st.components.v1.html(a4_html, height=1300, scrolling=True)

                    except Exception as e:
                        st.error(f"त्रुटी: {e}")

            # Case B: MUHS / NCISM Past 5 Years Questions & Model Answer Key
            elif "Past 5 Years Questions" in study_mode:
                pyq_prompt = f"""
                You are a senior MUHS / NCISM BAMS University Chief Examiner and Paper Setter.
                Subject: {subject}
                Topic: {topic}
                Language Selected: {language_preference}

                Create a definitive, high-yield 'University Past 5-Year Question Paper & Model Answer Analysis' for this topic:
                1. 🎯 Top 3 Frequently Asked University Questions:
                   - Long Answer Question (LAQ - 10 Marks)
                   - Short Answer Question (SAQ - 5 Marks)
                   - Very Short / Viva Question (2 Marks)
                2. ✍️ Examiner's Step-by-Step Model Answer Blueprint (How to score 10/10 Marks):
                   - Sequence of writing (Shloka -> Definition -> Nirukti -> Types/Features -> Flowchart -> Chikitsa).
                   - Crucial Sanskrit keywords examiner searches for.
                3. ⚠️ Common Mistakes to Avoid (Where students lose marks in this topic).
                4. 💡 Pro Examiner Tip for Top University Ranks.

                Format with bold headings, clean bullet points, and high readability.
                """
                with st.spinner("🎯 AI विद्यापीठ मागील ५ वर्षांचे प्रश्न व मॉडेल आन्सर तयार करत आहे..."):
                    try:
                        pyq_res = cached_ask_gemini(pyq_prompt, as_json=False)
                        st.balloons()
                        st.success("✅ University PYQ & Model Answer Key तयार झाली आहे!")
                        st.markdown(pyq_res)
                    except Exception as e:
                        st.error(f"त्रुटी: {e}")

            # Case C: Comprehensive Notes & Other Modes (WITH INSTANT PDF EXPORT)
            else:
                system_instruction = f"""
                You are a senior Ayurveda Acharya according to NCISM standards.
                Academic Level: {bams_year}, Subject: {subject}, Study Mode: {study_mode}, Topic: {topic}, Language: {language_preference}.
                Generate tailored, high-yield study material strictly aligned with '{study_mode}'.
                - If English is chosen, write purely in English with transliterated Sanskrit terms.
                - Format Sanskrit Shlokas inside blockquotes (> "Shloka").
                - Bold all key terms and format with clear, beautiful headings.
                """
                with st.spinner(f"⚡ AI आयुर्वेद तज्ज्ञ '{study_mode}' नुसार सविस्तर नोट्स तयार करत आहे..."):
                    try:
                        notes_text = cached_ask_gemini(system_instruction, as_json=False)
                        st.balloons()
                        st.success("✅ नोट्स तयार झाल्या आहेत!")

                        share_text = f"🌿 *AyurVeda AI Comprehensive Notes*\n📚 *Subject:* {subject}\n🎯 *Topic:* {topic}\n\nStudy Bot द्वारे तयार केलेली सविस्तर नोट!"
                        encoded_wa = urllib.parse.quote(share_text)
                        wa_url = f"[https://api.whatsapp.com/send?text=](https://api.whatsapp.com/send?text=){encoded_wa}"

                        # PDF प्रिंटर व WhatsApp शेअर बटणे
                        st.markdown(f"""
                        <div class="no-print" style="display: flex; gap: 12px; margin-bottom: 16px; flex-wrap: wrap;">
                            <button onclick="window.print()" style="
                                background: linear-gradient(135deg, #059669 0%, #047857 100%);
                                color: white;
                                border: none;
                                padding: 10px 22px;
                                font-size: 14.5px;
                                font-weight: 800;
                                border-radius: 12px;
                                cursor: pointer;
                                box-shadow: 0 4px 14px rgba(5,150,105,0.3);
                                display: inline-flex;
                                align-items: center;
                                gap: 6px;
                            ">
                                📄 PDF डाऊनलोड / सेव्ह करा
                            </button>
                            <a href="{wa_url}" target="_blank" class="wa-share-btn">
                                📲 WhatsApp वर Share करा
                            </a>
                        </div>
                        """, unsafe_allow_html=True)

                        # सुंदर कार्ड कंटेनरमध्ये नोट्स दाखवणे
                        st.markdown(f"""
                        <div class="notes-card-container">
                            {notes_text}
                        </div>
                        """, unsafe_allow_html=True)

                    except Exception as e:
                        st.error(f"त्रुटी: {e}")

# =========================================================================
# TAB 2: MEDICINE FORMULATION & MANUFACTURING
# =========================================================================
with tab2:
    st.markdown("""
    <div class="dynamic-hero" style="background: linear-gradient(135deg, #0f766e 0%, #0d9488 100%) !important; border-color: #5eead4;">
        <div class="festive-tag" style="background: rgba(255,255,255,0.18);">🌿 रसौषधी विधी</div>
        <h3 style="margin:0 0 6px 0; font-weight:900;">🧪 रसशास्त्र व भैषज्य कल्पना स्पेशल</h3>
        <p style="margin:0; font-size:13.5px; opacity:0.95;">आयुर्वेदिक औषध घटक व सविस्तर निर्माण विधी सोप्या स्टेप्समध्ये शिका.</p>
    </div>
    """, unsafe_allow_html=True)

    dosage_form = st.selectbox(
        "🏺 औषधाचा प्रकार (Dosage Form):",
        ["Vati / Gutika (गोळी / वटी)", "Churna (चूर्ण)", "Asava & Arishta (आसव व अरिष्ट)", "Taila / Ghrita (सिद्ध तेल व घृत)", "Bhasma & Pishti (भस्म व पिष्टी)"]
    )
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

# =========================================================================
# TAB 3: AI BAMS VIVA-VOCE SIMULATOR
# =========================================================================
with tab3:
    st.markdown("""
    <div class="dynamic-hero" style="background: linear-gradient(135deg, #1e1b4b 0%, #312e81 100%) !important; border-color: #a5b4fc;">
        <div class="festive-tag" style="background: rgba(255,255,255,0.18);">🎓 तोंडी परीक्षा सिम्युलेटर</div>
        <h3 style="margin:0 0 6px 0; font-weight:900;">🎯 BAMS University Practical & Viva Simulator</h3>
        <p style="margin:0; font-size:13.5px; opacity:0.95;">External Examiner च्या दृष्टिकोनातून विचारले जाणारे ५ महत्त्वाचे प्रश्न व आदर्श उत्तरे.</p>
    </div>
    """, unsafe_allow_html=True)

    viva_sub = st.selectbox(
        "📚 Viva साठी विषय:",
        ["Kriya Sharir", "Rachana Sharir", "Dravyaguna", "Rasa Shastra", "Agada Tantra", "Kayachikitsa", "Shalya Tantra"],
        key="viva_sub"
    )
    viva_lang = st.radio("🌐 Viva भाषा:", ["मराठी + Sanskrit Terms", "Simple Indian English"], horizontal=True, key="viva_lang")

    viva_topic = st.text_input("🎙️ Examiner कोणत्या विषयावर प्रश्न विचारतील?", placeholder="उदा. Pitta Sthana, Ashwagandha Guna, Vatsanabha Shodhana", key="viva_top")

    if st.button("🔥 AI Examiner कडून तोंडी परीक्षा प्रश्न घ्या", key="btn_viva", use_container_width=True):
        if not viva_topic.strip():
            st.warning("⚠️ कृपया विषयाचे नाव टाका.")
        else:
            with st.spinner("🎙️ External Examiner प्रश्न तयार करत आहेत..."):
                try:
                    viva_prompt = f"""
                    You are a strict University External Examiner for BAMS Practical Exams.
                    Subject: {viva_sub}
                    Topic: {viva_topic}
                    Language: {viva_lang}

                    Generate 5 high-yield, tricky Viva-Voce questions with precise model answers that students must speak:
                    1. Direct Definition / Shloka Reference Question
                    2. Clinical / Dosha Action Question
                    3. Tricky Difference / Exception Question
                    4. Dravyaguna / Formulation Question
                    5. Modern Diagnostic Correlation Question

                    Format beautifully with Bold Keywords and Examiner Tips.
                    """
                    viva_res = cached_ask_gemini(viva_prompt, as_json=False)
                    st.success("✅ Viva प्रश्नावली तयार झाली!")
                    st.markdown(viva_res)
                except Exception as e:
                    st.error(f"त्रुटी: {e}")

# =========================================================================
# TAB 4: CLINICAL CASE STUDY
# =========================================================================
with tab4:
    st.markdown("""
    <div class="dynamic-hero" style="background: linear-gradient(135deg, #0369a1 0%, #0284c7 100%) !important; border-color: #7dd3fc;">
        <div class="festive-tag" style="background: rgba(255,255,255,0.18);">🩺 क्लिनिकल ओपीडी व IPD केसशीट</div>
        <h3 style="margin:0 0 6px 0; font-weight:900;">📋 Complete Ayurvedic Clinical Case Presentation</h3>
        <p style="margin:0; font-size:13.5px; opacity:0.95;">Kayachikitsa, Panchakarma व Shalya साठी अष्टविध परीक्षा, संप्राप्ती विघटन, दीपन-पाचन व प्रत्यक्ष उपचार योजना.</p>
    </div>
    """, unsafe_allow_html=True)

    case_subject = st.selectbox(
        "🏥 क्लिनिकल विभाग (Department):",
        ["Kayachikitsa (कायचिकित्सा)", "Panchakarma (पंचकर्म)", "Shalya Tantra (शल्य)", "Shalakya (नेत्र/कर्ण/नासा)", "Stri Roga & Prasuti (स्त्रीरोग)", "Kaumarbhritya (बालरोग)"],
        key="case_sub"
    )
    case_lang = st.radio("🌐 भाषा:", ["मराठी + Clinical English", "Simple Indian English + Sanskrit"], horizontal=True, key="cs_lang")

    case_topic = st.text_input("🩺 आजाराचे नाव / मुख्य लक्षणे टाका:", placeholder="उदा. Amlapitta (GERD), Sandhivata (Osteoarthritis), Tamaka Shwasa (Asthma)", key="cs_top")

    if st.button("📋 संपूर्ण क्लिनिकल केसशीट तयार करा", key="btn_case", use_container_width=True):
        if not case_topic.strip():
            st.warning("⚠️ कृपया आजाराचे नाव टाका.")
        else:
            with st.spinner(f"🩺 AI क्लिनिकल तज्ज्ञ '{case_topic}' ची परिपूर्ण हॉस्पिटल केसशीट तयार करत आहे..."):
                try:
                    case_prompt = f"""
                    You are a Chief Clinical Physician and BAMS PG Guide in an Ayurvedic Hospital.
                    Department: {case_subject}
                    Disease/Condition: {case_topic}
                    Language: {case_lang}

                    Generate a complete, professional Ayurvedic Clinical Case Presentation Paper containing:
                    1. 👤 Patient Profile: Age, Gender, Prakriti (Vata/Pitta/Kapha), Agni Status, Kostha.
                    2. ⚠️ Chief Complaints (Pradhana Vedana) & Hetu Sevana (Aharaja, Viharaja, Manasika).
                    3. 🔍 Ashtavidha & Dashavidha Pariksha (Nadi, Jihwa, Mala, Mutra, etc.).
                    4. 🧬 Samprapti Vighatana: Dosha, Dushya, Srotas Dushti Prakara (Sanga, Vimargagamana), Udbhavasthana.
                    5. 💊 Step-by-Step Treatment Protocol:
                       - Phase 1: Deepana & Pachana (Amapachana drugs & dosage).
                       - Phase 2: Shamana Chikitsa (Classical Rasaushadhi, Churna, Kashaya with Anupana).
                       - Phase 3: Shodhana / Panchakarma (Specific Karma like Vamana, Virechana, or Basti if indicated).
                    6. 🥗 Pathya & Apathya (Diet & Lifestyle Chart).
                    7. 🔬 Modern Diagnostic Link & 15-day Clinical Follow-up Prognosis.

                    Format cleanly with bold subheadings and clinical bullet points.
                    """
                    case_res = cached_ask_gemini(case_prompt, as_json=False)
                    st.success("✅ क्लिनिकल केस प्रेझेंटेशन तयार झाले!")
                    st.markdown(case_res)
                except Exception as e:
                    st.error(f"त्रुटी: {e}")

# =========================================================================
# TAB 5: RESEARCH & EVIDENCE
# =========================================================================
with tab5:
    st.markdown("""
    <div class="dynamic-hero" style="background: linear-gradient(135deg, #4338ca 0%, #6366f1 100%) !important; border-color: #c7d2fe;">
        <div class="festive-tag" style="background: rgba(255,255,255,0.18);">🔬 सायंटिफिक ॲव्हिडन्स व क्लिनिकल ट्रायल्स</div>
        <h3 style="margin:0 0 6px 0; font-weight:900;">🧬 Evidence-Based Modern Ayurvedic Research</h3>
        <p style="margin:0; font-size:13.5px; opacity:0.95;">Active Phytochemicals, PubMed/Clinical Trial पुरावे, Pharmacology आणि Safety & Toxicity प्रोफाईल.</p>
    </div>
    """, unsafe_allow_html=True)

    res_topic = st.text_input("🔬 औषधी वनस्पती / घटकाचे नाव टाका:", placeholder="उदा. Withania somnifera (Ashwagandha), Tinospora cordifolia (Guduchi), Suvarna Bhasma", key="res_top")

    if st.button("🧬 वैज्ञानिक संशोधन व क्लिनिकल पुरावे शोधा", key="btn_research", use_container_width=True):
        if not res_topic.strip():
            st.warning("⚠️ कृपया संशोधन द्रव्याचे नाव टाका.")
        else:
            with st.spinner(f"🧬 AI संशोधक '{res_topic}' चे वैज्ञानिक पुरावे व क्लिनिकल ट्रायल्स संकलित करत आहे..."):
                try:
                    res_prompt = f"""
                    You are a Lead Scientist in Ayurvedic Reverse Pharmacology and Clinical Research (AYUSH & Pharmacopoeia).
                    Drug/Herb: {res_topic}

                    Generate a comprehensive Modern Evidence-Based Research Summary:
                    1. 🧪 Active Phytochemical Constituents (Key chemical compounds responsible for therapeutic actions).
                    2. 🔬 Pharmacological Mechanism of Action (How it acts on cellular/biochemical level in modern terms).
                    3. 📊 Clinical Trial Evidence (Key findings from human/animal trials, PubMed/AYUSH research highlights).
                    4. 🛡️ Safety, Toxicity & Heavy Metal Compliance (Safety window, LD50 insights, standard limits).
                    5. 💡 Contemporary Therapeutic Scope (Immunity, oncology, diabetes, adaptogen, or neuroprotection).

                    Format professionally with clear scientific headings and clean points.
                    """
                    res_out = cached_ask_gemini(res_prompt, as_json=False)
                    st.success("✅ वैज्ञानिक संशोधन अहवाल तयार झाला!")
                    st.markdown(res_out)
                except Exception as e:
                    st.error(f"त्रुटी: {e}")

# --- Footer ---
st.markdown(f"""
<div class="app-footer">
    {th['footer_text']} <strong>AyurVeda AI</strong> | Developed by <strong>Avishkar Alase</strong>
</div>
""", unsafe_allow_html=True)
