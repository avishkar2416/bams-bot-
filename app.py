import streamlit as st
from google import genai
from google.genai import types
import json
import time


# ============================================================
# 🌿 AYURVEDA AI — PREMIUM BAMS STUDY STUDIO
# ============================================================

st.set_page_config(
    page_title="AyurVeda AI | BAMS Study Studio",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="collapsed"
)


# ============================================================
# 🎨 PREMIUM GLOBAL CSS
# ============================================================

st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=Mukta:wght@400;500;600;700;800&display=swap');


/* =========================================================
   ROOT
   ========================================================= */

:root {
    --orange: #ea580c;
    --saffron: #d97706;
    --gold: #f59e0b;
    --dark-red: #7f1d1d;
    --cream: #fffaf0;
    --ink: #172033;
    --muted: #667085;
}


/* =========================================================
   MAIN APP
   ========================================================= */

.stApp {

    background:
        radial-gradient(
            circle at 5% 0%,
            rgba(251,191,36,0.18),
            transparent 25%
        ),
        radial-gradient(
            circle at 95% 8%,
            rgba(234,88,12,0.12),
            transparent 24%
        ),
        linear-gradient(
            180deg,
            #fffaf0 0%,
            #fffdf9 45%,
            #fff7ed 100%
        ) !important;

    font-family:
        'Mukta',
        'Plus Jakarta Sans',
        sans-serif !important;

    color: var(--ink);
}


/* subtle pattern */

.stApp::before {

    content: "";

    position: fixed;

    inset: 0;

    pointer-events: none;

    opacity: 0.18;

    background-image:
        radial-gradient(
            #b45309 0.6px,
            transparent 0.6px
        );

    background-size: 25px 25px;

    mask-image:
        linear-gradient(
            to bottom,
            black,
            transparent 75%
        );

    z-index: 0;
}


/* =========================================================
   STREAMLIT CLEANUP
   ========================================================= */

#MainMenu {
    visibility: hidden;
}

footer {
    visibility: hidden;
}

header[data-testid="stHeader"] {
    background: transparent !important;
}

div[data-testid="stDecoration"] {
    display: none;
}

.block-container {

    max-width: 1380px;

    padding-top:
        1.1rem !important;

    padding-bottom:
        3rem !important;
}


/* =========================================================
   GLOBAL TEXT
   ========================================================= */

h1,
h2,
h3,
h4,
h5,
p,
label,
span {

    font-family:
        'Mukta',
        'Plus Jakarta Sans',
        sans-serif !important;

    color: var(--ink);
}


/* =========================================================
   NAVBAR
   ========================================================= */

.premium-nav {

    position: relative;

    overflow: hidden;

    display: flex;

    align-items: center;

    justify-content: space-between;

    gap: 20px;

    padding: 14px 17px;

    margin-bottom: 20px;

    border:
        1px solid
        rgba(245,158,11,0.30);

    border-radius: 24px;

    background:
        rgba(255,255,255,0.76);

    backdrop-filter:
        blur(22px);

    -webkit-backdrop-filter:
        blur(22px);

    box-shadow:
        0 16px 45px
        rgba(120,53,15,0.09);
}


.premium-nav::after {

    content: "";

    position: absolute;

    width: 230px;

    height: 230px;

    right: -110px;

    top: -150px;

    border-radius: 50%;

    background:
        rgba(251,191,36,0.16);
}


.brand {

    display: flex;

    align-items: center;

    gap: 12px;

    position: relative;

    z-index: 2;
}


.brand-mark {

    width: 48px;

    height: 48px;

    display: flex;

    align-items: center;

    justify-content: center;

    border-radius: 16px;

    background:
        linear-gradient(
            145deg,
            #fff8dc,
            #fef3c7
        );

    border:
        1px solid
        #f3ce68;

    box-shadow:
        inset 0 1px white,
        0 8px 20px
        rgba(180,83,9,0.13);

    font-size: 25px;
}


.brand-title {

    font-family:
        'Plus Jakarta Sans',
        sans-serif !important;

    font-size: 20px;

    font-weight: 800;

    margin: 0;

    background:
        linear-gradient(
            90deg,
            #9a3412,
            #d97706,
            #a16207
        );

    -webkit-background-clip: text;

    -webkit-text-fill-color: transparent;
}


.brand-sub {

    margin-top: 2px;

    color:
        #9a5a13 !important;

    font-size: 10px;

    font-weight: 800;

    letter-spacing:
        0.6px;
}


.creator-pill {

    position: relative;

    z-index: 2;

    padding:
        9px 14px;

    border:
        1px solid
        rgba(245,158,11,0.28);

    border-radius:
        999px;

    background:
        linear-gradient(
            180deg,
            #fffdf5,
            #fff6dc
        );

    color:
        #8a4b08 !important;

    font-size:
        12px;

    font-weight:
        800;

    box-shadow:
        0 6px 18px
        rgba(180,83,9,0.08);
}


/* =========================================================
   HERO
   ========================================================= */

.hero {

    position: relative;

    overflow: hidden;

    padding:
        32px 32px 29px;

    margin-bottom:
        22px;

    border-radius:
        29px;

    background:
        radial-gradient(
            circle at 86% 12%,
            rgba(255,255,255,0.18),
            transparent 20%
        ),
        radial-gradient(
            circle at 3% 100%,
            rgba(251,191,36,0.20),
            transparent 28%
        ),
        linear-gradient(
            135deg,
            #9a3412,
            #c2410c 50%,
            #7f1d1d
        );

    border:
        1px solid
        rgba(254,240,138,0.65);

    box-shadow:
        0 24px 55px
        rgba(127,29,29,0.20);
}


.hero::after {

    content: "ॐ";

    position: absolute;

    right: 38px;

    top: -15px;

    font-family: serif;

    font-size: 170px;

    line-height: 1;

    color: white;

    opacity: 0.07;
}


.hero-kicker {

    display: inline-flex;

    align-items: center;

    padding:
        6px 12px;

    border:
        1px solid
        rgba(255,255,255,0.30);

    border-radius:
        999px;

    background:
        rgba(255,255,255,0.12);

    color:
        #ffffff !important;

    font-size:
        11px;

    font-weight:
        800;

    letter-spacing:
        0.6px;
}


.hero-title {

    color:
        #ffffff !important;

    font-family:
        'Plus Jakarta Sans',
        sans-serif !important;

    font-size:
        31px;

    font-weight:
        800;

    margin:
        12px 0 7px;
}


.hero-description {

    color:
        rgba(255,255,255,0.91) !important;

    max-width:
        900px;

    font-size:
        14px;

    line-height:
        1.65;

    margin:
        0;
}


/* =========================================================
   SECTION TITLE
   ========================================================= */

.section-title {

    display:
        flex;

    align-items:
        center;

    gap:
        10px;

    margin:
        5px 0 12px;

    color:
        #6b3410 !important;

    font-family:
        'Plus Jakarta Sans',
        sans-serif !important;

    font-size:
        15px;

    font-weight:
        800;
}


.section-title::before {

    content: "";

    width:
        4px;

    height:
        19px;

    border-radius:
        10px;

    background:
        linear-gradient(
            #f59e0b,
            #ea580c
        );
}


/* =========================================================
   INPUTS
   ========================================================= */

div[data-baseweb="select"] > div,
div[data-baseweb="input"] > div,
div[data-baseweb="textarea"] > div {

    background:
        rgba(255,255,255,0.94) !important;

    border:
        1px solid
        #ead8c2 !important;

    border-radius:
        15px !important;

    min-height:
        48px;

    box-shadow:
        0 4px 15px
        rgba(120,53,15,0.035) !important;

    transition:
        all 0.2s ease !important;
}


div[data-baseweb="select"] > div:hover,
div[data-baseweb="input"] > div:hover,
div[data-baseweb="textarea"] > div:hover {

    border-color:
        #e7a51d !important;

    box-shadow:
        0 8px 25px
        rgba(217,119,6,0.12) !important;
}


input,
textarea {

    color:
        #172033 !important;

    font-weight:
        600 !important;
}


[data-testid="stWidgetLabel"] p {

    color:
        #59320e !important;

    font-weight:
        800 !important;

    font-size:
        13px !important;
}


/* =========================================================
   RADIO
   ========================================================= */

div[role="radiogroup"] {

    gap:
        5px !important;
}


div[role="radiogroup"] label {

    background:
        rgba(255,255,255,0.70);

    border:
        1px solid
        rgba(180,83,9,0.12);

    border-radius:
        12px;

    padding:
        7px 10px;

    transition:
        0.2s ease;
}


div[role="radiogroup"] label:hover {

    border-color:
        #e8ad36;

    transform:
        translateY(-1px);
}


/* =========================================================
   BUTTON
   ========================================================= */

div.stButton > button {

    min-height:
        54px !important;

    border:
        none !important;

    border-radius:
        17px !important;

    color:
        #ffffff !important;

    font-family:
        'Plus Jakarta Sans',
        sans-serif !important;

    font-size:
        14px !important;

    font-weight:
        800 !important;

    background:
        linear-gradient(
            135deg,
            #ea580c,
            #d97706 52%,
            #b45309
        ) !important;

    box-shadow:
        0 13px 30px
        rgba(194,65,12,0.25) !important;

    transition:
        all 0.18s ease !important;
}


div.stButton > button:hover {

    transform:
        translateY(-2px) !important;

    box-shadow:
        0 18px 38px
        rgba(194,65,12,0.34) !important;
}


div.stButton > button:active {

    transform:
        scale(0.98) !important;
}


/* =========================================================
   TABS
   ========================================================= */

.stTabs [data-baseweb="tab-list"] {

    gap:
        7px;

    padding:
        6px;

    border-radius:
        19px;

    background:
        rgba(255,255,255,0.66);

    border:
        1px solid
        rgba(180,83,9,0.11);

    box-shadow:
        0 10px 28px
        rgba(120,53,15,0.05);
}


.stTabs [data-baseweb="tab"] {

    height:
        48px;

    padding:
        0 20px !important;

    border-radius:
        13px !important;

    color:
        #71400f !important;

    font-weight:
        800 !important;

    border:
        none !important;
}


.stTabs [aria-selected="true"] {

    background:
        linear-gradient(
            135deg,
            #fff3cf,
            #ffe4b2
        ) !important;

    color:
        #9a3412 !important;

    box-shadow:
        0 6px 18px
        rgba(217,119,6,0.13);
}


.stTabs [aria-selected="true"] * {

    color:
        #9a3412 !important;
}


/* =========================================================
   RESULT CARD
   ========================================================= */

.result-card {

    padding:
        22px 24px;

    border:
        1px solid
        rgba(180,83,9,0.13);

    border-radius:
        22px;

    background:
        rgba(255,255,255,0.76);

    box-shadow:
        0 14px 40px
        rgba(120,53,15,0.06);

    margin-top:
        10px;
}


/* =========================================================
   MEDICINE HERO
   ========================================================= */

.medicine-hero {

    background:
        radial-gradient(
            circle at 90% 10%,
            rgba(255,255,255,0.16),
            transparent 20%
        ),
        linear-gradient(
            135deg,
            #075e54,
            #0f766e 52%,
            #115e59
        );

    box-shadow:
        0 24px 55px
        rgba(15,118,110,0.20);
}


/* =========================================================
   SUCCESS
   ========================================================= */

div[data-testid="stAlert"] {

    border-radius:
        15px !important;
}


/* =========================================================
   FOOTER
   ========================================================= */

.footer {

    text-align:
        center;

    margin-top:
        42px;

    padding:
        20px 10px 5px;

    color:
        #8a5a20 !important;

    font-size:
        12px;

    font-weight:
        700;
}


.footer-line {

    width:
        90px;

    height:
        1px;

    margin:
        0 auto 12px;

    background:
        linear-gradient(
            90deg,
            transparent,
            #d97706,
            transparent
        );
}


/* =========================================================
   MOBILE
   ========================================================= */

@media (max-width: 768px) {

    .block-container {

        padding-left:
            0.8rem !important;

        padding-right:
            0.8rem !important;
    }


    .premium-nav {

        padding:
            11px 12px;

        border-radius:
            19px;
    }


    .brand-mark {

        width:
            42px;

        height:
            42px;

        font-size:
            22px;
    }


    .brand-title {

        font-size:
            16px;
    }


    .brand-sub {

        font-size:
            8px;

        letter-spacing:
            0.3px;
    }


    .creator-pill {

        font-size:
            9px;

        padding:
            7px 9px;
    }


    .hero {

        padding:
            24px 19px;

        border-radius:
            23px;
    }


    .hero-title {

        font-size:
            23px;
    }


    .hero-description {

        font-size:
            12.5px;
    }


    .stTabs [data-baseweb="tab"] {

        padding:
            0 9px !important;

        font-size:
            11px !important;
    }

}

</style>
""", unsafe_allow_html=True)


# ============================================================
# 🔑 GEMINI API
# ============================================================

api_key = st.secrets.get(
    "GEMINI_API_KEY",
    ""
)

if not api_key:

    st.error(
        "⚠️ Streamlit Secrets मध्ये GEMINI_API_KEY configure करा."
    )

    st.stop()


client = genai.Client(
    api_key=api_key
)


# ============================================================
# 🤖 GEMINI FUNCTION
# ============================================================

@st.cache_data(
    show_spinner=False,
    ttl=86400
)
def cached_ask_gemini(
    prompt: str,
    as_json: bool = False
):

    model_name = "gemini-3.6-flash"

    last_error = None

    for attempt in range(3):

        try:

            config = None

            if as_json:

                config = types.GenerateContentConfig(
                    response_mime_type="application/json"
                )


            response = client.models.generate_content(

                model=model_name,

                contents=prompt,

                config=config
            )


            if response and response.text:

                return response.text


        except Exception as error:

            last_error = error

            error_text = str(error)

            if (
                "429" in error_text
                or
                "RESOURCE_EXHAUSTED" in error_text
            ):

                time.sleep(16)

            else:

                time.sleep(2)


    raise RuntimeError(
        f"तांत्रिक अडचण आली: {last_error}"
    )


# ============================================================
# 📝 A4 HANDWRITTEN SHEET
# ============================================================

def create_a4_handwritten_doc(
    data,
    subject_name,
    topic_name,
    is_marathi=True
):

    marks = data.get(
        "exam_marks",
        "१० गुण - दीर्घोत्तरी (LAQ)"
        if is_marathi
        else
        "10 Marks - LAQ"
    )


    title = data.get(
        "main_heading",
        topic_name
    )


    t1 = data.get(
        "entity_1",
        {}
    )


    t2 = data.get(
        "entity_2",
        {}
    )


    include_flowchart = data.get(
        "include_flowchart",
        False
    )


    # --------------------------------------------------------
    # LABELS
    # --------------------------------------------------------

    lbl_flow = (
        "संप्राप्ती प्रवाह तक्ता"
        if is_marathi
        else
        "PATHOGENESIS FLOWCHART"
    )

    lbl_points = (
        "परीक्षेसाठी महत्त्वाचे मुद्दे"
        if is_marathi
        else
        "HIGH-YIELD EXAM POINTS"
    )

    lbl_clinical = (
        "लक्षणे, विकार व चिकित्सा"
        if is_marathi
        else
        "CLINICAL / SYSTEMIC FEATURES"
    )

    lbl_key = (
        "★ मुख्य संकल्पना"
        if is_marathi
        else
        "★ KEY EXAM CONCEPT"
    )

    lbl_modern = (
        "★ आधुनिक वैद्यकीय सांगड"
        if is_marathi
        else
        "★ CONTEMPORARY / MODERN LINK"
    )

    lbl_table = (
        "★ परीक्षा तुलनात्मक तक्ता"
        if is_marathi
        else
        "★ QUICK EXAM COMPARISON"
    )

    lbl_feature = (
        "मुद्दा / लक्षण"
        if is_marathi
        else
        "Feature"
    )

    lbl_punch = (
        "✍️ परीक्षेसाठी मुख्य सूत्र"
        if is_marathi
        else
        "✍️ EXAM PUNCH LINE"
    )

    lbl_def = (
        "व्याख्या:"
        if is_marathi
        else
        "Definition:"
    )

    lbl_png = (
        "📸 A4 PNG जतन करा"
        if is_marathi
        else
        "📸 SAVE A4 PNG"
    )

    lbl_pdf = (
        "📄 PDF / PRINT"
        if is_marathi
        else
        "📄 PDF / PRINT"
    )


    # --------------------------------------------------------
    # FLOWCHART
    # --------------------------------------------------------

    flow_html = ""

    steps = data.get(
        "flowchart_steps",
        []
    )


    if include_flowchart and steps:

        parts = []

        for index, step in enumerate(steps):

            if index == len(steps) - 1:

                parts.append(
                    f'<div class="a4-cloud">{step}</div>'
                )

            else:

                parts.append(
                    f'<div class="a4-step">{step}</div>'
                )

                parts.append(
                    '<div class="a4-arrow">↓</div>'
                )


        flow_html = f"""
        <div class="a4-flow">

            <div class="a4-label">
                {lbl_flow}
            </div>

            <div class="a4-flow-body">
                {''.join(parts)}
            </div>

        </div>
        """


    # --------------------------------------------------------
    # POINTS
    # --------------------------------------------------------

    points_1 = "".join(

        f"<li>{point}</li>"

        for point in t1.get(
            "key_points",
            []
        )
    )


    points_2 = "".join(

        f"<li>{point}</li>"

        for point in t2.get(
            "key_points",
            []
        )
    )


    # --------------------------------------------------------
    # TABLE
    # --------------------------------------------------------

    table_rows = ""

    for row in data.get(
        "comparison_table",
        []
    ):

        table_rows += f"""
        <tr>

            <td>
                <b>
                    {row.get("feature","")}
                </b>
            </td>

            <td>
                {row.get("point_1","")}
            </td>

            <td>
                {row.get("point_2","")}
            </td>

        </tr>
        """


    table_html = ""

    if table_rows:

        table_html = f"""
        <div class="a4-section-title">
            {lbl_table}
        </div>

        <table class="a4-table">

            <thead>

                <tr>

                    <th style="width:25%;">
                        {lbl_feature}
                    </th>

                    <th>
                        {t1.get("title","Concept 1")}
                    </th>

                    <th>
                        {t2.get("title","Concept 2")}
                    </th>

                </tr>

            </thead>

            <tbody>
                {table_rows}
            </tbody>

        </table>
        """


    font_family = (
        "'Mukta', sans-serif"
        if is_marathi
        else
        "'Patrick Hand', 'Caveat', cursive, sans-serif"
    )


    # --------------------------------------------------------
    # A4 HTML
    #
    # IMPORTANT:
    # This is a normal string, NOT an f-string.
    # Therefore CSS {} will NEVER create Python
    # f-string syntax errors.
    # --------------------------------------------------------

    html = """
<!DOCTYPE html>

<html>

<head>

<meta charset="UTF-8">

<script
src="https://cdnjs.cloudflare.com/ajax/libs/html2canvas/1.4.1/html2canvas.min.js">
</script>

<style>

@import url(
'https://fonts.googleapis.com/css2?family=Patrick+Hand&family=Caveat:wght@600;700&family=Mukta:wght@500;600;700;800;900&display=swap'
);

* {
    box-sizing: border-box;
}

body {

    margin: 0;

    padding: 20px 10px;

    background: #edf1f6;

    display: flex;

    flex-direction: column;

    align-items: center;

    font-family: FONT_FAMILY;
}

.a4-actions {

    display: flex;

    gap: 10px;

    margin-bottom: 16px;

    font-family:
        Arial,
        sans-serif;
}

.a4-button {

    border: 0;

    border-radius: 11px;

    padding:
        11px 17px;

    color: white;

    font-weight: 800;

    cursor: pointer;

    background:
        linear-gradient(
            135deg,
            #0369a1,
            #0284c7
        );

    box-shadow:
        0 7px 18px
        rgba(3,105,161,.25);
}

.a4-button.green {

    background:
        linear-gradient(
            135deg,
            #047857,
            #059669
        );
}

.a4-paper {

    width:
        794px;

    min-height:
        1123px;

    position:
        relative;

    overflow:
        hidden;

    background:
        #fffef9;

    border:
        2px solid
        #17325f;

    box-shadow:
        0 18px 45px
        rgba(15,23,42,.18);

    padding:
        28px 31px;

    color:
        #17325f;

    font-size:
        15px;

    line-height:
        1.42;
}

.a4-paper::before {

    content: "";

    position:
        absolute;

    inset:
        0;

    pointer-events:
        none;

    opacity:
        .20;

    background:
        repeating-linear-gradient(
            0deg,
            transparent 0,
            transparent 29px,
            rgba(23,50,95,.08) 30px
        );
}

.a4-paper > * {

    position:
        relative;

    z-index:
        1;
}

.a4-header {

    display:
        flex;

    align-items:
        center;

    justify-content:
        space-between;

    gap:
        14px;

    padding-bottom:
        10px;

    margin-bottom:
        12px;

    border-bottom:
        2px solid
        #17325f;
}

.a4-title {

    width:
        69%;

    padding:
        8px 13px;

    border:
        2px solid
        #17325f;

    border-radius:
        10px;

    background:
        white;

    text-align:
        center;

    font-size:
        21px;

    font-weight:
        800;
}

.a4-title span {

    border-bottom:
        2px double
        #17325f;
}

.a4-marks {

    padding:
        6px 10px;

    border:
        2px solid
        #17325f;

    border-radius:
        8px;

    background:
        white;

    text-align:
        center;

    font-size:
        12px;

    font-weight:
        800;
}

.hl-red {

    display:
        inline-block;

    background:
        #ffe1e5;

    color:
        #b42318;

    padding:
        1px 4px;

    border:
        1px solid
        #fecdd3;

    border-radius:
        4px;

    font-weight:
        800;
}

.a4-flow {

    text-align:
        center;

    margin:
        7px 0 13px;
}

.a4-label {

    display:
        inline-block;

    padding:
        2px 10px;

    border:
        1.5px solid
        #17325f;

    border-radius:
        999px;

    background:
        white;

    font-size:
        12px;

    font-weight:
        800;
}

.a4-flow-body {

    margin-top:
        6px;
}

.a4-step {

    width:
        82%;

    margin:
        auto;

    padding:
        4px 9px;

    border:
        1.4px solid
        #17325f;

    border-radius:
        8px;

    background:
        white;

    font-size:
        13px;

    font-weight:
        600;
}

.a4-cloud {

    width:
        86%;

    margin:
        auto;

    padding:
        5px 10px;

    border:
        1.7px dashed
        #17325f;

    border-radius:
        14px;

    background:
        white;

    font-size:
        13px;

    font-weight:
        800;
}

.a4-arrow {

    margin:
        1px 0;

    font-weight:
        900;

    font-size:
        13px;
}

.a4-columns {

    display:
        flex;

    gap:
        14px;
}

.a4-column {

    flex:
        1;

    padding:
        0 5px;
}

.a4-column:first-child {

    border-right:
        1.3px dashed
        #17325f;
}

.a4-badge {

    display:
        inline-block;

    padding:
        2px 10px;

    margin-bottom:
        4px;

    border:
        1.5px solid
        #17325f;

    border-radius:
        999px;

    background:
        white;

    font-size:
        15px;

    font-weight:
        800;
}

.a4-definition {

    margin:
        3px 0 5px;

    font-size:
        13px;
}

.a4-section-title {

    margin:
        7px 0 3px;

    font-size:
        14px;

    font-weight:
        800;

    text-decoration:
        underline;
}

.a4-list {

    margin:
        3px 0 7px;

    padding-left:
        17px;

    font-size:
        13px;
}

.a4-list li {

    margin-bottom:
        3px;
}

.a4-key {

    padding:
        6px 9px;

    border:
        1.4px dashed
        #17325f;

    border-radius:
        8px;

    background:
        #fbfbf8;

    font-size:
        12.5px;

    line-height:
        1.4;
}

.a4-table {

    width:
        100%;

    border-collapse:
        collapse;

    margin:
        4px 0 9px;

    background:
        white;

    font-size:
        12.5px;
}

.a4-table th,
.a4-table td {

    padding:
        4px 7px;

    border:
        1.3px solid
        #17325f;

    text-align:
        left;
}

.a4-table th {

    background:
        #f8fafc;

    font-weight:
        800;
}

.a4-punch {

    margin-top:
        8px;

    padding-top:
        7px;

    border-top:
        2px solid
        #17325f;

    font-size:
        13.5px;

    font-weight:
        800;
}

.a4-footer {

    position:
        absolute;

    right:
        22px;

    bottom:
        8px;

    font-family:
        Arial,
        sans-serif;

    font-size:
        9px;

    opacity:
        .55;
}

@media print {

    body {

        padding:
            0;

        background:
            white;
    }

    .a4-actions {

        display:
            none;
    }

    .a4-paper {

        border:
            0;

        box-shadow:
            none;
    }
}

</style>

</head>

<body>

<div class="a4-actions">

<button
class="a4-button"
onclick="downloadA4()">
PNG_TEXT
</button>

<button
class="a4-button green"
onclick="window.print()">
PDF_TEXT
</button>

</div>


<div
class="a4-paper"
id="a4Canvas">


<div class="a4-header">

<div class="a4-title">

<span>
TITLE_TEXT
</span>

</div>


<div class="a4-marks">

<b>
SUBJECT_TEXT
</b>

<br>

<span class="hl-red">
🎯 MARKS_TEXT
</span>

</div>

</div>


FLOW_HTML


<div class="a4-columns">


<div class="a4-column">


<div class="a4-badge">
① T1_TITLE
</div>


<div class="a4-definition">

<b>
DEF_TEXT
</b>

T1_DEFINITION

</div>


<div class="a4-section-title">

POINTS_TEXT

</div>


<ul class="a4-list">

T1_POINTS

</ul>


<div class="a4-key">

<b>
KEY_TEXT
</b>

<br>

T1_KEY

</div>


</div>



<div class="a4-column">


<div class="a4-badge">

② T2_TITLE

</div>


<div class="a4-definition">

<b>
DEF_TEXT
</b>

T2_DEFINITION

</div>


<div class="a4-section-title">

CLINICAL_TEXT

</div>


<ul class="a4-list">

T2_POINTS

</ul>


<div class="a4-key">

<b>
MODERN_TEXT
</b>

<br>

T2_KEY

</div>


</div>

</div>


TABLE_HTML


<div class="a4-punch">

PUNCH_TEXT

→

"EXAM_PUNCH"

</div>


<div class="a4-footer">

🌿 AyurVeda AI • BAMS Study Studio • Avishkar Alase

</div>


</div>


<script>

function downloadA4() {

    const element =
        document.getElementById(
            "a4Canvas"
        );

    html2canvas(
        element,
        {
            scale: 2.2,
            useCORS: true,
            backgroundColor: "#fffef9"
        }
    ).then(
        function(canvas) {

            const link =
                document.createElement("a");

            link.download =
                "AyurVeda_AI_A4_Notes.png";

            link.href =
                canvas.toDataURL(
                    "image/png"
                );

            link.click();

        }
    );
}

</script>

</body>

</html>
"""


    # ========================================================
    # SAFE REPLACEMENTS
    # ========================================================

    replacements = {

        "FONT_FAMILY":
            font_family,

        "PNG_TEXT":
            lbl_png,

        "PDF_TEXT":
            lbl_pdf,

        "TITLE_TEXT":
            str(title),

        "SUBJECT_TEXT":
            str(subject_name),

        "MARKS_TEXT":
            str(marks),

        "FLOW_HTML":
            flow_html,

        "T1_TITLE":
            str(
                t1.get(
                    "title",
                    "Concept 1"
                )
            ),

        "T2_TITLE":
            str(
                t2.get(
                    "title",
                    "Concept 2"
                )
            ),

        "DEF_TEXT":
            lbl_def,

        "T1_DEFINITION":
            str(
                t1.get(
                    "definition",
                    ""
                )
            ),

        "T2_DEFINITION":
            str(
                t2.get(
                    "definition",
                    ""
                )
            ),

        "POINTS_TEXT":
            lbl_points,

        "CLINICAL_TEXT":
            lbl_clinical,

        "T1_POINTS":
            points_1,

        "T2_POINTS":
            points_2,

        "KEY_TEXT":
            lbl_key,

        "MODERN_TEXT":
            lbl_modern,

        "T1_KEY":
            str(
                t1.get(
                    "exam_key",
                    ""
                )
            ),

        "T2_KEY":
            str(
                t2.get(
                    "exam_key",
                    ""
                )
            ),

        "TABLE_HTML":
            table_html,

        "PUNCH_TEXT":
            lbl_punch,

        "EXAM_PUNCH":
            str(
                data.get(
                    "exam_punch_line",
                    ""
                )
            )
    }


    for key, value in replacements.items():

        html = html.replace(
            key,
            value
        )


    return html


# ============================================================
# 🌿 PREMIUM NAVBAR
# ============================================================

st.html("""
<div class="premium-nav">

    <div class="brand">

        <div class="brand-mark">
            🪔
        </div>

        <div>

            <div class="brand-title">
                🌿 AyurVeda AI
            </div>

            <div class="brand-sub">
                BAMS STUDY STUDIO • FESTIVE PREMIUM EDITION
            </div>

        </div>

    </div>


    <div class="creator-pill">
        ✦ Created by Avishkar Alase
    </div>

</div>
""")


# ============================================================
# 📖 MAIN TABS
# ============================================================

tab1, tab2 = st.tabs([
    "📖  BAMS Study Studio",
    "🧪  Medicine & Manufacturing"
])


# ============================================================
# 📖 TAB 1
# ============================================================

with tab1:


    st.html("""
    <div class="hero">

        <span class="hero-kicker">
            🌺 ॥ श्री गणेशाय नमः ॥ • SMART BAMS ASSISTANT
        </span>

        <div class="hero-title">
            🎯 A4 Handwritten Notes, redesigned.
        </div>

        <p class="hero-description">
            University-focused Ayurveda notes with clean hierarchy,
            exam-weightage, flowcharts, comparison tables,
            red-highlighted keywords and polished handwritten
            A4 output — designed specially for BAMS students.
        </p>

    </div>
    """)


    st.html("""
    <div class="section-title">
        🎓 Academic Setup
    </div>
    """)


    # --------------------------------------------------------
    # YEAR + SUBJECT
    # --------------------------------------------------------

    col1, col2 = st.columns(
        [1, 1.2]
    )


    with col1:

        bams_year = st.selectbox(

            "BAMS वर्ष / Academic Year",

            [
                "BAMS 1st Professional (प्रथम वर्ष)",
                "BAMS 2nd Professional (द्वितीय वर्ष)",
                "BAMS 3rd Professional (तृतीय वर्ष)",
                "BAMS Final Professional (अंतिम वर्ष)"
            ]
        )


    with col2:

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


    # --------------------------------------------------------
    # STUDY MODE + LANGUAGE
    # --------------------------------------------------------

    col3, col4 = st.columns(
        [1.2, 1]
    )


    with col3:

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


    with col4:

        language_preference = st.radio(

            "🌐 माध्यम / Language",

            [
                "मराठी (संस्कृत श्लोक + सोपा अर्थ + मॉडर्न टर्म्स)",
                "Simple Indian English + Sanskrit"
            ],

            horizontal=True
        )


    # --------------------------------------------------------
    # TOPIC
    # --------------------------------------------------------

    topic = st.text_input(

        "🔍 Topic / Question",

        placeholder=(
            "उदा. Pitta Dosha • Garavisha vs Dooshivisha • "
            "Ashwagandha • Pandu Roga"
        )
    )


    # --------------------------------------------------------
    # GENERATE BUTTON
    # --------------------------------------------------------

    generate_btn = st.button(

        "🚀  Generate Premium Study Notes",

        key="btn_notes",

        use_container_width=True
    )


    # ========================================================
    # GENERATE
    # ========================================================

    if generate_btn:


        if not topic.strip():

            st.warning(
                "⚠️ कृपया अभ्यासाचा विषय प्रविष्ट करा."
            )


        else:

            is_marathi = (
                "मराठी"
                in language_preference
            )


            # ==================================================
            # A4 MODE
            # ==================================================

            if "A4 Blue Ballpen" in study_mode:


                if is_marathi:

                    language_rule = """

LANGUAGE RULE:

Write in simple, natural Marathi.

Use authentic Sanskrit Ayurveda terminology.

Explain difficult concepts in easy Marathi.

Use English medical terms in brackets
where helpful.

"""

                else:

                    language_rule = """

LANGUAGE RULE:

Write 100% in English.

Use Roman Sanskrit transliteration.

DO NOT use Marathi or Devanagari.

Example:

Pitta Dosha

Ushna Guna

Tikshna Guna

Rakta Dhatu

Virechana

"""


                prompt = f"""

You are a senior Ayurveda Professor
and BAMS University Paper Setter.

Academic Year:
{bams_year}

Subject:
{subject}

Topic:
{topic}

Language:
{language_preference}

{language_rule}


TASK:

Create highly exam-oriented,
crisp one-page A4 handwritten notes.

Determine whether this topic is better
for 10 Marks LAQ or 5 Marks SAQ.

Use flowchart ONLY when genuinely useful.

Highlight important keywords using:

<span class="hl-red">keyword</span>


Return ONLY valid JSON.

JSON FORMAT:

{{
    "exam_marks": "10 Marks - LAQ",

    "main_heading": "Topic Heading",

    "include_flowchart": true,

    "flowchart_steps": [
        "Step 1",
        "Step 2",
        "Step 3",
        "Final"
    ],

    "entity_1": {{

        "title": "Concept 1",

        "definition": "Short definition",

        "key_points": [
            "Point 1",
            "Point 2",
            "Point 3"
        ],

        "exam_key": "Important exam concept"
    }},

    "entity_2": {{

        "title": "Concept 2",

        "definition": "Short definition",

        "key_points": [
            "Point 1",
            "Point 2",
            "Point 3"
        ],

        "exam_key": "Clinical or modern correlation"
    }},

    "comparison_table": [

        {{
            "feature": "Feature",
            "point_1": "Point",
            "point_2": "Point"
        }},

        {{
            "feature": "Clinical Signs",
            "point_1": "Point",
            "point_2": "Point"
        }},

        {{
            "feature": "Treatment",
            "point_1": "Point",
            "point_2": "Point"
        }}

    ],

    "exam_punch_line":
        "One memorable exam conclusion"
}}

"""


                with st.spinner(
                    "✍️ Premium A4 handwritten sheet तयार करत आहे..."
                ):


                    try:

                        raw = cached_ask_gemini(
                            prompt,
                            as_json=True
                        )


                        clean = raw.strip()


                        if clean.startswith(
                            "```json"
                        ):

                            clean = clean[7:]


                        if clean.startswith(
                            "```"
                        ):

                            clean = clean[3:]


                        if clean.endswith(
                            "```"
                        ):

                            clean = clean[:-3]


                        data = json.loads(
                            clean.strip()
                        )


                        st.success(
                            "✅ Premium A4 Sheet तयार झाली!"
                        )


                        st.components.v1.html(

                            create_a4_handwritten_doc(

                                data,

                                subject,

                                topic,

                                is_marathi=is_marathi
                            ),

                            height=1280,

                            scrolling=True
                        )


                    except Exception as error:

                        st.error(
                            f"❌ त्रुटी: {error}"
                        )


            # ==================================================
            # NORMAL NOTES
            # ==================================================

            else:


                prompt = f"""

You are a senior Ayurveda Acharya
according to NCISM academic standards.

Academic Level:
{bams_year}

Subject:
{subject}

Study Mode:
{study_mode}

Topic:
{topic}

Language:
{language_preference}


Create high-yield BAMS study material.

Strictly follow selected study mode.

Use:

• Clear headings
• Short paragraphs
• Exam-focused bullets
• Bold important terms
• Sanskrit transliteration
• Tables where useful
• Flowcharts where useful

If English is selected,
use English + Roman Sanskrit.

For Sanskrit shlokas,
use Markdown blockquotes.

Make the answer useful for university exams.
"""


                with st.spinner(
                    "⚡ AI exam-ready notes तयार करत आहे..."
                ):


                    try:

                        notes = cached_ask_gemini(
                            prompt,
                            as_json=False
                        )


                        st.success(
                            "✅ Premium Notes तयार झाल्या!"
                        )


                        st.markdown(
                            '<div class="result-card">',
                            unsafe_allow_html=True
                        )


                        st.markdown(
                            notes
                        )


                        st.markdown(
                            '</div>',
                            unsafe_allow_html=True
                        )


                    except Exception as error:

                        st.error(
                            f"❌ त्रुटी: {error}"
                        )


# ============================================================
# 🧪 TAB 2 — MEDICINE
# ============================================================

with tab2:


    st.html("""
    <div class="hero medicine-hero">

        <span class="hero-kicker">
            🌿 RASAUSHADHI VIDHI • FORMULATION LAB
        </span>

        <div class="hero-title">
            🧪 Medicine & Manufacturing Studio
        </div>

        <p class="hero-description">
            Ayurvedic formulation ingredients, Shodhana,
            preparation sequence, quality-control concepts
            and high-yield BAMS exam points — all in one place.
        </p>

    </div>
    """)


    st.html("""
    <div class="section-title">
        🧪 Formulation Setup
    </div>
    """)


    med_col1, med_col2 = st.columns(
        [1.2, 1]
    )


    with med_col1:

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


    with med_col2:

        medicine_language = st.radio(

            "🌐 भाषा / Language",

            [
                "Simple Indian English",
                "मराठी"
            ],

            horizontal=True,

            key="medicine_language"
        )


    medicine_name = st.text_input(

        "💊 औषधाचे नाव / Medicine Name",

        placeholder=(
            "उदा. Arogyavardhini Vati • "
            "Chandraprabha Vati • Triphala Churna"
        )
    )


    medicine_btn = st.button(

        "🔬  Generate Formulation & Manufacturing Guide",

        key="btn_medicine",

        use_container_width=True
    )


    if medicine_btn:


        if not medicine_name.strip():

            st.warning(
                "⚠️ कृपया औषधाचे नाव टाका."
            )


        else:


            medicine_prompt = f"""

You are a senior Ayurveda Professor.

Explain the following Ayurvedic formulation
for BAMS academic study.

Medicine:
{medicine_name}

Dosage Form:
{dosage_form}

Language:
{medicine_language}


Include:

1. Introduction

2. Classical therapeutic purpose

3. Ingredients table

4. Shodhana / purification if applicable

5. Manufacturing / preparation sequence

6. Important process points

7. Quality-control concepts

8. Important exam points

9. Classical dose and Anupana
   only as educational context

10. Important safety precautions


Clearly distinguish classical Ayurvedic
description from modern safety,
quality and regulatory practices.

Do not provide personalized medical advice.

Use clean headings and tables.
"""


            with st.spinner(
                f"🔬 {medicine_name} चे premium formulation notes तयार करत आहे..."
            ):


                try:

                    medicine_result = cached_ask_gemini(

                        medicine_prompt,

                        as_json=False
                    )


                    st.success(
                        "✅ Formulation Guide तयार झाला!"
                    )


                    st.markdown(
                        '<div class="result-card">',
                        unsafe_allow_html=True
                    )


                    st.markdown(
                        medicine_result
                    )


                    st.markdown(
                        '</div>',
                        unsafe_allow_html=True
                    )


                except Exception as error:

                    st.error(
                        f"❌ त्रुटी: {error}"
                    )


# ============================================================
# 🌺 FOOTER
# ============================================================

st.html("""
<div class="footer">

    <div class="footer-line"></div>

    🌺 ॥ गणपती बाप्पा मोरया ॥ 🌿

    <br><br>

    <strong>AyurVeda AI</strong>

    • BAMS Study Studio •

    Crafted with ❤️ by

    <strong>Avishkar Alase</strong>

</div>
""")
