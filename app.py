import streamlit as st
from google import genai
from google.genai import types
import json
import time
import html
import re


# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="AyurVeda AI | BAMS Study Studio",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="collapsed"
)


# =========================================================
# PREMIUM STREAMLIT CSS
# =========================================================

st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Kalam:wght@400;700&family=Mukta:wght@400;500;600;700;800&family=Plus+Jakarta+Sans:wght@500;600;700;800&display=swap');

html, body, .stApp {
    background:
        radial-gradient(
            circle at 50% 0%,
            #fffdf5 0%,
            #fff7df 28%,
            #fffaf2 62%,
            #f5faf7 100%
        ) !important;

    font-family: 'Mukta', sans-serif !important;
    color: #172554 !important;
}

.stApp * {
    font-family: 'Mukta', sans-serif;
}

#MainMenu {
    visibility: hidden;
}

footer {
    visibility: hidden;
}

header {
    background: transparent !important;
}


/* =====================================================
   PREMIUM NAVBAR
   ===================================================== */

.premium-navbar {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 15px;

    padding: 14px 18px;
    margin-bottom: 20px;

    border: 1px solid rgba(217,119,6,.20);
    border-radius: 22px;

    background: rgba(255,255,255,.86);
    backdrop-filter: blur(18px);
    -webkit-backdrop-filter: blur(18px);

    box-shadow:
        0 12px 35px rgba(146,64,14,.09);
}

.brand-left {
    display: flex;
    align-items: center;
    gap: 12px;
}

.brand-icon {
    width: 48px;
    height: 48px;

    display: flex;
    align-items: center;
    justify-content: center;

    border-radius: 15px;

    background: linear-gradient(
        135deg,
        #fff7ed,
        #fef3c7
    );

    border: 1px solid #fcd34d;

    font-size: 26px;

    box-shadow:
        0 7px 18px rgba(245,158,11,.15);
}

.brand-title {
    font-size: 22px;
    font-weight: 900;
    line-height: 1.1;
    color: #92400e !important;
}

.brand-sub {
    margin-top: 3px;
    font-size: 10.5px;
    font-weight: 800;
    letter-spacing: .4px;
    color: #b45309 !important;
}

.creator-pill {
    padding: 8px 14px;
    border-radius: 30px;

    background: #fff7ed;
    border: 1px solid #fed7aa;

    color: #92400e !important;

    font-size: 12px;
    font-weight: 800;
}


/* =====================================================
   HERO
   ===================================================== */

.hero {
    position: relative;
    overflow: hidden;

    padding: 25px 24px;
    margin-bottom: 20px;

    border-radius: 23px;

    background:
        linear-gradient(
            135deg,
            #7c2d12 0%,
            #c2410c 45%,
            #b45309 100%
        );

    border: 1px solid #fef08a;

    color: white !important;

    box-shadow:
        0 20px 45px rgba(154,52,18,.25);
}

.hero:after {
    content: "✦";
    position: absolute;
    right: 25px;
    top: 2px;

    font-size: 85px;
    opacity: .11;
}

.hero * {
    color: white !important;
}

.hero-kicker {
    display: inline-block;

    padding: 5px 12px;
    margin-bottom: 8px;

    border-radius: 30px;

    background: rgba(255,255,255,.16);
    border: 1px solid rgba(255,255,255,.28);

    font-size: 11px;
    font-weight: 800;
    letter-spacing: .5px;
}

.hero h2 {
    margin: 0 0 5px 0;
    font-size: 26px;
    font-weight: 900;
}

.hero p {
    margin: 0;
    font-size: 13.5px;
    line-height: 1.6;
}


/* =====================================================
   TABS
   ===================================================== */

.stTabs [data-baseweb="tab-list"] {
    gap: 9px;
    margin-bottom: 20px;
}

.stTabs [data-baseweb="tab"] {
    border: 1px solid #fed7aa;
    border-radius: 14px;

    padding: 9px 17px;

    background: rgba(255,255,255,.80);

    font-weight: 800;

    color: #78350f !important;
}

.stTabs [aria-selected="true"] {
    color: white !important;

    background:
        linear-gradient(
            135deg,
            #b45309,
            #ea580c
        ) !important;

    border-color: #ea580c !important;

    box-shadow:
        0 8px 20px rgba(234,88,12,.22);
}

.stTabs [aria-selected="true"] * {
    color: white !important;
}


/* =====================================================
   INPUTS
   ===================================================== */

div[data-baseweb="select"] > div,
div[data-baseweb="input"] > div,
div[data-baseweb="textarea"] > div {
    background: rgba(255,255,255,.94) !important;

    border: 1.5px solid #fed7aa !important;

    border-radius: 14px !important;

    box-shadow:
        0 3px 10px rgba(146,64,14,.05) !important;
}

div[data-baseweb="select"] > div:focus-within,
div[data-baseweb="input"] > div:focus-within {
    border-color: #f59e0b !important;

    box-shadow:
        0 0 0 3px rgba(245,158,11,.12) !important;
}

.stSelectbox label,
.stTextInput label,
.stRadio label {
    color: #713f12 !important;
    font-weight: 800 !important;
    font-size: 13px !important;
}


/* =====================================================
   BUTTON
   ===================================================== */

div.stButton > button {
    min-height: 50px;

    border: 0 !important;
    border-radius: 16px !important;

    color: white !important;

    background:
        linear-gradient(
            135deg,
            #b45309 0%,
            #ea580c 50%,
            #c2410c 100%
        ) !important;

    font-size: 16px !important;
    font-weight: 900 !important;

    box-shadow:
        0 12px 28px rgba(194,65,12,.25) !important;

    transition: all .22s ease !important;
}

div.stButton > button:hover {
    transform: translateY(-2px);

    box-shadow:
        0 17px 34px rgba(194,65,12,.35) !important;
}


/* =====================================================
   SETUP CARD
   ===================================================== */

.setup-card {
    padding: 15px 17px;
    margin-bottom: 17px;

    border-radius: 18px;

    background: rgba(255,255,255,.75);

    border: 1px solid #fde68a;

    box-shadow:
        0 7px 22px rgba(146,64,14,.06);
}

.setup-title {
    color: #92400e !important;
    font-size: 17px;
    font-weight: 900;
    margin-bottom: 4px;
}


/* =====================================================
   FOOTER
   ===================================================== */

.app-footer {
    margin-top: 40px;
    padding: 25px 10px;

    text-align: center;

    color: #92400e !important;

    font-size: 13px;
    font-weight: 700;

    border-top: 1px solid #fde68a;
}


/* =====================================================
   MOBILE
   ===================================================== */

@media (max-width: 700px) {

    .premium-navbar {
        padding: 12px;
    }

    .brand-title {
        font-size: 18px;
    }

    .brand-sub {
        font-size: 8px;
    }

    .creator-pill {
        font-size: 9px;
        padding: 6px 9px;
    }

    .hero {
        padding: 21px 18px;
    }

    .hero h2 {
        font-size: 21px;
    }

}

</style>
""", unsafe_allow_html=True)


# =========================================================
# API KEY
# =========================================================

api_key = st.secrets.get("GEMINI_API_KEY", "")

if not api_key:
    st.error(
        "⚠️ GEMINI_API_KEY सापडली नाही. "
        "Streamlit Secrets मध्ये GEMINI_API_KEY add करा."
    )
    st.stop()

client = genai.Client(api_key=api_key)


# =========================================================
# GEMINI FUNCTION
# =========================================================

@st.cache_data(show_spinner=False, ttl=86400)
def ask_gemini(prompt, as_json=False):

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
                time.sleep(3)

    raise RuntimeError(
        f"Gemini API Error: {last_error}"
    )


# =========================================================
# HTML HELPERS
# =========================================================

def escape_text(value):

    if value is None:
        return ""

    return html.escape(str(value))


def safe_ai_html(value):

    if value is None:
        return ""

    text = str(value)

    text = text.replace(
        "<span class='hl-red'>",
        "___HL_START___"
    )

    text = text.replace(
        '<span class="hl-red">',
        "___HL_START___"
    )

    text = text.replace(
        "</span>",
        "___HL_END___"
    )

    text = html.escape(text)

    text = text.replace(
        "___HL_START___",
        '<span class="hl-red">'
    )

    text = text.replace(
        "___HL_END___",
        "</span>"
    )

    return text


def clean_json(raw):

    text = raw.strip()

    text = re.sub(
        r"^```json\s*",
        "",
        text,
        flags=re.I
    )

    text = re.sub(
        r"^```\s*",
        "",
        text
    )

    text = re.sub(
        r"\s*```$",
        "",
        text
    )

    start = text.find("{")
    end = text.rfind("}")

    if start != -1 and end != -1:
        text = text[start:end + 1]

    return text.strip()


# =========================================================
# A4 SHEET GENERATOR
# =========================================================

def create_a4_sheet(
    data,
    subject_name,
    topic_name,
    is_marathi=True
):

    if is_marathi:

        definition_label = "व्याख्या (Definition)"
        points1_label = "परीक्षेसाठी महत्त्वाचे मुद्दे"
        points2_label = "लक्षणे व चिकित्सा"
        key1_label = "★ मुख्य संकल्पना"
        key2_label = "★ परीक्षेसाठी महत्त्वाचा मुद्दा"
        flow_label = "संप्राप्ती (Pathogenesis)"
        table_label = "★ परीक्षा तुलनात्मक तक्ता"
        punch_label = "✍️ परीक्षेसाठी मुख्य सूत्र"

    else:

        definition_label = "Definition"
        points1_label = "High-Yield Exam Points"
        points2_label = "Clinical Features & Treatment"
        key1_label = "★ Key Exam Concept"
        key2_label = "★ Important Exam Point"
        flow_label = "Pathogenesis / Flowchart"
        table_label = "★ Quick Exam Comparison"
        punch_label = "✍️ Exam Punch Line"


    title = data.get(
        "main_heading",
        topic_name
    )

    marks = data.get(
        "exam_marks",
        "१० गुण - दीर्घोत्तरी (LAQ)"
        if is_marathi
        else
        "10 Marks - LAQ"
    )

    e1 = data.get(
        "entity_1",
        {}
    )

    e2 = data.get(
        "entity_2",
        {}
    )


    # =====================================================
    # LEFT POINTS
    # =====================================================

    p1 = ""

    for point in e1.get(
        "key_points",
        []
    )[:6]:

        p1 += (
            "<li>"
            + safe_ai_html(point)
            + "</li>"
        )


    # =====================================================
    # RIGHT POINTS
    # =====================================================

    p2 = ""

    for point in e2.get(
        "key_points",
        []
    )[:6]:

        p2 += (
            "<li>"
            + safe_ai_html(point)
            + "</li>"
        )


    # =====================================================
    # FLOWCHART
    # =====================================================

    flow_html = ""

    steps = data.get(
        "flowchart_steps",
        []
    )[:4]


    if data.get(
        "include_flowchart",
        False
    ) and steps:

        flow_html += """
<div class="flow-section">

<div class="flow-title">
FLOW_LABEL
</div>
"""

        for i, step in enumerate(steps):

            if i == len(steps) - 1:

                flow_html += (
                    '<div class="flow-final">'
                    + safe_ai_html(step)
                    + '</div>'
                )

            else:

                flow_html += (
                    '<div class="flow-box">'
                    + safe_ai_html(step)
                    + '</div>'
                )

                flow_html += (
                    '<div class="flow-arrow">↓</div>'
                )

        flow_html += """
</div>
"""


    # =====================================================
    # TABLE
    # =====================================================

    table_html = ""

    rows = data.get(
        "comparison_table",
        []
    )[:3]


    if rows:

        table_html = """
<div class="table-section">

<div class="table-heading">
TABLE_LABEL
</div>

<table>

<thead>

<tr>

<th style="width:25%;">
मुद्दा / Feature
</th>

<th>
E1_TABLE_TITLE
</th>

<th>
E2_TABLE_TITLE
</th>

</tr>

</thead>

<tbody>
"""


        for row in rows:

            table_html += (
                "<tr>"
                "<td><b>"
                + safe_ai_html(
                    row.get(
                        "feature",
                        ""
                    )
                )
                + "</b></td>"
                "<td>"
                + safe_ai_html(
                    row.get(
                        "point_1",
                        ""
                    )
                )
                + "</td>"
                "<td>"
                + safe_ai_html(
                    row.get(
                        "point_2",
                        ""
                    )
                )
                + "</td>"
                "</tr>"
            )


        table_html += """
</tbody>

</table>

</div>
"""


    # =====================================================
    # COMPLETE HTML
    #
    # IMPORTANT:
    # This is NOT an f-string.
    # =====================================================

    document = """
<!DOCTYPE html>

<html>

<head>

<meta charset="UTF-8">

<meta
name="viewport"
content="width=device-width, initial-scale=1.0"
>

<script
src="https://cdnjs.cloudflare.com/ajax/libs/html2canvas/1.4.1/html2canvas.min.js">
</script>


<style>

@import url(
'https://fonts.googleapis.com/css2?family=Kalam:wght@400;700&family=Mukta:wght@400;500;600;700;800&display=swap'
);


* {
    box-sizing: border-box;
}


body {

    margin: 0;

    padding: 12px;

    background: #e8edf3;

    display: flex;

    flex-direction: column;

    align-items: center;

    font-family:
        'Kalam',
        'Mukta',
        cursive;
}


/* =====================================================
   ACTION BUTTONS
   ===================================================== */

.action-bar {

    display: flex;

    gap: 10px;

    margin-bottom: 13px;

    font-family: Arial, sans-serif;
}


.action-btn {

    border: none;

    border-radius: 11px;

    padding: 10px 17px;

    color: white;

    font-weight: 800;

    cursor: pointer;

    background:
        linear-gradient(
            135deg,
            #075985,
            #0284c7
        );

    box-shadow:
        0 7px 18px
        rgba(2,132,199,.25);
}


.action-btn.green {

    background:
        linear-gradient(
            135deg,
            #047857,
            #059669
        );
}


/* =====================================================
   TRUE A4
   ===================================================== */

.a4 {

    width: 794px;

    height: 1123px;

    position: relative;

    overflow: hidden;

    padding:
        23px 27px 18px;

    background: #fffefa;

    border:
        2px solid
        #19376d;

    color:
        #173b7a;

    box-shadow:
        0 18px 45px
        rgba(0,0,0,.18);

    font-size: 15px;

    line-height: 1.30;
}


/* subtle paper */

.a4:before {

    content: "";

    position: absolute;

    inset: 0;

    pointer-events: none;

    opacity: .065;

    background:
        repeating-linear-gradient(
            to bottom,
            transparent 0px,
            transparent 27px,
            #6682ad 28px
        );
}


/* =====================================================
   HEADER
   ===================================================== */

.header {

    position: relative;

    z-index: 5;

    display: flex;

    align-items: center;

    justify-content: space-between;

    gap: 12px;

    padding-bottom: 9px;

    margin-bottom: 9px;

    border-bottom:
        2px solid
        #19376d;
}


.title-box {

    width: 69%;

    padding: 7px 12px;

    border:
        2px solid
        #19376d;

    border-radius: 11px;

    background: #fff;

    text-align: center;

    font-size: 21px;

    font-weight: 700;
}


.title-box span {

    border-bottom:
        2px double
        #19376d;
}


.marks-box {

    width: 27%;

    padding: 5px 6px;

    border:
        2px solid
        #19376d;

    border-radius: 9px;

    text-align: center;

    background: #fff;

    font-size: 12px;

    font-weight: 700;
}


/* =====================================================
   RED / PINK HIGHLIGHT
   ===================================================== */

.hl-red {

    display: inline;

    padding: 0 4px;

    border-radius: 4px;

    background:
        #ffdce3;

    color:
        #a91d32;

    font-weight: 700;
}


/* =====================================================
   MAIN TWO COLUMNS
   ===================================================== */

.main-grid {

    position: relative;

    z-index: 3;

    display: grid;

    grid-template-columns:
        1fr 1fr;

    gap: 18px;
}


.left-column {

    padding-right: 13px;

    border-right:
        1.5px dashed
        #19376d;
}


.right-column {

    padding-left: 2px;
}


/* =====================================================
   CONCEPT HEADING
   ===================================================== */

.concept-heading {

    display: block;

    width: 100%;

    padding: 4px 9px;

    margin: 0 0 5px;

    border:
        1.6px solid
        #19376d;

    border-radius: 15px;

    background:
        rgba(255,255,255,.97);

    font-size: 15px;

    font-weight: 700;

    line-height: 1.25;
}


/* =====================================================
   DEFINITION
   ===================================================== */

.definition {

    font-size: 13.1px;

    line-height: 1.35;

    margin:
        2px 0 6px;
}


/* =====================================================
   SECTION HEADING
   ===================================================== */

.section-heading {

    margin:
        5px 0 3px;

    font-size:
        15px;

    font-weight:
        700;

    text-decoration:
        underline;

    text-decoration-color:
        #dc5368;

    text-decoration-thickness:
        2px;

    text-underline-offset:
        3px;
}


/* =====================================================
   BULLET POINTS
   ===================================================== */

ul {

    margin:
        2px 0 6px;

    padding-left:
        18px;
}


li {

    margin-bottom:
        3px;

    font-size:
        13.15px;

    line-height:
        1.33;
}


/* =====================================================
   KEY CONCEPT BOX
   ===================================================== */

.key-box {

    padding:
        6px 9px;

    margin:
        7px 0;

    border:
        1.5px dashed
        #19376d;

    border-radius:
        9px;

    background:
        rgba(255,255,255,.92);

    font-size:
        12.2px;

    line-height:
        1.35;
}


/* =====================================================
   FLOWCHART
   ===================================================== */

.flow-section {

    text-align:
        center;

    margin:
        8px 0 8px;
}


.flow-title {

    display:
        inline-block;

    padding:
        2px 11px;

    margin-bottom:
        5px;

    border:
        1.5px solid
        #19376d;

    border-radius:
        12px;

    background:
        #fff;

    font-weight:
        700;

    font-size:
        13.5px;
}


.flow-box {

    width:
        82%;

    margin:
        0 auto;

    padding:
        4px 7px;

    border:
        1.5px solid
        #19376d;

    border-radius:
        8px;

    background:
        #fff;

    font-size:
        12.4px;

    line-height:
        1.25;
}


.flow-arrow {

    height:
        15px;

    line-height:
        15px;

    font-size:
        17px;

    font-weight:
        700;
}


.flow-final {

    width:
        88%;

    margin:
        0 auto;

    padding:
        5px 8px;

    border:
        2px dashed
        #19376d;

    border-radius:
        13px;

    background:
        #fff0f3;

    font-size:
        12.4px;

    font-weight:
        700;

    line-height:
        1.25;
}


/* =====================================================
   TABLE
   ===================================================== */

.table-section {

    position:
        relative;

    z-index:
        4;

    margin-top:
        6px;
}


.table-heading {

    margin:
        6px 0 3px;

    font-size:
        14px;

    font-weight:
        700;

    text-decoration:
        underline;

    text-decoration-color:
        #dc5368;
}


table {

    width:
        100%;

    border-collapse:
        collapse;

    background:
        rgba(255,255,255,.96);

    font-size:
        11.2px;
}


th,
td {

    border:
        1.2px solid
        #19376d;

    padding:
        4px 5px;

    text-align:
        left;

    vertical-align:
        top;
}


th {

    background:
        #fff3dc;

    font-weight:
        700;
}


/* =====================================================
   PUNCH LINE
   ===================================================== */

.punch {

    position:
        absolute;

    z-index:
        5;

    left:
        27px;

    right:
        27px;

    bottom:
        46px;

    padding:
        8px 10px;

    border-top:
        2px solid
        #19376d;

    background:
        rgba(255,255,255,.94);

    font-size:
        13.5px;

    font-weight:
        700;
}


.punch-text {

    margin-top:
        3px;

    text-decoration:
        underline;

    text-decoration-color:
        #dc5368;

    text-decoration-thickness:
        1.5px;
}


/* =====================================================
   FOOTER
   ===================================================== */

.paper-footer {

    position:
        absolute;

    z-index:
        6;

    right:
        18px;

    bottom:
        13px;

    font-family:
        Arial,
        sans-serif;

    font-size:
        9px;

    color:
        #31558e;

    opacity:
        .90;
}


/* =====================================================
   PRINT
   ===================================================== */

@media print {

    body {

        padding:
            0;

        background:
            white;
    }

    .action-bar {

        display:
            none !important;
    }

    .a4 {

        border:
            none;

        box-shadow:
            none;
    }
}

</style>

</head>


<body>


<!-- ACTION BUTTONS -->

<div class="action-bar">

<button
class="action-btn"
onclick="downloadPNG()">

📸 Save A4 PNG

</button>


<button
class="action-btn green"
onclick="window.print()">

📄 Print / Save PDF

</button>

</div>


<!-- ===================================================
     A4 PAPER
     =================================================== -->

<div
class="a4"
id="a4Canvas">


<!-- HEADER -->

<div class="header">

<div class="title-box">

<span>
TITLE
</span>

</div>


<div class="marks-box">

SUBJECT

<br>

<span class="hl-red">
🎯 MARKS
</span>

</div>

</div>


<!-- TWO COLUMNS -->

<div class="main-grid">


<!-- LEFT COLUMN -->

<div class="left-column">


<div class="concept-heading">
① E1_TITLE
</div>


<div class="definition">

<b>
DEFINITION_LABEL:
</b>

E1_DEFINITION

</div>


<div class="section-heading">

POINTS1_LABEL

</div>


<ul>

E1_POINTS

</ul>


<div class="key-box">

<b>
KEY1_LABEL
</b>

<br>

E1_KEY

</div>


</div>


<!-- RIGHT COLUMN -->

<div class="right-column">


<div class="concept-heading">

② E2_TITLE

</div>


<div class="definition">

<b>
DEFINITION_LABEL:
</b>

E2_DEFINITION

</div>


<div class="section-heading">

POINTS2_LABEL

</div>


<ul>

E2_POINTS

</ul>


<div class="key-box">

<b>
KEY2_LABEL
</b>

<br>

E2_KEY

</div>


FLOWCHART


</div>


</div>


TABLE


<!-- EXAM PUNCH -->

<div class="punch">

PUNCH_LABEL →

<div class="punch-text">

"EXAM_PUNCH"

</div>

</div>


<!-- FOOTER -->

<div class="paper-footer">

🌿 AyurVeda AI
&nbsp;•&nbsp;
BAMS Study Studio
&nbsp;•&nbsp;
By Avishkar Alase

</div>


</div>


<script>

function downloadPNG() {

    const element =
        document.getElementById(
            "a4Canvas"
        );

    html2canvas(
        element,
        {
            scale: 2.5,

            useCORS: true,

            backgroundColor:
                "#fffefa",

            logging: false
        }
    ).then(
        function(canvas) {

            const link =
                document.createElement(
                    "a"
                );

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


    # =====================================================
    # REPLACE PLACEHOLDERS
    # =====================================================

    replacements = {

        "TITLE":
            escape_text(title),

        "SUBJECT":
            escape_text(subject_name),

        "MARKS":
            escape_text(marks),

        "E1_TITLE":
            safe_ai_html(
                e1.get(
                    "title",
                    "Core Concept"
                )
            ),

        "E2_TITLE":
            safe_ai_html(
                e2.get(
                    "title",
                    "Lakshana & Chikitsa"
                )
            ),

        "DEFINITION_LABEL":
            definition_label,

        "E1_DEFINITION":
            safe_ai_html(
                e1.get(
                    "definition",
                    ""
                )
            ),

        "E2_DEFINITION":
            safe_ai_html(
                e2.get(
                    "definition",
                    ""
                )
            ),

        "POINTS1_LABEL":
            points1_label,

        "POINTS2_LABEL":
            points2_label,

        "E1_POINTS":
            p1,

        "E2_POINTS":
            p2,

        "KEY1_LABEL":
            key1_label,

        "KEY2_LABEL":
            key2_label,

        "E1_KEY":
            safe_ai_html(
                e1.get(
                    "exam_key",
                    ""
                )
            ),

        "E2_KEY":
            safe_ai_html(
                e2.get(
                    "exam_key",
                    ""
                )
            ),

        "FLOWCHART":
            flow_html,

        "TABLE":
            table_html,

        "TABLE_LABEL":
            table_label,

        "E1_TABLE_TITLE":
            safe_ai_html(
                e1.get(
                    "title",
                    "Concept 1"
                )
            ),

        "E2_TABLE_TITLE":
            safe_ai_html(
                e2.get(
                    "title",
                    "Concept 2"
                )
            ),

        "PUNCH_LABEL":
            punch_label,

        "EXAM_PUNCH":
            safe_ai_html(
                data.get(
                    "exam_punch_line",
                    ""
                )
            )
    }


    for key, value in replacements.items():

        document = document.replace(
            key,
            value
        )


    return document


# =========================================================
# NAVBAR
# =========================================================

st.markdown("""
<div class="premium-navbar">

<div class="brand-left">

<div class="brand-icon">
🌿
</div>

<div>

<div class="brand-title">
AyurVeda AI
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
""", unsafe_allow_html=True)


# =========================================================
# TABS
# =========================================================

tab1, tab2 = st.tabs(
    [
        "📚 BAMS Study Studio",
        "🧪 Medicine & Manufacturing"
    ]
)


# =========================================================
# TAB 1
# =========================================================

with tab1:

    st.markdown("""
<div class="hero">

<div class="hero-kicker">
🌺 ॥ श्री गणेशाय नमः ॥ • SMART BAMS ASSISTANT
</div>

<h2>
🎯 A4 Handwritten Exam Notes
</h2>

<p>
University-focused Ayurveda notes with clean
exam hierarchy, high-yield points, important
keywords, flowcharts and premium A4 output.
</p>

</div>
""", unsafe_allow_html=True)


    st.markdown("""
<div class="setup-card">

<div class="setup-title">
🎓 Academic Setup
</div>

<div>
BAMS year, subject, language आणि topic निवडा.
AI फक्त examination मध्ये आवश्यक असलेले
high-yield points तयार करेल.
</div>

</div>
""", unsafe_allow_html=True)


    # =====================================================
    # ACADEMIC YEAR / SUBJECT
    # =====================================================

    col1, col2 = st.columns(
        [1, 1.2]
    )


    with col1:

        bams_year = st.selectbox(
            "🎓 BAMS वर्ष / Academic Year",
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


    # =====================================================
    # MODE / LANGUAGE
    # =====================================================

    col3, col4 = st.columns(
        [1.2, 1]
    )


    with col3:

        study_mode = st.selectbox(
            "🎯 अभ्यासाचा प्रकार / Study Mode",
            [
                "📋 A4 Blue Ballpen Handwritten Sheet",
                "📖 Comprehensive Notes",
                "📜 Only Shlokas & Meanings",
                "📝 10-Mark LAQ Answer",
                "⚡ Quick Revision / Viva"
            ]
        )


    with col4:

        language_preference = st.radio(
            "🌐 माध्यम / Language",
            [
                "मराठी (संस्कृत + सोपा अर्थ + Modern Terms)",
                "Simple Indian English + Sanskrit"
            ],
            horizontal=True
        )


    # =====================================================
    # TOPIC
    # =====================================================

    topic = st.text_input(
        "🔍 अभ्यासाचा विषय / प्रश्न",
        placeholder=
        "उदा. Pitta Dosha, Garavisha vs Dooshivisha, Ashwagandha"
    )


    # =====================================================
    # GENERATE BUTTON
    # =====================================================

    generate_button = st.button(
        "🚀 Premium Exam Notes तयार करा",
        key="generate_notes",
        use_container_width=True
    )


    # =====================================================
    # GENERATE
    # =====================================================

    if generate_button:

        if not topic.strip():

            st.warning(
                "⚠️ कृपया अभ्यासाचा विषय टाका."
            )

        else:

            is_marathi = (
                "मराठी"
                in language_preference
            )


            # =================================================
            # A4 HANDWRITTEN MODE
            # =================================================

            if "A4 Blue Ballpen" in study_mode:


                if is_marathi:

                    language_rule = """
MARATHI MODE:

Write in simple, natural Maharashtra Marathi.

Use authentic Ayurveda Sanskrit terminology.

Use English terminology in brackets only when useful.

Avoid difficult literary Marathi.

The answer should look like a BAMS student
writing a university examination answer.
"""

                    marks_example = (
                        "१० गुण - दीर्घोत्तरी (LAQ)"
                    )

                else:

                    language_rule = """
ENGLISH MODE:

Use 100% English with Roman Sanskrit.

DO NOT use Marathi.

DO NOT use Devanagari.

Sanskrit terms must be Roman transliteration.

Examples:
Pitta Dosha
Ushna
Tikshna
Virechana
Rakta Dhatu
"""

                    marks_example = (
                        "10 Marks - LAQ"
                    )


                # =================================================
                # EXAM CONTENT PROMPT
                # =================================================

                prompt = f"""

You are a senior BAMS Ayurveda Professor,
University Paper Setter and Examination Mentor.

ACADEMIC YEAR:
{bams_year}

SUBJECT:
{subject}

TOPIC:
{topic}

LANGUAGE:
{language_preference}


{language_rule}


=========================================================
MOST IMPORTANT REQUIREMENT
=========================================================

Create ONE SINGLE A4 UNIVERSITY EXAM REVISION SHEET.

The student DOES NOT want textbook notes.

The student wants ONLY the answer content
actually required to score marks.

Think like a university paper setter.

Keep the answer SHORT, PRECISE,
HIGH-YIELD and EXAM-ORIENTED.


=========================================================
MARKS
=========================================================

Determine whether the topic is normally suitable
for a 5-mark SAQ or 10-mark LAQ.

For 5 marks:

Definition
+
4-6 important points
+
essential Lakshana / Chikitsa
+
one exam conclusion.

For 10 marks:

Definition
+
Nidana
+
Samprapti if relevant
+
Lakshana
+
Types if important
+
Chikitsa
+
important drugs if relevant
+
flowchart if useful
+
exam conclusion.


=========================================================
DO NOT ADD
=========================================================

Do NOT add:

- Long introduction
- History
- Repeated information
- Unnecessary explanation
- Irrelevant modern medicine
- Long paragraphs
- Low-yield textbook details


=========================================================
A4 SPACE LIMIT
=========================================================

The answer MUST comfortably fit ONE A4 page.

Maximum:

Entity 1 = 6 bullet points

Entity 2 = 6 bullet points

Flowchart = maximum 4 steps

Comparison table = maximum 3 rows


=========================================================
HIGHLIGHT
=========================================================

Highlight ONLY crucial keywords.

Use exactly:

<span class="hl-red">KEYWORD</span>

Examples:

<span class="hl-red">Ushna</span>

<span class="hl-red">Daha</span>

<span class="hl-red">Virechana</span>

<span class="hl-red">Pachaka Pitta</span>


DO NOT highlight entire sentences.


=========================================================
FLOWCHART
=========================================================

Use a flowchart only when genuinely useful.

Examples:

Samprapti
Pathogenesis
Disease stages
Mechanism
Sequence

Maximum 4 steps.

If unnecessary:

include_flowchart = false

flowchart_steps = []


=========================================================
COMPARISON TABLE
=========================================================

Use comparison table ONLY if useful.

Maximum 3 rows.

Otherwise:

comparison_table = []


=========================================================
JSON ONLY
=========================================================

Return ONLY valid JSON.

NO markdown.

NO ```json.

NO explanation outside JSON.

Use this exact schema:

{{
    "exam_marks":
        "{marks_example}",

    "main_heading":
        "Short Exam Topic Heading",

    "include_flowchart":
        false,

    "flowchart_steps":
        [],

    "entity_1":
    {{
        "title":
            "Core Concept",

        "definition":
            "Short 1-2 line exam definition.",

        "key_points":
        [
            "Important exam point",
            "Important exam point",
            "Important exam point",
            "Important exam point",
            "Important exam point"
        ],

        "exam_key":
            "One high-yield exam concept."
    }},

    "entity_2":
    {{
        "title":
            "Lakshana & Chikitsa",

        "definition":
            "Short definition if required.",

        "key_points":
        [
            "Important Lakshana",
            "Important Lakshana",
            "Important Chikitsa",
            "Important treatment",
            "Important drug"
        ],

        "exam_key":
            "One important exam point."
    }},

    "comparison_table":
    [],

    "exam_punch_line":
        "One memorable final sentence for examination."
}}


FINAL PRINCIPLE:

LESS CONTENT + MORE MARKS.

Make it look like a topper's
last-minute university revision sheet.
"""


                # =================================================
                # GEMINI
                # =================================================

                with st.spinner(
                    "✍️ Premium A4 handwritten exam sheet तयार होत आहे..."
                ):

                    try:

                        raw = ask_gemini(
                            prompt,
                            as_json=True
                        )

                        clean = clean_json(
                            raw
                        )

                        data = json.loads(
                            clean
                        )


                        # =================================================
                        # CREATE A4
                        # =================================================

                        sheet = create_a4_sheet(
                            data,
                            subject,
                            topic,
                            is_marathi
                        )


                        st.success(
                            "✅ Premium A4 Exam Sheet तयार झाली!"
                        )


                        st.components.v1.html(
                            sheet,
                            height=1180,
                            scrolling=True
                        )


                    except Exception as error:

                        st.error(
                            f"❌ A4 generation error: {error}"
                        )


            # =================================================
            # NORMAL NOTES MODES
            # =================================================

            else:

                if is_marathi:

                    language_instruction = """
Write in simple Maharashtra Marathi.
Use Sanskrit Ayurveda terminology.
Use English terms in brackets where useful.
"""

                else:

                    language_instruction = """
Write 100% English.
Use Roman Sanskrit transliteration.
Do not use Marathi or Devanagari.
"""


                normal_prompt = f"""

You are a senior BAMS Ayurveda Professor.

Academic Year:
{bams_year}

Subject:
{subject}

Topic:
{topic}

Study Mode:
{study_mode}

Language:
{language_preference}

{language_instruction}


Create high-yield BAMS examination material.

Strictly follow the selected study mode.

Avoid unnecessary textbook information.

Use bold for important terms.

Keep explanations clear and examination-oriented.
"""


                with st.spinner(
                    "⚡ AI BAMS notes तयार करत आहे..."
                ):

                    try:

                        result = ask_gemini(
                            normal_prompt,
                            as_json=False
                        )

                        st.success(
                            "✅ Notes तयार झाल्या!"
                        )

                        st.markdown(
                            result
                        )

                    except Exception as error:

                        st.error(
                            f"❌ Error: {error}"
                        )


# =========================================================
# TAB 2 - MEDICINE
# =========================================================

with tab2:

    st.markdown("""
<div class="hero"
style="
background:
linear-gradient(
135deg,
#064e3b,
#0f766e,
#0d9488
);
border-color:#5eead4;
">

<div class="hero-kicker">
🌿 RASASHASTRA • BHAISHAJYA KALPANA
</div>

<h2>
🧪 Medicine & Manufacturing Studio
</h2>

<p>
Ayurvedic formulations, ingredients,
Shodhana and manufacturing concepts
in simple BAMS examination language.
</p>

</div>
""", unsafe_allow_html=True)


    m1, m2 = st.columns(
        [1.2, 1]
    )


    with m1:

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


    with m2:

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
        placeholder=
        "उदा. Arogyavardhini Vati / Chandraprabha Vati"
    )


    medicine_button = st.button(
        "🔬 औषध घटक व निर्माण विधी तयार करा",
        key="medicine_button",
        use_container_width=True
    )


    if medicine_button:

        if not medicine_name.strip():

            st.warning(
                "⚠️ कृपया औषधाचे नाव टाका."
            )

        else:

            medicine_prompt = f"""

You are a senior BAMS Ayurveda Professor
specialized in Rasashastra and Bhaishajya Kalpana.

Medicine:
{medicine_name}

Dosage Form:
{dosage_form}

Language:
{medicine_language}


Explain the formulation for BAMS examination.

Include:

1. Introduction
2. Ingredients
3. Standard quantity only when confidently known
4. Shodhana if applicable
5. Bhavana if applicable
6. Classical preparation concept
7. Important precautions
8. Storage
9. Dose only where appropriate
10. Important exam points


Do NOT invent classical quantities.

If classical references differ,
mention that formulations can vary by reference.

For potentially hazardous mineral or metal preparations,
keep the explanation academic and safety-conscious.

Use simple examination-friendly language.
"""


            with st.spinner(
                f"🔬 {medicine_name} ची माहिती तयार होत आहे..."
            ):

                try:

                    medicine_result = ask_gemini(
                        medicine_prompt,
                        as_json=False
                    )

                    st.success(
                        "✅ Medicine information तयार झाली!"
                    )

                    st.markdown(
                        medicine_result
                    )

                except Exception as error:

                    st.error(
                        f"❌ Error: {error}"
                    )


# =========================================================
# FOOTER
# =========================================================

st.markdown("""
<div class="app-footer">

🌺 ॥ गणपती बाप्पा मोरया ॥ 🌺

<br>

🌿 <strong>AyurVeda AI</strong>
&nbsp;•&nbsp;
BAMS Study Studio

<br>

✦ Developed by
<strong>Avishkar Alase</strong>

</div>
""", unsafe_allow_html=True)
