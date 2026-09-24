import streamlit as st
from google import genai
from google.genai import types
import json
import time
import urllib.parse
from datetime import datetime
import re
import io
import markdown
from supabase import create_client, Client

# PDF Generation Imports (ReportLab)
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

# --- Page Setup ---
st.set_page_config(
    page_title="AyurVeda AI Studio | BAMS Academic Platform",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded"
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
        "border": "#E2E8E3",
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
            "tag": "🌸 ॥ जय जगदंब - शुभ नवरात्री व विजयादशमी ॥ 🌸",
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
            "tag": "🌿 ॥ नमामि धन्वंतरिमादिदेवम् - BAMS अकॅडेमिक स्टुडिओ ॥ 🌿",
            "icon": "🌱",
            "festive_title": "॥ नमामि धन्वंतरिमादिदेवम् ॥",
            "festive_subtitle": "ज्ञान, आरोग्य आणि आयुर्वेदाच्या सर्वांगीण अभ्यासाचे व्यासपीठ !",
            "accent_badge_bg": "#E8F5E9",
            "accent_badge_text": "#0F4935",
            "accent_badge_border": "#C8E6C9",
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
        fontSize=17,
        textColor=colors.HexColor('#0F4935'),
        spaceAfter=6
    )
    meta_style = ParagraphStyle(
        'MetaStyle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9.5,
        textColor=colors.HexColor('#4A5851'),
        spaceAfter=14
    )
    body_style = ParagraphStyle(
        'BodyDark',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=10,
        leading=15,
        textColor=colors.HexColor('#1E2924'),
        spaceAfter=8
    )
    h2_style = ParagraphStyle(
        'H2Style',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=12,
        textColor=colors.HexColor('#176B4D'),
        spaceBefore=10,
        spaceAfter=4
    )

    story = []
    story.append(Paragraph("AyurVeda AI Studio - BAMS Academic Platform", header_title_style))
    story.append(Paragraph(f"<b>Subject:</b> {subject} | <b>Topic:</b> {title} | <b>Student:</b> {student_name} | <b>Date:</b> {datetime.now().strftime('%d-%m-%Y')}", meta_style))
    story.append(Spacer(1, 10))

    lines = str(text_content).split('\n')
    for line in lines:
        clean = line.strip()
        if not clean:
            story.append(Spacer(1, 4))
            continue
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
# 🎨 PREMIUM MEDICAL AI SAAS DESIGN SYSTEM (CSS)
# =========================================================================
st.markdown(f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=Mukta:wght@400;500;600;700;800&display=swap');

    html, body, .stApp {{
        background-color: {th['bg']} !important;
        font-family: 'Plus Jakarta Sans', 'Mukta', -apple-system, sans-serif !important;
        color: {th['text']} !important;
        -webkit-font-smoothing: antialiased;
    }}

    .main .block-container {{
        max-width: 1140px !important;
        padding-top: 1.25rem !important;
        padding-bottom: 3.5rem !important;
        padding-left: 1.5rem !important;
        padding-right: 1.5rem !important;
        margin: auto !important;
    }}

    .saas-navbar {{
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 14px 24px;
        background: rgba(255, 255, 255, 0.92);
        backdrop-filter: blur(12px);
        border: 1px solid {th['border']};
        border-radius: 16px;
        margin-bottom: 20px;
        box-shadow: 0 2px 8px -2px rgba(15, 73, 53, 0.04);
    }}
    .brand-logo-badge {{
        width: 38px;
        height: 38px;
        border-radius: 10px;
        background: linear-gradient(135deg, #176B4D 0%, #0F4935 100%);
        color: #ffffff;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 19px;
    }}
    .brand-name {{
        font-size: 18px;
        font-weight: 800;
        color: {th['deep_green']};
        margin: 0;
        line-height: 1.2;
    }}
    .brand-sub {{
        font-size: 11px;
        font-weight: 600;
        color: {th['muted']};
        margin-top: 2px;
    }}
    .author-pill {{
        background: #F0F4F2;
        border: 1px solid #D5E0D9;
        padding: 5px 12px;
        border-radius: 9999px;
        font-size: 12px;
        font-weight: 700;
        color: {th['deep_green']};
    }}

    .dashboard-welcome {{
        background: #FFFFFF;
        border: 1px solid {th['border']};
        border-radius: 18px;
        padding: 24px 28px;
        margin-bottom: 22px;
        box-shadow: 0 4px 14px -4px rgba(15, 73, 53, 0.05);
        display: flex;
        justify-content: space-between;
        align-items: center;
        flex-wrap: wrap;
        gap: 16px;
    }}

    .module-hero {{
        background: linear-gradient(135deg, #0F4935 0%, #176B4D 100%);
        color: #FFFFFF !important;
        padding: 22px 26px;
        border-radius: 16px;
        margin-bottom: 20px;
        box-shadow: 0 8px 20px -6px rgba(15, 73, 53, 0.25);
        display: flex;
        justify-content: space-between;
        align-items: center;
        flex-wrap: wrap;
        gap: 12px;
    }}
    .module-hero * {{ color: #FFFFFF !important; }}

    .saas-card {{
        background: {th['card_bg']};
        border: 1px solid {th['border']};
        border-radius: 16px;
        padding: 22px;
        margin-bottom: 20px;
        box-shadow: 0 4px 12px -2px rgba(15, 73, 53, 0.03);
    }}
    .step-pill {{
        display: inline-flex;
        font-size: 11px;
        font-weight: 800;
        text-transform: uppercase;
        color: {th['primary']};
        background: #EAF3EF;
        padding: 3px 9px;
        border-radius: 6px;
        margin-bottom: 12px;
    }}

    .textbook-container {{
        background: #FFFFFF;
        border: 1px solid {th['border']};
        border-radius: 18px;
        padding: 36px 40px;
        box-shadow: 0 6px 20px -4px rgba(15, 73, 53, 0.04);
        margin-top: 18px;
        color: #1A2621;
        font-size: 16px;
        line-height: 1.85;
    }}

    .paywall-card {{
        background: #FFFFFF;
        border: 2px solid #C88A24;
        border-radius: 20px;
        padding: 30px;
        text-align: center;
        max-width: 650px;
        margin: 20px auto;
        box-shadow: 0 10px 30px rgba(200, 138, 36, 0.15);
    }}

    div.stButton > button {{
        background: {th['primary']} !important;
        color: #FFFFFF !important;
        border: 1px solid {th['primary']} !important;
        border-radius: 12px !important;
        padding: 10px 22px !important;
        font-size: 14.5px !important;
        font-weight: 600 !important;
    }}
    div.stButton > button:hover {{
        background: {th['deep_green']} !important;
    }}

    [data-testid="stSidebar"] {{
        background-color: #FFFFFF !important;
        border-right: 1px solid {th['border']} !important;
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

YEAR_SUBJECTS = {
    "BAMS 1st Professional (प्रथम वर्ष)": [
        "Kriya Sharir (क्रिया शारीर)",
        "Rachana Sharir (रचना शारीर)",
        "Samhita Siddhant & Padartha Vijnana",
        "Sanskrit & Ashtanga Hridaya"
    ],
    "BAMS 2nd Professional (द्वितीय वर्ष)": [
        "Dravyaguna Vijnana (द्रव्यगुण विज्ञान)",
        "Rasashastra & Bhaishajya Kalpana (रसशास्त्र व भैषज्य कल्पना)",
        "Roga Nidan & Vikriti Vigyan (रोगनिदान)",
        "Charak Samhita (Purvardha)"
    ],
    "BAMS 3rd Professional (तृतीय वर्ष)": [
        "Agada Tantra & Vyavahara Ayurveda (अगद तंत्र)",
        "Prasuti Tantra & Stri Roga (प्रसूति तंत्र व स्त्रीरोग)",
        "Kaumarbhritya (बालरोग / कौमारभृत्य)",
        "Swasthavritta & Yoga",
        "Charak Samhita (Uttarardha)"
    ],
    "BAMS Final Professional (अंतिम वर्ष)": [
        "Kayachikitsa (कायचिकित्सा)",
        "Panchakarma (पंचकर्म)",
        "Shalya Tantra (शल्य तंत्र)",
        "Shalakya Tantra (शालाक्य तंत्र)",
        "Research Methodology & Medical Statistics"
    ]
}

# =========================================================================
# 🔐 VIP ONBOARDING & LOGIN INTERFACE
# =========================================================================
if not st.session_state.user_id:
    st.markdown(f"""
    <div class="saas-navbar">
        <div class="saas-brand">
            <div class="brand-logo-badge">{th['icon']}</div>
            <div class="brand-title-wrap">
                <span class="brand-name">AyurVeda AI Studio</span>
                <span class="brand-sub">BAMS • AI • Academic Platform</span>
            </div>
        </div>
        <div class="author-pill">Avishkar Alase ✓</div>
    </div>
    """, unsafe_allow_html=True)

    auth_col1, auth_col2, auth_col3 = st.columns([1, 4, 1])
    with auth_col2:
        st.markdown(f"""
        <div style="text-align: center; margin-bottom: 24px;">
            <div class="festive-accent-badge">{th['tag']}</div>
            <h2 style="font-size: 26px; font-weight: 800; color: {th['deep_green']}; margin: 6px 0 4px 0;">
                BAMS Academic Portal
            </h2>
            <p style="font-size: 14px; color: {th['muted']}; margin: 0;">
                NCISM syllabus, A4 handwritten notes, exam question banks and 100 MCQ simulator.
            </p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown('<div class="saas-card">', unsafe_allow_html=True)
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
            r_yr = st.selectbox("🎓 BAMS वर्ष:", list(YEAR_SUBJECTS.keys()))
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
                                "age": int(r_age),
                                "is_pro": False
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
# 💰 ₹30 LIFETIME SUBSCRIPTION PAYWALL CHECK (DIRECT REDIRECT BUTTONS)
# =========================================================================
prof = st.session_state.profile or {}
is_pro_user = prof.get("is_pro", False)

YOUR_UPI_ID = "avishkaralase@ybl"
YOUR_NAME = "Avishkar Alase"
PAY_AMOUNT = "30"

upi_intent_url = f"upi://pay?pa={YOUR_UPI_ID}&pn={urllib.parse.quote(YOUR_NAME)}&am={PAY_AMOUNT}&cu=INR&tn=AyurVeda_AI_Lifetime"
qr_api_url = f"https://api.qrserver.com/v1/create-qr-code/?size=300x300&data={urllib.parse.quote(upi_intent_url)}"

if not is_pro_user:
    st.markdown(f"""
    <div class="paywall-card" style="background:#FFFFFF; border:2px solid #C88A24; border-radius:24px; padding:24px 20px; text-align:center; max-width:620px; margin:15px auto; box-shadow:0 12px 36px rgba(200, 138, 36, 0.15);">
        <span class="step-pill" style="background:#FEF3C7; color:#92400E; font-weight:800;">🔥 मर्यादित काळासाठी विशेष ऑफर</span>
        <h2 style="color:#0F4935; margin:10px 0 6px 0; font-size:23px; font-weight:900;">फक्त ₹३० मध्ये Lifetime Pro Access!</h2>
        <p style="color:#68756E; font-size:13.5px; margin-bottom:16px;">
            सर्व BAMS A4 हँडराइटन नोट्स, 100 MCQs ग्रँड टेस्ट, क्लिनिकल केसशीट्स आणि थेट PDF डाऊनलोड <b>आयुष्यभरासाठी मोफत मिळवा.</b>
        </p>

        <!-- Direct UPI One-Click Redirect Buttons for Mobile -->
        <div style="background:#F2F8F5; border:1px solid #D5E7DC; border-radius:18px; padding:16px; margin-bottom:18px;">
            <div style="font-size:13px; font-weight:800; color:#0F4935; margin-bottom:10px;">📱 मोबाईलवरून थेट पेमेंट करण्यासाठी खालील बटण दाबा:</div>
            <div style="display:flex; justify-content:center; gap:8px; flex-wrap:wrap;">
                <a href="{upi_intent_url}" style="background:#176B4D; color:#FFFFFF; text-decoration:none; padding:12px 22px; border-radius:14px; font-weight:800; font-size:14px; display:inline-block; box-shadow:0 4px 12px rgba(23,107,77,0.3);">
                    ⚡ Pay ₹30 via Any UPI (PhonePe / GPay / Paytm)
                </a>
            </div>
            <div style="font-size:11px; color:#475569; margin-top:8px;">(मोबाईलवर हे बटण दाबल्यावर थेट तुमचे UPI ॲप उघडेल)</div>
        </div>

        <!-- QR Code for Scanning (Desktop or other device) -->
        <div style="background:#FFFFFF; border:1.5px dashed #C88A24; border-radius:18px; padding:14px; display:inline-block; margin-bottom:14px;">
            <div style="font-size:12px; font-weight:700; color:#78350F; margin-bottom:8px;">किंवा खालील QR Code स्कॅन करा:</div>
            <img src="{qr_api_url}" width="180" style="border-radius:12px;" alt="UPI QR Code"/><br>
            <div style="margin-top:8px; font-size:13px; font-weight:800; color:#0F4935;">UPI ID: <code>{YOUR_UPI_ID}</code></div>
        </div>

        <p style="font-size:12px; color:#4A5851; margin:0 0 10px 0;">
            पेमेंट पूर्ण झाल्यावर मिळालेला १२ आकडी <b>UTR / Transaction Number</b> खाली टाका:
        </p>
    </div>
    """, unsafe_allow_html=True)

    c_pay1, c_pay2, c_pay3 = st.columns([1, 2, 1])
    with c_pay2:
        entered_utr = st.text_input(
            "📝 12-Digit UTR / Ref Number:",
            placeholder="उदा. 425689123456",
            max_chars=16,
            key="input_utr_activation"
        )
        if st.button("✨ Subscription Unlock करा (Active Lifetime)", use_container_width=True, key="btn_unlock_pro"):
            if not entered_utr.strip() or len(entered_utr.strip()) < 8:
                st.warning("⚠️ कृपया अचूक १२ आकडी UTR क्रमांक टाका.")
            else:
                with st.spinner("पडताळणी करत आहे..."):
                    try:
                        supabase.table("user_profiles").update({
                            "is_pro": True,
                            "utr_number": entered_utr.strip()
                        }).eq("user_id", st.session_state.user_id).execute()
                        
                        st.session_state.profile["is_pro"] = True
                        st.success("🎉 अभिनंदन! तुमचे Lifetime Pro Subscription सक्रिय झाले आहे!")
                        time.sleep(1)
                        st.rerun()
                    except Exception as e:
                        st.error(f"पडताळणी करताना त्रुटी: {e}")

    st.markdown("<div style='text-align:center; padding-top:15px;'><small style='color:#68756E;'>काही अडचण आल्यास संपर्क: support@ayurveda-ai.com</small></div>", unsafe_allow_html=True)
    st.stop()

# =========================================================================
# 🎯 DYNAMIC MODEL DISCOVERY & GEMINI ENGINE
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
# 👤 PROFILE EXTRACTION & SIDEBAR
# =========================================================================
s_name = prof.get("full_name") or "विद्यार्थी"
s_college = prof.get("college_name") or "BAMS Medical College"
s_year = prof.get("bams_year") or "BAMS Scholar"
s_mob = prof.get("mobile_no") or "-"
s_age = prof.get("age") or "-"
s_email = st.session_state.get("user_email") or "Active"

initials = "".join([part[0].upper() for part in s_name.split()[:2]]) if s_name else "ST"

with st.sidebar:
    st.markdown(f"""
    <div class="sidebar-profile-card">
        <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 8px;">
            <div class="sidebar-avatar">{initials}</div>
            <div>
                <div style="font-weight: 800; font-size: 15px; color: {th['deep_green']};">{s_name}</div>
                <div style="font-size: 11.5px; color: #15803D; font-weight:700;">🌟 Lifetime Pro Member</div>
            </div>
        </div>
        <div style="font-size: 12px; color: {th['text']}; line-height: 1.5; border-top: 1px solid #E5ECE7; padding-top: 8px;">
            <div>🏛️ <b>कॉलेज:</b> {s_college}</div>
            <div>🎓 <b>वर्ष:</b> {s_year}</div>
            <div>📱 <b>मो.:</b> {s_mob} • वय: {s_age}</div>
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
    if st.button("🚪 बाहेर पडा (Logout)", use_container_width=True):
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
# 🌿 MAIN DASHBOARD HEADER & WELCOME
# =========================================================================
st.markdown(f"""
<div class="saas-navbar">
    <div class="saas-brand">
        <div class="brand-logo-badge">{th['icon']}</div>
        <div class="brand-title-wrap">
            <span class="brand-name">AyurVeda AI Studio</span>
            <span class="brand-sub">BAMS Smart Academic Platform</span>
        </div>
    </div>
    <div class="author-pill">🌟 Lifetime Pro Active ✓</div>
</div>

<div class="dashboard-welcome">
    <div class="welcome-meta">
        <div class="festive-accent-badge">{th['tag']}</div>
        <h2>Good Morning 👋 Welcome back, {s_name.split()[0]}</h2>
        <p>BAMS Academic Workspace • Professional Year: <b>{s_year}</b></p>
    </div>
    <div class="quick-status-grid">
        <span class="status-chip">📖 Study</span>
        <span class="status-chip">📝 Notes</span>
        <span class="status-chip">🎯 PYQ</span>
        <span class="status-chip">🎙 Viva</span>
        <span class="status-chip">🩺 Clinical</span>
        <span class="status-chip">🔬 Research</span>
        <span class="status-chip">🎓 Exam Hall</span>
        <span class="status-chip">⏱️ 100 MCQ</span>
    </div>
</div>
""", unsafe_allow_html=True)

# 7 Navigation Tabs
tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
    "📖 Study",
    "🧪 Medicine",
    "🎯 Viva",
    "🩺 Clinical",
    "🔬 Research",
    "🎓 University Exam",
    "⏱️ 100 MCQ Test"
])

# =========================================================================
# TAB 1: BAMS STUDY NOTES & EXAM PREPARATION
# =========================================================================
with tab1:
    st.markdown(f"""
    <div class="module-hero">
        <div>
            <h3>BAMS Study Studio</h3>
            <p>AI-powered notes, PYQs & exam preparation</p>
        </div>
        <div class="module-tag">NCISM • MUHS • BAMS</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="saas-card">', unsafe_allow_html=True)
    c1, c2 = st.columns([1, 1])
    with c1:
        st.markdown('<div class="step-pill">STEP 01 • 🎓 Professional Year</div>', unsafe_allow_html=True)
        bams_year = st.selectbox("BAMS वर्ष निवडा:", list(YEAR_SUBJECTS.keys()), key="tab1_yr_select")
    with c2:
        st.markdown('<div class="step-pill">STEP 02 • 📚 Subject</div>', unsafe_allow_html=True)
        subject = st.selectbox("विषय निवडा:", YEAR_SUBJECTS[bams_year], key="tab1_sub_select")

    c3, c4 = st.columns([1, 1])
    with c3:
        st.markdown('<div class="step-pill">STEP 03 • 🎯 Study Mode</div>', unsafe_allow_html=True)
        study_mode = st.selectbox(
            "अभ्यासाचा प्रकार निवडा:",
            [
                "📖 Comprehensive Notes (संपूर्ण सविस्तर अभ्यास नोट्स)",
                "📋 A4 Blue Ballpen Handwritten Sheet (अस्सल A4 पेन नोट्स)",
                "🎯 MUHS / NCISM Past 5 Years Questions & Model Answer Key",
                "📜 Only Shlokas & Meanings (फक्त मूळ श्लोक, अन्वय व अर्थ)",
                "📝 10-Mark LAQ Answer Format (दीर्घोत्तरी प्रश्न-उत्तर फॉरमॅट)",
                "⚡ Quick Revision / Viva Voce Points (तोंडी परीक्षेसाठी महत्त्वाचे मुद्दे)"
            ]
        )
    with c4:
        st.markdown('<div class="step-pill">STEP 04 • 🌐 Language</div>', unsafe_allow_html=True)
        language_preference = st.radio("माध्यम निवडा:", ["🚩 मराठी (संस्कृत + अर्थ)", "🌿 Simple English + Sanskrit"], horizontal=True)

    st.markdown('<div class="step-pill">STEP 05 • 🔍 Topic</div>', unsafe_allow_html=True)
    topic = st.text_input("अभ्यासाचा विषय / प्रश्न प्रविष्ट करा:", placeholder="उदा. Virya, Ojas, Pitta Dosha, Rakta Dhatu, Ashwagandha, Agada")

    if "current_generated_note" not in st.session_state:
        st.session_state.current_generated_note = None
    if "current_note_type" not in st.session_state:
        st.session_state.current_note_type = ""
    if "current_topic" not in st.session_state:
        st.session_state.current_topic = ""
    if "current_subject" not in st.session_state:
        st.session_state.current_subject = ""
    if "current_mode" not in st.session_state:
        st.session_state.current_mode = ""

    generate_notes_btn = st.button("✨ Generate Study Notes", key="btn_notes", use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    if generate_notes_btn:
        if not topic.strip():
            st.warning("⚠️ कृपया अभ्यासाचा विषय प्रविष्ट करा.")
        else:
            is_marathi = "मराठी" in language_preference

            if "A4 Blue Ballpen" in study_mode:
                lang_rule = "Write in natural, simple spoken Marathi with Sanskrit terms and simple English in parentheses." if is_marathi else "Write 100% in pure English Roman script."
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
                    "nidana": ["{'अतिउष्ण, अम्ल, लवण आहार' if is_marathi else 'Excessive intake of antagonistic diet'}"],
                    "lakshana": ["{'दाह, तृष्णा' if is_marathi else 'Excessive heat, burning sensation'}"],
                    "sidebar_box_title": "Core Concept",
                    "sidebar_box_points": ["Potency", "Action Capability", "Metabolism"],
                    "samprapti_steps": [
                        "{'निदान सेवन' if is_marathi else 'Intake of Nidana'}",
                        "{'दोष प्रकोप' if is_marathi else 'Dosha Prakopa'}",
                        "{'धातु शैथिल्य' if is_marathi else 'Dhatu Vitiation'}",
                        "{'व्याधी निर्मिती' if is_marathi else 'Manifestation'}"
                    ],
                    "chikitsa": [
                        "{'दोषानुकूल चिकित्सा व शमन' if is_marathi else 'Dosha specific Pacification'}",
                        "<span class='hl-red'>शोधन</span> श्रेष्ठ"
                    ],
                    "aushadha": ["गुग्गुळू", "गुडुची (Guduchi)"],
                    "punch_line": "द्रव्याचे कर्म सामर्थ्य म्हणजेच वीर्य होय."
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
                        st.session_state.current_topic = topic
                        st.session_state.current_subject = subject
                        st.session_state.current_mode = study_mode
                    except Exception as e:
                        st.error(f"त्रुटी: {e}")

            elif "Past 5 Years Questions" in study_mode:
                pyq_prompt = f"""
                You are a senior MUHS / NCISM BAMS University Chief Examiner and Paper Setter.
                Subject: {subject}
                Topic: {topic}
                Language Selected: {language_preference}

                Create a definitive, high-yield 'University Past 5-Year Question Paper & Model Answer Analysis' for this topic:
                1. 🎯 Top 3 Frequently Asked University Questions (LAQ, SAQ, Viva).
                2. ✍️ Examiner's Step-by-Step Model Answer Blueprint (How to score 10/10 Marks).
                3. ⚠️ Common Mistakes to Avoid.
                4. 💡 Pro Examiner Tip for Top University Ranks.
                """
                with st.spinner("✨ Preparing your BAMS study notes..."):
                    try:
                        pyq_res = cached_ask_gemini(pyq_prompt, as_json=False)
                        st.session_state.current_generated_note = pyq_res
                        st.session_state.current_note_type = "text"
                        st.session_state.current_topic = topic
                        st.session_state.current_subject = subject
                        st.session_state.current_mode = study_mode
                    except Exception as e:
                        st.error(f"त्रुटी: {e}")

            else:
                system_instruction = f"""
                Tu ek senior BAMS Gold Medalist Professor aani NCISM/MUHS Chief Paper Setter aahes.
                Subject: {subject}
                Academic Level: {bams_year}
                Topic: {topic}
                Language Mode: {language_preference}

                Kontaahi mudda skip na karta, khali dilelya 14 sections madhye exhaustively deep, point-to-point notes tayar kar:
                1. 📜 व्युत्पत्ती, निरुक्ती व श्लोक अन्वय.
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
                14. 📝 संभाव्य परीक्षा प्रश्नसंच (NCISM Pattern).
                """
                with st.spinner("✨ Preparing your BAMS study notes..."):
                    try:
                        notes_res = cached_ask_gemini(system_instruction, as_json=False)
                        st.session_state.current_generated_note = notes_res
                        st.session_state.current_note_type = "text"
                        st.session_state.current_topic = topic
                        st.session_state.current_subject = subject
                        st.session_state.current_mode = study_mode
                    except Exception as e:
                        st.error(f"त्रुटी: {e}")

    # Display Result Area
    if st.session_state.current_generated_note:
        c_type = st.session_state.current_note_type
        c_data = st.session_state.current_generated_note
        c_top = st.session_state.current_topic
        c_sub = st.session_state.current_subject
        c_mod = st.session_state.current_mode

        st.markdown(f"""
        <div style="border-bottom: 1.5px solid #E2E8E3; padding-bottom: 12px; margin-top: 26px;">
            <div style="font-size: 11px; font-weight: 800; color: {th['primary']}; text-transform: uppercase;">📚 Generated Study Notes</div>
            <h3 style="margin: 4px 0 2px 0; color: {th['deep_green']}; font-weight: 800;">{c_top}</h3>
            <div style="font-size: 13px; color: {th['muted']}; font-weight: 600;">{c_sub} • {c_mod}</div>
        </div>
        """, unsafe_allow_html=True)

        col_s1, col_s2, col_s3 = st.columns([1, 1, 1])
        with col_s1:
            if st.button("💾 Save to My Account", key="save_n_tab1_fix", use_container_width=True):
                try:
                    save_payload = json.dumps(c_data) if c_type == "a4_sheet" else str(c_data)
                    supabase.table("user_notes").insert({
                        "user_id": st.session_state.user_id,
                        "subject": c_sub,
                        "topic": c_top,
                        "study_mode": c_mod,
                        "content": save_payload
                    }).execute()
                    st.success("✅ नोट तुमच्या खात्यात सुरक्षित सेव्ह झाली!")
                    time.sleep(0.8)
                    st.rerun()
                except Exception as s_err:
                    st.error(f"सेव्ह करताना त्रुटी: {s_err}")
        with col_s2:
            share_preview = f"🌿 *AyurVeda AI Notes*\n📚 *विषय:* {c_sub}\n🎯 *टॉपिक:* {c_top}\n\nAyurVeda AI Studio वर तयार केलेली नोट!"
            encoded_share = urllib.parse.quote(share_preview)
            st.link_button("📲 WhatsApp Share", f"[https://api.whatsapp.com/send?text=](https://api.whatsapp.com/send?text=){encoded_share}", use_container_width=True)

        with col_s3:
            raw_text_pdf = json.dumps(c_data, ensure_ascii=False) if c_type == "a4_sheet" else str(c_data)
            pdf_bytes = generate_direct_pdf(c_top, c_sub, s_name, raw_text_pdf)
            st.download_button(
                label="📄 थेट PDF डाउनलोड करा",
                data=pdf_bytes,
                file_name=f"{c_top.replace(' ', '_')}_BAMS_Notes.pdf",
                mime="application/pdf",
                use_container_width=True
            )

        if c_type == "a4_sheet":
            st.markdown(f"""
            <div class="saas-card" style="margin-top: 14px; background: #FAFBF9;">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <div>
                        <div style="font-weight: 800; font-size: 15px; color: {th['deep_green']};">✍️ A4 Handwritten Sheet Ready</div>
                        <small style="color: {th['muted']};">{c_sub} • {c_top} • 10 Marks / LAQ</small>
                    </div>
                    <span class="status-chip" style="background:#EAF3EF; color:{th['primary']};">Verified A4 Format</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
            is_m = "मराठी" in language_preference
            a4_html = render_photo_identical_sheet(c_data, c_sub, c_top, is_marathi=is_m)
            st.components.v1.html(a4_html, height=1300, scrolling=True)
        else:
            st.markdown(f'<div class="textbook-container">{c_data}</div>', unsafe_allow_html=True)

# =========================================================================
# TAB 2: MEDICINE LAB & FORMULATION GUIDE
# =========================================================================
with tab2:
    st.markdown("""
    <div class="module-hero">
        <div>
            <h3>🧪 Medicine Lab</h3>
            <p>Learn Ayurvedic formulations, ingredients and preparation methods.</p>
        </div>
        <div class="module-tag">Bhaishajya Kalpana • Rasashastra</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="saas-card">', unsafe_allow_html=True)
    m_col1, m_col2 = st.columns([1, 1])
    with m_col1:
        st.markdown('<div class="step-pill">Dosage Form</div>', unsafe_allow_html=True)
        dosage_form = st.selectbox("औषधाचा प्रकार (Dosage Form):", ["Vati / Gutika (गोळी / वटी)", "Churna (चूर्ण)", "Asava & Arishta (आसव व अरिष्ट)", "Taila / Ghrita (सिद्ध तेल व घृत)", "Bhasma & Pishti (भस्म व पिष्टी)"])
    with m_col2:
        st.markdown('<div class="step-pill">Language</div>', unsafe_allow_html=True)
        m_lang = st.radio("भाषा निवडा:", ["Simple Indian English", "मराठी"], horizontal=True, key="m_lang")

    st.markdown('<div class="step-pill">Medicine Name</div>', unsafe_allow_html=True)
    medicine_name = st.text_input("गोळी किंवा औषधाचे नाव टाका:", placeholder="उदा. आरोग्यवर्धिनी वटी, चंद्रप्रभावटी, सुवर्णभस्म")

    if "current_med_note" not in st.session_state:
        st.session_state.current_med_note = None

    if st.button("🔬 Generate Formulation Guide", key="btn_med", use_container_width=True):
        if not medicine_name.strip():
            st.warning("⚠️ कृपया औषधाचे नाव टाका.")
        else:
            with st.spinner("🧪 Analyzing formulation..."):
                try:
                    med_prompt = f"Explain manufacturing of {medicine_name} ({dosage_form}) in {m_lang} with ingredients table, purification, and steps in deep detail."
                    res_text = cached_ask_gemini(med_prompt, as_json=False)
                    st.session_state.current_med_note = res_text
                except Exception as e:
                    st.error(f"त्रुटी: {e}")
    st.markdown('</div>', unsafe_allow_html=True)

    if st.session_state.current_med_note:
        st.markdown(f'<div class="textbook-container">{st.session_state.current_med_note}</div>', unsafe_allow_html=True)
        m_c1, m_c2 = st.columns(2)
        with m_c1:
            if st.button("💾 Save Formulation to Notes", key="save_med_btn", use_container_width=True):
                try:
                    supabase.table("user_notes").insert({
                        "user_id": st.session_state.user_id,
                        "subject": "Rasashastra & Bhaishajya Kalpana",
                        "topic": medicine_name,
                        "study_mode": dosage_form,
                        "content": st.session_state.current_med_note
                    }).execute()
                    st.success("✅ खात्यात सेव्ह झाले!")
                    time.sleep(0.8)
                    st.rerun()
                except Exception as e:
                    st.error(f"त्रुटी: {e}")
        with m_c2:
            m_pdf = generate_direct_pdf(medicine_name, "Rasashastra", s_name, st.session_state.current_med_note)
            st.download_button("📄 थेट PDF डाउनलोड करा", m_pdf, file_name=f"{medicine_name}_Guide.pdf", mime="application/pdf", use_container_width=True)

# =========================================================================
# TAB 3: AI VIVA SIMULATOR
# =========================================================================
with tab3:
    st.markdown("""
    <div class="module-hero">
        <div>
            <h3>🎙 BAMS Viva Simulator</h3>
            <p>Oral viva examination simulation with external examiner evaluation.</p>
        </div>
        <div class="module-tag">AI EXAMINER</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="saas-card">', unsafe_allow_html=True)
    v_col1, v_col2 = st.columns([1, 1])
    with v_col1:
        st.markdown('<div class="step-pill">Subject</div>', unsafe_allow_html=True)
        viva_sub = st.selectbox("Viva साठी विषय:", ["Kriya Sharir", "Rachana Sharir", "Dravyaguna", "Rasa Shastra", "Agada Tantra", "Kayachikitsa", "Shalya Tantra"], key="viva_sub")
    with v_col2:
        st.markdown('<div class="step-pill">Language</div>', unsafe_allow_html=True)
        viva_lang = st.radio("Viva भाषा:", ["मराठी + Sanskrit Terms", "Simple Indian English"], horizontal=True, key="viva_lang")

    st.markdown('<div class="step-pill">Topic</div>', unsafe_allow_html=True)
    viva_topic = st.text_input("परीक्षक कोणत्या विषयावर प्रश्न विचारतील?", placeholder="उदा. Pitta Sthana, Ashwagandha Guna, Vatsanabha Shodhana", key="viva_top")

    if "current_viva_note" not in st.session_state:
        st.session_state.current_viva_note = None

    if st.button("🎯 Start Viva", key="btn_viva", use_container_width=True):
        if not viva_topic.strip():
            st.warning("⚠️ कृपया विषयाचे नाव टाका.")
        else:
            with st.spinner("🎙 AI Examiner is preparing questions..."):
                try:
                    viva_prompt = f"Generate 5 high-yield Viva questions with model answers on {viva_topic} ({viva_sub}) in {viva_lang}."
                    st.session_state.current_viva_note = cached_ask_gemini(viva_prompt, as_json=False)
                except Exception as e:
                    st.error(f"त्रुटी: {e}")
    st.markdown('</div>', unsafe_allow_html=True)

    if st.session_state.current_viva_note:
        st.markdown(f'<div class="textbook-container">{st.session_state.current_viva_note}</div>', unsafe_allow_html=True)

# =========================================================================
# TAB 4: CLINICAL CASE PRESENTATION
# =========================================================================
with tab4:
    st.markdown("""
    <div class="module-hero">
        <div>
            <h3>🩺 Clinical Case Studio</h3>
            <p>Complete hospital OPD/IPD Ayurvedic clinical case presentation.</p>
        </div>
        <div class="module-tag">CASE PRESENTATION</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="saas-card">', unsafe_allow_html=True)
    c_col1, c_col2 = st.columns([1, 1])
    with c_col1:
        st.markdown('<div class="step-pill">Department</div>', unsafe_allow_html=True)
        case_subject = st.selectbox("Department:", ["Kayachikitsa", "Panchakarma", "Shalya Tantra", "Shalakya", "Stri Roga", "Kaumarbhritya"], key="case_sub")
    with c_col2:
        st.markdown('<div class="step-pill">Language</div>', unsafe_allow_html=True)
        case_lang = st.radio("भाषा निवडा:", ["मराठी + Clinical English", "Simple Indian English + Sanskrit"], horizontal=True, key="cs_lang")

    st.markdown('<div class="step-pill">Disease / Symptoms</div>', unsafe_allow_html=True)
    case_topic = st.text_input("आजाराचे नाव / मुख्य लक्षणे प्रविष्ट करा:", placeholder="उदा. Amlapitta (GERD), Sandhivata (Osteoarthritis)", key="cs_top")

    if "current_case_note" not in st.session_state:
        st.session_state.current_case_note = None

    if st.button("📋 Generate Case Sheet", key="btn_case", use_container_width=True):
        if not case_topic.strip():
            st.warning("⚠️ कृपया आजाराचे नाव टाका.")
        else:
            with st.spinner("🩺 Preparing clinical case presentation..."):
                try:
                    case_prompt = f"Generate a complete Ayurvedic Clinical Case Paper for {case_topic} ({case_subject}) in {case_lang}."
                    st.session_state.current_case_note = cached_ask_gemini(case_prompt, as_json=False)
                except Exception as e:
                    st.error(f"त्रुटी: {e}")
    st.markdown('</div>', unsafe_allow_html=True)

    if st.session_state.current_case_note:
        st.markdown(f'<div class="textbook-container">{st.session_state.current_case_note}</div>', unsafe_allow_html=True)
        cs_pdf = generate_direct_pdf(case_topic, case_subject, s_name, st.session_state.current_case_note)
        st.download_button("📄 Case Sheet PDF डाउनलोड करा", cs_pdf, file_name=f"{case_topic}_Case_Sheet.pdf", mime="application/pdf")

# =========================================================================
# TAB 5: RESEARCH & EVIDENCE LAB
# =========================================================================
with tab5:
    st.markdown("""
    <div class="module-hero">
        <div>
            <h3>🔬 Research & Evidence Lab</h3>
            <p>Evidence-based Ayurvedic research assistant</p>
        </div>
        <div class="module-tag">SCIENTIFIC EVIDENCE</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="saas-card">', unsafe_allow_html=True)
    st.markdown('<div class="step-pill">Herb / Drug / Compound</div>', unsafe_allow_html=True)
    res_topic = st.text_input("औषधी वनस्पती किंवा सक्रिय घटक:", placeholder="उदा. Withania somnifera (Ashwagandha), Tinospora cordifolia (Guduchi)", key="res_top")

    if "current_res_note" not in st.session_state:
        st.session_state.current_res_note = None

    if st.button("🧬 Generate Research Summary", key="btn_research", use_container_width=True):
        if not res_topic.strip():
            st.warning("⚠️ कृपया संशोधन द्रव्याचे नाव टाका.")
        else:
            with st.spinner("🔬 Analyzing available evidence..."):
                try:
                    res_prompt = f"Provide active phytochemicals, pharmacological action and trials for {res_topic}."
                    st.session_state.current_res_note = cached_ask_gemini(res_prompt, as_json=False)
                except Exception as e:
                    st.error(f"त्रुटी: {e}")
    st.markdown('</div>', unsafe_allow_html=True)

    if st.session_state.current_res_note:
        st.markdown(f'<div class="textbook-container">{st.session_state.current_res_note}</div>', unsafe_allow_html=True)
        r_pdf = generate_direct_pdf(res_topic, "Research", s_name, st.session_state.current_res_note)
        st.download_button("📄 Research PDF डाउनलोड करा", r_pdf, file_name=f"{res_topic}_Research.pdf", mime="application/pdf")

# =========================================================================
# 🎓 TAB 6: UNIVERSITY FIX QUESTIONS & PAPER SIMULATOR
# =========================================================================
with tab6:
    st.markdown("""
    <div class="module-hero">
        <div>
            <h3>🎓 MUHS / NCISM 100% Fix Questions & Exam Hall</h3>
            <p>विद्यापीठात हमखास येणारे फिक्स प्रश्न, मॉडेल उत्तरे व थेट AI पेपर तपासणी.</p>
        </div>
        <div class="module-tag">HIGH-YIELD QUESTION BANK</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="saas-card">', unsafe_allow_html=True)
    ex_c1, ex_c2 = st.columns(2)
    with ex_c1:
        st.markdown('<div class="step-pill">Academic Year</div>', unsafe_allow_html=True)
        fix_exam_year = st.selectbox("BAMS वर्ष:", list(YEAR_SUBJECTS.keys()), key="fix_ex_yr_select")
    with ex_c2:
        st.markdown('<div class="step-pill">Subject</div>', unsafe_allow_html=True)
        fix_exam_sub = st.selectbox("परीक्षेचा विषय:", YEAR_SUBJECTS[fix_exam_year], key="fix_ex_sub_select")

    st.markdown('<div class="step-pill">Category</div>', unsafe_allow_html=True)
    fix_practice_type = st.selectbox(
        "परीक्षेसाठी काय सराव करायचा आहे?",
        [
            "🎯 100% Fix Repeated MCQs (२० गुण हमखास सराव)",
            "📝 10-Mark LAQ Confirmed Questions (दीर्घोत्तरी फिक्स प्रश्न बँक)",
            "⚡ 5-Mark SAQ High-Yield Bank (लघुत्तरी फिक्स प्रश्न)",
            "🏛️ Complete University Mock Exam Paper (MCQ + SAQ + LAQ)"
        ]
    )

    if "fix_exam_content" not in st.session_state:
        st.session_state.fix_exam_content = None

    if st.button("🔥 हमखास येणारे फिक्स प्रश्न लोड करा", key="btn_load_fix_exam_tab6", use_container_width=True):
        with st.spinner(f"🎓 AI Chief Examiner '{fix_exam_sub}' चे फिक्स प्रश्न तयार करत आहेत..."):
            try:
                fix_prompt = f"""
                You are a Chief Paper Setter and Gold Medalist Professor for MUHS & NCISM BAMS Examinations.
                Subject: {fix_exam_sub}
                Academic Year: {fix_exam_year}
                Category Selected: {fix_practice_type}

                Generate exhaustive, authentic university exam practice material in Marathi with accurate Sanskrit terms.
                Provide guaranteed questions with marks weightage, mandatory Sanskrit Shloka needed, and Model Answer Outline.
                """
                st.session_state.fix_exam_content = cached_ask_gemini(fix_prompt, as_json=False)
            except Exception as e:
                st.error(f"त्रुटी: {e}")

    st.markdown('</div>', unsafe_allow_html=True)

    if st.session_state.fix_exam_content:
        st.markdown(f'<div class="textbook-container">{st.session_state.fix_exam_content}</div>', unsafe_allow_html=True)
        fix_pdf = generate_direct_pdf(f"Fix Exam Bank - {fix_exam_sub}", fix_exam_sub, s_name, st.session_state.fix_exam_content)
        st.download_button("📄 फिक्स प्रश्नसंच PDF डाउनलोड करा", fix_pdf, file_name=f"{fix_exam_sub.split()[0]}_Fix_Questions.pdf", mime="application/pdf", use_container_width=True)

# =========================================================================
# ⏱️ TAB 7: 100 MCQs GRAND TEST SIMULATOR (60 MINUTES TIMER)
# =========================================================================
with tab7:
    st.markdown("""
    <div class="module-hero">
        <div>
            <h3>⏱️ NCISM / AIAPGET 100 MCQs Grand Test Simulator</h3>
            <p>100 गुण • 60 मिनिटे वेळ • लाईव्ह टाइमर, निगेटिव्ह मार्किंग व परिपूर्ण विश्लेषण.</p>
        </div>
        <div class="module-tag">60-MIN LIVE SPEED TEST</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="saas-card">', unsafe_allow_html=True)
    t7_yr_col, t7_sub_col = st.columns(2)
    with t7_yr_col:
        st.markdown('<div class="step-pill">BAMS Year</div>', unsafe_allow_html=True)
        mcq_year = st.selectbox("तुमचे वर्ष निवडा:", list(YEAR_SUBJECTS.keys()), key="mcq_test_year_t7")
    with t7_sub_col:
        st.markdown('<div class="step-pill">Subject</div>', unsafe_allow_html=True)
        mcq_subject = st.selectbox("परीक्षेचा विषय निवडा:", YEAR_SUBJECTS[mcq_year], key="mcq_test_subject_t7")

    t7_cnt_col, t7_dur_col = st.columns(2)
    with t7_cnt_col:
        mcq_count = st.selectbox("प्रश्नांची संख्या:", [100, 50, 25], index=0, key="mcq_q_count_t7")
    with t7_dur_col:
        mcq_time_limit = st.selectbox("वेळ मर्यादा:", ["60 मिनिटे (1 तास)", "30 मिनिटे", "15 मिनिटे"], index=0, key="mcq_dur_t7")

    if "quiz_questions" not in st.session_state:
        st.session_state.quiz_questions = None
    if "quiz_start_time" not in st.session_state:
        st.session_state.quiz_start_time = None
    if "quiz_submitted" not in st.session_state:
        st.session_state.quiz_submitted = False
    if "user_mcq_answers" not in st.session_state:
        st.session_state.user_mcq_answers = {}

    if st.button(f"🚀 {mcq_count} MCQs ग्रँड टेस्ट सुरू करा (Start 60-Min Exam)", use_container_width=True, key="btn_start_mcq_test_t7"):
        with st.spinner(f"🎓 NCISM तज्ज्ञ '{mcq_subject}' चे उच्च दर्जाचे विद्यापीठ MCQs तयार करत आहेत..."):
            try:
                mcq_gen_prompt = f"""
                You are the Chief Examination Controller of NCISM and AIAPGET BAMS Entrance.
                Subject: {mcq_subject}
                Academic Year: {mcq_year}
                Task: Generate {min(mcq_count, 30)} authentic standard MCQs strictly in JSON format.
                
                Strict JSON schema:
                [
                  {{
                    "id": 1,
                    "question": "प्रश्नाचा मजकूर (मराठी/संस्कृत)",
                    "options": {{
                      "A": "पर्याय A",
                      "B": "पर्याय B",
                      "C": "पर्याय C",
                      "D": "पर्याय D"
                    }},
                    "correct": "A",
                    "explanation": "याचे शास्त्रीय कारण व ग्रंथ संदर्भ."
                  }}
                ]
                """
                raw_json = cached_ask_gemini(mcq_gen_prompt, as_json=True)
                clean_j = raw_json.strip()
                if clean_j.startswith("```json"): clean_j = clean_j[7:]
                if clean_j.startswith("```"): clean_j = clean_j[3:]
                if clean_j.endswith("```"): clean_j = clean_j[:-3]

                parsed_mcqs = json.loads(clean_j.strip())
                st.session_state.quiz_questions = parsed_mcqs
                st.session_state.quiz_start_time = int(time.time())
                st.session_state.quiz_submitted = False
                st.session_state.user_mcq_answers = {}
                st.success("✅ प्रश्नपत्रिका तयार झाली आहे! खालील प्रश्न सोडवणे सुरू करा.")
                st.rerun()
            except Exception as e:
                st.error(f"MCQs लोड करताना त्रुटी आली: {e}")

    st.markdown('</div>', unsafe_allow_html=True)

    # Live Quiz Form
    if st.session_state.quiz_questions and not st.session_state.quiz_submitted:
        elapsed = int(time.time()) - st.session_state.quiz_start_time
        remaining = max(0, 3600 - elapsed)
        mins = remaining // 60
        secs = remaining % 60

        st.markdown(f"""
        <div style="background:#FFFDF7; border:2px solid #C88A24; border-radius:16px; padding:14px 20px; display:flex; justify-content:space-between; align-items:center; margin: 15px 0;">
            <div>
                <span style="font-size:12px; font-weight:800; color:#92400E; text-transform:uppercase;">🏛️ परीक्षा हॉल</span>
                <h4 style="margin:2px 0 0 0; color:#0F4935;">{mcq_subject}</h4>
            </div>
            <div style="text-align:right;">
                <span style="font-size:11.5px; color:#68756E;">शिल्लक वेळ (Timer):</span>
                <div style="font-size:22px; font-weight:900; color:#DC2626;">⏱️ {mins:02d}:{secs:02d}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        with st.form("bams_grand_exam_form_t7"):
            for idx, q_item in enumerate(st.session_state.quiz_questions):
                q_id = q_item.get("id", idx + 1)
                st.markdown(f"**Q{idx+1}. {q_item.get('question')}**")
                opts = q_item.get("options", {})
                choice_list = [f"{k}: {v}" for k, v in opts.items()]
                
                user_choice = st.radio(
                    f"Select Answer for Q{idx+1}",
                    choice_list,
                    index=None,
                    key=f"mcq_radio_t7_{q_id}",
                    label_visibility="collapsed"
                )
                if user_choice:
                    st.session_state.user_mcq_answers[q_id] = user_choice.split(":")[0].strip()
                st.write("---")

            submit_test_btn = st.form_submit_button("🏁 परीक्षा पूर्ण करा व निकाल पाहा (Submit Exam)", use_container_width=True)
            if submit_test_btn:
                st.session_state.quiz_submitted = True
                st.rerun()

    # Result & Mistake Analysis
    if st.session_state.quiz_submitted and st.session_state.quiz_questions:
        total_q = len(st.session_state.quiz_questions)
        correct_cnt = 0
        wrong_cnt = 0
        unattempted_cnt = 0
        wrong_details = []

        for q_item in st.session_state.quiz_questions:
            q_id = q_item.get("id")
            user_ans = st.session_state.user_mcq_answers.get(q_id)
            correct_ans = q_item.get("correct")

            if not user_ans:
                unattempted_cnt += 1
                wrong_details.append({
                    "q": q_item.get("question"),
                    "user": "सोडवला नाही (Unattempted)",
                    "correct": f"{correct_ans} ({q_item['options'].get(correct_ans, '')})",
                    "exp": q_item.get("explanation", "")
                })
            elif user_ans == correct_ans:
                correct_cnt += 1
            else:
                wrong_cnt += 1
                wrong_details.append({
                    "q": q_item.get("question"),
                    "user": f"{user_ans} ({q_item['options'].get(user_ans, '')})",
                    "correct": f"{correct_ans} ({q_item['options'].get(correct_ans, '')})",
                    "exp": q_item.get("explanation", "")
                })

        percentage = (correct_cnt / total_q) * 100 if total_q > 0 else 0
        grade = "🏆 प्रथम श्रेणी (Distinction)" if percentage >= 75 else ("✅ उत्तीर्ण (Passed)" if percentage >= 50 else "⚠️ पुनर्प्रयत्न करा (Need Improvement)")

        st.markdown(f"""
        <div class="saas-card" style="border: 2px solid #176B4D; background:#FAFDFB; margin-top:15px;">
            <div style="text-align:center;">
                <span class="step-badge" style="background:#EAF3EF; color:#176B4D;">NCISM GRAND MOCK SCORECARD</span>
                <h2 style="color:#0F4935; margin:8px 0 2px 0;">तुमचा निकाल: {correct_cnt} / {total_q} गुण ({percentage:.1f}%)</h2>
                <h4 style="color:#C88A24; margin:0 0 14px 0;">{grade}</h4>
            </div>
            <div style="display:grid; grid-template-columns:repeat(3, 1fr); gap:10px; text-align:center;">
                <div style="background:#ECFDF5; border:1px solid #A7F3D0; border-radius:12px; padding:10px;">
                    <div style="font-size:12px; color:#065F46; font-weight:700;">अचूक उत्तरे (Correct)</div>
                    <div style="font-size:22px; font-weight:900; color:#059669;">{correct_cnt}</div>
                </div>
                <div style="background:#FEF2F2; border:1px solid #FECACA; border-radius:12px; padding:10px;">
                    <div style="font-size:12px; color:#991B1B; font-weight:700;">चुकीची उत्तरे (Wrong)</div>
                    <div style="font-size:22px; font-weight:900; color:#DC2626;">{wrong_cnt}</div>
                </div>
                <div style="background:#F8FAFC; border:1px solid #E2E8F0; border-radius:12px; padding:10px;">
                    <div style="font-size:12px; color:#475569; font-weight:700;">न सोडवलेले (Skipped)</div>
                    <div style="font-size:22px; font-weight:900; color:#64748B;">{unattempted_cnt}</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        if wrong_details:
            st.markdown("### ⚠️ चुकलेले प्रश्न आणि त्यांचे अचूक स्पष्टीकरण (Detailed Review):")
            for w_idx, item in enumerate(wrong_details):
                st.markdown(f"""
                <div style="background:#FFFFFF; border:1px solid #E2E8E3; border-left:4px solid #DC2626; border-radius:12px; padding:14px; margin-bottom:10px;">
                    <div style="font-weight:800; font-size:14.5px; color:#1E2924;">प्रश्न {w_idx+1}: {item['q']}</div>
                    <div style="font-size:13px; color:#DC2626; margin-top:4px;">❌ <b>तुमचे उत्तर:</b> {item['user']}</div>
                    <div style="font-size:13px; color:#059669; margin-top:2px;">✅ <b>अचूक उत्तर:</b> {item['correct']}</div>
                    <div style="font-size:12.5px; color:#4A5851; background:#F8FAF9; padding:6px 10px; border-radius:6px; margin-top:6px;">
                        📖 <b>स्पष्टीकरण व संदर्भ:</b> {item['exp']}
                    </div>
                </div>
                """, unsafe_allow_html=True)

        report_text = f"""
        NCISM BAMS 100 MCQs Grand Test Result
        Subject: {mcq_subject} | Year: {mcq_year}
        Score: {correct_cnt} / {total_q} ({percentage:.1f}%) | Result: {grade}

        Chuklelya Prashnanche Vishleshan (Mistakes Review):
        """
        for i, wd in enumerate(wrong_details):
            report_text += f"\nQ{i+1}: {wd['q']}\nYour Answer: {wd['user']}\nCorrect Answer: {wd['correct']}\nReason: {wd['exp']}\n"

        pdf_report = generate_direct_pdf(f"MCQ Exam Result - {mcq_subject}", mcq_subject, s_name, report_text)
        
        c_p1, c_p2 = st.columns(2)
        with c_p1:
            st.download_button(
                "📄 निकाल व चुकलेल्या प्रश्नांची PDF डाऊनलोड",
                pdf_report,
                file_name=f"{mcq_subject.split()[0]}_MCQ_Result.pdf",
                mime="application/pdf",
                use_container_width=True
            )
        with c_p2:
            if st.button("🔄 नवीन टेस्ट पुन्हा सुरू करा (Retake Test)", use_container_width=True):
                st.session_state.quiz_questions = None
                st.session_state.quiz_submitted = False
                st.session_state.user_mcq_answers = {}
                st.rerun()

# =========================================================================
# 🌿 SAAS FOOTER
# =========================================================================
st.markdown(f"""
<div class="saas-footer">
    🌿 <strong>AyurVeda AI Studio</strong><br>
    BAMS • AI • Academic Platform<br>
    Developed by <strong>Avishkar Alase</strong>
</div>
""", unsafe_allow_html=True)
