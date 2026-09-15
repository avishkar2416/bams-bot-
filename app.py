import streamlit as st
from google import genai
from google.genai import types
import json
import time

# --- Page Setup ---
st.set_page_config(
    page_title="AyurVeda AI | Avishkar Alase",
    page_icon="🌺",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- Royal Festive Theme & Mobile Styling ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@500;600;700;800;900&family=Mukta:wght@400;600;700;800;900&display=swap');

    html, body, .stApp {
        background: radial-gradient(circle at 50% 0%, #fffbeb 0%, #fef3c7 25%, #fdfcf7 60%, #fff7ed 100%) !important;
        font-family: 'Mukta', 'Plus Jakarta Sans', sans-serif !important;
        color: #1e1b4b !important;
    }

    @keyframes goldPulse {
        0% { box-shadow: 0 0 0 0 rgba(245, 158, 11, 0.6); }
        70% { box-shadow: 0 0 0 18px rgba(245, 158, 11, 0); }
        100% { box-shadow: 0 0 0 0 rgba(245, 158, 11, 0); }
    }

    /* Floating Inputs */
    div[data-baseweb="select"] > div,
    div[data-baseweb="input"] > div {
        background-color: rgba(255, 255, 255, 0.95) !important;
        border: 2px solid #fed7aa !important;
        border-radius: 16px !important;
        box-shadow: 0 4px 12px rgba(245, 158, 11, 0.04) !important;
        transition: all 0.3s ease !important;
    }
    div[data-baseweb="select"] > div:hover,
    div[data-baseweb="input"] > div:hover {
        border-color: #f59e0b !important;
        box-shadow: 0 6px 20px rgba(245, 158, 11, 0.25) !important;
    }

    /* Golden Navbar */
    .ganesha-navbar {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 14px 22px;
        background: rgba(255, 255, 255, 0.9) !important;
        backdrop-filter: blur(18px);
        border: 2px solid #fde68a !important;
        border-radius: 24px;
        margin-bottom: 22px;
        box-shadow: 0 12px 35px -8px rgba(217, 119, 6, 0.2);
    }
    .brand-title {
        font-size: 21px;
        font-weight: 900;
        background: linear-gradient(135deg, #b45309 0%, #ea580c 50%, #d97706 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 0;
    }
    .vip-badge {
        background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%) !important;
        border: 1.5px solid #f59e0b;
        padding: 8px 18px;
        border-radius: 14px;
        font-size: 13.5px;
        font-weight: 800;
        color: #92400e !important;
    }

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

    /* Animated Action Button */
    div.stButton > button {
        background: linear-gradient(135deg, #ea580c 0%, #d97706 50%, #b45309 100%) !important;
        color: #ffffff !important;
        border: 2px solid #fde68a !important;
        border-radius: 18px !important;
        padding: 16px 32px !important;
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
def render_photo_identical_sheet(data, subject_name, topic_name):
    # JSON Data Extraction
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
    
    # Right Column Data
    sidebar_box_title = data.get("sidebar_box_title", "Pitta = Agni")
    sidebar_box_points = "".join([f"<div>✓ {p}</div>" for p in data.get("sidebar_box_points", [])])
    
    flow_steps = data.get("samprapti_steps", [])
    flow_html = ""
    if flow_steps:
        steps_inner = "".join([f'<div class="hw-box">{s}</div><div class="hw-arrow">↓</div>' for s in flow_steps[:-1]])
        steps_inner += f'<div class="hw-box-final">{flow_steps[-1]}</div>'
        flow_html = f"""
        <div class="sec-title">७. <u>संप्राप्ती (Pathogenesis)</u> :-</div>
        <div style="text-align:center; margin: 6px 0 14px 0;">
            {steps_inner}
        </div>
        """
        
    chikitsa_list = "".join([f"<li>{c}</li>" for c in data.get("chikitsa", [])])
    aushadha_list = "".join([f"<li>{a}</li>" for a in data.get("aushadha", [])])
    punch_line = data.get("punch_line", "")

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
                font-family: 'Mukta', 'Patrick Hand', sans-serif;
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

            /* अस्सल फोटोसारखे A4 पेज */
            .a4-container {{
                width: 820px;
                min-height: 1160px;
                background-color: #fcfbf7; /* अस्सल हस्तलिखित वहीचा रंग */
                border: 2px solid #0f2b5c;
                box-shadow: 0 12px 35px rgba(0,0,0,0.18);
                padding: 24px 28px;
                box-sizing: border-box;
                color: #0b2559; /* अस्सल निळा बॉलपेन */
                position: relative;
                font-size: 15.5px;
                line-height: 1.45;
            }}

            /* निळ्या व लाल पेनाचे हायलाईट */
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

            /* वरचे हेडर */
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
                font-family: 'Patrick Hand', 'Mukta', sans-serif;
                background: #ffffff;
                letter-spacing: 1px;
            }}
            .marks-box {{
                border: 1.8px solid #0f2b5c;
                border-radius: 6px;
                padding: 4px 10px;
                text-align: center;
                font-size: 13.5px;
                background: #ffffff;
            }}

            /* २ कॉलम लेआउट */
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

            /* उजव्या बाजूचा छोटा बॉक्स */
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

            /* फ्लोचार्ट बॉक्सेस */
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

            /* तळटीप (Exam Punch Line) */
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
                    <div class="sec-title">* <span class="u-red">व्याख्या (Definition)</span> :-</div>
                    <div style="margin-bottom:8px;">{definition} <span style="font-size:13.5px; opacity:0.9;">({def_sub})</span></div>

                    <div class="sec-title">१. <span class="u-red">स्थान (Location)</span> :-</div>
                    <ul class="hw-list">
                        <li><b>मुख्य स्थान</b> - {sthana_main}</li>
                        <li><b>उपस्थान</b> - {sthana_sub}</li>
                    </ul>

                    <div class="sec-title">२. <span class="u-red">गुणधर्म (Properties)</span> :-</div>
                    <ul class="hw-list">
                        <li>{gunadharma}</li>
                        <div style="font-size:13.5px; opacity:0.9; margin-top:2px;">({gunadharma_en})</div>
                    </ul>

                    <div class="sec-title">३. <span class="u-red">कार्ये (Functions)</span> :-</div>
                    <ul class="hw-list">{karya_list}</ul>

                    <div class="sec-title">४. <span class="u-red">पित्ताचे प्रकार (Types)</span> :-</div>
                    <ul class="hw-list">{types_list}</ul>

                    <div class="sec-title">५. <span class="u-red">प्रकोपांची कारणे (Nidana)</span> :-</div>
                    <ul class="hw-list">{nidana_list}</ul>

                    <div class="sec-title">६. <span class="u-red">प्रकोपांची लक्षणे (Lakshana)</span> :-</div>
                    <ul class="hw-list">{lakshana_list}</ul>
                </div>

                <!-- Right Column -->
                <div class="right-col">
                    <div class="side-card">
                        <div class="side-card-title">{sidebar_box_title}</div>
                        {sidebar_box_points}
                    </div>

                    {flow_html}

                    <div class="sec-title">८. <span class="u-red">चिकित्सा (Management)</span> :-</div>
                    <ul class="hw-list">{chikitsa_list}</ul>

                    <div class="side-card" style="margin-top:10px;">
                        <div class="side-card-title" style="color:#991b1b;">महत्त्वाची औषधे :-</div>
                        <ul class="hw-list" style="margin-bottom:2px;">{aushadha_list}</ul>
                    </div>
                </div>
            </div>

            <!-- Bottom Punchline -->
            <div class="punch-box">
                ✍️ <span class="u-red">परीक्षेसाठी मुख्य सूत्र (Exam Punch Line)</span> :-<br>
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
    <div style="display:flex; align-items:center; gap:10px;">
        <div style="font-size:26px;">🪔</div>
        <div>
            <div class="brand-title">🌿 AyurVeda AI</div>
            <small style="color:#b45309; font-weight:800;">गणेशोत्सव विशेष पर्व | BAMS HANDWRITTEN STUDIO</small>
        </div>
    </div>
    <div class="vip-badge">
        <span>Avishkar Alase</span> ✓
    </div>
</div>
""", unsafe_allow_html=True)

# --- Hero Section ---
st.markdown("""
<div class="ganesha-hero">
    <div style="font-weight:800; font-size:13px; margin-bottom:4px;">🌺 ॥ श्री गणेशाय नमः ॥ 🌺</div>
    <h3 style="margin:0 0 6px 0; font-weight:900;">🎯 अस्सल हस्तलिखित A4 वही-नोट्स (Photo Replica)</h3>
    <p style="margin:0; font-size:13.5px; opacity:0.95;">परीक्षेसाठी १००% आयकॉनिक रूप: वर '॥ श्री गणेशाय नमः ॥', निळ्या पेनाचे अक्षर, लाल पेन्सिल अंडरलाईन व संप्राप्ती फ्लोचार्ट.</p>
</div>
""", unsafe_allow_html=True)

c1, c2 = st.columns([1, 1.2])
with c1:
    bams_year = st.selectbox(
        "🎓 BAMS वर्ष निवडा:",
        ["BAMS 1st Year", "BAMS 2nd Year", "BAMS 3rd Year", "BAMS Final Year"]
    )
with c2:
    subject = st.selectbox(
        "📚 विषय निवडा:",
        [
            "Kriya Sharir (क्रिया शारीर)",
            "Agada Tantra (अगद तंत्र)",
            "Dravyaguna (द्रव्यगुण)",
            "Rasa Shastra (रसशास्त्र)",
            "Roga Nidan (रोगनिदान)",
            "Kayachikitsa (कायचिकित्सा)"
        ]
    )

topic = st.text_input("🔍 अभ्यासाचा विषय टाका:", value="Pitta Dosha")

if st.button("🚀 अस्सल हस्तलिखित A4 शीट जनरेट करा", use_container_width=True):
    prompt = f"""
    You are an expert Ayurveda University Examiner.
    Generate crisp, structured notes matching this topic: '{topic}' in Subject: '{subject}'.
    
    Format output ONLY as JSON matching this schema:
    {{
        "title": "{topic}",
        "marks": "10 Marks (LAQ)",
        "definition": "जे द्रव्य शरीरामध्ये <span class='hl-red'>पाचन, दहन, रूपांतरण व उष्णता</span> निर्माण करते त्याला 'पित्त दोष' म्हणतात.",
        "definition_sub": "It is the bio-transformative principle in the body",
        "sthana_main": "आमाशय, ग्रहणी, लहान आंत्र (Small intestine)",
        "sthana_sub": "रक्त, यकृत, प्लीहा, स्वेद, नेत्र",
        "gunadharma": "<span class='hl-red'>उष्ण, तीक्ष्ण, लघु, द्रव, सार, अम्ल, कटु</span>",
        "gunadharma_en": "Hot, Sharp, Light, Liquid, Spreading, Sour, Pungent",
        "karya": [
            "अन्न पचन व धातूंचे रूपांतरण",
            "देहाला उष्णता प्रदान करणे",
            "वर्ण, तेज, बुद्धी, दृष्टी प्रदान करणे",
            "मूत्र, पुरीष, स्वेद यांचे साधारण स्वरूप राखणे"
        ],
        "types": [
            {{"name": "पाचक पित्त", "desc": "आमाशय व ग्रहणी स्थित"}},
            {{"name": "रंजक पित्त", "desc": "यकृत व रक्तवह स्रोतस"}},
            {{"name": "साधक पित्त", "desc": "हृदय व मन"}},
            {{"name": "आलोचक पित्त", "desc": "नेत्र"}},
            {{"name": "भ्राजक पित्त", "desc": "त्वचा"}}
        ],
        "nidana": [
            "<span class='hl-red'>अतिउष्ण, अम्ल, लवण, कटु आहार</span>, मद्यपान",
            "क्रोध, अतिताप, उपवास, दिवास्वप्न"
        ],
        "lakshana": [
            "दाह (Burning sensation)",
            "तृष्णा, कृशाय, आम्ल ढेकर",
            "नेत्ररदाह, त्वचेवर लाली (Reddish complexion)",
            "ज्वर, स्वेदवृद्धि"
        ],
        "sidebar_box_title": "Pitta = Agni",
        "sidebar_box_points": ["Transformation", "Metabolism", "Heat", "Intelligence (Buddhi)"],
        "samprapti_steps": [
            "निदान सेवन (उष्ण, आम्ल, लवण, क्रोध इ.)",
            "पित्त दोष प्रकोप",
            "अग्निवृद्धि व दह गुण",
            "रक्त व इतर धातुंची दुष्टी",
            "पित्तज विकारांची निर्मिती"
        ],
        "chikitsa": [
            "शीत, मधुर, तिक्त आहार",
            "<span class='hl-red'>विरेचन</span> हे मुख्य शोधन (Best therapy)",
            "तिक्तघृत, शतधौत घृत, आवळा, गिलोय",
            "तक्र, धान्यांचे शीत पदार्थ"
        ],
        "aushadha": [
            "आवळा (Amalaki)",
            "गुडुची (Guduchi)",
            "शतधौत घृत",
            "सारिवा, उशीर"
        ],
        "punch_line": "पित्त हे दहन, पाचन व रूपांतरण करणारे उष्ण द्रव्य आहे."
    }}
    """
    with st.spinner("✍️ AI अस्सल वहीच्या पानावर फोटोसारख्या नोट्स तयार करत आहे..."):
        try:
            raw_res = cached_ask_gemini(prompt, as_json=True)
            clean_res = raw_res.strip()
            if clean_res.startswith("```json"): clean_res = clean_res[7:]
            if clean_res.startswith("```"): clean_res = clean_res[3:]
            if clean_res.endswith("```"): clean_res = clean_res[:-3]
            data = json.loads(clean_res.strip())

            st.balloons()
            st.success("✅ अस्सल वही-फोटो शीट तयार झाली आहे!")
            html_view = render_photo_identical_sheet(data, subject, topic)
            st.components.v1.html(html_view, height=1300, scrolling=True)
        except Exception as e:
            st.error(f"त्रुटी: {e}")
