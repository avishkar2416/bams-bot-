import streamlit as st
from google import genai
from google.genai import types
import json
import time

# ============================================================
# AYURVEDA AI — PREMIUM FESTIVE EDITION
# ============================================================

st.set_page_config(
    page_title="AyurVeda AI • BAMS Study Studio",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ----------------------------- PREMIUM CSS -----------------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=Mukta:wght@400;500;600;700;800&display=swap');

:root {
    --ink: #172033;
    --muted: #667085;
    --saffron: #d97706;
    --orange: #ea580c;
    --deep: #8f241c;
    --gold: #f59e0b;
    --cream: #fffaf0;
    --paper: rgba(255,255,255,.78);
    --line: rgba(180,83,9,.16);
}

/* App background */
.stApp {
    background:
        radial-gradient(circle at 8% 0%, rgba(251,191,36,.20), transparent 27%),
        radial-gradient(circle at 92% 4%, rgba(234,88,12,.14), transparent 25%),
        linear-gradient(180deg, #fffaf0 0%, #fffdf8 45%, #fff7ed 100%) !important;
    color: var(--ink);
    font-family: 'Mukta', 'Plus Jakarta Sans', sans-serif !important;
}
.stApp::before {
    content: "";
    position: fixed;
    inset: 0;
    pointer-events: none;
    opacity: .20;
    background-image:
        radial-gradient(#b45309 0.65px, transparent 0.65px);
    background-size: 24px 24px;
    mask-image: linear-gradient(to bottom, black, transparent 75%);
    z-index: 0;
}

.block-container {
    max-width: 1400px;
    padding-top: 1.2rem !important;
    padding-bottom: 3rem !important;
}

/* Remove default Streamlit chrome */
#MainMenu, footer {visibility:hidden;}
header[data-testid="stHeader"] {background: transparent !important;}
div[data-testid="stDecoration"] {display:none;}

/* Typography */
h1,h2,h3,h4,p,label,span {
    font-family: 'Mukta', 'Plus Jakarta Sans', sans-serif !important;
    color: var(--ink);
}
h1,h2,h3 {letter-spacing:-.5px;}

/* Top premium navbar */
.premium-nav {
    position: relative;
    overflow: hidden;
    display:flex;
    align-items:center;
    justify-content:space-between;
    gap:20px;
    padding:15px 18px;
    margin-bottom:22px;
    border:1px solid rgba(245,158,11,.28);
    border-radius:24px;
    background:rgba(255,255,255,.72);
    backdrop-filter:blur(22px);
    -webkit-backdrop-filter:blur(22px);
    box-shadow:0 16px 45px rgba(120,53,15,.10);
}
.premium-nav::after {
    content:"";
    position:absolute;
    width:240px;
    height:240px;
    right:-120px;
    top:-150px;
    border-radius:50%;
    background:rgba(251,191,36,.18);
}
.brand {
    display:flex;
    align-items:center;
    gap:13px;
    position:relative;
    z-index:1;
}
.brand-mark {
    width:48px;
    height:48px;
    display:flex;
    align-items:center;
    justify-content:center;
    border-radius:16px;
    background:linear-gradient(145deg,#fff7d6,#fef3c7);
    border:1px solid #f6d365;
    box-shadow:inset 0 1px white,0 8px 20px rgba(180,83,9,.12);
    font-size:26px;
}
.brand-title {
    margin:0;
    font-family:'Plus Jakarta Sans',sans-serif !important;
    font-size:20px;
    font-weight:800;
    background:linear-gradient(90deg,#9a3412,#d97706,#a16207);
    -webkit-background-clip:text;
    -webkit-text-fill-color:transparent;
}
.brand-sub {
    margin-top:2px;
    color:#9a5a13 !important;
    font-size:11px;
    font-weight:700;
    letter-spacing:.55px;
}
.creator-pill {
    position:relative;
    z-index:1;
    padding:9px 14px;
    border:1px solid rgba(245,158,11,.30);
    border-radius:999px;
    background:linear-gradient(180deg,#fffdf5,#fff7df);
    color:#8a4b08 !important;
    font-size:12px;
    font-weight:800;
    box-shadow:0 6px 18px rgba(180,83,9,.08);
}

/* Hero */
.hero {
    position:relative;
    overflow:hidden;
    padding:34px 34px 30px;
    border-radius:30px;
    margin-bottom:22px;
    color:white !important;
    background:
        radial-gradient(circle at 86% 18%,rgba(255,255,255,.18),transparent 18%),
        radial-gradient(circle at 4% 90%,rgba(251,191,36,.20),transparent 28%),
        linear-gradient(135deg,#9a3412 0%,#c2410c 48%,#7f1d1d 100%);
    border:1px solid rgba(254,240,138,.60);
    box-shadow:0 24px 55px rgba(127,29,29,.22);
}
.hero::before {
    content:"ॐ";
    position:absolute;
    right:42px;
    top:0px;
    font-family:serif;
    font-size:170px;
    line-height:1;
    opacity:.075;
    color:#fff;
}
.hero-kicker {
    display:inline-flex;
    padding:6px 12px;
    border:1px solid rgba(255,255,255,.28);
    border-radius:999px;
    background:rgba(255,255,255,.12);
    color:#fff !important;
    font-size:11px;
    font-weight:800;
    letter-spacing:.8px;
}
.hero h1 {
    color:#fff !important;
    margin:12px 0 6px;
    font-family:'Plus Jakarta Sans',sans-serif !important;
    font-size:32px;
    font-weight:800;
}
.hero p {
    color:rgba(255,255,255,.90) !important;
    max-width:850px;
    margin:0;
    font-size:15px;
    line-height:1.65;
}

/* Section headers */
.section-title {
    display:flex;
    align-items:center;
    gap:10px;
    margin:5px 0 12px;
    font-family:'Plus Jakarta Sans',sans-serif !important;
    font-size:15px;
    font-weight:800;
    color:#6b3410 !important;
}
.section-title::before {
    content:"";
    width:4px;
    height:18px;
    border-radius:5px;
    background:linear-gradient(#f59e0b,#ea580c);
}

/* Glass cards around controls */
div[data-testid="stVerticalBlockBorderWrapper"] {
    border:1px solid rgba(180,83,9,.13) !important;
    background:rgba(255,255,255,.62) !important;
    backdrop-filter:blur(14px);
    border-radius:22px !important;
    box-shadow:0 12px 35px rgba(120,53,15,.06);
}

/* Inputs */
div[data-baseweb="select"] > div,
div[data-baseweb="input"] > div,
div[data-baseweb="textarea"] > div {
    background:rgba(255,255,255,.92) !important;
    border:1px solid #ead7bf !important;
    border-radius:15px !important;
    min-height:48px;
    box-shadow:0 4px 15px rgba(120,53,15,.035) !important;
    transition:.2s ease !important;
}
div[data-baseweb="select"] > div:hover,
div[data-baseweb="input"] > div:hover,
div[data-baseweb="textarea"] > div:hover {
    border-color:#e8a11a !important;
    box-shadow:0 8px 24px rgba(217,119,6,.12) !important;
}
input, textarea {
    color:#172033 !important;
    font-weight:600 !important;
}
[data-testid="stWidgetLabel"] p {
    color:#59320e !important;
    font-weight:800 !important;
    font-size:13px !important;
}

/* Radio */
div[role="radiogroup"] label {
    background:rgba(255,255,255,.62);
    border:1px solid rgba(180,83,9,.12);
    border-radius:12px;
    padding:7px 11px;
    margin-right:5px;
    transition:.2s ease;
}
div[role="radiogroup"] label:hover {
    border-color:#f0b43c;
    transform:translateY(-1px);
}

/* Main CTA */
div.stButton > button {
    min-height:54px !important;
    border:none !important;
    border-radius:17px !important;
    color:white !important;
    font-family:'Plus Jakarta Sans',sans-serif !important;
    font-size:14px !important;
    font-weight:800 !important;
    letter-spacing:.1px;
    background:linear-gradient(135deg,#ea580c 0%,#d97706 52%,#b45309 100%) !important;
    box-shadow:0 13px 30px rgba(194,65,12,.26) !important;
    transition:transform .18s ease,box-shadow .18s ease !important;
}
div.stButton > button:hover {
    transform:translateY(-2px);
    box-shadow:0 18px 38px rgba(194,65,12,.34) !important;
}
div.stButton > button:active {transform:scale(.98);}

/* Tabs */
.stTabs [data-baseweb="tab-list"] {
    gap:8px;
    padding:6px;
    border-radius:19px;
    background:rgba(255,255,255,.60);
    border:1px solid rgba(180,83,9,.10);
    box-shadow:0 10px 28px rgba(120,53,15,.05);
}
.stTabs [data-baseweb="tab"] {
    height:48px;
    padding:0 20px !important;
    border-radius:13px !important;
    color:#71400f !important;
    font-weight:800 !important;
    border:none !important;
}
.stTabs [aria-selected="true"] {
    background:linear-gradient(135deg,#fff3cf,#ffe4b2) !important;
    color:#9a3412 !important;
    box-shadow:0 6px 18px rgba(217,119,6,.12);
}
.stTabs [aria-selected="true"] * {color:#9a3412 !important;}

/* Result panels */
.result-head {
    display:flex;
    align-items:center;
    justify-content:space-between;
    gap:12px;
    margin:22px 0 10px;
}
.result-badge {
    display:inline-flex;
    align-items:center;
    padding:6px 10px;
    border-radius:999px;
    background:#ecfdf5;
    border:1px solid #bbf7d0;
    color:#166534 !important;
    font-size:11px;
    font-weight:800;
}
.result-card {
    padding:22px 24px;
    border:1px solid rgba(180,83,9,.12);
    border-radius:22px;
    background:rgba(255,255,255,.72);
    box-shadow:0 14px 40px rgba(120,53,15,.06);
}

/* Medicine hero */
.medicine-hero {
    background:
        radial-gradient(circle at 90% 10%,rgba(255,255,255,.16),transparent 20%),
        linear-gradient(135deg,#075e54,#0f766e 52%,#115e59);
}

/* Footer */
.footer {
    text-align:center;
    margin-top:42px;
    padding:20px 10px 5px;
    color:#8a5a20 !important;
    font-size:12px;
    font-weight:700;
}
.footer-line {
    width:90px;
    height:1px;
    margin:0 auto 12px;
    background:linear-gradient(90deg,transparent,#d97706,transparent);
}

/* Mobile */
@media (max-width: 768px) {
    .block-container {padding-left:1rem !important;padding-right:1rem !important;}
    .premium-nav {padding:12px 13px;border-radius:19px;}
    .brand-mark {width:42px;height:42px;font-size:22px;}
    .brand-title {font-size:16px;}
    .brand-sub {font-size:9px;}
    .creator-pill {font-size:10px;padding:7px 10px;}
    .hero {padding:25px 20px;border-radius:23px;}
    .hero h1 {font-size:24px;}
    .hero p {font-size:13px;}
    .stTabs [data-baseweb="tab"] {padding:0 11px !important;font-size:12px !important;}
}
</style>
""", unsafe_allow_html=True)

# ----------------------------- API -----------------------------
api_key = st.secrets.get("GEMINI_API_KEY", "")
if not api_key:
    st.error("⚠️ कृपया Streamlit Secrets मध्ये GEMINI_API_KEY कॉन्फिगर करा.")
    st.stop()

client = genai.Client(api_key=api_key)

@st.cache_data(show_spinner=False, ttl=86400)
def cached_ask_gemini(prompt: str, as_json: bool = False):
    model_name = "gemini-3.6-flash"
    last_err = None
    for attempt in range(3):
        try:
            config = (
                types.GenerateContentConfig(response_mime_type="application/json")
                if as_json else None
            )
            res = client.models.generate_content(
                model=model_name,
                contents=prompt,
                config=config
            )
            if res and res.text:
                return res.text
        except Exception as e:
            last_err = e
            err_str = str(e)
            time.sleep(16 if ("429" in err_str or "RESOURCE_EXHAUSTED" in err_str) else 2)
    raise RuntimeError(f"तांत्रिक अडचण आली: {last_err}")

# ----------------------------- A4 ENGINE -----------------------------
def create_a4_handwritten_doc(data, subject_name, topic_name, is_marathi=True):
    marks = data.get(
        "exam_marks",
        "१० गुण - दीर्घोत्तरी (LAQ)" if is_marathi else "10 Marks - LAQ"
    )
    title = data.get("main_heading", topic_name)
    has_flowchart = data.get("include_flowchart", True)
    t1 = data.get("entity_1", {})
    t2 = data.get("entity_2", {})

    lbl_flowchart = "संप्राप्ती प्रवाह तक्ता" if is_marathi else "Pathogenesis Flowchart"
    lbl_exam_points = "परीक्षेसाठी महत्त्वाचे मुद्दे:" if is_marathi else "High-Yield Exam Points:"
    lbl_clinical = "लक्षणे, विकार व चिकित्सा:" if is_marathi else "Clinical / Systemic Features:"
    lbl_key = "★ मुख्य संकल्पना:" if is_marathi else "★ Key Exam Concept:"
    lbl_modern = "★ आधुनिक वैद्यकीय सांगड:" if is_marathi else "★ Contemporary / Modern Link:"
    lbl_table = "★ परीक्षा तुलनात्मक तक्ता:" if is_marathi else "★ Quick Exam Comparison Table:"
    lbl_feature = "मुद्दा / लक्षण" if is_marathi else "Feature"
    lbl_punch = "✍️ परीक्षेसाठी मुख्य सूत्र:" if is_marathi else "✍️ Exam Punch Line:"
    lbl_png = "📸 A4 PNG जतन करा" if is_marathi else "📸 Save A4 PNG"
    lbl_pdf = "📄 PDF / Print" if is_marathi else "📄 PDF / Print"
    lbl_def = "व्याख्या:" if is_marathi else "Def:"

    flow_html = ""
    steps = data.get("flowchart_steps", [])
    if has_flowchart and steps:
        flow_parts = []
        for i, step in enumerate(steps):
            cls = "cloud-step" if i == len(steps) - 1 else "box-step"
            flow_parts.append(f'<div class="{cls}">{step}</div>')
            if i < len(steps) - 1:
                flow_parts.append('<div class="arrow">↓</div>')
        flow_html = f"""
        <div class="flow-section">
            <span class="capsule-tag">{lbl_flowchart}</span>
            <div class="flow-wrap">{''.join(flow_parts)}</div>
        </div>
        """

    table_rows = "".join(
        f'<tr><td><b>{r.get("feature","")}</b></td>'
        f'<td>{r.get("point_1","")}</td><td>{r.get("point_2","")}</td></tr>'
        for r in data.get("comparison_table", [])
    )
    table_html = ""
    if table_rows:
        table_html = f"""
        <div class="section-heading">{lbl_table}</div>
        <table class="hw-table">
            <thead><tr>
                <th style="width:25%">{lbl_feature}</th>
                <th>{t1.get("title","Concept 1")}</th>
                <th>{t2.get("title","Concept 2")}</th>
            </tr></thead>
            <tbody>{table_rows}</tbody>
        </table>
        """

    p1_html = "".join(f"<li>{p}</li>" for p in t1.get("key_points", []))
    p2_html = "".join(f"<li>{p}</li>" for p in t2.get("key_points", []))
    font_family = "'Mukta', sans-serif" if is_marathi else "'Patrick Hand','Caveat',cursive,sans-serif"

    return f"""
<!doctype html>
<html lang="{'mr' if is_marathi else 'en'}">
<head>
<meta charset="UTF-8">
<title>{topic_name} — A4 Notes</title>
<script src="https://cdnjs.cloudflare.com/ajax/libs/html2canvas/1.4.1/html2canvas.min.js"></script>
<style>
@import url('https://fonts.googleapis.com/css2?family=Patrick+Hand&family=Caveat:wght@600;700&family=Mukta:wght@500;600;700;800;900&family=Plus+Jakarta+Sans:wght@700;800&display=swap');
*{box-sizing:border-box}
body{margin:0;padding:22px 10px;background:#eef2f7;display:flex;flex-direction:column;align-items:center;font-family:{font_family};}
.action-bar{display:flex;gap:10px;margin-bottom:18px;font-family:'Plus Jakarta Sans',sans-serif}
.btn-action{border:0;border-radius:11px;padding:11px 18px;color:#fff;font-weight:800;cursor:pointer;background:#0369a1;box-shadow:0 7px 18px rgba(3,105,161,.25)}
.btn-action.green{background:#047857}
.a4-paper{width:794px;min-height:1123px;background:#fffdf8;border:1.8px solid #17325f;box-shadow:0 18px 45px rgba(15,23,42,.18);padding:27px 31px;color:#17325f;position:relative;font-size:15px;line-height:1.42}
.a4-paper:before{content:"";position:absolute;inset:0;pointer-events:none;opacity:.20;background:repeating-linear-gradient(0deg,transparent 0,transparent 29px,rgba(23,50,95,.08) 30px)}
.a4-paper>*{position:relative;z-index:1}
.hl-red{background:#ffe1e5;color:#b42318;padding:1px 4px;border:1px solid #fecdd3;border-radius:4px;font-weight:800}
.header-grid{display:flex;justify-content:space-between;align-items:center;border-bottom:2px solid #17325f;padding-bottom:10px;margin-bottom:12px}
.title-box{border:2px solid #17325f;border-radius:10px;padding:8px 14px;width:69%;text-align:center;font-size:21px;font-weight:800;background:#fff}
.title-box span{border-bottom:2px double #17325f}
.marks-tag-box{border:2px solid #17325f;border-radius:8px;padding:5px 11px;text-align:center;font-size:12.5px;font-weight:700;background:#fff}
.flow-section{text-align:center;margin:8px 0 13px}
.capsule-tag,.capsule-badge{display:inline-block;border:1.5px solid #17325f;border-radius:999px;padding:2px 10px;font-weight:800;background:#fff}
.capsule-tag{font-size:12.5px}.capsule-badge{font-size:15.5px;margin-bottom:4px}
.flow-wrap{margin-top:6px}
.box-step{width:82%;margin:auto;border:1.4px solid #17325f;border-radius:8px;padding:4px 9px;background:#fff;font-size:13.5px;font-weight:600}
.cloud-step{width:86%;margin:auto;border:1.7px dashed #17325f;border-radius:14px;padding:5px 10px;background:#fff;font-size:13.5px;font-weight:800}
.arrow{font-weight:900;font-size:13px;margin:1px 0}
.dual-grid{display:flex;gap:13px}.col-half{flex:1;padding:0 5px}.col-half:first-child{border-right:1.3px dashed #17325f}
.col-half p{margin:3px 0 5px;font-size:13.5px}
.section-heading{font-size:14.5px;font-weight:800;text-decoration:underline;margin:7px 0 3px}
.hw-list{margin:3px 0 7px;padding-left:16px;font-size:13.5px}
.hw-list li{margin-bottom:3px}
.key-box{border:1.4px dashed #17325f;border-radius:8px;padding:6px 9px;font-size:12.8px;background:#fbfbf8;line-height:1.38}
.hw-table{width:100%;border-collapse:collapse;font-size:12.8px;margin:4px 0 8px;background:#fff}
.hw-table th,.hw-table td{border:1.3px solid #17325f;padding:4px 7px;text-align:left}
.hw-table th{background:#f8fafc}
.exam-line{border-top:2px solid #17325f;padding-top:7px;margin-top:8px;font-size:13.8px;font-weight:800}
.footer-tag{position:absolute;bottom:8px;right:22px;font:10px sans-serif;opacity:.6}
@media print{.action-bar{display:none}.a4-paper{border:0;box-shadow:none}body{padding:0;background:#fff}}
</style>
</head>
<body>
<div class="action-bar">
<button class="btn-action" onclick="downloadA4Image()">{lbl_png}</button>
<button class="btn-action green" onclick="window.print()">{lbl_pdf}</button>
</div>
<div class="a4-paper" id="a4Canvas">
<div class="header-grid">
<div class="title-box"><span>{title}</span></div>
<div class="marks-tag-box"><b>{subject_name}</b><br><span class="hl-red">🎯 {marks}</span></div>
</div>
{flow_html}
<div class="dual-grid">
<div class="col-half">
<div class="capsule-badge">① {t1.get("title","Concept 1")}</div>
<p><b>{lbl_def}</b> {t1.get("definition","")}</p>
<div class="section-heading">{lbl_exam_points}</div>
<ul class="hw-list">{p1_html}</ul>
<div class="key-box"><b>{lbl_key}</b><br>{t1.get("exam_key","")}</div>
</div>
<div class="col-half">
<div class="capsule-badge">② {t2.get("title","Concept 2")}</div>
<p><b>{lbl_def}</b> {t2.get("definition","")}</p>
<div class="section-heading">{lbl_clinical}</div>
<ul class="hw-list">{p2_html}</ul>
<div class="key-box"><b>{lbl_modern}</b><br>{t2.get("exam_key","")}</div>
</div>
</div>
{table_html}
<div class="exam-line">{lbl_punch} → "{data.get("exam_punch_line","")}"</div>
<div class="footer-tag">🌿 AyurVeda AI • BAMS Study Studio • Avishkar Alase</div>
</div>
<script>
function downloadA4Image(){
 const el=document.getElementById('a4Canvas');
 html2canvas(el,{scale:2.2,useCORS:true,backgroundColor:'#fffdf8'}).then(canvas=>{
   const a=document.createElement('a');
   a.download='{topic_name.replace(" ","_")}_A4_Notes.png';
   a.href=canvas.toDataURL('image/png'); a.click();
 });
}
</script>
</body>
</html>
"""

# ----------------------------- NAVBAR -----------------------------
st.markdown("""
<div class="premium-nav">
  <div class="brand">
    <div class="brand-mark">🪔</div>
    <div>
      <div class="brand-title">🌿 AyurVeda AI</div>
      <div class="brand-sub">BAMS STUDY STUDIO • FESTIVE PREMIUM EDITION</div>
    </div>
  </div>
  <div class="creator-pill">✦ Created by Avishkar Alase</div>
</div>
""", unsafe_allow_html=True)

# ----------------------------- TABS -----------------------------
tab1, tab2 = st.tabs([
    "📖  BAMS Study Studio",
    "🧪  Medicine & Manufacturing"
])

# ============================================================
# TAB 1
# ============================================================
with tab1:
    st.markdown("""
    <div class="hero">
      <span class="hero-kicker">🌺 ॥ श्री गणेशाय नमः ॥ • SMART BAMS ASSISTANT</span>
      <h1>🎯 A4 Handwritten Notes, redesigned.</h1>
      <p>
        University-focused Ayurveda notes with clean hierarchy, exam-weightage,
        flowcharts, comparison tables, red-highlighted keywords and a polished
        handwritten A4 output.
      </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="section-title">🎓 Academic Setup</div>', unsafe_allow_html=True)

    r1c1, r1c2 = st.columns([1, 1.2])
    with r1c1:
        bams_year = st.selectbox(
            "BAMS वर्ष / Academic Year",
            [
                "BAMS 1st Professional (प्रथम वर्ष)",
                "BAMS 2nd Professional (द्वितीय वर्ष)",
                "BAMS 3rd Professional (तृतीय वर्ष)",
                "BAMS Final Professional (अंतिम वर्ष)"
            ]
        )
    with r1c2:
        subject = st.selectbox(
            "📚 विषय / Subject",
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

    r2c1, r2c2 = st.columns([1.2, 1])
    with r2c1:
        study_mode = st.selectbox(
            "🎯 Study Mode",
            [
                "📋 A4 Blue Ballpen Handwritten Sheet (अस्सल A4 पेन नोट्स)",
                "📖 Comprehensive Notes (संपूर्ण सविस्तर अभ्यास नोट्स)",
                "📜 Only Shlokas & Meanings (फक्त मूळ श्लोक, अन्वय व अर्थ)",
                "📝 10-Mark LAQ Answer Format (दीर्घोत्तरी प्रश्न-उत्तर फॉरमॅट)",
                "⚡ Quick Revision / Viva Voce Points (तोंडी परीक्षेसाठी महत्त्वाचे मुद्दे)"
            ]
        )
    with r2c2:
        language_preference = st.radio(
            "🌐 माध्यम / Language",
            [
                "मराठी (संस्कृत श्लोक + सोपा अर्थ + मॉडर्न टर्म्स)",
                "Simple Indian English + Sanskrit"
            ],
            horizontal=True
        )

    topic = st.text_input(
        "🔍 Topic / Question",
        placeholder="उदा. Pitta Dosha • Garavisha vs Dooshivisha • Ashwagandha • Pandu Roga"
    )

    generate_notes_btn = st.button(
        "🚀  Generate Premium Study Notes",
        key="btn_notes",
        use_container_width=True
    )

    if generate_notes_btn:
        if not topic.strip():
            st.warning("⚠️ कृपया अभ्यासाचा विषय प्रविष्ट करा.")
        else:
            is_marathi = "मराठी" in language_preference

            if "A4 Blue Ballpen" in study_mode:
                lang_rule = (
                    """
                    LANGUAGE: Simple natural Marathi. Use authentic Sanskrit concepts/shlokas
                    with simple Marathi explanation and English medical terms in parentheses.
                    """
                    if is_marathi else
                    """
                    LANGUAGE: 100% English + Roman Sanskrit transliteration.
                    DO NOT output Marathi/Devanagari anywhere in JSON.
                    """
                )

                json_prompt = f"""
You are a senior Ayurveda Professor and BAMS University Paper Setter.
Academic Level: {bams_year}
Subject: {subject}
Topic: {topic}
{lang_rule}

Create crisp, highly readable one-page A4 handwritten exam notes.
Determine whether the topic is normally a 10-Mark LAQ or 5-Mark SAQ.
Only include a flowchart if it genuinely helps explain pathogenesis/stages.

Wrap crucial medical keywords, cardinal symptoms, important drugs and mechanisms
inside <span class="hl-red">...</span>.

Return ONLY valid JSON matching:
{{
 "exam_marks":"...",
 "main_heading":"...",
 "include_flowchart":true,
 "flowchart_steps":["..."],
 "entity_1":{{
   "title":"...",
   "definition":"...",
   "key_points":["...","...","..."],
   "exam_key":"..."
 }},
 "entity_2":{{
   "title":"...",
   "definition":"...",
   "key_points":["...","...","..."],
   "exam_key":"..."
 }},
 "comparison_table":[
   {{"feature":"...","point_1":"...","point_2":"..."}},
   {{"feature":"...","point_1":"...","point_2":"..."}},
   {{"feature":"...","point_1":"...","point_2":"..."}}
 ],
 "exam_punch_line":"..."
}}
"""
                with st.spinner("✍️ Premium A4 sheet तयार करत आहे..."):
                    try:
                        raw_json = cached_ask_gemini(json_prompt, as_json=True)
                        clean = raw_json.strip()
                        if clean.startswith("```json"):
                            clean = clean[7:]
                        if clean.startswith("```"):
                            clean = clean[3:]
                        if clean.endswith("```"):
                            clean = clean[:-3]

                        sheet_data = json.loads(clean.strip())
                        st.success(
                            f"✅ A4 Sheet तयार झाली • {sheet_data.get('exam_marks','Exam-ready')}"
                        )
                        st.components.v1.html(
                            create_a4_handwritten_doc(
                                sheet_data, subject, topic, is_marathi=is_marathi
                            ),
                            height=1260,
                            scrolling=True
                        )
                    except Exception as e:
                        st.error(f"त्रुटी: {e}")

            else:
                system_instruction = f"""
You are a senior Ayurveda Acharya according to NCISM standards.
Academic Level: {bams_year}
Subject: {subject}
Study Mode: {study_mode}
Topic: {topic}
Language: {language_preference}

Generate high-yield study material strictly aligned with the selected study mode.
If English is selected, write in English with Roman Sanskrit transliteration.
Use clear headings, concise bullets, bold key terms and exam-oriented structure.
For Sanskrit shlokas, use blockquotes.
"""
                with st.spinner("⚡ AI exam-ready notes तयार करत आहे..."):
                    try:
                        notes_text = cached_ask_gemini(system_instruction, as_json=False)
                        st.success("✅ Premium notes तयार झाल्या आहेत!")
                        st.markdown('<div class="result-card">', unsafe_allow_html=True)
                        st.markdown(notes_text)
                        st.markdown('</div>', unsafe_allow_html=True)
                    except Exception as e:
                        st.error(f"त्रुटी: {e}")

# ============================================================
# TAB 2
# ============================================================
with tab2:
    st.markdown("""
    <div class="hero medicine-hero">
      <span class="hero-kicker">🌿 RASAUSHADHI VIDHI • FORMULATION LAB</span>
      <h1>🧪 Medicine & Manufacturing Studio</h1>
      <p>
        Ayurvedic formulation ingredients, shodhana/purification concepts,
        preparation sequence and exam-focused explanation — presented in a
        clean step-by-step format.
      </p>
    </div>
    """, unsafe_allow_html=True)

    m1, m2 = st.columns([1.2, 1])
    with m1:
        dosage_form = st.selectbox(
            "🏺 औषधाचा प्रकार / Dosage Form",
            [
                "Vati / Gutika (गोळी / वटी)",
                "Churna (चूर्ण)",
                "Asava & Arishta (आसव व अरिष्ट)",
                "Taila / Ghrita (सिद्ध तेल व घृत)",
                "Bhasma & Pishti (भस्म व पिष्टी)"
            ]
        )
    with m2:
        m_lang = st.radio(
            "🌐 भाषा / Language",
            ["Simple Indian English", "मराठी"],
            horizontal=True,
            key="m_lang"
        )

    medicine_name = st.text_input(
        "💊 औषधाचे नाव / Medicine Name",
        placeholder="उदा. Arogyavardhini Vati • Chandraprabha Vati • Triphala Churna"
    )

    if st.button(
        "🔬  Generate Formulation & Manufacturing Guide",
        key="btn_med",
        use_container_width=True
    ):
        if not medicine_name.strip():
            st.warning("⚠️ कृपया औषधाचे नाव टाका.")
        else:
            med_prompt = f"""
Explain the Ayurvedic formulation {medicine_name} ({dosage_form})
in simple spoken {m_lang}.

Include:
1. Introduction and therapeutic purpose
2. Ingredients table with classical names
3. Shodhana / purification if applicable
4. Exact conceptual manufacturing sequence for BAMS study
5. Important precautions and quality-control points
6. Dose/anupana only as educational classical context, not personalized prescribing
7. High-yield exam points

Clearly distinguish classical textual method from modern safety/regulatory practice.
"""
            with st.spinner(f"🔬 {medicine_name} चे premium notes तयार करत आहे..."):
                try:
                    res_text = cached_ask_gemini(med_prompt, as_json=False)
                    st.success("✅ Formulation guide तयार झाला!")
                    st.markdown('<div class="result-card">', unsafe_allow_html=True)
                    st.markdown(res_text)
                    st.markdown('</div>', unsafe_allow_html=True)
                except Exception as e:
                    st.error(f"त्रुटी: {e}")

# ----------------------------- FOOTER -----------------------------
st.markdown("""
<div class="footer">
  <div class="footer-line"></div>
  🌺 ॥ गणपती बाप्पा मोरया ॥ 🌿<br>
  <strong>AyurVeda AI</strong> • BAMS Study Studio • Crafted by <strong>Avishkar Alase</strong>
</div>
""", unsafe_allow_html=True)
