import streamlit as st
from google import genai
from google.genai import types
import json
import time
import urllib.parse
from datetime import datetime
import re
import html
import io
import markdown
from supabase import create_client, Client

# PDF Generation Imports (ReportLab)
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

# =========================================================================
# ⚙️ PAGE CONFIGURATION
# =========================================================================
st.set_page_config(
    page_title="AyurVeda AI Studio | BAMS Academic Platform",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# =========================================================================
# 🎯 AUTOMATIC DYNAMIC FESTIVAL THEME ENGINE
# =========================================================================
def get_current_festival_theme():
    now = datetime.now()
    month, day = now.month, now.day

    base = {
        "primary": "#176B4D",
        "deep_green": "#0F4935",
        "gold": "#C88A24",
        "bg": "#F7F8F4",
        "card_bg": "#FFFFFF",
        "text": "#1E2924",
        "muted": "#68756E",
        "border": "#E8EBE7",
        "success": "#15803D"
    }

    if month == 9 and 12 <= day <= 26:
        return {
            **base,
            "name": "ganeshotsav",
            "tag": "🌺 ॥ श्री गणेशाय नमः ॥ 🌺",
            "icon": "🪔",
            "festive_title": "॥ श्री गणेशाय नमः ॥",
            "festive_subtitle": "ज्ञान, आरोग्य आणि यशाच्या हार्दिक शुभेच्छा !",
            "accent_badge_bg": "#FEF3C7",
            "accent_badge_text": "#92400E",
            "accent_badge_border": "#FDE68A",
            "active_tab_border": "#D97706",
            "footer_text": "🌺 ॥ गणपती बाप्पा मोरया ॥ 🌿"
        }
    elif month == 10 and 10 <= day <= 24:
        return {
            **base,
            "name": "navratri",
            "tag": "🌸 ॥ जय जगदंब - शुभ नवरात्री ॥ 🌸",
            "icon": "🔱",
            "festive_title": "॥ जय जगदंब - शुभ नवरात्री ॥",
            "festive_subtitle": "शक्ती, विद्या आणि आरोग्याची मंगलमय साधना !",
            "accent_badge_bg": "#FFE4E6",
            "accent_badge_text": "#9F1239",
            "accent_badge_border": "#FECDD3",
            "active_tab_border": "#E11D48",
            "footer_text": "🌸 ॥ सर्वमंगल मांगल्ये शिवे सर्वार्थ साधिके ॥ 🌿"
        }
    elif month == 11 and 4 <= day <= 14:
        return {
            **base,
            "name": "diwali",
            "tag": "🪔 ॥ ॐ महालक्ष्म्यै नमः - शुभ दीपावली ॥ 🪔",
            "icon": "✨",
            "festive_title": "॥ ॐ महालक्ष्म्यै नमः - शुभ दीपावली ॥",
            "festive_subtitle": "दीपोत्सवाच्या प्रकाशाने आयुष्य समृद्ध व निरोगी होवो !",
            "accent_badge_bg": "#FEF9C3",
            "accent_badge_text": "#854D0E",
            "accent_badge_border": "#FDE047",
            "active_tab_border": "#CA8A04",
            "footer_text": "🪔 ॥ शुभ दीपावली - सुख समृद्धी लाभो ॥ 🌿"
        }
    else:
        return {
            **base,
            "name": "ayurveda_classic",
            "tag": "🌿 ॥ नमामि धन्वंतरिमादिदेवम् ॥ 🌿",
            "icon": "🌱",
            "festive_title": "॥ नमामि धन्वंतरिमादिदेवम् ॥",
            "festive_subtitle": "ज्ञान, आरोग्य आणि आयुर्वेदाच्या सर्वांगीण अभ्यासाचे व्यासपीठ !",
            "accent_badge_bg": "#EAF5EF",
            "accent_badge_text": "#0F4935",
            "accent_badge_border": "#CCE7D8",
            "active_tab_border": "#176B4D",
            "footer_text": "🌿 ॥ आरोग्यं परमं भाग्यम् ॥ 🌿"
        }

th = get_current_festival_theme()

# =========================================================================
# 📄 DIRECT PDF GENERATOR ENGINE (REPORTLAB)
# =========================================================================
def generate_direct_pdf(title, subject, student_name, text_content):
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=36,
        leftMargin=36,
        topMargin=36,
        bottomMargin=36
    )
    styles = getSampleStyleSheet()
    
    header_title_style = ParagraphStyle(
        'HeaderTitle',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=18,
        textColor=colors.HexColor('#0F4935'),
        spaceAfter=6
    )
    meta_style = ParagraphStyle(
        'MetaStyle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=10,
        textColor=colors.HexColor('#4A5851'),
        spaceAfter=14
    )
    body_style = ParagraphStyle(
        'BodyDark',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=10.5,
        leading=15,
        textColor=colors.HexColor('#1E2924'),
        spaceAfter=8
    )
    h2_style = ParagraphStyle(
        'H2Style',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=13,
        textColor=colors.HexColor('#176B4D'),
        spaceBefore=10,
        spaceAfter=4
    )

    story = []
    story.append(Paragraph("AyurVeda AI Studio - BAMS Academic Notes", header_title_style))
    story.append(Paragraph(f"<b>Subject:</b> {subject} | <b>Topic:</b> {title} | <b>Student:</b> {student_name} | <b>Date:</b> {datetime.now().strftime('%d-%m-%Y')}", meta_style))
    story.append(Spacer(1, 10))

    # Clean text to paragraph flow
    lines = text_content.split('\n')
    for line in lines:
        clean = line.strip()
        if not clean:
            story.append(Spacer(1, 4))
            continue
        # Remove bold markdown delimiters for PDF paragraph
        safe_line = clean.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
        if safe_line.startswith('#'):
            heading_txt = safe_line.lstrip('#').strip()
            story.append(Paragraph(heading_txt, h2_style))
        elif safe_line.startswith('*') or safe_line.startswith('-'):
            bullet_txt = f"&bull; {safe_line.lstrip('*- ').strip()}"
            story.append(Paragraph(bullet_txt, body_style))
        else:
            story.append(Paragraph(safe_line, body_style))

    doc.build(story)
    buffer.seek(0)
    return buffer

# =========================================================================
# 🎨 HIGH-FIDELITY CSS - SCREENSHOT REPLICATION
# =========================================================================
st.markdown(f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=Mukta:wght@400;500;600;700;800&display=swap');

    html, body, .stApp {{
        background-color: #F6F8F5 !important;
        font-family: 'Plus Jakarta Sans', 'Mukta', -apple-system, sans-serif !important;
        color: #1E2924 !important;
        -webkit-font-smoothing: antialiased;
    }}

    .main .block-container {{
        max-width: 840px !important;
        margin: 0 auto !important;
        padding-top: 0.6rem !important;
        padding-bottom: 5.5rem !important;
        padding-left: 1rem !important;
        padding-right: 1rem !important;
    }}

    header[data-testid="stHeader"], footer, div[data-testid="stToolbar"] {{
        display: none !important;
    }}

    /* Top Header Card */
    .header-card {{
        background: #FFFFFF;
        border: 1px solid #EBEFEA;
        border-radius: 20px;
        padding: 10px 16px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        box-shadow: 0 3px 12px rgba(15, 73, 53, 0.03);
        margin-bottom: 12px;
    }}
    .header-left {{
        display: flex;
        align-items: center;
        gap: 10px;
    }}
    .menu-toggle-icon {{
        font-size: 20px;
        color: #1E2924;
    }}
    .header-brand-wrap {{
        display: flex;
        align-items: center;
        gap: 8px;
    }}
    .brand-leaf-icon {{
        font-size: 24px;
        line-height: 1;
    }}
    .header-titles {{
        display: flex;
        flex-direction: column;
    }}
    .header-main-title {{
        font-size: 17px;
        font-weight: 800;
        color: #0F4935;
        line-height: 1.2;
    }}
    .header-sub-title {{
        font-size: 11px;
        font-weight: 600;
        color: #68756E;
    }}
    .header-right {{
        display: flex;
        align-items: center;
        gap: 12px;
    }}
    .avatar-circle {{
        width: 38px;
        height: 38px;
        border-radius: 50%;
        background: linear-gradient(135deg, #176B4D 0%, #0F4935 100%);
        color: #FFFFFF;
        font-weight: 800;
        font-size: 13.5px;
        display: flex;
        align-items: center;
        justify-content: center;
    }}

    /* Welcome Card */
    .welcome-card {{
        background: #FFFFFF;
        border: 1px solid #EBEFEA;
        border-radius: 20px;
        padding: 16px 18px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        box-shadow: 0 3px 12px rgba(15, 73, 53, 0.03);
        margin-bottom: 12px;
    }}
    .welcome-left {{
        display: flex;
        align-items: center;
        gap: 12px;
    }}
    .welcome-avatar {{
        width: 48px;
        height: 48px;
        border-radius: 50%;
        background: #3B5A4D;
        color: #FFFFFF;
        font-weight: 800;
        font-size: 16px;
        display: flex;
        align-items: center;
        justify-content: center;
        flex-shrink: 0;
    }}
    .welcome-text {{
        display: flex;
        flex-direction: column;
    }}
    .welcome-greeting {{
        font-size: 13px;
        color: #1E2924;
        font-weight: 600;
    }}
    .welcome-name {{
        font-size: 17px;
        font-weight: 800;
        color: #0F4935;
        line-height: 1.25;
    }}
    .welcome-subtext {{
        font-size: 11.5px;
        color: #68756E;
    }}
    .welcome-right-badge {{
        background: #F1F6F2;
        border: 1px solid #DFECE3;
        border-radius: 16px;
        padding: 8px 12px;
        display: flex;
        align-items: center;
        gap: 8px;
    }}

    /* Festival Strip */
    .festival-strip {{
        background: #FFFDF7;
        border: 1px solid #F6E6C5;
        border-radius: 18px;
        padding: 10px 16px;
        display: flex;
        align-items: center;
        justify-content: space-between;
        margin-bottom: 14px;
    }}
    .festival-strip-left {{
        display: flex;
        align-items: center;
        gap: 12px;
    }}
    .festival-lamp {{
        font-size: 22px;
        background: #FEF3C7;
        border-radius: 12px;
        padding: 4px 8px;
    }}
    .festival-title {{
        font-size: 13.5px;
        font-weight: 800;
        color: #92400E;
    }}
    .festival-sub {{
        font-size: 11.5px;
        color: #78350F;
    }}

    /* Navigation Buttons */
    div[data-testid="stHorizontalBlock"]:has(button[key^="nav_btn_"]) {{
        gap: 6px !important;
        margin-bottom: 14px !important;
    }}
    button[key^="nav_btn_"] {{
        background: #FFFFFF !important;
        color: #1E2924 !important;
        border: 1px solid #E5E9E4 !important;
        border-radius: 16px !important;
        padding: 8px 4px !important;
        height: 70px !important;
        font-size: 12px !important;
        font-weight: 700 !important;
    }}
    button[key^="nav_btn_active_"] {{
        background: #0F4935 !important;
        color: #FFFFFF !important;
        border: 1px solid #0F4935 !important;
        border-radius: 16px !important;
        padding: 8px 4px !important;
        height: 70px !important;
        font-size: 12px !important;
        font-weight: 800 !important;
        box-shadow: 0 4px 12px rgba(15, 73, 53, 0.25) !important;
    }}
    button[key^="nav_btn_active_"] p, button[key^="nav_btn_active_"] div {{
        color: #FFFFFF !important;
    }}

    /* Hero Card */
    .hero-card {{
        background: linear-gradient(135deg, #093727 0%, #0F4935 60%, #176B4D 100%);
        border-radius: 22px;
        padding: 20px 22px;
        color: #FFFFFF;
        margin-bottom: 14px;
        box-shadow: 0 8px 24px -4px rgba(15, 73, 53, 0.28);
    }}
    .hero-tag-pill {{
        display: inline-block;
        background: rgba(255, 255, 255, 0.14);
        border: 1px solid rgba(255, 255, 255, 0.25);
        border-radius: 20px;
        padding: 3px 12px;
        font-size: 11px;
        font-weight: 700;
        margin-bottom: 8px;
        color: #E2ECE6;
    }}
    .hero-main-title {{
        font-size: 24px;
        font-weight: 800;
        margin: 0;
        color: #FFFFFF;
    }}
    .hero-main-title span {{
        color: #E8C172;
    }}
    .hero-desc {{
        font-size: 12.5px;
        color: #E0EAE4;
        margin: 6px 0 16px 0;
    }}
    .hero-benefits-grid {{
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 8px;
        border-top: 1px solid rgba(255, 255, 255, 0.15);
        padding-top: 14px;
    }}
    .benefit-label {{
        font-size: 10.5px;
        font-weight: 600;
        color: #F1F6F3;
    }}

    /* Card Box */
    .study-form-card {{
        background: #FFFFFF;
        border: 1px solid #EBEFEA;
        border-radius: 22px;
        padding: 22px;
        box-shadow: 0 4px 16px rgba(15, 73, 53, 0.04);
        margin-bottom: 16px;
    }}
    .step-badge {{
        background: #E8F2EC;
        color: #0F4935;
        font-size: 11px;
        font-weight: 800;
        padding: 2px 6px;
        border-radius: 6px;
    }}

    /* Main CTA */
    div.stButton > button[key^="btn_generate_"] {{
        background: linear-gradient(135deg, #176B4D 0%, #0F4935 100%) !important;
        color: #FFFFFF !important;
        border: none !important;
        border-radius: 18px !important;
        padding: 16px 28px !important;
        font-size: 16px !important;
        font-weight: 800 !important;
        box-shadow: 0 6px 20px -2px rgba(15, 73, 53, 0.35) !important;
    }}

    /* Textbook Rendering */
    .textbook-container {{
        background: #FFFFFF;
        border: 1px solid #E2E8E3;
        border-radius: 20px;
        padding: 26px 28px;
        margin-top: 18px;
        font-size: 15.5px;
        line-height: 1.8;
    }}
    .textbook-container h1, .textbook-container h2, .textbook-container h3 {{
        color: #0F4935 !important;
        font-weight: 800 !important;
    }}
    .textbook-container blockquote {{
        border-left: 4px solid #176B4D;
        background: #F4F8F6;
        padding: 10px 16px;
        border-radius: 0 10px 10px 0;
        font-weight: 700;
        color: #0F4935;
    }}

    /* Bottom Navbar */
    .bottom-navbar-fixed {{
        position: fixed;
        bottom: 0;
        left: 0;
        right: 0;
        height: 62px;
        background: rgba(255, 255, 255, 0.96);
        backdrop-filter: blur(14px);
        border-top: 1px solid #E5EBE6;
        display: flex;
        justify-content: space-around;
        align-items: center;
        z-index: 9999;
        max-width: 840px;
        margin: 0 auto;
    }}
    .bottom-nav-item {{
        display: flex;
        flex-direction: column;
        align-items: center;
        color: #68756E;
        font-size: 11px;
        font-weight: 600;
    }}
    .bottom-nav-item.active {{
        color: #176B4D;
        font-weight: 800;
    }}

    @media (max-width: 640px) {{
        .hero-benefits-grid {{
            grid-template-columns: repeat(2, 1fr);
        }}
    }}
</style>
""", unsafe_allow_html=True)

# --- Clients Setup ---
api_key = st.secrets["GEMINI_API_KEY"]
supabase_url = st.secrets["SUPABASE_URL"]
supabase_key = st.secrets["SUPABASE_KEY"]

client = genai.Client(api_key=api_key)
supabase: Client = create_client(supabase_url, supabase_key)

# =========================================================================
# 🔄 30-MINUTE SESSION PERSISTENCE ENGINE
# =========================================================================
SESSION_TIMEOUT = 1800
now_ts = int(time.time())

persisted_uid = st.query_params.get("uid")

if "user_id" not in st.session_state:
    if persisted_uid:
        st.session_state.user_id = persisted_uid
        st.session_state.last_active = now_ts
    else:
        st.session_state.user_id = None
        st.session_state.last_active = None

if st.session_state.user_id:
    last_act = st.session_state.get("last_active", now_ts)
    if (now_ts - last_act) > SESSION_TIMEOUT:
        st.session_state.user_id = None
        st.session_state.profile = None
        st.query_params.clear()
        st.warning("⏱️ ३० मिनिटे कोणतीही हालचाल नसल्यामुळे खाते सुरक्षिततेसाठी आपोआप लॉगआउट झाले आहे.")
        st.stop()
    else:
        st.session_state.last_active = now_ts

def fetch_profile(uid):
    try:
        r = supabase.table("user_profiles").select("*").eq("user_id", uid).execute()
        if r.data and len(r.data) > 0:
            return r.data[0]
    except Exception:
        pass
    return None

if "profile" not in st.session_state or not st.session_state.profile:
    if st.session_state.user_id:
        st.session_state.profile = fetch_profile(st.session_state.user_id)

# Initialize navigation states
if "active_nav" not in st.session_state:
    st.session_state.active_nav = "Study"
if "study_mode_sel" not in st.session_state:
    st.session_state.study_mode_sel = "📖 Comprehensive Notes (संपूर्ण सविस्तर अभ्यास नोट्स)"
if "study_lang_sel" not in st.session_state:
    st.session_state.study_lang_sel = "🚩 मराठी (संस्कृत + अर्थ)"
if "topic_input_val" not in st.session_state:
    st.session_state.topic_input_val = ""

# Exam session states
if "exam_paper_data" not in st.session_state:
    st.session_state.exam_paper_data = None
if "exam_eval_data" not in st.session_state:
    st.session_state.exam_eval_data = None

# =========================================================================
# 🔐 AUTHENTICATION MODAL (LOGIN & REGISTRATION)
# =========================================================================
if not st.session_state.user_id:
    st.markdown(f"""
    <div class="header-card">
        <div class="header-left">
            <span class="brand-leaf-icon">🌿</span>
            <div class="header-titles">
                <span class="header-main-title">AyurVeda AI Studio</span>
                <span class="header-sub-title">BAMS Smart Academic Platform</span>
            </div>
        </div>
        <div class="avatar-circle">AA</div>
    </div>
    """, unsafe_allow_html=True)

    auth_col1, auth_col2, auth_col3 = st.columns([1, 6, 1])
    with auth_col2:
        st.markdown(f"""
        <div style="text-align: center; margin: 18px 0;">
            <div class="festival-strip" style="justify-content: center; display: inline-flex;">
                <span style="font-weight: 700; color: #92400E;">{th['tag']}</span>
            </div>
            <h2 style="font-size: 24px; font-weight: 800; color: #0F4935; margin: 6px 0;">विद्यार्थी अकॅडेमिक पोर्टल</h2>
            <p style="font-size: 13.5px; color: #68756E; margin: 0;">NCISM BAMS अभ्यासक्रम, A4 हस्तलिखित नोट्स, विद्यापीठ परीक्षा व प्रश्नसंच.</p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown('<div class="study-form-card">', unsafe_allow_html=True)
        t_login, t_reg = st.tabs(["🔑 विद्यार्थी लॉगिन (Sign In)", "✨ नवीन नोंदणी (Student Register)"])

        with t_login:
            l_email = st.text_input("📧 ईमेल पत्ता:", placeholder="student@gmail.com", key="auth_login_email")
            l_pass = st.text_input("🔒 पासवर्ड:", type="password", placeholder="तुमचा पासवर्ड", key="auth_login_pass")

            if st.button("🚀 थेट लॉगिन करा (Enter Studio)", use_container_width=True, key="btn_l_submit"):
                if not l_email.strip() or not l_pass.strip():
                    st.warning("कृपया ईमेल आणि पासवर्ड दोन्ही टाका.")
                else:
                    try:
                        res = supabase.auth.sign_in_with_password({"email": l_email.strip(), "password": l_pass.strip()})
                        if res.user:
                            uid = str(res.user.id)
                            st.session_state.user_id = uid
                            st.session_state.user_email = res.user.email
                            st.session_state.last_active = int(time.time())
                            st.query_params["uid"] = uid
                            st.session_state.profile = fetch_profile(uid)
                            st.success("🎉 लॉगिन यशस्वी झाले!")
                            time.sleep(0.8)
                            st.rerun()
                    except Exception as e:
                        st.error(f"लॉगिन अयशस्वी: {e}")

        with t_reg:
            r_name = st.text_input("👤 विद्यार्थ्याचे पूर्ण नाव:", placeholder="उदा. राहुल प्रकाश जोशी")
            c_mob, c_age = st.columns([2, 1])
            with c_mob:
                r_mob = st.text_input("📱 मोबाईल नंबर:", placeholder="9876543210", max_chars=10)
            with c_age:
                r_age = st.number_input("वय (Age):", min_value=17, max_value=60, value=22)

            r_col = st.text_input("🏛️ BAMS कॉलेजचे नाव:", placeholder="उदा. Government Ayurved College, Nanded")
            r_yr = st.selectbox(
                "🎓 BAMS वर्ष:",
                [
                    "BAMS 1st Professional (प्रथम वर्ष)",
                    "BAMS 2nd Professional (द्वितीय वर्ष)",
                    "BAMS 3rd Professional (तृतीय वर्ष)",
                    "BAMS Final Professional (अंतिम वर्ष)",
                    "BAMS Intern (इंटर्नशिप)"
                ]
            )
            r_em = st.text_input("📧 ईमेल पत्ता:", placeholder="student@gmail.com", key="auth_reg_em")
            r_pw = st.text_input("🔒 पासवर्ड (किमान ६ अक्षरे):", type="password", key="auth_reg_pw")

            if st.button("✨ खाते तयार करा व VIP स्टुडिओ सुरू करा", use_container_width=True, key="btn_r_submit"):
                if not r_name.strip() or not r_col.strip() or not r_em.strip() or len(r_pw.strip()) < 6:
                    st.warning("कृपया सर्व माहिती व किमान ६ अक्षरांचा पासवर्ड भरा.")
                else:
                    try:
                        auth_res = supabase.auth.sign_up({"email": r_em.strip(), "password": r_pw.strip()})
                        if auth_res.user:
                            uid = str(auth_res.user.id)
                            p_data = {
                                "user_id": uid,
                                "full_name": r_name.strip(),
                                "mobile_no": r_mob.strip(),
                                "college_name": r_col.strip(),
                                "bams_year": r_yr,
                                "age": int(r_age)
                            }
                            supabase.table("user_profiles").upsert(p_data).execute()
                            st.session_state.user_id = uid
                            st.session_state.user_email = r_em.strip()
                            st.session_state.last_active = int(time.time())
                            st.session_state.profile = p_data
                            st.query_params["uid"] = uid
                            st.success("🎉 नोंदणी यशस्वी! स्टुडिओ सुरू होत आहे...")
                            time.sleep(0.8)
                            st.rerun()
                    except Exception as e:
                        st.error(f"नोंदणी त्रुटी: {e}")

        st.markdown('</div>', unsafe_allow_html=True)
    st.stop()

# =========================================================================
# 🎯 DYNAMIC GEMINI MODEL ENGINE
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

    fallbacks = ["gemini-2.5-flash", "gemini-2.0-flash", "gemini-1.5-flash"]
    for fb in fallbacks:
        if fb not in found:
            found.append(fb)
    return found

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
# ✍️ EXACT A4 HANDWRITTEN NOTE RENDERER (UNCHANGED CORE)
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
                color: white; border: none; padding: 10px 22px; font-size: 14.5px; font-weight: 700;
                border-radius: 10px; cursor: pointer; box-shadow: 0 4px 12px rgba(2,132,199,0.3);
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

# =========================================================================
# 👤 PROFILE EXTRACTION & SIDEBAR
# =========================================================================
prof = st.session_state.profile or {}
s_name = prof.get("full_name") or "Avishkar Alase"
s_college = prof.get("college_name") or "Government Ayurved College"
s_year = prof.get("bams_year") or "BAMS 1st Professional"
s_mob = prof.get("mobile_no") or "-"
s_age = prof.get("age") or "-"
s_email = st.session_state.get("user_email") or "Active"

initials = "".join([part[0].upper() for part in s_name.split()[:2]]) if s_name else "AA"

with st.sidebar:
    st.markdown(f"""
    <div style="padding: 10px 0;">
        <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 12px;">
            <div class="avatar-circle">{initials}</div>
            <div>
                <div style="font-weight: 800; font-size: 15px; color: #0F4935;">{s_name}</div>
                <div style="font-size: 12px; color: #68756E;">{s_year}</div>
            </div>
        </div>
        <div style="font-size: 12px; color: #1E2924; background: #F8FAF7; border: 1px solid #E5ECE7; border-radius: 12px; padding: 10px; line-height: 1.6;">
            <div>🏛️ <b>कॉलेज:</b> {s_college}</div>
            <div>📱 <b>मोबाईल:</b> {s_mob} • वय: {s_age}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("##### 📚 माझ्या सेव्ह केलेल्या नोट्स")
    try:
        notes_res = supabase.table("user_notes").select("*").eq("user_id", st.session_state.user_id).order("created_at", desc=True).execute()
        if not notes_res.data:
            st.caption("अद्याप कोणतीही नोट सेव्ह केलेली नाही.")
        else:
            for item in notes_res.data:
                note_title = f"{item.get('subject', 'Note')[:14]} • {item.get('topic', '')[:14]}"
                with st.expander(f"📄 {note_title}"):
                    st.caption(f"{item.get('created_at', '')[:10]} | {item.get('study_mode', '')}")
                    st.write(item.get("content", "")[:120] + "...")
                    if st.button("🗑️ हटवा", key=f"del_{item['id']}"):
                        supabase.table("user_notes").delete().eq("id", item["id"]).execute()
                        st.success("हटवले!")
                        st.rerun()
    except Exception as e:
        st.caption(f"लोडिंग त्रुटी: {e}")

    st.write("")
    if st.button("🚪 बाहेर पडा (Logout)", use_container_width=True, key="btn_logout_sidebar"):
        try:
            supabase.auth.sign_out()
        except Exception:
            pass
        st.session_state.user_id = None
        st.session_state.profile = None
        st.session_state.last_active = None
        st.query_params.clear()
        st.rerun()

# =========================================================================
# 📱 TOP HEADER
# =========================================================================
st.markdown(f"""
<div class="header-card">
    <div class="header-left">
        <span class="menu-toggle-icon">☰</span>
        <div class="header-brand-wrap">
            <span class="brand-leaf-icon">🌿</span>
            <div class="header-titles">
                <span class="header-main-title">AyurVeda AI Studio</span>
                <span class="header-sub-title">BAMS Smart Academic Platform</span>
            </div>
        </div>
    </div>
    <div class="header-right">
        <span style="font-size:18px;">🔍</span>
        <span style="font-size:18px;">🔔</span>
        <div class="avatar-circle">{initials}</div>
    </div>
</div>
""", unsafe_allow_html=True)

# =========================================================================
# 👋 WELCOME CARD
# =========================================================================
first_name = s_name.split()[0]
safe_first_name = html.escape(first_name)
st.markdown(f"""
<div class="welcome-card">
    <div class="welcome-left">
        <div class="welcome-avatar">{initials}</div>
        <div class="welcome-text">
            <div class="welcome-greeting">Good Morning 👋</div>
            <div class="welcome-name">Welcome back, {safe_first_name}</div>
            <div class="welcome-subtext">Stay consistent, keep learning.</div>
        </div>
    </div>
    <div class="welcome-right-badge">
        <span style="font-size:16px;">📅</span>
        <div style="display:flex; flex-direction:column;">
            <span style="font-size:12px; font-weight:700; color:#0F4935;">BAMS Scholar</span>
            <span style="font-size:10px; font-style:italic; color:#436957;">Ayurveda for<br>a Better Tomorrow</span>
        </div>
        <span style="font-size:24px; opacity:0.7;">🌿</span>
    </div>
</div>
""", unsafe_allow_html=True)

# =========================================================================
# 🪔 DYNAMIC FESTIVAL STRIP
# =========================================================================
st.markdown(f"""
<div class="festival-strip">
    <div class="festival-strip-left">
        <div class="festival-lamp">{th['icon']}</div>
        <div>
            <div class="festival-title">{th['festive_title']}</div>
            <div class="festival-sub">{th['festive_subtitle']}</div>
        </div>
    </div>
    <div style="font-weight:700; color:#92400E;">›</div>
</div>
""", unsafe_allow_html=True)

# =========================================================================
# 🧭 FEATURE NAVIGATION CARDS (6 TABS INCLUDING UNIVERSITY EXAM)
# =========================================================================
nav_cols = st.columns(6)
nav_items = [
    ("Study", "📖"),
    ("Medicine", "🧪"),
    ("Viva", "🎙"),
    ("Clinical", "🩺"),
    ("Research", "🔬"),
    ("Exam", "🎓")
]

for idx, (n_name, n_icon) in enumerate(nav_items):
    with nav_cols[idx]:
        is_active = (st.session_state.active_nav == n_name)
        k_prefix = "nav_btn_active_" if is_active else "nav_btn_"
        btn_label = f"{n_icon}\n{n_name}"
        if st.button(btn_label, key=f"{k_prefix}{n_name}", use_container_width=True):
            st.session_state.active_nav = n_name
            st.rerun()

# =========================================================================
# 🏛️ TAB MODULE ROUTER
# =========================================================================

# -------------------------------------------------------------------------
# MODULE 1: STUDY STUDIO
# -------------------------------------------------------------------------
if st.session_state.active_nav == "Study":
    st.markdown("""
    <div class="hero-card">
        <div class="hero-tag-pill">BAMS • AI • NCISM • MUHS</div>
        <h2 class="hero-main-title">BAMS <span>Study Studio</span></h2>
        <div class="hero-desc">AI-powered notes, PYQs and exam-focused preparation for every BAMS student.</div>
        <div class="hero-benefits-grid">
            <div>✍️ <span class="benefit-label">Handwritten Style</span></div>
            <div>🎯 <span class="benefit-label">PYQ Solved</span></div>
            <div>🧠 <span class="benefit-label">Exam Focused</span></div>
            <div>⚡ <span class="benefit-label">Quick Revision</span></div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="study-form-card">
        <div style="font-size: 18px; font-weight: 800; color: #0F4935; margin-bottom: 12px;">
            🌿 Create Your Study Notes
        </div>
    """, unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    with c1:
        st.markdown('<div style="font-size:13px; font-weight:700; color:#0F4935; margin-bottom:4px;"><span class="step-badge">01</span> Professional Year</div>', unsafe_allow_html=True)
        bams_year = st.selectbox(
            "BAMS Year",
            ["BAMS 1st Professional (प्रथम वर्ष)", "BAMS 2nd Professional (द्वितीय वर्ष)", "BAMS 3rd Professional (तृतीय वर्ष)", "BAMS Final Professional (अंतिम वर्ष)"],
            label_visibility="collapsed"
        )
    with c2:
        st.markdown('<div style="font-size:13px; font-weight:700; color:#0F4935; margin-bottom:4px;"><span class="step-badge">02</span> Subject</div>', unsafe_allow_html=True)
        subject = st.selectbox(
            "Subject",
            [
                "Agada Tantra & Vyavahara Ayurveda (अगद तंत्र)", "Kriya Sharir (क्रिया शारीर)", "Rachana Sharir (रचना शारीर)",
                "Dravyaguna Vijnana (द्रव्यगुण विज्ञान)", "Rasashastra & Bhaishajya Kalpana (रसशास्त्र व भैषज्य कल्पना)",
                "Roga Nidan & Vikriti Vigyan (रोगनिदान)", "Samhita Siddhant & Charak Samhita (संहिता सिद्धांत)",
                "Kayachikitsa (कायचिकित्सा)", "Panchakarma (पंचकर्म)", "Shalya Tantra (शल्य तंत्र)",
                "Shalakya Tantra (शालाक्य तंत्र)", "Prasuti Tantra & Stri Roga (प्रसूति तंत्र व स्त्रीरोग)", "Kaumarbhritya (कौमारभृत्य)"
            ],
            label_visibility="collapsed"
        )

    st.markdown('<div style="font-size:13px; font-weight:700; color:#0F4935; margin: 10px 0 4px 0;"><span class="step-badge">03</span> Study Mode</div>', unsafe_allow_html=True)
    mode_options = [
        ("📖 Comprehensive Notes (संपूर्ण सविस्तर अभ्यास नोट्स)", "📄 Comprehensive Notes"),
        ("🎯 MUHS / NCISM Past 5 Years Questions & Model Answer Key", "🎯 PYQ Focus"),
        ("⚡ Quick Revision / Viva Voce Points (तोंडी परीक्षेसाठी महत्त्वाचे मुद्दे)", "⚡ Quick Revision"),
        ("📋 A4 Blue Ballpen Handwritten Sheet (अस्सल A4 पेन नोट्स)", "✍️ A4 Handwritten")
    ]
    m_cols = st.columns(4)
    for m_idx, (m_val, m_title) in enumerate(mode_options):
        with m_cols[m_idx]:
            is_m_active = (st.session_state.study_mode_sel == m_val)
            m_key = f"mode_sel_active_{m_idx}" if is_m_active else f"mode_sel_{m_idx}"
            display_title = f"✓ {m_title}" if is_m_active else m_title
            if st.button(display_title, key=m_key, use_container_width=True):
                st.session_state.study_mode_sel = m_val
                st.rerun()

    st.markdown('<div style="font-size:13px; font-weight:700; color:#0F4935; margin: 10px 0 4px 0;"><span class="step-badge">04</span> Study Medium</div>', unsafe_allow_html=True)
    l_cols = st.columns(2)
    lang_opts = [("🚩 मराठी (संस्कृत + अर्थ)", "🇮🇳 मराठी (संस्कृत + अर्थ)"), ("🌿 Simple English + Sanskrit", "🌐 Simple English + Sanskrit")]
    for l_idx, (l_val, l_title) in enumerate(lang_opts):
        with l_cols[l_idx]:
            is_l_active = (st.session_state.study_lang_sel == l_val)
            l_key = f"lang_sel_active_{l_idx}" if is_l_active else f"lang_sel_{l_idx}"
            display_ltitle = f"✓ {l_title}" if is_l_active else l_title
            if st.button(display_ltitle, key=l_key, use_container_width=True):
                st.session_state.study_lang_sel = l_val
                st.rerun()

    st.markdown('<div style="font-size:13px; font-weight:700; color:#0F4935; margin: 10px 0 4px 0;"><span class="step-badge">05</span> What do you want to study?</div>', unsafe_allow_html=True)
    topic_input = st.text_input(
        "Topic Input",
        value=st.session_state.topic_input_val,
        placeholder="उदा. Virya, Ojas, Pitta Dosha, Rakta Dhatu, Ashwagandha...",
        label_visibility="collapsed",
        key="main_topic_input"
    )

    pop_cols = st.columns(5)
    pop_list = ["Virya", "Ojas", "Pitta Dosha", "Rakta Dhatu", "Ashwagandha"]
    for p_idx, p_name in enumerate(pop_list):
        with pop_cols[p_idx]:
            if st.button(p_name, key=f"topic_chip_{p_idx}", use_container_width=True):
                st.session_state.topic_input_val = p_name
                st.rerun()

    generate_notes_btn = st.button("✨ Generate Study Notes →", key="btn_generate_main", use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    if generate_notes_btn:
        final_topic = topic_input.strip() or st.session_state.topic_input_val.strip()
        if not final_topic:
            st.warning("⚠️ कृपया अभ्यासाचा विषय प्रविष्ट करा.")
        else:
            is_marathi = "मराठी" in st.session_state.study_lang_sel
            active_study_mode = st.session_state.study_mode_sel
            lang_preference = st.session_state.study_lang_sel

            if "A4 Blue Ballpen" in active_study_mode:
                lang_rule = "Write in natural, simple spoken Marathi with Sanskrit terms and simple English in parentheses." if is_marathi else "Write 100% in pure English Roman script."
                json_prompt = f"""
                You are a senior Ayurveda Professor and BAMS University Paper Setter.
                Subject: {subject}
                Topic: {final_topic}
                Language Selected: {lang_preference}
                {lang_rule}

                Generate crisp exam notes strictly matching this JSON schema:
                {{
                    "title": "{final_topic}",
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
                with st.spinner("✨ Preparing your BAMS study notes..."):
                    try:
                        raw_json = cached_ask_gemini(json_prompt, as_json=True)
                        clean_json = raw_json.strip()
                        if clean_json.startswith("```json"): clean_json = clean_json[7:]
                        if clean_json.startswith("```"): clean_json = clean_json[3:]
                        if clean_json.endswith("```"): clean_json = clean_json[:-3]

                        st.session_state.current_generated_note = json.loads(clean_json.strip())
                        st.session_state.current_note_type = "a4_sheet"
                        st.session_state.current_topic = final_topic
                        st.session_state.current_subject = subject
                        st.session_state.current_mode = active_study_mode
                    except Exception as e:
                        st.error(f"त्रुटी: {e}")

            elif "Past 5 Years Questions" in active_study_mode:
                pyq_prompt = f"""
                You are a senior MUHS / NCISM BAMS University Chief Examiner and Paper Setter.
                Subject: {subject}
                Topic: {final_topic}
                Language Selected: {lang_preference}
                Create a definitive, high-yield 'University Past 5-Year Question Paper & Model Answer Analysis' for this topic:
                1. 🎯 Top 3 Frequently Asked University Questions (LAQ, SAQ, Viva).
                2. ✍️ Examiner's Step-by-Step Model Answer Blueprint (How to score 10/10 Marks).
                3. ⚠️ Common Mistakes to Avoid.
                4. 💡 Pro Examiner Tip for Top University Ranks.
                Format with bold headings and clean points.
                """
                with st.spinner("✨ Preparing your BAMS study notes..."):
                    try:
                        pyq_res = cached_ask_gemini(pyq_prompt, as_json=False)
                        st.session_state.current_generated_note = pyq_res
                        st.session_state.current_note_type = "text"
                        st.session_state.current_topic = final_topic
                        st.session_state.current_subject = subject
                        st.session_state.current_mode = active_study_mode
                    except Exception as e:
                        st.error(f"त्रुटी: {e}")

            else:
                system_instruction = f"""
                Tu ek senior BAMS Gold Medalist Professor aani NCISM/MUHS Chief Paper Setter aahes.
                Subject: {subject}
                Academic Level: {bams_year}
                Topic: {final_topic}
                Language Mode: {lang_preference}

                Kontaahi mudda skip na karta, khali dilelya 14 sections madhye exhaustively deep, point-to-point notes tayar kar:
                1. 📜 व्युत्पत्ती, निरुक्ती व श्लोक अन्वय (Mukhya Sanskrit Shloka > blockquote madhye reference granthasaha).
                2. 🔬 व्याख्या व स्वरूप.
                3. 🌱 उत्पत्ती व निर्मिती प्रक्रिया.
                4. 📍 स्थान व आश्रय.
                5. ⚗️ गुणधर्म व भौतिक लक्षणे.
                6. ⚙️ प्राकृत कर्मे व कार्यपद्धती.
                7. 📏 प्रमाण व परीक्षण पद्धती.
                8. ⚠️ विकृती, क्षय व वृद्धी लक्षणे.
                9. 🔗 संबंधित संकल्पनांशी तुलना.
                10. 🏥 आधुनिक विज्ञानाशी सांगड.
                11. 💊 चिकित्सा व औषधीय महत्त्व.
                12. ⭐ High-Yield Points & Memory Mnemonics.
                13. 🎯 PG AIAPGET Special Focus.
                14. 📝 संभाव्य परीक्षा प्रश्नसंच (NCISM Pattern: 1 LAQ, 2 SAQ, 4 MCQs).
                """
                with st.spinner("✨ Preparing your BAMS study notes..."):
                    try:
                        notes_res = cached_ask_gemini(system_instruction, as_json=False)
                        st.session_state.current_generated_note = notes_res
                        st.session_state.current_note_type = "text"
                        st.session_state.current_topic = final_topic
                        st.session_state.current_subject = subject
                        st.session_state.current_mode = active_study_mode
                    except Exception as e:
                        st.error(f"त्रुटी: {e}")

    # Result Rendering with DIRECT PDF DOWNLOAD
    if st.session_state.get("current_generated_note"):
        c_type = st.session_state.current_note_type
        c_data = st.session_state.current_generated_note
        c_top = st.session_state.current_topic
        c_sub = st.session_state.current_subject
        c_mod = st.session_state.current_mode

        st.markdown(f"""
        <div style="border-bottom: 1.5px solid #E2E8E3; padding-bottom: 10px; margin-top: 22px;">
            <div style="font-size: 11px; font-weight: 800; color: #176B4D; text-transform: uppercase;">📚 Generated Result</div>
            <h3 style="margin: 4px 0 2px 0; color: #0F4935; font-weight: 800;">{c_top}</h3>
            <div style="font-size: 13px; color: #68756E;">{c_sub} • {c_mod}</div>
        </div>
        """, unsafe_allow_html=True)

        col_s1, col_s2, col_s3 = st.columns([1, 1, 1])
        with col_s1:
            if st.button("💾 Save Note", key="save_n_tab1_fix", use_container_width=True):
                try:
                    save_payload = json.dumps(c_data) if c_type == "a4_sheet" else str(c_data)
                    supabase.table("user_notes").insert({
                        "user_id": st.session_state.user_id,
                        "subject": c_sub,
                        "topic": c_top,
                        "study_mode": c_mod,
                        "content": save_payload
                    }).execute()
                    st.success("✅ नोट खात्यात सेव्ह झाली!")
                    time.sleep(0.8)
                    st.rerun()
                except Exception as s_err:
                    st.error(f"सेव्ह त्रुटी: {s_err}")

        with col_s2:
            share_preview = f"🌿 *AyurVeda AI Notes*\n📚 *विषय:* {c_sub}\n🎯 *टॉपिक:* {c_top}"
            encoded_share = urllib.parse.quote(share_preview)
            st.link_button("📲 WhatsApp Share", f"[https://api.whatsapp.com/send?text=](https://api.whatsapp.com/send?text=){encoded_share}", use_container_width=True)

        with col_s3:
            # 🎯 DIRECT PDF GENERATION & DOWNLOAD
            raw_text_for_pdf = json.dumps(c_data, ensure_ascii=False) if c_type == "a4_sheet" else str(c_data)
            pdf_bytes = generate_direct_pdf(c_top, c_sub, s_name, raw_text_for_pdf)
            st.download_button(
                label="📄 थेट PDF डाउनलोड करा",
                data=pdf_bytes,
                file_name=f"{c_top.replace(' ', '_')}_BAMS_Notes.pdf",
                mime="application/pdf",
                use_container_width=True
            )

        if c_type == "a4_sheet":
            is_m = "मराठी" in st.session_state.study_lang_sel
            a4_html = render_photo_identical_sheet(c_data, c_sub, c_top, is_marathi=is_m)
            st.components.v1.html(a4_html, height=1300, scrolling=True)
        else:
            st.markdown(f'<div class="textbook-container">{c_data}</div>', unsafe_allow_html=True)

# -------------------------------------------------------------------------
# MODULE 2: MEDICINE LAB
# -------------------------------------------------------------------------
elif st.session_state.active_nav == "Medicine":
    st.markdown("""
    <div class="hero-card">
        <div class="hero-tag-pill">Bhaishajya Kalpana • Rasashastra</div>
        <h2 class="hero-main-title">🧪 Medicine Lab</h2>
        <div class="hero-desc">Learn Ayurvedic formulations, ingredients, shodhana and manufacturing procedures.</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="study-form-card">', unsafe_allow_html=True)
    m_col1, m_col2 = st.columns(2)
    with m_col1:
        dosage_form = st.selectbox("Dosage Form:", ["Vati / Gutika", "Churna", "Asava & Arishta", "Taila / Ghrita", "Bhasma & Pishti"])
    with m_col2:
        m_lang = st.radio("Language:", ["Simple Indian English", "मराठी"], horizontal=True, key="m_lang")

    medicine_name = st.text_input("औषधाचे नाव टाका:", placeholder="उदा. आरोग्यवर्धिनी वटी, चंद्रप्रभावटी")

    if "current_med_note" not in st.session_state:
        st.session_state.current_med_note = None

    if st.button("🔬 Generate Formulation Guide", key="btn_med", use_container_width=True):
        if medicine_name.strip():
            with st.spinner("🧪 Analyzing formulation..."):
                med_prompt = f"Explain manufacturing of {medicine_name} ({dosage_form}) in {m_lang} with ingredients table, purification, and steps in deep detail."
                st.session_state.current_med_note = cached_ask_gemini(med_prompt, as_json=False)

    st.markdown('</div>', unsafe_allow_html=True)

    if st.session_state.current_med_note:
        st.markdown(f'<div class="textbook-container">{st.session_state.current_med_note}</div>', unsafe_allow_html=True)
        pdf_bytes = generate_direct_pdf(medicine_name, "Rasashastra", s_name, st.session_state.current_med_note)
        st.download_button("📄 थेट PDF डाऊनलोड", pdf_bytes, file_name=f"{medicine_name}_Guide.pdf", mime="application/pdf")

# -------------------------------------------------------------------------
# MODULE 3: VIVA SIMULATOR
# -------------------------------------------------------------------------
elif st.session_state.active_nav == "Viva":
    st.markdown("""
    <div class="hero-card">
        <div class="hero-tag-pill">AI EXAMINER</div>
        <h2 class="hero-main-title">🎙 BAMS Viva Simulator</h2>
        <div class="hero-desc">Oral viva examination simulation with external examiner evaluation.</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="study-form-card">', unsafe_allow_html=True)
    v_col1, v_col2 = st.columns(2)
    with v_col1:
        viva_sub = st.selectbox("Subject:", ["Kriya Sharir", "Rachana Sharir", "Dravyaguna", "Rasa Shastra", "Agada Tantra", "Kayachikitsa", "Shalya Tantra"], key="viva_sub")
    with v_col2:
        viva_lang = st.radio("Language:", ["मराठी + Sanskrit Terms", "Simple Indian English"], horizontal=True, key="viva_lang")

    viva_topic = st.text_input("परीक्षक कोणत्या विषयावर प्रश्न विचारतील?", placeholder="उदा. Pitta Sthana, Ashwagandha Guna", key="viva_top")

    if "current_viva_note" not in st.session_state:
        st.session_state.current_viva_note = None

    if st.button("🎯 Start Viva", key="btn_viva", use_container_width=True):
        if viva_topic.strip():
            with st.spinner("🎙 AI Examiner is preparing questions..."):
                viva_prompt = f"Generate 5 high-yield Viva questions with model answers on {viva_topic} ({viva_sub}) in {viva_lang}."
                st.session_state.current_viva_note = cached_ask_gemini(viva_prompt, as_json=False)

    st.markdown('</div>', unsafe_allow_html=True)

    if st.session_state.current_viva_note:
        st.markdown(f'<div class="textbook-container">{st.session_state.current_viva_note}</div>', unsafe_allow_html=True)

# -------------------------------------------------------------------------
# MODULE 4: CLINICAL CASE STUDIO
# -------------------------------------------------------------------------
elif st.session_state.active_nav == "Clinical":
    st.markdown("""
    <div class="hero-card">
        <div class="hero-tag-pill">CASE PRESENTATION</div>
        <h2 class="hero-main-title">🩺 Clinical Case Studio</h2>
        <div class="hero-desc">Hospital OPD/IPD case sheets with Ashtavidha Pariksha, Samprapti & Chikitsa plan.</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="study-form-card">', unsafe_allow_html=True)
    c_col1, c_col2 = st.columns(2)
    with c_col1:
        case_subject = st.selectbox("Department:", ["Kayachikitsa", "Panchakarma", "Shalya Tantra", "Shalakya", "Stri Roga", "Kaumarbhritya"], key="case_sub")
    with c_col2:
        case_lang = st.radio("Language:", ["मराठी + Clinical English", "Simple Indian English + Sanskrit"], horizontal=True, key="cs_lang")

    case_topic = st.text_input("आजाराचे नाव / मुख्य लक्षणे:", placeholder="उदा. Amlapitta (GERD), Sandhivata", key="cs_top")

    if "current_case_note" not in st.session_state:
        st.session_state.current_case_note = None

    if st.button("📋 Generate Case Sheet", key="btn_case", use_container_width=True):
        if case_topic.strip():
            with st.spinner("🩺 Preparing clinical case sheet..."):
                case_prompt = f"Generate a complete Ayurvedic Clinical Case Paper for {case_topic} ({case_subject}) in {case_lang}."
                st.session_state.current_case_note = cached_ask_gemini(case_prompt, as_json=False)

    st.markdown('</div>', unsafe_allow_html=True)

    if st.session_state.current_case_note:
        st.markdown(f'<div class="textbook-container">{st.session_state.current_case_note}</div>', unsafe_allow_html=True)
        pdf_bytes = generate_direct_pdf(case_topic, case_subject, s_name, st.session_state.current_case_note)
        st.download_button("📄 Case Sheet PDF डाऊनलोड", pdf_bytes, file_name=f"{case_topic}_Case_Sheet.pdf", mime="application/pdf")

# -------------------------------------------------------------------------
# MODULE 5: RESEARCH & EVIDENCE LAB
# -------------------------------------------------------------------------
elif st.session_state.active_nav == "Research":
    st.markdown("""
    <div class="hero-card">
        <div class="hero-tag-pill">SCIENTIFIC EVIDENCE</div>
        <h2 class="hero-main-title">🔬 Research & Evidence Lab</h2>
        <div class="hero-desc">Evidence-based Ayurvedic research assistant with phytochemicals and pharmacology.</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="study-form-card">', unsafe_allow_html=True)
    res_topic = st.text_input("औषधी वनस्पती / सक्रिय घटक:", placeholder="उदा. Withania somnifera, Curcumin", key="res_top")

    if "current_res_note" not in st.session_state:
        st.session_state.current_res_note = None

    if st.button("🧬 Generate Research Summary", key="btn_research", use_container_width=True):
        if res_topic.strip():
            with st.spinner("🔬 Analyzing research trials & evidence..."):
                res_prompt = f"Provide active phytochemicals, pharmacological action and trials for {res_topic}."
                st.session_state.current_res_note = cached_ask_gemini(res_prompt, as_json=False)

    st.markdown('</div>', unsafe_allow_html=True)

    if st.session_state.current_res_note:
        st.markdown(f'<div class="textbook-container">{st.session_state.current_res_note}</div>', unsafe_allow_html=True)
        pdf_bytes = generate_direct_pdf(res_topic, "Research", s_name, st.session_state.current_res_note)
        st.download_button("📄 Research PDF डाऊनलोड", pdf_bytes, file_name=f"{res_topic}_Research.pdf", mime="application/pdf")

# -------------------------------------------------------------------------
# 🎓 MODULE 6: UNIVERSITY MOCK EXAM SIMULATOR (NEW FEATURE)
# -------------------------------------------------------------------------
elif st.session_state.active_nav == "Exam":
    st.markdown("""
    <div class="hero-card">
        <div class="hero-tag-pill">MUHS • NCISM EXAM HALL</div>
        <h2 class="hero-main-title">🎓 University Mock Exam</h2>
        <div class="hero-desc">NCISM Pattern Question Papers (MCQ, SAQ, LAQ) with AI Chief Examiner Evaluation.</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="study-form-card">', unsafe_allow_html=True)
    ex_c1, ex_c2 = st.columns(2)
    with ex_c1:
        exam_subject = st.selectbox(
            "परीक्षेचा विषय:",
            ["Kriya Sharir", "Rachana Sharir", "Dravyaguna Vijnana", "Rasashastra", "Roga Nidan", "Kayachikitsa", "Shalya Tantra", "Agada Tantra"],
            key="exam_sub_box"
        )
    with ex_c2:
        exam_pattern = st.selectbox(
            "परीक्षा प्रकार:",
            ["NCISM Standard Paper (MCQ + SAQ + LAQ)", "Quick Test (5 SAQ Questions - 25 Marks)", "Final Prelim (LAQ Intensive - 50 Marks)"]
        )

    exam_chapters = st.text_input("कोणत्या चॅप्टर्स / मुद्द्यांवर परीक्षा हवी आहे?", placeholder="उदा. Dosha Dhatu Mala, Virya Vipaka, Pitta Prakopa, Agada", key="exam_chap_input")

    if st.button("📝 प्रश्नपत्रिका तयार करा (Generate Exam Paper)", use_container_width=True, key="btn_gen_exam"):
        with st.spinner("🎓 NCISM Chief Examiner विद्यापीठ प्रश्नपत्रिका तयार करत आहेत..."):
            exam_prompt = f"""
            Tu NCISM / MUHS University BAMS Chief Paper Setter aahes.
            Subject: {exam_subject}
            Focus Chapters/Topics: {exam_chapters if exam_chapters else 'Entire Syllabus'}
            Pattern: {exam_pattern}

            Khali dilya format madhye prashnapatrika banva:
            1. University Header (MUHS / NCISM Pattern, Marks, Time)
            2. SECTION A: 5 High-yield Multiple Choice Questions (MCQs)
            3. SECTION B: 3 Short Answer Questions (SAQ - 5 Marks each)
            4. SECTION C: 1 Long Answer Question (LAQ - 10 Marks with Shloka & Clinicals)
            
            Prashna Marathi + Sanskrit Terminology madhye tayar kara.
            """
            st.session_state.exam_paper_data = cached_ask_gemini(exam_prompt, as_json=False)

    st.markdown('</div>', unsafe_allow_html=True)

    if st.session_state.exam_paper_data:
        st.markdown(f"""
        <div class="textbook-container">
            <h3 style="color:#0F4935; border-bottom:2px solid #E2E8E3; padding-bottom:8px;">🏛️ University Question Paper: {exam_subject}</h3>
            {st.session_state.exam_paper_data}
        </div>
        """, unsafe_allow_html=True)

        # PDF Download of Question Paper
        qp_pdf = generate_direct_pdf(f"University Exam - {exam_subject}", exam_subject, s_name, st.session_state.exam_paper_data)
        st.download_button("📄 प्रश्नपत्रिका PDF डाउनलोड करा", qp_pdf, file_name=f"{exam_subject}_Question_Paper.pdf", mime="application/pdf")

        # Answer Submission Section
        st.markdown('<div class="study-form-card" style="margin-top:20px;">', unsafe_allow_html=True)
        st.markdown("#### ✍️ तुमचे उत्तर तपासा (AI Answer Paper Evaluation)")
        student_answer = st.text_area(
            "तुमचे उत्तर किंवा महत्त्वाचे मुद्दे येथे लिहा (किंवा टाइप करा):",
            placeholder="उदा. Question 1 चा श्लोक, संप्राप्ती, लक्षणे आणि उपचार पद्धती...",
            height=160
        )

        if st.button("🎯 पेपर तपासा आणि गुण द्या (Evaluate My Answer)", use_container_width=True, key="btn_eval_paper"):
            if not student_answer.strip():
                st.warning("⚠️ कृपया तपासण्यासाठी तुमचे उत्तर टाइप करा.")
            else:
                with st.spinner("👨‍🏫 AI Chief Examiner तुमचे उत्तर तपासून गुण देत आहेत..."):
                    eval_prompt = f"""
                    You are a Senior BAMS University Examiner.
                    Subject: {exam_subject}
                    Original Question Paper Snippet: {st.session_state.exam_paper_data[:500]}
                    Student's Written Answer:
                    {student_answer}

                    Check this answer strictly per NCISM University Assessment Rules:
                    1. 🎯 एकूण गुण (Marks Awarded out of 10/20)
                    2. ✅ उत्तरामधील अचूक मुद्दे (Strengths)
                    3. ⚠️ सुटलेले महत्त्वाचे श्लोक / संदर्भ (Missing Shlokas or References)
                    4. 💡 10/10 गुण मिळवण्यासाठी काय सुधारणा करावी (Examiner Feedback)
                    5. 🌟 Model Answer Blueprint
                    Provide response in clear, encouraging Marathi.
                    """
                    st.session_state.exam_eval_data = cached_ask_gemini(eval_prompt, as_json=False)

        st.markdown('</div>', unsafe_allow_html=True)

        if st.session_state.exam_eval_data:
            st.markdown(f"""
            <div class="textbook-container" style="border-left: 6px solid #C88A24;">
                <h3 style="color:#92400E;">🏆 Examiner's Marksheet & Feedback</h3>
                {st.session_state.exam_eval_data}
            </div>
            """, unsafe_allow_html=True)

            eval_pdf = generate_direct_pdf(f"Evaluation - {exam_subject}", exam_subject, s_name, st.session_state.exam_eval_data)
            st.download_button("📄 निकाल व गुणपत्रिका PDF", eval_pdf, file_name=f"{exam_subject}_Result.pdf", mime="application/pdf")

# =========================================================================
# 📱 FIXED MOBILE BOTTOM NAVIGATION BAR
# =========================================================================
st.markdown("""
<div class="bottom-navbar-fixed">
    <div class="bottom-nav-item active">
        <span style="font-size:18px;">⌂</span>
        <span>Home</span>
    </div>
    <div class="bottom-nav-item">
        <span style="font-size:18px;">🔖</span>
        <span>Saved</span>
    </div>
    <div class="bottom-nav-item">
        <span style="font-size:18px;">◷</span>
        <span>History</span>
    </div>
    <div class="bottom-nav-item">
        <span style="font-size:18px;">♙</span>
        <span>Profile</span>
    </div>
</div>
""", unsafe_allow_html=True)
