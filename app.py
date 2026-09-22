import streamlit as st
from google import genai
from google.genai import types
import json
import time
import urllib.parse
from datetime import datetime
import markdown
from supabase import create_client, Client

# --- Page Setup ---
st.set_page_config(
    page_title="AyurVeda AI | VIP Academic Studio",
    page_icon="🌿",
    layout="centered",
    initial_sidebar_state="expanded"
)

# =========================================================================
# 🎯 AUTOMATIC DYNAMIC FESTIVAL THEME ENGINE
# =========================================================================
def get_current_festival_theme():
    now = datetime.now()
    month, day = now.month, now.day

    if month == 9 and 12 <= day <= 26:
        return {
            "name": "ganeshotsav",
            "tag": "🌺 ॥ श्री गणेशाय नमः ॥ 🌺",
            "icon": "🪔",
            "title_sub": "गणेशोत्सव विशेष पर्व | BAMS HANDWRITTEN STUDIO",
            "bg": "radial-gradient(circle at 50% 0%, #fffbeb 0%, #fef3c7 25%, #fdfcf7 60%, #fff7ed 100%)",
            "hero_grad": "linear-gradient(135deg, #b45309 0%, #c2410c 45%, #991b1b 100%)",
            "hero_border": "#fef08a",
            "btn_grad": "linear-gradient(135deg, #ea580c 0%, #d97706 50%, #b45309 100%)",
            "border_color": "#fed7aa",
            "focus_color": "#f59e0b",
            "active_tab": "linear-gradient(135deg, #b45309 0%, #ea580c 100%)",
            "footer_text": "🌺 ॥ गणपती बाप्पा मोरया ॥ 🌿",
            "font_accent": "#92400e"
        }
    elif month == 10 and 10 <= day <= 24:
        return {
            "name": "navratri",
            "tag": "🌸 ॥ जय जगदंब - शुभ नवरात्री व विजयादशमी ॥ 🌸",
            "icon": "🔱",
            "title_sub": "शक्ती व विद्या पर्व विशेष | BAMS HANDWRITTEN STUDIO",
            "bg": "radial-gradient(circle at 50% 0%, #fff1f2 0%, #ffe4e6 30%, #fffdf9 70%, #fdf4ff 100%)",
            "hero_grad": "linear-gradient(135deg, #9f1239 0%, #be123c 45%, #881337 100%)",
            "hero_border": "#fda4af",
            "btn_grad": "linear-gradient(135deg, #e11d48 0%, #be123c 50%, #9f1239 100%)",
            "border_color": "#fecdd3",
            "focus_color": "#e11d48",
            "active_tab": "linear-gradient(135deg, #9f1239 0%, #e11d48 100%)",
            "footer_text": "🌸 ॥ सर्वमंगल मांगल्ये शिवे सर्वार्थ साधिके ॥ 🌿",
            "font_accent": "#881337"
        }
    elif month == 11 and 4 <= day <= 14:
        return {
            "name": "diwali",
            "tag": "🪔 ॥ ॐ महालक्ष्म्यै नमः - शुभ दीपावली ॥ 🪔",
            "icon": "✨",
            "title_sub": "दीपोत्सव महाविशेष पर्व | BAMS HANDWRITTEN STUDIO",
            "bg": "radial-gradient(circle at 50% 0%, #172554 0%, #1e1b4b 40%, #0f172a 100%)",
            "hero_grad": "linear-gradient(135deg, #d97706 0%, #b45309 40%, #78350f 100%)",
            "hero_border": "#fde047",
            "btn_grad": "linear-gradient(135deg, #eab308 0%, #ca8a04 50%, #a16207 100%)",
            "border_color": "#fde047",
            "focus_color": "#facc15",
            "active_tab": "linear-gradient(135deg, #ca8a04 0%, #eab308 100%)",
            "footer_text": "🪔 ॥ शुभ दीपावली - सुख समृद्धी लाभो ॥ 🌿",
            "font_accent": "#facc15"
        }
    else:
        return {
            "name": "ayurveda_classic",
            "tag": "🌿 ॥ नमामि धन्वंतरिमादिदेवम् - BAMS अकॅडेमिक स्टुडिओ ॥ 🌿",
            "icon": "🌱",
            "title_sub": "NCISM BAMS A4 HANDWRITTEN STUDIO",
            "bg": "radial-gradient(circle at 50% 0%, #ecfdf5 0%, #f0fdf4 35%, #f8fafc 70%, #e6fcf5 100%)",
            "hero_grad": "linear-gradient(135deg, #064e3b 0%, #047857 50%, #064e3b 100%)",
            "hero_border": "#a7f3d0",
            "btn_grad": "linear-gradient(135deg, #059669 0%, #047857 50%, #064e3b 100%)",
            "border_color": "#cbd5e1",
            "focus_color": "#059669",
            "active_tab": "linear-gradient(135deg, #064e3b 0%, #059669 100%)",
            "footer_text": "🌿 ॥ आरोग्यं परमं भाग्यम् ॥ 🌿",
            "font_accent": "#064e3b"
        }

th = get_current_festival_theme()

# --- VIP COMPACT CSS STYLES ---
st.markdown(f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@500;600;700;800;900&family=Mukta:wght@400;600;700;800;900&display=swap');

    html, body, .stApp {{
        background: {th['bg']} !important;
        background-attachment: fixed !important;
        font-family: 'Mukta', 'Plus Jakarta Sans', sans-serif !important;
        color: #0f172a !important;
    }}
    
    .main .block-container {{
        max-width: 820px !important;
        padding-top: 0.8rem !important;
        padding-bottom: 2.2rem !important;
        margin: auto !important;
    }}

    .vip-navbar {{
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 10px 18px;
        background: rgba(255, 255, 255, 0.95) !important;
        backdrop-filter: blur(16px);
        border: 1.8px solid {th['border_color']} !important;
        border-radius: 18px;
        margin-bottom: 12px;
        box-shadow: 0 8px 24px -6px rgba(0, 0, 0, 0.06);
    }}
    .brand-title {{
        font-size: 20px;
        font-weight: 900;
        background: {th['btn_grad']};
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 0;
        line-height: 1.2;
    }}
    .author-badge {{
        background: #ffffff !important;
        border: 1.5px solid {th['focus_color']};
        padding: 6px 14px;
        border-radius: 12px;
        font-size: 12.5px;
        font-weight: 800;
        color: {th['font_accent']} !important;
    }}

    .vip-hero {{
        background: {th['hero_grad']} !important;
        padding: 16px 20px;
        border-radius: 20px;
        margin-bottom: 14px;
        color: #ffffff !important;
        box-shadow: 0 12px 30px -8px rgba(0, 0, 0, 0.22);
        border: 1.8px solid {th['hero_border']};
    }}
    .vip-hero * {{ color: #ffffff !important; }}
    .festive-tag {{
        display: inline-flex;
        background: rgba(255, 255, 255, 0.22);
        padding: 3px 12px;
        border-radius: 20px;
        font-size: 11.5px;
        font-weight: 800;
        margin-bottom: 6px;
        border: 1px solid rgba(255, 255, 255, 0.35);
    }}

    .vip-card-box {{
        background: rgba(255, 255, 255, 0.97) !important;
        border: 1.8px solid {th['border_color']} !important;
        border-radius: 22px;
        padding: 20px 22px;
        box-shadow: 0 16px 36px -10px rgba(0, 0, 0, 0.1);
        margin: 0 auto;
    }}

    div[data-baseweb="select"] > div,
    div[data-baseweb="input"] > div {{
        background-color: #ffffff !important;
        border: 1.8px solid {th['border_color']} !important;
        border-radius: 14px !important;
    }}
    div[data-baseweb="select"] > div:hover,
    div[data-baseweb="input"] > div:hover {{
        border-color: {th['focus_color']} !important;
    }}

    div.stButton > button {{
        background: {th['btn_grad']} !important;
        color: #ffffff !important;
        border: 1.8px solid {th['hero_border']} !important;
        border-radius: 16px !important;
        padding: 12px 24px !important;
        font-size: 15.5px !important;
        font-weight: 800 !important;
        box-shadow: 0 8px 20px -5px rgba(0, 0, 0, 0.2) !important;
    }}

    .stTabs [data-baseweb="tab-list"] {{
        gap: 8px;
        margin-bottom: 14px;
    }}
    .stTabs [data-baseweb="tab"] {{
        background-color: rgba(255, 255, 255, 0.88) !important;
        border-radius: 14px !important;
        padding: 8px 16px !important;
        font-weight: 800 !important;
        font-size: 13.5px !important;
        border: 1.5px solid {th['border_color']} !important;
    }}
    .stTabs [aria-selected="true"] {{
        background: {th['active_tab']} !important;
        border-color: {th['focus_color']} !important;
        color: #ffffff !important;
    }}
    .stTabs [aria-selected="true"] * {{ color: #ffffff !important; }}

    .student-id-card {{
        background: linear-gradient(135deg, #ffffff 0%, #f0fdf4 100%);
        border: 1.8px solid #86efac;
        padding: 15px;
        border-radius: 18px;
        margin-bottom: 14px;
        box-shadow: 0 6px 18px -4px rgba(0, 0, 0, 0.06);
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

# =========================================================================
# 🔐 VIP LOGIN & REGISTRATION INTERFACE
# =========================================================================
if not st.session_state.user_id:
    st.markdown(f"""
    <div class="vip-navbar">
        <div style="display:flex; align-items:center; gap:10px;">
            <div style="font-size:26px;">{th['icon']}</div>
            <div>
                <div class="brand-title">🌿 AyurVeda AI Studio</div>
                <small style="color:{th['font_accent']}; font-weight:800; font-size:11.5px;">{th['title_sub']}</small>
            </div>
        </div>
        <div class="author-badge">Avishkar Alase ✓</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class="vip-hero">
        <div class="festive-tag">{th['tag']}</div>
        <h3 style="margin:0 0 4px 0; font-weight:900; font-size:20px;">🎓 BAMS VIP अकॅडेमिक पोर्टल</h3>
        <p style="margin:0; font-size:13px; opacity:0.95;">NCISM अभ्यासक्रम, A4 हस्तलिखित नोट्स, प्रश्नसंच व संपूर्ण क्लिनिकल सूट.</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="vip-card-box">', unsafe_allow_html=True)
    t_login, t_reg = st.tabs(["🔑 विद्यार्थी लॉगिन (Sign In)", "✨ नवीन नोंदणी (Student Register)"])

    with t_login:
        st.markdown(f"<h4 style='color:{th['font_accent']}; margin:0 0 10px 0; font-weight:900;'>लॉगिन करा:</h4>", unsafe_allow_html=True)
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
                        time.sleep(1)
                        st.rerun()
                except Exception as e:
                    st.error(f"लॉगिन अयशस्वी: {e}")

    with t_reg:
        st.markdown(f"<h4 style='color:{th['font_accent']}; margin:0 0 10px 0; font-weight:900;'>विद्यार्थी नोंदणी फॉर्म:</h4>", unsafe_allow_html=True)
        r_name = st.text_input("👤 विद्यार्थ्याचे पूर्ण नाव:", placeholder="उदा. राहुल प्रकाश जोशी")
        
        c_mob, c_age = st.columns([2, 1])
        with c_mob:
            r_mob = st.text_input("📱 मोबाईल नंबर:", placeholder="9423759186", max_chars=10)
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
                        time.sleep(1)
                        st.rerun()
                except Exception as e:
                    st.error(f"नोंदणी त्रुटी: {e}")

    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown(f"<div style='text-align:center; padding-top:20px; font-size:12.5px; font-weight:700; color:{th['font_accent']};'>{th['footer_text']} AyurVeda AI | Avishkar Alase</div>", unsafe_allow_html=True)
    st.stop()

# =========================================================================
# 🎯 DYNAMIC MODEL DISCOVERY & GEMINI CALLS
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
# अस्सल फोटोसारखी A4 HANDWRITTEN NOTE RENDERER
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
                color: white; border: none; padding: 12px 24px; font-size: 15px; font-weight: 800;
                border-radius: 12px; cursor: pointer; box-shadow: 0 4px 14px rgba(2,132,199,0.35);
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
# 👤 VIP SIDEBAR - विद्यार्थी आयडेंटिटी कार्ड आणि सेव्ह केलेल्या नोट्स
# =========================================================================
prof = st.session_state.profile or {}
s_name = prof.get("full_name") or "विद्यार्थी"
s_college = prof.get("college_name") or "Ayurvedic Medical College"
s_year = prof.get("bams_year") or "BAMS Scholar"
s_mob = prof.get("mobile_no") or "-"
s_age = prof.get("age") or "-"
s_email = st.session_state.get("user_email") or "Logged In"

with st.sidebar:
    st.markdown("### 🎓 विद्यार्थी आयडेंटिटी कार्ड")
    st.markdown(f"""
    <div class="student-id-card">
        <h4 style="margin:0 0 5px 0; color:#064e3b; font-weight:900; font-size:17px;">👨‍⚕️ {s_name}</h4>
        <div style="font-size:13px; margin-bottom:3px;"><b>🏛️ कॉलेज:</b> {s_college}</div>
        <div style="font-size:13px; margin-bottom:3px;"><b>🎓 वर्ष:</b> {s_year}</div>
        <div style="font-size:12.5px; color:#475569;"><b>📱 मो.:</b> {s_mob} | <b>वय:</b> {s_age}</div>
        <div style="font-size:11.5px; color:#059669; margin-top:5px; word-break:break-all;"><b>📧:</b> {s_email}</div>
    </div>
    """, unsafe_allow_html=True)

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

    st.write("---")
    st.markdown("### 📚 माझ्या सेव्ह केलेल्या नोट्स")
    try:
        notes_res = supabase.table("user_notes").select("*").eq("user_id", st.session_state.user_id).order("created_at", desc=True).execute()
        if not notes_res.data:
            st.info("अद्याप कोणतीही नोट सेव्ह केलेली नाही.")
        else:
            for item in notes_res.data:
                with st.expander(f"📌 {item.get('subject', '')} - {item.get('topic', '')[:16]}"):
                    st.caption(f"{item.get('created_at', '')[:10]} | {item.get('study_mode', '')}")
                    st.write(item.get("content", "")[:180] + "...")
                    if st.button("🗑️ हटवा", key=f"del_{item['id']}"):
                        supabase.table("user_notes").delete().eq("id", item["id"]).execute()
                        st.success("हटवले!")
                        st.rerun()
    except Exception as e:
        st.error(f"नोट्स लोड करताना त्रुटी: {e}")

# =========================================================================
# 🌿 मुख्य VIP स्टुडिओ (५ टॅब्स)
# =========================================================================
st.markdown(f"""
<div class="vip-navbar">
    <div style="display:flex; align-items:center; gap:10px;">
        <div style="font-size:26px;">{th['icon']}</div>
        <div>
            <div class="brand-title">🌿 AyurVeda AI Studio</div>
            <small style="color:{th['font_accent']}; font-weight:800; font-size:11.5px;">{th['title_sub']}</small>
        </div>
    </div>
    <div class="author-badge">Avishkar Alase ✓</div>
</div>
""", unsafe_allow_html=True)

tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📖 BAMS स्टडी नोट्स व प्रश्नसंच (Syllabus & PYQ)",
    "🧪 औषध घटक व निर्माण विधी (Medicine & Manufacturing)",
    "🎯 AI BAMS Viva-Voce Simulator (तोंडी परीक्षा)",
    "🩺 Clinical Case Study (केस प्रेझेंटेशन)",
    "🔬 Research & Evidence (वैज्ञानिक संशोधन)"
])

# =========================================================================
# TAB 1: SYLLABUS STUDY NOTES & UNIVERSITY PYQ SOLVER
# =========================================================================
with tab1:
    st.markdown(f"""
    <div class="vip-hero">
        <div class="festive-tag">{th['tag']}</div>
        <h3 style="margin:0 0 4px 0; font-weight:900; font-size:20px;">🎯 BAMS A4 बॉलपेन Handwritten नोट्स व PYQ Solver</h3>
        <p style="margin:0; font-size:13px; opacity:0.95;">ठळक मुख्य हेडिंग, सुवाच्य अक्षरे, महत्वाच्या शब्दांना <b>Red Highlight</b>, फ्लोचार्ट आणि मागील ५ वर्षांचे विद्यापीठ प्रश्नोत्तर.</p>
    </div>
    """, unsafe_allow_html=True)

    bams_year = st.selectbox(
        "🎓 BAMS वर्ष निवडा (Academic Year):",
        [
            "BAMS 1st Professional (प्रथम वर्ष)",
            "BAMS 2nd Professional (द्वितीय वर्ष)",
            "BAMS 3rd Professional (तृतीय वर्ष)",
            "BAMS Final Professional (अंतिम वर्ष)"
        ]
    )

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

    study_mode = st.selectbox(
        "🎯 अभ्यासाचा प्रकार निवडा (Study Mode):",
        [
            "📖 Comprehensive Notes (संपूर्ण सविस्तर अभ्यास नोट्स)",
            "📋 A4 Blue Ballpen Handwritten Sheet (अस्सल A4 पेन नोट्स)",
            "🎯 MUHS / NCISM Past 5 Years Questions & Model Answer Key",
            "📜 Only Shlokas & Meanings (फक्त मूळ श्लोक, अन्वय व अर्थ)",
            "📝 10-Mark LAQ Answer Format (दीर्घोत्तरी प्रश्न-उत्तर फॉरमॅट)",
            "⚡ Quick Revision / Viva Voce Points (तोंडी परीक्षेसाठी महत्त्वाचे मुद्दे)"
        ]
    )

    language_preference = st.radio(
        "🌐 माध्यम निवडा (Select Study Medium):",
        [
            "🚩 मराठी (संस्कृत + अर्थ)",
            "🌿 Simple English + Sanskrit"
        ],
        horizontal=True
    )

    topic = st.text_input(
        "🔍 अभ्यासाचा विषय / प्रश्न टाका:",
        placeholder="उदा. Virya, Ojas, Pitta Dosha, Rakta Dhatu, Ashwagandha, Agada"
    )

    # Session state variables to ensure notes persist across reruns
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

    generate_notes_btn = st.button("🚀 सविस्तर अभ्यास नोट्स तयार करा", key="btn_notes", use_container_width=True)

    if generate_notes_btn:
        if not topic.strip():
            st.warning("⚠️ कृपया अभ्यासाचा विषय प्रविष्ट करा.")
        else:
            is_marathi = "मराठी" in language_preference

            # Case A: A4 Blue Ballpen Handwritten Sheet
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
                with st.spinner("✍️ AI अस्सल वहीच्या पानावर फोटोसारख्या नोट्स तयार करत आहे..."):
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

            # Case B: MUHS / NCISM Past 5 Years Questions
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
                with st.spinner("🎯 AI विद्यापीठ मागील ५ वर्षांचे प्रश्न व मॉडेल आन्सर तयार करत आहे..."):
                    try:
                        pyq_res = cached_ask_gemini(pyq_prompt, as_json=False)
                        st.session_state.current_generated_note = pyq_res
                        st.session_state.current_note_type = "text"
                        st.session_state.current_topic = topic
                        st.session_state.current_subject = subject
                        st.session_state.current_mode = study_mode
                    except Exception as e:
                        st.error(f"त्रुटी: {e}")

            # Case C: Comprehensive Notes (14 Exhaustive Modules)
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
                with st.spinner(f"⚡ AI Professor '{topic}' वर सविस्तर नोट्स तयार करत आहेत..."):
                    try:
                        notes_res = cached_ask_gemini(system_instruction, as_json=False)
                        st.session_state.current_generated_note = notes_res
                        st.session_state.current_note_type = "text"
                        st.session_state.current_topic = topic
                        st.session_state.current_subject = subject
                        st.session_state.current_mode = study_mode
                    except Exception as e:
                        st.error(f"त्रुटी: {e}")

    # Display & Save Section
    if st.session_state.current_generated_note:
        c_type = st.session_state.current_note_type
        c_data = st.session_state.current_generated_note
        c_top = st.session_state.current_topic
        c_sub = st.session_state.current_subject
        c_mod = st.session_state.current_mode

        col_s1, col_s2 = st.columns([1, 1])
        with col_s1:
            if st.button("💾 ही नोट माझ्या खात्यात सेव्ह करा", key="save_n_tab1_fix", use_container_width=True):
                try:
                    save_payload = json.dumps(c_data) if c_type == "a4_sheet" else str(c_data)
                    supabase.table("user_notes").insert({
                        "user_id": st.session_state.user_id,
                        "subject": c_sub,
                        "topic": c_top,
                        "study_mode": c_mod,
                        "content": save_payload
                    }).execute()
                    st.success("✅ नोट तुमच्या खात्यात यशस्वीरीत्या सेव्ह झाली!")
                    time.sleep(1)
                    st.rerun()
                except Exception as s_err:
                    st.error(f"सेव्ह करताना त्रुटी: {s_err}")
        with col_s2:
            share_preview = f"🌿 *AyurVeda AI Notes*\n📚 *विषय:* {c_sub}\n🎯 *टॉपिक:* {c_top}\n\nAyurVeda AI Studio वर तयार केलेली नोट!"
            encoded_share = urllib.parse.quote(share_preview)
            st.link_button("📲 WhatsApp वर Share करा", f"[https://api.whatsapp.com/send?text=](https://api.whatsapp.com/send?text=){encoded_share}", use_container_width=True)

        if c_type == "a4_sheet":
            is_m = "मराठी" in language_preference
            a4_html = render_photo_identical_sheet(c_data, c_sub, c_top, is_marathi=is_m)
            st.components.v1.html(a4_html, height=1300, scrolling=True)
        else:
            html_content = markdown.markdown(c_data, extensions=['tables', 'fenced_code'])
            html_export = f"""<!DOCTYPE html>
<html lang="mr">
<head>
<meta charset="UTF-8">
<title>{c_top} - BAMS Comprehensive Notes</title>
<link href="[https://fonts.googleapis.com/css2?family=Mukta:wght@400;600;700;800;900&display=swap](https://fonts.googleapis.com/css2?family=Mukta:wght@400;600;700;800;900&display=swap)" rel="stylesheet">
<style>
    body {{ font-family: 'Mukta', sans-serif; line-height: 1.8; padding: 30px; color: #111827; max-width: 820px; margin: auto; }}
    table {{ width: 100%; border-collapse: collapse; margin: 15px 0; }}
    th, td {{ border: 1px solid #4b5563; padding: 8px 10px; }}
    blockquote {{ border-left: 4px solid #000; margin: 12px 0; padding: 10px 16px; background: #f8fafc; font-weight: 700; }}
</style>
</head>
<body>
    <h2>🌿 AyurVeda AI - {c_top}</h2>
    <div><b>विद्यार्थी:</b> {s_name} | <b>विषय:</b> {c_sub}</div>
    <hr>
    <div>{html_content}</div>
</body>
</html>"""
            st.download_button(
                label="📥 नोट्स सेव्ह करा (Printable HTML)",
                data=html_export.encode('utf-8'),
                file_name=f"{c_top.replace(' ', '_')}_Notes.html",
                mime="text/html",
                use_container_width=True
            )
            st.markdown(f'<div style="background:#fff; border-radius:18px; padding:22px; margin-top:15px; border:1.8px solid {th["border_color"]}; line-height:1.8;">{c_data}</div>', unsafe_allow_html=True)

# =========================================================================
# TAB 2: MEDICINE FORMULATION & MANUFACTURING
# =========================================================================
with tab2:
    st.markdown("""
    <div class="vip-hero" style="background: linear-gradient(135deg, #0f766e 0%, #0d9488 100%) !important; border-color: #5eead4;">
        <div class="festive-tag" style="background: rgba(255,255,255,0.18);">🌿 रसौषधी विधी</div>
        <h3 style="margin:0 0 4px 0; font-weight:900; font-size:20px;">🧪 रसशास्त्र व भैषज्य कल्पना स्पेशल</h3>
        <p style="margin:0; font-size:13px; opacity:0.95;">आयुर्वेदिक औषध घटक व सविस्तर निर्माण विधी सोप्या स्टेप्समध्ये शिका.</p>
    </div>
    """, unsafe_allow_html=True)

    dosage_form = st.selectbox(
        "🏺 औषधाचा प्रकार (Dosage Form):",
        ["Vati / Gutika (गोळी / वटी)", "Churna (चूर्ण)", "Asava & Arishta (आसव व अरिष्ट)", "Taila / Ghrita (सिद्ध तेल व घृत)", "Bhasma & Pishti (भस्म व पिष्टी)"]
    )
    m_lang = st.radio("🌐 भाषा:", ["Simple Indian English", "मराठी"], horizontal=True, key="m_lang")
    medicine_name = st.text_input("💊 गोळी किंवा औषधाचे नाव टाका:", placeholder="उदा. आरोग्यवर्धिनी वटी किंवा चंद्रप्रभावटी")

    if "current_med_note" not in st.session_state:
        st.session_state.current_med_note = None

    if st.button("🔬 औषध घटक व बनवण्याची कृती शिका", key="btn_med", use_container_width=True):
        if not medicine_name.strip():
            st.warning("⚠️ कृपया औषधाचे नाव टाका.")
        else:
            with st.spinner(f"🔬 AI तज्ज्ञ '{medicine_name}' ची निर्माण पद्धत तयार करत आहे..."):
                try:
                    med_prompt = f"Explain manufacturing of {medicine_name} ({dosage_form}) in {m_lang} with ingredients table, purification, and steps in deep detail."
                    res_text = cached_ask_gemini(med_prompt, as_json=False)
                    st.session_state.current_med_note = res_text
                except Exception as e:
                    st.error(f"त्रुटी: {e}")

    if st.session_state.current_med_note:
        st.markdown(st.session_state.current_med_note)
        if st.button("💾 ही औषध कृती खात्यात सेव्ह करा", key="save_med_btn", use_container_width=True):
            try:
                supabase.table("user_notes").insert({
                    "user_id": st.session_state.user_id,
                    "subject": "Rasashastra & Bhaishajya Kalpana",
                    "topic": medicine_name,
                    "study_mode": dosage_form,
                    "content": st.session_state.current_med_note
                }).execute()
                st.success("✅ खात्यात सेव्ह झाले!")
                time.sleep(1)
                st.rerun()
            except Exception as e:
                st.error(f"त्रुटी: {e}")

# =========================================================================
# TAB 3: AI BAMS VIVA-VOCE SIMULATOR
# =========================================================================
with tab3:
    st.markdown("""
    <div class="vip-hero" style="background: linear-gradient(135deg, #1e1b4b 0%, #312e81 100%) !important; border-color: #a5b4fc;">
        <div class="festive-tag" style="background: rgba(255,255,255,0.18);">🎓 तोंडी परीक्षा सिम्युलेटर</div>
        <h3 style="margin:0 0 4px 0; font-weight:900; font-size:20px;">🎯 BAMS University Practical & Viva Simulator</h3>
        <p style="margin:0; font-size:13px; opacity:0.95;">External Examiner च्या दृष्टिकोनातून विचारले जाणारे ५ महत्त्वाचे प्रश्न व आदर्श उत्तरे.</p>
    </div>
    """, unsafe_allow_html=True)

    viva_sub = st.selectbox(
        "📚 Viva साठी विषय:",
        ["Kriya Sharir", "Rachana Sharir", "Dravyaguna", "Rasa Shastra", "Agada Tantra", "Kayachikitsa", "Shalya Tantra"],
        key="viva_sub"
    )
    viva_lang = st.radio("🌐 Viva भाषा:", ["मराठी + Sanskrit Terms", "Simple Indian English"], horizontal=True, key="viva_lang")
    viva_topic = st.text_input("🎙️ Examiner कोणत्या विषयावर प्रश्न विचारतील?", placeholder="उदा. Pitta Sthana, Ashwagandha Guna, Vatsanabha Shodhana", key="viva_top")

    if "current_viva_note" not in st.session_state:
        st.session_state.current_viva_note = None

    if st.button("🔥 AI Examiner कडून तोंडी परीक्षा प्रश्न घ्या", key="btn_viva", use_container_width=True):
        if not viva_topic.strip():
            st.warning("⚠️ कृपया विषयाचे नाव टाका.")
        else:
            with st.spinner("🎙️ External Examiner प्रश्न तयार करत आहेत..."):
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

    if st.session_state.current_viva_note:
        st.markdown(st.session_state.current_viva_note)
        if st.button("💾 ही Viva प्रश्नावली सेव्ह करा", key="save_viva_btn", use_container_width=True):
            try:
                supabase.table("user_notes").insert({
                    "user_id": st.session_state.user_id,
                    "subject": viva_sub,
                    "topic": viva_topic,
                    "study_mode": "Viva-Voce Questions",
                    "content": st.session_state.current_viva_note
                }).execute()
                st.success("✅ खात्यात सेव्ह झाले!")
                time.sleep(1)
                st.rerun()
            except Exception as e:
                st.error(f"त्रुटी: {e}")

# =========================================================================
# TAB 4: CLINICAL CASE STUDY
# =========================================================================
with tab4:
    st.markdown("""
    <div class="vip-hero" style="background: linear-gradient(135deg, #0369a1 0%, #0284c7 100%) !important; border-color: #7dd3fc;">
        <div class="festive-tag" style="background: rgba(255,255,255,0.18);">🩺 क्लिनिकल ओपीडी व IPD केसशीट</div>
        <h3 style="margin:0 0 4px 0; font-weight:900; font-size:20px;">📋 Complete Ayurvedic Clinical Case Presentation</h3>
        <p style="margin:0; font-size:13px; opacity:0.95;">Kayachikitsa, Panchakarma व Shalya साठी अष्टविध परीक्षा, संप्राप्ती विघटन, दीपन-पाचन व प्रत्यक्ष उपचार योजना.</p>
    </div>
    """, unsafe_allow_html=True)

    case_subject = st.selectbox(
        "🏥 क्लिनिकल विभाग (Department):",
        ["Kayachikitsa (कायचिकित्सा)", "Panchakarma (पंचकर्म)", "Shalya Tantra (शल्य)", "Shalakya (नेत्र/कर्ण/नासा)", "Stri Roga & Prasuti (स्त्रीरोग)", "Kaumarbhritya (बालरोग)"],
        key="case_sub"
    )
    case_lang = st.radio("🌐 भाषा:", ["मराठी + Clinical English", "Simple Indian English + Sanskrit"], horizontal=True, key="cs_lang")
    case_topic = st.text_input("🩺 आजाराचे नाव / मुख्य लक्षणे टाका:", placeholder="उदा. Amlapitta (GERD), Sandhivata (Osteoarthritis), Tamaka Shwasa (Asthma)", key="cs_top")

    if "current_case_note" not in st.session_state:
        st.session_state.current_case_note = None

    if st.button("📋 संपूर्ण क्लिनिकल केसशीट तयार करा", key="btn_case", use_container_width=True):
        if not case_topic.strip():
            st.warning("⚠️ कृपया आजाराचे नाव टाका.")
        else:
            with st.spinner(f"🩺 AI क्लिनिकल तज्ज्ञ '{case_topic}' ची परिपूर्ण हॉस्पिटल केसशीट तयार करत आहे..."):
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

    if st.session_state.current_case_note:
        st.markdown(st.session_state.current_case_note)
        if st.button("💾 ही केसशीट खात्यात सेव्ह करा", key="save_case_btn", use_container_width=True):
            try:
                supabase.table("user_notes").insert({
                    "user_id": st.session_state.user_id,
                    "subject": case_subject,
                    "topic": case_topic,
                    "study_mode": "Clinical Case Study",
                    "content": st.session_state.current_case_note
                }).execute()
                st.success("✅ खात्यात सेव्ह झाले!")
                time.sleep(1)
                st.rerun()
            except Exception as e:
                st.error(f"त्रुटी: {e}")

# =========================================================================
# TAB 5: RESEARCH & EVIDENCE
# =========================================================================
with tab5:
    st.markdown("""
    <div class="vip-hero" style="background: linear-gradient(135deg, #4338ca 0%, #6366f1 100%) !important; border-color: #c7d2fe;">
        <div class="festive-tag" style="background: rgba(255,255,255,0.18);">🔬 सायंटिफिक ॲव्हिडन्स व क्लिनिकल ट्रायल्स</div>
        <h3 style="margin:0 0 4px 0; font-weight:900; font-size:20px;">🧬 Evidence-Based Modern Ayurvedic Research</h3>
        <p style="margin:0; font-size:13px; opacity:0.95;">Active Phytochemicals, PubMed/Clinical Trial पुरावे, Pharmacology आणि Safety & Toxicity प्रोफाईल.</p>
    </div>
    """, unsafe_allow_html=True)

    res_topic = st.text_input("🔬 औषधी वनस्पती / घटकाचे नाव टाका:", placeholder="उदा. Withania somnifera (Ashwagandha), Tinospora cordifolia (Guduchi)", key="res_top")

    if "current_res_note" not in st.session_state:
        st.session_state.current_res_note = None

    if st.button("🧬 वैज्ञानिक संशोधन व क्लिनिकल पुरावे शोधा", key="btn_research", use_container_width=True):
        if not res_topic.strip():
            st.warning("⚠️ कृपया संशोधन द्रव्याचे नाव टाका.")
        else:
            with st.spinner(f"🧬 AI संशोधक '{res_topic}' चे पुरावे संकलित करत आहे..."):
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

    if st.session_state.current_res_note:
        st.markdown(st.session_state.current_res_note)
        if st.button("💾 हा संशोधन अहवाल सेव्ह करा", key="save_res_btn", use_container_width=True):
            try:
                supabase.table("user_notes").insert({
                    "user_id": st.session_state.user_id,
                    "subject": "Research & Evidence",
                    "topic": res_topic,
                    "study_mode": "Modern Pharmacology",
                    "content": st.session_state.current_res_note
                }).execute()
                st.success("✅ खात्यात सेव्ह झाले!")
                time.sleep(1)
                st.rerun()
            except Exception as e:
                st.error(f"त्रुटी: {e}")

# --- Footer ---
st.markdown(f"""
<div style="text-align:center; padding:30px 10px 15px 10px; font-size:13px; color:{th['font_accent']}; font-weight:800;">
    {th['footer_text']} <strong>AyurVeda AI Studio</strong> | Developed by <strong>Avishkar Alase</strong>
</div>
""", unsafe_allow_html=True)
