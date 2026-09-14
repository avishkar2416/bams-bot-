import streamlit as st
from google import genai
from google.genai import types
import json
import time

# --- Page Setup ---
st.set_page_config(
    page_title="AyurVeda AI | Avishkar Alase",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- Base App Styling ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@500;600;700;800&display=swap');
    * { font-family: 'Plus Jakarta Sans', sans-serif; }
    .stApp { background-color: #f8fafc; }
    
    .premium-navbar {
        display: flex; justify-content: space-between; align-items: center;
        padding: 12px 20px; background: #ffffff; border: 1px solid #e2e8f0;
        border-radius: 16px; margin-bottom: 20px; box-shadow: 0 4px 15px rgba(0,0,0,0.03);
    }
    .brand-title { font-size: 18px; font-weight: 800; color: #064e3b; margin: 0; }
    .vip-badge { background: #ecfdf5; border: 1px solid #a7f3d0; padding: 6px 14px; border-radius: 10px; font-size: 12px; font-weight: 800; color: #064e3b; }
    
    div.stButton > button {
        background: linear-gradient(135deg, #059669 0%, #047857 100%) !important;
        color: white !important; border: none !important; border-radius: 14px !important;
        padding: 16px 28px !important; font-size: 16px !important; font-weight: 800 !important;
        box-shadow: 0 6px 20px rgba(5,150,105,0.3) !important;
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
def ask_gemini_json(prompt):
    models = ['gemini-2.5-flash', 'models/gemini-3.6-flash', 'models/gemini-2.5-pro']
    for m in models:
        try:
            res = client.models.generate_content(
                model=m,
                contents=prompt,
                config=types.GenerateContentConfig(response_mime_type="application/json")
            )
            if res and res.text:
                return res.text
        except Exception:
            time.sleep(1)
            continue
    raise RuntimeError("गुगल सर्व्हर व्यस्त आहे. कृपया काही सेकंदांनंतर पुन्हा प्रयत्न करा.")

# --- Real Hand-Written Note Sheet HTML/CSS Generator ---
def render_handwritten_sheet(data, subject_name, topic_name):
    # Parsing values safely
    t1 = data.get("entity_1", {})
    t2 = data.get("entity_2", {})
    comp = data.get("comparison_table", [])
    
    # Left Flowchart Steps
    flow_1_html = "".join([f'<div class="hw-step-box">{s}</div><div class="hw-arrow">↓</div>' for s in t1.get("flowchart", [])[:-1]])
    if t1.get("flowchart"):
        flow_1_html += f'<div class="hw-cloud-box">{t1.get("flowchart")[-1]}</div>'
        
    # Right Flowchart Steps
    flow_2_html = "".join([f'<div class="hw-step-box">{s}</div><div class="hw-arrow">↓</div>' for s in t2.get("flowchart", [])[:-1]])
    if t2.get("flowchart"):
        flow_2_html += f'<div class="hw-cloud-box">{t2.get("flowchart")[-1]}</div>'

    # Manifestations
    manif_1_html = "".join([f'<li>{m}</li>' for m in t1.get("manifestations", [])])
    manif_2_html = "".join([f'<li>{m}</li>' for m in t2.get("manifestations", [])])
    
    # Comparison rows
    table_rows = "".join([f'<tr><td><b>{r.get("feature","")}</b></td><td>{r.get("entity_1","")}</td><td>{r.get("entity_2","")}</td></tr>' for r in comp])

    full_html = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>{topic_name} - Handwritten Note</title>
        <script src="https://cdnjs.cloudflare.com/ajax/libs/html2canvas/1.4.1/html2canvas.min.js"></script>
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Caveat:wght@600;700&family=Kalam:wght@400;700&family=Patrick+Hand&display=swap');
            
            body {{
                background-color: #f1f5f9;
                font-family: 'Kalam', 'Patrick Hand', cursive;
                padding: 20px;
                color: #0f172a;
            }}
            
            .action-bar {{
                text-align: center;
                margin-bottom: 25px;
            }}
            .btn-img {{
                background: #0284c7; color: white; padding: 14px 30px; font-size: 16px; font-weight: bold;
                border: none; border-radius: 12px; cursor: pointer; box-shadow: 0 6px 18px rgba(2,132,199,0.3);
                font-family: sans-serif;
            }}
            
            /* A4 Sheet - Paper Feel */
            .page-sheet {{
                background: #ffffff;
                width: 820px;
                margin: auto;
                padding: 30px 35px;
                border: 2px solid #334155;
                box-shadow: 0 10px 35px rgba(0,0,0,0.1);
                position: relative;
                box-sizing: border-box;
            }}
            
            /* Top Headings */
            .top-header-wrap {{
                display: flex;
                justify-content: space-between;
                align-items: center;
                border-bottom: 2px solid #0f172a;
                padding-bottom: 12px;
                margin-bottom: 16px;
            }}
            .main-title-box {{
                border: 2px solid #0f172a;
                border-radius: 10px;
                padding: 8px 24px;
                font-size: 24px;
                font-weight: 700;
                text-align: center;
                width: 72%;
                letter-spacing: 0.5px;
            }}
            .tag-box {{
                border: 2px solid #0f172a;
                border-radius: 8px;
                padding: 6px 12px;
                font-size: 15px;
                font-weight: 700;
                text-align: center;
            }}
            
            /* 2 Columns Layout */
            .dual-col-wrap {{
                display: flex;
                gap: 20px;
                border-bottom: 2px solid #0f172a;
                padding-bottom: 18px;
            }}
            .note-col {{
                flex: 1;
            }}
            .note-col:first-child {{
                border-right: 2px solid #0f172a;
                padding-right: 18px;
            }}
            
            /* Entity Titles */
            .entity-badge {{
                display: inline-block;
                border: 2px solid #0f172a;
                border-radius: 14px;
                padding: 3px 14px;
                font-size: 20px;
                font-weight: 700;
                margin-bottom: 8px;
            }}
            .def-line {{
                font-size: 15px;
                line-height: 1.4;
                margin-bottom: 14px;
            }}
            
            /* Section Titles with Capsule border */
            .sec-tag {{
                display: inline-block;
                border: 2px solid #0f172a;
                border-radius: 14px;
                padding: 2px 12px;
                font-size: 14px;
                font-weight: 700;
                margin-bottom: 12px;
            }}
            
            /* Flowchart Boxes */
            .flow-wrap {{
                text-align: center;
                margin-bottom: 15px;
            }}
            .hw-step-box {{
                border: 2px solid #0f172a;
                border-radius: 10px;
                padding: 5px 8px;
                font-size: 13.5px;
                font-weight: 600;
                background: #ffffff;
                margin: auto;
                width: 82%;
            }}
            .hw-arrow {{
                font-size: 16px;
                font-weight: 800;
                line-height: 1.2;
                margin: 2px 0;
            }}
            .hw-cloud-box {{
                border: 2px dashed #0f172a;
                border-radius: 20px;
                padding: 6px 10px;
                font-size: 13px;
                font-weight: 700;
                width: 85%;
                margin: auto;
            }}
            
            /* Lists */
            .manifest-list {{
                list-style: none;
                padding-left: 0;
                font-size: 13.5px;
                margin: 0 0 14px 0;
                columns: 2;
                -webkit-columns: 2;
                line-height: 1.35;
            }}
            .manifest-list li {{
                margin-bottom: 4px;
                position: relative;
                padding-left: 12px;
            }}
            .manifest-list li::before {{
                content: '•';
                position: absolute;
                left: 0;
                font-size: 15px;
            }}
            
            /* Key Concept & Corr Box */
            .cloud-wrap-box {{
                border: 2px dashed #0f172a;
                border-radius: 14px;
                padding: 8px 12px;
                font-size: 13px;
                line-height: 1.4;
                margin-bottom: 12px;
            }}
            
            /* Comparison Table */
            .bottom-section {{
                padding-top: 16px;
            }}
            .table-title {{
                font-size: 17px;
                font-weight: 700;
                margin-bottom: 8px;
            }}
            .hw-table {{
                width: 100%;
                border-collapse: collapse;
                font-size: 13.5px;
                margin-bottom: 16px;
            }}
            .hw-table th, .hw-table td {{
                border: 1.5px solid #0f172a;
                padding: 5px 8px;
                text-align: left;
            }}
            .hw-table th {{
                font-size: 14.5px;
            }}
            
            /* In Short Bubbles */
            .in-short-wrap {{
                display: flex;
                align-items: center;
                justify-content: space-around;
                margin-bottom: 14px;
            }}
            .bubble {{
                border: 2px solid #0f172a;
                border-radius: 20px;
                padding: 8px 16px;
                text-align: center;
                font-size: 13px;
                width: 38%;
            }}
            .exam-line {{
                border-top: 1.5px solid #0f172a;
                padding-top: 8px;
                font-size: 14px;
                line-height: 1.4;
            }}
            
            .watermark {{
                text-align: right;
                font-size: 11px;
                margin-top: 15px;
                opacity: 0.7;
                font-family: sans-serif;
            }}
        </style>
    </head>
    <body>
        <div class="action-bar">
            <button class="btn-img" onclick="downloadSheet()">📸 फोटो (Exact Hand-written Sheet) डाऊनलोड करा</button>
        </div>

        <div class="page-sheet" id="handwrittenSheet">
            <div class="top-header-wrap">
                <div class="main-title-box">
                    <u>{data.get("main_heading", topic_name)}</u>
                </div>
                <div class="tag-box">
                    {subject_name}<br><small>(BAMS / MD)</small>
                </div>
            </div>

            <!-- 2-Columns Side by Side -->
            <div class="dual-col-wrap">
                <!-- Column 1 -->
                <div class="note-col">
                    <div class="entity-badge">① {t1.get("title","Garavisha")}</div>
                    <div class="def-line">→ {t1.get("definition","")}</div>
                    
                    <div style="text-align:center;"><span class="sec-tag">Pathogenesis / Role in disease manifestation</span></div>
                    <div class="flow-wrap">
                        {flow_1_html}
                    </div>

                    <div style="text-align:left;"><span class="sec-tag">Diseases / Manifestations</span></div>
                    <ul class="manifest-list">
                        {manif_1_html}
                    </ul>

                    <div class="cloud-wrap-box">
                        <b>Key Concept:</b><br>{t1.get("key_concept","")}
                    </div>
                </div>

                <!-- Column 2 -->
                <div class="note-col">
                    <div class="entity-badge">② {t2.get("title","Dooshivisha")}</div>
                    <div class="def-line">→ {t2.get("definition","")}</div>
                    
                    <div style="text-align:center;"><span class="sec-tag">Pathogenesis / Role in disease manifestation</span></div>
                    <div class="flow-wrap">
                        {flow_2_html}
                    </div>

                    <div style="text-align:left;"><span class="sec-tag">Diseases / Manifestations</span></div>
                    <ul class="manifest-list">
                        {manif_2_html}
                    </ul>

                    <div class="cloud-wrap-box">
                        <b>Key Concept:</b><br>{t2.get("key_concept","")}
                    </div>

                    <div class="cloud-wrap-box" style="border-style: solid;">
                        <b>Contemporary Correlation:</b><br>{t2.get("contemporary_correlation","")}
                    </div>
                </div>
            </div>

            <!-- Comparison Table & Exam Line -->
            <div class="bottom-section">
                <div class="table-title">★ Difference in Disease Manifestation</div>
                <table class="hw-table">
                    <thead>
                        <tr>
                            <th style="width: 25%;">Feature</th>
                            <th>{t1.get("title","Entity 1")}</th>
                            <th>{t2.get("title","Entity 2")}</th>
                        </tr>
                    </thead>
                    <tbody>
                        {table_rows}
                    </tbody>
                </table>

                <div class="in-short-wrap">
                    <div class="bubble">
                        <b>{t1.get("title","Entity 1")}</b><br>{t1.get("short_summary","")}
                    </div>
                    <div style="font-size:18px; font-weight:bold;">vs</div>
                    <div class="bubble">
                        <b>{t2.get("title","Entity 2")}</b><br>{t2.get("short_summary","")}
                    </div>
                </div>

                <div class="exam-line">
                    <b>Exam Line:</b> → "{data.get("exam_punch_line","")}"
                </div>

                <div class="watermark">
                    🌿 AyurVeda AI Handwritten Matrix | Developed by Avishkar Alase
                </div>
            </div>
        </div>

        <script>
            function downloadSheet() {{
                const el = document.getElementById('handwrittenSheet');
                html2canvas(el, {{ scale: 2.5, useCORS: true }}).then(canvas => {{
                    const a = document.createElement('a');
                    a.download = '{topic_name.replace(" ", "_")}_Handwritten_Notes.png';
                    a.href = canvas.toDataURL('image/png');
                    a.click();
                }});
            }}
        </script>
    </body>
    </html>
    """
    return full_html

# --- UI Header ---
st.markdown("""
<div class="premium-navbar">
    <div>
        <div class="brand-title">🌿 AyurVeda AI Handwritten Sheet Engine</div>
        <small style="color:#059669; font-weight:700;">NCISM BAMS TOPPER SHEET FORMAT</small>
    </div>
    <div class="vip-badge">Avishkar Alase ✓</div>
</div>
""", unsafe_allow_html=True)

# --- Form Inputs ---
col1, col2 = st.columns([1, 1.2])
with col1:
    subject = st.selectbox(
        "📚 विषय (Subject):",
        [
            "Agada Tantra (अगद तंत्र)",
            "Kriya Sharir (क्रिया शारीर)",
            "Roga Nidan (रोगनिदान)",
            "Kayachikitsa (कायचिकित्सा)",
            "Dravyaguna (द्रव्यगुण)",
            "Rachana Sharir (रचना शारीर)",
            "Rasashastra (रसशास्त्र)"
        ]
    )
with col2:
    topic = st.text_input(
        "🔍 विषय / संकल्पना (Topic for Handwritten Notes):",
        value="Role of Garavisha and Dooshivisha in the Manifestation of Diseases"
    )

gen_btn = st.button("📝 हुबेहूब Handwritten Notes शीट तयार करा (1-Click)", use_container_width=True)

if gen_btn:
    if not topic.strip():
        st.warning("कृपया विषय प्रविष्ट करा.")
    else:
        json_prompt = f"""
        You are a top Ayurvedic Doctor and Exam Evaluator.
        Subject: {subject}
        Topic: {topic}

        Structure this topic EXACTLY into the 2-column comparison handwritten paper layout.
        Return ONLY valid JSON matching this schema:
        {{
            "main_heading": "Title of the note",
            "entity_1": {{
                "title": "Name of Entity 1",
                "definition": "1-2 lines simple English definition with Sanskrit term",
                "flowchart": [
                    "Step 1: Intake / Nidana",
                    "Step 2: Agni Dushti",
                    "Step 3: Ama + Dosha Vitiation",
                    "Step 4: Srotodushti",
                    "Step 5: Doshadushya Sammurchana",
                    "Final: Disease Manifestation"
                ],
                "manifestations": ["Symptom 1 (Meaning)", "Symptom 2", "Symptom 3", "Symptom 4"],
                "key_concept": "Core exam mechanism sentence",
                "short_summary": "1 line short summary for bubble"
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
                "contemporary_correlation": "Modern toxicity / bioaccumulation correlation",
                "short_summary": "1 line short summary for bubble"
            }},
            "comparison_table": [
                {{"feature": "Nature", "entity_1": "...", "entity_2": "..."}},
                {{"feature": "Onset", "entity_1": "...", "entity_2": "..."}},
                {{"feature": "Main Mechanism", "entity_1": "...", "entity_2": "..."}},
                {{"feature": "Type of Manifestation", "entity_1": "...", "entity_2": "..."}},
                {{"feature": "Examples", "entity_1": "...", "entity_2": "..."}}
            ],
            "exam_punch_line": "Exact high-scoring summary sentence for the university answer sheet."
        }}
        """

        with st.spinner("✍️ AI अगदी कागदावर पेनने लिहिल्यासारखी Handwritten Sheet डिझाइन करत आहे..."):
            try:
                raw_json = ask_gemini_json(json_prompt)
                clean_json = raw_json.strip()
                if clean_json.startswith("```json"): clean_json = clean_json[7:]
                if clean_json.startswith("```"): clean_json = clean_json[3:]
                if clean_json.endswith("```"): clean_json = clean_json[:-3]
                
                sheet_data = json.loads(clean_json.strip())
                sheet_html = render_handwritten_sheet(sheet_data, subject, topic)
                
                st.balloons()
                st.success("✅ हुबेहूब Handwritten Sheet तयार झाली आहे! खालील बटण दाबून डाऊनलोड करा.")
                
                st.download_button(
                    label="📥 Handwritten Notes फोटो (Image) डाऊनलोड करा (.html viewer)",
                    data=sheet_html.encode('utf-8'),
                    file_name=f"{topic.replace(' ', '_')}_Handwritten.html",
                    mime="text/html",
                    use_container_width=True
                )
                
                # Preview inside Streamlit
                st.components.v1.html(sheet_html, height=1150, scrolling=True)

            except Exception as e:
                st.error(f"त्रुटी: {e}")

# Footer
st.markdown("<p style='text-align:center; color:#64748b; font-size:13px;'>🌿 AyurVeda AI Handwritten Engine | Developed by <strong>Avishkar Alase</strong></p>", unsafe_allow_html=True)
