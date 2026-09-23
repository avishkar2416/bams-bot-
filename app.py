import streamlit as st
from google import genai
from google.genai import types
import json
import time
import urllib.parse
from datetime import datetime
import re
import html
import markdown
from supabase import create_client, Client

# =========================================================================
# ⚙️ PAGE CONFIGURATION
# =========================================================================
st.set_page_config(
    page_title="AyurVeda AI Studio | BAMS Smart Academic Platform",
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
# 🎨 HIGH-FIDELITY CSS - SCREENSHOT REPLICATION
# =========================================================================
st.markdown(f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=Mukta:wght@400;500;600;700;800&display=swap');

    /* Reset & Viewport Constraints */
    html, body, .stApp {{
        background-color: #F6F8F5 !important;
        background-image: radial-gradient(at 100% 0%, rgba(23, 107, 77, 0.02) 0px, transparent 50%),
                          radial-gradient(at 0% 100%, rgba(200, 138, 36, 0.02) 0px, transparent 50%) !important;
        font-family: 'Plus Jakarta Sans', 'Mukta', -apple-system, sans-serif !important;
        color: #1E2924 !important;
        -webkit-font-smoothing: antialiased;
    }}

    /* Global Container Width */
    .main .block-container {{
        max-width: 820px !important;
        margin: 0 auto !important;
        padding-top: 0.6rem !important;
        padding-bottom: 5.5rem !important; /* Space for sticky bottom bar */
        padding-left: 1rem !important;
        padding-right: 1rem !important;
    }}

    /* Hide standard Streamlit header & decorative elements */
    header[data-testid="stHeader"] {{
        background-color: transparent !important;
        z-index: 10 !important;
    }}
    footer {{
        display: none !important;
    }}
    div[data-testid="stToolbar"] {{
        display: none !important;
    }}

    /* --- 1. TOP HEADER --- */
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
        cursor: pointer;
        display: flex;
        align-items: center;
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
        letter-spacing: -0.01em;
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
    .icon-action-btn {{
        font-size: 18px;
        color: #4A5851;
        cursor: pointer;
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
        letter-spacing: 0.5px;
    }}

    /* --- 2. WELCOME CARD --- */
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
        display: flex;
        align-items: center;
        gap: 4px;
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
        margin-top: 2px;
    }}
    .welcome-right-badge {{
        background: #F1F6F2;
        border: 1px solid #DFECE3;
        border-radius: 16px;
        padding: 8px 12px;
        display: flex;
        align-items: center;
        gap: 8px;
        position: relative;
        overflow: hidden;
    }}
    .badge-icon {{
        font-size: 16px;
    }}
    .badge-content {{
        display: flex;
        flex-direction: column;
    }}
    .badge-title {{
        font-size: 12px;
        font-weight: 700;
        color: #0F4935;
        line-height: 1.2;
    }}
    .badge-desc {{
        font-size: 10px;
        font-style: italic;
        color: #436957;
        line-height: 1.2;
    }}
    .badge-leaf-bg {{
        font-size: 26px;
        opacity: 0.7;
        margin-left: 2px;
    }}

    /* --- 3. FESTIVAL STRIP --- */
    .festival-strip {{
        background: #FFFDF7;
        border: 1px solid #F6E6C5;
        border-radius: 18px;
        padding: 10px 16px;
        display: flex;
        align-items: center;
        justify-content: space-between;
        margin-bottom: 14px;
        box-shadow: 0 2px 8px rgba(200, 138, 36, 0.04);
    }}
    .festival-strip-left {{
        display: flex;
        align-items: center;
        gap: 12px;
    }}
    .festival-lamp {{
        font-size: 24px;
        background: #FEF3C7;
        border-radius: 12px;
        padding: 4px 8px;
    }}
    .festival-text {{
        display: flex;
        flex-direction: column;
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
    .festival-arrow {{
        font-size: 14px;
        color: #92400E;
        font-weight: 700;
    }}

    /* --- 4. FEATURE NAVIGATION BUTTONS (COLUMNS MATCHING SCREENSHOT) --- */
    div[data-testid="stHorizontalBlock"]:has(button[key^="nav_btn_"]) {{
        gap: 8px !important;
        margin-bottom: 14px !important;
    }}
    button[key^="nav_btn_"] {{
        background: #FFFFFF !important;
        color: #1E2924 !important;
        border: 1px solid #E5E9E4 !important;
        border-radius: 16px !important;
        padding: 10px 4px !important;
        height: 72px !important;
        box-shadow: 0 2px 6px rgba(0,0,0,0.03) !important;
        display: flex !important;
        flex-direction: column !important;
        align-items: center !important;
        justify-content: center !important;
        transition: all 0.15s ease !important;
    }}
    button[key^="nav_btn_"]:hover {{
        border-color: #176B4D !important;
        transform: translateY(-2px);
    }}
    button[key^="nav_btn_active_"] {{
        background: #0F4935 !important;
        color: #FFFFFF !important;
        border: 1px solid #0F4935 !important;
        border-radius: 16px !important;
        padding: 10px 4px !important;
        height: 72px !important;
        box-shadow: 0 4px 12px rgba(15, 73, 53, 0.25) !important;
        display: flex !important;
        flex-direction: column !important;
        align-items: center !important;
        justify-content: center !important;
    }}
    button[key^="nav_btn_active_"] p, button[key^="nav_btn_active_"] div {{
        color: #FFFFFF !important;
        font-weight: 800 !important;
    }}

    /* --- 5. HERO CARD (BAMS STUDY STUDIO) --- */
    .hero-card {{
        background: linear-gradient(135deg, #093727 0%, #0F4935 60%, #176B4D 100%);
        border-radius: 22px;
        padding: 20px 22px;
        color: #FFFFFF;
        position: relative;
        overflow: hidden;
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
        letter-spacing: 0.05em;
        margin-bottom: 8px;
        color: #E2ECE6;
    }}
    .hero-title-row {{
        display: flex;
        justify-content: space-between;
        align-items: flex-start;
        gap: 10px;
    }}
    .hero-main-title {{
        font-size: 24px;
        font-weight: 800;
        line-height: 1.15;
        letter-spacing: -0.02em;
        margin: 0;
        color: #FFFFFF;
    }}
    .hero-main-title span {{
        color: #E8C172;
    }}
    .hero-desc {{
        font-size: 12.5px;
        color: #E0EAE4;
        line-height: 1.45;
        margin: 6px 0 16px 0;
        max-width: 75%;
    }}
    .hero-book-stack {{
        display: flex;
        flex-direction: column;
        gap: 3px;
        align-items: flex-end;
    }}
    .book-spine {{
        background: #5E3A20;
        border-left: 3px solid #E8C172;
        color: #FFFFFF;
        font-size: 9.5px;
        font-weight: 700;
        padding: 3px 8px;
        border-radius: 2px 4px 4px 2px;
        width: 82px;
        text-align: center;
        box-shadow: 1px 2px 5px rgba(0,0,0,0.3);
    }}
    .hero-benefits-grid {{
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 8px;
        border-top: 1px solid rgba(255, 255, 255, 0.15);
        padding-top: 14px;
    }}
    .hero-benefit-item {{
        display: flex;
        flex-direction: column;
        gap: 4px;
    }}
    .benefit-icon-badge {{
        width: 28px;
        height: 28px;
        border-radius: 8px;
        background: rgba(255, 255, 255, 0.15);
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 14px;
    }}
    .benefit-label {{
        font-size: 10.5px;
        line-height: 1.25;
        font-weight: 600;
        color: #F1F6F3;
    }}

    /* --- 6. STUDY NOTE CREATION CARD --- */
    .study-form-card {{
        background: #FFFFFF;
        border: 1px solid #EBEFEA;
        border-radius: 22px;
        padding: 22px;
        box-shadow: 0 4px 16px rgba(15, 73, 53, 0.04);
        margin-bottom: 16px;
    }}
    .card-header-row {{
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 16px;
        border-bottom: 1px solid #F1F4F0;
        padding-bottom: 12px;
    }}
    .card-header-left {{
        display: flex;
        align-items: center;
        gap: 8px;
        font-size: 18px;
        font-weight: 800;
        color: #0F4935;
    }}
    .step-indicator-pill {{
        background: #F3F6F3;
        border: 1px solid #E2E8E3;
        border-radius: 12px;
        padding: 4px 10px;
        font-size: 11.5px;
        font-weight: 700;
        color: #4A5851;
        display: flex;
        align-items: center;
        gap: 6px;
    }}
    .step-dots {{
        color: #176B4D;
        font-size: 10px;
        letter-spacing: 2px;
    }}

    .step-title-row {{
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-top: 14px;
        margin-bottom: 4px;
    }}
    .step-num-title {{
        display: flex;
        align-items: center;
        gap: 8px;
        font-size: 14.5px;
        font-weight: 700;
        color: #0F4935;
    }}
    .step-badge {{
        background: #E8F2EC;
        color: #0F4935;
        font-size: 11px;
        font-weight: 800;
        padding: 2px 6px;
        border-radius: 6px;
    }}
    .step-meta-hint {{
        font-size: 11.5px;
        color: #68756E;
        font-weight: 500;
    }}

    /* Custom Study Mode Selectable Grid Buttons */
    div[data-testid="stHorizontalBlock"]:has(button[key^="mode_sel_"]) {{
        gap: 8px !important;
        margin-top: 6px !important;
        margin-bottom: 10px !important;
    }}
    button[key^="mode_sel_"] {{
        background: #FFFFFF !important;
        color: #1E2924 !important;
        border: 1px solid #E5E9E4 !important;
        border-radius: 14px !important;
        padding: 12px 10px !important;
        height: 62px !important;
        font-size: 12.5px !important;
        font-weight: 700 !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        text-align: center !important;
        line-height: 1.25 !important;
        box-shadow: 0 1px 4px rgba(0,0,0,0.02) !important;
    }}
    button[key^="mode_sel_active_"] {{
        background: #F2F8F4 !important;
        color: #0F4935 !important;
        border: 1.8px solid #176B4D !important;
        border-radius: 14px !important;
        padding: 12px 10px !important;
        height: 62px !important;
        font-size: 12.5px !important;
        font-weight: 800 !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        text-align: center !important;
        line-height: 1.25 !important;
        box-shadow: 0 2px 8px rgba(23, 107, 77, 0.12) !important;
    }}

    /* Custom Language Selectable Grid Buttons */
    div[data-testid="stHorizontalBlock"]:has(button[key^="lang_sel_"]) {{
        gap: 8px !important;
        margin-top: 6px !important;
        margin-bottom: 10px !important;
    }}
    button[key^="lang_sel_"] {{
        background: #FFFFFF !important;
        color: #1E2924 !important;
        border: 1px solid #E5E9E4 !important;
        border-radius: 14px !important;
        padding: 12px !important;
        height: 52px !important;
        font-size: 13.5px !important;
        font-weight: 600 !important;
    }}
    button[key^="lang_sel_active_"] {{
        background: #F2F8F4 !important;
        color: #0F4935 !important;
        border: 1.8px solid #176B4D !important;
        border-radius: 14px !important;
        padding: 12px !important;
        height: 52px !important;
        font-size: 13.5px !important;
        font-weight: 800 !important;
        box-shadow: 0 2px 8px rgba(23, 107, 77, 0.12) !important;
    }}

    /* Popular Topics Row */
    .popular-topics-wrap {{
        display: flex;
        align-items: center;
        gap: 6px;
        flex-wrap: wrap;
        margin-top: 6px;
        margin-bottom: 18px;
    }}
    .popular-title {{
        font-size: 11.5px;
        font-weight: 600;
        color: #68756E;
    }}
    button[key^="topic_chip_"] {{
        background: #F3F6F3 !important;
        color: #1E2924 !important;
        border: 1px solid #E2E8E3 !important;
        border-radius: 9999px !important;
        padding: 4px 12px !important;
        font-size: 11.5px !important;
        font-weight: 600 !important;
        height: auto !important;
        min-height: 28px !important;
    }}
    button[key^="topic_chip_"]:hover {{
        background: #E8F2EC !important;
        border-color: #176B4D !important;
        color: #0F4935 !important;
    }}

    /* Main Emerald CTA Button */
    div.stButton > button[key="btn_generate_main"] {{
        background: linear-gradient(135deg, #176B4D 0%, #0F4935 100%) !important;
        color: #FFFFFF !important;
        border: none !important;
        border-radius: 18px !important;
        padding: 16px 28px !important;
        font-size: 16px !important;
        font-weight: 800 !important;
        letter-spacing: -0.01em !important;
        box-shadow: 0 6px 20px -2px rgba(15, 73, 53, 0.35) !important;
        transition: all 0.2s ease !important;
        margin-top: 6px !important;
    }}
    div.stButton > button[key="btn_generate_main"]:hover {{
        transform: translateY(-2px);
        box-shadow: 0 10px 26px -2px rgba(15, 73, 53, 0.45) !important;
    }}

    /* --- 7. WHY AYURVEDA AI STRIP --- */
    .why-card-strip {{
        background: #FFFFFF;
        border: 1px solid #EBEFEA;
        border-radius: 20px;
        padding: 14px 18px;
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 12px;
        margin-bottom: 20px;
        box-shadow: 0 2px 10px rgba(15, 73, 53, 0.03);
    }}
    .why-title-badge {{
        display: flex;
        align-items: center;
        gap: 8px;
        font-size: 13.5px;
        font-weight: 800;
        color: #0F4935;
        white-space: nowrap;
    }}
    .why-items-grid {{
        display: flex;
        gap: 14px;
        overflow-x: auto;
        scrollbar-width: none;
    }}
    .why-items-grid::-webkit-scrollbar {{
        display: none;
    }}
    .why-chip {{
        display: flex;
        align-items: center;
        gap: 6px;
        font-size: 11px;
        font-weight: 600;
        color: #4A5851;
        white-space: nowrap;
    }}

    /* --- 8. FIXED MOBILE BOTTOM NAVIGATION --- */
    .bottom-navbar-fixed {{
        position: fixed;
        bottom: 0;
        left: 0;
        right: 0;
        height: 64px;
        background: rgba(255, 255, 255, 0.96);
        backdrop-filter: blur(14px);
        -webkit-backdrop-filter: blur(14px);
        border-top: 1px solid #E5EBE6;
        display: flex;
        justify-content: space-around;
        align-items: center;
        z-index: 9999;
        box-shadow: 0 -4px 16px rgba(0, 0, 0, 0.04);
        max-width: 820px;
        margin: 0 auto;
    }}
    .bottom-nav-item {{
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        gap: 3px;
        color: #68756E;
        text-decoration: none;
        font-size: 11px;
        font-weight: 600;
        cursor: pointer;
        padding: 4px 12px;
    }}
    .bottom-nav-item.active {{
        color: #176B4D;
        font-weight: 800;
    }}
    .bottom-nav-icon {{
        font-size: 19px;
        line-height: 1;
    }}

    /* Streamlit Input Overrides for Medical SaaS */
    div[data-baseweb="select"] > div,
    div[data-baseweb="input"] > div {{
        background-color: #FFFFFF !important;
        border: 1px solid #E2E8E3 !important;
        border-radius: 12px !important;
        box-shadow: inset 0 1px 2px rgba(0,0,0,0.02) !important;
        min-height: 44px !important;
    }}
    div[data-baseweb="select"] > div:hover,
    div[data-baseweb="input"] > div:hover {{
        border-color: #176B4D !important;
    }}

    /* Textbook Format Container */
    .textbook-container {{
        background: #FFFFFF;
        border: 1px solid #E2E8E3;
        border-radius: 20px;
        padding: 30px 32px;
        box-shadow: 0 4px 18px rgba(15, 73, 53, 0.04);
        margin-top: 18px;
        font-family: 'Mukta', 'Plus Jakarta Sans', sans-serif;
        font-size: 16px;
        line-height: 1.85;
        color: #1E2924;
    }}
    .textbook-container h1, .textbook-container h2, .textbook-container h3 {{
        color: #0F4935 !important;
        font-weight: 800 !important;
        margin-top: 1.4em;
        margin-bottom: 0.5em;
        border-bottom: 1px solid #EEF2EE;
        padding-bottom: 6px;
    }}
    .textbook-container blockquote {{
        border-left: 4px solid #176B4D;
        background: #F4F8F6;
        padding: 12px 18px;
        margin: 16px 0;
        border-radius: 0 12px 12px 0;
        font-weight: 700;
        color: #0F4935;
    }}
    .textbook-container table {{
        width: 100%;
        border-collapse: collapse;
        margin: 18px 0;
    }}
    .textbook-container th, .textbook-container td {{
        border: 1px solid #E2E8E3;
        padding: 9px 12px;
    }}
    .textbook-container th {{
        background: #F1F6F3;
        color: #0F4935;
    }}

    /* Mobile Responsive Polish */
    @media (max-width: 640px) {{
        .hero-desc {{
            max-width: 100%;
        }}
        .hero-title-row {{
            flex-direction: column;
        }}
        .hero-book-stack {{
            display: none;
        }}
        .hero-benefits-grid {{
            grid-template-columns: repeat(2, 1fr);
            gap: 12px;
        }}
        .textbook-container {{
            padding: 18px 16px;
        }}
    }}
</style>
""", unsafe_allow_html=True)

# =========================================================================
# 🔌 CLIENT INITIALIZATION & SECRETS CHECK
# =========================================================================
api_key = st.secrets.get("GEMINI_API_KEY", "")
supabase_url = st.secrets.get("SUPABASE_URL", "")
supabase_key = st.secrets.get("SUPABASE_KEY", "")

if not api_key:
    st.error("⚠️ GEMINI_API_KEY सापडली नाही. कृपया Streamlit Secrets तपासा.")
    st.stop()

if not supabase_url or not supabase_key:
    st.error("⚠️ SUPABASE_URL किंवा SUPABASE_KEY सापडली नाही. कृपया Secrets तपासा.")
    st.stop()

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

# Initialize navigation state
if "active_nav" not in st.session_state:
    st.session_state.active_nav = "Study"
if "study_mode_sel" not in st.session_state:
    st.session_state.study_mode_sel = "📖 Comprehensive Notes (संपूर्ण सविस्तर अभ्यास नोट्स)"
if "study_lang_sel" not in st.session_state:
    st.session_state.study_lang_sel = "🚩 मराठी (संस्कृत + अर्थ)"
if "topic_input_val" not in st.session_state:
    st.session_state.topic_input_val = ""

# =========================================================================
# 🔐 AUTHENTICATION MODAL / LOGIN GATEWAY (IF NOT LOGGED IN)
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
        <div class="author-pill">
            <span class="author-avatar">AA</span>
            <span>Avishkar Alase ✓</span>
        </div>
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
            <p style="font-size: 13.5px; color: #68756E; margin: 0;">NCISM BAMS अभ्यासक्रम, A4 हस्तलिखित नोट्स व विद्यापीठ प्रश्नसंच.</p>
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
# 🎯 DYNAMIC GEMINI MODEL DISCOVERY & CALL ENGINE
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
# 👤 PROFILE EXTRACTION & SIDEBAR (COLLAPSIBLE / DESKTOP COMPACT)
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
# 📱 TOP HEADER (SCREENSHOT MATCH)
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
        <span class="icon-action-btn">🔍</span>
        <span class="icon-action-btn">🔔</span>
        <div class="avatar-circle">{initials}</div>
    </div>
</div>
""", unsafe_allow_html=True)

# =========================================================================
# 👋 WELCOME CARD (SCREENSHOT MATCH)
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
        <span class="badge-icon">📅</span>
        <div class="badge-content">
            <span class="badge-title">BAMS Scholar</span>
            <span class="badge-desc">Ayurveda for<br>a Better Tomorrow</span>
        </div>
        <span class="badge-leaf-bg">🌿</span>
    </div>
</div>
""", unsafe_allow_html=True)

# =========================================================================
# 🪔 DYNAMIC FESTIVAL STRIP (SCREENSHOT MATCH)
# =========================================================================
st.markdown(f"""
<div class="festival-strip">
    <div class="festival-strip-left">
        <div class="festival-lamp">{th['icon']}</div>
        <div class="festival-text">
            <div class="festival-title">{th['festive_title']}</div>
            <div class="festival-sub">{th['festive_subtitle']}</div>
        </div>
    </div>
    <div class="festival-arrow">›</div>
</div>
""", unsafe_allow_html=True)

# =========================================================================
# 🧭 FEATURE NAVIGATION CARDS (SCREENSHOT MATCH)
# =========================================================================
nav_cols = st.columns(5)
nav_items = [
    ("Study", "📖"),
    ("Medicine", "🧪"),
    ("Viva", "🎙"),
    ("Clinical", "🩺"),
    ("Research", "🔬")
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
# MODULE 1: STUDY STUDIO (PRIMARY SCREENSHOT SCREEN)
# -------------------------------------------------------------------------
if st.session_state.active_nav == "Study":
    # 5. Deep Emerald Hero Card
    st.markdown("""
    <div class="hero-card">
        <div class="hero-tag-pill">BAMS • AI • NCISM • MUHS</div>
        <div class="hero-title-row">
            <div>
                <h2 class="hero-main-title">BAMS <span>Study Studio</span></h2>
                <div class="hero-desc">
                    AI-powered notes, PYQs and exam-focused preparation for every BAMS student.
                </div>
            </div>
            <div class="hero-book-stack">
                <span class="book-spine">Charaka</span>
                <span class="book-spine" style="background:#4A2C18;">Sushruta</span>
                <span class="book-spine" style="background:#372111;">Ashtanga Hridaya</span>
            </div>
        </div>
        <div class="hero-benefits-grid">
            <div class="hero-benefit-item">
                <div class="benefit-icon-badge">✍️</div>
                <div class="benefit-label">Handwritten<br>Style Notes</div>
            </div>
            <div class="hero-benefit-item">
                <div class="benefit-icon-badge">🎯</div>
                <div class="benefit-label">PYQ Solved<br>with Answers</div>
            </div>
            <div class="hero-benefit-item">
                <div class="benefit-icon-badge">🧠</div>
                <div class="benefit-label">Exam Focused<br>Learning</div>
            </div>
            <div class="hero-benefit-item">
                <div class="benefit-icon-badge">⚡</div>
                <div class="benefit-label">Quick<br>Revision</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # 6. Study Note Creation Card (Step 1 to 5)
    st.markdown("""
    <div class="study-form-card">
        <div class="card-header-row">
            <div class="card-header-left">
                <span>🌿</span>
                <span>Create Your Study Notes</span>
            </div>
            <div class="step-indicator-pill">
                <span>Step 1 of 5</span>
                <span class="step-dots">● ○ ○ ○ ○</span>
            </div>
        </div>
    """, unsafe_allow_html=True)

    # STEP 01 & 02 DROPDOWNS
    st.markdown("""
        <div class="step-title-row">
            <div class="step-num-title">
                <span class="step-badge">01</span>
                <span>Professional Year</span>
            </div>
            <span class="step-meta-hint">BAMS Academic Year</span>
        </div>
    """, unsafe_allow_html=True)
    bams_year = st.selectbox(
        "Professional Year",
        [
            "BAMS 1st Professional (प्रथम वर्ष)",
            "BAMS 2nd Professional (द्वितीय वर्ष)",
            "BAMS 3rd Professional (तृतीय वर्ष)",
            "BAMS Final Professional (अंतिम वर्ष)"
        ],
        label_visibility="collapsed"
    )

    st.markdown("""
        <div class="step-title-row">
            <div class="step-num-title">
                <span class="step-badge">02</span>
                <span>Subject</span>
            </div>
            <span class="step-meta-hint">Choose Subject</span>
        </div>
    """, unsafe_allow_html=True)
    subject = st.selectbox(
        "Subject",
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
        ],
        label_visibility="collapsed"
    )

    # STEP 03: STUDY MODE SELECTABLE GRID CARDS
    st.markdown("""
        <div class="step-title-row">
            <div class="step-num-title">
                <span class="step-badge">03</span>
                <span>Study Mode</span>
            </div>
            <span class="step-meta-hint">How do you want to learn?</span>
        </div>
    """, unsafe_allow_html=True)

    mode_options = [
        ("📖 Comprehensive Notes (संपूर्ण सविस्तर अभ्यास नोट्स)", "📄 Comprehensive\nNotes"),
        ("🎯 MUHS / NCISM Past 5 Years Questions & Model Answer Key", "🎯 PYQ\nFocus"),
        ("⚡ Quick Revision / Viva Voce Points (तोंडी परीक्षेसाठी महत्त्वाचे मुद्दे)", "⚡ Quick\nRevision"),
        ("📋 A4 Blue Ballpen Handwritten Sheet (अस्सल A4 पेन नोट्स)", "✍️ A4\nHandwritten")
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

    # STEP 04: STUDY MEDIUM SELECTABLE OPTIONS
    st.markdown("""
        <div class="step-title-row">
            <div class="step-num-title">
                <span class="step-badge">04</span>
                <span>Study Medium</span>
            </div>
            <span class="step-meta-hint">Select Language</span>
        </div>
    """, unsafe_allow_html=True)

    l_cols = st.columns(2)
    lang_opts = [
        ("🚩 मराठी (संस्कृत + अर्थ)", "🇮🇳 मराठी (संस्कृत + अर्थ)"),
        ("🌿 Simple English + Sanskrit", "🌐 Simple English + Sanskrit")
    ]
    for l_idx, (l_val, l_title) in enumerate(lang_opts):
        with l_cols[l_idx]:
            is_l_active = (st.session_state.study_lang_sel == l_val)
            l_key = f"lang_sel_active_{l_idx}" if is_l_active else f"lang_sel_{l_idx}"
            display_ltitle = f"✓ {l_title}" if is_l_active else l_title
            if st.button(display_ltitle, key=l_key, use_container_width=True):
                st.session_state.study_lang_sel = l_val
                st.rerun()

    # STEP 05: TOPIC INPUT & POPULAR TOPICS CHIPS
    st.markdown("""
        <div class="step-title-row">
            <div class="step-num-title">
                <span class="step-badge">05</span>
                <span>What do you want to study?</span>
            </div>
            <span class="step-meta-hint">Enter topic or question</span>
        </div>
    """, unsafe_allow_html=True)

    topic_input = st.text_input(
        "What do you want to study?",
        value=st.session_state.topic_input_val,
        placeholder="उदा. Virya, Ojas, Pitta Dosha, Rakta Dhatu, Ashwagandha...",
        label_visibility="collapsed",
        key="main_topic_input"
    )

    # Popular Topic Pills
    st.markdown('<div class="popular-topics-wrap"><span class="popular-title">Popular topics:</span>', unsafe_allow_html=True)
    pop_cols = st.columns([1.1, 1.1, 1.4, 1.4, 1.6, 3])
    pop_list = ["Virya", "Ojas", "Pitta Dosha", "Rakta Dhatu", "Ashwagandha"]
    for p_idx, p_name in enumerate(pop_list):
        with pop_cols[p_idx]:
            if st.button(p_name, key=f"topic_chip_{p_idx}"):
                st.session_state.topic_input_val = p_name
                st.rerun()

    # Main Action CTA Button
    generate_notes_btn = st.button("✨ Generate Study Notes →", key="btn_generate_main", use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # 7. Why AyurVeda AI Strip (Screenshot Match)
    st.markdown("""
    <div class="why-card-strip">
        <div class="why-title-badge">
            <span>🌿</span>
            <span>Why AyurVeda AI?</span>
        </div>
        <div class="why-items-grid">
            <span class="why-chip">🛡️ <b>Accurate & Exam Focused</b></span>
            <span class="why-chip">👥 <b>Trusted by BAMS Students</b></span>
            <span class="why-chip">⏱️ <b>Saves Time & Effort</b></span>
            <span class="why-chip">💚 <b>Learn Ayurveda Build a Healthier You</b></span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Note Generation Execution Logic
    if generate_notes_btn:
        final_topic = topic_input.strip() or st.session_state.topic_input_val.strip()
        if not final_topic:
            st.warning("⚠️ कृपया अभ्यासाचा विषय प्रविष्ट करा.")
        else:
            is_marathi = "मराठी" in st.session_state.study_lang_sel
            active_study_mode = st.session_state.study_mode_sel
            lang_preference = st.session_state.study_lang_sel

            if "A4 Blue Ballpen" in active_study_mode:
                lang_rule = "Write in natural, simple spoken Marathi with Sanskrit terms and simple English in parentheses." if is_marathi else "Write 100% in pure English Roman script. All titles and terms in English."
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

                Format with bold headings, clean bullet points, and high readability.
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
                        st.session_state.current_topic = final_topic
                        st.session_state.current_subject = subject
                        st.session_state.current_mode = active_study_mode
                    except Exception as e:
                        st.error(f"त्रुटी: {e}")

    # Result Rendering Area
    if st.session_state.get("current_generated_note"):
        c_type = st.session_state.current_note_type
        c_data = st.session_state.current_generated_note
        c_top = st.session_state.current_topic
        c_sub = st.session_state.current_subject
        c_mod = st.session_state.current_mode

        st.markdown(f"""
        <div style="border-bottom: 1.5px solid #E2E8E3; padding-bottom: 12px; margin-top: 26px;">
            <div style="font-size: 11px; font-weight: 800; color: #176B4D; text-transform: uppercase; letter-spacing: 0.05em;">📚 Generated Study Notes</div>
            <h3 style="margin: 4px 0 2px 0; color: #0F4935; font-weight: 800;">{c_top}</h3>
            <div style="font-size: 13px; color: #68756E; font-weight: 600;">{c_sub} • {c_mod}</div>
        </div>
        """, unsafe_allow_html=True)

        col_s1, col_s2, col_s3 = st.columns([1, 1, 1])
        with col_s1:
            if st.button("💾 Save to Account", key="save_n_tab1_fix", use_container_width=True):
                try:
                    save_payload = json.dumps(c_data) if c_type == "a4_sheet" else str(c_data)
                    supabase.table("user_notes").insert({
                        "user_id": st.session_state.user_id,
                        "subject": c_sub,
                        "topic": c_top,
                        "study_mode": c_mod,
                        "content": save_payload
                    }).execute()
                    st.success("✅ नोट खात्यात सुरक्षित सेव्ह झाली!")
                    time.sleep(0.8)
                    st.rerun()
                except Exception as s_err:
                    st.error(f"सेव्ह करताना त्रुटी: {s_err}")

        with col_s2:
            share_preview = f"🌿 *AyurVeda AI Notes*\n📚 *विषय:* {c_sub}\n🎯 *टॉपिक:* {c_top}\n\nAyurVeda AI Studio वर तयार केलेली नोट!"
            encoded_share = urllib.parse.quote(share_preview)
            st.link_button("📲 WhatsApp Share", f"[https://api.whatsapp.com/send?text=](https://api.whatsapp.com/send?text=){encoded_share}", use_container_width=True)

        with col_s3:
            if c_type != "a4_sheet":
                html_content = markdown.markdown(c_data, extensions=['tables', 'fenced_code'])
                html_export = f"""<!DOCTYPE html>
<html lang="mr">
<head>
<meta charset="UTF-8">
<title>{c_top} - BAMS Notes</title>
<link href="[https://fonts.googleapis.com/css2?family=Mukta:wght@400;600;700;800&display=swap](https://fonts.googleapis.com/css2?family=Mukta:wght@400;600;700;800&display=swap)" rel="stylesheet">
<style>
    body {{ font-family: 'Mukta', sans-serif; line-height: 1.8; padding: 40px; color: #111827; max-width: 860px; margin: auto; }}
    table {{ width: 100%; border-collapse: collapse; margin: 18px 0; }}
    th, td {{ border: 1px solid #4b5563; padding: 10px 14px; }}
    blockquote {{ border-left: 4px solid #176B4D; margin: 14px 0; padding: 10px 18px; background: #f8fafc; font-weight: 700; }}
</style>
</head>
<body>
    <h2>🌿 AyurVeda AI • {c_top}</h2>
    <div><b>विद्यार्थी:</b> {s_name} | <b>विषय:</b> {c_sub}</div>
    <hr>
    <div>{html_content}</div>
</body>
</html>"""
                st.download_button(
                    label="📥 Download Printable HTML",
                    data=html_export.encode('utf-8'),
                    file_name=f"{c_top.replace(' ', '_')}_Notes.html",
                    mime="text/html",
                    use_container_width=True
                )

        if c_type == "a4_sheet":
            st.markdown(f"""
            <div class="study-form-card" style="margin-top: 14px; background: #FAFBF9;">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <div>
                        <div style="font-weight: 800; font-size: 15px; color: #0F4935;">✍️ A4 Handwritten Sheet Ready</div>
                        <small style="color: #68756E;">{c_sub} • {c_top} • 10 Marks / LAQ</small>
                    </div>
                    <span class="step-badge" style="background:#EAF3EF; color:#176B4D;">Verified A4 Format</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
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
    m_col1, m_col2 = st.columns([1, 1])
    with m_col1:
        st.markdown('<div class="step-num-title"><span class="step-badge">01</span><span>Dosage Form</span></div>', unsafe_allow_html=True)
        dosage_form = st.selectbox(
            "औषधाचा प्रकार (Dosage Form):",
            ["Vati / Gutika (गोळी / वटी)", "Churna (चूर्ण)", "Asava & Arishta (आसव व अरिष्ट)", "Taila / Ghrita (सिद्ध तेल व घृत)", "Bhasma & Pishti (भस्म व पिष्टी)"],
            label_visibility="collapsed"
        )
    with m_col2:
        st.markdown('<div class="step-num-title"><span class="step-badge">02</span><span>Language</span></div>', unsafe_allow_html=True)
        m_lang = st.radio("भाषा निवडा:", ["Simple Indian English", "मराठी"], horizontal=True, key="m_lang", label_visibility="collapsed")

    st.markdown('<div class="step-num-title" style="margin-top:10px;"><span class="step-badge">03</span><span>Medicine Name</span></div>', unsafe_allow_html=True)
    medicine_name = st.text_input("गोळी किंवा औषधाचे नाव टाका:", placeholder="उदा. आरोग्यवर्धिनी वटी, चंद्रप्रभावटी, सुवर्णभस्म", label_visibility="collapsed")

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
        if st.button("💾 Save Formulation to Notes", key="save_med_btn"):
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
    v_col1, v_col2 = st.columns([1, 1])
    with v_col1:
        st.markdown('<div class="step-num-title"><span class="step-badge">01</span><span>Subject</span></div>', unsafe_allow_html=True)
        viva_sub = st.selectbox(
            "Viva साठी विषय:",
            ["Kriya Sharir", "Rachana Sharir", "Dravyaguna", "Rasa Shastra", "Agada Tantra", "Kayachikitsa", "Shalya Tantra"],
            key="viva_sub",
            label_visibility="collapsed"
        )
    with v_col2:
        st.markdown('<div class="step-num-title"><span class="step-badge">02</span><span>Language</span></div>', unsafe_allow_html=True)
        viva_lang = st.radio("Viva भाषा:", ["मराठी + Sanskrit Terms", "Simple Indian English"], horizontal=True, key="viva_lang", label_visibility="collapsed")

    st.markdown('<div class="step-num-title" style="margin-top:10px;"><span class="step-badge">03</span><span>Topic</span></div>', unsafe_allow_html=True)
    viva_topic = st.text_input("परीक्षक कोणत्या विषयावर प्रश्न विचारतील?", placeholder="उदा. Pitta Sthana, Ashwagandha Guna, Vatsanabha Shodhana", key="viva_top", label_visibility="collapsed")

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
                <div style="background:#FFFFFF; border:1px solid #E2E8E3; border-radius:14px; padding:16px; margin-bottom:10px;">
                    <span class="step-badge" style="background:#FEF9EE; color:#C88A24;">QUESTION {idx+1:02d}</span>
                </div>
                """, unsafe_allow_html=True)
                lines = cleaned_block.split("\n", 1)
                st.markdown(f"**{lines[0].replace('**', '')}**")
                if len(lines) > 1:
                    with st.expander("View Model Answer"):
                        st.markdown(lines[1])
        else:
            st.markdown(f'<div class="textbook-container">{v_raw}</div>', unsafe_allow_html=True)

        if st.button("💾 Save Viva Set to Notes", key="save_viva_btn"):
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
    c_col1, c_col2 = st.columns([1, 1])
    with c_col1:
        st.markdown('<div class="step-num-title"><span class="step-badge">01</span><span>Department</span></div>', unsafe_allow_html=True)
        case_subject = st.selectbox(
            "क्लिनिकल विभाग (Department):",
            ["Kayachikitsa (कायचिकित्सा)", "Panchakarma (पंचकर्म)", "Shalya Tantra (शल्य)", "Shalakya (नेत्र/कर्ण/नासा)", "Stri Roga & Prasuti (स्त्रीरोग)", "Kaumarbhritya (बालरोग)"],
            key="case_sub",
            label_visibility="collapsed"
        )
    with c_col2:
        st.markdown('<div class="step-num-title"><span class="step-badge">02</span><span>Language</span></div>', unsafe_allow_html=True)
        case_lang = st.radio("भाषा निवडा:", ["मराठी + Clinical English", "Simple Indian English + Sanskrit"], horizontal=True, key="cs_lang", label_visibility="collapsed")

    st.markdown('<div class="step-num-title" style="margin-top:10px;"><span class="step-badge">03</span><span>Disease / Symptoms</span></div>', unsafe_allow_html=True)
    case_topic = st.text_input("आजाराचे नाव / मुख्य लक्षणे प्रविष्ट करा:", placeholder="उदा. Amlapitta (GERD), Sandhivata (Osteoarthritis), Tamaka Shwasa (Asthma)", key="cs_top", label_visibility="collapsed")

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
        if st.button("💾 Save Case Presentation to Notes", key="save_case_btn"):
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

# -------------------------------------------------------------------------
# MODULE 5: RESEARCH & EVIDENCE LAB
# -------------------------------------------------------------------------
elif st.session_state.active_nav == "Research":
    st.markdown("""
    <div class="hero-card">
        <div class="hero-tag-pill">SCIENTIFIC EVIDENCE</div>
        <h2 class="hero-main-title">🔬 Research & Evidence Lab</h2>
        <div class="hero-desc">Evidence-based Ayurvedic research assistant with phytochemical trials and pharmacology.</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="study-form-card">', unsafe_allow_html=True)
    st.markdown('<div class="step-num-title"><span class="step-badge">01</span><span>Herb / Drug / Compound</span></div>', unsafe_allow_html=True)
    res_topic = st.text_input("औषधी वनस्पती किंवा सक्रिय घटक:", placeholder="उदा. Withania somnifera (Ashwagandha), Tinospora cordifolia (Guduchi), Curcumin", key="res_top", label_visibility="collapsed")

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
        if st.button("💾 Save Research Report to Notes", key="save_res_btn"):
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

# =========================================================================
# 📱 FIXED MOBILE BOTTOM NAVIGATION BAR (SCREENSHOT MATCH)
# =========================================================================
st.markdown("""
<div class="bottom-navbar-fixed">
    <div class="bottom-nav-item active">
        <span class="bottom-nav-icon">⌂</span>
        <span>Home</span>
    </div>
    <div class="bottom-nav-item">
        <span class="bottom-nav-icon">🔖</span>
        <span>Saved</span>
    </div>
    <div class="bottom-nav-item">
        <span class="bottom-nav-icon">◷</span>
        <span>History</span>
    </div>
    <div class="bottom-nav-item">
        <span class="bottom-nav-icon">♙</span>
        <span>Profile</span>
    </div>
</div>
""", unsafe_allow_html=True)
