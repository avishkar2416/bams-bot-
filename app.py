import streamlit as st
from google import genai
from google.genai import types
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

# --- Base Theme & Mobile Clean UI ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@500;600;700;800&family=Mukta:wght@400;600;700;800;900&display=swap');

    html, body, .stApp {
        background-color: #f4f6f8 !important;
        font-family: 'Mukta', 'Plus Jakarta Sans', sans-serif !important;
        color: #0f172a !important;
    }

    label, p, span, div, h1, h2, h3 {
        color: #0f172a !important;
    }

    div[data-baseweb="select"] > div,
    div[data-baseweb="input"] > div {
        background-color: #ffffff !important;
        border: 1.5px solid #cbd5e1 !important;
        border-radius: 12px !important;
    }

    /* Top Navbar */
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
    .brand-title {
        font-size: 18px;
        font-weight: 800;
        color: #064e3b !important;
        margin: 0;
    }

    .vip-badge {
        background: #ecfdf5 !important;
        border: 1.5px solid #a7f3d0;
        padding: 6px 14px;
        border-radius: 12px;
        font-size: 13px;
        font-weight: 800;
        color: #064e3b !important;
    }

    .hero-banner {
        background: linear-gradient(135deg, #064e3b 0%, #047857 100%) !important;
        padding: 24px 20px;
        border-radius: 18px;
        margin-bottom: 22px;
        color: #ffffff !important;
    }
    .hero-banner * { color: #ffffff !important; }

    /* Action Buttons */
    div.stButton > button, div[data-testid="stDownloadButton"] > button {
        background: linear-gradient(135deg, #059669 0%, #047857 100%) !important;
        color: #ffffff !important;
        border: none !important;
        border-radius: 14px !important;
        padding: 15px 28px !important;
        font-size: 16px !important;
        font-weight: 800 !important;
        box-shadow: 0 8px 25px rgba(5, 150, 105, 0.35) !important;
        cursor: pointer !important;
    }

    .app-footer {
        text-align: center;
        padding: 30px 10px 15px 10px;
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
    raise RuntimeError("गुगल सर्व्हर व्यस्त आहे. कृपया पुन्हा प्रयत्न करा.")

# =========================================================================
# सुवाच्य, बोल्ड हेडिंग A4 HTML Generator
# =========================================================================
def create_a4_handwritten_doc(data, subject_name, topic_name):
    marks = data.get("exam_marks", "10 Marks - LAQ")
    title = data.get("main_heading", topic_name)
    has_flowchart = data.get("include_flowchart", True)
    
    t1 = data.get("entity_1", {})
    t2 = data.get("entity_2", {})
    
    flow_html = ""
    if has_flowchart and data.get("flowchart_steps"):
        flow_steps = "".join([f'<div class="box-step">{s}</div><div class="arrow">↓</div>' for s in data.get("flowchart_steps")[:-1]])
        flow_steps += f'<div class="cloud-step">{data.get("flowchart_steps")[-1]}</div>'
        flow_html = f"""
        <div style="text-align:center; margin: 10px 0 16px 0;">
            <span class="capsule-tag">Pathogenesis / Samprapti Flowchart</span>
            <div class="flow-wrap">{flow_steps}</div>
        </div>
        """

    table_rows = "".join([f'<tr><td><b>{r.get("feature","")}</b></td><td>{r.get("point_1","")}</td><td>{r.get("point_2","")}</td></tr>' for r in data.get("comparison_table", [])])
    table_html = ""
    if table_rows:
        table_html = f"""
        <div style="margin-top: 14px;">
            <div class="sec-heading">★ Quick Exam Comparison Table:</div>
            <table class="hw-table">
                <thead>
                    <tr>
                        <th style="width:26%;">Feature</th>
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

    full_html = f"""
    <!DOCTYPE html>
    <html lang="mr">
    <head>
        <meta charset="UTF-8">
        <title>{topic_name} - A4 Handwritten Notes</title>
        <script src="https://cdnjs.cloudflare.com/ajax/libs/html2canvas/1.4.1/html2canvas.min.js"></script>
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Architects+Daughter&family=Mukta:wght@500;600;700;800;900&display=swap');

            body {{
                background-color: #e2e8f0;
                margin: 0;
                padding: 20px 10px;
                display: flex;
                flex-direction: column;
                align-items: center;
                font-family: 'Architects Daughter', 'Mukta', sans-serif;
                -webkit-font-smoothing: antialiased;
            }}

            .action-bar {{
                margin-bottom: 20px;
                display: flex;
                gap: 12px;
                font-family: sans-serif;
            }}
            .btn-action {{
                background: #0284c7;
                color: white;
                border: none;
                padding: 12px 24px;
                font-size: 15px;
                font-weight: bold;
                border-radius: 10px;
                cursor: pointer;
                box-shadow: 0 4px 14px rgba(2,132,199,0.3);
            }}

            /* True A4 Paper Container */
            .a4-paper {{
                width: 794px;
                min-height: 1123px;
                background: #ffffff;
                border: 2px solid #0f2b5c;
                box-shadow: 0 10px 30px rgba(0,0,0,0.15);
                padding: 30px 34px;
                box-sizing: border-box;
                color: #123060;
                position: relative;
                font-style: normal !important;
                letter-spacing: 0.2px;
            }}

            /* RED TEXT HIGHLIGHTER */
            .hl-red {{
                background-color: #ffe4e6 !important;
                color: #b91c1c !important;
                padding: 1px 5px !important;
                border-radius: 4px !important;
                border: 1px solid #fecdd3 !important;
                font-weight: 700 !important;
                display: inline-block;
            }}

            /* Header Section */
            .header-grid {{
                display: flex;
                justify-content: space-between;
                align-items: center;
                border-bottom: 2px solid #123060;
                padding-bottom: 10px;
                margin-bottom: 14px;
            }}
            
            /* EXTRA BOLD & PROMINENT MAIN TITLE */
            .title-box {{
                border: 2.5px solid #123060;
                border-radius: 12px;
                padding: 10px 18px;
                font-size: 24px;
                font-weight: 900 !important;
                width: 68%;
                text-align: center;
                background: #ffffff;
                color: #0a1f42 !important;
                box-shadow: 0 2px 8px rgba(18, 48, 96, 0.08);
            }}
            .title-box span {{
                border-bottom: 3px double #123060;
                padding-bottom: 2px;
                display: inline-block;
                letter-spacing: 0.5px;
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

            /* 2 Columns Layout */
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
                font-size: 17px;
                font-weight: 800;
                margin-bottom: 6px;
                background: #ffffff;
            }}
            .capsule-tag {{
                display: inline-block;
                border: 1.5px solid #123060;
                border-radius: 10px;
                padding: 2px 12px;
                font-size: 13.5px;
                font-weight: 700;
                background: #ffffff;
            }}

            /* Flowchart Boxes */
            .box-step {{
                border: 1.5px solid #123060;
                border-radius: 8px;
                padding: 5px 12px;
                font-size: 13.5px;
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
                font-size: 13.5px;
                font-weight: 700;
                width: 85%;
                margin: auto;
                background: #ffffff;
            }}

            /* Lists */
            ul.hw-list {{
                margin: 6px 0 10px 0;
                padding-left: 18px;
                font-size: 14px;
                line-height: 1.5;
            }}
            ul.hw-list li {{ margin-bottom: 5px; }}

            /* Key concept & Exam line */
            .key-concept-box {{
                border: 1.5px dashed #123060;
                border-radius: 10px;
                padding: 8px 12px;
                font-size: 13.5px;
                margin: 8px 0;
                background: #fafafa;
                line-height: 1.45;
            }}

            .sec-heading {{
                font-size: 15px;
                font-weight: 700;
                text-decoration: underline;
                margin: 10px 0 6px 0;
            }}

            /* Table */
            .hw-table {{
                width: 100%;
                border-collapse: collapse;
                font-size: 13.5px;
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
                font-size: 14px;
                font-weight: 700;
                line-height: 1.4;
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
            <button class="btn-action" onclick="downloadA4Image()">📸 A4 बॉलपेन फोटो डाऊनलोड करा (.PNG)</button>
            <button class="btn-action" style="background:#059669;" onclick="window.print()">📄 थेट PDF प्रिंट करा</button>
        </div>

        <div class="a4-paper" id="a4Canvas">
            <!-- Header with Extra Bold Main Topic & Marks -->
            <div class="header-grid">
                <div class="title-box">
                    <span>{title}</span>
                </div>
                <div class="marks-tag-box">
                    <b>{subject_name}</b><br>
                    <span class="hl-red">🎯 {marks}</span>
                </div>
            </div>

            <!-- Flowchart (If relevant) -->
            {flow_html}

            <!-- 2-Column High-Yield Bullet Notes -->
            <div class="dual-grid">
                <div class="col-half">
                    <div class="capsule-badge">① {t1.get('title','Core Concept')}</div>
                    <p style="margin:4px 0 6px 0; font-size:13.5px;"><b>Def:</b> {t1.get('definition','')}</p>
                    <div class="sec-heading">High-Yield Exam Points:</div>
                    <ul class="hw-list">{p1_html}</ul>
                    <div class="key-concept-box">
                        <b>★ Key Exam Concept:</b><br>{t1.get('exam_key','')}
                    </div>
                </div>

                <div class="col-half">
                    <div class="capsule-badge">② {t2.get('title','Clinical Correlation')}</div>
                    <p style="margin:4px 0 6px 0; font-size:13.5px;"><b>Def:</b> {t2.get('definition','')}</p>
                    <div class="sec-heading">Clinical / Systemic Features:</div>
                    <ul class="hw-list">{p2_html}</ul>
                    <div class="key-concept-box">
                        <b>★ Contemporary / Modern Link:</b><br>{t2.get('exam_key','')}
                    </div>
                </div>
            </div>

            <!-- Comparison Table -->
            {table_html}

            <!-- Concluding Punch Line -->
            <div class="exam-line">
                ✍️ <b>Exam Punch Line:</b> → "{data.get('exam_punch_line','')}"
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
<div class="premium-navbar">
    <div>
        <div class="brand-title">🌿 AyurVeda AI</div>
        <small style="color:#059669; font-weight:700;">NCISM BAMS A4 HANDWRITTEN ENGINE</small>
    </div>
    <div class="vip-badge">Avishkar Alase ✓</div>
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
        <h3 style="margin:0 0 6px 0;">🎯 BAMS A4 बॉलपेन Handwritten नोट्स</h3>
        <p style="margin:0; font-size:13.5px; opacity:0.95;">ठळक मुख्य हेडिंग (Extra Bold Title), सरळ सुवाच्य अक्षरे, महत्वाच्या शब्दांना <b>Red Highlight</b>, फ्लोचार्ट आणि गुण (Marks Weightage).</p>
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
            ["मराठी (संस्कृत श्लोक + सोपा अर्थ + मॉडर्न टर्म्स)", "Simple Indian English + Sanskrit"],
            horizontal=True
        )

    topic = st.text_input(
        "🔍 अभ्यासाचा विषय / प्रश्न टाका:",
        placeholder="उदा. Pitta Dosha Swaroopa, Garavisha vs Dooshivisha, किंवा Ashwagandha"
    )

    generate_notes_btn = st.button("🚀 सविस्तर अभ्यास नोट्स तयार करा", key="btn_notes", use_container_width=True)

    if generate_notes_btn:
        if not topic.strip():
            st.warning("⚠️ कृपया अभ्यासाचा विषय प्रविष्ट करा.")
        else:
            if "A4 Blue Ballpen" in study_mode:
                json_prompt = f"""
                You are a senior Ayurveda Professor and BAMS University Paper Setter.
                Subject: {subject}
                Topic: {topic}
                Language: {language_preference}

                Create crisp, highly readable handwritten exam notes for an A4 page.
                Determine if this is typically a 10-Mark LAQ or 5-Mark SAQ in university exams.
                Only include flowchart steps IF it genuinely needs pathogenesis/stages.

                IMPORTANT:
                - Keep sentences neat, short, and very easy to read.
                - Wrap all crucial medical keywords, cardinal symptoms, important drugs, or main mechanisms inside `<span class="hl-red">...</span>` so they get a red background highlight!
                Example: `<span class="hl-red">Ushna-Tikshna</span>`, `<span class="hl-red">Rakta Dhatu</span>`, `<span class="hl-red">Virechana</span>`.
                
                Return ONLY valid JSON matching this schema:
                {{
                    "exam_marks": "10 Marks - LAQ" or "5 Marks - SAQ",
                    "main_heading": "Crisp Title of the Topic",
                    "include_flowchart": true or false,
                    "flowchart_steps": [
                        "Step 1: Nidana / Cause with <span class='hl-red'>keyword</span>",
                        "Step 2: Agni Dushti",
                        "Step 3: Ama + Dosha Vitiation",
                        "Final: Disease Manifestation"
                    ],
                    "entity_1": {{
                        "title": "Concept 1",
                        "definition": "1 crisp line definition with <span class='hl-red'>important word</span>",
                        "key_points": [
                            "Point with <span class='hl-red'>vital keyword</span>",
                            "Point 2",
                            "Point 3 with <span class='hl-red'>critical symptom</span>"
                        ],
                        "exam_key": "1 core mechanism sentence with <span class='hl-red'>high-yield concept</span>"
                    }},
                    "entity_2": {{
                        "title": "Concept 2",
                        "definition": "1 crisp line definition with <span class='hl-red'>important word</span>",
                        "key_points": [
                            "Point with <span class='hl-red'>vital keyword</span>",
                            "Point 2",
                            "Point 3 with <span class='hl-red'>clinical treatment</span>"
                        ],
                        "exam_key": "1 clinical or contemporary correlation sentence with <span class='hl-red'>modern correlation</span>"
                    }},
                    "comparison_table": [
                        {{"feature": "Nature / Guna", "point_1": "... with <span class='hl-red'>key</span>", "point_2": "..."}},
                        {{"feature": "Cardinal Lakshana", "point_1": "<span class='hl-red'>...</span>", "point_2": "<span class='hl-red'>...</span>"}},
                        {{"feature": "Treatment Line", "point_1": "<span class='hl-red'>...</span>", "point_2": "<span class='hl-red'>...</span>"}}
                    ],
                    "exam_punch_line": "1 memorable sentence with <span class='hl-red'>core punch</span> for final marks."
                }}
                """

                with st.spinner("✍️ AI ठळक हेडिंगसह A4 Sheet तयार करत आहे..."):
                    try:
                        raw_json = ask_gemini(json_prompt, as_json=True)
                        clean_json = raw_json.strip()
                        if clean_json.startswith("```json"): clean_json = clean_json[7:]
                        if clean_json.startswith("```"): clean_json = clean_json[3:]
                        if clean_json.endswith("```"): clean_json = clean_json[:-3]

                        sheet_data = json.loads(clean_json.strip())
                        a4_html = create_a4_handwritten_doc(sheet_data, subject, topic)

                        st.balloons()
                        st.success(f"✅ ठळक हेडिंगसह A4 Sheet तयार झाली आहे! (अपेक्षित गुण: {sheet_data.get('exam_marks')})")

                        st.components.v1.html(a4_html, height=1250, scrolling=True)

                    except Exception as e:
                        st.error(f"त्रुटी: {e}")

            else:
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
                        st.markdown(notes_text)
                    except Exception as e:
                        st.error(f"त्रुटी: {e}")

# =========================================================================
# TAB 2: MEDICINE FORMULATION & MANUFACTURING (औषध निर्माण विधी)
# =========================================================================
with tab2:
    st.markdown("""
    <div class="hero-banner" style="background: linear-gradient(135deg, #0f766e 0%, #0d9488 100%) !important;">
        <h3 style="margin:0 0 6px 0;">🧪 रसशास्त्र व भैषज्य कल्पना स्पेशल</h3>
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
        m_lang = st.radio("🌐 भाषा:", ["मराठी", "Simple Indian English"], horizontal=True, key="m_lang")

    medicine_name = st.text_input("💊 गोळी किंवा औषधाचे नाव टाका:", placeholder="उदा. आरोग्यवर्धिनी वटी किंवा चंद्रप्रभावटी")

    if st.button("🔬 औषध घटक व बनवण्याची कृती शिका", key="btn_med", use_container_width=True):
        if not medicine_name.strip():
            st.warning("⚠️ कृपया औषधाचे नाव टाका.")
        else:
            with st.spinner(f"🔬 AI तज्ज्ञ '{medicine_name}' ची निर्माण पद्धत तयार करत आहे..."):
                try:
                    med_prompt = f"Explain manufacturing of {medicine_name} ({dosage_form}) in {m_lang} with ingredients table, purification, and steps."
                    res_text = ask_gemini(med_prompt)
                    st.success("✅ माहिती तयार झाली आहे!")
                    st.markdown(res_text)
                except Exception as e:
                    st.error(f"त्रुटी: {e}")

# --- Footer ---
st.markdown("""
<div class="app-footer">
    🌿 <strong>AyurVeda AI Handwritten Studio</strong> | Developed by <strong>Avishkar Alase</strong>
</div>
""", unsafe_allow_html=True)
