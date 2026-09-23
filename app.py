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
# 🎯 AUTOMATIC DYNAMIC FESTIVAL THEME ENGINE (SUBTLE ACCENTS ONLY)
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
    story.append(Paragraph("AyurVeda AI Studio - BAMS Academic Notes", header_title_style))
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

    /* Global Foundation */
    html, body, .stApp {{
        background-color: {th['bg']} !important;
        background-image: radial-gradient(at 100% 0%, rgba(23, 107, 77, 0.03) 0px, transparent 50%),
                          radial-gradient(at 0% 100%, rgba(200, 138, 36, 0.03) 0px, transparent 50%) !important;
        font-family: 'Plus Jakarta Sans', 'Mukta', -apple-system, sans-serif !important;
        color: {th['text']} !important;
        -webkit-font-smoothing: antialiased;
    }}

    /* Global Responsive Container */
    .main .block-container {{
        max-width: 1140px !important;
        padding-top: 1.25rem !important;
        padding-bottom: 3.5rem !important;
        padding-left: 1.5rem !important;
        padding-right: 1.5rem !important;
        margin: auto !important;
    }}

    /* Header Nav */
    .saas-navbar {{
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 14px 24px;
        background: rgba(255, 255, 255, 0.92);
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        border: 1px solid {th['border']};
        border-radius: 16px;
        margin-bottom: 20px;
        box-shadow: 0 2px 8px -2px rgba(15, 73, 53, 0.04), 0 1px 2px -1px rgba(0, 0, 0, 0.02);
    }}
    .saas-brand {{
        display: flex;
        align-items: center;
        gap: 12px;
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
        box-shadow: 0 4px 10px -2px rgba(23, 107, 77, 0.25);
    }}
    .brand-title-wrap {{
        display: flex;
        flex-direction: column;
    }}
    .brand-name {{
        font-size: 18px;
        font-weight: 800;
        letter-spacing: -0.02em;
        color: {th['deep_green']};
        margin: 0;
        line-height: 1.2;
    }}
    .brand-sub {{
        font-size: 11px;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.06em;
        color: {th['muted']};
        margin-top: 2px;
    }}
    .author-pill {{
        display: flex;
        align-items: center;
        gap: 8px;
        background: #F0F4F2;
        border: 1px solid #D5E0D9;
        padding: 5px 12px;
        border-radius: 9999px;
        font-size: 12px;
        font-weight: 700;
        color: {th['deep_green']};
    }}
    .author-avatar {{
        width: 20px;
        height: 20px;
        border-radius: 50%;
        background: {th['primary']};
        color: #ffffff;
        display: inline-flex;
        align-items: center;
        justify-content: center;
        font-size: 10px;
        font-weight: 800;
    }}

    /* Welcome Hero Card */
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
    .welcome-meta h2 {{
        font-size: 22px;
        font-weight: 800;
        letter-spacing: -0.02em;
        color: {th['deep_green']} !important;
        margin: 0 0 4px 0 !important;
    }}
    .welcome-meta p {{
        font-size: 13.5px;
        color: {th['muted']} !important;
        margin: 0 !important;
    }}
    .festive-accent-badge {{
        display: inline-flex;
        align-items: center;
        gap: 6px;
        background: {th['accent_badge_bg']};
        border: 1px solid {th['accent_badge_border']};
        color: {th['accent_badge_text']};
        font-size: 11.5px;
        font-weight: 700;
        padding: 4px 10px;
        border-radius: 8px;
        margin-bottom: 6px;
    }}
    .quick-status-grid {{
        display: flex;
        gap: 8px;
        flex-wrap: wrap;
    }}
    .status-chip {{
        display: inline-flex;
        align-items: center;
        gap: 6px;
        background: #F4F6F4;
        border: 1px solid #E2E8E3;
        padding: 6px 12px;
        border-radius: 10px;
        font-size: 12px;
        font-weight: 600;
        color: {th['text']};
    }}

    /* Module Hero Banner */
    .module-hero {{
        background: linear-gradient(135deg, #0F4935 0%, #176B4D 100%);
        color: #FFFFFF !important;
        padding: 22px 26px;
        border-radius: 16px;
        margin-bottom: 20px;
        box-shadow: 0 8px 20px -6px rgba(15, 73, 53, 0.25);
        border: 1px solid rgba(255, 255, 255, 0.12);
        display: flex;
        justify-content: space-between;
        align-items: center;
        flex-wrap: wrap;
        gap: 12px;
    }}
    .module-hero * {{
        color: #FFFFFF !important;
    }}
    .module-hero h3 {{
        margin: 0 0 4px 0 !important;
        font-size: 20px !important;
        font-weight: 800 !important;
        letter-spacing: -0.01em;
    }}
    .module-hero p {{
        margin: 0 !important;
        font-size: 13.5px !important;
        opacity: 0.9;
        font-weight: 400;
    }}
    .module-tag {{
        background: rgba(255, 255, 255, 0.16);
        border: 1px solid rgba(255, 255, 255, 0.28);
        padding: 4px 10px;
        border-radius: 8px;
        font-size: 11.5px;
        font-weight: 700;
        letter-spacing: 0.04em;
    }}

    /* Modern Card Sections */
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
        align-items: center;
        gap: 6px;
        font-size: 11px;
        font-weight: 800;
        letter-spacing: 0.06em;
        text-transform: uppercase;
        color: {th['primary']};
        background: #EAF3EF;
        padding: 3px 9px;
        border-radius: 6px;
        margin-bottom: 12px;
    }}

    /* Reading Experience / Textbook Presentation */
    .textbook-container {{
        background: #FFFFFF;
        border: 1px solid {th['border']};
        border-radius: 18px;
        padding: 36px 40px;
        box-shadow: 0 6px 20px -4px rgba(15, 73, 53, 0.04);
        margin-top: 18px;
        color: #1A2621;
        font-family: 'Mukta', 'Plus Jakarta Sans', serif;
        font-size: 16px;
        line-height: 1.85;
    }}
    .textbook-container h1, .textbook-container h2, .textbook-container h3 {{
        color: {th['deep_green']} !important;
        font-weight: 800 !important;
        letter-spacing: -0.02em;
        margin-top: 1.5em;
        margin-bottom: 0.5em;
        padding-bottom: 6px;
        border-bottom: 1px solid #EBEFEA;
    }}
    .textbook-container blockquote {{
        border-left: 4px solid {th['primary']};
        background: #F4F8F6;
        padding: 14px 20px;
        margin: 18px 0;
        border-radius: 0 12px 12px 0;
        color: {th['deep_green']};
        font-weight: 600;
    }}
    .textbook-container table {{
        width: 100%;
        border-collapse: collapse;
        margin: 20px 0;
        font-size: 14.5px;
    }}
    .textbook-container th, .textbook-container td {{
        border: 1px solid #E2E8E3;
        padding: 10px 14px;
        text-align: left;
    }}
    .textbook-container th {{
        background-color: #F4F7F5;
        color: {th['deep_green']};
        font-weight: 700;
    }}
    .textbook-container tr:nth-child(even) {{
        background-color: #FAFBF9;
    }}

    /* Question & Clinical Presentation Cards */
    .viva-card {{
        background: #FFFFFF;
        border: 1px solid #E2E8E3;
        border-radius: 14px;
        padding: 18px 20px;
        margin-bottom: 14px;
        box-shadow: 0 2px 8px -2px rgba(0, 0, 0, 0.03);
    }}
    .viva-badge {{
        font-size: 11px;
        font-weight: 800;
        color: #C88A24;
        background: #FEF9EE;
        border: 1px solid #FBE6B8;
        padding: 3px 8px;
        border-radius: 6px;
        display: inline-block;
        margin-bottom: 8px;
    }}

    /* Streamlit Tabs Redesign */
    .stTabs [data-baseweb="tab-list"] {{
        gap: 6px;
        background-color: transparent;
        padding: 4px;
        border-bottom: 2px solid #E8ECE8;
        overflow-x: auto;
        white-space: nowrap;
        scrollbar-width: none;
    }}
    .stTabs [data-baseweb="tab-list"]::-webkit-scrollbar {{
        display: none;
    }}
    .stTabs [data-baseweb="tab"] {{
        background-color: transparent !important;
        border: none !important;
        border-bottom: 2px solid transparent !important;
        border-radius: 0px !important;
        padding: 10px 16px !important;
        font-size: 14.5px !important;
        font-weight: 600 !important;
        color: {th['muted']} !important;
        transition: all 0.2s ease !important;
    }}
    .stTabs [aria-selected="true"] {{
        color: {th['primary']} !important;
        border-bottom: 2px solid {th['active_tab_border']} !important;
        font-weight: 700 !important;
    }}

    /* Streamlit Input Components */
    div[data-baseweb="select"] > div,
    div[data-baseweb="input"] > div {{
        background-color: #FFFFFF !important;
        border: 1px solid {th['border']} !important;
        border-radius: 12px !important;
        transition: all 0.2s ease !important;
    }}
    div[data-baseweb="select"] > div:hover,
    div[data-baseweb="input"] > div:hover {{
        border-color: #B5C4BC !important;
    }}
    div[data-baseweb="select"] > div:focus-within,
    div[data-baseweb="input"] > div:focus-within {{
        border-color: {th['primary']} !important;
        box-shadow: 0 0 0 3px rgba(23, 107, 77, 0.1) !important;
    }}

    /* Streamlit Button System */
    div.stButton > button {{
        background: {th['primary']} !important;
        color: #FFFFFF !important;
        border: 1px solid {th['primary']} !important;
        border-radius: 12px !important;
        padding: 10px 22px !important;
        font-size: 14.5px !important;
        font-weight: 600 !important;
        letter-spacing: -0.01em !important;
        transition: all 0.2s ease !important;
        box-shadow: 0 2px 6px -1px rgba(23, 107, 77, 0.25) !important;
    }}
    div.stButton > button:hover {{
        background: {th['deep_green']} !important;
        border-color: {th['deep_green']} !important;
        transform: translateY(-1px);
        box-shadow: 0 4px 12px -2px rgba(23, 107, 77, 0.3) !important;
    }}

    /* Sidebar Clean Polish */
    [data-testid="stSidebar"] {{
        background-color: #FFFFFF !important;
        border-right: 1px solid {th['border']} !important;
    }}
    .sidebar-profile-card {{
        background: #F9FAF8;
        border: 1px solid #E6ECE8;
        border-radius: 14px;
        padding: 16px;
        margin-bottom: 18px;
    }}
    .sidebar-user-header {{
        display: flex;
        align-items: center;
        gap: 12px;
        margin-bottom: 10px;
    }}
    .sidebar-avatar {{
        width: 36px;
        height: 36px;
        border-radius: 50%;
        background: linear-gradient(135deg, #176B4D 0%, #0F4935 100%);
        color: #ffffff;
        font-weight: 800;
        font-size: 13px;
        display: flex;
        align-items: center;
        justify-content: center;
    }}
    .sidebar-saved-card {{
        background: #FFFFFF;
        border: 1px solid #E5ECE7;
        border-radius: 10px;
        padding: 10px 12px;
        margin-bottom: 8px;
        transition: all 0.15s ease;
    }}
    .sidebar-saved-card:hover {{
        border-color: {th['primary']};
    }}

    /* Minimalist Footer */
    .saas-footer {{
        text-align: center;
        padding: 24px 12px 10px 12px;
        font-size: 12.5px;
        color: {th['muted']};
        border-top: 1px solid {th['border']};
        margin-top: 40px;
    }}

    /* Mobile Responsive Polish */
    @media (max-width: 768px) {{
        .main .block-container {{
            padding-left: 1rem !important;
            padding-right: 1rem !important;
            padding-top: 0.75rem !important;
        }}
        .saas-navbar {{
            padding: 10px 14px;
        }}
        .dashboard-welcome {{
            padding: 16px 18px;
        }}
        .textbook-container {{
            padding: 20px 18px;
        }}
        .module-hero {{
            padding: 16px 18px;
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
# 🔄 30-MINUTE SESSION PERSISTENCE ENGINE (No logout on refresh)
# =========================================================================
SESSION_TIMEOUT = 1800  # 30 minutes in seconds
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
        <div class="author-pill">
            <span class="author-avatar">AA</span>
            <span>Avishkar Alase ✓</span>
        </div>
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
                NCISM syllabus, A4 handwritten notes, exam question banks and clinical suite.
            </p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown('<div class="saas-card">', unsafe_allow_html=True)
        t_login, t_reg = st.tabs(["🔑 विद्यार्थी लॉगिन (Sign In)", "✨ नवीन नोंदणी (Student Register)"])

        with t_login:
            st.markdown(f"<div style='font-size: 15px; font-weight: 700; color: {th['deep_green']}; margin-bottom: 12px;'>खात्यात प्रवेश करा:</div>", unsafe_allow_html=True)
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
            st.markdown(f"<div style='font-size: 15px; font-weight: 700; color: {th['deep_green']}; margin-bottom: 12px;'>विद्यार्थी नोंदणी फॉर्म:</div>", unsafe_allow_html=True)
            r_name = st.text_input("👤 विद्यार्थ्याचे पूर्ण नाव:", placeholder="उदा. राहुल प्रकाश जोशी")
            
            c_mob, c_age = st.columns([2, 1])
            with c_mob:
                r_mob = st.text_input("📱 मोबाईल नंबर:", placeholder="9876543210", max_chars=10)
            with c_age:
                r_age = st.number_input("वय (Age):", min_value=17, max_value=60, value=22)

            r_col = st.text_input("🏛️ BAMS कॉलेजचे नाव:", placeholder="उदा. Government Ayurved College, Nanded")
            r_yr = st.selectbox(
                "🎓 BAMS वर्ष:",
                ["BAMS 1st Professional (प्रथम वर्ष)", "BAMS 2nd Professional (द्वितीय वर्ष)", "BAMS 3rd Professional (तृतीय वर्ष)", "BAMS Final Professional (अंतिम वर्ष)", "BAMS Intern (इंटर्नशिप)"]
            )
            r_em = st.text_input("📧 ईमेल पत्ता:", placeholder="student@gmail.com", key="auth_reg_em")
            r_pw = st.text_input("🔒 पासवर्ड (किमान ६ अक्षरे/अंक):", type="password", key="auth_reg_pw")

            if st.button("✨ खाते तयार करा व VIP स्टुडिओ सुरू करा", use_container_width=True, key="btn_r_submit"):
                if not r_name.strip() or not r_col.strip() or not r_em.strip() or len(r_pw.strip()) < 6:
                    st.warning("कृपया सर्व आवश्यक माहिती आणि किमान ६ अक्षरांचा पासवर्ड भरा.")
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

    st.markdown(f"""
    <div class="saas-footer">
        {th['footer_text']} • <strong>AyurVeda AI Studio</strong> • BAMS Academic Platform • Developed by <strong>Avishkar Alase</strong>
    </div>
    """, unsafe_allow_html=True)
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
# 👤 SIDEBAR - COMPACT IDENTITY CARD & SAVED NOTES
# =========================================================================
prof = st.session_state.profile or {}
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
        <div class="sidebar-user-header">
            <div class="sidebar-avatar">{initials}</div>
            <div style="overflow: hidden;">
                <div style="font-weight: 800; font-size: 15px; color: {th['deep_green']}; text-overflow: ellipsis; white-space: nowrap; overflow: hidden;">{s_name}</div>
                <div style="font-size: 11.5px; color: {th['muted']}; font-weight: 600;">{s_year}</div>
            </div>
        </div>
        <div style="font-size: 12px; color: {th['text']}; line-height: 1.5; border-top: 1px solid #E5ECE7; padding-top: 8px;">
            <div>🏛️ <b>कॉलेज:</b> {s_college}</div>
            <div style="display: flex; gap: 8px; margin-top: 2px;">
                <span>📱 {s_mob}</span>
                <span>• वय: {s_age}</span>
            </div>
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
    <div class="author-pill">
        <span class="author-avatar">AA</span>
        <span>Avishkar Alase ✓</span>
    </div>
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
        <span class="status-chip">🎓 Exam</span>
    </div>
</div>
""", unsafe_allow_html=True)

# 6 Navigation Tabs (Including University Mock Exam)
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "📖 Study",
    "🧪 Medicine",
    "🎯 Viva",
    "🩺 Clinical",
    "🔬 Research",
    "🎓 University Exam"
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
        bams_year = st.selectbox(
            "BAMS वर्ष निवडा:",
            [
                "BAMS 1st Professional (प्रथम वर्ष)",
                "BAMS 2nd Professional (द्वितीय वर्ष)",
                "BAMS 3rd Professional (तृतीय वर्ष)",
                "BAMS Final Professional (अंतिम वर्ष)"
            ]
        )
    with c2:
        st.markdown('<div class="step-pill">STEP 02 • 📚 Subject</div>', unsafe_allow_html=True)
        subject = st.selectbox(
            "विषय निवडा:",
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
        language_preference = st.radio(
            "माध्यम निवडा:",
            [
                "🚩 मराठी (संस्कृत + अर्थ)",
                "🌿 Simple English + Sanskrit"
            ],
            horizontal=True
        )

    st.markdown('<div class="step-pill">STEP 05 • 🔍 Topic</div>', unsafe_allow_html=True)
    topic = st.text_input(
        "अभ्यासाचा विषय / प्रश्न प्रविष्ट करा:",
        placeholder="उदा. Virya, Ojas, Pitta Dosha, Rakta Dhatu, Ashwagandha, Agada"
    )

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
                lang_rule = "Write in natural, simple spoken Marathi with Sanskrit terms and simple English in parentheses." if is_marathi else "Write 100% in pure English Roman script. All titles and terms in English."
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

                Format with bold headings, clean bullet points, and high readability.
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

                1. 📜 व्युत्पत्ती, निरुक्ती व श्लोक अन्वय (Mukhya Sanskrit Shloka > blockquote madhye reference granthasaha).
                2. 🔬 व्याख्या व स्वरूप (Comprehensive Definition & Essential Characteristics).
                3. 🌱 उत्पत्ती व निर्मिती प्रक्रिया (Origin & Formation Process).
                4. 📍 स्थान व आश्रय (Physiological Seats & Distribution).
                5. ⚗️ गुणधर्म व भौतिक लक्षणे (Specific Attributes, Guna, Virya, Vipaka, Prabhava).
                6. ⚙️ प्राकृत कर्मे व कार्यपद्धती (Normal Physiological Functions with Clinical Examples).
                7. 📏 प्रमाण व परीक्षण पद्धती (Anjali Pramana, Clinical Dosage).
                8. ⚠️ विकृती, क्षय व वृद्धी लक्षणे (Pathological States).
                9. 🔗 संबंधित संकल्पनांशी तुलना (Differential Diagnosis Table).
                10. 🏥 आधुनिक विज्ञानाशी सांगड (Modern Physiology, Biochemistry Correlation).
                11. 💊 चिकित्सा व औषधीय महत्त्व (Clinical Application, Prime Formulations).
                12. ⭐ High-Yield Points & Memory Mnemonics.
                13. 🎯 PG AIAPGET Special Focus.
                14. 📝 संभाव्य परीक्षा प्रश्नसंच (NCISM Pattern: 1 LAQ, 2 SAQ, 4 MCQs).
                15. 📊 Master Summary Table.
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
            <div style="font-size: 11px; font-weight: 800; color: {th['primary']}; text-transform: uppercase; letter-spacing: 0.05em;">📚 Generated Study Notes</div>
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
            # 🎯 DIRECT REPORTLAB PDF GENERATION & DOWNLOAD
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
        dosage_form = st.selectbox(
            "औषधाचा प्रकार (Dosage Form):",
            ["Vati / Gutika (गोळी / वटी)", "Churna (चूर्ण)", "Asava & Arishta (आसव व अरिष्ट)", "Taila / Ghrita (सिद्ध तेल व घृत)", "Bhasma & Pishti (भस्म व पिष्टी)"]
        )
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
        viva_sub = st.selectbox(
            "Viva साठी विषय:",
            ["Kriya Sharir", "Rachana Sharir", "Dravyaguna", "Rasa Shastra", "Agada Tantra", "Kayachikitsa", "Shalya Tantra"],
            key="viva_sub"
        )
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
                    """
                    viva_res = cached_ask_gemini(viva_prompt, as_json=False)
                    st.session_state.current_viva_note = viva_res
                except Exception as e:
                    st.error(f"त्रुटी: {e}")
    st.markdown('</div>', unsafe_allow_html=True)

    if st.session_state.current_viva_note:
        v_raw = st.session_state.current_viva_note
        q_blocks = re.split(r'\n(?=[0-9]+\.|\*\*Question|\* \*\*|\bQuestion [0-9]+:)', v_raw)
        
        st.markdown("#### 📋 Examiner Questions & Evaluation")
        if len(q_blocks) > 1:
            for idx, block in enumerate(q_blocks):
                cleaned_block = block.strip()
                if not cleaned_block:
                    continue
                st.markdown(f"""
                <div class="viva-card">
                    <span class="viva-badge">QUESTION {idx+1:02d}</span>
                </div>
                """, unsafe_allow_html=True)
                lines = cleaned_block.split("\n", 1)
                st.markdown(f"**{lines[0].replace('**', '')}**")
                if len(lines) > 1:
                    with st.expander("View Model Answer"):
                        st.markdown(lines[1])
        else:
            st.markdown(f'<div class="textbook-container">{v_raw}</div>', unsafe_allow_html=True)

        v_c1, v_c2 = st.columns(2)
        with v_c1:
            if st.button("💾 Save Viva Set to Notes", key="save_viva_btn", use_container_width=True):
                try:
                    supabase.table("user_notes").insert({
                        "user_id": st.session_state.user_id,
                        "subject": viva_sub,
                        "topic": viva_topic,
                        "study_mode": "Viva-Voce Questions",
                        "content": st.session_state.current_viva_note
                    }).execute()
                    st.success("✅ खात्यात सेव्ह झाले!")
                    time.sleep(0.8)
                    st.rerun()
                except Exception as e:
                    st.error(f"त्रुटी: {e}")
        with v_c2:
            v_pdf = generate_direct_pdf(viva_topic, viva_sub, s_name, st.session_state.current_viva_note)
            st.download_button("📄 Viva PDF डाउनलोड करा", v_pdf, file_name=f"{viva_topic}_Viva.pdf", mime="application/pdf", use_container_width=True)

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
        case_subject = st.selectbox(
            "क्लिनिकल विभाग (Department):",
            ["Kayachikitsa (कायचिकित्सा)", "Panchakarma (पंचकर्म)", "Shalya Tantra (शल्य)", "Shalakya (नेत्र/कर्ण/नासा)", "Stri Roga & Prasuti (स्त्रीरोग)", "Kaumarbhritya (बालरोग)"],
            key="case_sub"
        )
    with c_col2:
        st.markdown('<div class="step-pill">Language</div>', unsafe_allow_html=True)
        case_lang = st.radio("भाषा निवडा:", ["मराठी + Clinical English", "Simple Indian English + Sanskrit"], horizontal=True, key="cs_lang")

    st.markdown('<div class="step-pill">Disease / Symptoms</div>', unsafe_allow_html=True)
    case_topic = st.text_input("आजाराचे नाव / मुख्य लक्षणे प्रविष्ट करा:", placeholder="उदा. Amlapitta (GERD), Sandhivata (Osteoarthritis), Tamaka Shwasa (Asthma)", key="cs_top")

    if "current_case_note" not in st.session_state:
        st.session_state.current_case_note = None

    if st.button("📋 Generate Case Sheet", key="btn_case", use_container_width=True):
        if not case_topic.strip():
            st.warning("⚠️ कृपया आजाराचे नाव टाका.")
        else:
            with st.spinner("🩺 Preparing clinical case presentation..."):
                try:
                    case_prompt = f"""
                    You are a Chief Clinical Physician and BAMS PG Guide in an Ayurvedic Hospital.
                    Department: {case_subject}
                    Disease/Condition: {case_topic}
                    Language: {case_lang}

                    Generate a complete, professional Ayurvedic Clinical Case Presentation Paper.
                    """
                    case_res = cached_ask_gemini(case_prompt, as_json=False)
                    st.session_state.current_case_note = case_res
                except Exception as e:
                    st.error(f"त्रुटी: {e}")
    st.markdown('</div>', unsafe_allow_html=True)

    if st.session_state.current_case_note:
        st.markdown(f'<div class="textbook-container">{st.session_state.current_case_note}</div>', unsafe_allow_html=True)
        
        cs_c1, cs_c2 = st.columns(2)
        with cs_c1:
            if st.button("💾 Save Case Presentation to Notes", key="save_case_btn", use_container_width=True):
                try:
                    supabase.table("user_notes").insert({
                        "user_id": st.session_state.user_id,
                        "subject": case_subject,
                        "topic": case_topic,
                        "study_mode": "Clinical Case Study",
                        "content": st.session_state.current_case_note
                    }).execute()
                    st.success("✅ खात्यात सेव्ह झाले!")
                    time.sleep(0.8)
                    st.rerun()
                except Exception as e:
                    st.error(f"त्रुटी: {e}")
        with cs_c2:
            cs_pdf = generate_direct_pdf(case_topic, case_subject, s_name, st.session_state.current_case_note)
            st.download_button("📄 Case Sheet PDF डाउनलोड करा", cs_pdf, file_name=f"{case_topic}_Case_Sheet.pdf", mime="application/pdf", use_container_width=True)

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
    res_topic = st.text_input("औषधी वनस्पती किंवा सक्रिय घटक:", placeholder="उदा. Withania somnifera (Ashwagandha), Tinospora cordifolia (Guduchi), Curcumin", key="res_top")

    if "current_res_note" not in st.session_state:
        st.session_state.current_res_note = None

    if st.button("🧬 Generate Research Summary", key="btn_research", use_container_width=True):
        if not res_topic.strip():
            st.warning("⚠️ कृपया संशोधन द्रव्याचे नाव टाका.")
        else:
            with st.spinner("🔬 Analyzing available evidence..."):
                try:
                    res_prompt = f"""
                    You are a Lead Scientist in Ayurvedic Reverse Pharmacology.
                    Drug/Herb: {res_topic}
                    Generate an authentic research summary with Phytochemicals, Mechanism, and Clinical trials.
                    """
                    res_out = cached_ask_gemini(res_prompt, as_json=False)
                    st.session_state.current_res_note = res_out
                except Exception as e:
                    st.error(f"त्रुटी: {e}")
    st.markdown('</div>', unsafe_allow_html=True)

    if st.session_state.current_res_note:
        st.markdown(f'<div class="textbook-container">{st.session_state.current_res_note}</div>', unsafe_allow_html=True)
        
        r_c1, r_c2 = st.columns(2)
        with r_c1:
            if st.button("💾 Save Research Report to Notes", key="save_res_btn", use_container_width=True):
                try:
                    supabase.table("user_notes").insert({
                        "user_id": st.session_state.user_id,
                        "subject": "Research & Evidence",
                        "topic": res_topic,
                        "study_mode": "Modern Pharmacology",
                        "content": st.session_state.current_res_note
                    }).execute()
                    st.success("✅ खात्यात सेव्ह झाले!")
                    time.sleep(0.8)
                    st.rerun()
                except Exception as e:
                    st.error(f"त्रुटी: {e}")
        with r_c2:
            r_pdf = generate_direct_pdf(res_topic, "Research", s_name, st.session_state.current_res_note)
            st.download_button("📄 Research PDF डाउनलोड करा", r_pdf, file_name=f"{res_topic}_Research.pdf", mime="application/pdf", use_container_width=True)

# =========================================================================
# 🎓 TAB 6: UNIVERSITY MOCK EXAM SIMULATOR (NEW FEATURE)
# =========================================================================
with tab6:
    st.markdown("""
    <div class="module-hero">
        <div>
            <h3>🎓 University Mock Exam Simulator</h3>
            <p>MUHS व NCISM पॅटर्ननुसार प्रश्नपत्रिका सोडवा आणि AI Chief Examiner कडून पेपर तपासून घ्या.</p>
        </div>
        <div class="module-tag">EXAM HALL SIMULATOR</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="saas-card">', unsafe_allow_html=True)
    ex_c1, ex_c2 = st.columns(2)
    with ex_c1:
        st.markdown('<div class="step-pill">Subject</div>', unsafe_allow_html=True)
        exam_subject = st.selectbox(
            "परीक्षेचा विषय निवडा:",
            [
                "Kriya Sharir (क्रिया शारीर)", "Rachana Sharir (रचना शारीर)", "Dravyaguna Vijnana (द्रव्यगुण विज्ञान)",
                "Rasashastra & Bhaishajya Kalpana", "Roga Nidan (रोगनिदान)", "Kayachikitsa (कायचिकित्सा)",
                "Shalya Tantra (शल्य तंत्र)", "Agada Tantra (अगद तंत्र)"
            ],
            key="exam_sub_select"
        )
    with ex_c2:
        st.markdown('<div class="step-pill">Exam Pattern</div>', unsafe_allow_html=True)
        exam_pattern = st.selectbox(
            "परीक्षेचा पॅटर्न निवडा:",
            [
                "NCISM Full Standard Paper (MCQ + SAQ + LAQ)",
                "Section B & C Focus (SAQ + LAQ - Theory Intensive)",
                "Rapid Prelim Test (5 SAQ - 25 Marks)"
            ],
            key="exam_pattern_select"
        )

    st.markdown('<div class="step-pill">Chapters / Specific Topics</div>', unsafe_allow_html=True)
    exam_chapters = st.text_input("कोणत्या चॅप्टर्सवर परीक्षा हवी आहे? (रिकामे ठेवल्यास संपूर्ण अभ्यासक्रम):", placeholder="उदा. Dosha Dhatu Mala, Virya Vipaka, Pitta Prakopa, Agada", key="exam_chap_input")

    if "exam_paper_data" not in st.session_state:
        st.session_state.exam_paper_data = None
    if "exam_eval_data" not in st.session_state:
        st.session_state.exam_eval_data = None

    if st.button("📝 प्रश्नपत्रिका तयार करा (Generate Exam Paper)", key="btn_gen_exam_tab6", use_container_width=True):
        with st.spinner("🎓 NCISM Chief Examiner विद्यापीठ प्रश्नपत्रिका तयार करत आहेत..."):
            try:
                exam_prompt = f"""
                You are a Chief Paper Setter and Examiner for NCISM / MUHS University BAMS Examinations.
                Subject: {exam_subject}
                Pattern: {exam_pattern}
                Focus Syllabus: {exam_chapters if exam_chapters.strip() else 'Entire Standard Syllabus'}

                Generate an authentic, high-yield university question paper in Marathi and Sanskrit terminology matching this structure:
                1. 🏛️ UNIVERSITY EXAM HEADER (Subject, Time Allowed, Max Marks)
                2. 📜 SECTION A: 5 High-Yield MCQs (Multiple Choice Questions with options)
                3. ✍️ SECTION B: Short Answer Questions (SAQ - 5 Marks each)
                4. 🎯 SECTION C: Long Answer Questions (LAQ - 10 Marks each with Shloka citation expectations)

                Format with clear bold headings, instructions, and standard university grading scheme.
                """
                st.session_state.exam_paper_data = cached_ask_gemini(exam_prompt, as_json=False)
            except Exception as e:
                st.error(f"त्रुटी: {e}")

    st.markdown('</div>', unsafe_allow_html=True)

    if st.session_state.exam_paper_data:
        st.markdown(f'<div class="textbook-container">{st.session_state.exam_paper_data}</div>', unsafe_allow_html=True)

        # PDF Download of Generated Question Paper
        qp_pdf = generate_direct_pdf(f"University Exam - {exam_subject}", exam_subject, s_name, st.session_state.exam_paper_data)
        st.download_button(
            label="📄 प्रश्नपत्रिका PDF डाउनलोड करा",
            data=qp_pdf,
            file_name=f"{exam_subject.split()[0]}_Question_Paper.pdf",
            mime="application/pdf",
            use_container_width=True
        )

        # Student Answer Paper Submission & Evaluation Section
        st.markdown('<div class="saas-card" style="margin-top:20px;">', unsafe_allow_html=True)
        st.markdown("#### ✍️ तुमचे उत्तर तपासा (AI Chief Examiner Evaluation)")
        student_answer = st.text_area(
            "तुमचे उत्तर किंवा महत्त्वाचे मुद्दे येथे लिहा (किंवा टाइप करा):",
            placeholder="उदा. प्रश्न क्रमांक १ चे उत्तर: श्लोक, संप्राप्ती घटक, प्राकृत कर्मे आणि चिकित्सा सूत्र...",
            height=160,
            key="student_exam_ans_input"
        )

        if st.button("🎯 पेपर तपासा आणि गुण द्या (Evaluate My Answer)", use_container_width=True, key="btn_eval_paper_tab6"):
            if not student_answer.strip():
                st.warning("⚠️ कृपया तपासण्यासाठी तुमचे उत्तर टाइप करा.")
            else:
                with st.spinner("👨‍🏫 AI Chief Examiner तुमचे उत्तर तपासून गुण देत आहेत..."):
                    try:
                        eval_prompt = f"""
                        You are a Senior BAMS University Chief Examiner evaluating a student's answer paper.
                        Subject: {exam_subject}
                        Exam Paper Snippet: {st.session_state.exam_paper_data[:500]}
                        Student's Written Answer:
                        {student_answer}

                        Perform a strict and rigorous evaluation based on NCISM criteria:
                        1. 🎯 मिळालेले एकूण गुण (Marks Awarded out of 10 or 20)
                        2. ✅ उत्तरातील अचूक मुद्दे व जमेची बाजू (Strengths)
                        3. ⚠️ सुटलेले महत्त्वाचे श्लोक / संदर्भ / अन्वय (Missing Shlokas & References)
                        4. 💡 10 पैकी 10 गुण मिळवण्यासाठी काय सुधारणा करावी (Examiner's Expert Tips)
                        5. 🌟 परिपूर्ण उत्तराचा आदर्श आराखडा (Model Answer Blueprint)

                        Respond in clear, constructive, and motivating Marathi with Sanskrit medical terms.
                        """
                        st.session_state.exam_eval_data = cached_ask_gemini(eval_prompt, as_json=False)
                    except Exception as e:
                        st.error(f"त्रुटी: {e}")

        st.markdown('</div>', unsafe_allow_html=True)

        if st.session_state.exam_eval_data:
            st.markdown(f"""
            <div class="textbook-container" style="border-left: 5px solid #C88A24;">
                <h3 style="color:#92400E; margin-top:0;">🏆 Examiner's Marksheet & Feedback</h3>
                {st.session_state.exam_eval_data}
            </div>
            """, unsafe_allow_html=True)

            eval_pdf = generate_direct_pdf(f"Evaluation - {exam_subject}", exam_subject, s_name, st.session_state.exam_eval_data)
            st.download_button(
                label="📄 निकाल व गुणपत्रिका PDF डाउनलोड करा",
                data=eval_pdf,
                file_name=f"{exam_subject.split()[0]}_Marksheet.pdf",
                mime="application/pdf",
                use_container_width=True
            )

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
