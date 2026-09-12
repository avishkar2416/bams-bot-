import streamlit as st
from google import genai
from google.genai import types
import markdown
import json
import time

# --- Page Setup ---
st.set_page_config(
    page_title="AyurVeda AI | Avishkar Alase",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- Universal Mobile & Theme CSS ---
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

    /* Top-Right VIP Name Card */
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

    /* Tab Design */
    .stTabs [data-baseweb="tab-list"] {
        gap: 12px;
        margin-bottom: 20px;
    }
    .stTabs [data-baseweb="tab"] {
        background-color: #ffffff !important;
        border-radius: 12px !important;
        padding: 10px 20px !important;
        font-weight: 700 !important;
        border: 1.5px solid #e2e8f0 !important;
    }
    .stTabs [aria-selected="true"] {
        background-color: #ecfdf5 !important;
        border-color: #059669 !important;
        color: #047857 !important;
    }

    /* Button */
    div.stButton > button, div[data-testid="stDownloadButton"] > button {
        background: linear-gradient(135deg, #059669 0%, #047857 100%) !important;
        color: #ffffff !important;
        border: none !important;
        border-radius: 14px !important;
        padding: 14px 24px !important;
        font-size: 16px !important;
        font-weight: 800 !important;
        box-shadow: 0 6px 20px rgba(5, 150, 105, 0.35) !important;
    }

    /* Scene Card */
    .scene-card {
        background: #ffffff;
        border-radius: 18px;
        padding: 22px;
        border: 1.5px solid #e2e8f0;
        margin-bottom: 25px;
        box-shadow: 0 8px 25px rgba(0,0,0,0.03);
    }
    .scene-title {
        color: #064e3b !important;
        font-size: 18px;
        font-weight: 800;
        margin-bottom: 12px;
    }
    .vo-box {
        background: #f0fdf4;
        border-left: 4px solid #10b981;
        padding: 12px 16px;
        border-radius: 0 10px 10px 0;
        margin: 10px 0;
        font-weight: 600;
        color: #065f46 !important;
    }

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
    st.error("⚠️ कृपया Settings > Secrets मध्ये GEMINI_API_KEY टाका.")
    st.stop()

client = genai.Client(api_key=api_key)

# Helper function to generate content using latest supported models
def generate_ai_content(prompt, as_json=False):
    models_to_try = [
        'gemini-3.6-flash',
        'gemini-2.5-pro'
    ]
    for model_name in models_to_try:
        try:
            config = types.GenerateContentConfig(response_mime_type="application/json") if as_json else None
            response = client.models.generate_content(
                model=model_name,
                contents=prompt,
                config=config
            )
            if response and response.text:
                return response.text
        except Exception:
            time.sleep(1)
            continue
    raise RuntimeError("सर्व मॉडेल्स सध्या व्यस्त आहेत. कृपया ५ सेकंदांनंतर पुन्हा प्रयत्न करा.")

# --- Printable Document Generator ---
def create_printable_html_doc(subject_name, topic_name, year_name, mode_name, raw_content):
    html_content = markdown.markdown(raw_content, extensions=['extra', 'nl2br'])
    return f"""
    <!DOCTYPE html>
    <html lang="mr">
    <head>
        <meta charset="UTF-8">
        <title>{topic_name} - BAMS Notes</title>
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+Devanagari:wght@400;600;700;800&display=swap');
            body {{ font-family: 'Noto Sans Devanagari', sans-serif; line-height: 1.8; color: #1e293b; padding: 30px; max-width: 850px; margin: auto; }}
            .header {{ background: #064e3b; color: white; padding: 20px; border-radius: 12px; margin-bottom: 20px; }}
            h1, h2 {{ color: #064e3b; }}
            blockquote {{ background: #f0fdf4; border-left: 4px solid #10b981; padding: 12px; margin: 15px 0; color: #065f46; font-weight: bold; }}
            .print-btn {{ background: #059669; color: white; padding: 10px 20px; border: none; border-radius: 8px; cursor: pointer; }}
            @media print {{ .no-print {{ display: none; }} }}
        </style>
    </head>
    <body>
        <div class="no-print" style="text-align: center; margin-bottom: 20px;">
            <button class="print-btn" onclick="window.print()">📥 PDF सेव्ह करा</button>
        </div>
        <div class="header">
            <h2>🌿 BAMS Study Guide</h2>
            <p>{year_name} | {subject_name} | {mode_name} | {topic_name}</p>
        </div>
        <div>{html_content}</div>
        <p style="text-align:center; margin-top:30px; font-size:12px; color:#888;">Developed by Avishkar Alase</p>
    </body>
    </html>
    """

# --- Navbar ---
st.markdown("""
<div class="premium-navbar">
    <div class="nav-brand">
        <div class="nav-logo">🌿</div>
        <div>
            <div class="brand-title">AyurVeda AI</div>
            <div class="brand-tag">NCISM Curriculum & Studio Engine</div>
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
tab_notes, tab_video = st.tabs(["📖 BAMS स्टडी नोट्स (Notes Engine)", "🎬 BAMS AI व्हिडिओ स्टुडिओ (Video Script & Images)"])

# ==========================================
# TAB 1: STUDY NOTES ENGINE
# ==========================================
with tab_notes:
    col1, col2 = st.columns([1, 1.2])
    with col1:
        bams_year = st.selectbox(
            "🎓 BAMS वर्ष निवडा:",
            ["BAMS 1st Professional (प्रथम वर्ष)", "BAMS 2nd Professional (द्वितीय वर्ष)", "BAMS 3rd Professional (तृतीय वर्ष)", "BAMS Final Professional (अंतिम वर्ष)"]
        )
    with col2:
        subject = st.selectbox(
            "📚 विषय निवडा:",
            ["Kriya Sharir (क्रिया शारीर)", "Rachana Sharir (रचना शारीर)", "Dravyaguna Vijnana (द्रव्यगुण विज्ञान)", "Rasashastra & Bhaishajya Kalpana (रसशास्त्र)", "Roga Nidan & Vikriti Vigyan (रोगनिदान)", "Kayachikitsa (कायचिकित्सा)", "Panchakarma (पंचकर्म)", "Shalya Tantra (शल्य तंत्र)", "Shalakya Tantra (शालाक्य तंत्र)"]
        )

    col3, col4 = st.columns([1.2, 1])
    with col3:
        study_mode = st.selectbox(
            "🎯 अभ्यासाचा प्रकार:",
            ["📖 Comprehensive Notes", "📜 Only Shlokas & Meanings", "📝 10-Mark LAQ Answer Format", "⚡ Quick Revision / Viva Voce Points", "🩺 Clinical Chikitsa & Formulations"]
        )
    with col4:
        language_preference = st.radio("🌐 माध्यम:", ["मराठी (संस्कृत श्लोक + सोपा अर्थ)", "English + Sanskrit"], horizontal=True)

    topic = st.text_input("🔍 अभ्यासाचा विषय टाका:", placeholder="उदा. Pitta Dosha Prakar किंवा Ashwagandha Pharmacology")

    if st.button("🚀 सविस्तर अभ्यास नोट्स तयार करा", key="notes_btn", use_container_width=True):
        if not topic.strip():
            st.warning("कृपया विषय प्रविष्ट करा.")
        else:
            with st.spinner("⚡ AI तज्ज्ञ अभ्यास नोट्स तयार करत आहे..."):
                prompt = f"""
                You are a senior Ayurveda Professor for BAMS.
                Academic Level: {bams_year}, Subject: {subject}, Study Mode: {study_mode}, Topic: {topic}, Language: {language_preference}.
                Generate comprehensive study notes:
                - Do not use ASCII trees or boxes.
                - Put all Sanskrit Shlokas in blockquotes (> "Shloka").
                - Bold important keywords.
                - Follow clean medical structure with Viva points.
                """
                try:
                    notes_output = generate_ai_content(prompt)
                    st.success("✅ नोट्स तयार झाल्या आहेत!")
                    st.markdown(notes_output)
                    doc_html = create_printable_html_doc(subject, topic, bams_year, study_mode, notes_output)
                    st.download_button("📥 PDF डाऊनलोड करा", data=doc_html.encode('utf-8'), file_name=f"{topic}_Notes.html", mime="text/html", use_container_width=True)
                except Exception as e:
                    st.error(f"त्रुटी: {e}")

# ==========================================
# TAB 2: AI VIDEO CREATOR STUDIO
# ==========================================
with tab_video:
    st.markdown("""
    <div style="background:#ecfdf5; padding:18px 20px; border-radius:16px; border:1px solid #a7f3d0; margin-bottom:20px;">
        <h3 style="margin:0 0 6px 0; color:#064e3b;">🎬 BAMS AI व्हिडिओ क्रिएटर स्टुडिओ</h3>
        <p style="margin:0; font-size:13.5px; color:#065f46;">तुम्ही टाकलेल्या विषयावर YouTube Shorts / Instagram Reels साठी <b>सीन-बाय-सीन व्हॉईसओव्हर, ऑन-स्क्रीन टेक्स्ट आणि प्रत्येकासाठी स्वतंत्र AI इमेज</b> तयार करा.</p>
    </div>
    """, unsafe_allow_html=True)

    v_col1, v_col2 = st.columns([1, 1])
    with v_col1:
        video_platform = st.selectbox("📱 व्हिडिओ फॉरमॅट:", ["Vertical Reels / Shorts (9:16)", "Landscape Video (16:9)"])
    with v_col2:
        voice_tone = st.selectbox("🎙️ व्हॉईसओव्हर टोन:", ["Educational & Engaging (अभ्यासपूर्ण व ओघवती)", "Doctor / Clinical Explanation (क्लिनिकल तज्ज्ञ)"])

    video_topic = st.text_input("🎯 कोणत्या BAMS विषयावर व्हिडिओ बनवायचा आहे?", placeholder="उदा. पित्ताचे ५ प्रकार, जलोदर निदान, किंवा अश्वगंधाचे चमत्कारिक फायदे")

    if st.button("🎥 AI व्हिडिओ स्क्रिप्ट आणि स्वतंत्र फोटो तयार करा", key="video_btn", use_container_width=True):
        if not video_topic.strip():
            st.warning("कृपया व्हिडिओचा विषय टाका.")
        else:
            with st.spinner("⚡ AI व्हिडिओ स्क्रिप्ट तयार करत आहे..."):
                script_prompt = f"""
                You are an expert Medical Video Producer & Ayurveda Scriptwriter.
                Topic: {video_topic}
                Platform: {video_platform}
                Tone: {voice_tone}

                Break down the topic into 3 distinct scenes for a 60-second educational video.
                Return ONLY a valid JSON array. Each object must have:
                - "scene_number": int (1, 2, 3)
                - "scene_title": Short title
                - "voiceover_marathi": Exact spoken voiceover script in natural, clear Marathi.
                - "screen_text": 2-3 bullet points to show on screen
                - "image_prompt": A highly descriptive English prompt to generate a photorealistic Ayurveda/medical image using AI (photorealistic, clean lighting, 8k, educational).
                
                No extra text, no markdown backticks around JSON. Return only the raw JSON.
                """

                try:
                    raw_json = generate_ai_content(script_prompt, as_json=True)
                    # Clean up possible markdown wrappers if model adds any
                    cleaned_json = raw_json.strip()
                    if cleaned_json.startswith("```json"):
                        cleaned_json = cleaned_json[7:]
                    if cleaned_json.startswith("```"):
                        cleaned_json = cleaned_json[3:]
                    if cleaned_json.endswith("```"):
                        cleaned_json = cleaned_json[:-3]
                    
                    scenes = json.loads(cleaned_json.strip())
                    st.success(f"✅ {len(scenes)} सीन्सची परिपूर्ण स्क्रिप्ट आणि इमेजेस तयार होत आहेत!")

                    aspect_ratio = "9:16" if "Vertical" in video_platform else "16:9"

                    for scene in scenes:
                        st.markdown(f"""
                        <div class="scene-card">
                            <div class="scene-title">🎬 सीन {scene.get('scene_number')}: {scene.get('scene_title')}</div>
                            <p><strong>🎙️ व्हॉईसओव्हर (Voiceover Script):</strong></p>
                            <div class="vo-box">"{scene.get('voiceover_marathi')}"</div>
                            <p><strong>📺 स्क्रीनवर दाखवायचा टेक्स्ट:</strong> {scene.get('screen_text')}</p>
                        </div>
                        """, unsafe_allow_html=True)

                        with st.spinner(f"🎨 सीन {scene.get('scene_number')} साठी AI इमेज तयार होत आहे..."):
                            try:
                                img_res = client.models.generate_images(
                                    model='imagen-3.0-generate-002',
                                    prompt=scene.get('image_prompt', 'Ayurveda medicinal herbs, photorealistic, 8k'),
                                    config=types.GenerateImagesConfig(
                                        number_of_images=1,
                                        aspect_ratio=aspect_ratio,
                                    )
                                )
                                for generated_image in img_res.generated_images:
                                    img_bytes = generated_image.image.image_bytes
                                    st.image(img_bytes, caption=f"सीन {scene.get('scene_number')} - AI व्हिज्युअल", use_container_width=True)
                                    st.download_button(
                                        f"📥 सीन {scene.get('scene_number')} इमेज डाऊनलोड करा",
                                        data=img_bytes,
                                        file_name=f"Scene_{scene.get('scene_number')}_{video_topic[:10]}.png",
                                        mime="image/png"
                                    )
                            except Exception as img_err:
                                st.info(f"💡 इमेज प्रॉम्ट: *{scene.get('image_prompt')}* (इमेज जनरेशन नोट: {img_err})")

                except Exception as e:
                    st.error(f"त्रुटी: {e}")

# --- Footer ---
st.markdown("""
<div class="app-footer">
    🌿 <strong>AyurVeda AI & Video Studio</strong> | Developed by <strong>Avishkar Alase</strong>
</div>
""", unsafe_allow_html=True)
