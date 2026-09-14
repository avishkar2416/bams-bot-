import streamlit as st
from google import genai
from google.genai import types
from PIL import Image, ImageDraw, ImageFont
import io
import json
import time
import markdown

# --- Page Setup ---
st.set_page_config(
    page_title="AyurVeda AI | Avishkar Alase",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- Universal Mobile UI CSS ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@500;600;700;800&family=Noto+Sans+Devanagari:wght@400;600;700;800&display=swap');

    html, body, .stApp {
        background-color: #f8faf9 !important;
        font-family: 'Noto Sans Devanagari', 'Plus Jakarta Sans', sans-serif !important;
        color: #0f172a !important;
    }

    label, p, span, div, h1, h2, h3, h4, h5, h6 {
        color: #0f172a !important;
    }

    div[data-baseweb="select"] > div,
    div[data-baseweb="input"] > div,
    ul[role="listbox"],
    li[role="option"] {
        background-color: #ffffff !important;
        color: #0f172a !important;
    }

    ul[role="listbox"] li {
        background-color: #ffffff !important;
        color: #0f172a !important;
        font-size: 14px !important;
        font-weight: 600 !important;
    }

    ul[role="listbox"] li:hover,
    ul[role="listbox"] li[aria-selected="true"] {
        background-color: #ecfdf5 !important;
        color: #047857 !important;
    }

    div[data-baseweb="select"] span {
        color: #0f172a !important;
        font-weight: 600 !important;
    }

    div[data-baseweb="input"] input {
        color: #0f172a !important;
        background-color: #ffffff !important;
    }

    .premium-navbar {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 12px 18px;
        background: #ffffff !important;
        border: 1px solid #e2e8f0;
        border-radius: 16px;
        margin-bottom: 20px;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.03);
    }
    .nav-brand {
        display: flex;
        align-items: center;
        gap: 10px;
    }
    .nav-logo {
        background: linear-gradient(135deg, #059669 0%, #10b981 100%);
        color: white !important;
        width: 38px;
        height: 38px;
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
        font-size: 9px;
        font-weight: 800;
        color: #059669 !important;
        text-transform: uppercase;
    }

    .vip-creator-card {
        display: flex;
        align-items: center;
        gap: 8px;
        background: #ecfdf5 !important;
        border: 1.5px solid #a7f3d0;
        padding: 6px 14px;
        border-radius: 12px;
    }
    .vip-avatar {
        width: 28px;
        height: 28px;
        border-radius: 8px;
        background: #059669;
        color: white !important;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 13px;
        font-weight: 800;
    }
    .vip-name {
        font-size: 13px;
        font-weight: 800;
        color: #064e3b !important;
        display: flex;
        align-items: center;
        gap: 5px;
    }
    .verified-tick {
        background: #10b981;
        color: white !important;
        font-size: 9px;
        width: 14px;
        height: 14px;
        border-radius: 50%;
        display: inline-flex;
        align-items: center;
        justify-content: center;
    }

    .hero-banner {
        background: linear-gradient(135deg, #064e3b 0%, #047857 100%) !important;
        padding: 26px 22px;
        border-radius: 18px;
        margin-bottom: 22px;
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
        font-size: 25px;
        font-weight: 800;
        margin: 0 0 6px 0;
    }
    .hero-desc {
        font-size: 13.5px;
        line-height: 1.6;
        opacity: 0.95;
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
        transition: all 0.35s ease !important;
        cursor: pointer !important;
    }

    .notes-box {
        background: #ffffff !important;
        border: 1px solid #e2e8f0;
        border-radius: 20px;
        padding: 30px 24px;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.04);
        margin-top: 25px;
        line-height: 1.85;
    }
    .notes-box h1 { color: #064e3b !important; font-size: 24px; font-weight: 800; border-bottom: 2px solid #ecfdf5; padding-bottom: 8px; }
    .notes-box h2 { color: #047857 !important; font-size: 19px; font-weight: 700; margin-top: 24px; }
    .notes-box blockquote { background: #f0fdf4 !important; border-left: 4px solid #10b981; padding: 14px 20px; border-radius: 0 12px 12px 0; margin: 18px 0; }
    .notes-box blockquote * { color: #065f46 !important; font-weight: 600; }

    .app-footer {
        text-align: center;
        padding: 35px 10px 15px 10px;
        font-size: 13px;
        color: #64748b !important;
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)

# --- API Key Setup ---
api_key = st.secrets.get("GEMINI_API_KEY", "")
if not api_key:
    st.error("⚠️ कृपया Settings > Secrets मध्ये GEMINI_API_KEY कॉन्फिगर करा.")
    st.stop()

client = genai.Client(api_key=api_key)

# Safe AI Call using stable models
def ask_gemini(prompt, as_json=False):
    models = ['gemini-2.5-flash', 'models/gemini-3.6-flash', 'models/gemini-2.5-pro']
    for m in models:
        try:
            config = types.GenerateContentConfig(response_mime_type="application/json") if as_json else None
            res = client.models.generate_content(model=m, contents=prompt, config=config)
            if res and res.text:
                return res.text
        except Exception:
            time.sleep(1)
            continue
    raise RuntimeError("गुगल सर्व्हर व्यस्त आहे. कृपया काही सेकंदांनंतर पुन्हा प्रयत्न करा.")

# =========================================================================
# REAL PIL ENGINE: अस्सल कागदावर पेनने रेखाटलेली HD Image तयार करणारी यंत्रणा
# =========================================================================
def wrap_text(text, max_chars=38):
    words = text.split()
    lines = []
    current_line = []
    current_len = 0
    for w in words:
        if current_len + len(w) + 1 <= max_chars:
            current_line.append(w)
            current_len += len(w) + 1
        else:
            lines.append(" ".join(current_line))
            current_line = [w]
            current_len = len(w)
    if current_line:
        lines.append(" ".join(current_line))
    return lines

def generate_authentic_handwritten_image(data, subject_name, topic_name):
    # A4 Pro Canvas Size
    width = 1100
    height = 2100
    
    # शुद्ध कागदाचा नैसर्गिक ऑफ-व्हाइट रंग
    img = Image.new("RGB", (width, height), color=(253, 252, 248))
    draw = ImageDraw.Draw(img)

    # बॉलपेनची शाई (Handwritten Dark Navy Ink)
    pen_color = (18, 30, 49)
    soft_pen = (35, 55, 80)
    
    font = ImageFont.load_default()

    # १. बाहेरील हॅन्ड-ड्रॉन मार्जिन बॉर्डर
    draw.rectangle([(25, 25), (width - 25, height - 25)], outline=pen_color, width=3)
    draw.rectangle([(28, 28), (width - 28, height - 28)], outline=soft_pen, width=1)

    # २. मुख्य हेडिंग आणि विषय बॉक्स
    title_text = data.get("main_heading", topic_name).upper()
    draw.rounded_rectangle([(45, 45), (800, 125)], radius=12, outline=pen_color, width=3)
    draw.text((65, 75), title_text[:68], fill=pen_color, font=font)

    draw.rounded_rectangle([(815, 45), (width - 45, 125)], radius=12, outline=pen_color, width=3)
    draw.text((830, 68), f"{subject_name[:18]}", fill=pen_color, font=font)
    draw.text((850, 92), "(BAMS / MD)", fill=pen_color, font=font)

    # ३. दोन स्तंभांची (Dual Columns) विभागणी रेषा
    mid_x = width // 2
    draw.line([(mid_x, 140), (mid_x, 1380)], fill=pen_color, width=3)

    t1 = data.get("entity_1", {})
    t2 = data.get("entity_2", {})

    # Helper function to render a single column
    def render_column(entity_data, start_x, num_badge):
        y = 150
        # Entity Header Capsule
        name = entity_data.get("title", f"Entity {num_badge}")
        draw.rounded_rectangle([(start_x, y), (start_x + 460, y + 42)], radius=18, outline=pen_color, width=3)
        draw.text((start_x + 20, y + 14), f"{num_badge}  {name[:40]}", fill=pen_color, font=font)
        y += 55

        # Definition Line
        lines = wrap_text(f"-> {entity_data.get('definition', '')}", max_chars=46)
        for line in lines[:3]:
            draw.text((start_x + 8, y), line, fill=soft_pen, font=font)
            y += 22
        y += 12

        # Pathogenesis Capsule
        draw.rounded_rectangle([(start_x + 30, y), (start_x + 430, y + 32)], radius=14, outline=pen_color, width=2)
        draw.text((start_x + 45, y + 8), "Pathogenesis / Role in disease manifestation", fill=pen_color, font=font)
        y += 44

        # Flowchart Step Boxes
        steps = entity_data.get("flowchart", [])
        for i, step in enumerate(steps[:5]):
            draw.rounded_rectangle([(start_x + 35, y), (start_x + 425, y + 44)], radius=8, outline=pen_color, width=2)
            step_lines = wrap_text(step, max_chars=36)
            for j, sl in enumerate(step_lines[:2]):
                draw.text((start_x + 50, y + 8 + (j * 16)), sl, fill=pen_color, font=font)
            y += 48
            # Hand-drawn Arrow
            draw.text((start_x + 225, y), "|", fill=pen_color, font=font)
            draw.text((start_x + 223, y + 10), "v", fill=pen_color, font=font)
            y += 24

        # Final Vyadhi Manifestation (Cloud Box)
        draw.rounded_rectangle([(start_x + 20, y), (start_x + 440, y + 50)], radius=24, outline=pen_color, width=3)
        draw.text((start_x + 45, y + 16), f"Final: {steps[-1] if steps else 'Manifestation'}"[:44], fill=pen_color, font=font)
        y += 66

        # Diseases / Manifestations Title
        draw.text((start_x + 10, y), "Diseases / Manifestations:", fill=pen_color, font=font)
        draw.line([(start_x + 10, y + 16), (start_x + 220, y + 16)], fill=pen_color, width=2)
        y += 24

        for item in entity_data.get("manifestations", [])[:5]:
            draw.text((start_x + 15, y), f"* {item[:42]}", fill=soft_pen, font=font)
            y += 20
        y += 10

        # Key Concept Box
        draw.rounded_rectangle([(start_x + 10, y), (start_x + 450, y + 75)], radius=12, outline=pen_color, width=2)
        draw.text((start_x + 20, y + 8), "Key Concept:", fill=pen_color, font=font)
        kc_lines = wrap_text(entity_data.get("key_concept", ""), max_chars=40)
        for k_idx, kcl in enumerate(kc_lines[:2]):
            draw.text((start_x + 20, y + 28 + (k_idx * 18)), kcl, fill=soft_pen, font=font)

    # Render Left (①) and Right (②)
    render_column(t1, start_x=45, num_badge="(1)")
    render_column(t2, start_x=mid_x + 25, num_badge="(2)")

    # ४. तळभागातील तुलनात्मक तक्ता (Handwritten Table)
    table_top = 1400
    draw.line([(45, table_top - 15), (width - 45, table_top - 15)], fill=pen_color, width=2)
    draw.text((50, table_top - 5), "* Difference in Disease Manifestation:", fill=pen_color, font=font)

    # Table Grid
    row_y = table_top + 25
    col_w1 = 260
    col_w2 = 360
    col_w3 = 360

    headers = ["Feature", t1.get("title", "Entity 1")[:24], t2.get("title", "Entity 2")[:24]]
    draw.rectangle([(45, row_y), (width - 45, row_y + 40)], outline=pen_color, width=2)
    draw.text((55, row_y + 12), headers[0], fill=pen_color, font=font)
    draw.text((50 + col_w1, row_y + 12), headers[1], fill=pen_color, font=font)
    draw.text((50 + col_w1 + col_w2, row_y + 12), headers[2], fill=pen_color, font=font)
    row_y += 40

    comp_rows = data.get("comparison_table", [])
    for row in comp_rows[:5]:
        draw.rectangle([(45, row_y), (width - 45, row_y + 42)], outline=pen_color, width=1)
        draw.text((55, row_y + 12), row.get("feature", "")[:28], fill=pen_color, font=font)
        draw.text((50 + col_w1, row_y + 12), row.get("entity_1", "")[:36], fill=soft_pen, font=font)
        draw.text((50 + col_w1 + col_w2, row_y + 12), row.get("entity_2", "")[:36], fill=soft_pen, font=font)
        row_y += 42

    # ५. In Short Bubbles
    row_y += 20
    draw.rounded_rectangle([(100, row_y), (480, row_y + 65)], radius=30, outline=pen_color, width=2)
    draw.text((125, row_y + 14), f"{t1.get('title','Entity 1')[:28]}", fill=pen_color, font=font)
    draw.text((125, row_y + 36), f"-> {t1.get('short_summary','')[:36]}", fill=soft_pen, font=font)

    draw.text((mid_x - 15, row_y + 24), "vs", fill=pen_color, font=font)

    draw.rounded_rectangle([(mid_x + 40, row_y), (width - 100, row_y + 65)], radius=30, outline=pen_color, width=2)
    draw.text((mid_x + 65, row_y + 14), f"{t2.get('title','Entity 2')[:28]}", fill=pen_color, font=font)
    draw.text((mid_x + 65, row_y + 36), f"-> {t2.get('short_summary','')[:36]}", fill=soft_pen, font=font)

    # ६. Exam Line Box & Watermark
    row_y += 85
    draw.line([(45, row_y), (width - 45, row_y)], fill=pen_color, width=2)
    row_y += 15
    draw.text((50, row_y), "Exam Line: -> ", fill=pen_color, font=font)
    ex_lines = wrap_text(f'"{data.get("exam_punch_line", "")}"', max_chars=88)
    for el in ex_lines[:2]:
        row_y += 18
        draw.text((70, row_y), el, fill=soft_pen, font=font)

    # Bottom Branding
    draw.text((width - 420, height - 48), "🌿 AyurVeda AI Handwritten Sheet | Avishkar Alase", fill=soft_pen, font=font)

    buf = io.BytesIO()
    img.save(buf, format="PNG", quality=95)
    return buf.getvalue()

# --- Top Navigation Bar ---
st.markdown("""
<div class="premium-navbar">
    <div class="nav-brand">
        <div class="nav-logo">🌿</div>
        <div>
            <div class="brand-title">AyurVeda AI</div>
            <div class="brand-tag">NCISM Curriculum & Handwritten Engine</div>
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
        <div class="hero-desc">अस्सल संहिता संदर्भ, टॉपर स्टाईल फ्लोचार्ट्स, संप्राप्ती चक्र, तुलनात्मक तक्ते आणि थेट गॅलरीत सेव्ह होणाऱ्या Handwritten नोट्स.</div>
    </div>
    """, unsafe_allow_html=True)

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
                "📋 Topper Hand-written Notes (फोटोसारखे पेन-ड्राऊन नोट्स)",
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
            ["Simple Indian English + Sanskrit (सोपे व थेट समजणारे इंग्रजी)", "मराठी (संस्कृत श्लोक + सोपा अर्थ + मॉडर्न टर्म्स)"],
            horizontal=True,
            key="lang_notes"
        )

    topic = st.text_input(
        "🔍 अभ्यासाचा विषय / प्रश्न टाका:",
        value="Role of Garavisha and Dooshivisha in Manifestation of Diseases"
    )

    generate_notes_btn = st.button("🚀 सविस्तर अभ्यास नोट्स तयार करा", key="btn_notes", use_container_width=True)

    if generate_notes_btn:
        if not topic.strip():
            st.warning("⚠️ कृपया अभ्यासाचा विषय प्रविष्ट करा.")
        else:
            if "Topper Hand-written" in study_mode:
                json_prompt = f"""
                You are a university topper and professor in Ayurveda (BAMS/MD).
                Subject: {subject}
                Topic: {topic}

                Structure this topic EXACTLY into the 2-column comparison handwritten paper layout.
                Return ONLY valid JSON matching this schema:
                {{
                    "main_heading": "Title of the note",
                    "entity_1": {{
                        "title": "Name of Entity 1",
                        "definition": "1-2 lines simple English definition",
                        "flowchart": [
                            "Step 1: Intake / Nidana",
                            "Step 2: Agni Dushti",
                            "Step 3: Ama + Dosha Vitiation",
                            "Step 4: Srotodushti",
                            "Step 5: Doshadushya Sammurchana",
                            "Final: Disease Manifestation"
                        ],
                        "manifestations": ["Symptom 1", "Symptom 2", "Symptom 3", "Symptom 4"],
                        "key_concept": "Core exam mechanism sentence",
                        "short_summary": "1 line short summary"
                    }},
                    "entity_2": {{
                        "title": "Name of Entity 2",
                        "definition": "1-2 lines simple English definition",
                        "flowchart": [
                            "Step 1: Latent cause / Residual",
                            "Step 2: Long term accumulation",
                            "Step 3: Chronic Dhatu involvement",
                            "Step 4: Srotas disturbance",
                            "Final: Chronic disease manifestation"
                        ],
                        "manifestations": ["Symptom 1", "Symptom 2", "Symptom 3", "Symptom 4"],
                        "key_concept": "Core exam mechanism sentence",
                        "short_summary": "1 line short summary"
                    }},
                    "comparison_table": [
                        {{"feature": "Nature", "entity_1": "...", "entity_2": "..."}},
                        {{"feature": "Onset", "entity_1": "...", "entity_2": "..."}},
                        {{"feature": "Main Mechanism", "entity_1": "...", "entity_2": "..."}},
                        {{"feature": "Type of Manifestation", "entity_1": "...", "entity_2": "..."}},
                        {{"feature": "Examples", "entity_1": "...", "entity_2": "..."}}
                    ],
                    "exam_punch_line": "Exact high-scoring summary sentence."
                }}
                """

                with st.spinner("✍️ अस्सल कागदावर बॉलपेनने काढलेली Handwritten Sheet तयार होत आहे..."):
                    try:
                        raw_json = ask_gemini(json_prompt, as_json=True)
                        clean_json = raw_json.strip()
                        if clean_json.startswith("```json"): clean_json = clean_json[7:]
                        if clean_json.startswith("```"): clean_json = clean_json[3:]
                        if clean_json.endswith("```"): clean_json = clean_json[:-3]

                        sheet_data = json.loads(clean_json.strip())
                        img_bytes = generate_authentic_handwritten_image(sheet_data, subject, topic)

                        st.balloons()
                        st.success("✅ हुबेहूब Handwritten Image तयार झाली आहे! थेट डाऊनलोड करा.")

                        # थेट डाऊनलोड बटण (१-क्लिकमध्ये मोबाईल गॅलरीत सेव्ह)
                        st.download_button(
                            label="📥 थेट Handwritten इमेज डाऊनलोड करा (.PNG)",
                            data=img_bytes,
                            file_name=f"{topic.replace(' ', '_')}_Handwritten_Notes.png",
                            mime="image/png",
                            use_container_width=True
                        )

                        # इमेजचे थेट प्रिव्ह्यू
                        st.image(img_bytes, caption="📸 Handwritten Sheet Preview", use_container_width=True)

                    except Exception as e:
                        st.error(f"त्रुटी: {e}")

            else:
                # Regular Syllabus Notes
                system_instruction = f"""
                You are a senior Ayurveda Acharya according to NCISM standards.
                Academic Level: {bams_year}, Subject: {subject}, Study Mode: {study_mode}, Topic: {topic}, Language: {language_preference}.
                Generate tailored, high-yield study material strictly aligned with '{study_mode}'.
                - Format Sanskrit Shlokas inside blockquotes (> "Shloka").
                - Bold all key terms.
                """
                with st.spinner(f"⚡ AI आयुर्वेद तज्ज्ञ '{study_mode}' नुसार नोट्स तयार करत आहे..."):
                    try:
                        notes_text = ask_gemini(system_instruction)
                        st.balloons()
                        st.success("✅ नोट्स तयार झाल्या आहेत!")
                        st.markdown('<div class="notes-box">', unsafe_allow_html=True)
                        st.markdown(notes_text)
                        st.markdown('</div>', unsafe_allow_html=True)
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
        <div class="hero-desc">कोणतीही आयुर्वेदिक गोळी, वटी, चूर्ण, आसव-अरिष्ट, भस्म किंवा घृत कशापासून बनवले आहे आणि कसे तयार करायचे ते सोप्या भाषेत शिका.</div>
    </div>
    """, unsafe_allow_html=True)

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
            ["Simple Indian English + Sanskrit", "मराठी (सविस्तर मराठी कृती + प्रमाण)"],
            horizontal=True,
            key="lang_med"
        )

    medicine_name = st.text_input(
        "💊 गोळी किंवा औषधाचे नाव टाका:",
        placeholder="उदा. आरोग्यवर्धिनी वटी, चंद्रप्रभावटी, सितोपलादी चूर्ण, किंवा त्रिभुवन कीर्ति रस"
    )

    generate_med_btn = st.button("🔬 औषध घटक व बनवण्याची पूर्ण कृती शिका", key="btn_med", use_container_width=True)

    if generate_med_btn:
        if not medicine_name.strip():
            st.warning("⚠️ कृपया औषधाचे नाव टाका.")
        else:
            med_prompt = f"""
            You are a master Rasashastra and Bhaishajya Kalpana Acharya.
            Medicine: {medicine_name}
            Dosage Form: {dosage_form}
            Language: {m_lang}

            Explain the manufacturing process in simple Indian English (or Marathi):
            - Easy-to-understand sentences.
            - Clear ingredients table with exact parts/ratios.
            - Simple Shodhana (purification) steps.
            - Practical preparation steps (Mardan, Agni, Paka).
            - Purity tests and clinical dose/anupana.
            """

            with st.spinner(f"🔬 AI तज्ज्ञ '{medicine_name}' ची निर्माण पद्धत तयार करत आहे..."):
                try:
                    med_text = ask_gemini(med_prompt)
                    st.balloons()
                    st.success(f"✅ {medicine_name} ची संपूर्ण निर्माण विधी तयार झाली आहे!")
                    st.markdown('<div class="notes-box">', unsafe_allow_html=True)
                    st.markdown(med_text)
                    st.markdown('</div>', unsafe_allow_html=True)
                except Exception as e:
                    st.error(f"त्रुटी: {e}")

# --- Footer ---
st.markdown("""
<div class="app-footer">
    🌿 <strong>AyurVeda AI & Handwritten Studio</strong> | Developed by <strong>Avishkar Alase</strong>
</div>
""", unsafe_allow_html=True)
